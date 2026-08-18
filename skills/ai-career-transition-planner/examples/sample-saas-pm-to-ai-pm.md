# Example: B2B SaaS PM → AI Agent PM / 示例：B 端 SaaS 产品经理转 AI Agent 产品经理

## Input / 输入

> 我做了 3 年传统 B 端 SaaS 产品经理，主要负责审批流和 CRM，没有任何 AI 经验，想转型 AI Agent 产品经理，每天有 1.5 小时。希望在 10 个工作日内开始投递。

## Expected diagnosis excerpt / 预期诊断节选

### Career destination / 职业定位

- **Primary role / 主目标岗位:** AI Agent Product Manager
- **Adjacent role / 相邻岗位:** AI Application Product Manager
- **Positioning / 定位:** Understands enterprise entities, approval rules, exception handling, and cross-role handoffs; transitioning this deterministic workflow expertise into AI-assisted task orchestration with measurable human oversight.

### Evidence translation / 经历翻译

| Existing evidence / 原有经历 | Transferable AI-product capability / 可迁移 AI 产品能力 | Claim boundary / 主张边界 |
|---|---|---|
| Designed approval flows with conditions and escalation rules | Can define agent states, deterministic guardrails, approval gates, and exception paths | Do not claim to have built an agent without a real agent project. |
| Owned CRM fields, status definitions, and permissions | Can model domain entities, tool inputs/outputs, access boundaries, and structured data quality | Do not call CRM data an AI knowledge base until freshness, permission, and retrieval needs are assessed. |
| Managed manual handoffs between sales and operations | Can identify human-in-the-loop boundaries and measure handoff rate | Do not claim automation savings without measured evidence. |

### Core transition lesson / 核心转型课题

Traditional approval flows are mostly deterministic: a defined condition triggers a defined state transition. An AI agent introduces probabilistic steps, such as interpreting a request or drafting a recommendation. The PM must keep irreversible approvals, permissions, and policy checks deterministic, while specifying acceptable AI quality, confidence/failure handling, fallback, and human escalation.

### Model decision example / 模型决策示例

For high-volume ticket classification, begin with a lower-cost, lower-latency model plus sampled quality checks. For a complex contract-risk summary, use a stronger model only if evaluation shows that the quality gain justifies the added cost and wait time; retain a human approval step before any action.

### Day 1 task / 第 1 天任务

**Goal / 目标:** Explain why an agent is not simply an automated approval flow.

**Learn / 学习:** Deterministic rules, probabilistic model output, guardrails, fallback, and human-in-the-loop.

**Apply / 应用:** Redraw one previous approval flow. Mark the steps that must remain rules, the one step that an AI model could assist, and the human approval boundary.

**Output / 产出:** One annotated flow and a 60-second answer.

**Done when / 完成标准:** The answer names one user benefit, one failure mode, one guardrail, and one metric.

**Time / 时长:** 90 minutes.
