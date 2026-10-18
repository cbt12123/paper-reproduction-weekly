"""Build the complete Chinese translation using XeLaTeX and shared references."""
from pathlib import Path
import shutil
import subprocess

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parent
BUILD = ROOT / "tmp" / "pdfs" / "v0.2_jpdc" / "zh"
OUTPUT = ROOT / "output" / "pdf" / "sglang_pd_agent_draft_zh_v0.2_jpdc.pdf"


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
    latex = shutil.which("xelatex")
    bibtex = shutil.which("bibtex")
    if not latex or not bibtex:
        raise SystemExit("XeLaTeX, BibTeX, ctex and Windows CJK fonts are required")
    shutil.copy2(SOURCE / "references.bib", BUILD / "references.bib")
    command = [latex, "-interaction=nonstopmode", "-halt-on-error",
               f"-output-directory={BUILD.as_posix()}", "main_zh.tex"]
    run(command, SOURCE, "latex_pass_1.txt")
    run([bibtex, "main_zh"], BUILD, "bibtex_console.txt")
    run(command, SOURCE, "latex_pass_2.txt")
    run(command, SOURCE, "latex_pass_3.txt")
    log = (BUILD / "main_zh.log").read_text(encoding="utf-8", errors="replace")
    fatal_checks = ["There were undefined citations", "undefined references",
                    "Citation `", "Overfull \\hbox", "Overfull \\vbox",
                    "Missing character:"]
    issues = [item for item in fatal_checks if item in log]
    if issues:
        raise SystemExit("Review LaTeX output before publishing: " + ", ".join(issues))
    shutil.copy2(BUILD / "main_zh.pdf", OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
