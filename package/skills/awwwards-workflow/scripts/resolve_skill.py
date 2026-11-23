#!/usr/bin/env python3
import argparse,json
RULES={'历史':'research','获奖':'research','年份':'research','分类':'research','案例':'reference','拆解':'reference','参考':'reference','配色':'design-system','字体':'design-system','设计系统':'design-system','布局':'layout','响应式':'layout','导航':'layout','动画':'motion','动效':'motion','滚动':'motion','3d':'webgl','webgl':'webgl','模型':'webgl','seo':'content','内容':'content','表单':'product-ux','支付':'product-ux','上传':'product-ux','业务':'product-ux','电商':'components','原型':'components','模板':'components','检查':'quality','性能':'quality','测试':'quality','发布':'release','交付':'release'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--task',required=True);a=p.parse_args();q=a.task.lower(); hits=list(dict.fromkeys('awwwards-'+v for k,v in RULES.items() if k.lower() in q));
 print(json.dumps({'task':a.task,'recommended':hits or ['awwwards-workflow'],'entrypoint':'awwwards-workflow'},ensure_ascii=False,indent=2))
