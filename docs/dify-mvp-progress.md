# Dify MVP 文档比对助手 — 工作进展与待办

> 日期：2026-06-01
> 阶段：Phase 1 — Dify 本地部署 + 文档比对 MVP

---

## 已完成事项

### 1. Dify 本地部署

- **版本**：Dify 1.14.2
- **部署方式**：Docker Compose，目录 `dify/dify-main/docker/`
- **服务状态**：全部正常（api, db_postgres, redis, weaviate, nginx, web, worker, plugin_daemon 等）
- **启动命令**：`docker compose -f dify-main/docker/docker-compose.yaml --profile postgresql --profile weaviate up -d`

### 2. 模型配置

- **模型**：GLM 5.1（智谱 AI）
- **接入方式**：Dify 后台 → 设置 → 模型供应商 → Zhipu → 填入 API Key
- **状态**：已连通，正常响应

### 3. Chatflow 基础搭建

- **应用名称**：文档比对助手
- **已跑通链路**：文件上传 → Document Extractor → LLM → 回复
- **LLM 能力验证**：上传 `procurement-contract-sample.txt`，GLM 5.1 能正确解析文档内容

### 4. 文档比对能力验证

- **测试数据**：
  - 合同文档：`docs/test-sample/procurement-contract-sample.md`
  - 电子流数据：`docs/test-sample/workflow-data-sample.json`
- **测试方式**：电子流数据硬编码在 System Prompt 中，用户上传合同文档做比对
- **测试结果**：GLM 5.1 成功找出全部 5 处差异，零遗漏、零误报
  - 合同金额（¥560k vs ¥580k）
  - 付款方式（两期 vs 三期）
  - 交付日期（07-15 vs 06-30）
  - UPS 单价（¥24k vs ¥34k）
  - 违约金比例（3% vs 5%）

### 5. Mock API 搭建

- **位置**：`dify/mock-api/main.py`
- **框架**：FastAPI + uvicorn
- **端口**：8001
- **接口**：
  - `GET /` — 健康检查
  - `GET /api/workflow/{workflow_id}` — 查询电子流数据
- **错误处理**：已改造为 HTTP 200 + 业务错误码（`code: 404`），适配 LLM Tool Calling
- **启动命令**：`cd dify/mock-api && python3 main.py`

### 6. Dify Custom Tool 注册

- **工具名称**：电子流查询
- **OpenAPI Schema**：已配置，服务器地址 `http://host.docker.internal:8001`
- **接口映射**：`/api/workflow/{workflow_id}` → `getWorkflow`
- **参数**：`workflow_id`（string，电子流编号）

### 7. Chatflow Tool 集成

- **参数提取器**：已配置，从用户自然语言中提取 workflow_id
- **Tool 节点**：调用电子流查询 API，`workflow_id` 绑定参数提取器输出
- **LLM User Message**：引用 `{{#tool_0.text#}}` 获取 API 返回数据
- **测试结果**：
  - ✅ 测试 1：自然语言 + 文档上传 → 正常比对
  - ✅ 测试 2：简洁输入 → 正常比对
  - ✅ 测试 4：不传编号 → 正常提示
  - ❌ 测试 3：错误编号 → LLM 使用历史数据输出了错误比对报告

---

## 待执行 Tasks

### Task 1：修复错误编号的容错处理

**问题**：输入不存在的电子流编号（如 `WF-9999-0001`），LLM 没有提示错误，而是使用了对话历史中的旧数据输出比对报告。

**解决方案**：在 Dify Chatflow 中添加 IF/ELSE 条件判断节点，在工作流层面拦截错误。

**需要执行的操作**：

1. 在 Chatflow 画布中，**Tool 节点和 LLM 节点之间**插入一个 **"条件判断"（IF/ELSE）节点**
2. 配置 IF 条件：
   - 变量：`{{#tool_0.text#}}`
   - 条件：**包含（contains）**
   - 值：`"code": 0`
