# Paper Reproduction Weekly
每周复现 1 篇顶会（ACL/NIPS/ICML 等）论文，聚焦深度学习核心模型，注重代码可复现性与原理拆解。

## 🌟 项目目标
1. 深入理解论文核心思想与技术细节，而非仅“跑通代码”；
2. 输出规范的复现文档与可复用代码，形成技术沉淀；
3. 培养“从论文到工程”的落地能力，积累深度学习实践经验。

## 📚 复现论文列表（更新中）
| 日期       | 论文标题                          | 领域         | 核心贡献                  | 复现状态 |
|------------|-----------------------------------|--------------|---------------------------|----------|
| 2024.09    | Attention Is All You Need         | NLP/Transformer | 提出 Transformer 架构，替代RNN | ✅ 完成   |
| 2024.10    | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | NLP | 提出双向预训练模型 BERT | 🚧 进行中 |


## SGLang PD 分离推理与 Agent 自动调优研究

更新于 2026-10-18，当前稿件为 v0.2。项目位于 [20261018-SGLang-Diagnostic-Autotuning/](20261018-SGLang-Diagnostic-Autotuning/)，包含中英文论文源稿与 PDF、35 条历史实验记录及分析、诊断技能设计、实验交接和版本归档。完整 Agent 与受控对照仍待实现和验证。

- [项目说明与构建方法](20261018-SGLang-Diagnostic-Autotuning/README.md)
- [中文论文 PDF](20261018-SGLang-Diagnostic-Autotuning/output/pdf/sglang_pd_agent_draft_zh_v0.2_jpdc.pdf)
- [英文论文 PDF](20261018-SGLang-Diagnostic-Autotuning/output/pdf/sglang_pd_agent_draft_v0.2_jpdc.pdf)
- [实验分析](20261018-SGLang-Diagnostic-Autotuning/analysis/existing_experiments_2026-10-18/README.md)
- [版本记录](20261018-SGLang-Diagnostic-Autotuning/manuscript/CHANGELOG.md)

## 🛠️ 使用指南
1. 克隆仓库：`git clone https://github.com/cbt12123/paper-reproduction-weekly.git`
2. 进入对应论文目录（如 Transformer）：`cd 202409-Transformer`
3. 安装依赖：`pip install -r requirements.txt`
4. 运行代码：直接打开 `transformer.ipynb` 执行（推荐 Jupyter Lab/Notebook）

## 📝 个人收获（可选，体现思考）
- 掌握 Transformer 中“多头注意力”的实现细节，解决了“掩码机制”的边界问题；
- 理解预训练模型（如 BERT）的“双向编码”与“微调”逻辑，优化了数据预处理流程；
- 养成“先梳理论文公式→再写核心代码→最后验证结果”的复现习惯。

## 📞 联系我
Gitee：[你的Gitee主页链接]  
邮箱：你的邮箱（简历中已写，此处可加，方便沟通）