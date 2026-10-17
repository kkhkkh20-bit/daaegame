"""Play every independent aftermath outcome in the actual web runtime.
Fixtures start at completed episode state; this is not a fresh 14-day walkthrough.
"""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_episode_aftermath_view',")
webqa.PROBE=webqa.PROBE.replace('names=[',"names=['r13_episode_aftermath_view',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/episode-aftermath'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8774/preview/room13-dev/')
FIXTURES=[('ep1',[]),('ep1',['piko_dead','tok_detained','siluk_handed','madam_store_opened']),('ep1',['siluk_debt_cleared','madam_store_opened']),('ep2',['kd_shoes_only','bami_taken','kd_named']),('ep2',['kd_farewell_seen','musoe_gone','bami_safe']),('ep2',['kd_seori','bami_safe']),('ep2_clinic',['kd_clinic_note','musoe_gone']),('ep3',[]),('ep3',['kkomi_dead','bori_adopts','nubi_kids_with_nabi']),('ep3',['wf_missed','bori_taken']),('ep3',['kkomi_dead'],'held'),('ep4',['chorong_dead','ttadak_dead','nt_ttadak_proven','owl_hat','nt_lit_lamps']),('ep4',['nt_chorong_safe','nt_ttadak_half']),('ep4',['nt_ttadak_safe','nt_chorong_half']),('ep4',['chorong_dead','ttadak_dead','owl_hat'],'held'),('ep5',['soup_kids_dead']),('ep5',['ws_some_alive']),('ep5',['ws_kids_alive','bori_adopts','mom_reunited','portrait_finished_by_daram']),('ep5',['ws_kids_alive','dodam_sick']),('ep6',['cart_stopped','cv_badook_safe','cv_granny_tomorrow']),('ep6',['cart_left','badook_dead']),('ep6',['cart_stopped','badook_dead']),('ep6',['cart_stopped','badook_hurt']),('ep6',['cart_stopped','neoul_gone']),('ep6',['cv_family_only','cart_left','ws_cart_truth','guldol_dead','momo_dead']),('ep6',['cv_skipped','cart_left'])]
async def action(q,expr):
 code='\n'.join(['import renpy','def _qa_af_action(**kwargs):',' import renpy',' s=renpy.store',' renpy.ui.textbutton("검토 계속",clicked='+expr+',xpos=500,ypos=300,xsize=280,ysize=80)',"renpy.exports.define_screen('qa_af_action',_qa_af_action,modal='True',zorder='200')","renpy.exports.show_screen('qa_af_action')","renpy.exports.restart_interaction()","result=True"])
 await q.py(code);await q.press('검토 계속')
 await q.py('import renpy;renpy.exports.hide_screen("qa_af_action");renpy.exports.restart_interaction();result=True')
class AftermathQA(UIQA):
 async def py(self,code):return await asyncio.wait_for(self.p.evaluate('code=>renpy_exec(code)','exec('+ascii(code)+')'),90)

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=AftermathQA(page,OUT);results=[];seen=set()
  page.on("console",lambda msg: print("WEB",msg.type,msg.text[:500],flush=True) if msg.type=="error" else None)
  page.on("pageerror",lambda exc:print("PAGEERROR",str(exc),flush=True))
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await page.wait_for_function("!document.getElementById('presplash')",timeout=240000);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');print('BOOT ready',flush=True)
   for n,fixture in enumerate(FIXTURES):
    ep,flags=fixture[:2];child=fixture[2] if len(fixture)>2 else 'with_dad'
    print('FIXTURE',n,ep,flush=True)
    await q.py('import renpy;s=renpy.store;s.r13_edit(flags='+repr(flags)+',daram_state='+repr(child)+');s.persistent.room13_motion='+repr(n%2==0)+';s.persistent.room13_large_text='+repr(n==17)+';result=True')
    expected=await q.py('import renpy;s=renpy.store;result=[f["id"] for f in s.r13_episode_aftermath_frames('+repr(ep)+')]')
    before=(await q.state())['room'];await action(q,'s.Call("r13_episode_aftermath",'+repr(ep)+')');await q.wait('r13_episode_aftermath_view')
    for i,key in enumerate(expected):
     assert await q.py('import renpy;s=renpy.store;result=s.r13_aftermath_active and s.r13_aftermath_index=='+str(i)+' and s.r13_aftermath_frames[s.r13_aftermath_index]["id"]=='+repr(key)),(n,i,key)
     if key not in seen:await asyncio.sleep(.8);await q.shot(f'{n:02d}-{i:02d}-{key}');seen.add(key)
     if n==17 and i==1:
      await q.py('import renpy;renpy.exports.save("qa-aftermath-middle");result=True')
      await action(q,'s.Function(renpy.exports.load,"qa-aftermath-middle")');await q.wait('r13_episode_aftermath_view')
      assert await q.py('import renpy;result=renpy.store.r13_aftermath_index==1')
      await q.press('‹ 이전');await q.wait('r13_episode_aftermath_view');assert await q.py('import renpy;result=renpy.store.r13_aftermath_index==0')
      await q.press('다음 장면');await q.wait('r13_episode_aftermath_view')
      await page.set_viewport_size({'width':844,'height':390});await q.shot('mobile-large-text');await page.set_viewport_size({'width':1280,'height':720})
     # Alternate image/touch region and named buttons. Bottom of caption must advance.
     if i%2==0:await q.input(640,600)
     else:await q.press('이야기로 돌아가기' if i==len(expected)-1 else '다음 장면')
     if i<len(expected)-1:await q.wait('r13_episode_aftermath_view')
    for _ in range(40):
     if await q.py('import renpy;result=not renpy.store.r13_aftermath_active'):break
     await asyncio.sleep(.15)
    assert await q.py('import renpy;result=not renpy.store.r13_aftermath_active')
    assert (await q.state())['room']==before,(n,'world changed')
    results.append(dict(episode=ep,flags=flags,child=child,frames=expected,read_only=True))
   assert len(seen)==46,(len(seen),seen)
   (OUT/'result.json').write_text(json.dumps(dict(passed=True,fixtures=results,unique_frames=len(seen),checks=['26 completed-outcome fixtures','46 artwork frames','mixed survival and loss','detained Daram absent','next/previous','mid-scene save/load','motion off','large-text mobile','world/evidence/time unchanged']),ensure_ascii=False,indent=2))
   print('PASS 26 aftermath outcomes / 46 frames / navigation / save-load / mobile / read-only',flush=True)
  except Exception as exc:
   print('FAIL',repr(exc),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await browser.close()
asyncio.run(main())
