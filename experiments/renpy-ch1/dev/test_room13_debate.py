"""Public-meeting engine: data integrity, judging, missing-evidence skip, give-up closing, proofs only via r13_prove."""
import copy,json,textwrap,types
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'game/room13-content.json').read_text())
evidence=content['evidence'] if isinstance(content['evidence'],dict) else {e['id']:e for e in content['evidence']}
claims={c['id']:c for c in content['claims']}
block=(root/'game/systems/room13_debate.rpy').read_text().split('init 98 python:\n',1)[1].split('\nlabel ',1)[0]
store=types.SimpleNamespace(room13=dict(propositions=[],flags=[],evidence=[],finale_started=False))
env=dict(store=store,winter_copy=copy,R13_NAMES={},
    r13_has=lambda k:k in store.room13['flags'] or k in store.room13['evidence'])
exec(compile(textwrap.dedent(block),'debate','exec'),env)
D=env['R13_DEBATE'];checks=[]

# Data: every claim exists, every accepted/soft item is a real evidence id, reveal targets exist.
assert set(D)=={'C1','C2','C3','C4','F1','F2','F3','F4'}
for cid,spec in D.items():
    assert cid in claims
    ids=[st['id'] for st in spec['statements']]
    assert len(ids)==len(set(ids))
    for st in spec['statements']:
        assert '【' in st['text'] and '】' in st['text'],(cid,st['id'])
        assert st.get('hint') and st.get('wrong')
        for key in st.get('accept',[])+list(st.get('soft',{})):
            assert key in evidence,(cid,st['id'],key)
        if st.get('reveals'):assert st['reveals'] in ids
        if not st.get('truth'):
            assert st.get('accept') or st.get('ready_flags'),(cid,st['id'])
    kinds=[k for k,t in spec['conclusion']['options']]
    assert sorted(kinds)==['correct','over','weak']
    for k in ('correct','over','weak'):assert spec['conclusion'][k]
checks.append('8 claims, statements, conclusions and evidence ids are consistent')
# 0.18.41 counters: three options, one correct, a reply for each wrong one; gated counters name a real claim.
counters=[(cid,st['id'],st['counter']) for cid,spec in D.items() for st in spec['statements'] if st.get('counter')]
assert len(counters)>=2
for cid,sid,c in counters:
    kinds=sorted(k for k,t in c['options'])
    assert kinds==['correct','over','weak'] and c['correct'] and c['lines'] and c['prompt'],(cid,sid)
    assert set(c['wrong'])=={'over','weak'},(cid,sid)
    assert c.get('need_prop') in (None,)+tuple(D),(cid,sid)
checks.append('counters: options, replies and gates are consistent')

# Every accepted item was already part of that claim's original support evidence (obtainability kept),
# except E37 which is the direct operation record of the same passage as E05.
for cid,spec in D.items():
    old={e for path in claims[cid]['support_sets'] for e in path}|({'E37'} if 'E05' in str(claims[cid]['support_sets']) else set())
    for st in spec['statements']:
        for key in st.get('accept',[]):
            assert key in old,(cid,st['id'],key)
checks.append('accepted evidence is a subset of the original support sets')

# Judging on C2.
store.room13['evidence']=['E06','E07','E10','E01','E35']
j=env['r13_debate_judge']
assert j('C2','s1','E06')[0]=='break'
assert j('C2','s1','E35')[0]=='soft'          # breaks another visible statement: no penalty
# 0.18.35: a record never says more than it shows. The broken candlestick / the pin alone
# do not order the blows; only the wound comparison (E35) breaks those statements.
assert j('C2','s2','E07')[0]=='soft' and j('C2','s2','E35')[0]=='break'
assert j('C4','s2','E14')[0]=='soft' and j('C4','s2','E35')[0]=='break'
# Each accepted record of a multi-record statement has its own rebuttal lines.
for cid,spec in D.items():
    for st in spec['statements']:
        if len(st.get('accept',[]))>1 and not set(st['accept'])<= {'E05','E37'}:
            assert set(st.get('broken_by',{}))>=set(st['accept']),(cid,st['id'])
