"""1부 클릭 연결을 정적으로 추출한다. 실행·도달 가능성·재미를 통과 판정하지 않는다."""
from __future__ import annotations
import argparse, ast, collections, csv, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
OUT=ROOT/'docs/reviews/review146'
RID=re.compile(r'MS14_D(\d\d)_[A-Z0-9]+_L\d+(?:_O\d+)?')
LABEL=re.compile(r'^label ([A-Za-z_]\w*)(?:\([^\n]*\))?:',re.M)
WAIT=re.compile(r"call r13_v111_wait\(['\"]([^'\"]+)['\"]\)")
SOURCE_FILES=tuple(sorted(p for p in GAME.rglob('*.rpy') if 'qa_tests' not in p.parts))

def read_json(path):return json.loads(path.read_text())
def rel(path):return str(path.relative_to(ROOT))
def literal(text):
    try:return ast.literal_eval(text)
    except (ValueError,SyntaxError):return None

def split_args(text):
    """문자열·괄호 안의 쉼표를 보존한다. Ren'Py 행동식은 실행하지 않는다."""
    out=[];start=0;depth=0;quote=None;escaped=False
    for i,ch in enumerate(text):
        if quote:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch==quote:quote=None
        elif ch in "\"'":quote=ch
        elif ch in '([{':depth+=1
        elif ch in ')]}':depth-=1
        elif ch==',' and depth==0:out.append(text[start:i].strip());start=i+1
    out.append(text[start:].strip())
    return out

def call_inside(text,name):
    start=text.find(name+'(')
    if start<0:return None
    start+=len(name)+1;depth=1;quote=None;escaped=False
    for i in range(start,len(text)):
        ch=text[i]
        if quote:
            if escaped:escaped=False
            elif ch=='\\':escaped=True
            elif ch==quote:quote=None
        elif ch in "\"'":quote=ch
        elif ch=='(':depth+=1
        elif ch==')':
            depth-=1
            if depth==0:return text[start:i]
    return None

def sources():
    labels={};screens={}
    for path in SOURCE_FILES:
        text=path.read_text();matches=list(LABEL.finditer(text));day=None
        if path.name=='room13_v111_days123.rpy':day=1
        elif path.name=='room13_v111_days45.rpy':day=4
        elif path.name=='room13_v111_days610.rpy':day=6
        elif path.name=='room13_v111_days1114.rpy':day=11
        for n,m in enumerate(matches):
            block=text[m.start():matches[n+1].start() if n+1<len(matches) else len(text)]
            trailing=re.search(r'\n(?=init\b|screen\b|default\b|transform\b|style\b)',block)
            if trailing:block=block[:trailing.start()]
            scene=re.search(r"r13_v111_scene\(['\"]MS14_D(\d\d)_",block)
            change=re.search(r"r13_v111_set\(['\"]day['\"],\s*(\d+)\)",block)
            strong=int(change[1]) if change else int(scene[1]) if scene else None
            record_days=[int(d) for d in re.findall(r"r13_v111_lines\(\[\s*['\"]MS14_D(\d\d)_",block)]
            if strong is None and record_days:strong=record_days[0]
            if strong is not None:day=strong
            named=re.fullmatch(r'r13_v111_(?:day|morning)(\d+)',m[1])
            if named:day=strong=int(named[1])
            top=[l.strip() for l in block.splitlines()[1:] if l.startswith('    ') and not l.startswith('     ') and l.strip() and not l.lstrip().startswith('#')]
            fallthrough=matches[n+1][1] if n+1<len(matches) and not (top and (top[-1].startswith('jump ') or top[-1].startswith('return'))) else None
            labels[m[1]]=dict(name=m[1],source=rel(path),line=text.count('\n',0,m.start())+1,text=block,context_day=strong,day_hint=day,fallthrough=fallthrough)
        matches=list(re.finditer(r'^screen ([A-Za-z_]\w*)[^\n]*:',text,re.M))
        for n,m in enumerate(matches):
            end=matches[n+1].start() if n+1<len(matches) else len(text)
            # 다음 최상위 선언을 화면 본문으로 포함하지 않는다.
            tail=text[m.end():end]
            stop=re.search(r'\n(?=init\b|label\b|default\b|transform\b|style\b)',tail)
            if stop:end=m.end()+stop.start()
            header=text[m.start():m.end()]
            inside=header[header.find('(')+1:header.rfind(')')] if '(' in header else ''
            screens[m[1]]=dict(name=m[1],source=rel(path),line=text.count('\n',0,m.start())+1,text=text[m.start():end],params=[v.split('=',1)[0].strip() for v in split_args(inside) if v])
    # 명시 날짜가 없는 보조 라벨은 호출자와 순차 진입으로 날짜를 전파한다. 날짜 전환 목적지는 자체 날짜를 우선한다.
    for row in labels.values():
        targets=set(re.findall(r'^\s*(?:call|jump)\s+(r13_\w+)',row['text'],re.M))
        targets.update(re.findall(r"['\"](r13_\w+)['\"]",row['text']))
        if row.get('fallthrough'):targets.add(row['fallthrough'])
        row['targets']=sorted(t for t in targets if t in labels)
        row['days']=set([row['context_day']]) if row['context_day'] else set()
    for _ in range(len(labels)+1):
        changed=False
        for row in labels.values():
            for key in row['targets']:
                target=labels[key]
                if target['context_day']:continue
                prev=len(target['days']);target['days'].update(row['days']);changed|=len(target['days'])!=prev
        if not changed:break
    for row in labels.values():
        row['day_source']='명시 날짜 또는 호출/순차 진입 전파' if row['days'] else '파일 문맥 보조 추정'
        if not row['days'] and row['day_hint']:row['days'].add(row['day_hint'])
    return labels,screens

