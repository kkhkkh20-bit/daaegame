"""Approved four originals, plus the authorized KI-1 daily kitchen activation.
Run after the action27 importers. Originals are never pixelated in-place.
"""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import derive_map_image,validate_map_image
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path('/workspace/nabi-extra4-input');COMMIT='64264145c81635843cfde00fdf987dd4c6283f5a'
POSES={'stir_pot':('KI-2','냄비의 수프를 천천히 젓는다.'),'ladle_soup':('KI-3','그릇에 수프를 담는다.'),'wash_dishes':('KI-4','조리대 곁에서 접시를 닦는다.'),'arrange_tray':('KI-5','쟁반에 빵과 수프를 올린다.')}
COUNTER=[[600,530],[790,555],[1100,595],[1620,565],[1620,720],[600,720]]
def days(index):return [d for d in range(2,15) if (d-2)%5==index]
def main():
 manifest=json.loads((SOURCE/'manifest.json').read_text());assert manifest==json.loads((SOURCE/'external-manifest.json').read_text())
 folder=ROOT/'art/approved-nabi-kitchen-extra4';(folder/'originals').mkdir(parents=True,exist_ok=True);shutil.copy(SOURCE/'manifest.json',folder/'manifest.json');receipts=[]
 regpath=ROOT/'game/assets/room13-map-action27.json';reg=json.loads(regpath.read_text());reg['rows']=[r for r in reg['rows'] if r['request_id'] not in {p[0] for p in POSES.values()}]
 for row in reg['rows']:
  if row['request_id']=='KI-1':row.update(periods=[0],days=days(0),min_day=2,activation='daily_kitchen');row['variants']['morning'].update(target=[700,542],occlusion=[COUNTER])
 for index,r in enumerate(manifest,1):
  assert r['character_id']=='nabi';pose=r['pose_id'];key,activity=POSES[pose];src=SOURCE/r['file'];b=src.read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
  im=Image.open(src).convert('RGBA');W,H=im.size;assert list(im.size)==r['size'];original=folder/'originals'/(pose+'.png');original.write_bytes(b)
  out,t=derive_map_image(im);validate_map_image(out);file='assets/map-action27/'+key+'--nabi.webp';dest=ROOT/'game'/file;out.save(dest,lossless=True,method=6,exact=True);validate_map_image(Image.open(dest).convert('RGBA'));sx,sy=t['source_to_export'];norm=r['normalized_full_canvas'];points={k:[v[0]*W*sx,v[1]*H*sy] for k,v in norm.items() if len(v)==2};head=[v*(W*sx if i%2==0 else H*sy) for i,v in enumerate(norm['head_xywh'])]
  # Props are source-authored, including the open pot. Keep them above the work surface.
  # The stove's already painted lidded pot is a different vessel; the new pot uses the gap.
  polys={'stir_pot':[[[560,440],[1024,440],[1024,885],[560,885]]], 'ladle_soup':[[[40,400],[500,400],[500,835],[40,835]]], 'wash_dishes':[[[0,540],[420,540],[420,900],[0,900]]], 'arrange_tray':[[[50,550],[620,550],[620,850],[50,850]]]}[pose]
  spec=dict(file=file,crop=[0,0,out.width,768],head=head,foot=points['foot'],anchors=points,foreground_parts=[[[x*sx,y*sy] for x,y in poly] for poly in polys],contact='behind_counter',stature_ratio=1,source_commit=COMMIT,source_sha256=r['sha256'])
  v=dict(world_width=2160,render_height=244,anchor='prop_support',target=[700,542],occlusion=[COUNTER])
  if pose=='stir_pot':v.update(render_height=210,target=[1835,354],occlusion=[[[1590,355],[2080,355],[2080,625],[1590,625]],[[1660,300],[1775,300],[1775,355],[1660,355]]])
  reg['rows'].append(dict(request_id=key,status='approved',person='nabi',pose='map31_nabi_'+pose,location='kitchen',periods=[0],days=days(index),min_day=2,activation='daily_kitchen',replace_poses=['neutral','activity','inn_activity','world','action_1','action_2'],variants={'morning':v},spec=spec,activity=activity))
  receipts.append(dict(request_id=key,pose=pose,source=str(original.relative_to(ROOT)),source_size=[W,H],source_bytes=len(b),source_sha256=r['sha256'],export=file,export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),transform=t))
 assert len(receipts)==4 and len({r['request_id'] for r in reg['rows']})==31
 reg.update(status='approved_31_sources_31_scheduled',nabi_extra4_source_commit=COMMIT);regpath.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n');(folder/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,source_archive_bytes=4572352,source_archive_sha256='d86dd434a00dd27abf6613699b65187393efbd39563fdfb35bb350486443049f',rows=receipts),indent=2)+'\n')
if __name__=='__main__':main()
