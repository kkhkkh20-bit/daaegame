"""대사 모듈 build/check/apply. JSON 다운로드의 text/review_status만 되가져온다.

python3 dev/dialogue_modules.py build
python3 dev/dialogue_modules.py check 수정.json
python3 dev/dialogue_modules.py apply 수정.json --write
"""
from __future__ import annotations
import argparse,ast,copy,datetime,hashlib,io,json,os,re,subprocess,sys,tempfile,tokenize
import html as html_module
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA='room13.dialogue.v1'
EDIT_SCHEMA='room13.dialogue-edit.v1'
STATUSES={'draft','reviewed','needs_work'}
MUTABLE={'text','review_status'}
KOREAN=re.compile('[가-힣ㄱ-ㅎㅏ-ㅣ…]')

class ModuleError(ValueError):pass

def digest(value):
    return hashlib.sha256(value.encode('utf-8') if isinstance(value,str) else value).hexdigest()
def encode(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def pointer(path):return '/'+ '/'.join(str(k).replace('~','~0').replace('/','~1') for k in path)
def get_at(data,path):
    for k in path:data=data[k]
    return data

def closing(text,start):
    """Find one Python literal/call expression's closing bracket, skipping strings."""
    opener=text[start];pairs={'(':')','[':']','{':'}'};stack=[pairs[opener]];i=start+1
    while i<len(text):
        c=text[i]
        if c in "\"'":
            q=c*3 if text.startswith(c*3,i) else c;i+=len(q)
            while i<len(text):
                if text[i]=='\\':i+=2;continue
                if text.startswith(q,i):i+=len(q);break
                i+=1
            continue
        if c=='#':
            end=text.find('\n',i);i=len(text) if end<0 else end+1;continue
        if c in pairs:stack.append(pairs[c])
        elif c in ')]}':
            if not stack or c!=stack.pop():return None
            if not stack:return i+1
        i+=1
    return None

def ast_span(fragment,node,offset=0):
    lines=fragment.splitlines(keepends=True)
    def pos(line,col):
        # AST columns count UTF-8 bytes; stored spans count Python Unicode characters.
        return sum(len(x) for x in lines[:line-1])+len(lines[line-1].encode('utf-8')[:col].decode('utf-8'))+offset
    return [pos(node.lineno,node.col_offset),pos(node.end_lineno,node.end_col_offset)]

def scan_rpy(text,file):
    """Literal edits only. Expression strings are inventoried but never evaluated."""
    contexts={};label=None;stack=[];current_scene=None;calls=[];special={};safe={}
    for number,line in enumerate(text.splitlines(),1):
        indent=len(line)-len(line.lstrip());strip=line.strip()
        if strip.startswith('label '):label=strip.split()[1].split('(')[0].rstrip(':');stack=[]
        if strip and not strip.startswith('#'):
            while stack and indent<=stack[-1][0]:stack.pop()
        m=re.search(r"r13_v111_scene\(['\"]([^'\"]+)",line)
        if m:current_scene=m.group(1)
        contexts[number]=dict(label=label,guards=[x[1] for x in stack],scene=current_scene)
        if re.match(r'(if |elif |else:|menu:|for |while )',strip) and strip.endswith(':'):stack.append((indent,strip))
    # Safe direct dialogue and display_menu labels, using actual AST spans.
    for match in re.finditer(r'\b(r13_lines|renpy\.display_menu)\s*\(',text):
        begin=text.index('(',match.start());end=closing(text,begin)
        if end is None:continue
        fragment=text[match.start():end]
        try:call=ast.parse(fragment,mode='eval').body
        except SyntaxError:continue
        if not isinstance(call,ast.Call) or not call.args:continue
        def choices(node):
            if isinstance(node,(ast.List,ast.Tuple)):return node.elts
            if isinstance(node,ast.ListComp):return [node.elt]
            if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):return choices(node.left)+choices(node.right)
            return []
        for node in choices(call.args[0]):
            if not isinstance(node,ast.Tuple) or len(node.elts)<2:continue
            candidate=node.elts[1 if match.group(1)=='r13_lines' else 0]
            if isinstance(candidate,ast.Constant) and isinstance(candidate.value,str):
                span=ast_span(fragment,candidate,match.start())
                speaker=None
                if match.group(1)=='r13_lines' and isinstance(node.elts[0],ast.Constant):speaker=node.elts[0].value
                safe[tuple(span)]=dict(speaker=speaker,kind='dialogue' if speaker else 'narration',origin='rpy_literal',id=None)
    for variable in ('R13_V111_CARRIAGE_TEXT','R13_NW_WRONG_THOUGHTS'):
        for match in re.finditer(r'\b'+variable+r'\s*=\s*\{',text):
            begin=text.index('{',match.start());end=closing(text,begin)
            if end is None:continue
            fragment=text[begin:end]
            try:tree=ast.parse(fragment,mode='eval').body
            except SyntaxError:continue
            def walk(node,path=()):
                if isinstance(node,ast.Dict):
                    for k,v in zip(node.keys,node.values):
                        try:key=ast.literal_eval(k)
                        except (ValueError,TypeError):continue
                        walk(v,path+(key,))
                elif isinstance(node,ast.Constant) and isinstance(node.value,str):
                    span=ast_span(fragment,node,begin)
                    safe[tuple(span)]=dict(speaker='아빠' if variable.endswith('THOUGHTS') else None,kind='thought' if variable.endswith('THOUGHTS') else 'dialogue',origin='rpy_override',id=str(path[0]) if variable.endswith('CARRIAGE_TEXT') else variable+':'+':'.join(map(str,path)))
            walk(tree)
    # The remaining strings are explicitly read-only inventory (not all are dialogue).
    rows=[];offset=0
    for number,line in enumerate(text.splitlines(keepends=True),1):
        try:
            tokens=tokenize.generate_tokens(io.StringIO(line.lstrip()).readline)
            for token in tokens:
                if token.type!=tokenize.STRING:continue
                dynamic=False
                try:value=ast.literal_eval(token.string)
                except (ValueError,SyntaxError):
                    if not KOREAN.search(token.string):continue
                    value=token.string;dynamic=True
                if not isinstance(value,str) or not KOREAN.search(value):continue
                lead=len(line)-len(line.lstrip());span=[offset+lead+token.start[1],offset+lead+token.end[1]]
                info=None if dynamic else safe.get(tuple(span))
                stripped=line.strip()
                if not dynamic and not info and any(x.startswith('menu:') for x in contexts.get(number,{}).get('guards',[])) and re.match(r"^[\"']",stripped) and stripped.endswith(':'):
                    # Ren'Py menu text, including an optional if clause. Only literal token changes.
                    info=dict(speaker=None,kind='choice',origin='rpy_menu',id=None)
                context=contexts.get(number,{})
                rid=(info or {}).get('id') or f'{file}:{number}:{token.start[1]+lead}'
                rows.append(dict(file=file,path=span,id=rid,when=None,speaker=(info or {}).get('speaker'),kind=(info or {}).get('kind','unknown'),text=value,
                    origin=(info or {}).get('origin','rpy_inventory'),editable=bool(info),usage='active' if info else 'unknown',line=number,
                    scene=context.get('scene') or context.get('label') or '기타 문자열',block=context.get('label'),placement='literal',
                    call_sites=[dict(file=file,line=number,label=context.get('label'),guards=context.get('guards',[]))],
                    note='리터럴 범위만 수정; 호출 조건은 실행해 판정하지 않음' if info else '직접 실행 위치를 안전하게 확정하지 못한 한국어 문자열: 읽기 전용'))
        except (tokenize.TokenError,IndentationError):pass
        offset+=len(line)
    # Multi-line direct literals safely parsed above may not be tokenized line by line.
    existing={tuple(r['path']) for r in rows}
    for span,info in safe.items():
        if span in existing:continue
        try:value=ast.literal_eval(text[span[0]:span[1]])
        except (ValueError,SyntaxError):continue
        if not KOREAN.search(value):continue
        number=text.count('\n',0,span[0])+1;ctx=contexts.get(number,{})
        rows.append(dict(file=file,path=list(span),id=info.get('id') or f'{file}:{number}:{span[0]}',when=None,speaker=info.get('speaker'),kind=info['kind'],text=value,origin=info['origin'],editable=True,usage='active',line=number,scene=ctx.get('scene') or ctx.get('label') or '기타 문자열',block=ctx.get('label'),placement='literal',call_sites=[dict(file=file,line=number,label=ctx.get('label'),guards=ctx.get('guards',[]))],note='다중 행 리터럴 범위만 수정'))
    # Triple-quoted expressions not recognized as safe dialogue are explicit readonly inventory.
    existing={tuple(r['path']) for r in rows}
    pattern=r"(?s)(?P<prefix>[rRuUbBfF]{0,2})(?P<quote>\"{3}|'{3}).*?(?<!\\)(?P=quote)"
    for m in re.finditer(pattern,text):
        span=(m.start(),m.end())
        if span in existing or not KOREAN.search(m.group(0)):continue
        number=text.count('\n',0,m.start())+1
        if text[text.rfind('\n',0,m.start())+1:m.start()].lstrip().startswith('#'):continue
        try:value=ast.literal_eval(m.group(0))
        except (ValueError,SyntaxError):value=m.group(0)
        if not isinstance(value,str):continue
        ctx=contexts.get(number,{})
        rows.append(dict(file=file,path=list(span),id=f'{file}:{number}:{m.start()}',when=None,speaker=None,kind='unknown',text=value,origin='rpy_inventory',editable=False,usage='unknown',line=number,scene=ctx.get('scene') or ctx.get('label') or '기타 문자열',block=ctx.get('label'),placement='literal',call_sites=[dict(file=file,line=number,label=ctx.get('label'),guards=ctx.get('guards',[]))],note='여러 줄 문자열/표현식: 실행 용도를 확정하지 않아 읽기 전용'))
    # Call-site metadata is a lexical inventory, not a route simulator.
    for match in re.finditer(r"r13_nw_block\(\s*['\"]([^'\"]+)['\"]|r13_v111_lines\(\s*\[([^\]]*)\]",text,re.S):
        number=text.count('\n',0,match.start())+1;ctx=contexts.get(number,{})
        refs=[('block',match.group(1))] if match.group(1) else [('record',x) for x in re.findall(r'MS14_\w+',match.group(2))]
        for typ,key in refs:calls.append((typ,key,dict(file=file,line=number,label=ctx.get('label'),guards=ctx.get('guards',[]))))
    return rows,calls

