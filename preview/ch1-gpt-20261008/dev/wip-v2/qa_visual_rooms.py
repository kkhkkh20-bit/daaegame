"""Read-only visual inventory using prepared native prologue/room states.

No evidence is granted. This renders existing assets/controllers and captures
screens for human review; it does not claim fresh-game progression coverage.
"""
import argparse,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from qa_scene_guidance import Investigation


def final_room_check(page, engine, room):
    """Exercise opaque body points and native panning, never force selectors."""
    qa=Investigation(page)
    expected=engine('Array.from(document.querySelectorAll("#bigscene .npc[data-npc]"))'
                    '.filter(e=>!e.dataset.nohit).map(e=>e.dataset.npc)')
    if not expected:return {'npcs':[], 'reachable':[]}
    summary=page.locator('.stagebar .scap').inner_text()
    assert not any(t in summary for t in ('모두 조사했어요','증거 수집 완료')), ('Unasked NPC room incorrectly marked complete',room,summary)
    if room=='kitchen':
        sources=page.locator('#bigscene image.wn9').evaluate_all('es=>es.map(e=>e.getAttribute("href"))')
        assert all('/npc.png' not in s for s in sources), ('Kitchen still uses old reading/chair poses',sources)
    def points():
        return page.evaluate('''()=>{const result=[];
          for(const im of document.querySelectorAll('#bigscene image.wn9')){
            const r=im.getBoundingClientRect(),k=im.dataset.k;
            const cx=r.x+r.width/2,cy=r.y+r.height/2;
            if(cx<=0||cx>=innerWidth||cy<=60||cy>=innerHeight-12)continue;
            for(const fy of [.5,.35,.65,.2,.8])for(const fx of [.5,.35,.65,.2,.8]){
              const x=r.x+r.width*fx,y=r.y+r.height*fy;
              if(x>0&&x<innerWidth&&y>60&&y<innerHeight-12&&__innNpcHit(x,y)===k){
                result.push({k,x,y,center:{x:cx,y:cy}});break}
            }
          }return result}''')
    initial=points()
    assert initial, ('No initial NPC body center and opaque hit point inside viewport',room)
    if room=='dining':
        assert any(p['k']=='seryeon' for p in initial), ('First dining frame misses Seryeon body',initial)
        if not any(p['k']=='innma' for p in initial):
            labels=page.locator('#fsal,#fsar').evaluate_all('es=>es.map(e=>e.getAttribute("aria-label")||"")')
            assert any('할머니' in label for label in labels), ('Offscreen grandmother has no directional label',labels)
    if room=='kitchen':
        assert any(p['k']=='nabi' for p in initial), ('First kitchen frame misses Nabi body',initial)
    reached=set();pan_steps={}
    def talk_visible():
        for _ in range(len(expected)):
            remaining=[p for p in points() if p['k'] not in reached]
            if not remaining:return
            point=remaining[0];k=point['k'];page.wait_for_timeout(800)
            assert page.evaluate('(p)=>__innNpcHit(p.x,p.y)',point)==k, ('Body hit changed before input',room,point)
            page.mouse.click(point['x'],point['y']);page.wait_for_timeout(900)
            selected=engine('({who:G.who,sceneTalk:G.sceneTalk,dl:!!DL})')
            assert selected['who']==k or selected['sceneTalk']==k, ('Opaque NPC body click failed',room,k,selected)
            qa.drain()
            back=page.locator('#w209back:visible')
            assert back.count(), ('NPC dialogue has no native return control',room,k)
            back.click();page.wait_for_timeout(900);reached.add(k)
    talk_visible()
    # Native arrows move by fractions of a viewport. Inspect each camera step
    # until the endpoint disables the arrow, with a bound on accidental loops.
    for direction in ('#fsar','#fsal'):
        steps=0
        for _ in range(12):
            arrow=page.locator(direction+':visible')
            if not arrow.count() or not arrow.is_enabled():break
            arrow.click();page.wait_for_timeout(700);steps+=1;talk_visible()
        else:
            arrow=page.locator(direction+':visible')
            assert not arrow.count() or not arrow.is_enabled(), ('Native pan never reaches endpoint',room,direction)
        pan_steps[direction]=steps
    assert set(expected)<=reached, ('Native panning cannot reach all room NPCs',room,expected,sorted(reached))
    return {'npcs':expected,'initialBodyPoints':initial,'reachable':sorted(reached),'panSteps':pan_steps}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url',default='http://127.0.0.1:8000/playT.html')
    parser.add_argument('--layout',choices=['landscape','portrait'],default='landscape')
    parser.add_argument('--check-final',action='store_true',help='Require initial NPC framing, opaque pointer access, native panning and pending dialogue guidance')
    parser.add_argument('--rooms',help='Focused comma-separated room IDs; skips prologue capture')
    parser.add_argument('--keep-going',action='store_true',help='Capture later rooms after a failed check, then fail with all findings')
    args=parser.parse_args();out=Path('/tmp/visual-rooms-'+args.layout);out.mkdir(exist_ok=True)
    v={'width':844,'height':390} if args.layout=='landscape' else {'width':390,'height':844}
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=b.new_page(viewport=v);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(args.url,wait_until='domcontentloaded');page.wait_for_timeout(16000)
        def e(s):return page.evaluate('(s)=>__T(s)',s)
        e('S.prog.inn=fresh(CASES.findIndex(c=>c.id==="inn"));S.prog.inn.introDone=true;S.prog.inn.beats={inn_pro:1,inn_i9:1};')
        page.evaluate('document.querySelector("#innmain").remove();__w209boot()');page.wait_for_timeout(1500)
        pro=page.evaluate('EP1INN.PRO.map((s,i)=>({i,sid:s.sid,title:s.title,bg:s.bg,who:s.who}))')
        data=[];failures=[]
        def snapshot(kind,key):
            page.screenshot(path=str(out/(kind+'-'+key+'.png')))
            d=page.evaluate('''()=>({actors:Array.from(document.querySelectorAll('#innstage .isf,.wn9,.tfig,.spk9')).map(e=>({k:e.dataset.k||e.dataset.npc||e.getAttribute('data-character'),cls:e.className,rect:e.getBoundingClientRect().toJSON(),images:[...(e.matches('img,image')?[e]:[]),...e.querySelectorAll('img,image')].map(i=>i.getAttribute('src')||i.getAttribute('href'))})),bg:Array.from(document.querySelectorAll('#bigscene svg[data-bg],#bigscene svg[data-inn-world]')).map(e=>({key:e.dataset.bg||e.dataset.innWorld,rect:e.getBoundingClientRect().toJSON()})),spots:Array.from(document.querySelectorAll('#bigscene [data-spot],#bigscene [data-obs]')).map(e=>({id:e.dataset.spot||e.dataset.obs,rect:e.getBoundingClientRect().toJSON(),visible:getComputedStyle(e).visibility,display:getComputedStyle(e).display})),text:document.querySelector('#vnbox')?.innerText||''})''')
            d['cameraDebug']=page.evaluate('''()=>{const fx=document.querySelector('#fsscroll'),sc=document.querySelector('#bigscene'),sv=sc?.querySelector('svg[data-inn-world],svg[data-bg]');return {scroll:fx?{left:fx.scrollLeft,width:fx.clientWidth,total:fx.scrollWidth}:null,scene:sc?.getBoundingClientRect().toJSON(),viewBox:sv?.getAttribute('viewBox'),buttons:Array.from(document.querySelectorAll('#bigscene .npc')).map(e=>({k:e.dataset.npc,rect:e.getBoundingClientRect().toJSON()}))}}''')
            d.update(kind=kind,key=key);data.append(d);print(kind,key,flush=True)
        for s in ([] if args.rooms else pro):
            e('if(DL){DL.done=null;endDlg()};G=fresh(CASES.findIndex(c=>c.id==="inn"));G.introDone=true;G.beats={inn_pi:'+str(s['i'])+'};__innStart()')
            page.wait_for_timeout(2100)
            # Advance only to the first actual native line if leading stage cues
            # have not yet completed; no controller or asset is replaced.
            for _ in range(12):
                if e('!!DL'):break
                page.wait_for_timeout(200)
            snapshot('pro',s['sid'] or str(s['i']))
        rooms=e('CASES.find(c=>c.id==="inn").locations.map((l,i)=>({i,id:l.id}))')
        for r in rooms:
            if args.rooms and r['id'] not in args.rooms.split(','):continue
            e('if(DL){DL.done=null;endDlg()};G=fresh(CASES.findIndex(c=>c.id==="inn"));G.introDone=true;G.beats={inn_pro:1,inn_i9:1};G.loc='+str(r['i'])+';G.tab="scene";render()')
            page.wait_for_timeout(1200);snapshot('room',r['id'])
            if args.check_final:
                try:
                    data[-1]['finalChecks']=final_room_check(page,e,r['id'])
                    print('PASS final room',r['id'],data[-1]['finalChecks'],flush=True)
                except AssertionError as failure:
                    if not args.keep_going:raise
                    detail={'room':r['id'],'failure':str(failure),'actors':data[-1]['actors']}
                    failures.append(detail);print('FAIL final room',json.dumps(detail),flush=True)
        (out/'inventory.json').write_text(json.dumps({'pro':pro,'screens':data,'errors':errors},ensure_ascii=False,indent=2))
        assert not errors,errors
        assert not failures,failures
        print('PASS visual capture JS0',str(out),flush=True);b.close()
if __name__=='__main__':main()
