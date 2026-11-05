"""실제 새 게임에서 중앙 좌석·표정·하차·저장 복원을 확인한다."""
import asyncio,json,os,sys
from pathlib import Path
os.environ.setdefault('ROOM13_QA_OUT','/tmp/room13-opening-web')
from qa_novel_adaptation import until,save_and_load,capture
from webqa import SayQA
from playwright.async_api import async_playwright
out=Path(os.environ['ROOM13_QA_OUT']);out.mkdir(exist_ok=True)
async def main():
 report={'scope':'첫 마차 실제 새 게임, PC·휴대폰 표시와 저장 복원','checks':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=SayQA(page,out);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function' && !document.getElementById('presplash')",timeout=180000)
   await q.wait('main_menu');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터')
   await until(q,text='일곱 개에서')
   before=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,bounds=renpy.exports.get_image_bounds("r13_visitor"),seat=s.r13_carriage_seat_shown)')
   assert 280<before['bounds'][0]<360,before
   await capture(q,'마차_중앙_PC');print('PC 확인',flush=True)
   await page.set_viewport_size({'width':844,'height':390});await capture(q,'마차_중앙_휴대폰');await page.set_viewport_size({'width':1280,'height':720})
   await save_and_load(q)
   after=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,bounds=renpy.exports.get_image_bounds("r13_visitor"),seat=s.r13_carriage_seat_shown)')
   assert before==after,(before,after);report['checks'].append('첫 마차 얼굴 중앙 위치·PC/휴대폰 표시·저장/불러오기 일치');print('저장 복원 확인',flush=True)
   await until(q,text='엄마 거야!')
   await capture(q,'마차_다른표정_PC')
   after=await q.py('import renpy;result=renpy.exports.get_image_bounds("r13_visitor")');assert before['bounds']==after
   await q.press('건너뛰기');await until(q,screen='r13_hub')
   assert await q.py('import renpy;s=renpy.store;result=s.place=="눈에 막힌 입구" and all(renpy.music.get_playing(channel=c) is None for c in ("carriage_ride","carriage_hooves","scene_fx","sound"))')
   report['checks'].append('표정 변경 위치 유지·건너뛰기 후 하차 효과 채널 무음')
   report['version']=await q.py('import renpy;result=renpy.store.config.version');assert report['version']=='0.20.98';assert not errors,errors
   report.update(status='passed',page_errors=errors)
  except Exception as e:
   report.update(status='failed',error=str(e)[:800],page_errors=errors);await page.screenshot(path=str(out/'실패.png'));raise
  finally:
   (out/'결과.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
 print(json.dumps(report,ensure_ascii=False),flush=True)
if __name__=='__main__':asyncio.run(main())
