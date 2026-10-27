"""현장(조사 화면) 인물 그림을 대화 도트판과 같은 도트 수로 다시 찍는다(2026-10-27).

규칙
- 서 있는 그림(neutral): 대화 도트판 assets/dialogue-dot-v2/<인물>/560/neutral.webp 가 있으면 그것을 정확히 1/2 로
  되돌려(560 판은 2배 복제) 1배 도트 마스터로 쓴다. 어른 210·덩치 230·노인 195·부리 185·아이 165·도담 132 도트.
- 몸동작 그림(action_1/2·activity·living_*·map27 등): 원본 잘라낸 영역을 칸 평균으로 줄여 같은 도트 칸으로 찍는다.
  같은 시트에서 온 자세는 평온 그림과 같은 배율(원래 그림 안의 비율 유지), 다른 파일이면 stature_ratio
  (없으면 머리 크기 비율)로 키를 정한다.
- 색은 그 그림의 48색 팔레트로 되돌리고 알파는 끊는다(110). 무손실 저장.
- 발·손·고리·좌석·머리 상자는 같은 배율로 도트 좌표로 옮겨 표(json)에 적는다.
결과: game/assets/field-dot-v2/<인물>/<자세>.webp, game/assets/room13-field-dot-v2.json
원본 파일은 건드리지 않는다.
"""
import json,sys,os
from pathlib import Path
from PIL import Image
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
from dotlib import bb,palette,regrid

game=Path(sys.argv[1])
OUT=game/"assets/field-dot-v2"
TABLE=game/"assets/room13-field-dot-v2.json"
KID={"daram","kid_kkomi","resident_somi","resident_tosil","bami","resident_kongi","kid_saemi","v111_child"}
SMALL={"kid_dodam"}
OLD={"granny","resident_owlgp","npc_pandol","elder","v111_lowerroad_elder"}
TEEN={"buri"}
BIG={"resident_bori","resident_guldol","resident_musoe","resident_teacher","karo"}
def target_dots(p):
    if p in BIG:return 230
    if p in KID or p.startswith("kid_"):return 165
    if p in SMALL:return 132
    if p in OLD:return 195
    if p in TEEN:return 185
    return 210

def load_specs():
    specs={}
    A=json.load(open(game/"assets/room13-pixel-acting.json"))
    for p,d in A.items():
        for pose,s in d.items():
            if isinstance(s,dict) and "crop" in s and not pose.startswith("avatar_"):specs.setdefault(p,{})[pose]=s
    for row in json.load(open(game/"assets/room13-map-action27.json"))["rows"]:
        if row.get("status")=="approved" and (game/row["spec"]["file"]).exists():specs.setdefault(row["person"],{})[row["pose"]]=row["spec"]
    for row in json.load(open(game/"assets/room13-map-work-nine.json"))["people"]:
        specs.setdefault(row["person"],{})[row["pose"]]=row["spec"]
    sr=json.load(open(game/"assets/room13-seori-review-art.json"))
    specs.setdefault(sr["person"],{})[sr["pose"]]=sr["spec"]
    for g in json.load(open(game/"assets/room13-life-groups.json"))["groups"]:
        for m in g["members"]:
            if m.get("spec") and (game/m["spec"]["file"]).exists():specs.setdefault(m["person"],{})[m["pose"]]=m["spec"]
    return specs

def crop_image(spec):
    x,y,w,h=[int(round(v)) for v in spec["crop"]]
    return Image.open(game/spec["file"]).convert("RGBA").crop((x,y,x+w,y+h))

def head_from_alpha(im):
    a=np.asarray(im)[...,3]>=128
    x0,y0,x1,y1=bb(im)
    hh=max(1,int(round((y1-y0)*0.35)))
    rows=a[y0:y0+hh]
    cols=np.where(rows.any(0))[0]
    if len(cols)==0:return [x0,y0,x1-x0,hh]
    return [int(cols.min()),y0,int(cols.max()-cols.min()+1),hh]

def finish(im,person,pose,points,source,ratio,origin="field"):
    # 불투명 영역만 남기고 자르되, 좌표는 자른 만큼 옮긴다.
    x0,y0,x1,y1=bb(im)
    im=im.crop((x0,y0,x1,y1))
    rel="assets/field-dot-v2/%s/%s.webp"%(person,pose)
    (game/rel).parent.mkdir(parents=True,exist_ok=True)
    im.save(game/rel,lossless=True,quality=100,method=6)
    entry=dict(file=rel,size=[im.width,im.height],origin=origin,source=source,ratio=ratio)
    for k,v in points.items():
        if k=="head":entry[k]=[round(v[0]-x0,1),round(v[1]-y0,1),round(v[2],1),round(v[3],1)]
        else:entry[k]=[round(v[0]-x0,1),round(v[1]-y0,1)]
    if "head" not in entry:entry["head"]=head_from_alpha(im)
    if "foot" not in entry:entry["foot"]=[im.width/2.0,float(im.height)]
    return entry

