"""증거 서랍 시안(2026-10-24): 실제 14일 기록 화면 캡처 위에 왼쪽 목록만 다시 그린다.

소유자 지시 "증거가 너무 많아서 헷갈리는 문제 해결방안 제시" → 추천안 1부(사건별 서랍,
갱신은 쪽지로, 이름+날·곳 꼬리표). 화면 변경이라 게임에 넣기 전에 이미지로 먼저 보인다.
색은 캡처에서 뽑은 값이다. 새 부품은 기존 카드·칩 모양을 그대로 따른다.
사용: python3 dev/make_evidence_drawer_mockup.py 출력폴더
"""
import sys,os
from PIL import Image,ImageDraw,ImageFont

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT=os.path.join(ROOT,"docs/reviews/play-review-20261023/screens/desktop-normal-burnt-page.png")
EV=os.path.join(ROOT,"game/assets/evidence")
FONT=os.path.join(ROOT,"game/assets/Galmuri11.ttf")
BG=(45,30,22);CARD=(52,36,26);EDGE=(196,160,98);INK=(227,214,189);DIM=(190,170,140);RED=(114,28,34);GOLD=(240,198,106)

def f(n):return ImageFont.truetype(FONT,n)

def icon(key,size):
    p=os.path.join(EV,key+".webp")
    im=Image.open(p).convert("RGBA");im.thumbnail((size,size))
    return im

