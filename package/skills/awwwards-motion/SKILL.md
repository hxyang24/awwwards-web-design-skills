---
name: awwwards-motion
description: Specify and implement progressive, cleanup-safe scroll and microinteractions with reduced-motion handling.
---

# awwwards-motion

## 何时使用
为标题、卡片、分屏、滚动或鼠标交互添加动画，尤其要求无障碍和卸载清理时使用。

## 必要输入
1. 元素、触发条件、可达状态
2. 动画时长/距离/缓动
3. 手机和减少动画回退

## 严格执行顺序
1. 写 motion-spec.json：触发器、states、duration、fallback、cleanup。
2. JS 前内容保持可见；动画是渐进增强。
3. 优先 CSS/IntersectionObserver，复杂时间线才用 GSAP。
4. prefers-reduced-motion 时停止位移动画。
5. 路由离开时只释放本模块事件/观察器，防止影响其他模块。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-motion/scripts/check_motion_spec.py skills/awwwards-motion/examples/motion-spec.json
```

## 验收门槛
1. reduced_motion 字段不能缺失。
2. 必须注明 teardown 行为。
3. 离线无 JS 不丢主内容。

## 本技能包含
- `scripts/check_motion_spec.py`
- `assets/progressive-motion.js`
- `examples/motion-spec.json`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
