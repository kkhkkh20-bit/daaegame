from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,zipfile
p=Path(__file__).parent
names=['reception','dining','kitchen','corridor','room13','temporary_guestroom','hidden_passage']
for n in names:
 im=Image.open(p/'originals'/f'{n}.png').convert('RGBA'); im.thumbnail((448,448),Image.Resampling.LANCZOS)
 out=Image.new('RGBA',(512,512)); out.alpha_composite(im,((512-im.width)//2,(512-im.height)//2)); out.save(p/'assets'/f'room_{n}_512.png')
base=Image.open(p/'originals/base.png').convert('RGB').resize((1136,570),Image.Resampling.LANCZOS); base.save(p/'assets/map_inn_base_1136x570.png')
frame=Image.open('/workspace/shared/restore/map/delivery/assets/notebook_frame_1280x720.png').convert('RGBA'); frame.save(p/'assets/notebook_frame_1280x720.png')
coords=[('corridor',95,68,280,2),('room13',409,56,290,2),('temporary_guestroom',770,56,290,2),('reception',95,300,270,1),('dining',430,300,270,1),('kitchen',775,300,270,1),('hidden_passage',652,103,160,2)]
items=[]
for n,x,y,s,f in coords:
 items.append(dict(id=n,file=f'assets/room_{n}_512.png',x=x,y=y,width=s,height=s,floor=f,anchor={'type':'bottom_center','x':x+s/2,'y':y+s},label={'x':x+s/2,'y':min(y+s-12,536)},default_visible=n!='hidden_passage',z_index=5 if n=='hidden_passage' else 10))
meta={'status':'시안·미적용 / 연결 좌표 검증 전','coordinate_space':'1136x570 map-local, top-left origin; notebook offset x88 y58','not_story_geometry':True,'connections':None,'visibility_note':'숨은 통로는 별도 레이어. 개발자가 기존 이야기 공개 조건과 연결할 때만 표시. 새 플래그, 자동 공개, 이동·문·증거 판정은 정의하지 않음.','items':items}
(p/'placement_proposal.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',24)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',17)
labels={'corridor':'복도','room13':'13호실','temporary_guestroom':'임시 객실','reception':'접수대','dining':'식당','kitchen':'주방','hidden_passage':'숨은 통로'}
for spoiler in [False,True]:
 canvas=base.convert('RGBA')
 for item in sorted(items,key=lambda t:t['z_index']):
  if not item['default_visible'] and not spoiler: continue
  im=Image.open(p/item['file']).resize((item['width'],item['height']),Image.Resampling.LANCZOS)
  canvas.alpha_composite(im,(item['x'],item['y']))
 d=ImageDraw.Draw(canvas)
 for it in items:
  if not it['default_visible'] and not spoiler:continue
  x,y=it['label']['x'],it['label']['y']; txt=labels[it['id']]; box=d.textbbox((0,0),txt,font=small); w=box[2]
  d.rounded_rectangle((x-w/2-8,y-4,x+w/2+8,y+24),radius=8,fill='#fff6df',outline='#6e4835');d.text((x,y),txt,font=small,anchor='mt',fill='#533528')
 out=Image.new('RGBA',(1280,720),'#e3d4bc');out.alpha_composite(canvas,(88,58));out.alpha_composite(frame)
 d=ImageDraw.Draw(out);d.rounded_rectangle((185,646,1100,696),radius=12,fill='#fff6df',outline='#6e4835');d.text((642,668),'시안·미적용 / 연결 좌표 검증 전'+('  ·  스포일러 공개 검토용' if spoiler else '  ·  기본 상태'),font=font,anchor='mm',fill='#533528')
 out.convert('RGB').save(p/'previews'/('inn_spoiler_visible_PROPOSAL.png' if spoiler else 'inn_default_PROPOSAL.png'))
# QA contact sheet: transparent artwork composited on neutral gray only for inspection.
sheet=Image.new('RGB',(1024,560),'#dedbd5');d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=Image.open(p/'assets'/f'room_{n}_512.png').resize((230,230));x=(i%4)*256;y=(i//4)*280;sheet.paste(im,(x,y),im);d.text((x+12,y+235),labels[n],font=small,fill='#493528')
sheet.save(p/'previews/room_contact_sheet_SPOILERS.png')
manifest=[]
for file in sorted((p/'assets').glob('*.png')):
 im=Image.open(file); a=im.getchannel('A') if im.mode=='RGBA' else None
 manifest.append({'file':str(file.relative_to(p)),'width':im.width,'height':im.height,'mode':im.mode,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'alpha_extrema':a.getextrema() if a else None,'alpha_bbox':a.getbbox() if a else None,'transparent_pixels':a.histogram()[0] if a else 0})
(p/'manifest.json').write_text(json.dumps(manifest,indent=2))
(p/'README_KO.txt').write_text('여관 안 지도 B 추가 에셋\n시안·미적용 / 연결 좌표 검증 전\n\n1136×570 불투명 빈 단면 바탕, 512×512 투명 방 스티커 6개와 별도 숨은 통로 1개. 스티커 유효 그림은 최대 448×448 안에 들어가고 원본 RGBA를 보존했습니다. 기존 수첩 틀은 변경 없이 복사했습니다.\n\n기본 미리보기에는 숨은 통로를 합성하지 않았습니다. SPOILER 파일은 검토 전용입니다. 실제 공개는 개발자가 기존 이야기 조건에 연결해야 하며 새 플래그나 자동 공개를 제안하지 않습니다.\n\n좌표는 미술 배치 제안입니다. 층 구분 외 실제 방 인접·이동 연결·문·밀실·증거 판정은 검증하거나 정의하지 않았습니다. 13호실 그림은 지도용 아이콘이며 기존 실내 화면을 대체하지 않습니다.\n\nPNG에 글자는 없습니다. 미리보기 라벨만 별도 합성했습니다. 게임 소스는 수정하지 않았습니다.\n\n생성: built-in imagegen. 원본은 originals/에 별도 보존. 모든 방은 개별 호출. 실제 알파 채널은 manifest.json에 검증 기록.\n')
