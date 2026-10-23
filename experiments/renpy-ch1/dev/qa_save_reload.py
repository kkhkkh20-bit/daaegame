"""처음부터 입구까지 진행한 뒤 PC/터치 저장·새로고침·불러오기 확인."""
import asyncio, json, os, traceback
from pathlib import Path
from webqa import UIQA as QA
from playwright.async_api import async_playwright
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/save-reload'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')
async def run(mobile):
 tag='mobile' if mobile else 'pc'
 result={'화면':tag,'페이지오류':[],'캡처':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
  ctx=await b.new_context(viewport={'width':844 if mobile else 1280,'height':390 if mobile else 720},device_scale_factor=2 if mobile else 1,is_mobile=mobile,has_touch=mobile)
  pg=await ctx.new_page(); q=QA(pg,OUT); q.touch=mobile
  pg.on('pageerror',lambda e:result['페이지오류'].append(str(e)))
  async def check():
   assert not await q.py("import renpy;result=renpy.display.screen.get_screen('_exception') is not None"),'Ren’Py 예외 화면'
   assert not result['페이지오류'],result['페이지오류']
  async def shot(name):
   await asyncio.sleep(1.5);await check();await pg.screenshot(path=str(OUT/(name+'.png')));result['캡처'].append(name+'.png')
  try:
   await pg.goto(URL);await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
   print(tag,'시작 화면 확인',flush=True)
   result['버전']=await q.py('import renpy;result=renpy.config.version')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터')
   for _ in range(400):
    st=await q.state()
    if 'r13_hub' in st['screens']:break
    if 'choice' in st['screens'] and any('편지를 접는다' in x['text'] for x in st['buttons']):await q.press('편지를 접는다');continue
    await q.input(640,300);await asyncio.sleep(.2)
   await q.wait('r13_hub');await check();print(tag,'입구 도착',flush=True)
   before=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],location=s.room13["location"],period=s.room13["period"])')
   st=await q.state();result['저장전버튼']=[x['text'] for x in st['buttons']]
   await q.input(1222,52);await q.press('설정');await q.wait('pause_menu');await shot('settings-'+tag);print(tag,'설정 진입',flush=True)
   await q.press('저장');await q.wait('save');await q.press('1쪽 1번');await asyncio.sleep(1)
   if 'confirm' in (await q.state())['screens']:await q.press('예')
   await shot('saved-'+tag);print(tag,'저장 완료',flush=True)
   result['저장가능']=await q.py('import renpy;result=renpy.exports.can_load("1-1")')
   await asyncio.sleep(3);await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
   print(tag,'새로고침 완료',flush=True);await q.press('불러오기');await q.wait('load');await q.press('1쪽 1번');await asyncio.sleep(1)
   if 'confirm' in (await q.state())['screens']:await q.press('예')
   await asyncio.sleep(3);await check()
   after=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],location=s.room13["location"],period=s.room13["period"])')
   result['저장복원']={'저장전':before,'복원후':after,'일치':before==after};assert before==after
   await shot('loaded-'+tag);result['결과']='통과'
  except Exception:
   result['결과']='실패';result['오류']=traceback.format_exc();await pg.screenshot(path=str(OUT/('error-'+tag+'.png')))
  finally:
   (OUT/('browser-'+tag+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));print(tag,result['결과'],result.get('오류',''),flush=True);await b.close()
async def main():
 for mobile in (False,True):
  try:await run(mobile)
  except Exception:
   tag='mobile' if mobile else 'pc'
   error={'화면':tag,'결과':'실행 환경 오류로 확인 불가','오류':traceback.format_exc()}
   (OUT/('browser-'+tag+'.json')).write_text(json.dumps(error,ensure_ascii=False,indent=2))
   print(tag,error['오류'],flush=True)
 for tag in ('pc','mobile'):
  if json.loads((OUT/('browser-'+tag+'.json')).read_text()).get('결과')!='통과':
   raise SystemExit(1)

if __name__=='__main__':asyncio.run(main())
