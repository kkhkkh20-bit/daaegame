"""본편 집필 검토용 조건 분리 대사본. 게임 코드를 실행하거나 수정하지 않는다."""
import ast
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
GAME=ROOT/'game'
loader=importlib.util.spec_from_file_location('manuscript_story_master',ROOT/'dev/story_master.py')
sm=importlib.util.module_from_spec(loader);loader.loader.exec_module(sm)
INPUTS=set()
def read(path):
    path=Path(path);INPUTS.add(path);return path.read_text(encoding='utf-8')
def load(path):return json.loads(read(path))
def relative(path):return str(Path(path).relative_to(ROOT))
REC=load(GAME/'v111/records.json')['records']
OVERLAY_NAMES=[f'd{i:02d}' for i in range(1,15)]+['hidden_pandol','hidden_base','lamp_attempt']
MERGED={k:{} for k in ['replace','before','after','blocks','titles']};MERGED['drop']=[]
OWNERS={};patches={}
for name in OVERLAY_NAMES:
    p=GAME/'v111/newworld'/f'{name}.json';part=load(p);patches[name]=part
    for section in ['replace','before','after','blocks','titles']:
        for key,value in part.get(section,{}).items():
            assert key not in MERGED[section],(section,key)
            MERGED[section][key]=value;OWNERS[section,key]=p
    MERGED['drop']+=part.get('drop',[])
DROP=collections.defaultdict(list)
for item in MERGED['drop']:
    rid,when=(item,'always') if isinstance(item,str) else (item['id'],item.get('when','always'))
    DROP[rid].append(when)
NAMES={}
for name in ['room13_v111_source_cast.rpy','room13_v111_later_bindings.rpy']:
    text=read(GAME/name)
    for body in re.findall(r'MS14_SPEAKERS(?: = |\.update\()\{(.*?)\}',text,re.S):
        NAMES.update(dict(re.findall(r'"([^"]+)":"([a-z_0-9]+)"',body)))
BY_ID={v:k for k,v in NAMES.items()};BY_ID.update(dad='아빠',daram='다람',mom='엄마')
CARRIAGE=sm.literal_after(read(GAME/'room13_v111.rpy'),'R13_V111_CARRIAGE_TEXT =',GAME/'room13_v111.rpy') or {}
CONDITIONS=sm.parse_when(read(GAME/'room13_v111_newworld_text.rpy'))
SOURCES=[GAME/name for name in sm.DAY_FILES]
SOURCES += [p for p in GAME.glob('room13_v111*.rpy') if p not in SOURCES]
SOURCES += [p for p in (GAME/'systems').glob('room13_v111*.rpy') if p not in SOURCES]
CALLS=collections.defaultdict(list);BLOCK_CALLS=collections.defaultdict(list);GATES=collections.defaultdict(list)
LITERALS=collections.defaultdict(list);DYNAMIC=[];CONTROLS=collections.defaultdict(list)

def day_of(text):
    m=re.search(r'MS14_D(\d{2})_',text or '')
    if m:return int(m.group(1))
    nums=re.findall(r'(\d{1,2})(?:_|$)',text or '')
    return next((int(n) for n in reversed(nums) if 1<=int(n)<=14),None)

def contextualize(text):
    contexts=[];label='(공통 함수)';scene=None;conditions=[];function=''
    for number,raw in enumerate(text.splitlines(),1):
        s=raw.strip();ind=len(raw)-len(raw.lstrip())
        if s and not s.startswith('#'):
            while conditions and ind<=conditions[-1][0]:conditions.pop()
            m=re.match(r'label (\w+)',s)
            if m and ind==0:label=m[1];function=''
            m=re.match(r'def (\w+)',s)
            if m:function=m[1]
            m=re.search(r'r13_v111_scene\([\'"](MS14_[^\'"]+)',s)
            if m:scene=m[1]
            if re.match(r'(?:if |elif |else:|for |while )',s) and s.endswith(':'):
                conditions.append((ind,s[:-1]))
            elif (s.startswith(('"',"'")) and s.endswith(':')):
                conditions.append((ind,'선택 '+s[:-1]))
        inferred=day_of(label) or day_of(scene)
        contexts.append(dict(label=label,scene=scene,day=inferred,conditions=[x[1] for x in conditions],function=function,line=number))
    return contexts

