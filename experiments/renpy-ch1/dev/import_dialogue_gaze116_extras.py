"""판설·아랫길 노인의 기존 표정과 자세를 유지한 대화용 시선 교정본 반입."""
from concurrent.futures import ProcessPoolExecutor
import json
from pathlib import Path

from import_art import encode
from import_dialogue_gaze116 import ROOT,ART,read_source
from build_closeup_smooth import APPROVED_EXTRA_MASTERS


def main():
    rows=[]
    for person,frames in APPROVED_EXTRA_MASTERS.items():
        for slot,file in frames.items():
            source=ART/person/(slot+'.png')
            row=read_source(source);row.update(person=person,emotion=slot,file=file)
            rows.append(row)
    with ProcessPoolExecutor(max_workers=4) as pool:
        for row,data in zip(rows,pool.map(encode,(ROOT/row['source_master'] for row in rows))):
            path=ROOT/'game'/row['file'];path.parent.mkdir(exist_ok=True);path.write_bytes(data)
    extra=ROOT/'game/assets/room13-dialogue-talk-art-extra.json'
    data=json.loads(extra.read_text());notes=data['source_resolution_notes']
    notes['smooth_mapping']='room13-closeup-smooth.json: 두 인물은 기존 승인 원본의 시선을 교정한 같은 크기의 대화 전용 파일을 쓴다. 현장·초상 파일은 유지한다.'
    notes['player_facing_dialogue_masters']=APPROVED_EXTRA_MASTERS
    extra.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (ART/'extras-runtime-manifest.json').write_text(json.dumps(dict(approval='소유자: 캐릭터 나를 보게 시선 바꾸고 이미지 퀄리티 체크',frames=rows),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(people=2,frames=len(rows)),ensure_ascii=False))


if __name__=='__main__':main()
