#!/usr/bin/env python3
"""Suggest focused skills; does not execute actions or replace user scope."""
import argparse,json
RULES=[
 ('enterprise',['后台','crm','erp','审批','权限','enterprise','admin']),('fintech',['金融','行情','交易','订单簿','fintech','trading','portfolio']),
 ('ecommerce',['电商','购物车','结算','commerce','checkout','store']),('ai-agent',['agent','工作流','工具审批','chatbot','模型']),
 ('mobile',['移动','手机','触控','mobile','responsive']),('advanced-motion',['动效','动画','gsap','motion','animation']),
 ('3d-experience',['three','3d','webgl','shader']),('design-intelligence',['截图','参照','screenshot','reference']),
 ('visual-reconstruction',['重建','复现','rebuild','reconstruction']),('visual-diff',['视觉差','对比截图','visual diff','截图','复现','重建']),
 ('page-library',['页面','网站','路由','page','website','route'])]
def route(task):
 text=task.casefold();skills=['awwwards-workflow']
 for name,terms in RULES:
  if any(term in text for term in terms):skills.append('awwwards-'+name)
 if len(skills)==1:skills.append('awwwards-page-library')
 skills.append('awwwards-acceptance-docs')
 return {'task':task,'suggested_skills':skills,'entry':'V2_START_HERE.md','scope':'Routing suggestion only. Read current project and user instructions; no implied external authorization.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--task',required=True);a=p.parse_args();print(json.dumps(route(a.task),ensure_ascii=True,indent=2))
