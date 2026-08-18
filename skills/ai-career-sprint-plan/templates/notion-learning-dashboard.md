# Notion Learning Dashboard / Notion 学习看板

Use this guide after the Skill has produced an accepted diagnosis and sprint plan. Start manually; do not build an API integration for a first use.

在 Skill 已生成并确认诊断与冲刺计划后使用本指南。首次使用请手动搭建，不要急于连接 API。

## 1. Create the dashboard / 创建首页

Create a Notion page called `AI Career Transition Dashboard / AI 职业转型看板`.

Add three sections:

1. `Career Diagnosis / 职业诊断` — paste or import the generated `career-diagnosis.md`.
2. `Current Sprint / 当前冲刺` — embed the task database created below.
3. `Interview Cards / 面试回答卡` — paste the generated answer cards and update them after interviews.

## 2. Create one task database / 创建一个任务数据库

Create a full-page table database named `AI Career Sprint / AI 职业冲刺`. Add these properties:

| Property / 属性 | Type / 类型 | Purpose / 用途 |
|---|---|---|
| Task / 任务 | Title | One concrete daily task. |
| Day / 天数 | Number | Sprint sequence, such as 1–10. |
| Topic / 主题 | Select | LLM, Prompt, Product, RAG, Agent, Evaluation, AI UX, Data, Case, Interview. |
| Goal / 目标 | Text | Capability the task is intended to build. |
| Time (min) / 时长 | Number | Planned focused minutes. |
| Status / 状态 | Status | Not started, In progress, Done, Blocked. |
| Output / 产出 | Text | Knowledge card, decision note, answer, or link. |
| Done when / 完成标准 | Text | Observable completion criterion. |
| Source link / 来源链接 | URL | Link to a Markdown file, Notion note, or project artifact. |
| Due date / 截止日 | Date | Optional; use only when the sprint has fixed dates. |

## 3. Add views / 添加视图

- **Today / 今日:** Filter `Status` is not `Done`; sort by `Due date`, then `Day`.
- **Sprint / 冲刺全览:** Table grouped by `Status`.
- **Topics / 主题复盘:** Board grouped by `Topic`.
- **Blocked / 阻塞项:** Filter `Status` is `Blocked`.

Do not create separate databases for every concept. One task database is enough for the first sprint.

## 4. Move a Skill output into Notion / 将 Skill 输出导入 Notion

1. Import or paste `career-diagnosis.md` into the `Career Diagnosis` section.
2. Copy the `Task import rows / 任务导入行` table from the Skill output.
3. Paste its rows into the matching columns of `AI Career Sprint`.
4. Open each task page only when needed; add the detailed study note, link, and final answer there.
5. At the end of each day, update `Status`, attach the output link, and add one sentence about what remains unclear.

Notion can import Markdown as pages and CSV as databases. Use CSV only when you already have a prepared task table; do not expect a CSV import to update existing rows automatically.

## 5. Optional automation after one manual sprint / 完成一轮后再考虑自动化

Only automate a repeated, stable action. A safe first workflow is:

```text
Accepted plan → structured task rows → create Notion task pages → human reviews → user starts learning
```

For a personal workspace, create a Notion internal connection, share only the target database with it, and have a script or no-code platform create task pages from the approved rows. Never paste the access token into a public repository or Skill output. For a public product, use an OAuth connection so each user authorizes access to only their workspace.

## Feishu Bitable alternative / 飞书多维表格替代方案

Create the same fields in a Bitable table, then paste or import the `Task import rows`. Use it when reminders, views, and data-based workflow automation matter more than a polished personal knowledge base. Add automation only after the task fields and status transitions are stable.
