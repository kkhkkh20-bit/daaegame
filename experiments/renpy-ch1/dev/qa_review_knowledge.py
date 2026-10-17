import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from webqa import UIQA
import os
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'review01916';OUT.mkdir(parents=True,exist_ok=True)
class ReviewQA(UIQA):
 async def py(self,code):
  return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)

async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720})
  q=ReviewQA(page,OUT)
  await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
  transport=await (await page.request.get(page.url+'game-transport.json')).json()
  (OUT/'transport.json').write_text(json.dumps(transport,ensure_ascii=False,indent=2))
  await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000)
  await q.wait('main_menu');await q.shot('01-title')
  print('VERSION',await q.py('import renpy;result=renpy.store.config.version'),flush=True)
  await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
  await q.press('처음부터');await asyncio.sleep(2)
  if any('씬 건너뛰기' in v['text'] for v in (await q.state())['buttons']):await q.press('씬 건너뛰기')
  await q.advance();await q.wait('r13_hub');await q.shot('02-natural-start')
  result=await q.py('''import renpy,copy
s=renpy.store
original=copy.deepcopy(s.room13)
rows=[]
try:
 for key in ('M01','J04','J05'):
  for day in (1,2,3):
   n=s.r13_new();n.update(life_poc=True,day=day,period=1,location='square',case_state='pending',evidence=['E01',key]);s.room13=n
   lines=s.r13_present('resident_lamplighter',key)
   k=s.r13_mother_knowledge()
   assert k['promised'] and k['named'] and k['recognized']==(key=='M01'),k
   assert 'E18' not in s.room13['evidence']
   assert '봉투' in str(s.r13_intro_direction_lines())
   assert len([v for v in s.r13_calendar_promises() if '초롱' in v])==1
   before=copy.deepcopy(s.room13)
   notes=s.r13_first_mystery_notes();s.r13_calendar_promises();s.r13_mother_knowledge()
   assert s.room13==before
   s.room13['day']=3
   opening=s.r13_conversation_opening('resident_lamplighter',False)
   assert '다시 오셨군요' in str(opening)
   assert 'topic:lamplighter_warning' in s.room13['flags']
   rows.append(dict(key=key,day=day,lines=lines,notes=notes,opening=opening))
 for key in ('J04','J05'):
  n=s.r13_new();n.update(life_poc=True,day=2,evidence=['M01',key],flags=['mother_lamplighter_lead']);s.room13=n
  assert s.r13_mother_note_row() is None
  notes=s.r13_first_mystery_notes();direction=s.r13_intro_direction_lines()
  assert '봉투' in str(notes) and '봉투' in str(direction)
  rows.append(dict(key=key,notes=notes,direction=direction))
 for key in ('L02','L03','L04','L05','L06'):
  n=s.r13_new();n.update(life_poc=True,day=3,evidence=[key]);s.room13=n
  lines=s.r13_present('resident_seori',key)
  assert len(lines)==2 and s.room13['evidence']==[key]
  rows.append(dict(key=key,lines=lines))
 n=s.r13_new();n.update(life_poc=True,day=3,flags=['lt_dawn']);s.room13=n
 lines=s.r13_conversation_topic_lines('ep1:tok_lamps');assert '내일' not in str(lines)
 rows.append(dict(key='post-theft-tok',lines=lines))
 n=s.r13_new();n.update(life_poc=True,flags=['lodging_cheap']);s.room13=n
 before=copy.deepcopy(s.room13);s.r13_cheap_room_refund();assert s.room13==before
finally:s.room13=original
result=dict(kind='injected-runtime-fixtures-restored',rows=rows)
''')
  (OUT/'runtime-fixtures.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
  print('RUNTIME FIXTURES',len(result['rows']),flush=True)
  # Explicit fixture: enter the normal field UI with an owned memo; all subsequent
  # actions are real clicks. This is not a claim of a naturally played full run.
  await q.py("import renpy;s=renpy.store;s.r13_edit(day=1,period=1,location='square',life_poc=True);s.r13_flag('entry_corrected','lodging','ev_a_done','ep1_patrol_seen');s.r13_grant(['M01'],'QA owned memo');result=True")
  await q.py("import renpy\ndef jump_field(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide('qa_review_jump'),renpy.store.Jump('r13_roam')])\nrenpy.display.screen.define_screen('qa_review_jump',jump_field,zorder='200');renpy.exports.show_screen('qa_review_jump');renpy.exports.restart_interaction();result=True")
  await asyncio.sleep(3);await q.advance();await q.wait('r13_hub');print('FIELD', (await q.state())['screens'],flush=True)
  for _ in range(2):
   await q.press('초롱');await q.advance()
   if 'r13_resident_approach' in (await q.state())['screens']:break
  await q.wait('r13_resident_approach');await q.press('등 점검이');await q.advance();await q.wait('r13_topics')
  await q.press('보여주기');await q.wait('r13_book');await q.press('엄마의 메모');await q.press('초롱에게 보여주기')
  # The first line is the protagonist's introduction; advance to the NPC's reply.
  for _ in range(8):
   st=await q.state()
   if '봉투를 맡아' in st['say']:break
   await q.input(810,610)
  assert '모레' in st['say'] and '봉투' in st['say'],st
  await q.shot('03-memo-promise-dialogue');await q.advance()
  k=await q.py('import renpy;s=renpy.store;result=dict(knowledge=s.r13_mother_knowledge(),notes=s.r13_first_mystery_notes(),calendar=s.r13_calendar_promises())')
  assert k['knowledge']['promised'] and k['knowledge']['recognized'] and any('초롱' in v for v in k['calendar'])
  (OUT/'ui-result.json').write_text(json.dumps(k,ensure_ascii=False,indent=2))
  await q.shot('04-after-presentation');print('PASS: natural boot; 17 isolated runtime fixtures; owned memo shown with real UI clicks; promise/calendar/notebook agree',flush=True)
  await b.close()
asyncio.run(main())
