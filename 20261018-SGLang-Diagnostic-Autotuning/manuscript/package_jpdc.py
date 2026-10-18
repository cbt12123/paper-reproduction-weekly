"""Package the English flat source tree and bilingual working manuscript."""
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "manuscript"
OUTPUT = ROOT / "output"
STAGE = ROOT / "tmp" / "jpdc_source"


def main():
    STAGE.mkdir(parents=True, exist_ok=True)
    tex = (SOURCE / "main.tex").read_text(encoding="utf-8")
    (STAGE / "main.tex").write_text(
        tex.replace("figures/resource_tradeoff.png", "resource_tradeoff.png"),
        encoding="utf-8")
    for path in [SOURCE / "references.bib", SOURCE / "figures/resource_tradeoff.png",
                 ROOT / "tmp/pdfs/v0.2_jpdc/main.bbl"]:
        shutil.copy2(path, STAGE / path.name)
    for name in ["elsarticle.cls", "elsarticle-num.bst"]:
        path = subprocess.check_output(["kpsewhich", name], text=True).strip()
        shutil.copy2(path, STAGE / name)
    with zipfile.ZipFile(OUTPUT / "jpdc_english_source_v0.2.zip", "w",
                         zipfile.ZIP_DEFLATED) as archive:
        for path in STAGE.iterdir():
            archive.write(path, path.name)
    with zipfile.ZipFile(OUTPUT / "manuscript_bilingual_bundle_v0.2_jpdc.zip", "w",
                         zipfile.ZIP_DEFLATED) as archive:
        for path in SOURCE.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, path.relative_to(ROOT))
        for path in (OUTPUT / "pdf").glob("*v0.2_jpdc.pdf"):
            archive.write(path, path.relative_to(ROOT))
    for filename in ["jpdc_english_source_v0.2.zip",
                     "manuscript_bilingual_bundle_v0.2_jpdc.zip"]:
        with zipfile.ZipFile(OUTPUT / filename) as archive:
            assert archive.testzip() is None
        print(OUTPUT / filename)


if __name__ == "__main__":
    main()
