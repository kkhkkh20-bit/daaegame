"""Prepared investigation UI test: native room-map pointer and keyboard access."""
from playwright.sync_api import sync_playwright
import shutil,json

with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 for w,h in [(844,390),(390,844),(640,360)]:
  page=b.new_page(viewport={'width':w,'height':h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');page.wait_for_timeout(16000)
  page.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1};');document.querySelector('#innmain').remove();window.__w209boot()''');page.wait_for_timeout(1000)
  page.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};G.loc=CASES[G.ci].locations.findIndex(l=>l.id==="hall");G.tab="scene";G.found=["C06"];G.visited=[G.loc];render()')''');page.wait_for_timeout(1500)
  page.locator('#w209rail .g>[data-w="move"]').click();page.wait_for_timeout(400)
  m=page.locator('#innmove');assert m.get_attribute('data-space-map')=='1','Map module not loaded'
  print('MAP',w,h,page.evaluate('''()=>{const m=document.querySelector('#innmove');return {rect:m.getBoundingClientRect().toJSON(),scrollHeight:m.scrollHeight,clientHeight:m.clientHeight,text:m.innerText,rooms:[...m.querySelectorAll('[data-i]')].map(b=>({label:b.getAttribute('aria-label'),disabled:b.disabled,rect:b.getBoundingClientRect().toJSON()})),overlap:!!document.querySelector('#wmap')}}'''),flush=True)
  assert page.locator('#innmove [data-map]').is_hidden()
  assert page.locator('#innmove [data-room-id="hall"]').get_attribute('aria-current')=='true'
  assert page.locator('#innmove [aria-current]').count()==1
  page.locator('#innmove [data-room-id="dotoroom"]').focus()
  assert '도토의 날씨 일지' in page.locator('#inn-map-purpose').inner_text()
  assert page.locator('#wmap').count()==0
  expected=page.evaluate('window.__T("CASES[G.ci].locations.map((l,i)=>i).filter(i=>locOpen(CASES[G.ci],i))")')
  actual=page.locator('#innmove [data-i]').evaluate_all('(bs)=>bs.map(b=>+b.dataset.i).sort((a,b)=>a-b)')
  assert actual==expected,'Native room lock state changed'
  assert page.locator('#innmove .map-room-clues').count()==1
  assert '단서 1' in page.locator('#innmove [data-room-id="hall"]').inner_text()
  assert '솜솜' not in m.inner_text() and '첫눈' not in m.inner_text()
  for btn in page.locator('#innmove button[data-i]').all():
   r=btn.bounding_box();assert r['width']>=44 and r['height']>=44
   assert r['x']>=0 and r['x']+r['width']<=w
  page.screenshot(path=f'/tmp/map-navigation-{w}.png',animations='disabled')
  # All available rooms reachable by tab; focus cycles within native dialog.
  page.locator('#innmove [data-x]').focus();focus=[]
  for i in range(10):
   page.keyboard.press('Tab');focus.append(page.evaluate('document.activeElement.outerHTML.slice(0,150)'))
   assert page.evaluate('!!document.activeElement.closest("#innmove")')
  print('FOCUS',w,focus,flush=True)
  page.keyboard.press('Escape');page.wait_for_timeout(200);assert page.locator('#innmove').count()==0
  page.locator('#w209rail .g>[data-w="move"]').click();page.wait_for_timeout(300)
  doto=page.locator('#innmove [data-room-id="dotoroom"]');r=doto.bounding_box();xy=(r['x']+r['width']/2,r['y']+r['height']/2)
  assert 0<=xy[0]<w and 0<=xy[1]<h
  page.mouse.click(*xy);page.wait_for_timeout(1400)
  assert page.locator('#innmove').count()==0
  assert page.evaluate('window.__T("CASES[G.ci].locations[G.loc].id")')=='dotoroom'
  print('PASS',w,h,'native move to dotoroom; pageerrors',errors,flush=True);assert not errors
  page.close()
 b.close()
