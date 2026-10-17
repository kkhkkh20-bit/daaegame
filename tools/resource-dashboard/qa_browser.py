"""Real Chromium QA of the read-only dashboard; no game state is modified."""
import json, os
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(os.environ.get('DASHBOARD_QA_OUT','reports/resource-dashboard-20261017'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('DASHBOARD_URL','http://127.0.0.1:8765/preview/resource-dashboard/')
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1365,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.locator('[data-person]').first.wait_for();page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
 assert page.locator('[data-person]').count()>50;checks.append('real generated characters loaded')
 page.locator('#query').fill('resident_seori');assert page.locator('[data-person]').count()==1
 page.locator('[data-person]').first.click();page.locator('dialog[open]').wait_for();assert 'resident_seori' in page.locator('#detail-title').inner_text()
 page.screenshot(path=str(OUT/'seori-detail.png'));page.keyboard.press('Escape');page.wait_for_function('!document.querySelector("dialog").open');page.wait_for_timeout(150)
 assert page.evaluate('document.activeElement.dataset.person')=='resident_seori';checks.append('search, detail, Escape and focus restoration')
 for _ in range(3):
  page.locator('[data-person]').first.click();page.locator('dialog[open]').wait_for();page.go_back();page.wait_for_function('!document.querySelector("dialog").open')
 checks.append('repeated detail open and browser Back')
 page.locator('#query').fill('');page.locator('#place').select_option('market');assert page.locator('[data-person]').count()>0;page.locator('#day').select_option('14');page.locator('#period').select_option('1');checks.append('place/day/period filter')
 page.locator('#place').select_option('');page.locator('#day').select_option('');page.locator('#period').select_option('')
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth');page.locator('[data-person]').first.click();page.locator('dialog[open]').wait_for();assert page.evaluate('document.querySelector("dialog").scrollWidth <= document.querySelector("dialog").clientWidth')
 page.screenshot(path=str(OUT/'mobile-detail.png'));page.locator('#close').click();checks.append('390px mobile layout and popup overflow')
 page.set_viewport_size({'width':1365,'height':1000});page.locator('[data-tab=places]').click();assert page.locator('table').count()>0;page.screenshot(path=str(OUT/'places.png'),full_page=True);page.locator('#place').select_option('kitchen');page.locator('#day').select_option('3');assert 'map31_nabi_stir_pot' in page.locator('#content').inner_text();assert 'map31_nabi_ladle_soup' not in page.locator('#content').inner_text();page.locator('#place').select_option('');page.locator('#day').select_option('');checks.append('place overview with stable pose IDs and sparse day conditions')
 page.locator('[data-tab=audio]').click();page.locator('#query').fill('sfx-click');controls=page.locator('[data-audio]');assert controls.count()>=2
 assert page.evaluate('[...audioInstances].every(a=>a.paused)')
 controls.nth(0).locator('[data-action=play]').click();page.wait_for_function('Array.from(document.querySelectorAll("[role=status]")).some(e=>e.textContent==="재생 중")');checks.append('user-click real WAV playback')
 controls.nth(1).locator('[data-action=play]').click();page.wait_for_timeout(200);assert page.locator('[data-audio] [role=status]').all_text_contents().count('재생 중')<=1
 controls.nth(1).locator('[data-action=pause]').click();controls.nth(1).locator('input').fill('0.2');controls.nth(1).locator('[data-action=stop]').click();assert controls.nth(1).locator('[role=status]').inner_text()=='정지';assert page.evaluate('[...audioInstances].every(a=>a.paused)');checks.append('exclusive playback, pause, volume and stop')
 page.locator('#query').fill('bgm-title.mp3');page.locator('[data-audio]').first.locator('[data-action=play]').click();page.wait_for_function('[...audioInstances].some(a=>!a.paused && a.currentTime>0)');page.locator('[data-audio]').first.locator('[data-action=stop]').click();checks.append('real MP3 BGM playback')
 page.locator('#query').fill('');page.set_viewport_size({'width':1365,'height':1000});page.screenshot(path=str(OUT/'audio.png'),full_page=False)
 page.route('**/sfx-click.wav',lambda route:route.fulfill(status=404,body='missing'));page.locator('#query').fill('sfx-click');page.locator('[data-audio]').first.locator('[data-action=play]').click();page.wait_for_timeout(700);status=page.locator('[data-audio]').first.locator('[role=status]').inner_text();assert '오류' in status or '실패' in status,status;checks.append('missing audio 404 error feedback')
 page.unroute('**/sfx-click.wav');page.route('**/sfx-click.wav',lambda route:route.fulfill(status=200,content_type='audio/wav',body='invalid audio'));page.locator('#query').fill('page');page.locator('#query').fill('sfx-click');page.locator('[data-audio]').first.locator('[data-action=play]').click();page.wait_for_timeout(700);assert any(x in page.locator('[data-audio]').first.locator('[role=status]').inner_text() for x in ('오류','실패'));checks.append('unsupported audio payload feedback')
 page.locator('#refresh').click();page.wait_for_function('document.querySelector("#summary").textContent.includes("최신 데이터")');checks.append('refresh version check')
 updated=page.evaluate('JSON.parse(JSON.stringify(data))');updated['data_version']='qa-next-version';page.route('**/version.json?*',lambda route:route.fulfill(json={k:updated[k] for k in ('schema','game_commit','data_version','generated_at')}));page.route('**/data.json?*',lambda route:route.fulfill(json=updated));page.locator('#refresh').click();page.wait_for_function('document.querySelector("#version").textContent.includes("qa-next-vers")');checks.append('new deployed version detection and reload')
 page2=b.new_page(viewport={'width':390,'height':844});page2.route('**/thumbs/**',lambda route:route.fulfill(status=404,body='missing'));page2.goto(URL);page2.locator('.portrait .error').first.wait_for();checks.append('missing image error feedback');page2.close()
 assert not errors,errors
 (OUT/'browser-report.json').write_text(json.dumps({'status':'passed','url':URL,'browser':b.version,'checks':checks,'page_errors':errors},ensure_ascii=False,indent=2)+'\n');b.close();print(json.dumps(checks,ensure_ascii=False))
