# 视觉差异评估 执行契约

## 最小输出
输出 visual-diff.json、diff.png 与 baseline-approval。工具支持 JSON 配置的 regions 和 masks；样例阈值须按项目约定。

## 不变量
尺寸不一致直接失败，不自动缩放掩盖错误。像素相似只能用于回归判断，不能单独证明设计质量或业务正确。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
按专项执行步骤检查正常、打断、失败、恢复与重复挂载。不得用静态规范替代运行证据。

## 证据结构
```json
{"id":"visual-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
