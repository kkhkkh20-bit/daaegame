"""Compare original appearance with final investigation-grid pixels at real map sizes."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/action27-p0'
def main():
 rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'];receipts=json.loads((ROOT/'art/approved-action27-p0/receipt.json').read_text())['rows'];canvas=Image.new('RGB',(1000,280*len(rows)),'#aaa');draw=ImageDraw.Draw(canvas)
 for index,row in enumerate(rows):
  receipt=next(r for r in receipts if r['request_id']==row['request_id']);src=Image.open(ROOT/receipt['source']).convert('RGBA');export=Image.open(ROOT/'game'/row['spec']['file']).convert('RGBA');h=row['variants']['morning']['render_height'];w=round(512*h/768)
  reference=src.resize((w,h),Image.Resampling.LANCZOS);actual=export.resize((w//2,h//2),Image.Resampling.NEAREST).resize((w//2*2,h//2*2),Image.Resampling.NEAREST)
  y=index*280;draw.text((10,y+4),row['request_id']+' '+row['person']+' | original fit / map 2px | face crops 4x, no palette reduction',fill='black');canvas.paste(reference,(10,y+25),reference);canvas.paste(actual,(180,y+25),actual)
  x0,y0,ww,hh=row['spec']['head'];scale=h/768;box=(int(x0*scale),int(y0*scale),int((x0+ww)*scale),int((y0+hh)*scale))
  for x,im in [(400,reference),(680,actual)]:
   face=im.crop(box);face=face.resize((face.width*4,face.height*4),Image.Resampling.NEAREST);canvas.paste(face,(x,y+30),face)
 canvas.save(OUT/'actual-size-pixel-comparison.png')
if __name__=='__main__':main()
