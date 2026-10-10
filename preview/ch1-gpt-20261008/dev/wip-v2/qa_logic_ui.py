"""Independent deduction expectations, real card selection and wrong feedback."""
from playwright.sync_api import sync_playwright
import shutil
SOLUTIONS={'linen':[['C02','C03']], 'time':[['C06','C07'],['C13','C08']], 'location':[['C04','C10']], 'contact':[['C05','C01']], 'seal':[['C10','C12']]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 for vp in [{'width':844,'height':390},{'width':390,'height':844}]:
  page=b.new_page(viewport=vp);errors=[];bad=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
  page.goto('http://127.0.0.1:8000/playT.html');page.wait_for_timeout(16000)
  page.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot();window.__T('G.found=["C01","C02","C04","C05","C06","C08","C09","C10"];G.asked=["C03","C07","C12","C13"];G.beats.inn_show_geokkuri_C08=1;G.beats.inn_locationClaim=1;G.tab="scene";render()')''')
  page.wait_for_timeout(1000)
  # Exercise notebook UI without triggering scripted room arrival.
  page.evaluate('window.__T("if(DL){DL.done=null;endDlg()}");window.__logicOpen("linen",{mode:"notebook"})')
  assert page.locator('#logic-panel [data-act=submit]').is_disabled()
  hp=page.evaluate('window.__T("G.hp")')
  for cid in ['C02','C03']:page.locator(f'#logic-panel [data-card="{cid}"]').click()
  page.locator('#logic-panel [data-option="1"]').click();page.locator('#logic-panel [data-act=submit]').click()
  assert '돈을 옮겼다는 증거는 아니다' in page.locator('.lp-feedback').inner_text()
  assert page.evaluate('window.__T("G.hp")')==hp
  # Both distinct cards are selected once; re-click removes rather than duplicates.
  page.locator('#logic-panel [data-card="C02"]').click()
  assert page.locator('#logic-panel [data-act=submit]').is_disabled()
  page.locator('#logic-panel [data-card="C02"]').click()
  page.locator('#logic-panel [data-option="0"]').click();page.wait_for_timeout(600)
  page.locator('#logic-panel [data-act=submit]').click()
  assert page.locator('.lp-summary').count()
  page.locator('#logic-panel [data-act=finish]').click()
  assert 'linen' in page.evaluate('window.__T("G.reason.solved")')
  # Save sanitizer keeps only known completed ids and excludes malicious drafts.
  state=page.evaluate('''window.__T('sanitizeState({v:3,prog:{inn:Object.assign(fresh(G.ci),{introDone:true,reason:{version:1,solved:["linen","bad"],drafts:{injected:true}}})}}).prog.inn.reason')''')
  assert state=={'version':1,'solved':['linen']},state
  for qid,pairs in SOLUTIONS.items():
   page.evaluate('window.__T("if(DL){DL.done=null;endDlg()}")')
   assert page.evaluate('(id)=>window.__logicOpen(id,{mode:"notebook"})',qid),qid
   for j,pair in enumerate(pairs):
    if qid=='time' and j==0:
     before=page.locator('.lp-clock svg').get_attribute('aria-label')
     page.locator('#logic-panel [data-act=rotate]').click()
     assert page.locator('.lp-clock svg').get_attribute('aria-label')!=before
    # Reverse order is equally valid; all testimony comes from asked.
    for cid in reversed(pair):page.locator(f'#logic-panel [data-card="{cid}"]').click()
    page.locator('#logic-panel [data-option="0"]').click();page.wait_for_timeout(600)
    page.locator('#logic-panel [data-act=submit]').click()
   assert page.locator('.lp-summary').count(),qid
   page.screenshot(path=f'/tmp/logic-{qid}-{vp["width"]}.png')
   page.locator('#logic-panel [data-act=finish]').click()
  assert len(page.evaluate('window.__T("G.reason.solved")'))==5
  assert not errors,errors
  assert not bad,bad
  print(vp,'all five independent deductions, reverse order, asked testimony, notebook no penalty, save sanitization OK',flush=True)
  page.close()
 b.close()
