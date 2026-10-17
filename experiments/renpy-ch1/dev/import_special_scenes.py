"""Verify approved scene sources; composite the supplied attendance SVGs by their quads.
No artwork is generated. The original source pixels remain unchanged outside the overlay.
"""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
COMMIT='4c4978ed4d06c1e482dfb8aad9938d4e9fa8d1e1'
def svg_image(path,size,font):
 root=ET.fromstring(path.read_text());out=Image.new('RGBA',tuple(size));draw=ImageDraw.Draw(out)
 for group in root:
  for el in group:
   a=el.attrib;tag=el.tag.rsplit('}',1)[-1]
   if tag=='text':
    draw.text((int(a['x']),int(a['y'])),el.text,font=ImageFont.truetype(font,int(group.attrib['font-size'])),fill=group.attrib['fill'],anchor='ls')
   elif tag=='ellipse':
    x,y,rx,ry=[int(a[k]) for k in ('cx','cy','rx','ry')]
    draw.ellipse((x-rx,y-ry,x+rx,y+ry),outline=group.attrib['stroke'],width=int(group.attrib['stroke-width']))
   else:raise ValueError('Unsupported SVG element '+tag)
 return out

def warp(page,quad,size):
 # PIL maps destination -> source; solve the approved four-corner homography.
 src=[(0,0),(page.width,0),(page.width,page.height),(0,page.height)];matrix=[];values=[]
 for (x,y),(u,v) in zip(quad,src):
  matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);values.extend([u,v])
 coeff=np.linalg.solve(np.array(matrix,dtype=float),np.array(values,dtype=float))
 return page.transform(size,Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)

def main(folder):
 folder=Path(folder);manifest=json.loads((folder/'special-scenes-manifest.json').read_text());source=folder/'extracted';out=ROOT/'game/assets/special-scenes';out.mkdir(exist_ok=True)
 for row in manifest['assets']+manifest['attendance_overlays']:
  p=source/row['file'];assert p.stat().st_size==row['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
  if 'size' in row:
   with Image.open(p) as im:assert list(im.size)==row['size']
 overlays={r['scene_id']:r for r in manifest['attendance_overlays']};scenes={}
 for row in manifest['assets']:
  key=row['scene_id'];im=Image.open(source/row['file']).convert('RGBA')
  if key in overlays:
   o=overlays[key];svg=ET.fromstring((source/o['file']).read_text());names=[x.text for x in svg.iter() if x.tag.endswith('}text')];assert names==o['rows']
   page=svg_image(source/o['file'],o['source_canvas'],'/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
   layer=warp(page,o['target_page_quad_px_TL_TR_BR_BL'],im.size);before=np.asarray(im).copy();im=Image.alpha_composite(im,layer)
   assert np.array_equal(np.asarray(im)[np.asarray(layer)[:,:,3]==0],before[np.asarray(layer)[:,:,3]==0])
   review=ROOT/'docs/reviews/special-scenes';review.mkdir(exist_ok=True);page.save(review/(key+'-attendance.png'))
  dest=out/(key+'.webp');im.save(dest,format='WEBP',lossless=True,method=4)
  scenes[key]=dict(visible_bounds=list(im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()),cut_max_height=340 if key.startswith('teacher_') else 400,cut_ground_y=490,file=str(dest.relative_to(ROOT/'game')),size=list(im.size),source_sha256=row['sha256'],display_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
 registry=dict(source_commit=COMMIT,scenes=scenes,attendance_overlays=manifest['attendance_overlays'])
 (ROOT/'game/assets/room13-special-scenes.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
 receipt=dict(source_commit=COMMIT,verified_assets=8,verified_overlays=2,manifest=manifest,display=scenes)
 p=ROOT/'docs/reviews/special-scenes';p.mkdir(exist_ok=True);(p/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 print('Verified 8 sources + 2 SVGs; composited only supplied attendance overlays')
if __name__=='__main__':main(sys.argv[1])
