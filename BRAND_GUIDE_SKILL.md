# 品牌指南页面 Skill

新增 `awwwards-page-external-brand-guide`，用于品牌系统、设计指南及原创资源包页面。四个来源章节提炼为同一任务族，不按网址增加四套技能。它与已有作者主页、灵感参考、商品、集合和技术产品技能分开，当前共24核心、50页面、4机制，78套。全站及所有获奖外站内页仍未全部提炼。

## 使用与交付

先读取 `skills/awwwards-page-external-brand-guide/SKILL.md` 与 `references/page-contract.json`。导出到一个空目录：

```text
python skills/awwwards-page-external-brand-guide/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

进入导出目录后运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 `http://127.0.0.1:8000/`。模板不依赖外部字体、库或在线图片。修改 `guide.json` 后运行 `python render_static.py`，同步全文、色板、资源文件及数据摘要；不能只更换JSON而保留旧静态内容。

原创虚构 Common Room 指南包含六色调色板、双框圆心标志、四个几何图标、两个运动预设。所有章节一直可读；窄屏可打开原生模态导航，Escape恢复触发焦点，选择章节聚焦标题，变宽时回到可见导航。无脚本或数据失败仍保留完整内容、原生SVG/CSS/JSON下载与恢复入口。

## 可验证的工具边界

对比度工具只接受不透明六位 sRGB 十六进制；使用 W3C 相对亮度公式中的0.04045分段值、0.2126/0.7152/0.0722权重及亮暗比值。正常文本阈值4.5:1、大文本阈值3:1用未舍入比值判断，显示向下保留两位，避免把4.499显示成已达4.50。大文本资格仍取决于字号和字重；不处理透明、图片、渐变或其他色域，不把单个比值称为完整WCAG合规。

原始依据：[WCAG 2.2相对亮度](https://www.w3.org/TR/WCAG22/#dfn-relative-luminance)、[W3C对比度说明](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)。已直接读取官方页面核对公式；这里只转述数值和适用边界。输入或交换后旧结果及其下载失效，错误不伪装成旧值成功。

复制颜色或色板等待实际设备确认；拒绝、缺失、超时提供选中文本供手工复制。晚到的旧确认不能覆盖新操作。图标组合仅重排本地原创元素。运动从不自动启动，可暂停、继续和重置；界面等待浏览器确认暂停后才报告暂停。减少动态默认静态终点，明确勾选才允许本次预览；偏好、尺寸或预设改变取消旧运行。清理只取消自有监听、动画、下载地址和等待，不改宿主历史及内容。

## 来源事实及权利

已匿名读取并有限观察 [颜色](https://brand.dropbox.com/color)、[标志](https://brand.dropbox.com/logo)、[图标](https://brand.dropbox.com/iconography)、[动效](https://brand.dropbox.com/motion)。有限截图人工审阅、导航开关、图标示例局部文字和几何变化有记录；布局与动作观察不等于完整状态验收。四个精确来源身份绑定缓存摘要，改变后须重审。另有[官方作品详情](https://www.awwwards.com/sites/dropbox-brand)标题的SOTD标签观察，未独立审核当前每个内页获奖或历史版本一致性。

没有操作源站复制、下载许可、完整动效、全部偏好和错误状态。原站颜色、标志、字体、图标、文字、图片、影片、截图及HTML不进入公开包。模板的代码、文字、颜色和SVG是独立原创MIT示例；来源品牌、素材和商标权利不由本许可授予。真实项目须建立逐项出处、版本、许可证及授权台账，无法确认权利的素材不分发。

## 验证方式

```text
node tools/test_brand_model.mjs
node tools/test_brand_page.mjs
python tools/test_page_skills.py
node tools/test_page_skills.mjs
```

浏览器测试使用仓库锁定的测试依赖，默认读取 `package/v2/package.json`，并由CI安装Chromium；源码模板本身不需要安装这些依赖。实测报告位于 `research/brand_skill_validation/`。自动规则不能替代读屏、真机、Safari/Firefox、完整人工无障碍、生产性能或源站逐像素重建验收。全站完整覆盖仍是未完成工作。

固定快照实测：品牌指南30组浏览器、13项模型，页面工具32项与完整50页44组检查通过，V1 187文件一致。新指南另覆盖320/390/768/1440宽度。首次测试发现并修复标志说明对比度和暂停确认时序；失败记录保留于私有工作台账。最终提交CI、独立ZIP与公开资产读回另有回执。
