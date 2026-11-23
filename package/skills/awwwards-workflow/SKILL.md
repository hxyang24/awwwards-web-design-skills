---
name: awwwards-workflow
description: Orchestrate an evidence-based, accessible Awwwards-inspired website research-to-release workflow with explicit stage gates and honest verification states.
---

# awwwards-workflow

## 何时使用
当要求研究获奖网页并形成实际网站、跨阶段改造网站、交付项目、或不确定先调用哪项专项技能时使用。

## 必要输入
1. 目标、业务类型、最终用户任务
2. 目标仓库/现有项目路径和授权范围
3. 交付形态、已有设计与内容
4. 是否允许新增依赖、部署、替换代码

## 严格执行顺序
1. 读取当前项目、已有文件、git status；不得重置用户改动。
2. 用 init_project.py 建立项目约束和阶段账本。
3. 通过 awwwards-research、awwwards-reference 确认可引用的事实和可借鉴模式。
4. 调用 design-system/layout/content/product-ux 生成无动画基线。
5. 先接入 components，再视必要性调用 motion/webgl 增强。
6. 运行 quality 中可用的静态、自动化和人工测试，并记录 not_run。
7. 调用 release 生成交付清单；除非有真实证据，不得标记通过。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-workflow/scripts/init_project.py --output PROJECT --goal "企业财务SaaS" --kind saas
python skills/awwwards-workflow/scripts/validate_stage.py --project PROJECT
python skills/awwwards-workflow/scripts/resolve_skill.py --task "3D 产品展示"
```

## 验收门槛
1. 每阶段交付 artifacts 数组和 tests 数组。
2. 测试必须记录 status=passed|failed|blocked|not_run 和可核验 evidence。
3. 未测量的性能指标不可填为通过。
4. 业务下单、支付、上传、持久化无后端时必须标为预览，不能假装执行。

## 本技能包含
- `scripts/init_project.py`
- `scripts/validate_stage.py`
- `scripts/resolve_skill.py`
- `references/stage-contract.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
