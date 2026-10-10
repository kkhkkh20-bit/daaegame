"""Prepared-state late-discovery regression, not a fresh-game walkthrough.

The prerequisite truth table deliberately prepares found/asked arrays. Actual
pointer input must still enforce the boundary; card/observation are granted
only by finishing the authored scene. Existing actual investigation QA remains
separate. No production sources or original test expectations are changed.
"""
import argparse, shutil
from playwright.sync_api import sync_playwright
from qa_scene_guidance import Investigation

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
p.add_argument('--only-legacy-hold',action='store_true',help='Only the added prepared old-save health admission/money pause regression')
p.add_argument('--only-save',action='store_true',help='Only save migration and clinical abstention preservation')
a=p.parse_args()
UNDER='#bigscene [data-obs="o_under"]'
READY_FOUND=['C01','C02','C09'];READY_ASKED=['C03','C12']
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':844,'height':390});qa=Investigation(page)
    page.goto(a.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
    page.wait_for_function('typeof __innDiscoveryReady==="function"')
    qa.engine('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1};')
    page.evaluate('()=>{document.querySelector("#innmain").remove();window.__w209boot()}')
    page.wait_for_timeout(1200)
    def setup(found=(),asked=(),obs=()):
        import json
        qa.engine('if(DL){DL.done=null;endDlg()};closeModal();G=fresh(CASES.findIndex(c=>c.id==="inn"));G.introDone=true;G.beats={inn_pro:1,inn_i9:1,toMeet:1};G.loc=0;G.tab="scene";'
                  'G.found='+json.dumps(list(found))+';G.asked='+json.dumps(list(asked))+';G.obsSeen='+json.dumps(list(obs))+';render();')
        page.wait_for_timeout(1100);qa.drain();qa.spoken=[]
    def ready():return page.evaluate('window.__innDiscoveryReady()')
    def legacy_hold():
        setup(['C04'])
        assert qa.engine('window.__rtReady(CASES[G.ci])'),'C04-only old save cannot enter the health examination'
        qa.engine('G.beats.inn_meeting_version=2;window.__rtOpen(CASES[G.ci])')
        page.wait_for_timeout(2300)
        assert qa.engine('!!G.debate&&G.debate.pi===0&&window.__inMeeting'), 'C04-only old save did not open first clinical phase'
        qa.engine('if(DL){DL.done=null;endDlg()};window.__rtgReset();document.querySelectorAll("body>.rt").forEach(e=>e.remove());window.__inMeeting=false')
        setup(['C04'])
        qa.engine('G.beats.inn_life_confirmed=1;G.beats.inn_meeting_version=2;G.debate={pi:2,sus:{},hold:null};window.__rtOpen(CASES[G.ci])')
        page.wait_for_timeout(2600)
        state=qa.engine('({pi:G.debate&&G.debate.pi,hold:G.debate&&G.debate.hold,found:G.found,meeting:window.__inMeeting})')
        assert state['pi']==2 and state['hold']['need']==['C01','C02','C03'] and not state['meeting'],state
        assert state['found']==['C04'],'Money pause changed old-save clues'
        assert not page.locator('body>.rt').count(),'Money pause left council input on screen'
        print('PASS C04-only legacy save enters clinical phase; missing money evidence pauses at pi2 without clue loss',flush=True)
    if a.only_legacy_hold:
        legacy_hold()
        assert not qa.errors,qa.errors
        browser.close()
        raise SystemExit(0)
    migration=qa.engine("""(()=>{
      const make=(flags={},version=null)=>{let g=fresh(CASES.findIndex(c=>c.id==='inn'));
        g.introDone=true;g.beats={inn_pro:1,toMeet:1,inn_i9:1,rtTally:{karo:2},rtVotes:{karo:"innma",nabi:"innma"},...flags};
        if(version!==null)g.beats.inn_meeting_version=version;
        g.found=['C01','C02','C09'];g.asked=['C03','C12'];g.obsSeen=['o_inn_head'];
        g.debate={pi:version===2?1:3,sus:{karo:4},done:!!flags.done,hold:null};return g};
      const clean=g=>sanitizeState({...S,prog:{inn:g}}).prog.inn;
      return {old:clean(make()),current:clean(make({},2)),clinical:clean(make({rtTally:{"기권":6},rtVotes:{karo:"기권",nabi:"기권"}},2)),
        mixed:clean(make({rtTally:{innma:3,"부녀":2,"기권":1,"기권(나비)":1,bogus:1}},2)),done:clean(make({done:1})),
        meeting:clean(make({inn_meet:1})),final:clean(make({inn_final:1})),end:clean(make({inn_end:1}))};
    })()""")
    old=migration['old']
    assert old.get('debate') is None and not old['beats'].get('rtTally') and not old['beats'].get('rtVotes'),('Old numeric phase survived migration',old)
    assert old['found']==READY_FOUND and old['asked']==READY_ASKED and old['obsSeen']==['o_inn_head'],('Migration discarded clues/testimony',old)
    assert old['beats']['inn_meeting_version']==2
    for name in ('done','meeting','final','end'):
        state=migration[name]
        assert state['debate']['pi']==3 and state['debate']['sus']['karo']==4,('Completed state reset',name,state)
        assert state['beats']['inn_life_confirmed'] and state['beats']['inn_meeting_version']==2
    assert migration['current']['debate']['pi']==1 and migration['current']['debate']['sus']['karo']==4
    assert migration['clinical']['beats']['rtTally']=={'기권':6},migration['clinical']
    assert migration['clinical']['beats']['rtVotes']=={'karo':'기권','nabi':'기권'},migration['clinical']
    assert migration['mixed']['beats']['rtTally']=={'innma':3,'부녀':2,'기권':1,'기권(나비)':1},migration['mixed']
    print('PASS sanitize old phase reset/clues preserved; schema2 and completed meeting/final/end preserved',flush=True)
    print('PASS clinical abstentions and authored vote destinations survive save sanitization; unknown destination removed',flush=True)
    if a.only_save:
        assert not qa.errors,qa.errors
        browser.close()
        raise SystemExit(0)
    setup(['C04'],['C03'])
    assert not qa.engine('window.__innSun()'),'Clinical-before state opened the headboard puzzle'
    pre=qa.engine('(()=>{const x=EP1INN.SHOW.innma.C04;return {beat:x.beat||null,text:JSON.stringify(x)}})()')
    assert not pre['beat'] and '겨울잠이면' not in pre['text'],('Grandma record skipped clinical examination',pre)
    qa.engine('G.beats.inn_life_confirmed=1')
    assert qa.engine('window.__innSun()'),'Asked C03 plus confirmed life did not open later sunlight'
    assert qa.engine('EP1INN.SHOW.innma.C04.beat')=='inn_show_innma_C04','Postclinical grandma response was not restored'
    print('PASS clinical boundary: no premature sunlight/winter explanation; original grandma SHOW restored afterward',flush=True)

    setup();assert not ready(),'Empty investigation unlocked discovery'
    setup(READY_FOUND,READY_ASKED);assert ready(),'Real inventory split (found objects/asked witnesses) did not unlock discovery'
    for missing in READY_FOUND+READY_ASKED:
        setup([x for x in READY_FOUND if x!=missing],[x for x in READY_ASKED if x!=missing])
        assert not ready(),('Missing prerequisite unlocked discovery',missing)
    setup(['C04']);assert ready(),'Legacy C04 was blocked by new prerequisites'
    setup(obs=['o_under']);assert ready(),'Legacy observation was blocked by new prerequisites'
    setup(['C11']);assert not qa.engine('window.__innAvail("C05")'),'Legacy C11-only state exposed undiscovered guest fur'
    print('PASS helper prerequisite truth table, legacy bypasses and no C05 before C04',flush=True)

    setup(['C01','C02'])
    qa.click(UNDER);qa.drain()
    state=qa.state()
    assert 'C04' not in state['found'] and 'o_under' not in state['obs'],('Early curiosity granted discovery',state)
    assert not page.locator('#inn-under-scene').count(),'Early curiosity opened the full rescue scene'
    assert qa.spoken,'Early curiosity offered no short response'
    assert not any('바구니' in t or '겨울잠쥐' in t or '작은 애가' in t for _,t in qa.spoken),('Early response revealed the guest',qa.spoken)
    print('PASS C01/C02 → actual early under-bed click is a short response, no observation/card/rescue',flush=True)

    setup(READY_FOUND,READY_ASKED)
    qa.click(UNDER)
    assert page.locator('#inn-under-scene').count(),'Complete money-case investigation did not begin discovery'
    assert 'C04' not in qa.state()['found'],'C04 granted before rescue finished'
    qa.drain()
    assert qa.state()['found'].count('C04')==1 and 'o_under' in qa.state()['obs'],qa.state()
    assert 'held' in qa.captured,'Late discovery skipped the loaded rescue illustration'
    assert any(w=='buri' and '차갑' in t for w,t in qa.spoken),'Discovery skipped Buri physical examination'
    print('PASS late actual rescue → illustration/examination → one C04 and observation',flush=True)

    setup(['C04']);qa.click(UNDER)
    assert not page.locator('#inn-under-scene').count(),'Legacy C04 replayed rescue'
    qa.drain();assert qa.state()['found'].count('C04')==1
    setup(obs=['o_under']);qa.click(UNDER)
    assert not page.locator('#inn-under-scene').count(),'Observation-only save replayed rescue'
    qa.drain();assert qa.state()['found'].count('C04')==1
    print('PASS actual legacy reinspection/observation-only completion without new prerequisites',flush=True)

    setup(READY_FOUND,READY_ASKED);qa.click(UNDER)
    assert page.locator('#inn-under-scene').count()
    result=qa.engine('(()=>{let old=G,done=DL&&DL.done;if(DL){DL.done=null;endDlg()};G=fresh(old.ci);G.introDone=true;G.beats={inn_pro:1,toMeet:1};G.loc=0;G.tab="scene";render();if(done)done();return {old:old.found.slice(),now:G.found.slice()}})()')
    page.wait_for_timeout(1200)
    assert 'C04' not in result['old'] and 'C04' not in result['now'],result
    assert not page.locator('#inn-under-scene').count(),'State replacement left a rescue scene'
    assert not page.evaluate('Boolean(window.__innDiscoveryTransferred)'),'State replacement left a transient transferred body'
    # Native open must migrate in-memory numeric indices before stt(), and
    # delayed native banner completion may not mutate a replacement game.
    setup(READY_FOUND+['C04'],READY_ASKED)
    native=qa.engine("""(()=>{G.debate={pi:3,sus:{karo:4}};G.beats.rtVotes={karo:"innma"};delete G.beats.inn_meeting_version;
      window.__rtOpen(CASES[G.ci]);return {debate:G.debate,version:G.beats.inn_meeting_version,votes:G.beats.rtVotes||null}})()""")
    assert native['debate'] is None and native['version']==2 and not native['votes'],native
    qa.drain();page.wait_for_timeout(1500)
    qa.engine('if(DL){DL.done=null;endDlg()};window.__innCutting=false;document.querySelectorAll("body>.rt").forEach(e=>e.remove());window.__inMeeting=false;window.__rtgReset();')
    setup(READY_FOUND+['C04'],READY_ASKED)
    qa.engine('G.beats.inn_meeting_version=2;G.beats.inn_i9=1;G.debate={pi:1,sus:{karo:4}};window.__rtOpen(CASES[G.ci]);'
              'G=fresh(G.ci);G.introDone=true;G.beats={inn_pro:1,toMeet:1};G.loc=0;G.tab="scene";'
              'window.__rtgReset();document.querySelectorAll("body>.rt").forEach(e=>e.remove());window.__inMeeting=false;render();')
    page.wait_for_timeout(2600)
    assert qa.engine('!G.debate&&!DL'),'Old native banner callback changed the replacement game'
    print('PASS native open migration and stale banner completion rejected',flush=True)
    setup(READY_FOUND+['C04'],READY_ASKED)
    qa.engine('window.__pacingMF=0;window.__pacingPlay=window.__innPlay;window.__innPlay=function(items,done){if(items===EP1INN.MF)window.__pacingMF++;return window.__pacingPlay.apply(this,arguments)};window.__innFail("meet");')
    page.wait_for_timeout(800)
    assert page.evaluate('window.__pacingMF')==0,'Preclinical failure played the false death/grandma departure scene'
    assert qa.state()['found']==READY_FOUND+['C04'] and qa.state()['asked']==READY_ASKED,'Clinical restart discarded collected records'
    assert not qa.engine('!!G.beats.inn_life_confirmed'),'Clinical failure counted as survival confirmation'
    qa.engine('window.__innPlay=window.__pacingPlay')
    print('PASS preclinical failure retries without MF death/departure or evidence loss',flush=True)
    legacy_hold()
    assert not qa.errors,qa.errors
    print('PASS late discovery stale completion is rejected after G replacement; JS errors0',flush=True)
    browser.close()
