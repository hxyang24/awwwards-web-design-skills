---
name: awwwards-mobile
description: Adapt web products for narrow screens, touch, safe areas, mobile keyboards and responsive navigation with preserved task context.
---

# 移动端与响应式

按内容压力决定断点。手机页面需要重新组织信息和操作，不能只等比缩小桌面；视口模拟不能替代真机。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 在 320、390、768、1440 检查重排与溢出，中间宽度检查换行。
2. 触摸入口目标建议 44px；WCAG 2.2 AA 最小目标含 24px 及例外条件。
3. 单独处理安全区、dvh、软键盘、横屏、缩放和长语言文本。
4. 手势提供按钮与键盘替代；导航收起时焦点不可留在隐藏区域。
5. 引导返回保留输入，提交失败保留字段，真机检查键盘与屏幕阅读器。

## 交付与检查
输出 breakpoint-map、mobile-state-matrix 与 device-report。Daylight 提供三步引导和移动任务入口。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
