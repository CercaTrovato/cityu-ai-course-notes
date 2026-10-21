# Olist 小组项目工作区

状态：draft。2026-09-30 用户确认本项目属于 IS6400；6 人各自探索一个角度，不预先锁定延迟预测。

## 从这里开始

1. 用 Jupyter 打开 `olist-data-guide.ipynb`。从本目录启动时无需改路径；否则在第一格设置 `WORK_DIR`。
2. 首次阅读先看 §1–4：文件、九张表、52 个字段位置、连接关系；再读时间、金额、评价与六个方向。
3. `olist-data-guide.html` 是同一 Notebook 的标准 nbconvert 导出，只读即可看已有输出；不是提交版。

## 文件

- `data/source/olist-v2.zip`：Kaggle 官方原始包；只读保留。
- `data/raw/`：9 个原始 CSV；不得直接覆盖或清洗后写回。
- `data/source-manifest.json`：来源 URL、版本、许可、下载时间及逐文件 SHA-256。
- `olist-data-guide.ipynb`：完整教学及可运行探索；运行不联网、不写原始数据、不建模。
- `olist-data-guide.html`：同源阅读版。

正式分析后续另开 Notebook；不要把清洗数据或结果当作官方原件。团队内部使用按 CC BY-NC-SA 4.0 保留归属；本目录被 Git 忽略，不公开个人完整作业。

## 边界

现阶段是数据熟悉，尚未确定成员题目、最终汇报结构或结论。Canvas Announcements 尝试访问后跳转登录，Assignments/Files/Modules 的本轮现行要求也未完成核验；沿用本地任务说明，保持 draft。全库备份与私有完整性快照在 `D:/上课资料/CityU_backups/olist-20260930/`。
