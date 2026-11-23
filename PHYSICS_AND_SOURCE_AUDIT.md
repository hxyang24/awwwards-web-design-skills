# 有界物理 Skill 与来源采样审计

`awwwards-pattern-bounded-physics` 将装饰对象的碰撞、输入、暂停和恢复约束写成可调用 Skill，附独立原创 Shape Room 蓝本。它可与 About、实验展示或高级动效页面技能组合。完整全站整理仍在进行。

## 来源观察与原创实现

[Ponpon Mania 官方作品详情](https://www.awwwards.com/sites/ponpon-mania) 报告 SOTD；[当前 About 内页](https://ponpon-mania.com/about) 在手机与宽屏视口显示堆叠字符。针对可见物体的指针取样前后，堆叠排列发生变化。该观察没有建立物体跟随指针的证据，也没有确认源站的物理引擎、碰撞参数、触屏、暂停或键盘行为。当前内页不被宣称为独立获奖或历史版本复现。

原创蓝本使用八个编号圆形和自行实现的 Canvas 2D 装饰模型；没有复制角色、音乐、字体、原站源代码或截图。Skill 将下列内容明确记为原创实现与建议约束：

- 固定步进、有限对象数与速度、时间步和碰撞预算，避免页面长时间恢复后失控。
- 指针捕获、取消和释放；等价的选择及键盘定位控件。
- 主动播放、暂停、重置、减少动画偏好、离屏和后台停帧；返回时不自动重启动画。
- 无渲染能力或无脚本时保留静态图与说明；隐藏增强内容不丢失正文。
- 销毁时释放输入、观察器和动画；不接管所在页面的其他按钮。

这是一种可控装饰模型，未进行科学仿真或生产物理验收。

## 调用与运行

```text
python tools/install_all_skills.py --target YOUR_SKILLS_DIRECTORY
python skills/awwwards-pattern-bounded-physics/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

在导出目录启动 `python -m http.server 8000 --bind 127.0.0.1`，打开 http://127.0.0.1:8000/ 。蓝本无需安装运行依赖。可指定“读取 bounded-physics 与 external-about Skill，为品牌介绍页实现可暂停的原创物理装饰，并保留静态内容”，再按真实项目接入品牌和数据。

## 实际通过的检查

| 对象 | 结果与范围 |
|---|---|
| 原创模型 | 8 项：预算、有限时间步、重力、碰撞、拖动边界、键盘移动、可重复长序列、重置与销毁 |
| 物理浏览器专项 | 16 组：320/390/768/1440 宽度、两次选定无障碍规则扫描、状态控制、鼠标、触控仿真、取消、离屏、隐藏、静态替代及宿主控件独立性 |
| 来源采样工具 | 12 项原创夹具：遮挡/隐藏、错误/兼容/未找到、画布待审及动作后清理 |
| 故事增强回退 | 35 组叙事/提示词专项中包含三章无脚本全文、原生深链接焦点与数据失败恢复 |

物理专项首次离屏检查因测试视口仍能看到部分画布而失败；检查改为先证明画布已完全离屏，再检查停止，保留原失败回执。触控使用 Chromium 仿真，未进行真机、Safari/Firefox、真实 GPU 性能或完整辅助技术验收。自动规则扫描不能替代完整无障碍验收。

回执：[模型](research/physics_skill_validation/engine-results.json)、[物理浏览器](research/physics_skill_validation/browser-results.json)、[来源采样](research/source_state_validation/browser-results.json)、[来源状态摘要](research/live_pages/interaction-observations.json)。公开图片均为原创蓝本截图，原站截图留在私有研究缓存。

## 来源采样修正与限制

原采样工具在普通动作后也按 Escape。在 Ponpon 中这可能关闭 About 并返回首页，使下一动作落到错误页面。本轮修正为只有明确要求 Escape 或确认新增对话框后才清理，并记录动作前后地址与清理结果。已重新观察物理页面，旧的跳页样本不作为正常 About 交互的依据。

来源截图保留动画运行，不再为截图快进源站 CSS 动画。可见标题需检查透明度与遮挡；加载覆盖层、未找到、错误和兼容回退分别记录。只有自动可见内容信号仍需人工视觉审阅；画布存在不能证明图形正确、WebGL 使用或完整体验成功。

HTTP 采样对 404/410 保留有界 HTML 错误参照，并从普通来源选择中排除提示为错误的页面。`content_state_hint=unclassified` 表示未被标题/标题节点规则识别，不代表页面正常。403、robots 拒绝和挑战页保持受限状态，没有绕过。

这些修正验证工具的保守判定与原创模板行为，不能证明每个源站、每个页面或隐藏状态已整理完成。待审队列与全站目标见 [完成标准](docs/FULL_SITE_SKILLS_GOAL.md)。
