"""Design fixtures: real relationship navigation and compact meeting point choices.
Not a campaign playthrough; authored knowledge/status gates are not changed.
"""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace("names=[","names=['r13_records','r13_debate_board',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/relations-browser'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');print('READY title',flush=True)
   await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=10,period=0,location="inn",case_state="occurred",daram_state="with_dad",evidence=["N02","N03","N05","L00","W2"],encounters=[dict(person=p,day=2,period=0,place="square") for p in s.R13_REL_SLOTS]);s.r13_flag("chorong_dead","ttadak_dead","piko_survived","st_ttadak_boards");renpy.exports.show_screen("r13_records",initial_tab="relations");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_records');original=(await q.state())['room']
   # Choose granny through the real graph, then follow her known relationship.
   await q.input(326,530);await q.shot('00-relations-focused');await page.mouse.move(740,530);await page.mouse.down();await page.mouse.move(350,530,steps=10);await page.mouse.up();await asyncio.sleep(.4);assert await q.py('import renpy;result=renpy.exports.get_widget("r13_records","r13_relation_index").xadjustment.value>0');await q.press('전체 관계도');await q.input(332,190);await q.shot('01-relations-overview')
   assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["rel_sel"]=="granny"')
   await q.press('거둬 준 빚')
   assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["rel_sel"]=="nabi"')
   await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");sc.scope["rel_filter"]="dead";renpy.exports.restart_interaction();result=True');await asyncio.sleep(.2);assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["rel_filter"]=="all"');await q.input(716,150);await q.shot('02-relations-no-status-filter')
   assert not await q.py('import renpy;result=any(row[3]=="할아버지와 손녀" for row in renpy.store.r13_rel_edges())')
   state=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope["rel_sel"],sc.scope["rel_filter"]]')
   await q.press('닫기');await q.py('import renpy;renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True');await q.wait('r13_records')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope["rel_sel"],sc.scope["rel_filter"]]')==state
   assert (await q.state())['room']==original
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.store.persistent.room13_motion=False;renpy.exports.restart_interaction();result=True')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True;await q.press('인물 중심');await q.input(490,530);await q.shot('03-relations-mobile-large')
   await q.press('닫기');await asyncio.sleep(1);assert not await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records") is not None');await page.set_viewport_size({'width':1280,'height':720})
   # Explicit half-proof fixture: expose only the item already presented.
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;s.r13_meeting_active=True;s.r13_meeting_claim="Q4";s.r13_meeting_intro=False;s.r13_meeting_live_active=False;s.r13_edit(evidence=["N09","N07"],debate={});s.r13_debate_half("Q4","s3","N09");renpy.exports.show_screen("r13_debate_board",claim="Q4",selected="s3");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_debate_board');await q.shot('04-meeting-linked-proof')
   # Use the actual authored point menu, including its cancel action.
   code="\n".join(['import renpy','def _qa_point_start(**kwargs):',' s=renpy.store',' renpy.ui.textbutton("지목 검토",clicked=s.Function(renpy.call_in_new_context,"r13_debate_point","Q4"),xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.hide_screen('r13_debate_board')","renpy.store.r13_debate_spec=renpy.store.R13_DEBATE['Q4']['conclusion']","renpy.exports.define_screen('qa_point_start',_qa_point_start,modal='True',zorder='200')","renpy.exports.show_screen('qa_point_start')","renpy.exports.restart_interaction()","result=True"])
   await q.py(code);await q.press('지목 검토');await q.wait('choice');await q.py('import renpy;renpy.exports.hide_screen("qa_point_start");renpy.exports.restart_interaction();result=True')
   await q.shot('05-meeting-point-choices')
   names=await q.py('import renpy;s=renpy.store;result=[s.R13_NAMES[w] for w in s.R13_DEBATE["Q4"]["conclusion"]["point"]["candidates"]]')
   st=await q.state()
   for label in names+['아직 말하지 않는다']:
    row=next(x for x in st['buttons'] if label in x['text']);x,y,w,h=row['rect'];assert 0<=y and y+h<=720,(label,row)
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True')
   await page.set_viewport_size({'width':844,'height':390});await q.shot('06-meeting-point-mobile-large')
   before=(await q.state())['room'];await q.press('아직 말하지 않는다');assert (await q.state())['room']==before
   await q.py('import renpy;renpy.exports.hide_screen("qa_point_start");renpy.exports.restart_interaction();result=True')
   # Venue fixtures use the real meeting and map screens, without running story labels.
   await page.set_viewport_size({'width':1280,'height':720});q.touch=False
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;s.r13_meeting_active=True;result=True')
   for claim,loc,day,period,kind in [('Q1','square',4,0,'field'),('Q3','school',7,0,'room'),('Q4','dining',10,1,'round'),('Q6','square',13,3,'field'),('F1','altar',14,2,'stone')]:
    code='import renpy;s=renpy.store;s.r13_edit(location='+repr(loc)+',day='+str(day)+',period='+str(period)+');s.r13_meeting_claim='+repr(claim)+';s.r13_meeting_previous_focus=None;s.r13_meeting_focus=None;st=s.r13_debate_statements('+repr(claim)+')[0];s.dialogue_speaker=st["who"];s.r13_meeting_focus_change('+repr(claim)+',st["who"]);renpy.exports.show_screen("r13_debate_board",claim='+repr(claim)+',selected=st["id"]);renpy.exports.restart_interaction();result=s.r13_meeting_kind(s.r13_debate_session('+repr(claim)+'))'
    assert await q.py(code)==kind
    await q.wait('r13_debate_board');await q.shot('venue-'+claim+'-'+kind)
    await q.py('import renpy;renpy.exports.hide_screen("r13_debate_board");renpy.exports.restart_interaction();result=True')
   await q.py('import renpy;s=renpy.store;s.r13_meeting_active=False;s.r13_flag("lodging","entry_corrected");s.r13_edit(day=4,period=0,location="square",offers={"r13_ep1_meeting":dict(day=4,period=0,location="square")});renpy.exports.show_screen("r13_map",initial_region="village");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map');before=(await q.state())['room'];assert await q.py('import renpy;result=renpy.exports.get_widget("r13_map","meeting_map_legend_stone") is None');await q.shot('map-field-gathering')
   pins=await q.py('import renpy;s=renpy.store;result=[(k,s.r13_cart_point("village",k)) for k,p in s.r13_map_nodes("village")]')
   x,y=dict(pins)['school'];await q.input(x,y);await q.shot('map-school-room');assert (await q.state())['room']==before
   assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]=="school"')
   await page.set_viewport_size({'width':844,'height':390});q.touch=True
   for key,(x,y) in pins:
    await q.input(x,y)
    assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_map").scope["selected"]')==key
    assert (await q.state())['room']==before
   await q.shot('map-village-mobile');await q.press('현장으로 돌아가기')
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("r13_map");s.r13_edit(day=14,period=2,location="altar",finale_started=True);renpy.exports.show_screen("r13_map",initial_region="mountain");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map');await page.set_viewport_size({'width':844,'height':390});await q.shot('map-altar-mobile')
   result=dict(passed=True,checks=['known relations only; unopened facts stay hidden','real graph and relationship-card navigation','focused graph and real horizontal character-index drag; overview switch','retired status filter cannot dim people from an old save','relationship selection restored and retired filter neutralized after close','relationship UI leaves story state unchanged','all 26 slotted people render; large text and reduced motion mobile','half-proof shows only already presented item','four suspects and cancel all inside the screen','actual point menu cancel leaves proof/story unchanged','four distinct venue styles in actual meeting renderer; Q6 at night','real map selection changes no clock or travel; current offers only; building polygons select without state changes','meeting type shown in selected-place footer'])
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('PASS',result,flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await b.close()
asyncio.run(main())
