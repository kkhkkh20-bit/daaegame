"""Add the approved next 120 masters without replacing the first 20 or event art.

Pass a folder containing the eight independent ZIPs, two manifests and extracted/.
Never concatenate the ZIPs. The source commit is kept as immutable provenance.
"""
import hashlib,json,sys,zipfile
from pathlib import Path
from PIL import Image
from prepare_dialogue_source_profiles import prepare
ROOT=Path(__file__).resolve().parents[1]
COMMIT='f25caf86ded3a8d874c938e353d14c268b23b8e2'
ALIASES={p:'resident_'+p for p in ('sling','tosil','piko','tori','kalbaram','ppul','seori','tok','nero','librarian','ttadak','dalgeurak','siluk')}
SLOTS=('neutral','joy','angry','anxious','surprise_talk','surprise_react')
def main(folder):
 folder=Path(folder);records=[];archives=[]
 for batch in ('third10','fourth10'):
  manifest=json.loads((folder/f'smooth-{batch}-60sources-manifest.json').read_text())
  assert len(manifest['records'])==60
  records.extend(manifest['records'])
  for part in range(1,5):
   path=folder/f'smooth-{batch}-sources-{part}-of-4.zip'
   with zipfile.ZipFile(path) as z:
    assert z.testzip() is None
    for name in z.namelist():
     if name.startswith('sources/') and not name.endswith('/'):
      assert z.read(name)==(folder/'extracted'/name).read_bytes()
   archives.append(dict(file=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 assert archives[-1]['sha256']=='c169941686fc7915d66812211b48047275349ebb6f1d79ad3b6096f6c5aec9a2'
 assert len({(r['character'],r['slot']) for r in records})==120
 characters=list(dict.fromkeys(r['character'] for r in records));assert len(characters)==20
 reg=ROOT/'game/assets/room13-dialogue-talk-art.json';data=json.loads(reg.read_text());previous=data['people'].copy()
 assert not set(ALIASES.get(p,p) for p in characters)&set(previous)
 fullbody=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
 for r in records:
  path=folder/'extracted'/r['runtime_file'];assert path.stat().st_size==r['bytes']
  assert hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256']
  with Image.open(path) as im:assert list(im.size)==r['size']
 layout=dict(source_commit=COMMIT,scale_policy='one normalized source-canvas scale per character/profile; bottom anchor only; no per-pose bbox fitting; no mirroring',people={});upscaled=[]
 for person in characters:
  rid=ALIASES.get(person,person);assert rid in fullbody
  files={s:folder/'extracted/sources'/person/(s+'.png') for s in SLOTS}
  ims={s:Image.open(p).convert('RGBA') for s,p in files.items()}
  entry={'profiles':{}}
  for height in (560,760,840):
   target=min(height*1.05,(400 if height<800 else 880)/max(im.width/im.height for im in ims.values()))
   sizes={s:(round(im.width*target/im.height),round(target)) for s,im in ims.items()}
   width=max(v[0] for v in sizes.values())+16;baseline=round(target)+16;frames={}
   for s,im in ims.items():
    size=sizes[s];box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();assert box
    scale=size[1]/im.height
    frames[s]=dict(source_master=str(files[s]),size=list(size),offset=[round((width-size[0])/2),baseline-round(box[3]*scale)])
    if scale>1.01:upscaled.append(dict(person=rid,slot=s,height=height,scale=scale))
   entry['profiles'][str(height)]=dict(canvas=[width,baseline+8],frames=frames)
  layout['people'][rid]=entry
 result=prepare(layout,ROOT/'game/assets/dialogue-source-master')
 for rid,entry in result['people'].items():
  for profile in entry['profiles'].values():
   for frame in profile['frames'].values():
    png=ROOT/'game'/frame['file'];webp=png.with_suffix('.webp')
    with Image.open(png) as im:im.save(webp,format='WEBP',quality=95,method=2)
    png.unlink();frame['file']=str(webp.relative_to(ROOT/'game'))
  entry.update(status='approved_runtime',stance='standing',gaze='player',source_commit=COMMIT)
 data['people'].update(result['people']);assert len(data['people'])==40
 assert all(data['people'][k]==v for k,v in previous.items())
 data.update(status='approved 40-person / 240 source-master packages; event poses excluded',source_commit=COMMIT,source_commits=list(dict.fromkeys([v['source_commit'] for v in data['people'].values()])))
 data['art_contract']['activation']='Only the two approved final 120-source packages; intermediate deliveries excluded; authored poses and meeting art preserved'
 reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 out=ROOT/'docs/reviews/dialogue-beats'
 receipt=dict(source_commit=COMMIT,base_main='10630d2a',verified_count=120,independent_zip_count=8,records=records,archives=archives,people=list(result['people']),upscaled_display_profiles=upscaled,preserved_previous_people=list(previous))
 for name,obj in [('smooth-next20-layout',layout),('smooth-next20-receipt',receipt)]:
  (out/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 # Application status follows resource availability, not a fresh emotion inference.
 cues=ROOT/'game/assets/room13-dialogue-beats.json';beats=json.loads(cues.read_text())
 for rows in beats['lines'].values():
  for cue in rows.values():
   if cue['person'] in result['people']:cue['application_status']='approved_source_master'
 cues.write_text(json.dumps(beats,ensure_ascii=False,indent=2)+'\n')
 print('Verified/imported 120 masters; total 40 people / 720 display frames; upscaled new profiles:',len(upscaled))
if __name__=='__main__':main(sys.argv[1])
