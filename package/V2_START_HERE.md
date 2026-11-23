# Awwwards Skills V2.0 完整交付

日期：2026-11-23（Asia/Shanghai）。本包是在实际读取并解压 V1 完整 ZIP 后扩展，不是按聊天摘要重造 V1。12 套既有技能、研究、原始示例和历史报告全部保留原字节，新增 12 套，共 24 套。

## 先运行
需要 Node.js 20+；演示运行不需要联网或安装依赖，GSAP/Three.js 必要浏览器模块已随包保留许可。
```text
cd v2
node server.mjs
```
打开 http://127.0.0.1:4173/ 。不要双击 HTML 使用 file://；浏览器模块和 JSON 加载需要 HTTP。服务只监听本机，不自动部署。

## 安装技能
先预览，再复制到你选定的技能目录。Python 3.10+：
```text
python v2/tools/install.py --list
python v2/tools/install.py --target YOUR_SKILLS_DIRECTORY
```
同名目录一律跳过，不覆盖。这里只打包交付，未修改你机器的已安装技能。新技能正文可独立使用，集中演示/工具继续位于完整包路径。

## 给 AI 的入口
V1 原工作流仍有效。V2 项目先读本文件，再读 `v2/docs/AI_WORKFLOW.md`；按任务选择 `skills/awwwards-page-library`、企业后台、金融、电商、Agent、移动、动效、3D 或视觉重建专项。旧技能的脚本、名称和接口不变。

## 单独导出新模板
```text
python v2/tools/scaffold.py --kind enterprise --output YOUR_EMPTY_PROJECT_DIRECTORY
```
kind 可选 enterprise、fintech、commerce、agent、mobile、studio。导出后在新项目中运行 `node v2/server.mjs`。拒绝覆盖非空目录；这会复制模板和所需本地资源，不连接任何真实业务。

## 内容索引
- `skills/`：24 套技能，每套有输入、执行、产物、失败处理与证据边界。
- `research/`：原版 206 条档案、30 个案例、来源及冲突记录；本轮未重新核验全部历史站点。
- `examples/`：原版 6 个蓝本。
- `v2/demos/`：新增 Morrow、Axis、Forma、Relay、Daylight、Orbit，另有可搜索页面库和原创视觉参照。
- `v2/library/page-patterns.json`：82 个页面规格，22 个标记可运行路由，详见 `v2/docs/COVERAGE.md`。
- `v2/tools/`：截图、图片尺寸/颜色分析、视觉差异、引用简报校验、验收校验、安装与完整性核验。
- `v2/evidence/`：这次实际测试结果与截图。根目录 `tests/` 是保留的 V1 历史证据。
- `v2/docs/VALIDATION.md`：最终实测、未测和限制。

## 重跑测试
```text
cd v2
python tools/verify.py
npm ci
npx playwright install chromium
npm test
npm run test:tools
npm run test:browser
npm run test:export
```
测试依赖和 Chromium 初次安装需要网络。依赖被精确锁定；不把 node_modules 或浏览器二进制塞进交付 ZIP。

完整性检查应在未修改的解压包中先执行。重跑测试会更新 `v2/evidence/`，之后与出厂清单出现证据哈希差异是预期行为；保留原始 ZIP 作为交付基准。只重查结构和 V1 保留情况可运行 `python tools/verify.py --structure-only`。

## 保证范围
完整并不表示世界上所有页面均已实现或验收。页面目录明确区分规格和示例；真实服务端授权、持久化、支付、交易、模型与生产部署未接入。浏览器模拟与本机软件 WebGL 不能代替真机 GPU、手机键盘、读屏与真实用户性能验证。
