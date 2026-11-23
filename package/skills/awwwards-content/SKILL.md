---
name: awwwards-content
description: Audit truthful product messaging, metadata, CMS contracts, structured content, source provenance and useful empty states.
---

# awwwards-content

## 何时使用
为获奖风格页面撰写产品内容、SEO、CMS 模型、错误状态和 CTA 时使用。

## 必要输入
1. 真实商业资料、品牌表述与功能清单
2. 页面清单、用户查询意图
3. 可发布素材与使用许可

## 严格执行顺序
1. 先整理可验证产品能力，不编造客户、获奖、财务指标。
2. 为每个路由记录标题、描述、H1、CTA、image alt。
3. 落实加载、空态、无权限、失败和恢复文案。
4. 所有 SEO title 与 H1 需匹配真实页面功能。
5. CMS 内容字段与组件显示状态一一对应。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-content/scripts/audit_content.py skills/awwwards-content/examples/site-content.json
```

## 验收门槛
1. 不存在 placeholder、lorem ipsum 等生产占位符。
2. 所有公开断言都有用户材料或明确来源。
3. 未发布/无后端功能不得称为已上线。

## 本技能包含
- `scripts/audit_content.py`
- `examples/site-content.json`
- `references/content-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
