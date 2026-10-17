import asyncio,json,sys
from pathlib import Path
from playwright.async_api import async_playwright
sys.path.insert(0,'/workspace/daaegame/experiments/renpy-ch1/dev')
from webqa import UIQA
OUT=Path('/workspace/kkwak-local-review')
SETUP='''import renpy,copy,json
s=renpy.store
s.room13=s.r13_new()
s.r13_edit(day=1,period=1,location="gate")
s.persistent.room13_motion=False
s.kkwak_new=copy.deepcopy(s.R13_FULLBODY["people"]["resident_kkwak"])
s.kkwak_old=json.loads(open("/game/assets/kkwak-before-entry.json").read())
s.R13_FULLBODY_FILES.add(s.kkwak_old["images"]["neutral"]["file"])
s.kkwak_variant="approved"
def compare_screen(**kwargs):
    s=renpy.store
    renpy.ui.add(s.Solid("#000000"))
    renpy.ui.add(s.Crop((0,0,1280,720),s.r13_world_background("gate","afternoon")))
    if s.kkwak_variant=="field":
        art=s.r13_staged_art(dict(person="resident_kkwak",pose="neutral",width=137,height=260,contact="standing"),still=True)
        renpy.ui.add(s.Transform(art,xpos=650,ypos=290))
    else:
        art=s.r13_close_art("resident_kkwak","neutral",840)
        renpy.ui.add(s.Transform(art,xpos=s.r13_close_x("resident_kkwak","neutral",840),xanchor=.5,ypos=s.r13_fullbody_close_y("resident_kkwak",840,110,"neutral"),nearest=True))
    renpy.ui.add(s.Transform(s.Solid("#19212cee"),xpos=0,ypos=558,xsize=1280,ysize=162))
    renpy.ui.text("꽥순",xpos=65,ypos=575,size=25,color="#f2dbb0")
    renpy.ui.text("승인 기본 디자인 · 로컬 렌더 검수",xpos=65,ypos=625,size=26,color="#fff4dd")
    renpy.ui.text(s.kkwak_variant,xpos=30,ypos=30,size=26,color="#ffffff")
renpy.display.screen.define_screen("kkwak_review",compare_screen,zorder="300")
renpy.exports.show_screen("kkwak_review")
renpy.exports.restart_interaction()
result={"version":s.config.version,"new":s.kkwak_new}
'''
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
  q=UIQA(page,OUT)
  await page.goto('http://127.0.0.1:8791/daaegame/preview/room13-dev/')
  await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000)
  await q.wait('main_menu')
  for url,dest in [('/kkwak-local-review/before-entry.json','kkwak-before-entry.json'),('/daaegame/experiments/renpy-ch1/game/assets/room13-role-resident_kkwak.webp','room13-role-resident_kkwak.webp')]:
   await page.evaluate('''async ([url,dest])=>{let r=await fetch(url); if(!r.ok) throw Error(r.status); FS.writeFile('/game/assets/'+dest,new Uint8Array(await r.arrayBuffer()));}''',[url,dest])
  results={'setup':await q.py(SETUP),'fixture':'actual RenPy renderer; controlled dialogue panel on gate afternoon; not a story playthrough','screens':[]}
  for variant in ['before','approved_with_grid','approved','field']:
   code='''import renpy,copy
s=renpy.store
s.kkwak_variant=%r
s.R13_FULLBODY["people"]["resident_kkwak"]=copy.deepcopy(s.kkwak_old if s.kkwak_variant=="before" else s.kkwak_new)
s.R13_FULLBODY_CENTRE["resident_kkwak"]=-10 if s.kkwak_variant=="before" else -20
if s.kkwak_variant=="approved_with_grid":
 for v in s.R13_FULLBODY["people"]["resident_kkwak"]["images"].values():v.pop("native_detail",None)
s.R13_FULLBODY_ART_CACHE.clear()
renpy.exports.restart_interaction()
result={"scale":s.r13_fullbody_scale("resident_kkwak",840),"x":s.r13_close_x("resident_kkwak","neutral",840),"y":s.r13_fullbody_close_y("resident_kkwak",840,110,"neutral")}
'''%variant
   state=await q.py(code);await asyncio.sleep(1.5)
   probe=await q.py('import renpy;result={"screen":renpy.display.screen.get_screen("kkwak_review") is not None,"exception":renpy.display.screen.get_screen("_exception") is not None}')
   assert probe['screen'] and not probe['exception'],probe
   await page.screenshot(path=str(OUT/(variant+'.png')))
   results['screens'].append({'variant':variant,'state':state,'probe':probe})
  (OUT/'execution.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
  await browser.close()
asyncio.run(main())
