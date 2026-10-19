# Recommended-only six-hearing presentation. Source-wired, native validation pending.
# Default-off: no release activation without the native matrix in the handoff document.
default r13_rec_staging_enabled = False
default r13_rec_staging_active = False
default r13_rec_staging_snapshot = None
default r13_rec_stage_session = None
default r13_rec_stage_memory = {}
default r13_rec_stage_preview_mode = False

init 925 python:
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

    # Narrow adapters: legacy callers still receive the exact existing implementation.
    R13_REC_STAGE_CLAIMS = {r13_rec_stage_claim(ep): ep for ep in R13_REC_STAGE_HEARINGS}
    for _ep, _spec in R13_REC_STAGE_HEARINGS.items():
        _session = 'rec_hearing_%d' % _ep
        R13_MEETING_VENUES[_session] = (_spec['venue'], _spec['kind'], _spec['title'])
        R13_EP_MEETING_PLACE[_session] = _spec['background']
    _r13_rec_stage_session_base = r13_debate_session
    def r13_debate_session(claim):
        ep = R13_REC_STAGE_CLAIMS.get(claim)
        return 'rec_hearing_%d' % ep if ep else _r13_rec_stage_session_base(claim)
    _r13_rec_stage_cast_base = r13_meeting_cast
    def r13_meeting_cast(claim, session, speaker=None):
        ep = R13_REC_STAGE_CLAIMS.get(claim)
        if ep:
            return [(p, None) for p in r13_rec_stage_roster(ep, getattr(store, 'r13_recommended', {}) or {}) if p in CAST]
        return _r13_rec_stage_cast_base(claim, session, speaker)
    _r13_rec_stage_focus_base = r13_meeting_focus_person
    def r13_meeting_focus_person(claim):
        if claim not in R13_REC_STAGE_CLAIMS:
            return _r13_rec_stage_focus_base(claim)
        people = [p for p, _ in r13_meeting_cast(claim, r13_debate_session(claim))]
        focus = getattr(store, 'r13_meeting_focus', None)
        return focus if focus in people else (people[0] if people else None)

    R13_REC_STAGE_LEGACY_SCREENS = ('r13_book', 'r13_records', 'r13_meeting_agenda',
        'r13_debate_board', 'r13_meeting_rebuttal_hold', 'r13_meeting_ballot',
        'r13_meeting_evidence_hold', 'r13_meeting_objection', 'r13_meeting_cut_in',
        'r13_more_tools', 'r13_material_corner', 'r13_hud')
    R13_REC_STAGE_FIELDS = ('dialogue_speaker', 'dialogue_expression', 'r13_last_partner',
        'r13_meeting_focus', 'r13_meeting_previous_focus', 'r13_meeting_previous_expression',
        'r13_meeting_shot_revision', 'r13_meeting_pan_direction', 'r13_meeting_pan_started',
        'r13_meeting_pan_painted_revision', 'r13_meeting_direction', 'r13_meeting_direction_poses',
        'r13_meeting_direction_music', 'r13_meeting_line_token', 'r13_meeting_listener',
        'r13_meeting_art_slots', 'r13_meeting_reaction')
    R13_REC_STAGE_BASE_CHARS = dict(R13_CHARS)
    R13_REC_STAGE_BASE_THOUGHT = source_thought
    R13_REC_STAGE_CHARS = {key: Character(char.name, kind=char, screen='r13_rec_stage_say') for key, char in R13_CHARS.items()}
    R13_REC_STAGE_THOUGHT = Character(None, kind=source_thought, screen='r13_rec_stage_say')

    def r13_rec_stage_active():
        return bool(getattr(store, 'r13_rec_staging_active', False) and getattr(store, 'r13_rec_stage_session', None))

    def r13_rec_stage_clear_legacy():
        # Do not create a fake old claim: that would open old records and proof menus.
        store.r13_meeting_active = False
        store.r13_meeting_claim = None
        store.r13_meeting_live_active = False
        store.r13_meeting_live_sid = None
        store.r13_meeting_live_command = None
        store.r13_meeting_pending_resume = None
        store.r13_meeting_resume_listening = False
        store.r13_meeting_interrupting = False
        store.r13_meeting_replaying = False
        store.r13_meeting_intro = False
        store.r13_meeting_proof_reveal = None
        store.r13_meeting_shock_target = None
        store.r13_meeting_reaction = None
        store.r13_meeting_direction_return_audio = {}
        for screen_name in R13_REC_STAGE_LEGACY_SCREENS:
            renpy.hide_screen(screen_name)
        renpy.hide('r13_visitor')

    def r13_rec_stage_audio():
        if not r13_rec_stage_active(): return
        state = store.r13_rec_stage_session
        beat = state.get('beat', 'listen')
        # Same approved tracks/ambience and channel gain API as meeting_direction.
        # No impact SFX: typewriter callbacks remain on the inherited Characters.
        wanted = 'pressure' if beat in ('recover', 'reversal', 'cornered') else (state.get('music') or 'council')
        path = R13_BGM[wanted]
        if renpy.music.get_playing(channel='music') != path:
            renpy.music.play(path, channel='music', loop=True, fadeout=.28, fadein=.35)
        renpy.music.set_pause(False, channel='music')
        gain = 0.0 if state.get('silence') else R13_MEETING_BEATS.get(beat, R13_MEETING_BEATS['listen'])[1]
        renpy.music.set_volume(gain, delay=.16, channel='music')
        r13_sound_ambience('wind' if R13_REC_STAGE_HEARINGS[state['episode']]['kind'] == 'field' else 'fire')
        store.r13_rec_stage_session = dict(state, music=wanted)

    def r13_rec_stage_paint():
        if not r13_rec_stage_active(): return
        state = store.r13_rec_stage_session
        claim = state['claim']
        people = [p for p, _ in r13_meeting_cast(claim, r13_debate_session(claim))]
        focus = state.get('focus')
        if focus not in people: focus = people[0] if people else None
        if focus: r13_meeting_focus_change(claim, focus)
        store.r13_meeting_direction = dict(claim=claim, beat=state.get('beat', 'listen'))
        store.r13_meeting_direction_poses = {p: r13_rec_stage_pressure_pose(state['pressure'].get(p, 0)) for p in people}
        store.r13_meeting_art_slots = {}
        store.r13_meeting_listener = next((p for p in people if p != focus and state.get('group', {}).get(p, {}).get('phase') == 'pending'), None)
        store.r13_meeting_line_token = state.get('last_line')

    def r13_rec_stage_enter(episode, preview=False):
        if not (getattr(store, 'r13_rec_staging_enabled', False) or preview): return False
        if episode not in R13_REC_STAGE_HEARINGS: return False
        if not preview and (getattr(store, 'r13_recommended', {}) or {}).get('episode') != episode: return False
        if r13_rec_stage_active() and store.r13_rec_stage_session['episode'] == episode: return True
        if r13_rec_stage_active(): r13_rec_stage_exit()
        # Finish any legacy audio ownership before taking our own snapshot.
        r13_meeting_direct_end()
        snapshot = {key: copy.deepcopy(getattr(store, key, None)) for key in R13_REC_STAGE_FIELDS}
        snapshot['return_stack'] = list(renpy.get_return_stack())
        snapshot['audio'] = {channel: dict(path=renpy.music.get_playing(channel=channel),
            volume=r13_meeting_channel_gain(channel), paused=renpy.music.get_pause(channel=channel))
            for channel in ('music', 'ambience')}
        store.r13_rec_staging_snapshot = snapshot
        saved = (getattr(store, 'r13_rec_stage_memory', {}) or {}).get(str(episode))
        store.r13_rec_stage_session = r13_rec_stage_settle_model(saved) if saved and not preview else r13_rec_stage_new(episode)
        store.r13_rec_staging_active = True
        store.r13_rec_stage_preview_mode = bool(preview)
        r13_rec_stage_clear_legacy()
        store.r13_meeting_focus = None
        store.r13_meeting_previous_focus = None
        store.R13_CHARS = dict(R13_REC_STAGE_CHARS)
        store.source_thought = R13_REC_STAGE_THOUGHT
        r13_rec_stage_paint()
        r13_rec_stage_audio()
        return True

    def r13_rec_stage_prompt(step_id):
        if not r13_rec_stage_active(): return
        state = r13_rec_stage_settle_model(store.r13_rec_stage_session)
        state.update(step=step_id, beat='select', feedback=False)
        store.r13_rec_stage_session = state
        r13_rec_stage_paint()
        r13_rec_stage_audio()

    def r13_rec_stage_answer(step_id, correct):
        if not r13_rec_stage_active(): return
        store.r13_rec_stage_session = r13_rec_stage_reduce(store.r13_rec_stage_session, step_id, bool(correct), store.r13_recommended)
        r13_rec_stage_paint()
        r13_rec_stage_audio()

    def r13_rec_stage_settle():
        if not r13_rec_stage_active(): return
        store.r13_rec_stage_session = r13_rec_stage_settle_model(store.r13_rec_stage_session)
        r13_rec_stage_paint()
        r13_rec_stage_audio()

    _r13_rec_stage_line_base = r13_meeting_direct_line
    def r13_meeting_direct_line(identity, index, packet, expression, pose):
        if not r13_rec_stage_active() or not identity.startswith('recommended:'):
            return _r13_rec_stage_line_base(identity, index, packet, expression, pose)
        state = copy.deepcopy(store.r13_rec_stage_session)
        token = (identity, index, packet[0], packet[1])
        if token != state.get('last_line'):
            # Preserve the reveal through its explanation, not merely the first click.
            if state.get('last_line') and state['last_line'][0] != identity:
                state = r13_rec_stage_settle_model(state)
            state['last_line'] = token
            if identity in R13_REC_STAGE_LINE_CUES:
                state['beat'] = R13_REC_STAGE_LINE_CUES[identity]
            elif not state.get('feedback'):
                state['beat'] = 'listen'
        people = r13_rec_stage_roster(state['episode'], store.r13_recommended)
        person = packet[0]
        if person in people:
            state['focus'] = person
            # Authored non-neutral poses remain authoritative; nervous talking persists.
            if pose in (None, 'neutral', 'interview_neutral'):
                pose = r13_rec_stage_pressure_pose(state['pressure'].get(person, 0))
            expression = pose
        store.r13_rec_stage_session = state
        r13_rec_stage_paint()
        if person in people: store.r13_meeting_direction_poses[person] = pose
        r13_rec_stage_audio()
        return expression, pose

    _r13_rec_stage_speaker_base = r13_speaker
    def r13_speaker(who, expression='neutral', pose=None):
        if not r13_rec_stage_active(): return _r13_rec_stage_speaker_base(who, expression, pose)
        people = r13_rec_stage_roster(store.r13_rec_stage_session['episode'], store.r13_recommended)
        if who in people and who in CAST:
            r13_meeting_focus_change(store.r13_rec_stage_session['claim'], who)
            store.r13_rec_stage_session = dict(store.r13_rec_stage_session, focus=who)
        store.dialogue_speaker = who if who in CAST else None
        store.dialogue_expression = expression
        renpy.hide('r13_visitor')

    _r13_rec_stage_reaction_art_base = r13_meeting_reaction_art
    def r13_meeting_reaction_art(person, pose, height, settled):
        if not r13_rec_stage_active(): return _r13_rec_stage_reaction_art_base(person, pose, height, settled)
        reaction = store.r13_rec_stage_session.get('group', {}).get(person)
        if not reaction or reaction['phase'] == 'settled': return settled
        # Existing approved source frame and shared phase rules, no new art/filter.
        profile = r13_dialogue_source_profile(person, 'surprise', height)
        frame = (profile or {}).get('frames', {}).get('surprise_react')
        if frame and renpy.loadable(frame['file']):
            react = Fixed(Transform(frame['file'], xpos=frame['offset'][0], ypos=frame['offset'][1],
                zoom=frame.get('scale', 1.0), nearest=False, subpixel=True), xysize=tuple(profile['canvas']))
        else:
            react = r13_fullbody_close_art(person, 'surprise', height) or settled
        return R13RecStageReaction(person, reaction['token'], react, settled)

    class R13RecStageReaction(renpy.Displayable):
        def __init__(self, person, token, react, settled, **kwargs):
            super(R13RecStageReaction, self).__init__(**kwargs)
            self.person, self.token, self.react, self.settled = person, token, react, settled
            self.claimed, self.started = False, None
        def visit(self): return [self.react, self.settled]
        def render(self, width, height, st, at):
            if renpy.predicting() or not r13_rec_stage_active(): return renpy.render(self.settled, width, height, st, at)
            state = store.r13_rec_stage_session
            reaction = state.get('group', {}).get(self.person)
            elapsed = 0.0 if self.started is None else max(0.0, st-self.started)
            phase = r13_meeting_reaction_phase(reaction, self.token, self.claimed, elapsed,
                renpy.is_skipping() or renpy.in_rollback() or not persistent.room13_motion)
            if phase == 'playing':
                if not self.claimed:
                    self.claimed, self.started = True, st
                    group = dict(state['group']); group[self.person] = dict(reaction, phase='playing')
                    store.r13_rec_stage_session = dict(state, group=group)
                renpy.redraw(self, .035)
                return renpy.render(self.react, width, height, st, at)
            if reaction and reaction['phase'] != 'settled':
                group = dict(state['group']); group[self.person] = dict(reaction, phase='settled')
                store.r13_rec_stage_session = dict(state, group=group)
            return renpy.render(self.settled, width, height, st, at)

    def r13_rec_stage_exit():
        if not r13_rec_stage_active() and not getattr(store, 'r13_rec_staging_snapshot', None): return
        if r13_rec_stage_active() and not getattr(store, 'r13_rec_stage_preview_mode', False):
            memory = dict(getattr(store, 'r13_rec_stage_memory', {}) or {})
            memory[str(store.r13_rec_stage_session['episode'])] = r13_rec_stage_settle_model(store.r13_rec_stage_session)
            store.r13_rec_stage_memory = memory
        snapshot = getattr(store, 'r13_rec_staging_snapshot', {}) or {}
        store.r13_rec_staging_active = False
        store.R13_CHARS = dict(R13_REC_STAGE_BASE_CHARS)
        store.source_thought = R13_REC_STAGE_BASE_THOUGHT
        r13_meeting_direct_end()
        for key in R13_REC_STAGE_FIELDS:
            if key in snapshot: setattr(store, key, snapshot[key])
        for channel, state in snapshot.get('audio', {}).items():
            path = state['path']
            if renpy.music.get_playing(channel=channel) != path:
                if path: renpy.music.play(path, channel=channel, loop=True, fadeout=.2, fadein=.2)
                else: renpy.music.stop(channel=channel, fadeout=.2)
            renpy.music.set_volume(state['volume'], delay=.2, channel=channel)
            renpy.music.set_pause(state['paused'], channel=channel)
        r13_rec_stage_clear_legacy()
        store.r13_meeting_direction = {}
        store.r13_meeting_direction_poses = {}
        store.r13_meeting_art_slots = {}
        store.r13_meeting_line_token = None
        store.r13_meeting_focus = None
        store.r13_meeting_previous_focus = None
        store.r13_rec_stage_session = None
        store.r13_rec_staging_snapshot = None
        store.r13_rec_stage_preview_mode = False
        renpy.hide_screen('r13_rec_stage_pause')
        renpy.hide_screen('r13_rec_stage_say')
        renpy.music.stop(channel='typing')

    def r13_rec_stage_leave():
        # A footer may interrupt inside r13_lines or a nested inspection call.
        # Unwind only calls made after entry, including their dynamic variables.
        saved_stack = list((getattr(store, 'r13_rec_staging_snapshot', {}) or {}).get('return_stack', renpy.get_return_stack()))
        while len(renpy.get_return_stack()) > len(saved_stack):
            renpy.pop_call()
        renpy.set_return_stack(saved_stack)
        r13_rec_stage_exit()
        renpy.jump('r13_recommended_hub')

    def r13_rec_stage_after_load():
        if not r13_rec_stage_active(): return
        # Other meeting load callbacks ran first and may have cleared camera fields.
        # Restore our own saved session without repeating the reveal or modifying progress.
        store.r13_rec_stage_session = r13_rec_stage_settle_model(store.r13_rec_stage_session)
        r13_rec_stage_clear_legacy()
        store.R13_CHARS = dict(R13_REC_STAGE_CHARS)
        store.source_thought = R13_REC_STAGE_THOUGHT
        store.r13_meeting_previous_focus = None
        r13_rec_stage_paint()
        r13_rec_stage_audio()
    config.after_load_callbacks.append(r13_rec_stage_after_load)

    _r13_rec_stage_afm_base = config.afm_callback
    def r13_rec_stage_afm():
        if r13_rec_stage_active() and any(renpy.get_screen(name) for name in (
                'r13_rec_stage_pause', 'r13_recommended_notebook', 'r13_recommended_card_detail',
                'r13_recommended_cards', 'r13_rec_stage_choice')): return False
        return _r13_rec_stage_afm_base() if _r13_rec_stage_afm_base else True
    config.afm_callback = r13_rec_stage_afm

