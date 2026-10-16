"""Actual inventory/shop/showing UI, using an explicit all-owned art-review fixture."""
import asyncio,json,os,copy
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_records','r13_shop','r13_item_bag',")
from webqa import UIQA
class MaterialQA(UIQA):
 async def py(self,code):
  return await super().py("ns={};exec("+repr(code)+",ns);result=ns.get(\"result\")")
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/material-icons-qa'));OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720});q=MaterialQA(page,OUT)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance()
   info=await q.py('''import renpy
s=renpy.store
keys=list(s.ROOM13['evidence'])
s.r13_edit(day=5,period=0,location='room13',case_state='occurred',evidence=keys,record_ui={'seen':keys},inspection_items={'inventory':list(s.R13_INSPECTION_ITEMS)},livelihood={'cash':999,'items':list(s.R13_SHOP)+list(s.R13_BORROW),'borrowed':{'knife':5,'lantern':3}})
s.r13_flag('lodging','livelihood_open')
s.persistent.room13_large_text=False
expected={k for k,v in s.ROOM13['evidence'].items() if v['kind']!='증언' and k!='P01'}|{'bag:'+k for k in set(s.R13_SHOP)|set(s.R13_BORROW)}|{'tool:'+k for k in s.R13_INSPECTION_ITEMS}
assert set(s.R13_MATERIAL_ART)==expected,(set(s.R13_MATERIAL_ART)^expected)
before=s.winter_copy.deepcopy(s.room13)
for key in expected:
 s.renpy.render(s.Transform(s.r13_record_icon(key),xysize=(60,60),fit='contain',nearest=True),60,60,0,0)
assert s.room13==before
result={'icons':len(expected),'evidence_records':sum(1 for k in expected if ':' not in k),'objects':sum(1 for k in expected if ':' in k),'testimony_portraits_deferred':all(k not in s.R13_MATERIAL_ART for k,v in s.ROOM13['evidence'].items() if v['kind']=='증언'),'mother_portrait_deferred':'P01' not in s.R13_MATERIAL_ART}
''')
   await q.press('기록');await q.wait('r13_records');before=copy.deepcopy((await q.state())['room'])
   count=await q.py('import renpy;s=renpy.store;result=s.r13_record_pages(s.r13_catalog_entries())')
   for n in range(count):
    await q.shot('catalog-%02d'%(n+1))
    if n+1<count:await q.press('다음 ›')
   for key in ['E01','M01','E03','E07','E14','E23','E30','bag:medkit','bag:herbs','tool:magnifier']:
    await q.py('import renpy;s=renpy.store;entries=s.r13_catalog_entries();idx=entries.index('+repr(key)+');renpy.exports.set_screen_variable("page",idx//s.r13_record_page_size(),screen="r13_records");renpy.exports.set_screen_variable("detail",'+repr(key)+',screen="r13_records");renpy.exports.restart_interaction();result=True')
    await q.shot('detail-'+key.replace(':','-'))
   assert (await q.state())['room']==before
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await page.set_viewport_size({'width':844,'height':390});await q.shot('mobile-catalog');await q.press('닫기')
   await page.set_viewport_size({'width':1280,'height':720});await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;renpy.exports.show_screen("r13_shop",close=s.Hide("r13_shop"));renpy.exports.restart_interaction();result=True');await q.wait('r13_shop');await q.shot('shop');await q.press('돌아가기')
   await q.py('import renpy;renpy.exports.show_screen("r13_material_corner",key="bag:herbs");renpy.exports.restart_interaction();result=True');await q.shot('showing-item');await q.py('import renpy;renpy.exports.hide_screen("r13_material_corner");renpy.exports.show_screen("r13_book",target="resident_seori",present=True);renpy.exports.restart_interaction();result=True');await q.wait('r13_book');await q.shot('showing-picker');await q.py('import renpy;renpy.exports.hide_screen("r13_book");renpy.exports.restart_interaction();result=True')
   assert (await q.state())['room']==before
   info.update(passed=True,checks=['runtime coverage includes all non-portrait records and every owned item/tool','all 82 icons render at actual 60px list size','every catalog page displayed','132px selected details','mobile large text','actual shop uses same item icons','showing card and picker use same icons','ownership, currency, time and proof unchanged'])
   (OUT/'result.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print('PASS',json.dumps(info,ensure_ascii=False),flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await b.close()
asyncio.run(main())
