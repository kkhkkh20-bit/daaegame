"""주행 로그의 「배치」 줄을 읽어 겹침(가로 55% 넘고 세로 절반 넘게)·화면 밖(폭의 1/3 넘게)·이름표 가림 후보를 적는다.
좌표는 화면 기준(x-오프셋). 사용: python3 dev/qa_layout_check.py <자동 완주 로그>"""
import ast,sys
log=open(sys.argv[1],encoding='utf-8').read().splitlines()
shot=None;day=None
for line in log:
    if line.startswith('===='):day=line.strip('= ')
    if line.startswith('SHOT '):shot=line[5:].strip()
    if not line.startswith('  배치 '):continue
    try:rows=ast.literal_eval(line[len('  배치 '):])
    except Exception:continue
    issues=[]
    for p,x,y,w,h,s in rows:
        # 화면 가장자리에 걸쳐 1/3 넘게 잘린 사람만 적는다. 통째로 밖이면 옆 구역(화살표로 간다)이다.
        hidden=max(0,-x)+max(0,x+w-1280)
        if w and hidden>w/3.0 and (x<1280 and x+w>0):issues.append('가장자리 %s x%d w%d'%(p,x,w))
    for i,(p,x,y,w,h,s) in enumerate(rows):
        for q,x2,y2,w2,h2,s2 in rows[i+1:]:
            if not (w and w2):continue
            cover=min(x+w,x2+w2)-max(x,x2);vert=min(y+h,y2+h2)-max(y,y2)
            if cover>0.55*min(w,w2) and vert>0.5*min(h,h2):issues.append('겹침 %s/%s 가로%d'%(p,q,cover))
    if issues:print(day,shot,'|',' ; '.join(issues))
