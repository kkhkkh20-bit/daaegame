import sys,json,hashlib,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'dev'))
from map27_pixel_derivative import derive_map_image,validate_map_image
a=ROOT/'art/approved-badook-lantern';r=json.loads((a/'source-manifest.json').read_text());source=a/'source-original.png';assert hashlib.sha256(source.read_bytes()).hexdigest()==r['sha256']
a=ROOT/'art/approved-badook-lantern';a.mkdir(exist_ok=True);(a/'source-manifest.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
im,tr=derive_map_image(Image.open(source));validate_map_image(im);dest=ROOT/'game/assets/map-action27/VA-1--resident_badook.webp';im.save(dest,lossless=True,method=6,exact=True);validate_map_image(Image.open(dest).convert('RGBA'))
sx,sy=tr['source_to_export'];foot=[(r['foot_left'][0]+r['foot_right'][0])/2,max(r['foot_left'][1],r['foot_right'][1])]
anchors={k:[v[0]*sx,v[1]*sy] for k,v in r.items() if k.startswith(('foot_','hand_'))};anchors['foot']=[foot[0]*sx,foot[1]*sy]
spec=dict(file=str(dest.relative_to(ROOT/'game')),crop=[0,0,im.width,im.height],head=[240*sx,20*sy,540*sx,420*sy],foot=anchors['foot'],anchors=anchors,contact='standing',stature_ratio=1,source_sha256=r['sha256'],source_commit='b9ba25ebc0d0ca2baf114f9fc39d3f5d6f9180c2')
row=dict(request_id='VA-1',status='approved',person='resident_badook',pose='map27_lantern_patrol',location='square',periods=[2],replace_poses=['living_bootlace'],variants={'evening':dict(world_width=1920,render_height=300,anchor='foot',target=[245,676],occlusion=[])},spec=spec,activity='등불을 들고 광장을 순찰한다.')
p=ROOT/'game/assets/room13-map-action27.json';j=json.loads(p.read_text());j['rows']=[x for x in j['rows'] if x['request_id']!='VA-1']+[row];p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
(a/'receipt.json').write_text(json.dumps(dict(source_commit=spec['source_commit'],original_sha256=r['sha256'],export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=tr,notes='Only square evening existing living_bootlace resident; all event offers, special poses, absence and daytime remain authoritative. Head bbox is visual estimate; verify in engine.'),indent=2))
print(row)
