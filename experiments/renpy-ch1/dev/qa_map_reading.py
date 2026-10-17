"""Owned-only material filters and real record/relation round-trip; UI fixtures."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
import webqa
webqa.FLOW_PROBE=webqa.FLOW_PROBE.replace('names=[',"names=['r13_records',")
from webqa import UIQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/material-reading-browser'));OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=UIQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8773/preview/room13-dev/'));await page.wait_for_function("typeof renpy_exec==='function'",timeout=150000);await q.wait('main_menu')
   await q.press('처음부터');await q.press('건너뛰기');await q.wait('say');await q.press('건너뛰기');await q.advance();await q.wait('r13_hub')
   await q.py('import renpy;s=renpy.store;s.r13_edit(evidence=["E01","E06","E10","E12"],encounters=[dict(person=p,day=2,period=0,place="square") for p in ("daram","bami","nabi")]);renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_records');await q.press('증언')
   assert set(await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["entries"]'))=={'E06','E10','E12'}
   await q.input(350,200);await q.shot('01-testimony-filter')
   await q.press('나비 · 관계도');await q.shot('02-source-relation')
   assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["rel_sel"]')=='nabi'
   await q.press('공구 운반공백');await q.shot('03-return-to-material')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope["tab"],sc.scope["selected_record"]]')==['all','E12']
   await q.press('사람');assert await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["rel_sel"]')=='nabi'
   await q.press('자료');await q.press('전체');assert set(await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["entries"]'))=={'E01','E06','E10','E12'}
   await q.press('증언');await q.input(350,200);await q.press('닫기')
   await q.py('import renpy;renpy.exports.show_screen("r13_records");renpy.exports.restart_interaction();result=True');await q.wait('r13_records')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_records");result=[sc.scope["material_filter"],sc.scope["selected_record"]]')==['testimony','E12']
   await q.py('import renpy;renpy.store.persistent.room13_large_text=True;renpy.exports.restart_interaction();result=True');await page.set_viewport_size({'width':844,'height':390});q.touch=True
   await q.shot('04-material-mobile');await q.press('전달 가능');assert not await q.py('import renpy;result=renpy.display.screen.get_screen("r13_records").scope["entries"]')
   await q.shot('05-empty-transfer');await q.press('닫기')
   # Unknown source stays unnamed; UI source reads do not grant people or clues.
   before=(await q.state())['room']
   assert await q.py('import renpy;result=renpy.store.r13_material_source_person("E15")') is None
   assert (await q.state())['room']==before
   # The old works belong underneath the inn, and stay hidden before discovery.
   await q.py('import renpy;s=renpy.store;s.r13_edit(location="ancient");renpy.exports.show_screen("r13_map");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map')
   assert not await q.py('import renpy;result="ancient" in dict(renpy.store.r13_map_nodes("inn"))')
   await q.press('현장으로 돌아가기')
   await q.py('import renpy;s=renpy.store;s.r13_edit(day=9,period=0,week2_started=True,passage_open=True,location="ancient");s.r13_flag("ancient_found");renpy.exports.show_screen("r13_map");renpy.exports.restart_interaction();result=True')
   await q.wait('r13_map');await q.shot('06-underground-discovered-mobile')
   assert await q.py('import renpy;sc=renpy.display.screen.get_screen("r13_map");result=[sc.scope["region"],sc.scope["selected"]]')==['inn','ancient']
   await q.press('현장으로 돌아가기')
   await q.py('import renpy;renpy.exports.show_screen("r13_book",target="bami",present=True,hearing=True);renpy.exports.restart_interaction();result=True')
   await q.wait('r13_book');st=await q.state();assert not any('전달 가능' in b['text'] for b in st['buttons'])
   assert set(await q.py('import renpy;result=renpy.display.screen.get_screen("r13_book").scope["entries"]'))=={'E01','E06','E10','E12'}
   await q.press('증언');await q.shot('07-hearing-material-mobile')
   assert set(await q.py('import renpy;result=renpy.display.screen.get_screen("r13_book").scope["entries"]'))=={'E06','E10','E12'}
   await q.py('import renpy;renpy.exports.hide_screen("r13_book");renpy.exports.restart_interaction();result=True')
   result=dict(passed=True,checks=['owned evidence only in type filters','explicit known source opens relationship','relationship opens owned testimony and its correct page','relationship selection retained across tab return','filter and selected material restored after close','mobile touch and large text','transfer lens uses actual eligibility; no second inventory','unknown source not revealed; source lookup leaves story state unchanged','underground belongs to inn; discovered only; current floor visible on mobile','hearing filters keep owned evidence only and hide transfer lens'])
   (OUT/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('PASS',result,flush=True)
  except Exception as e:
   print('FAIL',repr(e),flush=True);await page.screenshot(path=str(OUT/'stop.png'));raise
  finally:await b.close()
asyncio.run(main())
