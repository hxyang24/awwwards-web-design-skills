---
name: awwwards-pattern-discovery-navigation
description: Implement a distinct discovery navigation pattern with recorded source-state observations, a standalone original example and explicit fallback, keyboard and lifecycle contracts.
---

# 发现门户：巨型标题、分组导航与浮动章节入口

## 用于什么任务
为相应页面增加此机制。它可以与 awwwards-page-discovery-home, awwwards-page-website-explorer 配合；不要因此替换用户既有框架、品牌、接口或其他页面。

## 读取来源与限制
先读 [具体观察与配方](references/pattern-contract.json)。observed 是已记录的来源观察；recipe 是本库的原创实现方法；源站事实、推断和蓝本验证不得混用。

- 主站在 1440 宽度呈现约 127px 的居中主标题，390 宽度约 42px；这是两个具体视口的实测值。
- 实际点击 Explore 后，可见链接计数由 118 变为 125。源控件是带点击行为的 span，不据此声称其键盘或 ARIA 已合格。
- 页面存在搜索表单；本轮只读策略排除了提交按钮，因此未执行原站搜索。

## 实施
1. 将跨页面导航、站内章节入口和搜索分成三种独立状态，避免一个按钮承担多重含义。
2. 用 button、aria-expanded 和关联 nav 实现分组导航；打开后可进入链接，Escape、离开区域或点击外部可关闭并维护焦点。
3. 主标题按内容压力缩放，底部章节导航与提示层预留空间，不遮挡主要操作。
4. 本地搜索只是原创蓝本的结果筛选，接真实接口时重新定义查询、加载、空结果和失败恢复。

## 不变量与验收
- 主导航、章节跳转与搜索结果均可用键盘访问。
- 导航缩窄后不得让焦点留在隐藏区域；提示层不能挡住底部入口。
- 源站字体仅作为测量事实，不打包其字体文件或品牌资产。
- 按钮点击后必须检查展开、焦点或结果的实际变化，不仅检查按钮存在。
- 在 320/390/768/1440 宽度检查阅读顺序、主操作、溢出和焦点；实际操作主路径、失败恢复和减少动画路径。
- passed 需要本次运行证据；未执行的源站状态、真实设备或后端接入保留 not_run/blocked。

## 独立原创蓝本
```text
python scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```
在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1` 并访问 http://127.0.0.1:8000/ 。拒绝覆盖非空目录，不依赖 npm 或原站素材。此示例不加载原站代码或第三方运行库。

## 剩余边界
- 原站搜索未提交；蓝本搜索不是原站搜索的复刻。
- 版式配方使用原创几何和系统字体，不声称逐像素一致。

原站图像、字体、视频、音乐和标志不随技能分发。所有示例文案、几何和行为代码为原创；第三方库适用各自许可。