def loc(path,ctx):
    route=ctx['label'] if ctx['label']!='(공통 함수)' else (ctx['function'] or '(공통)')
    suffix=' / '.join(ctx['conditions']) or '외부 조건은 호출 라벨 참조'
    return f'{relative(path)}:{ctx["line"]} | {route} | {suffix}'.rstrip()

def get_text(node):
    try:return ast.literal_eval(node)
    except (ValueError,TypeError,SyntaxError):return None

def inline_row(node,path,ctx,sequence):
    if isinstance(node,(ast.Tuple,ast.List)) and len(node.elts)>=2:
        who=get_text(node.elts[0]);text=get_text(node.elts[1])
        if isinstance(text,str):
            meta=get_text(node.elts[2]) if len(node.elts)>2 else {}
            meta=meta if isinstance(meta,dict) else {}
            return dict(id=f'(원문ID 없음: {relative(path)}:{ctx["line"]}, 항목 {sequence})',speaker=BY_ID.get(who,who),text=text,kind='thought' if meta.get('thought') else ('dialogue' if who else 'narration'))
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='r13_nw_added_line' and node.args:
        data=node.args[0]
        if isinstance(data,ast.Call) and isinstance(data.func,ast.Name) and data.func.id=='dict':
            fields={k.arg:get_text(k.value) for k in data.keywords}
            if isinstance(fields.get('text'),str):return dict(id=f'(원문ID 없음: {relative(path)}:{ctx["line"]}, 항목 {sequence})',**fields)
    return None

for path in SOURCES:
    text=read(path);contexts=contextualize(text)
    for i,raw in enumerate(text.splitlines()):
        s=raw.strip();ctx=contexts[i]
        if s.startswith(('if ','elif ','else:','menu:','jump ','return','call ')) and not s.startswith('call r13_lines'):
            CONTROLS[ctx['day']].append((loc(path,ctx),s))
    for m in re.finditer(r'\b(r13_v111_lines|r13_nw_block|r13_v111_wait|r13_lines)\s*\(',text):
        line=text.count('\n',0,m.start());ctx=contexts[line]
        prefix=text[text.rfind('\n',0,m.start())+1:m.start()]
        if prefix.lstrip().startswith('#') or prefix.rstrip().endswith('def'):continue
        body=sm.balanced(text,text.index('(',m.start()))
        if not body: DYNAMIC.append((loc(path,ctx),'호출 괄호 읽기 실패'));continue
        try:call=ast.parse(m[1]+body,mode='eval').body
        except SyntaxError:DYNAMIC.append((loc(path,ctx),m[1]+body[:180]));continue
        if not call.args:continue
        value=get_text(call.args[0]);name=m[1]
        if name=='r13_v111_lines':
            if isinstance(value,list) and all(isinstance(x,str) for x in value):
                for rid in value:CALLS[rid].append(loc(path,ctx))
            else:DYNAMIC.append((loc(path,ctx),'정본 ID 동적 식: '+ast.unparse(call.args[0])))
        elif name=='r13_nw_block':
            if isinstance(value,str):BLOCK_CALLS[value].append(loc(path,ctx))
            else:DYNAMIC.append((loc(path,ctx),'추가 블록 동적 식: '+ast.unparse(call.args[0])))
        elif name=='r13_v111_wait':
            if isinstance(value,str):GATES[value].append((ctx['day'],loc(path,ctx)))
            else:DYNAMIC.append((loc(path,ctx),'현장 질문 동적 식: '+ast.unparse(call.args[0])))
        elif isinstance(call.args[0],ast.List):
            rows=[]
            for n,node in enumerate(call.args[0].elts,1):
                row=inline_row(node,path,ctx,n)
                if row:rows.append(row)
                else:DYNAMIC.append((loc(path,ctx),'직접 대사 동적 식: '+ast.unparse(node)))
            if rows:LITERALS[ctx['day']].append((loc(path,ctx),rows))
        elif not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('r13_v111_lines','r13_nw_block') for n in ast.walk(call.args[0])):
            DYNAMIC.append((loc(path,ctx),'대사 꾸러미 동적 식: '+ast.unparse(call.args[0])))

# 예전 제작 문서의 장면 표제가 현행 각색과 다를 수 있어 제목은 실제 장면 ID만 쓴다.
SCENES={}
BINDINGS=load(GAME/'v111/field-bindings.json')
for key,titles in MERGED['titles'].items():
    for index,title in titles.items():BINDINGS[key]['options'][int(index)]['title']=title
