"""Native admin shortcuts on the clean wrapper; preserve actual normal saves.

Uses an investigation save obtained from real fresh play. No evaluation hook,
injected game state, console commands, or prepared evidence in the harness.
"""
import argparse
import json
import re
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--url',required=True)
ap.add_argument('--version',required=True)
ap.add_argument('--save',required=True)
ap.add_argument('--viewport',choices=['landscape','portrait'],default='landscape')
ap.add_argument('--output',default='/tmp/admin-test-qa')
args=ap.parse_args()
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
normal='daae-preview-ch1-gpt-20261008:'
snap=r'''prefix=>{const r=window.__W209REAL,a={};for(let i=0;i<r.length;i++){const k=r.key(i);if(k.startsWith(prefix))a[k]=r.getItem(k)}return a}'''
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    size={'width':844,'height':390} if args.viewport=='landscape' else {'width':390,'height':844}
    context=b.new_context(viewport=size,storage_state=args.save)
    pg=context.new_page();errors=[];bad=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    pg.goto(args.url,wait_until='domcontentloaded')
    frame=pg.frame_locator('#game')
    inner=pg.locator('#game').element_handle().content_frame()
    frame.locator('#innmain [data-m="set"]').click(timeout=25000)
    assert not inner.evaluate('typeof window.__T!=="undefined"')
    assert 'build='+args.version in inner.url
    music=frame.locator('#innopt [data-s="musicVolume"]')
    original=inner.evaluate('__innSettings().musicVolume')
    music.focus();pg.keyboard.press('ArrowLeft')
    frame.locator('#innopt .sv').click()
    assert inner.evaluate('__innSettings().musicVolume')==max(0,original-5)
    frame.locator('#innmain [data-m="set"]').click()
    frame.locator('#innopt [data-admin-open]').click()
    assert frame.locator('#inn-admin [data-admin-scene]').count()==12
    assert not frame.locator('#inn-admin input[type="range"]').count()
    pg.keyboard.press('Shift+Tab')
    assert inner.evaluate('document.activeElement.dataset.adminScene')=='report'
    pg.keyboard.press('Tab')
    assert inner.evaluate('document.activeElement.hasAttribute("data-admin-close")')
    pg.keyboard.press('Tab');pg.keyboard.press('Tab');pg.keyboard.press('Space')
    assert frame.locator('#inn-admin [data-admin-scene="investigation"]').is_visible()
    assert not frame.locator('#inn-admin [data-admin-scene="carriage"]').is_visible()
    pg.keyboard.press('Shift+Tab');pg.keyboard.press('Enter')
    assert frame.locator('#inn-admin [data-admin-scene="carriage"]').is_visible()
    pg.screenshot(path=str(out/f'panel-{args.viewport}.png'))
    pg.keyboard.press('Escape')
    assert not frame.locator('#inn-admin').count()
    assert frame.locator('#innopt').count()
    frame.locator('#innopt .x').click()
    frame.locator('#innmain [data-m="cont"]').click()
    frame.locator('#w209rail [data-more]').click(timeout=20000)
    pg.screenshot(path=str(out/f'menu-{args.viewport}.png'))
    frame.locator('#w209more [data-admin-open]').click()
    pre=inner.evaluate(snap,normal)
    before=json.loads(pre[normal+'daae-detective-v3'])['prog']['inn']
    cases=[('carriage','P1'),('welcome','P3'),('night','P10b'),('report','P11'),
           ('investigation',None),('discovery',None),('puzzle',None),('meeting',None),
           ('final',None),('ending','E1'),('mother','E4'),('cold',None)]
    if args.viewport=='portrait':cases=[('night','P10b'),('meeting',None),('investigation',None)]
    baseline=None;rows=[]
    for scene,sid in cases:
        if not frame.locator('#inn-admin').count():frame.locator('#inn-admin-status [data-admin-open]').click()
        group='스토리' if scene in ('cold','carriage','welcome','night','report') else '조사' if scene in ('investigation','discovery','puzzle') else '회의 · 대결' if scene in ('meeting','final') else '후일담'
        frame.locator(f'#inn-admin [data-admin-group="{group}"]').click()
        frame.locator(f'#inn-admin [data-admin-scene="{scene}"]').click()
        inner.wait_for_url(re.compile('testScene='+scene),timeout=20000)
        frame.locator('#inn-admin-status').wait_for(timeout=20000)
        assert not frame.locator('#qaslot9').count()
        inner.wait_for_function('window.__W209P==="daae-preview-ch1-gpt-20261008-admin-test:"')
        assert not inner.evaluate('typeof window.__T!=="undefined"')
        if frame.locator('#bootld').count():
            assert not inner.evaluate('document.querySelector("#inncold,#dlgveil,#inn-under-scene,body>.rt")'),('Test scene started behind boot cover',scene)
        frame.locator('#bootld').wait_for(state='detached',timeout=20000)
        if sid:inner.wait_for_function('(sid)=>__innPresentationState().sid===sid',arg=sid,timeout=20000)
        if scene=='cold':frame.locator('#inncold').wait_for(timeout=20000)
        elif scene=='discovery':frame.locator('#inn-under-scene').wait_for(timeout=20000)
        elif scene in ('meeting','final'):frame.locator('body>.rt').wait_for(timeout=20000)
        else:inner.wait_for_function('!!document.querySelector("#bigscene,#dlgveil")',timeout=20000)
        pg.wait_for_timeout(500)
        after=inner.evaluate(snap,normal)
        if baseline is None:
            baseline=after
            saved=json.loads(after[normal+'daae-detective-v3'])['prog']['inn']
            assert saved['found']==before['found'] and saved['asked']==before['asked']
            assert after[normal+'inn_settings']==pre[normal+'inn_settings']
        assert after==baseline,('Normal storage changed during a test',scene)
        pg.screenshot(path=str(out/f'{scene}-{args.viewport}.png'))
        rows.append({'scene':scene,'sid':sid,'prefix':inner.evaluate('__W209P')})
        print('PASS native shortcut',scene,args.viewport,flush=True)
        # Opening the panel must not advance an active dialogue or cold scene.
        line=inner.evaluate('__innAudioState().line')
        frame.locator('#inn-admin-status [data-admin-open]').click()
        pg.wait_for_timeout(200)
        if line:assert inner.evaluate('__innAudioState().line')==line,('Admin click advanced dialogue',scene)
    frame.locator('#inn-admin [data-admin-close]').click()
    frame.locator('#inn-admin-status [data-admin-return]').click()
    frame.locator('#innmain').wait_for(timeout=25000)
    assert 'testScene=' not in inner.url and 'slot=admin-test' not in inner.url
    assert inner.evaluate('__W209P')==normal
    assert inner.evaluate(snap,normal)==baseline
    frame.locator('#innmain [data-m="cont"]').click()
    frame.locator('#w209rail').wait_for(timeout=20000)
    pg.wait_for_timeout(500)
    resumed=json.loads(inner.evaluate(snap,normal)[normal+'daae-detective-v3'])['prog']['inn']
    original_saved=json.loads(baseline[normal+'daae-detective-v3'])['prog']['inn']
    assert resumed['found']==original_saved['found'] and resumed['asked']==original_saved['asked']
    assert not frame.locator('#inn-admin-status').count()
    assert not errors,errors
    assert not bad,bad
    pg.screenshot(path=str(out/f'return-{args.viewport}.png'))
    (out/f'result-{args.viewport}.json').write_text(json.dumps({'cases':rows,'normalSavePreserved':True,'settingsSaved':True,'errors':errors,'bad':bad},ensure_ascii=False))
    print('PASS normal settings, panel keyboard, right menu, isolated test saves and native normal Continue; JS/HTTP errors 0',flush=True)
    b.close()
