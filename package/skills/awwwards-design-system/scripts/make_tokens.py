#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
PALETTES={
'fintech':{'background':'#0B1522','surface':'#142438','text':'#F7FAFC','muted':'#C4D3DF','primary':'#8FE3C2','on_primary':'#06221A','border':'#587184','focus':'#F6CA56'},
'editorial':{'background':'#FCFAF5','surface':'#FFFFFF','text':'#191C1A','muted':'#48524B','primary':'#1C5843','on_primary':'#FFFFFF','border':'#89938A','focus':'#8256C4'},
'playful':{'background':'#FCF4E7','surface':'#FFFFFF','text':'#211A23','muted':'#51485A','primary':'#5F2E7C','on_primary':'#FFFFFF','border':'#877F94','focus':'#B3420D'},
}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preset',choices=PALETTES,default='fintech');p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 if any(a.output.iterdir()):p.error('输出目录不为空，拒绝覆盖已有文件')
 d={'schema_version':'1.0','preset':a.preset,'colors':PALETTES[a.preset],'typography':{'font_family':'system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif','body_rem':1,'heading_scale':[1.25,1.56,1.95,2.44,3.05],'line_height':1.6},'spacing':{'xs':4,'sm':8,'md':16,'lg':24,'xl':40,'xxl':64},'radii':{'sm':6,'md':12,'lg':20},'breakpoints':{'phone':320,'tablet':768,'desktop':1200},'contrast_pairs':[{'foreground':'text','background':'background','minimum':4.5},{'foreground':'muted','background':'background','minimum':4.5},{'foreground':'on_primary','background':'primary','minimum':4.5}]}
 (a.output/'design-tokens.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 css=':root {\n'+''.join(f'  --color-{k.replace("_","-")}: {v};\n' for k,v in d['colors'].items())+''.join(f'  --space-{k}: {v}px;\n' for k,v in d['spacing'].items())+'}\n'
 (a.output/'tokens.css').write_text(css,encoding='utf-8')
 print(json.dumps({'created':str(a.output),'preset':a.preset,'note':'run validate_tokens.py to verify contrast'},ensure_ascii=False))
