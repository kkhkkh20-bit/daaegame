"""Verify approved Git inputs and import 15 smooth poses plus chinchilla Solbang."""
import argparse,hashlib,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];COMMIT='1687deb04d44746fa5ca819db72fc03ce3623b8a'
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def main(folder):
 rows=[];originals=ROOT/'art/approved-remaining22/originals';originals.mkdir(parents=True,exist_ok=True)
 for pack in sorted(folder.iterdir()):
  if not pack.is_dir():continue
  manifest=json.loads((pack/'manifest.json').read_text());records=manifest if isinstance(manifest,list) else manifest['assets']
  write(ROOT/'art/approved-remaining22/manifests'/(pack.name+'.json'),manifest)
  for r in records:
   who=r.get('character_id',r.get('character'));pose=r.get('slot',r.get('pose'));rel=r.get('file',r.get('path',r.get('source_relative_path')));p=pack/'extracted'/rel;b=p.read_bytes();im=Image.open(p).convert('RGBA');assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'] and list(im.size)==r['size']
   src=originals/(who+'--'+pose+'.png');shutil.copyfile(p,src);rows.append(dict(person=who,pose=pose,source=str(src.relative_to(ROOT)),source_sha256=r['sha256'],source_size=r['size'],metadata=r))
 assert len(rows)==22
 poses={'people':{}};receipt=[]
 # Visible height is a dialogue framing decision, not a standing-height stretch.
 heights={'hide_bowl':410,'collapse_attendance':480,'chair_read':620,'chair_listen':620,'hold_storybook':610,'offer_lantern':620,'show_fragments':650,'lick_ladle':570,'cling_leg':570,'door_peek':570,'hideout_proud':570}
 for r in rows:
  if r['person']=='resident_solbang':continue
  who,pose=r['person'],r['pose'];im=Image.open(ROOT/r['source']).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>=12 else 0).getbbox();x,y,x2,y2=box
  # Trim only transparent margins; retain all pose-specific props and body direction.
  profiles={}
  for h in (560,760,840):
   target=heights.get(pose,660)*h/840;scale=min(target/(y2-y),(390 if h<800 else 760)/(x2-x));size=(max(1,round((x2-x)*scale)),max(1,round((y2-y)*scale)))
   out=im.crop(box).resize(size,Image.Resampling.LANCZOS);path=ROOT/'game/assets/dialogue-pose-source'/who/pose/(str(h)+'.webp');path.parent.mkdir(parents=True,exist_ok=True);out.save(path,lossless=True,method=4)
   profiles[str(h)]=dict(canvas=[size[0]+24,size[1]+24],frames={'neutral':dict(file=str(path.relative_to(ROOT/'game')),offset=[12,12],source_master=r['source'],source_sha256=r['source_sha256'],source_commit=COMMIT)})
  entry=poses['people'].setdefault(who,{'pose_profiles':{}});entry['pose_profiles'][pose]=dict(profiles=profiles,source_crop_xywh=[x,y,x2-x,y2-y],source_sha256=r['source_sha256'],kind='approved_authored_smooth_pose',visible_height_at_840=heights.get(pose,660))
 write(ROOT/'game/assets/room13-dialogue-pose-source-art.json',poses)
 # Solbang's six slots share a source-canvas scale and foot baseline.
 sol={r['pose']:r for r in rows if r['person']=='resident_solbang'};talkpath=ROOT/'game/assets/room13-dialogue-talk-art.json';talk=json.loads(talkpath.read_text());entry=dict(status='approved_runtime',art_style='storybook_source',source_kind='source_master',stance='standing',gaze='player',source_commit=COMMIT,profiles={})
 for h in (560,760,840):
  scale=min(h*1.05/1536,(400 if h<800 else 880)/1024);w,hh=round(1024*scale),round(1536*scale);frames={}
  for pose,r in sol.items():
   if pose=='work_herb_bundle':continue
   im=Image.open(ROOT/r['source']).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>=12 else 0).getbbox();path=ROOT/'game/assets/dialogue-source-master/resident_solbang'/str(h)/(pose+'.webp');path.parent.mkdir(parents=True,exist_ok=True);im.resize((w,hh),Image.Resampling.LANCZOS).save(path,quality=95,method=4)
   frames[pose]=dict(file=str(path.relative_to(ROOT/'game')),offset=[8,round(hh+16-box[3]*scale)],source_master=r['source'],source_sha256=r['source_sha256'],source_commit=COMMIT)
  entry['profiles'][str(h)]=dict(canvas=[w+16,hh+24],frames=frames)
 talk['people']['resident_solbang']=entry;talk['source_commits']=list(dict.fromkeys(talk.get('source_commits',[])+[COMMIT]));write(talkpath,talk)
 # The 59th smooth profile uses the exact approved original-space square.
 r=sol['neutral'];im=Image.open(ROOT/r['source']).convert('RGBA');icon=Image.new('RGBA',(256,256));icon.alpha_composite(im.crop((220,60,760,600)).resize((232,232),Image.Resampling.LANCZOS),(12,12));path=ROOT/'game/assets/profile-source-master/resident_solbang.webp';icon.save(path,lossless=True,method=4)
 profpath=ROOT/'game/assets/room13-profile-source-art.json';profiles=json.loads(profpath.read_text());profiles['people']['resident_solbang']=dict(file=str(path.relative_to(ROOT/'game')),size=[256,256],padding=12,source_sha256=r['source_sha256'],source_commit=COMMIT,source_master=r['source'],source_size=r['source_size'],crop=[220,60,540,540],sha256=hashlib.sha256(path.read_bytes()).hexdigest());profiles['excluded']=[x for x in profiles['excluded'] if x!='resident_solbang'];write(profpath,profiles)
 cropspath=ROOT/'docs/reviews/profile-icons/approved-crops.json';crops=json.loads(cropspath.read_text());crops=[c for c in crops if c['character_id']!='resident_solbang'];crops.append(dict(character_id='resident_solbang',source_sha256=r['source_sha256'],source_size=[1024,1536],face_crop_normalized=[220/1024,60/1536,540/1024,540/1536]));write(cropspath,crops)
 # Separate map derivatives. Existing aliases all point to the approved identity.
 maprows={}
 for pose in ('neutral','work_herb_bundle'):
  r=sol[pose];im=Image.open(ROOT/r['source']).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>=12 else 0).getbbox();crop=im.crop(box);scale=420/crop.height;w=round(crop.width*scale);w-=w%2;out=crop.resize((w,420),Image.Resampling.LANCZOS).resize((w//2,210),Image.Resampling.NEAREST).resize((w,420),Image.Resampling.NEAREST)
  path=ROOT/'game/assets/solbang-chinchilla-map'/(pose+'.webp');path.parent.mkdir(exist_ok=True);out.save(path,lossless=True,method=4)
  maprows[pose]=dict(file=str(path.relative_to(ROOT/'game')),crop=[0,0,w,420],foot=[w*.5,418],head=[max(0,round((220-box[0])*scale)),0,round(540*scale),round((600-box[1])*scale)],nearest=True,contact='standing',reviewed=True,source_sha256=r['source_sha256'],source_commit=COMMIT)
 castpath=ROOT/'game/assets/cast.json';cast=json.loads(castpath.read_text());actpath=ROOT/'game/assets/room13-pixel-acting.json';acting=json.loads(actpath.read_text())
 for registry in (cast,acting):
  for key in list(registry['resident_solbang']):registry['resident_solbang'][key]=dict(file=profiles['people']['resident_solbang']['file'],crop=[0,0,256,256],nearest=False) if key.startswith('avatar_') else dict(maprows['neutral'])
  registry['resident_solbang']['work_herb_bundle']=maprows['work_herb_bundle']
 write(castpath,cast);write(actpath,acting)
 portraitpath=ROOT/'game/assets/room13-portraits.json';portraits=json.loads(portraitpath.read_text())
 for key in portraits.get('resident_solbang',{}):portraits['resident_solbang'][key]=dict(file='assets/solbang-chinchilla-source/neutral.webp',crop=[0,0,1024,1536],head=[220,60,540,540],full_body=True,nearest=False,source_sha256=sol['neutral']['source_sha256'])
 write(portraitpath,portraits)
 # Replace the dormant fullbody fallback too, preserving the new species in old-save recovery.
 fullpath=ROOT/'game/assets/room13-fullbody-dialogue.json';full=json.loads(fullpath.read_text());images={}
 for emotion,slot in dict(neutral='neutral',joy='joy',angry='angry',anxious='anxious',surprise='surprise_talk',flustered='anxious').items():
  r=sol[slot];path=ROOT/'game/assets/solbang-chinchilla-source'/(slot+'.webp');path.parent.mkdir(exist_ok=True);Image.open(ROOT/r['source']).save(path,lossless=True,method=4);images[emotion]=dict(file=str(path.relative_to(ROOT/'game')),size=r['source_size'],native_detail=True,smooth_source=True,source_sha256=r['source_sha256'])
 full['people']['resident_solbang']=dict(name_ko='솔방울',crop=[0,0,1024,1536],figure=[64,103,940,1406],images=images,source_commit=COMMIT,role_connect='approved-chinchilla-20261017');fullpath.write_text(json.dumps(full,ensure_ascii=False,indent=1)+'\n')
 write(ROOT/'art/approved-remaining22/receipt.json',dict(source_commit=COMMIT,verified_count=len(rows),rows=rows))
 print('Imported 22 verified sources, 15 smooth poses, Solbang six slots + map + profile')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);main(p.parse_args().folder)
