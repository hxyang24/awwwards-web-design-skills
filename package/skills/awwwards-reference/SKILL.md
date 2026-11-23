---
name: awwwards-reference
description: Deconstruct representative award-winning websites into citations, patterns, independent implementation proposals, and honest inspection status.
---

# awwwards-reference

## 何时使用
要求拆解特定获奖网站的页面结构、前端技术、视觉/交互机制、性能和复现方案时使用。

## 必要输入
1. 案例 ID 或 Awwwards URL
2. 证据来源（官方页/制作方/技术文章）
3. 拟借鉴的交互模块及业务场景

## 严格执行顺序
1. 通过 case_tool.py 读取已核验案例信息。
2. facts 必须各自关联 sources.id；inferences 不可搬入 facts。
3. 如果没有访问真实页面，observations 与 measurements 保持空数组；inspection_plan.status=not_run。
4. 写原创蓝图：输入→状态→步骤→输出→fallback→cleanup→acceptance。
5. 按版权边界重建机制，不复制原站品牌、受保护素材与文字。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-reference/scripts/case_tool.py list
python skills/awwwards-reference/scripts/case_tool.py show --id nike-better-world
python skills/awwwards-reference/scripts/case_tool.py validate
```

## 验收门槛
1. 技术版本只有证据支持时才能明确。
2. 未经现场验证不声称逐像素还原、完整源码或 CWV 数据。
3. 跨站推断应附估计依据与局限。

## 本技能包含
- `scripts/case_tool.py`
- `references/case-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
