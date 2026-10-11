"""Fresh native opening playback, with read-only per-frame presentation traces.

No clues, story beats, scenes, or dialogue are prepared by this test. The only
injected code observes DOM and existing read-only presentation hooks. Both
speeds start at the real main menu and use real pointer/keyboard input.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import time
from playwright.sync_api import sync_playwright, TimeoutError


LOGGER = r'''(()=>{
 const ids=new WeakMap(),sources=new Map();let serial=0;
 const identity=e=>{if(!e)return null;if(!ids.has(e))ids.set(e,++serial);return ids.get(e)};
 const css=e=>{if(!e)return null;const s=getComputedStyle(e);return {visibility:s.visibility,display:s.display,opacity:+s.opacity}};
 const compact=src=>{if(!src||!src.startsWith('data:'))return src;if(!sources.has(src)){let h=2166136261;for(let i=0;i<src.length;i++){h^=src.charCodeAt(i);h=Math.imul(h,16777619)}sources.set(src,'embedded:'+src.length+':'+(h>>>0).toString(16))}return sources.get(src)};
 const image=e=>e?{src:compact(e.getAttribute('src')||e.getAttribute('href')),loaded:e.tagName==='IMG'?e.complete&&e.naturalWidth>0:true,css:css(e),width:e.naturalWidth||null,height:e.naturalHeight||null}:null;
 const safe=f=>{try{return f()}catch(e){return {error:String(e)}}};
 const withoutGame=v=>{if(v&&typeof v==='object'){const {game,...rest}=v;return rest}return v};
 const trace={frames:[],changes:[],last:null,stopped:false};window.__qaPresentationTrace=trace;
 window.__qaPresentationState=function(){
  const q=s=>document.querySelector(s),audio=safe(()=>window.__innAudioState?.()),amb=safe(()=>window.__innAmb?.()),
   cinematic=safe(()=>withoutGame(window.__innStoryCinematics?.())),opening=safe(()=>withoutGame(window.__innOpeningDirection?.())),
   engine=typeof window.__T==='function'?safe(()=>window.__T('({sid:G&&G.beats&&G.beats.inn_psid,bg:G&&G.beats&&G.beats.inn_bg,done:!!(G&&G.beats&&G.beats.inn_pro),dl:!!DL,typing:!!(DL&&DL.typing),screen:S.screen,tab:G&&G.tab})')):null,
   cg=q('#inn-story-cg'),veil=q('#ov #dlgveil');
  return {t:performance.now(),sid:engine?.done?null:engine?.sid||cinematic?.scene||opening?.scene||null,
   engine,menu:!!q('#innmain'),cold:q('#inncold')?{id:q('#inncold').dataset.beat||q('#inncold').dataset.id,text:q('#inncold').innerText}:null,
   audio,amb,cinematic,opening,cg:cg?{uid:identity(cg),cut:cg.dataset.cut,css:css(cg),image:image(cg.querySelector('.cinema-picture'))}:null,
   cgCount:document.querySelectorAll('#inn-story-cg').length,veil:identity(veil),dialog:!!veil,
   actorImages:Array.from(document.querySelectorAll('#innstage img,#innstage svg image,#vnfig img,.fstalk .tfig img,.fstalk .tfig svg image')).map(image),actorCss:css(q('#innstage')),
   busts:safe(()=>withoutGame(window.__innDialogueState?.())),worldActors:Array.from(document.querySelectorAll('#bigscene image.wn9,#bigscene image.innseat')).map(e=>({k:e.dataset.k||'det1',crop:e.__worldCrop||null,posture:e.dataset.posture||null,...image(e)})),
   nightActors:Array.from(document.querySelectorAll('#inn-night-walk svg[data-surface]')).map(e=>({surface:e.dataset.surface,crop:e.getAttribute('viewBox'),src:e.querySelector('image')?.getAttribute('href')})),
   speaker:q('#vnbox .spk9')?{k:q('#vnbox .spk9').dataset.k,mood:q('#vnbox .spk9').dataset.mood,crop:q('#vnbox .spk9 img')?.dataset.crop,image:image(q('#vnbox .spk9 img')),expected:safe(()=>window.__innDialogueFace?.((q('#vnbox .spk9').dataset.k||'').split('|')[0],q('#vnbox .spk9').dataset.mood))}:null,
   worldBg:q('#bigscene>svg[data-bg]')?.dataset.bg||null,dialogBg:image(q('#dlgveil>.vnbg img')),
   banner:q('.banner,.placecard')?q('.banner,.placecard').innerText:null,night:!!q('#inn-night-walk'),
   foundText:q('#w209rail .n')?.innerText||null,
   media:Array.from(document.querySelectorAll('audio')).map(e=>({src:e.currentSrc||e.src,paused:e.paused,time:+e.currentTime.toFixed(2),volume:e.volume})),
   ac:safe(()=>typeof window.__T==='function'?window.__T('AC&&AC.state'):null)};
 };
 function tick(){if(trace.stopped)return;const s=window.__qaPresentationState();trace.frames.push(s);
  const key=JSON.stringify([s.sid,s.menu,s.cold?.id,s.audio?.line,s.amb?.music,s.amb?.want,s.cg?.uid,s.cg?.cut,s.cg?.css?.visibility,s.actorCss?.visibility,s.worldBg,s.banner,s.night]);
  if(key!==trace.last){trace.last=key;trace.changes.push(s)}requestAnimationFrame(tick)}
 window.addEventListener('load',()=>requestAnimationFrame(tick),{once:true});
})();'''


def contiguous_intervals(frames, predicate):
    intervals, start, end = [], None, None
    for row in frames:
        if predicate(row):
            if start is None:
                start = row
            end = row
        elif start is not None:
            intervals.append({'start':start['t'],'end':end['t'],
                              'ms':round(end['t']-start['t'],1),
                              'line':(start.get('audio') or {}).get('line'),
                              'sid':start['sid']})
            start = None
    if start is not None:
        intervals.append({'start':start['t'],'end':end['t'],'ms':round(end['t']-start['t'],1),
                          'line':(start.get('audio') or {}).get('line'),'sid':start['sid']})
    return intervals


def check_wrapper(page):
    """Read the production wrapper transform; never alter its orientation."""
    if not page.locator('#game').count():return None
    matrix=page.locator('#game').evaluate('e=>{const m=new DOMMatrix(getComputedStyle(e).transform);return [m.a,m.b,m.c,m.d]}')
    x,y=math.hypot(*matrix[:2]),math.hypot(*matrix[2:])
    assert x>0 and abs(x-y)<1e-7,('Nonuniform production wrapper scale',matrix)
    assert abs(matrix[0]*matrix[2]+matrix[1]*matrix[3])<1e-7,('Sheared production wrapper',matrix)
    if page.viewport_size['height']>page.viewport_size['width']:
        assert abs(matrix[0])<1e-7 and abs(matrix[3])<1e-7 and abs(matrix[1])>0 and abs(matrix[2])>0,('Portrait wrapper lost forced landscape rotation',matrix)
    return matrix


def check_art_trace(trace,manifest):
    """World and close art may share a PNG, but must use distinct authored crops."""
    seen_world=set();seen_night=set();speakers=0
    for row in trace['frames']:
        for actor in row['worldActors']:
            art=manifest.get('world',{}).get(actor['k'])
            if art and actor['crop']:
                assert actor['src']==art['src'] and actor['crop']==art['crop'],actor
                seen_world.add(actor['k'])
        for actor in row.get('nightActors',[]):
            # Bedroom and corridor both show the child inside the world;
            # close dialogue has its own stage surface, never a legless actor.
            assert actor['surface'] in ('world','room'),actor
            art=manifest['world']['det1']
            assert actor['src']==art['src'] and [float(v) for v in actor['crop'].split()]==art['crop'],actor
            seen_night.add(actor['surface'])
        speaker=row.get('speaker');expected=speaker and speaker.get('expected')
        if row['dialog'] and speaker and expected:
            # The native observer can take one task before refreshing the DOM;
            # count settled, correct faces rather than assert transitional data.
            desired='|'.join(map(str,[(speaker['k'] or '').split('|')[0],expected['src'],expected['x'],expected['y'],expected['size']]))
            if speaker['crop']==desired and speaker['image']['src']==expected['src']:speakers+=1
    assert seen_night=={'world','room'},('Bedroom/corridor full-body crops not exercised',seen_night)
    assert speakers>0,'No actual speaker face matched its new authored crop'
    return {'worldCharacters':sorted(seen_world),'nightSurfaces':sorted(seen_night),'matchedSpeakerFrames':speakers}


def summarize(trace):
    frames=trace['frames'];p1=[r for r in frames if r['sid']=='P1']
    visible=lambda r:bool(r['cg'] and r['cg']['css']['visibility']=='visible' and r['cg']['css']['display']!='none' and r['cg']['image'] and r['cg']['image']['loaded'])
    first_cg=next((r['t'] for r in p1 if visible(r) and r['cg']['cut']=='carriage'),float('inf'))
    last_family=max((r['t'] for r in p1 if visible(r) and r['cg']['cut']=='carriage'),default=first_cg)
    last_driver=max((r['t'] for r in p1 if visible(r) and r['cg']['cut']=='driver'),default=first_cg)
    gap=lambda r:r['sid']=='P1' and first_cg<=r['t']<=last_family and not visible(r)
    groups={}
    for row in frames:
        if row['sid'] and visible(row):
            groups.setdefault(row['sid']+':'+row['cg']['cut'],[]).append(row)
    within_cut_gaps={};invisible_frames={}
    for key, rows in groups.items():
        sid=rows[0]['sid'];lo,hi=rows[0]['t'],rows[-1]['t']
        gaps=contiguous_intervals(frames,lambda r:r['sid']==sid and lo<=r['t']<=hi and not visible(r))
        within_cut_gaps[key]=[r for r in gaps if r['ms']>=40]
        invisible_frames[key]=sum(r['sid']==sid and lo<=r['t']<=hi and not visible(r) for r in frames)
    return {'frames':len(frames),'changes':len(trace['changes']),
            'scenes':list(dict.fromkeys(r['sid'] for r in frames if r['sid'])),
            'CGInstancesByScene':{key:len({r['cg']['uid'] for r in rows}) for key,rows in groups.items()},
            'withinCutGapsOver40ms':within_cut_gaps,
            'withinCutInvisibleFrames':invisible_frames,
            'familyCGInstances':len({r['cg']['uid'] for r in p1 if r['cg'] and r['cg']['cut']=='carriage'}),
            'familyCGGapsOver40ms':[r for r in contiguous_intervals(frames,gap) if r['ms']>=40],
            'carriageDriverGapsOver40ms':[r for r in contiguous_intervals(frames,lambda r:r['sid']=='P1' and first_cg<=r['t']<=last_driver and not visible(r)) if r['ms']>=40],
            'carriageDriverInvisibleFrames':sum(r['sid']=='P1' and first_cg<=r['t']<=last_driver and not visible(r) for r in frames),
            'nightMusicWantedOver200ms':[r for r in contiguous_intervals(frames,lambda r:r['sid']=='P10b' and (r.get('amb') or {}).get('want') not in (None,'')) if r['ms']>=200],
            'bannerMusicOver100ms':[r for r in contiguous_intervals(frames,lambda r:bool(r['sid'] and r['banner'] and (r.get('amb') or {}).get('want'))) if r['ms']>=100],
            'duplicateCGFrames':sum(r['cgCount']>1 for r in frames)}


def menu_resume(browser,args,viewport,output):
    """Leave an actual new game's carriage, then use its actual Continue slot."""
    context=browser.new_context(viewport=viewport)
    context.add_init_script(LOGGER)
    page=context.new_page();errors=[];bad=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
    frame=page.locator('#game').element_handle().content_frame() if page.locator('#game').count() else page
    matrix=check_wrapper(page)
    if args.version:
        assert 'build='+args.version in frame.url,frame.url
        assert frame.evaluate('typeof __T')=='undefined'
    frame.locator('#innmain [data-m="new"]').click()
    deadline=time.monotonic()+90
    while not frame.locator('#inn-story-cg.ready').count() and time.monotonic()<deadline:
        if frame.locator('#inncold').count():
            try:frame.locator('#inncold').click(timeout=1000)
            except TimeoutError:
                if frame.locator('#inncold').count():raise
        else:page.keyboard.press('Enter')
        page.wait_for_timeout(180)
    assert frame.locator('#inn-story-cg.ready').count(),'Native new game failed to show its carriage'
    page.wait_for_timeout(500)
    before=frame.evaluate('__qaPresentationState()')
    frame.locator('#w209rail [data-more]:visible').first.click()
    frame.locator('#w209more [data-w="main"]').click()
    # Main may reload the native game document. Await the actual destination
    # rather than mistake its loader for a missing confirmation dialog.
    frame.locator('#innmain,.innconf').first.wait_for(state='visible',timeout=20000)
    confirmation=[]
    if not frame.locator('#innmain').count():
        buttons=frame.locator('.innconf button:visible')
        confirmation=buttons.all_inner_texts()
        accepted=next((i for i,t in enumerate(confirmation) if any(k in t for k in ('메인','돌아','확인','네')) and not any(k in t for k in ('취소','계속'))),None)
        assert accepted is not None,('Unrecognized native main confirmation',confirmation,frame.locator('body').inner_text()[-800:])
        buttons.nth(accepted).click()
    frame.locator('#innmain').wait_for(state='visible',timeout=5000)
    frame.wait_for_function('!!document.querySelector("#innmain [data-m=cont]:not([disabled])")',timeout=20000)
    page.wait_for_timeout(2200)
    main=frame.evaluate('__qaPresentationState()')
    assert not main['cg'] and not main['night'],'Old story image survived native main-menu entry'
    assert (main.get('amb') or {}).get('want') in (None,'inn_title'),main
    assert not (main.get('amb') or {}).get('dep'),'A captured carriage departure remained active in main'
    assert not (main.get('audio') or {}).get('heartbeatActive'),'A captured story pulse continued in main'
    assert not (main.get('audio') or {}).get('coldHeartbeat'),'Cold heartbeat remained after main'
    page.screenshot(path=str(output/f'menu-{args.viewport}.png'))
    frame.locator('#innmain [data-m="cont"]').click()
    deadline=time.monotonic()+50
    while not frame.locator('#inn-story-cg.ready').count() and time.monotonic()<deadline:
        page.keyboard.press('Enter');page.wait_for_timeout(200)
    assert frame.locator('#inn-story-cg.ready').count(),'Actual Continue failed to restore its carriage'
    page.wait_for_timeout(500)
    resumed=frame.evaluate('__qaPresentationState()')
    if args.version:
        assert 'build='+args.version in frame.url,frame.url
        assert frame.evaluate('typeof __T')=='undefined'
    assert resumed['sid']=='P1' and resumed['cg']['cut']=='carriage',resumed
    assert resumed['cgCount']==1,resumed
    assert (resumed.get('amb') or {}).get('want') in (None,'inn_travel'),resumed
    page.screenshot(path=str(output/f'menu-continue-{args.viewport}.png'))
    assert not errors,errors
    assert not bad,bad
    report={'url':frame.url,'wrapperMatrix':matrix,'actualFresh':True,'actualContinue':True,'confirmation':confirmation,'before':before,'main':main,'resumed':resumed,'errors':errors,'bad':bad}
    (output/f'menu-continue-{args.viewport}.json').write_text(json.dumps(report,ensure_ascii=False),encoding='utf-8')
    print('PASS actual fresh carriage → native main → actual Continue; stale CG/pulse/departure clear; JS/HTTP0',flush=True)
    context.close()


