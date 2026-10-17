"""사건별 인물관계도 (사건마다 한 장). 데이터: docs/relations_by_episode.json (대본에서 정리).
   python3 dev/relation_chart_cases.py OUT_DIR [--no-spoiler]
   자리: 왼쪽 위 피해자·희생자 / 가운데 조사하는 사람·관련자 / 오른쪽 위 용의자·범인 / 아래 증인 · 조력자.
   선: 관계 종류별 색. 점선 = 사실과 다른 의심. 보라 굵은 선과 ★ = 정답이 드러나는 관계(--no-spoiler면 뺀다)."""
import json,math,sys,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];G=ROOT/"game"
FONT=str(G/"assets/Galmuri11.ttf")
def F(n):return ImageFont.truetype(FONT,n)
DATA=json.load(open(ROOT/"docs/relations_by_episode.json"))
NAMES={}
sys.path.insert(0,str(Path(__file__).resolve().parent))
try:
    from relation_chart import people as _bible
    NAMES.update({k:v["name"] for k,v in _bible.items()})
except Exception:pass
try:NAMES.update(json.load(open("/tmp/room13-qa/thread_audit.json"))["names"])
except Exception:pass
NAMES.update({"dad":"아빠","daram":"다람","mom":"엄마","granny":"할머니","kid_siluk1":"실룩네 큰아이","kid_siluk2":"실룩네 작은아이","chorong_mother":"초롱의 어머니"})
AV=json.load(open(G/"assets/room13-avatars.json"))
KIND={"family":((178,134,46),5,"가족"),"work":((70,110,160),3,"함께 일함"),"help":((60,140,90),3,"도움·부탁"),
 "suspect":((190,60,40),3,"의심·지목"),"conflict":((214,120,30),3,"갈등·해침"),"secret":((110,80,140),3,"숨긴 거래·비밀"),
 "hide":((140,100,70),3,"감쌈·숨겨 줌")}
SPOIL=(150,40,170)
ZONES=[("victim",("피해자","희생자"),"피해자 · 희생자",(244,220,214)),
 ("center",("조사자","의뢰인"),"조사하는 사람",(236,226,204)),
 ("culprit",("용의자","범인"),"용의자 · 범인",(226,214,214)),
 ("related",("관련자",),"관련된 사람",(236,230,214)),
 ("witness",("증인",),"증인",(220,230,236)),
 ("helper",("조력자",),"조력자",(222,236,222))]
CW,CH=150,150;SX,SY=186,176;GAP=24
def layout(groups):
    """Zone rectangles sized to their people: top row victim | center+related | culprit, bottom row witness | helper."""
    cols={"victim":3,"center":5,"related":5,"culprit":3,"witness":6,"helper":6}
    def hgt(z):return 0 if not groups[z] else 54+math.ceil(len(groups[z])/cols[z])*SY
    wz={z:cols[z]*SX+30 for z in cols}
    top=max(hgt("victim"),hgt("center")+(GAP if hgt("center") and hgt("related") else 0)+hgt("related"),hgt("culprit"))
    W=40+wz["victim"]+GAP+wz["center"]+GAP+wz["culprit"]+40
    R={};y0=190;x=40
    R["victim"]=(x,y0,wz["victim"],top);x+=wz["victim"]+GAP
    R["center"]=(x,y0,wz["center"],hgt("center"));R["related"]=(x,y0+hgt("center")+(GAP if hgt("center") else 0),wz["center"],hgt("related"));x+=wz["center"]+GAP
    R["culprit"]=(x,y0,wz["culprit"],top)
    y1=y0+top+GAP*2;bw=(W-80-GAP)//2;bh=max(hgt("witness"),hgt("helper"))
    R["witness"]=(40,y1,bw,bh);R["helper"]=(40+bw+GAP,y1,bw,bh)
    return W,y1+bh+40,R,cols
