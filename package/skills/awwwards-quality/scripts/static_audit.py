#!/usr/bin/env python3
"""Lightweight static audit. Its pass is NOT browser/keyboard/Lighthouse success."""
import argparse,json,sys
from html.parser import HTMLParser
from pathlib import Path
class Audit(HTMLParser):
 def __init__(self):
  super().__init__();self.stack=[];self.tagcounts={};self.errors=[];self.ids=set();self.links=[];self.lang=False;self.desc=False;self.titles=[];self.in_title=False;self.title='';self.buttons=0
 def handle_starttag(self,t,a):
  d=dict(a);self.tagcounts[t]=self.tagcounts.get(t,0)+1
  if t=='html':self.lang=bool(d.get('lang'))
  if t=='meta' and d.get('name')=='description' and d.get('content'):self.desc=True
  if t=='title':self.in_title=True
  if d.get('id'):self.ids.add(d['id'])
  if t=='img' and 'alt' not in d:self.errors.append('image missing alt')
  if t=='a':
   href=d.get('href','')
   if href.startswith('#'):self.links.append(href[1:])
   if not href:self.errors.append('a missing href')
  if t=='button':self.buttons+=1
 def handle_data(self,data):
  if self.in_title:self.title+=data.strip()
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();s=a.path.read_text(encoding='utf-8');parser=Audit();parser.feed(s);e=parser.errors
 if not parser.lang:e.append('missing html lang')
 if not parser.desc:e.append('missing meta description')
 if not parser.title:e.append('missing title')
 if parser.tagcounts.get('main',0)!=1:e.append('page must have exactly one main')
 if parser.tagcounts.get('h1',0)!=1:e.append('page must have exactly one h1')
 if 'main' not in parser.ids:e.append('main requires id=main')
 for ref in parser.links:
  if ref and ref not in parser.ids:e.append('broken internal anchor #'+ref)
 if 'prefers-reduced-motion' not in s and 'styles.css' not in s:e.append('no visible reduced-motion path or linked stylesheet (verify manually)')
 print(json.dumps({'passed_static':not e,'errors':e,'counts':parser.tagcounts,'limitations':['does not execute JavaScript','does not test focus order, 320px viewport, network, or color contrast','linked stylesheet must be inspected separately']},ensure_ascii=False,indent=2));sys.exit(bool(e))
