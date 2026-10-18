"""Preserve approved sources and create map-only derivatives for three shared actions."""
import hashlib,json
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'art/cooperative-work-three-20261018';COMMIT='8b553e7ce1e81543c3415f5ba9c3f329907ee78e'
p=ROOT/'game/assets/room13-life-groups.json';reg=json.loads(p.read_text());groups={g['id']:g for g in reg['groups']};receipt=[]
for r in json.loads((SOURCE/'manifest.json').read_text()):
 who=r['person_id'];src=SOURCE/r['file'];assert src.stat().st_size==r['bytes'] and hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256']
 with Image.open(src) as source:im,tr=derive_map_image(source)
 validate_map_image(im);dest=ROOT/'game/assets'/('room13-group-'+who+'-cooperative.webp');im.save(dest,lossless=True,method=6,exact=True)
 sx,sy=tr['source_to_export'];anchors={k:[v[0]*sx,v[1]*sy] for k,v in r['contacts_source_pixels'].items() if k!='gaze_target_direction'}
 anchors['foot']=[(anchors['foot_left'][0]+anchors['foot_right'][0])/2,max(anchors['foot_left'][1],anchors['foot_right'][1])]
 heads={'buri':[250,16,550,450],'resident_tok':[290,60,520,470],'resident_tori':[260,10,550,520]};h=heads[who]
 spec=dict(file=str(dest.relative_to(ROOT/'game')),crop=[0,0,im.width,im.height],head=[h[0]*sx,h[1]*sy,h[2]*sx,h[3]*sy],anchors=anchors,foot=anchors['foot'],contact='shared_work' if who!='resident_tori' else 'standing',facing=r['facing'],stature_ratio=1,source_sha256=r['sha256'],source_commit=COMMIT)
 if who in ('buri','resident_tok'):
  poly=[[400,630],[934,630],[934,830],[400,830]] if who=='buri' else [[120,650],[330,650],[580,850],[330,910],[120,790]]
  spec['foreground_parts']=[[[x*sx,y*sy] for x,y in poly]]
 group=groups['inn_mending' if who=='resident_tori' else 'workshop_pair'];member=next(m for m in group['members'] if m['person']==who)
 member.update(pose='group_cooperative',spec=spec,anchor='foot' if who=='resident_tori' else 'shared_component_contact' if who=='buri' else 'screwdriver_tip',target=[625,545] if who=='resident_tori' else [570,425],height=300 if who=='resident_tori' else 208 if who=='buri' else 220)
 group['status']='awaiting_live_review';group['art_gap']='Approved cooperative source imported; actual engine contacts and clicks must pass before enablement.'
 if who=='resident_tori':
  group['label_position']=[420,150];member['occlusion_polygons']=[[[555, 458], [580, 453], [614, 466], [677, 466], [692, 382], [735, 379], [770, 402], [752, 551], [741, 615], [716, 620], [712, 554], [584, 548], [584, 607], [561, 608]]]
 if group['id']=='workshop_pair':group['label_position']=[460,225]
 receipt.append(dict(person=who,source_sha256=r['sha256'],export=spec['file'],export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=tr))
p.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n');(SOURCE/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,zip_sha256='efebceeba74efcd1f17f62a3fe4a1d8d279056c716cb2dabea3c6d0d100bbdd4',exports=receipt),indent=2)+'\n')