def native_talk(page,frame,args,output):
    """Question Grandma from the actually reached investigation, without clues."""
    if frame.locator('#closeNotice:visible').count():frame.locator('#closeNotice').click()
    page.wait_for_timeout(800)
    frame.locator('#w209rail .g>[data-w="move"]').click()
    frame.locator('#innmove [data-room-id="dining"]').click()
    page.wait_for_timeout(2200)
    point=None
    for direction in (None,'#fsar','#fsar','#fsal'):
        if direction and frame.locator(direction+':visible').count():
            frame.locator(direction).click();page.wait_for_timeout(700)
        point=frame.evaluate('''()=>{const r=document.querySelector('#bigscene').getBoundingClientRect();
          for(let y=Math.max(12,r.top+12);y<Math.min(innerHeight-12,r.bottom-12);y+=6)
           for(let x=Math.max(12,r.left+12);x<Math.min(innerWidth-12,r.right-12);x+=6)
            if(document.elementFromPoint(x,y)?.closest('#bigscene')&&[[0,0],[-6,0],[6,0],[0,-6],[0,6]].every(([dx,dy])=>window.__innNpcHit(x+dx,y+dy)==='innma'))return {x,y};return null}''')
        if point:break
    assert point,'Grandma has no reachable opaque character pixels in the actual dining room'
    world=frame.evaluate('__innWorldActors?__innWorldActors():__qaPresentationState().worldActors')
    manifest=frame.evaluate('window.__innDialogueManifest')
    world_grandma=next(a for a in world if a['k']=='innma')
    expected_world=manifest['world']['innma']
    assert world_grandma['src']==expected_world['src'] and world_grandma['crop']==expected_world['crop'],world_grandma
    assert world_grandma.get('maskReady'),world_grandma
    page.screenshot(path=str(output/f'world-dining-{args.viewport}.png'))
    if page.locator('#game').count():
        point=page.locator('#game').evaluate('''(e,p)=>{const m=new DOMMatrix(getComputedStyle(e).transform),r=e.getBoundingClientRect(),q=m.transformPoint(new DOMPoint(p.x,p.y)),corners=[[0,0],[e.clientWidth,0],[0,e.clientHeight],[e.clientWidth,e.clientHeight]].map(([x,y])=>m.transformPoint(new DOMPoint(x,y)));return {x:r.left+q.x-Math.min(...corners.map(c=>c.x)),y:r.top+q.y-Math.min(...corners.map(c=>c.y))}}''',point)
    page.mouse.click(point['x'],point['y']);page.wait_for_timeout(1000)
    for _ in range(100):
        if not frame.locator('#dlgveil').count():break
        page.keyboard.press('Enter');page.wait_for_timeout(200)
    else:raise AssertionError('Native NPC greeting did not finish')
    frame.locator('.fstalk').wait_for(state='visible')
    page.wait_for_timeout(500)
    talk=frame.evaluate('__innDialogueState()')
    assert any(a['k']=='innma' and a['surface']=='talk' for a in talk['actors']),talk
    assert frame.locator('.fstalk svg.dialogue-bust[data-k="innma"]').is_visible(),'Native question view has a hidden bust'
    dialogue_sources={a['src'] for a in talk['assets']}
    assert expected_world['crop']!=manifest['characters']['innma']['neutral']['crop'],'World and dialogue crops are identical'
    page.screenshot(path=str(output/f'talk-{args.viewport}.png'))
    topic=frame.locator('.fstalk .topic:not([disabled]):visible').first
    assert topic.count(),'Native Grandma talk has no reachable question'
    question=topic.inner_text();topic.click();page.wait_for_timeout(550)
    frame.locator('#dlgveil').wait_for(state='visible')
    for _ in range(80):
        reply=frame.evaluate('__innAudioState()')
        if reply['who']=='innma':break
        assert frame.locator('#dlgveil').count(),('Native question ended before Grandma replied',question,reply)
        page.keyboard.press('Enter');page.wait_for_timeout(220)
    else:raise AssertionError(('Native question never reached Grandma reply',question,reply))
    page.wait_for_timeout(500)
    dialogue=frame.evaluate('__innDialogueState()')
    page.screenshot(path=str(output/f'talk-question-{args.viewport}.png'))
    diagnostics=frame.evaluate('''()=>({body:document.body.className,fig:document.querySelector('#dlgveil #vnfig')?.outerHTML||null,
      actors:Array.from(document.querySelectorAll('#dlgveil img,#dlgveil svg image,.fstalk .tfig img,.fstalk .tfig svg image')).map(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e),src=e.getAttribute('src')||e.getAttribute('href')||'';return {host:e.closest('#vnfig,#innstage,.tfig,.spk9')?.id||e.closest('#vnfig,#innstage,.tfig,.spk9')?.className,src:src.startsWith('data:')?src.slice(0,90):src,visible:r.width>0&&r.height>0&&c.visibility==='visible'&&c.display!=='none',rect:{x:r.x,y:r.y,w:r.width,h:r.height},visibility:c.visibility,display:c.display}})})''')
    (output/f'talk-question-diagnostic-{args.viewport}.json').write_text(json.dumps({'dialogue':dialogue,'diagnostics':diagnostics},ensure_ascii=False),encoding='utf-8')
    # Native talk replies intentionally retain the question panel's tfig;
    # direct story dialogue uses innstage. Validate the visible art and actual
    # speaker, rather than prescribe one of these native presentation hosts.
    assert any(a['k']=='innma' and a['surface'] in ('stage','talk') for a in dialogue['actors']),dialogue
    visible=frame.locator('#innstage svg.dialogue-bust[data-k="innma"]:visible,.fstalk svg.dialogue-bust[data-k="innma"]:visible')
    assert visible.count()==1,('Native reply does not have exactly one visible Grandma bust',dialogue,diagnostics)
    assert visible.first.get_attribute('data-src') in dialogue_sources,dialogue
    expression=visible.first.get_attribute('data-expression')
    expected_bust=manifest['characters']['innma'][expression]
    assert visible.first.get_attribute('data-src')==expected_bust['src'],dialogue
    assert [float(v) for v in visible.first.get_attribute('viewBox').split()]==expected_bust['crop'],dialogue
    face=frame.evaluate('__qaPresentationState().speaker')
    expected_face='|'.join(map(str,['innma',expected_bust['src'],*expected_bust['face']]))
    assert face['k'].split('|')[0]=='innma' and face['crop']==expected_face and face['image']['src']==expected_bust['src'],face
    assert not frame.locator('#dlgveil #vnfig:visible').count(),'Legacy reply figure overlaps the bust'
    assert not frame.locator('#inn-story-cg').count(),'Opening CG overlaps the actual investigation question'
    page.screenshot(path=str(output/f'talk-question-{args.viewport}.png'))
    report={'actualReachedInvestigation':True,'actualNativeNpc':True,'question':question,'reply':reply,'world':world,'talk':talk,'dialogue':dialogue,'replyFace':face,'authoredWorld':expected_world,'authoredBust':expected_bust}
    (output/f'talk-{args.viewport}.json').write_text(json.dumps(report,ensure_ascii=False),encoding='utf-8')
    print('PASS actual investigation → opaque Grandma pointer → native question → actual Grandma reply with one visible dialogue bust; full-body/bust/face authored source+crop match',flush=True)


