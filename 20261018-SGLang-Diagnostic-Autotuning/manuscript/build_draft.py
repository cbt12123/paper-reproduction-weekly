"""Build the JPDC-targeted Elsevier elsarticle submission draft."""
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
BUILD = ROOT / "tmp" / "pdfs" / "v0.2_jpdc"
OUTPUT = ROOT / "output" / "pdf" / "sglang_pd_agent_draft_v0.2_jpdc.pdf"


def run(command, cwd, log_name):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    (BUILD / log_name).write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        print(result.stdout[-7000:])
        print(result.stderr[-2000:])
        raise SystemExit(result.returncode)


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    latex = shutil.which("pdflatex")
    bibtex = shutil.which("bibtex")
    if not latex or not bibtex:
        raise SystemExit("pdflatex and bibtex must be installed and on PATH")
    shutil.copy2(SOURCE / "references.bib", BUILD / "references.bib")
    command = [latex, "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={BUILD.as_posix()}", "main.tex"]
    run(command, SOURCE, "latex_pass_1.txt")
    run([bibtex, "main"], BUILD, "bibtex_console.txt")
    run(command, SOURCE, "latex_pass_2.txt")
    run(command, SOURCE, "latex_pass_3.txt")
    log = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    fatal_checks = ["There were undefined citations", "undefined references",
                    "Citation `", "Overfull \\hbox", "Overfull \\vbox"]
    issues = [item for item in fatal_checks if item in log]
    if issues:
        raise SystemExit("Review LaTeX output before publishing: " + ", ".join(issues))
    shutil.copy2(BUILD / "main.pdf", OUTPUT)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
