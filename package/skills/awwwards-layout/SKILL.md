---
name: awwwards-layout
description: Turn an approved page specification into semantic responsive layout contracts with keyboard, no-JS and overflow checks.
---

# awwwards-layout

## 何时使用
构建首页、详情、内容页和响应式导航，或复核页面结构时使用。

## 必要输入
1. 页面类型与主要 CTA
2. 内容分区
3. 设备断点及可访问要求

## 严格执行顺序
1. 识别页面的一级任务和主要操作。
2. 按语义标签 header/nav/main/section/footer 排布，保持标题层级。
3. 先设计无 JS 的完整内容和锚点。
4. 再接入移动菜单与动画增强。
5. 在 320/390/768/1440 的视宽复核换行、焦点、滚动、点击区域。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-layout/scripts/prepare_layout.py --kind saas --output PROJECT/layout.json
```

## 验收门槛
1. 每页仅一个语义主内容区域。
2. 键盘可访问所有主要功能。
3. 关键内容不能仅在 hover 或滚动动画后出现。

## 本技能包含
- `scripts/prepare_layout.py`
- `references/layout-rules.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
