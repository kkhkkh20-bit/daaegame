from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from pathlib import Path
import numpy as np, random, json, hashlib
random.seed(1222)
O=Path(__file__).resolve().parent
B=Path('/home/claude/daaegame/experiments/renpy-ch1/game/assets/evidence')
S=4; N=384; L=N*S

def source(k):return Image.open(B/(k+'.webp')).convert('RGBA').resize((L,L),Image.Resampling.LANCZOS)
def blank():return Image.new('RGBA',(L,L))
def poly(points):
 m=Image.new('L',(L,L));ImageDraw.Draw(m).polygon([(int(x*S),int(y*S)) for x,y in points],fill=255);return m

def line(im,pts,col,w=1):ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in pts],fill=col,width=max(1,round(w*S)),joint='curve')
def ellipse(im,box,col,w=1):ImageDraw.Draw(im).ellipse(tuple(round(v*S) for v in box),outline=col,width=round(w*S))
def clipped(im,m):
 r=im.copy();r.putalpha(ImageChops.multiply(r.getchannel('A'),m));return r

def save(im,k):
 im=im.resize((N,N),Image.Resampling.LANCZOS)
 if k=='NW_PIKO_PAINTING_reveal':im.putalpha(Image.open(B/'NW_PIKO_PAINTING.webp').getchannel('A'))
 im.save(O/(k+'.webp'),'WEBP',lossless=True,exact=True)

def place(im,box,size,pos):
 p=im.crop(tuple(round(v*S) for v in box));p=p.resize(tuple(round(v*S) for v in size),Image.Resampling.LANCZOS);r=blank();r.alpha_composite(p,tuple(round(v*S) for v in pos));return r

# 회색 겉옷: 원본의 음영·먹선을 보존하고 색만 직물 회색으로 변경.
coat=source('E23');a=np.array(coat);lum=(a[:,:,0]*.299+a[:,:,1]*.587+a[:,:,2]*.114)
for c,f,off in [(0,1.08,12),(1,1.10,13),(2,1.11,15)]:a[:,:,c]=np.clip(lum*f+off,0,255)
coat=Image.fromarray(a)
# 두 줄 수선실은 분리 전 공통 원본에 그린다.
for x in [86,95]:
 for y in range(189,279,7):
  line(coat,[(x,y),(x+1.0,y+4)],(37,35,31,255),1.8)
  line(coat,[(x-.3,y),(x+.7,y+3.4)],(193,183,156,255),.8)
# 소매/왼쪽 아래 가장자리로 열린 결손. 비대칭 갈고리와 계단형 경계.
tear=[(0,226),(60,226),(70,220),(77,230),(85,225),(90,237),(105,232),(115,245),(105,256),(114,264),(100,273),(105,285),(87,289),(78,301),(0,330)]
m=poly(tear);piece=clipped(coat,m);body=clipped(coat,ImageOps.invert(m))
edge=tear[1:-1]
line(body,edge,(43,43,40,255),.9)
# 짧은 풀린 올: 양쪽에 동일한 직물색, 과도한 강조 없이.
for i in range(len(edge)-1):
 x,y=edge[i];x2,y2=edge[i+1]
 for t in [.2,.55,.8]:
  xx=x+(x2-x)*t; yy=y+(y2-y)*t
  line(body,[(xx+1,yy),(xx+3,yy-2)],(139,139,127,230),.45)
  line(piece,[(xx-1,yy),(xx-3,yy+2)],(139,139,127,230),.45)
save(body,'E23')
# 분리 조각은 같은 방향으로 확대 배치. 천 결은 원본 겉옷 그대로.
patch=place(piece,(32,215,120,307),(223,233),(80,76));save(patch,'E22')
coat.save(O/'검수_천_공통원본.png');m.resize((384,384),Image.Resampling.LANCZOS).save(O/'검수_천_분리마스크.png')

# 핀 수리 끝: 공통 구리선에 두 굴곡을 만들고 중간 구간을 실제 분리.
assembly=source('E08_CONTACT_ASSEMBLY')
# 원본 구리선의 입체 질감과 실제 굴곡을 그대로 사용한다.
wire=blank()
wsrc=source('E08_WOUND_WIRE').resize((190*S,163*S),Image.Resampling.LANCZOS)
wire.alpha_composite(wsrc,(152*S,120*S))
# 양단은 수리 끝에 남고, 두 굴곡이 있는 중앙 부분이 분리된다.
wm=poly([(211,198),(226,190),(307,208),(310,232),(279,245),(225,242),(207,221)])
frag=clipped(wire,wm);ends=clipped(wire,ImageOps.invert(wm))
assembly.alpha_composite(ends)
save(assembly,'E08_CONTACT_ASSEMBLY')
wirepiece=place(frag,(207,190,311,246),(281,151),(51,116));save(wirepiece,'E08_WOUND_WIRE')
whole=source('E08_CONTACT_ASSEMBLY');whole.alpha_composite(wire);whole.save(O/'검수_구리선_공통원본.png');wm.resize((384,384),Image.Resampling.LANCZOS).save(O/'검수_구리선_분리마스크.png')