screen r13_rec_stage_background():
    if r13_rec_staging_active and r13_rec_stage_session:
        $ claim = r13_rec_stage_session['claim']
        use r13_meeting_stage(claim, r13_meeting_focus_person(claim), True)
        frame:
            area (24,18,1000,64) padding (16,10) background R13PaperFrame()
            text R13_REC_STAGE_HEARINGS[r13_rec_stage_session['episode']]['title'] size r13_read_size(23,27) color '#493b30'
        if r13_rec_stage_session.get('silence'):
            timer .42 action Function(r13_rec_stage_settle)

screen r13_rec_stage_footer():
    hbox:
        xpos 24 ypos r13_control_y() spacing 12
        use r13_control('수첩 · 확인한 사실', 'record', Function(renpy.call_in_new_context, 'r13_rec_stage_notebook'), width=300)
        use r13_control('지나간 대화', 'dialogue', Show('r13_backlog'), width=250)
        use r13_control('잠깐 멈추기', None, Show('r13_rec_stage_pause'), width=250)
        use r13_control('저장 · 불러오기', 'record', ShowMenu('save'), width=350)
    key 'K_h' action Show('r13_backlog')
    key 'game_menu' action Show('r13_rec_stage_pause')

screen r13_rec_stage_say(who, what):
    tag say
    use r13_rec_stage_background()
    $ who = r13_speaker_label(who)
    window:
        id 'window'
        area (80,r13_control_y()-148,1120,132) background R13InkPanel(alpha='d9',slim=True) padding (22,36,22,14)
        r13_dialogue_text what id 'what' style 'say_dialogue' size r13_read_size(23,29) line_spacing 5 xsize 1076 font r13_ui_font() color '#fff4df'
    if who:
        text who id 'who' xpos 104 ypos (r13_control_y()-144) size r13_read_size(24,26) color '#f6dfac' font r13_ui_font() xmaximum 1076
    text '▸' xpos 1160 ypos (r13_control_y()-48) size 24 color '#e8d9b0'
    timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
    use r13_rec_stage_footer()

