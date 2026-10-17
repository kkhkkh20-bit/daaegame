"""Actual WASM review with parsed source overlays (not a rebuilt release).

Use the unchanged base preview plus the working-tree sources. No fixture enters game data.
"""
import asyncio,json,os,textwrap,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','speaker-review'));OUT.mkdir(parents=True,exist_ok=True)
FILES=['screens.rpy','room13_screens.rpy','room13_notebook.rpy','systems/room13_relations.rpy']
SETUP='''import renpy
s=renpy.store
s.room13=s.r13_new();s.room13_mode=True;s.preferences.text_cps=0
s.r13_meeting_active=False;s.r13_thought_active=False;s.r13_cg_active=False
s.persistent.room13_motion=False;s.persistent.room13_large_text=False
renpy.exports.hide_screen("main_menu")
result=True
'''
async def main():
 report={'kind':'Actual WASM base + parsed working-tree screen overlay; not a release build or full playthrough','captures':[]}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader']);page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
  try:
   await page.goto(os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/'));await page.wait_for_function("typeof renpy_exec==='function'",timeout=240000);await q.wait('main_menu')
   report['base_version']=await q.py('import renpy;result=renpy.store.config.version')
   await q.py(SETUP)
   for phase in ('before','after'):
    if phase=='after':
     src=(ROOT/'game/room13_speaker_display.rpy').read_text()
     await q.py('import renpy\nexec('+repr(textwrap.dedent(src.split('init 150 python:\n')[1]))+',renpy.store.__dict__)\nresult=True')
     report['parsed_sources']={}
     for filename in ['room13_speaker_display.rpy']+FILES:
      src=(ROOT/'game'/filename).read_text()
      result=await q.py('''import renpy
renpy.parser.parse_errors=[]
nodes=renpy.parser.parse(%r,filedata=%r)
renpy.game.script.update_bytecode()
pending=list(nodes or []);names=[]
while pending:
 node=pending.pop(0)
 if isinstance(node,renpy.ast.Init):pending.extend(node.block)
 elif isinstance(node,renpy.ast.Screen):
  node.screen.define((node.filename,node.linenumber));names.append(node.screen.name)
result=dict(errors=list(renpy.parser.parse_errors),screens=names)
'''%('qa_speaker_overlay/'+filename,src))
      assert not result['errors'],result
      report['parsed_sources'][filename]={'sha256':hashlib.sha256(src.encode()).hexdigest(),**result}
     await q.py('import renpy;renpy.exports.hide_screen("say");renpy.exports.restart_interaction();result=True')
    for name,loc,period,who,person,width,height,large in [
      ('nubi-snow','square',0,'누비 아주머니','resident_nubi',1280,720,False),
      ('momo-dark','inn',2,'모모 관장','resident_momo',1280,720,False),
      ('long-name','square',0,'부엉이 할아버지','resident_owlgp',1280,720,False),
      ('anonymous','inn',2,'???','resident_nubi',1280,720,False),
      ('two-speakers','square',0,'누비 · 모모','resident_nubi',1280,720,False),
      ('mobile-snow','square',0,'누비 아주머니','resident_nubi',844,390,False),
      ('mobile-dark-large','inn',2,'부엉이 할아버지','resident_owlgp',844,390,True),
    ]:
     await page.set_viewport_size({'width':width,'height':height})
     await q.py('''import renpy
s=renpy.store
s.r13_edit(location=%r,period=%r);s.persistent.room13_large_text=%r
s.place=s.R13_PLACES[s.room13['location']][0];s.r13_packet=(%r,"마른 빨래부터 따로 묶어 두었어요.")
renpy.exports.scene()
renpy.exports.show("qa_background",what=s.r13_background(s.R13_PLACES[s.room13['location']][1]))
renpy.exports.show("r13_visitor",what=s.r13_close_art(%r,"neutral",840),at_list=[s.Transform(xpos=s.r13_close_x(%r,"neutral"),xanchor=.5,ypos=s.r13_close_y(%r,840,110,"neutral"))])
renpy.exports.show_screen("say",who=%r,what="마른 빨래부터 따로 묶어 두었어요.")
renpy.exports.restart_interaction();result=True
'''%(loc,period,large,person,person,person,person,who))
     await asyncio.sleep(.6)
     result=await q.py('import renpy;w=renpy.exports.get_widget("say","who");result=dict(text=w.text,size=w.style.size,exception=bool(renpy.display.screen.get_screen("_exception")))')
     assert not result['exception'],result
     if phase=='after' and name=='nubi-snow':assert result['text']==['누비'],result
     if phase=='after' and name=='anonymous':assert result['text']==['???'],result
     await page.screenshot(path=str(OUT/(phase+'-'+name+'.png')));report['captures'].append(dict(name=phase+'-'+name,**result))
    print('CAPTURED',phase,flush=True)
   await page.set_viewport_size({'width':1280,'height':720})
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;s.r13_meeting_active=True;s.r13_meeting_claim="C1";s.r13_edit(day=7,period=2,location="dining");renpy.exports.show_screen("say",who="할머니",what="그날 들은 말을 다시 이야기할게요.");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.6)
   report['meeting_label']=await q.py('import renpy;w=renpy.exports.get_widget("say","who");result=dict(text=w.text,size=w.style.size,exception=bool(renpy.display.screen.get_screen("_exception")))')
   assert not report['meeting_label']['exception'] and report['meeting_label']['size']==24
   await page.screenshot(path=str(OUT/'after-meeting.png'))
   await q.py('import renpy;renpy.store.r13_meeting_active=False;result=True')
   await q.py('import renpy;s=renpy.store;s.persistent.room13_large_text=False;renpy.exports.hide_screen("say");renpy.exports.hide("r13_visitor");renpy.exports.show_screen("r13_resident_approach",approach="안녕하세요.",person="resident_nubi");renpy.exports.restart_interaction();result=True')
   await asyncio.sleep(.7);await page.screenshot(path=str(OUT/'after-introduction.png'))
   await q.py('''import renpy
s=renpy.store
renpy.exports.hide_screen("r13_resident_approach")
for who in ("resident_nubi","resident_momo","buri"):s.r13_note_encounter(who)
result=s.r13_rel_people()
''')
   report['shown_people']=await q.py('import renpy;result=renpy.store.r13_rel_people()')
   assert 'resident_teacher' not in report['shown_people']
   for who in ('resident_nubi','resident_momo','buri'):
    await q.py('import renpy;s=renpy.store;s.r13_records_view=s.dict(rel_sel=%r,rel_focus=True);renpy.exports.hide_screen("r13_records");renpy.exports.show_screen("r13_records",initial_tab="relations");renpy.exports.set_screen_variable("rel_sel",s.r13_records_view["rel_sel"],screen="r13_records");renpy.exports.restart_interaction();result=True'%who)
    await q.press(await q.py('import renpy;result=renpy.store.r13_display_name(%r)'%who))
    await asyncio.sleep(.5);await page.screenshot(path=str(OUT/('after-record-'+who+'.png')))
   await q.py('import renpy;renpy.exports.hide_screen("r13_records");renpy.exports.show_screen("main_menu");renpy.exports.restart_interaction();result=True')
   await q.press('처음부터');await asyncio.sleep(1)
   for _ in range(45):
    st=await q.state()
    if 'say' in st['screens'] and await q.py('import renpy;result=bool(renpy.store.r13_packet and renpy.store.r13_packet[0])'):break
    if any('씬 건너뛰기' in v['text'] for v in st['buttons']):await q.press('씬 건너뛰기')
    else:await q.input(810,640)
   await q.wait('say');await page.screenshot(path=str(OUT/'after-natural-start.png'))
   # The opening hides file tools; expose the normal line toolbar for this save UI fixture.
   await q.py('import renpy;renpy.store.place="마을 입구";renpy.exports.restart_interaction();result=True')
   report['save_toolbar_fixture']='Opening line with normal line toolbar exposed; script/packet unchanged'
   report['before_save']=await q.py('import renpy;result=renpy.store.r13_packet')
   await q.say_save(2);await q.say_load(2)
   report['after_load']=await q.py('import renpy;result=renpy.store.r13_packet')
   assert report['before_save']==report['after_load']
   await page.screenshot(path=str(OUT/'after-load.png'))
   for _ in range(8):await q.input(810,640)
   report['after_repeated_clicks']=await q.state()
   assert '_exception' not in report['after_repeated_clicks']['screens']
   report['status']='passed'
  except Exception as e:
   report['error']=repr(e);await page.screenshot(path=str(OUT/'failure.png'));print(repr(e),flush=True)
   raise
  finally:
   (OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));await b.close()
if __name__=='__main__':asyncio.run(main())
