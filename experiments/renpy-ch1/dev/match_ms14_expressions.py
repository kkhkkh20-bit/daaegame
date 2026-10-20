"""Explicit, context-reviewed presentation cues for the implemented D01-D05.
IDs below are editorial choices, not a keyword/emotion classifier.
Route text, operations and conditions are never modified.
"""
import ast, collections, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/dialogue-beats/expression-fit-20261020'
GROUPS={
 'joy':'''D01_S01_L0003 D01_S01_L0007 D01_S01_L0013 D01_S01_L0019 D01_S01_L0021 D01_S03_L0011 D01_S04_L0006 D01_S04_L0010 D01_S05_L0001 D01_S05_L0004 D01_S05_L0020 D01_S05_L0023
 D02_S02_L0028 D02_S03_L0003 D02_S03_L0016 D02_S03_L0018 D02_S03_L0019 D02_S03_L0022 D02_S04_L0027 D02_S04_L0031 D02_S04_L0033
 D03_S01_L0023 D03_S01_L0024 D03_S01_L0026 D03_S01_L0037 D03_S01_L0038 D03_S06_L0003 D03_S06_L0025 D03_S06_L0030 D03_S06_L0038 D03_S06_L0039
 D04_S02_L0002 D04_S02_L0006 D04_S02_L0012
 D05_S01_L0010 D05_S05_L0009 D05_S05_L0012 D05_S05_L0026''',
 'anxious':'''D01_S01_L0009 D01_S02_L0017 D01_S03_L0005 D01_S03_L0017 D01_S04_L0002 D01_S05_L0007 D01_S05_L0008 D01_S05_L0013 D01_S05_L0016 D01_S05_L0025 D01_S05_L0028 D01_S05_L0033 D01_S05_L0040 D01_S05_L0043 D01_S05_L0050
 D02_S01_L0038 D02_S02_L0026 D02_S03_L0008 D02_S03_L0023 D02_S03_L0030 D02_S03_L0032 D02_S04_L0014 D02_S04_L0016 D02_S04_L0018 D02_S04_L0019 D02_S04_L0045 D02_S04_L0073 D02_S05_L0012
 D03_S01_L0003 D03_S01_L0008 D03_S01_L0010 D03_S01_L0012 D03_S01_L0014 D03_S01_L0016 D03_S01_L0019 D03_S01_L0028 D03_S03_L0015 D03_S03_L0017 D03_S04_L0020 D03_S04_L0030 D03_S04_L0035 D03_S04_L0037 D03_S05_L0008 D03_S05_L0013 D03_S05_L0017 D03_S05_L0025 D03_S05_L0033 D03_S05_L0036 D03_S05_L0037 D03_S05_L0044 D03_S05_L0054 D03_S05_L0065 D03_S06_L0006 D03_S06_L0011 D03_S06_L0015 D03_S06_L0018
 D04_S01_L0007 D04_S01_L0011 D04_S01_L0022 D04_S01_L0039 D04_S01_L0041 D04_S01_L0051 D04_S01_L0060 D04_S03_L0009 D04_S03_L0012 D04_S03_L0017 D04_S04_L0003 D04_S04_L0006 D04_S04_L0012 D04_S04_L0014 D04_S04_L0029 D04_S04_L0031 D04_S04_L0043 D04_S04_L0045 D04_S04_L0049 D04_S04_L0061
 D05_S01_L0018 D05_S01_L0024 D05_S02_L0003 D05_S02_L0006 D05_S02_L0009 D05_S02_L0011 D05_S02_L0015 D05_S02_L0017 D05_S02_L0019 D05_S02_L0021 D05_S03_L0003 D05_S03_L0005 D05_S03_L0029 D05_S03_L0033 D05_S03_L0035 D05_S04_L0010 D05_S04_L0012 D05_S04_L0020 D05_S05_L0011 D05_S05_L0040 D05_S05_L0042 D05_S05_L0050 D05_S05_L0055 D05_S05_L0061''',
 'angry':'''D01_S04_L0021
 D02_S04_L0005 D02_S04_L0007 D02_S04_L0032 D02_S04_L0055
 D03_S01_L0033 D03_S02_L0003 D03_S02_L0005 D03_S02_L0021 D03_S03_L0009 D03_S03_L0011 D03_S03_L0023 D03_S03_L0029 D03_S04_L0014 D03_S04_L0022 D03_S05_L0014 D03_S05_L0041
 D04_S01_L0055 D04_S03_L0002 D04_S03_L0005 D04_S03_L0014 D04_S03_L0019 D04_S04_L0017 D04_S04_L0022 D04_S04_L0023
 D05_S01_L0020 D05_S01_L0022 D05_S02_L0002 D05_S02_L0013 D05_S02_L0024 D05_S03_L0018 D05_S03_L0019 D05_S03_L0023 D05_S05_L0002 D05_S05_L0007''',
 'surprise':'''D01_S01_L0011 D01_S03_L0010 D02_S03_L0043 D02_S04_L0024 D03_S01_L0029 D04_S01_L0043 D04_S01_L0045 D04_S04_L0016 D05_S04_L0007''',
}
REASONS={
 'D01':'가족 재회를 기대하는 장난과 안도는 joy, 입구의 자기 탓 걱정과 빈방 이후 불안은 anxious. 돌목의 행정 설명과 너울의 통제는 담담하게 유지.',
 'D02':'피코의 자조·농담과 아이의 얼굴 묘사는 joy. 잠자리/야간 안전의 걱정은 anxious. 나비의 작업 공간 경계와 네로의 선 긋기만 angry.',
 'D03':'피코 생존/사망 분기를 별도 ID로 검토. 사망 장면은 anxious, 생존 농담만 joy. 톡·부리의 억울한 항변과 실룩의 방어/막다른 불안은 구분.',
 'D04':'네로의 돌봄 부담과 아이들의 불안, 밤이의 억울함을 구분. 목격/증거 설명과 바둑이의 보호 설명은 neutral을 유지.',
 'D05':'솜이의 보호·저항과 밤이의 불안, 가족 편지의 기대/두려움을 구분. 진료/인계·증거 설명을 기계적으로 과장하지 않음.',
}

