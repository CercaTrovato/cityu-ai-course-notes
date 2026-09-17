# NOTICE · 版权、隐私与使用限制声明

> 这是我（香港城市大学 MSc 在读学生，GitHub：CercaTrovato）为**自己学习**建立、并选择公开的课程知识库。公开的目的是让其他人能够**复现或改进这套"AI 辅助笔记"的方法与工具**，以及让同课程的同学可以读笔记、挑错，**不是**为了传播课程材料。请在使用前完整阅读本声明。中文为准，英文摘要在文末。

---

## 1. 课程材料（`*/course_files_export/`）

这些目录下的讲义（PDF / PPTX）、课程大纲、作业 notebook、数据集等，**版权归各任课教师与香港城市大学所有**，我不拥有其任何权利。

- **禁止下载、转载、再分发或用于任何商业用途，除非已获得版权方的书面许可。**
- 保留在仓库中的唯一目的，是让笔记里的"讲义 p.X"引用、页码映射表和 `code/` 下的复现脚本有可核对的对象，便于他人检验这套方法的准确性。
- 数据集（`*.csv`）由任课教师提供、仅供课堂教学使用；其原始数据来源与授权条款以各文件所在讲义为准。
- **如版权方认为任何文件侵权，请通过本仓库的 Issue 或 commit 记录里的邮箱联系我，收到通知后我会立即删除相应文件并从历史记录中清除。**

## 2. 课堂转录（`*/transcripts/`）

这些文本是课堂录音经语音识别自动生成的转录稿（2026-09-18 起用本地 Whisper large-v3，此前用 Notta），**不是源音频**（音频不在仓库里），也不是逐字校对过的文字记录。

- 转录**可能存在大量识别错误**（专有名词、数字、术语），各笔记 §9.5 列出了已发现的错误样本；请勿把转录内容当作教师原话的准确记录。
- 转录中的发言内容属于任课教师；公开仅为让笔记中"🎙️ 课堂补充"的引用可回溯。**禁止用于任何与本课程学习无关的目的。**
- 如任课教师或学校不希望转录公开，请联系我，我会立即删除。

## 3. 笔记与规则（`*/notes/`、`*/_meta/`、`_meta/`、`.claude/`）

笔记正文是我借助 AI 工具（Claude Code）从讲义与转录中整理、改写并复核的**二次创作**，其中：

- 引用讲义原文与教师口述的部分，版权归原作者；
- 我自己的解释、算例、误解辨析、规则文件与脚本，按 `LICENSE.md` 的条款开放。
- **笔记可能有错**。每篇笔记的 §9.3 / §9.5 记录了已知的讲义问题与待核对项，但不保证完整。请以官方材料为准，尤其在考试与作业中。

## 4. 个人信息

- 仓库不含我的学号、密码、私钥、同步服务配置或任何私人通信（已通过 `.gitignore` 排除）。
- 教师姓名与办公邮箱来自公开的课程大纲；助教与同学的个人邮箱已在笔记中隐去。如仍有遗漏，请联系我删除。

## 5. 不构成任何背书

本仓库与香港城市大学及任何任课教师**无隶属关系**，未经其审阅或认可。笔记中对课程、考核、评分的推断均标有可信度等级（🔴 教授明示 / 🟡 大纲反推 / ⚪ 笔记推断），⚪ 级内容尤其可能出错。

---

## Summary (English)

This repository is my personal study knowledge base (I am an MSc student at CityU; GitHub: CercaTrovato), made public so that others can **reproduce or improve the AI-assisted note-taking workflow and tooling** — not to redistribute course materials.

- **Course materials** under `*/course_files_export/` (slides, syllabi, notebooks, datasets) are © their respective instructors and City University of Hong Kong. **Do not download, redistribute or reuse them without written permission from the copyright holders.** They are kept only so that page references and reproduction scripts can be verified. **Copyright holders: contact me (Issue, or the email in the commit log) and the files will be removed immediately, including from git history.**
- **Transcripts** under `*/transcripts/` are automatic speech-recognition output (local Whisper large-v3 from 2026-09-18; Notta before that), **not source audio and not verified verbatim records** — audio files are never committed; they contain recognition errors. They are kept only so that quoted classroom remarks in the notes can be traced. Instructors may request removal at any time.
- **Notes, rules and scripts** are my own derivative work; see `LICENSE.md`. Notes may contain errors — official materials prevail.
- No affiliation with, and no endorsement by, City University of Hong Kong or any instructor.
