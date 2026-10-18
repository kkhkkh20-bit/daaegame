#!/usr/bin/env python3
"""Read-only resource index. No Ren'Py code is executed; unresolved branches stay unknown."""
import argparse, ast, hashlib, json, os, re, shutil, subprocess, textwrap
from functools import lru_cache
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GAME_REL = Path('experiments/renpy-ch1/game')
EMOTIONS = ['neutral','joy','angry','anxious','surprise_talk','surprise_react']

def python_blocks(text, errors=None):
    lines=text.splitlines(); i=0
    while i<len(lines):
        if re.match(r'^init(?:\s+-?\d+)?\s+python(?:\s+in\s+\w+)?:',lines[i]):
            start=i+1; i=start
            while i<len(lines) and not re.match(r'^(?:init|label|screen|transform|default|define|style|image)\b',lines[i]): i+=1
            try: yield ast.parse('\n'.join(line[4:] if line.startswith('    ') else line for line in lines[start:i])),start
            except SyntaxError as exc:
                if errors is not None:errors.append(dict(line=start+(exc.lineno or 1),error=exc.msg))
        else:i+=1

def literal_tables(text):
    result={}
    for tree,_ in python_blocks(text):
        for node in tree.body:
            if isinstance(node,ast.Assign):
                try: value=ast.literal_eval(node.value)
                except (ValueError,TypeError):continue
                for t in node.targets:
                    if isinstance(t,ast.Name):result[t.id]=value
    return result

def declared_days(row):
    return [day for day in range(max(1,row.get('min_day',1)),min(14,row.get('max_day',14))+1) if 'days' not in row or day in row['days']]

