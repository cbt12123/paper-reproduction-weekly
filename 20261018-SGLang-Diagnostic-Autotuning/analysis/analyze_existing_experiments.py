"""Audit the historical CSV without treating heterogeneous runs as replicates.

Run from any directory. Requires matplotlib for the descriptive figures.
Original CSV/article materials are never modified. Row IDs exclude the header.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "experiments" / "dsv4pro_32card_pd_ratio_scan.csv"
OUT = ROOT / "analysis" / "existing_experiments_2026-10-18"
NUMERIC = ["卡数", "并发", "cache命中率(%)", "输入", "输出", "avg TTFT(s)",
           "avg E2E", "avg TPOT", "总TPM", "平均单卡TPM", "TPM：P", "TPM:D"]


def pct(before, after):
    return (after / before - 1) * 100 if before else None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        originals = list(csv.DictReader(stream))
    rows = []
    for index, original in enumerate(originals, 1):
        row = dict(original)
        for key in NUMERIC:
            row[key] = float(row[key]) if row[key] else None
        note = row["特征"]
        row["row_id"] = index
        # Missing/sentinel zeros are preserved in source fields, never interpreted
        # as measured zero latency. Status is descriptive, not a ground truth label.
        if index in (24, 25):
            status = "cache_probe_no_full_metrics"
        elif index == 22:
            status = "deployment_blocked_reported"
        elif index in (32, 34):
            status = "partial_success_reported"
        elif "失败轮" in note or "成功率仅" in note:
            status = "failure_or_degraded_reported"
        elif "100%" in note:
            status = "full_success_reported_in_note"
        else:
            status = "success_fraction_not_explicit"
        row["audit_status"] = status
        row["throughput_available"] = row["总TPM"] > 0
        row["latency_available"] = row["avg TTFT(s)"] > 0
        row["sum_tpm_residual"] = row["总TPM"] - row["TPM：P"] - row["TPM:D"]
        row["per_card_tpm_residual"] = row["平均单卡TPM"] - row["总TPM"] / row["卡数"]
        row["p_column_share_pct"] = row["TPM：P"] / row["总TPM"] * 100 if row["throughput_available"] else None
        rows.append(row)

    lookup = {row["row_id"]: row for row in rows}
    comparison_specs = [
        (1, 5, "async_at_c64"), (4, 6, "async_at_c88"),
        (8, 29, "old_vs_fixed_environment_cold_c88"),
        (11, 15, "32card_1p1d_vs_48card_2p1d"),
        (29, 26, "cold_single_pass_vs_2h_reuse"),
        (29, 32, "cold_single_pass_vs_24h_reuse"),
        (29, 33, "cold_concurrency_88_vs_96"),
        (33, 34, "manual_vs_skill_run_not_matched"),
        (27, 29, "L2_vs_L3_cold_reference_a"),
        (31, 29, "L2_vs_L3_cold_reference_b"),
        (30, 26, "L2_vs_L3_2h"),
    ]
    metrics = ["总TPM", "平均单卡TPM", "TPM:D", "avg TTFT(s)", "avg E2E", "avg TPOT"]
    comparisons = []
    for a, b, label in comparison_specs:
        comparisons.append({"label": label, "before_row": a, "after_row": b,
                            "percent_changes": {key: pct(lookup[a][key], lookup[b][key]) for key in metrics},
                            "cache_hit_change_percentage_points": lookup[b]["cache命中率(%)"] - lookup[a]["cache命中率(%)"],
                            "interpretation": "historical unmatched observations; not causal estimates"})

    valid = [row for row in rows if row["throughput_available"]]
    summary = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "row_id_convention": "one-based data row, excluding CSV header",
        "rows": len(rows),
        "ratio_counts": dict(Counter(row["PD配比"] for row in rows)),
        "card_counts": dict(Counter(str(int(row["卡数"])) for row in rows)),
        "architecture_counts": dict(Counter(row["PD分离/非PD分离"] for row in rows)),
        "status_counts": dict(Counter(row["audit_status"] for row in rows)),
        "all_rows_missing_fields": [key for key in originals[0] if all(not row[key] for row in originals)],
        "positive_throughput_rows": len(valid),
        "zero_tpm_rows_not_assumed_measured_zero": [row["row_id"] for row in rows if not row["throughput_available"]],
        "p_column_share_pct_range": [min(row["p_column_share_pct"] for row in valid), max(row["p_column_share_pct"] for row in valid)],
        "max_abs_sum_tpm_residual": max(abs(row["sum_tpm_residual"]) for row in rows),
        "max_abs_per_card_tpm_residual": max(abs(row["per_card_tpm_residual"]) for row in rows),
        "r32_success_pct_from_note_counts": 284733 / 284738 * 100,
        "r34_success_pct_from_note_counts": 1578 / 1606 * 100,
        "r32_decode_tokens_per_second": lookup[32]["TPM:D"] / 60,
        "r19_conditional_reconciliation": {
            "assumptions": "input/output are mean tokens per successful request; 992 successes; full 1800s measurement interval",
            "count_implied_total_tpm": (lookup[19]["输入"] + lookup[19]["输出"]) * 992 / 30,
            "reported_total_tpm": lookup[19]["总TPM"],
            "implied_measurement_seconds": (lookup[19]["输入"] + lookup[19]["输出"]) * 992 * 60 / lookup[19]["总TPM"],
            "action": "reconcile raw-log metric windows and denominator; not declared a data error",
        },
        "metric_semantics": {
            "p_and_d_columns": "author-confirmed prefill TPM and decode TPM; not independently profiled stage capacity ceilings",
            "total_tpm": "author-confirmed inclusive of cached tokens; do not interpret as fresh prefill compute throughput",
            "tpot_unit": "milliseconds (author-confirmed)",
            "cache_hit_definition_and_weighting": "unknown",
        },
        "historical_decision_provenance": "author-confirmed human diagnosis/action selection with skill execution; autonomous Agent selection is planned, not demonstrated",
        "comparisons": comparisons,
        "inference_limits": "No confidence intervals, causal effects, goodput, tail latency, or agent search gains can be recovered from these aggregate heterogeneous records alone.",
    }
    assert summary["max_abs_sum_tpm_residual"] < 0.05
    assert summary["max_abs_per_card_tpm_residual"] < 0.02
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "rows_audited.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["row_id", "audit_status", "throughput_available", "latency_available"]
                                + list(originals[0])
                                + ["sum_tpm_residual", "per_card_tpm_residual", "p_column_share_pct"])
        writer.writeheader()
        writer.writerows(rows)

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "svg.fonttype": "none", "figure.dpi": 140})
    chosen = [lookup[i] for i in (29, 26, 32)]
    labels = ["R29\nCold / single pass", "R26\n2 h / repeated", "R32\n24 h / repeated"]
    colors = ["#4C78A8", "#F2A541", "#54A576"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.7))
    specs = [("总TPM", 1e6, "Reported total TPM (millions)"),
             ("TPM:D", 1e3, "Decode TPM (thousands)"),
             ("avg TTFT(s)", 1, "Mean TTFT (seconds)"),
             ("cache命中率(%)", 1, "Reported cache hit (%)")]
    for axis, (key, scale, title) in zip(axes.flat, specs):
        values = [row[key] / scale for row in chosen]
        axis.bar(range(3), values, color=colors, width=0.58)
        axis.set_xticks(range(3), labels)
        axis.set_title(title, loc="left", fontweight="bold")
        axis.set_ylim(0, max(values) * 1.2)
        axis.grid(axis="y", alpha=0.2)
        axis.set_axisbelow(True)
        for i, value in enumerate(values):
            axis.text(i, value + max(values) * 0.025, f"{value:.2f}", ha="center", fontsize=10)
    fig.suptitle("Historical outcomes across cache/run contexts", fontsize=15, fontweight="bold", y=0.98)
    fig.text(0.5, 0.015, "Historical runs, not a controlled A/B: workload realization, run duration and output lengths differ.\n"
             "All use 32-card 1P1D at concurrency 88; total TPM includes cached tokens.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=[0, 0.07, 1, 0.94])
    for suffix in ("png", "svg"):
        fig.savefig(OUT / "figures" / ("cache_context." + suffix), dpi=180)
    plt.close(fig)

    comparison = next(item for item in comparisons if item["label"] == "32card_1p1d_vs_48card_2p1d")
    keys = ["总TPM", "平均单卡TPM", "avg TTFT(s)", "avg TPOT"]
    names = ["Total TPM (higher better)", "TPM per card (higher better)",
             "Mean TTFT (lower better)", "Mean TPOT (lower better)"]
    values = [comparison["percent_changes"][key] for key in keys]
    fig, axis = plt.subplots(figsize=(10, 4.8))
    axis.barh(range(4), values, color=["#4C78A8", "#C96C65", "#4C78A8", "#C96C65"])
    axis.set_yticks(range(4), names)
    axis.invert_yaxis()
    axis.axvline(0, color="#555555", linewidth=1)
    axis.set_xlim(-85, 55)
    axis.set_xlabel("Change from R11 to R15 (%)")
    axis.set_title("More capacity does not imply higher efficiency", loc="left", fontweight="bold", pad=14)
    for index, value in enumerate(values):
        axis.text(value + (1.5 if value >= 0 else -1.5), index, f"{value:+.1f}%",
                  va="center", ha="left" if value >= 0 else "right")
    fig.text(0.5, 0.025, "R11: 32-card 1P1D; R15: 48-card 2P1D. Different machine groups and historical runs.\n"
             "Descriptive differences only; not a fixed-resource ratio sweep or a causal scaling result.", ha="center", fontsize=9)
    fig.tight_layout(rect=[0, 0.11, 1, 1])
    for suffix in ("png", "svg"):
        fig.savefig(OUT / "figures" / ("resource_tradeoff." + suffix), dpi=180)
    plt.close(fig)
    print(json.dumps({"rows": len(rows), "out": str(OUT),
                      "status_counts": summary["status_counts"],
                      "source_sha256": summary["source_sha256"]}, ensure_ascii=True))


if __name__ == "__main__":
    main()
