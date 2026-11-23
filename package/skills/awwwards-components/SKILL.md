---
name: awwwards-components
description: Scaffold six original, responsive HTML/CSS/JS blueprints for SaaS, commerce, dashboard, portfolio, editorial and immersive sites.
---

# awwwards-components

## 何时使用
需要即用型落地页、组件演示、快速起站、交互基础模板时使用。

## 必要输入
1. kind=saas|commerce|dashboard|portfolio|editorial|immersive
2. 输出目录、品牌名称
3. 是否已有框架/业务代码

## 严格执行顺序
1. 如果现有代码存在，优先新分支或独立目录，不覆盖。
2. 用 scaffold.py 复制对应模板，替换名称、标题。
3. 先检查静态语义 HTML，再检查菜单、筛选、弹窗和表单。
4. 接真实 API 前保留清晰的 preview 提示。
5. 需要 Next/Nuxt 时移植 DOM 与交互协议，不直接声称 HTML 是框架实现。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-components/scripts/scaffold.py --kind saas --name "明账" --output /tmp/mingzhang
python skills/awwwards-components/scripts/scaffold.py --kind commerce --name "商品精选" --output /tmp/catalog
```

## 验收门槛
1. 不写入非空目录。
2. 无外部 CDN 和受保护品牌素材。
3. 静态内容可阅读；按钮真实响应或明确 disabled。

## 本技能包含
- `scripts/scaffold.py`
- `templates/`
- `scripts/static_self_test.py`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
