"""Apply reviewed object centers, retaining the original game's positions for comparison."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'scene-map.json';s=json.loads(p.read_text());override=json.loads((root/'scene-point-overrides.json').read_text())
for key,fix in override['locations'].items():
 l=s['locations'][key]
 for e in l['evidence']:
  if e['spotId'] in fix.get('evidence',{}):e['point']=fix['evidence'][e['spotId']]
 for o in l['observations']:
  if o['id'] in fix.get('observations',{}):
   o.setdefault('sourcePoint',o['point']);o['point']=fix['observations'][o['id']];o['x'],o['y']=o['point']
 for zk,z in l['zooms'].items():
  for it in z['items']:
   point=override.get('zooms',{}).get(zk,{}).get(it['id'])
   if point:it['x'],it['y']=point
   for e in l['evidence']:
    if e['inZoom']==zk and e['spotId']==it['id']:e['point']=[it['x'],it['y']]
for l in s['locations'].values():
 for e in l['evidence']:assert 0<=e['point'][0]<=360 and 0<=e['point'][1]<=200
s['reviewedLocations']=list(override['locations']);s['placementVersion']=3
p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('Reviewed location mappings:',len(override['locations']))
