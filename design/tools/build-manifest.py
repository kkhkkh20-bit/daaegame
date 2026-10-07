"""Read generated PNG metadata and locate atlas cells; never edit image pixels."""
from pathlib import Path
import json, argparse
from PIL import Image
import numpy as np
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--partial',action='store_true');args=parser.parse_args()
spec=json.loads((root/'character-specs.json').read_text());canon=json.loads((root/'canon.json').read_text());generated=json.loads((root/'generated-assets.json').read_text());outputs=generated['characters'];bgoutputs=generated['backgrounds'];bgs=json.loads((root/'background-specs.json').read_text())
regions={**{k:'silver' for k in ['seol','ppul','tok','bami','sling']},**{k:'mine' for k in ['musoe','somi','seori','ubak','nubi']},**{k:'city' for k in ['eunho','guseul','badook','lamplighter']}}
species={'rabbit':'토끼','bear':'곰','fox':'여우','cat':'고양이','owl':'부엉이','dog':'개','squirrel':'다람쥐','duck':'오리','crow':'까마귀','lynx':'스라소니','crane':'두루미','goat':'염소','mole':'두더지','bat':'박쥐','weasel':'족제비','woodpecker':'딱따구리','peacock':'공작새','panda':'판다','raccoon':'너구리','flyingsq':'날다람쥐'}
cache={}
def atlas(data,opaque=False):
 path=root/data['path'];key=(str(path),data.get('columns',3),data.get('rows',1),opaque)
 if key in cache:return cache[key]
 im=Image.open(path);w,h=im.size;cols=data.get('columns',3);rows=data.get('rows',1)
 xcuts=[round(w*i/cols) for i in range(cols+1)];ycuts=[round(h*i/rows) for i in range(rows+1)]
 # Transparency can shift the crop around an atlas. Locate the quietest safe gaps
 # near expected row/column divisions rather than assuming a fixed cell width.
 if not opaque:
  assert im.mode=='RGBA',str(path)+' must preserve alpha'
  alpha=np.asarray(im.getchannel('A'));assert np.mean(alpha<24)>.06,str(path)+' has no usable transparency'
  ink=alpha>90
  for i in range(1,rows):
   expected=h*i/rows;lo=max(ycuts[i-1]+1,round(expected-h/rows*.13));hi=min(h-1,round(expected+h/rows*.13))
   counts=ink[lo:hi+1].sum(axis=1);mins=np.flatnonzero(counts==counts.min())+lo;ycuts[i]=int(mins[np.argmin(abs(mins-expected))])
  rowxcuts=[]
  for row in range(rows):
   cuts=xcuts.copy();counts=ink[ycuts[row]:ycuts[row+1]].sum(axis=0)
   for col in range(1,cols):
    expected=w*col/cols;lo=max(cuts[col-1]+1,round(expected-w/cols*.12));hi=min(w-1,round(expected+w/cols*.12))
    part=counts[lo:hi+1];mins=np.flatnonzero(part==part.min())+lo;cuts[col]=int(mins[np.argmin(abs(mins-expected))])
   rowxcuts.append(cuts)
 else:rowxcuts=[xcuts for _ in range(rows)]
 result=(w,h,[[[rowxcuts[r][c],ycuts[r],rowxcuts[r][c+1]-rowxcuts[r][c],ycuts[r+1]-ycuts[r]] for c in range(cols)] for r in range(rows)])
 cache[key]=result;return result
characters={};order=[]
for c in spec['characters']:
 id=c['id']
 if id not in outputs:
  if args.partial:continue
  raise RuntimeError('Missing character '+id)
 d=outputs[id];w,h,frames=atlas(d)
 characters[id]={k:v for k,v in c.items() if k not in ['prompt','persona']};characters[id].update({'src':d['path'],'width':w,'height':h,'frames':frames[d.get('row',0)],'labels':['기본','생각·의심','감정'],'region':regions.get(id,'forest'),'species':species[c['animal']],'role':c['persona'].get('tag',c['kind'])});order.append(id)
for id in ['luka','shadow']:
 if id not in outputs:
  if args.partial:continue
  raise RuntimeError('Missing Nero costume '+id)
 d=outputs[id];w,h,frames=atlas(d);c=canon['cast'][id]
 characters[id]={**c,'id':id,'src':d['path'],'width':w,'height':h,'frames':frames[d['row']],'labels':['기본','생각·의심','감정'],'region':'forest','species':'스라소니','role':c['kind'],'bio':canon['bio'].get(id,''),'design':'네로의 동일한 얼굴을 유지한 변장 외형','aliasOf':'nero'}
daram=root/'reference/daram-pixel.png';im=Image.open(daram);w,h=im.size
characters['daram']={'id':'daram','name':'다람','species':'다람쥐 탐정','role':'기존 주인공 디자인','src':'reference/daram-pixel.png','width':w,'height':h,'frames':[[round(w*i/3),0,round(w/3),h] for i in range(3)],'labels':['기본','생각','증거 제시'],'preserved':True}
backgrounds={};bgorder=[]
for s in bgs:
 id=s['id']
 if id not in bgoutputs:
  if args.partial:continue
  raise RuntimeError('Missing background '+id)
 d=bgoutputs[id];w,h,frames=atlas(d,True);backgrounds[id]={'id':id,'name':s['name'],'src':d['path'],'width':w,'height':h,'frames':[frames[d['row']][d['column']]],'caseId':id if id in [c['id'] for c in canon['cases']] else None};bgorder.append(id)
if args.partial and 'main' not in backgrounds:
 im=Image.open(root.parent/'chapter-one/assets/home-pixel.png');w,h=im.size;backgrounds['main']={'id':'main','name':'메인 화면 임시 미리보기','src':'../chapter-one/assets/home-pixel.png','width':w,'height':h,'frames':[[0,0,w,h]]};bgorder.insert(0,'main')
if not args.partial:assert len(order)==35 and len(backgrounds)==17
manifest={'version':1,'game':'다람 탐정 사무소','source':'game.html CAST / BIO / PERSONA / CASES','characterCount':len(order),'preservedCharacters':['daram'],'aliases':{'luka':'nero','shadow':'nero'},'order':order,'characters':characters,'backgroundOrder':bgorder,'backgrounds':backgrounds,'frameFormat':'[x,y,width,height] in original PNG pixels; render with a clipped SVG viewport or equivalent atlas renderer','representativeBackgrounds':True}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(f'Manifest: {len(order)} unique characters + Daram + Nero costumes; {len(backgrounds)} backgrounds')
