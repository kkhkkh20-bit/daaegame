from pathlib import Path
import json
from playwright.sync_api import sync_playwright
P=Path(__file__).parent
errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8098/index.html'+'?standalone&direction=a&mode=investigation')
 page.evaluate('document.fonts.ready');page.wait_for_timeout(300)
 for direction in ['a','b','c']:
  for mode in ['investigation','title','questions']:
   page.evaluate('([d,m])=>setDirection(d,m)',[direction,mode]);page.wait_for_timeout(180)
   page.screenshot(path=str(P/'screenshots'/f'{direction}-{mode}.png'))
 page.evaluate("setDirection('b','investigation')")
 page.get_by_role('button',name='대화',exact=True).click() if False else page.locator('[data-action=talk]').click()
 assert page.locator('.stage').get_attribute('data-mode')=='questions'
 page.locator('[data-question="0"]').click();assert page.locator('.stage').get_attribute('data-mode')=='dialogue'
 page.locator('.next').click()
 page.evaluate("setDirection('b','investigation')")
 page.locator('[data-action=evidence]').click();assert page.locator('.modal').is_visible()
 page.locator('#close').click();assert not page.locator('.modal').is_visible()
 page.locator('.h1').click();assert page.locator('.modal').is_visible();page.locator('#close').click()
 page.goto('http://127.0.0.1:8098/index.html');page.wait_for_timeout(200);page.screenshot(path=str(P/'screenshots'/'comparison-page.png'),full_page=True)
 mobile=b.new_context(viewport={'width':844,'height':390},device_scale_factor=1,is_mobile=True,has_touch=True)
 m=mobile.new_page();m.on('pageerror',lambda e:errors.append(str(e)))
 m.goto('http://127.0.0.1:8098/index.html'+'?standalone&direction=b');m.wait_for_timeout(300)
 m.screenshot(path=str(P/'screenshots'/'b-mobile.png'))
 m.locator('[data-action=talk]').tap();assert m.locator('.stage').get_attribute('data-mode')=='questions';m.locator('#back').tap()
 # image load validation including CSS backgrounds
 assets=['legacy-gate.png','legacy-daram.png','legacy-guard.png','new-pixel.png','handpainted.png']
 loaded=page.evaluate('async (assets)=>await Promise.all(assets.map(src=>new Promise(resolve=>{let i=new Image();i.onload=()=>resolve({src,width:i.naturalWidth,height:i.naturalHeight});i.onerror=()=>resolve({src,error:true});i.src="assets/"+src})))',assets)
 report={'viewport':[1280,720],'mobile':[844,390],'errors':errors,'assets':loaded,'checks':['three directions x title/investigation/questions screenshot','dialogue question and next action','evidence modal open/cancel','hotspot modal open/cancel','touch talk/back'],'runtimeModified':False,'note':'Design prototype only, no actual game playthrough. Existing originals A contain mixed raster detail; B/C are new concept images.'}
 (P/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 b.close()
 print(json.dumps(report,ensure_ascii=False,indent=2))