def overlays():
    rows={};blocks={};titles={}
    for path in sorted((GAME/'v111/newworld').glob('*.json')):
        data=read_json(path)
        rows.update({k:dict(value=v,source=rel(path)) for k,v in data.get('replace',{}).items()})
        blocks.update({k:dict(rows=v,source=rel(path)) for k,v in data.get('blocks',{}).items()})
        for gate,opts in data.get('titles',{}).items():titles.setdefault(gate,{}).update(opts)
    return rows,blocks,titles

def packet_excerpt(rid,records,replace):
    row=records.get(rid,{});over=replace.get(rid,{})
    if isinstance(over.get('value'),list):variants=over['value']
    else:variants=[over.get('value',{})]
    return dict(id=rid,speaker=row.get('speaker'),base_kind=row.get('kind'),
                variants=[dict(text=v.get('text',row.get('text')),when=v.get('when')) for v in variants],
                source=over.get('source','game/v111/records.json'),requires=row.get('requires',[]))

def first_packets(text,labels,records,replace,blocks,seen=()):
    for line in text.splitlines():
        inside=call_inside(line,'r13_lines')
        if inside:
            args=split_args(inside);direct=literal(args[0]) if args else None
            if isinstance(direct,list) and direct and all(isinstance(p,(tuple,list)) and len(p)>=2 for p in direct):
                return dict(method='명시 인라인 대사 재생 후보',packets=[dict(speaker=p[0],text=p[1]) for p in direct[:2]])
        inside=call_inside(line,'r13_v111_proof')
        if inside:
            return dict(method='자료 대조 화면에서 플레이어 입력 대기',proof=literal(split_args(inside)[0]),packets=[])
        m=re.search(r'call r13_lines\(r13_v111_lines\((\[[^\n]*?\])\)',line)
        if m:
            ids=literal(m[1]) or []
            return dict(method='첫 명시 record 재생 후보',packets=[packet_excerpt(i,records,replace) for i in ids[:2]])
        m=re.search(r"call r13_lines\(r13_nw_block\(['\"]([^'\"]+)['\"]\)",line)
        if m:
            b=blocks.get(m[1],{})
            return dict(method='첫 명시 block 재생 후보',block=m[1],source=b.get('source'),packets=b.get('rows',[])[:2])
        m=re.match(r'\s*(?:jump|call)\s+(r13_\w+)',line)
        if m and m[1] in labels and m[1] not in seen and len(seen)<4 and m[1] not in ('r13_v111_wait','r13_v111_travel'):
            out=first_packets(labels[m[1]]['text'],labels,records,replace,blocks,seen+(m[1],))
            if out.get('packets') or out.get('proof'):return dict(out,via=[m[1]]+out.get('via',[]))
    if re.search(r'^\s*return\b',text,re.M):return dict(method='상위 호출자로 복귀. 후속 진행은 호출자 조건에 따름',packets=[])
    return dict(method='정적으로 최초 대사를 특정하지 못함',packets=[])

