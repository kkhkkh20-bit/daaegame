"""제작자에게 전달할 현재 역할 계약·원본·실측 캡처 묶음."""
import io
import json
import zipfile
from pathlib import Path


def source_usage(project, model, role):
    rules=model.bindings['bindings']
    rule=rules.get(role)
    if rule is None:raise ValueError('등록된 역할을 선택하세요.')
    group=rule.get('group',role)
    roles=[key for key,value in rules.items() if value.get('group',key)==group]
    terms=set(roles)
    consumers=[]
    for key in roles:
        for state in rules[key].get('states',['basic']):
            terms.add(model.resolve(key,state)['path'])
        # 파일 연결을 바꿔도 기존 화면은 원래 경로를 계속 참조한다.
        if key.startswith('file:'):terms.add(key[5:])
        for consumer in rules[key].get('consumers',[]):
            if consumer not in consumers:consumers.append(consumer)
    found=[]
    for source in (Path(project)/'game').rglob('*.rpy'):
        if 'qa_tests' in source.parts:continue
        for number,line in enumerate(source.read_text(encoding='utf-8').splitlines(),1):
            if any(term in line for term in terms):found.append(str(source.relative_to(project))+':'+str(number))
    return {'direct_references':found,'declared_consumers':consumers,'note':'같이 변경되는 역할 묶음의 정적 검색 결과입니다. 동적으로 조합되는 경로는 포함되지 않을 수 있습니다.'}


def request_zip(project, model, role):
    rules=model.bindings['bindings']
    if role not in rules:raise ValueError('등록된 역할을 선택하세요.')
    group=rules[role].get('group',role)
    roles=[key for key,rule in rules.items() if rule.get('group',key)==group]
    items=[]; files=set()
    for key in roles:
        for state in rules[key].get('states',['basic']):
            spec=model.resolve(key,state)
            items.append(dict(role=key,state=state,path=spec['path'],size=spec.get('size'),render=spec.get('render',{}),tags=spec['tags'],contract=rules[key]))
            files.add(spec['path'])
    root=(Path(project)/'game/assets').resolve()
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(files):
            source=(Path(project)/'game'/name).resolve()
            if not source.is_relative_to(root) or not source.is_file():raise ValueError('원본 파일 경로를 확인하세요.')
            archive.write(source,'originals/'+name)
        archive.writestr('usage.json',json.dumps(source_usage(project,model,role),ensure_ascii=False,indent=2))
        archive.writestr('matching.json',json.dumps({'role':role,'group':group,'items':items},ensure_ascii=False,indent=2))
        archive.writestr('제작요청.txt','다람탐정 에셋 제작 요청\n역할: '+role+'\n\nmatching.json의 상태·캔버스·crop·배율 계약을 유지하세요. 원본 가로세로 비율을 따로 늘리지 마세요. 버튼 문자는 게임에서 올립니다. 굵고 테두리 있는 귀여운 스티커 수첩 콘셉트를 유지하세요.\n표시 크기는 render의 crop 및 zoom과 연결 계약을 참고하세요. 화면에서 늘어나는 Frame은 기존 설정을 유지하세요. 고정 표시 크기가 없는 부품은 임의로 수치를 만들지 말고 적용 담당자에게 확인하세요.\n새 파일과 역할·상태·태그 목록을 ZIP으로 납품하세요. 원본 및 대사·분기는 수정하지 마세요.\n캡처가 있으면 capture.json의 생성 시각과 설정 지문을 확인하세요. 캡처는 마지막 렌더 시점 기준입니다.\n')
        preview=Path(project)/'docs/reviews/toolbox-preview'
        for source in preview.glob('*'):
            if source.is_file() and not source.is_symlink() and source.suffix in ('.png','.json'):
                archive.write(source,'reference/'+source.name)
    return output.getvalue()
