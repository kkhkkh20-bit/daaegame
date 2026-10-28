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

# ---------------------------------------------------------------- ROUTE=true (진엔딩 「새로운 아침」 예방 길)
# 미래를 아는 플레이어가 사건마다 미리 손을 써서 사망 0·대승리 둘·필수 회의 넷 이김으로 14일 결말에 닿는 길.
# 조건은 game/room13_v111_newworld_rules.rpy 의 r13_nw_true_ending_ready(). 계획에 없는 관문·선택창은 기본 길과 같다.
# 항목은 「제목」 또는 (제목, 조건) — 조건은 지금 판정 값(values)을 받아 참일 때만 그 제목을 고른다.
TRUE_ROUTE=os.environ.get('ROUTE')=='true'
TRUE_GATES={
    # 2일 피코(3번 등 밑에서 얼어 죽음): 나비 포대 → 할머니 마른 천 → 벤치 살피기·닦기 → 피코에게 자리 → 함께 입실.
    # 네로 쪽(침구 두 장)은 고르지 않는다. 그래서 12일 다람에게 열이 나고 수프는 배식 직전 중단으로 막는다.
    'afternoon2':['포대를 옮긴다','마른 천을 빌린다','벤치 표면을 살핀다','천으로 벤치의 물감을 닦는다','식당에 앉을 자리를 전한다'],
    # 2일 밤: 등 끈 묶기(3번 등 미수판)는 하지 않는다. 식당 생존판 하나로 간다(3일 회의 증거가 달라지지 않게).
    'lamp_prep2':['방으로 들어간다'],
    # 4일 밤 문 앞: 세 곳을 하나씩 본다(같은 것을 다시 누르지 않게).
    'inspect_gate4':[('울타리 천',lambda v:not v.get('d4_fence_seen')),('겹친 발자국',lambda v:not v.get('d4_tracks_seen')),('엎어진 양동이',lambda v:not v.get('d4_bucket_seen'))],
    # 5일 저녁(불 대승리 길1): 여관 가는 길에 빨래터로 돌아 젖은 장갑을 건다 → 누비네 이야기를 엿듣는다(NW_LAUNDRY_TALK).
    'travel':[('마을 빨래터',lambda v:not v.get('grand_laundry_seen5'))],
    'laundry5':['빨래 줄에 젖은 장갑을 건다','여관 접수대'],
    # 6일 꼬미(장작 창고 불): 깡통 줄 살피기 → 줄 풀고 도토리 → 선생님께 자리 → 같이 가자 → 학교 인계.
    'afternoon6':['장작더미 옆 깡통 줄을 살핀다','줄을 풀고 도토리를 챙긴다','아이들 자리를 여쭌다','학교에 자리가 났어. 같이 갈래?'],
    'hp_meal6':['다람아, 애들한테 가자.'],
    # 7일 불 회의 대승리: 보리 목격 전에 기름통 밑 홈에서 누비네 배급표(NW_NUBI_TICKET)를 꺼낸다.
    'bori_witness7':['통 밑 홈을 들춘다','창고 문 앞에서 무엇을 보셨습니까?'],
    # 7일 부엉이(13호 살인): 부리에게 집게 → 재받이의 배급 돌 → 13호 난로의 검푸른 돌과 바꾼다(prevention=stone).
    'free_day7':['집게 하나만 빌릴 수 있을까?','재받이를 들여다본다','집게로 돌을 꺼내고, 주머니의 배급 돌을 넣는다','다람아, 이제 13호에 가 보자.'],
    # 10일 기록 회의 뒤: 부엉이에게 편지 전달을 묻고, 공개 수치로 인계한다.
    'private_handoff10':[('아내가 직접 편지를 건넸습니까?',lambda v:not v.get('owl_invitation_testimony')),'공개 수치만 대조하고 인계해 주십시오.'],
    # 11일 엄마: 세 질문을 하나씩.
    'mother_questions11':[('어떻게 지냈어?',lambda v:not v.get('mother_q_life')),('왜 우리를 부르지 않았어?',lambda v:not v.get('mother_q_invitation')),('왜 돌아오지 못했어?',lambda v:not v.get('mother_q_return'))],
    # 11일 네로·아랫길 노인(등이 끊긴 밤 늦은 출발로 사망): 낮에 수레를 준비해 세 사람을 학교로 옮긴다.
    # 짐칸을 살피며 흰 그릇 하나를 주머니에 넣는다(12일 수프 대승리 NW_RETURNED_BOWL 의 앞 단계).
    'rescue_cart11':['수레 짐칸을 살핀다','그릇 하나를 집는다','수레 짐을 내려 자리를 비운다','덮개를 접어 빈 짐칸에 싣는다','까로에게 운반을 부탁한다','아랫길을 비추는 등을 점검한다','아랫길 세 사람의 받을 자리를 비운다','수레를 끌고 아랫길로 간다'],
    'rescue_handoff11':['세 사람을 맞은 자리와 명단을 확인한다'],
    'night_rescue_prepare11':['낮에 챙긴 운반 준비를 확인한다'],
    'sleep11_input':['잠자리를 정리한다'],
    # 12일 도담(학교 국): 다람의 열로 아침 예방은 막혀 있다. 배식 직전 작은 냄비·흰 그릇·봉인을 보고 냄비를 열어 멈춘다.
    'morning_prep12':['배식 준비를 살핀다'],
    'meal_inspect12':['작은 냄비와 국자 자리를 살핀다','흰 그릇이 놓인 자리를 살핀다','선반에 놓인 병의 봉인을 살핀다','흰 그릇을 옆으로 옮기고 작은 냄비를 연다'],
    # 12일 수프 회의 대승리: 주머니의 그릇을 배식대 옆에 놓아 「돌아온 흰 그릇」을 얻는다.
    'bottle_match12':['주머니의 그릇을 배식대 옆에 놓아 본다','병과 파편의 경계를 대조한다'],
    # 수프를 미리 막은 판(회의 없음)일 때의 대체: 그릇을 보이고 돌목에게 바닥 표시를 묻는다(결정 7).
    'early_bowl12':['주머니의 그릇을 배식대 옆에 놓아 본다','이 그릇 바닥의 표시는 무엇입니까?','저녁 배식을 돕는다'],
    # 13일 담요 회의: 판돌의 담요를 실제로 수선해 둔다(E13_MENDING).
    'blanket_mend13':['회색 담요를 실제로 수선한다'],
    # 13일 수레 뒤: 호송 고리를 바둑이·돌목·까로 순으로 끊고 학교로 돌아간다.
    'transport_cleanup13':['앞으로의 호송을 확인한다','명령 전체를 중지하고, 사본을 직접 전하겠습니다.','강제 운반은 맡지 말고, 빈 수레를 돌려주자.','빈 수레 반환을 요청한다.','중지 명령 사본을 너울에게 다시 보인다.','학교로 돌아간다'],
}
# 선택창(메뉴) 글귀. 보이는 것 중 앞에 있는 것을 고른다. 없으면 기본 길과 같다.
TRUE_CHOICES=[
    '그릇을 돌려주러 같이 가자.',                       # 6일 꼬미를 만나러 학교 뒤로
    '아이들은 학교에서 기다리게 하자.',                 # 7일 누비네 아이들을 학교로
    '집게로 돌을 꺼내고, 주머니의 배급 돌을 넣는다',     # 7일 13호 난로(물건 행동 고르기 창)
    '통 밑 홈을 들춘다',                               # 7일 기름통(물건 행동 고르기 창)
    '아랫길 대피 준비를 확인한다',                       # 11일 네로·노인 낮 구조
    # 11일 가설 회의(정답 쪽만 고른다)
    '꺼낸 아르카 곁에 오래 있던 사람부터 무너진다','두 사람이 아르카 곁에 머문 시간을 비교한다','백 부인은 그 돌 곁에서 잠을 자지 않는다',
    '요즘 태우는 돌이 더 독하다','아이들이 밤을 어디서 보내는지 본다','한 방의 돌을 꺼내자 그 앞에서 흐려지던 머리가 맑아졌다',
    '한 방의 돌을 치우자 무너지던 사람이 돌아왔다',
    '배식 전에 더 살핀다',                             # 12일 배식 직전 중단
    '흰 그릇을 옆으로 옮기고 작은 냄비를 연다',
    '주머니의 그릇을 배식대 옆에 놓아 본다',
    '약장 밖에 맡긴 약도 있는지 묻는다',
    '돌목에게 감독을 맡긴다',                           # 12일 선생님을 너울에게 넘기지 않는다
    ('거절하고 현장에 남는다',lambda v:v.get('family_offer_terms_seen')),   # 13일 가족만 빠지는 거래를 거절
    '조건을 더 묻는다',
    '엄마와 다람이 곁에 남게 한다',
    ('하차한 사람부터 부축한다',lambda v:v.get('handover_prepared13')),     # 13일 수레의 사람을 모두 학교로
    '학교 침상과 인수를 먼저 확인한다',
    '7일 회의 기록을 함께 읽는다',                     # 13일 군중(옛 메뉴): 불 대승리 기록
]
TRUE_PREFER_PROOF=('NW_NUBI_TICKET','NW_RETURNED_BOWL')   # 대승리 보너스 증거가 든 정답 묶음을 먼저 낸다
TRUE_TRACK=('piko_alive','KKOMI_ALIVE','OWL_ALIVE','nero_alive','prevention','route7','route12','carried_dry_blankets','daram_fever12',
    'neoul_promise_proven','transfer_list_voided','grand_bowl_pocket','grand_ticket_spot_known','grand_laundry_seen5','departed_names',
    'outcome13','crowd_injury','ending14','lower_road_handover','family_location','DARAM_DETAINED','bami_status','silluk_status','stove13_7')
