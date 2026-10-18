import json,hashlib,copy
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'art/approved-resident-actions-remaining7';COMMIT='69e8e718959253743e4440e71d47c6676ec581b1'
p=ROOT/'game/assets/room13-map-action27.json';reg=json.loads(p.read_text());post=next(r for r in reg['rows'] if r['request_id']=='PO-3')
rows=[];receipt=[]
for n,r in enumerate(json.loads((SOURCE/'manifest.json').read_text())):
 psrc=SOURCE/'originals'/Path(r['file']).name;assert psrc.stat().st_size==r['bytes'] and hashlib.sha256(psrc.read_bytes()).hexdigest()==r['sha256']
 im,tr=derive_map_image(Image.open(psrc));validate_map_image(im);dest=ROOT/'game/assets/map-action27'/('VA-'+str(n+6)+'--'+r['person']+'.webp');im.save(dest,lossless=True,method=6,exact=True)
 sx,sy=tr['source_to_export'];anchors={k:[v[0]*sx,v[1]*sy] for k,v in r.items() if k.startswith(('foot_','hand_'))};anchors['foot']=[(anchors['foot_left'][0]+anchors['foot_right'][0])/2,max(anchors['foot_left'][1],anchors['foot_right'][1])]
 head={'resident_badook':[240,0,540,430],'resident_bori':[340,0,520,430],'doto':[240,0,560,520],'resident_jongjong':[260,0,480,500]}[r['person']]
 spec=dict(file=str(dest.relative_to(ROOT/'game')),crop=[0,0,im.width,im.height],head=[head[0]*sx,head[1]*sy,head[2]*sx,head[3]*sy],foot=anchors['foot'],anchors=anchors,contact='standing',stature_ratio=1,source_sha256=r['sha256'],source_commit=COMMIT)
 if n==0:configs=[('gate',[0],1920,300,[1110,651],['living_bootlace'])]
 elif n==1:configs=[('gate',[0],1920,280,[920,620],['living_firewood'])]
 elif n==2:configs=[('store',[1],1920,340,[1350,689],['living_firewood'])]
 elif n==3:configs=[('square',[0,1],1920,245,[900,620],['action_1']),('hall',[0],2160,255,[1017,669],['action_1'])]
 elif n==4:configs=[('square',[2],1920,245,[900,620],['action_1']),('hall',[1,2],2160,255,[1017,669],['action_1','action_2'])]
 else:configs=[('post',[0] if n==5 else [1,2],0,0,[],post['replace_poses'])]
 for loc,periods,width,height,target,replace in configs:
  variants={daylight:dict(world_width=width,render_height=height,anchor='foot',target=target,occlusion=[]) for daylight in ('morning','afternoon','evening')}
  if loc=='post':
   variants=copy.deepcopy(post['variants'])
   for daylight,v in variants.items():v['render_height']=210 if daylight=='morning' else 240
  row=dict(request_id='VA-'+str(n+6)+'-'+loc,status='approved',person=r['person'],pose='map27_'+r['pose'],location=loc,periods=periods,replace_poses=replace,variants=variants,spec=spec,activity=['순찰용 밧줄의 매듭을 살핀다.','작업장갑을 끼고 장작을 나른다.','자신의 배급표와 주머니를 확인한다.','토시를 끼고 장부에 적는다.','두 배급표의 표기를 비교한다.','우편 봉투를 분류한다.','우편 가방에 편지를 챙긴다.'][n]);rows.append(row)
 receipt.append(dict(id=r['id'],source_sha256=r['sha256'],export=spec['file'],export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=tr,anchors_note='Visual estimates; actual engine and all face targets require review'))
ids={r['request_id'] for r in rows};reg['rows']=rows+[r for r in reg['rows'] if r['request_id'] not in ids];p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n');(SOURCE/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,rows=receipt),indent=2)+'\n')
