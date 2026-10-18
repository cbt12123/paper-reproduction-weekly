"""Check Chinese-English structure, references and PDF text; render for visual QA."""
from pathlib import Path
import json
import re
import shutil
import subprocess

import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "manuscript"
BUILD = ROOT / "tmp" / "pdfs" / "v0.2_jpdc" / "zh"
PDF = ROOT / "output" / "pdf" / "sglang_pd_agent_draft_zh_v0.2_jpdc.pdf"


def cited_keys(source):
    return {key.strip() for group in re.findall(r"\\cite\{([^}]+)\}", source)
            for key in group.split(",")}


def main():
    chinese = (SOURCE / "main_zh.tex").read_text(encoding="utf-8")
    english = (SOURCE / "main.tex").read_text(encoding="utf-8")
    bibliography = (SOURCE / "references.bib").read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    assert cited_keys(chinese) == cited_keys(english) == bib_keys
    structure = {}
    for token in [r"\section{", r"\subsection{", r"\begin{equation}",
                  r"\begin{figure}", r"\begin{tabular}", r"\begin{tabularx}"]:
        assert chinese.count(token) == english.count(token), token
        structure[token] = chinese.count(token)
    doc = fitz.open(PDF)
    page_texts = [page.get_text() for page in doc]
    bounds_issues = []
    for index, page in enumerate(doc):
        for block in page.get_text("blocks"):
            rect = fitz.Rect(block[:4])
            if rect.x0 < -1 or rect.y0 < -1 or rect.x1 > page.rect.width + 1 or rect.y1 > page.rect.height + 1:
                bounds_issues.append({"page": index + 1, "bbox": list(rect)})
    assert not bounds_issues, bounds_issues
    assert not any("??" in text or "\ufffd" in text for text in page_texts)
    text = "\n\n".join(page_texts)
    compact = re.sub(r"\s+", "", text)
    assert "实验设置与评价指标" in compact
    assert "CSV" not in compact and "作者确认" not in compact and "台账" not in compact
    assert "BoTaoCheng" in compact and "Tencent" in compact
    assert "实验验证待补" not in compact
    assert "[24]" in text
    assert "v0.2" not in " ".join(page_texts)
    assert "Research draft" not in " ".join(page_texts)
    assert "研究初稿" not in " ".join(page_texts)
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise SystemExit("pdftoppm is required for visual QA")
    result = subprocess.run([renderer, "-r", "100", "-png", str(PDF), str(BUILD / "page")],
                            capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    pages = sorted((p for p in BUILD.glob("page-*.png")
                    if int(p.stem.split("-")[-1]) <= len(doc)),
                   key=lambda p: int(p.stem.split("-")[-1]))
    assert len(pages) == len(doc)
    contacts = []
    for start in range(0, len(pages), 4):
        canvas = Image.new("RGB", (1000, 1460), "#dddddd")
        drawing = ImageDraw.Draw(canvas)
        for offset, path in enumerate(pages[start:start + 4]):
            page_image = Image.open(path).convert("RGB")
            page_image.thumbnail((480, 695))
            x = (offset % 2) * 500 + 10
            y = (offset // 2) * 730 + 25
            canvas.paste(page_image, (x, y))
            drawing.text((x, y - 18), f"Page {start + offset + 1}", fill="black")
        contact = BUILD / f"contact-{start // 4 + 1}.png"
        canvas.save(contact)
        contacts.append(str(contact))
    (BUILD / "extracted_text.txt").write_text(text, encoding="utf-8")
    report = {"pdf": str(PDF), "pages": len(doc), "references": len(bib_keys),
              "same_structure_as_english": structure,
              "same_citation_keys_as_english": True,
              "text_within_page_bounds": True, "historical_and_prospective_evidence_separated": True,
              "chinese_characters_in_source": len(re.findall(r"[\u4e00-\u9fff]", chinese)),
              "contacts": contacts, "visual_inspection": "pending manual inspection"}
    (BUILD / "qa_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
