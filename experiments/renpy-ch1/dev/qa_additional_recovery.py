"""추가 QA: 소스 안내를 참고한 실제 클릭 진행과 2일 아침 복구.

진행 상태/세이브 주입 없음. renpy_exec는 읽기와 대사 속도 설정에만 사용한다.
새 게임부터 2일 교환함 완료까지 진행한 뒤 취소, 복구, 재진행, 수동 저장을 비교한다.
"""
import asyncio, ast, json, os, re, traceback
from pathlib import Path
from playwright.async_api import async_playwright
from qa_play_review_proof import ProofQA
from qa_map_review import MapQA

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/work/daram-additional-qa/recovery'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')
PROOFS={}
for path in (ROOT/'game').glob('room13_v111*.rpy'):
 for match in re.finditer(r'call r13_v111_proof\(([^\n]+)\)',path.read_text()):
  try:args=ast.literal_eval('('+match.group(1)+',)')
  except (ValueError,SyntaxError):continue
  PROOFS[args[0]]=args[1]
DAY1={'V111:'+key for key in ('E01','E02','E03','E04','E05','E06','E30')}

class RecoveryQA(ProofQA):
 async def input(self,x,y):
  await self.p.mouse.click(x,y);await asyncio.sleep(.12)
 async def snapshot(self):
  return await self.py('import renpy;import copy;s=renpy.store;result=dict(room=copy.deepcopy(s.room13),mornings=copy.deepcopy(s.persistent.r13_mornings),goal=s.r13_v111_goal() if s.r13_v111_active() else s.r13_campaign_goal())')
 async def press(self,label):
  for _ in range(35):
   st=await self.state();bs=[b for b in st['buttons'] if label in b['text'] and b['rect'][3]>15]
   if bs:
    x,y,w,h=min(bs,key=lambda b:b['rect'][2]*b['rect'][3])['rect'];await self.input(x+w/2,y+h/2);return
   await asyncio.sleep(.15)
  raise AssertionError(('버튼 없음',label,st))
 async def object(self,key):
  st=await self.state()
  if any('주변 살피기' in b['text'] for b in st['buttons']):await self.press('주변 살피기')
  for attempt in range(15):
   pos=await self.py('import renpy;s=renpy.store;k='+repr(key)+';x,y,w,h=s.r13_object_target_rect(k,s.ROOM13["objects"][s.room13["location"]][k]);z=s.r13_field_zoom();result=[(x+w*.5-s.r13_world_offset())*z,(y+h*.5)*z]')
   if 35<pos[0]<1245 and 110<pos[1]<640:
    await self.input(*pos);return
   st=await self.state();arrow='‹' if pos[0]<35 else '›'
   if any(arrow in b['text'] for b in st['buttons']):await self.press(arrow);await asyncio.sleep(1.2)
   else:await asyncio.sleep(.8)
  raise AssertionError(('조사 대상 이동 실패',key))
 async def map_move(self,target):
  region='inn' if target in ('inn','room13','dining') else 'mountain' if target=='forest' else 'village'
  await self.press({'inn':'여관 안','mountain':'숲·산길','village':'마을'}[region])
  if region!='inn':
   focus=await self.py('import renpy;result=renpy.store.r13_cart_focus('+repr(region)+','+repr(target)+')')
   for _ in range(8):
    current=await self.py('import renpy;v=renpy.exports.get_widget("r13_map","r13_map_view");result=[v.xadjustment.value,v.yadjustment.value]')
    dx=max(-400,min(400,focus[0]-current[0]));dy=max(-170,min(170,focus[1]-current[1]))
    if abs(dx)+abs(dy)<35:break
    await self.p.mouse.move(650,350);await self.p.mouse.down();await self.p.mouse.move(650-dx,350-dy,steps=12);await self.p.mouse.up();await asyncio.sleep(.35)
  widget=('map_room_' if region=='inn' else 'map_name_')+target
  rect=await self.py('import renpy;w=renpy.exports.get_widget("r13_map",'+repr(widget)+');result=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if f.widget is w and f.x is not None),None)')
  assert rect,(widget,'지도 대상 없음');x,y,w,h=rect;await self.input(x+w/2,y+h/2);await self.press('이곳으로 이동')
 async def drive(self,stop,limit=1800):
  last=None;book_target=None
  for step in range(limit):
   st=await self.state();room=st['room'] or {};v=room.get('v111',{});gate=v.get('gate');sc=st['screens']
   if stop(st):return st
   state=(gate,tuple(sc),room.get('location'))
   if state!=last:print('진행',step,state,st.get('say','')[:60],flush=True);last=state
   if 'say' in sc:await self.input(810,610);continue
   if 'choice' in sc:
    rows=await self.py('import renpy;result=[i.caption for i in renpy.display.screen.get_screen("choice").scope["items"] if i.action is not None]')
    label=next((s for s in rows if '편지를 접는다' in s),rows[0]);await self.press(label);continue
   if 'r13_cinematic_view' in sc:await self.press('계속');continue
   if 'r13_arrival_card' in sc:await self.input(800,400);continue
   if 'r13_confirm' in sc:
    await self.press(await self.py('import renpy;result=renpy.display.screen.get_screen("r13_confirm").scope["yes"]'));continue
   if 'r13_crisis_proof' in sc:
    claim=await self.py('import renpy;result=renpy.store.v111_claim');correct=PROOFS[claim[5:]];selected=room.get('arguments',{}).get(claim,[])
    missing=['V111:'+k for k in correct if 'V111:'+k not in selected]
    if missing:book_target=missing[0];await self.press('자료 고르기')
    else:await self.press('선택한 근거 제출')
    continue
   if 'r13_book' in sc:
    if book_target:await self.pick(book_target);await self.press('에 추가');book_target=None
    else:await self.press('선택 마치기')
    continue
   binding=await self.py('import renpy;result=renpy.store.r13_v111_binding()')
   options=binding.get('options',[])
   if 'r13_map' in sc:
    target=next(o['move'] for o in options if o.get('move'));await self.map_move(target);continue
   if 'r13_topics' in sc:
    if gate=='gate_investigate' and not {'V111:E03','V111:E04'}<=set(room['evidence']):
     await self.press('돌아가기');continue
    person=await self.py('import renpy;result=renpy.display.screen.get_screen("r13_topics").scope["person"]')
    opts=[o for o in options if o.get('person')==person]
    preferred={'gate_investigate':5,'gate_choice':1,'registered_menu':1}.get(gate)
    option=next((o for o in opts if o.get('index')==preferred),opts[0] if opts else None)
    if option:
     if option.get('present'):book_target=option['present']
     await self.press(option['title'])
    else:await self.press('돌아가기')
    continue
   if 'r13_hub' in sc:
    if gate=='registered_menu' and not getattr(self,'checkpoint',False):
     self.checkpoint=True;await self.slot('저장',1);continue
    if not options:raise AssertionError(('진행 선택지 없음',gate,room))
    if gate=='gate_investigate':
     idx=0 if 'V111:E03' not in room['evidence'] else 1 if 'V111:E04' not in room['evidence'] else 5
     option=next(o for o in options if o.get('index')==idx)
    elif gate=='registered_menu':option=next(o for o in options if o.get('move'))
    else:option=options[0]
    if option.get('move'):await self.press('지도')
    elif option.get('person'):
     if any('사람 보기' in b['text'] for b in st['buttons']):await self.press('사람 보기')
     name=await self.py('import renpy;result=renpy.store.R13_NAMES['+repr(option['person'])+']');await self.press(name)
    elif option.get('object'):await self.object(option['object'])
    else:raise AssertionError(('지원하지 않는 진행',option))
    continue
   await asyncio.sleep(.15)
  raise AssertionError(('진행 제한 초과',st))
 async def morning(self,cancel=False):
  await self.input(1222,52);await self.press('다시 시작할 아침');await self.press('2일 아침부터')
  if cancel:
   await self.press('그만두기');await self.press('돌아가기')
  else:await self.press('돌아간다');await asyncio.sleep(2);await self.wait('r13_hub')
 async def slot(self,mode,number=2):
  await self.input(1222,52);await self.press('설정');await self.press(mode);await self.wait('save' if mode=='저장' else 'load');await self.press('1쪽 %d번'%number)
  await asyncio.sleep(.7)
  if 'confirm' in (await self.state())['screens']:await self.press('예')
  if mode=='저장':
   await self.press('돌아가기');await self.press('닫기')
  else:await asyncio.sleep(2)


