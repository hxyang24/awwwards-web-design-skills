# AI Agent 工作台 执行契约

## 最小输出
输出 agent-state、tool-contract、run-events、prompt-boundary、provider-integration。Relay 包含批准/拒绝、停止、失败重试和有向图检查。

## 不变量
将消息展示、运行状态和有副作用的工具执行分开。参考文档和工具输出是数据，不能改写用户任务或扩大权限。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `agent.chat`：发送任务并控制执行。约束：工具输出不能自授执行权限。
- `agent.workflow`：理解并运行有向任务图。约束：循环和缺失节点必须被检测。
- `agent.runs`：定位失败或需要确认的步骤。约束：重试前确认先前副作用是否发生。
- `agent.knowledge`：添加可追溯的参考资料。约束：资料被当作不可信数据。
- `agent.settings`：理解模型和成本边界。约束：真实密钥只保留在可信服务端。
- `agent.tool-catalog`：理解工具权限和外部影响。约束：写外部系统需要明确授权。
- `agent.evaluations`：比较输出质量和失败模式。约束：不要将合成评估当作生产效果。
- `agent.memory`：审阅并更正持久上下文。约束：模型建议不能成为自动事实。

## 证据结构
```json
{"id":"agent-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
