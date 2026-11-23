# 质量验收矩阵

| 类别 | 最低场景 | 自动化可能性 | 证据 |
|---|---|---|---|
| 静态 | lang/title/meta/h1/main/alt/锚点 | Python | 静态检查 JSON 输出 |
| 结构 | 320/390/768/1440 px 无横向滚动 | 浏览器 | viewport 截图/日志 |
| 键盘 | tab/shift-tab/enter/esc | 浏览器/人工 | 录屏或测试日志 |
| 触控 | 菜单、按钮、输入 | 真机或浏览器 | 设备记录 |
| 无脚本 | 正文、导航与主要 CTA 可读 | 浏览器禁用 JS | 截图 |
| 减少动画 | 所有内容可用且无大位移 | matchMedia + 浏览器 | 录屏 |
| 性能 | LCP/INP/CLS | RUM/lab | 测量数据、环境、时间 |
| 安全 | 后端验证/鉴权/支付状态 | API/集成测试 | 服务端记录 |

重要：`check_budget.py` 仅校验用户提供的数字是否达标，不会测量数据。`browser_audit.py` 缺少 Playwright 时返回 blocked (exit 2)，不可写通过。
