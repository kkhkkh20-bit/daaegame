"""Prepared native P10b→P13 opening presentation regression.

The fixture starts the existing __innStart controller at authored P10b with no
collected evidence. It uses real Enter and pointer input, native banner promises
and dialogue. It checks layout/source/cues rather than judging source art style.
"""
import argparse
import json
import shutil
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--only-layout',choices=['landscape','portrait'],help='Focused layout regression')
    args=parser.parse_args()
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        for name,viewport,reduced in [('landscape',{'width':844,'height':390},'no-preference'),
                                      ('portrait',{'width':390,'height':844},'reduce')]:
            if args.only_layout and name!=args.only_layout:continue
            page=browser.new_page(viewport=viewport,reduced_motion=reduced)
            errors=[];bad=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
            page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
            def engine(code):return page.evaluate('(code)=>window.__T(code)',code)
            engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
            page.evaluate('document.querySelector("#innmain").remove();window.__w209boot()');page.wait_for_timeout(1400)
            assert page.evaluate('typeof __innOpeningDirection==="function"'),'Build lacks opening direction module'
            engine('if(DL){DL.done=null;endDlg()};G.beats={inn_pi:EP1INN.PRO.findIndex(s=>s.sid==="P10b")};window.__innStart()')
            required=set();cues=[];banners=set();pointer_turns=0;keyboard_turns=0;facts=[];last_input=None;advanced={'pointer':0,'keyboard':0};bedroom_seen=False;dim_seen=set()
            for turn in range(1000):
                state=engine('({sid:G.beats.inn_psid,done:!!G.beats.inn_pro,dl:!!DL,i:DL&&DL.i,row:DL&&DL.lines[DL.i],found:G.found.slice()})')
                row=state['row'];who=row[0] if isinstance(row,list) else None
                text=(row[7] if len(row)>7 and row[7] else row[1]) if isinstance(row,list) else ''
                if text:facts.append(text)
                identity=(state['sid'],state['i'],text)
                if last_input and last_input[1]!=identity:
                    advanced[last_input[0]]+=1
                last_input=None
                # The native panel auto-removes. Snapshot in one browser task
                # so count/rect/text reads cannot race its expiration callback.
                panel=page.evaluate("""()=>{const e=document.querySelector('.banner.inn-place-panel .mid');
                  if(!e)return null;const sid=__T('G.beats.inn_psid'),a=EP1INN.PRO.find(x=>x.sid===sid);
                  return {bounds:e.getBoundingClientRect().toJSON(),text:e.innerText,icons:e.querySelectorAll('.place-time-icon svg').length,
                    sid:sid,title:a&&a.title,sub:a&&a.sub}}""")
                if panel and panel['sid'] not in banners:
                    bounds=panel['bounds'];content=panel['text'].replace('\xa0',' ')
                    assert content.strip(),('Empty location/time panel',state)
                    assert bounds['width']<=min(480,viewport['width']-15) and bounds['height']<=150,('Large opening banner still covers scene',bounds,content)
                    assert panel['icons']==1,'Location/time icon absent or duplicated'
                    assert panel['title'] in content and panel['sub'] in content,('Native place/time lost',panel)
                    banners.add(panel['sid'])
                direction=page.evaluate('()=>Object.assign(__innOpeningDirection(),{nodeCount:document.querySelectorAll("#inn-night-walk").length})')
                if direction['night'] and state['sid']!='P10b':
                    page.wait_for_timeout(220)
                    direction=page.evaluate('()=>Object.assign(__innOpeningDirection(),{nodeCount:document.querySelectorAll("#inn-night-walk").length})')
                assert direction['nodeCount']<=1,('Duplicate night overlays',direction)
                # Automatic fade may remove the scene between readbacks. Active
                # native dialogue is stable until this test sends the next input.
                if direction['night'] and state['dl']:
                    assert state['sid']=='P10b',('Night overlay leaks into another scene',state,direction)
                    assert direction['nodeCount']==1,('Night API disagrees with its DOM',direction)
                    assert page.locator('#inn-night-walk').evaluate('e=>getComputedStyle(e).pointerEvents')=='none','Night overlay blocks input'
                    hint=page.locator('#inn-night-walk').inner_text()
                    assert not any(x in hint for x in ['C04','솜솜','바구니','열세 번째 침대']),('Night cue reveals investigation answer',hint)
                    cue=direction.get('cue')
                    if not cue and state['dl'] and not bedroom_seen:
                        room=page.locator('#inn-night-walk .night-bedroom')
                        assert float(room.evaluate('e=>getComputedStyle(e).opacity'))==1,'Wake bedroom is hidden'
                        child=page.locator('#inn-night-walk .night-room-child image')
                        r=child.bounding_box()
                        assert r and r['x']<viewport['width'] and r['x']+r['width']>0 and r['y']<viewport['height'] and r['y']+r['height']>0,('Wake Daram lies outside viewport',r)
                        assert 'daram-worried-dialogue.png' in child.get_attribute('href'),'Wake Daram uses wrong approved expression'
                        page.screenshot(path='/tmp/opening-'+name+'-wake-bedroom.png')
                        bedroom_seen=True
                    if cue in ('out','touch') and cue not in dim_seen:
                        # Allow the existing short filter/opacity transition to
                        # settle without skipping a native line or banner.
                        page.wait_for_timeout(400)
                        room_alpha=float(page.locator('#inn-night-walk .night-bedroom').evaluate('e=>getComputedStyle(e).opacity'))
                        filt=page.locator('#bigscene>svg[data-bg]').first.evaluate('e=>getComputedStyle(e).filter')
                        expected='.58' if cue=='out' else '.43'
                        assert room_alpha==0,('Bedroom remains over corridor',cue,room_alpha)
                        assert ('brightness(0'+expected+')') in filt,('Night corridor stays bright',cue,filt)
                        dim_seen.add(cue)
                    if cue and cue not in cues:
                        cues.append(cue)
                        if reduced=='reduce':
                            moving=page.locator('#inn-night-walk').evaluate('e=>e.getAnimations({subtree:true}).filter(a=>a.playState==="running").map(a=>({type:a.constructor.name,name:a.animationName,property:a.transitionProperty,target:a.effect.target.tagName,cls:a.effect.target.getAttribute("class"),id:a.effect.target.id}))')
                            assert not moving,('Reduced-motion night path animates',cue,moving)
                        page.screenshot(path='/tmp/opening-'+name+'-night-'+cue+'.png')
                key=(state['sid'],who)
                if state['sid'] in ['P10b','P12','P13'] and who in ['geokkuri','wanggu'] and key not in required:
                    page.wait_for_timeout(220)
                    image=page.locator('#innstage .isf img').first
                    source=image.get_attribute('src');bounds=image.bounding_box()
                    page.screenshot(path='/tmp/opening-'+name+'-'+state['sid']+'.png')
                    assert image.evaluate('i=>i.complete&&i.naturalWidth>0'),('Actor art not loaded',source)
                    if who=='geokkuri':
                        assert 'action-poses/bami/dialogue.png' in source,('Bami stands upright during ceiling encounter',source)
                    else:
                        assert 'neoul' in source,('Wrong Neoul actor',source)
                        im=Image.open(ROOT/source.split('?')[0]).convert('RGBA')
                        alpha=im.getchannel('A').point(lambda v:255 if v>15 else 0).getbbox()
                        bottom=bounds['y']+alpha[3]/im.height*bounds['height']
                        plates=page.locator('#vnbox .vtxt').evaluate_all('xs=>xs.map(e=>e.getBoundingClientRect().toJSON()).filter(r=>r.height>10)')
                        assert plates, 'Native dialogue plate missing'
                        plate_top=min(r['top'] for r in plates)
                        assert bottom>=plate_top-1,('Cropped actor body end floats above dialogue baseline',source,bottom,plate_top)
                        print(name,state['sid'],'actor',source,'alpha',alpha,'screen bottom',round(bottom,1),'dialogue top',round(plate_top,1),flush=True)
                    required.add(key);page.screenshot(path='/tmp/opening-'+name+'-'+state['sid']+'.png')
                assert not any(x in state['found'] for x in ['C04','C05','C08']),('Opening cue grants later investigation evidence',state)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Opening creates horizontal overflow'
                if state['done']:break
                if state['dl']:
                    # Group input samples: strict alternation can always let
                    # one mode fill text and the other advance it.
                    if turn%8<4:
                        page.keyboard.press('Enter');keyboard_turns+=1;last_input=('keyboard',identity)
                    else:
                        target=page.locator('#vnbox .vtxt').first
                        if target.count() and target.bounding_box():
                            target.click();pointer_turns+=1;last_input=('pointer',identity)
                        else:page.keyboard.press('Enter');keyboard_turns+=1;last_input=('keyboard',identity)
                page.wait_for_timeout(180)
            assert state['done'],('Native opening did not finish',state)
            assert required=={('P10b','geokkuri'),('P12','wanggu'),('P13','wanggu')},required
            assert bedroom_seen and dim_seen=={'out','touch'},('Wake face or corridor darkening missing',bedroom_seen,dim_seen)
            assert cues==['out','touch','return'],('Night path cues missing/out of order',cues)
            assert 'P10b' in banners and 'P12' in banners and 'P13' in banners,('Native place/time transitions absent',banners)
            assert pointer_turns>4 and keyboard_turns>4,('Both native input modes were not exercised',pointer_turns,keyboard_turns)
            assert advanced['pointer']>4 and advanced['keyboard']>4,('Native input failed to advance dialogue',advanced)
            page.wait_for_timeout(500)
            assert not page.locator('#inn-night-walk').count(),'Night overlay persists into investigation'
            assert not errors,errors
            assert not bad,bad
            print(name,'PASS native opening progression / upside-down Bami / night cues / compact place-time / baseline / later evidence withheld',flush=True)
            page.close()
        browser.close()
    print('PASS opening presentation; JavaScript and HTTP errors: 0',flush=True)


if __name__=='__main__':main()
