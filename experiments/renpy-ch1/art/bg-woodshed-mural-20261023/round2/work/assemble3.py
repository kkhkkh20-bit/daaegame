from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import numpy as np
import json, shutil
R=Path(__file__).resolve().parents[1]; B=R.parent
G=Path('/root/.codex/generated_images/01a16724-8aa1-7b93-8a68-9d82ecd59ba2')
FILES={'afternoon':'exec-17e456e9-c990-4190-8263-2258f852f364.png','morning':'exec-6ff110f7-cb95-4172-92a6-28b502660f0b.png','evening':'exec-218c2163-e719-4b74-905c-efe2f3718d91.png'}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
report=[]
for t,name in FILES.items():
 shutil.copy2(G/name,R/'work'/f'facility3-{t}-generated.png')
 original=Image.open(B/'ref'/f'room13-pixel-ready-facility0177-{t}.webp').convert('RGB')
 src=Image.open(G/name).convert('RGB').resize((1024,768),Image.Resampling.LANCZOS)
 patch=src.crop((512,0,1024,768))
 # Composite the separately corrected floor geometry, keeping each lighting variant's slab.
 floor=Image.open(G/'exec-f9a12d05-e64d-4657-ac4d-dad7c39380ac.png').convert('RGB').resize((1024,768),Image.Resampling.LANCZOS).crop((512,0,1024,768))
 shutil.copy2(G/'exec-f9a12d05-e64d-4657-ac4d-dad7c39380ac.png',R/'work'/'facility3-floor-generated.png')
 arr=np.array(floor).astype(float)
 # Color transfer uses the existing floor's diffuse midtone for each time of day.
 aft=Image.open(B/'ref'/'room13-pixel-ready-facility0177-afternoon.webp').convert('RGB')
 target=np.median(np.array(original)[680:750,1940:2020].reshape(-1,3),axis=0)
 base=np.median(np.array(aft)[680:750,1940:2020].reshape(-1,3),axis=0)
 arr*=target/base
 floor=Image.fromarray(np.uint8(np.clip(arr,0,255)))
 mask=Image.new('L',(512,768));md=ImageDraw.Draw(mask)
 md.polygon([(0,638),(512,664),(512,768),(0,768)],fill=255)
 # Slab and its immediate contact shadow remain from the lighting variant.
 md.polygon([(250,630),(400,640),(400,669),(250,663)],fill=0)
 patch.paste(floor,(0,0),mask)
 out=Image.new('RGB',(2560,768));out.paste(original,(0,0));out.paste(patch,(2048,0))
 out.save(R/f'facility-wide3-{t}.webp',lossless=True,method=6)
 check=np.array(Image.open(R/f'facility-wide3-{t}.webp').convert('RGB'))
 diff=check[:,:2048].astype(int)-np.array(original).astype(int)
 assert not diff.any()
 report.append({'time':t,'size':list(out.size),'changed_original_pixels':int(np.any(diff,axis=2).sum()),'max_channel_difference':int(abs(diff).max())})
(R/'work'/'validation3.json').write_text(json.dumps(report,indent=2)+'\n')
p=Image.new('RGB',(1280,3450),'#20202a');d=ImageDraw.Draw(p)
for i,t in enumerate(['morning','afternoon','evening']):
 im=Image.open(R/f'facility-wide3-{t}.webp')
 d.text((10,i*750+4),f'{t.upper()} - RIGHT VIEW 1280 x 720 (x=1280, y=48)',font=font,fill='white')
 p.paste(im.crop((1280,48,2560,768)),(0,i*750+30))
# Native 320x180 crops enlarged exactly 2x, no smoothing.
a=Image.open(B/'ref'/'room13-pixel-ready-facility0177-afternoon.webp');b=Image.open(R/'facility-wide3-afternoon.webp');old=Image.open(R/'facility-wide-afternoon.webp')
comparisons=[(a,(1430,110),'ORIGINAL FACILITY - 2x',b,(2110,100),'NEW MURAL - 2x'),(old,(1990,588),'ROUND 2 FLOOR JOIN - 2x',b,(1990,588),'ROUND 3 FLOOR JOIN - 2x'),(old,(2240,430),'ROUND 2 TABLET - 2x',b,(2240,430),'ROUND 3 STONE / SCRATCHES - 2x')]
for row,(a,pa,la,b,pb,lb) in enumerate(comparisons):
 y=2250+row*400
 for col,(im,pt,label) in enumerate([(a,pa,la),(b,pb,lb)]):
  d.text((col*640+8,y+5),label,font=font,fill='white')
  x,z=pt;p.paste(im.crop((x,z,x+320,z+180)).resize((640,360),Image.Resampling.NEAREST),(col*640,y+35))
p.save(R/'preview3_facility.png')
print(json.dumps(report))
