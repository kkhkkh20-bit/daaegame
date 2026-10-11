"""Check alternate deduction paths and knowledge gates from the shipped case data."""
import ast
import json
import textwrap
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent


def functions(path, names):
    source = path.read_text().split('init ', 1)[1].split(' python:\n', 1)[1]
    source = source.split('\nlabel ', 1)[0].split('\nscreen ', 1)[0]
    tree = ast.parse(textwrap.dedent(source))
    return ast.Module(body=[node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name in names], type_ignores=[])


def main():
    episode = json.loads((ROOT / 'game/chapter-source.json').read_text())['episode']
    episode.update(json.loads((ROOT / 'game/chapter-dialogue.json').read_text())['sections'])
    timeline = json.loads((ROOT / 'game/village-state.json').read_text())
    state = SimpleNamespace(source_group='meet', source_phase=7, source_statement=0,
        source_step=0, source_pressed=False, source_claim_progress={}, source_proof_marks=[],
        source_inventory=[], source_seen=[], source_flags=[], source_found=False,
        source_question_revisions={},
        village_minutes=1050,village_time_events=[],village_trust={'neoul':-1},
        village_trust_events=[])
    env = {'store': state, 'TIMELINE': timeline, 'SOURCE_EP':episode,
        'arrival_question_lines': lambda question: question['lines']}
    names = {'source_claim_key', 'source_remember_claim', 'source_select_claim',
        'source_soft_available', 'source_apply_soft', 'source_card'}
    exec(compile(functions(ROOT / 'game/source.rpy', names), 'source.rpy', 'exec'), env)
    exec(compile(functions(ROOT / 'game/timeline.rpy', {'village_question_lines',
        'village_question_variant','village_question_revision','village_question_done',
        'village_question_new','village_topic_available','village_event','village_advance_evening'}),
        'timeline.rpy', 'exec'), env)

    clock_claim = episode['MEET']['phases'][7]['stms'][0]
    clock = clock_claim['soft']['C06']
    testimony = clock_claim['soft']['C13']
    # A witness record alone must not skip the still-unexamined clock.
    assert not env['source_soft_available'](testimony)
    assert env['source_soft_available'](clock)
    env['source_apply_soft'](clock)
    assert state.source_proof_marks == ['m3c06']
    assert env['source_soft_available'](testimony)
    env['source_apply_soft'](testimony)
    assert (state.source_statement, state.source_step) == (1, 1)
    witness_claim = episode['MEET']['phases'][7]['stms'][1]
    assert 'C07' in witness_claim['steps'][state.source_step]['ids']
    assert 'C08' not in witness_claim['steps'][state.source_step]['ids']
    assert env['source_soft_available'](witness_claim['soft']['C08'])
    # Checking another suspect must preserve comparisons and questions already asked.
    state.source_step, state.source_pressed = 2, True
    env['source_select_claim'](2)
    assert (state.source_step, state.source_pressed) == (0, False)
    env['source_select_claim'](1)
    assert (state.source_step, state.source_pressed) == (2, True)
    assert not env['source_soft_available'](witness_claim['soft']['C08'])
    assert 'C08' in witness_claim['a']
    # A different round cannot inherit comparison progress from the same row index.
    state.source_phase = 8
    state.source_step, state.source_pressed = 0, False
    env['source_select_claim'](2)
    assert (state.source_step, state.source_pressed) == (0, False)

    granny = next(q for q in episode['TALK']['innma'] if q['id'] == 'T_ma6')
    assert not env['village_topic_available'](granny)
    state.source_inventory = ['C04']
    assert not env['village_topic_available'](granny)
    state.source_found = True
    assert env['village_topic_available'](granny)
    gamble = next(q for q in episode['TALK']['seryeon'] if q['id'] == 'T_se4')
    assert not env['village_topic_available'](gamble)
    state.source_flags = ['inn_karo_gamble']
    assert env['village_topic_available'](gamble)

    fixed_questions = ('C13', 'T_ba3', 'T_se2', 'C12')
    for question_id in fixed_questions:
        question = next(q for topics in episode['TALK'].values()
            for q in topics if q['id'] == question_id)
        state.source_flags = []
        assert env['village_question_lines'](question) == question['lines']
        state.source_flags = ['inn_c13fix']
        changed = env['village_question_lines'](question)
        assert changed != question['lines'], question_id
        # The correction must not append the original false-alibi/6:30 passage.
        old_false_claim = {'C13': 3, 'T_ba3': 3, 'T_se2': 3}.get(question_id)
        if old_false_claim is not None:
            assert question['lines'][old_false_claim] not in changed

    bed_question=next(q for q in episode['TALK']['innma'] if q['id']=='T_ma1')
    state.source_seen=['T_ma1','C13']
    state.source_inventory,state.source_flags=[],[]
    state.source_question_revisions={'T_ma1':'base','C13':'base'}
    assert env['village_question_done'](bed_question)
    state.source_inventory=['C04']
    assert env['village_question_new'](bed_question)
    changed_revision=env['village_question_revision'](bed_question)
    state.source_question_revisions['T_ma1']=changed_revision
    assert env['village_question_done'](bed_question)
    witness=next(q for q in episode['TALK']['geokkuri'] if q['id']=='C13')
    assert env['village_question_done'](witness)
    state.source_flags=['inn_c13fix']
    assert env['village_question_new'](witness)
    state.source_question_revisions['C13']=env['village_question_revision'](witness)
    assert env['village_question_done'](witness)
    assert state.source_seen==['T_ma1','C13'] and state.village_trust_events==[]
    for spec in timeline['residents'].values():
        assert all(word not in spec['public_purpose'] for word in ('겨울잠 손님','새벽 5시','계약','돈','종의 오차'))

    state.source_flags=[]
    assert env['source_card']('C04')==episode['EV']['C04']['card']
    state.source_flags=['inn_life_confirmed']
    assert '숨 쉬는' in env['source_card']('C04')
    assert '침대 밑, 상자 뒤' in env['source_card']('C04')
    for _ in range(200):env['village_advance_evening'](5)
    assert state.village_minutes==1260
    env['village_event']('arrival_new_topic')
    assert state.village_minutes==1260 and state.village_trust=={'neoul':-1}
    assert state.village_trust_events==[]
    env['village_event']('case_begin')
    assert state.village_minutes==1890
    # Repeat observations contain no grants, milestones, or first-discovery speeches.
    assert all(isinstance(packet,list) and packet[0] not in ('@grant','@dir')
        for packets in timeline['repeat_observations'].values() for packet in packets)
    assert len(timeline['repeat_observations']['under'])<=3
    assert len(timeline['repeat_observations']['chest'])<=4

    # Post-case scenes advance through afternoon and night, without rewinding
    # when a scene is revisited or a saved scene is resumed.
    last=state.village_minutes
    for scene in episode['END']:
        event='ending_'+scene['sid']
        env['village_event'](event)
        assert state.village_minutes>=last
        assert state.village_minutes>=timeline['events'][event]['at']
        last=state.village_minutes
    assert 18*60 <= state.village_minutes%1440 < 24*60
    env['village_event']('ending_E1')
    assert state.village_minutes==last

    print(json.dumps(dict(alternate_clock_deduction_requires_prior_comparison=True,
        alternate_path_enters_correct_next_comparison=True,
        switching_claims_preserves_comparisons_and_pressing=True,
        comparison_progress_is_scoped_to_each_round=True,
        undiscovered_guest_and_unheard_accusation_hidden=True,
        corrected_testimony_stays_correct_on_revisit=True,
        confirmed_living_guest_evidence_updated=True,
        long_evening_exploration_stays_before_lodging_without_farming_trust=True,
        repeated_discoveries_have_no_grants_or_story_beats=True,
        newly_available_variants_marked_unread_until_heard=True,
        revised_questions_do_not_reset_relationship_rewards=True,
        resident_notebook_does_not_reveal_unheard_alibis=True,
        after_story_advances_to_night_without_revisit_rewind=True), indent=2))


if __name__ == '__main__':
    main()