3. 连接 IF 分支（成功）→ 原有的 LLM 节点（保持不变）
4. 连接 ELSE 分支（失败）→ **新建一个"回复"（Answer）节点**，内容为：

```
未找到对应的电子流数据，请检查编号是否正确。

错误信息：{{#tool_0.text#}}

请确认编号格式正确后重试，例如：WF-2026-0387
```

5. 最终工作流结构应为：

```
开始 → 文档提取器 ──────────────────────────────────┐
     → 参数提取器 → Tool(电子流查询) → IF/ELSE
                                           ├── 成功(code==0) → LLM → 回复
                                           └── 失败(code!=0) → 回复(错误提示)
```

6. 用以下用例重新测试：
   - 输入 `WF-9999-0001` → 应直接输出错误提示，不生成比对报告
   - 输入 `WF-2026-0387` + 上传合同 → 应正常输出比对结果

**备注**：Mock API 已修复，错误编号返回 `{"code": 404, "data": null, "message": "电子流 WF-9999-0001 不存在，请检查编号是否正确"}`，HTTP 状态码始终为 200。

---

### Task 2：从 System Prompt 中移除硬编码数据

**前提**：Task 1 完成后执行。

**需要执行的操作**：

1. 打开 LLM 节点的 **System Prompt**
2. 找到并删除末尾的 `## 电子流系统数据（参考基准）` 整段 JSON 数据
3. 保留 System Prompt 中的比对规则、输出格式、错误处理指令

**预期效果**：LLM 完全依赖 Tool API 返回的数据做比对，不再使用任何硬编码数据。

---

### Task 3：测试完整链路

**前提**：Task 1 + Task 2 完成后执行。

**测试用例**：

| # | 操作 | 输入 | 上传文档 | 预期结果 |
|---|------|------|---------|---------|
| 1 | 正常比对 | "请帮我对比电子流 WF-2026-0387 与这份合同的差异" | procurement-contract-sample.txt | 输出 5 处不一致的比对报告 |
| 2 | 简洁输入 | "比对 WF-2026-0387" | procurement-contract-sample.txt | 同上 |
| 3 | 错误编号 | "对比电子流 WF-9999-0001 与这份合同" | procurement-contract-sample.txt | 输出错误提示，不生成比对报告 |
| 4 | 缺少编号 | "帮我对比这份合同" | procurement-contract-sample.txt | 提示用户补充电子流编号 |
| 5 | 不上传文档 | "比对 WF-2026-0387" | 无 | 提示用户上传合同文档 |

---

## 后续研究方向

> 以下内容已记录为长期研究方向，不在当前 MVP 范围内。

- 支持更多文档格式（PDF、DOCX、扫描件 OCR）
- 更复杂的比对规则（语义级别差异检测、金额自动计算校验）
- 批量比对能力
- 比对结果导出（PDF/Excel）
- 对接真实 Java 后端 API（替换 Mock）
- 多轮对话式比对（用户追问某一项差异的详情）

---

## 文件索引

| 文件路径 | 用途 |
|---------|------|
| `dify/dify-main/docker/` | Dify 部署目录（docker-compose.yaml、.env） |
| `dify/mock-api/main.py` | 电子流 Mock API 服务 |
| `dify/.env` | Dify 环境变量配置 |
| `docs/test-sample/procurement-contract-sample.md` | 测试用采购合同文档 |
| `docs/test-sample/workflow-data-sample.json` | 测试用电子流数据（含 5 处差异） |
| `docs/research/01-agent-framework-survey.md` | Agent 框架调研报告 |
| `docs/research/02-dify-vs-langgraph.md` | Dify vs LangGraph 深度对比 |
| `docs/research/03-spring-ai-evaluation.md` | Spring AI 评估 |
| `docs/research/04-deepagent-research.md` | DeepAgent 研究 |
| `docs/research/05-deepagent-vs-dify-vs-langgraph.md` | 三框架对比 |
