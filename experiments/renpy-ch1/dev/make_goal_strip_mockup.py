"""수첩 목표 띠 시안(2026-10-24): 기록 화면 아래쪽에 아빠의 최종 목표 세 칸을 둔다.

소유자 지시: "아빠의 최종 목표를 상기시켜야 해. 마을을 조사하고 엄마 되찾고 나가자" → "수첩안 빼고 별로".
실제 기록 화면 캡처(증거 서랍 적용본) 위에 띠만 그린다. 색은 캡처의 금색·버건디를 쓴다.
사용: python3 dev/make_goal_strip_mockup.py 출력폴더
"""
import os,sys
from PIL import Image,ImageDraw,ImageFont

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT=os.path.join(ROOT,"docs/reviews/evidence-drawer-20261024/applied/drawer-01-now-pc.png")
FONT=os.path.join(ROOT,"game/assets/Galmuri11.ttf")
GOLD=(214,178,108);INK=(236,224,200);DIM=(150,132,110);RED=(120,28,36);BG=(36,24,18)

def f(n):return ImageFont.truetype(FONT,n)

def pill(im,steps,current):
    # 탭 줄 오른쪽 빈자리(x530~735)에 지금 단계만 짧게. 세 점이 어디까지 왔는지 보인다.
    d=ImageDraw.Draw(im)
    x0,y0,x1,y1=528,38,738,74
    d.rounded_rectangle((x0,y0,x1,y1),8,fill=BG,outline=GOLD,width=1)
    d.text((x0+10,y0+9),"목표",font=f(15),fill=GOLD)
    for i in range(len(steps)):
        cx=x0+52+i*13;cy=y0+18
        fill=GOLD if i<current else (RED if i==current else None)
        d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=fill,outline=GOLD)
    d.text((x0+92,y0+9),steps[current],font=f(16),fill=INK)
    return im

def card(im,steps,current,note):
    # 목표 칸을 누르면 펼쳐지는 작은 판: 세 단계와 그날의 한 줄.
    im=pill(im,steps,current)
    d=ImageDraw.Draw(im)
    x0,y0,x1,y1=528,80,900,222
    d.rounded_rectangle((x0,y0,x1,y1),10,fill=BG,outline=GOLD,width=2)
    for i,label in enumerate(steps):
        y=y0+14+i*32
        done=i<current;now=i==current
        d.ellipse((x0+18,y+6,x0+30,y+18),fill=GOLD if done else (RED if now else None),outline=GOLD)
        d.text((x0+42,y+2),label+("  ← 지금" if now else ""),font=f(18),fill=INK if (done or now) else DIM)
    d.line((x0+16,y0+108,x1-16,y0+108),fill=(90,70,50))
    d.text((x0+18,y0+114),note,font=f(14),fill=DIM)
    return im

def main(out):
    os.makedirs(out,exist_ok=True)
    base=Image.open(SHOT).convert("RGB")
    A=["마을을 조사한다","엄마를 찾는다","셋이 나간다"];B=["마을을 조사한다","엄마를 지킨다","셋이 나간다"]
    # 캡처가 14일 상태라 14일 단계로 그린다. 11일 전에는 가운데 칸이 「엄마를 찾는다」.
    a=pill(base.copy(),B,2)
    b=card(base.copy(),B,2,"첫 길이 열려도, 이름판에 남은 이름은 못 탄다.")
    c=card(base.copy(),A,1,"(11일 전 예) 밤이가 강 쪽에서 엄마를 봤다고 했다.")
    for im,n in ((a,"목표_닫힘.png"),(b,"목표_펼침_14일.png"),(c,"목표_펼침_11일전예시.png")):im.save(os.path.join(out,n))
    sheet=Image.new("RGB",(base.width,base.height*3+24),(20,14,10))
    for i,im in enumerate((a,b,c)):sheet.paste(im,(0,i*(base.height+12)))
    sheet.save(os.path.join(out,"목표_비교.png"))

if __name__=="__main__":main(sys.argv[1])
