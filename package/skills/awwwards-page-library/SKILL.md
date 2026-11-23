---
name: awwwards-page-library
description: Select page patterns and state contracts for multi-page website design across marketing, identity, content, community, education and booking products.
---

# 页面模式与业务路由

先识别用户要完成的任务，再组合页面；不要把营销首页直接套进交易或后台。目录的 specification 记录只是规格，runnable_demo 才有演示路由。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 按网站类型、用户任务、前置权限和数据依赖列出路由。
2. 为每个路由选择模式；缺少模式时添加新 ID，不伪造覆盖。
3. 为主路径画出进入、操作、确认、返回；列出加载、空、错、无权限。
4. 为页面命名语义区域和组件职责，再实现视觉层级。
5. 用覆盖矩阵逐项标明规范、实现、实测、生产接入的不同状态。

## 交付与检查
输出 route-map.json（path、pattern_id、goal、permission、states、evidence），以及主路径和剩余规格清单。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
