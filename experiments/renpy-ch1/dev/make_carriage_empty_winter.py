"""Build assets/room13-pixel-carriage-empty-winter.webp.

usage: make_carriage_empty_winter.py INTRO04_carriage_empty.png room13-pixel-carriage-morning.(png|webp) OUT.png
The empty interior comes from preview/ch1-gpt-20261008/art/ch1/bg/INTRO04_carriage_empty.png (git history).
"""
import sys
import numpy as np
from PIL import Image, ImageDraw
emp=Image.open(sys.argv[1]).convert('RGB')
cgim=Image.open(sys.argv[2]).convert('RGB')
x0,y0,x1,y1=70,0,301,282
poly=[(x0,0),(x1,0),(x1,252),(x0,282)]
mk=Image.new('L',emp.size,0);ImageDraw.Draw(mk).polygon(poly,fill=255)
inside=np.asarray(mk)==0
cg=np.asarray(cgim).astype(float);e=np.asarray(emp).astype(float)
# Match the interior's colour statistics to the existing winter carriage art
# (wood/seat/wall regions without people or window).
ref=np.concatenate([r.reshape(-1,3) for r in (cg[0:60,560:1672],cg[0:700,1500:1672],cg[860:941,0:1672],cg[600:860,0:300])])
src=e[inside]
out=e.copy()
out[inside]=(src-src.mean(0))/src.std(0)*ref.std(0)+ref.mean(0)
out=Image.fromarray(np.clip(out,0,255).astype('uint8'))
win=cgim.crop((110,0,490,463)).resize((x1-x0,y1-y0),Image.LANCZOS)
layer=out.copy();layer.paste(win,(x0,y0))
out=Image.composite(layer,out,mk)
out=out.crop((30,0,30+693,390)).resize((1386,780),Image.NEAREST)
out.save(sys.argv[3])
