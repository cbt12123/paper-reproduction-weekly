Research ledger / 文献与主张核验记录，2026-10-18。

**Reading scope and drafting policy**

本轮主要读取作者/会议/期刊原文及官方项目资料。文献总结采用简短转述，不复刻原文段落或图表。论文提出的方法属于待实现设计；机器资源由用户提供，不来自公共性能测试。没有将预印本标成已发表期刊。

**Core sources**

| BibTeX key | Primary source and status | Supports / boundary |
|---|---|---|
| sglang2024 | [NeurIPS 2024](https://proceedings.nips.cc/paper_files/paper/2024/hash/724be4472168f31ba1c9ac630f15dec8-Abstract-Conference.html) | SGLang 框架背景；原论文不证明 P800 后端功能 |
| distserve2024 | [OSDI 2024](https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin) | PD、阶段 SLO 与 goodput；不能称首次 PD 规划 |
| splitwise2024 | [微软论文页](https://www.microsoft.com/en-us/research/publication/splitwise-efficient-generative-llm-inference-using-phase-splitting/) | 按阶段配置硬件；不是本文新增概念 |
| sarathi2024 | [OSDI 2024](https://www.usenix.org/conference/osdi24/presentation/agrawal) | 有力同置/分块 prefill 对照 |
| hexgen2025 | [ICLR 原文](https://openreview.net/pdf?id=Cs6MrbFuMq)、[作者 HTML](https://arxiv.org/html/2502.07903v1) | 已考虑异构资源与通信，不能描述为忽略网络 |
| mooncake2024 | [作者技术报告](https://arxiv.org/abs/2407.00079) | 本稿引用技术报告版本；另有 [TOS 期刊版](https://doi.org/10.1145/3773772)，不得混用版本数据 |
| scoot2025 | [作者全文 v2](https://arxiv.org/html/2408.04323v2)、[作者代码](https://github.com/Ketonmi/SCOOT) | WWW 2025，正式 DOI 10.1145/3696410.3714930；推理约束调优近邻 |
| gptuner2024 | [PVLDB 正式 PDF](https://vldb.org/pvldb/vol17/p1939-tang.pdf) | 领域知识与数值优化近邻 |
| lambdatune2025 | [SIGMOD 官方期刊目录](https://2025.sigmodconf.hosting.acm.org/toc-3-1.html) | PACMMOD 2025；整配置生成及评价代价，属于方法参考 |
| stellar2025 | [完整作者 HTML](https://arxiv.org/html/2602.23220v1)、[正式 DOI](https://doi.org/10.1145/3712285.3759887) | SC 2025；作者上传 arXiv 在 2026，不能据此改会议年份 |
| sysinsight2026 | [完整作者 HTML](https://arxiv.org/html/2603.22708v1) | 原文明确 PVLDB 19(6):1358-1371，2026，正式 DOI；比上一轮仅“接收信息”的核验更完整 |
| storagextuner2025 | [作者摘要](https://arxiv.org/abs/2510.25017) | 预印本；验证经验和多角色调优也是相关方向，未声称全文分析完成 |
| methodology2024 | [作者机构说明](https://ac.liacs.nl/blog/methodology-paper)、[DOI](https://doi.org/10.1016/j.future.2024.05.021) | FGCS 2024；完整时间与随机性评价 |
| autotunebench2026 | [作者原文](https://arxiv.org/abs/2609.18123) | 预印本；Agent 调优测量协议已有研究 |
| sglangpd | [官方 PD 文档](https://docs.sglang.io/docs/advanced_features/pd_disaggregation) | 动态文档；不同 TP 的 staging buffer 已有，不作为新增贡献 |
| kunlunplugin | [官方仓库](https://github.com/baidu-baige/sglang-kunlun) | 已有 P800/PD 相关 hooks；本地版本能力待验 |
| ecotuning2026 | [作者原文](https://arxiv.org/abs/2610.08373) | 预印本；结构化建模与有限预算约束优化已有 |
| sloguard2026 | [作者原文](https://arxiv.org/abs/2604.17627) | 预印本；失败感知和预算一致性已有 |
| tokenscale2025 | [作者原文](https://arxiv.org/abs/2512.03416) | 预印本；阶段/网络工作速率与自动伸缩已有 |
| pdresources2026 | [作者原文](https://arxiv.org/abs/2603.04716) | 预印本；SLO 与 P/D 数量规划已有 |

**Nearest-neighbor checks**

STELLAR 全文 4.3-4.4：已包含自适应分析请求、带上下文 JSON 规则和冲突处理。因此，本稿不把这些结构本身写成新颖点。

SysInsight 全文 4-5：已将代码关联、实测规则、诊断与可靠性维护结合。因此，本稿不能声称首次使用条件规则或反馈验证。新设计需要在 PD 诊断动作及迁移重放上证明额外价值。

StorageXTuner 摘要也包含经过实测的经验管理；仅“可验证经验”不是足够的差异。

**Claims that are deliberately absent**

- 首个 Agent 自动调优器；首个带记忆/skill 的调优系统。
- 首次用文档、性能分析或上下文规则指导搜索。
- 首次在 PD 中考虑通信、资源数量或 SLO。
- 已发现 P800 的某种确定硬件瓶颈。
- 已实现、已生产部署、已经优于基线、全局最优或收敛保证。

**Design choices versus established facts**

技能元组、局部重放门槛、诊断评分和保留全空间探索是本文提出的设计，不是引用论文已经为本系统验证的结论。评分的区分能力尚无概率模型，不写成“最大化真实信息增益”。经验支持率不写成因果概率。

TTFT 的实际关键路径必须测量。不能假定状态传输和 D 接纳永远处于首 token 的关键路径，也不能将重叠阶段耗时全部相加。

**Known adjacent journal examples, not central algorithm evidence**

[Nightjar, JSA 178 (2026), 103889](https://doi.org/10.1016/j.sysarc.2026.103889)、[SpectraBench, FGCS 181 (2026), 108423](https://doi.org/10.1016/j.future.2026.108423) 是已检索到的刊物内容对标；本轮仍主要取得出版者摘要，未靠它们推断本文的方法空白。

[HwPC 自动调优, FGCS 179 (2026), 108358](https://doi.org/10.1016/j.future.2025.108358) 有[作者机构全文](https://ddd.uab.cat/pub/artpub/2026/324811/1-s2.0-S0167739X25006521-main.pdf)。可后续用于深化观测选择方法，不在本文尚未确定可采集硬件计数器时强行嫁接其特征集。

**Remaining literature and implementation work**

继续跟踪诊断技能选择、可迁移 agent memory、PD 调优和大规模资源规划的新论文。正式提交前还需从确定目标刊导入最终模板，并对所有引文从 DOI/作者原文导出做最后核对。本轮不宣称已做穷尽检索，也不将“未检索到完全同题文章”当成原创证明。
