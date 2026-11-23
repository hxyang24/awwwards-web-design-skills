---
name: awwwards-pattern-bounded-physics
description: Implement a distinct bounded physics pattern with recorded source-state observations, a standalone original example and explicit fallback, keyboard and lifecycle contracts.
---

# 有界物理装饰：可控对象、等价输入与静态替代

## 用于什么任务
为相应页面增加此机制。它可以与 awwwards-page-external-about, awwwards-page-external-experiment, awwwards-advanced-motion 配合；不要因此替换用户既有框架、品牌、接口或其他页面。

## 读取来源与限制
先读 [具体观察与配方](references/pattern-contract.json)。observed 是已记录的来源观察；recipe 是本库的原创实现方法；源站事实、推断和蓝本验证不得混用。

- 官方作品页将 About 物理效果列为展示点；本轮 About 的两种宽度都显示画布中的装饰性对象堆叠。
- 修正采样工具多余 Escape 输入后，页面保持 About；指针采样期间对象位置发生重排。
- 抓取跟随、精确受力、碰撞规则和源站引擎版本尚未确认；不能把像素变化单独算作对应手势已验证。

## 实施
1. 将物理效果作为说明、导航与内容之外的增强层，保留静态内容及可退出路径。
2. 为对象数量、世界边界、速度与单帧追赶设预算；使用固定时间步，隐藏或离屏后不积累巨大补偿。
3. 指针直接操作同时提供对象选择、按钮与键盘等价操作；指针取消或丢失捕获时解除约束。
4. 播放由用户请求，提供暂停、重置、减少动画和静态路径；销毁取消动画帧、释放对象并移除观察器与事件。

## 不变量与验收
- 示例中的圆、文字和动力学代码为原创，不复制源站角色、音乐或引擎。
- 对象保持边界内且参数有界；模拟是装饰用途，不是科学或生产物理求解器。
- 减少动画时不自动积分；手动定位仍可用，离屏返回不会自行播放。
- 任何输入失败、图形不可用或卸载都不应锁住页面滚动、导航或已有内容。
- 在 320/390/768/1440 宽度检查阅读顺序、主操作、溢出和焦点；实际操作主路径、失败恢复和减少动画路径。
- passed 需要本次运行证据；未执行的源站状态、真实设备或后端接入保留 not_run/blocked。

## 独立原创蓝本
```text
python scripts/scaffold.py --output YOUR_EMPTY_DIRECTORY
```
在导出目录运行 `python -m http.server 8000 --bind 127.0.0.1` 并访问 http://127.0.0.1:8000/ 。拒绝覆盖非空目录，不依赖 npm 或原站素材。此示例不加载原站代码或第三方运行库。

## 剩余边界
- 源站对象抓取和移动端真实触控尚未确认；原创示例的拖动不是源站手感复刻。
- 软件浏览器测试不等于真机、完整辅助技术或生产性能验收。

原站图像、字体、视频、音乐和标志不随技能分发。所有示例文案、几何和行为代码为原创；第三方库适用各自许可。
