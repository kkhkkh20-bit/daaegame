"""Overlay source in the local web renderer; no build or release file changes.
Start a repository HTTP server on :8765. Captures/report: ROOM13_QA_OUT.
This fixture does not substitute for a rebuilt full-game/save-file regression.
"""
import asyncio,json,os,subprocess,textwrap,time
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
from qa_design_restore import FIELD
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/two-zone-qa'))
async def screens(q,source):
    name='zone_fixture_'+str(time.time_ns())+'.rpy'
    await q.py('import renpy\nnodes=renpy.parser.parse('+repr(name)+',filedata='+repr(source)+')\nassert nodes,renpy.parser.parse_errors\nfor node in nodes:\n if isinstance(node,renpy.ast.Init):\n  for child in node.block:child.screen.define((child.filename,child.linenumber))\nrenpy.game.script.update_bytecode()\nresult=True')
async def install(q):
    camera=(ROOT/'game/room13_world_camera.rpy').read_text()
    code=textwrap.dedent(camera.split('init 58 python:\n')[1].split('\ninit 62 python:')[0])
    await q.py('import renpy\ns=renpy.store\nold_bg=s.r13_world_background\nexec('+repr(code)+',s.__dict__)\ns.r13_world_background=old_bg\ns.config.after_load_callbacks.append(s.r13_world_restore_zone)\nresult=True')
    source=(ROOT/'game/room13_screens.rpy').read_text()
    await screens(q,source[source.index('screen r13_hub('):source.index('screen r13_question_list(')])
    await screens(q,camera[camera.index('screen r13_world_camera_controls('):camera.index('# Retained for existing saves.')])
    source=(ROOT/'game/systems/room13_field_views.rpy').read_text()
    await screens(q,source[source.index('screen r13_field_view_controls('):])
PROBE='''import renpy
s=renpy.store;h=renpy.display.screen.get_screen('r13_hub');a=h.scope['world_adjustment']
result=dict(x=a.value,target=a.animation_target,moving=h.scope['world_moving'],ready=h.scope['input_ready'],saved=s.r13_world_offset(),room=s.room13,
 actors=[(x['person'],x['x'],x['y'],x['width'],x['height']) for x in s.r13_stage_people()])
'''
PICKS='''import renpy
s=renpy.store;a=renpy.display.screen.get_screen('r13_hub').scope['world_adjustment'];points={}
def hit(x,y):
 f=renpy.display.render.focus_at_point(x,y)
 if not f:return None
 a=getattr(f.widget,'action',None)
 for action in (a if isinstance(a,list) else [a]):
  if action.__class__.__name__=='Return':return list(action.value) if isinstance(action.value,tuple) else action.value
 return str(a)
for key,rect,mask in s.r13_objects_over_actors():
 x,y,w,h=rect
 for sx in range(max(82,int(x-a.value)),min(1190,int(x+w-a.value)),8):
  for sy in range(max(160,int(y)),min(550,int(y+h)),8):
   points[str((sx,sy))]=[key,hit(sx,sy)]
result=points
'''
async def fixture(q,loc='gate'):
    await q.py('state='+repr(dict(day=3,period=0,location=loc,life_poc=True))+'\n'+FIELD)
    await asyncio.sleep(1)
    await q.py('import renpy;renpy.store.persistent.room13_motion=True;result=True')
async def slide(q,page,direction,report,tag):
    before=await q.py(PROBE)
    await page.mouse.click(1230 if direction>0 else 45,275)
    samples=[]
    for i in range(8):
        sample=await q.py(PROBE);samples.append({k:sample[k] for k in ('x','moving','ready')})
        if sample['moving']:assert not sample['ready']
        if sample['moving'] and i==0:
            await page.mouse.click(45 if direction>0 else 1230,275)
            await page.mouse.click(700,420)
        await asyncio.sleep(.06)
    await asyncio.sleep(.2)
    after=await q.py(PROBE)
    end=await q.py('import renpy;result=renpy.store.r13_world_width()-1280')
    assert after['x']==(end if direction>0 else 0) and not after['moving'] and after['ready'],after
    assert before['room']==after['room'] and before['actors']==after['actors']
    assert any(0<s['x']<end for s in samples),samples
    await page.screenshot(path=str(OUT/(tag+'.png')))
    report[tag]=dict(samples=samples,endpoint=after['x'],state_unchanged=True,actors_unchanged=True)
async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report={'kind':'source overlay in actual RenPy web renderer; not a release build'}
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME','/usr/bin/chromium'),args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=await b.new_page(viewport={'width':1280,'height':720},has_touch=True);q=ReviewQA(page,OUT)
        try:
            await page.goto(os.environ.get('ROOM13_URL','http://localhost:8765/preview/room13-dev/'))
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await q.wait('main_menu')
            await install(q);await fixture(q)
            await page.screenshot(path=str(OUT/'gate-left.png'))
            await slide(q,page,1,report,'gate-right');await slide(q,page,-1,report,'gate-return')
            base=subprocess.check_output(['git','show','f3093aed:experiments/renpy-ch1/game/room13_screens.rpy'],cwd=ROOT,text=True)
            await screens(q,base[base.index('screen r13_world_contents('):base.index('screen r13_resident_stage(')])
            await q.py('import renpy;renpy.exports.restart_interaction();result=True');await asyncio.sleep(.25);old=await q.py(PICKS)
            current=(ROOT/'game/room13_screens.rpy').read_text()
            await screens(q,current[current.index('screen r13_world_contents('):current.index('screen r13_resident_stage(')])
            await q.py('import renpy;renpy.exports.restart_interaction();result=True');await asyncio.sleep(.25);new=await q.py(PICKS)
            improved={point:dict(before=old[point],after=value) for point,value in new.items() if value[1]==['object',value[0]] and old[point][1]!=value[1]}
            assert improved,'No overlap improvement observed';report['object_overlap_improved']=improved
            await q.py('import renpy;renpy.store.persistent.room13_motion=False;result=True')
            await page.mouse.click(1230,275);await asyncio.sleep(.1);reduced=await q.py(PROBE)
            assert reduced['x']==640 and not reduced['moving'];report['reduced_motion']=True
            await q.py("import renpy\ns=renpy.store;s.persistent.room13_motion=True\na=renpy.display.screen.get_screen('r13_hub').scope['world_adjustment']\ns.r13_pan_camera(a,-1)\ns.r13_world_restore_zone()\nrenpy.exports.restart_interaction();result=True")
            restored=await q.py(PROBE);assert restored['x']==0 and not restored['moving'],restored;report['load_callback_restore']=True
            await page.set_viewport_size({'width':844,'height':390});scale=390/720;left=(844-1280*scale)/2
            await page.touchscreen.tap(left+1230*scale,275*scale);await asyncio.sleep(.9);mobile=await q.py(PROBE)
            assert mobile['x']==640 and mobile['ready'];await page.screenshot(path=str(OUT/'gate-mobile.png'))
            report['mobile_touch']=dict(viewport=[844,390],endpoint=mobile['x'],arrow_css_size=80*scale)
            await page.set_viewport_size({'width':1280,'height':720});await fixture(q,'market')
            await page.screenshot(path=str(OUT/'market-left.png'));await slide(q,page,1,report,'market-right')
            report['status']='passed'
        except Exception as e:
            report.update(status='failed',error=repr(e));await page.screenshot(path=str(OUT/'failure.png'));raise
        finally:
            (OUT/'renderer-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()
if __name__=='__main__':asyncio.run(main())
