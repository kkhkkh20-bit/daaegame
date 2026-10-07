"""Add widescreen location artwork and the original evidence index to the manifest."""
import json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
primary={'cake':'kitchen','window':'under','crown':'props','star':'hill','bell':'tower','dark':'office','museum':'hall','cart':'hill','glove':'parlor','festival':'square','snow':'lamp','clapper':'tower','bureau':'backroom','lining':'cloak','kitchen':'kitchen'}
def augment(m,partial=False):
 source=json.loads((root/'scene-map.json').read_text());assets={}
 for p in sorted((root/'background-results').glob('*.json')):
  batch=json.loads(p.read_text());im=Image.open(root/batch['path']);w,h=im.size;cols=batch.get('columns',2);rows=batch.get('rows',2)
  for n,id in enumerate(batch['ids']):
   col=n%cols;row=n//cols;x=round(w*col/cols);y=round(h*row/rows);pw=round(w*(col+1)/cols)-x;ph=round(h*(row+1)/rows)-y
   fw=min(pw,round(ph*16/9));fh=min(ph,round(pw*9/16));x+=round((pw-fw)/2);y+=round((ph-fh)/2)
   assets[id]={'src':batch['path'],'width':w,'height':h,'frames':[[x,y,fw,fh]],'aspectRatio':[16,9],'safeFrame':True}
 missing=[]
 for key,loc in source['locations'].items():
  art=assets.get(key)
  if art is None:
   missing.append(key)
   if not partial:continue
   art={**m['backgrounds'][loc['caseId']]}
  m['backgrounds'][key]={**art,'id':key,'name':loc['caseTitle']+' · '+loc['name'],'caseId':loc['caseId'],'locationId':loc['locationId']}
 if missing and not partial:raise RuntimeError('Missing actual-location art: '+', '.join(missing))
 for zk,zid in source.get('zoomBackgrounds',{}).items():
  if zid in assets:m['backgrounds'][zid]={**assets[zid],'id':zid,'name':zk+' · 확대 조사','caseId':None}
  elif not partial:raise RuntimeError('Missing zoom art '+zid)
 for cid,lid in primary.items():
  if cid+'-'+lid in m['backgrounds']:m['backgrounds'][cid]={**m['backgrounds'][cid+'-'+lid],'id':cid,'aliasOf':cid+'-'+lid}
 for id in ['main','forest-path']:
  if id in assets:m['backgrounds'][id]={**assets[id],'id':id,'name':'탐정 사무소 · 메인 화면' if id=='main' else '마을을 잇는 숲길','caseId':None}
  else:
   b=m['backgrounds'][id];x,y,w,h=b['frames'][0];fw=min(w,round(h*16/9));fh=min(h,round(w*9/16));b['frames']=[[x+round((w-fw)/2),y+round((h-fh)/2),fw,fh]];b['aspectRatio']=[16,9]
 if not partial:
  assert len(source['locations'])==82 and source['evidenceCount']==250
  assert 'forest-path' in assets and 'main' in assets
 m.update({'version':3,'representativeBackgrounds':False,'aspectRatio':[16,9],'backgroundOrder':['main',*source['locationOrder'],'forest-path'],'locationOrder':source['locationOrder'],'locationCount':82,'evidenceCount':250,'sceneMap':'scene-map.json','zoomBackgrounds':source.get('zoomBackgrounds',{}),'cases':source['cases'],'locations':{k:{f:l[f] for f in ['id','caseId','locationId','name','backgroundId']} for k,l in source['locations'].items()}})
 if partial:m['pendingBackgrounds']=missing
 return m
