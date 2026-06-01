# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ToB 财经 SaaS Agent 框架 MVP。为以电子流为主的财经 SaaS 系统提供智能问答、工作流自动化和数据分析能力。

**当前阶段**：调研与方案设计，尚未进入编码阶段。

## Repository Structure

```
agent_harness/
├── docs/
│   ├── agent-mvp-architecture.md      # MVP 架构方案（核心文档）
│   ├── research/                       # 框架调研报告
│   │   ├── 01-agent-framework-survey.md          # 全景调研
│   │   ├── 02-dify-vs-langgraph.md               # Dify vs LangGraph 对比
│   │   ├── 03-spring-ai-evaluation.md            # Spring AI 评估
│   │   ├── 04-deepagent-research.md              # DeepAgent 研究
│   │   └── 05-deepagent-vs-dify-vs-langgraph.md  # 三方对比
│   ├── guides/                         # 使用指南
│   └── test-sample/                    # 测试样本数据
├── dify/                               # Dify 私有化部署配置
│   ├── docker-compose.yaml             # 生产部署
│   ├── docker-compose.middleware.yaml   # 开发中间件
│   ├── .env                            # 环境变量（不提交敏感值）
│   └── dify-main/                      # Dify 源码（子目录）
```

## Key Decisions

以下决策已在调研中确定，不要随意推翻：

| 决策 | 选择 | 理由 |
|------|------|------|
| 后端技术栈 | Java | 现有 SaaS 系统 |
| Agent 技术栈 | Python | AI 生态更丰富 |
| LLM | 国产模型（Qwen/DeepSeek/GLM） | 私有化 + OpenAI 兼容接口 |
| 部署方式 | 私有化部署 | 金融合规 |
| MVP 范围 | 文档比对 + 智能填写/生成 | 最高业务价值 |
| MVP 框架 | Dify | 开发速度 + 国产模型支持 + 私有化部署 |
| 深化框架 | LangGraph | Dify 表达力不足时 |

## Dify Deployment

Dify 通过 Docker Compose 私有化部署，配置在 `dify/` 目录：

```bash
# 生产部署
cd dify
docker compose up -d

# 开发中间件（仅 PostgreSQL + Redis + Weaviate）
docker compose --env-file middleware.env -f docker-compose.middleware.yaml -p dify up -d

# 环境变量同步（升级后）
./dify-env-sync.sh
```

Dify 源码在 `dify/dify-main/`，修改时参考其 `AGENTS.md`：
- 后端 API（`api/`）：Python Flask + DDD 架构
- 前端 Web（`web/`）：Next.js + TypeScript + React
- 后端 CLI 命令通过 `uv run --project api <command>` 执行

## Language

- 研究文档和沟通使用中文
- 技术术语保持英文原文
- 代码标识符使用英文
