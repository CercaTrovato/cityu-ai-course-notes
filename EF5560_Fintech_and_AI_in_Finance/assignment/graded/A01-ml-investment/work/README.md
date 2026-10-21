# 工作文件入口

先读 [开始这里](../notes/开始这里.md)，再用 Jupyter 打开 [逐步实操 Notebook](EF5560-A01-逐步实操.ipynb)。Notebook 是唯一完整教学和分析源码。

- `output/`：Notebook 生成的三表、Figure 1–4、Figure A1、结果 JSON 与权重。
- `build_report.py`：从既有结果生成 7 页正文＋1 页附录 PDF。
- `package_draft.py`：官方 checker、草稿权重与清除输出的 Notebook 源码 ZIP。
- `safe_write.py`：原子保存辅助代码。

原始 course_files_export 只读，所有提交件仍为 DRAFT。独立复现时从 ZIP 解压目录启动 Jupyter，在第一格设置数据路径，然后 Restart & Run All。
