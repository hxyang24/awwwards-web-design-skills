# 金融交易终端 执行契约

## 最小输出
输出 order-state-machine、money-contract、quote-contract、risk-checklist 和模拟/真实边界。Axis 演示只支持 USD 整股限价买单。

## 不变量
先定义价格单位、交易数量、币种、报价时间和订单状态机。演示不能显示真实成交、余额变更或资金已到账。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `fintech.terminal`：审阅行情并构造模拟订单。约束：模拟与真实交易必须显著区分。
- `fintech.orders`：追踪并撤销符合条件的订单。约束：撤单应防止状态竞争和重复提交。
- `fintech.portfolio`：理解敞口和持仓变化。约束：净值与收益必须有计算口径。
- `fintech.risk`：理解限制和异常。约束：真实风控在可信服务端执行。
- `fintech.watchlist`：跟踪关注的资产。约束：延迟行情必须显示延迟标识。
- `fintech.asset-detail`：审阅资产信息与风险。约束：日期币种时区及拆股口径明确。
- `fintech.transfers`：审阅资金流转请求。约束：本模板不得采集支付凭证或真实转账。
- `fintech.statements`：核对交易和费用。约束：审计金额用定点数或整数最小单位。

## 证据结构
```json
{"id":"fintech-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
