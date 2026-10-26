"""13호 난로 v2(오후 그림 위에 그린 것)에서 난로 부분만 떼어 6개 배경(사건 전후 x 아침·오후·저녁) 조명에 맞춘 조각을 만든다."""
import json,sys
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
SRC=Path(sys.argv[1]); GAME=Path(sys.argv[2]); OUT=GAME/"assets/room13-stove"; OUT.mkdir(exist_ok=True)
BOX=(1850,0,2080,530)
base=np.asarray(Image.open(GAME/"assets/room13-pixel-wide-room13-before-afternoon.webp").convert("RGB")).astype(float)
states={k:np.asarray(Image.open(SRC/f"ROOM13-STOVE-{k}-v2.png").convert("RGB")).astype(float) for k in ("inner","ration","empty")}
x0,y0,x1,y1=BOX
m=np.zeros(base.shape[:2],bool)
for a in states.values(): m|=np.abs(a-base).sum(2)>60
m[:, :x0]=False;m[:, x1:]=False;m[y1:]=False
mi=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(5))
m=np.asarray(mi)>0
# 행마다 안쪽 빈칸을 메운다(난로 몸통 안의 비슷한 색 때문에 구멍이 나지 않게)
for y in range(m.shape[0]):
    xs=np.where(m[y])[0]
    if len(xs)>1:
        # 50px 넘게 떨어진 조각은 따로 둔다
        start=xs[0]
        for a,b in zip(xs[:-1],xs[1:]):
            if b-a<=50: m[y,a:b+1]=True
ys,xs=np.where(m); bx=(xs.min(),ys.min(),xs.max()+1,ys.max()+1); print("patch bbox",bx)
def blur(a): return np.asarray(Image.fromarray(np.clip(a,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40))).astype(float)
bb=blur(base)
manifest={"source":"ROOM13-STOVE-*-v2 (2026-10-26)","patch_rect":list(map(int,[bx[0],bx[1],bx[2]-bx[0],bx[3]-bx[1]])),"files":{}}
for case in ("before","after"):
    for per in ("morning","afternoon","evening"):
        tgt=np.asarray(Image.open(GAME/f"assets/room13-pixel-wide-room13-{case}-{per}.webp").convert("RGB")).astype(float)
        gain=blur(tgt)/np.maximum(bb,1)
        for st,a in states.items():
            px=np.clip(a*gain,0,255)
            rgba=np.zeros(base.shape[:2]+(4,),np.uint8); rgba[...,:3]=px.astype(np.uint8); rgba[...,3]=np.where(m,255,0)
            im=Image.fromarray(rgba).crop(bx)
            name=f"stove-{st}-{case}-{per}.webp"; im.save(OUT/name,lossless=True,quality=100,method=6)
            manifest["files"][f"{st}/{case}/{per}"]="assets/room13-stove/"+name
# 재받이 돌 조각: 보이는 부분만 잘라 제안 크기(38x18)로
ov=Image.open(SRC/"ROOM13-ASHBIN-ration-overlay.png").convert("RGBA").crop((376,293,1162,657)).resize((38,18),Image.LANCZOS)
a=np.asarray(ov).copy(); a[...,3]=np.where(a[...,3]>=128,255,0); a[a[...,3]==0]=0
Image.fromarray(a).save(OUT/"ashbin-ration-stone.webp",lossless=True,quality=100,method=6)
manifest["ashbin"]={"file":"assets/room13-stove/ashbin-ration-stone.webp","rect":[1920,492,38,18]}
json.dump(manifest,open(OUT/"manifest.json","w"),ensure_ascii=False,indent=1)
