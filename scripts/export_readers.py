#!/usr/bin/env python3
"""Build static, credential-free reading views from a local material library.

This script reads sources, never executes notebooks, and never alters learner state.
Pandoc is required only for the optional TeX publication build, not study or CI.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(!?)\[([^\]]*)\]\((?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\)")
UNRELATED = re.compile(r"inferera|dashboard/billing|total_usage|HTTPAdapter|urllib3|requests\.|\bAuthorization\b|\bBearer\b|api[_-]?key|gh[op]_[A-Za-z0-9]+|sk-[A-Za-z0-9]{12,}|\bimport\s+(?:dai|xgboost|structlog)\b|def\s+main\(datasources", re.I)
SECRET = re.compile(r"\b(?:gh[op]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,})\b")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_index() -> tuple[list[str], list[dict[str, str]]]:
    with (ROOT / "resources/materials.csv").open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return fields, list(reader)


def clean_text(text: str) -> str:
    text = re.sub(r"/Users/[^\s`\"'<>]+", "<LOCAL_PATH>", text)
    if SECRET.search(text):
        raise ValueError("待发布文本出现疑似凭证，已中止；请检查本地源，不要直接发布。")
    return text.rstrip() + "\n"


def without_fences(text: str) -> str:
    return re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$", "", text)


def convert_tex(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    # Strip custom section redefinitions from the preamble so Pandoc retains headings.
    body = text.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    for command in (r"\maketitle", r"\clearpage", r"\tableofcontents"):
        body = body.replace(command, "")
    body = body.replace(r"\solutionhead{}", r"\textbf{解答.} ")
    with tempfile.TemporaryDirectory(prefix="quant-reader-") as temporary:
        input_path = Path(temporary) / "body.tex"
        input_path.write_text(body, encoding="utf-8")
        result = subprocess.run(["pandoc", str(input_path), "--from=latex", "--to=gfm+tex_math_dollars", "--wrap=none"],
                                check=True, capture_output=True, text=True)
    # Transparent anchors are redundant here; removing their wrappers preserves math and headings.
    text = re.sub(r"(?m)^</?div[^>]*>\s*$", "", result.stdout)
    return clean_text(text)


def notebook_view(source: Path) -> tuple[str, list[dict[str, object]]]:
    notebook = json.loads(source.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise ValueError(f"不支持的 Notebook 结构：{source.name}")
    pieces = []
    omitted = []
    for index, cell in enumerate(notebook["cells"]):
        raw = cell.get("source", [])
        text = raw if isinstance(raw, str) else "".join(raw)
        if UNRELATED.search(text):
            omitted.append({"index": index, "reason": "unrelated network/billing/credential/platform cell"})
            continue
        if not text.strip():
            continue
        if cell["cell_type"] == "markdown":
            pieces.append(text)
        elif cell["cell_type"] == "code":
            # Preserve learning code only; no execution counts, outputs, attachments or metadata.
            fence = "`" * max(3, max((len(m.group()) for m in re.finditer(r"`+", text)), default=0) + 1)
            pieces.append(f"{fence}python\n{text.rstrip()}\n{fence}")
    return clean_text("\n\n".join(pieces)), omitted


def build(source_root: Path) -> dict[str, object]:
    fields, resources = read_index()
    source_root = source_root.resolve()
    readers = ROOT / "resources/readers"
    readers.mkdir(parents=True, exist_ok=True)
    path_map: dict[Path, Path] = {}
    entries: dict[Path, dict[str, str]] = {}
    for row in resources:
        relative = Path(row["relative_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("原资料路径须为资料库中的相对路径。")
        source = (source_root / relative).resolve()
        source.relative_to(source_root)
        if not source.is_file():
            raise FileNotFoundError(f"缺少材料：{row['id']}")
        public = Path(f"resources/readers/{row['id']}.md")
        row["public_path"] = public.as_posix()
        path_map[source] = public
        entries[source] = row

    # Add direct Markdown references so role maps and factor tables lead to readable sections.
    companions: dict[Path, Path] = {}
    for source in list(path_map):
        if source.suffix != ".md":
            continue
        for match in LINK.finditer(without_fences(source.read_text(encoding="utf-8"))):
            target = unquote((match.group(3) or match.group(4)).split("#", 1)[0])
            if not target or urlsplit(target).scheme:
                continue
            candidate = (source.parent / target).resolve()
            try:
                relative = candidate.relative_to(source_root)
            except ValueError:
                continue
            if candidate.suffix == ".md" and candidate.is_file() and candidate not in path_map and len(companions) < 60:
                public = Path("resources/readers/references") / (digest(relative.as_posix().encode())[:12] + ".md")
                companions[candidate] = public
                path_map[candidate] = public

    documents: dict[Path, str] = {}
    resource_records = []
    companion_records = []

    def write(public: Path, content: str) -> None:
        documents[public] = clean_text(content)

    def rewrite_links(text: str, source: Path, public: Path) -> str:
        def replace(match: re.Match[str]) -> str:
            image, label = match.group(1), match.group(2)
            target = match.group(3) or match.group(4)
            parts = target.split("#", 1)
            filename = unquote(parts[0])
            if not filename or urlsplit(filename).scheme:
                return match.group()
            candidate = (source.parent / filename).resolve()
            if not image and candidate in path_map:
                destination = path_map[candidate]
                relative = Path(os.path.relpath(destination, public.parent)).as_posix()
                fragment = "#" + parts[1] if len(parts) == 2 else ""
                return f"[{label}]({relative}{fragment})"
            # Keep provenance of references outside the published reading set without a broken link.
            return f"{label}（原本地参考：`{filename}`）"
        # Avoid rewriting Markdown-shaped strings in literal code.
        segments = re.split(r"(?ms)(^(`{3,}|~{3,})[^\n]*\n.*?^\2\s*$)", text)
        if len(segments) == 1:
            return LINK.sub(replace, text)
        result = []
        index = 0
        while index < len(segments):
            result.append(LINK.sub(replace, segments[index]))
            if index + 1 < len(segments):
                result.append(segments[index + 1])
            index += 3
        return "".join(result)

    for source, row in entries.items():
        public = path_map[source]
        record: dict[str, object] = {"id": row["id"], "source_relative_path": row["relative_path"],
                                     "source_sha256": digest(source.read_bytes()), "public_path": public.as_posix()}
        header = (f"# {row['title']}：在线阅读版\n\n"
                  f"来源：本地资料 `{row['relative_path']}`。这是便于浏览的派生正文，保留来源中的题面与说明；不代表逐题答案或当前公司规则已核验。\n\n"
                  "[返回资料索引](../README.md)\n\n")
        if source.suffix == ".ipynb":
            body, omitted = notebook_view(source)
            record.update(transformation="notebook cells to Markdown; outputs/metadata omitted", omitted_cells=omitted)
            header += "只保留学习正文与代码；未运行代码，已排除输出、执行状态和无关网络/计费/凭证单元。示例可能包含解法，先独立完成当天任务，再对照阅读。\n\n"
            write(public, header + rewrite_links(body, source, public))
        elif source.suffix == ".tex":
            body = convert_tex(source)
            record["transformation"] = "TeX body to split GitHub Markdown via Pandoc; no compilation"
            chapter_paths = []
            chunks = re.split(r"(?m)(?=^# )", body)
            for number, chunk in enumerate(c for c in chunks if c.strip()):
                title = chunk.splitlines()[0].removeprefix("# ")
                chapter = Path("resources/readers/probability") / f"chapter_{number + 1:02d}.md"
                chapter_paths.append(f"- [{title}](probability/{chapter.name})")
                write(chapter, f"[返回概率讲义目录](../probability_notes.md)\n\n{chunk}")
            write(public, header + "为避免单页过长，按源标题拆分正文；保留数学表达，OCR 原有疑点需要结合题面复核。\n\n" + "\n".join(chapter_paths))
        elif source.suffix == ".csv":
            with source.open(encoding="utf-8-sig", newline="") as handle:
                questions = list(csv.DictReader(handle))
            counts = Counter(row["primary_category"] for row in questions)
            links = []
            for number, category in enumerate(counts, 1):
                category_path = Path("resources/readers/questions") / f"category_{number:02d}.md"
                links.append(f"- [{category}（{counts[category]} 条）](questions/{category_path.name})")
                parts = [f"# {category}\n\n[返回题库目录](../core_questions.md)\n\n“可用”是原整理标签，仍可能含残句或合并题；以下逐条保留，不猜补缺失题意。\n"]
                for question in questions:
                    if question["primary_category"] == category:
                        body = question["question"].replace("<", "&lt;").replace(">", "&gt;")
                        parts.append(f"## {question['question_id']}\n\n{body}\n\n来源：`{question['source']}`\n")
                write(category_path, "\n".join(parts))
            record["transformation"] = "CSV records to categorized Markdown; original wording preserved"
            write(public, header + f"共 {len(questions)} 条原标记可用记录，按主分类提供正文。\n\n" + "\n".join(links))
        else:
            record["transformation"] = "Markdown readable view with relocated source references"
            write(public, header + rewrite_links(source.read_text(encoding="utf-8"), source, public))
        resource_records.append(record)

    for source, public in companions.items():
        relative = source.relative_to(source_root).as_posix()
        content = source.read_text(encoding="utf-8")
        write(public, f"# 补充章节阅读\n\n来源：`{relative}`。内容为本地整理快照，未在导出时重新验证外部规则。\n\n[返回资料索引](../../README.md)\n\n" + rewrite_links(content, source, public))
        companion_records.append({"source_relative_path": relative, "source_sha256": digest(source.read_bytes()), "public_path": public.as_posix()})

    for public, content in documents.items():
        target = ROOT / public
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    files = [{"path": path.as_posix(), "bytes": len(text.encode("utf-8")), "sha256": digest(text.encode("utf-8"))}
             for path, text in sorted(documents.items(), key=lambda item: item[0].as_posix())]
    manifest: dict[str, object] = {"version": 1, "resources": resource_records, "references": companion_records, "files": files}
    (ROOT / "resources/publish_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if "public_path" not in fields:
        fields.append("public_path")
    with (ROOT / "resources/materials.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(resources)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.source_root)
    print(f"Generated {len(manifest['resources'])} material entry points and {len(manifest['files'])} static reading files; no source notebooks executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
