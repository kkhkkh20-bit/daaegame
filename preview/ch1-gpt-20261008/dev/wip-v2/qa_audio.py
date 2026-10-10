"""Browser audio cue checks and offline signal sanity; not a listening test."""
import shutil
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 844, 'height': 390})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('http://127.0.0.1:8000/playT.html', wait_until='domcontentloaded')
    page.wait_for_timeout(16000)
    page.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''')
    page.wait_for_timeout(1000)
    def run(code):
        return page.evaluate('(code)=>window.__T(code)', code)
    run('if(DL){DL.done=null;endDlg()};G.beats.inn_pro=0;G.beats.inn_pi=window.EP1INN.PRO.findIndex(x=>x.sid==="P1");window.__innWant();S.sound=false;SFX.carStop()')
    assert page.evaluate('window.__innAudioState().carStopped')
    run('G.beats.inn_pi=window.EP1INN.PRO.findIndex(x=>x.sid==="P10");window.__innWant();SFX.bell10()')
    assert page.evaluate('window.__innAudioState().bell')
    assert page.evaluate('window.__innWant()') is None
    # Sound-off still advances semantic cues, and the next scene releases them.
    run('G.beats.inn_pi=window.EP1INN.PRO.findIndex(x=>x.sid==="P11");window.__innWant()')
    assert not page.evaluate('window.__innAudioState().bell')
    run('G.beats.inn_pro=1;G.beats.inn_meet=1;window.__innOpenFinal()')
    page.wait_for_timeout(300)
    page.evaluate('window.__innAudioLine({w:"doto",t:"첫눈은 자정이었어요. 종이 열두 번 쳤고요."})')
    assert page.evaluate('window.__innKeyLine()')
    assert page.evaluate('window.__innDuck()') == 0
    page.evaluate('window.__innAudioLine({w:"seryeon",t:"…네."});window.__innWant()')
    assert page.evaluate('window.__innAudioState().confession')
    assert page.evaluate('window.__innWant()') is None
    page.wait_for_timeout(2700)
    assert page.evaluate('window.__innWant()') == 'inn_t_innma'
    page.evaluate('window.__innAudioFailure(true)')
    assert page.evaluate('window.__innWant()') is None
    page.evaluate('window.__innAudioFailure(false);window.__innAudioReset()')
    assert not page.evaluate('window.__innAudioState().confession')
    stats = page.evaluate('''async()=>{
      const result={};
      for(const key of ['inn_travel','inn_serious','inn_inv','inn_meet','inn_climax','inn_t_innma','inn_after']){
        const b=await __AUD.render(key,8);let peak=0,sum=0,clipped=0;
        for(let c=0;c<b.numberOfChannels;c++)for(const x of b.getChannelData(c)){
          if(!Number.isFinite(x))throw Error(key+' non-finite audio');
          peak=Math.max(peak,Math.abs(x));sum+=x*x;if(Math.abs(x)>=1)clipped++;
        }
        result[key]={peak,rms:Math.sqrt(sum/(b.length*b.numberOfChannels)),clipped};
      }return result;
    }''')
    for key, st in stats.items():
        assert st['rms'] > 0, (key, st)
        assert st['clipped'] == 0, (key, st)
    assert not errors, errors
    print('Audio cues OK; offline 8-second samples (default mix, no live duck multiplier):', stats)
    browser.close()
