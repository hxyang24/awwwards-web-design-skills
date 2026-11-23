---
name: awwwards-page-external-brand-guide
description: Design and implement a external brand guide page with task-specific structure, state contracts, original runnable blueprint and explicit source-evidence boundaries.
---

# 获奖来源外站品牌指南、资源与可控演示

## 适用任务
理解品牌指南、资产权利与版本，可靠计算、复制、演示及下载原创示例。 使用于这一页面族；不要把它扩张为完整网站或所有业务的通用流程。现有项目优先保留其框架、品牌、路由和真实接口。

## 先读取
读取 [页面契约](references/page-contract.json)。其中 regions 是建议结构，workflow 是原创实现步骤，sources/visual_metrics 才是已记录观察。当前证据层级 `rendered_source_observations`；页面族覆盖 `observed_examples`。同类页面共用此技能，但这不证明该页面族所有网站均已逐页检查。

## 页面结构与实施
建议区域：指南身份、章节导航、原创色板、对比度计算、标志、图标组合、可控动效、下载与复制回退。
1. 把指南内容、品牌资产许可、示范工具和真实产品规则分别记录，不因公开可读而推断允许分发。
2. 核实导航开关及组合示例的局部内容变化；不要用整页截图差异代替作用区域与滚动证据。
3. 为原创色板提供六位不透明 sRGB 对比度计算，使用原始比值判定并说明完整合规仍需其他检查。
4. 复制必须等待设备确认；拒绝、缺失或超时提供可选文本。输入变化使旧计算及其下载失效。
5. 动效仅明确启动，可暂停、继续或重置；减少动态时默认显示静态结果，尺寸或偏好变化取消旧运行。
6. 编辑指南后同步生成完整静态内容及下载；断网、脚本失败、数据不符时仍可阅读并获得原创资源。

## 数据与状态
字段：guide_version, palette[].hex, asset_origin, asset_license, foreground, background, raw_ratio, normal_text_ratio_met, large_text_ratio_met, symbol_order, transition_duration, motion_preference, copy_confirmation。未知值保留 unknown/null，不用演示数据冒充实况。明确主路径、加载、空态、失败恢复、禁用、权限、键盘、减少动画和窄屏状态。布局从语义区域开始，再落实 tokens、组件边界和媒体增强。

关键恢复：无效颜色不能沿用旧比值；复制失败不报成功；过期动画与复制确认不能覆盖当前状态；数据失败保留完整静态指南并可重试。

## 动效与响应式
无自动播放；提供暂停、继续、重置和明确选择；减少动态默认静态，改变视口或偏好取消旧运动；窄屏导航可关闭并恢复焦点。 在 320/390/768/1440 宽度验证内容重排、主操作和溢出；移动软键盘与真机读屏需要额外验证。原站只观察了桌面时，移动决策必须注明为原创推断。

## 可运行原创蓝本
`assets/` 包含独立 HTML/CSS/JS 与契约，不需要 npm 或第三方素材。导出到用户指定的空目录：
```text
python scripts/scaffold.py --output YOUR_EMPTY_PROJECT_DIRECTORY
```
进入导出目录运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。file:// 不能加载 JSON 模块。已有项目按契约移植，不直接覆盖用户代码。

蓝本使用虚构数据和明确本地预览状态。它示范区域、交互与恢复，不意味着按像素复刻原站，也不包含真实业务接口。看见按钮后必须操作测试；静态检查不能代替浏览器证据。

## 验收与交付
交付路由/组件边界、状态矩阵、数据契约、来源和素材台账、实际运行命令、截图及未测项。检查契约中的每条 acceptance，记录 passed/failed/blocked/not_run 并给出证据。不要从一个测试通过推断整站、全部设备或生产已验收。

## 已读取的来源
- https://brand.dropbox.com/color（http_dom；2026-11-23T10:47:51.956145+00:00）
- https://brand.dropbox.com/iconography（http_dom；2026-11-23T10:47:52.118545+00:00）
- https://brand.dropbox.com/logo（http_dom；2026-11-23T10:47:52.280266+00:00）
- https://brand.dropbox.com/motion（http_dom；2026-11-23T10:47:52.444187+00:00）

来源受各自版权和访问规则约束；只借鉴结构与机制，使用原创或已授权文案、图像、字体和模型。未知技术版本、隐藏状态和服务端行为不得根据截图补造。

## 品牌指南专项
读取 `assets/guide.json`、`assets/model.mjs` 与 `brand_contract`。先核实真实指南任务、导航和演示作用区域，再建立颜色、标志、图标、运动与素材许可清单。颜色对比度只计算不透明六位 sRGB，显示向下保留两位，使用原始比值判定；输入变化废弃旧结果与下载，不能称为完整 WCAG 认证。复制等待确认，失败或超时提供手工文本；没有自动播放，提供暂停、继续、重置和减少动态的静态路径。修改数据后运行 `python render_static.py` 同步完整无脚本指南与原创建议包。源站资产、标志、字体、截图及视频不公开分发；公开可访问不等于获得素材许可。
