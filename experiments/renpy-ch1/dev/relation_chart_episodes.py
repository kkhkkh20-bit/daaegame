"""사건별 인물관계도: 에피소드마다 한 칸, 그 사건에 나오는 인물과 그 사건에서 드러나는 관계만.
   python3 dev/relation_chart_episodes.py out.png
   인물 = 그 에피소드 파일에서 대사가 두 줄 이상인 사람. 이야기 관계 = room13_relations.rpy의 깃발 접두사로 사건을 정한다."""
import json,math,re,sys
from PIL import Image,ImageDraw
sys.path.insert(0,__import__("os").path.dirname(__file__))
from relation_chart import people,edges,F,G
EPISODES=[("①","등 도둑","1~4일","room13_ep1_lamp_thief.rpy","L"),
 ("②","다람 탐정단","4~5일","room13_ep2_kids.rpy","K"),
 ("③","장작 창고의 불","5~7일","room13_ep3_woodfire.rpy","F"),
 ("13호","사건과 재판","7~10일",None,"EW"),
 ("④","13호의 밤","8~10일","room13_ep4_night13.rpy","NJ"),
 ("⑤","긴 밤과 겨울 수프","10~12일","room13_ep5_soup.rpy","Y"),
 ("⑥","끌려가는 수레 · 제단","13~14일","room13_ep6_cart.rpy","V")]
CASE13=["granny","nabi","resident_tosil","resident_owlgp","buri","neoul","guard","resident_badook","resident_tok","resident_lamplighter"]
# 접두사가 아닌 깃발로 드러나는 관계의 사건
FLAG_EP={"somi_secret":"②","st_chorong_after":"①","nt_ttadak_safe":"④","ttadak_dead":"④","st_ttadak_boards":"④",
 "st_dodam_seen":"⑤","st_kkomi_class_seen":"③"}
rel=(G/"systems/room13_relations.rpy").read_text()
story=[]
for a,b,kind,label,trig in re.findall(r'\("([\w]+)","([\w]+)","(family|work|suspect)","([^"]+)",([^\n]*)\)',rel):
    keys=re.findall(r'"([\w]+)"',trig) if "_r13_rel_any" in trig else []
    eps=set()
    for k in keys:
        if k in FLAG_EP:eps.add(FLAG_EP[k])
        for ep in EPISODES:
            if re.fullmatch(r"[%s]\d+"%ep[4],k):eps.add(ep[0])
    story.append((a,b,kind,label,eps or {"*"}))
def cast(ep):
    if ep[3] is None:return list(CASE13)
    src=(G/"systems"/ep[3]).read_text();cnt={}
    for pid in re.findall(r'\("([a-z_0-9]+)",\s*"',src):
        if pid in people and pid!="dad":cnt[pid]=cnt.get(pid,0)+1
    return [p for p,n in sorted(cnt.items(),key=lambda x:-x[1]) if n>=2]
COL={"family":(178,134,46),"work":(60,100,150),"suspect":(170,60,35)}
PW,PH,COLS=1000,860,3;TOP=150
rows=math.ceil(len(EPISODES)/COLS);W,H=PW*COLS,TOP+PH*rows
img=Image.new("RGB",(W,H),(243,231,206));d=ImageDraw.Draw(img)
av=json.load(open(G/"assets/room13-avatars.json"))
def face(p,x,y):
    d.rounded_rectangle((x-44,y-46,x+44,y+48),8,fill=(234,215,179),outline=(150,120,80),width=2)
    im=None;spec=(av.get(p) or {}).get("avatar_neutral")
    try:
        if spec:
            im=Image.open(G/spec["file"]).convert("RGBA");cx0,cy0,cw,ch=spec["crop"];im=im.crop((cx0,cy0,cx0+cw,cy0+ch))
        else:
            alt=sorted(G.glob("assets/room13-role-%s*.webp"%p))+sorted(G.glob("assets/room13-fullbody-%s-neutral.webp"%p))+sorted(G.glob("assets/room13-canonical-default-%s.webp"%p))
            if alt:
                im=Image.open(alt[0]).convert("RGBA");im=im.crop(im.getbbox() or (0,0,im.width,im.height))
                side=int(im.width*0.62);x0=(im.width-side)//2;im=im.crop((x0,0,x0+side,side))
    except Exception:im=None
    if im:
        im.thumbnail((78,64),Image.NEAREST);img.paste(im,(int(x-im.width/2),int(y-42+(64-im.height)/2)),im)
    else:d.text((x-10,y-30),people[p]["name"][:1],font=F(30),fill=(120,88,52))
    nm=people[p]["name"];tw=d.textlength(nm,font=F(14));d.text((x-tw/2,y+27),nm,font=F(14),fill=(80,58,36))
