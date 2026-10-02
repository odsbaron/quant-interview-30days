#!/usr/bin/env python3
"""Validate the schedule, relative references and progress without doing exercises."""
from __future__ import annotations

import csv
import json
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    start = date.fromisoformat(config["start_date"])
    if config["daily_budget_minutes"] != 60:
        errors.append("本计划每日预算必须为 60 分钟，总预算为 1800 分钟。")
    plan = rows(root / "plan/30_days.csv")
    resources = rows(root / "resources/materials.csv")
    resource_ids = {row["id"] for row in resources}
    if len(resource_ids) != len(resources):
        errors.append("材料 ID 重复。")
    if len(plan) != 30 or [int(row["day"]) for row in plan] != list(range(1, 31)):
        errors.append("计划必须按顺序包含 Day 1 到 Day 30，且无重复。")
    if sum(int(row[key]) for row in plan for key in ("review_minutes", "learn_minutes", "practice_minutes", "record_minutes")) != 1800:
        errors.append("30 天总预算必须为 1800 分钟。")
    for row in resources:
        relative = Path(row["relative_path"])
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"材料 {row['id']} 包含非相对路径。")
        anchor = f'id="{row["id"]}"'
        if anchor not in (root / "resources/README.md").read_text(encoding="utf-8"):
            errors.append(f"材料 {row['id']} 缺少导航锚点。")
    for row in plan:
        day = int(row["day"])
        expected_date = (start + timedelta(days=day - 1)).isoformat()
        if row["date"] != expected_date:
            errors.append(f"Day {day:02d} 日期不连续。")
        minutes = [int(row[key]) for key in ("review_minutes", "learn_minutes", "practice_minutes", "record_minutes")]
        if any(value < 0 for value in minutes) or sum(minutes) != config["daily_budget_minutes"]:
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
        if not (root / row["artifact"]).is_file():
            errors.append(f"Day {day:02d} 笔记模板尚未创建。")
    progress = rows(root / "progress/progress.csv")
    if len(progress) != 30 or [int(row["day"]) for row in progress] != list(range(1, 31)):
        errors.append("进度表须包含 30 个不重复学习日。")
    valid_statuses = {"not_started", "in_progress", "needs_review", "completed"}
    plan_map = {int(row["day"]): row for row in plan}
    for row in progress:
        day = int(row["day"])
        reference = plan_map.get(day)
        if reference and (row["date"] != reference["date"] or row["artifact"] != reference["artifact"]):
            errors.append(f"Day {day:02d} 进度日期或笔记路径与计划不一致。")
        if row["status"] not in valid_statuses or int(row["actual_minutes"]) < 0:
            errors.append(f"Day {day:02d} 进度状态或用时不合法。")
        if row["status"] == "completed" and (row["result"] != "pass" or int(row["actual_minutes"]) <= 0):
            errors.append(f"Day {day:02d} 完成状态缺少通过记录。")
    for document in root.rglob("*.md"):
        if ".git" in document.parts:
            continue
        content = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", content):
            if target.startswith(("https://", "http://", "mailto:")):
                continue
            filename = unquote(target.split("#", 1)[0])
            if filename.startswith("/"):
                errors.append(f"{document.relative_to(root)} 包含机器绝对文件链接。")
            elif filename and not (document.parent / filename).exists():
                errors.append(f"{document.relative_to(root)} 引用不存在的文件：{filename}")
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError, KeyError) as error:
        print(f"计划无法读取：{error}")
        return 1
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("通过：30 个连续学习日，每天 60 分钟，共 1800 分钟；材料 ID、文档、笔记和进度引用有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
