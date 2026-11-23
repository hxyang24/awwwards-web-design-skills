# 响应式布局规则

- 320、390、768、1024、1440 像素为最低检查集合；不是只能用这些断点。
- `header/nav/main/footer` 语义结构，跳转主内容 `#main`，每页 1 个 H1。
- 动效必须渐进增强，正文默认可见，`prefers-reduced-motion` 有完整路径。
- 菜单开闭同步 `aria-expanded` 与 `hidden`；窄屏切换时将焦点移出隐藏菜单。
- 图片保持宽高或 `aspect-ratio`，减少 CLS；按钮应可通过键盘触发。
