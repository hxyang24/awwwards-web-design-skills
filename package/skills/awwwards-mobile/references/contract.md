# 移动端与响应式 执行契约

## 最小输出
输出 breakpoint-map、mobile-state-matrix 与 device-report。Daylight 提供三步引导和移动任务入口。

## 不变量
按内容压力决定断点。手机页面需要重新组织信息和操作，不能只等比缩小桌面；视口模拟不能替代真机。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `mobile.today`：快速完成当日主要任务。约束：安全区、键盘和触控目标要实测。
- `mobile.onboarding`：逐步建立最少必要设置。约束：返回保留已输入值。
- `mobile.preferences`：配置个人体验。约束：开关不应假装申请系统权限。
- `mobile.offline`：在网络失效时保持方向。约束：不要显示未同步的操作为成功。

## 证据结构
```json
{"id":"mobile-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
