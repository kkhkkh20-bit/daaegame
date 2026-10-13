"""Guarded dialogue-only revision. Run after the latest content generation."""
import argparse, copy, json, pathlib, shutil
HERE=pathlib.Path(__file__).resolve().parent

def apply_content(data):
    revised=copy.deepcopy(data)
    for p in json.loads((HERE/'content-patch.json').read_text(encoding='utf-8')):
        parent=revised
        for key in p['path'][:-1]:parent=parent[key]
        key=p['path'][-1]
        if parent[key]==p['after']:continue
        if parent[key] not in [p['before'],p.get('previous_after',p['before'])]+p.get('accepted_before',[]):raise ValueError('대사 원문이 달라 적용 중단: '+'.'.join(p['path']))
        parent[key]=p['after']
    return revised

def prepare(project):
    project=pathlib.Path(project); game=project/'game'; outputs={}
    content=game/'room13-content.json'
    outputs[content]=json.dumps(apply_content(json.loads(content.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2)+'\n'
    patches=json.loads((HERE/'runtime-patch.json').read_text(encoding='utf-8'))
    for p in patches:
        path=game/p['file'];text=outputs.get(path,path.read_text(encoding='utf-8'))
        if any(after in text for after in p.get('superseded_by', [])):continue
        if p['after'] in text:continue
        candidates=sorted(set(p.get('accepted_before',[])+[p.get('previous_after',p['before']),p['before']]),key=len,reverse=True)
        match=next((old for old in candidates if text.count(old)==1),None)
        if match is None:
            if p.get('optional_if_absent') and not any(old in text for old in candidates):continue
            raise ValueError('실행 대사 원문이 달라 적용 중단: '+p['file'])
        outputs[path]=text.replace(match,p['after'],1)
    # New scene files are isolated and guarded against unrelated local rewrites.
    for spec in json.loads((HERE/'new-files.json').read_text(encoding='utf-8')):
        path=game/spec['file']
        if path.exists() and path.read_text(encoding='utf-8') not in [spec['content']]+spec.get('accepted_before',[]):
            raise ValueError('새 대화 파일이 다른 내용으로 수정되어 적용 중단: '+spec['file'])
        outputs[path]=spec['content']
    # Keep generated content changes across rebuilds, after every existing pass.
    generator=project/'dev/build_room13_content.py'
    hook='from room13_dialogue_revision import apply_content as r13_apply_dialogue_revision\nD = r13_apply_dialogue_revision(D)\n'
    if generator.exists():
        text=generator.read_text(encoding='utf-8');anchor="(ROOT/'game/room13-content.json').write_text("
        if hook not in text:
            if text.count(anchor)!=1:raise ValueError('콘텐츠 생성기 형식이 달라 적용 중단')
            outputs[generator]=text.replace(anchor,hook+anchor,1)
        outputs[project/'dev/room13_dialogue_revision.py']=pathlib.Path(__file__).read_text(encoding='utf-8')
        outputs[project/'dev/content-patch.json']=(HERE/'content-patch.json').read_text(encoding='utf-8')
        # Runtime text edits remain on .rpy; the hook imports only apply_content.
        outputs[project/'dev/runtime-patch.json']=(HERE/'runtime-patch.json').read_text(encoding='utf-8')
    return outputs

def install(project,write=False):
    outputs=prepare(project) # all guard checks complete before the first write
    if write:
        backup=pathlib.Path(project)/'dialogue-backup-20261013'
        for path,text in outputs.items():
            if path.exists() and path.read_text(encoding='utf-8')==text:continue
            if path.exists():
                target=backup/path.relative_to(project);target.parent.mkdir(parents=True,exist_ok=True)
                if not target.exists():shutil.copy2(path,target)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
            if path.suffix=='.rpy':path.with_suffix('.rpyc').unlink(missing_ok=True)
    print(('APPLIED' if write else 'DRY RUN'),len(outputs),'files; story conditions and costs unchanged')
    return outputs

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--project',required=True,type=pathlib.Path);a.add_argument('--write',action='store_true');args=a.parse_args();install(args.project,args.write)
