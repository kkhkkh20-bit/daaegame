"""Real pointer regression: dialogue taps must not spill into scene investigation."""
import argparse, shutil, subprocess
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--baseline',action='store_true');args=ap.parse_args()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 viewports=[{'width':844,'height':390}]
 if not args.baseline:viewports.append({'width':390,'height':844})
 for viewport in viewports:
  pg=b.new_page(viewport=viewport);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  if args.baseline:
   source=subprocess.check_output(['git','show','cd0b802:preview/ch1-gpt-20261008/play_v2.html'],text=True)
   hook='CASES.forEach(function(c){var cf=CONFESS[c.id];c.contra.forEach(function(x){if(cf&&x.unlock===cf)x.unlock=null})});\n'
   assert source.count(hook)==1
   source=source.replace(hook,hook+'window.__T=function(code){return eval(code)};\n')
   pg.route('**/playT.html',lambda route:route.fulfill(body=source,content_type='text/html'))
  pg.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');pg.wait_for_timeout(16000)
  pg.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1};');document.querySelector('#innmain').remove();window.__w209boot()''');pg.wait_for_timeout(1000)
  pg.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};G.loc=CASES[G.ci].locations.findIndex(l=>l.id==="hall");G.tab="scene";render()')''');pg.wait_for_timeout(2000)
  def clock_point():
   # Use the player's actual pan controls. scrollIntoView previously produced
   # temporary offscreen coordinates on mobile and hid a real access problem.
   for _ in range(10):
    box=pg.locator('[data-spot="C06"]').bounding_box()
    x=box['x']+box['width']/2;y=box['y']+box['height']/2
    if 5<x<viewport['width']-5 and 5<y<viewport['height']-5:return x,y
    arrow=pg.locator('#fsar' if x>=viewport['width']-5 else '#fsal')
    assert arrow.is_visible() and arrow.is_enabled(),('Clock inaccessible',box,viewport)
    arrow.click();pg.wait_for_timeout(400)
   raise AssertionError(('Clock stayed outside the viewport',box,viewport))
  if args.baseline:
   # Historic reproduction predates usable portrait pan controls.
   pg.locator('[data-spot="C06"]').scroll_into_view_if_needed();pg.wait_for_timeout(150)
   box=pg.locator('[data-spot="C06"]').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
  else:x,y=clock_point()
  # Complete the final spoken line with a genuine click over the clock's screen position.
  pg.evaluate('''window.__T('say([["det0","조사를 시작하자."]],function(){render()});clearInterval(DL.timer);DL.timer=null')''')
  pg.mouse.click(x,y)
  assert not pg.evaluate('window.__T("!!DL")'),'Final dialogue did not close'
  # Keep a continuous burst past the old 1.8-second guard limit. Re-read the
  # hotspot rectangle because the portrait layout can settle after dialogue.
  if not args.baseline:clock_point()
  for i in range(18):
   pg.wait_for_timeout(170)
   box=pg.locator('[data-spot="C06"]').bounding_box()
   if not args.baseline:assert 5<box['x']+box['width']/2<viewport['width']-5,('Clock moved offscreen after dialogue',box)
   pg.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
   if args.baseline and pg.evaluate('window.__T("!!DL")'):break
  leaked=pg.evaluate('window.__T("!!DL||G.found.includes(\\"C06\\")")')
  if args.baseline:
   assert leaked,'Expected the old build to reproduce the clock click-through'
   print(viewport,'baseline: clock opened during dialogue tapping',flush=True);pg.close();continue
  assert not leaked,'Clock opened from dialogue tapping'
  pg.wait_for_timeout(750);pg.mouse.click(*clock_point());pg.wait_for_timeout(100)
  assert pg.evaluate('window.__T("!!DL")'),'Clock failed to respond to a deliberate fresh tap'
  for _ in range(80):
   if not pg.evaluate('window.__T("!!DL")'):break
   pg.keyboard.press('Enter');pg.wait_for_timeout(180)
  assert pg.evaluate('window.__T("G.found.includes(\\"C06\\")")'),'The reachable clock was not collected'
  # Even if a transition removes the veil between down and up, the same gesture cannot investigate.
  pg.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};G.found=[];render()')''');pg.wait_for_timeout(2000)
  x,y=clock_point()
  pg.evaluate('''window.__T('say([["det0","이제 주변을 살펴보자."]],function(){render()});clearInterval(DL.timer);DL.timer=null')''')
  pg.mouse.move(x,y);pg.mouse.down()
  pg.evaluate('window.__T("endDlg()")');pg.wait_for_timeout(900);pg.mouse.up();pg.wait_for_timeout(100)
  assert not pg.evaluate('window.__T("!!DL||G.found.includes(\\"C06\\")")'),'Held gesture leaked across transition'
  # Scene handlers must also reject background observation before introduction completion.
  pg.evaluate('''window.__T('G.beats.inn_pro=0;render()')''');pg.wait_for_timeout(2000)
  pg.mouse.click(*clock_point());pg.wait_for_timeout(100)
  assert not pg.evaluate('window.__T("!!DL||G.found.includes(\\"C06\\")")'),'Investigation started before introduction completed'
  assert not errors,errors
  print(viewport,'OK: native pan reaches clock, rapid taps blocked, fresh tap collects C06, held gesture and pre-investigation blocked',flush=True)
  pg.close()
 b.close()
