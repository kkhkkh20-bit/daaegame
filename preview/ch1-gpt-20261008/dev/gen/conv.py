# 장면 대본 JSON(줄별 전체 상태) → 게임 데이터(EP.PRO, EP.END, EP.I9, 조사·질문 대사 덮어쓰기)
import json,re,sys
D=json.load(open('/tmp/claude-0/in2/sc.json'))
SC={s['id']:s for s in D['scenes']}
KEY={'아빠':'det0','다람':'det1','할머니':'innma','세련':'seryeon','너울':'wanggu','나비':'nabi','밤이':'geokkuri','도토':'doto','부리':'buri','까로':'karo'}
# 화면 인물 표정(그림 강도 기준) → 무대 표정 키. 없는 그림은 기본.
def face(who,expr):
    e=expr or ''
    if who=='det1':
        if e in('놀람','당황'):return 'shock'
        if e in('걱정','그리움'):return 'sad'
        if e=='결심':return 'resolve'
        if e in('활짝 웃음','기쁨','큰 웃음'):return 'laugh'
        return ''
    if who=='seryeon':return 'shock' if e in('놀람','다급함') else ''
    if who=='geokkuri':return 'shock' if e in('놀람','당황') else ''
    if who=='innma':
        if e in('경계','망설임','걱정'):return 'think'
        if e in('옅은 미소','안도'):return 'smile'
        return ''
    if who in('doto',):return 'shock' if e in('당황','놀람') else ('think' if e in('의문',) else '')
    if who=='buri':return 'shock' if e in('미안함',) else ''
    if who=='wanggu':return 'think' if e in('의문',) else ''
    return ''
def js(s):return json.dumps(s,ensure_ascii=False)
def fg(l):
    f=l.get('foreground') or ''
    return KEY.get(f.split(' ')[0],'')
# 연출 줄 처리표: 표시할 회색 지문(대체 그림 없는 사실), 효과음, 특수 연출
NARR={'P1-10':'아빠가 안주머니에서 접힌 편지를 꺼낸다.','P1-24':'아빠와 다람이 차례로 승객 명부에 서명한다.',
 'P2-10':'긴 옷을 입은 노인이 걸음을 멈추고 다람의 목걸이를 바라본다.','P2-11':'노인은 말없이 고개를 돌려 골목으로 사라진다.',
 'P4-06':'아빠가 펜을 받아 두 사람 이름을 적는다.','P9-10':'세련이 내려놓은 가방 틈으로, 처음 보는 봉인이 찍힌 편지 묶음이 보인다.',
 'P13-09':'아빠가 겨울잠쥐를 조심스럽게 꺼내 빈 빵 바구니로 옮기고, 수건을 한 겹 덮는다.',
 'E1-06':'너울의 기록부 사이로, 처음 보는 봉인이 찍힌 편지 묶음이 들어간다.','E2-09':'마차가 고개 너머로 멀어진다. 길이 금세 하얗게 지워진다.',
 'E4-05':'펼쳐진 공책. 표지에 「손님 장부 둘째 권」.','E4-14':'할머니가 다람이 내민 엄마 사진을 한참 들여다보다가, 장부를 천천히 덮는다.',
 'E5-05':'창고 안쪽에서 이불 펴는 소리가 난다.','E5-13':'다람이 마차에서부터 아껴 둔 마지막 간식 봉지를 뜯어, 절반을 아빠 손에 올린다.'}
SFX={'P1-21':'doorOpen','P5-16':'door','P8-11':'door','P10-09':'bell10','P12-18':'steps','P13-12':'steps','P13-17':'steps','I04-05':'steps','I07-08':'steps',
 'I12-03':'lock','E2-09':'carDepart','E4-09':'steps','E4-16':'door','E5-08':'steps','P3-15':'steps','P5-18':'steps','P2-11':'steps'}
