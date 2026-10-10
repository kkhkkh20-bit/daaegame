"""Prepared-evidence native proof regression; no separate reasoning quiz.

Real pointer inputs check explicit presentation, damage and legacy saves.
The final stale-animation check deliberately controls the async music effect.
"""
import shutil
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 for width,height in [(844,390),(390,844)]:
  page=b.new_page(viewport={'width':width,'height':height});page.set_default_timeout(6000);errors=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
  page.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');page.wait_for_timeout(16000)
  def state(code):return page.evaluate('(code)=>window.__T(code)',code)
  state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
  page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1000)
  state('if(DL){DL.done=null;endDlg()};G.found=Object.keys(EP1INN.EV);G.asked=["C03","C07","C12","C13"];G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);G.reason={version:1,solved:["linen","time","location","contact","seal"]};')
  def drain():
   quiet=0
   for _ in range(150):
    if page.locator('#rtgq').count() or page.locator('#rtnext').count():
     quiet=0;page.locator('#rtgbar [data-g="next"]').click();page.wait_for_timeout(170)
    else:
     quiet+=1;page.wait_for_timeout(200)
     if quiet>=12:break
   assert not page.locator('#rtgq,#rtnext').count(),'Dialogue did not return to the statement'
  def open_linen():
   state('if(DL){DL.done=null;endDlg()};document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;window.__rtgReset();G.beats.inn_meeting_version=2;G.beats.inn_life_confirmed=1;G.debate={pi:3,sus:{}};window.__rtOpen(CASES[G.ci])')
   page.wait_for_timeout(4300)
   page.locator('#rtgbar [data-g="next"]').click();page.wait_for_timeout(300)
   assert page.evaluate('window.__rtPh().stms[1].w')=='nabi'
  def select(cid):
   if not page.evaluate('document.body.classList.contains("rtg-drw")'):
    page.locator('#rtgbar [data-g="ev"]').click()
   page.locator('.rt [data-bl="'+cid+'"]').click();page.wait_for_timeout(250)
  def present():
   page.locator('#rtgbar [data-g="present"]').click();page.wait_for_timeout(350)
  open_linen()
  print(width,height,'native proof ready',flush=True)
  assert not page.locator('#logic-panel,#logic-note').count()
  select('C03')
  assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==0
  assert state('G.hp')==5 and state('G.wrong')==0
  present();drain()
  print(width,height,'premature card checked',flush=True)
  assert state('G.debate.pi')==3 and state('G.hp')==5
  assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==0,'A final card bypassed its first observation'
  select('C02');present();drain()
  print(width,height,'first observation checked',flush=True)
  assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==1
  assert not page.locator('.rt .bl.on').count(),'Next evidence was selected automatically'
  assert state('G.debate.pi')==3,'First observation auto-completed the accusation'
  select('C09')
  assert state('G.hp')==5,'Selecting an unrelated clue dealt damage before presenting'
  present();drain()
  print(width,height,'wrong presentation checked',flush=True)
  assert state('G.hp')==4 and state('G.wrong')==1
  # Catch stale success callbacks across a new council; no old queue may appear.
  page.evaluate('()=>{window.__qaHush=window.__hush;window.__hush=()=>new Promise(resolve=>window.__releaseHush=resolve)}')
  select('C03');present()
  print(width,height,'pending proof requested',flush=True)
  assert page.evaluate('typeof window.__releaseHush')=='function'
  page.evaluate('''()=>{const word=document.querySelector('.rt-bub.stm .wk');for(let i=0;i<12;i++)word?.click()}''')
  open_linen()
  print(width,height,'pending proof reset',flush=True)
  page.evaluate('window.__releaseHush();window.__hush=window.__qaHush');page.wait_for_timeout(1800)
  assert state('G.debate.pi')==3 and not page.locator('#rtnext,#rtgq').count()
  assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==0
  # F1 keeps its phase index but requires the player to present fur, then bag.
  state('document.querySelectorAll("body>.rt").forEach(x=>x.remove());window.__inMeeting=false;window.__rtgReset();G.beats.inn_meet=1;G.hp=5;window.__rtOpen(CASES[G.ci],EP1INN.FINAL)')
  print(width,height,'final intro opened',flush=True)
  page.wait_for_timeout(2000);drain()
  assert state('G.innfinal.pi')==0 and page.evaluate('window.__rtPh().type')=='debate'
  select('C01');present();drain()
  assert state('G.innfinal.pi')==0 and state('G.hp')==5
  select('C05');present();drain()
  assert page.evaluate('window.__rtgStep(window.__rtPh().stms[0])')==1
  assert not page.locator('.rt .bl.on').count()
  assert state('G.innfinal.pi')==0
  assert not errors,errors
  assert not bad,bad
  print(width,height,'OK: direct proof, no auto selection/completion, premature relevant card free, damage only on presentation, legacy notebook cannot skip proof, stale animation blocked, F1 requires fur then bag',flush=True)
  page.close()
 b.close()
