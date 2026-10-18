# SGLang Diagnostic Autotuning

面向 SGLang 预填充与解码（PD）分离推理服务的诊断技能复用与 Agent 自动调优研究。

当前阶段为论文设计、初稿写作与历史实验整理。已导入作者的 35 条探索性实验记录；这些记录尚不能验证所提完整 Agent 与技能复用方法。初稿 v0.2 的方法与主结果仍需实现、受控比较和留出测试支撑。

作者：**BoTao Cheng**；机构：**Tencent**。当前版本 **v0.2**，加入历史观测与技能约束；旧版本源文件见 `manuscript/versions/v0.1/`，PDF 保留。

## 从哪里开始

- [完整中文初稿](manuscript/main_zh.tex) 与 [中文 PDF](output/pdf/sglang_pd_agent_draft_zh_v0.2_jpdc.pdf)
- [英文初稿](manuscript/main.tex) 与 [英文 PDF](output/pdf/sglang_pd_agent_draft_v0.2_jpdc.pdf)
- [中文导读与证据边界](manuscript/README_中文导读.md)
- [文献核验记录](manuscript/research_ledger.md) 与 [共享参考文献](manuscript/references.bib)
- [诊断技能设计样例](manuscript/diagnostic_skills.design.json)：设计数据，不是可执行实现
- [版本变化](manuscript/CHANGELOG.md) 与 [Agent 实验交接](manuscript/agent_experiment_handoff_v0.2.md)
- [实验记录说明](experiments/README.md)
- [已有实验价值分析与证据审查](analysis/existing_experiments_2026-10-18/README.md)：逐行审查历史 CSV、描述性图表、对论文主题的帮助及补实验优先级。

根目录保存前期选题、期刊与实验设计调研。`32卡P800实验设计_2026-10-18.md` 是早期固定规模方案；当前资源规模按实际完整副本条件选择，以资源池方案和稿件为准。

## 论文素材库（article/）

`article/` 目录复制自 dsv4-pro 环境（2026-10-13 起整理），是本论文的前期调研与素材库：

- [P800-PD分离论文规划.md](article/P800-PD分离论文规划.md)：创新层级定位（L0–L3）、论文创新点 bullet、实验缺口清单（E1–E6）与投稿期刊清单（JSA/FGCS 首选，JPDC 等保底）。
- [同类论文阅读清单.md](article/同类论文阅读清单.md)：按相关度分组的对标文献（Beyond the Buzz、Vidur、DistServe、TaiChi 等），含每篇的划界句。
- [Ollama-vs-vLLM-并发LLM服务基准测试-中文翻译.md](article/Ollama-vs-vLLM-并发LLM服务基准测试-中文翻译.md)：Applied Sciences 基准测试论文的学习用中文翻译，单硬件平台 characterization study 的写作范本。
- `article/papers/`：13 篇参考论文 PDF 原文；`article/images/`：翻译稿配图；`applsci-16-05435-v3.pdf` 与 `extracted.txt` 为翻译底稿及提取文本。

该目录为只读素材，后续在 dsv4-pro 环境更新后需重新同步覆盖并提交。

## 两个环境交叉更新

当前同步位置为 [paper-reproduction-weekly](https://github.com/cbt12123/paper-reproduction-weekly) 仓库的 `20261018-SGLang-Diagnostic-Autotuning/` 目录；仓库中已有的其他论文复现内容独立保留。

首次在另一环境克隆（推送时需使用有写入权限的 GitHub 账号）：

```sh
git clone https://github.com/cbt12123/paper-reproduction-weekly.git
cd paper-reproduction-weekly/20261018-SGLang-Diagnostic-Autotuning
```

每次开始修改前，先在干净工作区更新：

```sh
git pull --ff-only
```

完成一批修改后检查差异、提交并推送，再切换到另一环境：

```sh
git status
git diff
git add <本次修改的文件或目录>
git commit -m "Describe the manuscript or experiment update"
git push
```

两个环境同时工作时，分别使用主题分支，例如 `writing/method-revision` 和 `experiments/p800-baseline`，合并完成后再更新 `master`。若 `pull --ff-only` 失败，先检查分支差异并合并或变基；不要用强制推送覆盖另一环境的工作。

中英文是同一研究的两份稿件。改动方法、公式、结论或文献后，应同步另一语言版本；尚未同步时，在提交说明中记录。LaTeX 与 BibTeX 是文本源文件，PDF 是阅读快照；只有重新编译并检查后才更新 PDF。

## 补充实验信息

实验环境首先补充能力清单与实际硬件/软件版本，再按 `experiments/README.md` 新建运行记录。实测数字需要关联运行 ID、配置、负载和统计口径。未执行实验保留未执行状态，不用估计值替代结果。原始大文件放在 Git 外部，仓库记录存储位置与校验信息。

## 本地构建

英文需要 Python、TeX Live（pdfLaTeX 和 BibTeX）。中文额外需要 XeLaTeX、ctex；当前中文源稿指定 Windows 字体集，在 Linux 上编译前需安装对应字体或调整 `main_zh.tex` 的 `fontset` 设置。

在项目根目录运行：

```sh
python manuscript/build_draft.py
python manuscript/build_draft_zh.py
```

检查及页面渲染还需要 PyMuPDF、Pillow 和 Poppler 的 `pdftoppm`：

```sh
python -m pip install -r requirements.txt
python manuscript/check_draft.py
python manuscript/check_draft_zh.py
```

检查脚本核对引用、页面边界及中英文结构，生成 `tmp/pdfs/` 下的页面图片；交付 PDF 前仍需人工查看渲染。临时编译与渲染文件、重复 ZIP、原始实验文件不会提交到 Git；中英文 PDF 阅读版会提交。
