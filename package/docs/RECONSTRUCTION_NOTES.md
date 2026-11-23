# 归档与本次打包的来源说明

- 当前容器可读的历史产物是一份 `Awwwards_Research_Skills_2026-11-23.html`。它内部嵌有 `archive`、`cases`、`coverage`、`verification`、`independent_execution_test` 的完整 JSON 数据。
- 本压缩包从这份 HTML **无损提取结构化研究对象**，并导出 CSV、年度 Markdown、30 个案例文档。可在 `research/` 检查其内容。
- 上一轮所提及的 12 个技能的原始脚本目录并未出现在当前容器可访问的路径中。本次按照先前报告中列出的技能名称与职责**重新编写了可运行技能脚本和六类原创代码蓝本**；并非原技能源码的字节级备份。
- `research/coverage/prior_run_verification.json` 和 `prior_execution_test.json` 是上轮报告附带的数据与声明，**不是本次重新编写代码的测试证据**。本次新做的结果位于 `tests/package-test-results.json`。
- 早期历史月份缺口、标签来源、技术推断的边界均保留。没有把不可核验信息自动修正为确定值。
- 客户端 JavaScript 的单元与静态测试不等于 Chrome/Safari 真机测试；如无法启动浏览器，保持 `blocked`。
