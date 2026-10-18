"""Actual local browser QA for reader-facing resource UI and original-ratio image viewers."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(os.environ.get('DASHBOARD_QA_OUT',ROOT/'reports/resource-ui-polish-20261018'));OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ.get('DASHBOARD_ORIGIN','http://127.0.0.1:8765')
URL=BASE+'/preview/resource-dashboard/'
checks=[];errors=[]
def shot(page,name):page.screenshot(path=str(OUT/(name+'.png')))
def ratio(page,selector):
 result=page.locator(selector).first.evaluate('e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,nw:e.naturalWidth,nh:e.naturalHeight,fit:getComputedStyle(e).objectFit}}')
 assert result['nw']>0,result
 # Contain allows letterboxing in a fixed frame; auto-height images must also preserve their box ratio.
 assert result['fit']=='contain',result
 return result
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':1365,'height':1000});page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.locator('[data-person]').first.wait_for();shot(page,'after-desktop');assert 'resident_' not in page.locator('body').inner_text();checks.append('default character cards hide technical identifiers')
 page.locator('#query').fill('서리 검사원');assert page.locator('[data-person]').count()==1;page.locator('[data-person]').click();page.locator('#detail[open]').wait_for();shot(page,'after-character');assert 'resident_seori' not in page.locator('#detail').inner_text();assert 'assets/' not in page.locator('#detail').inner_text()
 # Portrait opens the unaltered original in a second modal and returns focus/scroll to its opener.
 image_button=page.locator('#detail .image-button').first;image_button.click();page.locator('.image-viewer[open] img').wait_for();page.wait_for_function('document.querySelector(".image-viewer img").naturalWidth>0');ratio(page,'.image-viewer img');shot(page,'after-portrait-expanded')
 for _ in range(6):page.keyboard.press('Tab');assert page.evaluate('document.querySelector(".image-viewer").contains(document.activeElement)')
 page.keyboard.press('Escape');page.wait_for_function('!document.querySelector(".image-viewer").open');assert page.locator('#detail').evaluate('e=>e.open');assert image_button.evaluate('e=>e===document.activeElement')
 image_button.click();page.locator('.image-viewer[open]').wait_for();page.go_back();page.wait_for_function('!document.querySelector(".image-viewer").open');assert page.locator('#detail').evaluate('e=>e.open');checks.append('portrait full-ratio viewer, nested focus trap, Escape and browser Back')
 for _ in range(2):page.locator('#close').click();page.wait_for_function('!document.querySelector("#detail").open');page.wait_for_timeout(100);page.locator('[data-person]').click();page.locator('#detail[open]').wait_for()
 page.locator('#detail .technical').last.locator('summary').click();assert 'resident_seori' in page.locator('#detail').inner_text();checks.append('raw source evidence preserved in closed details')
 page.locator('#close').click();page.wait_for_timeout(150);page.locator('#query').fill('');page.locator('[data-tab=places]').click();page.locator('#place').select_option('kitchen');page.locator('#day').select_option('3');shot(page,'after-places');assert 'map31_' not in page.locator('#content').inner_text();assert page.locator('.placement-card').count()>0;checks.append('Korean place/action/day filters and hidden pose IDs')
 page.locator('#place').select_option('');page.locator('#day').select_option('');page.locator('[data-tab=audio]').click();shot(page,'after-audio');assert 'assets/' not in page.locator('#content').inner_text();assert page.evaluate('[...audioInstances].every(a=>a.paused)')
 page.locator('#query').fill('bgm-title.mp3');assert 'Sleep (Piano Only)' in page.locator('#content').inner_text();page.locator('[data-action=play]').click();page.wait_for_function('[...audioInstances].some(a=>!a.paused&&a.currentTime>0)');page.locator('[data-action=pause]').click();page.locator('[data-audio] input').fill('0.2');assert page.evaluate('[...audioInstances][0].volume')==.2;page.locator('[data-action=stop]').click();assert page.evaluate('[...audioInstances][0].currentTime')==0;checks.append('real MP3 playback/pause/stop/volume with actual title/credit')
 page.locator('#query').fill('sfx-click');page.locator('[data-action=play]').first.click();page.wait_for_timeout(80);page.locator('[data-action=play]').nth(1).click();assert page.evaluate('[...audioInstances].filter(a=>!a.paused).length')<=1;page.locator('[data-tab=characters]').click();assert page.evaluate('[...audioInstances].every(a=>a.paused)');checks.append('WAV playback, exclusive audio, tab/filter transitions stop old audio')
 page.locator('[data-tab=audio]').click();page.route('**/sfx-click.wav',lambda r:r.fulfill(status=200,content_type='audio/wav',body='bad audio'));page.locator('#query').fill('');page.locator('#query').fill('sfx-click');page.locator('[data-action=play]').first.click();page.wait_for_timeout(700);assert any(t in page.locator('[data-audio] [role=status]').first.inner_text() for t in ('실패','읽을 수 없'));page.unroute('**/sfx-click.wav');checks.append('unsupported audio feedback')
 page.route('**/sfx-click.wav',lambda r:r.fulfill(status=404,body='missing'));page.locator('#query').fill('page');page.locator('#query').fill('sfx-click');page.locator('[data-action=play]').first.click();page.wait_for_timeout(500);assert any(t in page.locator('[data-audio] [role=status]').first.inner_text() for t in ('실패','읽을 수 없'));page.unroute('**/sfx-click.wav');checks.append('missing audio error feedback')
 page.locator('#query').fill('');page.locator('#refresh').click();page.wait_for_function('document.querySelector("#summary").textContent.includes("최신 자료")')
 updated=page.evaluate('JSON.parse(JSON.stringify(data))');updated['data_version']='qa-next';page.route('**/version.json?*',lambda r:r.fulfill(json={k:updated[k] for k in ('schema','game_commit','data_version','generated_at')}));page.route('**/data.json?*',lambda r:r.fulfill(json=updated));page.locator('#refresh').click();page.wait_for_function('data.data_version==="qa-next"');checks.append('automatic data version reload remains functional')
 # Gallery original screenshots and review claims survive enhancement.
 page.goto(BASE+'/reports/place-balance-01936/');page.locator('.gallery-grid').first.wait_for();assert page.locator('figure').count()==66;shot(page,'after-gallery-desktop');page.locator('#gallery-place').select_option(label='임시 진료실');assert '서리' in page.locator('main').inner_text();page.locator('#gallery-day').select_option('2');page.locator('#gallery-period').select_option('오전');assert page.locator('figure:visible').count()==1
 page.locator('figure:visible .image-button').click();page.wait_for_function('document.querySelector(".image-viewer img").naturalWidth>0');r=ratio(page,'.image-viewer img');assert abs(r['width']/r['height']-r['nw']/r['nh'])<.01;shot(page,'after-landscape-expanded');page.locator('.image-viewer [data-zoom]').click();assert page.locator('.viewer-stage').evaluate('e=>e.scrollWidth>=e.clientWidth');page.locator('.image-viewer [data-zoom]').click();page.locator('.image-viewer [data-close]').click();page.wait_for_function('!document.querySelector(".image-viewer").open');assert page.locator('figure:visible .image-button').evaluate('e=>e===document.activeElement');checks.append('66 original captures retained, Korean gallery filters, landscape ratio, zoom/fit/focus')
 # Real mobile emulation (including viewport meta and touch); no fixed maximum-scale disables pinch.
 mobile=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,device_scale_factor=1);m=mobile.new_page();m.on('pageerror',lambda e:errors.append(str(e)))
 m.goto(URL);m.locator('[data-person]').first.wait_for();assert m.evaluate('innerWidth===390&&document.documentElement.scrollWidth<=390');shot(m,'after-mobile');m.locator('#query').fill('서리 검사원');m.locator('[data-person]').tap();m.locator('#detail[open]').wait_for();shot(m,'after-character-mobile');m.locator('#detail .image-button').first.tap();m.wait_for_function('document.querySelector(".image-viewer img").naturalWidth>0');ratio(m,'.image-viewer img');shot(m,'after-portrait-mobile');m.locator('.image-viewer [data-zoom]').tap();m.locator('.viewer-stage').evaluate('e=>e.scrollTop=80');assert m.locator('.viewer-stage').evaluate('e=>e.scrollHeight>=e.clientHeight');m.locator('.image-viewer [data-close]').tap();m.wait_for_function('!document.querySelector(".image-viewer").open');m.locator('#close').tap();m.wait_for_timeout(150);m.locator('#query').fill('');m.locator('[data-tab=audio]').tap();m.evaluate('scrollTo(0,0)');shot(m,'after-audio-mobile');assert m.evaluate('document.documentElement.scrollWidth<=innerWidth')
 m.goto(BASE+'/reports/place-balance-01936/');m.locator('.gallery-grid').first.wait_for();assert m.evaluate('innerWidth===390&&document.documentElement.scrollWidth<=390');shot(m,'after-gallery-mobile');r=ratio(m,'figure img');assert abs(r['width']/r['height']-r['nw']/r['nh'])<.01;m.locator('figure .image-button').first.tap();m.wait_for_function('document.querySelector(".image-viewer img").naturalWidth>0');shot(m,'after-landscape-mobile');assert 'maximum-scale' not in m.locator('meta[name=viewport]').get_attribute('content');assert m.locator('.viewer-stage').evaluate('e=>getComputedStyle(e).touchAction') in ('auto','manipulation','pan-x pan-y pinch-zoom')
 # CDP pinch gesture checks Chromium's visual viewport rather than merely checking CSS.
 cdp=mobile.new_cdp_session(m);cdp.send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':2})
 def pinch_gesture(start,gaps):
  def points(g):return [{'x':195-g,'y':400,'id':0},{'x':195+g,'y':400,'id':1}]
  cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':points(start)})
  for gap in gaps:cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':points(gap)});m.wait_for_timeout(60)
  cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});m.wait_for_timeout(300)
 pinch_gesture(35,[45,55,65,80,100,120]);pinch=m.evaluate('visualViewport.scale');assert pinch>1,pinch
 pinch_gesture(120,[100,80,65,50,35,20]);assert m.evaluate('visualViewport.scale')<=1.1
 m.locator('.image-viewer [data-close]').tap();m.wait_for_function('!document.querySelector(".image-viewer").open')
 checks.append('390px mobile no overflow; touch zoom/scroll; actual two-finger pinch in/out and close')
 assert not errors,errors
 report={'status':'passed','source':'local checkout; public URLs blocked by proxy CONNECT 403','browser':b.version,'checks':checks,'page_errors':errors,'mobile_pinch_scale':pinch};(OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');b.close();print(json.dumps(report,ensure_ascii=False))