def saved_talk(browser,args,viewport,output):
    context=browser.new_context(viewport=viewport,storage_state=args.save)
    context.add_init_script(LOGGER)
    page=context.new_page();errors=[];bad=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
    page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
    frame=page.locator('#game').element_handle().content_frame() if page.locator('#game').count() else page
    check_wrapper(page)
    if args.version:
        assert 'build='+args.version in frame.url,frame.url
        assert frame.evaluate('typeof __T')=='undefined'
    frame.locator('#innmain [data-m="cont"]').click();page.wait_for_timeout(1800)
    native_talk(page,frame,args,output)
    assert not errors,errors
    assert not bad,bad
    print('PASS actual stored investigation Continue; no evidence preparation; JS/HTTP0',flush=True)
    context.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--version',help='Require exact build= version and no __T in a production wrapper')
    parser.add_argument('--mode',choices=['fast','slow','both'],default='both')
    parser.add_argument('--viewport',choices=['landscape','portrait'],default='landscape')
    parser.add_argument('--output',default='/tmp/presentation-timing')
    parser.add_argument('--deadline',type=int,default=420)
    parser.add_argument('--frozen-html',help='Serve an unchanged captured baseline bundle for this fresh-play browser run')
    parser.add_argument('--expect-stable',action='store_true',help='Require one CG instance per authored cut and no native direction gaps')
    parser.add_argument('--check-menu',action='store_true',help='Also use native main/Continue during an actual new carriage scene')
    parser.add_argument('--only-menu',action='store_true',help='Run the native main/Continue cancellation check only')
    parser.add_argument('--check-talk',action='store_true',help='Question Grandma from the actual reached investigation and verify separate bust art')
    parser.add_argument('--only-talk',action='store_true',help='Run native talk from an actual previously collected investigation save only')
    parser.add_argument('--save',help='Actual browser storage_state for --only-talk; no prepared clue fixture')
    args=parser.parse_args();output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    if args.only_talk and not args.save:parser.error('--only-talk requires --save')
    viewport={'width':844,'height':390} if args.viewport=='landscape' else {'width':390,'height':844}
    speeds=[] if args.only_menu or args.only_talk else ['fast','slow'] if args.mode=='both' else [args.mode]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        for speed in speeds:
            context=browser.new_context(viewport=viewport)
            if args.frozen_html:
                body=Path(args.frozen_html).read_bytes()
                context.route(args.url.split('?')[0]+'*',lambda route:route.fulfill(status=200,content_type='text/html',body=body))
            context.add_init_script(LOGGER)
            page=context.new_page();errors=[];bad=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
            page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
            frame=page.locator('#game').element_handle().content_frame() if page.locator('#game').count() else page
            matrix=check_wrapper(page)
            source_hash=hashlib.sha256(frame.content().encode()).hexdigest()[:12]
            if args.version:
                assert 'build='+args.version in frame.url,(frame.url,args.version)
                assert frame.evaluate('typeof __T')=='undefined','QA evaluation hook leaked into production'
            frame.locator('#innmain [data-m="new"]').click()
            deadline=time.monotonic()+args.deadline;seen=set();previous=None;previous_cg=None;inputs=0;done=False;driver_seen=False
            while time.monotonic()<deadline:
                state=frame.evaluate('__qaPresentationState()');sid=state['sid'];line=(state.get('audio') or {}).get('line','')
                if (state.get('audio') or {}).get('who')=='karo' and sid=='P1':driver_seen=True
                if sid!=previous:
                    print(speed,'scene',sid,'line',line,'CG',state['cg'] and state['cg']['cut'],'music',state.get('amb'),flush=True);previous=sid
                cg_key=(sid,state['cg'] and state['cg']['uid'],state['cg'] and state['cg']['cut'])
                if cg_key!=previous_cg:
                    print(speed,'camera',cg_key,'line',line,'dialog',state['dialog'],'world',state['worldBg'],flush=True);previous_cg=cg_key
                shot=None
                if state['cg'] and state['cg']['css']['visibility']=='visible':shot=state['cg']['cut']
                if state['night']:shot='night-'+str((state.get('opening') or {}).get('cue') or 'wake')
                if sid in ('P3','P11','P12') and state['dialog']:shot=sid
                if driver_seen and sid=='P1' and not state['cg'] and state['dialog']:shot='driver-camera'
                if shot and shot not in seen:
                    page.wait_for_timeout(500)
                    page.screenshot(path=str(output/f'{speed}-{args.viewport}-{shot}.png'));seen.add(shot)
                has_p13='P13' in frame.evaluate('__qaPresentationTrace.changes.map(r=>r.sid)')
                if has_p13 and not sid and not state['dialog'] and not state['cold'] and not state['banner']:
                    done=True;page.wait_for_timeout(600)
                    page.screenshot(path=str(output/f'{speed}-{args.viewport}-investigation.png'))
                    context.storage_state(path=str(output/f'{speed}-{args.viewport}-actual-investigation.json'));break
                if state['cold']:
                    try:frame.locator('#inncold').click(timeout=1000)
                    except TimeoutError:
                        if frame.locator('#inncold').count():raise
                elif state['dialog']:
                    # Native dialogue plate taps and native Enter, in blocks so
                    # each mode gets both typing-completion and advancement.
                    target=frame.locator('#vnbox .vtxt').first
                    if inputs%8<4 and target.count():target.click()
                    else:page.keyboard.press('Enter')
                    inputs+=1
                else:page.keyboard.press('Enter')
                page.wait_for_timeout(180 if speed=='fast' else 800)
            frame.evaluate('__qaPresentationTrace.stopped=true')
            trace=frame.evaluate('__qaPresentationTrace');summary=summarize(trace)
            manifest=frame.evaluate('window.__innDialogueManifest')
            art_summary=check_art_trace(trace,manifest) if manifest.get('world') else None
            report={'url':frame.url,'sourceHash':source_hash,'mode':speed,'viewport':viewport,'wrapperMatrix':matrix,'artSummary':art_summary,'actualFresh':True,
                    'finishedInvestigation':done,'inputs':inputs,'errors':errors,'bad':bad,'summary':summary,'trace':trace}
            (output/f'{speed}-{args.viewport}.json').write_text(json.dumps(report,ensure_ascii=False),encoding='utf-8')
            print('RESULT',json.dumps({k:v for k,v in report.items() if k!='trace'},ensure_ascii=False),flush=True)
            assert done,('Fresh opening failed to reach investigation',state)
            assert not errors,errors
            assert not bad,bad
            if args.expect_stable:
                for key in ('P1:driver','P2:village','P13:seal'):
                    assert summary['CGInstancesByScene'].get(key)==1,(key,summary)
                    assert not summary['withinCutGapsOver40ms'].get(key),(key,summary)
                    assert not summary['withinCutInvisibleFrames'].get(key),(key,summary)
                assert summary['familyCGInstances']==1,summary
                assert not summary['familyCGGapsOver40ms'],summary
                assert not summary['carriageDriverGapsOver40ms'],summary
                assert not summary['carriageDriverInvisibleFrames'],summary
                assert not summary['nightMusicWantedOver200ms'],summary
                assert not summary['bannerMusicOver100ms'],summary
                assert not summary['duplicateCGFrames'],summary
            if args.check_talk:
                native_talk(page,frame,args,output)
                assert not errors,errors
                assert not bad,bad
            context.close()
        if args.check_menu or args.only_menu:menu_resume(browser,args,viewport,output)
        if args.only_talk:saved_talk(browser,args,viewport,output)
        browser.close()


if __name__=='__main__':main()
