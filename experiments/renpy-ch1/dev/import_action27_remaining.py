"""Import the 19 approved remaining originals, preserving the shipped P0 rows.
Inputs are the verified source archives extracted to /workspace/action27-rest-input.
No art branch is merged. All anchors use actual source dimensions.
"""
import ast,copy,hashlib,json,shutil
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/workspace/action27-rest-input')
COMMIT='14c7384afcfa0ee374ea5501adf1592b97a5f2af'
# location, contact anchor, target, full-canvas rendered height, optional mask
PLACEMENTS={
 'MK-1':('market','foot',[705,505],160,'prod'),
 'MK-7':('market','foot',[1450,668],218,None),
 'MK-8':('market','foot',[1300,700],251,None),
 'PO-2':('post','foot',[560,600],194,None),
 'PO-3':('post','foot',[1040,640],159,None),
 'IN-1':('inn','foot',[300,655],248,None),
 'ST-1':('store','foot',[1100,430],162,None),
 'ST-2':('store','foot',[1470,640],319,None),
 'SQ-1':('square','foot',[560,540],200,'cart'),
 'GA-1':('gate','foot',[810,620],211,None),
 'CL-1':('clinic','seat',[1150,408],240,None),
 'SC-1':('school','foot',[330,452],210,'desks'),
 'FA-1':('facility','work',[1250,411],193,'desk'),
 'DI-1a':('dining','seat',[660,415],212,'back1'),
 'DI-1b':('dining','seat',[1965,415],236,'back3'),
 'KI-1':('kitchen','board_bottom',[700,542],244,'table'),
 'RI-1':('river','foot',[260,705],176,None),
 'RI-2':('river','foot',[520,712],274,None),
 'FO-1':('forest','inspect_ground',[1250,706],180,None),
}
ACTIVITY={'MK-1':'약초 묶음을 들어 보인다.','MK-7':'바구니를 들고 장을 본다.','MK-8':'류트 줄을 튕긴다.','PO-2':'종이를 펼쳐 말린다.','PO-3':'편지를 안고 나갈 채비를 한다.','IN-1':'빨래를 접어 바구니에 담는다.','ST-1':'자루를 어깨에 메고 옮긴다.','ST-2':'나무 상자를 나른다.','SQ-1':'수레 옆에서 보따리를 펼친다.','GA-1':'명부를 들고 입구를 가리킨다.','CL-1':'침대 가장자리에 앉아 담요를 여민다.','SC-1':'책을 들고 칠판을 가리킨다.','FA-1':'책상에 손을 짚고 이야기를 듣는다.','DI-1a':'수프를 떠먹는다.','DI-1b':'수프를 떠먹는다.','KI-1':'도마 위의 당근을 썬다.','RI-1':'물통에 앉아 낚싯줄을 드리운다.','RI-2':'긴 장대를 땅에 짚는다.','FO-1':'무릎을 낮추고 발자국을 살핀다.'}
REPLACE={'PO-2':['living_bookpaper'],'PO-3':['map9_letters_waiting'],'IN-1':['map9_inn_sort_tie_laundry'],'ST-1':['map9_store_sort_boxes'],'CL-1':['map9_clinic_rest_alive_v2','distressed'],'SC-1':['map9_school_spread_wet_coat'],'RI-1':['map9_river_haul_net'],'RI-2':['map9_rope_coiling']}
# Foreground hands/props are above furniture, never the whole lower body.
FOREGROUND={'MK-1':[[[430,500],[800,500],[800,735],[430,735]]],
 'SQ-1':[[[200,410],[1005,410],[1005,830],[200,830]]],
 'SC-1':[[[660,480],[890,480],[890,850],[660,850]]],
 'FA-1':[[[340,760],[560,760],[560,865],[340,865]],[[800,760],[1024,760],[1024,865],[800,865]]],
 'DI-1a':[[[560,420],[1010,420],[1010,680],[560,680]]],
 'DI-1b':[[[160,400],[510,400],[510,775],[160,775]]],
 'KI-1':[[[50,540],[630,540],[630,875],[50,875]]],}

