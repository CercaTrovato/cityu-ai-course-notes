# 给文档个人助手：如何安排每日事项

1. 先读 `progress/daily-plan.json`，再按任务 ID 回到 `progress/timeline.json`。`TIMELINE.md` 是同源的人类阅读版。
2. 检查 `as_of`、`observed_on` 和最新 GitHub 提交。文件更新不代表所有事项重新核验；超过七天或有新回件，先向总监督核实。
3. `readiness=ready` 只表示已登记前置满足，可以提出安排；`verify` 先核状态，`waiting_dependency` 等前置成果，`waiting_external` 等回件。不要把给组员的任务排成本人执行任务。
4. `target.basis=official` 是正式节点，`agreed` 才是确认安排，`proposed` 只是建议。无时刻的日期不能补成 23:59；`before_date` 表示该日前。当天及已过日期要按 Asia/Shanghai 重新计算，不能照用旧导出的紧急程度。
5. 工时未知为 null，不当作零分钟。`my_next_action` 是总监督可以做的具体动作；提出每日候选后还需结合本人日历、空闲时间和确认，不自动创建日程、承诺交期或替本人发送消息。
6. 已完成指标题所述阶段。收到初稿、验收、团队定稿和正式提交分别记录；观察日期不冒充实际完成日期。
7. 依赖中的 `dependency_gates` 可只要求上游部分验收项通过，而非整个上游完全结束。`acceptance` 记录 pass/gap/unknown；history 记录状态变化，后续更新追加事实，不抹去旧阶段。

私有仓库需要个人助手通过其已有 GitHub 授权读取。不要将访问令牌、登录 Cookie 或私人材料复制到提示词或公开地址。

维护者每批更新：核事实 → 原子维护 timeline.json 和 history → 同源生成 Markdown 与每日事项 JSON → GitHub 推送并核远端 → 本地看板 → 线上发布回读。保留 task ID，关闭已补齐的缺口，未确认日期和成员状态如实标注。
