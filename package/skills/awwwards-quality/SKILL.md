---
name: awwwards-quality
description: Run evidence-based static, accessibility, functional and Core Web Vitals budget checks without falsely marking unmeasured metrics as passed.
---

# awwwards-quality

## 何时使用
需要性能、无障碍、浏览器兼容、交互行为和发布前检查时使用。

## 必要输入
1. 页面地址或本地路径
2. 目标设备/浏览器/测量环境
3. 预算规范和真实结果 JSON

## 严格执行顺序
1. 先跑静态 HTML、ARIA 和脚本语法检查。
2. 环境存在 Playwright 才做浏览器实际测试；不可启动则记 blocked。
3. 分别检查键盘、缩屏、减少动画、无 JS。
4. 性能数据明确来源、日期与设备；无实测不得通过预算。
5. 整理 passed/failed/blocked/not_run 并关联证据。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-quality/scripts/static_audit.py examples/saas/index.html
python skills/awwwards-quality/scripts/check_budget.py skills/awwwards-quality/examples/metric-result.json
```

## 验收门槛
1. LCP <= 2.5s, INP <= 200ms, CLS <= 0.1（75百分位，真实监测口径）。
2. 无测量信息状态为 not_run。
3. 脚本静态检查不等于浏览器可访问性验收。

## 本技能包含
- `scripts/static_audit.py`
- `scripts/check_budget.py`
- `examples/metric-result.json`
- `references/testing-matrix.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
