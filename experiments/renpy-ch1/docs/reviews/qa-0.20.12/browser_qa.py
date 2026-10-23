import asyncio, json, sys, traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'dev'))
from webqa import QA
from playwright.async_api import async_playwright
OUT=Path(__file__).parent
URL='http://localhost:8766/'
async def run(mobile):
 tag='mobile' if mobile else 'pc'
 result={'화면':tag,'페이지오류':[],'캡처':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',args=['--no-sandbox','--enable-unsafe-swiftshader'])
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
   result['버전']=await q.py('import renpy;result=renpy.config.version')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터')
   for _ in range(400):
    st=await q.state()
    if 'r13_hub' in st['screens']:break
    if 'choice' in st['screens'] and any('편지를 접는다' in x['text'] for x in st['buttons']):await q.press('편지를 접는다');continue
    await q.input(640,300);await asyncio.sleep(.2)
   await q.wait('r13_hub');await check()
   result['자료수']=await q.py('import renpy\ns=renpy.store\nev=list(s.room13["evidence"])\nfor k in s.ROOM13["evidence"]:\n if k.startswith("V111:") and k not in ev:ev.append(k)\ns.r13_edit(evidence=ev)\nrenpy.exports.show_screen("r13_book")\nrenpy.exports.restart_interaction()\nresult=len(ev)')
   await q.wait('r13_book')
   # 긴 이름이 포함된 페이지와 모든 페이지의 이름 계산을 기록한다.
   result['자료이름']=await q.py('import renpy\ns=renpy.store\nsc=renpy.display.screen.get_screen("r13_book")\nentries=sc.scope["entries"]\nrows=[]\nfor k in entries:\n title=s.r13_evidence_short(k,24 if s.r13_touch_ui() else 20)\n rows.append(dict(key=k,name=s.R13_RECORD_SHORT.get(k) or s.r13_catalog_title(k),display=s.r13_ev_two_lines(title,116 if s.r13_touch_ui() else 76,18 if s.r13_touch_ui() else 14,2 if s.r13_touch_ui() else 3)))\nidx=next((i for i,k in enumerate(entries) if "첫 비명 뒤 핀" in (s.R13_RECORD_SHORT.get(k) or s.r13_catalog_title(k))),0)\ns.r13_record_select("r13_book","page",idx//s.r13_record_page_size(),False)\nrenpy.exports.restart_interaction()\nresult=rows')
   await shot('book-'+tag)
   await q.py('import renpy;renpy.exports.hide_screen("r13_book");renpy.exports.restart_interaction();result=True')
   if not mobile:
    result['장소']=[]
    for loc,day,per,edge,name in [('v111_woodshed',6,1,0,'woodshed-left'),('v111_woodshed',6,1,99999,'woodshed-right'),('v111_woodshed',6,2,0,'woodshed-evening'),('facility',11,1,0,'facility-left'),('facility',11,1,99999,'facility-right')]:
     data=await q.py('import renpy\ns=renpy.store\ns.r13_edit(location=%r,day=%d,period=%d)\ns.r13_world_cameras=dict(s.r13_world_cameras,**{%r:%d})\nrenpy.exports.restart_interaction()\nresult=dict(location=s.room13["location"],period=s.room13["period"],width=s.r13_world_width(),offset=s.r13_world_offset(),maximum=s.r13_camera_range())'%(loc,day,per,loc,edge))
     result['장소'].append(data);await shot(name)
   before=await q.py('import renpy;s=renpy.store;result=dict(day=s.room13["day"],location=s.room13["location"],period=s.room13["period"])')
   st=await q.state();result['저장전버튼']=[x['text'] for x in st['buttons']]
   await q.press('설정');await q.wait('pause_menu');await shot('settings-'+tag)
   await q.press('저장');await q.wait('save');await q.press('1쪽 1번');await asyncio.sleep(1)
   if 'confirm' in (await q.state())['screens']:await q.press('예')
   await shot('saved-'+tag)
   result['저장가능']=await q.py('import renpy;result=renpy.exports.can_load("1-1")')
   await asyncio.sleep(3);await pg.reload();await pg.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
   await q.press('불러오기');await q.wait('load');await q.press('1쪽 1번');await asyncio.sleep(1)
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
asyncio.run(main())