# 준비 때 온전한 병은 원본을 기준으로 하며, 파손 그림은 동일 병 입구를 참조해 마감.
bottle=Image.open(O/'제작자료/봉인병_생성원본.png').convert('RGBA').resize((L,L),Image.Resampling.LANCZOS)
save(bottle,'E12_SEAL')
glass=Image.open(O/'제작자료/유리_생성원본.png').convert('RGBA')
# 원본 냄비 형태를 다시 그린 구간과 동일 생성 원본의 깨진 병목·파편을 나눠 여백 정렬.
scene=blank()
pot=glass.crop((15,387,804,999)).resize((239*S,186*S),Image.Resampling.LANCZOS)
scene.alpha_composite(pot,(4*S,112*S))
neck=glass.crop((807,414,1241,1001)).resize((139*S,188*S),Image.Resampling.LANCZOS)
scene.alpha_composite(neck,(242*S,81*S))
save(scene,'E12_FRAGMENT')

# 등 받침: 기존 표면에 압흔과 직선 긁힘만 더한다.
tray=source('E10');layer=blank();d=ImageDraw.Draw(layer)
# 테두리 위쪽 왼편의 둥근 눌림: 타원형 어두운 홈과 아래쪽 밝은 눌린 금속.
d.arc(tuple(int(v*S) for v in (102,112,143,131)),0,360,fill=(49,35,26,230),width=2*S)
d.arc(tuple(int(v*S) for v in (103,114,143,133)),5,170,fill=(184,149,102,210),width=S)
d.arc(tuple(int(v*S) for v in (107,115,138,127)),180,345,fill=(30,27,24,170),width=S)
# 안쪽 표면 한 줄의 새 긁힘. 원형과 위치·형태가 분명히 다르다.
line(layer,[(169,219),(258,183)],(43,34,27,245),2.3)
line(layer,[(170,220),(259,184)],(199,166,115,245),1.0)
line(layer,[(179,216),(252,187)],(223,192,143,235),.5)
tray.alpha_composite(layer);save(tray,'E10')

# 생성된 밑그림은 종이 내부에만 합성해 원본 실루엣·테두리 보존.
p=O/'제작자료/초상_생성원본.png'
gen=Image.open(p).convert('RGBA')
# 원본 종이의 사각 외곽에 맞게 생성 이미지의 종이 내부를 정렬.
gen=gen.crop((126,166,1156,1155)).resize((int(280*S),int(275*S)),Image.Resampling.LANCZOS)
paper=source('NW_PIKO_PAINTING');insert=blank();insert.alpha_composite(gen,(53*S,57*S))
mask=poly([(58,68),(160,59),(267,57),(319,63),(329,130),(332,235),(325,319),(246,329),(138,333),(58,325),(51,252),(52,149)]).filter(ImageFilter.GaussianBlur(5*S))
mask=ImageChops.multiply(mask,insert.getchannel('A'))
paper=Image.composite(insert,paper,mask);paper.putalpha(source('NW_PIKO_PAINTING').getchannel('A'));save(paper,'NW_PIKO_PAINTING_reveal')

# 글자 없는 나란히 검수본, 밝고 어두운 배경에서 알파 가장자리도 검사.
pairs=[('cloth','E22','E23'),('wire','E08_WOUND_WIRE','E08_CONTACT_ASSEMBLY'),('glass','E12_FRAGMENT','E12_SEAL')]
for name,left,right in pairs:
 canvas=Image.new('RGB',(800,408),(221,211,189))
 for k,x in [(left,8),(right,408)]:
  im=Image.open(O/(k+'.webp')).convert('RGBA');canvas.paste(im,(x,12),im)
 canvas.save(O/f'compare_{name}.png')
allnames=['NW_PIKO_PAINTING_reveal','E22','E23','E08_WOUND_WIRE','E08_CONTACT_ASSEMBLY','E12_FRAGMENT','E12_SEAL','E10']
sheet=Image.new('RGB',(1536,768),(218,207,183))
for i,k in enumerate(allnames):
 im=Image.open(O/(k+'.webp'));sheet.paste(im,((i%4)*384,(i//4)*384),im)
sheet.save(O/'검수_전체.png')
checks={}
for k in allnames:
 p=O/(k+'.webp');im=Image.open(p);checks[k]={'size':im.size,'mode':im.mode,'alpha_range':im.getchannel('A').getextrema(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(O/'검수_파일.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps(checks,ensure_ascii=False,indent=2))