def build(repo=REPO, output=None):
    subprocess_blob_hash.cache_clear()
    repo=Path(repo); game=repo/GAME_REL; output=Path(output or repo/'preview/resource-dashboard');output.mkdir(parents=True,exist_ok=True)
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    inputs={};issues=[];sources={};tables={};functions=[]
    def read(path):
        p=game/path; raw=p.read_bytes();inputs[str(GAME_REL/path)]=hashlib.sha256(raw).hexdigest();return raw.decode('utf-8-sig')
    def data(path):return json.loads(read(Path(path)))
    def ref(path,line=1,pointer=None):
        return dict(path=str(GAME_REL/path),line=line,**({'pointer':pointer} if pointer else {}))
    for p in sorted(game.rglob('*.rpy')):
        if 'qa_tests' in p.parts:continue
        rel=p.relative_to(game);text=read(rel);sources[str(rel)]=text;tables.update(literal_tables(text))
        parse_errors=[]
        for tree,offset in python_blocks(text,parse_errors):
            for n in ast.walk(tree):
                if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    functions.append(dict(name=n.name,source=ref(rel,offset+n.lineno),code='\n'.join(text.splitlines()[offset+n.lineno-1:offset+n.end_lineno])))
        issues.extend(dict(kind='unparsed_python',path=str(GAME_REL/rel),**error) for error in parse_errors)
    def code_refs(person,pose=None):
        pattern=re.compile(r'''["']'''+re.escape(person)+r'''["']''')
        out=[]
        for p,text in sources.items():
            ls=text.splitlines()
            for i,line in enumerate(ls):
                if not line.lstrip().startswith('#') and pattern.search(line) and (not pose or pose in '\n'.join(ls[max(0,i-1):i+2])):
                    out.append(dict(**ref(Path(p),i+1),code='\n'.join(ls[max(0,i-2):min(len(ls),i+3)]),resolution='unknown: static reference; surrounding branches and override chain apply'))
        return out
    def function_refs(names):return [f for f in functions if f['name'] in names]
    seen_thumbnails=set()
    def media(path,crop=None,pixel=False):
        # Only repository-relative paths; never expose local source-master paths as URLs.
        p=Path(path)
        if p.is_absolute() or '..' in p.parts:return dict(path=path,exists=False,error='unsafe/non-repository path')
        full=game/p;exists=full.is_file();row=dict(path=str(GAME_REL/p),url='../../'+str(GAME_REL/p),exists=exists)
        if exists:
            inputs[str(GAME_REL/p)]=subprocess_blob_hash(full)
            if full.suffix.lower() in ('.png','.webp','.jpg','.jpeg'):
                from PIL import Image
                key=hashlib.sha256((inputs[str(GAME_REL/p)]+str(crop)+str(pixel)).encode()).hexdigest()[:24]
                thumb=output/'thumbs'/f'{key}.webp';thumb.parent.mkdir(exist_ok=True)
                if not thumb.exists():
                    try:
                        with Image.open(full) as im:
                            im=im.convert('RGBA')
                            if crop:
                                x,y,w,h=crop;im=im.crop((x,y,x+w,y+h))
                            im.thumbnail((240,240),Image.Resampling.NEAREST if pixel else Image.Resampling.LANCZOS);im.save(thumb,'WEBP',quality=85)
                    except Exception as e:issues.append(dict(kind='thumbnail_error',path=str(p),error=str(e)))
                if thumb.exists():
                    row['thumbnail']='thumbs/'+thumb.name;seen_thumbnails.add(thumb.name)
        else:issues.append(dict(kind='missing_file',path=str(GAME_REL/p)))
        return row
    cast=data('assets/cast.json'); full=data('assets/room13-fullbody-dialogue.json')['people'];talk=data('assets/room13-dialogue-talk-art.json')['people'];special=data('assets/room13-dialogue-pose-source-art.json')['people'];profiles=data('assets/room13-profile-source-art.json')['people'];acting=data('assets/room13-pixel-acting.json')
    content=data('room13-content.json'); residents=content['residents'];village=data('village-residents.json')['profiles'];world=data('assets/room13-world-layout.json');map27=data('assets/room13-map-action27.json')['rows'];map9=data('assets/room13-map-work-nine.json')['people'];beats=data('assets/room13-dialogue-beats.json')
    characters=[]
    for person in sorted(set(cast)|set(full)|set(talk)|set(special)|set(profiles)):
        assets=[]
        def add(kind,pose,spec,source,status='registered',conditions=None,pixel=False):
            if not isinstance(spec,dict) or not spec.get('file'):return
            m=media(spec['file'],spec.get('crop'),pixel)
            assets.append(dict(kind=kind,pose=pose,style='map-dot' if pixel else 'dialogue-smooth' if kind in ('dialogue','special') else 'source',status=status if m['exists'] else 'missing',generated=m['exists'],registered=status!='generated',active_call=status=='conditional_call',runtime_observed=False,conditions=conditions or 'unknown: runtime selection / fallback',source=source,media=m,crop=spec.get('crop')))
        for pose,spec in cast.get(person,{}).items():add('profile' if pose.startswith('avatar_') else 'legacy',pose,spec,ref(Path('assets/cast.json'),pointer=f'/{person}/{pose}'),pixel=True)
        for pose,spec in acting.get(person,{}).items():add('map',pose,spec,ref(Path('assets/room13-pixel-acting.json'),pointer=f'/{person}/{pose}'),pixel=True)
        for pose,spec in full.get(person,{}).get('images',{}).items():add('fallback',pose,spec,ref(Path('assets/room13-fullbody-dialogue.json'),pointer=f'/people/{person}/images/{pose}'),conditions='Fallback only; r13_fullbody_close_art first checks dialogue beat/source profile.',pixel=bool(spec.get('cell')))
        for pose,spec in full.get(person,{}).get('poses',{}).items():add('special',pose,spec,ref(Path('assets/room13-fullbody-dialogue.json'),pointer=f'/people/{person}/poses/{pose}'),pixel=bool(spec.get('cell')))
        for pose,spec in talk.get(person,{}).get('profiles',{}).get('560',{}).get('frames',{}).items():
            add('dialogue',pose,spec,ref(Path('assets/room13-dialogue-talk-art.json'),pointer=f'/people/{person}/profiles/560/frames/{pose}'),'conditional_call',conditions='r13_dialogue_plan: approved_runtime + standing + player gaze + exact reviewed text/speaker binding; meeting/thought/pose gates. 560 thumbnail; runtime also has 760/840 profiles.')
        for pose,entry in special.get(person,{}).get('pose_profiles',{}).items():
            spec=entry.get('profiles',{}).get('560',{}).get('frames',{}).get('neutral',{})
            add('special',pose,spec,ref(Path('assets/room13-dialogue-pose-source-art.json'),pointer=f'/people/{person}/pose_profiles/{pose}'),'conditional_call',conditions='r13_dialogue_source_pose: explicit pose selection; registration is not proof of a reachable story call.')
        if person in profiles:add('profile','source-neutral',profiles[person],ref(Path('assets/room13-profile-source-art.json'),pointer=f'/people/{person}'),'conditional_call',conditions='r13_profile_source_art: avatar_neutral override; profile UI invocation required.')
        for asset in assets:
            if asset['kind']=='dialogue':
                emotion='surprise' if asset['pose'].startswith('surprise_') else asset['pose']
                evidence=[dict(source=ref(Path('assets/room13-dialogue-beats.json'),pointer='/lines/'+identity+'/'+str(index)),identity=identity,index=index,reviewed=cue.get('reviewed')) for identity,rows in beats.get('lines',{}).items() for index,cue in rows.items() if cue.get('person')==person and cue.get('emotion')==emotion and cue.get('reviewed') and (asset['pose']!='surprise_react' or cue.get('reaction'))]
                asset['call_evidence']=evidence
                if not evidence and asset['status']!='missing':asset.update(status='registered',active_call=False,conditions=asset['conditions']+' No reviewed cue resolved for this frame; dynamic bindings remain unknown.')
            elif asset['kind']=='special':
                evidence=code_refs(person,asset['pose']);asset['call_evidence']=evidence
                if not evidence and asset['status']!='missing':asset.update(status='registered',active_call=False)
        placements=[]
        for filename,rows,selector in [('room13-map-action27.json',map27,'r13_map27_variant'),('room13-map-work-nine.json',map9,'r13_map_work_nine_allowed')]:
            for index,row in enumerate(rows):
                if row['person']!=person:continue
                registered=row.get('status','approved')=='approved'
                add('map',row['pose'],row['spec'],ref(Path('assets')/filename,pointer=f'/{"rows" if rows is map27 else "people"}/{index}'),'conditional_call' if registered else 'generated',conditions='Existing resident required; selector guards and upstream schedule/offer/pose checks apply.',pixel=True)
                placements.append(dict(row,source=ref(Path('assets')/filename,pointer=f'/{index}'),guards=function_refs([selector]),resolution='conditional: upstream resident presence and override chain unknown',days=declared_days(row),capture_status='실제 캡처 없음',maps={k:media(v) for k,v in world.get(row['location'],{}).get('files',{}).items()}))
        seori_path=Path('assets/room13-seori-review-art.json')
        if person=='resident_seori' and (game/seori_path).exists():
            review=data(seori_path)
            add('map',review['pose'],review['spec'],ref(seori_path),'conditional_call',conditions='Existing clinic living_notes actor; morning/evening only; no active offer; loadable source. Actual weekly location can be store/school.',pixel=True)
            placements.append(dict(person=person,pose=review['pose'],location='clinic',periods=[0,2],days=list(range(1,15)),source=ref(seori_path),guards=function_refs(['r13_stage_people']),resolution='conditional: replaces an existing clinic actor only; no schedule invention',capture_status='실제 캡처 없음',maps={k:media(v) for k,v in world.get('clinic',{}).get('files',{}).items()}))
        schedule=residents.get(person,{}).get('weekly_locations');override=tables.get('R13_WEEKLY_ROUTINES',{}).get(person)
        if override:schedule=override
        weekly=[dict(day=d,period=p,location=schedule[(d-1)%7][p],resolution='base schedule only; runtime overrides unknown') for d in range(1,15) for p in range(3)] if schedule and len(schedule)==7 else []
        name=tables.get('R13_NAMES',{}).get(person) or residents.get(person,{}).get('name') or village.get(person,{}).get('name') or full.get(person,{}).get('name_ko') or person
        characters.append(dict(id=person,name=name,assets=assets,placements=placements,schedule=weekly,profile={k:v for k,v in residents.get(person,village.get(person,{})).items() if k in ('name','work','protects','activity','role','public_purpose')},references=code_refs(person),schedule_code=function_refs(['r13_where','r13_resident_where','r13_w2_where']),captures=[],schedule_source=ref(Path('room13_life.rpy')) if override else ref(Path('room13-content.json'),pointer='/residents/'+person+'/weekly_locations')))
    # Existing real QA captures: only explicit machine-recorded person/speaker/actor fields.
    # A matching filename alone never proves that a character appears in a screenshot.
    by_id={c['id']:c for c in characters}
    for p in sorted((repo/'reports').rglob('*.json')):
        shot=p.with_suffix('.png')
        if not shot.exists():continue
        try:j=json.loads(p.read_text())
        except (ValueError,UnicodeError):continue
        if not isinstance(j,dict) or not j.get('screens'):continue
        room=j.get('room',{});found=set()
        def explicit(v):
            if isinstance(v,dict):
                for k,x in v.items():
                    if k in ('person','speaker') and isinstance(x,str) and x in by_id:found.add(x)
                    if k not in ('room','buttons'):explicit(x)
            elif isinstance(v,list):
                for x in v:explicit(x)
        explicit(j)
        for who in found:
            inputs[str(p.relative_to(repo))]=hashlib.sha256(p.read_bytes()).hexdigest()
            inputs[str(shot.relative_to(repo))]=subprocess_blob_hash(shot)
            actor=next((a for a in j.get('actors',[]) if a.get('person')==who),j.get('actor',{}))
            by_id[who]['captures'].append(dict(url='../../'+str(shot.relative_to(repo)),evidence=str(p.relative_to(repo)),day=room.get('day'),period=room.get('period'),location=room.get('location'),screens=j['screens'],game_commit=j.get('game_commit','unknown'),pose=actor.get('pose'),actor=actor,archive_sha256=j.get('archive_sha256'),capture_kind=j.get('capture_kind','historical QA'),label='실제 엔진 QA 캡처 · 상태 fixture / 현재 source commit 일치 미검증'))
    for c in characters:
        for placement in c['placements']:
            placement['captures']=[capture for capture in c['captures'] if capture.get('pose')==placement['pose'] and capture['location']==placement['location']]
            if placement['captures']:placement['capture_status']='해당 포즈의 실제 엔진 fixture 캡처 있음; 전체 날짜/조건 검증 아님'
    sound_source=Path('systems/room13_sound.rpy');sound=sources[str(sound_source)];sound_tables=literal_tables(sound);audio=[]
    for group,table in [('BGM',sound_tables.get('R13_BGM',{})),('환경음',sound_tables.get('R13_AMBIENCE',{})),('효과음',{k:'assets/'+v+'.wav' for k,v in sound_tables.get('R13_FX',{}).items()})]:
        for key,path in table.items():
            usages=[]
            for bg,(tracks,amb) in sound_tables.get('R13_PLACE_SOUND',{}).items():
                for slot,track in enumerate(tracks):
                    if group=='BGM' and track==key:usages.append(dict(place=bg,condition=['calm','search','night'][slot],note='mood slot, not a guaranteed morning/afternoon/evening schedule',source=ref(sound_source)))
                if group=='환경음' and amb==key:usages.append(dict(place=bg,condition='ambient place rule',source=ref(sound_source)))
            for (bg,title),(track,amb) in sound_tables.get('R13_SCENE_SOUND',{}).items():
                if (group=='BGM' and track==key) or (group=='환경음' and amb==key):usages.append(dict(place=bg,condition=title,source=ref(sound_source)))
            calls=[]
            pattern=re.compile(r'''(?:source_fx|r13_fx_path)\(\s*["']'''+re.escape(key)+r'''["']''')
            for p,t in sources.items():
                for i,line in enumerate(t.splitlines()):
                    if pattern.search(line):calls.append(dict(**ref(Path(p),i+1),code=line.strip()))
            audio.append(dict(id=group+':'+key,key=key,group=group,media=media(path),usages=usages,calls=calls,source=ref(sound_source),loop=False if group=='효과음' else True if group=='환경음' else 'unknown: inspect scene music call',volume=(1.0 if key=='heartbeat' else .55) if group=='환경음' else ('r13_scene: .5 if mood == quiet else 1.0; user mixer applies' if group=='BGM' else 'unknown: channel/settings dependent'),resolver=function_refs(['r13_sound_choice','r13_sound_scene_music','r13_sound_ambience','source_fx']) ))
    credits=read(Path('assets/music-v6-credits.txt'))
    for a in audio:
        credit=re.search(r'^'+re.escape(Path(a['media']['path']).name)+r'\s+(.+?)\s+—\s+(.+?)\s+(https?://\S+)',credits,re.M)
        if credit:a.update(track_title=credit[1],artist=credit[2],credit_url=credit[3],credit_source=ref(Path('assets/music-v6-credits.txt')))
        a['resolver']=a['resolver']+[dict(name='r13_scene music playback/volume',source=ref(Path('room13.rpy'),7),code='\n'.join(sources['room13.rpy'].splitlines()[6:39]))]
    used={a['media']['path'] for c in characters for a in c['assets']}|{a['media']['path'] for a in audio}
    # File inventory is generated independently; unlinked means this extractor did not resolve a link.
    orphan=[]
    for p in sorted((game/'assets').rglob('*')):
        if p.suffix.lower() not in ('.png','.webp','.jpg','.wav','.mp3','.ogg'):continue
        rel=str(p.relative_to(repo))
        if rel not in used:orphan.append(dict(path=rel,status='unresolved',note='미사용 확정 아님: 이 인덱스에서 캐릭터/음향 연결 미해결'))
    for source_file in [Path(__file__),Path(__file__).with_name('gallery.py'),*(Path(__file__).parent/'web').iterdir(),*(Path(__file__).parent/'gallery').iterdir()]:
        inputs[str(source_file.relative_to(repo))]=subprocess_blob_hash(source_file)
    version=hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest()
    result=dict(schema=1,game_commit=sha,data_version=version,generated_at=datetime.fromtimestamp(int(os.environ['SOURCE_DATE_EPOCH']),timezone.utc).isoformat() if os.environ.get('SOURCE_DATE_EPOCH') else datetime.now(timezone.utc).isoformat(),characters=characters,audio=audio,unresolved_assets=orphan,issues=issues,inputs=inputs,limitations=['Static source index, not a RenPy state evaluator. Conditional calls do not prove runtime reachability.','All function override layers are retained as evidence. Unknown conditions are not evaluated.','Existing QA screenshots are historical unless their recorded game commit matches.','Generated art outside game/assets is not exhaustively indexed.'])
    details=output/'characters';details.mkdir(exist_ok=True)
    index_characters=[]
    for c in characters:
        (details/(c['id']+'.json')).write_text(json.dumps(c,ensure_ascii=False,separators=(',',':'))+'\n')
        hero=next((a for a in c['assets'] if a['kind']=='profile' and a['pose']=='source-neutral'),next(iter(c['assets']),None))
        index_characters.append(dict(id=c['id'],name=c['name'],hero=hero,detail_url='characters/'+c['id']+'.json',asset_count=len(c['assets']),dialogue_count=sum(a['kind']=='dialogue' for a in c['assets']),placement_count=len(c['placements']),captures=[{k:v for k,v in capture.items() if k!='actor'} for capture in c['captures']],statuses=sorted({a['status'] for a in c['assets']}),search=json.dumps([c['name'],c['id'],c['profile'],[(a['pose'],a['media']['path']) for a in c['assets']]],ensure_ascii=False).lower(),schedule=c['schedule'],placements=[dict({k:p[k] for k in ('location','days','periods','pose','capture_status')},activity=p.get('activity'),media=next((a['media'] for a in c['assets'] if a['kind']=='map' and a['pose']==p['pose']),None)) for p in c['placements']]+[dict(location=cap['location'],days=[cap['day']],periods=[cap['period']],pose=cap['pose'],capture_status='실제 엔진 fixture 관측 · 이 날짜/시간만 확인',media=next((a['media'] for a in c['assets'] if a['kind']=='map' and a['pose']==cap['pose']),None)) for cap in c['captures'] if cap['pose'] and not any(p['pose']==cap['pose'] for p in c['placements'])]))
    index=dict(result,characters=index_characters,audio=[{k:v for k,v in a.items() if k!='resolver'} for a in audio])
    index['audio_resolver']=audio[0]['resolver'] if audio else []
    (output/'data.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n')
    (output/'version.json').write_text(json.dumps({k:result[k] for k in ('schema','game_commit','data_version','generated_at')})+'\n')
    (output/'errors.json').write_text(json.dumps(dict(issues=issues,limitations=result['limitations']),ensure_ascii=False,indent=2)+'\n')
    for p in (output/'thumbs').glob('*.webp'):
        if p.name not in seen_thumbnails:p.unlink()
    for p in (Path(__file__).parent/'web').iterdir():shutil.copy2(p,output/p.name)
    gallery_spec=importlib.util.spec_from_file_location('dashboard_gallery',Path(__file__).with_name('gallery.py'))
    gallery_module=importlib.util.module_from_spec(gallery_spec);gallery_spec.loader.exec_module(gallery_module);gallery_module.install(repo)
    print(json.dumps(dict(commit=sha,characters=len(characters),audio=len(audio),issues=len(issues),output=str(output)),ensure_ascii=False))
    return result

@lru_cache(maxsize=None)
def subprocess_blob_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();build(output=args.output)
