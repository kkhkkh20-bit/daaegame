"""자동 완주 검사: 웹 빌드를 브라우저(Playwright)로 열어 1일 마차부터 결말까지 플레이어처럼 눌러 간다.
선택·질문·조사·지도 이동·회의 제출(정답표 기준)을 하고, 관문·화면이 바뀔 때마다 캡처와 상태를 남긴다.
현장마다 인물 좌표를 「배치」 줄로 찍는다(dev/qa_layout_check.py 가 겹침·가장자리 잘림을 거른다).

길(ROUTE):  비움=기본(선택창마다 첫 선택지) · alt=다른 길(마지막 선택지부터)
            cheese=꼼수(회의마다 기회가 셋 이상이면 「전부 내기」와 「엉뚱한 하나」를 먼저 내고 결과를 판정)
이어 하기:  RESUME_DAY=N 이면 저장 auto-dayN 에서 시작(날짜가 바뀔 때마다 auto-dayN 으로 저장한다)
캡처 폴더:  ROOM13_QA_OUT (기본 dev/qa-out/autoplay)
실행 방법은 docs/QA_AUTOPLAY.md."""
import asyncio,os,sys,json,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;GAME=HERE.parent/'game'
sys.path.insert(0,str(HERE))
OUT=Path(os.environ.get('ROOM13_QA_OUT',str(HERE/'qa-out'/'autoplay')))
os.environ['ROOM13_QA_OUT']=str(OUT);OUT.mkdir(parents=True,exist_ok=True)
from qa_v111_play import Fast,PROOFS
import re,glob
# 4일 이후의 제시는 compiled-reference 에 없다. 이야기 파일의 r13_v111_proof('제목',[정답…]) 호출에서 바로 읽는다.
for f in glob.glob(str(GAME/'*.rpy'))+glob.glob(str(GAME/'systems'/'*.rpy')):
    for m in re.finditer(r"r13_v111_proof\(\s*(['\"])(.+?)\1\s*,\s*\[([^\]]*)\]",open(f,encoding='utf-8').read()):
        title=m.group(2);keys=re.findall(r"['\"]([A-Za-z0-9_]+)['\"]",m.group(3))
        PROOFS.setdefault(title,dict(title=title,correct=keys))
# 대체 정답(R13_PROOF_ALTERNATES): 보유 자료로 채울 수 있는 묶음을 고른다
import ast
_rules=open(GAME/'room13_v111_newworld_rules.rpy',encoding='utf-8').read()
_m=re.search(r"R13_PROOF_ALTERNATES=\{(.*?)\n    \}",_rules,re.S)
ALTERNATES={}
if _m:
    body='\n'.join(l for l in _m.group(1).splitlines() if not l.strip().startswith('#'))
    try:ALTERNATES=ast.literal_eval('{'+body+'}')
    except Exception as e:print('ALTERNATES parse failed',e)
def proof_sets(title):
    base=PROOFS[title]['correct'] if title in PROOFS else []
    return [list(base)]+[list(a) for a in ALTERNATES.get(title,())]
from playwright.async_api import async_playwright
URL=os.environ.get('ROOM13_QA_URL','http://localhost:8766/preview/room13-dev/')
class Driver(Fast):
    async def press(self,label):
        # 기록 책의 칩 이름이 「지난 사건」→「지난」으로 짧아졌다(0.20.74). 옛 도우미의 이름을 지금 칩으로 옮긴다.
        label={'지난 사건':'지난','이번 사건':'이번'}.get(label,label)
        return await super().press(label)
LOG=[]
def log(*a):
    s=' '.join(str(x) for x in a);print(s,flush=True);LOG.append(s)
SCREENS=("main_menu","say","choice","r13_confirm","r13_hub","r13_topics","r13_map","r13_book","r13_records","r13_crisis_proof","r13_proof_workspace","r13_more_tools","r13_side_questions","r13_fork_screen","_exception")
n_shot=[0]
async def shot(q,name):
    n_shot[0]+=1;await q.shot('%03d-%s'%(n_shot[0],name))

