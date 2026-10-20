import asyncio,json,sys,os
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'existing-inn';OUT.mkdir(exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),ignore_default_args=['--mute-audio'],args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
  c=await b.new_context(viewport={'width':1280,'height':720});pg=await c.new_page();q=UIQA(pg,OUT);report={'checks':[]};errors=[];pg.on('pageerror',lambda e:errors.append(str(e)));pg.on('console',lambda m:(OUT/'console.txt').open('a').write(m.type+': '+m.text+'\n'))
  try:
   await pg.goto(os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/'),wait_until='domcontentloaded',timeout=180000)
   print('BOOT document ready',flush=True)
   await pg.wait_for_function("typeof renpy_exec==='function'",timeout=240000,polling=500)
   print('BOOT bridge ready',flush=True);await asyncio.sleep(12);await pg.mouse.click(1100,600);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
   await q.press('처음부터');await q.wait('say');await q.shot('01-existing-carriage')
   before=await q.py('import renpy;s=renpy.store;result=dict(ms14=s.ms14,music=renpy.audio.music.get_playing(),scene=s.r13_scene_key,place=s.place)')
   assert before['ms14'] is None and before['music'] and before['place']=='마차 안',before
   await q.advance();await q.wait('r13_hub');await q.shot('02-existing-gate-click-scene')
   gate=await q.py('import renpy;s=renpy.store;result=dict(ms14=s.ms14,music=renpy.audio.music.get_playing(),ambience=renpy.audio.music.get_playing(channel="ambience"),actors=[a["person"] for a in s.r13_stage_people(True)],location=s.room13["location"],evidence=s.room13["evidence"])')
   assert gate['ms14'] is None and gate['location']=='gate' and {'guard','karo','daram'}<=set(gate['actors']),gate
   assert gate['music']=='assets/bgm-snow.mp3' and gate['ambience']=='assets/amb-wind.mp3',gate
   report['checks'].append('Original scene music and ambience channels are active')
   await q.value(('person','guard'));await q.wait('r13_entry_topics');await q.shot('03-original-guard-questions')
   await q.press('제가 낸 신청서');await q.advance();await q.wait('r13_entry_topics')
   room=(await q.state())['room'];assert 'G3' in room['evidence'] and 'entry_corrected' not in room['flags'],room
   await q.press('자료 보여주기');await q.wait('r13_book');await q.shot('04-original-notebook');await q.press('그만두기');await q.advance();await q.wait('r13_entry_topics')
   assert (await q.state())['room']==room,'Cancel changed story state'
   await q.press('돌아가기');await q.wait('r13_hub')
   async def object_click(key):
    pos=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"]["gate"]['+repr(key)+']["rect"];result=[x+w/2-s.r13_world_offset(),y+h/2]')
    assert 0<pos[0]<1280,pos
    await q.input(*pos);await q.advance();await q.wait('r13_hub')
   await object_click('gate_documents');await q.shot('05-clicked-shelf-new-original')
   assert 'G1' in (await q.state())['room']['evidence']
   await object_click('rules');await q.shot('06-clicked-rules')
   assert 'G2' in (await q.state())['room']['evidence']
   await q.value(('person','guard'));await q.wait('r13_entry_topics')
   await q.press('자료 보여주기');await q.wait('r13_book')
   title=await q.py('import renpy;result=renpy.store.R13_RECORD_SHORT["G1"]')
   await q.press(title);await q.shot('07-new-evidence-existing-book');await q.press('돌목에게 보여주기');await q.advance();await q.wait('r13_hub')
   end=(await q.state())['room'];assert 'entry_corrected' in end['flags'],end
   await q.shot('08-existing-engine-after-presentation')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.value('inn');await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub')
   await q.value(('person','granny'));await q.advance()
   if 'r13_resident_approach' in (await q.state())['screens']:
    await q.press('편지를 받고 왔다고 인사한다');await q.advance()
   await q.wait('r13_topics')
   actual=await q.py('import renpy;result=renpy.store.r13_conversation_topic_lines("register")')
   assert actual[0][0]=='granny' and '다돌 씨죠?' in actual[0][1],actual
   await q.press('아내가 머물던 방을 묻는다');await q.wait('say');await q.shot('09-new-checkin-original-dialogue')
   await q.advance();await q.wait('r13_topics');assert 'lodging' in (await q.state())['room']['flags']
   await q.press('돌아가기');await q.advance();await q.wait('r13_hub')
   await q.press('지도 · 이동');await q.wait('r13_map');await q.press('여관 안');await q.value('room13');await q.press('이곳으로 이동');await q.advance();await q.wait('r13_hub');await q.shot('10-existing-room-with-delivered-bundle')
   async def room_click(key):
    for _ in range(6):
     pos=await q.py('import renpy;s=renpy.store;x,y,w,h=s.ROOM13["objects"]["room13"]['+repr(key)+']["rect"];result=[x+w/2-s.r13_world_offset(),y+h/2]')
     if 20<pos[0]<1260:break
     await q.input(38 if pos[0]<20 else 1244,270)
    assert 0<pos[0]<1280,pos
    await q.input(*pos);await asyncio.sleep(.8);await q.advance();await q.wait('r13_hub')
   before_room=(await q.state())['room'];assert 'M01' not in before_room['evidence'] and 'FAMILY_BUNDLE' not in before_room['evidence']
   await room_click('mother_note');await q.shot('11-note-clicked')
   note=await q.py('import renpy;s=renpy.store;result=dict(text=s.ROOM13["evidence"]["M01"]["establishes"],evidence=s.room13["evidence"],flags=s.room13["flags"])')
   assert '물건은 책상 아래에 두었어.' in note['text'] and 'mother_lamplighter_lead' in note['flags'],note
   await room_click('family_bundle');await q.shot('12-bundle-clicked')
   await room_click('family_bundle')
   bundle=await q.py('import renpy;s=renpy.store;result=dict(count=s.room13["evidence"].count("FAMILY_BUNDLE"),text=s.ROOM13["evidence"]["FAMILY_BUNDLE"]["establishes"],flags=s.room13["flags"])')
   assert bundle['count']==1 and 'under_desk_checked' in bundle['flags'] and '주소나 다른 봉투는 없다' in bundle['text'],bundle
   await q.press('기록');await q.wait('r13_records');await q.press('책상 아래 보따리');await q.shot('13-delivered-prop-in-existing-notebook');await q.press('닫기')
   report['inn_update']=dict(checkin=actual,note=note,bundle=bundle)
   report.update(status='passed',opening=before,gate=gate,final_location=(await q.state())['room']['location'],page_errors=errors,scope='Natural start and real clicks only; game-state probes are read-only except text speed preference')
  except Exception as e:
   report.update(status='failed',error=repr(e));print('ORIGINAL FAILURE',repr(e),flush=True)
   try:await pg.screenshot(path=str(OUT/'failure.png'),timeout=5000)
   except:pass
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']!='passed':raise SystemExit(1)
asyncio.run(main())
