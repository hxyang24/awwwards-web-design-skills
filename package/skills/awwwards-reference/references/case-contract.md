# 代表案例事实与蓝图契约

案例的 `sources` 存储 URL 和支持范围。每条 `facts[*]` 都要引用 `source_ids`。`inferences` 单独保存。`blueprints` 为原创重建建议，不视为原站源代码。`inspection_plan.status=not_run` 代表没有进行现场浏览器检查，不能补上声称已验证的画面和性能数字。

推荐先运行：

```bash
python skills/awwwards-reference/scripts/case_tool.py validate
python skills/awwwards-reference/scripts/case_tool.py show --id terminal-industries
```

输出重建方案时，必须包含：可读 DOM → 状态图 → 技术选型及替代方案 → 动效与资源清理 → 移动回退 → 验收和未解决问题。
