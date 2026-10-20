"""Existing web renderer fixtures for approved placement and record formatting.
Unbuilt Python/data are overlaid in a disposable browser, not a release build.
"""
import ast,asyncio,json,textwrap
from pathlib import Path
from playwright.async_api import async_playwright
from qa_smooth20_dialogue import ReviewQA
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/design-restore-20261020'

def nodes(file,priority,names):
    source=(ROOT/'game'/file).read_text().split('init %d python:\n'%priority,1)[1]
    lines=source.splitlines();end=next((i for i,x in enumerate(lines) if x and not x.startswith((' ','#'))),len(lines))
    tree=ast.parse(textwrap.dedent('\n'.join(lines[:end])))
    return ast.unparse(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names],type_ignores=[]))

FIELD='''import renpy
s=renpy.store
s.room13_mode=True;s.winter_mode=True;s.source_mode=False;s.winter=s.winter_new()
s.room13=s.r13_new();s.r13_upgrade();s.r13_edit(**state)
s.r13_flag("lodging","entry_corrected","livelihood_open")
s.r13_world_cameras={};s.r13_inspection_location=None;s.r13_scene_key=None
s.r13_life_field_active=True;s.r13_meeting_active=False;s.r13_cg_active=False
s.persistent.room13_motion=False;s.persistent.room13_admin=False
s.place=s.R13_PLACES[state['location']][0];s.dialogue_speaker=None
renpy.exports.hide_screen("main_menu");renpy.exports.hide_screen("say")
renpy.exports.hide_screen("r13_map");renpy.exports.hide_screen("r13_hub")
renpy.exports.scene();renpy.exports.show("qa_restore_background",what=s.r13_background(s.R13_PLACES[state['location']][1]))
renpy.exports.show_screen("r13_hub");renpy.exports.show_screen("r13_hud")
renpy.exports.restart_interaction()
result=[dict(person=a['person'],pose=a['pose'],rect=a['rect'],height=a['height']) for a in s.r13_stage_people()]
'''

async def main():
    OUT.mkdir(exist_ok=True);report={'kind':'actual renderer fixtures, not rebuilt release/full play'}
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
        page=await b.new_page(viewport={'width':1280,'height':720});q=ReviewQA(page,OUT)
        try:
            await page.goto('http://127.0.0.1:8891/preview/room13-dev/')
            await page.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await q.wait('main_menu')
            scenarios={'inn':dict(day=2,period=0,location='inn',life_poc=True),'piko':dict(day=2,period=0,location='square',life_poc=True,offers={'r13_w1c_portrait':dict(day=2,period=0,location='square')})}
            # Select a real scheduled market population, never spawn merchants.
            await q.py('import renpy\ns=renpy.store\ns.room13=s.r13_new();s.r13_upgrade()\nresult=True')
            probes=await q.py('import renpy\ns=renpy.store\nrows=[]\nfor d in range(1,8):\n for p in (0,1):\n  s.r13_edit(day=d,period=p,location="market",life_poc=True)\n  a=s.r13_stage_people()\n  rows.append(dict(day=d,period=p,people=[x["person"] for x in a]))\nresult=rows')
            chosen=max(probes,key=lambda x:len(x['people']));scenarios['market']=dict(day=chosen['day'],period=chosen['period'],location='market',life_poc=True)
            report['market_schedule']=probes
            for name,state in scenarios.items():
                report[name+'-before']=await q.py('state='+repr(state)+'\n'+FIELD);await asyncio.sleep(.8);await page.screenshot(path=str(OUT/(name+'-before.png')))
            # Keep outer production wrappers; replace only their captured base.
            life=nodes('room13_life.rpy',57,{'r13_resident_where'})
            await q.py('import renpy\ns=renpy.store\nouter=s.r13_resident_where\nexec('+repr(life)+',s.__dict__)\ns._r13_new_places_resident_where=s.r13_resident_where\ns.r13_resident_where=outer\nresult=True')
            contact=nodes('systems/room13_spatial_contacts.rpy',179,{'r13_stage_people'})
            await q.py('import renpy\ns=renpy.store\nouter=s.r13_stage_people\nexec('+repr(contact)+',s.__dict__)\ns._r13_life_groups_stage=s.r13_stage_people\ns.r13_stage_people=outer\nresult=True')
            mask=nodes('systems/room13_map_action27.rpy',178,{'R13Map27FurnitureAlphaMask','r13_staged_visible_art'})
            await q.py('import renpy\nexec('+repr(mask)+',renpy.store.__dict__)\nresult=True')
            for f,target in [('room13-world-layout.json','R13_WORLD_LAYOUTS'),('room13-map-action27.json','R13_MAP_ACTION27')]:
                data=json.loads((ROOT/'game/assets'/f).read_text());await q.py('import renpy\nrenpy.store.'+target+'='+repr(data)+'\nrenpy.store.R13_STAGE_CACHE.clear()\nresult=True')
            for name,state in scenarios.items():
                report[name+'-after']=await q.py('state='+repr(state)+'\n'+FIELD);await asyncio.sleep(.8);await page.screenshot(path=str(OUT/(name+'-after.png')))
            assert any(x['person']=='resident_piko' for x in report['piko-after'])
            report['status']='passed'
        except Exception as e:
            report.update(status='failed',error=repr(e));await page.screenshot(path=str(OUT/'failure.png'));raise
        finally:
            (OUT/'renderer-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await b.close()

if __name__=='__main__':asyncio.run(main())
