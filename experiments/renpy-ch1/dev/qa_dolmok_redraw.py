"""새 게임의 첫 돌목 대화·표정·저장 복원·질문을 PC와 휴대폰에서 확인한다."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import SayQA
from qa_novel_adaptation import until,save_and_load
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/dolmok-web'));OUT.mkdir(parents=True,exist_ok=True)
async def run(q,code):return await q.py('ns={};exec('+repr(code)+',ns);result=ns["result"]')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},has_touch=True)
  q=SayQA(page,OUT);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
   await q.wait('main_menu');await run(q,'import renpy;renpy.store.preferences.text_cps=0;result=True')
   await q.press('처음부터');await until(q,text='흠흠.')
   before=await run(q,'import renpy;s=renpy.store;result=dict(packet=s.r13_packet,pose=s.r13_current_pose,person=s.r13_motion_person,version=s.config.version,files={h:{k:f["file"] for k,f in p["frames"].items()} for h,p in s.r13_dialogue_player_profiles("guard").items()})')
   assert before['packet'][0]=='guard' and before['person']=='guard',before
   assert all('dialogue-player-facing/' in f for p in before['files'].values() for f in p.values()),before
   await asyncio.sleep(1);await page.screenshot(path=str(OUT/'돌목_대화_PC.png'))
   await page.set_viewport_size({'width':844,'height':390});await page.screenshot(path=str(OUT/'돌목_대화_휴대폰.png'))
   await page.set_viewport_size({'width':1280,'height':720})
   await save_and_load(q)
   after=await run(q,'import renpy;s=renpy.store;result=dict(packet=s.r13_packet,pose=s.r13_current_pose,person=s.r13_motion_person)')
   assert all(after[k]==before[k] for k in after),[before,after]
   for pose,name in [('joy','웃음'),('angry','화남'),('anxious','걱정'),('flustered','당황'),('surprise','놀람')]:
    await run(q,'import renpy;s=renpy.store;s.r13_dialogue_beat=None;s.r13_speaker("guard",'+repr(pose)+','+repr(pose)+');renpy.exports.restart_interaction();result=True')
    await asyncio.sleep(.8);await page.screenshot(path=str(OUT/('돌목_'+name+'.png')))
   await run(q,'import renpy;s=renpy.store;renpy.exports.hide("r13_visitor");renpy.exports.hide_screen("say");renpy.exports.show_screen("r13_question_list",person="guard",pose="neutral",title="질문",entries=[("입구 등록에 관해",s.NullAction(),False)],ready=True);renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.5);await page.screenshot(path=str(OUT/'돌목_질문_PC.png'))
   await page.set_viewport_size({'width':844,'height':390});await page.screenshot(path=str(OUT/'돌목_질문_휴대폰.png'))
   assert not errors,errors
   report=dict(status='통과',version=before['version'],portrait=before,save_restored=after,checks=['새 게임 첫 돌목 실제 대화','PC·휴대폰 표시','현재 판 저장·불러오기','실제 표현 별칭으로 표정 5종 렌더 fixture','질문 화면 fixture'],pageerrors=errors)
   (OUT/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False),flush=True)
  finally:await browser.close()
if __name__=='__main__':asyncio.run(main())
