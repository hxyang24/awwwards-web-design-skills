# 给 AI 代理的执行手册（从这里开始）

**角色**：你是网站研究员、UI/UX 设计师和前端工程师。你的目标不是套上某个获奖网站的图片，而是按经过核验的模式交付具备可用性、证据与测试记录的原创网站。

## 不允许跳过的 10 条规则

1. 先读取本 `AGENT_START_HERE.md`、`README.md`、目标 skill 的 `SKILL.md`、用户项目现有代码以及项目授权边界。
2. 无输入时选择保守默认，但不得编造品牌、产品功能、公司数据、客户、奖项月份、技术栈版本、性能指标。
3. 目录为空才运行脚手架；原目录非空则读取项目并请求明确授权或使用独立的新目录。绝对不得覆盖未知用户文件。
4. 先完成没有 JavaScript 时仍可读的 HTML 主体与关键任务，再添加动效、3D、特效。
5. 每个按钮和控件要么确实生效，要么显示明确的「预览/尚未接入」边界。无后端不可显示虚假成功。
6. 资料来源分为官方证据、第三方标签、工程推断和原创蓝图；不能相互偷换。
7. 视图状态至少覆盖默认、输入、加载、成功、错误、空数据、禁用、键盘、减少动画和触摸；不适用须写理由。
8. 测试仅在真正执行后可标记 passed；浏览器无法启动记 blocked，性能无测量记 not_run。
9. 3D/WebGL 只是增强层：必须提供 static fallback、资源清理和明确预算，服务端业务权限另行验证。
10. 所有交付列出文件、环境条件、执行命令、已测项、未测项、来源与授权范围。

## 推荐流水线

| 顺序 | 读取技能 | 标准产物 | 进入下一步条件 |
|---|---|---|---|
| 01 | awwwards-workflow | PROJECT.json, stages/*.json | 项目目标与范围已记录 |
| 02 | awwwards-research | 筛选来源与时间表 | 关键获奖信息有来源；冲突保留 |
| 03 | awwwards-reference | 案例 facts + blueprint | facts 与 source_ids 匹配 |
| 04 | awwwards-design-system | design-tokens.json, tokens.css | 对比度验收通过 |
| 05 | awwwards-content / layout | 文案及页面结构 | 语义结构、链接、主流程明确 |
| 06 | awwwards-product-ux | 业务流程状态机 | API/preview 边界明确 |
| 07 | awwwards-components | 可运行页面 | 静态检查和基础行为通过 |
| 08 | awwwards-motion / webgl | 动效和场景 | fallback、cleanup、性能预算齐全 |
| 09 | awwwards-quality | 证据型测试记录 | 失败、阻塞、未运行如实记录 |
| 10 | awwwards-release | 交付清单和 SHA256 | 真实文件匹配声明 |

## 一次最小可运行示例

```bash
python skills/awwwards-workflow/scripts/init_project.py --goal '原创财务SaaS官网' --kind saas --output /tmp/site-project
python skills/awwwards-design-system/scripts/make_tokens.py --preset fintech --output /tmp/site-project/design
python skills/awwwards-design-system/scripts/validate_tokens.py /tmp/site-project/design/design-tokens.json
python skills/awwwards-layout/scripts/prepare_layout.py --kind saas --primary-cta '申请演示' --output /tmp/site-project/layout.json
python skills/awwwards-components/scripts/scaffold.py --kind saas --name '明账' --output /tmp/site-project/site
python skills/awwwards-quality/scripts/static_audit.py /tmp/site-project/site/index.html
# 在 site 目录运行 python -m http.server 8000 后通过浏览器打开 http://localhost:8000
python skills/awwwards-workflow/scripts/validate_stage.py --project /tmp/site-project
```

`validate_stage.py` 初始阶段都为 not_run，返回 `fully_verified=false` 是正确行为，不可在没有证据的情况下改成 true。

## 读取并复用研究成果

- `research/archive/sites_of_the_month.json`：206 条作品记录（部分未知或冲突）
- `research/archive/timeline.csv`：逐月状态（documented、missing_evidence、conflict）
- `research/cases/representative_30.json`：30 个带证据和原创蓝图的案例
- `research/cases/individual/`：30 份单独可读拆解文档
- `research/Awwwards_Research_Skills_2026-11-23.html`：完整历史研究报告
- `examples/`：六类零依赖可运行 HTML/CSS/JS 示例

**所有获奖作品仅作为研究参考。没有包含原网站受版权保护的源代码、图像、音频、3D 模型或商标。**
