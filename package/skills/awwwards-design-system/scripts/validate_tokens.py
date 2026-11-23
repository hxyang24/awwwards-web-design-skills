#!/usr/bin/env python3
"""WCAG relative luminance contrast verification."""
import sys,json, argparse
from pathlib import Path

def rgb(h):
 h=h.strip().lstrip('#')
 if len(h)==3:h=''.join(x*2 for x in h)
 if len(h)!=6:raise ValueError(f'bad color #{h}')
 return [int(h[i:i+2],16)/255 for i in (0,2,4)]
def lum(h):
 arr=rgb(h);linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in arr]
 return sum(a*b for a,b in zip(linear,(0.2126,0.7152,0.0722)))
def ratio(a,b):
 x,y=sorted([lum(a),lum(b)],reverse=True);return (x+.05)/(y+.05)
def validate(d):
 e=[]; r=[]
 if len(set(d.get('breakpoints',{}).values()))!=len(d.get('breakpoints',{})):e.append('duplicate breakpoint')
 for x in d.get('contrast_pairs',[]):
  try:val=ratio(d['colors'][x['foreground']],d['colors'][x['background']])
  except Exception as err:e.append(str(err));continue
  r.append({'pair':x['foreground']+' / '+x['background'],'ratio':round(val,2),'minimum':x['minimum']})
  if val+1e-9 < x['minimum']:e.append(f'contrast too low: {r[-1]}')
 return e,r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'));e,r=validate(d);print(json.dumps({'passed':not e,'pairs':r,'errors':e},ensure_ascii=False,indent=2));sys.exit(bool(e))
