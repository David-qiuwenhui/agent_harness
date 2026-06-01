# Spring AI 评估报告

> 调研时间：2026-05-30
> 项目背景：SaaS 电子流系统 Agent 能力构建

## 概况

| 维度 | 状态 |
|------|------|
| 版本 | GA（正式发布），当前 1.x |
| 语言 | Java / Kotlin |
| Spring 生态 | 原生集成（自动配置、Bean、属性驱动） |
| 国产模型 | 通过 Spring AI Alibaba 支持 Qwen、通义千问等 |
| MCP | 支持（Client + Server） |
| Tool Calling | 原生支持，`@Tool` 注解 |
| RAG | 支持（VectorStore + Advisor 模式） |
| Structured Output | 支持（直接映射 Java Record） |
| 生产就绪 | 是（GA） |

## 核心能力

### 1. Tool 定义

一个注解把 Java 方法变成 Agent 可调用的 Tool：

```java
@Service
public class WorkflowQueryService {
    @Tool(description = "查询指定电子流的详细信息和当前状态")
    public WorkflowDetail getWorkflowDetail(String workflowId) {
        return workflowRepository.findById(workflowId)
            .map(this::toDetail)
            .orElseThrow();
    }
}
```

### 2. Advisors API（核心设计）

可组合的请求/响应拦截器，类似 Middleware 模式：

```java
ChatClient agent = ChatClient.builder(chatModel)
    .defaultAdvisors(
        new MessageChatMemoryAdvisor(chatMemory),
        new QuestionAnswerAdvisor(vectorStore)
    )
    .build();
```

可自定义 Advisor 实现租户上下文注入、输出净化、Token 用量监控、速率限制等。

### 3. Structured Output

LLM 响应直接映射为 Java 对象，适用于文档比对结果输出：

```java
record ComparisonResult(
    List<Inconsistency> inconsistencies,
    String summary,
    double matchScore
) {}

ComparisonResult result = chatClient.prompt()
    .user("比对电子流 #123 与上传的合同文档")
    .call()
    .entity(ComparisonResult.class);
```

## 对项目场景的匹配度

| 场景需求 | 支持度 | 说明 |
|----------|--------|------|
| 调用后端 API 查询电子流 | 高 | `@Tool` 直接调用现有 Service 或 HTTP Client |
| 文档比对 | 中高 | RAG + Structured Output，但文档解析库不如 Python 丰富 |
| 智能填写/生成 | 高 | Structured Output 天然适合结构化表单数据 |
| 国产模型 | 高 | Spring AI Alibaba 原生支持 Qwen |
| 知识库管理 | 中 | VectorStore 抽象层有，管理界面需自建 |
| 私有化部署 | 高 | 标准 Spring Boot 微服务 |
| 嵌入式 Chat Widget | 低 | 需自己开发前端组件 |

## Java Agent 框架竞品对比

| 框架 | Spring 原生 | 规划模型 | MCP | A2A | Checkpointing | 状态 |
|------|------------|---------|-----|-----|--------------|------|
| Spring AI | Native | ReAct loop | 支持 | 不支持 | 不支持 | GA |
| LangChain4j | 支持 | ReAct loop | 支持 | 支持 | 不支持 | GA |
| Embabel | 支持 | GOAP + Utility AI | 支持 | 支持 | 规划中 | Beta |
| Koog | 支持 | Graph-based | 支持 | 不支持 | 支持 | Beta |
| Google ADK | 支持 | Hierarchical | 支持 | 支持 | 不支持 | Pre-GA |

## 决策：暂不采用

**理由**：团队已决定 Agent 侧用 Python（AI 生态更丰富，灵活切换框架），Spring AI 意味着 Agent 也是 Java，与决策冲突。

**保留选项**：如果未来考虑混合架构（如 Java 侧做简单 Agent 逻辑，Python 侧重文档处理），Spring AI 是首选。

## 参考资料

- [Spring AI 官方文档](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [Spring AI Alibaba](https://github.com/LLLLLLLLM/spring-ai-alibaba-update)
- [Spring AI Alibaba 教程（B 站）](https://www.bilibili.com/video/BV1sdkYBGEga/)
- [Spring AI + MCP 企业实践](https://javapro.io/2026/01/07/building-mcp-tools-for-ai-agents-using-spring-ai/)
- [Java AI Agent 框架对比 2026](https://codewiz.info/blog/java-ai-agent-frameworks-2026/)
