"""다람 일반 6표정·활성 몸짓 8종을 원본 해상도 그대로 연결한다.

기본은 원본·표시 계약 검증이며 --apply일 때만 q95 WebP와 다람 등록을 쓴다.
기존 마차·현장·작업 그림, 비활성 몸짓 04/07, 대사 바인딩은 수정하지 않는다.
"""
import argparse
import copy
import hashlib
import io
import json
import math
from pathlib import Path

from PIL import Image

from import_art import encode

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/daram-consistency-20261107'
SOURCE=ART/'source'
REVISION='daram-consistency-20261107'
RUNTIME='assets/dialogue-player-facing/'+REVISION
VISIBLE_HEIGHT_840=494.293333
QUESTION_VISIBLE_HEIGHT=560.0*2/3
GENERAL=('neutral','joy','angry','anxious','flustered','surprise_talk')
CONTEXT=('intake21_01_bravado','intake21_02_reproach_lean','intake21_03_stubborn',
         'intake21_05_playful_evasion','intake21_06_eureka','intake21_08_scared_brave',
         'intake21_09_wipe_tears','intake21_10_resolve')
INACTIVE=('intake21_04_flustered','intake21_07_delighted')


def read_source(path):
    with Image.open(path) as image:
        if image.mode!='RGBA' or image.width<1024 or image.height<1536:
            raise ValueError('투명 고해상도 원본 필요: '+str(path))
        alpha=image.getchannel('A')
        bounds=alpha.point(lambda a:255 if a>=40 else 0).getbbox()
        if not bounds or bounds[0]<=0 or bounds[1]<=0 or bounds[2]>=image.width or bounds[3]>=image.height:
            raise ValueError('전신 잘림 또는 배경 검수 필요: '+str(path))
        if any(alpha.getpixel(p)>4 for p in ((0,0),(image.width-1,0),(0,image.height-1),(image.width-1,image.height-1))):
            raise ValueError('모서리가 불투명함: '+str(path))
        return dict(size=list(image.size),bounds=list(bounds),source_master=path.relative_to(ROOT).as_posix(),
                    source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def build_profiles(sources):
    if set(sources)!=set(GENERAL+CONTEXT):raise ValueError('일반6·활성몸짓8 원본이 모두 필요하다')
    profiles={}
    for height in (560,760,840):
        visible=QUESTION_VISIBLE_HEIGHT if height==560 else VISIBLE_HEIGHT_840*height/840
        scales={key:visible/(row['bounds'][3]-row['bounds'][1]) for key,row in sources.items()}
        width=max((row['bounds'][2]-row['bounds'][0])*scales[key] for key,row in sources.items())
        canvas=[math.ceil(width)+48,math.ceil(visible)+48]
        frames={}
        for key,row in sources.items():
            left,top,right,bottom=row['bounds'];scale=scales[key]
            if height==840 and scale*1302/840>1:raise ValueError('1302에서 원본을 확대함: '+key)
            frames[key]=dict(file=row['file'],offset=[round(canvas[0]/2-(left+right)*scale/2),round(canvas[1]-24-bottom*scale)],
                             scale=round(scale,9),nearest=False,native_detail=True,anchor=[(left+right)/2,bottom],
                             source_master=row['source_master'],source_sha256=row['source_sha256'])
        profile=dict(canvas=canvas,frames=frames)
        if height==560:
            feet=max(frames[k]['offset'][1]+row['bounds'][3]*frames[k]['scale'] for k,row in sources.items())
            # 질문에서는 어른의 2/3 키이며, 같은 바닥에 서도록 위 여백을 더 준다.
            profile['question_top']=math.floor(708-feet)
        profiles[str(height)]=profile
    return profiles


def select_frames(profiles,slots):
    return {height:dict(profile,frames={slot:copy.deepcopy(profile['frames'][slot]) for slot in slots})
            for height,profile in profiles.items()}


def updated_registries(player,context,profiles):
    active={cue['slot'] for cue in context['bindings'] if cue['person']=='daram'}
    if active!=set(CONTEXT):raise ValueError('활성 다람 몸짓 바인딩이 준비 범위와 다르다')
    player=copy.deepcopy(player);context=copy.deepcopy(context)
    player['people']['daram']=dict(status='approved_runtime',stance='standing',gaze='player',
                                  art_style='storybook_source',source_kind='source_master',art_revision=REVISION,
                                  approval='소유자 승인: 1부 판매 준비의 다람 일반6·활성몸짓8 작화 통일',
                                  visible_height_840=VISIBLE_HEIGHT_840,profiles=select_frames(profiles,GENERAL))
    for slot in CONTEXT:
        key='daram:'+slot
        old=context['entries'][key]
        context['entries'][key]=dict(old,profiles=select_frames(profiles,(slot,)),batch=REVISION,
                                    previous_batch=old.get('previous_batch',old.get('batch')),art_revision=REVISION)
    return player,context


def prepare():
    sources={}
    for slot in GENERAL+CONTEXT:
        source=SOURCE/(slot+'.png')
        row=read_source(source)
        filename=('daram-flustered' if slot=='flustered' else slot)+'.webp'
        sources[slot]=dict(row,file=RUNTIME+'/'+filename)
    return sources,build_profiles(sources)


def write_json(path,data):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    sources,profiles=prepare()
    player_path=ROOT/'game/assets/room13-dialogue-player-facing.json'
    context_path=ROOT/'game/assets/room13-dialogue-context-art.json'
    player,context=updated_registries(json.loads(player_path.read_text()),json.loads(context_path.read_text()),profiles)
    if args.apply:
        for row in sources.values():
            source=ROOT/row['source_master'];data=encode(source)
            # q95는 RGB만 압축한다. 픽셀 크기와 투명도는 받은 원본 그대로여야 한다.
            with Image.open(source) as original,Image.open(io.BytesIO(data)) as runtime:
                if original.size!=runtime.size or original.getchannel('A').tobytes()!=runtime.getchannel('A').tobytes():
                    raise ValueError('원본 크기 또는 알파가 바뀜: '+str(source))
            target=ROOT/'game'/row['file'];target.parent.mkdir(parents=True,exist_ok=True)
            temporary=target.with_suffix('.webp.tmp');temporary.write_bytes(data);temporary.replace(target)
        write_json(player_path,player);write_json(context_path,context)
        write_json(ART/'import-manifest.json',dict(revision=REVISION,general_slots=list(GENERAL),context_slots=list(CONTEXT),
                   preserved_inactive_slots=list(INACTIVE),visible_height_840=VISIBLE_HEIGHT_840,
                   question_visible_height=QUESTION_VISIBLE_HEIGHT,question_feet_line=708,sources=sources,
                   unchanged=['대사·바인딩','마차8착석','현장도트','기타작업특수','다른인물등록'],
                   scope='다람 일반6·활성몸짓8만. 전체 인물·전체 특수 그림의 작화 통일을 뜻하지 않는다.'))
    print(json.dumps(dict(general=len(GENERAL),active_context=len(CONTEXT),preserved_inactive=len(INACTIVE),
                         visible_height_840=VISIBLE_HEIGHT_840,applied=args.apply),ensure_ascii=False))


if __name__=='__main__':main()
