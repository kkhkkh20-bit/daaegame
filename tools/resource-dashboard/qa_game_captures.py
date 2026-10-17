"""Actual existing web build captures with explicit fixtures; never a full-playthrough claim."""
import asyncio,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experiments/renpy-ch1/dev'))
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_dialogue_routes import native_jump
from qa_remaining_approved22 import setup
OUT=ROOT/'reports/resource-dashboard-20261017/game';OUT.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'));await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');print('GAME READY',flush=True)
   version=await q.py('import renpy;result=renpy.store.config.version')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(.6)
   for who,day,period,loc in [('resident_eunho',2,0,'market'),('resident_sling',2,2,'post'),('resident_seori',2,0,'clinic')]:
    await setup(q,day,loc,flags=['ev_g_done'],period=period)
    a=await q.py('import renpy;s=renpy.store;result=next((a for a in s.r13_stage_people() if a["person"]=='+repr(who)+'),None)');assert a,(who,'absent')
    width=await q.py('import renpy;result=renpy.store.r13_world_width()');offset=max(0,min(a['x']+a['width']/2-640,width-1280))
    await q.py('import renpy;s=renpy.store;s.r13_world_cameras=s.dict(s.r13_world_cameras,**{'+repr(loc)+':'+str(offset)+'});result=True');await native_jump(q,'r13_field');await q.wait('r13_hub');await asyncio.sleep(.4)
    name=who+'-'+str(day)+'-'+str(period);await page.screenshot(path=str(OUT/(name+'.png')))
    result=dict(screens=['r13_hub'],room={'day':day,'period':period,'location':loc,'fixture_flags':['entry_corrected','lodging','ev_g_done']},person=who,actor=a,game_version=version,game_commit='unknown (existing web build; source checkout is separately recorded)',source_checkout=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),archive_sha256=json.loads((ROOT/'preview/room13-dev/game-transport.json').read_text())['archive_sha256'],capture_kind='real RenPy renderer, explicit state fixture; not a natural campaign playthrough')
    (OUT/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('CAPTURE',who,a['pose'],flush=True)
  finally:await b.close()
if __name__=='__main__':asyncio.run(main())
