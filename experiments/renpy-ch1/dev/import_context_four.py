"""Import four exact-context expressions; hold the two differently cast mother images."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image
from prepare_dialogue_source_profiles import resize_source
ROOT=Path(__file__).resolve().parents[1]
COMMIT='d7a55faa91ca85b4a0665d204187ffdc76367daf'
def box(im):return im.convert('RGBA').getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
def main(folder):
 folder=Path(folder);records=json.loads((folder/'manifest.json').read_text());base=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text());entries={}
 aliases={'chorong':'resident_lamplighter','tosil':'resident_tosil'}
 bindings=[('bami','small_relief','ep2:bami:blanket',1,'……이거 너네 아빠 거지? 따뜻하다.'),('resident_lamplighter','guarded_relief','nt:night8:safe',3,'직접 전해 드린다고 했잖아요.'),('kid_kkomi','resilient_pride','wf:morning:alive',1,'우리 집 다 탔어. ……근데 대장은 표시 안 잃어버렸다.'),('resident_tosil','empathetic_confusion','cv:altar:granny',7,'……할머니. 여기가 산 너머야?')]
 for r in records:
  p=folder/'extracted'/r['source_relative_path'];assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'];im=Image.open(p).convert('RGBA');assert list(im.size)==r['size']
  if r['character_id']=='chorong_mother':continue
  person=aliases.get(r['character_id'],r['character_id']);key=person+':'+r['slot'];profiles={};bb=box(im)
  for h,profile in base['people'][person]['profiles'].items():
   old=profile['frames']['neutral'];oldim=Image.open(ROOT/'game'/old['file']);ob=box(oldim);scale=(ob[3]-ob[1])/float(bb[3]-bb[1]);new=resize_source(im,[round(im.width*scale),round(im.height*scale)]);nb=box(new)
   centre=old['offset'][0]+(ob[0]+ob[2])/2.;foot=old['offset'][1]+ob[3];offset=[round(centre-(nb[0]+nb[2])/2.),foot-nb[3]]
   assert 0<=offset[0]+nb[0]<=offset[0]+nb[2]<=profile['canvas'][0]
   assert 0<=offset[1]+nb[1]<=offset[1]+nb[3]<=profile['canvas'][1]
   dest=ROOT/'game/assets/dialogue-context-master'/person/h/(r['slot']+'.webp');dest.parent.mkdir(parents=True,exist_ok=True);new.save(dest,format='WEBP',quality=95,method=2)
   frame=dict(file=str(dest.relative_to(ROOT/'game')),offset=offset,source_master=r['source_relative_path'],source_sha256=r['sha256'],source_commit=COMMIT)
   profiles[h]=dict(canvas=profile['canvas'],frames={r['slot']:frame})
  entries[key]=dict(person=person,slot=r['slot'],profiles=profiles,status='approved_runtime')
 assert len(entries)==4
 data=dict(source_commit=COMMIT,entries=entries,bindings=[dict(person=p,slot=s,identity=i,index=n,text=t,key=p+':'+s) for p,s,i,n,t in bindings])
 (ROOT/'game/assets/room13-dialogue-context-art.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 out=ROOT/'docs/reviews/dialogue-context';out.mkdir(exist_ok=True);(out/'receipt.json').write_text(json.dumps(dict(source_commit=COMMIT,verified_originals=6,records=records,applied_entries=list(entries),held=[r for r in records if r['character_id']=='chorong_mother'],hold_reason='The requested mom role differs from the supplied chorong_mother identity. Do not overwrite mom or the authored offer_lantern action.'),ensure_ascii=False,indent=2)+'\n')
 print('6 verified;4 exact-context assets imported;2 mother-role images held')
if __name__=='__main__':main(sys.argv[1])