def infer_day(value):
    m=re.search(r'(?:D|d)(\d{2})(?:_|\b)',value or '')
    if m:return int(m.group(1))
    m=re.search(r'(1[0-4]|[1-9])$',value or '')
    return int(m.group(1)) if m else None

def source_files(root):
    game=root/'game'
    return sorted([game/'v111/records.json',game/'v111/field-bindings.json']+list((game/'v111/newworld').glob('*.json'))+
        [p for p in game.rglob('*.rpy') if 'qa_tests' not in p.parts])

def collect(root=ROOT,out=None):
    root=Path(root);out=Path(out) if out else root/'docs/dialogue-modules'
    files=source_files(root);sources={str(p.relative_to(root)):p.read_bytes() for p in files if p.exists()}
    hashes={k:digest(v) for k,v in sources.items()};stamp=digest(json.dumps(hashes,sort_keys=True))
    records=json.loads(sources['game/v111/records.json'])['records']
    try:
        scene_title_map={x['scene_id']:x.get('title',x['scene_id']) for x in json.loads((root/'docs/story-ms14/source/다람탐정_제작기준본01_대사연출조건.json').read_text())['scenes']}
    except (OSError,KeyError,ValueError):scene_title_map={}
    patches={name:json.loads(raw) for name,raw in sources.items() if '/newworld/' in name and name.endswith('.json')}
    calls={};rpy_rows=[];carriage=set();predicates={};used_when=set()
    for file,raw in sources.items():
        if not file.endswith('.rpy'):continue
        text=raw.decode('utf-8');rows,sites=scan_rpy(text,file);rpy_rows.extend(rows)
        for typ,key,site in sites:calls.setdefault((typ,key),[]).append(site)
        carriage.update(r['id'] for r in rows if r['origin']=='rpy_override' and r['id'].startswith('MS14_'))
        # Exact source expressions of named predicates, without evaluating game Python.
        for m in re.finditer(r'^[ \t]*[\"\']([^\"\']+)[\"\']\s*:\s*(lambda[^\n]+)',text,re.M):
            predicates[m.group(1)]=m.group(2).rstrip().rstrip(',')
    shadow={};drops={}
    for file,data in patches.items():
        for rid,value in data.get('replace',{}).items():
            variants=value if isinstance(value,list) else [value]
            shadow.setdefault(rid,[]).extend(variants)
        for entry in data.get('drop',[]):drops.setdefault(entry if isinstance(entry,str) else entry['id'],[]).append(None if isinstance(entry,str) else entry.get('when'))
    rows=[]
    def add(file,path,text,**meta):
        if not isinstance(text,str):return
        rid=meta.get('id') or pointer(path);ref=meta.get('ref') or rid
        match=re.match(r'(MS14_D\d{2}_.+)_L\d+',str(ref))
        scene=meta.pop('scene',None) or (match.group(1) if match else meta.get('block') or '공통')
        day=meta.pop('day',None) or infer_day(file) or infer_day(str(ref)) or infer_day(meta.get('block') or '')
        defaults=dict(id=rid,file=file,path=path,origin='json',day=day,scene=scene,block=None,placement='text',ref=ref,when=None,speaker=None,kind='dialogue',text=text,editable=True,usage='active',note='',call_sites=[])
        defaults.update(meta);defaults['text']=text;defaults['scene_title']=scene_title_map.get(scene,scene)
        defaults['source_hash']=hashes[file];defaults['baseline_hash']=digest(text)
        defaults['uid']=digest(file+'#'+pointer(path))[:24]
        defaults['review_status']='draft';defaults['baseline_review_status']='draft'
        defaults['branch_key']='|'.join([f'd{day:02}' if day else '공통',scene,defaults['origin'],defaults.get('block') or defaults['placement'],defaults.get('when') or '행 조건 없음'])
        defaults['activation_note']='when은 이 행의 조건만 표시한다. 상위 호출·선택·앞선 변형 우선순위가 추가로 적용될 수 있다.'
        rows.append(defaults)
        if defaults.get('when'):used_when.add(defaults['when'])
    for rid,row in records.items():
        if 'text' not in row:continue
        variants=shadow.get(rid,[]);drop=drops.get(rid,[]);sites=calls.get(('record',rid),[])
        usage='active';note='원문 변경은 해당 날짜 newworld 기본 replace로 반영한다.'
        if not sites:usage='unused';note='직접 대사 호출을 정적으로 찾지 못함. 진행 메모/미사용 원문일 수 있어 읽기 전용.'
        elif None in drop:usage='dropped';note='무조건 drop으로 화면에서 제외됨.'
        elif any(not v.get('when') for v in variants):usage='overridden';note='무조건 replace가 있으므로 이 원문을 수정해도 현재 대사는 바뀌지 않음.'
        elif rid in carriage:usage='overridden';note='R13_V111_CARRIAGE_TEXT가 덮어씀. rpy_override 행을 수정해야 함.'
        elif variants or drop:note+=' 조건부 replace/drop 이후 원문 fallback이며 무조건 표시된다는 뜻이 아니다.'
        day=infer_day(rid)
        add('game/v111/records.json',['records',rid,'text'],row['text'],id=rid,origin='base',day=day,speaker=row.get('speaker'),kind=row.get('kind','unknown'),usage=usage,editable=usage=='active' and bool(day),note=note,call_sites=sites,activation=dict(replace_conditions=[v.get('when') for v in variants],drop_conditions=drop))
    for file,data in patches.items():
        for section in ('replace','before','after','blocks'):
            for ref,value in data.get(section,{}).items():
                seq=value if isinstance(value,list) else [value]
                for i,row in enumerate(seq):
                    if not isinstance(row,dict) or 'text' not in row:continue
                    path=[section,ref]+([i] if isinstance(value,list) else [])+['text']
                    block=ref if section=='blocks' else None;sites=calls.get(('block' if block else 'record',ref),[])
                    add(file,path,row['text'],id=row.get('id') or ref,ref=ref,origin='patch',placement=section,block=block,when=row.get('when'),speaker=row.get('speaker',records.get(ref,{}).get('speaker')),kind=row.get('kind',records.get(ref,{}).get('kind','dialogue')),call_sites=sites,usage='active' if sites else 'unknown',note='' if sites else '呼出位置を静的に確定できない'.replace('呼出位置を静的に確定できない','호출 위치를 정적으로 확정하지 못함'))
        for section in ('evidence','new_evidence'):
            for ref,spec in data.get(section,{}).items():
                if 'name' in spec:add(file,[section,ref,'name'],spec['name'],id=ref+':name',ref=ref,origin='catalog',kind='evidence_name',placement=section)
                for group in ('variants','add_variants'):
                    for variant,text in spec.get(group,{}).items():add(file,[section,ref,group,variant],text,id=ref+':'+variant,ref=ref,origin='catalog',kind='evidence',placement=section,block=ref)
        for gate,options in data.get('titles',{}).items():
            for key,text in options.items():add(file,['titles',gate,key],text,id=gate+':'+key,origin='choice',kind='choice',placement='titles',block=gate)
    # Original evidence descriptions that have no patched catalog entry are kept read-only.
    record_data=json.loads(sources['game/v111/records.json'])
    for key,spec in record_data.get('evidence',{}).items():
        for variant,text in spec.get('variants',{}).items():add('game/v111/records.json',['evidence',key,'variants',variant],text,id=key+':'+variant,origin='base_catalog',kind='evidence',placement='evidence',block=key,editable=False,note='원본 자료 설명. 이 도구의 기본 대사 override 대상이 아니므로 읽기 전용; newworld evidence 변형을 사용한다.')
    binding_file='game/v111/field-bindings.json'
    if binding_file in sources:
        for gate,b in json.loads(sources[binding_file]).items():
            for i,opt in enumerate(b.get('options',[])):
                if 'title' in opt:add(binding_file,[gate,'options',i,'title'],opt['title'],id=gate+':'+str(opt.get('index',i)),origin='choice',kind='choice',placement='binding',block=gate,day=infer_day(gate),activation=dict(guard=opt.get('guard',[]),location=opt.get('location'),person=opt.get('person'),object=opt.get('object')))
    for row in rpy_rows:
        if row['origin']=='rpy_override' and row['id'] in records:
            row['speaker']=records[row['id']].get('speaker');row['kind']=records[row['id']].get('kind','dialogue')
            row['scene']=re.sub(r'_L\d+.*$','',row['id']);row['call_sites']=calls.get(('record',row['id']),[])
        text=row.pop('text');file=row.pop('file');path=row.pop('path');add(file,path,text,**row)
    for key in used_when:
        if key not in predicates:
            if key.startswith('listed:'):predicates[key]=f'r13_v111_value({key!r}) is True (실행 시 생성되는 이름별 조건)'
            elif key.startswith('dead:'):predicates[key]=f'{key[5:]!r} in r13_nw_dead() (실행 시 생성되는 이름별 조건)'
            else:predicates[key]='실행 시 등록되는 조건; 정적 식을 확정하지 못함. room13_v111_newworld_text.rpy 등 원본 확인 필요.'
    status_file=out/'review-status.json'
    statuses=json.loads(status_file.read_text()).get('entries',{}) if status_file.exists() else {}
    for row in rows:
        entry=statuses.get(row['uid'],{})
        if entry.get('baseline_hash')==row['baseline_hash'] and entry.get('review_status') in STATUSES:row['review_status']=row['baseline_review_status']=entry['review_status']
    branch_map={}
    for row in rows:
        key=row['branch_key'];b=branch_map.setdefault(key,dict(key=key,label=' · '.join([str(row['day'])+'일' if row['day'] else '공통',row['scene_title'],row.get('block') or row['placement'],row.get('when') or '행 조건 없음']),count=0,file='branches/'+digest(key)[:16]+'.json'));b['count']+=1
    try:revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,stderr=subprocess.DEVNULL,text=True).strip()
    except (OSError,subprocess.CalledProcessError):revision='unknown'
    return dict(schema=SCHEMA,stamp=stamp,source_stamp=stamp,revision=revision,generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,predicates={k:predicates[k] for k in sorted(used_when)},branches=list(branch_map.values()),coverage=dict(source_files=len(sources),rows=len(rows),editable=sum(r['editable'] for r in rows),readonly=sum(not r['editable'] for r in rows),scope='원문 records·모든 newworld JSON·field 선택 제목·비QA rpy 한국어 문자열. 안전하게 확인한 리터럴만 rpy 편집 가능. 정적 조건/호출 목록이며 전체 실행 경로를 계산한 시뮬레이터가 아님.'))

