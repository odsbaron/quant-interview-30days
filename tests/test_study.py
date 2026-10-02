"""Progress and validation contracts, exercised only in temporary repositories."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAN_FIELDS = [
    "day", "date", "phase", "topic", "review_minutes", "learn_minutes",
    "practice_minutes", "record_minutes", "task", "acceptance",
    "resource_ids", "artifact",
]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TemporaryRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="quant-study-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        for directory in ("scripts", "plan", "resources", "progress", "templates", "days", "notes"):
            (self.root / directory).mkdir(parents=True)
        for name in ("study.py", "validate_plan.py"):
            shutil.copy2(PROJECT_ROOT / "scripts" / name, self.root / "scripts" / name)
        self.study = load_module(self.root / "scripts/study.py", "temporary_study")
        self.validator = load_module(self.root / "scripts/validate_plan.py", "temporary_validator")
        self.config = {
            "start_date": "2026-10-02",
            "timezone": "Asia/Shanghai",
            "daily_budget_minutes": 60,
            "source_root_env": "QUANT_TEST_SOURCE_ROOT",
        }
        self.write_config()
        (self.root / "templates/daily_note.md").write_text("## 我的独立推导\n\n尚未作答。\n", encoding="utf-8")
        self.plan_rows = []
        self.progress_rows = []
        for day in range(1, 31):
            planned_date = (date(2026, 10, 2) + timedelta(days=day - 1)).isoformat()
            artifact = f"notes/day{day:02d}.md"
            self.plan_rows.append({
                "day": str(day), "date": planned_date, "phase": "基础训练",
                "topic": f"主题 {day}", "review_minutes": "5", "learn_minutes": "10",
                "practice_minutes": "35", "record_minutes": "10",
                "task": "独立推导并实现一个小问题。", "acceptance": "口述思路并检查边界。",
                "resource_ids": "sample", "artifact": artifact,
            })
            self.progress_rows.append({
                "day": str(day), "date": planned_date, "status": "not_started",
                "actual_minutes": "0", "result": "", "help_used": "",
                "review_date": "", "artifact": artifact, "updated_at": "",
            })
            (self.root / f"days/day{day:02d}.md").write_text(
                f"# Day {day:02d}\n\n日期：{planned_date}\n\n" + "独立完成推导、代码与边界复盘。\n" * 20,
                encoding="utf-8",
            )
            (self.root / artifact).write_text(f"# Day {day:02d} 既有笔记\n\n保留我的旧推导。\n", encoding="utf-8")
        self.write_plan()
        write_csv(self.root / "progress/progress.csv", self.progress_rows, self.study.PROGRESS_FIELDS)
        write_csv(self.root / "progress/log.csv", [], self.study.LOG_FIELDS)
        self.resource_rows = [{"id": "sample", "relative_path": "library/sample.md"}]
        self.write_resources()
        (self.root / "resources/README.md").write_text('<span id="sample"></span>\n', encoding="utf-8")

    def write_config(self) -> None:
        (self.root / "config.json").write_text(json.dumps(self.config), encoding="utf-8")

    def write_plan(self) -> None:
        write_csv(self.root / "plan/30_days.csv", self.plan_rows, PLAN_FIELDS)

    def write_resources(self) -> None:
        write_csv(self.root / "resources/materials.csv", self.resource_rows, ["id", "relative_path"])

    def state_snapshot(self) -> dict[str, bytes]:
        """Capture all learner state, including whether a note/log was created."""
        return {
            str(path.relative_to(self.root)): path.read_bytes()
            for directory in ("notes", "progress")
            for path in (self.root / directory).rglob("*")
            if path.is_file()
        }

    def record(self, **changes):
        arguments = {
            "status": "in_progress", "minutes": 12, "result": "partial",
            "help_used": "no", "summary": "我已独立推导，但还需要检查边界。",
            "now": datetime(2026, 11, 20, 23, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
        }
        arguments.update(changes)
        return self.study.record_day(self.root, 1, **arguments)


class StudyTests(TemporaryRepositoryTest):
    def test_cli_help_and_status_work_and_do_not_change_learner_data(self) -> None:
        before = self.state_snapshot()
        for arguments, expected_text in (
            (["--help"], "usage:"),
            (["record", "--help"], "--help-used"),
            (["status"], "未开始：30 天"),
        ):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    ["python3", "scripts/study.py", *arguments], cwd=self.root,
                    capture_output=True, text=True, timeout=10,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                self.assertIn(expected_text, result.stdout)
                if arguments == ["status"]:
                    self.assertIn("累计记录：0 分钟 / 原计划 1800 分钟", result.stdout)
                self.assertEqual(self.state_snapshot(), before)

    def test_repeated_records_preserve_notes_and_logs_and_accumulate_minutes(self) -> None:
        old_note = (self.root / "notes/day01.md").read_text(encoding="utf-8")
        old_log = {
            "timestamp": "2026-10-03T19:00:00+08:00", "day": "2", "status": "in_progress",
            "minutes": "8", "result": "partial", "help_used": "yes",
            "review_date": "2026-10-05", "summary": "历史记录，必须保留。",
        }
        write_csv(self.root / "progress/log.csv", [old_log], self.study.LOG_FIELDS)

        first = self.record(summary="第一轮：写出了暴力实现。")
        self.assertEqual(first["actual_minutes"], "12")
        self.assertEqual(first["review_date"], "2026-11-22")
        self.assertEqual(first["date"], "2026-10-02")
        after_first = (self.root / "notes/day01.md").read_text(encoding="utf-8")

        second = self.record(
            status="completed", minutes=18, result="pass", help_used="yes",
            summary="第二轮：参考提示后检查了重复数和无解。",
            now=datetime(2026, 11, 21, 0, 5, tzinfo=ZoneInfo("Asia/Shanghai")),
        )
        self.assertEqual(second["actual_minutes"], "30")
        self.assertEqual(second["review_date"], "2026-11-23")
        self.assertEqual(second["help_used"], "yes")
        note = (self.root / "notes/day01.md").read_text(encoding="utf-8")
        self.assertTrue(note.startswith(old_note))
        self.assertTrue(note.startswith(after_first))
        self.assertIn("第一轮：写出了暴力实现。", note)
        self.assertIn("第二轮：参考提示后检查了重复数和无解。", note)
        logs = self.study.read_csv(self.root / "progress/log.csv")
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0], old_log)
        self.assertEqual([row["minutes"] for row in logs[1:]], ["12", "18"])
        saved = self.study.read_csv(self.root / "progress/progress.csv")
        self.assertEqual(saved[0]["actual_minutes"], "30")
        self.assertEqual(saved[0]["status"], "completed")
        self.assertEqual(saved[1:], self.progress_rows[1:])

    def test_completed_requires_pass_and_rejection_does_not_change_data(self) -> None:
        for result in ("partial", "fail"):
            with self.subTest(result=result):
                before = self.state_snapshot()
                with self.assertRaisesRegex(ValueError, "pass"):
                    self.record(status="completed", result=result)
                self.assertEqual(self.state_snapshot(), before)

    def test_blank_summary_rejected_without_creating_note_or_log(self) -> None:
        (self.root / "notes/day01.md").unlink()
        (self.root / "progress/log.csv").unlink()
        for summary in ("", " \n\t "):
            with self.subTest(summary=summary):
                before = self.state_snapshot()
                with self.assertRaisesRegex(ValueError, "不能留空"):
                    self.record(summary=summary)
                self.assertEqual(self.state_snapshot(), before)

    def test_invalid_minutes_and_duplicate_progress_rejected_without_writes(self) -> None:
        for minutes in (0, -1, 1441):
            with self.subTest(minutes=minutes):
                before = self.state_snapshot()
                with self.assertRaises(ValueError):
                    self.record(minutes=minutes)
                self.assertEqual(self.state_snapshot(), before)
        duplicated = self.progress_rows + [dict(self.progress_rows[0])]
        write_csv(self.root / "progress/progress.csv", duplicated, self.study.PROGRESS_FIELDS)
        before = self.state_snapshot()
        with self.assertRaisesRegex(ValueError, "重复"):
            self.record()
        self.assertEqual(self.state_snapshot(), before)

    def test_note_existing_file_is_not_overwritten(self) -> None:
        note = self.root / "notes/day01.md"
        old = "我自己的笔记\n包括不该被模板替换的推导。\n"
        note.write_text(old, encoding="utf-8")
        result = self.study.note_day(self.root, 1)
        self.assertEqual(result, note)
        self.assertEqual(note.read_text(encoding="utf-8"), old)

    def test_material_rejects_invalid_ids_missing_files_and_unsafe_paths(self) -> None:
        library = Path(self.temporary.name) / "source"
        (library / "library").mkdir(parents=True)
        existing = library / "library/sample.md"
        existing.write_text("source", encoding="utf-8")
        self.assertEqual(self.study.material_path(self.root, "sample", str(library)), existing.resolve())
        with self.assertRaisesRegex(ValueError, "未知材料"):
            self.study.material_path(self.root, "unknown", str(library))
        for relative in ("../outside.md", str(existing.resolve()), "library/missing.md"):
            with self.subTest(relative=relative):
                self.resource_rows[0]["relative_path"] = relative
                self.write_resources()
                with self.assertRaises(ValueError):
                    self.study.material_path(self.root, "sample", str(library))


class PlanValidationTests(TemporaryRepositoryTest):
    def test_valid_fixture_and_read_only_validation(self) -> None:
        before = self.state_snapshot()
        self.assertEqual(self.validator.validate(self.root), [])
        self.assertEqual(self.state_snapshot(), before)

    def test_wrong_daily_budget_and_duplicate_day_detected(self) -> None:
        self.plan_rows[0]["practice_minutes"] = "36"
        self.write_plan()
        self.assertTrue(any("时间预算" in error for error in self.validator.validate(self.root)))
        self.plan_rows[0]["practice_minutes"] = "35"
        self.plan_rows[1]["day"] = "1"
        self.write_plan()
        self.assertTrue(any("无重复" in error for error in self.validator.validate(self.root)))

    def test_config_cannot_change_the_promised_sixty_minute_budget(self) -> None:
        self.config["daily_budget_minutes"] = 90
        self.write_config()
        for row in self.plan_rows:
            row["practice_minutes"] = "65"
        self.write_plan()
        errors = self.validator.validate(self.root)
        self.assertTrue(errors, "90 分钟配置与30小时承诺冲突，应当被拒绝。")


if __name__ == "__main__":
    unittest.main()
