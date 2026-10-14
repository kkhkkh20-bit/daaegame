"""대사집 내보내기·반영 (소유자 요청, 0.18.6).

  python3 dev/dialogue_tool.py export [--out DIR]
      대사와 선택지를 장면별 CSV(엑셀·구글 시트용, UTF-8 BOM)와 지침.md로 꺼낸다.
  python3 dev/dialogue_tool.py import FILE_OR_DIR_OR_ZIP [--apply]
      "수정" 칸이 채워진 CSV를 읽는다. 기본은 시험 반영(파일을 바꾸지 않고 보고서만 쓴다).
      --apply 를 붙여야 실제로 고친다.

안전 장치(하나라도 걸리면 그 줄은 반영하지 않고 보고서에 이유를 적는다)
  - 위치(파일·줄)와 원문이 지금 소스와 정확히 같아야 한다. 줄이 옮겨졌으면 같은 파일에서
    원문이 딱 하나일 때만 찾아서 바꾼다.
  - {b}·{/b}·[이름]·%d 같은 코드 조각이 원문과 똑같아야 한다.
  - 인물 이름이 원문과 같은 횟수로 남아야 한다.
  - 줄바꿈, 백슬래시, 문자열을 닫는 따옴표(" 또는 ')는 쓸 수 없다. 따옴표는 ‘’ “”를 쓴다.
  - 선택지는 24자 이하, 대사는 원문의 1.5배(최소 +20자)와 140자 이하.
  - 테스트가 그 글자로 확인하는 대사는 내보내지 않는다(잠김). 테스트가 클릭하는 선택지는
    반영할 때 tests.rpy의 같은 문구도 함께 바꾼다.
"""
import csv,hashlib,io,json,re,sys,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
JSON_FILES=['room13-content.json','room13-dialogue-openings.json']
CHUNK=150
CHOICE_LIMIT=24
HANGUL=re.compile(r'[가-힣]')
TOKEN=re.compile(r'\{[^{}]*\}|\[[^\[\]]*\]|%[sd%]')
SPEAKER_KEY=r'(?:None|"[a-z][a-z0-9_]*"|\'[a-z][a-z0-9_]*\')'
STRING=r'(?:"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\')'
LINE_RE=re.compile(r'\(\s*('+SPEAKER_KEY+r')\s*,\s*'+STRING)
CHOICE_RE=re.compile(r'^(\s+)"([^"\\\n]+)"(\s+if\s[^\n]*)?:\s*$')
FIELDS=['번호','종류','장면','화자','원문','수정','위치']

def rpy_files():
    for f in sorted(GAME.rglob('*.rpy')):
        rel=f.relative_to(GAME).as_posix()
        if rel.startswith('qa_tests/') or Path(rel).name.startswith('winter'):continue
        yield f,rel

def names():
    """Runtime display names: options NAMES, WINTER_NAMES, R13_NAMES.update(...), then residents only where missing."""
    out={}
    opts=(GAME/'options.rpy').read_text(encoding='utf-8')
    m=re.search(r'NAMES\s*=\s*\{([^}]*)\}',opts)
    if m:out.update(re.findall(r'"([a-z_]+)"\s*:\s*"([^"]+)"',m.group(1)))
    win=(GAME/'winter.rpy').read_text(encoding='utf-8')
    m=re.search(r'WINTER_NAMES\s*=\s*dict\(NAMES,([^)]*)\)',win)
    if m:out.update(re.findall(r'([a-z_]+)\s*=\s*"([^"]+)"',m.group(1)))
    for f,rel in rpy_files():
        for block in re.findall(r'R13_NAMES\.update\((.*?)\)',f.read_text(encoding='utf-8'),re.S):
            out.update(re.findall(r'([a-z_]+)\s*=\s*"([^"]+)"',block))
    # room13_life.rpy fills only missing names (setdefault), as the game does.
    data=json.loads((GAME/'room13-content.json').read_text(encoding='utf-8'))
    for k,v in data.get('residents',{}).items():
        if isinstance(v,dict) and v.get('name'):out.setdefault(k,v['name'])
    return out