screen r13_rec_stage_choice(items):
    if not r13_rec_staging_active:
        use choice(items)
    else:
        modal True
        use r13_rec_stage_background()
        frame:
            area (100,220,1080,390) padding (22,18) background R13InkPanel(alpha='ed',slim=True)
            viewport:
                mousewheel True draggable True scrollbars 'vertical'
                vbox:
                    spacing 14
                    for item in items:
                        if item.action is None:
                            text item.caption size 24 color '#fff4df' xsize 1000
                        else:
                            textbutton item.caption action item.action xsize 1000 text_size r13_read_size(22,26)
        use r13_rec_stage_footer()

screen r13_rec_stage_pause():
    modal True
    zorder 120
    add Solid('#10212adf')
    frame:
        xalign .5 yalign .5 xsize 760 padding (30,24) background R13PaperFrame()
        vbox:
            spacing 20
            text '회의를 잠깐 멈췄어요' size 30 color '#493b30'
            text '확인한 사실과 답변은 그대로 남습니다.' size 22 color '#493b30'
            textbutton '이 말부터 계속 듣기' action Hide('r13_rec_stage_pause') text_size 26
            textbutton '수첩을 보고 돌아오기' action [Hide('r13_rec_stage_pause'), Function(renpy.call_in_new_context, 'r13_rec_stage_notebook')] text_size 26
            textbutton '현장으로 돌아가 다시 조사하기' action Function(r13_rec_stage_leave) text_size 26
            textbutton '저장 · 불러오기' action ShowMenu('save') text_size 26
    key 'game_menu' action Hide('r13_rec_stage_pause')

