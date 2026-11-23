---
name: awwwards-advanced-motion
description: Compose timeline, scroll and page transition motion with lifecycle cleanup, interruption and reduced-motion alternatives.
---

# 高级动效

动效表达状态关系；先交付稳定语义内容。时间轴必须可中断，反复挂载不得叠加监听器或动画实例。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 为触发、初始、进行、完成和打断状态建立 motion-spec。
2. 使用 GSAP context/matchMedia 按区域管理生命周期；卸载 revert。
3. 滚动动画先测量再读写，避免布局抖动和滚动劫持。
4. 路由转场确保标题焦点与阅读顺序，减少动画直接展示最终布局。
5. 验证暂停、重新播放、路由卸载、用户偏好改变以及触屏回退。

## 交付与检查
输出 motion-spec 与 cleanup-test。Orbit 内含实装 GSAP 时间轴；高级滚动编排与跨页面转场是接入配方，不能称已实测。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