# 다람 강한 감정(v3 전신 포즈): 장면 대본의 같은 '걱정' 중에서도 무서운 발견을 전하는 줄만. 포즈가 줄마다 바뀌지 않게 이어지는 줄까지 유지
STRONG={'P1-17':'sad','P1-18':'sad','P1-19':'sad','P1-20':'sad','P12-23':'cower','P12-24':'cower','P13-10':'cower','P13-11':'cower','I01-06':'oops','I01-07':'oops'}
INSPECT={'I01-05':'C01a','I01-09':'C01b','I03-06':'C11','I08-04':'C05','I10-03':'C08','I11-03':'C09','I16-09':'C01show'}
def conv(s,mode):
    """mode: play(프롤로그·후일담: 배열+객체) / say(조사·질문: 배열, 연출은 @dir)"""
    out=[];prev_fg=None
    for l in s['lines']:
        lid=l['line_id'];t=l['text'];ty=l['type'];cond=l.get('condition') or ''
        f=fg(l);fc=face(f,l.get('expression_required'))
        entry=cond.startswith('이 장소에 새로 진입') or cond.startswith('첫 진입 또는')
        snd=l.get('appearance_sfx') or ''
        chime=('띠링' in snd)
        old_fg=prev_fg
        if ty!='연출' or l.get('display_change') in('등장','교체','퇴장'):prev_fg=f if l.get('display_change')!='퇴장' else None
        if ty=='연출':
            dc=l.get('display_change')
            d={}
            if lid in SFX:d['sfx']=SFX[lid]
            if dc in('등장','교체') and f:d['who']=f;d['chime']=1 if chime else 0
            if dc=='퇴장':d['who']='none'
            m=re.match(r'\[(안내|암전|증거 획득[^\]]*)\]\s*(.*)',t)
            items=[]
            if lid=='P3-15' or lid=='P5-18' or lid=='P13-17' or lid=='I07-08' or lid=='E5-08':
                # 실제 퇴장 뒤 다람 등장: 비우고 잠깐 뒤 다람
                items.append(('dir',{'who':'none','sfx':SFX.get(lid,'steps'),'ms':380}))
                if lid=='I07-08':items.append(('dir',{'who':'det1','chime':0,'ms':220}))
                elif lid=='E5-08':items.append(('dir',{'who':'det1','chime':1,'ms':220}))
                elif lid=='P13-17':pass
                else:items.append(('dir',{'who':'det1','chime':1,'ms':220}))
                d={}
            elif lid=='P2-10':items.append(('dir',{'who':'none','ms':300}))
            elif lid=='E4-16':items.append(('dir',{'who':'none','sfx':'door','ms':450}));items.append(('dir',{'who':'det1','chime':0,'ms':250}));d={}
            elif lid in('P12-08','P13-12','E4-09','I04-05','E5-05','P6-06','E1-02','E2-02','P1-21'):
                if 'sfx' in d:items.append(('dir',{'sfx':d.pop('sfx'),'ms':380}))
            if m:
                k=m.group(1)
                if k=='안내':items.append(('hint',m.group(2)))
                elif k=='암전':items.append(('fade',1))
                elif k.startswith('증거 획득'):items.append(('grant','C07'))
                d={}
            if d:dd=dict(d);dd.setdefault('ms',4000 if d.get('sfx')=='bell10' else 380 if 'who' in d else 420);items.append(('dir',dd))
            if lid in INSPECT:items.append(('inspect',INSPECT[lid]))
            if lid in NARR:items.append(('narr',NARR[lid]))
            if lid=='P13-09':items.insert(0,('beat','inn_basket_transferred'))
            for it in items:out.append(it+(entry,))
            continue
        w=KEY.get(l.get('speaker'),'narr')
        dc=l.get('display_change')
        if dc in('등장','교체') and f and f!=old_fg and mode in('play','say'):
            out.append(('dir',{'who':f,'chime':1 if chime else 0,'ms':260},entry))
        if lid in STRONG:fc=STRONG[lid]
        if ty=='속마음':out.append(('inner',t,entry,fc));continue
        txt=re.sub(r'^[①②③]\s*','',t)
        out.append(('line',w,txt,fc,entry))
    return out
def emit(items,mode):
    r=[]
    for it in items:
        k=it[0]
        if k=='line':
            _,w,t,fc,entry=it;r.append('L(%s,%s,%s)'%(js(w),js(t),js(fc)) if fc else 'L(%s,%s)'%(js(w),js(t)))
        elif k=='inner':
            _,t,entry,fc=it;r.append('I(%s%s)'%(js(t[1:-1] if t.startswith('(') else t),',null,1' if entry else ''))
        elif k=='narr':r.append('N(%s)'%js(it[1]))
        elif k=='dir':
            d=it[1];entry=it[2]
            if mode=='play':r.append('D(%s)'%js(d))
            else:r.append('L("@dir",%s)'%js(';'.join('%s:%s'%(a,b) for a,b in d.items())+(';entry:1' if entry else '')))
        elif k=='hint':r.append('{hint:%s}'%js(it[1]))
        elif k=='fade':r.append('{fade:1}')
        elif k=='grant':r.append('{grant:"C07",card:1}')
        elif k=='beat':r.append('{beat:%s}'%js(it[1]) if mode=='play' else '')
        elif k=='inspect':r.append('L("@inspect",%s)'%js(it[1]))
    return ',\n   '.join(x for x in r if x)
