from PIL import Image, ImageDraw, ImageChops
from pathlib import Path
import sys, json
out=Path('/home/claude/daaegame/experiments/renpy-ch1/art/gate-wide-20261022')
src=Image.open('/home/claude/daaegame/experiments/renpy-ch1/game/assets/room13-pixel-ready-gate0173-morning.webp').convert('RGB').resize((1920,720),Image.Resampling.NEAREST)
gen=Image.open(sys.argv[1]).convert('RGB')
print('생성 크기',gen.size)
gen=gen.resize((2560,960),Image.Resampling.LANCZOS) if gen.size!=(2560,960) else gen
# 외곽에만 2px 픽셀 격자를 적용한다.
gen=gen.resize((1280,480),Image.Resampling.BOX).resize((2560,960),Image.Resampling.NEAREST)
# 원본 바깥 6px에서만 접합 색상 차이를 점진적으로 보정한다.
import numpy as np
a=np.array(gen).astype(float)
b=np.array(src).astype(float)
for k in range(1,7):
    w=(7-k)/7
    a[200:920,320-k,:]+=w*(b[:,0,:]-np.array(gen) [200:920,320,:])
    a[200:920,2239+k,:]+=w*(b[:,-1,:]-np.array(gen)[200:920,2239,:])
    a[200-k,320:2240,:]+=w*(b[0,:,:]-np.array(gen)[200,320:2240,:])
    a[919+k,320:2240,:]+=w*(b[-1,:,:]-np.array(gen)[919,320:2240,:])
gen=Image.fromarray(np.clip(a,0,255).astype('uint8'))
gen.paste(src,(320,200))
gen.save(out/'gate-wide-morning.png')
preview=gen.resize((1920,720),Image.Resampling.NEAREST)
d=ImageDraw.Draw(preview)
d.rectangle((0,0,1279,719),outline=(255,70,100),width=2)
d.rectangle((640,0,1919,719),outline=(35,235,210),width=2)
preview.save(out/'preview-75.png')
assert gen.size==(2560,960)
assert ImageChops.difference(gen.crop((320,200,2240,920)),src).getbbox() is None
print('검증 통과: 2560×960, 중앙 1920×720 모든 픽셀 일치, 미리보기 1920×720')