def locked_texts():
    """Strings tests check by text: never exported. Choices clicked in tests.rpy are handled separately."""
    blob=''
    for f in list((ROOT/'dev').glob('*.py'))+[GAME/'qa_tests/helpers.rpy']:
        if f.name!='dialogue_tool.py':blob+=f.read_text(encoding='utf-8')
    tests=(GAME/'qa_tests/tests.rpy').read_text(encoding='utf-8')
    clicks=set(re.findall(r'(?:click|until)\s+"([^"]+)"',tests))
    other=re.sub(r'(?:click|until)\s+"[^"]+"','',tests)
    return blob+other,clicks

def scene_of(text_before):
    m=list(re.finditer(r'^(?:label|testcase)\s+([A-Za-z0-9_]+)',text_before,re.M))
    return m[-1].group(1) if m else '(시작)'

def collect():
    """Rows in source order: dict(kind, file, line, scene, speaker, text, quote).
    Only real speakers (known names) or narration (None) count as dialogue; UI tuples are skipped."""
    speakers=set(names())|{'None','dad','daram','mom'}
    rows=[]
    for f,rel in rpy_files():
        src=f.read_text(encoding='utf-8')
        lines=src.split('\n')
        offsets=[0]
        for l in lines:offsets.append(offsets[-1]+len(l)+1)
        for i,l in enumerate(lines):
            m=CHOICE_RE.match(l)
            if m and HANGUL.search(m.group(2)):
                rows.append(dict(kind='선택지',file=rel,line=i+1,scene=scene_of(src[:offsets[i]]),speaker='',text=m.group(2),quote='"'))
            for m in LINE_RE.finditer(l):
                if m.start()>0 and re.match(r'[A-Za-z0-9_]',l[m.start()-1]):continue   # a call like _ep_topic("npc","title")
                text=m.group(2) if m.group(2) is not None else m.group(3)
                if text is None or not HANGUL.search(text) or '\\' in text:continue
                key=m.group(1).strip('"\'')
                if key not in speakers:continue
                thought=bool(re.match(r'\s*,\s*\{\s*["\']thought["\']\s*:\s*True',l[m.end():]))
                rows.append(dict(kind='대사',file=rel,line=i+1,scene=scene_of(src[:offsets[i]]),speaker=key,text=text,
                    quote='"' if m.group(2) is not None else "'",thought=thought))
    for name in JSON_FILES:
        data=json.loads((GAME/name).read_text(encoding='utf-8'))
        def walk(node,path):
            if isinstance(node,list):
                if (len(node) in (2,3) and (node[0] is None or (isinstance(node[0],str) and node[0] in speakers))
                        and isinstance(node[1],str) and HANGUL.search(node[1])):
                    rows.append(dict(kind='대사',file=name,line='/'.join(map(str,path+[1])),scene='/'.join(map(str,path[:2])),
                        speaker=node[0] or 'None',text=node[1],quote='',thought=len(node)>2 and isinstance(node[2],dict) and node[2].get('thought')))
                    return
                for i,x in enumerate(node):walk(x,path+[i])
            elif isinstance(node,dict):
                for k,v in node.items():walk(v,path+[k])
        walk(data,[])
    return rows

def row_id(r):
    return 'D'+hashlib.sha1(('%s|%s|%s'%(r['file'],r['line'],r['text'])).encode()).hexdigest()[:7]

def speaker_label(r,nm):
    if r['kind']=='선택지':return '(선택지)'
    if r['speaker']=='None':return '서술'
    who=nm.get(r['speaker'],r['speaker'])
    return ('속마음 · '+who) if r.get('thought') else who

def export(out):
    nm=names();blob,clicks=locked_texts()
    rows=collect()
    keep=[];locked=0
    for r in rows:
        if r['kind']=='대사' and (r['text'] in blob or r['text'] in clicks):locked+=1;continue
        if r['kind']=='선택지' and (r['text'] in blob or any(c in r['text'] and c!=r['text'] for c in clicks)):locked+=1;continue
        keep.append(r)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('대사집_*.csv'):old.unlink()
    groups=[];cur=[];last=None
    for r in keep:
        if len(cur)>=CHUNK and r['scene']!=last:groups.append(cur);cur=[]
        cur.append(r);last=r['scene']
    if cur:groups.append(cur)
    for n,g in enumerate(groups,1):
        with open(out/('대사집_%02d.csv'%n),'w',encoding='utf-8-sig',newline='') as fh:
            w=csv.writer(fh);w.writerow(FIELDS)
            for r in g:w.writerow([row_id(r),r['kind'],r['scene'],speaker_label(r,nm),r['text'],'','%s:%s'%(r['file'],r['line'])])
    # Voice samples: three lines per frequent speaker.
    by={}
    for r in keep:
        if r['kind']=='대사' and r['speaker'] not in ('None',) and not r.get('thought'):by.setdefault(r['speaker'],[]).append(r['text'])
    voices='\n'.join('- **%s**: %s'%(nm.get(k,k),' / '.join('“%s”'%(t if len(t)<=60 else t[:58]+'…') for t in v[:3])) for k,v in sorted(by.items(),key=lambda kv:-len(kv[1]))[:25])
    (out/'지침.md').write_text(GUIDE.format(files=len(groups),rows=len(keep),voices=voices,limit=CHOICE_LIMIT),encoding='utf-8')
    print(json.dumps(dict(out=str(out),files=len(groups),rows=len(keep),locked=locked),ensure_ascii=False))

