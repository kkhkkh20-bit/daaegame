"""Focused discovery scene playback; does not seed a whole-game walkthrough."""
import shutil
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':844,'height':390});errors=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');pg.wait_for_timeout(16000)
    pg.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''');pg.wait_for_timeout(1000)
    for width,height in [(844,390),(390,844)]:
        pg.set_viewport_size({'width':width,'height':height})
        pg.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};window.__innAudioReset();G.tab="scene"');window.__sceneDone=false;
          const scene=EP1INN.LOCS.flatMap(l=>l.obs||[]).find(o=>o.id==='o_under');
          window.__innPlay(scene.say,()=>window.__sceneDone=true)''')
        peek=False;body=False
        for i in range(600):
            pg.wait_for_timeout(100)
            state=pg.evaluate('({line:__innAudioState().line,tense:__innTense(),want:__innWant(),done:__sceneDone})')
            if state['line'].startswith('…상자 뒤에 뭐가 있어'):
                assert state['tense'] and state['want'] is None,state
                peek=True
            if '작은 몸이 웅크리고 있다' in state['line']:
                assert state['tense'] and state['want'] is None,state
                body=True
            if state['done']:break
            pg.evaluate('window.__T("if(DL)advance()")')
        assert state['done'] and peek and body,(width,state,peek,body)
        pg.wait_for_timeout(2800)
        assert not pg.evaluate('window.__innTense()')
        assert pg.evaluate('window.__innWant()') == 'inn_inv'
        print('Discovery anticipation → reveal → tension release OK',width,height,flush=True)
    assert not errors,errors
    b.close()