STATS=collections.Counter()

def row_text(row,base=None,prefix=''):
    base=base or {};kind=row.get('kind',base.get('kind','dialogue'))
    who=row.get('speaker',base.get('speaker'))
    if kind=='thought':who=(who or '아빠')+'(생각)'
    elif not who:who={'evidence':'자료','choice':'선택지','system':'안내'}.get(kind,'지문')
    rid=row.get('id') or base.get('id') or '(ID 없음)'
    when=row.get('when','always');tags=[]
    if when!='always':tags.append('조건 '+when)
    for k,v in [('cut','컷'),('endcut','결말 컷'),('expression','표정')]:
        if row.get(k):tags.append(v+' '+str(row[k]))
    if kind in ('action','system'):tags.append('원본 종류 '+kind)
    text=row.get('text',base.get('text','')).replace('\r\n','\n')
    STATS['출력문장']+=1
    return f'{prefix}[{rid}] {who}'+(' {'+'; '.join(tags)+'}' if tags else '')+': '+text.replace('\n','\n    ')

lines=['다람탐정 기존 본편 1~14일 조건 분리 원문 대사본','작성 기준: 2026-11-05 작업 디렉터리 스냅샷. 게임에 반영된 개작본이 아니다.','',
'읽는 법','1. 이 파일은 한 번의 플레이를 재현한 소설이 아니다. 정본 ID 순서에 호출 라벨·분기를 표시한 집필 검토 원문이다.',
'2. 사망/생존·회의 승리/패배·예방/발생 줄을 이어 읽지 말고 호출 라벨과 조건 묶음별로 읽는다.',
'3. [조건 대체]의 여러 문장은 연속 대사가 아니다. 위에서부터 처음 참인 조건 하나만 실제 재생된다.',
'4. {w=...} 등 재생 태그와 원문 ID는 그대로 남긴다. 직접 쓴 대사에 원래 ID가 없으면 파일·줄·항목 번호로만 표시한다.',
'5. 실제 함수의 동적 계산, 상태 판정, 모든 점프 경로를 실행하지 않았다. 삭제·추가·분기와 미해석 호출의 목록을 함께 확인한다.',
'6. 일반 파일의 원문을 모은 자료이며, 실제 화면에 찍힌 1~3일 주행 대사본과 구별한다.','']
used=set()
for day in range(1,15):
    lines += ['\n'+'='*72,f'{day:02d}일차', '='*72]
    scene=None;last_route=None
    for rid,rec in REC.items():
        if not rid.startswith(f'MS14_D{day:02d}_') or rid not in CALLS:continue
        sid=rid.rsplit('_',1)[0]
        if sid!=scene:
            scene=sid;last_route=None;lines += ['',f'장면 {sid}']
        route=' / '.join(sorted({c.split(' | ')[1] for c in CALLS[rid]}))
        if route!=last_route:
            lines += ['',f'--- 호출 경로 묶음: {route} ---'];last_route=route
        for row in MERGED['before'].get(rid,[]):lines.append(row_text(row,prefix='앞에 추가 '))
        base=dict(rec,id=rid,text=CARRIAGE.get(rid,rec.get('text','')))
        drops=DROP.get(rid,[])
        if 'always' in drops:
            lines.append(f'[{rid}] 현재 표시 제외. 앞뒤 추가 줄은 별도로 재생될 수 있음.');STATS['무조건삭제']+=1
        else:
            if drops:lines.append('[원문 표시 조건: 다음 삭제 조건이 모두 거짓일 때만] '+', '.join(drops))
            variants=MERGED['replace'].get(rid)
            if variants:
                variants=[variants] if isinstance(variants,dict) else variants
                if len(variants)==1 and variants[0].get('when','always')=='always':lines.append(row_text(variants[0],base));STATS['교체원문']+=1
                else:
                    lines.append(f'[조건 대체 시작 {rid}: 다음 중 처음 맞는 한 줄만 선택]')
                    for order,v in enumerate(variants,1):
                        label=v.get('when','always')
                        lines.append(f'  대체 {order}: '+('앞의 조건들이 모두 아니면' if label=='always' else label))
                        lines.append(row_text(v,base,prefix='    '));STATS['조건대체문장']+=1
                    if not any(v.get('when','always')=='always' for v in variants):
                        lines.append('  어느 대체 조건도 아니면 원래 문장:');lines.append(row_text(base,prefix='    '))
                    lines.append('[조건 대체 끝]')
            else:lines.append(row_text(base))
        for row in MERGED['after'].get(rid,[]):lines.append(row_text(row,prefix='뒤에 추가 '))
        if rec.get('requires'):lines.append('  [원문 요구 조건] '+json.dumps(rec['requires'],ensure_ascii=False))
        used.add(rid)
    for name,rows in MERGED['blocks'].items():
        if OWNERS['blocks',name].stem!=f'd{day:02d}':continue
        lines += ['',f'--- 추가 블록 {name} ---','호출: '+(' / '.join(BLOCK_CALLS[name]) if BLOCK_CALLS[name] else '직접 문자열 호출 미확인: 간접 호출·보조 블록일 수 있음')]
        lines += [row_text(row) for row in rows];STATS['추가블록']+=1
    for origin,rows in LITERALS.get(day,[]):
        lines += ['', '--- 직접 작성 대사: '+origin+' ---'];lines += [row_text(row) for row in rows]
    gates=[(gate,refs) for gate,refs in GATES.items() if any(d==day for d,_ in refs)]
    if gates:lines += ['',f'--- {day:02d}일 현장 질문·보기(동적 필터·추가 보기 처리 전 등록문구) ---']
    for gate,refs in gates:
        lines.append('관문 '+gate+' | '+' / '.join(r for d,r in refs if d==day))
        for index,row in enumerate(BINDINGS.get(gate,{}).get('options',[])):
            lines.append(f'  원래 보기 {index} | {BY_ID.get(row.get("person"),row.get("person") or "현장")} | '+row.get('title','(제목 없음)')+(' | 조건 '+str(row['guard']) if row.get('guard') else ''))
    lines += ['',f'--- {day:02d}일 라벨·분기·이동 참고(실행한 경로가 아니라 소스에 있는 연결) ---']
    for origin,text in CONTROLS.get(day,[]):lines.append(origin+'\n  '+text)

