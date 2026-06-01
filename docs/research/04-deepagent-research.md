# DeepAgent 深度研究报告

*生成日期: 2026-06-01 | 来源数: 20+ | 置信度: High*

---

## Executive Summary

"DeepAgent" 实际上指代**两个完全不同的项目**：

1. **DeepAgents (LangChain)** — 生产级开源 Agent 框架，2026 年 3 月发布，被称为"开源版 Claude Code"
2. **DeepAgent (RUC-NLPIR)** — 中国人民大学的学术研究项目，WWW 2026 论文，专注动态工具发现

两者不相关。**对 agent_harness 项目有直接参考价值的是 LangChain 的 DeepAgents**。

---

## 1. DeepAgents (LangChain) — 生产级 Agent 框架

### 1.1 基本信息

| 项目 | 信息 |
|------|------|
| 仓库 | [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) |
| JS 版本 | [langchain-ai/deepagentsjs](https://github.com/langchain-ai/deepagentsjs) |
| Java 版本 | [langgraph4j/langgraph4j-deepagents](https://github.com/langgraph4j/langgraph4j-deepagents) |
| 创建者 | LangChain（LangChain/LangGraph 生态公司） |
| 发布时间 | 2026 年 3 月 15 日 |
| 定位 | 长时间、多步骤、产物密集的 Agent 工作流框架 |
| 安装 | `pip install deepagents` |
| 模型支持 | Claude / GPT / Gemini / DeepSeek / Llama / Mistral 等 |

### 1.2 四大核心支柱

#### 支柱 1：Planning Tool (write_todos)

将任务规划作为一等工具，而非硬编码在 prompt 中：

- 内置 `write_todos` 工具进行任务分解和进度追踪
- 嵌套 TODO 支持复杂任务的层级分解
- 与 Junie/Cursor/Kiro 的规划模式类似

#### 支柱 2：Sub-agent Isolation (子代理隔离)

解决上下文爆炸问题：

- 生成专门的子代理，拥有独立的上下文窗口
- 主代理只接收最终结果，不接收中间工具调用
- 支持异步子代理进行并行工作

#### 支柱 3：Filesystem as Shared Workspace

文件系统作为共享工作空间：

- 替代纯内存传递，中间结果写入文件
- 支持跨长任务的持久化状态
- Virtual filesystem 访问（read/write/edit/search）

#### 支柱 4：Auto Context Management

自动上下文管理：

- 自动对话压缩中间件
- 减少工作内存体积同时保留重要细节
- SummarizationMiddleware 自动触发

### 1.3 关键技术特性

| 特性 | 说明 |
|------|------|
| 中间件架构 | TodoListMiddleware、FilesystemMiddleware、SubAgentMiddleware、SummarizationMiddleware、HumanInTheLoopMiddleware |
| 存储后端 | StateBackend（临时）、FilesystemBackend（磁盘）、StoreBackend（持久化）、CompositeBackend（混合路由） |
| MCP 支持 | 通过 langchain-mcp-adapters 集成 MCP 工具服务器 |
| CLI 工具 | 命令行工具，支持构建带持久记忆的编码 Agent |
| 安全模型 | "Trust the tools, not the model" — 工具级别限制，非 prompt 护栏 |
| TerminalBench 2.0 | ~42.65%（Sonnet 4.5），与 Claude Code 水平相当 |

### 1.4 核心架构图

```
+-----------------------------------------------------------+
|                    User / CLI / API                        |
+---------------------------+-------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                   DeepAgents Runtime                       |
|                                                           |
|  +------------------+  +-------------------------------+  |
|  | Planning Engine  |  | Context Management            |  |
|  | (write_todos)    |  | (Auto-compress + summarize)   |  |
|  +------------------+  +-------------------------------+  |
|                                                           |
|  +------------------+  +-------------------------------+  |
|  | Sub-agent Pool   |  | Filesystem Workspace          |  |
|  | (isolated ctx)   |  | (persistent state)            |  |
|  +------------------+  +-------------------------------+  |
|                                                           |
|  +-----------------------------------------------------+ |
|  |              Middleware Pipeline                      | |
|  |  Todo | FS | SubAgent | Summarize | HumanInLoop     | |
|  +-----------------------------------------------------+ |
+---------------------------+-------------------------------+
                            |
                            v
+-----------------------------------------------------------+
|                   LangGraph Runtime                        |
|           (durable execution + streaming)                  |
+---------------------------+-------------------------------+
                            |
                            v
                   +-----------------+
                   |       LLM       |
                   |  (任意模型)      |
                   +-----------------+
```

---

## 2. DeepAgent (RUC-NLPIR) — 学术研究

### 2.1 基本信息

| 项目 | 信息 |
|------|------|
| 仓库 | [RUC-NLPIR/DeepAgent](https://github.com/RUC-NLPIR/DeepAgent) |
| 论文 | [arxiv.org/abs/2510.21618](https://arxiv.org/abs/2510.21618) |
| 会议 | WWW 2026（已接收） |
| 荣誉 | Hugging Face Daily Paper #1（2025 年 10 月） |
| 创建者 | 中国人民大学 RUC-NLPIR 实验室 |

### 2.2 核心创新

- **统一推理循环**：单一连续思考循环，决定何时搜索工具、何时调用、何时推理
- **按需工具发现**：不依赖预定义工具集，执行中按语义查找工具索引
- **记忆折叠 (Memory Folding)**：压缩中间推理步骤和工具使用历史，防止上下文溢出
- **可扩展工具集**：新工具可添加而无需模型微调

### 2.3 与 agent_harness 的关系

学术价值高，但实用性有限。工具发现机制的理念可借鉴，但实现需要大幅改造才适合生产。

---

## 3. 框架对比

### 3.1 DeepAgents vs 主流框架

| 维度 | DeepAgents | LangGraph | CrewAI | AutoGen | Dify | Claude Code |
|------|-----------|-----------|--------|---------|------|-------------|
| 定位 | 长链路 Agent 骨架 | 通用 LLM 框架 | 多角色协作 | 多代理对话 | 低代码 AI 平台 | 代码 Agent |
| 模型 | 任意 | 任意 | 任意 | 主要 OpenAI | 任意 | 仅 Claude |
| 上下文管理 | 自动压缩+隔离 | 手动 | 有限 | 有限 | N/A | 内置 |
| 生产就绪 | 中（较新） | 成熟 | 中 | 中 | 成熟 | 成熟 |
| 学习曲线 | 中高 | 高 | 低中 | 中 | 低 | 低 |
| 适用场景 | 长链路工程任务 | 通用 | 团队模拟 | 研究 | 业务快速落地 | 软件开发 |

### 3.2 关键差异

**DeepAgents vs Claude Code**
- DeepAgents 核心差异化：模型灵活性，不绑定特定 LLM
- 安全模型不同：工具级别限制 vs prompt 护栏
- DeepAgents 直接受 Claude Code 启发，LangChain 逆向工程了其模式

**DeepAgents vs Dify**
- Dify 是低代码平台，面向非技术用户
- DeepAgents 是代码优先的框架，面向开发者
- 非直接竞争：Dify 适合业务快速落地，DeepAgents 适合深度定制

---

## 4. 社区评价

### 4.1 正面

- TODO 列表模式被公认为有效的规划方法 ([HackerNews](https://news.ycombinator.com/item?id=44761299))
- 子代理隔离解决了真实痛点
- 文件系统作为工作空间是务实的设计选择
- Context Engineering 作为独立系统问题的思路得到认可 ([Towards AI](https://pub.towardsai.net/deepagents-the-open-source-framework-for-building-long-horizon-ai-agents-b2b97a0332e3))

### 4.2 负面

- "只是 agents+tools 加上新术语" — 质疑创新性
- 继承了 LangChain 的品牌包袱（社区对复杂性和 breaking changes 有历史不满）
- 项目较新，缺乏大规模生产验证
- 抽象层过多，调试困难

### 4.3 社区主流态度

**谨慎乐观** — 认可设计理念但担心生产稳定性。常见建议："先用 LangGraph 原生，遇到上下文管理瓶颈再考虑 DeepAgents"。

---

## 5. 对 agent_harness 项目的参考价值

### 5.1 值得借鉴的设计

| 模式 | 参考价值 | 备注 |
|------|----------|------|
| 自动上下文压缩 | 极高 | 长对话场景必备，learn-claude-code 也有类似实现 |
| 子代理隔离 | 高 | 财经场景的多步骤审批可能需要 |
| 规划工具 (write_todos) | 高 | 复杂任务分解的通用模式 |
| 文件系统持久化 | 中 | 企业场景可能需要数据库而非文件 |
| 中间件管道 | 中 | 可插拔的工具/安全中间件是好的设计 |
| 模型无关 | 高 | 企业场景需要支持国内模型 |

### 5.2 不建议直接采用的原因

1. **LangGraph 依赖重** — 底层绑定 LangGraph 生态，引入大量不必要的依赖
2. **学习曲线高** — LangChain 体系的抽象层对企业团队负担大
3. **项目仍在早期** — 缺乏大规模生产验证
4. **工具层不匹配** — 默认工具面向编码而非财经业务

### 5.3 推荐策略

**学习架构思想，轻量自建框架。** 具体路径：

1. 借鉴 DeepAgents 的四大支柱设计，作为 agent_harness 的架构参考
2. 用更轻量的方式实现核心模式（不需要 LangGraph 的全部能力）
3. 工具层按财经业务场景定制
4. 模型层保持灵活性（参考 DeepAgents 的 model-agnostic 设计）

---

## 6. 参考来源

### 官方资源
1. [langchain-ai/deepagents (GitHub)](https://github.com/langchain-ai/deepagents)
2. [langchain-ai/deepagentsjs (GitHub)](https://github.com/langchain-ai/deepagentsjs)
3. [DeepAgents 官方文档](https://docs.langchain.com/oss/python/deepagents/overview)
4. [Context Engineering 文档](https://docs.langchain.com/oss/python/deepagents/context-engineering)
5. [Deep Agents 发布博客](https://www.langchain.com/blog/deep-agents)
6. [Context Management 博客](https://www.langchain.com/blog/context-management-for-deepagents)
7. [Deep Agents CLI 博客](https://www.langchain.com/blog/introducing-deepagents-cli)

### 社区评测
8. [Towards AI 深度解析](https://pub.towardsai.net/deepagents-the-open-source-framework-for-building-long-horizon-ai-agents-b2b97a0332e3)
9. [Flowtivity 框架评测](https://flowtivity.ai/blog/langchain-deep-agents-framework-review/)
10. [MarkTechPost 发布报道](https://www.marktechpost.com/2026/03/15/langchain-releases-deep-agents-a-structured-runtime-for-planning-memory-and-context-isolation-in-multi-step-ai-agents/)
11. [Medium 架构分析](https://medium.com/github-all-stars/github-all-stars-5-deepagents-architecture-of-deep-reasoning-for-agentic-ai-b77261a49bde)

### 生产集成
12. [Milvus 生产集成指南](https://milvus.io/blog/how-to-build-productionready-ai-agents-with-deep-agents-and-milvus.md)

### 学术研究
13. [RUC-NLPIR/DeepAgent (GitHub)](https://github.com/RUC-NLPIR/DeepAgent)
14. [DeepAgent 论文 (arXiv)](https://arxiv.org/abs/2510.21618)
15. [MarkTechPost 论文解读](https://www.marktechpost.com/2025/11/01/deepagent-a-deep-reasoning-ai-agent-that-performs-autonomous-thinking-tool-discovery-and-action-execution-within-a-single-reasoning-process/)

### 社区讨论
16. [HackerNews 讨论](https://news.ycombinator.com/item?id=44761299)

### 教程
17. [Deep Agents from Scratch](https://github.com/langchain-ai/deep-agents-from-scratch)

---

## 方法论

通过 2 个并行研究代理执行 27 次搜索查询，分析 20+ 个来源。覆盖官方文档、社区讨论、学术资源、生产案例。