def option_branch(after,index):
    lines=after.splitlines();matches=[]
    for n,line in enumerate(lines):
        m=re.match(r'^(\s*)if\s+(?:v111_answer|_return)\s*==\s*(-?\d+)\s*:',line)
        if not m or int(m[2])!=index:continue
        indent=len(m[1]);end=n+1
        while end<len(lines) and (not lines[end].strip() or len(lines[end])-len(lines[end].lstrip())>indent):end+=1
        matches.append('\n'.join(lines[n+1:end]))
    return '\n'.join(matches) if matches else after

def object_path(node):
    if isinstance(node,ast.Name):return [node.id]
    if isinstance(node,ast.Subscript):
        prefix=object_path(node.value)
        value=node.slice.value if isinstance(node.slice,ast.Constant) else None
        return prefix+[value] if prefix else []
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='setdefault':
        prefix=object_path(node.func.value)
        value=node.args[0].value if node.args and isinstance(node.args[0],ast.Constant) else None
        return prefix+[value] if prefix else []
    return []

def object_definitions(bindings):
    out=[];known=read_json(GAME/'room13-content.json')['objects']
    selected={(o.get('location') or b.get('location'),o.get('object')) for b in bindings.values() for o in b.get('options',[]) if o.get('object')}
    for place,items in known.items():
        for key,spec in items.items():
            out.append(dict(location=place,key=key,source='game/room13-content.json',origin='기초 데이터',text=spec.get('text'),special=spec.get('special'),give=spec.get('give',[]),flags=spec.get('flags',[])))
    for path in SOURCE_FILES:
        source=path.read_text()
        for block in re.finditer(r'^init[^\n]* python:\n([\s\S]*?)(?=^\S|\Z)',source,re.M):
            import textwrap
            try:tree=ast.parse(textwrap.dedent(block[1]))
            except SyntaxError:continue
            offset=source.count('\n',0,block.start(1))
            for node in ast.walk(tree):
                if not isinstance(node,ast.Assign):continue
                for target in node.targets:
                    parts=object_path(target)
                    if parts[:2]!=['ROOM13','objects'] or len(parts)<4:continue
                    value=node.value;fields={}
                    if isinstance(value,ast.Call) and isinstance(value.func,ast.Name) and value.func.id=='dict':
                        fields={kw.arg:literal(ast.unparse(kw.value)) for kw in value.keywords if kw.arg in ('text','special','give','flags')}
                    elif isinstance(value,ast.Dict):
                        fields={literal(ast.unparse(k)):literal(ast.unparse(v)) for k,v in zip(value.keys,value.values) if k is not None}
                    elif len(parts)==5 and parts[4]=='text':fields={'text':literal(ast.unparse(value))}
                    if isinstance(fields.get('text'),str):out.append(dict(location=parts[2],key=parts[3],source=rel(path),line=offset+node.lineno,origin='런타임 등록의 정적 문자열',**{k:fields.get(k) for k in ('text','special','give','flags')}))
    plain_path=GAME/'systems/room13_field_click146.rpy';plain={}
    if plain_path.exists():
        m=re.search(r'R13_FIELD_PLAIN_OBSERVATIONS146=(\{.*?\n    \})',plain_path.read_text(),re.S)
        if m:plain=literal(m[1]) or {}
    for row in out:
        text=row.get('text') or '';row['noun_like']=bool(text and len(text.split())<=8 and len(text)<=60 and not any(c in text for c in '.?!。！？'))
        row['has_authored_binding']=(row['location'],row['key']) in selected
        row['runtime_verified']=False
        row['output_mode']='raw_definition_not_final_output'
        row['route_class']='선택 대기에서 직접 처리되는 대상 있음' if row['has_authored_binding'] else '비진행 관찰 또는 숨김 조건의 런타임 검증 필요'
        if (row['location'],row['key']) in (('room13','books'),('kitchen','shelf'),('passage','handle')):
            row['route_class']='레거시 비밀 통로 필터 있음. 일반 1부 실제 노출 미확인'
        if (row['location'],row['key'])==('room13','family_bundle'):row['route_class']='본편 E30 기록/선택 대기 우선. 명사구 원문이 곧 출력문이라는 뜻 아님'
        pair=(row['location'],row['key'])
        if pair in plain:
            row['fallback_literal']=plain[pair];row['output_mode']='selected_literal_or_safe_hidden'
            row['fallback_policy']='원래 가시성 조건 통과 시 중립 관찰. 조건 미충족 시 None. 본편 기록/선택 대기 우선'
        elif row.get('special') or row.get('give') or row.get('flags'):
            row['fallback_policy']='본편 기록/선택 대기에 없으면 레거시 상태 지급 관찰은 None으로 숨김'
        row['limitation']='기초 데이터와 런타임 등록을 합성 실행하지 않은 원문 목록. 새 등록이 앞 등록을 대체할 수 있음'
    return out

