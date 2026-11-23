---
name: awwwards-product-ux
description: Validate real user tasks, state machines, backend contracts, idempotency, error recovery and preview-vs-production boundaries.
---

# awwwards-product-ux

## 何时使用
把创意展示用于 SaaS、电商、财务软件、销售/支付/上传等真实业务流程时使用。

## 必要输入
1. 用户核心任务、权限、后端 API
2. 提交/支付/订单/上传状态流
3. 必要风控与合规控制

## 严格执行顺序
1. 记录 user journey 和输入校验。
2. 标明真实服务端动作与仅前端演示的区别。
3. 列出 idle/loading/success/error/empty/disabled 状态。
4. 失败提供重试/恢复路径，禁止假成功。
5. 支付与订单相关操作必须以后端权威状态为准，不在浏览器伪造。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-product-ux/scripts/validate_flow.py skills/awwwards-product-ux/examples/demo-request-flow.json
```

## 验收门槛
1. 演示流程必须标 mode=preview，并说明数据未发送。
2. 生产流程必须提供 backend_contract 和 errors。
3. 涉及授权必须有真实权限验证策略。

## 本技能包含
- `scripts/validate_flow.py`
- `examples/demo-request-flow.json`
- `references/product-ux-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
