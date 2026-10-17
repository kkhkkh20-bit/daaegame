"""Approved source8 -> original receipts + map-only 768/2px derivatives and placements."""
import ast,hashlib,json,shutil,subprocess
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/workspace/action27-p0-input')
COMMIT='9371f483d2c3e6026cfa3784c90507c91f8e6376'
# Exact full-original coordinates; masks protect only held foreground props/hands.
FOREGROUND={
 'MK-2':[[[450,650],[1000,650],[1000,850],[450,850]]],
 'MK-3':[[[230,480],[630,480],[630,860],[230,860]]],
 'MK-4':[[[315,450],[940,450],[940,960],[315,960]]],
 'MK-5':[[[660,430],[905,430],[905,710],[660,710]]],
 'PO-1':[[[590,700],[1010,700],[1010,935],[590,935]],[[405,540],[480,540],[550,650],[590,720],[630,770],[760,800],[760,930],[600,950],[500,870],[440,780]],[[780,570],[850,570],[890,660],[950,705],[980,780],[900,795],[800,730]]],
 'WS-1':[[[150,490],[650,490],[650,915],[350,915],[350,680],[150,680]]],
}
# anchor, world target, whole-canvas render height, location, occluder name
PLACEMENTS={
 'MK-2':('work_support',[1270,432],160,'market','cheese'),
 'MK-3':('work_support',[1520,438],148,'market','cheese'),
 'MK-4':('foot',[1772,497],160,'market','cloth'),
 'MK-5':('foot',[1915,497],160,'market','cloth'),
 'MK-6':('foot_baseline',[2050,503],160,'market','pots'),
 'PO-1':('parcel_bottom',[1450,548],280,'post','counter'),
 'SQ-2':('foot',[1020,585],220,'square','bench'),
 'WS-1':('work_support',[1585,383],196,'workshop','rbench'),
}
def main():
 src=subprocess.check_output(['git','show','3ff28cc:experiments/renpy-ch1/docs/placement_mockups/make_mockups.py'],text=True)
 occ=next(ast.literal_eval(n.value) for n in ast.parse(src).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='OCC')
 approved=ROOT/'art/approved-action27-p0';(approved/'originals').mkdir(parents=True,exist_ok=True);(approved/'manifests').mkdir(exist_ok=True)
 rows=[];receipt=[]
 for folder in sorted(SOURCE.iterdir()):
  m=json.loads((folder/'manifest.json').read_text());assert m==json.loads((folder/'external-manifest.json').read_text());shutil.copy(folder/'manifest.json',approved/'manifests'/(folder.name+'.json'))
  for r in m:
   who=r['character_id'];key=r.get('request_id',r.get('slot'));srcpath=folder/(r.get('file') or r['source_relative_path']);b=srcpath.read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
   im=Image.open(srcpath).convert('RGBA');assert list(im.size)==r['size']==[1024,1536]
   original=approved/'originals'/(key+'--'+who+'.png');original.write_bytes(b)
   out,transform=derive_map_image(im);validate_map_image(out);file='assets/map-action27/'+key+'--'+who+'.webp';dest=ROOT/'game'/file;dest.parent.mkdir(exist_ok=True);out.save(dest,lossless=True,method=6,exact=True);validate_map_image(Image.open(dest).convert('RGBA'))
   if 'contacts_px' in r:points=r['contacts_px'];head=r['head_bbox_px']
   else:
    norm=r.get('normalized_full_canvas',r.get('contacts_normalized_full_canvas'));points={k:[v[0]*1024,v[1]*1536] for k,v in norm.items() if len(v)==2}
    head=[norm['head_xywh'][i]*(1024 if i%2==0 else 1536) for i in range(4)] if 'head_xywh' in norm else ({'SQ-2':[280,90,300,270],'MK-6':[455,55,300,340]}[key])
   if 'foot' not in points:points['foot']=[(points['foot_left'][0]+points['foot_right'][0])/2,max(points['foot_left'][1],points['foot_right'][1])]
   spec=dict(file=file,crop=[0,0,512,768],head=[v*.5 for v in head],foot=[v*.5 for v in points['foot']],anchors={k:[v*.5 for v in point] for k,point in points.items()},foreground_parts=[[[x*.5,y*.5] for x,y in poly] for poly in FOREGROUND.get(key,[])],contact='behind_counter',stature_ratio=1,source_sha256=r['sha256'],source_commit=COMMIT)
   anchor,target,height,loc,mask=PLACEMENTS[key];width={'market':2160,'post':2160,'square':1920,'workshop':1800}[loc]
   variant=dict(world_width=width,render_height=height,anchor=anchor,target=target,occlusion=[occ[loc][mask]])
   if key=='WS-1':variant['occlusion']=[[[1405,374],[1460,374],[1460,354],[1480,353],[1480,330],[1560,330],[1560,370],[1600,350],[1710,351],[1730,380],[1730,512],[1405,512]]]
   variants={p:dict(variant) for p in ['morning','afternoon','evening']}
   if key=='PO-1':
    contacts=json.loads((ROOT/'docs/reviews/action27-preparation/contacts.json').read_text())['placements']
    for c in contacts:
     if c['request']=='PO-1':variants[c['daylight']]=dict(world_width=c['world_width'],render_height=c['standing_height_reference'],anchor='parcel_bottom',target=c['target'],occlusion=c['occlusion'])
   if key=='PO-1':
    variants['morning']['render_height']=280
    for period in ('afternoon','evening'):variants[period].update(render_height=290,target=[800,540])
   replace=['neutral','activity','inn_activity','world']
   if key=='MK-6':replace+=['map9_pots_display']
   if key=='MK-3':replace+=['living_stamp']
   row=dict(request_id=key,status='approved',person=who,pose='map27_'+key.lower().replace('-','_'),location=loc,periods=[0,1,2] if key=='PO-1' else [0,1],replace_poses=replace,variants=variants,spec=spec)
   if key=='SQ-2':row['max_day']=10

   row['activity']={'MK-2':'장부에 값을 적는다.','MK-3':'저울에 치즈를 올린다.','MK-4':'줄무늬 천을 펼쳐 보인다.','MK-5':'장갑의 구멍을 꿰맨다.','MK-6':'항아리를 들어 보인다.','PO-1':'소포를 창구에 내려놓는다.','SQ-2':'액자 그림을 들어 보인다.','WS-1':'랜턴의 나사를 조인다.'}[key]
   rows.append(row);receipt.append(dict(request_id=key,person=who,source=str(original.relative_to(ROOT)),source_sha256=r['sha256'],source_bytes=len(b),source_size=list(im.size),export=file,export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=transform))
 assert len(rows)==8
 regpath=ROOT/'game/assets/room13-map-action27.json';reg=json.loads(regpath.read_text()) if regpath.exists() else dict(schema=1,status='approved_p0_eight')
 reg.update(source_commit=COMMIT,rows=rows+[r for r in reg.get('rows',[]) if r['request_id'] not in PLACEMENTS])
 regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
 (approved/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,rows=receipt),indent=2)+'\n')
if __name__=='__main__':main()
