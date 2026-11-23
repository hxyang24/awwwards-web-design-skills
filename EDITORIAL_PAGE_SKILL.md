# 杂志与文章索引页面 Skill

`awwwards-page-external-editorial-index` 将精选故事、主题浏览、完整目录搜索、渐进加载和阅读返回整理为可调用 Skill，附独立原创 Fieldnotes 蓝本。全站整理仍在进行。

## 来源与实际观察

[Àpini Magazine](https://apinistudio.com/blogs/notizie) 的手机与宽屏视口有实际观察；[官方作品详情](https://www.awwwards.com/sites/apini-studio) 在本次读取中确认 Honorable Mention。已操作拒绝 Cookie 提示和 Bespoke 主题入口，目标地址确实进入杂志标签页。

[Emily Nixon 的 b.66](https://www.emilynixon.com/blogs/b-66/) 有精选故事、期刊介绍和文章图像的私有截图审阅。两种宽度下操作 Load 4 more articles 后，可见链接分别由 58 增至 70、56 增至 68。链接增长不独立证明精确新增卡片数，也不代表宣传的全部文章都已逐篇分析。[其官方详情](https://www.awwwards.com/sites/emily-nixon) 保存的标题标为 Honorable Mention，较新的结构化读取返回 403，继续保留这个缺口。

Àpini 页面缺少本工具可识别的可见语义标题，因此自动就绪提示仍为 insufficient_visible_content；人工截图确认了杂志区域可见，不能把该提示等同于空白页或自动提升为全站体验通过。两个当前内页也不被宣称为独立获奖或历史版本复刻。

## 防止误点同名来源控件

先前宽屏采样按 Bespoke 名称选择第一个链接，实际进入了全站导航中的服务页；该样本不作为主题筛选证据。本轮修正后，宽屏的三个同名可见候选由已观察的杂志目标地址明确缩小到一个，并重新操作验证。

`tools/source_target.mjs` 默认拒绝歧义匹配，显式选择器也必须唯一。预期地址必须来自已检查的链接；返回的目标保持严格匹配，后续出现重复节点会停止操作。10 项原创浏览器夹具检查涵盖同名导航、错误地址、隐藏副本、动态重复节点、特殊字符与普通唯一按钮。

原站截图、照片、完整 HTML、文章原文和字体保留在私有研究缓存；公开记录只有摘要、URL、有限状态与哈希。新采样记录见 [来源摘要](research/live_pages/editorial-page-observations.json)。

## 原创蓝本与规则

Fieldnotes 使用十二篇原创短文、虚构作者和 CSS 几何插图。默认先显示四篇，搜索针对完整目录；主题和排序独立保存，未知日期保持未知并排在已知日期之后。

- 加载更多只追加新记录，保留已有节点、当前焦点和已确认数量；失败时保留已有故事并重试同一游标。
- 游标绑定目录版本与查询；筛选改变会取消旧请求，过期响应不能覆盖当前视图。
- 阅读入口提供完整正文。返回后恢复主题、查询、排序、已展开位置及触发点；页内锚点不重新发起目录查询。
- 无脚本或资源失败时，全部十二篇原文和目录仍可读取，并有原生锚点。数据变更后必须重新生成静态内容。
- 空结果、请求失败、未知主题、输入超限和不可用文章分别解释；不能把网络失败包装成零文章。

本地异步适配器用于说明接口与失败行为，不是源站 API。二十条记录的扩展位置已有测试；解析上限只是资源边界，不代表已验收大型目录的生产性能。真实项目应将完整查询、权限、游标和数量接入可信服务，保留已有框架与路由。

## 安装与运行

```text
python tools/install_all_skills.py --target YOUR_SKILLS_DIRECTORY
python skills/awwwards-page-external-editorial-index/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。导出拒绝覆盖已有内容，不需要 npm 或源站素材。

调用时要求先读 `references/page-contract.json` 的 `editorial_contract`，再映射真实文章数据与生产分页接口。示例内容不能充当真实出版记录或真实作者资料。

## 验证与限制

目录模型 12 项检查与页面 30 组浏览器检查通过。页面覆盖四种宽度、两次选定无障碍规则扫描、完整搜索、排序、增量加载、终止、失败重试、取消旧请求、防重复操作、阅读返回、浏览器历史、无脚本、资源失败及清理。

首轮发现 320 宽度的插图横溢出和页内锚点误触查询刷新，已修复。原首轮的禁用检查对象是 fieldset，随后改为直接验证输入控件不可用。完整包复核还发现缩短后的可见阅读文案与辅助名称不一致；现已对齐，两种宽度的无障碍扫描重新通过。各轮失败回执均保留，未覆盖成通过。

[目录模型回执](research/editorial_skill_validation/catalog-results.json) · [页面回执](research/editorial_skill_validation/browser-results.json) · [来源目标夹具](research/source_state_validation/target-results.json)。

未验收全部源站主题、文章正文和终止状态，未接入源站后端或订阅服务；真机、Safari/Firefox、完整辅助技术、大型生产目录和实际跨浏览器缓存恢复未验收。受控生命周期信号不是完整缓存恢复证明，自动扫描也不能替代无障碍验收。

网站族分类、DOM 记录和结构差异仍是待审候选。完整范围及待办见 [全站目标](docs/FULL_SITE_SKILLS_GOAL.md)。