def true_tracked(values):
    return {k:v for k,v in (values or {}).items() if k in TRUE_TRACK or k.startswith(('meeting:','grand:','alive:','listed:','departed:','fate'))}
def _entry(e):
    return (e,None) if isinstance(e,str) else e
def true_option(gate,options,values,person=None):
    """계획에서 지금 열려 있는 첫 선택(현장·질문)."""
    for e in TRUE_GATES.get(gate,()):
        title,cond=_entry(e)
        if cond and not cond(values):continue
        o=next((o for o in options if o.get('title')==title and (person is None or o.get('person')==person)),None)
        if o:return o
    return None
def true_caption(gate,captions,values):
    """선택창 글귀: 이 관문의 계획 제목 → 전역 계획 글귀 순."""
    for e in list(TRUE_GATES.get(gate,()))+TRUE_CHOICES:
        title,cond=_entry(e)
        if cond and not cond(values):continue
        if title in captions:return captions.index(title)
    return None
def true_set(sets,owned):
    """가진 정답 묶음 가운데 대승리 보너스 증거가 든 것을 먼저."""
    have=[s for s in sets if all('V111:'+k in owned for k in s)]
    return next((s for s in have if any(k in TRUE_PREFER_PROOF for k in s)),have[0] if have else None)
TRUE_CHECK=('import renpy;s=renpy.store;v=s.r13_v111_value;result=dict(ready=s.r13_nw_true_ending_ready(),ending14=v("ending14"),'
    'ending_calc=s.r13_nw_ending14(),dead=s.r13_nw_dead(),ledger=s.r13_v111_owned("NW_NEOUL_LEDGER"),grand_fire=v("grand:fire"),'
    'grand_soup=v("grand:soup"),meetings={m:v("meeting:"+m) for m in ("gate","lamp","gate_post","fire","room13","records","hypothesis","soup","blanket","piko","altar")},'
    'departed=v("departed_names"),outcome13=v("outcome13"),crowd_injury=v("crowd_injury"))')
