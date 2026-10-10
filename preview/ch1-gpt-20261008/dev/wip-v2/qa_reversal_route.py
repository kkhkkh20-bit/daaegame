"""Prepared-state actual pointer check: related evidence routes to native proof."""
from playwright.sync_api import sync_playwright
import shutil
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 page=b.new_page(viewport={'width':844,'height':390});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8000/playT.html');page.wait_for_timeout(16000)
 page.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''')
 page.wait_for_timeout(1200)
 page.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};G.found=["C01","C02","C04"];G.asked=["C03"];G.exam={};allSpots(CASES[G.ci]).forEach(s=>G.exam[s.ev.id]=true);G.beats.inn_meeting_version=2;G.beats.inn_life_confirmed=1;G.debate={pi:3,sus:{}};window.__rtgReset();window.__rtOpen(CASES[G.ci])')''')
 page.wait_for_timeout(2200)
 for _ in range(6):
  if page.locator('.rt-bub.stm em').inner_text().startswith('3'):break
  page.locator('#rtgbar [data-g="next"]').click();page.wait_for_timeout(700)
 assert page.locator('.rt-bub.stm em').inner_text().startswith('3'),page.locator('.rt-bub.stm').inner_text()
 page.locator('#rtgbar [data-g="ev"]').click();page.wait_for_timeout(200)
 page.locator('.rt [data-bl="C02"]').click();page.wait_for_timeout(200)
 page.locator('#rtgbar [data-g="present"]').click()
 for _ in range(30):
  if page.locator('.rt-bub.stm').count() and page.locator('.rt-bub.stm em').inner_text().startswith('2') and not page.locator('#rtgq').count():break
  if page.locator('#rtgq').count() and page.locator('#rtgq').is_visible():page.locator('#rtgq').click()
  elif page.locator('#rtgbar [data-g="next"]').is_visible():page.locator('#rtgbar [data-g="next"]').click()
  else:break
  page.wait_for_timeout(250)
 assert page.evaluate('window.__T("G.hp===5&&G.wrong===0")')
 assert page.locator('.rt-bub.stm em').inner_text().startswith('2'),page.locator('.rt-bub.stm').inner_text()
 assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==0
 if not page.evaluate('document.body.classList.contains("rtg-drw")'):page.locator('#rtgbar [data-g="ev"]').click()
 page.locator('.rt [data-bl="C02"]').click();page.wait_for_timeout(250)
 page.locator('#rtgbar [data-g="present"]').click();page.wait_for_timeout(250)
 assert not page.locator('#logic-panel').count()
 assert page.evaluate('window.__rtgStep(window.__rtPh().stms[1])')==1
 assert not page.locator('.rt .bl.on').count()
 assert page.evaluate('window.__T("G.debate.pi")')==3
 assert page.evaluate('window.__T("G.hp===5&&G.wrong===0")')
 assert not errors,errors
 print('Related clue on Seryeon claim → Nabi native proof; explicit first observation, no auto completion or wrongful damage, errors 0',flush=True)
 b.close()