async def snap(q):
    return await q.py('import renpy;s=renpy.store;result=dict(screens=[n for n in %r if renpy.display.screen.get_screen(n)],gate=(s.room13 or {}).get("v111",{}).get("gate"),day=(s.room13 or {}).get("day"),period=(s.room13 or {}).get("period"),choice=getattr(s,"v111_menu_owner",None),claim=getattr(s,"v111_claim",None),binding=s.r13_v111_binding() if s.r13_v111_active() else {},values=(s.room13 or {}).get("v111",{}).get("values",{}),evidence=(s.room13 or {}).get("evidence",[]),location=(s.room13 or {}).get("location"),say=(lambda x:str(x.scope.get("what","")) if x else "")(renpy.display.screen.get_screen("say")),who=(lambda x:str(x.scope.get("who","")) if x else "")(renpy.display.screen.get_screen("say")),people=s.r13_visible_people() if s.r13_v111_active() else [])'%(SCREENS,))

async def proof(q,st):
    """통합 대조 화면: 아는 정답 자료에 표시하고 제출한다."""
    title=(st['claim'] or '')[5:];node=PROOFS.get(title)
    if not node:
        # 제목이 다른 꼴일 수 있다(「v111:」 뒤 키가 제목 자체). 부분 일치로 한 번 더 찾는다.
        node=next((v for k,v in PROOFS.items() if k in title or title in k),None)
    selected=await q.py('import renpy;result=list(renpy.store.room13["arguments"].get(renpy.store.v111_claim,[]))')
    if not node:
        log('  대조 정답 모름',title);await shot(q,'proof-unknown');return False
    async def find(bid):
        r=await q.py('import renpy\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if getattr(f.widget,"id",None)=="%s"),None)'%bid)
        if r:return r
        # 글자 버튼(쪽 넘김)은 id 가 초점 목록에 안 잡힐 수 있어 글자로 찾는다
        text={'r13_pw_next':'다음 →','r13_pw_prev':'← 이전'}.get(bid)
        if not text:return None
        st=await q.state();bs=[b for b in st['buttons'] if b['text'].strip()==text]
        return bs[0]['rect'] if bs else None
    tab_all=await q.py('import renpy\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if getattr(f.widget,"id",None)=="r13_pw_tab_all"),None)')
    if tab_all:await q.input(tab_all[0]+tab_all[2]/2,tab_all[1]+tab_all[3]/2);await asyncio.sleep(.3)
    owned=await q.py('import renpy;result=list(renpy.store.room13["evidence"])')
    sets=proof_sets(title);chosen_set=next((s for s in sets if all('V111:'+k in owned for k in s)),node['correct'])
    if chosen_set!=node['correct']:log('  대체 정답 사용',chosen_set)
    for k in chosen_set:
        if 'V111:'+k in selected:continue
        # 첫 쪽부터 찾고, 없으면 「다음 →」로 쪽을 넘긴다
        prev=await find('r13_pw_prev')
        for _ in range(6):
            if prev is None:break
            p2=await find('r13_pw_prev');await q.input(p2[0]+p2[2]/2,p2[1]+p2[3]/2);await asyncio.sleep(.25)
            prev=await find('r13_pw_prev')
        rect=None
        for _ in range(6):
            rect=await find('r13_pw_check_%s'%k)
            if rect:break
            nxt=await find('r13_pw_next')
            if not nxt:break
            await q.input(nxt[0]+nxt[2]/2,nxt[1]+nxt[3]/2);await asyncio.sleep(.3)
        if rect:x,y,w,h=rect;await q.input(x+w/2,y+h/2);await asyncio.sleep(.3)
        else:log('  자료 칸 없음',k)
    await shot(q,'proof-checked-'+title[:12])
    rect=await q.py('import renpy\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if getattr(f.widget,"id",None)=="r13_pw_submit"),None)')
    if rect:x,y,w,h=rect;await q.input(x+w/2,y+h/2);await asyncio.sleep(.6);return True
    log('  제출 버튼 없음');return False

CHEESE={}   # 쟁점별 꼼수 단계: 0 전부 내기 → 1 엉뚱한 하나 → 2 정답
async def chances_left(q,key):
    r=await q.py('import renpy;result=renpy.store.r13_v111_proof_chances(%r)'%key)
    if r is None:return None
    m=re.search(r"남은 기회 (\d+)",r);return int(m.group(1)) if m else None
