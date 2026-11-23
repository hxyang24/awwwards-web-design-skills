# V1 → V2 兼容迁移

V1 的 187 个文件全部位于原相对路径，字节未改。原 12 套技能名称、入口、脚本参数、模板目录和研究数据结构继续保留。根目录原 `MANIFEST.json` 仅属于 V1；V2 完整盘点使用 `MANIFEST-V2.json`。

新增技能：page-library、enterprise、fintech、ecommerce、ai-agent、mobile、advanced-motion、3d-experience、design-intelligence、visual-reconstruction、visual-diff、acceptance-docs，完整名称均以 `awwwards-` 开头。

旧 `awwwards-workflow/scripts/resolve_skill.py` 仍为原版 12 技能路由器，不暗改其行为。需要 V2 建议时在完整包根目录运行：

```text
python v2/tools/route_task.py --task "金融交易终端按照截图重建"
```

输出是建议集合，AI 应按实际任务读取。关键词匹配不取代业务理解，也不授权部署、发消息、支付或交易。

安装器默认复制 24 套，已存在同名目录跳过。若需要更新用户已有的同名技能，应先比较差异并在用户授权范围内合并；本交付未替用户覆盖安装。新技能可独立阅读，演示与工具通过安装时生成的 `PACKAGE_LOCATION.json` 定位完整包。

原版的历史测试报告、12 张截图仍保留；V2 重测记录单独位于 `v2/evidence/`。本轮在独立副本中重跑了旧 42 项检查，没有覆盖旧报告。
