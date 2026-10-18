import json,hashlib
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'art/approved-piko-guldol-four';COMMIT='d301395b62ba3bb93b3ab050cbd1cf8d0c741937'
OCC=[[331,460],[470,439],[683,441],[1060,483],[1060,624],[890,678],[350,604]]
rows=[];receipt=[]
for n,r in enumerate(json.loads((SOURCE/'manifest.json').read_text())):
 p=SOURCE/'originals'/Path(r['file']).name;assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 im,tr=derive_map_image(Image.open(p));validate_map_image(im);dest=ROOT/'game/assets/map-action27'/('VA-'+str(n+2)+'--'+r['person']+'.webp');im.save(dest,lossless=True,method=6,exact=True)
 sx,sy=tr['source_to_export'];anchors={k:[v[0]*sx,v[1]*sy] for k,v in r.items() if k.startswith(('foot_','hand_'))};anchors['foot']=[(anchors['foot_left'][0]+anchors['foot_right'][0])/2,max(anchors['foot_left'][1],anchors['foot_right'][1])]
 head=[270,0,420,350] if n<2 else [200,10,530,480]
 spec=dict(file=str(dest.relative_to(ROOT/'game')),crop=[0,0,im.width,im.height],head=[head[0]*sx,head[1]*sy,head[2]*sx,head[3]*sy],foot=anchors['foot'],anchors=anchors,contact='standing',stature_ratio=1,source_sha256=r['sha256'],source_commit=COMMIT)
 loc='workshop' if n==3 else 'square';periods=[0,1] if n in (0,3) else [1]
 variant=dict(world_width=1800 if n==3 else 1920,render_height=300 if n<2 else 280 if n==3 else 260,anchor='foot',target=[1050,625] if n<2 else [780,547] if n==3 else [710,580],occlusion=[OCC] if n==3 else [])
 row=dict(request_id='VA-'+str(n+2),status='approved',person=r['person'],pose='map27_'+r['pose'],location=loc,periods=periods,replace_poses=['neutral','activity','inn_activity','world'] if n<2 else ['neutral'] if n==2 else ['map9_stone_tapping'],variants={k:variant for k in ('morning','afternoon')},spec=spec,activity=['그림판에 풍경을 그린다.','팔레트에서 물감 색을 섞는다.','돌 조각의 결을 살핀다.','가죽 도구집의 끌을 정리한다.'][n])
 if n<2:row.update(max_day=10,days=[1,3,5,6,7,9] if n==0 else [2,4,8,10])
 rows.append(row);receipt.append(dict(id=r['id'],source_sha256=r['sha256'],export=spec['file'],export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=tr,head_bbox_note='visual estimate; inspect in actual background'))
p=ROOT/'game/assets/room13-map-action27.json';j=json.loads(p.read_text());ids={r['request_id'] for r in rows};j['rows']=rows+[r for r in j['rows'] if r['request_id'] not in ids];p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');(SOURCE/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,rows=receipt),indent=2)+'\n')
