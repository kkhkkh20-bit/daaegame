"""자료 UI의 실제 터치·스크롤·상태 보존 검사. 자료 보유 상태는 명시적인 검수용 fixture."""
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa/evidence-readability'))
URL = os.environ.get('ROOM13_URL', 'http://127.0.0.1:8765/preview/room13-dev/')
OUT.mkdir(parents=True, exist_ok=True)

class EvidenceQA(UIQA):
 async def py(self, code):
  return await super().py("ns={};exec("+ascii(code)+",ns);result=ns.get('result')")

async def main():
 async with async_playwright() as p:
  browser = await p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox', '--enable-unsafe-swiftshader'])
  page = await browser.new_page(viewport={'width':1280,'height':720}, has_touch=True)
  q = EvidenceQA(page, OUT)
  page_errors=[]
  page.on('pageerror',lambda error:page_errors.append(str(error)))
  try:
   await page.goto(URL)
   await page.wait_for_function("typeof renpy_exec==='function'", timeout=150000)
   await q.wait('main_menu')
   await q.press('처음부터')
   await q.wait('say')
   await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=[k for k in s.ROOM13["evidence"] if k.startswith("V111:")]);renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True')
   before = (await q.state())['room']
   # Existing authored records with the longest reading load, not invented facts.
   worst = await q.py('import renpy;s=renpy.store;result=sorted(s.r13_catalog_entries(),key=lambda k:len(s.r13_catalog_title(k))+sum(len(x) for x in s.r13_evidence_facts(k)),reverse=True)[:2]')
   # Render every current title and icon through the engine, not a width estimate.
   asset_check=await q.py('''import renpy
s=renpy.store
keys=[k for k in s.ROOM13["evidence"] if k.startswith("V111:")]
rows=[]
for key in keys:
 picture=s.r13_evidence_picture(key,60)
 rendered=renpy.display.render.render(picture,60,60,0,0)
 heights=[]
 for size in (18,22,24):
  label=s.r13_ev_two_lines(s.r13_catalog_title(key),174,size,3)
  text=renpy.text.text.Text(label,font=s.r13_ui_font(),size=size,xsize=174,line_spacing=-1)
  w,h=renpy.display.render.render(text,174,88,0,0).get_size()
  assert h<=88 and w<=174,(key,size,w,h,label)
  assert "…" not in label,(key,label)
  heights.append(h)
 rows.append(dict(key=key,title=s.r13_catalog_title(key),picture=list(rendered.get_size()),title_heights=heights))
assert len(rows)==80,len(rows)
result=rows
''')
   (OUT/'all-evidence-render.json').write_text(json.dumps(asset_check,ensure_ascii=False,indent=2))
   measurements=[]
   for touch in (False, True):
    await page.set_viewport_size({'width':844,'height':390} if touch else {'width':1280,'height':720})
    q.touch=touch
    for large in (False, True):
     prefix=('mobile' if touch else 'desktop')+('-large' if large else '-normal')
     await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text='+str(large)+';sc=renpy.display.screen.get_screen("r13_records");sc.scope.update(detail=None,page=0,pair=None);renpy.exports.restart_interaction();result=True')
     # Old remembered page and full long title are exercised in the same actual list.
     await q.py('import renpy;s=renpy.store;sc=renpy.display.screen.get_screen("r13_records");entries=s.r13_catalog_entries();sc.scope.update(page=s.r13_compare_page(entries,"V111:NW_BURNT_PAGE"),detail="V111:NW_BURNT_PAGE");renpy.exports.restart_interaction();result=True')
     await q.shot(prefix+'-burnt-page')
     await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");sc.scope.update(page=0,detail=None);renpy.exports.restart_interaction();result=True')
     await q.input(90,185)
     await q.shot(prefix+'-single')
     await q.press('출처 펼치기');await q.press('출처 접기')
     await q.press('나란히 놓기');await q.input(90,270)
     await q.shot(prefix+'-pair')
     pair=await q.py('import renpy;result=list(renpy.display.screen.get_screen("r13_records").scope["pair"])')
     assert all(pair) and pair[0]!=pair[1],pair
     await q.press('자리 바꾸기')
     assert await q.py('import renpy;result=list(renpy.display.screen.get_screen("r13_records").scope["pair"])')==pair[::-1]
     # Page navigation and slot replacement through actual input.
     await q.press('번 바꾸기');await q.press('›');await q.input(90,185)
     await q.press('한 장만 보기')
     scope=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result={k:sc.scope[k] for k in ("detail","page","pair")}')
     assert scope['pair'] is None and scope['detail']
     await q.press('‹')
     # The toughest existing pair must remain inside a bounded reading viewport.
     await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");sc.scope["pair"]='+repr(tuple(worst))+';renpy.exports.restart_interaction();result=True')
     await q.shot(prefix+'-long-pair')
     measure=await q.py('''import renpy
s=renpy.store
sc=renpy.display.screen.get_screen("r13_records")
seen=set();views=[]
def walk(w):
 if id(w) in seen:return
 seen.add(id(w))
 if isinstance(w,renpy.display.layout.Viewport):views.append(dict(range=w.yadjustment.range,page=w.yadjustment.page,value=w.yadjustment.value))
 for c in w.visit():walk(c)
walk(sc)
result=dict(fact=s.r13_ev_fact_size(),button=s.r13_ev_button_height(),views=views)
''')
     if touch:
      assert measure['fact']*390/720>=16,measure
      assert measure['button']*390/720>=44,measure
      controls=[b for b in (await q.state())['buttons'] if any(x in b['text'] for x in ('한 장만 보기','자리 바꾸기','번 바꾸기'))]
      assert len(controls)==3 and all(b['rect'][3]*390/720>=44 and b['rect'][1]+b['rect'][3]<=670 for b in controls),controls
      # A finger drag on each reading column moves long content without moving the fixed footer.
      for x in (550,1000):
       scale=390/720;offset=(844-1280*scale)/2
       client=await page.context.new_cdp_session(page)
       await client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':offset+x*scale,'y':500*scale}]})
       await client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':offset+x*scale,'y':230*scale}]})
       await client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
       await client.detach()
     else:
      await page.mouse.move(1000,400);await page.mouse.wheel(0,700)
     scrolled=await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");seen=set();views=[]\ndef walk(w):\n if id(w) in seen:return\n seen.add(id(w))\n if isinstance(w,renpy.display.layout.Viewport):views.append(dict(range=w.yadjustment.range,value=w.yadjustment.value))\n for c in w.visit():walk(c)\nwalk(sc)\nresult=views')
     if touch:
      assert all(v['value']>0 for v in scrolled if v['range']>0),scrolled
     measure['after_scroll']=scrolled
     await q.shot(prefix+'-long-scrolled')
     measure['mode']=prefix;measurements.append(measure)
   # Maximum filter combination is a layout fixture, not a claim that an ordinary run exposes every archive.
   await q.py('import renpy;s=renpy.store;s._qa_filter_chips=s.r13_ev_filter_chips;s.r13_ev_filter_chips=lambda *a,**kw:[(label,False,s.NullAction()) for label in ("전체","증언","전달 가능","지난 사건","지난 플레이")];renpy.exports.restart_interaction();result=True')
   await q.shot('mobile-large-all-filters')
   chips=[b for b in (await q.state())['buttons'] if b['text'].strip() in ('전체','증언','전달 가능','지난 사건','지난 플레이')]
   assert len(chips)==5 and min(b['rect'][0] for b in chips)>=616,chips
   assert all(b['rect'][2]*390/720>=44 and b['rect'][3]*390/720>=44 for b in chips),chips
   await q.py('import renpy;s=renpy.store;s.r13_ev_filter_chips=s._qa_filter_chips;renpy.exports.restart_interaction();result=True')
   # UI use may mark records read; no evidence, clock, branch or inventory mutation.
   after=(await q.state())['room']
   assert {k:v for k,v in before.items() if k!='record_ui'}=={k:v for k,v in after.items() if k!='record_ui'}
   await q.input(1210,58)
   await q.py('import renpy;renpy.exports.show_screen("r13_book",target="buri",present=True);renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book');await q.input(90,185);await q.shot('mobile-present')
   await q.press('출처 펼치기');await q.press('출처 접기')
   await q.input(1210,58)
   await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=[]);s.r13_records_view={};renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True')
   await q.shot('mobile-empty')
   await q.input(1210,58)
   await page.set_viewport_size({'width':390,'height':844});await q.shot('portrait-rotation')
   assert not page_errors,page_errors
   result={'page_errors':page_errors,'passed':True,'version':(await q.info())['version'],'scope':'오프닝 실제 진입, 자료 화면은 보유 상태를 구성한 검수','worst_existing_records':worst,'measurements':measurements,'world_state_preserved':True}
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False),flush=True)
  finally:await browser.close()

if __name__=='__main__':asyncio.run(main())
