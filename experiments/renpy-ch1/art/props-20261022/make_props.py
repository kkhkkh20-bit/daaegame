"""0.20.7 prop pictures for the day-1 cuts: Daram's family drawing (three arms) and the snack bag
folded twice. 384x384 RGBA like game/assets/evidence/*.webp. Run from experiments/renpy-ch1."""
import math,random
from PIL import Image,ImageDraw,ImageFilter
random.seed(13)
S=4;W=384*S
def paper(img,box,angle,color=(242,228,198),edge=(120,82,52)):
    x0,y0,x1,y1=box
    sheet=Image.new('RGBA',(x1-x0,y1-y0),color+(255,))
    d=ImageDraw.Draw(sheet)
    for _ in range(900):
        x=random.randrange(sheet.width);y=random.randrange(sheet.height);c=random.randint(-14,8)
        d.point((x,y),fill=(color[0]+c,color[1]+c,color[2]+c,255))
    d.rectangle((0,0,sheet.width-1,sheet.height-1),outline=edge+(255,),width=3*S)
    sheet=sheet.filter(ImageFilter.GaussianBlur(0.6*S))
    rot=sheet.rotate(angle,resample=Image.BICUBIC,expand=True)
    shadow=Image.new('RGBA',rot.size,(0,0,0,0));shadow.paste((40,24,14,110),mask=rot.split()[3])
    shadow=shadow.filter(ImageFilter.GaussianBlur(6*S))
    cx=(x0+x1)//2;cy=(y0+y1)//2
    img.alpha_composite(shadow,(cx-rot.width//2+4*S,cy-rot.height//2+6*S))
    img.alpha_composite(rot,(cx-rot.width//2,cy-rot.height//2))
def crayon(d,pts,col,w=5):
    for (ax,ay),(bx,by) in zip(pts,pts[1:]):
        n=max(2,int(math.hypot(bx-ax,by-ay)/(3*S)))
        prev=None
        for i in range(n+1):
            t=i/n;x=ax+(bx-ax)*t+random.uniform(-1.2,1.2)*S;y=ay+(by-ay)*t+random.uniform(-1.2,1.2)*S
            if prev:d.line([prev,(x,y)],fill=col,width=int(w*S))
            prev=(x,y)
def circle(d,cx,cy,r,col,w=5):
    pts=[(cx+r*math.cos(a/24*2*math.pi)*random.uniform(.94,1.06),cy+r*math.sin(a/24*2*math.pi)*random.uniform(.94,1.06)) for a in range(25)]
    crayon(d,pts,col,w)
def person(d,x,y,h,col,arms=2,scarf=None):
    r=h*.16;circle(d,x,y-h*.8,r,col)
    crayon(d,[(x,y-h*.64),(x,y-h*.2)],col)
    crayon(d,[(x,y-h*.2),(x-h*.14,y)],col);crayon(d,[(x,y-h*.2),(x+h*.14,y)],col)
    for i in range(arms):
        ang=[-160,-20,35][i] if arms==3 else [-150,-30][i]
        ex=x+math.cos(math.radians(ang))*h*.3;ey=y-h*.5+math.sin(math.radians(ang))*h*.22
        crayon(d,[(x,y-h*.5),(ex,ey)],col)
    if scarf:crayon(d,[(x-r,y-h*.62),(x+r,y-h*.62),(x+r*.6,y-h*.48)],scarf,7)
# family drawing
img=Image.new('RGBA',(W,W),(0,0,0,0))
paper(img,(40*S,50*S,344*S,334*S),-4)
layer=Image.new('RGBA',(W,W),(0,0,0,0));d=ImageDraw.Draw(layer)
circle(d,300*S,95*S,22*S,(236,170,40,255),6)
for a in range(0,360,45):
    crayon(d,[(300*S+math.cos(math.radians(a))*28*S,95*S+math.sin(math.radians(a))*28*S),(300*S+math.cos(math.radians(a))*40*S,95*S+math.sin(math.radians(a))*40*S)],(236,170,40,255),4)
person(d,120*S,280*S,150*S,(70,92,150,255))
person(d,195*S,280*S,132*S,(150,70,60,255),scarf=(205,40,40,255))
person(d,262*S,284*S,96*S,(120,72,40,255),arms=3)
crayon(d,[(70*S,292*S),(330*S,296*S)],(90,140,70,255),5)
layer=layer.rotate(-4,resample=Image.BICUBIC,center=(192*S,192*S)).filter(ImageFilter.GaussianBlur(0.5*S))
img.alpha_composite(layer)
img.resize((384,384),Image.LANCZOS).save('game/assets/evidence/D01_FAMILY_DRAWING.webp','WEBP',quality=92)
# snack bag folded twice
img=Image.new('RGBA',(W,W),(0,0,0,0))
bag=Image.new('RGBA',(200*S,210*S),(0,0,0,0));d=ImageDraw.Draw(bag)
body=(196,150,96);d.rounded_rectangle((10*S,40*S,190*S,205*S),18*S,fill=body+(255,),outline=(110,72,40,255),width=4*S)
for i,yy in enumerate((12*S,30*S)):
    d.rounded_rectangle((14*S,yy,186*S,yy+26*S),8*S,fill=(206+i*6,162+i*6,108+i*6,255),outline=(110,72,40,255),width=4*S)
d.ellipse((70*S,100*S,130*S,160*S),outline=(160,60,48,255),width=5*S)
for _ in range(500):
    x=random.randrange(14*S,186*S);y=random.randrange(44*S,200*S);c=random.randint(-12,8)
    d.point((x,y),fill=(body[0]+c,body[1]+c,body[2]+c,255))
bag=bag.filter(ImageFilter.GaussianBlur(0.6*S)).rotate(6,resample=Image.BICUBIC,expand=True)
shadow=Image.new('RGBA',bag.size,(0,0,0,0));shadow.paste((40,24,14,110),mask=bag.split()[3]);shadow=shadow.filter(ImageFilter.GaussianBlur(7*S))
ox=(W-bag.width)//2;oy=(W-bag.height)//2+10*S
img.alpha_composite(shadow,(ox+5*S,oy+8*S));img.alpha_composite(bag,(ox,oy))
img.resize((384,384),Image.LANCZOS).save('game/assets/evidence/D01_SNACK_BAG.webp','WEBP',quality=92)
