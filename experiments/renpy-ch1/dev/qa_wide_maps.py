# Browser check (0.18.59/0.18.60): the wide maps and the two elders in the real web build.
# For each scene: the right picture (state x daylight) is shown at the right width, every
# visible object is pressed at a point Ren'Py's own focus lookup gives to that object,
# and the click really selects it. Screenshots go to $ROOM13_QA_OUT/wide-maps.
import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright
from webqa import UIQA

URL = os.environ.get('ROOM13_URL', 'http://localhost:8765/preview/room13-dev/')
OUT = Path(os.environ.get('ROOM13_QA_OUT', '/tmp/room13-qa')) / 'wide-maps'
OUT.mkdir(parents=True, exist_ok=True)
QUIET = ["entry_corrected", "lodging", "livelihood_open", "ev_g_done", "ev_i_done", "ev_a_done", "ev_l_done",
         "ep1_patrol_seen", "ep1_eaves_seen", "qa_auto_offer"] + ["evening_brief:%d" % d for d in range(1, 14)]
# (name, location, day, period, case, camera)
SCENES = [
    ("kitchen-morning", "kitchen", 2, 0, "pending", 440),
    ("dining-evening-3", "dining", 7, 2, "pending", 0),
    ("passage-evening", "passage", 2, 2, "pending", 880),
    ("post-morning-6", "post", 3, 0, "pending", 0),
    ("post-afternoon-old", "post", 3, 1, "pending", 0),
    ("inn-afternoon-elders", "inn", 3, 1, "pending", 640),
    ("hall-after-afternoon", "hall", 6, 1, "occurred", 440),
    ("room13-before-morning", "room13", 3, 0, "pending", 440),
    ("room13-after-afternoon", "room13", 6, 1, "occurred", 440),
]

PICK = r'''
import renpy
s=renpy.store
def hit(x,y):
    f=renpy.display.render.focus_at_point(x,y)
    if f is None:return None
    a=getattr(f.widget,"action",None)
    for b in (a if isinstance(a,list) else [a]):
        if b.__class__.__name__=="Return":
            v=b.value
            return list(v) if isinstance(v,tuple) else v
    return ["other"]
loc=s.room13["location"];cam=s.r13_world_offset();picks={}
for key,spec in s.ROOM13["objects"].get(loc,{}).items():
    if not s.r13_object_visible(spec):continue
    x,y,w,h=spec["rect"];best=None
    for i in range(12):
        for j in range(9):
            sx=int(x+w*(i+.5)/12.0-cam);sy=int(y+h*(j+.5)/9.0)
            if 0<=sx<1280 and 0<=sy<720 and hit(sx,sy)==["object",key]:
                d=(i-5.5)**2+(j-4)**2
                if best is None or d<best[0]:best=(d,sx,sy)
    if best:picks[key]=[best[1],best[2]]
layout=s.r13_layout(loc)
inview=[k for k,spec in s.ROOM13["objects"].get(loc,{}).items() if s.r13_object_visible(spec) and min(spec["rect"][0]+spec["rect"][2],cam+1280)-max(spec["rect"][0],cam)>=30]
result=dict(width=s.r13_world_width(),camera=cam,inview=inview,file=s.r13_world_file(loc,s.r13_daylight()) if layout else None,
    picks=picks,actors=[(a["person"],a["pose"],a["y"]+a["height"],a["height"]) for a in s.r13_stage_people(False)])
'''


async def goto(q, loc, day, period, case, camera):
    victim = "dead" if case == "occurred" else "alive"
    daram = "held" if case == "occurred" else "with_dad"
    # A close-up opened by the previous click (e.g. the inn door) is closed first.
    await q.py('import renpy\nfor t in list(renpy.exports.get_showing_tags("screens")):\n    if t not in ("r13_hud","r13_hub","say"):renpy.exports.hide_screen(t)\nresult=True')
    await q.py('import renpy;s=renpy.store;s.r13_edit(day=%d,period=%d,location=%r,life_poc=True,secret_route_unlocked=True,case_state=%r,victim_state=%r,daram_state=%r);'
               's.r13_flag(*%r);s.r13_world_cameras={%r:%d};s.r13_upgrade();result=True' % (day, period, loc, case, victim, daram, QUIET, loc, camera))
    await q.py('import renpy;s=renpy.store\ndef f(**kw):renpy.ui.timer(0.2,action=[renpy.store.Hide("qa_jump"),renpy.store.Jump("r13_field")])\n'
               'renpy.display.screen.define_screen("qa_jump",f,zorder="200")\nrenpy.exports.show_screen("qa_jump");renpy.exports.restart_interaction();result=True')
    await asyncio.sleep(2.5)
    await q.advance()
    await q.wait('r13_hub')
    await asyncio.sleep(1.0)


async def main():
    report = {'checks': [], 'scenes': {}}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('ROOM13_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'),
                                    args=['--no-sandbox', '--enable-unsafe-swiftshader'])
        c = await b.new_context(viewport={'width': 1280, 'height': 720}, has_touch=True)
        pg = await c.new_page()
        q = UIQA(pg, OUT)
        try:
            await pg.goto(URL)
            await pg.wait_for_function("typeof renpy_exec==='function'", timeout=150000)
            await q.wait('main_menu')
            await q.py('import renpy;s=renpy.store;s.preferences.text_cps=0;result=True')
            await q.press('처음부터'); await q.advance(); await q.wait('r13_hub')
            only = os.environ.get('QA_SCENES')
            for name, loc, day, period, case, camera in SCENES:
                if only and name not in only.split(','):
                    continue
                await goto(q, loc, day, period, case, camera)
                for _ in range(8):
                    info = await q.py('ns={};exec(' + repr(PICK) + ',ns);result=ns["result"]')
                    if len(info['picks']) >= len(info['inview']):
                        break
                    await asyncio.sleep(0.6)
                await q.shot(name)
                clicks = {}
                for key, (x, y) in sorted(info['picks'].items()):
                    await goto(q, loc, day, period, case, camera)
                    await q.py('import renpy;renpy.store.r13_choice=None;result=True')
                    await q.input(x, y)
                    await asyncio.sleep(1.2)
                    choice = await q.py('import renpy;c=getattr(renpy.store,"r13_choice",None);result=list(c) if isinstance(c,tuple) else c')
                    clicks[key] = choice == ['object', key]
                info['clicks'] = clicks
                report['scenes'][name] = info
                assert all(clicks.values()), (name, clicks)
            report['checks'].append('every visible object in every scene selected by a real mouse click')
            report['status'] = 'passed'
        except Exception as e:
            report['status'] = 'failed'
            report['error'] = repr(e)[:300]
            try:
                report['showing'] = await q.py('import renpy;result=[str(t) for t in renpy.exports.get_showing_tags("screens")]+[str(renpy.store.r13_choice)]')
                await q.shot('failure')
            except Exception as e2:
                report['showing'] = repr(e2)[:200]
        await b.close()
    (OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k != 'scenes'}, ensure_ascii=False)[:1500])
    for name, info in report['scenes'].items():
        print(name, info['width'], info['camera'], info['file'], 'inview', len(info['inview']), 'clicks %d/%d' % (sum(info['clicks'].values()), len(info['clicks'])), info['actors'])


asyncio.run(main())
