# 피코의 처마 옆 그림(NW_PIKO_SKETCH4) 임시 그림: 1일 가족 그림의 종이 위에 숯 선을 그린다.
import random, math
from PIL import Image, ImageDraw, ImageFilter
SRC='/home/user/daaegame/experiments/renpy-ch1/game/assets/evidence/D01_FAMILY_DRAWING.webp'
base=Image.open(SRC).convert('RGBA')
W,H=base.size
px=base.load()
# 종이 안쪽 색을 표본으로 잡아 원래 크레용 그림을 지운다(테두리·그림자는 그대로).
paper=px[150,240]
mask=Image.new('L',(W,H),0)
md=ImageDraw.Draw(mask)
md.polygon([(56,56),(340,66),(334,326),(44,314)],fill=255)
clean=base.copy(); cd=ImageDraw.Draw(clean)
cd.polygon([(56,56),(340,66),(334,326),(44,314)],fill=paper)
# 테두리 가까이 남은 해 그림(노랑·주황) 점을 종이색으로 덮는다.
cp=clean.load()
for y in range(40,140):
    for x in range(280,360):
        r,g,b,a=cp[x,y]
        if a>0 and r>180 and b<150 and r-b>90: cp[x,y]=paper
# 종이 결: 아주 옅은 얼룩
random.seed(4)
grain=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(grain)
for _ in range(900):
    x=random.randint(45,340); y=random.randint(55,325); a=random.randint(4,12)
    gd.point((x,y),fill=(120,100,70,a))
clean=Image.alpha_composite(clean,Image.composite(grain,Image.new('RGBA',(W,H),(0,0,0,0)),mask))
ink=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ink)
C=(48,44,40,215)
def shaky(points,width=4,jit=1.6,col=C,passes=2):
    for p in range(passes):
        pts=[]
        for (x0,y0),(x1,y1) in zip(points,points[1:]):
            n=max(2,int(math.hypot(x1-x0,y1-y0)/6))
            for i in range(n):
                t=i/n; pts.append((x0+(x1-x0)*t+random.uniform(-jit,jit),y0+(y1-y0)*t+random.uniform(-jit,jit)))
        pts.append(points[-1])
        d.line(pts,fill=col if p==0 else (col[0],col[1],col[2],110),width=width if p==0 else max(1,width-2),joint='curve')
# 처마 기둥과 처마 끝(왼쪽)
shaky([(92,318),(96,96)],6); shaky([(70,100),(150,84)],5)
for y in range(110,300,46): shaky([(94,y),(102,y+3)],2)
# 울타리(오른쪽)
for x in (276,306,330):
    shaky([(x,312),(x+2,232)],4)
shaky([(262,250),(336,246)],3); shaky([(262,282),(336,278)],3)
# 허리를 숙인 사람: 머리·굽은 등·다리
d.ellipse((222,184,244,206),outline=C,width=4)   # 앞으로 숙인 머리
shaky([(224,196),(204,178),(186,184),(172,214)],5)  # 굽은 등(가장 높은 데가 y178)
shaky([(172,214),(166,262),(158,312)],4)          # 뒷다리
shaky([(176,216),(194,262),(212,306)],4)          # 앞다리
shaky([(158,312),(146,314)],3); shaky([(212,306),(226,309)],3)  # 맨발
shaky([(204,190),(226,222),(238,246)],4)          # 앞으로 늘어뜨린 팔
# 찢어진 소매: 팔꿈치 아래로 늘어진 천 조각
shaky([(220,212),(210,240),(218,258)],3); shaky([(228,222),(228,246),(218,258)],3)
for k in range(3): shaky([(212+k*4,244),(210+k*4,262)],2)
# 키를 잰 표시: 기둥 절반 높이 눈금과 화살표
shaky([(84,207),(110,207)],3); [d.line([(x,178),(x+5,178)],fill=(48,44,40,150),width=2) for x in range(104,198,10)]
d.text((112,212),"1/2",fill=(48,44,40,190))
# 발자국 방향 점선
for x in range(236,262,8): d.line([(x,306),(x+4,306)],fill=(48,44,40,150),width=2)
ink=ink.filter(ImageFilter.GaussianBlur(0.6))
out=Image.alpha_composite(clean,Image.composite(ink,Image.new('RGBA',(W,H),(0,0,0,0)),mask))
# 정식 그림이 오기 전까지 쓰는 임시 그림이다(0.20.18). 다시 만들 때: python3 dev/make_piko_sketch4.py
out.save(SRC.replace('D01_FAMILY_DRAWING','NW_PIKO_SKETCH4'),lossless=True)
print(out.size,paper)