def runtime_tokens(text):
    # Doubled brackets/braces are literal escapes, not runtime expressions.
    return re.findall(r'(?<!\[)\[(?!\[)[^\]\n]*\]|(?<!\{)\{(?!\{)[^}\n]*\}',text)

def validate(package,inventory):
    if not isinstance(package,dict) or set(package)!={'schema','source_stamp','entries'}:raise ModuleError('편집 JSON 최상위 필드는 schema/source_stamp/entries만 허용한다.')
    if package['schema']!=EDIT_SCHEMA:raise ModuleError('지원하지 않는 편집 schema')
    if package['source_stamp']!=inventory['stamp']:raise ModuleError('오래된 source_stamp: 현재 모듈을 다시 다운로드해야 한다.')
    if not isinstance(package['entries'],list):raise ModuleError('entries는 배열이어야 한다.')
    current={r['uid']:r for r in inventory['rows']};seen=set();changes=[]
    for item in package['entries']:
        if not isinstance(item,dict):raise ModuleError('각 항목은 객체여야 한다.')
        uid=item.get('uid')
        if not isinstance(uid,str) or uid not in current:raise ModuleError('알 수 없는 uid')
        if uid in seen:raise ModuleError('중복 uid: '+uid)
        seen.add(uid);old=current[uid]
        if set(item)!=set(old):raise ModuleError('항목 필드 추가/삭제는 허용하지 않는다: '+uid)
        if json.dumps({k:item[k] for k in old if k not in MUTABLE},sort_keys=True,ensure_ascii=False)!=json.dumps({k:old[k] for k in old if k not in MUTABLE},sort_keys=True,ensure_ascii=False):raise ModuleError('메타데이터/조건/원본 hash가 달라졌다: '+uid)
        if item['review_status'] not in STATUSES:raise ModuleError('검수 상태는 draft/reviewed/needs_work만 허용한다.')
        if not isinstance(item['text'],str) or '\x00' in item['text']:raise ModuleError('text는 NUL 없는 문자열이어야 한다.')
        if item['text']!=old['text']:
            if not old['editable']:raise ModuleError('읽기 전용 항목의 text 변경: '+uid)
            if not item['text'].strip():raise ModuleError('빈 text로 대사를 삭제할 수 없다.')
            if runtime_tokens(item['text'])!=runtime_tokens(old['text']):raise ModuleError('Ren’Py 보간식/제어 태그는 변경하거나 추가할 수 없다: '+uid)
        if item['text']!=old['text'] or item['review_status']!=old['review_status']:changes.append((old,item))
    return changes