assert j('C2','s1','E08')[1]!=j('C2','s1','E06')[1]
assert j('C2','s1','E01')[0]=='wrong'
assert j('C2','s3','E10')[0]=='soft'          # E10 needs bami's consent
store.room13['flags'].append('bami_consent');assert j('C2','s3','E10')[0]=='break'
checks.append('break / soft (other statement, consent) / wrong; one record, one claim')

# Hidden statements appear only after pressing the revealing one; truths are not required.
assert not env['r13_debate_visible']('C1',env['r13_debate_statement']('C1','s2'))
env['r13_debate_mark']('pressed','C1','s1')
assert env['r13_debate_visible']('C1',env['r13_debate_statement']('C1','s2'))
assert env['r13_debate_required']('C1')==['s2']
checks.append('press reveals hidden statement; true statements are not required')

# Ready only when every required statement is broken; proofs are not written by the engine.
assert not env['r13_debate_ready']('C2')
for sid in ('s1','s2','s3'):env['r13_debate_mark']('broken','C2',sid)
assert env['r13_debate_ready']('C2') and 'C2' not in store.room13['propositions']
checks.append('conclusion unlocks after all required statements; propositions untouched')

# No trust meter: wrong answers only count misses (for hints). Failure = missing evidence or giving up.
assert 'r13_debate_lose_trust' not in env and 'R13_DEBATE_TRUST_MAX' not in env
env['r13_debate_miss']('C2');env['r13_debate_miss']('C2')
assert env['r13_debate_state']()['misses']['C2']>=2
# C4 needs E13 (whose pin, 0.18.3), E15, E35 and E36 for a full rebuttal. Since 0.18.35 holding only
# E15 still opens it (one statement breakable); holding nothing breakable does not.
store.room13['evidence']=['E15']
assert not env['r13_debate_arguable']('C4') and env['r13_debate_open']('C4')
store.room13['evidence']=['E14']
assert not env['r13_debate_engageable']('C4') and not env['r13_debate_open']('C4')
store.room13['evidence']=['E13','E14','E15','E36']
assert not env['r13_debate_arguable']('C4')   # the pin without the wound comparison
store.room13['evidence']=['E13','E15','E35','E36']
assert env['r13_debate_arguable']('C4')
# 0.18.35 partial: holding E06 and E09 but not E35 still opens C2; it cannot be concluded.
env['r13_debate_gap_lines']=lambda claim,st:[]
store.room13.update(evidence=['E06','E07','E09'],flags=[],propositions=[]);store.room13['debate']={}
assert not env['r13_debate_arguable']('C2') and env['r13_debate_engageable']('C2') and env['r13_debate_open']('C2')
assert not env['r13_debate_stuck']('C2')
env['r13_debate_mark']('broken','C2','s1');env['r13_debate_mark']('broken','C2','s3')
assert env['r13_debate_stuck']('C2') and not env['r13_debate_ready']('C2')
rows=env['r13_debate_partial_lines']('C2')
assert '아이 혼자' in rows[0][1] and '한 번 휘둘렸을 뿐' in rows[0][1]
store.room13.update(evidence=['E07']);store.room13['debate']={}
assert not env['r13_debate_engageable']('C2')   # nothing breakable: skipped as before
checks.append('partial rebuttal: engageable with some evidence, stuck when nothing breakable is left')
# 0.18.50: closing never crashes — everything broken but no conclusion, or only a skipped statement.
store.room13['debate']={};store.room13.update(propositions=[])
env['r13_debate_mark']('broken','C1','s2')
assert env['r13_debate_partial_lines']('C1')[0][1].startswith('(말은 모두 뒤집었다')
store.room13['debate']={};store.room13.update(propositions=['C2','C3','C4'])
assert env['r13_debate_dad_broken']('F4')==0 and env['r13_debate_progress']('F4')[0]==1
assert env['r13_debate_partial_lines']('F4')[0][1].startswith('(맞는 자료를 찾지 못했다')
store.room13.update(propositions=[]);store.room13['debate']={}
checks.append('partial close is safe when all or none of the statements were broken')
# The passage counter in C2 only exists once C1 is proven.
store.room13.update(propositions=[])
assert env['r13_debate_counter']('C2','s3') is None and env['r13_debate_counter']('C4','s1') is not None
store.room13.update(propositions=['C1'])
assert env['r13_debate_counter']('C2','s3') is not None
store.room13.update(propositions=[])
checks.append('C2 passage counter appears only after C1')
# Giving up closes the claim for this session only.
store.room13['finale_started']=False
env['r13_debate_close']('C3','gave_up')
assert env['r13_debate_closed']('C3') and not env['r13_debate_open']('C3')
store.room13['finale_started']=True;assert not env['r13_debate_closed']('C3')
store.room13['finale_started']=False
checks.append('no trust meter; missing evidence makes a claim unarguable; give-up closes per session')

