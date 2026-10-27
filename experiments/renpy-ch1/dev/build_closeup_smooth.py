"""근접 대화 그림을 도트판(dialogue-dot-v2) 대신 붓 원본(dialogue-source-master-v2)으로 그릴 때 쓰는 크기표.
도트판은 원본을 N칸으로 다시 찍은 것이라 폭·높이 비율이 높이마다 다르다. 같은 자리에 같은 크기로 겹치도록
파일별 (도트 w,h, 원본 w,h) 를 적어 두고, 실행 중에는 scale = 도트 h / 원본 h 만 곱한다.
python3 dev/build_closeup_smooth.py  →  game/assets/room13-closeup-smooth.json"""
import json,os
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT/'game'
DOT=GAME/'assets/dialogue-dot-v2';MASTER=GAME/'assets/dialogue-source-master-v2'
table={}
for person in sorted(os.listdir(DOT)):
    for height in sorted(os.listdir(DOT/person)):
        for f in sorted(os.listdir(DOT/person/height)):
            if not f.endswith('.webp'):continue
            dot=DOT/person/height/f;master=MASTER/person/height/f
            if not master.exists():continue
            with Image.open(dot) as a,Image.open(master) as b:
                table['assets/dialogue-dot-v2/%s/%s/%s'%(person,height,f)]=dict(master='assets/dialogue-source-master-v2/%s/%s/%s'%(person,height,f),dot=list(a.size),src=list(b.size))
(GAME/'assets/room13-closeup-smooth.json').write_text(json.dumps(table,ensure_ascii=False,indent=0)+'\n')
print('항목',len(table))
