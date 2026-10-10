"""Menu geometry and sampled music integration, in both screen orientations."""
from playwright.sync_api import sync_playwright
import shutil

with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    for vp in [{'width':844,'height':390},{'width':390,'height':844}]:
        page=b.new_page(viewport=vp);errors=[];bad=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
        page.on('request',lambda r:requests.append(r.url) if '/audio/v2/' in r.url else None)
        page.goto('http://127.0.0.1:8000/playT.html');page.wait_for_timeout(16000)
        assert page.locator('#innmain .chapter-tag').inner_text()=='1장 · 열세 번째 침대'
        for button in page.locator('#innmain .menu button').all():
            r=button.bounding_box()
            assert r['x']>=0 and r['y']>=0 and r['x']+r['width']<=vp['width'] and r['y']+r['height']<=vp['height'],r
            assert r['height']>=44,r
        if page.locator('#sndhint9').count():page.locator('#sndhint9').click()
        else:page.mouse.click(vp['width']-40,150)
        page.wait_for_function('__AUD.cur==="inn_title" && __AUD.mediaState["audio/v2/title-v1.mp3"]==="ready"')
        assert page.evaluate('window.__T("AC.state")')=='running'
        page.screenshot(path=f'/tmp/polish-main-{vp["width"]}.png')
        # Muting must stop the existing music path; unmuting reuses the buffer.
        page.evaluate('window.__T("setSound(false)")');page.wait_for_timeout(1000)
        assert page.evaluate('__AUD.cur') is None
        page.evaluate('window.__T("setSound(true)")');page.wait_for_timeout(1000)
        assert page.evaluate('__AUD.cur')=='inn_title'
        assert sum('title-v1.mp3' in u for u in requests)==1,requests
        page.locator('#innmain [data-m="set"]').click()
        music=page.locator('#innopt [data-s="musicVolume"]')
        previous=int(music.input_value());music.focus();page.keyboard.press('ArrowLeft');page.wait_for_timeout(500)
        assert int(music.input_value())==max(0,previous-5)
        assert page.evaluate('__AUD.cur')=='inn_title','Volume adjustment restarted or stopped menu music'
        page.screenshot(path=f'/tmp/polish-options-{vp["width"]}.png')
        page.locator('#innopt .sv').click()
        assert not page.locator('#innopt').count()
        # The new score renderer must produce real, finite, unclipped signals.
        stats=page.evaluate('''async()=>{const out={};for(const key of ['inn_title','inn_travel','inn_inv']){const b=await __AUD.render(key,8);let peak=0,sum=0;for(const x of b.getChannelData(0)){if(!Number.isFinite(x))throw Error(key);peak=Math.max(peak,Math.abs(x));sum+=x*x}out[key]={peak,rms:Math.sqrt(sum/b.length)}}return out}''')
        assert all(0<s['peak']<1 and s['rms']>.001 for s in stats.values()),stats
        page.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1};');document.querySelector('#innmain').remove();window.__w209boot();window.__T('G.found=["C01","C02","C04"];G.asked=["C03"];render()')''')
        page.wait_for_timeout(3000)
        # Acquired clues can trigger the existing room-arrival sunbeam dialogue.
        # Finish it with normal input before testing the investigation toolbar.
        quiet=0
        for _ in range(200):
            if page.locator('#tostay2').count():
                page.locator('#tostay2').click();quiet=0
            elif page.evaluate('window.__T("!!DL")'):
                page.keyboard.press('Enter');quiet=0
            else:quiet+=1
            page.wait_for_timeout(180)
            if quiet>=8:break
        page.screenshot(path=f'/tmp/polish-scene-{vp["width"]}.png')
        page.locator('#w209rail .g>[data-w="ev"]').click();page.wait_for_timeout(500)
        assert page.locator('.crec2').is_visible()
        tabs=page.locator('.crec2 .crtab2 button').evaluate_all('(els)=>els.map(e=>({text:e.innerText,image:getComputedStyle(e).backgroundImage,borderImage:getComputedStyle(e).borderImageSource,color:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor}))')
        assert all(t['text'].strip() and t['image']=='none' and t['borderImage']=='none' and t['color']!=t['bg'] for t in tabs),tabs
        page.screenshot(path=f'/tmp/polish-evidence-{vp["width"]}.png')
        close=page.locator('.crec2 .cr-x')
        if close.is_visible():close.click()
        else:page.locator('#w209back').click()
        assert not page.locator('.crec2').count(),'Evidence panel did not close'
        assert not errors,errors
        assert not bad,bad
        print(vp,'OK: menu geometry, music unlock/mute/cache, three sampled scores, evidence UI; errors 0',stats,flush=True)
        page.close()
    b.close()