def face(img,d,p,x,y,note,role):
    d.rounded_rectangle((x,y,x+CW-10,y+CH-10),10,fill=(250,243,226),outline=(150,120,80),width=2)
    im=None;spec=(AV.get(p) or {}).get("avatar_neutral")
    try:
        if spec:
            im=Image.open(G/spec["file"]).convert("RGBA");a,b,c,e=spec["crop"];im=im.crop((a,b,a+c,b+e))
        else:
            alt=sorted(G.glob("assets/room13-role-%s*.webp"%p))+sorted(G.glob("assets/room13-fullbody-%s-neutral.webp"%p))+sorted(G.glob("assets/room13-canonical-default-%s.webp"%p))+sorted(G.glob("assets/*%s*.webp"%p))
            if alt:
                im=Image.open(alt[0]).convert("RGBA");im=im.crop(im.getbbox() or (0,0,im.width,im.height))
                s=int(im.width*0.62);x0=(im.width-s)//2;im=im.crop((x0,0,x0+s,s))
    except Exception:im=None
    cx=x+(CW-10)//2
    if im:
        im.thumbnail((76,62),Image.NEAREST);img.paste(im,(int(cx-im.width/2),y+6+(62-im.height)//2),im)
    else:
        d.ellipse((cx-28,y+8,cx+28,y+64),fill=(222,204,170));nm=NAMES.get(p,p)[:1];tw=d.textlength(nm,font=F(28));d.text((cx-tw/2,y+20),nm,font=F(28),fill=(120,88,52))
    nm=NAMES.get(p,p);f=F(17 if len(nm)<=6 else 14);tw=d.textlength(nm,font=f);d.text((cx-tw/2,y+72),nm,font=f,fill=(70,48,30))
    lines=wrap(note,CW-22,F(12))[:3]
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=F(12));d.text((cx-tw/2,y+96+i*15),l,font=F(12),fill=(120,96,70))
def wrap(t,w,f):
    out=[];cur=""
    for ch in t:
        if ImageDraw.Draw(Image.new("RGB",(1,1))).textlength(cur+ch,font=f)>w:out.append(cur);cur=ch
        else:cur+=ch
    if cur:out.append(cur)
    return out
def zone_of(role):
    for z,roles,_,_ in ZONES:
        if role in roles:return z
    return "related"
def draw(ep,out,spoil=True):
    groups={z:[] for z,_,_,_ in ZONES}
    for p in ep["people"]:groups[zone_of(p["role"])].append(p)
    W,H,RECT,COLS=layout(groups)
    rels=[r for r in ep["relations"] if spoil or not r.get("spoiler")]
    TAB=H;H=H+70+math.ceil(len(rels)/2)*30
    img=Image.new("RGB",(W,H),(243,231,206));d=ImageDraw.Draw(img)
    d.text((40,26),ep["title"] if ep["title"].startswith(ep["mark"]) else "%s %s"%(ep["mark"],ep["title"]),font=F(44),fill=(90,64,38))
    d.text((44,84),ep["days"]+" · "+ep["summary"],font=F(20),fill=(110,86,60))
    lx=40
    for k,(c,w,lab) in KIND.items():
        d.line((lx,134,lx+34,134),fill=c,width=w);d.text((lx+40,124),lab,font=F(16),fill=c);lx+=40+d.textlength(lab,font=F(16))+28
    d.line((lx,134,lx+34,134),fill=(150,140,130),width=3);d.text((lx+40,124),"점선 = 사실과 다른 의심",font=F(16),fill=(120,110,100));lx+=250
    if spoil:d.line((lx,134,lx+34,134),fill=SPOIL,width=6);d.text((lx+40,124),"★ 정답이 드러나는 관계",font=F(16),fill=SPOIL)
    pos={}
    for z,roles,lab,col in ZONES:
        x,y,w,h=RECT[z];ps=groups[z]
        if not ps:
            continue
        d.rounded_rectangle((x,y,x+w,y+h),16,fill=col,outline=(190,170,140),width=2);d.text((x+16,y+10),lab,font=F(20),fill=(110,86,60))
        cols=COLS[z]
        for i,p in enumerate(ps):
            r,c=divmod(i,cols);n=min(cols,len(ps)-r*cols)
            px=x+(w-n*SX)//2+c*SX+(SX-CW)//2+5;py=y+44+r*SY
            pos[p["id"]]=(px+(CW-10)/2,py+(CH-10)/2,px,py,p)
    lay=Image.new("RGBA",(W,H),(0,0,0,0));ld=ImageDraw.Draw(lay)
    labels=[]
    for i,r in enumerate(rels):
        if r["a"] not in pos or r["b"] not in pos:continue
        (x1,y1),(x2,y2)=pos[r["a"]][:2],pos[r["b"]][:2]
        c,w,_=KIND.get(r["kind"],((120,120,120),3,""))
        if r.get("spoiler"):c,w=SPOIL,6
        # slight curve so parallel edges separate
        mx,my=(x1+x2)/2,(y1+y2)/2;L=math.hypot(x2-x1,y2-y1) or 1;off=((i%5)-2)*45
        cx,cy=mx-(y2-y1)/L*off,my+(x2-x1)/L*off
        pts=[((1-t)**2*x1+2*(1-t)*t*cx+t*t*x2,(1-t)**2*y1+2*(1-t)*t*cy+t*t*y2) for t in [k/40 for k in range(41)]]
        dashed=r.get("truth") is False
        for k in range(40):
            if dashed and k%2:continue
            ld.line(pts[k]+pts[k+1],fill=c+(235,),width=w)
        # arrowhead toward b
        ax,ay=pts[34];bx,by=pts[37];ang=math.atan2(by-ay,bx-ax)
        tip=pts[36];ld.polygon([tip,(tip[0]-16*math.cos(ang-0.4),tip[1]-16*math.sin(ang-0.4)),(tip[0]-16*math.cos(ang+0.4),tip[1]-16*math.sin(ang+0.4))],fill=c+(235,))
        labels.append((r,pts,c))
    img.paste(lay,(0,0),lay);d=ImageDraw.Draw(img)
    cards=[(v[2]-4,v[3]-4,v[2]+CW-6,v[3]+CH-6) for v in pos.values()]
    for v in pos.values():face(img,d,v[4]["id"],v[2],v[3],v[4].get("note",""),v[4]["role"])
    boxes=list(cards)
    def free(b):return all(b[2]<o[0] or b[0]>o[2] or b[3]<o[1] or b[1]>o[3] for o in boxes)
    d.text((40,TAB+10),"관계 목록 (번호 = 그림의 번호표, 화살표는 앞 사람 → 뒤 사람)",font=F(22),fill=(90,64,38))
    colw=(W-80)//2
    for n,(r,pts,c) in enumerate(labels,1):
        text=("★ " if r.get("spoiler") else "")+r["label"]+(" (틀림)" if r.get("truth") is False else "")
        badge=str(n);bw=d.textlength(badge,font=F(15))+12
        tw=d.textlength(text,font=F(15));best=None;short=True
        for t,dy in [(t,dy) for dy in (0,-22,22) for t in (20,16,24,12,28,8,32)]:
            mx,my=pts[t];my+=dy;b=(mx-(tw+bw)/2-6,my-12,mx+(tw+bw)/2+6,my+12)
            if free(b) and 0<b[0] and b[2]<W:best=b;break
        if best is None:
            short=False
            for t,dy in [(t,dy) for dy in (0,-18,18,-36,36) for t in (20,16,24,12,28,8,32,4,36)]:
                mx,my=pts[t];my+=dy;b=(mx-bw/2-2,my-12,mx+bw/2+2,my+12)
                if free(b):best=b;break
            if best is None:mx,my=pts[20];best=(mx-bw/2-2,my-12,mx+bw/2+2,my+12)
        boxes.append(best);d.rounded_rectangle(best,5,fill=(252,247,234),outline=c,width=2)
        d.rounded_rectangle((best[0]+2,best[1]+2,best[0]+bw,best[3]-2),4,fill=c);d.text((best[0]+8,best[1]+4),badge,font=F(15),fill=(255,250,240))
        if short:d.text((best[0]+bw+6,best[1]+4),text,font=F(15),fill=c)
        row,col=divmod(n-1,2);tx=40+col*colw;ty=TAB+50+row*30
        d.rounded_rectangle((tx,ty,tx+bw,ty+24),4,fill=c);d.text((tx+6,ty+3),badge,font=F(15),fill=(255,250,240))
        line="%s → %s · %s"%(NAMES.get(r["a"],r["a"]),NAMES.get(r["b"],r["b"]),text)
        rv=r.get("reveal","")
        d.text((tx+bw+8,ty+3),line,font=F(16),fill=c)
        lw=d.textlength(line,font=F(16))
        if rv:
            rv="  알게 되는 곳: "+rv
            while rv and lw+d.textlength(rv,font=F(13))>colw-bw-30:rv=rv[:-2]+"…" if len(rv)>3 else ""
            d.text((tx+bw+8+lw,ty+6),rv,font=F(13),fill=(130,110,90))
    img.save(out)
    return len(pos),len(labels)
if __name__=="__main__":
    out=Path(sys.argv[1] if len(sys.argv)>1 else "relation_cases");out.mkdir(parents=True,exist_ok=True)
    spoil="--no-spoiler" not in sys.argv
    for i,ep in enumerate(DATA["episodes"]):
        n,m=draw(ep,out/("%d_%s.png"%(i+1,ep["id"])),spoil);print(ep["id"],n,"people",m,"relations")
