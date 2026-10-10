"""Prepared-state pointer checks for simple native controls in both orientations.

No extra UI script is injected. The game under test is the generated build.
"""
import shutil
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':844,'height':390});errors=[];bad=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
 page.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');page.wait_for_timeout(16000)
 def state(code):return page.evaluate('(code)=>window.__T(code)',code)
 state('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
 page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1000)
 state('if(DL){DL.done=null;endDlg()};G.found=Object.keys(EP1INN.EV).filter(id=>!["C03","C07","C12","C13"].includes(id));G.asked=["C03","C07","C12","C13"];G.debate={pi:1,sus:{}};window.__rtOpen(CASES[G.ci])')
 page.wait_for_timeout(4400)
 def buttons(expected):
  controls=page.locator('#rtgbar button:visible')
  assert controls.evaluate_all('(bs)=>bs.map(b=>b.dataset.g)')==expected
  assert controls.evaluate_all('(bs)=>bs.every(b=>{let r=b.getBoundingClientRect();return r.width>=44&&r.height>=44&&b.querySelector("svg.simple-icon[aria-hidden=true]")&&b.getAttribute("aria-label")})')
 for width,height in [(844,390),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(700)
  buttons(['ev','press','next'])
  assert not page.locator('#logic-note,#logic-panel').count()
  assert not page.locator('#rtgbar [data-g=obj]').is_visible()
  page.screenshot(path=f'/tmp/simple-current-meet-{width}.png')
  original=page.locator('body>.rt .rt-bub.stm p').inner_text().strip()
  hp=state('G.hp');page.locator('#rtgbar [data-g=ev]').click();page.wait_for_timeout(300)
  page.locator('body>.rt [data-bl=C01]').click();page.wait_for_timeout(500)
  buttons(['present','back'])
  claim=page.locator('#simple-drawer-claim')
  assert claim.is_visible() and claim.locator('p').inner_text().strip()==original
  assert page.locator('body>.rt .bl.on').get_attribute('data-bl')=='C01'
  assert state('G.hp')==hp,'Selecting a card should not present it'
  assert page.locator('body>.rt .rt-bub.stm').evaluate('(b)=>getComputedStyle(b).visibility')=='hidden'
  assert page.locator('body>.rt .rt-bul [data-bl]').evaluate_all('(bs)=>bs.every(b=>b.querySelector(".evic")&&b.getAttribute("aria-label"))')
  for selector in ['.rt-evd','.rt-bul']:
   box=page.locator('body>.rt '+selector).bounding_box();c=claim.bounding_box()
   assert box['y']>=c['y']+c['height']+4,(selector,c,box)
   bar=page.locator('#rtgbar').bounding_box()
   assert box['y']+box['height']<=bar['y']-4,(selector,box,bar)
  page.screenshot(path=f'/tmp/simple-current-drawer-{width}.png')
  page.locator('#rtgbar [data-g=back]').click();page.wait_for_timeout(350)
  assert not claim.count();buttons(['ev','press','next'])
  assert not page.locator('body>.rt .bl.on').count(),'Cancel retained the selected card'
  page.locator('#rtgbar [data-g=press]').click();page.wait_for_timeout(350)
  assert page.locator('#rtgq').count() and not claim.count()
  if width<550:
   q=page.locator('#rtgq').bounding_box();menu=page.locator('#rtgtr').bounding_box()
   assert q['y']>=menu['y']+menu['height']+4,(q,menu)
  page.screenshot(path=f'/tmp/simple-current-queue-{width}.png')
  for _ in range(40):
   if not page.locator('#rtgq').count():break
   page.locator('#rtgbar [data-g=next]').click();page.wait_for_timeout(200)
  assert not page.locator('#rtgq').count()
  page.wait_for_timeout(500)
  print(width,height,'OK: 3 native controls, 2 drawer controls, icons/accessible names/44px targets, original claim alongside cards, explicit selection, cancel and press dialogue',flush=True)
 assert not errors,errors
 assert not bad,bad
 browser.close()
