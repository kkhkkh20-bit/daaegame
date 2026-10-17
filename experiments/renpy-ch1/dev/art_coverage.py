"""Reconcile runtime art, canonical sources and outstanding requests without rendering claims.

python3 dev/art_coverage.py [--check]
Human screen reviews belong in docs/art-coverage/reviews.json, with evidence and asset hash.
"""
import argparse
import ast
import collections
import csv
import hashlib
import io
import json
import re
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'
OUT = ROOT / 'docs/art-coverage'
EMOTIONS = ('neutral', 'joy', 'flustered', 'angry', 'anxious', 'surprise')
PERIODS = ('morning', 'afternoon', 'evening')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()[:12]


def init_trees(path):
    """Parse Python init blocks without executing Ren'Py or evaluating conditions."""
    lines = path.read_text().splitlines(True)
    for i, line in enumerate(lines):
        if re.match(r'^init(?:\s+-?\d+)?\s+python:', line):
            end = i + 1
            while end < len(lines) and (not lines[end].strip() or lines[end][0].isspace() or lines[end].startswith('#')):
                end += 1
            try:
                yield ast.parse(textwrap.dedent(''.join(lines[i+1:end]))), i + 1
            except SyntaxError:
                continue


def assignment(path, name):
    for tree, offset in init_trees(path):
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                return node.value, offset + node.lineno
    raise ValueError((path, name))