async def cheese_submit(q,st,mode):
    """꼼수 제출. all: 가진 자료를 쪽마다 전부 체크. wrong: 정답·덧붙임에 없는 자료 하나. 결과를 판정해 로그로 남긴다."""
    claim=st['claim'];key=claim[5:];node=PROOFS.get(key) or next((v for k,v in PROOFS.items() if k in key or key in k),None)
    owned=await q.py('import renpy;result=list(renpy.store.room13["evidence"])')
    async def ids():
        return await q.py('import renpy\nresult=[(f.widget.id,[f.x,f.y,f.w,f.h]) for f in renpy.display.focus.focus_list if str(getattr(f.widget,"id","") or "").startswith("r13_pw_check_")]') or []
    async def selected():
        return await q.py('import renpy;result=list(renpy.store.room13["arguments"].get(%r,[]))'%claim) or []
    async def page(step):
        st2=await q.state();bs=[b for b in st2['buttons'] if b['text'].strip()==('다음 →' if step>0 else '← 이전')]
        if not bs:return False
        x,y,w,h=bs[0]['rect'];await q.input(x+w/2,y+h/2);await asyncio.sleep(.3);return True
    tab_all=await q.py('import renpy\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if getattr(f.widget,"id",None)=="r13_pw_tab_all"),None)')
    if tab_all:await q.input(tab_all[0]+tab_all[2]/2,tab_all[1]+tab_all[3]/2);await asyncio.sleep(.3)
    for _ in range(8):
        if not await page(-1):break
    if mode=='all':
        seen=set()
        for _ in range(12):
            cur=await ids();keys=tuple(i for i,_ in cur)
            if keys in seen:break
            seen.add(keys)
            for wid,r in cur:
                if 'V111:'+wid[len('r13_pw_check_'):] not in await selected():
                    await q.input(r[0]+r[2]/2,r[1]+r[3]/2);await asyncio.sleep(.2)
            if not await page(1):break
    else:
        sets=await q.py('import renpy;s=renpy.store;result=sorted(set().union(*s.r13_v111_proof_sets(%r,%r))|set("V111:"+k for k in s.R13_PROOF_EXTRAS.get(%r,())))'%(key,list(node['correct']) if node else [],key)) or []
        pool=[k for k in owned if k not in sets]
        if not pool:log('  꼼수 엉뚱 자료 없음',key);return False
        target=pool[(len(key)*7)%len(pool)][5:]
        for _ in range(10):
            hit=next((r for wid,r in await ids() if wid=='r13_pw_check_'+target),None)
            if hit:await q.input(hit[0]+hit[2]/2,hit[1]+hit[3]/2);await asyncio.sleep(.2);break
            if not await page(1):break
    given=await selected()
    await shot(q,'cheese-%s-%s'%(mode,key[:10]))
    rect=await q.py('import renpy\nresult=next(([f.x,f.y,f.w,f.h] for f in renpy.display.focus.focus_list if getattr(f.widget,"id",None)=="r13_pw_submit"),None)')
    if not rect or not given:log('  꼼수 제출 불가',mode,key,len(given));return False
    before=await chances_left(q,key)
    x,y,w,h=rect;await q.input(x+w/2,y+h/2);await asyncio.sleep(1.0)
    won=await q.py('import renpy;result=renpy.store.r13_v111_value("proof_given:"+%r)'%key)
    kept=await selected();after=await chances_left(q,key)
    verdict='통과(확인 필요)' if won else '막힘'
    log('  꼼수',mode,key,'낸 수',len(given),'→',verdict,'남김',[k[5:] for k in kept],'기회',before,'→',after)
    if won:log('CHEESE-PASS',mode,key,[k[5:] for k in given])
    if not won and mode=='all' and len(kept)>0:log('CHEESE-KEPT',key,[k[5:] for k in kept])
    return True

