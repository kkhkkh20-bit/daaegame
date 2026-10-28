"""자동 완주 캡처(PNG + 같은 이름 JSON 의 buttons)로 버튼 글자의 위아래 여백을 잰다.
2026-10-28 소유자: "모든 정렬 이 게임에 들어가는 버튼과 대사 맞춰줘". 눈으로 보는 대신 잉크 줄로 잰다.
사용: python3 dev/qa_text_centering.py <캡처 폴더>...   → 화면·버튼별 (위 여백 - 아래 여백) 이 큰 것부터."""
import json,sys,glob,os
from collections import defaultdict
import numpy as np
from PIL import Image

def ink_rows(crop):
    # 칸 바탕색(가장 흔한 색)과 크게 다른 화소를 잉크로 본다. 테두리를 피하려고 안쪽만 본다.
    h,w,_=crop.shape
    flat=crop.reshape(-1,3)
    vals,counts=np.unique((flat//8),axis=0,return_counts=True)
    bgc=vals[counts.argmax()]*8+4
    diff=np.abs(crop-bgc).sum(axis=2)
    rows=[y for y in range(h) if (diff[y]>150).sum()>=max(2,w//80)]
    return rows

def measure(png,js):
    im=np.asarray(Image.open(png).convert('RGB')).astype(int)
    H,W,_=im.shape;sx=W/1280.0;sy=H/720.0
    st=json.load(open(js))
    out=[]
    for b in st.get('buttons',[]):
        t=(b.get('text') or '').strip()
        x,y,w,h=b['rect']
        if not t or w<60 or h<28 or h>200:continue
        pad=6
        x0,y0,x1,y1=int((x+pad)*sx),int((y+pad)*sy),int((x+w-pad)*sx),int((y+h-pad)*sy)
        if x1-x0<20 or y1-y0<12 or x0<0 or y0<0 or x1>W or y1>H:continue
        rows=ink_rows(im[y0:y1,x0:x1])
        if not rows:continue
        top=rows[0];bot=(y1-y0-1)-rows[-1]
        out.append((t.replace('\n',' ')[:24],round((top-bot)/sy,1),round(h,0)))
    return out

if __name__=='__main__':
    agg=defaultdict(list)
    for d in sys.argv[1:]:
        for js in sorted(glob.glob(os.path.join(d,'*.json'))):
            png=js[:-5]+'.png'
            if not os.path.exists(png):continue
            kind=os.path.basename(js).split('-')[1] if '-' in os.path.basename(js) else '?'
            for t,off,h in measure(png,js):agg[(kind,t)].append((off,h))
    rows=[(sum(o for o,h in v)/len(v),len(v),k) for k,v in agg.items()]
    rows.sort(key=lambda r:-abs(r[0]))
    for off,n,(kind,t) in rows[:80]:print('%+5.1f  %3d  %-8s %s'%(off,n,kind,t))