def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def current_source_packets():
    # Inspect the real packet adapter, without running the campaign/init block.
    import textwrap
    source=(ROOT/'game/ms14_story.rpy').read_text()
    mapping=ast.literal_eval(source.split('    MS14_SPEAKERS = ',1)[1].split('\n    R13_CHARS',1)[0])
    body='def ms14_line'+source.split('    def ms14_line',1)[1].split('    def ms14_menu_options',1)[0]
    env={'MS14_SPEAKERS':mapping}
    exec('def ms14_line(record):\n'+textwrap.indent(textwrap.dedent(body.split('\n',1)[1]),'    '),env)
    records=json.loads((ROOT/'game/ms14/route.json').read_text())['records']
    return {rid:env['ms14_line'](r) for rid,r in records.items()
        if r.get('kind')=='dialogue' and r.get('player_visible') and r.get('speaker') not in (None,'아빠') and mapping.get(r.get('speaker'))}

def main():
    route=json.loads((ROOT/'game/ms14/route.json').read_text())
    source=(ROOT/'game/ms14_story.rpy').read_text().split('    MS14_SPEAKERS = ',1)[1].split('\n    R13_CHARS',1)[0]
    speakers=ast.literal_eval(source)
    available=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
    beats_path=ROOT/'game/assets/room13-dialogue-beats.json';full_path=ROOT/'game/assets/room13-fullbody-line-emotions.json'
    beats=json.loads(beats_path.read_text());full=json.loads(full_path.read_text())
    choices={}
    for emotion,keys in GROUPS.items():
        for key in keys.split():
            rid='MS14_'+key
            assert rid in route['records'],rid
            assert rid not in choices,rid
            choices[rid]=emotion
    matched=[];missing=[];lookup={}
    for rid,record in route['records'].items():
        if record.get('kind')!='dialogue' or not record.get('player_visible') or record.get('speaker') in (None,'아빠'):continue
        person=speakers.get(record['speaker'])
        if person not in available:
            missing.append(dict(id=rid,speaker=record['speaker'],reason='no runtime speaker/art; do not borrow a face'));continue
        emotion=choices.get(rid,'neutral');reason=REASONS[rid.split('_')[1]]
        cue=dict(person=person,text=record['text'],emotion=emotion,reaction=False,reviewed=True,
            reason=reason,batch='expression-fit-20261020',application_status='approved_source_master')
        beats['lines'][rid]={'0':cue}
        full['lines'][rid]={'0':dict(person=person,text=record['text'],emotion=emotion,reason=reason)}
        matched.append(dict(id=rid,person=person,text=record['text'],emotion=emotion))
        if rid.startswith('MS14_D01_'):lookup[person,record['text']]=cue
    # Current live D01 also uses the restored original engine labels. Only
    # exact text+speaker matches from the reviewed D01 records are updated.
    live=[]
    for identity,rows in list(beats['lines'].items()):
        if identity.startswith('MS14_'):continue
        if not (identity.startswith('entry:') or identity.startswith('carriage')):continue
        for index,cue in rows.items():
            new=lookup.get((cue['person'],cue['text']))
            if new and any(x['id'].startswith('MS14_D01_') and (x['person'],x['text'])==(cue['person'],cue['text']) for x in matched):
                cue.update(emotion=new['emotion'],reaction=False,reason=new['reason'],batch=new['batch'])
                full['lines'].setdefault(identity,{})[index]=dict(person=cue['person'],text=cue['text'],emotion=cue['emotion'],reason=cue['reason'])
                live.append(dict(identity=identity,index=index,person=cue['person'],emotion=cue['emotion']))
    binding_path=ROOT/'game/assets/room13-dialogue-bindings.json'
    bindings=json.loads(binding_path.read_text());dynamic=[]
    review_path=ROOT/'docs/reviews/dialogue-beats/dynamic-context-review.json'
    review=json.loads(review_path.read_text())
    # The current carriage has an existing call-site snapshot binding.
    for key in bindings['routes']['dynamic:016']['cues']:
        cue=bindings['cues'][key];new=lookup.get((cue['person'],cue['text']))
        if new:
            cue.update(emotion=new['emotion'],reaction=False)
            ref=cue['review_ref'].split(':')[-1]
            if ref in review['rows']:review['rows'][ref].update(emotion=new['emotion'],reaction=False,reason=new['reason'])
            dynamic.append(dict(identity='carriage:intro',person=cue['person'],text=cue['text'],emotion=cue['emotion']))
    write(binding_path,bindings);write(review_path,review)
    live.extend(dynamic)
    write(beats_path,beats);write(full_path,full)
    OUT.mkdir(exist_ok=True)
    write(OUT/'expression-matching.json',dict(scope=route['scope'],matched=matched,missing=missing,
        active_entry_matches=live,counts=dict(collections.Counter(x['emotion'] for x in matched)),
        note='D01-D05 source records exist; this change does not activate the dormant MS14 campaign or modify dialogue/conditions. Missing roles are not hidden.'))
    print('Reviewed NPC rows',len(matched),'missing speaker/art',len(missing),'live entry matches',len(live))

if __name__=='__main__':main()
