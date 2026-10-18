"""Render the final PDF and record checks; visual inspection remains required."""
from pathlib import Path
import json
import re
import shutil
import subprocess

import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "manuscript"
BUILD = ROOT / "tmp" / "pdfs"
PDF = ROOT / "output" / "pdf" / "sglang_pd_agent_draft_v0.1.pdf"


def main():
    doc = fitz.open(PDF)
    page_texts = [page.get_text() for page in doc]
    bounds_issues = []
    for index, page in enumerate(doc):
        for block in page.get_text("blocks"):
            rect = fitz.Rect(block[:4])
            if rect.x0 < -1 or rect.y0 < -1 or rect.x1 > page.rect.width + 1 or rect.y1 > page.rect.height + 1:
                bounds_issues.append({"page": index + 1, "bbox": list(rect)})
    latex_source = (SOURCE / "main.tex").read_text(encoding="utf-8")
    bib_source = (SOURCE / "references.bib").read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_source))
    citations = {key.strip() for group in re.findall(r"\\cite\{([^}]+)\}", latex_source)
                 for key in group.split(",")}
    skills = json.loads((SOURCE / "diagnostic_skills.design.json").read_text(encoding="utf-8"))
    assert skills["execution_enabled"] is False
    assert len(skills["skills"]) == 4
    assert citations == bib_keys, (citations - bib_keys, bib_keys - citations)
    assert not bounds_issues, bounds_issues
    assert not any("??" in text or "\ufffd" in text for text in page_texts)
    assert "This draft reports no empirical results" in " ".join(page_texts).replace("\n", " ")
    assert "[20]" in "\n".join(page_texts)
    renderer = shutil.which("pdftoppm")
    if not renderer:
        raise SystemExit("pdftoppm is required for the visual QA pass")
    result = subprocess.run([renderer, "-r", "100", "-png", str(PDF), str(BUILD / "page")],
                            capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    pages = sorted((p for p in BUILD.glob("page-*.png")
                    if int(p.stem.split("-")[-1]) <= len(doc)),
                   key=lambda p: int(p.stem.split("-")[-1]))
    assert len(pages) == len(doc), "Expected one current rendering per PDF page"
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
    (BUILD / "extracted_text.txt").write_text("\n\n".join(page_texts), encoding="utf-8")
    report = {
        "pdf": str(PDF), "pages": len(doc), "references": len(bib_keys),
        "citations_resolved": True, "text_within_page_bounds": True,
        "unmeasured_status_explicit": True, "design_skills": len(skills["skills"]),
        "approximate_body_words": len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", latex_source.split("\\section{Introduction}")[1].split("\\bibliographystyle")[0])),
        "contacts": contacts,
        "visual_inspection": "pending manual inspection of rendered pages"
    }
    (BUILD / "qa_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
