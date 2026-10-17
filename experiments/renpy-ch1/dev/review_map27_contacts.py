"""Render contact annotations on native scene backgrounds, not new character mockups."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/action27-preparation'
def main():
 layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text());atlases=json.loads((ROOT/'game/assets/room13-pixel-layouts.json').read_text());data=json.loads((OUT/'contacts.json').read_text());proof=[]
 for row in data['placements']:
  loc,period=row['location'],row['daylight'];lay=layouts[loc]
  if loc=='post' and period!='morning':
   file='assets/room13-pixel-village-'+period+'.webp';crop=atlases[Path(file).name]['rects'][1]
  else:file=lay['files'][period];crop=lay.get('crops',{}).get(period)
  p=ROOT/'game'/file;im=Image.open(p).convert('RGB')
  if crop:x,y,w,h=crop;im=im.crop((x,y,x+w,y+h))
  im=im.resize((row['world_width'],720),Image.Resampling.NEAREST);draw=ImageDraw.Draw(im)
  for poly in row['occlusion']:draw.line([tuple(p) for p in poly]+[tuple(poly[0])],fill='#ffbf00',width=3)
  for name,(x,y) in dict({row['anchor']:row['target']},**row.get('secondary_targets',{})).items():
   draw.line((x-12,y,x+12,y),fill='#00ffdf',width=3);draw.line((x,y-12,x,y+12),fill='#00ffdf',width=3)
   label=f'{name} ({x},{y})';draw.rectangle((x+14,y-22,x+14+len(label)*7,y),fill='black');draw.text((x+16,y-20),label,fill='#00ffdf')
  title=f"{row['request']} {loc}/{period} {im.width}x720 | BACKGROUND CONTACT REVIEW - ART PENDING"
  draw.rectangle((0,0,im.width,24),fill='black');draw.text((8,6),title,fill='white')
  target=OUT/(row['request']+'-'+period+'.png');im.save(target)
  proof.append(dict(request=row['request'],daylight=period,file=file,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),crop=crop,output=target.name))
 (OUT/'background-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
if __name__=='__main__':main()
