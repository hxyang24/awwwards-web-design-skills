---
name: awwwards-webgl
description: Design progressive 3D experiences with explicit rendering budgets, lifecycle cleanup, fallback, and non-WebGL primary tasks.
---

# awwwards-webgl

## 何时使用
构建 3D 产品展示、WebGL/Three.js 场景、Shader、沉浸式滚动时使用。

## 必要输入
1. GPU 需求及可接受预算
2. 三维素材授权和模型质量
3. 主要 CTA 的 DOM 备用入口

## 严格执行顺序
1. 优先完成静态 DOM 版内容和 CTA。
2. 场景规范列出模型、纹理、DPR、FPS、场景分段、渲染暂停。
3. 使用资源注册表管理自有 geometry/material/texture 的生命周期。
4. offscreen、隐藏标签或 reduced-motion 时停帧或降低质量。
5. GPU 初始化失败自动切换静态图与文字。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-webgl/scripts/check_scene_spec.py skills/awwwards-webgl/examples/scene-spec.json
node skills/awwwards-webgl/scripts/test_resource_scope.mjs
```

## 验收门槛
1. 必须有 static_fallback 与 dispose_policy。
2. 不得直接覆盖业务流程 DOM。
3. 模型、纹理无凭证不得声称拥有可分发权。

## 本技能包含
- `scripts/check_scene_spec.py`
- `assets/resource-scope.mjs`
- `scripts/test_resource_scope.mjs`
- `examples/scene-spec.json`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
