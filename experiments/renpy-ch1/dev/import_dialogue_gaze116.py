"""검수한 정면 원본을 웹 형식으로 가져온다. 그림 수정·축소는 하지 않는다.

현재 캐릭터의 근접 키는 runtime-fit-targets.json으로 보존한다.
질문용 560 프로필은 전신을 보여 주고, 일반 대사는 기존 1302 표시를 유지한다.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import math
from pathlib import Path

from PIL import Image

from import_art import encode

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/dialogue-gaze-20261107'
SLOTS=('neutral','joy','angry','anxious','flustered','surprise_talk')


def read_source(path):
    with Image.open(path) as image:
        if image.mode!='RGBA' or image.width<1024 or image.height<1536:
            raise ValueError('투명 고해상도 원본 필요: '+str(path))
        alpha=image.getchannel('A')
        bounds=alpha.point(lambda n:255 if n>=40 else 0).getbbox()
        if not bounds or bounds[0]<=0 or bounds[1]<=0 or bounds[2]>=image.width or bounds[3]>=image.height:
            raise ValueError('전신 잘림 또는 배경 확인 필요: '+str(path))
        for point in ((0,0),(image.width-1,0),(0,image.height-1),(image.width-1,image.height-1)):
            if alpha.getpixel(point)>4:raise ValueError('모서리가 불투명함: '+str(path))
        return dict(bounds=list(bounds),size=list(image.size),source_master=path.relative_to(ROOT).as_posix(),
                    source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def build_profiles(sources,visible_height_840):
    profiles={}
    for height in (560,760,840):
        visible=560 if height==560 else visible_height_840*height/840
        scales={slot:visible/(row['bounds'][3]-row['bounds'][1]) for slot,row in sources.items()}
        width=max((row['bounds'][2]-row['bounds'][0])*scales[slot] for slot,row in sources.items())
        canvas=[math.ceil(width)+48,math.ceil(visible)+48]
        feet=canvas[1]-24
        frames={}
        for slot,row in sources.items():
            left,top,right,bottom=row['bounds'];scale=scales[slot]
            frames[slot]=dict(file=row['file'],offset=[round(canvas[0]/2-(left+right)*scale/2),round(feet-bottom*scale)],
                              scale=round(scale,9),nearest=False,native_detail=True,anchor=[(left+right)/2,bottom],
                              source_master=row['source_master'],source_sha256=row['source_sha256'])
        profiles[str(height)]=dict(canvas=canvas,frames=frames)
    return profiles


def normalize_question_layout(people):
    """픽셀 좌표를 정수로 고정하고 실제 알파 경계로 질문용 발끝을 화면 안에 둔다."""
    for entry in people.values():
        if entry.get('status')!='approved_runtime':continue
        for profile in entry['profiles'].values():
            for frame in profile['frames'].values():
                frame['offset']=[round(v) for v in frame['offset']]
        question=entry['profiles']['560']
        feet=[]
        for frame in question['frames'].values():
            with Image.open(ROOT/'game'/frame['file']) as image:
                box=image.convert('RGBA').getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
            feet.append(frame['offset'][1]+box[3]*frame.get('scale',1))
        question['question_top']=min(118,math.floor(708-max(feet)))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    targets=json.loads((ART/'runtime-fit-targets.json').read_text())
    prepared={}
    for person,target in targets.items():
        sources={}
        for slot in SLOTS:
            path=ART/person/(slot+'.png')
            row=read_source(path)
            filename=(person+'-flustered' if slot=='flustered' else slot)+'.webp'
            row['file']='assets/dialogue-player-facing/gaze116/'+person+'/'+filename
            sources[slot]=row
        profiles=build_profiles(sources,target['visible_height_840'])
        for frame in profiles['840']['frames'].values():
            # 달그락은 기존 근접 키와 새 전신 여백을 보존하면 약1.03배가 된다.
            # 새 그림을 크게 늘리는 연결은 막되, 키를 줄이거나 여백을 없애지 않는다.
            if frame['scale']*1302/840>1.05:
                raise ValueError('일반 대사에서 원본을 5% 넘게 확대함: '+person)
        prepared[person]=dict(status='approved_runtime',stance='standing',gaze='player',art_style='storybook_source',
                              source_kind='source_master',art_revision='gaze-quality-20261107',
                              approval='소유자: 캐릭터 나를 보게 시선 바꾸고 이미지 퀄리티 체크',profiles=profiles)
    if args.apply:
        frames=[frame for entry in prepared.values() for frame in entry['profiles']['840']['frames'].values()]
        # 독립된 원본 압축만 병렬로 계산하고, 파일·연결표 쓰기는 순서대로 마친다.
        with ProcessPoolExecutor(max_workers=4) as pool:
            for frame,data in zip(frames,pool.map(encode,(ROOT/frame['source_master'] for frame in frames))):
                target=ROOT/'game'/frame['file'];target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(data)
        registry=ROOT/'game/assets/room13-dialogue-player-facing.json'
        data=json.loads(registry.read_text());data['people'].update(prepared)
        normalize_question_layout(data['people'])
        registry.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(people=len(prepared),frames=len(prepared)*len(SLOTS),applied=args.apply),ensure_ascii=False))


if __name__=='__main__':main()
