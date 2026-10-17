"""Pre-cut v6 polygon masks and discovered-place patches, never runtime clipping.
Run after importing full map art; source SHA values are checked before cropping.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'game/room13-cartography.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 data=json.loads(DATA.read_text()); assets=ROOT/'game/assets'
 for region,spec in data['regions'].items():
  path=ROOT/'game'/spec['art']; assert sha(path)==spec['sha256']
  src=ROOT.parents[1]/spec['mask_source'] if 'mask_source' in spec else path
  if 'mask_sha256' in spec: assert sha(src)==spec['mask_sha256']
  art=Image.open(src).convert('RGBA')
  for key,node in spec['nodes'].items():
   x,y,w,h=node['bounds']; points=[(a-x,b-y) for a,b in node['polygon']]
   mask=Image.new('L',(w,h)); ImageDraw.Draw(mask).polygon(points,fill=255)
   cut=art.crop((x,y,x+w,y+h));cut.putalpha(mask)
   line=Image.new('RGBA',(w,h));ImageDraw.Draw(line).polygon(points,outline=(255,213,123,220),width=4)
   for suffix,im in [('',cut),('-outline',line)]:im.save(assets/f'room13-map-{region}-{key}{suffix}.webp','WEBP',lossless=True,method=6)
  if region=='mountain':
   for key,spec in data['reveals'].items():
    x,y,w,h=spec['bounds'];patch=art.crop((x,y,x+w,y+h))
    mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rectangle((20,0 if y==0 else 20,w-21,h-21),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(8));patch.putalpha(mask)
    patch.save(ROOT/'game'/spec['art'],'WEBP',lossless=True,method=6)
if __name__=='__main__':main()