def atomic_write_batch(updates):
    """Stage all bytes first; restore every replaced file if any replacement fails."""
    originals={p:p.read_bytes() if p.exists() else None for p in updates};temps={};written=[]
    def stage(path,raw):
        path.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
        with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        os.chmod(name,(path.stat().st_mode&0o777) if path.exists() else 0o644)
        return Path(name)
    try:
        for path,raw in updates.items():temps[path]=stage(path,raw)
        for path,temp in temps.items():os.replace(temp,path);written.append(path)
    except Exception:
        for path in reversed(written):
            if originals[path] is None:path.unlink(missing_ok=True)
            else:
                restored=stage(path,originals[path]);os.replace(restored,path)
        raise
    finally:
        for temp in temps.values():temp.unlink(missing_ok=True)

def apply_package(package,root=ROOT,out=None,write=False):
    root=Path(root);out=Path(out) if out else root/'docs/dialogue-modules';inv=collect(root,out);changes=validate(package,inv)
    parsed={};spans={};status_file=out/'review-status.json';status=json.loads(status_file.read_text()) if status_file.exists() else dict(schema='room13.dialogue-status.v1',entries={});targets=[]
    def document(file):
        if file not in parsed:
            p=root/file;parsed[file]=json.loads(p.read_text()) if p.exists() else {}
        return parsed[file]
    # Apply existing patch paths before adding an original-text fallback variant.
    for old,item in sorted(changes,key=lambda pair:pair[0]['origin']=='base'):
        target_file=old['file'];target_path=old['path'];target_uid=old['uid']
        if old['text']!=item['text']:
            if old['origin']=='base':
                target_file=f"game/v111/newworld/d{old['day']:02}.json";doc=document(target_file);replaces=doc.setdefault('replace',{});value=replaces.get(old['id'])
                if value is None:replaces[old['id']]={'text':item['text']};target_path=['replace',old['id'],'text']
                elif isinstance(value,list):value.append({'text':item['text']});target_path=['replace',old['id'],len(value)-1,'text']
                elif value.get('when'):replaces[old['id']]=[value,{'text':item['text']}];target_path=['replace',old['id'],1,'text']
                else:raise ModuleError('원문이 이미 대체되어 있어 수정할 수 없다.')
                target_uid=digest(target_file+'#'+pointer(target_path))[:24]
            elif target_file.endswith('.rpy'):
                spans.setdefault(target_file,[]).append((target_path[0],target_path[1],json.dumps(item['text'],ensure_ascii=False)))
            else:
                doc=document(target_file);parent=get_at(doc,target_path[:-1]);parent[target_path[-1]]=item['text']
        status['entries'][old['uid']]=dict(baseline_hash=old['baseline_hash'] if old['origin']=='base' else digest(item['text']),review_status=item['review_status'])
        if target_uid!=old['uid']:status['entries'][target_uid]=dict(baseline_hash=digest(item['text']),review_status=item['review_status'])
        targets.append(dict(uid=old['uid'],id=old['id'],file=target_file,path=target_path,before=old['text'],after=item['text'],review_status=item['review_status']))
    updates={root/file:encode(data) for file,data in parsed.items()}
    for file,edits in spans.items():
        text=(root/file).read_text();edits=sorted(edits,reverse=True)
        for i,(start,end,replacement) in enumerate(edits):
            if i and end>edits[i-1][0]:raise ModuleError('겹치는 rpy 편집 범위')
            text=text[:start]+replacement+text[end:]
        updates[root/file]=text.encode('utf-8')
    if changes:updates[status_file]=encode(status)
    if write and updates:
        # Check the source stamp once more before committing staged mutations.
        if collect(root,out)['stamp']!=inv['stamp']:raise ModuleError('검사 중 소스가 바뀌었다. 다시 확인해야 한다.')
        atomic_write_batch(updates)
    return dict(status='passed',write=write,entries=len(package['entries']),changed=len(changes),files=[str(p.relative_to(root)) if p.is_relative_to(root) else str(p) for p in updates],changes=targets)

