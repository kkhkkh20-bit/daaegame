"""근접 대화 그림을 도트판(dialogue-dot-v2) 대신 붓 원본(dialogue-source-master-v2)으로 그릴 때 쓰는 크기표.
도트판은 원본을 N칸으로 다시 찍은 것이라 폭·높이 비율이 높이마다 다르다. 같은 자리에 같은 크기로 겹치도록
파일별 (도트 w,h, 원본 w,h) 를 적어 두고, 실행 중에는 scale = 도트 h / 원본 h 만 곱한다.
python3 dev/build_closeup_smooth.py  →  game/assets/room13-closeup-smooth.json"""
import json,os
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];GAME=ROOT/'game'
# 두 인물은 기존 승인 원본의 시선만 고친 대화용 파일을 쓴다. 현장·초상 원본은 보존한다.
APPROVED_EXTRA_MASTERS={
    'npc_panseol':{e:'assets/panseol/dialogue-gaze116-%s.webp'%e for e in ('neutral','anxious','tired')},
    'v111_lowerroad_elder':{e:'assets/lowerroad-elder/dialogue-gaze116-%s.webp'%e
                          for e in ('neutral','joy','angry','anxious','flustered','surprise_talk')},
}

def build_table(game=GAME):
    dot_root=game/'assets/dialogue-dot-v2';source_root=game/'assets/dialogue-source-master-v2'
    table={}
    for person in sorted(os.listdir(dot_root)):
        for height in sorted(os.listdir(dot_root/person)):
            for f in sorted(os.listdir(dot_root/person/height)):
                if not f.endswith('.webp'):continue
                dot=dot_root/person/height/f;master=source_root/person/height/f
                if not master.exists():
                    approved=APPROVED_EXTRA_MASTERS.get(person,{}).get(Path(f).stem)
                    if not approved:continue
                    master=game/approved
                if not master.exists():continue
                with Image.open(dot) as a,Image.open(master) as b:
                    table[dot.relative_to(game).as_posix()]=dict(master=master.relative_to(game).as_posix(),dot=list(a.size),src=list(b.size))
    return table

if __name__=='__main__':
    table=build_table()
    (GAME/'assets/room13-closeup-smooth.json').write_text(json.dumps(table,ensure_ascii=False,indent=0)+'\n')
    print('항목',len(table))
