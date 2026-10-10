"""Browser audio cue checks and offline signal sanity; not a listening test."""
import shutil
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 844, 'height': 390})
    errors = []; bad=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('response',lambda r:bad.append(r.url) if r.status>=400 and 'favicon' not in r.url else None)
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
    # Isolate injected cue timing from live engine metadata; qa_flow checks integration.
    page.evaluate('window.__qaLine=window.__innAudioLine;window.__innAudioLine=function(){}')
    page.evaluate('window.__qaLine({w:"doto",t:"첫눈은 자정. 종 열두 번을 기록했어요."})')
    assert page.evaluate('window.__innKeyLine()')
    assert page.evaluate('window.__innDuck()') == 0
    page.mouse.click(2,2)
    run('S.sound=true;ac();MASTER.gain.value=MGAIN;AC.resume()')
    assert run('AC.state') == 'running'
    page.evaluate('window.__qaLine({w:"narr",t:"바구니를 지켜본다.",audio:"pulse"})')
    page.wait_for_timeout(200)
    assert page.evaluate('window.__innTense()')
    assert page.evaluate('window.__innAudioState().heartbeat') == 0
    assert page.evaluate('window.__innWant()') is None
    page.wait_for_timeout(1400)
    assert page.evaluate('window.__innAudioState().heartbeat') >= 1, (page.evaluate('window.__innAudioState()'),run('({sound:S.sound,ac:AC&&AC.state,screen:S.screen})'),errors)
    page.evaluate('window.__qaLine({w:"det0",t:"다시 여쭙겠습니다.",audio:"press"})')
    page.wait_for_timeout(100)
    assert not page.evaluate('window.__innTense()')
    assert page.evaluate('window.__innWant()') == 'inn_climax_press'
    page.evaluate('window.__qaLine({w:"seryeon",t:"그건..."})')
    assert page.evaluate('window.__innWant()') == 'inn_climax_press'
    page.evaluate('window.__qaLine({w:"det0",t:"처음부터 백 냥입니다.",audio:"impact"})')
    assert page.evaluate('window.__innWant()') is None
    page.wait_for_timeout(900)
    assert page.evaluate('window.__innWant()') == 'inn_climax_press'
    page.evaluate('window.__qaLine({w:"det0",t:"왜 숨기셨습니까?",audio:"silence"})')
    assert page.evaluate('window.__innWant()') is None
    page.evaluate('window.__audioOriginalPhase=window.__rtPh;window.__rtPh=()=>EP1INN.FINAL.phases.at(-1);window.__qaLine({w:"seryeon",t:"…네."});window.__innWant()')
    assert page.evaluate('window.__innAudioState().confession')
    assert page.evaluate('window.__innWant()') is None
    page.wait_for_timeout(2700)
    assert page.evaluate('window.__innWant()') == 'inn_t_innma'
    page.evaluate('window.__innAudioFailure(true)')
    assert page.evaluate('window.__innWant()') is None
    page.evaluate('window.__rtPh=window.__audioOriginalPhase;window.__innAudioFailure(false);window.__innAudioReset()')
    assert not page.evaluate('window.__innAudioState().confession')
    stats = page.evaluate('''async()=>{
      const result={};
      for(const key of Object.keys(window.__INN_MUSIC)){
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
    cache=page.evaluate('__AUD.mediaCacheInfo()')
    assert len(cache['urls'])<=3 and cache['bytes']<115_000_000,cache
    assert page.evaluate('__AUD.SONGS.inn_meet_press.bpm>__AUD.SONGS.inn_meet.bpm && __AUD.SONGS.inn_climax_press.bpm>__AUD.SONGS.inn_climax.bpm')
    # Render across a whole loop in Web Audio, accelerated offline.
    loop=page.evaluate('''async()=>{const seconds=__AUD.SONGS.inn_title.loopSeconds,b=await __AUD.render('inn_title',seconds+3),x=b.getChannelData(0),offset=Math.round(seconds*b.sampleRate);let diff=0,power=0;for(let i=Math.round(.2*b.sampleRate);i<Math.round(1.2*b.sampleRate);i++){diff+=(x[i]-x[i+offset])**2;power+=x[i]**2}return {relativeError:Math.sqrt(diff/power),seconds}}''')
    assert loop['relativeError']<.02,loop
    assert not errors, errors
    assert not bad,bad
    print('String score: decoded cues, pressure tempo, bounded media cache and full title loop OK',cache,loop)
    print('Audio cues OK; offline 8-second samples (default mix, no live duck multiplier):', stats)
    browser.close()
