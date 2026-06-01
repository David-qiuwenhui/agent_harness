# Agent 框架调研报告

> 调研时间：2026-05-30
> 项目背景：SaaS 电子流系统，需独立部署 Agent 能力

## 项目约束

| 维度 | 选择 |
|------|------|
| 后端技术栈 | Java 体系，Agent 服务独立部署不耦合 |
| Agent 技术栈 | Python |
| LLM | 国产模型（Qwen / DeepSeek / GLM，OpenAI 兼容接口） |
| 部署方式 | 私有化部署 |
| MVP 范围 | 文档比对 + 智能填写/生成 |
| 团队背景 | 前后端开发，Python 为主，AI 辅助开发模式 |
| 用户交互 | 嵌入式对话窗口 + 独立 Agent 工作台 |

## 调研框架一览

| 框架 | 语言 | 定位 | 适合度 | 核心理由 |
|------|------|------|--------|----------|
| **Dify** | Python | 低代码 Agent 平台 | 高 | 直接面向业务 Agent 场景，开箱即用 |
| **LangGraph** | Python | 灵活 Agent 编排框架 | 高 | 最大灵活性，适合复杂编排 |
| **Spring AI** | Java | Spring 生态 AI 框架 | 高 | 团队零学习曲线，但与 Python 路线冲突 |
| **Agno** | Python | 轻量 Agent 框架 | 中 | 快速 MVP，但生态不如 Dify/LangGraph |
| **LangChain4j** | Java | Java Agent 框架 | 中高 | 非 Spring 项目的 Java 首选 |
| **Hermes Agent** | Python | 自主学习 Agent | 中低 | 自学习有亮点，但太年轻（2026.02 发布） |
| **OpenCode** | Go | 终端编码助手 | 低 | 编码助手，非 Agent 构建框架 |

## 排除的方案

### OpenCode — 不适合

OpenCode 是终端 AI 编码助手（类似 Claude Code / Cursor），定位是帮开发者写代码。

- 设计意图：开发者工具，面向代码编辑场景
- 知识库 / RAG：无原生支持
- 文档比对 / 表单填写：不在能力范围内

关键区分：OpenCode 是"AI 助手"（成品），不是"Agent 构建框架"（积木）。我们的场景需要积木。

### Hermes Agent — 有亮点但需谨慎

Nous Research 出品的自主学习 Agent（GitHub 60K-95K+ stars），核心卖点是"越用越聪明"。

亮点：
- 自学习机制（Skill 自动提炼）与"预提供领域知识 + Skills + Tools"思路天然契合
- 5 层持久化记忆系统
- 6 种执行后端（local / Docker / SSH 等）
- 原生 MCP 支持

风险：
- 2026 年 2 月才发布，API 稳定性未经验证
- 本质是通用自主 Agent，非 SaaS 嵌入导向
- 自学习 Skill 质量不可控，业务场景中可能生成"幻觉 Skill"
- 文档比对等结构化任务，靠自学习不如显式编排可靠

折中思路：用 Dify / LangGraph 做主体框架，借鉴 Hermes 的 Skill 自动提炼模式作为增值能力。

### Spring AI — 适合但不符合 Python 路线

Spring AI 是 Java 生态中最成熟的 AI 框架，GA 状态，原生 Spring 集成。

优势：
- 团队零学习曲线（Java 原生）
- `@Tool` 注解直接注册方法为 Agent Tool
- Advisors API（可组合的请求/响应拦截器）
- Structured Output（LLM 响应直接映射 Java Record）
- Spring AI Alibaba 原生支持 Qwen
- 生产稳定性（GA + Spring 运维工具链）

关键张力：团队已决定 Agent 侧用 Python（生态更丰富，灵活切换框架），Spring AI 意味着 Agent 也是 Java，与决策冲突。如果未来考虑混合架构，Spring AI 值得重新评估。

## 最终策略：分阶段推进

1. **阶段 1（MVP）— Dify**：快速验证文档比对和智能填写两个核心场景
2. **阶段 2（深化）— LangGraph**：当 Dify 表达力不够时，复杂逻辑迁移到 LangGraph
3. **两者共存**：Dify 做简单场景，LangGraph 做复杂编排

## 参考资料

- [Java AI Agent 框架对比 2026](https://codewiz.info/blog/java-ai-agent-frameworks-2026/)
- [2026 开源 Agent 框架对比](https://www.tencentcloud.com/techpedia/144032?lang=en)
- [Hermes Agent GitHub](https://github.com/nousresearch/hermes-agent)
- [Spring AI 官方文档](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [Spring AI Alibaba](https://github.com/LLLLLLLLM/spring-ai-alibaba-update)
- [OpenCode 官网](https://opencode.ai/)
