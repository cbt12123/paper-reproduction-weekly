"""Render manuscript figures from measured CSV values; keep audit IDs out of labels."""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "figures"


def main():
    with (ROOT / "experiments/dsv4pro_32card_pd_ratio_scan.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    # Provenance is retained here and in the external working notes.
    before, after = rows[10], rows[14]
    assert before["PD配比"] == "1p1d" and before["卡数"] == "32"
    assert after["PD配比"] == "2p1d" and after["卡数"] == "48"
    keys = ["总TPM", "平均单卡TPM", "avg TTFT(s)", "avg TPOT"]
    names = ["Total TPM", "TPM per card", "Mean TTFT", "Mean TPOT"]
    values = [(float(after[key]) / float(before[key]) - 1) * 100 for key in keys]
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "none"})
    fig, axis = plt.subplots(figsize=(9.5, 4.3))
    axis.barh(range(4), values, color=["#4C78A8", "#C96C65", "#4C78A8", "#C96C65"])
    axis.set_yticks(range(4), names)
    axis.invert_yaxis()
    axis.axvline(0, color="#555555", linewidth=1)
    axis.set_xlim(-85, 55)
    axis.set_xlabel("Change from 32-card 1P1D to 48-card 2P1D (%)")
    for index, value in enumerate(values):
        axis.text(value + (1.4 if value >= 0 else -1.4), index, f"{value:+.1f}%",
                  ha="left" if value >= 0 else "right", va="center")
    fig.tight_layout()
    for extension in ["png", "svg"]:
        fig.savefig(OUT / f"resource_tradeoff.{extension}", dpi=220)
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
