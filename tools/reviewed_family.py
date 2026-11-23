"""Exact-URL task-family reviews anchored to a particular metadata revision.

This records a reviewed page identity, not completed design extraction. A later
HTTP observation with a different hash invalidates the assignment automatically.
"""
import json,re
from pathlib import Path
from page_research import family

def load_reviews(root):
 root=Path(root);path=root/'research/live_pages/reviewed-page-families.json'
 if not path.exists():return {}
 if path.stat().st_size>1048576:raise ValueError('Shard family reviews before exceeding 1 MiB')
 data=json.loads(path.read_text(encoding='utf-8'));result={}
 if data.get('schema_version')!=1:raise ValueError('Unsupported family-review schema')
 for entry in data.get('reviews',[]):
  if entry.get('family') not in ('external.product','external.collection','external.editorial-index','external.article','external.project','external.service','external.about','external.contact','external.careers'):raise ValueError('Unsupported reviewed family')
  if not re.fullmatch(r'[a-f0-9]{64}',entry.get('source_sha256','')):raise ValueError('Review requires an exact source metadata hash')
  relative=Path(entry.get('evidence_file',''));evidence=(root/relative).resolve()
  allowed=(root/'research/live_pages').resolve()
  if not evidence.is_relative_to(allowed) or evidence.suffix!='.json' or evidence.stat().st_size>1048576:raise ValueError('Invalid bounded review evidence file')
  observations=json.loads(evidence.read_text(encoding='utf-8')).get('observations',[])
  matched=[x for x in observations if x.get('id')==entry.get('evidence_id') and x.get('url')==entry.get('url') and x.get('source_id')==entry.get('source_id') and x.get('status')=='rendered_observed']
  if len(matched)!=1:raise ValueError('Family review lacks one rendered source observation')
  if entry['url'] in result:raise ValueError('Duplicate exact URL review')
  result[entry['url']]=entry
 return result

def assign_family(source,reviews):
 heuristic=family(source['url']);review=reviews.get(source['url'])
 if not review:return {'family':heuristic,'heuristic':heuristic,'assignment':'URL heuristic; not a reviewed design conclusion'}
 if review['source_id']!=source.get('id') or review['source_sha256']!=source.get('source_sha256') or source.get('inspection_level')!='http_dom':
  return {'family':heuristic,'heuristic':heuristic,'assignment':'Reviewed task family is stale or the source is unavailable; requires new review','review_status':'stale'}
 return {'family':review['family'],'heuristic':heuristic,'assignment':'Exact-URL reviewed task family; does not establish complete page design extraction','review_status':'current_metadata_anchor','review':review}
