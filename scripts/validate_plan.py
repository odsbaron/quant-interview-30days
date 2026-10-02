#!/usr/bin/env python3
"""Validate schedules, public readers, links and integrity without doing exercises."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from datetime import date, timedelta
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLAN_FIELDS = {
    "day", "date", "phase", "topic", "review_minutes", "learn_minutes",
    "practice_minutes", "record_minutes", "resource_ids", "task", "acceptance", "artifact",
}
RESOURCE_FIELDS = {"id", "title", "relative_path", "kind", "usage", "scope_note", "public_path"}
PROGRESS_FIELDS = {"day", "date", "status", "actual_minutes", "result", "help_used", "review_date", "artifact", "updated_at"}
LOG_FIELDS = {"timestamp", "day", "status", "minutes", "result", "help_used", "review_date", "summary"}
MINUTE_FIELDS = ("review_minutes", "learn_minutes", "practice_minutes", "record_minutes")


def rows(path: Path, required: set[str], errors: list[str]) -> list[dict[str, str]]:
    """Reject malformed CSV explicitly before records reach semantic checks."""
    parsed: list[dict[str, str]] = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            header = next(reader, None)
            if not header:
                errors.append(f"{path.name} CSV 缺少表头。")
                return parsed
            if len(set(header)) != len(header):
                errors.append(f"{path.name} CSV 表头重复。")
                return parsed
            missing = required - set(header)
            if missing:
                errors.append(f"{path.name} CSV 缺少必需列：{', '.join(sorted(missing))}。")
                return parsed
            for values in reader:
                if not values:
                    continue
                if len(values) != len(header):
                    errors.append(f"{path.name} CSV 第 {reader.line_num} 行列宽异常：{len(values)}，预期 {len(header)}。")
                    continue
                parsed.append(dict(zip(header, values)))
    except (OSError, UnicodeError, csv.Error) as error:
        errors.append(f"{path.name} CSV 无法读取：{error}")
    return parsed


def integer(value: str, label: str, errors: list[str]) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        errors.append(f"{label} 必须为整数。")
        return None


def relative_file(root: Path, value: str, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} 路径不能为空。")
        return None
    relative = Path(value)
    if relative.is_absolute() or PureWindowsPath(value).is_absolute() or ".." in relative.parts:
        errors.append(f"{label} 必须使用不含 .. 的相对路径。")
        return None
    candidate = root / relative
    if not candidate.resolve().is_relative_to(root.resolve()):
        errors.append(f"{label} 路径越出仓库范围。")
        return None
    return candidate


def without_code_fences(content: str) -> str:
    output: list[str] = []
    fence_character = ""
    fence_length = 0
    for line in content.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence_character:
            if marker and marker.group(1)[0] == fence_character and len(marker.group(1)) >= fence_length and not marker.group(2).strip():
                fence_character = ""
            output.append("\n")
        elif marker:
            fence_character = marker.group(1)[0]
            fence_length = len(marker.group(1))
            output.append("\n")
        else:
            output.append(line)
    return "".join(output)


def markdown_targets(content: str) -> list[str]:
    """Read inline destinations, including <paths with spaces> and parentheses."""
    targets: list[str] = []
    for match in re.finditer(r"!?\[[^\]\n]*\]\(\s*", content):
        start = match.end()
        if start >= len(content):
            continue
        if content[start] == "<":
            end = content.find(">", start + 1)
            if end >= 0 and "\n" not in content[start:end]:
                targets.append(content[start + 1:end])
            continue
        end = start
        depth = 0
        while end < len(content):
            character = content[end]
            if character == "\\" and end + 1 < len(content):
                end += 2
                continue
            if character == "(":
                depth += 1
            elif character == ")":
                if depth == 0:
                    break
                depth -= 1
            elif character.isspace():
                break
            end += 1
        if end > start:
            targets.append(re.sub(r"\\([\\()])", r"\1", content[start:end]))
    for match in re.finditer(r"^ {0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))", content, re.MULTILINE):
        targets.append(match.group(1) or match.group(2))
    return targets


def markdown_anchors(content: str) -> set[str]:
    content = without_code_fences(content)
    anchors = set(re.findall(r"\bid\s*=\s*[\"']([^\"']+)[\"']", content))
    anchors.update(re.findall(r"<a\b[^>]*\bname\s*=\s*[\"']([^\"']+)[\"']", content, re.IGNORECASE))
    headings = re.findall(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", content, re.MULTILINE)
    headings.extend(re.findall(r"^([^\n]+)\n {0,3}(?:=+|-+)\s*$", content, re.MULTILINE))
    used: set[str] = set()
    for heading in headings:
        heading = re.sub(r"<[^>]+>", "", heading).lower()
        heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        base = "".join(character for character in heading if character in "-_" or character.isspace() or unicodedata.category(character)[0] in "LMN")
        base = re.sub(r"\s", "-", base)
        slug = base
        suffix = 0
        while slug in used:
            suffix += 1
            slug = f"{base}-{suffix}"
        used.add(slug)
        anchors.add(slug)
    return anchors


def validate_links(root: Path, errors: list[str]) -> None:
    anchor_cache: dict[Path, set[str]] = {}
    for document in root.rglob("*.md"):
        if ".git" in document.parts:
            continue
        content = without_code_fences(document.read_text(encoding="utf-8"))
        for target in markdown_targets(content):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            filename = unquote(parsed.path)
            if filename.startswith("/") or PureWindowsPath(filename).is_absolute():
                errors.append(f"{document.relative_to(root)} 包含机器绝对文件链接。")
                continue
            path = (document.parent / filename).resolve() if filename else document.resolve()
            if not path.is_relative_to(root.resolve()):
                errors.append(f"{document.relative_to(root)} 链接越出仓库：{filename}")
                continue
            if not path.exists():
                errors.append(f"{document.relative_to(root)} 引用不存在的文件：{filename}")
                continue
            if parsed.fragment and path.is_file() and path.suffix.lower() in {".md", ".html", ".htm"}:
                if path not in anchor_cache:
                    anchor_cache[path] = markdown_anchors(path.read_text(encoding="utf-8"))
                fragment = unquote(parsed.fragment)
                if fragment not in anchor_cache[path]:
                    errors.append(f"{document.relative_to(root)} 引用不存在的锚点：{target}")


def validate_manifest(root: Path, errors: list[str]) -> None:
    manifest_path = root / "resources/publish_manifest.json"
    if not manifest_path.exists():
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        errors.append(f"publish_manifest.json 无法读取：{error}")
        return
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        errors.append("publish_manifest.json 版本必须为 1。")
        return
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        errors.append("publish_manifest.json 缺少 files 文件清单。")
        return
    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict) or not {"path", "bytes", "sha256"} <= entry.keys():
            errors.append("publish_manifest.json 文件条目缺少 path、bytes 或 sha256。")
            continue
        value = entry["path"]
        path = relative_file(root, value, "发布清单文件", errors)
        if path is None:
            continue
        if value in seen:
            errors.append(f"发布清单文件重复：{value}")
        seen.add(value)
        if not path.is_file():
            errors.append(f"发布清单文件不存在：{value}")
            continue
        content = path.read_bytes()
        if type(entry["bytes"]) is not int or entry["bytes"] != len(content):
            errors.append(f"发布清单大小不一致：{value}")
        if not isinstance(entry["sha256"], str) or entry["sha256"] != hashlib.sha256(content).hexdigest():
            errors.append(f"发布清单 SHA256 不一致：{value}")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    start = date.fromisoformat(config["start_date"])
    if config["daily_budget_minutes"] != 60:
        errors.append("本计划每日预算必须为 60 分钟，总预算为 1800 分钟。")
    plan = rows(root / "plan/30_days.csv", PLAN_FIELDS, errors)
    resources = rows(root / "resources/materials.csv", RESOURCE_FIELDS, errors)
    progress = rows(root / "progress/progress.csv", PROGRESS_FIELDS, errors)
    if (root / "progress/log.csv").exists():
        rows(root / "progress/log.csv", LOG_FIELDS, errors)
    resource_ids = {row["id"] for row in resources}
    if len(resource_ids) != len(resources) or "" in resource_ids:
        errors.append("材料 ID 重复或为空。")
    plan_days = [integer(row["day"], "计划学习日", errors) for row in plan]
    if len(plan) != 30 or plan_days != list(range(1, 31)):
        errors.append("计划必须按顺序包含 Day 1 到 Day 30，且无重复。")
    minute_rows = [[integer(row[key], f"Day {row['day']} {key}", errors) for key in MINUTE_FIELDS] for row in plan]
    if any(value is None for values in minute_rows for value in values) or sum(value for values in minute_rows for value in values if value is not None) != 1800:
        errors.append("30 天总预算必须为 1800 分钟。")
    resource_anchors = markdown_anchors((root / "resources/README.md").read_text(encoding="utf-8"))
    for row in resources:
        relative_file(root, row["relative_path"], f"材料 {row['id']} relative_path", errors)
        public = relative_file(root, row["public_path"], f"材料 {row['id']} public_path", errors)
        if public is not None and (not public.is_file() or public.stat().st_size < 250 or not public.read_text(encoding="utf-8").strip()):
            errors.append(f"材料 {row['id']} public_path 缺少完整公开正文（至少 250 字节）。")
        if row["id"] not in resource_anchors:
            errors.append(f"材料 {row['id']} 缺少导航锚点。")
    for row, day, minutes in zip(plan, plan_days, minute_rows):
        if day is None or not 1 <= day <= 30:
            errors.append(f"学习日 {row['day']} 超出 1 到 30 范围。")
            continue
        expected_date = (start + timedelta(days=day - 1)).isoformat()
        if row["date"] != expected_date:
            errors.append(f"Day {day:02d} 日期不连续。")
        if any(value is None or value < 0 for value in minutes) or sum(value for value in minutes if value is not None) != 60:
            errors.append(f"Day {day:02d} 时间预算不是 60 分钟。")
        refs = {value.strip() for value in row["resource_ids"].split(";") if value.strip()}
        if not refs or not refs <= resource_ids:
            errors.append(f"Day {day:02d} 材料 ID 不存在或为空。")
        for key in ("phase", "topic", "task", "acceptance"):
            if not row[key].strip():
                errors.append(f"Day {day:02d} 缺少 {key}。")
        if row["artifact"] != f"notes/day{day:02d}.md":
            errors.append(f"Day {day:02d} 笔记路径不符合约定。")
        daily = root / f"days/day{day:02d}.md"
        if not daily.is_file() or daily.stat().st_size < 250:
            errors.append(f"Day {day:02d} 缺少完整任务文档。")
        elif row["date"] not in daily.read_text(encoding="utf-8"):
            errors.append(f"Day {day:02d} 文档日期与计划不一致。")
        artifact = relative_file(root, row["artifact"], f"Day {day:02d} 笔记", errors)
        if artifact is not None and not artifact.is_file():
            errors.append(f"Day {day:02d} 笔记模板尚未创建。")
    progress_days = [integer(row["day"], "进度学习日", errors) for row in progress]
    if len(progress) != 30 or progress_days != list(range(1, 31)):
        errors.append("进度表须包含 30 个不重复学习日。")
    valid_statuses = {"not_started", "in_progress", "needs_review", "completed"}
    plan_map = dict(zip(plan_days, plan))
    for row, day in zip(progress, progress_days):
        reference = plan_map.get(day)
        if reference and (row["date"] != reference["date"] or row["artifact"] != reference["artifact"]):
            errors.append(f"Day {day} 进度日期或笔记路径与计划不一致。")
        actual_minutes = integer(row["actual_minutes"], f"Day {day} 进度用时", errors)
        if row["status"] not in valid_statuses or actual_minutes is None or actual_minutes < 0:
            errors.append(f"Day {day} 进度状态或用时不合法。")
        if row["status"] == "completed" and (row["result"] != "pass" or actual_minutes is None or actual_minutes <= 0):
            errors.append(f"Day {day} 完成状态缺少通过记录。")
    validate_links(root, errors)
    validate_manifest(root, errors)
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError, KeyError, UnicodeError) as error:
        print(f"计划无法读取：{error}")
        return 1
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("通过：30 个连续学习日，每天 60 分钟，共 1800 分钟；公开正文、CSV、锚点、清单和进度引用有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
