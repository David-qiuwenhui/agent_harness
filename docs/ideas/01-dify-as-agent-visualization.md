# Dify 作为 Agent 可视化演示平台

> 日期：2026-06-02
> 状态：灵感

## 背景

我们在分阶段推进 Agent 能力建设：

- Phase 1：Dify 低代码搭建 MVP（进行中）
- Phase 2：LangGraph / DeepAgents 代码级框架（规划中）

这两个阶段各有优劣——Dify 可视化但灵活性受限，代码框架灵活但对非技术人员不直观。

## 想法

在搭建 LangGraph 或 DeepAgents 框架时，**同步在 Dify 上构建对应的可视化版本**，形成"影子副本"。

### 用途

1. **理解 Agent 机制** — Dify 的可视化画布能直观展示节点编排、数据流转、条件分支，帮助开发团队快速理解 Agent 的状态图、Tool 调用链路等抽象概念
2. **向团队演示** — 用 Dify 的交互式界面展示 Agent 能力（文档比对、智能问答等），比纯代码更容易让产品、运营等非技术人员理解
3. **方案对比** — 同一个业务场景，在 Dify 和代码框架中分别实现，对比低代码 vs 代码方案的边界和适用场景

### 执行方式

每在 LangGraph/DeepAgents 中实现一个 Agent 能力，就在 Dify 中同步搭建一个对应的可视化版本。例如：

| 代码框架实现                   | Dify 可视化对应               |
| ------------------------------ | ----------------------------- |
| LangGraph 状态图（文档比对）   | Dify Chatflow（文档比对助手） |
| Tool Calling（查询电子流 API） | Dify Custom Tool              |
| RAG Pipeline（知识库问答）     | Dify Knowledge + Chatflow     |
| Multi-Agent 协作               | Dify Workflow 多节点编排      |

## 价值

- 降低 Agent 概念的沟通成本
- 为团队提供一个"所见即所得"的 Agent 学习路径
- 在选择技术方案时提供直观的对比参考
