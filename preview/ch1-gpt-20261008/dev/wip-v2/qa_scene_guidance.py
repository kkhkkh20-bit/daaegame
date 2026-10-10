"""Scene guidance regression through real pointer inputs.

The fixture completes the introduction only. Evidence is never seeded: C01,
C02, C04 and C08 must be collected through the player's scene interactions.
Run against the generated QA bundle (which exposes the read-only/state setup
__T hook). This is focused investigation QA, not an entire fresh-game run.
"""
import argparse
import json
import shutil

from playwright.sync_api import sync_playwright


class Investigation:
    def __init__(self, page):
        self.page = page
        self.errors = []
        self.captured = set()
        self.spoken = []
        page.on('pageerror', lambda error: self.errors.append(str(error)))

    def engine(self, code):
        return self.page.evaluate('(code) => window.__T(code)', code)

    def state(self):
        return self.engine('({found:G.found.slice(),asked:G.asked.slice(),'
                           'obs:(G.obsSeen||[]).slice(),dl:!!DL,'
                           'room:CASES[G.ci].locations[G.loc].id,tab:G.tab})')

    def drain(self, limit=500):
        quiet = 0
        for _ in range(limit):
            line = self.engine('DL&&DL.lines&&DL.lines[DL.i]?'
                               '[DL.lines[DL.i][0],String(DL.lines[DL.i][7]||DL.lines[DL.i][1]||"")]:null')
            if line and (not self.spoken or self.spoken[-1] != line):
                self.spoken.append(line)
            shot = self.page.evaluate("""()=>{
                const scene=document.querySelector('#inn-under-scene'),image=scene&&scene.querySelector('.under-held');
                const rect=image&&image.getBoundingClientRect(),style=image&&getComputedStyle(image);
                return {stage:scene&&scene.dataset.stage,held:image?{loaded:image.complete&&image.naturalWidth>0,
                    src:image.getAttribute('src'),visible:rect.width>0&&rect.height>0&&style.display!=='none'&&style.visibility!=='hidden'&&+style.opacity>0}:null};
            }""")
            stage = shot['stage']
            if stage:
                if stage == 'held':
                    held = shot['held']
                    assert held and held['visible'], 'Rescued guest illustration is hidden'
                    assert held['loaded'], 'Rescued guest illustration failed to load'
                    assert 'somsom-held.png' in held['src'], 'Wrong rescue illustration'
                if stage not in self.captured:
                    self.page.screenshot(path='/tmp/scene-guidance-' + stage + '.png')
                    self.captured.add(stage)
            buttons = self.page.locator(
                '#innins [data-k="next"]:visible,'
                '#innins [data-k="ok"]:visible,#okfind:visible')
            if buttons.count():
                buttons.first.click()
                quiet = 0
                self.page.wait_for_timeout(450)
            elif self.state()['dl']:
                self.page.keyboard.press('Enter')
                quiet = 0
                self.page.wait_for_timeout(200)
            else:
                quiet += 1
                self.page.wait_for_timeout(200)
                if quiet >= 10:
                    return
        raise AssertionError(('Dialogue failed to finish', self.state(),
                              self.page.locator('body').inner_text()[-600:]))

    def click(self, selector):
        """Require a real reachable element; never force a hidden hotspot."""
        self.page.wait_for_timeout(800)
        target = self.page.locator(selector + ':visible').first
        target.wait_for(state='visible')
        box = target.bounding_box()
        assert box, ('No pointer rectangle', selector)
        viewport = self.page.viewport_size
        x, y = box['x'] + box['width']/2, box['y'] + box['height']/2
        assert 0 < x < viewport['width'] and 0 < y < viewport['height'], (
            'Target outside viewport', selector, box)
        self.page.mouse.click(x, y)
        self.page.wait_for_timeout(300)

    def collect(self, evidence):
        print('Investigating', evidence, flush=True)
        before = self.state()['found']
        assert evidence not in before, ('Already collected', evidence)
        self.click('#bigscene [data-spot="' + evidence + '"]')
        self.drain()
        assert evidence in self.state()['found'], (
            'Single deliberate investigation did not collect evidence',
            evidence, self.state())
        print('Collected', evidence, flush=True)

    def open_map(self):
        self.click('#w209rail .g>[data-w="move"]')
        self.page.locator('#innmove[data-space-map]').wait_for(state='visible')

    def move(self, room):
        self.open_map()
        self.click('#innmove [data-room-id="' + room + '"]')
        self.drain()
        assert self.state()['room'] == room, self.state()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8000/playT.html')
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=shutil.which('chromium'), args=['--no-sandbox'])
        context = browser.new_context(viewport={'width':844,'height':390})
        page = context.new_page()
        qa = Investigation(page)
        page.goto(args.url, wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        qa.engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));'
                  'S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1};')
        page.evaluate('()=>{document.querySelector("#innmain").remove();'
                      'window.__w209boot()}')
        page.wait_for_timeout(1500)
        qa.drain()
        assert not qa.state()['found'], ('Fixture granted evidence', qa.state())
        assert qa.state()['room'] == 'bed13', qa.state()
        powder = '#bigscene image[data-world-prop="C02_trace"]'
        assert page.locator(powder).is_visible(), 'Powder clue has no visible scene trace'
        assert float(page.locator(powder).evaluate('e=>getComputedStyle(e).opacity')) >= .8, (
            'Powder trace is too faint to see')
        under = '#bigscene [data-obs="o_under"]'
        sleeping = '#bigscene [data-scene-trace="sleeping-guest"]'
        assert page.locator(sleeping).count() == 1, 'Sleeping guest has no physical trace before discovery'
        assert 0 < float(page.locator(sleeping).evaluate('e=>getComputedStyle(e).opacity')) < .6, 'Sleeping guest is not faint'
        decoration = page.locator(under).evaluate('''e=>{let c=getComputedStyle(e);return {
          border:c.borderWidth,background:c.backgroundColor,shadow:c.boxShadow,
          before:getComputedStyle(e,'::before').display,after:getComputedStyle(e,'::after').display,
          icon:e.querySelectorAll('.under-cue-icon').length}}''')
        assert decoration == {'border':'0px','background':'rgba(0, 0, 0, 0)','shadow':'none','before':'none','after':'none','icon':0}, ('Under-bed target has a visible box or icon', decoration)
        page.evaluate('window.__pointAt("[data-obs=o_under]")')
        assert not page.locator('.ptring').count(), 'Explicit hint draws an answer ring around the hidden guest'
        initial = page.locator(under).bounding_box()
        assert initial and page.locator(under).is_visible(), 'Under-bed curiosity is hidden'
        assert 'innunderlook9' not in (page.locator(under).get_attribute('class') or ''), (
            'Old flashing target remains')
        assert not page.locator('#inn-under-scene').count()
        qa.collect('C01')
        qa.collect('C02')
        page.wait_for_timeout(1100)
        assert not page.locator('.ptring').count(), 'Collecting early clues automatically draws an answer ring'
        assert page.locator(sleeping).count() == 1, 'Early clue collection removed the sleeping guest'
        after = page.locator(under).bounding_box()
        assert all(abs(initial[key]-after[key]) < 2 for key in ('x','y')), (
            'Under-bed target appeared at a new position', initial, after)
        assert 'C04' not in qa.state()['found'] and 'o_under' not in qa.state()['obs'], (
            'Collecting two clues automatically discovered Somsom', qa.state())
        assert not page.locator('#inn-under-scene').count()
        assert not page.locator('#bigscene [data-spot="C04"]:visible').count(), (
            'Basket appeared before the under-bed investigation')

        # Record every authored visual stage independently of polling intervals.
        page.evaluate('''()=>{
          window.__sceneQAStages=[];
          function record(p){p=p||document.querySelector('#inn-under-scene');
            if(p&&p.dataset.stage){let a=window.__sceneQAStages;
              if(a[a.length-1]!==p.dataset.stage)a.push(p.dataset.stage)}}
          window.__sceneQAObserver=new MutationObserver(ms=>{
            ms.forEach(m=>{if(m.target.id==='inn-under-scene')record(m.target);
              m.removedNodes.forEach(n=>{if(n.id==='inn-under-scene')record(n)})});
            record();});
          window.__sceneQAObserver.observe(document.body,
            {childList:true,subtree:true,attributes:true,attributeFilter:['data-stage']});
          record();
        }''')
        qa.spoken = []
        qa.click(under)
        assert 'C04' not in qa.state()['found'], 'Discovery granted evidence before its scene'
        qa.drain()
        stages = page.evaluate('window.__sceneQAStages')
        assert stages == ['dark','fur','light','body','held','basket'], (
            'Missing authored discovery stages', stages, qa.errors, qa.state())
        assert qa.state()['found'].count('C04') == 1 and 'o_under' in qa.state()['obs'], (
            'Single investigation did not complete observation and evidence', qa.state())
        buri_lines = ' '.join(text for speaker,text in qa.spoken if speaker == 'buri')
        assert '장치공 부리' in buri_lines and '차갑고' in buri_lines and '다 식으면 끝이죠' in buri_lines, (
            'Automatic discovery skipped the Buri testimony needed for the meeting', qa.spoken)
        assert not page.locator('#inn-under-scene').count(), 'Discovery visual did not close'
        assert 'held' in qa.captured, 'Rescue illustration was never checked while visible'
        assert not page.locator(sleeping).count(), 'Rescued guest remains hidden under the bed'
        print('PASS faint physical trace → six discovery stages/loaded rescue illustration → Buri introduction/cold claim → one C04', flush=True)

        # The scene remains legible after a modal and an actual room round trip.
        trace = '#bigscene [data-scene-trace="headboard"]'
        assert page.locator(trace).is_visible(), 'Headboard has no visible scene trace'
        acquired = qa.state()['found'][:]
        qa.open_map()
        assert page.locator('#innmove .map-floor').count() == 3, 'Floor map is incomplete'
        qa.click('#innmove [data-x]')
        assert page.locator(trace).is_visible(), 'Map cancellation removed the scene trace'
        assert qa.state()['found'] == acquired, 'Map cancellation changed evidence'
        qa.move('hall')
        qa.open_map()
        page.locator('#innmove [data-room-id="dotoroom"]').focus()
        hint = page.locator('#inn-map-purpose').inner_text()
        assert '일지' in hint and '자정' not in hint, ('Doto purpose missing/spoiled', hint)
        qa.click('#innmove [data-room-id="dotoroom"]')
        qa.drain()
        assert qa.state()['room'] == 'dotoroom'
        assert 'C08' not in qa.state()['found'], 'Room entry granted the diary automatically'
        # Examine the pre-acquisition observation scripts without changing G.
        before_diary = page.evaluate('window.EP1INN.LOOK.dotoroom.map(x=>[x[4],x[5]]).flat(Infinity).join(" ")')
        assert '일지' in before_diary and '자정' not in before_diary, before_diary
        qa.collect('C08')
        qa.move('bed13')
        assert page.locator(trace).is_visible(), 'Returning to the room removed the trace'
        assert page.locator(powder).is_visible(), 'Collecting the clue removed its physical powder trace'
        assert qa.state()['found'].count('C04') == 1, 'Room return duplicated discovery evidence'
        assert not page.locator('#inn-under-scene').count(), 'Collected discovery replayed on return'
        assert not page.locator(sleeping).count(), 'Room return restored an already rescued guest'
        print('PASS floor map, Doto diary purpose, actual C08, persistent trace', flush=True)

        # Long clicking while finishing dialogue cannot spill onto the under-bed
        # hotspot. A later deliberate interaction must still work.
        qa.engine('say([["det0","다시 주변을 살펴보자."]],function(){render()});'
                  'clearInterval(DL.timer);DL.timer=null;')
        box = page.locator(under).bounding_box()
        x, y = box['x']+box['width']/2, box['y']+box['height']/2
        page.mouse.click(x,y)
        assert not qa.state()['dl'], 'Final dialogue did not close'
        for _ in range(18):
            page.wait_for_timeout(170)
            page.mouse.click(x,y)
        assert not qa.state()['dl'] and not page.locator('#inn-under-scene').count(), (
            'Dialogue burst entered investigation', qa.state())
        assert qa.state()['found'].count('C04') == 1
        print('PASS dialogue burst blocked over collected discovery', flush=True)

        # Reload the actually collected save; no evidence fixtures are injected.
        qa.engine('saveProg();')
        page.reload(wait_until='domcontentloaded')
        page.wait_for_timeout(16000)
        page.locator('#innmain [data-m="cont"]').click()
        page.wait_for_timeout(1200)
        qa.drain()
        assert all(e in qa.state()['found'] for e in ('C01','C02','C04','C08')), qa.state()
        assert page.locator(trace).is_visible(), 'Reload lost the scene trace'
        assert page.locator(powder).is_visible(), 'Reload lost the physical powder trace'
        assert not page.locator('#inn-under-scene').count(), 'Reload replayed a completed discovery'
        assert not page.locator(sleeping).count(), 'Reload restored an already rescued guest'
        print('PASS actual save reload preserves discovery and scene trace', flush=True)
        print('Reloaded actual collection:', json.dumps(qa.state(), ensure_ascii=False), flush=True)

        # Compatibility fixtures are derived from the actually collected save.
        # They explicitly exercise older split observation/card storage, rather
        # than claiming to be additional fresh investigation runs.
        qa.engine('G.obsSeen=(G.obsSeen||[]).filter(x=>x!=="o_under");render();')
        qa.click(under)
        assert not page.locator('#inn-under-scene').count(), 'C04-only save replayed discovery'
        qa.drain()
        assert qa.state()['found'].count('C04') == 1
        assert not page.locator(sleeping).count(), 'C04-only save restored the hidden guest'
        qa.engine('G.found=G.found.filter(x=>x!=="C04");'
                  'if(!G.obsSeen.includes("o_under"))G.obsSeen.push("o_under");render();')
        qa.spoken = []
        qa.click(under)
        assert not page.locator('#inn-under-scene').count(), 'Legacy observation replayed the under-bed discovery'
        qa.drain()
        assert qa.state()['found'].count('C04') == 1 and 'o_under' in qa.state()['obs'], (
            'Legacy observation-only save failed to complete evidence', qa.state())
        assert any(speaker == 'buri' and '차갑고' in text for speaker,text in qa.spoken), (
            'Legacy observation-only save skipped the basket testimony', qa.spoken)
        assert not page.locator(sleeping).count(), 'Legacy discovery completion restored the hidden guest'
        print('PASS explicit C04-only and observation-only compatibility fixtures', flush=True)

        # A prepared state replacement models retry/load during pending dialogue.
        # Invoke the saved completion after the new G exists: it must not grant
        # the old discovery to either object or leave the cutscene visible.
        qa.engine('G=fresh(CASES.findIndex(c=>c.id==="inn"));'
                  'G.introDone=true;G.beats={inn_pro:1};G.loc=0;G.tab="scene";render();')
        page.wait_for_timeout(2000)
        qa.drain()
        qa.click(under)
        assert page.locator('#inn-under-scene').count(), 'Cancellation fixture did not start'
        result = qa.engine('(()=>{var old=G,done=DL.done;DL.done=null;endDlg();'
                           'G=fresh(old.ci);G.introDone=true;G.beats={inn_pro:1};'
                           'G.loc=0;G.tab="scene";render();if(done)done();'
                           'return {oldFound:old.found.slice(),newFound:G.found.slice()}})()')
        page.wait_for_timeout(1000)
        assert 'C04' not in result['oldFound'] and 'C04' not in result['newFound'], result
        assert not page.locator('#inn-under-scene').count(), 'State replacement left a stale cutscene'
        assert not page.evaluate('Boolean(window.__innDiscoveryTransferred)'), 'Transient basket survived cancel'
        assert page.locator(sleeping).count() == 1, 'Cancel removed the new game sleeping guest'
        print('PASS stale completion rejected after game-state replacement', flush=True)
        assert not qa.errors, qa.errors
        print('PASS all scene guidance checks; JavaScript errors: 0', flush=True)
        browser.close()


if __name__ == '__main__':
    main()
