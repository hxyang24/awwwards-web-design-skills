# 房地产三维浏览页面 Skill

新增 `awwwards-page-external-property-explorer`，用于公开房地产项目的三维空间浏览、房源比较、即时筛选与详情返回。它不是后台库存系统、工程设计工具或真实日照分析器。当前24核心、51页面、4机制，共79套；原12套及187个V1文件保持兼容。全站及所有获奖外站内页仍未全部提炼。

## 使用

先读对应 `SKILL.md` 与 `references/page-contract.json`。导出到一个空目录：

```text
python skills/awwwards-page-external-property-explorer/scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```

进入导出目录，运行 `python -m http.server 8000 --bind 127.0.0.1`，打开 `http://127.0.0.1:8000/`。模板不需要 npm 或源站素材。三维预览须明确启用，首次加载使用本包固定的Three.js0.187.0及MIT许可；系统字体、静态图、程序化几何和虚构房源均在本地。编辑 `catalogue.json` 后运行 `python render_static.py`，同步完整静态目录、研究笔记与数据摘要，再验证。

## 页面和状态

原创 Court / Yard 包含两栋程序化建筑、12个完整虚构空间、静态示意图与本地笔记下载。空间身份、楼栋、楼层、位置、面积百分之一平方米、半房间单位及未知状态分开；未知面积、房间数、可用状态和价格不转成零或可售。非空面积范围排除面积未知记录，排序始终将未知面积放在已知值后。房间数能保留1.5等分数。

有效筛选即时更新完整目录及可选图形单元；未完成或倒置范围保留并明确标记上次已确认结果，不伪装为空结果。多个特征采用全部满足，不同维度采用AND。窄屏原生模态面板关闭后保留确认选择；断点变化避免焦点留在隐藏表单。详情、Return、浏览器Back/Forward和深链均有恢复路径，保留宿主查询和历史字段。三维点选与键盘列表进入同一详情。

三维按需绘制，没有自动旋转、背景动画或持续帧循环；时间是示例小时，不能当作项目校准日照。视角、旋转、时间和轻量档可操作，像素比有限。图形模块失败仍有完整DOM，可重载页面；WebGL不可用或上下文丢失保留静态图、筛选与阅读，可重新启用新上下文。取消加载和清理不会在晚到模块完成后重新创建图形。释放范围仅包括当前实例的监听、观察器、几何、材质和渲染器。

研究简报仅在本机生成，保留未知值、目录版本及当前视图；选择或视图改变后旧文件地址失效。没有发送询价、预约、消息、支付或真实库存写入。

## 来源与边界

来源为 [Belgrade Arbor三维页](https://belgradearbor.rs/en/3d)，关联[官方作品详情](https://www.awwwards.com/sites/belgrade-arbor)。缓存及新读取的官方标题标签是SOTD；未独立核验当前每个内页获奖或与历史版本相同。

已区分早期加载进度与稍后实际三维画面，在1440/390以及不同运动偏好下分别记录。已操作镜头按钮、时间滑块、Properties→Residences、筛选面板、1 BR选择与关闭再打开：来源报告结果从208变为80并保留。它是界面报告，不是独立库存核验。Properties的视觉大写不是精确可访问名称，首次大写定位未触发点击；按实际名称唯一定位后再操作。时间的归一化值从0.33变为0.331，不能称为“一小时”。

未操作全部房源、商业模式、完整范围和特征组合、真实询价及后台，也未进行完整原站无障碍、所有设备或真实日照审计。源站建筑、贴图、照片、标志、字体、文本、截图及HTML不公开分发。原创建模、文案、静态图、样式和虚构数据适用本库MIT；Three依赖保留 `THREE-LICENSE` 和逐文件来源摘要，来源站权利不由本许可授予。

实现参考为Three.js官方 [WebGLRenderer](https://threejs.org/docs/pages/WebGLRenderer.html)、[Raycaster](https://threejs.org/docs/pages/Raycaster.html)、[BoxGeometry](https://threejs.org/docs/pages/BoxGeometry.html)。已读取官方文档并核对冻结库实际代码；不据此推断参照站采用了同一框架。采用当前冻结版本支持的PCF阴影类型。

## 验证

```text
node tools/test_property_model.mjs
node tools/test_property_page.mjs
python tools/test_page_skills.py
node tools/test_page_skills.mjs
```

开发验证依赖使用仓库 `package/v2` 的锁定版本，三维浏览器测试明确请求软件WebGL；图形是否真正绘制还检查WebGL2上下文、实际三角形/绘制调用、非空像素、镜头与光照变化和实际鼠标射线点选。报告位置 `research/property_skill_validation/`；受控故障夹具与真实正常绘制分别记录。真机、物理GPU、Safari/Firefox、生产性能、完整人工辅助技术、工程、校准日照和真实业务接口仍需另行验收。

固定快照实测：38组完整浏览器、18项模型、34项页面工具和完整51页45组检查通过，原V1 187文件一致。实际软件WebGL2绘制、非空像素、镜头/光照变化及鼠标射线选择都有执行；图形恢复与资源释放不是仅看静态图。测试修正了范围预期数量和异步尺寸读取，画面复查修正手机图裁切及冻结库已移除的阴影常量。独立ZIP与精确提交CI、公开下载回读另有回执。
