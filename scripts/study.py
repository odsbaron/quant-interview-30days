#!/usr/bin/env python3
"""Display daily tasks and preserve learner-reported progress (standard library only)."""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
PROGRESS_FIELDS = ["day", "date", "status", "actual_minutes", "result", "help_used", "review_date", "artifact", "updated_at"]
LOG_FIELDS = ["timestamp", "day", "status", "minutes", "result", "help_used", "review_date", "summary"]
LABELS = {"not_started": "未开始", "in_progress": "进行中", "needs_review": "需补练", "completed": "已完成"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_text(rows: list[dict[str, str]], fields: list[str]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def plan_day(root: Path, day: int) -> dict[str, str]:
    if not 1 <= day <= 30:
        raise ValueError("学习日必须在 1 到 30 之间。")
    for row in read_csv(root / "plan/30_days.csv"):
        if int(row["day"]) == day:
            return row
    raise ValueError(f"计划中缺少 Day {day:02d}。")


def local_now(root: Path) -> datetime:
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    return datetime.now(ZoneInfo(config["timezone"]))


def note_day(root: Path, day: int) -> Path:
    row = plan_day(root, day)
    target = root / row["artifact"]
    if not target.exists():
        template = (root / "templates/daily_note.md").read_text(encoding="utf-8")
        atomic_write(target, f"# Day {day:02d}：{row['topic']}\n\n计划日期：{row['date']}\n\n" + template)
    return target


def record_day(root: Path, day: int, *, status: str, minutes: int, result: str,
               help_used: str, summary: str, now: datetime | None = None) -> dict[str, str]:
    plan_day(root, day)
    if status not in {"in_progress", "needs_review", "completed"}:
        raise ValueError("记录状态必须为 in_progress、needs_review 或 completed。")
    if not 1 <= minutes <= 1440:
        raise ValueError("本次实际用时须为 1 到 1440 的整数分钟。")
    if result not in {"pass", "partial", "fail"} or help_used not in {"yes", "no", "unknown"}:
        raise ValueError("结果或提示使用情况不合法。")
    if not summary.strip():
        raise ValueError("请填写实际作答总结，不能留空。")
    if status == "completed" and result != "pass":
        raise ValueError("完成状态要求验收结果 pass；未通过时请记录 needs_review。")
    rows = read_csv(root / "progress/progress.csv")
    matches = [row for row in rows if int(row["day"]) == day]
    if len(matches) != 1:
        raise ValueError("进度表缺少该学习日或出现重复，请先运行 validate_plan.py。")
    current = matches[0]
    timestamp = now if now is not None else local_now(root)
    review_date = (timestamp.date() + timedelta(days=2)).isoformat()
    current.update(status=status, actual_minutes=str(int(current["actual_minutes"]) + minutes),
                   result=result, help_used=help_used, review_date=review_date,
                   updated_at=timestamp.isoformat(timespec="seconds"))
    log_path = root / "progress/log.csv"
    logs = read_csv(log_path) if log_path.exists() else []
    logs.append(dict(timestamp=current["updated_at"], day=str(day), status=status,
                     minutes=str(minutes), result=result, help_used=help_used,
                     review_date=review_date, summary=summary.strip()))
    note = note_day(root, day)
    entry = (f"\n\n## 作答记录 {current['updated_at']}\n\n"
             f"- 本次用时：{minutes} 分钟\n- 状态：{LABELS[status]}\n"
             f"- 结果：{result}\n- 使用提示：{help_used}\n- 复习日期：{review_date}\n\n"
             f"{summary.strip()}\n")
    atomic_write(note, note.read_text(encoding="utf-8") + entry)
    atomic_write(log_path, csv_text(logs, LOG_FIELDS))
    atomic_write(root / "progress/progress.csv", csv_text(rows, PROGRESS_FIELDS))
    return current


def material_path(root: Path, resource_id: str, source_root: str | None) -> Path:
    resources = read_csv(root / "resources/materials.csv")
    resource = next((row for row in resources if row["id"] == resource_id), None)
    if resource is None:
        raise ValueError(f"未知材料 ID：{resource_id}")
    config = json.loads((root / "config.json").read_text(encoding="utf-8"))
    configured = source_root or os.environ.get(config["source_root_env"])
    library = Path(configured).expanduser() if configured else root.parent
    relative = Path(resource["relative_path"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("材料索引必须使用资料库内的相对路径。")
    path = (library / relative).resolve()
    if not path.is_file():
        raise ValueError("未找到原资料；请用 --source-root 指定资料库，或直接使用 days 中的题面。")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="30 天量化训练：查看任务、笔记和真实进度")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("today", help="按 Asia/Shanghai 日期显示任务")
    for name in ("day", "note"):
        child = sub.add_parser(name)
        child.add_argument("day", type=int)
    sub.add_parser("status")
    material = sub.add_parser("material", help="定位原资料，不执行它")
    material.add_argument("id")
    material.add_argument("--source-root")
    record = sub.add_parser("record", help="根据实际作答记录；不自动认证掌握度")
    record.add_argument("day", type=int)
    record.add_argument("--status", choices=("in_progress", "needs_review", "completed"), required=True)
    record.add_argument("--minutes", type=int, required=True)
    record.add_argument("--result", choices=("pass", "partial", "fail"), required=True)
    record.add_argument("--help-used", dest="help_used", choices=("yes", "no", "unknown"), default="unknown")
    record.add_argument("--summary", required=True)
    args = parser.parse_args()
    try:
        if args.command in {"day", "today"}:
            if args.command == "today":
                rows = read_csv(ROOT / "plan/30_days.csv")
                today = local_now(ROOT).date().isoformat()
                found = next((row for row in rows if row["date"] == today), None)
                if found is None:
                    print(f"今天（{today}）不在原定 30 天排期中。用 day N 查看任务，status 查看待完成项。")
                    return 0
                day = int(found["day"])
            else:
                day = args.day
            row = plan_day(ROOT, day)
            print(f"Day {day:02d} | {row['date']} | {row['topic']} | 60 分钟\n")
            print((ROOT / f"days/day{day:02d}.md").read_text(encoding="utf-8"))
        elif args.command == "note":
            print(note_day(ROOT, args.day))
        elif args.command == "material":
            print(material_path(ROOT, args.id, args.source_root))
        elif args.command == "status":
            rows = read_csv(ROOT / "progress/progress.csv")
            counts = Counter(row["status"] for row in rows)
            for key, label in LABELS.items():
                print(f"{label}：{counts[key]} 天")
            print(f"累计记录：{sum(int(row['actual_minutes']) for row in rows)} 分钟 / 原计划 1800 分钟")
            pending = [f"{int(row['day']):02d}" for row in rows if row["status"] != "completed"]
            print("待完成学习日：" + (", ".join(pending) if pending else "无"))
        elif args.command == "record":
            row = record_day(ROOT, args.day, status=args.status, minutes=args.minutes,
                             result=args.result, help_used=args.help_used, summary=args.summary)
            print(f"已记录 Day {args.day:02d}：{LABELS[row['status']]}，累计 {row['actual_minutes']} 分钟；复习 {row['review_date']}")
            if args.minutes > 60:
                print("本次用时超过 60 分钟预算，已保留真实用时；下一次优先处理卡点。")
    except (ValueError, OSError, KeyError) as error:
        print(f"无法完成：{error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
