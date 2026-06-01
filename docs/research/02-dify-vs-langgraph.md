# Dify vs LangGraph 深度对比

> 调研时间：2026-05-30
> 适用场景：SaaS 电子流系统 Agent 能力构建

## 1. 架构哲学

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **核心模型** | 可视化工作流 + 节点编排 | 代码级有向图状态机 |
| **思维模式** | "拖拽搭建" — 产品经理也能参与设计 | "代码编排" — 开发者完全掌控每一步 |
| **学习曲线** | 低 — 看着界面就能上手 | 中高 — 需理解 State、Node、Edge、Checkpoint |
| **开发方式** | Web UI 配置 + 少量 API 调用 | 纯 Python 代码 |
| **版本状态** | GA，Beehive 架构提升了模块化 | GA，LangGraph Platform 支持生产部署 |

**本质区别**：Dify 是"平台"——你在这个平台上构建应用；LangGraph 是"库"——你用代码组合出应用。

## 2. MVP 场景逐项对比

### 场景 A：文档比对

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **文档解析** | 内置解析器（PDF/Word/TXT），开箱即用 | 需自行集成（推荐 Docling、Unstructured） |
| **RAG 管线** | 可视化配置：上传 → 分段 → 向量化 → 检索 | 需用 LangChain 的 VectorStore 等组件手动组装 |
| **比对逻辑** | 工作流节点串联：检索 → 解析 → LLM 比对 → 输出 | 状态图中定义节点，可加重试、分支、人工审核 |
| **原型速度** | 1-2 天 | 3-5 天 |
| **精细控制** | 基础比对足够 | 多轮细化、差异分级、逐步修正 |

### 场景 B：智能填写/生成

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **表单结构理解** | 通过 Prompt + Knowledge 注入表单 schema | 代码中定义 Pydantic 模型，精确控制字段 |
| **数据来源** | Knowledge Base 检索 + Tool 调用后端 API | Tool 节点直接调用 API，状态图管理数据流 |
| **生成质量** | 依赖 Prompt 工程 + 模型能力 | 可做"生成 → 验证 → 修正"循环 |
| **多字段关联** | 线性编排，复杂关联受限 | 条件分支、并行填写、字段间依赖 |

## 3. 与 Java 后端的集成

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **自定义 Tool** | 通过 OpenAPI schema 注册自定义 API Tool | Python 函数即 Tool，完全自由 |
| **调用后端 API** | 在 UI 中配置端点、参数、认证 | `@tool` 装饰器 + `httpx`/`requests` |
| **认证方式** | API Key、OAuth 等 | 代码中任意实现 |
| **复杂查询** | 单次调用为主，链式需多节点 | 任意组合多次调用、条件调用 |
| **MCP** | 原生支持 | LangChain 生态有 MCP adapter |

### 代码示例（LangGraph）

```python
from langgraph.graph import StateGraph

class CompareState(TypedDict):
    workflow_id: str
    workflow_data: dict | None
    doc_content: str | None
    inconsistencies: list[dict] | None

def fetch_workflow(state):
    data = workflow_api.get(state["workflow_id"])
    return {**state, "workflow_data": data}

def parse_document(state):
    content = doc_parser.parse(uploaded_file)
    return {**state, "doc_content": content}

def compare(state):
    result = llm.compare(state["workflow_data"], state["doc_content"])
    return {**state, "inconsistencies": result}

graph = StateGraph(CompareState)
graph.add_node("fetch", fetch_workflow)
graph.add_node("parse", parse_document)
graph.add_node("compare", compare)
graph.add_edge("fetch", "compare")
graph.add_edge("parse", "compare")
```

## 4. 国产模型支持

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **Qwen** | 原生支持（下拉选择） | 通过 `langchain-openai` 配置 `base_url` |
| **DeepSeek** | 原生支持 | 同上 |
| **GLM（智谱）** | 原生支持 | 同上 |
| **模型切换** | UI 一键切换 | 代码更换初始化参数 |
| **多模型编排** | 不同节点可用不同模型 | 代码中完全自由 |

## 5. 私有化部署 & 运维

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **部署方式** | Docker Compose 一键部署 | 自行构建 Python 服务 |
| **依赖组件** | PostgreSQL + Redis + 向量库 + Nginx | 向量库 + 应用服务器 |
| **运维复杂度** | 中（自带管理界面） | 高（需自建 observability） |
| **资源占用** | 较重（完整平台） | 较轻（精简可控） |

## 6. 团队适配度

| 维度 | Dify | LangGraph |
|------|------|-----------|
| **AI 经验要求** | 低 | 中 |
| **Python 深度** | 浅 | 深 |
| **协作模式** | 产品经理 + 开发者在同一 UI 协作 | 纯开发者工作流 |
| **迭代速度** | 前期极快，后期受限 | 前期较慢，后期不受限 |

## 7. 天花板与风险

| 风险 | Dify | LangGraph |
|------|------|-----------|
| **功能天花板** | 工作流表达力有限 | 无天花板 |
| **供应商锁定** | 中等 | 低（纯 Python） |
| **长期维护** | 依赖社区 | 自主掌控 |

## 参考资料

- [Dify vs LangChain 深度对比](https://agent.nexus/blog/dify-vs-langchain)
- [Dify 官方部署文档](https://docs.dify.ai/en/self-host/quick-start/docker-compose)
- [Dify Tool 文档](https://docs.dify.ai/en/use-dify/workspace/tools)
- [Dify 架构升级（Beehive）](https://dify.ai/blog/dify-rolls-out-new-architecture)
- [Dify + DeepSeek 私有化部署](https://dify.ai/blog/dify-deepseek-deploy-a-private-ai-assistant)
- [LangGraph 9 种 RAG 架构对比](https://zhuanlan.zhihu.com/p/1944652206402954231)
- [Dify 6 个月深度评测](https://dev.to/nova_gg/dify-review-2026-i-used-it-for-6-months-to-build-ai-agents-honest-verdict-2d25)