label r13_rec_stage_notebook:
    call screen r13_recommended_notebook
    while _return is not None:
        $ r13_rec_stage_card = _return.split(':', 1)[1]
        call screen r13_recommended_card_detail(r13_rec_stage_card)
        call screen r13_recommended_notebook
    return

screen r13_rec_stage_preview():
    modal True
    use r13_rec_stage_background()
    frame:
        area (30,440,1220,250) padding (20,16) background R13InkPanel(alpha='ed',slim=True)
        vbox:
            spacing 14
            text '실제 여섯 회의의 연출 연결 검증 · 본편 기본 꺼짐' size 24
            hbox:
                spacing 16
                for ep in range(1,7):
                    textbutton ('회의 %d' % ep) action [Function(r13_rec_stage_exit), Function(r13_rec_stage_enter, ep, True)]
            hbox:
                spacing 18
                textbutton '근거에 흔들림' action Function(r13_rec_stage_answer, next(iter(R13_REC_STAGE_STEPS[r13_rec_stage_session['episode']])), True)
                textbutton '반문이 타당함' action Function(r13_rec_stage_answer, next(iter(R13_REC_STAGE_STEPS[r13_rec_stage_session['episode']])), False)
                textbutton '큰 사실에 함께 놀람' action Function(r13_rec_stage_answer, next(key for key, value in R13_REC_STAGE_STEPS[r13_rec_stage_session['episode']].items() if value.get('group')), True)
            textbutton '돌아가기' action Return(True)
    key 'game_menu' action Return(True)

label r13_recommended_staging_admin:
    $ r13_rec_stage_enter((r13_recommended or {}).get('episode',1), preview=True)
    call screen r13_rec_stage_preview
    $ r13_rec_stage_exit()
    return
