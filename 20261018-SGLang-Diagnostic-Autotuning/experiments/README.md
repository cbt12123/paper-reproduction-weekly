# 实验记录

已有 CSV 的解析、证据边界和后续实验建议见 [已有实验价值分析](../analysis/existing_experiments_2026-10-18/README.md)。其中 R1–R35 按 CSV 数据行编号，源 CSV 未改写；部分零值是未报告或失败标记，不应解释为零时延。

本目录用于在实验环境补充可追溯证据。当前已有 dsv4pro 32 卡 P800 PD 配比扫描的汇总数据与记录模板；各次运行的完整元数据仍待按以下结构补齐。

## 已有数据

- `dsv4pro_32card_pd_ratio_scan.csv`：dsv4pro 在 32 卡 P800 上的 mP:nD 配比扫描汇总（PD 分离与非 PD 分离，含并发、cache 命中率、TTFT/TPOT/E2E、总 TPM 与单卡 TPM 等；失败轮已保留并在"特征"列标注失败原因）。原始压测日志在 TIONE 环境，路径见各行的 `log_path` 列，尚未入库校验。

建议目录：

```text
experiments/
  templates/run_metadata.template.json
  runs/<run-id>/metadata.json
  runs/<run-id>/config.json
  runs/<run-id>/summary.json
  runs/<run-id>/analysis.md
  raw/                           # Git 忽略；大规模原始数据在外部保存
```

1. 复制模板为唯一运行 ID 对应的 `metadata.json`。填写实际机器、能力清单、SGLang/插件/驱动版本及配置；模板的 `null` 表示尚未填写，不是零值。
2. 运行前记录模型与精度、P/D 副本和并行策略、资源分配、负载、SLO、超时、随机种子及预算。控制器与技能库版本也应记录。
3. 运行后记录时间区间、原始数据位置与校验值、失败情况、恢复和全部成本。完成状态不等于达到 SLO，需单独报告可行性。
4. 汇总文件给出指标数值、单位、样本量及计算口径，明确区分实测、推导与未测项。保留失败或未达标运行。
5. 在 `analysis.md` 写明证据支持或反驳了什么，再将已验证结论更新到中英文稿，并在正文或分析中引用运行 ID。

建议运行 ID 使用 UTC 时间和简短任务名，例如 `YYYYMMDDTHHMMSSZ-baseline-01`。源任务建库、阈值验证及最终留出测试需要分开；先冻结对照条件，再进行正式比较。压测原始数据和模型权重不直接加入 Git，用可在另一环境访问的位置及校验值关联。
