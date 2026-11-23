#!/usr/bin/env python3
import json, collections
from pathlib import Path
r=Path(__file__).resolve().parents[3]/'research/archive/sites_of_the_month.json'
d=json.loads(r.read_text(encoding='utf-8')); rows=d['rows']
print(json.dumps({'record_count':len(rows),'coverage':d['scope'],'award_types':dict(collections.Counter(x['award_type'] for x in rows)),'unknown_months':[x['id'] for x in rows if x.get('award_month') is None],'method':d['method']},ensure_ascii=False,indent=2))