def card(d,base,x,y,key,name,tag,chosen=False,note=None,dot=False):
    w,h=250,82
    d.rounded_rectangle((x,y,x+w,y+h),8,fill=RED if chosen else CARD,outline=EDGE,width=2)
    ic=icon(key,56);base.alpha_composite(ic,(x+8,y+(h-ic.height)//2))
    d.text((x+72,y+18),name,font=f(20),fill=INK)
    d.text((x+72,y+48),tag,font=f(15),fill=GOLD if chosen else DIM)
    if dot:d.ellipse((x+50,y-5,x+60,y+5),fill=GOLD)
    if note:
        # 갱신 기록은 새 카드가 아니라 원래 카드 귀퉁이의 쪽지로 붙는다.
        nx,ny=x+w-58,y-8
        d.polygon([(nx,ny),(nx+54,ny),(nx+54,ny+22),(nx+6,ny+22)],fill=(236,222,190))
        d.text((nx+10,ny+3),note,font=f(13),fill=(80,50,30))

def chip(d,x,y,w,label,on):
    d.rounded_rectangle((x,y,x+w,y+36),8,fill=RED if on else BG,outline=EDGE,width=2)
    tw=d.textlength(label,font=f(17));d.text((x+(w-tw)/2,y+8),label,font=f(17),fill=INK)

def base_img():
    im=Image.open(SHOT).convert("RGBA")
    d=ImageDraw.Draw(im)
    d.rectangle((52,104,326,690),fill=BG)          # 왼쪽 목록 자리 비움
    d.rectangle((960,44,1170,90),fill=BG)          # 위쪽 거르기 칩 자리 비움
    return im,d

def chips(d,current):
    chip(d,858,48,96,"이번 사건",current=="now")
    chip(d,962,48,96,"지난 사건",current=="past")
    chip(d,1066,48,96,"사람별",current=="person")

def pager(d,text):
    d.rounded_rectangle((62,626,128,666),8,outline=EDGE,width=2);d.text((88,636),"‹",font=f(20),fill=INK)
    d.text((150,636),text,font=f(19),fill=INK)
    d.rounded_rectangle((246,626,312,666),8,outline=EDGE,width=2);d.text((272,636),"›",font=f(20),fill=INK)

def now_view():
    im,d=base_img();chips(d,"now")
    d.text((62,112),"이번 사건 · 14일  6개",font=f(19),fill=INK)
    rows=[("NW_NEOUL_LEDGER","너울의 장부","14일 · 회관",False,"쪽지 1"),
          ("NW_TABLET_A","제단 밑돌의 글자","14일 · 광장",False,None),
          ("NW_IRON_MARK","쇠의 공방 표식","14일 · 제단",False,None),
          ("NW_BURNT_PAGE","반쯤 탄 수첩 장","13일 밤 · 주방",True,None),
          ("NW_MADAM_DAY7","백 부인 장부","14일 · 창고",False,None)]
    for i,(k,n,t,c,note) in enumerate(rows):card(d,im,62,146+i*94,k,n,t,c,note,dot=(i in (3,4)))
    pager(d,"1 / 2")
    return im

def past_view():
    im,d=base_img();chips(d,"past")
    d.text((62,112),"지난 사건 · 10건  74개",font=f(19),fill=INK)
    cases=[("⑪ 담요의 새","13일",6,["NW_HALL_WINDOW","E13_ORDER","NW_TRANSFER_LIST"]),
           ("⑩ 학교의 국","12일",8,["NW_WHITE_BOWLS","E12_SEAL","E12_FRAGMENT"]),
           ("⑨ 네 가지 가설","11일",9,["NW_KEEPER_DATE","NW_SICK_BEDS","NW_STONE"]),
           ("⑧ 맡긴 기록","10일",7,["E27","E28","E10_PUMP"]),
           ("⑦ 13호의 밤","7~9일",12,["E08_ROOM","E09_PIN_OWNER","E08_TOOL"])]
    for i,(name,day,n,keys) in enumerate(cases):
        x,y=62,146+i*94
        chosen=i==0
        d.rounded_rectangle((x,y,x+250,y+82),8,fill=RED if chosen else CARD,outline=EDGE,width=2)
        for j,k in enumerate(keys):
            ic=icon(k,40);im.alpha_composite(ic,(x+8+j*22,y+40-ic.height//2+(j%2)*6))
        d.text((x+86,y+16),name,font=f(19),fill=INK)
        d.text((x+86,y+48),"%s · 자료 %d"%(day,n),font=f(15),fill=GOLD if chosen else DIM)
    pager(d,"1 / 2")
    # 오른쪽: 고른 사건의 자료를 한눈에. 누르면 지금처럼 상세가 열린다.
    d.rectangle((336,104,1250,690),fill=BG)
    d.text((370,116),"⑪ 담요의 새 · 13일",font=f(30),fill=INK)
    d.text((370,160),"회의가 끝난 사건의 자료입니다. 다른 회의에서도 낼 수 있습니다.",font=f(17),fill=DIM)
    items=[("NW_HALL_WINDOW","회관 창문","13일 · 회관"),("E13_ORDER","이송 명령 사본","13일 · 초소"),("NW_TRANSFER_LIST","이송 명단","13일 · 회관"),
           ("E13_HANDOVER","학교 인수 장부","12일 · 학교"),("PROP_D11_blank_name_tag_bundle","빈 이름표 묶음","11일 · 학교"),("E14_SUPPLY","온기 상자 인수","12일 · 학교")]
    for i,(k,n,t) in enumerate(items):
        card(d,im,370+(i%3)*280,206+(i//3)*110,k,n,t,note=("쪽지 1" if k=="E13_HANDOVER" else None))
    return im

def label(im,text):
    d=ImageDraw.Draw(im);d.rectangle((0,0,im.width,30),fill=(20,14,10));d.text((12,6),text,font=f(17),fill=(255,240,210))
    return im

def main(out):
    os.makedirs(out,exist_ok=True)
    before=Image.open(SHOT).convert("RGBA")
    a=now_view();b=past_view()
    a.convert("RGB").save(os.path.join(out,"02_이번사건.png"))
    b.convert("RGB").save(os.path.join(out,"03_지난사건.png"))
    sheet=Image.new("RGB",(1280*2+20,720*2+20),(20,14,10))
    for i,(im,t) in enumerate([(before,"지금: 자료 80개가 한 목록, 16쪽"),(a,"시안 A: 이번 사건만 먼저(꼬리표 날·곳, 갱신은 쪽지)"),
                               (b,"시안 B: 지난 사건은 사건별 묶음, 회의에서도 열 수 있음"),(None,None)]):
        if im is None:continue
        sheet.paste(label(im.copy(),t).convert("RGB"),((i%2)*1300,(i//2)*740))
    d=ImageDraw.Draw(sheet)
    notes=["바뀌는 것","· 회의가 끝나면 그 사건 자료가 「지난 사건」으로 넘어간다(이미 있는 기능을 지금 이야기에 넓힘)",
           "· 회의·대화의 자료 보여주기에서도 「지난 사건」을 열 수 있다 — 다시 쓰일 자료를 표시하지 않기 위해",
           "· 카드 아래 줄에 날·곳 꼬리표. 정정·결과 기록은 원래 카드의 쪽지로 붙어 목록에서 빠진다",
           "· 「사람별」: 그 사람이 나오는 자료만","바뀌지 않는 것","· 자료 내용·회의 정답·기회 수, 오른쪽 상세·나란히 놓기"]
    for i,t in enumerate(notes):d.text((1320,760+i*36),t,font=f(20 if not t.startswith("·") else 18),fill=(255,240,210))
    sheet.save(os.path.join(out,"01_비교.png"))

if __name__=="__main__":main(sys.argv[1])