def sidequest_controls():
    """146 선택 의뢰의 화면 문구와 상태별 재생 블록. 조건을 평가하지 않는다."""
    path=GAME/'v111/sidequests146.json'
    if not path.exists():return []
    out=[]
    for key,spec in read_json(path).get('quests',{}).items():
        context=dict(quest=key,quest_title=spec['title'],person=spec['owner'],
            location=spec['work_place'],object=spec['object'],source=rel(path),days=list(range(2,8)),
            offer_days=spec['offer_days'],guards=['평온한 재방문 가능 상태','주인 생존·미이탈·비업무중','대면 선택은 현장 재실','본편의 같은 물건 선택이 우선'],
            route_class='조건과 저장 상태로 선택되는 동적 대사',runtime_verified=False)
        def add(action,title,phase,status,**extra):
            variants=[]
            for p in phase:
                variants.append(dict(phase=p,lines=spec['blocks'].get(p,[])))
            out.append(dict(context,kind='sidequest_control',action=action,title=title,status=status,
                dialogue_variants=variants,**extra))
        add('offer',spec['offer_title'],['offer'],'unseen/declined/deferred. 수락 창 2~5일')
        for action in ('accept','decline','defer'):
            add(action,spec[action+'_title'],[action],'offer 선택 후',cancel_behavior='offer 화면 취소는 defer로 처리' if action=='defer' else None)
        add('status',spec.get('status_title','어디부터 손대면 될까요?'),['reminder'],'accepted')
        add('report',spec.get('report_title','부탁하신 일을 마쳤습니다.'),['report_'+c['result'] for c in spec['choices']],'worked')
        add('done',spec.get('done_title','그 뒤로 좀 괜찮으세요?'),['done']+(['done_tight'] if 'done_tight' in spec['blocks'] else []),'done')
        add('close',spec.get('close_title','그때 부탁하신 일은 어떻게 됐습니까?'),['passed'],'declined/deferred/passed. 6~7일')
        add('work_confirm_yes',spec['work_title'],[],'accepted',message=spec['work_message'],next='작업 방식 선택')
        add('work_confirm_no','그냥 살펴본다',[],'accepted',next='False 반환 후 호출자의 일반 조사 흐름',route_effect='의뢰 상태 변경 없음')
        for choice in spec['choices']:
            add('work_'+choice['result'],choice['title'],['work_'+choice['result']],'accepted',result=choice['result'],next='worked. 주인에게 결과 보고')
    return out

def script_menu_calls(labels):
    """화면 정의 밖의 메뉴/확인창 호출을 놓치지 않는다. 동적 목록은 식을 보존한다."""
    rows=[]
    for name,row in labels.items():
        days=[d for d in row['days'] if 1<=d<=7]
        if not days:continue
        for n,line in enumerate(row['text'].splitlines()):
            context=dict(label=name,source=row['source'],line=row['line']+n,days=sorted(days),runtime_verified=False)
            inside=call_inside(line,'renpy.display_menu')
            if inside is not None:
                args=split_args(inside);value=literal(args[0]) if args else None
                options=[dict(title=p[0],value=p[1],selectable=p[1] is not None) for p in value if isinstance(p,(tuple,list)) and len(p)>=2] if isinstance(value,list) else None
                rows.append(dict(context,kind='script_menu_call',menu_type='display_menu',expression=inside,options=options,
                    route_class='명시 선택지 목록' if options is not None else '호출 시 구성되는 동적 선택지 목록',
                    limitation='메뉴를 여는 호출의 원문. 메뉴 전 지역 변수와 if 결과를 평가하지 않아 출력·복귀 경로를 확정하지 않음'))
            if 'call screen r13_confirm(' in line:
                inside=call_inside(line,'r13_confirm');args=split_args(inside)
                rows.append(dict(context,kind='script_menu_call',menu_type='confirm',expression=inside,
                    message_expression=args[0] if args else '',options=[dict(title_expression=args[i],title_literal=literal(args[i]),value=bool(2-i)) for i in (1,2) if len(args)>i],
                    route_class='확인(True)/취소(False)를 상위 호출자로 반환',limitation='실제 입력·상위 조건 분기는 런타임 검증 필요'))
    return rows