def build():
    cast = load(GAME / 'assets/cast.json')
    fb = load(GAME / 'assets/room13-fullbody-dialogue.json')['people']
    acting = load(GAME / 'assets/room13-pixel-acting.json')
    portraits = load(GAME / 'assets/room13-portraits.json')
    layouts = load(GAME / 'assets/room13-world-layout.json')
    canon = {r['roleId']: r for r in csv.DictReader(io.StringIO((ROOT / 'art/canonical48-rev45/canonical48.csv').read_text(encoding='utf-8-sig')))}
    approved = load(ROOT / 'art/role-connect-20261016/registry.json')['roles']
    action_registry = load(ROOT / 'art/map-actions-20261015/registry.json')['poses']
    historical = list(csv.DictReader(io.StringIO((ROOT / 'docs/ART_REQUEST_P0P1_20261016.csv').read_text(encoding='utf-8-sig'))))
    prior_pending = load(ROOT / 'art/canonical-channel-alignment-20261017/report.json')
    reviews = load(OUT / 'reviews.json')
    items = {}
    hashes = {}

    def file_hash(file):
        if file not in hashes:
            p = GAME / file
            hashes[file] = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
        return hashes[file]

    def reference(person):
        row = approved.get(person, {})
        if row.get('mode') == 'pixel_set':
            source = row['dialogue']['neutral']['source']
        else:
            source = row.get('source')
        if source:
            path = (ROOT / 'art/role-connect-20261016' / source).resolve().relative_to(ROOT)
            return {'path': str(path), 'decision': row.get('decision'), 'version': row['version']}
        if person == 'resident_nero':
            return {'path': 'art/nero-grey-lynx-originals/fullbody/neutral.png', 'decision': '회색 털·남색 망토·금색 브로치, 은색 늑대 미배정'}
        if person in canon:
            return {'path': 'art/canonical48-rev45/originals/' + person + '.webp', 'sha256': canon[person]['sha256'], 'decision': '48명 확정 시트; 할머니 원본·나비 교복 보존'}
        return {'path': 'art/ep-art-20261016/registry.json', 'decision': '추가 에피소드 인물; 개별 원본과 승인 이력 확인 필요'}

    def add(key, kind, person=None, location=None, period=None, condition=None, requirement='', files=(), production='available_unreviewed', connection='linked', priority='P2', evidence=(), **extra):
        files = sorted(set(f for f in files if f))
        assets = [{'file': f, 'exists': (GAME / f).is_file(), 'sha256': file_hash(f)} for f in files]
        if any(not a['exists'] for a in assets):
            connection = 'broken_path'
        review = reviews.get(key)
        context_hash = hashlib.sha256(json.dumps([key,location,period,condition,requirement,extra],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        verified = bool(review and review.get('evidence') and review.get('asset_hashes') == {a['file']: a['sha256'] for a in assets} and review.get('context_sha256') == context_hash and review.get('status') == 'passed')
        items[key] = dict(id=key, kind=kind, character=person, character_name=canon.get(person, {}).get('roleName', fb.get(person, {}).get('name_ko')), location=location,
            period=period, event_condition=condition, requirement=requirement, current_assets=assets,
            canonical_reference=reference(person) if person else None, production_status=production, connection_status=connection,
            screen_review={'status': 'passed' if verified else 'not_run', 'evidence': review.get('evidence') if verified else None},
            priority=priority, next_action={'available_unreviewed':'render_and_review','not_produced':'produce_from_approved_reference','needs_correction':'correct_existing_from_approved_reference','needs_reconciliation':'resolve_requirement_and_existing_assets','candidate_held':'await_design_approval','runtime_effect':'verify_state_transition'}.get(production,'resolve_requirement'),
            source_evidence=list(evidence), context_sha256=context_hash, **extra)

    for person in sorted(set(cast) | set(fb)):
        entry = fb.get(person, {})
        images = entry.get('images', {})
        for emotion in EMOTIONS:
            image = images.get(emotion, {})
            neutral = images.get('neutral', {})
            file = image.get('file') or neutral.get('file')
            same = emotion != 'neutral' and file and file_hash(file) == file_hash(neutral.get('file', ''))
            pending = same or image.get('fallback') or not image
            correction = person == 'guard' and emotion != 'neutral' and not image.get('review_batch')
            add(f'character/{person}/dialogue/{emotion}', 'dialogue_expression', person, requirement=emotion,
                files=[file], production='needs_correction' if correction else ('not_produced' if pending else 'available_unreviewed'),
                connection='neutral_fallback' if pending else 'linked', priority='P0' if person in ('guard','resident_teacher','neoul') and (correction or pending) else ('P1' if pending else 'P2'),
                evidence=['game/assets/room13-fullbody-dialogue.json'], canonical_roster=person in canon,
                geometry={k: entry.get(k) for k in ('crop','figure','pixel')}, image_geometry={k:image[k] for k in ('crop','map','cell') if k in image})
        for channel, table in (('investigation', acting), ('profile', portraits), ('cast', cast), ('dialogue_pose', {p:v.get('poses', {}) for p,v in fb.items()})):
            for pose, spec in table.get(person, {}).items():
                if not isinstance(spec, dict) or not spec.get('file'):
                    continue
                add(f'character/{person}/{channel}/{pose}', channel, person, requirement=pose, files=[spec['file']],
                    production='needs_correction' if person == 'guard' and channel == 'investigation' and pose not in ('neutral',) and not pose.startswith('avatar_') else 'available_unreviewed',
                    evidence=[f'game/assets/{"room13-pixel-acting.json" if channel == "investigation" else "cast.json" if channel == "cast" else "room13-portraits.json" if channel == "profile" else "room13-fullbody-dialogue.json"}'], geometry={k:spec[k] for k in ('crop','foot','head','seat','hand','stature_ratio') if k in spec})

    def usage(location, field, person, pose, period=None, condition=None, source='game/assets/room13-world-layout.json'):
        spec = acting.get(person, {}).get(pose)
        exists = bool(spec)
        fallback = acting.get(person, {}).get('neutral', cast.get(person, {}).get('neutral', {}))
        key = f'usage/{location}/{field}/{person}/{pose}/{period or "any"}'
        add(key, 'investigation_usage', person, location, period, condition, pose,
            files=[(spec or fallback).get('file')], production='available_unreviewed' if exists else 'not_produced',
            connection='linked' if exists else 'neutral_fallback', priority='P1' if not exists else 'P2', evidence=[source],
            asset_id=f'character/{person}/investigation/{pose}')

    fallback_groups = {'kitchen':'inn', 'dining':'inn', 'passage':'inn', 'post':'village'}
    for location, layout in layouts.items():
        for state, files in (layout.get('state_files') or {'normal':layout.get('files',{})}).items():
            for period in PERIODS:
                file = files.get(period)
                legacy = period not in layout.get('periods', PERIODS)
                if legacy:
                    group = fallback_groups.get(location)
                    file = f'assets/room13-pixel-{group}-{period}.webp' if group else None
                add(f'map/{location}/{state}/{period}', 'map_time_state', location=location, period=period,
                    condition='case_state == occurred' if state == 'after' else 'case_state != occurred' if state == 'before' else 'normal navigation',
                    requirement='장소 구조·출입구·인물 접지점 유지, 시간대 조명', files=[file],
                    production='available_unreviewed' if file else 'unresolved', connection='legacy_atlas' if legacy and file else 'linked' if file else 'unresolved',
                    evidence=['game/assets/room13-world-layout.json','game/room13_world_camera.rpy','game/room13_life.rpy'],
                    geometry={k:layout[k] for k in ('width','height','crops','periods') if k in layout})
        for field in ('poses','slot_actions','old_scene_slot_actions'):
            for person, value in layout.get(field,{}).items():
                for period, pose in (value.items() if isinstance(value,dict) else [(None,value)]):
                    usage(location,field,person,pose,period, '주민이 현재 장소에 있을 때; slot action은 neutral 상태·이벤트 제안 없음 조건')
        for prop in layout.get('props',[]):
            add(f'map/{location}/prop/{Path(prop["file"]).stem}', 'map_prop', location=location, condition=prop.get('when'), requirement=prop.get('note','prop overlay'), files=[prop['file']], evidence=['game/assets/room13-world-layout.json'],geometry={'rect':prop.get('rect')})

    for row in prior_pending['pending_layout_actions']:
        for period,pose in (row['requested'].items() if isinstance(row['requested'],dict) else [(None,row['requested'])]):
            usage(row['place'],row['field'],row['person'],pose,period,'0.19.1에서 정본 재제작까지 연결 보류', 'art/canonical-channel-alignment-20261017/report.json')
    for person,row in prior_pending['roles'].items():
        for pose in row['pending_revised_actions']:
            add(f'character/{person}/dialogue_pose/{pose}', 'dialogue_pose', person, requirement=pose,
                files=[fb[person]['images']['neutral']['file']],production='not_produced',connection='neutral_fallback',priority='P0' if pose != 'wipe_board' else 'P1', evidence=['art/canonical-channel-alignment-20261017/report.json'])

    ep = GAME / 'systems/room13_ep_art.rpy'
    node,line = assignment(ep,'R13_EP_BACKGROUNDS')
    for key,value in ast.literal_eval(node).items():
        for period,file in (value.items() if isinstance(value,dict) else [('authored',value)]):
            add(f'map/event/{key}/{period}','map_event',location=key,period=period,condition=f'r13_scene background key == {key}',requirement=key,files=['assets/'+file], evidence=[f'game/systems/room13_ep_art.rpy:{line}'], time_reuse=key=='ep_laundry' and period=='morning')
    node,line = assignment(ep,'R13_EP_OVERLAYS')
    for place,variants in zip(node.keys,node.values):
        for variant in variants.elts:
            file,condition = variant.elts
            add(f'map/{place.value}/event/{file.value.removesuffix(".webp")}', 'map_event_overlay',location=place.value,condition=ast.unparse(condition),requirement=file.value,files=['assets/'+file.value],evidence=[f'game/systems/room13_ep_art.rpy:{line}'])

    # Authored living-pose selection includes requirements whose layout override was removed.
    path = GAME / 'room13_acting.rpy'
    for tree, offset in init_trees(path):
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or node.name != 'r13_living_pose':continue
            for value in ast.walk(node):
                if not isinstance(value, ast.Dict):continue
                for pair, selection in zip(value.keys,value.values):
                    if not isinstance(pair,ast.Tuple):continue
                    person,location=ast.literal_eval(pair)
                    for period_index,period in enumerate(PERIODS):
                        allowed=(ast.Expression,ast.Constant,ast.IfExp,ast.Compare,ast.Eq,ast.In,ast.Name,ast.Load)
                        expr=ast.Expression(body=selection)
                        if not all(isinstance(n,allowed) for n in ast.walk(expr)):continue
                        pose=eval(compile(expr,'living-pose','eval'),{'__builtins__':{}},{'period':period_index,'poses':acting.get(person,{})})
                        usage(location,'living_rule',person,pose,period,ast.unparse(selection),f'game/room13_acting.rpy:{offset+value.lineno}')

    for name,field in (('room13-fullbody-line-emotions.json','emotion'),('room13-line-direction.json','pose')):
        data=load(GAME/'assets'/name)
        for scene,lines in data.get('lines',data).items():
            if not isinstance(lines,dict):continue
            for index,cue in lines.items():
                if not isinstance(cue,dict) or 'person' not in cue or field not in cue:continue
                person,key=cue['person'],cue[field]
                asset=items.get(f'character/{person}/dialogue/{key}') if field=='emotion' else items.get(f'character/{person}/investigation/{key}')
                add(f'dialogue-cue/{scene}/{index}/{field}', 'dialogue_usage',person,condition='identity, person and text must match live line; dynamic branch not executed',requirement=key,
                    files=[a['file'] for a in asset['current_assets']] if asset else [],production=asset['production_status'] if asset else 'needs_reconciliation',
                    connection=asset['connection_status'] if asset else 'requires_resolution',evidence=['game/assets/'+name],line_text=cue.get('text'),asset_id=asset['id'] if asset else None)

    cartography=load(GAME/'room13-cartography.json')
    for region,spec in cartography['regions'].items():
        add(f'navigation/{region}/base','navigation_map',location=region,condition='region selected',requirement='illustrated navigation map',files=[spec['art']],evidence=['game/room13-cartography.json','game/room13_worldmap_v5.rpy'])
        for place,node in spec.get('nodes',{}).items():
            for variant,suffix in (('cutout',''),('outline','-outline')):
                file=f'assets/room13-map-{region}-{place}{suffix}.webp'
                add(f'navigation/{region}/{place}/{variant}','navigation_node',location=place,condition='discovered node; hover/selection uses outline',requirement=variant,
                    files=[file] if (GAME/file).is_file() else [],production='available_unreviewed' if (GAME/file).is_file() else 'needs_reconciliation',
                    connection='linked' if (GAME/file).is_file() else 'requires_resolution',evidence=['game/room13-cartography.json','game/room13_worldmap_v5.rpy'],geometry=node)
    for secret,spec in cartography.get('reveals',{}).items():
        add(f'navigation/reveal/{secret}','navigation_reveal',location=secret,condition=f'r13_map_discovered({secret!r}); see runtime reveal rule',requirement='discovered area overlay',files=[spec['art']],evidence=['game/room13-cartography.json','game/room13_worldmap_v5.rpy'],geometry={'bounds':spec['bounds']})
    for location in ('inn','hall','room13'):
        add(f'map/{location}/treatment/after','map_runtime_treatment',location=location,condition='case_state == occurred',requirement='existing background tint/saturation; no new illustration required',production='runtime_effect',connection='linked',evidence=['game/systems/room13_scene_contrast.rpy'])

    # Existing requests are retained as requirements, never trusted as completion evidence.
    for row in historical:
        person,pose = row['id'],row['state_key']
        spec = acting.get(person,{}).get(pose)
        candidate = next((e for e in action_registry if e['person']==person and e['pose']==pose and e.get('hold')),None)
        key='request/'+person+'/'+digest('|'.join(row[k] for k in ('kind','state_key','map','condition','output_file')))
        add(key,'production_request',person,row['map'],row['time'],row['condition'],row['expression_body_prop_gaze'],
            files=[spec['file']] if spec else [],production='candidate_held' if candidate else 'available_unreviewed' if spec else 'needs_reconciliation',
            connection='linked' if spec else 'not_linked' if candidate else 'requires_resolution',priority=row['priority'],evidence=['docs/ART_REQUEST_P0P1_20261016.csv',row['script_ref']],
            request_details=row, candidate=candidate, next_action_override='소유자 승인 전 후보 연결 금지' if candidate else None)

    # Literal authored pose cues: preserve source context; never guess the speaker/conditions.
    for path in sorted(GAME.rglob('*.rpy')):
        if 'qa_tests' in path.parts:continue
        text = path.read_text()
        for match in re.finditer(r'["\']pose["\']\s*:\s*["\']([\w]+)["\']',text):
            line = text.count('\n',0,match.start())+1
            start=text.rfind('\n',0,max(0,match.start()-200))
            context=text[max(0,start):text.find('\n',match.end())].strip()
            rel=str(path.relative_to(ROOT))
            key='cue/'+rel+'/'+match.group(1)+'/'+digest(context)
            add(key,'script_pose_cue',condition='source context; branch reachability not executed',requirement=match.group(1),production='needs_reconciliation',connection='requires_resolution',evidence=[f'{rel}:{line}'],context=context)
    packet_path=OUT/'batch-01.json'
    if packet_path.exists():
        for job in load(packet_path)['jobs']:
            for output in job['outputs']:
                if output['id'] not in items:
                    person=job['character']
                    add(output['id'],job['channel'],person,condition=job['scene_requirement'],requirement=output['key']+': '+job['direction'],
                        files=[fb[person]['images']['neutral']['file']],production='not_produced',connection='neutral_fallback',priority=job['priority'],evidence=['docs/art-coverage/batch-01.json'])
                items[output['id']]['production_batch']='art-coverage-batch-01'
    # Dad is a first-person viewpoint: inventory the archived channels, never queue new visible art.
    for item in items.values():
        if item['character']=='dad':
            item.update(production_status='not_required_viewpoint',connection_status='viewpoint_hidden',next_action='preserve_first_person_no_dad_render')
    registry_audit=[]
    for row in action_registry:
        spec=acting.get(row['person'],{}).get(row['pose'],{})
        status='held' if row.get('hold') else 'withdrawn' if row.get('withdrawn') else 'linked' if spec.get('source_sha256')==row['sha256'] else 'needs_reconciliation'
        registry_audit.append(dict(person=row['person'],pose=row['pose'],source=str((ROOT/'art/map-actions-20261015'/row['source']).resolve().relative_to(ROOT)),status=status,reason=row.get('hold') or row.get('withdrawn')))
    result={'schema_version':1,'source_revision':subprocess.check_output(['git','log','-1','--format=%H','--','game'],cwd=ROOT,text=True).strip(),'basis_version':re.search(r'config.version = "([^"]+)"',(GAME/'options.rpy').read_text()).group(1),
        'canonical_roster':list(canon),'runtime_roster':sorted(set(cast)|set(fb)),
        'additional_runtime_characters':sorted((set(cast)|set(fb))-set(canon)),
        'scope_limits':['Static requirements and paths, not a complete playthrough.','Dynamic expressions, scripted pose cues and branch reachability require review.','Historical screenshots are references, not fresh screen passes.','Repeated neutral files do not complete expressions.','No new artwork or design approval is inferred.'],
        'registry_audit':registry_audit,'items':sorted(items.values(),key=lambda x:x['id'])}
    result['summary']={'items':len(items),'by_kind':dict(collections.Counter(i['kind'] for i in items.values())), 'production':dict(collections.Counter(i['production_status'] for i in items.values())), 'connection':dict(collections.Counter(i['connection_status'] for i in items.values())), 'screen_review':dict(collections.Counter(i['screen_review']['status'] for i in items.values()))}
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    result=build()
    rendered=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    path=OUT/'coverage.json'
    if args.check:
        assert path.read_text()==rendered,'art coverage is stale; run dev/art_coverage.py'
    else:
        path.write_text(rendered)
        stream=io.StringIO();fields=['id','kind','character','character_name','location','period','event_condition','requirement','current_assets','canonical_reference','production_status','connection_status','screen_review','priority','next_action','source_evidence']
        writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\n');writer.writeheader()
        for item in result['items']:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in item.items() if k in fields})
        (OUT/'coverage.csv').write_text(stream.getvalue(),encoding='utf-8-sig')
        lines=['# 아트 충족 현황 — 자동 생성', '', f"기준: {result['basis_version']} / `{result['source_revision']}`. 확정 48명과 추가/기존 보조 런타임 15명을 구분한다. 추가 15명 모두를 신규 제작 대상으로 확정한 것은 아니다.", '',
            'JSON이 단일 현황 원장이고 CSV는 같은 자료의 보기다. 자산·사용 장면·제작 요청을 포함하므로 전체 행 수는 그림 장수가 아니다. 기존 제작 요청 153건은 최신 연결과 재조정할 항목이며, 옛 상태 문구를 완료 근거로 사용하지 않는다.', '',
            '실제 화면 검수는 이번 실행에서 전부 미실행이다. 파일 존재, 과거 캡처, 단위 검사로 화면 합격을 대신하지 않는다. 동적 조건과 script_pose_cue는 정적 추출 한계로 별도 확인이 필요하다.', '',
            '## 범위', '', '|유형|행 수|','|---|---:|']
        lines += [f'|{k}|{v}|' for k,v in result['summary']['by_kind'].items()]
        lines += ['', '## 대화 표정', '', '|인물 ID|이름|독립 파일 표정 수*|중립 대체|수정 필요|', '|---|---|---:|---|---|']
        for person in result['runtime_roster']:
            rows=[i for i in result['items'] if i['character']==person and i['kind']=='dialogue_expression']
            ready=sum(i['production_status']=='available_unreviewed' for i in rows)
            missing=','.join(i['requirement'] for i in rows if i['production_status']=='not_produced') or '—'
            fix=','.join(i['requirement'] for i in rows if i['production_status']=='needs_correction') or '—'
            lines.append(f'|{person}|{rows[0]["character_name"] or person}|{ready}|{missing}|{fix}|')
        lines += ['', '*파일과 중립 중복 여부 기준이며 디자인 승인/화면 합격 수가 아니다. 아빠는 1인칭 시점이라 화면 제작 대상에서 제외한다. 기본 6키 밖의 동작은 별도 행으로 관리한다.', '',
                  '## 장소·시간대', '', '|장소|상태|시간|연결|파일|','|---|---|---|---|---|']
        for item in result['items']:
            if item['kind']=='map_time_state':lines.append('|'+ '|'.join([item['location'],item['id'].split('/')[-2],item['period'],item['connection_status'],', '.join(a['file'] for a in item['current_assets'])])+'|')
        lines += ['', '## 다음 처리', '', '1. `BATCH_01.md` / `BATCH_02.md`의 후보 보고와 `NEXT_QUEUE.md`를 따라 수신·개별 승인·통합을 우선한다. 이미 생성된 후보를 중복 발주하지 않으며 승인 전 현재 연결을 유지한다.', '2. 기존 요청과 코드 조건 재조정: 특히 조사 생활 동작, 겨울 야외 옷, 눈 깜빡임, 추가 인물 제한 표정.', '3. 새 승인 그림 수령 후 경로·해시·2×2 셀·몸 비율·접점 검사 → 해당 장면 화면 검수 → 연결 상태와 리뷰 기록 갱신.', '4. 맵 66 시간/사건 조합과 18 이벤트 배경, 13 겹침 효과는 그림 추가가 필요한지 실제 조건별 화면을 보고 결정. 시간대 재사용/기존 atlas를 곧바로 누락으로 판단하지 않는다.', '5. 전체 6표정이 중립인 23명 외에도 초롱/추가 아이들 등 일부 표정 fallback이 있다. 제한 표정 세트가 의도된 경우 장면 필요도를 확인한 뒤 제작 여부 결정.', '']
        (OUT/'SUMMARY.md').write_text('\n'.join(lines))
    print(json.dumps(result['summary'],ensure_ascii=False,indent=2))


if __name__=='__main__':main()
