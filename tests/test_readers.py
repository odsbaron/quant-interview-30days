"""Static export safety: synthetic notebooks only, no source-code execution."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("reader_export", ROOT / "scripts/export_readers.py")
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)


class NotebookReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="static-reader-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def notebook(self, cells: list[dict]) -> Path:
        source = self.directory / "synthetic.ipynb"
        source.write_text(json.dumps({
            "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"private_note": "NOTEBOOK_METADATA_MUST_NOT_APPEAR"},
            "cells": cells,
        }), encoding="utf-8")
        return source

    def test_code_is_displayed_without_running_or_exporting_output_metadata(self) -> None:
        sentinel = self.directory / "executed.txt"
        code = f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('executed')\n"
        source = self.notebook([
            {
                "cell_type": "markdown", "source": ["# 学习正文\n"],
                "metadata": {"private_note": "CELL_METADATA_MUST_NOT_APPEAR"},
                "attachments": {"private.png": {"image/png": "ATTACHMENT_MUST_NOT_APPEAR"}},
            },
            {
                "cell_type": "code", "source": code, "execution_count": 777,
                "metadata": {"private_note": "CODE_METADATA_MUST_NOT_APPEAR"},
                "outputs": [{"output_type": "stream", "name": "stdout", "text": "OUTPUT_MUST_NOT_APPEAR"}],
            },
        ])
        text, omitted = export.notebook_view(source)
        self.assertFalse(sentinel.exists(), "导出不得执行源 code cell。")
        self.assertIn("# 学习正文", text)
        self.assertIn(code.rstrip(), text)
        self.assertEqual(omitted, [])
        for private in (
            "NOTEBOOK_METADATA_MUST_NOT_APPEAR", "CELL_METADATA_MUST_NOT_APPEAR",
            "CODE_METADATA_MUST_NOT_APPEAR", "ATTACHMENT_MUST_NOT_APPEAR",
            "OUTPUT_MUST_NOT_APPEAR", "execution_count", "777",
        ):
            self.assertNotIn(private, text)

    def test_unrelated_cells_are_omitted_whole_and_backticks_use_longer_fence(self) -> None:
        unrelated = [
            "BILLING_CELL_MARKER = 1\nurl = 'https://example.invalid/dashboard/billing'\n",
            "API_CELL_MARKER = 1\napi_key = 'not-a-real-key'\n",
            "NETWORK_CELL_MARKER = 1\nrequests.get('https://example.invalid/')\n",
            "PLATFORM_CELL_MARKER = 1\nimport dai\n",
        ]
        learning = 'def example():\n    return "``` is literal text"\n'
        cells = [{"cell_type": "code", "source": value} for value in unrelated]
        cells.append({"cell_type": "code", "source": learning})
        source = self.notebook(cells)
        text, omitted = export.notebook_view(source)
        self.assertEqual([entry["index"] for entry in omitted], [0, 1, 2, 3])
        for marker in ("BILLING_CELL_MARKER", "API_CELL_MARKER", "NETWORK_CELL_MARKER", "PLATFORM_CELL_MARKER"):
            self.assertNotIn(marker, text, "混入不相关逻辑时应排除整个单元。")
        self.assertTrue(text.startswith("````python\n"))
        self.assertTrue(text.endswith("\n````\n"))
        self.assertIn(learning.rstrip(), text)

    def test_synthetic_long_secret_is_rejected_without_printing_its_value(self) -> None:
        fake_token = "sk-" + "FAKE_TOKEN_FOR_TEST_ONLY_" * 3
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            with self.assertRaises(ValueError) as caught:
                export.clean_text(f"some harmless text {fake_token} more text")
        self.assertNotIn(fake_token, str(caught.exception))
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