def at_post(st):
 r=st['room'] or {};v=r.get('v111',{})
 return 'r13_hub' in st['screens'] and r.get('day')==2 and v.get('travel_to')=='post' and v.get('values',{}).get('arrival_note_sent') is True

def at_box(st):return 'r13_hub' in st['screens'] and (st['room'] or {}).get('v111',{}).get('gate')=='box_inspect'

async def main():
 OUT.mkdir(parents=True,exist_ok=True);report={'resume_actual_ui_save':bool(os.environ.get('RECOVERY_RESUME')),'scope':'소스 안내를 참고한 새 게임부터의 실제 클릭 재현. 진행/세이브 주입 없음. Chromium PC 모사.','checks':[],'page_errors':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch_persistent_context(str(OUT/'profile'),viewport={'width':1280,'height':720},executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page();q=RecoveryQA(page,OUT)
  page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await q.wait('main_menu')
   report['version']=(await q.info())['version'];await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
   if os.environ.get('RECOVERY_RESUME'):
    await q.press('불러오기');await q.press('1쪽 1번');await asyncio.sleep(.7)
    if 'confirm' in (await q.state())['screens']:await q.press('예')
    q.checkpoint=True
   else:await q.press('처음부터')
   await q.drive(at_post);await asyncio.sleep(1);report['before']=await q.snapshot();await q.shot('01-box-complete')
   await q.morning(cancel=True);after=await q.snapshot();assert after==report['before'],('취소 상태 변경',after,report['before']);report['checks'].append('확인 취소: room13 전체·아침기록·목표 보존')
   await q.morning();restored=await q.snapshot();r=restored['room'];v=r['v111'];values=v['values']
   assert (r['day'],r['period'],r['location'])==(2,0,'room13'),r
   assert set(r['evidence'])==DAY1,r['evidence'];assert not values.get('mother_box_checked_day2');assert not values.get('arrival_note_sent');assert v['travel_to']=='gate';assert values.get('elapsed_minutes',0)==0
   assert restored['goal']!=report['before']['goal'],('복귀 목표 미변경',restored['goal']);report['morning']=restored;report['checks'].append('2일 오전13호실·1일자료7개·교환함/쪽지/시간/이동목표 복구');await q.shot('02-morning-restored')
   await q.drive(at_box);await q.slot('저장');saved=await q.snapshot();report['manual_saved']=saved;await q.shot('03-manual-before-box')
   await q.drive(at_post);report['replayed']=await q.snapshot();assert len(report['replayed']['room']['evidence'])==len(set(report['replayed']['room']['evidence']));report['checks'].append('복귀 후 입구→초롱→교환함 조사·쪽지 전달 재진행, 자료 중복 없음')
   await q.morning();await q.slot('불러오기');loaded=await q.snapshot();assert loaded['room']==saved['room'],('수동저장복원 불일치',loaded,saved);assert loaded['goal']==saved['goal'];report['manual_loaded']=loaded;report['checks'].append('아침 복구 뒤 수동저장 불러오기: 교환함 조사 전 전체상태·목표 복원');await q.shot('04-manual-restored')
   assert not report['page_errors'];report['status']='passed'
  except Exception:
   report['status']='failed';report['error']=traceback.format_exc();await page.screenshot(path=str(OUT/'failure.png'));report['last_state']=await q.state();raise
  finally:
   (OUT/'recovery-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await browser.close()
if __name__=='__main__':asyncio.run(main())
