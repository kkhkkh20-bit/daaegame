"""Local web renderer check using the existing build and production functions.

Installs unbuilt image bytes/functions in the disposable browser filesystem.
This is a renderer fixture, not a compiled-build or full-playthrough claim.
"""
import ast, asyncio, base64, json, textwrap, os
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA, SETUP

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/dialogue-beats/expression-fit-20261020/screens'

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report={'kind':'existing web build + production-function/image overlay; not rebuilt game'}
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=await browser.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
        try:
            await page.goto('http://127.0.0.1:8891/preview/room13-dev/')
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000)
            await q.wait('main_menu')
            data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())
            selected={k:data['people'][k] for k in ('daram','karo','guard')}
            for who,entry in selected.items():
                for height,profile in entry['profiles'].items():
                    for slot,frame in profile['frames'].items():
                        original=ROOT/'game'/frame['file']
                        frame['file']='assets/dialogue-source-master/qa-fit/'+who+'/'+height+'/'+slot+'.webp'
                        payload=base64.b64encode(original.read_bytes()).decode()
                        code='import os,base64,renpy\np=os.path.join(renpy.config.gamedir,%r)\nos.makedirs(os.path.dirname(p),exist_ok=True)\nopen(p,"wb").write(base64.b64decode(%r))\nresult=True'%(frame['file'],payload)
                        await q.py(code)
            # Redefine only changed production rendering nodes, preserving wrappers.
            source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:\n',1)[1]
            tree=ast.parse(textwrap.dedent(source))
            chosen=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in ('R13DialogueBeat','r13_dialogue_fit_profile','r13_dialogue_source_neutral')]
            code=ast.unparse(ast.Module(body=chosen,type_ignores=[]))
            await q.py('import renpy\nexec('+repr(code)+',renpy.store.__dict__)\nrenpy.store.R13_DIALOGUE_TALK_ART["people"].update('+repr(selected)+')\nresult=True')
            for filename,target in [('room13-dialogue-beats.json','R13_DIALOGUE_BEATS'),('room13-dialogue-bindings.json','R13_DIALOGUE_BINDINGS'),('room13-fullbody-line-emotions.json','R13_FULLBODY_LINES')]:
                value=json.loads((ROOT/'game/assets'/filename).read_text())
                await q.py('import renpy\nrenpy.store.'+target+'='+repr(value)+'\nresult=True')
            await q.py(SETUP)
            for who,slot in ([] if os.environ.get('EXPRESSION_QA_NATURAL_ONLY') else [('daram','joy'),('karo','neutral'),('guard','anxious')]):
                for height in (760,840):
                    await q.py('import renpy\ns=renpy.store\ns.qa_person=%r;s.qa_height=%r;s.qa_slot=%r;s.qa_title=%r\ns.r13_dialogue_beat=dict(person=s.qa_person,talk=s.qa_slot,react=None,settled=True,duration=.35)\nrenpy.exports.restart_interaction();result=True'%(who,height,slot,'2x2 final render: '+who+' '+str(height)))
                    await asyncio.sleep(.8)
                    await page.screenshot(path=str(OUT/(who+'-'+str(height)+'-'+slot+'.png')))
            await q.py('import renpy\nrenpy.exports.hide_screen("qa_smooth_gallery")\nrenpy.store.preferences.text_cps=0\nrenpy.exports.restart_interaction()\nresult=True')
            await q.press('처음부터')
            for _ in range(25):
                await asyncio.sleep(.3)
                state=await q.py('import renpy\ns=renpy.store\nresult=dict(packet=s.r13_packet,beat=s.r13_dialogue_beat)')
                if state.get('packet') and state['packet'][0]=='daram' and state['packet'][1]=='아빠는 안 부서지잖아.':break
                await q.input(1000,640)
            assert state['beat'] and state['beat']['talk']=='joy',state
            await asyncio.sleep(.8)
            await page.screenshot(path=str(OUT/'d01-natural-joy.png'))
            report['natural_d01']=state
            report['piko_diagnostic']=await q.py('import renpy\ns=renpy.store\ns.room13=s.r13_new();s.r13_upgrade();s.r13_edit(day=2,period=0,location="square",life_poc=True)\ns.r13_offer("r13_w1c_portrait")\nactors=s.r13_stage_people()\nresult=dict(people=[a["person"] for a in actors],offer=s.r13_offer_for_person("resident_piko"),staged=s.r13_offer_staged("r13_w1c_portrait",actors),world_offset=s.r13_world_offset(),piko=[a for a in actors if a["person"]=="resident_piko"])')
            await q.py('import renpy\nrenpy.exports.show_screen("r13_map",initial_region="village")\nrenpy.exports.restart_interaction()\nresult=True')
            await asyncio.sleep(1)
            await page.screenshot(path=str(OUT/'map-before-mask-limitation.png'))
            report['status']='passed';report['profiles']=selected
        except Exception as e:
            report['status']='failed';report['error']=repr(e)
            await page.screenshot(path=str(OUT/'failure.png'))
            raise
        finally:
            (OUT/'renderer-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            await browser.close()

if __name__=='__main__':asyncio.run(main())
