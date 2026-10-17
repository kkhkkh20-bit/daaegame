"""Exact production branch packets through the real r13_lines/cut/save renderer.
Focused fixtures, not a full story playthrough or a replacement for branch-condition tests.
"""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from test_special_scenes import scene_calls,MAP
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/special-scenes-screen-review'));OUT.mkdir(exist_ok=True)
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8887/preview/room13-dev/')
async def invoke(q,rows,identity):
 code='import renpy\ns=renpy.store\ns.qa_entries='+repr(rows)+'\ns.qa_entries=[tuple(row[:2])+(s.dict(row[2]),) if len(row)>2 else tuple(row) for row in s.qa_entries]\ns.qa_identity='+repr(identity)+'''\ndef special_call(**kwargs):
 s=renpy.store
 renpy.ui.textbutton("장면 검토",clicked=[s.Hide("qa_special_call"),s.Call("r13_lines",s.qa_entries,s.qa_identity)],xpos=500,ypos=300,xsize=280,ysize=80)
renpy.exports.define_screen("qa_special_call",special_call,modal="True",zorder="200")
renpy.exports.show_screen("qa_special_call");renpy.exports.restart_interaction();result=True'''
 await q.py(code);await q.press('장면 검토');await q.wait('say')
async def main():
 report=dict(kind='production packets in actual r13_lines; focused fixtures',scenes=[])
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
   report['version']=await q.py('import renpy;result=renpy.store.config.version');await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(2)
   for identity,rows in scene_calls().items():
    key=MAP[identity];bg='ep_belltower_night' if key.startswith('chorong') else 'r13_river' if key.startswith('nero') else 'r13_school'
    await q.py('import renpy\ns=renpy.store\ns.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=12,period=2,location="school")\ns.room13_mode=True;s.r13_meeting_active=False;s.r13_cg_active=False;s.r13_camera="stage";s.r13_scene_bg='+repr(bg)+';s.place="특수 장면 검토"\nrenpy.exports.hide("r13_visitor");result=True')
    await q.py('import renpy;renpy.store.persistent.room13_large_text='+repr(key=='teacher_blanket_dodam_only')+';result=True')
    await invoke(q,rows,identity);await asyncio.sleep(.5)
    state=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,identity=s.r13_read_id,tags=sorted(renpy.exports.get_showing_tags()),background=s.r13_scene_bg)')
    assert state['identity'].startswith(identity+':') and 'r13_ep_cut' in state['tags'];assert state['packet'][2]['cut']==key
    await page.screenshot(path=str(OUT/(key+'-narration.png')))
    # Advance to spoken line where available; same cut must remain visible.
    if len(rows)>1:
     for _ in range(5):
      await q.input(810,640);await asyncio.sleep(.15)
      packet=await q.py('import renpy;result=renpy.store.r13_packet')
      if packet[0] is not None:break
     assert packet[0] is not None
    await page.screenshot(path=str(OUT/(key+'-dialogue.png')))
    before=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,identity=s.r13_read_id,background=s.r13_scene_bg)')
    await q.open_file_menu('save');await q.press('1쪽 3번')
    if 'confirm' in (await q.state())['screens']:await q.press('예')
    await q.press('돌아가기');await q.say_load(3)
    after=await q.py('import renpy;s=renpy.store;result=dict(packet=s.r13_packet,identity=s.r13_read_id,background=s.r13_scene_bg)')
    assert before==after and await q.py('import renpy;result="r13_ep_cut" in renpy.exports.get_showing_tags()')
    await page.screenshot(path=str(OUT/(key+'-restored.png')))
    # Let the production block finish; its own lifecycle must remove the cut.
    for _ in range(16):
     if not (await q.py('import renpy;result=renpy.store.r13_read_id')).startswith(identity+':'):break
     await q.input(810,640);await asyncio.sleep(.15)
    assert not await q.py('import renpy;result="r13_ep_cut" in renpy.exports.get_showing_tags()')
    await page.screenshot(path=str(OUT/(key+'-returned.png')))
    report['scenes'].append(dict(scene=key,identity=identity,state=after,save_restored=True,cut_cleared_on_return=True));print('PASS',key,flush=True)
   report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
