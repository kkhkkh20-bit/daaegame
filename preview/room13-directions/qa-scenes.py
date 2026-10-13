from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).parent
BASE='http://127.0.0.1:8098/'
SCENES=['investigation','guard','daram','room13']
expected=[f'{d}-{s}-{suffix}.png' for d in ['b','c'] for s,suffix in [('guard','dialogue'),('daram','dialogue'),('room13','cutscene')]]
missing=[name for name in expected if not (ROOT/'assets'/name).exists()]
if missing:print(json.dumps({'missing':missing}));sys.exit(2)
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
 page.on('pageerror',lambda err:errors.append(str(err)))
 page.goto(BASE+'scenes.html?standalone&direction=b&scene=guard')
 page.evaluate('document.fonts.ready')
 assets=[]
 for direction in ['b','c']:
  for scene in SCENES:
   page.evaluate('([d,s])=>setScene(d,s)',[direction,scene])
   page.wait_for_function('document.querySelector(".scene-art").complete && document.querySelector(".scene-art").naturalWidth>0')
   page.wait_for_timeout(120)
   assert page.locator('.stage').get_attribute('data-failed')=='false'
   assets.append(page.locator('.scene-art').evaluate('(img)=>({src:img.getAttribute("src"),width:img.naturalWidth,height:img.naturalHeight})'))
   page.screenshot(path=str(ROOT/'screenshots'/f'{direction}-{scene}-scene.png'))
   if scene in ['guard','daram']:
    assert page.locator('.dialogue-ui').is_visible()
    assert not page.locator('.investigation-ui').is_visible()
   if scene=='room13':
    assert page.locator('.cutscene-ui').is_visible()
    assert not page.locator('.dialogue-ui').is_visible()
    assert not page.locator('.investigation-ui').is_visible()
 page.goto(BASE+'scenes.html')
 page.get_by_role('button',name='C · 손그림 방향',exact=True).click()
 page.get_by_role('button',name='다람이 감정',exact=True).click()
 assert page.locator('.stage').get_attribute('data-direction')=='c'
 assert page.locator('.stage').get_attribute('data-scene')=='daram'
 page.get_by_role('button',name='UI 숨기기',exact=True).click()
 assert not page.locator('.dialogue-ui').is_visible()
 page.get_by_role('button',name='UI 보이기',exact=True).click()
 assert page.locator('.dialogue-ui').is_visible()
 assert page.locator('#original').get_attribute('href')=='assets/c-daram-dialogue.png'
 page.get_by_role('button',name='B · 새 도트 방향',exact=True).click()
 page.get_by_role('button',name='경비 대화',exact=True).click()
 page.screenshot(path=str(ROOT/'screenshots'/'scene-comparison-page.png'),full_page=True)
 mobile=browser.new_context(viewport={'width':844,'height':390},device_scale_factor=1,is_mobile=True,has_touch=True)
 m=mobile.new_page();m.on('pageerror',lambda err:errors.append(str(err)))
 for direction in ['b','c']:
  m.goto(BASE+f'scenes.html?standalone&direction={direction}&scene=daram')
  m.wait_for_function('document.querySelector(".scene-art").complete && document.querySelector(".scene-art").naturalWidth>0')
  m.evaluate('document.fonts.ready');m.wait_for_timeout(120)
  m.screenshot(path=str(ROOT/'screenshots'/f'{direction}-daram-mobile.png'))
  box=m.locator('.frame').bounding_box();assert box['y']>=-1 and box['y']+box['height']<=391
 m.goto(BASE+'scenes.html')
 m.get_by_role('button',name='C · 손그림 방향',exact=True).tap()
 m.get_by_role('button',name='13호실 컷씬',exact=True).tap()
 assert m.locator('.stage').get_attribute('data-direction')=='c'
 assert m.locator('.stage').get_attribute('data-scene')=='room13'
 m.get_by_role('button',name='UI 숨기기',exact=True).tap();assert not m.locator('.cutscene-ui').is_visible()
 m.get_by_role('button',name='UI 보이기',exact=True).tap();assert m.locator('.cutscene-ui').is_visible()
 report={'desktop':[1280,720],'mobile':[844,390],'sceneAssets':assets,'jsErrors':errors,'checks':['B/C x four scenes loaded and rendered','six dialogue and cutscene full-frame screenshots','B/C mobile Daram screenshots','UI toggle hides all game overlays','desktop style and scene tab clicks','mobile real touch style/scene/UI toggle','room13 scene has no investigation HUD/actions','mobile full frame remains inside viewport'],'scope':'Standalone static visual concepts only; not actual game test or animation implementation.'}
 (ROOT/'qa-scenes-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False,indent=2))
 browser.close()
