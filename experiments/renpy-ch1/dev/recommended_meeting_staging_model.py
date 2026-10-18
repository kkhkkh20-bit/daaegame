"""Pure, presentation-only model. Never reads legacy claims or writes story facts."""
import copy

R13_REC_STAGE_HEARINGS = {
    1: dict(title='4일 · 광장의 돌과 인계', venue='dining', kind='round', background='council', target='nabi', cast=('nabi','resident_lamplighter','resident_ppul','daram','kid_kkomi','resident_piko')),
    2: dict(title='5일 · 수레 앞에서 있었던 일', venue='square', kind='field', background='winter_square', target='guard', cast=('guard','resident_badook','bami','daram','resident_ppul')),
    3: dict(title='6일 · 창고 문밖의 불', venue='school', kind='room', background='r13_school', target='resident_nubi', cast=('resident_nubi','resident_bori','resident_teacher','daram','kid_nubi1')),
    4: dict(title='10일 · 문과 구조를 함께 확인하는 회의', venue='dining', kind='round', background='council', target='neoul', cast=('neoul','nabi','resident_seori','resident_ppul','daram','buri')),
    5: dict(title='13일 · 배식과 책임을 구별하는 회의', venue='school', kind='room', background='r13_school', target='resident_teacher', cast=('resident_teacher','resident_bori','kid_saemi','resident_seori','resident_ppul','resident_badook','daram')),
    6: dict(title='14일 · 남을 수 있는 오늘', venue='school', kind='room', background='r13_school', target='granny', cast=('granny','resident_ppul','nabi','resident_badook','resident_mungchi','resident_siluk','resident_seori','daram','mom')),
}

# Explicit public proof steps, not word matching, hidden culprit flags or verdict inference.
# delta is visible argumentative pressure, not guilt. "recover" acknowledges a sound defense.
R13_REC_STAGE_STEPS = {
 1: {
    'empty_heat': dict(target='nabi', delta=1, group=False),
    'stone': dict(target='nabi', delta=0, group=False),
    'child': dict(target='nabi', delta=1, group=True),
    'container': dict(target='nabi', delta=1, group=True),
 },
 2: {
    'e2_card_rail': dict(target='guard', delta=1, group=False),
    'e2_card_badook': dict(target='guard', delta=1, group=True),
    'e2_card_ties': dict(target='guard', delta=1, group=False),
    'e2_card_dolmok': dict(target='guard', delta=0, group=False),
    'e2_order': dict(target='guard', delta=1, group=True),
 },
 3: {
    'e3_card_wall': dict(target='resident_nubi', delta=1, group=False),
    'e3_card_teacher': dict(target='resident_nubi', delta=1, group=True),
    'e3_card_can': dict(target='resident_nubi', delta=0, group=False, recover=True),
    'e3_map_0': dict(target='resident_nubi', delta=0, group=False),
    'e3_map_1': dict(target='resident_nubi', delta=0, group=False),
    'e3_map_2': dict(target='resident_nubi', delta=0, group=False),
    'e3_map_3': dict(target='resident_nubi', delta=0, group=False),
    'e3_map_4': dict(target='resident_nubi', delta=0, group=False),
    # The source geometry gate decides whether this is a limited conclusion.
    'e3_finish': dict(target='resident_nubi', delta=1, group=True),
 },
 4: {
    'e4_tool_use': dict(target='neoul', delta=1, group=False),
    'e4_daram_side': dict(target='neoul', delta=1, group=False),
    'e4_alive': dict(target='neoul', delta=1, group=True),
    'e4_course': dict(target='neoul', delta=1, group=False),
    'e4_external_open': dict(target='neoul', delta=1, group=True),
    'e4_knowledge7': dict(target='neoul', delta=1, group=False),
    'e4_refusal': dict(target='neoul', delta=1, group=True),
    'e4_access9': dict(target='neoul', delta=1, group=False),
    'e4_work_warning': dict(target='neoul', delta=1, group=True),
 },
 5: {
    'e5_cabinet_kept': dict(target='resident_teacher', delta=0, group=False, recover=True),
    'e5_room_kept': dict(target='resident_teacher', delta=0, group=False, recover=True),
    'e5_body': dict(target='resident_teacher', delta=1, group=True),
    'e5_original_target': dict(target='resident_teacher', delta=0, group=False, recover=True),
    'e5_label_path': dict(target='resident_teacher', delta=1, group=True),
    'e5_lid_actor': dict(target='resident_teacher', delta=1, group=False),
    'e5_same_bottle': dict(target='resident_teacher', delta=1, group=False),
    'e5_responsibility': dict(target='resident_teacher', delta=1, group=True),
 },
 6: {
    'e6_false_status': dict(target='resident_ppul', delta=1, group=False),
    'e6_dates': dict(target='granny', delta=1, group=False),
    'e6_prior_notice': dict(target='granny', delta=1, group=True),
    'e6_order': dict(target='granny', delta=1, group=True),
    'e6_next_carer': dict(target='granny', delta=1, group=False),
    'e6_altar_care': dict(target='granny', delta=1, group=True),
    'e6_today_heat': dict(target='granny', delta=0, group=False, recover=True),
    'e6_real_preparation': dict(target='granny', delta=1, group=False),
    'e6_granny_choice': dict(target='granny', delta=1, group=True),
 },
}
R13_REC_STAGE_LINE_CUES = {
    'recommended:hearing:new-defense': 'recover',
    'recommended:hearing:earlier-account': 'listen',
    'recommended:hearing:direct-removal': 'settle',
    'recommended:hearing:result': 'settle',
    'recommended:e2:new-order-claim': 'recover',
    'recommended:e2:blanket-rebuttal': 'recover',
    'recommended:e2:separate-responsibility': 'settle',
    'recommended:e2:partial-result': 'settle',
    'recommended:e3:legitimate-resistance': 'recover',
    'recommended:e3:can-rebuttal': 'recover',
    'recommended:e3:new-handoff-path': 'recover',
    'recommended:e3:conclusion': 'settle',
    'recommended:late:hearing:challenge': 'listen',
    'recommended:late:hearing:wrong-card': 'recover',
    'recommended:e5:hearing:body': 'recover',
    'recommended:e4:result:detained': 'settle',
    'recommended:e5:result:prevented': 'settle',
    'recommended:e5:result:responsibility': 'settle',
    'recommended:e6:result:execution': 'settle',
}

