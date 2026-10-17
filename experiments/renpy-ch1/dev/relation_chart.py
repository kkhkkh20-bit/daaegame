"""전체 인물관계도 그림 (docs/CAST_BIBLE.md 가족·일터 + systems/room13_relations.rpy 이야기 관계).
   python3 dev/relation_chart.py out.png"""
import json,math,re,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];G=ROOT/"game"
FONT=str(G/"assets/Galmuri11.ttf")
def F(n):return ImageFont.truetype(FONT,n)
bible=(ROOT/"docs/CAST_BIBLE.md").read_text()
people={};order=[]
for m in re.finditer(r"### (\d+) (.+?) \(`([^`]+)`\)[^\n]*\n(.*?)(?=\n### |\Z)",bible,re.S):
    name=m.group(2).split("(")[0].replace("곰 선생님 → ","").strip();pid=m.group(3);body=m.group(4)
    f=lambda k:(re.search(r"- "+k+r": ([^\n]+)",body) or [None,""])[1]
    work=f("일터");wp,_,mates=work.partition("/ 같이 일하는 사람:")
    people[pid]=dict(name=name,home=f("사는 곳").strip(),work=wp.strip(),mates=mates.strip(),fam=f("가족·관계"),role=f("직업·역할"))
    order.append(pid)
names={v["name"]:k for k,v in people.items()}
names.update({"아빠":"dad","엄마":"mom","할머니":"granny","촌장":"resident_ppul","뿔이 촌장":"resident_ppul","사자 선생님":"resident_teacher","선생님":"resident_teacher"})
def find(text):
    out=[]
    for n,pid in sorted(names.items(),key=lambda x:-len(x[0])):
        if n and n in text and pid not in out:out.append(pid);text=text.replace(n," ")
    return out
edges={}
def add(a,b,kind,label=""):
    if a==b or a not in people or b not in people:return
    k=tuple(sorted((a,b)))
    if k in edges and edges[k][0]=="story":return
    edges[k]=(kind,label)
FAMILY=re.compile(r"딸|아들|손녀|손자|남편|아내|부모|엄마|아빠|가족|거둔|거두|함께 산|형제|자매")
for pid,p in people.items():
    for o in find(p["fam"]):add(pid,o,"family" if FAMILY.search(p["fam"]) else "work")
    for o in find(p["mates"]):add(pid,o,"work")
rel=(G/"systems/room13_relations.rpy").read_text()
for a,b,kind,label in re.findall(r'\("([\w]+)","([\w]+)","(family|work|suspect)","([^"]+)"',rel):
    if a in people and b in people:edges[tuple(sorted((a,b)))]=("story:"+kind,label)
# 묶음 배치: 사는 곳·일터로 무리 짓기
groups=[("여관",["granny","nabi","resident_tosil","resident_owlgp","buri","seryeon","doto"]),
 ("다람 가족",["daram","dad","mom"]),
 ("질서·회의",["resident_ppul","neoul","guard","resident_badook","resident_seol","resident_seori","resident_ubak"]),
 ("등불·수리",["resident_lamplighter","resident_tok","resident_ttadak","resident_piko","resident_guldol"]),
 ("시장·창고",["resident_eunho","resident_guseul","resident_madam","resident_mungchi","resident_siluk","resident_dalgeurak","resident_yeoni","resident_kongi","resident_tori","resident_kkwak","resident_hyeoni"]),
 ("우체국",["resident_sling","resident_momo","resident_librarian","resident_jongjong"]),
 ("아이들·학교·아랫길",["bami","resident_somi","resident_musoe","resident_nero","resident_teacher","resident_bori","resident_nubi"]),
 ("바깥",["karo","resident_mulgyeol","resident_solbang","resident_kalbaram"])]
