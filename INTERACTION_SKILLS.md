# 具体机制整理为可调用 Skills

页面技能负责该页面的任务与结构；机制技能负责一组具体的视觉、交互与恢复规则。可以按需组合，既有项目继续使用原来的框架与数据服务。

| Skill | 实际交付 | 观察边界 |
|---|---|---|
| [awwwards-pattern-discovery-navigation](skills/awwwards-pattern-discovery-navigation/SKILL.md) | 巨型标题、可展开导航、搜索对话框、浮动章节入口、焦点恢复 | 主站 Explore 展开已操作；原站搜索未提交。蓝本搜索为原创本地筛选。 |
| [awwwards-pattern-careers-culture](skills/awwwards-pattern-careers-culture/SKILL.md) | 双层导航、主动播放与暂停、价值观画廊、岗位过滤与详情预览 | 当前招聘内页的导航、控制标签和画廊有状态观察；影片及申请后端未测。 |
| [awwwards-pattern-immersive-fallback](skills/awwwards-pattern-immersive-fallback/SKILL.md) | 原创 Three.js 图形、静态回退、轻量档、停帧、context loss 恢复与资源销毁 | 源站在本轮环境只观察到兼容回退。正常源站图形体验未验证。 |

例如指定“使用 `awwwards-page-external-careers` 和 `awwwards-pattern-careers-culture`，制作有品牌叙事、岗位过滤和减少动画路径的招聘页面”，先读取两者契约，再按项目的品牌与真实服务实现。示例中的虚构岗位不能充当实况，也不能显示真实申请成功。

在仓库根目录安装全部 68 套技能，或者单独导出一个机制蓝本：

```text
python tools/install_all_skills.py --target YOUR_SKILLS_DIRECTORY
python skills/awwwards-pattern-careers-culture/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

导出目录内运行 `python -m http.server 8000 --bind 127.0.0.1`，访问 http://127.0.0.1:8000/ 。导出不覆盖非空目录。三个机制均能独立运行；图形示例自带有 MIT 许可的 Three.js，使用原创模型，没有复制来源网站的品牌或媒体资产。

## 实际验证

Windows Chromium 下 31 组机制检查通过，包括三套蓝本在 320/390/768/1440 的溢出检查、六次选定无障碍规则扫描、导航焦点、空结果恢复、画廊、动效停止、软件 WebGL 的实际上下文丢失和资源清理。首轮的三处焦点或章节状态问题已修复，首轮失败记录与当前通过记录均保留。

工具另有 5 项检查，覆盖独立导出、拒绝覆盖、来源引用、第三方许可、68 套安装清单与独立招聘实现。测试对象是原创蓝本，未据此宣称原站逐像素重建、全部源站交互或全部页面已完成。

查看 [浏览器回执](research/interaction_skill_validation/browser-results.json)、[工具回执](research/interaction_skill_validation/unit-results.json)、[来源状态观察](research/live_pages/interaction-observations.json)、[来源到技能的候选映射](research/skill_extraction/coverage.json)。候选映射也不算逐页设计审阅完成。

## 来源与权利

主要观察页面：[Awwwards 主站](https://www.awwwards.com/)、[Apple Careers 当前内页](https://www.apple.com/careers/us/)、[Active Theory 当前站点](https://activetheory.net/)。获奖关联来自研究台账中的主站作品详情；当前内页不被宣称为单独获奖，当前内容也不被等同于历史获奖版本。

原站截图、完整 HTML、影片、字体、商标及原站实现不随这些新增技能分发。保留几何测量、状态记录与来源链接。物理设备、真实 GPU、Safari/Firefox、完整辅助技术审阅及真实业务服务尚未验收。
