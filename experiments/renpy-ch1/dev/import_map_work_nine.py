"""Import approved map-only sources; no dialogue/profile registry changes."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def main(source):
 manifest=json.loads((source/'manifest.json').read_text());contacts={x['character_id']:x for x in json.loads((source/'contacts.json').read_text())};rows=[]
 conditions={'resident_piko':('clinic',[0,1,2]),'resident_teacher':('school',[0,1]),'resident_kkwak':('river',[1]),'resident_nubi':('inn',[0]),'resident_mungchi':('store',[1]),'resident_mulgyeol':('river',[0,1]),'resident_dalgeurak':('market',[0,1]),'resident_jongjong':('post',[0,1,2]),'resident_guldol':('workshop',[0,1])}
 for m in manifest:
  f=source/m['source_relative_path'];b=f.read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'];im=Image.open(f).convert('RGBA');assert list(im.size)==m['size'];c=contacts[m['character_id']];x,y,x2,y2=c['crop_bbox_alpha128'];w,h=x2-x,y2-y
  target='assets/map-work-nine/'+m['character_id']+'--'+m['pose']+'.webp';dst=ROOT/'game'/target;dst.parent.mkdir(exist_ok=True);im.save(dst,lossless=True,method=6)
  points=c['contacts_normalized_full_canvas'];feet=[v for k,v in points.items() if k.startswith('foot_') and v];foot=points.get('foot') or ([sum(v[0] for v in feet)/len(feet),max(v[1] for v in feet)] if feet else [.5,1]);foot=[round(foot[0]*im.width-x,3),round(foot[1]*im.height-y,3)]
  spec=dict(file=target,crop=[x,y,w,h],foot=foot,contact='lying' if m['character_id']=='resident_piko' else 'standing',stature_ratio=c['stature_ratio'],source_sha256=m['sha256'],head=[int(w*.15),0,int(w*.65),int(h*.3)])
  if m['character_id']=='resident_kkwak':spec['head']=[307,167,250,190]
  if m['character_id']=='resident_piko':spec['head']=[0,int(h*.12),int(w*.3),int(h*.6)]
  loc,periods=conditions[m['character_id']];rows.append(dict(person=m['character_id'],pose='map9_'+m['pose'],source_pose=m['pose'],source_size=m['size'],location=loc,periods=periods,spec=spec,contacts=c))
 out=ROOT/'game/assets/room13-map-work-nine.json';out.write_text(json.dumps(dict(source_commit='fc2a0e7cc84e0cfbce49064e44a46b6bc3e2a2fa',people=rows),ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);main(p.parse_args().source)
