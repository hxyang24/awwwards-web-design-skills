---
name: awwwards-enterprise
description: Build enterprise administration interfaces with editable records, approvals, role-aware controls, audit views and conflict recovery.
---

# 企业后台

关注高密度任务流：筛选排序分页保留上下文，详情与修改采用版本检查。客户端按钮权限仅用于展示，不能当作授权。

## 输入与边界
读取用户目标、已有项目、允许修改的范围、目标设备和可用业务接口。缺省使用明确标识的本地样例；不要要求与当前任务无关的部署、审批或配置。

## 执行
1. 定义实体键、版本、字段约束、角色动作矩阵和可审计事件。
2. 明确筛选作用于全部结果还是当前页；翻页后保留查询。
3. 编辑使用服务器版本或 ETag；409 冲突保留草稿并重新加载。
4. 批量审批先预览影响，使用幂等键，服务端逐项授权。
5. 检查 viewer/editor/admin、无结果、长字段、并发修改、分页边界。

## 交付与检查
输出 entity-contract、permission-matrix、audit-contract、冲突恢复说明。演示 Morrow 的目录、审批、日志与设置可直接运行。

根据任务读取 [专项执行契约](references/contract.md)。如与原有 V1 技能共同使用，保留已有脚本和接口；V2 负责补充当前任务所需范围。

## 配套演示和工具
完整 ZIP 中的 `V2_START_HERE.md` 列出启动和工具命令。安装时 `PACKAGE_LOCATION.json` 记录资源包绝对位置；安装后的技能正文和契约可独立阅读，演示和集中工具仍在完整包中。不要假设聊天沙盒路径在用户机器存在。
