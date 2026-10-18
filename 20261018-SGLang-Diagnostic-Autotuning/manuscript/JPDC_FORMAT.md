# JPDC 投稿格式整理

2026-10-18：当前 v0.2 正文迁移到 Elsevier `elsarticle`，采用 `preprint,12pt` 单栏投稿版式；英文为目标投稿稿，中文为同结构内部对照稿，不是 JPDC 的中文投稿模板。

作者：BoTao Cheng；机构：Tencent。此次不新增或更改实验结果。版本记录保留在 CHANGELOG.md，PDF 不展示版本说明、工作进度或起草日期。首页仅保留普通页码，避免模板默认的“Preprint submitted to”字样被误读为已经投稿。

## 来源与核验边界

- [Elsevier 官方 LaTeX 说明与模板入口](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions)
- [JPDC 作者指南](https://www.sciencedirect.com/journal/journal-of-parallel-and-distributed-computing/publish/guide-for-authors)

官方通用说明已核对，JPDC 专属作者指南本轮返回 HTTP 403。因此当前是以 JPDC 为目标的官方通用模板适配，不宣称已逐项核验期刊所有投稿条件。编号文献采用官方 `elsarticle-num.bst`。通讯邮箱、机构详细地址以及投稿声明须在正式投稿前依据作者真实信息与最新指南补齐，本轮不虚构。

## 构建与文件

在仓库根目录运行：

```powershell
python manuscript/build_draft.py
python manuscript/build_draft_zh.py
python manuscript/check_draft.py
python manuscript/check_draft_zh.py
```

英文需要 TeX Live 的 elsarticle、BibTeX 与 pdfLaTeX；中文另外需要 XeLaTeX、ctex 和 Windows 中文字体。源文件为 main.tex、main_zh.tex，共享 references.bib 与 figures。模板迁移前的 v0.2 源文件保存在 versions/v0.2_pre_jpdc。

新 PDF 为 output/pdf/sglang_pd_agent_draft_v0.2_jpdc.pdf 与 output/pdf/sglang_pd_agent_draft_zh_v0.2_jpdc.pdf。

另提供英文扁平源文件包，便于迁移和后续投稿系统编译。该包为格式预备包，不代表实验和全部投稿材料已经完成。中文与工作文档留在双语工作包，不放入英文投稿源文件包。
