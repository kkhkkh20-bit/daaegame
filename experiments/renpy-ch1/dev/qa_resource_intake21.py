"""Existing Ren'Py build + disposable source/data overlay, NOT a new build."""
import asyncio,base64,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA,SETUP
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/resource-intake21-qa'))
async def main():
 OUT.mkdir(parents=True,exist_ok=True)
 data=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())
 cues=[c for c in data['bindings'] if c.get('batch')=='resource-intake-20261021']
 report={'kind':('official build; no asset overlay' if os.environ.get('INTAKE_QA_OFFICIAL') else 'existing build + disposable source/data overlay; NOT new build or deployment'),'captures':[]}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'))
   await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await q.wait('main_menu')
   report['base_version']=await q.py('import renpy;result=renpy.config.version');print('READY',report['base_version'],flush=True)
   if not os.environ.get('INTAKE_QA_OFFICIAL'):
    for c in cues:
     for profile in data['entries'][c['key']]['profiles'].values():
      f=profile['frames'][c['slot']]['file'];payload=base64.b64encode((ROOT/'game'/f).read_bytes()).decode()
      await q.py('import os,base64,renpy\np=os.path.join(renpy.config.gamedir,%r)\nos.makedirs(os.path.dirname(p),exist_ok=True)\nopen(p,"wb").write(base64.b64decode(%r))\nresult=True'%(f,payload))
    await q.py('import renpy\nrenpy.store.R13_DIALOGUE_CONTEXT_ART='+repr(data)+'\nresult=True')
   await q.py(SETUP)
   report['before_state']=await q.py('import renpy;result=repr(renpy.store.room13)')
   for c in ([] if os.environ.get('INTAKE_QA_NATURAL_ONLY') else cues):
    for height in (560,760,840):
     name=c['slot']+'-'+str(height)
     code='import renpy\ns=renpy.store\ns.qa_person=%r;s.qa_height=%r;s.qa_title=%r\ns.r13_dialogue_beat_begin(%r,%r,(%r,%r),"neutral")\nrenpy.exports.restart_interaction();result=s.r13_dialogue_beat'%(c['person'],height,name,c['identity'],c['index'],c['person'],c['text'])
     beat=await q.py(code);assert beat['context_key']==c['key'],beat
     await asyncio.sleep(.15);await page.screenshot(path=str(OUT/(name+'.png')))
     assert not await q.py('import renpy;result=bool(renpy.display.screen.get_screen("_exception"))')
     report['captures'].append(name)
    print('CAPTURED',c['slot'],flush=True)
   report['after_state']=await q.py('import renpy;result=repr(renpy.store.room13)');assert report['before_state']==report['after_state']
   await page.set_viewport_size({'width':390,'height':844})
   await asyncio.sleep(.3);await page.screenshot(path=str(OUT/'mobile-ubak.png'))
   # Natural current story route, then the existing save/load UI.
   await page.set_viewport_size({'width':1280,'height':720})
   await q.py('import renpy;renpy.exports.hide_screen("qa_smooth_gallery");renpy.store.preferences.text_cps=0;renpy.exports.restart_interaction();result=True')
   await q.press('처음부터')
   for _ in range(100):
    st=await q.state()
    snap=await q.py('import renpy;s=renpy.store;result=dict(packet=getattr(s,"r13_packet",None),beat=s.r13_dialogue_beat)')
    if snap['beat'] and snap['beat'].get('context_key')=='daram:intake21_01_bravado':break
    if 'say' in st['screens']:await q.input(810,400)
    elif 'r13_cinematic_view' in st['screens']:await q.press('계속')
    else:await asyncio.sleep(.2)
   assert snap['beat'] and snap['beat'].get('context_key')=='daram:intake21_01_bravado',snap
   report['natural_scene']=snap
   print('NATURAL',snap,flush=True)
   await page.screenshot(path=str(OUT/'natural-bravado.png'))
   if os.environ.get('INTAKE_QA_SKIP_SAVE'):
    report['status']='passed';return
   await q.py('import renpy;renpy.store.persistent.room13_motion=False;result=True')
   report['save_before']=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,beat=s.r13_dialogue_beat,room=s.room13)')
   await q.say_save(6)
   await q.input(810,400)
   await q.say_load(6)
   report['loaded']=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,beat=s.r13_dialogue_beat,room=s.room13)')
   assert report['loaded']==report['save_before']
   assert report['loaded']['beat']['settled']
   await page.screenshot(path=str(OUT/'after-load.png'));report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await browser.close()
if __name__=='__main__':asyncio.run(main())
