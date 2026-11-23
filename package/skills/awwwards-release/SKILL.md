---
name: awwwards-release
description: Create reproducible delivery manifests with SHA-256, authorization boundaries, real test statuses and unresolved risk ledger.
---

# awwwards-release

## 何时使用
需要打包交付、推送 PR、交接文档、可追溯发布时使用。

## 必要输入
1. 项目目录、授权范围、目标交付目录
2. 验证日志、已知风险
3. 许可证、依赖与运行要求

## 严格执行顺序
1. 检查用户授权，确认范围内才修改仓库或部署。
2. 收集真实文件、可复现命令、依赖版本和测试状态。
3. 生成 manifest 与 SHA256 索引。
4. 逐条列出 blocked/not_run 与后续人工条件。
5. 未获授权不自动上线；不要把发布当作纯视觉验收。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-release/scripts/delivery_manifest.py --root PROJECT --output PROJECT/DELIVERY.json
python skills/awwwards-release/scripts/delivery_manifest.py --verify PROJECT/DELIVERY.json --root PROJECT
```

## 验收门槛
1. 所有交付文件可核验哈希。
2. 状态与实际测试一致。
3. 不得声称已上线、已合并或已安装，除非操作实际完成。

## 本技能包含
- `scripts/delivery_manifest.py`
- `references/delivery-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