placed={p for _,ps in groups for p in ps}
rest=[p for p in order if p not in placed]
if rest:groups.append(("그 밖",rest))
W,H=2600,1800;img=Image.new("RGB",(W,H),(243,231,206));d=ImageDraw.Draw(img)
pos={};cx,cy=W/2,H/2+40;R=640
n=len(groups)
for gi,(gname,ps) in enumerate(groups):
    ang=2*math.pi*gi/n-math.pi/2;gx=cx+R*1.15*math.cos(ang);gy=cy+R*0.85*math.sin(ang)
    cols=min(4,len(ps))
    for i,p in enumerate(ps):
        if p not in people:continue
        r,c=divmod(i,cols);pos[p]=(gx+(c-(cols-1)/2)*118,gy+(r-(len(ps)-1)//cols/2)*132)
    gw=d.textlength(gname,font=F(24));d.text((gx-gw/2,gy-((len(ps)-1)//cols/2)*132-104),gname,font=F(24),fill=(120,88,52))
COL={"family":(178,134,46),"work":(110,140,170),"story:family":(178,134,46),"story:work":(60,100,150),"story:suspect":(170,60,35)}
faint=Image.new("RGBA",(W,H),(0,0,0,0));fd=ImageDraw.Draw(faint)
for (a,b),(kind,label) in edges.items():
    if a in pos and b in pos and not kind.startswith("story"):
        (x1,y1),(x2,y2)=pos[a],pos[b];c=COL[kind]
        fd.line((x1,y1,x2,y2),fill=c+(255 if kind=="family" else 90,),width=5 if kind=="family" else 2)
img.paste(faint,(0,0),faint);d=ImageDraw.Draw(img)
boxes=[]
def free(b):return all(b[2]<o[0] or b[0]>o[2] or b[3]<o[1] or b[1]>o[3] for o in boxes)
for (a,b),(kind,label) in edges.items():
    if a not in pos or b not in pos or not kind.startswith("story"):continue
    (x1,y1),(x2,y2)=pos[a],pos[b];col=COL[kind];w=5 if kind.endswith("family") else 3
    if kind=="story:suspect":
        L=math.hypot(x2-x1,y2-y1);steps=max(2,int(L//14))
        for s_ in range(0,steps,2):
            t0,t1=s_/steps,min(1,(s_+1)/steps);d.line((x1+(x2-x1)*t0,y1+(y2-y1)*t0,x1+(x2-x1)*t1,y1+(y2-y1)*t1),fill=col,width=w)
    else:d.line((x1,y1,x2,y2),fill=col,width=w)
    tw=d.textlength(label,font=F(15))
    for t in (.5,.38,.62,.28,.72,.2,.8):
        mx,my=x1+(x2-x1)*t,y1+(y2-y1)*t;bx=(mx-tw/2-5,my-11,mx+tw/2+5,my+11)
        if free(bx):break
    boxes.append(bx);d.rounded_rectangle(bx,4,fill=(250,243,226),outline=col);d.text((bx[0]+5,my-8),label,font=F(15),fill=col)
av=json.load(open(G/"assets/room13-avatars.json"))
for p,(x,y) in pos.items():
    d.rounded_rectangle((x-48,y-50,x+48,y+52),8,fill=(234,215,179),outline=(150,120,80),width=2)
    spec=(av.get(p) or {}).get("avatar_neutral")
    if spec:
        try:
            im=Image.open(G/spec["file"]).convert("RGBA");cx0,cy0,cw,ch=spec["crop"];im=im.crop((cx0,cy0,cx0+cw,cy0+ch))
            im.thumbnail((84,70),Image.NEAREST);img.paste(im,(int(x-im.width/2),int(y-46+(70-im.height)/2)),im)
        except Exception:pass
    else:
        alt=sorted(G.glob("assets/room13-role-%s*.webp"%p))+sorted(G.glob("assets/room13-fullbody-%s-neutral.webp"%p))+sorted(G.glob("assets/room13-canonical-default-%s.webp"%p))
        if alt:
            im=Image.open(alt[0]).convert("RGBA");bb=im.getbbox() or (0,0,im.width,im.height);im=im.crop(bb)
            side=int(im.width*0.62);x0=(im.width-side)//2;im=im.crop((x0,0,x0+side,side));im.thumbnail((84,70),Image.NEAREST)
            img.paste(im,(int(x-im.width/2),int(y-46+(70-im.height)/2)),im)
        else:d.text((x-10,y-30),people[p]["name"][:1],font=F(34),fill=(120,88,52))
    nm=people[p]["name"];tw=d.textlength(nm,font=F(15));d.text((x-tw/2,y+28),nm,font=F(15),fill=(80,58,36))
d.text((40,30),"Room13 전체 인물관계도",font=F(40),fill=(90,64,38))
d.text((40,84),"가족(금색 굵은 선) · 함께 일함(푸른 선) · 이야기에서 드러나는 관계(이름표 있는 선, 붉은 점선 = 의심·갈등)",font=F(20),fill=(110,86,60))
d.text((40,112),"출처: docs/CAST_BIBLE.md 가족·일터, systems/room13_relations.rpy 이야기 관계. 게임 안 관계도는 이 가운데 플레이어가 알게 된 것만 보인다.",font=F(16),fill=(130,106,80))
img.save(sys.argv[1] if len(sys.argv)>1 else "relation_chart.png");print(len(people),"people",len(edges),"edges")
