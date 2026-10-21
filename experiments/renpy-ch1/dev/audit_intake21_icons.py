"""Locate held prop IDs in original planning versus compiled runtime data."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/resource-intake-20261021'
SOURCE='docs/story-v111/source/다람탐정_82씬_실행매핑_V1.1.1.json'
OLD='docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json'
def main():
 plan=json.loads((ROOT/SOURCE).read_text());index={}
 for si,s in enumerate(plan['scenes']):
  for bi,b in enumerate(s['blocks']):
   for ci,c in enumerate(b['cues']):
    r=c['source_record'];index[r['id']]=dict(record=r,block_condition=b['source_block'].get('when',[]),pointer=f'/scenes/{si}/blocks/{bi}/cues/{ci}/source_record')
 old=(ROOT/OLD).read_text()
 live={p:json.loads((ROOT/p).read_text())['records'] for p in ['game/v111/records.json','game/ms14/route.json']}
 icons=json.loads((OUT/'receipt.json').read_text())['held_icons']['assets'];assets=[]
 for a in icons:
  rows=[]
  for e in a['evidence']:
   ref=index.get(e['line_id']);r=ref['record'] if ref else {}
   rows.append(dict(line_id=e['line_id'],planning_source=SOURCE,json_pointer=ref['pointer'] if ref else None,source_text_matches=r.get('text')==e['text'],source_requires_matches=r.get('requires',[])==e['requires'],block_condition_matches=bool(ref) and ref['block_condition']==e['block_condition'],present_in_old_source=e['line_id'] in old,runtime_presence={p:e['line_id'] in records for p,records in live.items()}))
  assets.append(dict(asset_id=a['asset_id'],status='HELD_NOT_RUNTIME_REGISTERED',archive='design/resource-intake-20261021/dialogue-icons-8.zip',archive_commit='ae62bf081fce0e08eebbbf2dcd8896292175bd56',members={k:dict(member=k+'/'+Path(v['path']).name,sha256=v['sha256']) for k,v in a['files'].items()},evidence=rows))
 result=dict(conclusion='IDs have not been renamed. Native D01-D14 records now exist. These eight source props remain held for exact scene/state matching, not because later days are absent.',native_limit='game/room13_v111_days123.rpy + days45 + days610 + days1114',older_limit='dev/import_ms14.py:315 and :342',runtime_days={p:sorted({rid.split('_')[1] for rid in records}) for p,records in live.items()},assets=assets)
 (OUT/'icon-source-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 rows=[e for a in assets for e in a['evidence']]
 print(json.dumps(dict(assets=len(assets),evidence=len(rows),exact_plan_matches=sum(all(e[k] for k in ['source_text_matches','source_requires_matches','block_condition_matches']) for e in rows),present_runtime=sum(any(e['runtime_presence'].values()) for e in rows)),ensure_ascii=False))
if __name__=='__main__':main()