def dashed(x1,y1,x2,y2,col,w):
    L=math.hypot(x2-x1,y2-y1);n=max(2,int(L//14))
    for s_ in range(0,n,2):
        t0,t1=s_/n,min(1,(s_+1)/n);d.line((x1+(x2-x1)*t0,y1+(y2-y1)*t0,x1+(x2-x1)*t1,y1+(y2-y1)*t1),fill=col,width=w)
total_story=0
for i,ep in enumerate(EPISODES):
    r,c=divmod(i,COLS);ox,oy=c*PW,TOP+r*PH
    d.rounded_rectangle((ox+14,oy+10,ox+PW-14,oy+PH-14),14,outline=(170,140,100),width=3,fill=(248,239,220))
    d.text((ox+36,oy+26),"%s %s"%(ep[0],ep[1]),font=F(30),fill=(90,64,38))
    d.text((ox+36,oy+66),ep[2],font=F(18),fill=(130,106,80))
    ps=cast(ep)
    for a,b,kind,label,eps in story:
        if ep[0] in eps:
            for p in (a,b):
                if p in people and p not in ps and p!="dad":ps.append(p)
    ps=ps[:16];cx,cy=ox+PW/2,oy+PH/2+40;R=min(330,90+22*len(ps))
    pos={p:(cx+R*math.cos(2*math.pi*k/len(ps)-math.pi/2),cy+R*0.86*math.sin(2*math.pi*k/len(ps)-math.pi/2)) for k,p in enumerate(ps)}
    faint=Image.new("RGBA",(W,H),(0,0,0,0));fd=ImageDraw.Draw(faint)
    for (a,b),(kind,label) in edges.items():
        if a in pos and b in pos and not kind.startswith("story"):
            fd.line(pos[a]+pos[b],fill=(178,134,46,200) if kind=="family" else (110,140,170,90),width=4 if kind=="family" else 2)
    img.paste(faint,(0,0),faint);d=ImageDraw.Draw(img)
    boxes=[]
    for a,b,kind,label,eps in story:
        if a not in pos or b not in pos or not (ep[0] in eps or "*" in eps):continue
        (x1,y1),(x2,y2)=pos[a],pos[b];col=COL[kind];w=5 if kind=="family" else 3
        if ep[0] in eps:total_story+=1
        (dashed if kind=="suspect" else (lambda *q:d.line(q[:4],fill=q[4],width=q[5])))(x1,y1,x2,y2,col,w)
        tw=d.textlength(label,font=F(15))
        for t in (.5,.38,.62,.28,.72):
            mx,my=x1+(x2-x1)*t,y1+(y2-y1)*t;bx=(mx-tw/2-5,my-11,mx+tw/2+5,my+11)
            if all(bx[2]<o[0] or bx[0]>o[2] or bx[3]<o[1] or bx[1]>o[3] for o in boxes):break
        boxes.append(bx);d.rounded_rectangle(bx,4,fill=(250,243,226),outline=col);d.text((bx[0]+5,my-8),label,font=F(15),fill=col)
    for p,(x,y) in pos.items():face(p,x,y)
d.text((40,28),"Room13 사건별 인물관계도",font=F(40),fill=(90,64,38))
d.text((40,82),"칸마다 그 사건에 나오는 인물(대사 두 줄 이상)과 그 사건에서 드러나는 관계. 가족(금색) · 함께 일함(푸른 선) · 이름표 선 = 이야기 관계, 붉은 점선 = 의심·갈등",font=F(19),fill=(110,86,60))
d.text((40,110),"출처: 에피소드 파일 대사, docs/CAST_BIBLE.md, systems/room13_relations.rpy(깃발 접두사로 사건 배정). 13호 칸은 여관·순찰 인물 고정 목록.",font=F(16),fill=(130,106,80))
img.save(sys.argv[1] if len(sys.argv)>1 else "relation_chart_episodes.png");print(len(EPISODES),"panels",total_story,"story edges placed")
