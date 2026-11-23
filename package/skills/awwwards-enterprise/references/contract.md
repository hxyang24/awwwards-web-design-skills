# 企业后台 执行契约

## 最小输出
输出 entity-contract、permission-matrix、audit-contract、冲突恢复说明。演示 Morrow 的目录、审批、日志与设置可直接运行。

## 不变量
关注高密度任务流：筛选排序分页保留上下文，详情与修改采用版本检查。客户端按钮权限仅用于展示，不能当作授权。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `enterprise.overview`：识别今日需要处理的工作。约束：样例指标不代表真实运营数据。
- `enterprise.records`：定位并修改客户记录。约束：更新必须具备版本冲突处理。
- `enterprise.record-detail`：理解单个实体并安全变更。约束：权限与版本应由服务端检查。
- `enterprise.approvals`：做出可追踪的审批决定。约束：生产审批需要持久审计和幂等。
- `enterprise.audit`：重建谁在何时做了什么。约束：客户端列表不等于不可篡改审计。
- `enterprise.roles`：配置最小业务权限。约束：隐藏按钮不能替代服务端授权。
- `enterprise.billing`：核对账单与付款状态。约束：付款状态跟随真实账务系统。
- `enterprise.import`：在写入前预览导入结果。约束：限制文件大小，处理公式注入与重复键。
- `enterprise.settings`：配置工作空间选项。约束：演示设置刷新会清空。
- `enterprise.reports`：按口径比较业务表现。约束：聚合口径和缺失数据必须说明。

## 证据结构
```json
{"id":"enterprise-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