def resident_controls():
    path=GAME/'v111/resident-dialogue.json'
    if not path.exists():return []
    rows=[]
    for person,spec in read_json(path).get('people',{}).items():
        common=dict(kind='resident_control',person=person,name=spec['name'],source=rel(path),
            guards=['생사·현장 재실·일과·동행·본편 장소·연출 중 여부 등 실행 시 조건'],runtime_verified=False,
            availability_query='r13_v111_resident_talk_available('+repr(person)+')',
            dynamic_query='r13_v111_resident_topics('+repr(person)+')',
            query_evaluated=False,
            condition_sources=['r13_v111_resident_talk_available','r13_v111_resident_talk_context','r13_v111_resident_catalogue_topics'],
            route_class='주민별 명시 대사. 표시 조건은 실행 시 평가')
        for topic in spec.get('topics',[]):
            first,last=topic['days']
            rows.append(dict(common,id='resident146:'+person+':'+topic['id'],title=topic['title'],days=list(range(first,last+1)),catalogue_kind='ordinary',query_kind='ordinary_day_range_or_next_day_work',
                selection_query='현재 날짜가 topics.days 안이고 context가 없음'+(' 또는 piko_after 다음 날(4일 이후)/화재 반응 다음 날(7일)에 work만 함께 표시' if topic['id']=='work' else ''),
                lines=topic['lines'],context='일반 상태. 생활 질문 1개와 시기별 질문 1개. 사건 다음 날에는 work만 사건 반응에 다시 붙을 수 있음'))
        urgent=spec.get('urgent')
        if urgent:rows.append(dict(common,id='resident146:'+person+':urgent_CONTEXT',title=urgent['title'],days=list(range(1,8)),catalogue_kind='urgent',query_kind='context_fallback_with_busy_override',
            selection_query='r13_v111_resident_talk_context(person)이 참이고 entry.reactions[context]가 없으면 urgent를 사용',
            dynamic_override='busy가 daram_guard/school_transport/family_walk/medical_call이면 제목·두 발화를 현재 맡은 돌봄/이송의 동적 응답으로 교체. runtime_condition_sources에 원문 보존',
            lines=urgent['lines'],context='fire/piko/event/busy 등의 문맥에서 전용 reaction이 없는 경우의 기본 짧은 응답'))
        for context,reaction in spec.get('reactions',{}).items():
            conditions={
                'piko_after':['3<=day<=7','person in (nabi,buri)','piko_alive is False','V111:E09 소유','piko_news3:person이 참'],
                'fire_safe':['6<=day<=7','D06_S03P_empty_fire_completed is True','warehouse_children_school_handover==4','KKOMI_ALIVE is True'],
                'fire_lost':['6<=day<=7','D06_S03_main_completed is True','warehouse_children_rescued==3','KKOMI_ALIVE is False'],
            }.get(context,['소스의 문맥 선택 조건 확인 필요'])
            rows.append(dict(common,id='resident146:'+person+':urgent_'+context,title=reaction['title'],days=list(range(3 if context=='piko_after' else 6,8)),catalogue_kind='reaction',query_kind='known_event_result_context',
                reaction_context=context,selection_query=('r13_v111_resident_talk_context('+repr(person)+') == '+repr(context)
                    + (' 또는 7일 화재 후속 문맥이며 r13_v111_resident_piko_heard(person)가 참' if context=='piko_after' else '')),
                context_conditions=conditions,priority='fire 현장→긴급 장면(piko/event)→busy→fire_safe/fire_lost→piko_after 순서. 실제 인계가 끝난 7일 자유 오후는 S02 장면 번호를 유지해도 긴급에서 제외하며, 화재 후속과 실제 들은 피코 소식은 함께 표시.',
                lines=reaction['lines'],context='확인한 사건 결과·전해 들은 소식에 따른 전용 응답. 다음 날에는 work 질문도 함께 표시 가능'))
    return rows