BG={'P1':'carriage','P2':'plaza','P3':'reception','P4':'reception_desk','P5':'corridor','P6':None,'P7':None,'P8':None,'P9':'reception','P10':'room','P11':'corridor','P12':None,'P13':None,
    'E1':'reception','E2':'reception','E3':None,'E4':'corridor','E5':'corridor'}
LOC={'P1':'front','P2':'front','P3':'front','P4':'front','P5':'hall','P6':'dining','P7':'dining','P8':'dining','P9':'front','P10':'hall','P11':'hall','P12':'bed13','P13':'kitchen',
     'E1':'front','E2':'front','E3':'dining','E4':'hall','E5':'hall'}
SUB={'P1':('고갯길, 우편 마차 안','첫날 오후'),'P2':('마을 입구, 광장','첫날 저녁'),'P3':('여관 현관','첫날 저녁'),'P4':('여관 접수대','첫날 저녁'),'P5':('2층 복도','첫날 저녁'),
 'P6':('여관 식당','첫날 저녁'),'P7':('식당 창가 자리','첫날 저녁'),'P8':('식당 안쪽, 부엌문 앞','첫날 저녁'),'P9':('여관 현관','첫날 밤 9시'),'P10':('부녀의 방','첫날 한밤'),
 'P11':('2층 복도','다음 날 아침 7시'),'P12':('2층 창고 앞','아침 7시 반'),'P13':('부엌','아침 7시 반'),
 'E1':('여관 앞','정오'),'E2':('여관 앞, 우편 마차','정오'),'E3':('식당','오후'),'E4':('할머니 방 앞','밤'),'E5':('2층 복도','다음 날 저녁')}
def scene(id_,extra_pre=None):
    s=SC[id_];items=conv(s,'play')
    pre=extra_pre or []
    body=emit(items,'play')
    who=None
    for it in items:
        if it[0]=='dir' and it[1].get('who') not in(None,'none'):who=it[1]['who'];break
    title,sub=SUB[id_]
    after=',"title"' if id_=='P5' else ''
    return '  /* %s %s */\n  B(%s,%s,S(%s,%s,%s,[%s%s\n   %s]%s))'%(id_,s['title'],js(BG[id_]),js(who),js(LOC[id_]),js(title),js(sub),''.join(p+',' for p in pre),'' ,body,after)
PRE={'P1':[],'P3':['D({sfx:"knock",ms:650})','D({sfx:"doorOpen",ms:550})','D({sfx:"door",ms:450})'],'P5':['D({sfx:"steps",ms:450})'],
     'P9':['D({sfx:"doorOpen",ms:500})','D({sfx:"door",ms:350})'],'P2':[],'P13':['D({sfx:"steps",ms:450})'],'P11':['{sfx:"slam"}'],'P4':[],'P6':[],'E2':[]}