def build(root=ROOT,out=None,template=None):
    root=Path(root);out=Path(out) if out else root/'docs/dialogue-modules';template=Path(template) if template else root/'dev/dialogue-modules/index.html';inv=collect(root,out)
    if not template.exists():raise ModuleError('HTML 템플릿이 없다: '+str(template))
    readings={}
    reader=root/'dev/dialogue_day.py'
    required=[root/'game/v111/records.json']+[root/f'game/v111/newworld/d{day:02}.json' for day in range(1,15)]
    if reader.exists() and all(p.exists() for p in required):
        for day in range(1,15):
            try:readings[f'reading/d{day:02}.txt']=subprocess.check_output([sys.executable,str(reader),'show',str(day)],cwd=root,text=True,encoding='utf-8').encode('utf-8')
            except subprocess.CalledProcessError as e:raise ModuleError(f'{day}일 합본 대본 생성 실패') from e
            lines=[]
            for line in readings[f'reading/d{day:02}.txt'].decode('utf-8').splitlines():
                m=re.match(r'^(\s*\+?)(NW_[A-Za-z0-9_]+|S[0-9]+_[A-Za-z0-9_]+)',line)
                if m:
                    ref=m.group(2) if m.group(2).startswith('NW_') else f'MS14_D{day:02}_'+m.group(2)
                    rendered=html_module.escape(m.group(1))+f'<a href="../?day={day}&amp;q={ref}">'+html_module.escape(m.group(2))+'</a>'+html_module.escape(line[m.end():])
                else:rendered=html_module.escape(line)
                lines.append(rendered)
            page=f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{day}일 순서 대본</title><style>body{{max-width:1100px;margin:24px auto;padding:16px;background:#fffaf0;color:#332a21;font:16px/1.8 system-ui,sans-serif}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}}a{{color:#704322}}nav{{position:sticky;top:0;background:#fffaf0;padding:12px 0;border-bottom:1px solid #cbb799}}</style><nav><a href="../?day={day}">대사 편집기</a> · <a href="d{day:02}.txt" download>합본 텍스트 받기</a></nav><h1>{day}일 순서 대본</h1><p>대사 ID를 누르면 편집기로 이동합니다. 조건이 다른 줄은 나란히 표시되며 한 번의 플레이에서 모두 나오는 줄이 아닙니다.</p><pre>'+"\n".join(lines)+'</pre></html>'
            readings[f'reading/d{day:02}.html']=page.encode('utf-8')
    inv['reading']={str(day):f'reading/d{day:02}.html' for day in range(1,15)} if readings else {}
    inv['reading_note']='기존 dialogue_day show의 순서 합본이다. 서로 다른 조건의 줄은 나란히 표시되며, 실제 한 번의 플레이에서 모두 재생된다는 뜻은 아니다.'
    html=template.read_text()
    if html.count('__DATA__')!=1:raise ModuleError('템플릿에는 __DATA__가 정확히 한 번 있어야 한다.')
    payload=json.dumps(inv,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    out.mkdir(parents=True,exist_ok=True)
    updates={out/'inventory.json':encode(inv),out/'branches.json':encode(inv['branches']),out/'index.html':html.replace('__DATA__',payload).encode('utf-8')}
    updates.update({out/file:raw for file,raw in readings.items()})
    if not (out/'review-status.json').exists():updates[out/'review-status.json']=encode(dict(schema='room13.dialogue-status.v1',entries={}))
    groups={b['key']:[] for b in inv['branches']}
    for row in inv['rows']:groups[row['branch_key']].append(row)
    for branch in inv['branches']:updates[out/branch['file']]=encode(dict(schema=EDIT_SCHEMA,source_stamp=inv['stamp'],entries=groups[branch['key']]))
    atomic_write_batch(updates)
    return dict(status='passed',stamp=inv['stamp'],rows=len(inv['rows']),branches=len(inv['branches']),coverage=inv['coverage'])

def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--out',type=Path)
    sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build');b.add_argument('--template',type=Path)
    for cmd in ('check','apply'):
        q=sub.add_parser(cmd);q.add_argument('file',type=Path)
        if cmd=='apply':q.add_argument('--write',action='store_true')
    args=p.parse_args()
    try:
        result=build(args.root,args.out,args.template) if args.command=='build' else apply_package(json.loads(args.file.read_text()),args.root,args.out,args.command=='apply' and args.write)
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ModuleError,OSError,ValueError,KeyError,TypeError) as e:
        print(json.dumps(dict(status='failed',error=str(e)),ensure_ascii=False));return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
