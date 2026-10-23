"""대사 기계 검사 (2026-10-23): 읽지 않고 잡히는 것만 싸게 찾는다.
Ren'Py 치환 함정([ { %), 따옴표 짝, 흔한 맞춤법, 말줄임 혼용, 연속 중복, 인사말, 긴 줄.
연속 중복은 분기 때문에 실제로는 한 번만 나올 수 있으니 dialogue_day.py show 로 확인한다.
  python3 dev/dialogue_sweep.py
"""
import json,glob,re,collections,os,sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','game'))
rows=[]  # (where, speaker, text)
def walk(o,path,f):
    if isinstance(o,dict):
        if isinstance(o.get('text'),str): rows.append((f+':'+path,o.get('speaker'),o['text']))
        for k,v in o.items(): walk(v,path+'/'+str(k),f)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+f'[{i}]',f)
for f in sorted(glob.glob('v111/newworld/*.json')): walk(json.load(open(f)),'',os.path.basename(f))
# rpy: 튜플 ("화자","대사") / say 문
tup=re.compile(r'\(\s*(None|"[^"\n]*"|\'[^\'\n]*\')\s*,\s*"((?:[^"\\\n]|\\.)*)"')
for f in sorted(glob.glob('room13_v111*.rpy')):
    for n,l in enumerate(open(f),1):
        for m in tup.finditer(l):
            t=m.group(2)
            if re.search('[가-힣]',t): rows.append((f'{f}:{n}',m.group(1).strip('"\''),t))
print('대사 수',len(rows))
spk=collections.Counter(r[1] for r in rows)
print('화자 빈도(5회 이하):',[(k,v) for k,v in spk.items() if v<=5])
out=collections.defaultdict(list)
spell=['됬','몇일','어떻해','할께','될께','줄께','되요','안되요','웬지 ','금새','어의없','희안','왠만','설겆','바램','되서 ','않되','오랫만','일일히','깨끗히','곰곰히','어떡게','역활','건들이']
greet=re.compile(r'또 오셨|어서 오세요|반가워요|안녕하세요')
for w,s,t in rows:
    u=t.replace('[[','').replace('{{','')
    if re.search(r'\[(?!\[)',u) : out['Ren\'Py [ ] 치환 위험'].append((w,t))
    if re.search(r'\{(?!/?(i|b|w|p|nw|fast|color|size|s|u|a|k|cps|alpha|font|image|space|vspace|outlinecolor|=)\b)',u): out['{ } 태그 의심'].append((w,t))
    if re.search(r'%(?!%)',t): out['% 기호'].append((w,t))
    for a,b in ['“”','‘’','()','「」','『』']:
        if t.count(a)!=t.count(b): out['괄호·따옴표 짝'].append((w,t));break
    for x in spell:
        if x in t: out['맞춤법 의심 '+x.strip()].append((w,t))
    if '  ' in t: out['이중 공백'].append((w,t))
    if re.search(r'\.\.\.|…(?!…)',t) and '……' not in t: out['말줄임 표기 혼용(... 또는 … 한 개)'].append((w,t))
    if greet.search(t): out['인사말(긴장 장면 확인 필요)'].append((w,t))
    if len(t)>90: out['90자 넘는 줄'].append((w,t))
    if not t.strip(): out['빈 대사'].append((w,t))
prev=None
for r in rows:
    if prev and r[2]==prev[2] and r[1]==prev[1]: out['연속 중복'].append((r[0],r[2]))
    prev=r
for k,v in out.items():
    print(f'\n## {k} ({len(v)})')
    for w,t in v[:6]: print(' ',w,'|',t[:100])