GUIDE='''# 다람탐정 대사 다듬기 지침

파일 {files}개, 대사·선택지 {rows}줄입니다. 파일 하나씩 따로 맡겨 주세요.

## 꼭 지킬 것 (어기면 그 줄은 게임에 반영되지 않습니다)
1. **"수정" 칸만 채웁니다.** 번호·종류·장면·화자·원문·위치 칸은 한 글자도 바꾸지 않습니다. 줄을 지우거나 합치거나 순서를 바꾸지 않습니다.
2. 고칠 필요가 없는 줄은 **"수정" 칸을 비워 둡니다.**
3. `{{b}}` `{{/b}}` `{{color=…}}` `[이름]` `%d` 같은 괄호 조각은 원문 그대로 둡니다.
4. 인물 이름(너울, 바둑이, 나비 등)은 원문에 나온 만큼 그대로 둡니다. 다른 이름으로 바꾸지 않습니다.
5. 큰따옴표 `"` 와 작은따옴표 `'`, 줄바꿈은 쓰지 않습니다. 따옴표가 필요하면 ‘ ’ 나 “ ” 를 씁니다.
6. **선택지는 {limit}자 이하**로, 무엇을 하는지만 짧게 씁니다.
7. 대사는 원문보다 많이 길게 하지 않습니다(대략 1.5배, 140자 이내).
8. 사실 내용(누가, 언제, 어디서, 무엇을)은 바꾸지 않습니다. 단서와 추리가 걸려 있습니다.

## 말투 (원문 예시)
{voices}

- **서술**: 아빠 시점의 짧은 관찰문. 과장하지 않는다.
- **속마음 · 아빠**: 괄호 안의 생각. 짧고 단정하게.

## 돌려줄 때
- 같은 열 구성의 CSV로 저장해서 올려 주세요. 엑셀이면 "CSV UTF-8"로 저장합니다.
'''

def read_uploads(path):
    path=Path(path);texts=[]
    if path.is_dir():texts=[(p.name,p.read_bytes()) for p in sorted(path.rglob('*.csv'))]
    elif path.suffix=='.zip':
        with zipfile.ZipFile(path) as z:texts=[(n,z.read(n)) for n in z.namelist() if n.endswith('.csv')]
    else:texts=[(path.name,path.read_bytes())]
    rows=[]
    for name,data in texts:
        text=data.decode('utf-8-sig')
        dialect='excel-tab' if text.split('\n',1)[0].count('\t')>text.split('\n',1)[0].count(',') else 'excel'
        for r in csv.DictReader(io.StringIO(text),dialect=dialect):
            r={(k or '').strip():(v or '') for k,v in r.items()}
            r['_file']=name;rows.append(r)
    return rows

def check(orig,new,kind,nm):
    if '\n' in new or '\r' in new:return '줄바꿈이 들어 있음'
    if '\\' in new:return '백슬래시가 들어 있음'
    if sorted(TOKEN.findall(orig))!=sorted(TOKEN.findall(new)):return '괄호 조각({…}/[…]/%d)이 원문과 다름'
    for v in set(nm.values()):
        if len(v)>=2 and v not in ('아빠','엄마','할머니','촌장') and orig.count(v)!=new.count(v):return '인물 이름 "%s"의 횟수가 원문과 다름'%v
    if kind=='선택지' and len(new)>CHOICE_LIMIT:return '선택지가 %d자를 넘음(%d자)'%(CHOICE_LIMIT,len(new))
    if kind=='대사' and (len(new)>140 or len(new)>max(len(orig)*1.5,len(orig)+20)):return '대사가 너무 김(%d자)'%len(new)
    return None