lines += ['\n'+'='*72,'선택·예방·숨은 갈래의 추가 대사: 본편과 같은 17개 overlay 중 보충 3개','='*72]
for owner in ['hidden_pandol','hidden_base','lamp_attempt']:
    lines += ['', '보충 갈래 '+owner]
    for name,rows in MERGED['blocks'].items():
        if OWNERS['blocks',name].stem!=owner:continue
        lines += ['', '블록 '+name, '호출: '+(' / '.join(BLOCK_CALLS[name]) or '직접 문자열 호출 미확인: 간접 호출·보조 블록일 수 있음')]
        lines += [row_text(row) for row in rows];STATS['보충블록']+=1

lines += ['\n'+'='*72,'공통 인사·자료 반응·후속 질문: 각 날짜·보유 자료·읽음 상태에 따라 선택됨','='*72]
GREETINGS=load(GAME/'v111/newworld/greetings.json')
for person,rows in GREETINGS.items():
    lines += ['', '인물 '+BY_ID.get(person,person)+' | 실제 호출·긴장 상태는 idle 코드 참조']
    for i,row in enumerate(rows):
        if row.get('dad'):lines.append('(인사 자료: 원문ID 없음) 아빠: '+row['dad'])
        lines.append('(인사 자료: 원문ID 없음; 행 %s) %s: %s'%(i,BY_ID.get(person,person),row.get('text','')))
        if row.get('first'):lines.append('  [첫 대면 변형] '+row['first'])
REACTIONS=load(GAME/'v111/newworld/reactions.json')
for spec in REACTIONS['present']+REACTIONS['followups']:
    lines += ['', '반응/질문 '+str(spec.get('id') or (spec.get('person')+':'+spec.get('evidence','')))+' | 인물 '+BY_ID.get(spec.get('person'),str(spec.get('person')))+' | 날짜 '+str(spec.get('days'))+' | 보유 '+str(spec.get('after') or spec.get('evidence'))+(' | 회의 후 '+spec['after_meeting'] if spec.get('after_meeting') else '')]
    if spec.get('title'):lines.append('기본 질문 제목: '+spec['title'])
    if spec.get('piko_mourning'):lines.append('[다음 기본 줄은 피코 사망 직후 변형이 선택되지 않은 경우. 두 묶음을 이어 읽지 않음]')
    lines += [row_text(row) for row in spec['lines']]
    if spec.get('piko_mourning'):
        variant=spec['piko_mourning'];lines += ['[대체 분기: r13_v111_tense_context() == piko. 기본 묶음 대신 이 묶음만]','질문 제목: '+variant['title']]
        lines += [row_text(row) for row in variant['lines']]
