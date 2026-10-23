from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import numpy as np, shutil, json
R=Path(__file__).resolve().parents[1]; B=R.parent
G=Path('/root/.codex/generated_images/01a1671a-872d-7a22-bddb-cffe6dcbb5d5')
FILES={'woods-afternoon':'exec-13899d70-7b38-474a-873d-42a8dc68b035.png','woods-evening':'exec-036d2d5a-9a82-413c-a266-c08a5a1725d7.png','facility-afternoon':'exec-698d5a08-65f6-4777-85ac-018fad1fd306.png','facility-evening':'exec-c062eecc-2236-4c22-968a-c2f5dcc99eee.png'}
N=Image.Resampling.NEAREST
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
def flat(im,colors=96):
    sz=im.size
    return im.resize((sz[0]//3,sz[1]//3),Image.Resampling.BOX).quantize(colors=colors,dither=Image.Dither.NONE).convert('RGB').resize(sz,N)
def save(im,name): im.save(R/name,lossless=True,method=6)
def woods(im):
    # Preserve requested landmarks while allocating extra width to side storage.
    im=im.resize((2048,683),N)
    xs=[0,500,650,790,1090,1275,1660,2048]
    ds=[0,450,520,720,1300,1500,2050,2560]
    out=Image.new('RGB',(2560,768))
    for a,b,c,d in zip(xs,xs[1:],ds,ds[1:]):out.paste(im.crop((a,0,b,683)).resize((d-c,768),N),(c,0))
    return flat(out)
for key,name in FILES.items():
    shutil.copy2(G/name,R/'work'/f'{key}-generated.png')
for t in ['afternoon','evening']:
    im=woods(Image.open(R/'work'/f'woods-{t}-generated.png').convert('RGB'))
    save(im,'woodshed-interior-wide'+('-evening' if t=='evening' else '')+'.webp')
def facility(t):
    original=Image.open(B/'ref'/f'room13-pixel-ready-facility0177-{t}.webp').convert('RGB')
    src=Image.open(R/'work'/f'facility-{t}-generated.png').convert('RGB').resize((1983,793),N)
    patch=Image.new('RGB',(512,768))
    # Align wall/baseboard/floor heights to original right edge.
    ys=[0,475,610,793]; yd=[0,500,632,768]
    for a,b,c,d in zip(ys,ys[1:],yd,yd[1:]):patch.paste(src.crop((1490,a,1983,b)).resize((512,d-c),N),(0,c))
    patch=flat(patch.filter(ImageFilter.MedianFilter(5)),32)
    # Edge matching is entirely in the new region. Original pixels are untouched.
    ar=np.array(patch).astype(float); edge=np.array(original)[:,-1,:].astype(float)
    for x in range(24):
        w=(x//3)/8
        ar[:,x,:]=edge*(1-w)+ar[:,x,:]*w
    patch=Image.fromarray(np.uint8(np.clip(ar,0,255)))
    # Remove generated carpet fragment; extend the original clear tile floor.
    tablet=patch.copy()
    tile=original.crop((1820,632,2048,768)).transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((512,136),N)
    patch.paste(tile,(0,632))
    dr=ImageDraw.Draw(patch)
    # New bay baseboard continues the exact height of the old wall.
    dr.polygon([(0,500),(512,530),(512,662),(0,632)],fill=original.getpixel((2047,570)))
    dr.line([(0,500),(512,530)],fill=original.getpixel((2047,503)),width=7)
    dr.line([(0,518),(512,548)],fill=original.getpixel((2047,520)),width=3)
    dr.line([(0,632),(512,662)],fill=original.getpixel((2047,630)),width=3)
    mask=Image.new('L',(512,768));md=ImageDraw.Draw(mask)
    md.polygon([(270,475),(290,473),(308,478),(326,476),(340,488),(359,490),(388,515),(376,643),(366,657),(305,657),(275,648),(255,628)],fill=255)
    patch.paste(tablet,(0,0),mask)
    # Structural post at the join covers wall-bay boundary without touching original.
    dr=ImageDraw.Draw(patch)
    dr.polygon([(0,0),(27,0),(27,646),(0,640)],fill=original.getpixel((1660,300)))
    dr.line([(26,0),(26,646)],fill=original.getpixel((1670,300)),width=3)
    out=Image.new('RGB',(2560,768));out.paste(original,(0,0));out.paste(patch,(2048,0))
    save(out,f'facility-wide-{t}.webp')
    check=Image.open(R/f'facility-wide-{t}.webp').convert('RGB')
    assert np.array_equal(np.array(check)[:,:2048],np.array(original))
    return {'time':t,'size':list(check.size),'original_left_changed_pixels':int(np.any(np.array(check)[:,:2048]!=np.array(original),axis=2).sum())}
report=[facility(t) for t in ['morning','afternoon','evening']]
(R/'work'/'validation.json').write_text(json.dumps(report,indent=2))
def label(canvas,txt,xy):ImageDraw.Draw(canvas).text(xy,txt,font=font,fill='white')
w=Image.open(R/'woodshed-interior-wide.webp')
p=Image.new('RGB',(1280,1220),'#20202a');p.paste(w.resize((1280,384),N),(0,30));label(p,'AFTERNOON - FULL 2560 x 768 / 50%',(12,4))
for i,x in enumerate([0,1280]):
    tile=w.crop((x,48,x+1280,768));p.paste(tile.resize((640,360),N),(i*640,448));label(p,f'VIEW {i+1} - x={x}, y=48 / 50%',(i*640+8,420))
e=Image.open(R/'woodshed-interior-wide-evening.webp');p.paste(e.resize((1280,384),N),(0,836));p=p.crop((0,0,1280,1220));p.save(R/'preview2_woodshed.png')
p=Image.new('RGB',(1280,2250),'#20202a')
for i,t in enumerate(['morning','afternoon','evening']):
    f=Image.open(R/f'facility-wide-{t}.webp');label(p,f'{t.upper()} - RIGHT VIEW 1280 x 720 (x=1280,y=48)',(10,i*750+4));p.paste(f.crop((1280,48,2560,768)),(0,i*750+30))
p.save(R/'preview2_facility.png')
# Every comparison takes 240x180 native pixels and enlarges exactly 3x nearest.
p=Image.new('RGB',(1440,1180),'#20202a')
pairs=[(Image.open(B/'ref'/'room13-pixel-panorama-woodshed-intact.webp'),(900,250),w,(1020,280),'EXISTING WOODSHED','NEW WET LOGS'),(Image.open(B/'ref'/'room13-pixel-ready-facility0177-afternoon.webp'),(1450,120),Image.open(R/'facility-wide-afternoon.webp'),(2200,170),'EXISTING FACILITY','NEW MURAL')]
for row,(a,pa,b,pb,la,lb) in enumerate(pairs):
    for col,(im,pt,txt) in enumerate([(a,pa,la),(b,pb,lb)]):
        x,y=pt;tile=im.crop((x,y,x+240,y+180)).resize((720,540),N);p.paste(tile,(col*720,row*590+38));label(p,txt+' - 3x',(col*720+10,row*590+7))
p.save(R/'preview2_dot_compare.png')
print(json.dumps(report))