def r13_rec_stage_claim(episode):
    return 'REC_HEARING_%d' % episode

def r13_rec_stage_roster(episode, campaign):
    people = list(R13_REC_STAGE_HEARINGS[episode]['cast'])
    # Reunion is necessary but not sufficient: only EP6 authors Mother at the meeting.
    explicit = campaign.get('meeting_present', {}).get(str(episode))
    if explicit is not None:
        people = [p for p in people if p in explicit]
    return [p for p in people if p != 'dad'
        and (p != 'mom' or campaign.get('mother') == 'M2')
        and (p != 'resident_piko' or campaign.get('piko') == 'safe')
        and (p != 'neoul' or campaign.get('neoul', 'active') != 'detained')
        and (p != 'kid_nubi1' or campaign.get('episodes', {}).get('3', {}).get('privacy') is True)]

def r13_rec_stage_new(episode):
    return dict(episode=episode, claim=r13_rec_stage_claim(episode), pressure={}, seen=[],
        group={}, beat='listen', focus=None, step=None, last_line=None, silence=False, feedback=False)

def r13_rec_stage_pressure_pose(level):
    return ('neutral', 'anxious', 'flustered', 'anxious')[max(0, min(3, level))]

def r13_rec_stage_reduce(session, step_id, correct, campaign):
    state = copy.deepcopy(session)
    spec = R13_REC_STAGE_STEPS.get(state['episode'], {}).get(step_id)
    if spec is None:
        return state
    target = spec['target']
    state.update(step=step_id, feedback=True, focus=target, group={}, silence=False, last_line=None)
    state['beat'] = 'recover' if not correct or spec.get('recover') else 'shaken' if spec['delta'] else 'explain'
    token = '%s:%s:%s' % (state['claim'], step_id, 'correct' if correct else 'defended')
    if token in state['seen']:
        return state
    state['seen'].append(token)
    pressure = state['pressure'].get(target, 0)
    if not correct or spec.get('recover'):
        pressure = max(0, pressure - 1)
    else:
        pressure = min(3, pressure + spec['delta'])
    state['pressure'][target] = pressure
    # A limited conclusion cannot visually convict an unverified EP3 alternative.
    limited = step_id == 'e3_finish' and campaign.get('episodes', {}).get('3', {}).get('verdict') != 'nubi_ignition_bori_afterward'
    if limited:
        state['beat'] = 'settle'
        state['pressure'][target] = max(0, pressure - spec['delta'])
    elif correct and spec.get('group'):
        state['silence'] = True
        state['group'] = {p: dict(token=token+':'+p, phase='pending') for p in r13_rec_stage_roster(state['episode'], campaign)}
    return state

def r13_rec_stage_settle_model(session):
    state = copy.deepcopy(session)
    state['silence'] = False
    state['group'] = {p: dict(reaction, phase='settled') for p, reaction in state.get('group', {}).items()}
    return state
