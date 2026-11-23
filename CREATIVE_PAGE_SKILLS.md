# 叙事章节与提示词详情 Skills

本轮将三个实际内页类型整理为可调用技能。它们具备独立原创蓝本；来源观察、原创实现和实测回执分别记录。全站整理仍在进行。

| Skill | 任务与可运行行为 | 主要来源与边界 |
|---|---|---|
| [awwwards-page-external-story-index](skills/awwwards-page-external-story-index/SKILL.md) | 章节封面与可用状态、阅读入口、可选进度恢复、未发布章节说明 | [章节索引](https://ponpon-mania.com/chapters) 的手机视口已观察；不复制角色、封面或音乐。 |
| [awwwards-page-external-story-chapter](skills/awwwards-page-external-story-chapter/SKILL.md) | 逐格、全文及横向画格阅读、前后操作、文字替代、失效地址恢复、可选本地记忆 | [章节内页](https://ponpon-mania.com/chapter/1) 在较长加载后可见。声音播放、画布手势和全部隐藏状态未验收。 |
| [awwwards-page-external-prompt-detail](skills/awwwards-page-external-prompt-detail/SKILL.md) | Unicode 与文字方向、可编辑分层配方、复制成功与失败恢复、结果选项卡、放大查看 | [提示词详情](https://aifont.ai/fonts/tagging-letters) 的文字替换、模型选项卡、查看器和手机折叠有状态观察。未调用模型或验证原站模型评测。 |

章节蓝本使用原创 Signal Atlas 故事和 CSS 风景，提示词蓝本使用原创 Letter Lab 配方与系统字体。结果示意不是 AI 模型输出，也不是可安装字体文件。接入真实素材、生成服务或音频后，需要另行确认权利和验证相应状态。

## 安装与导出

仓库共 73 套技能：24 套核心、45 套页面、4 套机制。保留原有技能及其资源位置；安装和导出均拒绝覆盖已有项目。

```text
python tools/install_all_skills.py --target YOUR_SKILLS_DIRECTORY
python skills/awwwards-page-external-story-chapter/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1`，访问 http://127.0.0.1:8000/ 。新蓝本不依赖 npm 或源站素材。可以指定这些 Skill 制作项目页面，也可以将契约移植到既有框架和接口。

## 实测范围

三个新蓝本的 35 组专项浏览器检查通过，覆盖四种宽度、六次选定无障碍规则扫描、章节边界、三种阅读方式、无效地址、进度选择与清除、存储损坏或拒绝、图形隐藏、Unicode 长度、文字方向、配方恢复、文本注入防护、复制等待与失败、键盘选项卡、查看器以及禁用脚本的内容。

章节蓝本现预置三章原创全文和原生章节锚点。脚本关闭或阅读数据加载失败时，所有章节仍可阅读与跳转；只有成功初始化后才开放增强阅读及本地记忆按钮。静态正文由同一份原创数据生成，避免脚本和回退内容分叉。增强路由只在数据初始化完成后启用，加载失败时点击章节不会触发未初始化的阅读器。无脚本深链接的键盘焦点及资源失败时不误报就绪均有独立检查。

复制检查对 API 使用可控替身，以验证等待、拒绝和编辑期间的竞态；未验证操作系统剪贴板集成。真机、Safari/Firefox、实际模型生成、原站声音和完整辅助技术验收未测。35 组通过不能推广为所有源站状态通过。

最初两次验收的末项分别遇到测试匹配器忽略 noscript、普通可见文本读取不包含 textarea 值的问题。实际截图及可见内容检查确认了正文和配方仍可读取；用对应的可见文本或字段值检查后通过。原始记录保留于同一验证目录，未覆盖成虚假成功。后续补查资源失败后的链接操作，复现了未初始化路由错误；增加就绪防护后，全套 35 组重新通过，失败回执另存。

[专项浏览器回执](research/creative_page_validation/browser-results.json) · [来源状态记录](research/live_pages/creative-page-observations.json) · [完整页面检查](research/page_skill_validation/browser-results.json)。

## 继续提炼的依据

来源到技能的候选映射现在关联了实际视口和状态记录；[变体待审账本](research/skill_extraction/variant-backlog.json) 按 DOM 结构特征聚合，帮助定位同类页面中的差异。出现 canvas 不证明使用 WebGL，出现表单不证明提交已验证，结构签名也不算视觉设计完成。

外站来自主站作品详情的明确外链。这个关联不独立证明其获奖状态，也不代表当前内页单独获奖或保持历史版本。原站截图、漫画画格、提示词原文、图像、字体、声音和源代码不随新增技能分发。

## 官方来源状态补核

字体站的官方作品页在保存的 HTTP 观察中标为 Nominee（提名），后续实时读取返回 403；作为补充参照，不计为已确认获奖案例。漫画站官方作品页明确展示 SOTD，但这仍不表示每个当前内页单独获奖。

[官方作品页标题状态台账](research/skill_extraction/award-provenance-coverage.json) 区分 SOTD、Honorable Mention、Nominee 和未确定。它记录来源报告，不能冒充全部获奖网站的枚举或逐一实时复核。
