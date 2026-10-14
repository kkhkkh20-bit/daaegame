"""Village map v5 (ported from closed PR #8): real mouse/keyboard/touch input on
the built web release, with explicit eligibility fixtures (not a natural campaign).
Run from experiments/renpy-ch1 with the repository root served on :8765."""
import asyncio,json,os,urllib.request
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa'))/'worldmap';OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/')
DATA=json.loads((Path(__file__).resolve().parents[1]/'game/room13-worldmap-v5.json').read_text())
async def main():
 report={'archive':json.load(urllib.request.urlopen(URL+'game-transport.json'))['archive_sha256'],'kind':'Actual Chromium inputs with explicitly injected lodging/secret states, not natural full campaign','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),args=['--no-sandbox','--enable-unsafe-swiftshader']);c=await b.new_context(viewport={'width':1280,'height':720},has_touch=True,service_workers='block');pg=await c.new_page();q=UIQA(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  async def scope():return await q.py('import renpy;s=renpy.display.screen.get_screen("r13_map").scope;result={k:s[k] for k in ("region","selected","map_hover")}')
  async def fixture(**changes):
   await q.py('import renpy;s=renpy.store;s.r13_edit(**'+repr(changes)+');renpy.exports.restart_interaction();result=True')
  async def world():
   await q.press('지도 · 이동');await q.wait('r13_map')
   if (await scope())['region']!='village':await q.press('마을 보기')
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu');await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;s.persistent.room13_map_list=False;result=True');await q.press('처음부터');await q.advance();await q.wait('r13_hub')
   # Unregistered: private destinations cannot be clicked or named by map widgets.
   await q.py('import renpy;s=renpy.store;s.r13_flag("entry_corrected");w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub')
   await world();st=await q.state();assert not any(any(n in x['text'] for n in ('진료실','학교','공동 창고')) for x in st['buttons']);await q.shot('01-unregistered');await q.press('현장으로 돌아가기');await q.wait('r13_hub')
   await fixture(day=2,period=0,location='inn',flags=['entry_corrected','lodging'])
   await q.py('import renpy;s=renpy.store;s.r13_upgrade();w=renpy.exports.get_widget("r13_hub","r13_options_gear");w.action=s.Jump("r13_field");w.clicked=w.action;result=True');await q.input(1220,50);await q.wait('r13_hub')
   before=await q.room();await world();await q.shot('02-world-all-eight')
   for key,spec in DATA['layers'].items():
    if not spec['node']:continue
    x,y=spec['point'];await q.input(30+round(x*860/1672),150+round(y*860/1672));assert (await scope())['selected']==key,(key,await scope());assert await q.room()==before
   report['checks'].append('All 8 actual polygon targets select their exact node without any run-state/time change')
   await q.input(30+round(1047*860/1672),150+round(498*860/1672));await q.shot('03-inn-selected')
   # Inn bbox corner is outside its silhouette: must not select inn from rectangle.
   await q.press('우체국');keep=(await scope())['selected'];x,y,w,h=DATA['layers']['inn']['bounds'];await q.input(30+round(x*860/1672)+1,150+round(y*860/1672)+1);assert (await scope())['selected']==keep
   report['checks'].append('Transparent inn bounding-box corner rejects pointer input (polygon mask, not rectangle)')
   x,y=DATA['layers']['inn']['point'];await pg.mouse.move(30+x*860/1672,150+y*860/1672);await asyncio.sleep(.4);assert (await scope())['map_hover']=='inn';await q.shot('04-hover-individual-building');assert await q.room()==before
   # Direction-key focus must activate the same per-building highlight before Enter selects.
   await pg.keyboard.press('ArrowLeft');await asyncio.sleep(.5);f=await scope();assert f['map_hover'] is not None,f;await q.shot('05-keyboard-focus');await pg.keyboard.press('Enter');await asyncio.sleep(.4);assert (await scope())['selected']==f['map_hover'];assert await q.room()==before
   report['checks'].append('Mouse hover and arrow-key focus independently highlight a building; Enter selects without travel')
   await pg.keyboard.press('Escape');await q.wait('r13_hub');assert await q.room()==before
   # The workshop scene stalls headless software GL (also on the previous build): use the post office.
   await world();await q.press('우체국');await q.press('이곳으로 이동');await q.wait('r13_hub');after=await q.room();assert after['location']=='post';assert (after['day'],after['period'])==(before['day'],before['period'])
   await world();assert (await scope())['selected']=='post';await q.press('현장으로 돌아가기');await q.wait('r13_hub')
   report['checks'].append('Escape cancellation preserves exact state; confirmed travel and reentry reflect actual current location at zero time cost')
   # Saving inside the workshop takes 40-60 s (and crashed the previous public build) in headless software GL; save at the store instead.
   await world();await q.press('공동 창고');await q.press('이곳으로 이동');await q.wait('r13_hub')
   await q.save(1);saved=await q.room();await world();await q.press('진료실');await q.press('이곳으로 이동');await q.wait('r13_hub');await q.load(1);assert await q.room()==saved;await q.shot('06-save-restored');await world();assert (await scope())['selected']=='store';await q.press('현장으로 돌아가기');await q.wait('r13_hub')
   report['checks'].append('Real save UI, travel, load UI restore exact room state and map current location')
   await world();await q.press('여관 접수대');await q.press('여관 내부 보기');await q.shot('07-existing-inn-map');await q.press('주방');await q.press('이곳으로 이동');await q.wait('r13_hub');assert (await q.room())['location']=='kitchen';await q.press('접수대');await q.wait('r13_hub');await q.press('2층으로');await q.wait('r13_hub');await q.shot('08-existing-hall');await q.press('13호실');await q.wait('r13_hub');assert (await q.room())['location']=='room13'
   report['checks'].append('Existing inn overview and kitchen→reception→hall→13 access still work')
   # Day/case eligibility as explicit fixtures; labels, tooltips and accessible alt names inspected together.
   await world();await fixture(location='passage',passage_open=True,secret_route_unlocked=False)
   await q.press('여관 안');secrets=await q.py('import renpy;s=renpy.store;result={"nodes":s.r13_map_nodes("inn"),"selected":renpy.display.screen.get_screen("r13_map").scope["selected"],"path":s.r13_location_path(),"alts":[str(getattr(f.widget,"alt",None)) for f in renpy.display.focus.focus_list],"tooltips":[str(getattr(f.widget,"tooltip",None)) for f in renpy.display.focus.focus_list]}');assert 'passage'not in [k for k,v in secrets['nodes']] and secrets['selected']!='passage' and '통로'not in str(secrets['alts'])+str(secrets['tooltips'])+secrets['path'];await q.shot('09-secret-stale-location-hidden')
   await fixture(location='inn',passage_open=True,secret_route_unlocked=True,case_state='occurred');keys=await q.py('import renpy;result=[k for k,v in renpy.store.r13_map_nodes("inn")]');assert 'passage'in keys and 'guestroom'in keys
   await fixture(passage_open=False,case_state='pending');keys=await q.py('import renpy;result=[k for k,v in renpy.store.r13_map_nodes("inn")]');assert 'passage'not in keys and 'guestroom'not in keys
   await q.press('현장으로 돌아가기');await q.wait('r13_hub');report['checks'].append('Stale secret current-location save reveals no passage node/name/tooltip/alt; discovered-open and incident guestroom conditions retained')
   await pg.set_viewport_size({'width':844,'height':390});q.touch=True;await world();await q.shot('10-mobile-landscape');x,y=DATA['layers']['store']['point'];await q.input(30+round(x*860/1672),150+round(y*860/1672));assert (await scope())['selected']=='store';await q.press('이곳으로 이동');await q.wait('r13_hub');assert (await q.room())['location']=='store'
   await world();await q.press('큰 목록 보기');await q.shot('11-mobile-large-list');await q.press('여관 접수대');await q.press('이곳으로 이동');await q.wait('r13_hub')
   await pg.set_viewport_size({'width':390,'height':844});await world();await q.shot('12-mobile-portrait-list');await q.press('현장으로 돌아가기');await q.wait('r13_hub');report['checks'].append('844×390 touchscreen polygon travel and large-list travel; 390×844 portrait list and cancellation')
   await pg.set_viewport_size({'width':1280,'height':720});q.touch=False;await world();await q.press('지도로 보기');await q.press('학교');st=await q.state();button=next(x for x in st['buttons'] if '이곳으로 이동'in x['text']);x,y,w,h=button['rect'];before=await q.room();await pg.mouse.dblclick(x+w/2,y+h/2,delay=30);await q.wait('r13_hub');after=await q.room();assert after['location']=='school';assert before['day']==after['day'] and before['period']==after['period'];await q.shot('13-double-click-arrival');report['checks'].append('Double-click confirmation reaches one destination without time change')
   assert not errors,errors;report['status']='passed'
  except Exception as e:
   import traceback;report.update(status='failed',error=repr(e),trace=traceback.format_exc());await pg.screenshot(path=str(OUT/'failure.png'))
   try:(OUT/'failure-state.json').write_text(json.dumps(await q.state(),ensure_ascii=False,indent=2))
   except:pass
  report['errors']=errors;(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True);await b.close()
  if report['status']!='passed':raise SystemExit(1)
asyncio.run(main())
