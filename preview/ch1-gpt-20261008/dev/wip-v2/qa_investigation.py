"""Fresh game, actual clues/testimony and manual Somsom discovery. No clue injection."""
from playwright.sync_api import sync_playwright
import shutil
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--resume",help="Resume an actual storage snapshot collected by this real walkthrough")
args=parser.parse_args()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 context=b.new_context(viewport={'width':844,'height':390},storage_state=args.resume if args.resume else None)
 page=context.new_page();errors=[];bad=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
 page.goto('http://127.0.0.1:8000/playT.html');page.wait_for_timeout(16000)
 def state():return page.evaluate('window.__T("({beats:G&&G.beats,found:G&&G.found,asked:G&&G.asked,obs:G&&G.obsSeen,reason:G&&G.reason,dl:!!DL,loc:G&&G.loc,tab:G&&G.tab})")')
 def drain(limit=450):
  quiet=0
  for _ in range(limit):
   if page.locator('#innins [data-k="next"],#innins [data-k="ok"]').count():page.locator('#innins [data-k="next"],#innins [data-k="ok"]').first.click();quiet=0;page.wait_for_timeout(350)
   elif state()['dl']:page.keyboard.press('Enter');quiet=0;page.wait_for_timeout(180)
   elif page.locator('#okfind').count():page.locator('#okfind').click();quiet=0;page.wait_for_timeout(750)
   elif page.locator('#tostay2').count():page.locator('#tostay2').click();quiet=0;page.wait_for_timeout(750)
   else:
    quiet+=1;page.wait_for_timeout(200)
    if quiet>=6:break
 def click(sel):
  page.wait_for_timeout(700)
  page.locator(sel).first.click(timeout=7000)
  page.wait_for_timeout(400);drain()
 def scene_click(sel):
  for direction in [None,'#fsal','#fsar','#fsar']:
   if direction and page.locator(direction).count():page.locator(direction).click();page.wait_for_timeout(550)
   e=page.locator(sel).first
   if e.count():
    r=e.bounding_box()
    if r and 5<r['x']+r['width']/2<700 and 5<r['y']+r['height']/2<385:
     click(sel);return
  raise AssertionError('Scene target not visible: '+sel)
 def scene_npc(npc):
  # Sprite buttons intentionally ignore DOM hit testing; the game checks opaque
  # character pixels instead. Use a genuine pointer on that visible character.
  page.wait_for_timeout(700)
  # Wait for the real alpha mask, then tap inside the body instead of the
  # fallback rectangle or a hair-edge pixel that moves with the idle animation.
  page.wait_for_function('(npc)=>{const im=document.querySelector("#bigscene svg image.wn9[data-k="+npc+"]");return im&&window.__innMask()[im.getAttribute("href")]==="ok"}',arg=npc)
  point=page.evaluate('(npc)=>{const r=document.querySelector("#bigscene").getBoundingClientRect();for(let y=Math.max(12,r.top+12);y<Math.min(innerHeight-12,r.bottom-12);y+=6)for(let x=Math.max(12,r.left+12);x<Math.min(688,r.right-12);x+=6)if(document.elementFromPoint(x,y)?.closest("#bigscene")&&[[0,0],[-6,0],[6,0],[0,-6],[0,6]].every(([dx,dy])=>window.__innNpcHit(x+dx,y+dy)===npc))return {x,y};return null}',npc)
  assert point,('No visible character pixel',npc,state())
  page.mouse.click(point['x'],point['y']);page.wait_for_timeout(400);drain();assert state()['tab']=='talk',(npc,point,state())
 def move(i):
  if state()['loc']==i:
   if state()['tab']!='scene':click('#w209rail .g>[data-w="scene"]')
   return
  click('#w209rail .g>[data-w="move"]')
  click('#innmove [data-i="'+str(i)+'"]')
  if state()['tab']!='scene':click('#w209rail .g>[data-w="scene"]')
  print('location',i,flush=True)
 page.locator('#innmain [data-m="'+('cont' if args.resume else 'new')+'"]').click()
 for _ in range(1000):
  z=state()
  if z['beats'] and z['beats'].get('inn_pro'):break
  if z['dl']:page.keyboard.press('Enter')
  elif page.locator('#inncold').count():page.mouse.click(400,250)
  else:page.keyboard.press('Enter')
  if _%100==0:print('intro checkpoint',_,z,flush=True)
  page.wait_for_timeout(180)
 assert state()['beats'].get('inn_pro'),state()
 drain()
 if not args.resume:assert not state()['found'],state()
 if not args.resume:context.storage_state(path='/tmp/investigation-after-intro.json')
 print(('Resumed actual saved investigation' if args.resume else 'Fresh intro complete; no evidence seeded'),flush=True)
 if 'C04' not in state()['found']:
  for cid in ['C01','C02']:
   if cid not in state()['found']:scene_click('#bigscene [data-spot="'+cid+'"]')
  page.wait_for_timeout(2500)
  assert 'C04' not in state()['found'], 'Somsom was still auto-discovered'
  assert not state()['dl'], 'Somsom dialogue started without an investigation click'
  assert page.locator('#bigscene .inn-under-cue').count()==1
  assert page.locator('#bigscene .innunderlook9').count()==0
  page.screenshot(path='/tmp/investigation-manual-discovery.png')
  scene_click('#bigscene [data-obs="o_under"]')
  assert 'o_under' in state()['obs'],state()
  assert 'C04' in state()['found'],state()
  context.storage_state(path='/tmp/investigation-after-somsom.json')
  print('Somsom found by deliberate scene click',flush=True)
 else:
  assert 'o_under' in state()['obs'],state()
  print('Resumed real collected Somsom state; manual discovery already verified in previous run',flush=True)
 move(2)
 if 'C03' not in state()['asked']:
  scene_npc('nabi');click('[data-ask="C03"]:visible')
 assert 'C03' in state()['asked'],state()
 # Investigation now collects clues directly, without a separate quiz.
 if state()['tab']!='scene':click('#w209rail .g>[data-w="scene"]')
 assert not page.locator('#logic-note,#logic-panel').count()
 assert all(cid in state()['found'] for cid in ['C01','C02','C04'])
 context.storage_state(path='/tmp/investigation-after-linen.json')
 move(3);scene_click('#bigscene [data-spot="C06"]');scene_npc('geokkuri')
 click('[data-ask="C07"]:visible');click('[data-ask="C13"]:visible')
 move(4);scene_click('#bigscene [data-spot="C08"]')
 move(3);scene_npc('geokkuri')
 click('#showev');click('[data-show="C08"]')
 assert state()['beats'].get('inn_show_geokkuri_C08'),state()
 assert '올해 첫눈이 내리기 시작했다' in page.evaluate('EP1INN.EV.C13.card')
 print('Weather follow-up acquired through actual evidence presentation',flush=True)
 if state()['tab']!='scene':click('#w209rail .g>[data-w="scene"]')
 assert all(cid in state()['found'] for cid in ['C06','C08']),state()
 assert all(cid in state()['asked'] for cid in ['C07','C13']),state()
 assert not page.locator('#logic-note,#logic-panel').count()
 assert not errors,errors
 assert not bad,bad
 print('Actual scene clues, witness questions and weather follow-up collected without a separate quiz OK',state(),flush=True)
 b.close()
