"""Derive smooth profile icons from hash-verified approved neutral originals.
Original-space crops avoid ambiguities from dialogue trim/scale/padding.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SIZE=256
PAD=12

def main(search):
 specs=json.loads((ROOT/'docs/reviews/profile-icons/approved-crops.json').read_text())
 people=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
 wanted={r['source_sha256'] for r in specs};sources={}
 for folder in search:
  for file in Path(folder).rglob('*.png'):
   if file.name not in ('neutral.png','source.png'):continue
   sha=hashlib.sha256(file.read_bytes()).hexdigest()
   if sha in wanted:sources.setdefault(sha,file)
 missing=wanted-set(sources)
 assert not missing, 'Missing approved originals: '+str([r['character_id'] for r in specs if r['source_sha256'] in missing])
 entries={};receipt=[]
 for r in specs:
  who=r['character_id'];frame=people[who]['profiles']['840']['frames']['neutral']
  registered_sha=frame.get('source_sha256') or hashlib.sha256(Path(frame['source_master']).read_bytes()).hexdigest()
  assert registered_sha==r['source_sha256'],who
  source=sources[r['source_sha256']]
  with Image.open(source) as opened:im=opened.convert('RGBA')
  assert list(im.size)==r['source_size'],who
  w,h=im.size;nx,ny,nw,nh=r['face_crop_normalized'];x,y,cw,ch=round(nx*w),round(ny*h),round(nw*w),round(nh*h)
  assert cw==ch and 0<=x<x+cw<=w and 0<=y<y+ch<=h,(who,[x,y,cw,ch])
  crop=im.crop((x,y,x+cw,y+ch)).resize((SIZE-2*PAD,SIZE-2*PAD),Image.Resampling.LANCZOS)
  icon=Image.new('RGBA',(SIZE,SIZE));icon.alpha_composite(crop,(PAD,PAD))
  path=ROOT/'game/assets/profile-source-master'/(who+'.webp');path.parent.mkdir(exist_ok=True)
  icon.save(path,format='WEBP',lossless=True,method=4)
  entries[who]=dict(file=str(path.relative_to(ROOT/'game')),size=[SIZE,SIZE],padding=PAD,source_sha256=r['source_sha256'],source_commit=frame.get('source_commit',people[who]['source_commit']),source_master=frame['source_master'],source_size=r['source_size'],crop=[x,y,cw,ch],sha256=hashlib.sha256(path.read_bytes()).hexdigest())
  receipt.append(dict(character_id=who,verified_original=str(source),**entries[who]))
 assert set(entries)==set(people)-{'resident_solbang'}
 (ROOT/'game/assets/room13-profile-source-art.json').write_text(json.dumps(dict(people=entries,excluded=['resident_solbang','dad','elder','bodum','workshop']),ensure_ascii=False,indent=2)+'\n')
 (ROOT/'docs/reviews/profile-icons/receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 print('Verified and imported',len(entries),'approved original crops')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('search',nargs='+');main(parser.parse_args().search)
