"""Import 54 approved final-batch masters and replace three neutral slots only."""
import copy,hashlib,json,sys,zipfile
from pathlib import Path
from PIL import Image
from prepare_dialogue_source_profiles import prepare,resize_source
ROOT=Path(__file__).resolve().parents[1]
COMMIT='e523ad0995efa9012780438785e8bb0f1555c628'
HIGH_COMMIT='a59c4fed98b707febd7d9572f4d0bd555f2f194b'
SLOTS={'neutral','joy','angry','anxious','surprise_talk','surprise_react'}
def alpha_box(im):return im.convert('RGBA').getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main(folder):
 folder=Path(folder);records=json.loads((folder/'manifest.json').read_text());high=json.loads((folder/'neutral-highres-public-manifest.json').read_text())
 assert len(records)==54 and len(high)==3
 archives=[];zipped={}
 for path in sorted(folder.glob('*.zip')):
  with zipfile.ZipFile(path) as z:
   assert z.testzip() is None
   for name in z.namelist():
    if name.endswith('.png'):
     content=z.read(name);assert content==(folder/'extracted'/name).read_bytes();zipped[name]=hashlib.sha256(content).hexdigest()
  archives.append(dict(file=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 assert len(archives)==6 and len(zipped)==57
 for r in records+high:
  assert set(r)=={'character_id','slot','source_relative_path','sha256','size','bytes'}
  path=folder/'extracted'/r['source_relative_path'];assert path.stat().st_size==r['bytes']
  assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']==zipped[r['source_relative_path']]
  with Image.open(path) as im:assert list(im.size)==r['size']
 registry=ROOT/'game/assets/room13-dialogue-talk-art.json';data=json.loads(registry.read_text());previous=copy.deepcopy(data['people']);assert len(previous)==50
 people=list(dict.fromkeys(r['character_id'] for r in records));assert len(people)==9 and not set(people)&set(previous)
 layout=dict(expected_people=9,source_commit=COMMIT,scale_policy='source-canvas proportions retained; one normalized height per character/profile; feet anchored; children use existing Daram 0.85 stature convention',people={})
 for person in people:
  rows={r['slot']:r for r in records if r['character_id']==person};assert set(rows)==SLOTS
  ims={s:Image.open(folder/'extracted'/r['source_relative_path']).convert('RGBA') for s,r in rows.items()}
  entry=dict(profiles={});tuning=.85 if person.startswith('kid_') else 1.0
  for height in (560,760,840):
   target=min(height*1.05*tuning,(400 if height<800 else 880)/max(im.width/im.height for im in ims.values()))
   sizes={s:(round(im.width*target/im.height),round(target)) for s,im in ims.items()};width=max(x[0] for x in sizes.values())+16;baseline=round(target)+16;frames={}
   for s,im in ims.items():
    box=alpha_box(im);assert box
    size=sizes[s];scale=size[1]/im.height
    frames[s]=dict(source_master=str(folder/'extracted'/rows[s]['source_relative_path']),size=list(size),offset=[round((width-size[0])/2),baseline-round(box[3]*scale)])
   entry['profiles'][str(height)]=dict(canvas=[width,baseline+8],frames=frames)
  layout['people'][person]=entry
 result=prepare(layout,ROOT/'game/assets/dialogue-source-master')
 for person,entry in result['people'].items():
  for profile in entry['profiles'].values():
   for slot,frame in profile['frames'].items():
    png=ROOT/'game'/frame['file'];webp=png.with_suffix('.webp')
    with Image.open(png) as im:im.save(webp,format='WEBP',quality=95,method=2)
    png.unlink();frame['file']=str(webp.relative_to(ROOT/'game'))
    row=next(r for r in records if r['character_id']==person and r['slot']==slot)
    frame['source_master']=row['source_relative_path'];frame['source_commit']=COMMIT;frame['source_sha256']=row['sha256']
  entry.update(status='approved_runtime',stance='standing',gaze='player',source_commit=COMMIT)
 data['people'].update(result['people']);replacements=[]
 for row in high:
  person={'somi':'resident_somi'}.get(row['character_id'],row['character_id']);assert person in ('daram','bami','resident_somi') and row['slot']=='neutral'
  path=folder/'extracted'/row['source_relative_path'];im=Image.open(path).convert('RGBA');box=alpha_box(im)
  for height,profile in data['people'][person]['profiles'].items():
   frame=profile['frames']['neutral'];target=ROOT/'game'/frame['file'];old=Image.open(target).convert('RGBA');old_box=alpha_box(old)
   # Preserve the old approved neutral's visible height, centre and foot baseline.
   # Other five frames, their canvases and their positions stay byte-for-byte intact.
   scale=(old_box[3]-old_box[1])/float(box[3]-box[1]);size=[round(im.width*scale),round(im.height*scale)]
   new=resize_source(im,size);new_box=alpha_box(new)
   old_centre=frame['offset'][0]+(old_box[0]+old_box[2])/2.0;old_foot=frame['offset'][1]+old_box[3]
   offset=[round(old_centre-(new_box[0]+new_box[2])/2.0),old_foot-new_box[3]]
   assert 0<=offset[0]+new_box[0] and offset[0]+new_box[2]<=profile['canvas'][0]
   assert 0<=offset[1]+new_box[1] and offset[1]+new_box[3]<=profile['canvas'][1]
   new.save(target,format='WEBP',quality=95,method=2)
   frame.update(offset=offset,source_master=row['source_relative_path'],source_commit=HIGH_COMMIT,source_sha256=row['sha256'])
   replacements.append(dict(person=person,profile=height,source_size=list(im.size),display_size=size,scale=scale,foot_baseline=old_foot,visible_height=old_box[3]-old_box[1],source_sha256=row['sha256']))
  data['people'][person]['neutral_source_commit']=HIGH_COMMIT
 assert len(data['people'])==59
 for person,entry in previous.items():
  if person not in ('daram','bami','resident_somi'):assert data['people'][person]==entry
  else:
   for h,profile in entry['profiles'].items():
    assert profile['canvas']==data['people'][person]['profiles'][h]['canvas']
    for slot,frame in profile['frames'].items():
     if slot!='neutral':assert frame==data['people'][person]['profiles'][h]['frames'][slot]
 data.update(status='approved 59-person / 354 source-master slots; event poses excluded',source_commit=COMMIT,source_commits=list(dict.fromkeys(data['source_commits']+[COMMIT,HIGH_COMMIT])))
 data['art_contract']['activation']='Approved final packages only; five high-resolution neutral replacements; authored poses and meeting art preserved'
 write(registry,data)
 out=ROOT/'docs/reviews/dialogue-beats';write(out/'smooth-final9-receipt.json',dict(source_commit=COMMIT,neutral_source_commit=HIGH_COMMIT,base_main='928c7591',verified_count=57,new_people=people,total_people=59,total_slots=354,archives=archives,records=records,neutral_replacements=high,display_replacements=replacements))
 # Local layout paths are retained only in a local review artifact, not published.
 write(folder/'layout.json',layout)
 cues=ROOT/'game/assets/room13-dialogue-beats.json';beats=json.loads(cues.read_text())
 for rows in beats['lines'].values():
  for cue in rows.values():
   if cue['person'] in people:cue['application_status']='approved_source_master'
 write(cues,beats)
 print('Verified 57 originals; added 9 people / 162 frames; replaced 9 neutral frames; total 59 people / 354 slots')
if __name__=='__main__':main(sys.argv[1])