async def true_check(q,where):
    try:r=await q.py(TRUE_CHECK)
    except Exception as e:log('TRUE-CHECK 실패',where,str(e)[:120]);return None
    fails=[]
    if r['ending_calc']!='morning':fails.append('ending14 판정=%s'%r['ending_calc'])
    if r['dead']:fails.append('사망·떠남 %s'%r['dead'])
    if not r['ledger']:fails.append('NW_NEOUL_LEDGER 없음')
    if r['grand_fire'] is not True:fails.append('grand:fire=%s'%r['grand_fire'])
    if r['grand_soup'] is not True:fails.append('grand:soup=%s'%r['grand_soup'])
    for m in ('records','hypothesis','blanket','altar'):
        if r['meetings'].get(m)!='win':fails.append('meeting:%s=%s'%(m,r['meetings'].get(m)))
    log('TRUE-CHECK',where,'ready=',r['ready'],'ending14=',r['ending14'],'회의=',r['meetings'],'떠남=',r['departed'],'outcome13=',r['outcome13'],'못 맞춘 조건=',fails or '없음')
    return r
SCREENS=("main_menu","say","choice","r13_confirm","r13_hub","r13_topics","r13_map","r13_book","r13_records","r13_crisis_proof","r13_proof_workspace","r13_more_tools","r13_side_questions","r13_fork_screen","_exception")
if TRUE_ROUTE:SCREENS=SCREENS+("r13_meeting_retry_choice",)   # 진엔딩 길: 회의를 지면 뜨는 다시 하기 창을 알아본다
n_shot=[0]
async def shot(q,name):
    n_shot[0]+=1;await q.shot('%03d-%s'%(n_shot[0],name))