async def cheese_crisis(q,st,mode):
    """옛 대조 화면 꼼수. 고른 목록을 직접 채우고(all: 가진 자료 전부, wrong: 엉뚱한 하나) 「논리를 연결한다」로 낸다."""
    claim=st['claim'];key=claim[5:];node=PROOFS.get(key) or next((v for k,v in PROOFS.items() if k in key or key in k),None)
    owned=await q.py('import renpy;result=list(renpy.store.room13["evidence"])') or []
    if mode=='all':given=list(owned)
    else:
        allowed=await q.py('import renpy;s=renpy.store;result=sorted(set().union(*s.r13_v111_proof_sets(%r,%r))|set("V111:"+k for k in s.R13_PROOF_EXTRAS.get(%r,())))'%(key,list(node['correct']) if node else [],key)) or []
        pool=[k for k in owned if k not in allowed]
        if not pool:log('  꼼수 엉뚱 자료 없음',key);return False
        given=[pool[(len(key)*7)%len(pool)]]
    await q.py('import renpy;s=renpy.store;c=__import__("copy").deepcopy(s.room13);c["arguments"][%r]=%r;s.room13=c;renpy.exports.restart_interaction();result=True'%(claim,given))
    await asyncio.sleep(.5);await shot(q,'cheese-%s-%s'%(mode,key[:10]))
    before=await chances_left(q,key)
    await q.press('논리를 연결한다');await asyncio.sleep(1.0)
    won=await q.py('import renpy;result=renpy.store.r13_v111_value("proof_given:"+%r)'%key)
    kept=await q.py('import renpy;result=list(renpy.store.room13["arguments"].get(%r,[]))'%claim) or []
    after=await chances_left(q,key)
    log('  꼼수',mode,key,'낸 수',len(given),'→','통과(확인 필요)' if won else '막힘','남김',[k[5:] for k in kept],'기회',before,'→',after)
    if won:log('CHEESE-PASS',mode,key,[k[5:] for k in given])
    if not won and mode=='all' and kept:log('CHEESE-KEPT',key,[k[5:] for k in kept])
    return True

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch_persistent_context(str(OUT.parent/('profile-autoplay-'+(os.environ.get('ROUTE') or 'base'))),executable_path='/opt/pw-browsers/chromium',viewport={'width':1280,'height':720},args=['--no-sandbox','--enable-unsafe-swiftshader','--autoplay-policy=no-user-gesture-required'])
        for prev in b.pages:await prev.close()
        pg=await b.new_page();q=Driver(pg,OUT);errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
        await pg.goto(URL,wait_until='domcontentloaded',timeout=180000)
        await pg.wait_for_function("typeof renpy_exec==='function'",timeout=180000);await asyncio.sleep(12)
        # 빈 프로필(캐시 없음)에서는 엔진이 뜨기까지 더 걸린다. 응답할 때까지 최대 4분 기다린다.
        for _ in range(24):
            try:
                await asyncio.wait_for(q.py('result=1'),20);break
            except Exception:
                await asyncio.sleep(10)
        for _ in range(30):
            await q.input(1100,600);await asyncio.sleep(1)
            try:
                if 'main_menu' in (await q.state())['screens']:break
            except Exception:pass
        await shot(q,'main')
        await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True')
        log('BUILD',await q.py('import renpy;result=renpy.store.config.version'))
        if os.environ.get('RESUME_DAY'):
            code='import renpy;renpy.exports.load("auto-day%s")'%os.environ['RESUME_DAY']
            await pg.evaluate('code=>{renpy_exec("exec("+JSON.stringify(code)+")").catch(()=>{});return true;}',code)
            await asyncio.sleep(3)
            try:await pg.evaluate("window._renpy_cmd_callback({data:true})")
            except Exception:pass
            log('RESUME auto-day'+os.environ['RESUME_DAY'])
        else:await q.press('처음부터')
        last=None;seen_shots=set();visits={};book_target=None;map_target=None;stale_n=0;stale_last=None;object_attempts={};say_shots={};last_day=1;t0=time.time()
        try:
            for step in range(30000):
                st=await snap(q);sc=st['screens']
                if '_exception' in sc:await shot(q,'exception');log('EXCEPTION');break
                if st['day'] and st['day']>=15:log('15일 도착');await shot(q,'day15');break
                if 'main_menu' in sc and step>50:log('메인 화면(결말)');await shot(q,'ending');break
                if st['day'] and st['day']!=last_day:
                    log('==== %d일'%st['day']);last_day=st['day']
                    try:await q.py('import renpy;renpy.exports.save("auto-day%d");result=True'%st['day']);log('SAVED auto-day%d'%st['day'])
                    except Exception as e:log('save failed',repr(e))
                key=(st['gate'],tuple(sc),st['choice'],st['claim'],st['location'])
                if key!=last:
                    log('STATE',step,st['day'],st['period'],st['gate'],sc,st['choice'],st['location'],'사람=',st['people']);last=key
                finger=json.dumps([st['gate'],sc,st['location'],st.get('values'),st.get('evidence'),st.get('say'),st.get('choice')],sort_keys=True,default=str)
                stale_n=stale_n+1 if finger==stale_last else 0;stale_last=finger
                if stale_n>=60:
                    dump=await q.state();log('STALE',st['gate'],st['location'],[b['text'] for b in dump['buttons']][:30]);await shot(q,'stale-'+str(st['gate']));break
                if 'say' in sc:
                    g=str(st['gate']);say_shots[g]=say_shots.get(g,0)+1
                    if say_shots[g]<=2:await shot(q,'say-%s-%s'%(g,st['who'] or '지문'))
                    await q.advance_dialogue();continue
                if 'r13_confirm' in sc:
                    yes=await q.py('import renpy;result=renpy.display.screen.get_screen("r13_confirm").scope["yes"]')
                    await shot(q,'confirm-'+str(st['gate']));await q.press(yes);continue
                if 'choice' in sc:
                    ck=('choice',st['gate'],st['choice']);visits[ck]=visits.get(ck,0)
                    try:captions=await q.py('import renpy;result=[i.caption for i in renpy.display.screen.get_screen("choice").scope["items"] if i.action is not None]')
                    except Exception as e:
                        if "'NoneType' object has no attribute" not in str(e):raise
                        await asyncio.sleep(1);continue
                    if not captions:await asyncio.sleep(.5);continue
                    pick=visits[ck]%len(captions)
                    if os.environ.get('ROUTE')=='alt':pick=(len(captions)-1-visits[ck])%len(captions)   # 다른 길: 마지막 선택지부터
                    if st['gate']=='lamp_observe':
                        pick=next((i for i in range(4) if not st['values'].get('lamp_part_'+str(i))),4)
                    if st['choice']=='afternoon' and os.environ.get('ROUTE')!='alt':pick=visits[ck]%len(captions)   # 포대·천·벤치·닦기 순으로 하고 식당 자리를 전한다
                    if ck not in seen_shots:await shot(q,'choice-%s'%(st['choice'] or st['gate']));seen_shots.add(ck)
                    visits[ck]+=1;log('  선택',pick,captions[pick]);await asyncio.sleep(.3);await q.press(captions[pick]);continue
                if 'r13_proof_workspace' in sc or 'r13_crisis_proof' in sc:
                    pk=('proof',st['claim']);visits[pk]=visits.get(pk,0)+1
                    if visits[pk]>60:log('STALE proof',st['claim']);await shot(q,'stale-proof');break
                    if pk not in seen_shots:await shot(q,'proof-'+str(st['gate']));seen_shots.add(pk)
                    if 'r13_proof_workspace' in sc and os.environ.get('ROUTE')=='cheese':
                        ck2=st['claim'];stage=CHEESE.get(ck2,0);left=await chances_left(q,ck2[5:])
                        # 기회가 셋 이상 남았거나 무제한일 때만 꼼수를 쓴다(회의를 지게 만들지 않는다)
                        if stage<2 and (left is None or left>=3):
                            CHEESE[ck2]=stage+1
                            if await cheese_submit(q,st,('all','wrong')[stage]):continue
                        else:CHEESE[ck2]=2
                    if 'r13_proof_workspace' in sc:
                        ok=await proof(q,st)
                        if not ok:
                            st2=await q.state();bs=[b for b in st2['buttons'] if b['text'].strip() in ('되묻는다','자료 다시 보기','조사 계속')]
                            if bs:x,y,w,h=bs[0]['rect'];await q.input(x+w/2,y+h/2);await asyncio.sleep(.6)
                            else:await q.input(1202,86);await asyncio.sleep(.5)
                        continue
                    if os.environ.get('ROUTE')=='cheese':
                        ck2=st['claim'];stage=CHEESE.get(ck2,0);left=await chances_left(q,ck2[5:])
                        if stage<2 and (left is None or left>=3):
                            CHEESE[ck2]=stage+1
                            try:
                                if await cheese_crisis(q,st,('all','wrong')[stage]):continue
                            except AssertionError as e:log('  꼼수 실패',str(e)[:80])
                        else:CHEESE[ck2]=2
                    title=st['claim'][5:];node=PROOFS.get(title) or next((v for k,v in PROOFS.items() if k in title or title in k),None)
                    if not node:
                        log('  대조 정답 모름',title);await shot(q,'proof-unknown');await q.press('되묻는다');continue
                    selected=await q.py('import renpy;result=list(renpy.store.room13["arguments"].get(renpy.store.v111_claim,[]))')
                    owned=await q.py('import renpy;result=list(renpy.store.room13["evidence"])')
                    chosen_set=next((s2 for s2 in proof_sets(title) if all('V111:'+k in owned for k in s2)),node['correct'])
                    missing=[x for x in chosen_set if 'V111:'+x not in selected]
                    if missing:book_target='V111:'+missing[0];await q.press('근거를 내놓는다')
                    else:await q.press('논리를 연결한다')
                    continue
                if 'r13_book' in sc:
                    if book_target:await q.select_material(book_target);book_target=None
                    else:
                        # 「자료 다시 보기」로 연 책에는 「선택 마치기」가 없다. 없으면 X 로 닫는다.
                        st2=await q.state()
                        if any('선택 마치기' in ''.join(b['text'].split()) for b in st2['buttons']):await q.press('그만두기')
                        else:await q.input(1202,86);await asyncio.sleep(.4)
                    continue
                if 'r13_records' in sc:await q.input(1202,86);await asyncio.sleep(.4);continue
                if 'r13_more_tools' in sc:await q.input(100,600);await asyncio.sleep(.4);continue
                if 'r13_fork_screen' in sc:await shot(q,'fork');await q.input(1202,86);await asyncio.sleep(.4);continue
                if 'r13_topics' in sc:
                    options=st['binding'].get('options',[]);person=await q.py('import renpy;c=renpy.display.screen.get_screen("r13_topics");result=c.scope["person"] if c else None')
                    if person is None:await asyncio.sleep(.3);continue
                    tk=('topics',st['gate'],person)
                    if tk not in seen_shots:await shot(q,'topics-%s-%s'%(st['gate'],person));seen_shots.add(tk)
                    eligible=[o for o in options if o.get('person')==person and (not o.get('location') or o.get('location')==st['location'])]
                    gate=st['gate']
                    if gate=='gate_investigate' and any(k not in st['evidence'] for k in ('V111:E03','V111:E04')):
                        await q.press('돌아가기');continue
                    preferred={'gate_investigate':5,'gate_choice':1,'registered_menu':1,'post_menu':1}.get(gate)
                    if not eligible:await q.press('돌아가기');await asyncio.sleep(.3);continue
                    visits[tk]=visits.get(tk,0)
                    # 같은 관문에서 같은 질문을 두 번 했으면 다른 질문으로, 다 했으면 돌아간다(12일 서리 「약장 관리」가 끝없이 반복됐다)
                    asked={k[3] for k in visits if k[:3]==('asked',gate,person)}
                    fresh=[o for o in eligible if visits.get(('asked',gate,person,o['title']),0)<2]
                    if not fresh:await q.press('돌아가기');await asyncio.sleep(.3);continue
                    option=next((o for o in fresh if o.get('index')==preferred),fresh[visits[tk]%len(fresh)]);visits[tk]+=1
                    visits[('asked',gate,person,option['title'])]=visits.get(('asked',gate,person,option['title']),0)+1
                    if option.get('present'):book_target=option['present']
                    log('  질문',option['title']);await q.press(option['title']);continue
                if 'r13_map' in sc:
                    moves=[o.get('move') for o in st['binding'].get('options',[]) if o.get('move')]
                    target=map_target or (moves[0] if moves else None);map_target=None
                    if not target:
                        try:await q.press('현장으로')
                        except AssertionError:await q.input(1240,40);await asyncio.sleep(.4)
                        continue
                    mk=('map',target)
                    if mk not in seen_shots:await shot(q,'map-'+str(target));seen_shots.add(mk)
                    try:await q.navigate_map(target)
                    except AssertionError as e:log('  지도 이동 실패(다음 바퀴)',str(e)[:80]);await asyncio.sleep(.5)
                    continue
                if 'r13_hub' in sc:
                    gate=st['gate'];options=st['binding'].get('options',[])
                    hk=('hub',gate,st['location'])
                    if hk not in seen_shots:
                        await asyncio.sleep(.5);await shot(q,'hub-%s-%s'%(gate,st['location']));seen_shots.add(hk)
                        # 인물 좌표(화면 기준 x·y·폭·높이, 자리 여부)를 남겨 캡처와 대조한다.
                        try:
                            log('  배치',await q.py('import renpy;s=renpy.store;off=s.r13_world_offset();result=[(a["person"],int(a["x"]-off),int(a["y"]),int(a.get("width",0) or 0),int(a["height"]),bool(a.get("slot"))) for a in s.r13_stage_people()]'))
                        except Exception as e:log('  배치 실패',str(e)[:80])
                        try:
                            log('  층15',await q.py('import renpy;s=renpy.store;loc=s.room13.get("location");result=(s.r13_v111_active(),s.r13_world_offset(),s.r13_world_width(),[tuple(r) for r in s.r13_stage_critical(loc,s.R13_WORLD_LAYOUTS.get(loc))],[(a["person"],a.get("rect"),bool(a.get("slot")),a.get("depth")) for a in s._r13_clear_stage_people()])'))
                        except Exception as e:log('  층15 실패',str(e)[:120])
                        try:
                            log('  층16직접',await q.py('import renpy;s=renpy.store;loc=s.room13.get("location");rects=[tuple(r) for r in s.r13_stage_critical(loc,s.R13_WORLD_LAYOUTS.get(loc))];rows=s._r13_clear_stage_people();out=s.r13_separate_overlaps(rows,rects,s.r13_world_width());result=[(a["person"],a.get("rect")) for a in out]+[("층16출력",[(a["person"],a.get("rect")) for a in s._r13_field_dot_stage()])]'))
                        except Exception as e:log('  층16직접 실패',str(e)[:160])
                    if not options:
                        log('  선택 없음',gate);await asyncio.sleep(.5);continue
                    visits[hk]=visits.get(hk,0)
                    if gate=='gate_investigate':
                        idx=0 if 'V111:E03' not in st['evidence'] else 1 if 'V111:E04' not in st['evidence'] else 5
                        option=next((o for o in options if o['index']==idx),options[0])
                    elif gate=='lamp_observe':
                        idx=next((i for i in range(4) if not st['values'].get('lamp_part_'+str(i))),4);option=next((o for o in options if o['index']==idx),options[0])
                    elif gate=='registered_menu':option=next((o for o in options if o.get('move')),options[0])
                    else:
                        fresh=[o for o in options if not (o.get('person') and visits.get(('asked',gate,o['person'],o['title']),0)>=2) and not (o.get('object') and object_attempts.get((gate,o['object']),0)>=8) and visits.get(('asked',gate,'__obj__',o['title']),0)<9]
                        pool=fresh or options
                        option=pool[(visits[hk]//6)%len(pool)]   # 같은 선택이 여섯 바퀴 안에 안 풀리면 다음 선택
                        if os.environ.get('ROUTE')=='alt':option=pool[(len(pool)-1-visits[hk]//6)%len(pool)]
                    visits[hk]+=1
                    if option.get('location') and option['location']!=st['location']:
                        map_target=option.get('move') or option['location'];await q.press('지도');continue
                    if option.get('move'):await q.press('지도');continue
                    if option.get('person'):
                        person=option['person'];state=await q.state()
                        if not any(b.get('value')==repr(('person',person)) for b in state['buttons']):
                            try:
                                x=await q.py('import renpy;s=renpy.store;a=next(a for a in s.r13_stage_people() if a["person"]=='+repr(person)+');result=a["x"]-s.r13_world_offset()')
                            except Exception:
                                log('  사람 없음',person);await asyncio.sleep(.5);continue
                            arrow='‹' if x<640 else '›'
                            if any(arrow in b['text'] for b in state['buttons']):await q.press(arrow)
                            await asyncio.sleep(.6)
                        else:await q.value(('person',person))
                        continue
                    if option.get('object'):
                        obj=option['object'];attempt=object_attempts.get((gate,obj),0);object_attempts[(gate,obj)]=attempt+1
                        try:await q.click_object(obj,attempt%28)
                        except AssertionError:log('  물건 못 누름',obj);visits[('asked',gate,'__obj__',option['title'])]=9;await asyncio.sleep(.4)
                        continue
                    log('  처리 못 한 선택',option);await asyncio.sleep(.5);continue
                await asyncio.sleep(.15)
        except Exception as e:
            log('ERROR',repr(e));await pg.screenshot(path=str(OUT/'failure.png'))
        log('ERRORS',errors[:5],'시간',int(time.time()-t0))
        (OUT/'log.txt').write_text('\n'.join(LOG));await b.close()
asyncio.run(main())
