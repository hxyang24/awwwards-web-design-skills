# 电商完整路径 执行契约

## 最小输出
输出 checkout-contract、pricing-examples、order/return 状态图与支付边界。Forma 的本地订单不是付款凭证。

## 不变量
从商品变体与库存开始，再实现购物车、审阅和结算。价格和库存最终由服务端重算；浏览器总价不可信。

## 主路径与失败路径
执行前记录任务入口、权限、数据前置条件；操作后核对实际状态、返回路径和用户反馈。测试不能只检查按钮存在。
- `commerce.collection`：找到适合的商品。约束：缺货不可伪装可购买。
- `commerce.product`：确认规格和购买条件。约束：素材有许可，规格不可混淆。
- `commerce.cart`：核对数量与总价。约束：金额使用整数分并明确舍入。
- `commerce.checkout`：审阅配送和费用并提交。约束：无真实支付接入不能显示已扣款。
- `commerce.orders`：查看订单并启动售后。约束：售后申请不等于已退款。
- `commerce.order-detail`：核对购买记录及物流。约束：状态应来自服务端事件。
- `commerce.wishlist`：保存考虑中的商品。约束：明确本地和账户同步边界。
- `commerce.reviews`：识别真实产品体验。约束：不得捏造真实用户或验证购买。
- `commerce.returns`：选择售后原因并审阅处理方式。约束：不承诺未确认的退款日期。
- `commerce.account`：管理资料与订单入口。约束：个人信息不得进入公共测试快照。

## 证据结构
```json
{"id":"commerce-primary-flow","status":"not_run","method":"browser interaction or focused unit test","environment":null,"evidence":[],"limitations":[]}
```
只有执行后填写 `passed` 或 `failed`；无法运行记 `blocked` 并说明条件。参考来源见完整包 `v2/docs/SOURCES.md`，可用规范入口：W3C WCAG 2.2、MDN prefers-reduced-motion、GSAP 官方文档、Three.js 官方文档、Playwright 官方文档。

## 移植与维护
已有 React/Vue/Next/Nuxt 项目优先复用其路由、组件和数据层；原生 HTML 示例仅为行为参照。不得声称示例已通过这些框架的构建测试。业务接口、密钥管理、服务端授权、数据持久化与生产部署需要项目实际接入和验证。