for person,rows in REACTIONS['generic'].items():
    lines += ['', '관계없는 자료에 대한 기본 반응: '+BY_ID.get(person,person)+' | 실제 문맥 표정은 반응 코드 참조']
    lines += [row_text(dict(row,speaker=BY_ID.get(person,person),id='(원문ID 없음: generic '+person+')')) for row in rows]
for origin,rows in LITERALS.get(None,[]):
    lines += ['', '공통 직접 대사: '+origin];lines += [row_text(row) for row in rows]

lines += ['\n'+'='*72,'조건 이름과 현재 코드의 식: 상태를 평가하지 않은 참고표','='*72]
for name,expression in sorted(CONDITIONS.items()):lines.append(name+' = '+str(expression))
lines += ['\n'+'='*72,'미해석·부분 추출 호출: 실제 재생 문장으로 대신 쓰지 않았음','='*72]
for origin,text in sorted(set(DYNAMIC)):lines += [origin,'  '+text]
lines += ['', '범위 한계', '이 파일은 실제 재생 엔진을 실행하지 않았다. 같은 장면 안에도 서로 다른 라벨·선택·생사·승패가 있다.',
'정본 줄은 실제 문자 ID 호출이 확인된 줄만 본문에 수록했다. 호출되지 않는 관리/선택/옛 정본은 현재 대사로 섞지 않았다.',
'추가 블록은 17개 overlay 전부 수록하므로 간접 호출·예비 블록도 포함할 수 있다. 조건을 실행하거나 도달 가능성을 증명한 것은 아니다.',
'이동·인물·보유 자료·동적 질문 필터·자료 본문을 모두 재현하지 않는다. 식으로 생성되는 문구는 위 미해석 호출을 보완해야 한다.',
'공통 함수 내부의 상수 표·조건식에서 계산되는 말과 사용자 인터페이스 설명 전체를 완전 수록했다고 주장하지 않는다.',
'실제 한 경로 대사본은 별도 주행 기록을 기준으로 읽어야 하며, 이 원문을 소설처럼 처음부터 끝까지 이어 읽으면 안 된다.','']
raw='\n'.join(lines)
(OUT/'원문_1-14일_조건분리.txt').write_text(raw,encoding='utf-8')
clean=re.sub(r'\{/?(?:w(?:=[^}]*)?|b|i|color(?:=[^}]*)?|size(?:=[^}]*)?|alpha(?:=[^}]*)?)\}','',raw)
clean=clean.replace('4.  등 재생 태그와 원문 ID는 그대로 남긴다. 직접 쓴 대사에 원래 ID가 없으면 파일·줄·항목 번호로만 표시한다.','4. 원문 TXT는 재생 태그를 보존한다. 이 읽기본에서는 기다림·색·굵기 태그만 제거했고 원문 ID·문장은 유지한다. 직접 대사에 원래 ID가 없으면 파일·줄·항목 번호로 표시한다.')
clean='읽기본: 대사 문장을 개작하지 않고 재생용 기다림·색·굵기 태그만 숨겼다. 분기·원문 ID는 유지한다.\n\n'+clean
(OUT/'읽기본_1-14일_조건분리.txt').write_text(clean,encoding='utf-8')
manifest=dict(기준일='2026-11-05',기준커밋=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),추출상태='작업 디렉터리 스냅샷, 단일 경로 실행본 아님',overlay=OVERLAY_NAMES,정본직접호출줄=len(used),정본전체줄=len(REC),직접문자호출미확인정본=[k for k in REC if k not in used],집계=dict(STATS),동적미해석호출=len(set((a,b) for a,b in DYNAMIC)),입력파일={relative(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(INPUTS)})
(OUT/'추출정보.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:manifest[k] for k in ['정본직접호출줄','정본전체줄','집계','동적미해석호출']},ensure_ascii=False))
