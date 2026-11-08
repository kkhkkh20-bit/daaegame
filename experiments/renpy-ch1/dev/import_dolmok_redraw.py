"""돌목 승인 원화를 보존하고 같은 얼굴·발 기준으로 대화 프로필을 등록한다."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
from import_art import encode
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'neutral':'exec-54514f3c-02cf-4fb8-900f-99dec1baee52.png',
 'joy':'exec-752d490f-8545-43da-94ed-5d5f93c56fa5.png',
 'angry':'exec-de015b44-58c9-445a-9ccb-fecb8ff14c83.png',
 'anxious':'exec-d87425a3-d418-44be-8d24-28e125185f72.png',
 'flustered':'exec-859b40d9-b129-4da4-90fe-3c8c26cdb7a3.png',
 'surprise_talk':'exec-c5a80bdf-abc3-4140-be37-a3f46fd780a3.png',
}
def main():
 datafile=ROOT/'game/assets/room13-dialogue-player-facing.json'
 if json.loads(datafile.read_text())['people'].get('guard',{}).get('art_revision')=='guard-pixel-consistency-20261108':
  print('새 돌목 도트 원화를 유지합니다. 재가져오기는 dev/import_guard_pixel.py 사용.');return
 art=ROOT/'art/dolmok-redraw-20261105';masters=art/'sources';masters.mkdir(parents=True,exist_ok=True)
 target=ROOT/'game/assets/dialogue-player-facing/guard-redesign';target.mkdir(parents=True,exist_ok=True)
 rows={}
 for slot,name in SOURCES.items():
  source=Path('/workspace/generated_images')/name
  saved=masters/(slot+'.png')
  if source.exists():shutil.copy2(source,saved)
  elif not saved.exists():raise FileNotFoundError(source)
  path=target/(slot+'.webp') if slot!='flustered' else target.parent/'guard-flustered.webp'
  path.write_bytes(encode(saved))
  with Image.open(saved) as im:
   assert im.mode=='RGBA'
   box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();assert box
   assert box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height
   assert im.getpixel((0,0))[3]==0
   rows[slot]=dict(file=str(path.relative_to(ROOT/'game')),source_master=str(saved.relative_to(ROOT)),source_sha256=hashlib.sha256(saved.read_bytes()).hexdigest(),canvas=list(im.size),bounds=list(box))
 datafile=ROOT/'game/assets/room13-dialogue-player-facing.json';data=json.loads(datafile.read_text())
 entry=dict(status='approved_runtime',stance='standing',gaze='player',art_style='storybook_source',source_kind='source_master',approval='소유자: 돌목 대화 모습을 예쁘게 다시 제작',art_revision='dolmok-redraw-20261105',profiles={})
 for height,canvas,wanted in ((560,[373,612],570),(760,[416,682],640),(840,[552,906],870)):
  visible=min(wanted,min((canvas[0]-16)*(r['bounds'][3]-r['bounds'][1])/(r['bounds'][2]-r['bounds'][0]) for r in rows.values()))
  feet=canvas[1]-24;frames={}
  for slot,r in rows.items():
   x0,y0,x1,y1=r['bounds'];scale=visible/(y1-y0)
   frames[slot]=dict(file=r['file'],offset=[round(canvas[0]/2-(x0+x1)*scale/2),round(feet-y1*scale)],scale=round(scale,8),nearest=False,anchor=[(x0+x1)/2,y1],source_master=r['source_master'],source_sha256=r['source_sha256'])
  entry['profiles'][str(height)]=dict(canvas=canvas,frames=frames)
 data['people']['guard']=entry;datafile.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (art/'manifest.json').write_text(json.dumps(dict(approval=entry['approval'],sources=rows,profiles=entry['profiles'],kept='오소리 성인 경비·청록 외투·빨간 목도리·장부·붓; 현장 도트와 작은 기존 프로필은 별도 역할로 유지'),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({slot:dict(file=r['file'],bounds=r['bounds']) for slot,r in rows.items()},ensure_ascii=False))
if __name__=='__main__':main()
