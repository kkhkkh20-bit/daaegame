"""Information boundaries and ledger consent, using the generated browser engine."""
import shutil
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':844,'height':390});errors=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.goto('http://127.0.0.1:8000/playT.html',wait_until='domcontentloaded');pg.wait_for_timeout(16000)
    # Check every spoken branch, including soft/press/wrong paths before the slip.
    result=pg.evaluate('''()=>{
      const phases=EP1INN.MEET.phases,end=phases.findIndex(p=>p.stms&&p.stms.some(l=>/침대 밑/.test(l.t)));if(end<0)throw Error('Private-location slip phase missing');
      function spoken(o,out=[]){if(!o||typeof o!=='object')return out;if(o.w&&o.t)out.push(o);Object.values(o).forEach(v=>{if(v&&typeof v==='object')spoken(v,out)});return out}
      const leaked=spoken(phases.slice(0,end)).filter(l=>/침대 밑|상자 뒤/.test(l.t)).map(l=>[l.w,l.t]);
      const opening=phases[end].stms.find(l=>/침대 밑/.test(l.t));
      return {leaked,speaker:opening&&opening.w};
    }''')
    assert result=={'leaked':[],'speaker':'seryeon'},result
    pg.evaluate('''window.__T('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};');document.querySelector('#innmain').remove();window.__w209boot()''');pg.wait_for_timeout(1000)
    pg.evaluate('''window.__T('if(DL){DL.done=null;endDlg()};G.found=["C04","C03"];G.beats.inn_life_confirmed=1;G.loc=0;G.tab="scene";render()')''')
    pg.wait_for_timeout(900)
    # Entering the room can trigger its sunbeam observation. Finish that dialogue first.
    for _ in range(80):
        if not pg.evaluate('window.__T("!!DL")'):break
        pg.keyboard.press('Enter');pg.wait_for_timeout(250)
    assert not pg.evaluate('window.__T("!!DL")')
    pg.wait_for_timeout(900)
    # Start at the lock itself: reading the headboard first is not assumed.
    pg.locator('[data-obs="o_inn_lock"]').click(force=True)
    assert not pg.locator('#innpad').count(), 'Lock opened before consent dialogue'
    permission=False
    for i in range(120):
        line=pg.evaluate('window.__innAudioState().line')
        if '첫째 권만 봐요' in line:permission=True
        if pg.locator('#innpad').count():break
        pg.evaluate('window.__T("if(DL)advance()")');pg.wait_for_timeout(180)
    assert permission and pg.locator('#innpad').count(),(permission,pg.locator('body').inner_text()[-1200:])
    assert pg.evaluate('window.__T("!!G.beats.inn_ledger_permission")')
    assert not errors,errors
    print('Story checks OK: private location retained until Seryeon slip; ledger consent before keypad')
    b.close()