def runtime_condition_sources():
    """조건을 실행하지 않고, 목록의 query가 실제로 정의된 소스 함수를 연결한다."""
    requests={
        'game/systems/room13_v111_resident_talk.rpy':['r13_v111_resident_talk_available','r13_v111_resident_talk_context','r13_v111_resident_piko_heard','r13_v111_resident_catalogue_topics','r13_v111_required_business'],
        'game/room13_v111_idle.rpy':['r13_v111_tense_context'],
        'game/room13_v111.rpy':['r13_v111_free7_ready','r13_v111_revisit_allowed'],
        'game/room13_piko_reactions.rpy':['r13_piko_required_business','r13_piko_report_due'],
        'game/room13_v111_reactions.rpy':['r13_reaction_day_ok','r13_v111_followups','r13_v111_followup_display','r13_v111_present_reaction'],
    }
    out={}
    for source,names in requests.items():
        text=(ROOT/source).read_text()
        for name in names:
            m=re.search(r'^    def '+re.escape(name)+r'\([^\n]*\):\n([\s\S]*?)(?=^    (?:def |[A-Za-z_]\w*\s*=)|^\S|\Z)',text,re.M)
            if m:out[name]=dict(source=source,line=text.count('\n',0,m.start())+1,source_text=m[0].rstrip(),runtime_evaluated=False)
    return out