def main():
    specs=load_specs()
    table={}
    report=[]
    persons=sorted(set(specs)|{d for d in os.listdir(game/"assets/dialogue-dot-v2") if (game/"assets/dialogue-dot-v2"/d/"560/neutral.webp").exists()})
    for person in persons:
        poses=specs.get(person,{})
        T=target_dots(person)
        dia=game/"assets/dialogue-dot-v2"/person/"560/neutral.webp"
        entries={}
        # 평온(서 있는) 그림
        neutral_spec=poses.get("neutral")
        f_n=None;neutral_file=None
        if neutral_spec:
            nim=crop_image(neutral_spec);nb=bb(nim);f_n=T/float(nb[3]-nb[1]);neutral_file=neutral_spec["file"]
        if dia.exists():
            a=np.asarray(Image.open(dia).convert("RGBA"))[::2,::2]
            im=Image.fromarray(a.copy())
            entries["neutral"]=finish(im,person,"neutral",{},dict(file=str(dia.relative_to(game)),crop=None),1.0,origin="dialogue")
            report.append((person,"neutral","dialogue",entries["neutral"]["size"][1]))
        elif neutral_spec:
            pal=palette(nim)
            d=regrid(nim,f_n,pal)
            pts={k:[v[0]*f_n,v[1]*f_n] for k,v in neutral_spec.items() if k in ("foot","hook","seat","hand") and isinstance(v,list)}
            if neutral_spec.get("anchor") and isinstance(neutral_spec["anchor"],dict) and "foot" in neutral_spec["anchor"] and "foot" not in pts:
                pts["foot"]=[neutral_spec["anchor"]["foot"][0]*f_n,neutral_spec["anchor"]["foot"][1]*f_n]
            if neutral_spec.get("head"):h=neutral_spec["head"];pts["head"]=[h[0]*f_n,h[1]*f_n,h[2]*f_n,h[3]*f_n]
            entries["neutral"]=finish(d,person,"neutral",pts,dict(file=neutral_spec["file"],crop=neutral_spec["crop"]),1.0)
            report.append((person,"neutral","field-regrid",entries["neutral"]["size"][1]))
        n_head=neutral_spec.get("head") if neutral_spec else None
        n_h=(bb(nim)[3]-bb(nim)[1]) if neutral_spec else None
        for pose,spec in poses.items():
            if pose=="neutral":continue
            try:im=crop_image(spec)
            except Exception as e:print("건너뜀",person,pose,e);continue
            b=bb(im);ph=b[3]-b[1]
            ratio=spec.get("stature_ratio")
            same_sheet=neutral_file==spec["file"] and f_n
            if same_sheet:
                f=f_n;ratio=round(ph*f/float(T),3)
            else:
                if ratio is None:
                    head=spec.get("head")
                    if head and n_head and n_h:
                        ratio=(ph/float(head[3]))/(n_h/float(n_head[3]))
                        ratio=max(.55,min(1.0,ratio))
                    else:ratio=1.0
                f=T*ratio/float(ph)
            pal=palette(im)
            d=regrid(im,f,pal)
            pts={k:[v[0]*f,v[1]*f] for k,v in spec.items() if k in ("foot","hook","seat","hand") and isinstance(v,list)}
            if isinstance(spec.get("anchor"),dict) and "foot" in spec["anchor"] and "foot" not in pts:
                pts["foot"]=[spec["anchor"]["foot"][0]*f,spec["anchor"]["foot"][1]*f]
            if isinstance(spec.get("anchors"),dict):
                for k,v in spec["anchors"].items():pts["anchor:"+k]=[v[0]*f,v[1]*f]
            if spec.get("head"):h=spec["head"];pts["head"]=[h[0]*f,h[1]*f,h[2]*f,h[3]*f]
            entries[pose]=finish(d,person,pose,pts,dict(file=spec["file"],crop=spec["crop"]),round(ratio,3))
            report.append((person,pose,"same-sheet" if same_sheet else "ratio",entries[pose]["size"][1]))
        if entries:table[person]=dict(target_dots=T,poses=entries)
    json.dump(dict(schema="room13-field-dot-v2/1",note="현장 인물 그림을 대화 도트판과 같은 도트 수로 다시 찍은 표. 좌표는 모두 도트(1배) 기준.",people=table),
        open(TABLE,"w"),ensure_ascii=False,indent=1)
    json.dump(report,open(Path(__file__).parent.parent/"field"/"build_report.json","w"),ensure_ascii=False,indent=0)
    print(len(table),"명",sum(len(v["poses"]) for v in table.values()),"장")

main()
