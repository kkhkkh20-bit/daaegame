"""Real web profile rendering at small sizes and unchanged record discovery gates."""
import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
OUT=Path(os.environ.get('ROOM13_QA_OUT','/workspace/profile-icons-review'));OUT.mkdir(exist_ok=True)
SETUP='''import renpy
s=renpy.store
s.qa_profile_page=0
def profile_gallery(**kwargs):
 import renpy
 s=renpy.store
 renpy.ui.add(s.Solid("#ead7b3"))
 people=list(s.R13_PROFILE_SOURCE_ART["people"])[s.qa_profile_page*16:(s.qa_profile_page+1)*16]
 for i,person in enumerate(people):
  x=12+(i%4)*316;y=12+(i//4)*170
  renpy.ui.text(person,xpos=x,ypos=y,size=18,font=s.r13_ui_font(),color="#493b30")
  offset=0
  for size in (44,60,76,80):
   renpy.ui.add(s.Transform(s.r13_art(person,"avatar_neutral"),xpos=x+offset,ypos=y+30,xysize=(size,size),nearest=s.r13_profile_nearest(person)))
   renpy.ui.text(str(size),xpos=x+offset,ypos=y+116,size=16,font=s.r13_ui_font(),color="#493b30")
   offset+=size+10
renpy.exports.define_screen("qa_profile_gallery",profile_gallery,zorder="200")
renpy.exports.show_screen("qa_profile_gallery");renpy.exports.restart_interaction();result=True
'''
async def main():
 report={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await browser.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8887/preview/room13-dev/'));await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu');report['version']=await q.py('import renpy;result=renpy.store.config.version')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await asyncio.sleep(1)
   await q.py(SETUP)
   for i in range(4):
    await q.py('import renpy;renpy.store.qa_profile_page='+str(i)+';renpy.exports.restart_interaction();result=True');await asyncio.sleep(.15);await page.screenshot(path=str(OUT/('all-profiles-'+str(i)+'.png')))
   report['files']=await q.py('import renpy\ns=renpy.store\nresult={}\nfor who,entry in s.R13_PROFILE_SOURCE_ART["people"].items():\n result[who]=dict(file=entry["file"],loadable=s.renpy.loadable(entry["file"]),nearest=s.r13_profile_nearest(who))')
   assert len(report['files'])==59 and all(e['loadable'] and not e['nearest'] for e in report['files'].values())
   await q.py('''import renpy
s=renpy.store
renpy.exports.hide_screen("qa_profile_gallery")
s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="square")
s.room13_mode=True
for who in ("daram","bami","resident_hyeoni","resident_jongjong","resident_lamplighter","resident_musoe","resident_nero","resident_solbang"):
 s.r13_note_encounter(who)
s.r13_flag("chorong_dead","musoe_gone","nero_alive")
s.r13_records_view=s.dict(rel_sel="mom",rel_focus=False)
renpy.exports.show_screen("r13_records",initial_tab="relations");renpy.exports.restart_interaction();result=True''')
   await q.wait('r13_records');await page.screenshot(path=str(OUT/'records-missing-mother.png'))
   report['gates_before']=await q.py('import renpy;s=renpy.store;result=dict(met=s.r13_met_people(),shown=s.r13_rel_people(),mom=s.r13_rel_status("mom"),dead=s.r13_rel_status("resident_lamplighter"),gone=s.r13_rel_status("resident_musoe"),saved=s.r13_rel_status("resident_nero"),held_nearest=s.r13_profile_nearest("resident_solbang"))')
   assert report['gates_before']['mom'][0]=='missing' and 'resident_teacher' not in report['gates_before']['shown'];assert report['gates_before']['dead'][0]=='dead';assert report['gates_before']['gone'][0]=='gone';assert report['gates_before']['saved'][0]=='saved';assert not report['gates_before']['held_nearest']
   await q.py('import renpy;s=renpy.store;s.r13_records_view=s.dict(rel_sel="resident_solbang",rel_focus=True);renpy.exports.restart_interaction();result=True');await page.screenshot(path=str(OUT/'solbang-record.png'))
   await q.press('인물 중심');await page.screenshot(path=str(OUT/'relations-focus.png'))
   await q.py('import renpy;s=renpy.store;renpy.exports.hide_screen("r13_records");s.r13_edit(mom_state="reunited");s.r13_note_encounter("mom");s.r13_records_view=s.dict(rel_sel="mom",rel_focus=True);renpy.exports.show_screen("r13_records",initial_tab="relations");renpy.exports.restart_interaction();result=True');await q.wait('r13_records');await page.screenshot(path=str(OUT/'mother-reunited.png'))
   assert (await q.py('import renpy;result=renpy.store.r13_rel_status("mom")'))[0] is None
   await q.py('import renpy;renpy.exports.hide_screen("r13_records");renpy.exports.show_screen("r13_resident_notes");renpy.exports.restart_interaction();result=True');assert await q.py('import renpy;result=bool(renpy.display.screen.get_screen("r13_resident_notes"))');await page.screenshot(path=str(OUT/'daram-notebook.png'))
   report['gates_after']=await q.py('import renpy;s=renpy.store;result=dict(met=s.r13_met_people(),shown=s.r13_rel_people())');assert set(report['gates_after']['met'])==set(report['gates_before']['met'])|{'mom'}
   report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await browser.close()
if __name__=='__main__':asyncio.run(main())