def build():
    data=read_json(GAME/'v111/records.json');bindings=read_json(GAME/'v111/field-bindings.json')
    labels,screens=sources();replace,blocks,titles=overlays();waiters=collections.defaultdict(list)
    for label,row in labels.items():
        for m in WAIT.finditer(row['text']):
            waiters[m[1]].append(dict(label=label,source=row['source'],line=row['line']+row['text'].count('\n',0,m.start()),days=sorted(row['days']),after=row['text'][m.end():]))
    rows=[];later=[];compat=[]
    for gate,b in bindings.items():
        calls=waiters.get(gate,[]);days=sorted({d for call in calls for d in call['days']})
        if not calls:
            compat.append(dict(gate=gate,source='game/v111/field-bindings.json',reason='직접 대기 호출 없음. 호환 데이터 또는 별도 동적 경로 여부 확인 필요',options=len(b.get('options',[]))))
            continue
        if not any(1<=d<=7 for d in days):later.append(dict(gate=gate,days=days));continue
        for position,opt in enumerate(b.get('options',[])):
            index=opt.get('index',position);dialogues=[]
            for call in calls:
                if not any(1<=d<=7 for d in call['days']):continue
                branch=option_branch(call['after'],index)
                dialogues.append(dict(label=call['label'],source=call['source'],line=call['line'],days=[d for d in call['days'] if 1<=d<=7],
                    branch_preview=branch.strip().splitlines()[:5],dialogue=first_packets(branch,labels,data['records'],replace,blocks)))
            flags=[]
            if opt.get('person') and re.search(r'(?:한다|묻는다|살핀다|확인한다|고른다)$',titles.get(gate,{}).get(str(position),opt['title'])):flags.append('인물 선택 문구가 실제 발화인지 확인')
            rows.append(dict(kind='field_option',gate=gate,days=[d for d in days if 1<=d<=7],source='game/v111/field-bindings.json',
                position=position,index=index,title=titles.get(gate,{}).get(str(position),opt['title']),base_title=opt['title'],
                location=opt.get('location') or b.get('location'),target=opt.get('person') or opt.get('object') or opt.get('move'),
                action_type='person' if opt.get('person') else 'object' if opt.get('object') else 'move' if opt.get('move') else 'unknown',
                guards=opt.get('guard',[]),present=opt.get('present'),present_only=opt.get('present_only',False),
                routes=dialogues,review_flags=flags,runtime_verified=False,
                limitation='조건문 분기를 실행하지 않은 최초 재생 후보. 실제 표시·인물 위치·타이핑/취소·자료 획득 검사는 별도 필요'))
    # 본편 라벨이 여는 화면과 그 안에서 use 하는 공통 화면의 정적 참조 폐쇄.
    used=set()
    for row in labels.values():
        if any(1<=d<=7 for d in row['days']) and ('room13_v111' in row['source'] or row['name'] in ('r13_lines','r13_scene','r13_observe')):
            used.update(re.findall(r'call screen\s+(\w+)',row['text']))
    used.update(('r13_hub','r13_topics','r13_map','r13_confirm','r13_records','r13_more_tools','save','load','say','choice'))
    for _ in range(25):
        more=set()
        for name in used:
            if name in screens:more.update(re.findall(r'\buse\s+(\w+)',screens[name]['text']));more.update(re.findall(r'(?:Show|ShowMenu)\(["\x27](\w+)',screens[name]['text']))
        prev=len(used);used.update(more)
        if len(used)==prev:break
    controls=[]
    for name in sorted(used):
        if name not in screens:continue
        row=screens[name];ls=row['text'].splitlines()
        for n,line in enumerate(ls):
            caption=None;command=None;kind=None;control_id=None
            m=re.search(r'use\s+(r13_\w*(?:control|button)\w*)\((.*)\)',line)
            if m:
                args=split_args(m[2]);kind=m[1];params=screens.get(kind,{}).get('params',[])
                ci=next((i for i,v in enumerate(params) if v in ('caption','label','title','text')),0)
                ai=next((i for i,v in enumerate(params) if v in ('command','action','choose')),2)
                caption=args[ci] if len(args)>ci else '';command=args[ai] if len(args)>ai else ''
                control_id=next((v.split('=',1)[1] for v in args if v.startswith('control_id=')),None)
            elif re.match(r'\s*(?:textbutton|imagebutton|button)\b',line):
                kind=line.strip().split()[0].rstrip(':');rest=line.strip()[len(kind):].strip().rstrip(':')
                caption=re.split(r'\s+(?:action|style|xsize|ysize|text_size|text_font|sensitive|xpos|ypos)\s+',rest,1)[0]
                inline=re.search(r'\baction\s+(.+?)(?=\s+(?:sensitive|xsize|ysize|text_size|text_font|xpos|ypos)\s+|$)',rest)
                indent=len(line)-len(line.lstrip());body=[]
                for tail in ls[n+1:]:
                    if tail.strip() and len(tail)-len(tail.lstrip())<=indent:break
                    body.append(tail.strip())
                body_actions=[re.search(r'\baction\s+(.+?)(?=\s+(?:sensitive|selected|xsize|ysize|xysize|text_size|text_font|xpos|ypos|alt|hovered|unhovered)\s+|$)',v) for v in body]
                command=inline[1] if inline else next((m[1] for m in body_actions if m),None)
                control_id=next((v[3:] for v in body if v.startswith('id ')),None)
                if kind=='imagebutton':caption=next((v[4:].split(' action ',1)[0] for v in body if v.startswith('alt ')),caption)
            if kind:controls.append(dict(kind='screen_control',screen=name,source=row['source'],line=row['line']+n,control_kind=kind,caption_expression=caption,caption_literal=literal(caption),action_expression=command,control_id_expression=control_id,route_class='화면 조작·선택된 동적 처리' if command else '조건/포함 화면에서 동작을 받는지 직접 확인 필요',scope='1~7일/공통 화면의 정적 참조 후보',runtime_verified=False))
    reactions=read_json(GAME/'v111/newworld/reactions.json')
    followups=[dict(kind='followup',id=s['id'],person=s['person'],title=s['title'],days=s.get('days'),after=s['after'],after_meeting=s.get('after_meeting'),heard_in=s.get('heard_in',[]),piko_mourning=s.get('piko_mourning'),lines=s['lines'],source='game/v111/newworld/reactions.json',runtime_verified=False,
        selection_query='생존·미이탈·actor_ready, spec.person 일치, after 자료 소유, days 범위, after_meeting 지정 시 회의 결과가 None이 아님',
        variant_query='긴급 문맥 piko이고 piko_mourning 원문이 있으면 제목과 lines만 그 변형으로 표시',
        condition_sources=['r13_v111_followups','r13_reaction_day_ok','r13_v111_followup_display']) for s in reactions.get('followups',[]) if (s.get('days') or [1,14])[0]<=7]
    present=[dict(kind='evidence_response',person=s['person'],evidence=s['evidence'],days=s.get('days'),after_meeting=s.get('after_meeting'),lines=s['lines'],source='game/v111/newworld/reactions.json',runtime_verified=False,
        selection_query='대상 person 및 제시 evidence 일치, days 범위, after_meeting 지정 시 회의 결과가 None이 아님',
        condition_sources=['r13_v111_present_reaction','r13_reaction_day_ok']) for s in reactions.get('present',[]) if (s.get('days') or [1,14])[0]<=7]
    objects=object_definitions(bindings);sidequests=sidequest_controls();menus=script_menu_calls(labels);residents=resident_controls()
    for row in rows:row.update(route_class='원래 선택 index에 따른 동적 대사/화면 전환 후보',output_mode='selected_dynamic')
    for row in controls+sidequests+menus:row['output_mode']='selected_dynamic'
    for row in followups+present+residents:row.update(route_class='조건 통과 시 명시된 대사 목록 재생',output_mode='literal_after_dynamic_guard')
    files=list(SOURCE_FILES)+[GAME/'v111/records.json',GAME/'v111/field-bindings.json',GAME/'room13-content.json']+list((GAME/'v111/newworld').glob('*.json'))
    files+=[p for p in (GAME/'v111/sidequests146.json',GAME/'v111/resident-dialogue.json') if p.exists()]
    digest=hashlib.sha256()
    for path in sorted(files):digest.update(rel(path).encode());digest.update(path.read_bytes())
    counts={str(d):dict(field_options=sum(d in r['days'] for r in rows),gates=len({r['gate'] for r in rows if d in r['days']})) for d in range(1,8)}
    summary=dict(scope='1부 1~7일 정적 클릭·대사 연결 감사',date='2026-11-10',
        method='대기 호출의 소스 문맥 날짜, 선택지의 원래 index, 명시 분기, 최초 대사 후보와 화면 참조를 추출. 엔진 실행이나 전 경로 완주가 아님.',
        source_digest_sha256=digest.hexdigest(),
        counts=dict(field_options=len(rows),gates=len({r['gate'] for r in rows}),screen_controls=len(controls),screens=len({r['screen'] for r in controls}),followups=len(followups),evidence_responses=len(present),object_definitions=len(objects),noun_like_object_texts=sum(r['noun_like'] for r in objects),sidequest_controls=len(sidequests),script_menu_calls=len(menus),resident_controls=len(residents),resident_people=len({r['person'] for r in residents}),resident_ordinary_controls=sum(r['catalogue_kind']=='ordinary' for r in residents),resident_urgent_controls=sum(r['catalogue_kind']=='urgent' for r in residents),resident_reaction_controls=sum(r['catalogue_kind']=='reaction' for r in residents)),
        by_day=counts,compatibility_without_waiter=compat,later_gates_excluded=later,
        limits=['화면의 조건·스크롤·가림·키보드·실제 선택 성공은 정적 추출로 검증하지 않음','최초 대사 후보는 when/if 조건 평가 전이며 오답·대체 조합·되묻기·재시도 모두의 실제 출력과 같다고 단정하지 않음','일반 버튼은 대사 대신 지도/저장/자료창을 열거나 취소하는 역할도 있음','다른 작업자가 추가한 146 주민·퀘스트 콘텐츠는 통합 뒤 이 생성기를 다시 실행해 목록을 갱신해야 함'])
    return dict(summary=summary,field_options=rows,screen_controls=controls,followups=followups,evidence_responses=present,object_definitions=objects,sidequest_controls=sidequests,script_menu_calls=menus,resident_controls=residents,runtime_condition_sources=runtime_condition_sources())

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=OUT);args=p.parse_args();d=build();args.out.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(d,ensure_ascii=False,indent=2)
    (args.out/'버튼대사목록.json').write_text(raw+'\n')
    with (args.out/'버튼대사목록.tsv').open('w',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(('종류','날짜','화면/대기/의뢰','index/행동','대상','제목','위치','조건','연결/출처','실제 검증'))
        for r in d['field_options']:w.writerow((r['kind'],','.join(map(str,r['days'])),r['gate'],r['index'],r['target'],r['title'],r['location'],json.dumps(r['guards'],ensure_ascii=False),','.join(x['label'] for x in r['routes']),'미실행'))
        for r in d['screen_controls']:w.writerow((r['kind'],'공통',r['screen'],r['action_expression'],'',r['caption_literal'] or r['caption_expression'],'','조건식 평가 전',r['source']+':'+str(r['line']),'미실행'))
        for kind in ('followups','evidence_responses'):
            for r in d[kind]:w.writerow((r['kind'],str(r.get('days')),r.get('id','자료 제시'),r.get('evidence',''),r['person'],r.get('title','자료 반응'),'','조건식 평가 전',r['source'],'미실행'))
        for r in d['sidequest_controls']:w.writerow((r['kind'],','.join(map(str,r['days'])),r['quest'],r['action'],r['person'],r['title'],r['location'],r['status'],r['source'],'미실행'))
        for r in d['script_menu_calls']:w.writerow((r['kind'],','.join(map(str,r['days'])),r['label'],r['menu_type'],'',r['expression'],'',r['route_class'],r['source']+':'+str(r['line']),'미실행'))
        for r in d['resident_controls']:w.writerow((r['kind'],','.join(map(str,r['days'])),r['id'],r['catalogue_kind'],r['person'],r['title'],'',r['context']+' / '+r['selection_query'],r['source'],'미실행'))
    print(json.dumps(d['summary'],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
