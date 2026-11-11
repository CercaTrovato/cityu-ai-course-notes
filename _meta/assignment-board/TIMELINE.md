# 项目时间线与每日事项数据

## 同一份事实，三个阅读入口

各课程 `assignment/graded/Axx-*/timeline.json` 是精细进度与未来安排的本地权威记录。GitHub 的 `progress/timeline.json` 保持同版本；`TIMELINE.md` 和 `progress/daily-plan.json` 从它生成。看板读取 timeline.json，线上发布同一课程快照，不能分别手写三套相互冲突的进度。

每门课有自己的 GitHub 仓库，入口清单见 [timeline-index.json](timeline-index.json)。时间线包括已完成、当前推进／待核和未来计划；不以文件存在推定完成，不把组员自报当验收。

## 每批必更新

1. 读取最新远端和本课 assignment.json、管理验收、timeline.json，先核新增事实和差异。保护组员新提交，禁止旧本地覆盖新远端。
2. 保留任务 id，更新负责人、状态、实际结果、下一步、依赖、验收和证据；状态变化追加 history。本人同意与团队承诺必须有真实来源。
3. started_on、completed_on 只记已知实际日期；未知为 null。observed_on 是本次事实核验日期。target 的 official/agreed/proposed/unknown 分别表示正式截止、已确认安排、内部建议和未定。工时 estimated_minutes 未估计为 null。
4. 确保本批时间线已复核，再刷新 basis_revision 为本课 assignment.json 的 SHA-256，basis_management_revision 为管理配置本课对象的排序 JSON SHA-256。不能只改指纹掩盖未审变化。源更新时看板标待复核，不把旧个人事项当当前可执行。
5. 用 `_meta/assignment-board/timeline.py --id <作业编号> --output <已确认仓库目录>` 同源生成 TIMELINE.md、progress/timeline.json、progress/daily-plan.json 和 ASSISTANT-README.md；原子写、回读并检查差异。目标目录必须先完成远端合并，不能用导出命令覆盖组员的新版本。
6. 同步 GitHub 成果与当前进度入口、推送并核远端；本地看板回读后同批发布线上，分别给三处回执。详见 [SUPERVISION.md](SUPERVISION.md) 和 [ONLINE-SYNC.md](ONLINE-SYNC.md)。

## 给个人助手的边界

助手读 daily-plan.json 后按 task id 回 timeline.json 查证据。只将本人负责或 my_next_action 明确的事项作为个人候选；等待外部或依赖未满足的执行任务不排成可立即开始。先核真实日期和最新版本，建议日期不当作约定，未知用时不当零。时间线不能代替本人日历，也不授权自动发送消息或提交作业。

GitHub 私有仓库继续要求助手具备已有访问授权；不把令牌写入索引。组员在线上看板仍只能查看自己课程及下载获准资料。