def main():
 # Historical mockup is a starting polygon only; actual desk tops below were inspected.
 src=__import__('subprocess').check_output(['git','show','3ff28cc:experiments/renpy-ch1/docs/placement_mockups/make_mockups.py'],text=True)
 occ=next(ast.literal_eval(n.value) for n in ast.parse(src).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='OCC')
 occ['facility']['desk']=[[720,411],[1450,411],[1462,445],[1462,625],[720,625]]
 occ['kitchen']['table']=[[600,530],[790,555],[1100,595],[1620,565],[1620,720],[600,720]]
 occ['school']['desks']=[[155,363],[500,363],[500,465],[155,465]]
 approved=ROOT/'art/approved-action27-remaining';(approved/'originals').mkdir(parents=True,exist_ok=True);(approved/'manifests').mkdir(exist_ok=True)
 regpath=ROOT/'game/assets/room13-map-action27.json';reg=json.loads(regpath.read_text());prior_ki=next((r for r in reg['rows'] if r['request_id']=='KI-1'),{});rows=[r for r in reg['rows'] if r['request_id'] not in PLACEMENTS];receipts=[]
 for folder in sorted(SOURCE.iterdir()):
  if not folder.is_dir():continue
  manifest=json.loads((folder/'manifest.json').read_text());assert manifest==json.loads((folder/'external-manifest.json').read_text());shutil.copy(folder/'manifest.json',approved/'manifests'/(folder.name+'.json'))
  for r in manifest:
   key=r.get('request_id',r.get('slot'));who=r['character_id'];p=folder/(r.get('file') or r['source_relative_path']);b=p.read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
   im=Image.open(p).convert('RGBA');W,H=im.size;assert list(im.size)==r.get('size',r.get('size_px'))
   original=approved/'originals'/(key+'--'+who+'.png');original.write_bytes(b)
   out,t=derive_map_image(im);validate_map_image(out);file='assets/map-action27/'+key+'--'+who+'.webp';dest=ROOT/'game'/file;out.save(dest,lossless=True,method=6,exact=True);validate_map_image(Image.open(dest).convert('RGBA'));sx,sy=t['source_to_export']
   norm=r.get('normalized_full_canvas',r.get('contacts_normalized_full_canvas',{}))
   points=r.get('contacts_px') or {k:[v[0]*W,v[1]*H] for k,v in norm.items() if isinstance(v,list) and len(v)==2}
   if 'foot' not in points:points['foot']=[sum(points[k][0] for k in ['foot_left','foot_right'])/2,max(points[k][1] for k in ['foot_left','foot_right'])]
   if 'head_bbox_px' in r:head=r['head_bbox_px']
   elif 'head_xywh' in norm:head=[v*(W if i%2==0 else H) for i,v in enumerate(norm['head_xywh'])]
   elif 'head_bbox_normalized_full_canvas' in r:
    # These supplied values are bounding corners, unlike head_xywh.
    x,y,right,bottom=r['head_bbox_normalized_full_canvas'];head=[x*W,y*H,(right-x)*W,(bottom-y)*H]
   else:
    cx,cy=points['head_center'];head=[cx-180,cy-170,360,340]
   spec=dict(file=file,crop=[0,0,out.width,768],head=[v*(sx if i%2==0 else sy) for i,v in enumerate(head)],foot=[points['foot'][0]*sx,points['foot'][1]*sy],anchors={k:[v[0]*sx,v[1]*sy] for k,v in points.items()},foreground_parts=[[[x*sx,y*sy] for x,y in poly] for poly in FOREGROUND.get(key,[])],contact=r.get('contact',r.get('posture','standing')),stature_ratio=r.get('stature_ratio',r.get('stature_ratio_estimate',1)),source_sha256=r['sha256'],source_commit=COMMIT)
   loc,anchor,target,height,mask=PLACEMENTS[key];width={'market':2160,'post':2160,'square':1920,'inn':1920,'store':1920,'gate':1920,'clinic':1920,'school':1800,'facility':1920,'dining':2160,'kitchen':2160,'river':2160,'forest':2160}[loc]
   v=dict(world_width=width,render_height=height,anchor=anchor,target=target,occlusion=[occ[loc][mask]] if mask else [])
   if key=='DI-1a':v['secondary_targets']={'bowl_bottom':[720,365]}
   if key=='DI-1b':v['secondary_targets']={'bowl_bottom':[1934,356]}
   variants={p:copy.deepcopy(v) for p in ['morning','afternoon','evening']}
   if loc=='post':
    for period in ['afternoon','evening']:variants[period].update(world_width=1280,target=[435,650] if key=='PO-2' else [300,700],render_height=300 if key=='PO-2' else 185,occlusion=[[[366,552],[1030,466],[1030,392],[1279,392],[1279,720],[366,720]]] if key=='PO-2' else [])
   row=dict(request_id=key,status='approved',person=who,pose='map27_'+key.lower().replace('-','_'),location=loc,periods=[] if key=='KI-1' else [0,1,2],replace_poses=['neutral','activity','inn_activity','world']+REPLACE.get(key,[]),variants=variants,spec=spec,activity=ACTIVITY[key])
   if key=='KI-1':
    row['activation']='preview_only_no_existing_kitchen_schedule'
    if prior_ki.get('activation')=='daily_kitchen':
     for field in ['activation','periods','days','min_day']:row[field]=prior_ki[field]
     row['variants']['morning']=copy.deepcopy(prior_ki['variants']['morning'])
   if key=='CL-1':row['min_day']=11
   if key=='FO-1':row['min_day']=2
   if key in ['GA-1','FA-1']:row['costume_id']=r['costume_id'];row['usage']='map_only'
   rows.append(row)
   for loc2,target2,height2 in ({'MK-8':[('square',[1310,615],232),('dining',[120,690],260)],'IN-1':[('school',[180,690],266),('facility',[400,680],262)]}.get(key,[])):
    reused=copy.deepcopy(row);reused['location']=loc2
    for variant in reused['variants'].values():variant.update(world_width=1800 if loc2=='school' else 2160 if loc2=='dining' else 1920,target=target2,render_height=height2)
    rows.append(reused)
   receipts.append(dict(request_id=key,person=who,source=str(original.relative_to(ROOT)),source_sha256=r['sha256'],source_bytes=len(b),source_size=[W,H],export=file,export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=t))
 assert len(receipts)==19 and set(PLACEMENTS)<={r['request_id'] for r in rows}
 reg.update(status='approved_31_sources_31_scheduled' if len({r['request_id'] for r in rows})==31 else 'approved_27_sources_26_scheduled_one_preview',remaining_source_commit=COMMIT,rows=rows);regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
 (approved/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,rows=receipts),indent=2)+'\n');shutil.copy(SOURCE/'archives.json',approved/'source-archives.json')
if __name__=='__main__':main()
