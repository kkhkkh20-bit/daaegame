"""Import the explicitly approved 8c80550 120-master package; separate map pixels."""
import json,hashlib,statistics,sys
from pathlib import Path
from PIL import Image
from prepare_dialogue_source_profiles import prepare
ROOT=Path(__file__).resolve().parents[1]
ALIASES={'bori':'resident_bori','teacher':'resident_teacher','nubi':'resident_nubi','somi':'resident_somi','kkwak':'resident_kkwak','guseul':'resident_guseul','momo':'resident_momo','musoe':'resident_musoe','chorong':'resident_lamplighter','madam':'resident_madam'}
SLOTS=('neutral','joy','angry','anxious','surprise_talk','surprise_react')
def main(folder):
 folder=Path(folder);manifest=json.loads((folder/'art/incoming/smooth-dialogue-20261017/smooth20-source-only-manifest.json').read_text());sources=folder/'extracted'
 assert len(manifest['records'])==120
 for r in manifest['records']:assert hashlib.sha256((sources/r['runtime_file']).read_bytes()).hexdigest()==r['sha256']
 layout={'source_commit':'8c80550dda6ecf7af335827bba7e4fa6f4052ddf','scale_policy':'one normalized source-canvas scale per character/profile; bottom anchor only; no per-pose bbox fitting; no mirroring','people':{}}
 low=[]
 for person in manifest['characters']:
  rid=ALIASES.get(person,person);files={s:sources/'sources'/person/(s+'.png') for s in SLOTS};ims={s:Image.open(p).convert('RGBA') for s,p in files.items()}
  # Canvas proportions are normalized by full source height, not each pose silhouette.
  # Small neutral originals have additional export margins, corrected explicitly.
  neutral_margin={'neoul':1.04,'teacher':1.05}.get(person,1.0)
  tuning={'daram':.85,'bami':.88,'doto':.92}.get(person,1.0)
  entry={'profiles':{}}
  for height in (560,760,840):
   target=height*1.05*tuning
   widest=max(im.width/im.height*(neutral_margin if s=='neutral' else 1) for s,im in ims.items())
   target=min(target,(400 if height<800 else 880)/widest)
   sizes={s:(round(im.width*target/im.height*(neutral_margin if s=='neutral' else 1)),round(target*(neutral_margin if s=='neutral' else 1))) for s,im in ims.items()}
   width=max(v[0] for v in sizes.values())+16;baseline=round(target)+16;canvas=[width,baseline+8]
   frames={}
   for s,im in ims.items():
    size=sizes[s];box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();scale=size[1]/im.height
    offset=[round((width-size[0])/2),baseline-round(box[3]*scale)]
    frames[s]={'source_master':str(files[s]),'size':list(size),'offset':offset}
    if scale>1.01:low.append(dict(person=rid,slot=s,height=height,source_size=list(im.size),display_size=list(size),scale=round(scale,3)))
   entry['profiles'][str(height)]={'canvas':canvas,'frames':frames}
  layout['people'][rid]=entry
 target=ROOT/'game/assets/dialogue-source-master';result=prepare(layout,target)
 for entry in result['people'].values():
  for profile in entry['profiles'].values():
   for frame in profile['frames'].values():
    png=ROOT/'game'/frame['file'];webp=png.with_suffix('.webp')
    with Image.open(png) as im:im.save(webp,format='WEBP',quality=95,method=2)
    png.unlink();frame['file']=str(webp.relative_to(ROOT/'game'))
 for rid,entry in result['people'].items():entry.update(status='approved_runtime',stance='standing',gaze='player',source_commit=layout['source_commit'])
 reg=ROOT/'game/assets/room13-dialogue-talk-art.json';data=json.loads(reg.read_text());data.update(status='approved 20-person source-master package; event poses excluded',people=result['people'],source_commit=layout['source_commit']);data['art_contract']['activation']='Approved final 120-source package only; prior intermediate six-person excluded'
 reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 out=ROOT/'docs/reviews/dialogue-beats'
 for name,obj in [('smooth20-layout',layout),('smooth20-receipt',dict(source_commit=layout['source_commit'],verified_count=120,independent_zip_count=8,records=manifest['records'],upscaled_display_profiles=low))]:
  (out/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('Imported',len(result['people']),'people / 360 display frames; upscaled profiles',len(low))
if __name__=='__main__':main(sys.argv[1])
