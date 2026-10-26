# 工作文件入口

先读 [开始这里](../notes/开始这里.md)，再用 Jupyter 打开 [逐步实操 Notebook](EF5560-A01-逐步实操.ipynb)。Notebook 是唯一完整教学和分析源码。

- `output/`：Notebook 生成的三表、Figure 1–4、Figure A1、结果 JSON 与权重。
- `build_report.py`：从既有结果生成 7 页正文＋1 页附录 PDF。
- `package_draft.py`：官方 checker、草稿权重与清除输出的 Notebook 源码 ZIP。
- `safe_write.py`：原子保存辅助代码。

原始 course_files_export 只读，所有提交件仍为 DRAFT。独立复现时从 ZIP 解压目录启动 Jupyter，在第一格设置数据路径，然后 Restart & Run All。


## 2026-10-27 · A01 本次教学重审记录

A01导览与115格实操Notebook已分别完成全范围独审及原审定向复核；新增原题中英对照、模型手例与行业上限流程图。仅20格Markdown source变化，全部代码/保存输出/执行计数/metadata保持；未重训或改正式报告/CSV/ZIP。结构/AST与实际标准HTML显示已核，主写者已在隔离副本补核原生JupyterLab的LASSO公式、旧输出与行业cap流程；Markdown检查器仍不支持ipynb，不冒称其PASS。原生结构/36代码AST/全cell保持性、实际独审与原生必要显示构成本次适用验收，不代表新执行。10/21既有邮件库记录已见10/12提交，本次不改本人状态；当前Canvas/评分/上传附件未新核。原主写者已接受真实候选并完成CAS原子写回/精确回读；原发布计划内两个整文件candidate_file为过期副本，已按同计划operations.source及真实独审SHA使用最终原字节，未使用过期副本。新增SVG仅尺寸维护530×1662，节点/边/文字不变。