# Story order for 13호 points.
store.room13['propositions']=[]
assert env['r13_case_available']()==['C1','C2']
store.room13['propositions']=['C2'];assert env['r13_case_available']()==['C1','C2','C3']
store.room13['propositions']=[]
checks.append('C3 opens after C2, C4 after C3')

# F3 manpower statement breaks by pressing once the real preparation flags exist.
env['r13_debate_mark']('pressed','F3','s3')
assert not env['r13_debate_is_broken']('F3','s3')
store.room13['flags']+=['operators_ready','patient_transport']
assert env['r13_debate_is_broken']('F3','s3')
checks.append('F3 manpower depends on real preparation flags')

# F4 separation statement counts as settled once C4 was proven.
assert not env['r13_debate_is_broken']('F4','s2')
store.room13['propositions'].append('C4');assert env['r13_debate_is_broken']('F4','s2')
checks.append('F4 s2 skipped after C4')

# Seats move with progress; the accuser never moves; sessions are separate.
seats=dict(env['r13_debate_seats']('trial'))
assert seats['seryeon']==0 and seats['buri']>=1
assert env['r13_debate_session']('C2')=='trial'
store.room13['finale_started']=True;assert env['r13_debate_session']('C2')=='finale'
checks.append('seat stances derived from progress; sessions separated')

# Conclusion order is deterministic and not always first.
firsts={cid:env['r13_debate_conclusion_options'](cid)[0][0] for cid in D}
assert len(set(firsts.values()))>1
checks.append('conclusion positions vary per claim')
# After a break the selection moves to a statement that still needs a rebuttal, not a true one.
store.room13.update(propositions=[],flags=[],evidence=[],finale_started=False);store.room13['debate']={}
n=env['r13_debate_next_target']
assert n('C3','s1')=='s2' and n('C1','s1')=='s1'
env['r13_debate_mark']('broken','C3','s2');assert n('C3','s2')=='s3'
store.room13['debate']={}
checks.append('selection skips true statements after a break')
# Goal line: meeting countdown and evidence readiness for the candlestick point.
env['r13_first_mystery_notes']=lambda:[dict(question='누가 마지막으로 만났을까?')]
env['r13_crisis_preparations']=lambda:[('a',True),('b',False),('c',True),('d',False)]
store.room13.update(day=5,finale_started=False,trial_ended=False,case_state='occurred',evidence=['E06','E07'],flags=[],propositions=[])
store.room13['debate']={}
assert env['r13_debate_evidence_ready']('C2')==(1,3)
assert env['r13_campaign_goal']()=='식당 회의까지 2일 · 촛대 논점에 쓸 자료 1/3'
store.room13.update(case_state='pending',day=3);assert env['r13_campaign_goal']()=='의문 · 누가 마지막으로 만났을까?'
store.room13.update(trial_ended=True,day=9);assert env['r13_campaign_goal']()=='제단까지 5일 · 함께 버틸 준비 2/4'
checks.append('goal line shows meeting countdown and evidence/preparation readiness')
print(json.dumps({'passed':True,'checks':checks},ensure_ascii=False,indent=2))