pro=[scene('P%d'%i,PRE.get('P%d'%i)) for i in range(1,14)]
# P9: 문 소리는 세련 등장 전
end=[scene('E%d'%i) for i in range(1,6)]
head=''' /* ---- 프롤로그 P1~P13 (2026-10-09 장면 대본 JSON에서 생성: gen/conv.py) ----
    I(속마음[,무대,첫진입만]) / L(화자,대사,"",표정) / N(회색 지문: 대체 그림이 없는 사실만) / D({who,sfx,ms,chime}) 글자 없는 연출 */
 function I(t,cue,entry){var x="("+t+")";if(cue)(window.__INNCUE=window.__INNCUE||{})[x]=cue;if(entry)(window.__INNENTRY=window.__INNENTRY||{})[x]=1;return ["narr",x]}
 function B(bg,who,s){s.bg=bg;s.who=who;return s}
 function D(o){return {dir:o}}
 function FL(w,t,f){return f?[w,t,"","","","",f]:[w,t]}
 window.__INNFL=FL;
'''
body=' EP.PRO=[\n'+',\n'.join(pro)+'\n ];\n'
pro_js=head+body.replace('L(','FL(').replace('FL("@','L("@')
open('/home/claude/daae/stage/pro_new.js','w').write(pro_js)
# 후일담·회의 직전
r0=conv(SC['R0'],'play')
end_js=' var FL=window.__INNFL;\n /* ---- 후일담 E1~E5 · 회의 직전 R0 (장면 대본 JSON에서 생성) ---- */\n EP.END=[\n'+',\n'.join(end).replace('L(','FL(')+'\n ];\n EP.THE_END={banner:["1장 끝","열세 번째 침대"],notice:{title:"1장 끝 · 열세 번째 침대",text:"다람탐정 1장을 마쳤어요."}};\n'
end_js+=' EP.I9=[{loc:"dining"},\n   '+emit(r0,'play').replace('L(','FL(')+'];\n'
# 조사 대사 덮어쓰기
SPOT={'I01':('bed13','spots','bag'),'I02':('bed13','spots','quilt'),'I03':('bed13','spots','ledger'),'I04':('bed13','obs','o_inn_box'),'I05':('bed13','obs','o_inn_head'),'I06':('bed13','obs','o_inn_head2'),
 'I07':('kitchen','spots','basket'),'I08':('kitchen','spots','fur'),'I09':('hall','spots','clock'),'I10':('dotoroom','spots','diary'),'I11':('front','spots','book')}
ov=[' /* ---- 조사·질문 대사 (장면 대본 JSON에서 생성) ---- */',' function FIND(loc,kind,id){var l=EP.LOCS.filter(function(x){return x.id===loc})[0];return l&&(l[kind]||[]).filter(function(x){return x.id===id})[0]}']
for sid,(loc,kind,id_) in SPOT.items():
    items=conv(SC[sid],'say')
    if sid=='I04':items.append(('dir',{'who':'none','sfx':'steps','ms':380},False))
    if sid=='I06':items.append(('inner','(열한 번째 달 둘째 날. 네 자리 숫자로 옮기면 될까.)',False,''))
    ov.append(' (function(){var x=FIND(%s,%s,%s);if(x)x.say=[%s];})();'%(js(loc),js(kind),js(id_),emit(items,'say').replace('L(','FL(').replace('FL("@','L("@')))
# 자물쇠 열림
ov.append(' EP.LOCK.open=[L("@dir","sfx:lock;ms:500")];')
# 질문: 장면별로 질문 단위 분리
def talk(sid):
    s=SC[sid];groups={};order=[];entry=None
    for l in s['lines']:
        c=l.get('condition') or ''
        if c.startswith('이 장소에 새로') and l['type']=='속마음':entry=l['text'];continue
        if c.startswith('첫 진입 또는'):continue
        g=c[len('질문 선택 '):] if c.startswith('질문 선택') else '_first'
        groups.setdefault(g,[]).append(l)
        if g not in order:order.append(g)
    return entry,order,groups
def tlines(ls):
    sub={'scenes':[]};fake={'lines':ls}
    return emit(conv(fake,'say'),'say').replace('L(','FL(').replace('FL("@','L("@')
TMAP={'I13':('innma',{'_first':'T_ma1','어젯밤 할머니는':'T_ma2','세련에 대해':'T_ma3'}),
      'I14':('seryeon',{'_first':'T_se1','어젯밤 무엇을 했나':'T_se2','이 여관에 와 본 적은 → C12':'C12'}),
      'I15':('nabi',{'_first':'C03','열세 번째 침대에 대해':'T_na2','할머니에 대해':'T_na3'}),
      'I16':('geokkuri',{'_first':'C13'})}
for sid,(who,mp) in TMAP.items():
    entry,order,groups=talk(sid)
    ov.append(' (window.__INNTALKENTRY=window.__INNTALKENTRY||{})[%s]=%s;'%(js(who),js(entry)))
    for g in order:
        tid=mp.get(g)
        if not tid:print('미대응',sid,g);continue
        ls=[l for l in groups[g] if not (l['type']=='연출' and '획득' in l['text'])]
        ov.append(' (function(){var t=EP.TALK[%s].filter(function(x){return x.id===%s})[0];if(t)t.lines=[%s].concat(t.__follow||[]);})();'%(js(who),js(tid),tlines(ls)))
open('/home/claude/daae/stage/gen/end_gen.js','w').write(end_js+'\n'.join(ov)+'\n')
print('ok')
