# Classification 图源与复算记录

对应 M06 / T07（2026-10-14）。SVG 是正式教学图；JSON 为复算与来源记录，原件在 course_files_export 只读。

代码是实际核对过的源码存档。复算前复制到 E:/app-data/codex/scratchpad/ 的独立工作目录，先把输出路径指向该目录；不要让复算覆盖 vault。原 lecture-a/calc.py 与 lecture-b/calc.py 的结果名相同，分别在不同子目录运行；源码含路径设置，应先读。教程脚本显式使用本轮 scikit-learn 1.5.1 与种子口径，未声称原 Notebook 软件版本相同。

最终数值图由 render_figure.py 排版，包含可检索文字。它使用 calc-tutorial.py 已核对的两张混淆矩阵及同参数合成散点。15张流程图的可编辑源直接在两篇笔记的 Mermaid 块中。

extra-results.json 的 additional_checks 由同任务 finish_scopes.py 中的 math.hypot/exp/log 当场追加；不是初版 calc-extra.py 的自动输出。其输入分别为(3,4)、-1/+1、错误率0.25、概率0.51/0.51/0，本记录公开这一边界。

远端 CSV/ipynb 原始字节未重新下载做哈希比对；HTML题面通过现有已登录Canvas预览核对。原课程数据字典缺口、AdaBoost差异和正式截止待核见制作验收记录。
