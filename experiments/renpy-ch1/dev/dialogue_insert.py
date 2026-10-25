"""기준 줄 바로 뒤에 새 대사 줄을 넣는다(주고받기로 쪼갤 때 쓴다).

사용: python3 dev/dialogue_insert.py 파일 — 줄 "기준ID|새ID|화자(-는 지문)|표정(-는 없음)|문장".
기준 줄이 조건부로 삭제되는 줄이면 새 줄만 남으므로 쓰지 않는다. 넣은 뒤 reanchor·story_master·dialogue_modules 를 다시 만든다.
"""
import json,sys,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'game/v111/newworld'
files={p:json.loads(p.read_text()) for p in R.glob('*.json')}
allids=set(re.findall(r'"id": "([^"]+)"',''.join(p.read_text() for p in files)))
last={}
n=0
for raw in open(sys.argv[1],encoding='utf-8'):
    raw=raw.rstrip('\n')
    if not raw.strip() or raw.startswith('#'):continue
    a,i,sp,ex,t=raw.split('|',4)
    assert i not in allids,i
    row={"id":i,"speaker":None if sp=='-' else sp,"kind":"narration" if sp=='-' else "dialogue","text":t}
    if ex!='-':row['expression']=ex
    a=last.get(a,a);done=False
    for p,d in files.items():
        if done:break
        if a.startswith('MS14_'):
            m=re.match(r'MS14_D(\d\d)_',a)
            if p.name!='d%s.json'%m.group(1):continue
            d.setdefault('after',{}).setdefault(a,[]).insert(0,row);done=True
        else:
            for sec in ('before','after','blocks'):
                for l in d.get(sec,{}).values():
                    for j,r in enumerate(l):
                        if r['id']==a:l.insert(j+1,row);done=True;break
                    if done:break
                if done:break
    assert done,a
    last[raw.split('|')[0]]=i;allids.add(i);n+=1
for p,d in files.items():
    s=json.dumps(d,ensure_ascii=False,indent=2)+'\n'
    if p.read_text()!=s:p.write_text(s)
print('삽입',n)
