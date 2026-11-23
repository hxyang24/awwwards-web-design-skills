---
name: awwwards-design-system
description: Generate and audit original semantic design tokens, responsive scales, palettes, and WCAG contrast constraints.
---

# awwwards-design-system

## 何时使用
创建配色、字体、间距、圆角、阴影、断点和可复用 UI 组件规范时使用。

## 必要输入
1. 品牌定位和产品类型
2. 首要用户操作
3. 对比度与响应式要求

## 严格执行顺序
1. 先选业务适用的风格，不默认做满屏特效。
2. 生成 design-tokens.json 和 tokens.css 并保持一致。
3. 检验主文字、次要文字和按钮组合对比度。
4. 禁止无许可证字体，优先系统字体与开源可商用字体。
5. 视觉 token 只做样式，不改变业务状态。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-design-system/scripts/make_tokens.py --preset fintech --output PROJECT/design
python skills/awwwards-design-system/scripts/validate_tokens.py PROJECT/design/design-tokens.json
```

## 验收门槛
1. 正文常规文本目标 WCAG AA ≥4.5:1；大字 ≥3:1。
2. 至少覆盖 320、390、768、1440 px。
3. 有高对比度焦点样式。

## 本技能包含
- `scripts/make_tokens.py`
- `scripts/validate_tokens.py`
- `references/token-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