async def press_map(q):
    # 진엔딩 길: 지도 단추를 누른 바로 뒤의 바퀴가 아직 현장 화면을 읽으면 두 번 눌러 「지도」를 못 찾고 멈췄다(6일 저녁).
    # 이미 지도가 열려 있으면 다음 바퀴에서 지도 처리로 넘긴다. 다른 길은 예전 그대로 바로 누른다.
    if not TRUE_ROUTE:return await q.press('지도')
    try:await q.press('지도')
    except AssertionError as e:
        if 'r13_map' not in str(e)[:200]:raise
        log('  지도가 이미 열려 있음')

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
    if TRUE_ROUTE:chosen_set=true_set(sets,owned) or chosen_set
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
        last=None;true_prev={};seen_shots=set();visits={};book_target=None;map_target=None;stale_n=0;stale_last=None;object_attempts={};say_shots={};last_day=1;t0=time.time()
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
                if TRUE_ROUTE:
                    tv=true_tracked(st.get('values'))
                    for k in sorted(set(tv)|set(x for x in true_prev if not x.startswith('_'))):
                        if tv.get(k)!=true_prev.get(k):log('  값',k,true_prev.get(k),'→',tv.get(k))
                    if tv.get('ending14') and tv.get('ending14')!=true_prev.get('ending14'):await true_check(q,'결말 판정 직후')
                    fin=true_prev.get('_final');true_prev.clear();true_prev.update(tv);true_prev['_final']=fin
                    if 'r13_meeting_retry_choice' in sc:
                        # 진엔딩 길에서 회의를 지면 그 판은 진엔딩이 안 된다. 기록을 남기고 결과를 받아들여 끝까지 가 본다.
                        log('MEETING-LOST',st['claim'],{k:v for k,v in st['values'].items() if k.startswith('meeting:')});await shot(q,'meeting-lost')
                        await q.press('결과를 받아들인다');continue
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
                    if TRUE_ROUTE and st['values'].get('story14_completed') and not true_prev.get('_final'):
                        true_prev['_final']=True;await true_check(q,'이야기를 마친 뒤')
                        log('결말 이름',await q.py('import renpy;s=renpy.store;result=s.R13_FORK_ENDINGS.get(s.r13_v111_value("ending14"))'))
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
                    if TRUE_ROUTE:
                        tp=true_caption(st['gate'],captions,st['values'])
                        if tp is not None:pick=tp
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
                    if TRUE_ROUTE:chosen_set=true_set(proof_sets(title),owned) or chosen_set
                    missing=[x for x in chosen_set if 'V111:'+x not in selected]
                    if missing:book_target='V111:'+missing[0];await q.press('근거를 내놓는다')
                    else:await q.press('논리를 연결한다')
                    continue
                if 'r13_book' in sc:
                    if TRUE_ROUTE and not book_target:
                        # 이야기가 직접 여는 「보여 주기」 책: 13일 너울에게 중지 명령 사본, 14일 장치 앞에서 인계 기록.
                        want={13:'V111:E13_ORDER',14:'V111:E13_HANDOVER'}.get(st['day'])
                        if want and want in st['evidence'] and await q.py('import renpy;c=renpy.display.screen.get_screen("r13_book");result=bool(c and c.scope.get("present_label"))'):
                            book_target=want;log('  보여 줄 자료',want)
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
                    if TRUE_ROUTE:
                        planned=true_option(gate,eligible,st['values'],person)
                        if planned:option=planned
                        elif gate in TRUE_GATES and true_option(gate,options,st['values']):
                            await q.press('돌아가기');await asyncio.sleep(.3);continue   # 계획의 다음 일은 다른 사람·물건이다
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
                    elif TRUE_ROUTE and true_option(gate,options,st['values']):option=true_option(gate,options,st['values'])
                    else:
                        fresh=[o for o in options if not (o.get('person') and visits.get(('asked',gate,o['person'],o['title']),0)>=2) and not (o.get('object') and object_attempts.get((gate,o['object']),0)>=8) and visits.get(('asked',gate,'__obj__',o['title']),0)<9]
                        pool=fresh or options
                        option=pool[(visits[hk]//6)%len(pool)]   # 같은 선택이 여섯 바퀴 안에 안 풀리면 다음 선택
                        if os.environ.get('ROUTE')=='alt':option=pool[(len(pool)-1-visits[hk]//6)%len(pool)]
                    visits[hk]+=1
                    if option.get('location') and option['location']!=st['location']:
                        map_target=option.get('move') or option['location'];await press_map(q);continue
                    if option.get('move'):
                        if TRUE_ROUTE:map_target=option['move']   # 들르는 길(빨래터)도 지도에서 그 자리를 고른다
                        await press_map(q);continue
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
