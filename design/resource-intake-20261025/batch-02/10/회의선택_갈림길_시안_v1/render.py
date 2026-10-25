from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path
import json, math, shutil
R=Path(__file__).resolve().parent; A=R/'references'; O=R/'previews';O.mkdir(exist_ok=True)
NAVY='#263B52'; RED='#B8483D'; INK='#354151'; MUTED='#756F66'; CREAM='#FFF8E9'; GOLD='#B98B51'
FONT=str(A/'Pretendard-Regular.otf')
def font(n):return ImageFont.truetype(FONT,n)
def txt(im,xy,s,n=24,c=INK,anchor=None):ImageDraw.Draw(im).text(xy,s,font=font(n),fill=c,anchor=anchor)
def paste(im,f,xy,size=None):
 a=Image.open(f).convert('RGBA') if isinstance(f,(str,Path)) else f.copy().convert('RGBA')
 if size:a=a.resize(size,Image.Resampling.LANCZOS)
 im.alpha_composite(a,xy)
def bg(name='room13-pixel-panorama-square-evening.webp'):
 a=Image.open(A/name).convert('RGBA');h=720;w=round(a.width*h/a.height);a=a.resize((w,h));a=a.crop(((w-1280)//2,0,(w+1280)//2,720));return a

def chip(im,xy,s,color=RED,n=18):
 d=ImageDraw.Draw(im);w=math.ceil(d.textlength(s,font=font(n)))+26;x,y=xy;d.rounded_rectangle((x,y,x+w,y+32),radius=9,fill=color);txt(im,(x+13,y+6),s,n,'#FFFFFF')
def btn(im,x,y,w,s,primary=False,n=26):
 f=R/'assets'/('primary_basic.png' if primary else 'standard_basic.png')
 h=round(w*52/160);paste(im,f,(x,y),(w,h));txt(im,(x+w/2,y+h/2-2),s,n,CREAM if primary else NAVY,'mm')
def label(im,s):
 ImageDraw.Draw(im).rounded_rectangle((26,17,578,49),radius=8,fill='#203247ED');txt(im,(40,23),s,18,'#FFFFFF')
def retry(mobile=False):
 im=bg();im=Image.alpha_composite(im,Image.new('RGBA',im.size,(15,26,40,125)))
 paste(im,A/'b_opt_panel.png',(138,86),(1000,557))
 paste(im,A/'b_opt_title_tape.png',(240,120),(182,76));txt(im,(331,156),'회의를 마치며',23,NAVY,'mm')
 paste(im,A/'b_opt_sticker_corner.png',(953,117),(120,120))
 txt(im,(640,265),'다 있었다.',36,NAVY,'mm');txt(im,(640,315),'그런데 이어 붙이지 못했다.',36,NAVY,'mm')
 # 원본 버튼 비율 보존, 긴 문구에 필요한 너비를 같은 배율로 확보한다.
 btn(im,218,380,410,'결과를 받아들인다',True,28 if mobile else 26)
 btn(im,652,380,410,'회의를 처음부터 다시',False,28 if mobile else 26)
 txt(im,(423,507),'이 결과로 이야기를 이어갑니다.',22,MUTED,'mm')
 txt(im,(857,507),'같은 회의의 첫머리로 돌아갑니다.',22,MUTED,'mm')
 label(im,'06 · 화면 시안 / 실제 플레이 캡처 아님')
 txt(im,(640,675),'기본 강조는 ‘결과를 받아들인다’ · 자동 재시작 없음',22,'#FFF7E6','mm')
 if mobile:
  im=im.resize((960,540),Image.Resampling.LANCZOS);im.save(O/'06_회의선택_휴대폰가로_960x540.png')
 else:im.save(O/'06_회의선택_PC_1280x720.png')

def dashed(d,box,col='#AB9B81'):
 x,y,x2,y2=box
 for xx in range(x,x2,10):d.line((xx,y,min(xx+5,x2),y),fill=col,width=1);d.line((xx,y2,min(xx+5,x2),y2),fill=col,width=1)
 for yy in range(y,y2,10):d.line((x,yy,x,min(yy+5,y2)),fill=col,width=1);d.line((x2,yy,x2,min(yy+5,y2)),fill=col,width=1)
def lock(im,x,y):
 d=ImageDraw.Draw(im);d.arc((x+5,y,x+17,y+18),180,360,fill=NAVY,width=2);d.rounded_rectangle((x+1,y+9,x+21,y+25),radius=3,fill=NAVY);d.ellipse((x+10,y+14,x+12,y+17),fill=CREAM)
def card(im,x,y,result,seen,marked,scene):
 d=ImageDraw.Draw(im);d.rounded_rectangle((x,y,x+175,y+116),radius=9,fill='#FFFCF3',outline=GOLD,width=2)
 a=bg(scene).resize((165,93));a=a.crop((0,10,165,82));
 if seen:a=ImageEnhance.Color(a).enhance(.35)
 paste(im,a,(x+5,y+5));txt(im,(x+10,y+88),result,20,NAVY)
 txt(im,(x+165,y+91),'본 결과' if seen else '이번 판',15,MUTED,'ra')
 if marked:
  d.ellipse((x+145,y+7,x+169,y+31),fill=RED,outline=CREAM,width=2);d.polygon([(x+157,y+12),(x+159,y+17),(x+164,y+19),(x+159,y+21),(x+157,y+26),(x+155,y+21),(x+150,y+19),(x+155,y+17)],fill=CREAM)
def fork(concept='A',meeting='fire',unseen=False):
 im=bg();im=Image.alpha_composite(im,Image.new('RGBA',im.size,(15,26,40,130)));paste(im,A/'b_opt_panel.png',(0,0),(1280,720));d=ImageDraw.Draw(im)
 txt(im,(115,69),'이야기의 갈림길',34,NAVY);txt(im,(115,111),'기록 / 지나온 이야기',18,MUTED)
 chip(im,(435,71),('가 · 개수만 / 추천' if concept=='A' else '나 · 이미 본 대승리만 표식'))
 txt(im,(1190,81),'시안 · 샘플 기록',20,RED,'ra');paste(im,R/'assets/close_normal.png',(1198,60),(40,40))
 d.line((85,149,1210,149),fill='#C6B394',width=1)
 d.line((115,174,142,174),fill=RED,width=3);txt(im,(153,162),'이번 회차',18)
 dashed(d,(255,173,285,174));txt(im,(297,162),'다른 회차에서 본 결과',18)
 lock(im,529,160);txt(im,(560,162),'안 본 결과는 개수만',18)
 d.ellipse((800,159,827,186),outline=GOLD,width=2);txt(im,(814,173),'?',19,NAVY,'mm');txt(im,(838,162),'운명이 갈린 곳',18)
 if meeting=='fire':cols=[('7일째','불 회의'),('7일째 밤','13호'),('10일째 오후','13호실 회의'),('10일째 오후','기록 회의'),('11일째','가설 회의'),('11일째 밤','아랫길')];focus=0;scene='room13-pixel-panorama-woodshed-fire.webp'
 else:cols=[('11일째','가설 회의'),('11일째 밤','아랫길'),('12일째 낮','학교 배식'),('12일째','수프 회의'),('13일째','담요 회의'),('13일째','피코 회의')];focus=3;scene='room13-pixel-wide-dining-afternoon.webp'
 for i,(day,title) in enumerate(cols):
  x=110+182*i;txt(im,(x+87,207),day,17,MUTED,'mm');txt(im,(x+87,238),title,23,NAVY,'mm')
  if i<5:d.line((x+175,318,x+182,318),fill='#BCA989',width=2)
  if i!=focus:
   dashed(d,(x,264,x+175,380),'#CEBEA5');txt(im,(x+87,309),'기존 기록 영역',18,'#968A79','mm');txt(im,(x+87,338),'시안에서 생략',16,'#968A79','mm')
  else:
   card(im,x,264,'짐',False,False,scene)
   d.ellipse((x+142,273,x+168,299),fill=NAVY,outline='#D9BC7B',width=2);txt(im,(x+155,286),'?',19,CREAM,'mm')
   y=396
   if not unseen:card(im,x,y,'대승리',True,concept=='B',scene);y+=132
   d.rounded_rectangle((x,y,x+175,y+56),radius=8,fill='#EFE4CF',outline='#C3B192',width=1);lock(im,x+14,y+14);txt(im,(x+45,y+18),'다른 결과 '+('3' if unseen else '2'),20,NAVY)
 # 실제 기록과 분리한 시안 안내를 하단 종이에 명시한다.
 d.line((85,605,1210,605),fill='#C6B394',width=1)
 txt(im,(335,535),'검토용 샘플 · 실제 플레이어 기록이 아닙니다.',20,RED)
 txt(im,(335,567),('미확인 예시: 이름·그림·특별 표식 없이 숫자만 표시.' if unseen else '확인한 결과 예시: ‘짐’과 ‘대승리’를 본 경우. 다른 결과는 숫자만.'),17,MUTED)
 btn(im,1055,600,160,'닫기',False,20)
 name=f'07_{concept}_{"7일불" if meeting=="fire" else "12일수프"}_{"아직안봄" if unseen else "본뒤"}_PC.png';im.save(O/name)
 return im
retry();retry(True)
for c in ['A','B']:
 fork(c,'fire');fork(c,'soup')
fork('A','fire',True)
# 표식 공개 전/후를 한눈에 대조하는 검토 보드. 시안 이미지 자체를 사용한다.
board=Image.new('RGB',(1600,1100),'#E8E1D3');txt(board,(52,32),'갈림길 대승리 · 두 안 비교',36,NAVY);txt(board,(52,84),'실제 6열 구조를 유지한 디자인 시안 / 숫자와 기록은 검토용 샘플',23,MUTED)
for i,c in enumerate(['A','B']):
 x=40+i*780;txt(board,(x,143),'가 · 개수만 추가 (추천)' if c=='A' else '나 · 본 대승리에만 작은 표식',29,NAVY)
 a=Image.open(O/f'07_{c}_7일불_본뒤_PC.png').resize((760,428));board.paste(a,(x,193))
 txt(board,(x,649),'7일 불 회의 확대 · 이미 본 결과 예시',23,NAVY)
 a=Image.open(O/f'07_{c}_7일불_본뒤_PC.png').crop((100,196,295,592)).resize((195,396));board.paste(a,(x+20,694))
 txt(board,(x+245,736),'안 본 결과: 개수만',24,NAVY)
 txt(board,(x+245,784),'본 대승리: 일반 결과와 동일' if c=='A' else '본 대승리: 우상단 작은 표식',23,RED)
 txt(board,(x+245,840),'조건·방법·생사 정보 없음',22,MUTED)
 txt(board,(x+245,891),'12일 수프 회의에도 같은 규칙',22,MUTED)
 txt(board,(x+245,951),'아직 안 봤다면 두 안 모두',22,MUTED);txt(board,(x+245,985),'이름과 특별 표식을 숨깁니다.',22,MUTED)
board.save(O/'07_갈림길_두안_비교.png')
print('\n'.join(str(p) for p in O.iterdir()))
