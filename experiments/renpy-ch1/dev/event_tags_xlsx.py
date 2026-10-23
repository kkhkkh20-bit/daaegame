"""분기 지도 엑셀에 사건 태그 열을 붙인다 (2026-10-23 소유자: "각 사건 태그를 걸어서 쉽게 구분하고 정리해 보자").

  python3 dev/event_tags_xlsx.py 원본.xlsx 결과.xlsx

각 시트 맨 오른쪽에 "사건 태그" 열을 더하고(기존 열 순서와 수식은 그대로), 맨 앞에 "사건태그" 정의 시트를 넣는다.
행의 라벨·대사 ID·블록·관문 이름·"파일:줄"(0.20.15 기준)·분기 ID 순으로 읽어 docs/design/event_tags.json 의 태그를 단다.
"""
import json,re,openpyxl,subprocess,glob,sys
from openpyxl.styles import Font,PatternFill
from copy import copy
SRC,OUT=sys.argv[1],sys.argv[2]
d=json.load(open('docs/design/event_tags.json'))
L=d['labels']; S={s:t for t,e in d['events'].items() for s in e['scenes']}
B={b:t for t,e in d['events'].items() for b in e['branches']}
LINE={}
for f in ['room13_v111_days123.rpy','room13_v111_days45.rpy','room13_v111_days610.rpy','room13_v111_days1114.rpy','room13_v111.rpy','room13_v111_later_bindings.rpy']:
    src=subprocess.run(['git','show','5f6654e:experiments/renpy-ch1/game/'+f],capture_output=True,text=True).stdout.split('\n')
    cur=None
    for n,l in enumerate(src,1):
        m=re.match(r'label (\w+)',l)
        if m: cur=m.group(1)
        elif l.strip() and not l.startswith(' '): cur=None
        LINE[(f,n)]=cur
BLOCK={};GATE={}
for f in glob.glob('game/room13_v111*.rpy'):
    cur=None
    for l in open(f):
        m=re.match(r'label (\w+)',l)
        if m: cur=m.group(1)
        for b in re.findall(r"r13_nw_block\('(\w+)'\)",l):
            if cur: BLOCK.setdefault(b,cur)
        for g in re.findall(r"r13_v111_wait\(['\"](\w+)['\"]",l):
            if cur: GATE.setdefault(g,cur)
def tag_of(cells):
    text=' '.join(str(c) for c in cells if c is not None)
    for l in re.findall(r'r13_v111_\w+',text):
        if l in L: return L[l]
    for m in re.findall(r'MS14_(D\d\d_[A-Z0-9_]+?)_L\d{4}',text):
        if 'MS14_'+m in S: return S['MS14_'+m]
    for m in re.findall(r'\bMS14_(D\d\d_[A-Z0-9_]+?)\b',text):
        if 'MS14_'+m in S: return S['MS14_'+m]
    for b in re.findall(r'blocks\.(\w+)',text):
        if BLOCK.get(b) in L: return L[BLOCK[b]]
    for f,n in re.findall(r'(room13_v111\w*\.rpy):(\d+)',text):
        lab=LINE.get((f,int(n)))
        if lab in L: return L[lab]
    for m in re.findall(r'\b(D\d\d-[A-Z0-9]+)',text):
        if B.get(m): return B[m]
    for w in re.findall(r'\b([a-z][a-z0-9_]{3,})\b',text):   # 접두어 없는 관문·라벨 이름(field-bindings)
        if 'r13_v111_'+w in L: return L['r13_v111_'+w]
    for w in re.findall(r'\b([a-z][a-z0-9_]{3,})\b',text):   # 관문 이름 -> 그 관문에서 기다리는 라벨
        if GATE.get(w) in L: return L[GATE[w]]
    if re.search(r'newworld_text\.rpy|newworld_rules\.rpy|meeting_stage|room13_v111\.rpy',text): return 'COMMON'
    return None
wb=openpyxl.load_workbook(SRC)
for ws in wb.worksheets:
    if ws.title=='테스트': hdr=next(r for r in range(1,20) if ws.cell(r,1).value=='테스트 ID')
    else: hdr=next((r for r in range(1,15) if sum(1 for c in ws[r] if c.value not in (None,''))>=4),None)
    if hdr is None: continue
    col=ws.max_column+1
    h=ws.cell(hdr,col,'사건 태그'); src=ws.cell(hdr,col-1)
    h.font=copy(src.font); h.fill=copy(src.fill); h.border=copy(src.border); h.alignment=copy(src.alignment)
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width=15
    ws.auto_filter.ref=None
    n=ok=0; miss=[]
    for r in range(hdr+1,ws.max_row+1):
        vals=[ws.cell(r,c).value for c in range(1,col)]
        if not any(v not in (None,'') for v in vals): continue
        n+=1; t=tag_of(vals)
        if t: ws.cell(r,col,t); ok+=1
        else: miss.append(vals)
    print(f'{ws.title}: {ok}/{n}행'); [print('    빈칸 예',[str(x)[:50] for x in v if x][:3]) for v in miss[:3]]
ts=wb.create_sheet('사건태그',0)
ts.append(['사건 태그','사건','장면','회의 키','세부 분기(PDF·엑셀)','라벨 수'])
for c in ts[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='2F5D50')
for t,e in d['events'].items():
    ts.append([t,e['name'],', '.join(s.split('_',2)[2] for s in e['scenes']),e['meeting'] or '',', '.join(e['branches']),len(e['labels'])])
for col,w in zip('ABCDEF',(16,34,26,12,40,8)): ts.column_dimensions[col].width=w
ts.freeze_panes='A2'
wb.save(OUT)