def do_import(src,apply):
    nm=names();current={row_id(r):r for r in collect()}
    by_loc={}
    for r in current.values():by_loc.setdefault((r['file'],r['text']),[]).append(r)
    applied=[];rejected=[];seen=set()
    edits={}   # file -> list of (row, new)
    for u in read_uploads(src):
        new=(u.get('수정') or '').strip()
        if not new:continue
        rid=(u.get('번호') or '').strip();orig=u.get('원문') or '';loc=(u.get('위치') or '').strip()
        tag='%s %s'%(u['_file'],rid)
        if rid in seen:rejected.append((tag,orig,new,'같은 번호가 두 번 나옴'));continue
        seen.add(rid)
        if new==orig:continue
        r=current.get(rid)
        if r is None:
            file=loc.rsplit(':',1)[0]
            cands=by_loc.get((file,orig),[])
            if len(cands)==1:r=cands[0]
            else:rejected.append((tag,orig,new,'원문을 지금 소스에서 찾을 수 없음' if not cands else '같은 원문이 여러 곳이라 위치를 정할 수 없음'));continue
        if r['text']!=orig:rejected.append((tag,orig,new,'원문 칸이 바뀌었음'));continue
        quote=r.get('quote')
        if quote and quote in new:rejected.append((tag,orig,new,'따옴표 %s 는 쓸 수 없음(‘’ “” 사용)'%quote));continue
        why=check(orig,new,r['kind'],nm)
        if why:rejected.append((tag,orig,new,why));continue
        edits.setdefault(r['file'],[]).append((r,new));applied.append((tag,orig,new,r))
    tests_changes=[]
    if apply:
        for file,items in edits.items():
            path=GAME/file
            if file.endswith('.json'):
                raw=path.read_text(encoding='utf-8')
                data=json.loads(raw)
                for r,new in items:
                    node=data;parts=r['line'].split('/')
                    for p in parts[:-1]:node=node[int(p)] if isinstance(node,list) else node[p]
                    assert node[int(parts[-1])]==r['text']
                    node[int(parts[-1])]=new
                path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+('\n' if raw.endswith('\n') else ''),encoding='utf-8')
            else:
                lines=path.read_text(encoding='utf-8').split('\n')
                for r,new in items:
                    i=r['line']-1;q=r['quote']
                    old=q+r['text']+q
                    assert lines[i].count(old)>=1,(file,r['line'])
                    lines[i]=lines[i].replace(old,q+new+q,1)
                    if r['kind']=='선택지':tests_changes.append((r['text'],new))
                path.write_text('\n'.join(lines),encoding='utf-8')
        if tests_changes:
            tp=GAME/'qa_tests/tests.rpy';t=tp.read_text(encoding='utf-8')
            for old,new in tests_changes:t=t.replace('"%s"'%old,'"%s"'%new)
            tp.write_text(t,encoding='utf-8')
    report=['# 대사 반영 보고서 (%s)'%('반영함' if apply else '시험 반영 · 파일은 바뀌지 않음'),'',
        '- 반영 %d줄 · 거절 %d줄'%(len(applied),len(rejected)),'']
    if rejected:
        report+=['## 거절된 줄','','| 위치 | 이유 | 원문 | 수정 |','|---|---|---|---|']
        report+=['| %s | %s | %s | %s |'%(t,w,o.replace('|','/'),n.replace('|','/')) for t,o,n,w in rejected]
        report.append('')
    report+=['## 반영 목록','','| 위치 | 원문 | 수정 |','|---|---|---|']
    report+=['| %s:%s | %s | %s |'%(r['file'],r['line'],o.replace('|','/'),n.replace('|','/')) for t,o,n,r in applied]
    print('\n'.join(report[:4]))
    return '\n'.join(report)+'\n',len(applied),len(rejected)

if __name__=='__main__':
    args=sys.argv[1:]
    if args[:1]==['export']:
        out=args[args.index('--out')+1] if '--out' in args else str(ROOT.parents[1]/'dialogue_work/export')
        export(out)
    elif args[:1]==['import'] and len(args)>=2:
        text,n,bad=do_import(args[1],'--apply' in args)
        out=Path(args[args.index('--report')+1]) if '--report' in args else ROOT.parents[1]/'dialogue_work/반영_보고서.md'
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding='utf-8');print('report:',out)
    else:
        print(__doc__);sys.exit(2)
