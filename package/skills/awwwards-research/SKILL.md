---
name: awwwards-research
description: Research historical Awwwards SOTM archives without inventing months, mixing SOTD/SOTY, or claiming unverified technical stacks.
---

# awwwards-research

## 何时使用
涉及历年 SOTM 获奖作品、名单完整性、奖项月份、行业/风格/技术分类、统计及溯源时使用。

## 必要输入
1. 官方获奖作品 URL 和明确月份证据
2. 第三方元数据来源及快照时间
3. 研究时间范围与标签词表

## 严格执行顺序
1. 始终先读取 research/archive/sites_of_the_month.json。
2. 奖项身份与月份来自官方 SOTM 档案或官方公告；SOTD 日期仅保留辅助信息。
3. 按行业、视觉、交互、技术四轴记录，多标签允许重叠。
4. 若月份来源矛盾，分别保留主张和 URL，status=conflict；未知记 null。
5. 统计采用明确分母，不把未标注解释为技术不存在。

## 可运行命令（从完整包根目录运行）
```bash
python skills/awwwards-research/scripts/archive_tool.py stats
python skills/awwwards-research/scripts/archive_tool.py search --year 2025
python skills/awwwards-research/scripts/archive_tool.py search --keyword "Cartier"
python skills/awwwards-research/scripts/archive_tool.py missing
```

## 验收门槛
1. 至少提供 evidence_url 和 retrieved_at。
2. 不能以排名、作品详情页日期、常识或第三方索引推断 SOTM 月份。
3. 旧作品不可用时标识 unavailable；不可假称现场审计。

## 本技能包含
- `scripts/archive_tool.py`
- `scripts/summarize_dataset.py`
- `references/evidence-policy.md`

## 通用规则与失败处理
- 读取现有资料、权限与用户改动后再实施；默认不覆盖非空目录或修改生产资源。
- 不以第三方技术标签推断源码细节；不伪造源码、技术版本、性能数据或现场检查结果。
- 记录每步状态：`passed`、`failed`、`blocked`、`not_run`；只有证据支持时才能写 `passed`。
- 没有浏览器则仅完成可执行的静态与逻辑检查，浏览器项保留 `blocked`，其他阶段继续完成。
- 尊重原站品牌、代码和素材版权：可借鉴交互思想和布局机制，使用原创或获得授权的图文/模型/字体，不复制其受保护内容。
- 脚本使用 Python 3.10+ 标准库为主（某些组件测试使用 Node 18+）；不会默认访问网络。
