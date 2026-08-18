# AI 产品职业与学习工具包

这是一个通用的 Agent Skills 工具包，帮助用户转向 AI 相关的设计、UX、产品、Agent 或体验岗位，也可用于系统学习 AI 产品知识。

它会根据用户的真实经历、目标岗位要求和学习偏好生成个性化路线，再用对话式学习帮助用户建立知识之间的连接。

核心采用通用目录约定：`skills/<skill-name>/SKILL.md`。

## 包含的 Skill

- `ai-career-transition-planner`：职业方向、经历证据与能力缺口诊断。
- `ai-career-sprint-plan`：个性化学习路线，包含 AI 主线与产品基础双轨安排。
- `adaptive-ai-learning-coach`：多轮对话学习、发散问题处理、应用题、进度与学习日志。
- `ai-career-case-strategy`：将真实项目整理为可信案例。
- `ai-career-interview-positioning`：准备自我介绍、面试回答和反问。

## 如何使用

在支持 Agent Skills 的编码 Agent 或运行时中，使用该平台的安装方式。支持 `skills.sh` 的环境可按需安装单个 Skill，例如：

```bash
npx skills add lannn55555-byte/ai-product-career-learning --skill adaptive-ai-learning-coach
```

常见路径是：职业诊断 → 学习计划 → 对话学习；案例策略和面试表达在后期按需使用。

不同平台的安装命令、Skill 发现方式、可访问的文件与工具会不同。安装后请在平台内检查相应 Skill 是否已经被发现。

## 学习设计

默认的 10 天是“建立连接的基础冲刺”，不是术语清单，也不承诺十天后就具备岗位能力。

学习从同一张 AI 产品系统图开始：模型行为、任务上下文、外部知识、工具与后端动作、状态/规则/人工接管、用户控制与恢复、评估与可观测性。之后每学一个主题，都会回到一个锚点场景，说明系统图中哪一部分发生了变化、为什么需要它、它不能解决什么。

学习不会只考记忆。每个能力节点都有 0–5 的掌握度：见过、能识别、能解释、能做判断、能设计、能迁移。基础冲刺结束后，用户需要用一个没有见过的新场景重建系统，并说明组件选择与取舍。

AI 主线与产品基础分别记录进度，但会通过明确的设计问题连接：例如 RAG 与事实来源/信息架构、Tool Calling 与服务蓝图/决策表、Agent 状态与用户旅程、评估与指标研究。

## 网页聊天产品

网页聊天产品不会使用与编码 Agent 相同的本地 Skill 安装流程。可使用平台原生的定制形式，例如 Gem 或自定义指令。GitHub 链接有时只能提供临时阅读上下文，具体行为取决于平台。

## 使用原则

默认采用“对话优先 + 阶段性 Markdown 记录”：学习和协作发生在对话中；仅在诊断确认、学习路线确认、重要学习节点、案例确认或面试材料确认后，才生成可编辑文件。如果平台不能写入工作区，应返回有明确标题、可直接复制保存的 Markdown 内容。

所有交接信息都应由用户可见、可纠正，不传递完整对话或隐藏推理。

## 语言与本地化

原始 Skill 指令和供 Agent 使用的参考资料全部为英文。给用户的模板与示例按语言分开存放在 `en/` 和 `zh-CN/`；一次产出只使用一种语言，不在同一文件内中英混排。

## 示例

示例供浏览仓库的人理解输出形式，Skill 不会把它们当作运行指令。

- [中文职业诊断输出](../examples/zh-CN/career-diagnosis-output.md)
- [中文职业转化模式](../examples/zh-CN/role-translation-patterns.md)
- [English career-diagnosis output](../examples/en/career-diagnosis-output.md)
- [English role-translation patterns](../examples/en/role-translation-patterns.md)

## 隐私

不要提交真实简历、学习日志、面试记录、联系方式、密钥或公司保密信息。公开示例必须匿名，并保持个人贡献与团队贡献的边界。
