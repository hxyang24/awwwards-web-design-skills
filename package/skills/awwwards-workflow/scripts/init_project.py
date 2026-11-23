#!/usr/bin/env python3
"""Initialize a new non-destructive, evidence-driven research/build workspace."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

STAGES=[('research','研究来源'),('reference','案例拆解'),('design-system','设计令牌'),('layout','响应式布局'),('content','内容与SEO'),('product-ux','业务任务'),('components','静态组件'),('motion','交互动效'),('webgl','3D增强'),('quality','质量验收'),('release','交付')]

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--goal',required=True);p.add_argument('--kind',choices=['saas','commerce','dashboard','portfolio','editorial','immersive'],default='saas');a=p.parse_args()
 if a.output.exists() and any(a.output.iterdir()):p.error('输出目录不为空：不会覆盖已有用户文件')
 a.output.mkdir(parents=True,exist_ok=True)
 now=datetime.now(timezone.utc).isoformat()
 (a.output/'stages').mkdir(exist_ok=True)
 spec={'schema_version':'1.0','goal':a.goal,'kind':a.kind,'created_at':now,'scope':{'authorized_mutations':[],'deployment_authorized':False},'stages':[x[0] for x in STAGES],'rules':['缺少来源不能写已证实','不伪造浏览器与性能测试','所有业务动作必须标明真实或演示','无许可不复刻品牌资产']}
 (a.output/'PROJECT.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for slug,display in STAGES:
  step={'schema_version':'1.0','stage':slug,'label':display,'status':'not_run','artifacts':[],'tests':[],'notes':'','blocking_issues':[]}
  (a.output/'stages'/f'{slug}.json').write_text(json.dumps(step,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (a.output/'README.md').write_text(f'# {a.goal}\n\n项目类型：{a.kind}\n\n本目录由 awwwards-workflow 创建；所有阶段初始状态均为 not_run。完成验收前不得改为 passed。\n\n运行：`python skills/awwwards-workflow/scripts/validate_stage.py --project {a.output}`（从交付包根目录执行）。\n',encoding='utf-8')
 print(json.dumps({'created':str(a.output),'stages':len(STAGES)},ensure_ascii=False))
if __name__=='__main__': main()
