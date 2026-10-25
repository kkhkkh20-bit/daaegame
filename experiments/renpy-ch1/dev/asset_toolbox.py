"""에셋 도구함: scan / validate / serve. 게임 로직과 별도로 실행한다."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT/'game/python-packages'))
from r13_assets import Registry, AssetError

IMAGE = {'.png','.webp','.jpg','.jpeg','.svg'}
AUDIO = {'.mp3','.ogg','.wav','.opus'}
FONT = {'.otf','.ttf','.woff2'}
STATES = ('basic','pressed','selected','disabled')


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)


def scan(project=PROJECT):
    game=project/'game'; folder=game/'asset-toolbox'
    old=json.loads((folder/'catalog.json').read_text()) if (folder/'catalog.json').exists() else {'assets':{}}
    binding=json.loads((folder/'bindings.json').read_text()) if (folder/'bindings.json').exists() else {'version':1,'bindings':{}}
    catalog={'version':1,'assets':{}}
    for path in sorted((game/'assets').rglob('*')):
        ext=path.suffix.lower()
        if not path.is_file() or ext not in IMAGE|AUDIO|FONT:continue
        rel=path.relative_to(game).as_posix(); key='file:'+rel
        media='image' if ext in IMAGE else 'audio' if ext in AUDIO else 'font'
        tags={'media:'+media,'folder:'+path.parent.name,'state:basic'}
        if '/ui-' in rel or '/map-' in rel:tags.add('style:diary-b')
        name=path.stem.lower()
        kind=(media if media!='image' else
              'button' if 'button' in name or 'opt_choice' in name or path.parent.name=='ui-button-states' else
              'icon' if 'icon' in name else
              'sticker' if 'sticker' in name or path.parent.name=='map-status' else
              'evidence' if '/evidence/' in rel else
              'background' if any(t in name for t in ('panorama','background','overview','wide-','wild-','village_clean')) else
              'character' if 'fullbody' in name or 'face' in name else
              'panel' if any(t in name for t in ('panel','frame','paper','card','notebook')) else 'image')
        tags.add('kind:'+kind)
        import re
        suffix=re.match(r'^(.*)[_-](basic|pressed|selected|disabled|hover)$',path.stem)
        if suffix:
            base,state=suffix.groups()
            tags.discard('state:basic');tags.add('state:'+state)
            tags.add('pack:file/'+path.parent.relative_to(game/'assets').as_posix()+'/'+base)
        elif any(path.with_name(path.stem+'_'+state+path.suffix).exists() for state in STATES+('hover',)):
            tags.add('pack:file/'+path.parent.relative_to(game/'assets').as_posix()+'/'+path.stem)
        size=None
        if media=='image':
            try:
                with Image.open(path) as im:size=list(im.size)
            except Exception:
                if ext!='.svg':raise
                import re
                text=path.read_text()[:16384]
                match=re.search(r'viewBox=["\']\s*[\d.-]+\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)',text)
                size=[int(float(x)) for x in match.groups()] if match else [1,1]
        entry=dict(path=rel,media=media,size=size,tags=sorted(tags),render={})
        if key in old['assets']:
            entry['tags']=old['assets'][key].get('tags',entry['tags'])
            entry['render']=old['assets'][key].get('render',{})
        catalog['assets'][key]=entry
        group=key
        # 같은 승인 부품의 복사본은 한 번의 변경으로 함께 연결한다.
        if path.name in ('b_button.png','b_button_primary.png','b_panel_small.png') and '/ui-b-' in rel:
            group='shared:'+path.name
        binding['bindings'].setdefault(key,dict(label=path.stem,match=['asset:'+key],states=['basic'],media=media,canvas_size=size if media=='image' else None,group=group,refresh='restart'))

    def virtual(key,path,tags,render,group=None,label=None,states=None):
        with Image.open(game/path) as im:size=list(im.size)
        previous=old['assets'].get(key,{})
        catalog['assets'][key]=dict(path=path,media='image',size=size,tags=previous.get('tags',tags),render=dict(render,**previous.get('render',{})),label=previous.get('label',label or key))
    def role(key,label,match,states=('basic',),refresh='live',fallback=None,group=None):
        binding['bindings'].setdefault(key,dict(label=label,match=match,states=list(states),media='image',refresh=refresh,fallback=fallback or {},group=group or key))

    for family,label in [('primary','빨강 버튼'),('standard','크림 버튼'),('wide_choice','넓은 선택 버튼')]:
        pack='pack:button-states-v1/'+family
        for state in STATES:
            path='assets/ui-button-states/%s_%s.png'%(family,state)
            virtual('button.%s.%s'%(family,state),path,[pack,'kind:button','family:'+family,'state:'+state],{'crop':[4,4,232,52] if family=='wide_choice' else [12,6,136,40],'policy':'uniform','text_color':'#8b8175' if state=='disabled' else '#fff5e5' if family=='primary' else '#493324'})
        role('button.'+family,label,[pack],STATES,fallback={'hover':'basic'})

    sheet='assets/ui-b-sticker/button_sheet.png'
    for name,row in [('standard',0),('focused',1),('primary',2)]:
        key='surface.button.'+name
        virtual(key,sheet,['kind:surface','surface:'+name,'state:basic'],{'crop':[64,64+293*row,1410,292],'zoom':1/3,'frame':[27,16,27,16],'allow_frame':True})
        role(key,'공통 큰 버튼 · '+name,['asset:'+key])

    def font_role(name,path,state):
        key='file:'+path
        entry=catalog['assets'][key]
        entry['tags']=sorted(set(entry['tags'])-{'state:basic'}|{'state:'+state,'pack:font/pretendard'})
        binding['bindings'].setdefault(name,dict(label='전역 글꼴 · '+state,match=['pack:font/pretendard'],states=[state],fallback={'basic':state},media='font',refresh='restart',group='font.family'))
    font_role('font.body','assets/Pretendard-Regular.otf','regular')
    font_role('font.bold','assets/Pretendard-Bold.otf','bold')
    binding['bindings'].setdefault('font.symbols',dict(label='보조 기호 글꼴',match=['asset:file:assets/Galmuri11.ttf'],states=['basic'],media='font',refresh='restart',group='font.symbols'))

    for key,label,path in [
        ('icon.map.locked','지도 · 잠금','assets/map-status/locked.png'),
        ('icon.map.current','지도 · 현재 위치','assets/map-status/current_location.png'),
        ('icon.map.selected','지도 · 선택','assets/map-status/map_selected.png'),
        ('paper.shared','공통 종이 패널','assets/ui-b-field/b_panel_small.png'),
        ('main.logo','메인 · 제목','assets/ui-b-main/b_logo.png'),
        ('main.cast','메인 · 인물 포스터','assets/ui-b-main/b_main_cast_poster_plain.png'),
        ('map.village','지도 · 마을 배경','assets/map-village-b/village_clean.png'),
        ('panel.options','설정 · 수첩','assets/ui-b-options/b_opt_panel.png'),
        ('panel.dialogue','대사 · 수첩','assets/ui-b-dialogue/b_panel_dialogue.png'),
    ]:
        raw='file:'+path
        if raw not in catalog['assets']:continue
        original=binding['bindings'][raw]
        binding['bindings'].setdefault(key,dict(label=label,match=deepcopy(original['match']),states=['basic'],media='image',canvas_size=original['canvas_size'],group=original['group'],refresh='live' if key.startswith('icon.map.') else 'restart'))
    for family in ('primary','standard','wide_choice'):
        binding['bindings']['button.'+family].setdefault('forbid_render',['frame'])
    for name in ('standard','focused','primary'):
        binding['bindings']['surface.button.'+name].setdefault('requires_render',['frame'])
    # 실제 기본값을 검증한 뒤에만 파일을 갱신한다.
    registry=Registry(catalog,binding)
    errors=registry.validate()
    if errors:raise AssetError('\n'.join(errors[:20]))
    save(folder/'catalog.json',catalog);save(folder/'bindings.json',binding)
    return registry


def main():
    parser=argparse.ArgumentParser(description='다람탐정 에셋 도구함')
    parser.add_argument('command',choices=['scan','validate','serve'])
    parser.add_argument('--port',type=int,default=8787)
    args=parser.parse_args()
    if args.command=='scan':
        registry=scan();print('등록 에셋 %d개 · 연결 역할 %d개'%(len(registry.catalog['assets']),len(registry.bindings['bindings'])))
    elif args.command=='validate':
        folder=PROJECT/'game/asset-toolbox'
        registry=Registry(json.loads((folder/'catalog.json').read_text()),json.loads((folder/'bindings.json').read_text()))
        errors=registry.validate()
        for asset in registry.catalog['assets'].values():
            if not (PROJECT/'game'/asset['path']).is_file():errors.append('파일 없음: '+asset['path'])
        if errors:raise SystemExit('\n'.join(errors))
        print('에셋 연결·상태·비율 검증 통과')
    else:
        from asset_toolbox_server import run
        run(PROJECT,port=args.port)

if __name__=='__main__':main()
