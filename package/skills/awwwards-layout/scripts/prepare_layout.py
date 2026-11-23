#!/usr/bin/env python3
import argparse,json
from pathlib import Path
KINDS={
'saas':['intro','trust','problem','features','workflow','pricing_optional','demo_contact'],
'commerce':['intro','categories','products','details','faq','cart_boundary'],
'dashboard':['overview','filters','kpis','table','empty_error_states'],
'portfolio':['intro','featured_work','project_index','about','contact'],
'editorial':['headline','dek','table_of_contents','sections','references','related'],
'immersive':['intro','static_chapters','progressive_canvas','transcript','continue_action'],
}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=KINDS,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--primary-cta',default='了解更多');a=p.parse_args()
 if a.output.exists():p.error('不会覆盖已有布局规格')
 d={'schema_version':'1.0','kind':a.kind,'landmarks':['header','nav','main','footer'],'skip_link':'#main','sections':[{'id':x,'heading_required':True,'content_visible_without_js':True} for x in KINDS[a.kind]],'primary_action':{'label':a.primary_cta,'needs_destination':True},'viewports':[320,390,768,1024,1440],'interaction_modes':['pointer','keyboard','touch','reduced_motion','no_js'],'requirements':['single main landmark','one logical page h1','visible focus outline','no horizontal content overflow','no information only on hover','no fake success']}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('created',a.output)
