"""정면 대화 원본의 승인·감정 완비·화면 문맥과 원래 자세의 경계를 확인한다."""
import ast
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {'neutral', 'joy', 'angry', 'anxious', 'flustered', 'surprise_talk'}
PEOPLE = {'daram', 'guard', 'resident_piko', 'resident_bori', 'karo', 'doto', 'neoul', 'resident_siluk', 'resident_seori', 'seryeon', 'resident_kongi', 'resident_ubak'}
NEW_PEOPLE=set(json.loads((ROOT/'art/dialogue-gaze-20261107/runtime-fit-targets.json').read_text()))


def profiles(prefix):
    return {str(h): dict(canvas=[500, h + 66], frames={slot: dict(
        file=(f'assets/dialogue-player-facing/actor-flustered.webp' if prefix == 'front' and slot == 'flustered'
              else f'assets/{"dialogue-source-master" if prefix == "front" else "dialogue-dot-v2"}/actor/{h}/{slot}.webp'),
        offset=[16, 22], nearest=False) for slot in SLOTS}) for h in (560, 760, 840)}


class PlayerFacingProfiles(unittest.TestCase):
    def setUp(self):
        source = (ROOT / 'game/systems/room13_dialogue_beats.rpy').read_text()
        tree = ast.parse(textwrap.dedent(source.split('init 170 python:', 1)[1]))
        wanted = {'r13_dialogue_fit_profile', 'r13_dialogue_pose_source', 'r13_dialogue_player_profiles',
                  'r13_dialogue_render_profiles', 'r13_dialogue_source_profile', 'r13_dialogue_beat_art'}
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
        self.original = profiles('original')
        self.front = profiles('front')
        self.front_entry = dict(status='approved_runtime', gaze='player', stance='standing',
                                source_kind='source_master', art_style='storybook_source', profiles=self.front)
        self.loads = []
        self.env = dict(store=types.SimpleNamespace(r13_meeting_active=False, r13_thought_active=False,
                                                    r13_meeting_focus=None),
                        renpy=types.SimpleNamespace(loadable=lambda path: self.loads.append(path) or True),
                        R13_DIALOGUE_PLAYER_FACING=dict(people=dict(actor=self.front_entry)),
                        _r13_player_facing_ready={}, R13_DIALOGUE_B_ART_ON=False,
                        R13_CLOSEUP_SMOOTH=False, R13_MEETING_SOLO=False,
                        R13_DIALOGUE_POSE_SOURCE=dict(people={}),
                        R13_DIALOGUE_TALK_ART=dict(people=dict(actor=dict(status='approved_runtime', profiles=self.original))),
                        R13_FULLBODY_PLAIN=SLOTS | {'surprise', 'thinking'},
                        r13_fullbody_key=lambda pose: pose.removeprefix('interview_'))
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '정면 대화 선택', 'exec'), self.env)

    def render(self, player_facing=True):
        return self.env['r13_dialogue_render_profiles']('actor', self.env['R13_DIALOGUE_TALK_ART']['people']['actor'],
                                                       player_facing=player_facing)

    def test_only_explicit_direct_portrait_path_uses_complete_approved_front_set(self):
        self.assertIs(self.render(), self.front)
        self.assertIs(self.render(False), self.original)
        self.assertEqual(set(self.front['840']['frames']), SLOTS)

    def test_reviewed_beat_default_and_existing_b_selection_are_unchanged(self):
        old_b = profiles('old-b')
        self.env.update(R13_DIALOGUE_B_ART_ON=True, R13_DIALOGUE_B_ART={'actor': old_b})
        render = self.env['r13_dialogue_render_profiles']
        entry = self.env['R13_DIALOGUE_TALK_ART']['people']['actor']
        self.assertIs(render('actor', entry), old_b)
        self.assertIs(self.render(), self.front)

    def guard(self):
        self.env['R13_DIALOGUE_PLAYER_FACING']['people']['guard'] = self.front_entry
        entry = dict(status='approved_runtime', profiles=self.original)
        self.env['R13_DIALOGUE_TALK_ART']['people']['guard'] = entry
        return entry

    def test_guard_direct_and_reviewed_beat_share_approved_expressions(self):
        entry = self.guard()
        render = self.env['r13_dialogue_render_profiles']
        old_b = profiles('old-b')
        self.env.update(R13_DIALOGUE_B_ART_ON=True, R13_DIALOGUE_B_ART={'guard': old_b})
        for direct in (False, True):
            with self.subTest(direct=direct):
                chosen = render('guard', entry, direct)
                self.assertIs(chosen, self.front)
                self.assertEqual(set(chosen['840']['frames']), SLOTS)
                self.assertNotIn('surprise_react', chosen['840']['frames'])
                self.assertIsNot(chosen['840']['frames']['flustered'], chosen['840']['frames']['anxious'])
        get = self.env['r13_dialogue_source_profile']
        for slot in SLOTS:
            self.assertIs(get('guard', slot, 840), self.front['840'])
        # 돌목의 예외가 다른 인물의 비직접 표정 선택으로 퍼지지 않는다.
        self.assertIs(self.render(False), self.original)

    def test_guard_meeting_retains_direct_solo_focus_boundary(self):
        entry = self.guard()
        render = self.env['r13_dialogue_render_profiles']
        state = self.env['store']
        state.r13_meeting_active = True
        for solo, focus, direct in ((False, 'guard', False), (False, 'guard', True),
                                    (True, 'other', False), (True, 'other', True),
                                    (True, 'guard', False), (True, 'guard', True)):
            with self.subTest(solo=solo, focus=focus, direct=direct):
                self.env['R13_MEETING_SOLO'] = solo
                state.r13_meeting_focus = focus
                expected = self.front if solo and focus == 'guard' and direct else self.original
                self.assertIs(render('guard', entry, direct), expected)

    def test_guard_incomplete_or_unapproved_set_keeps_original_matching_slots(self):
        entry = self.guard()
        render = self.env['r13_dialogue_render_profiles']
        del self.front['760']['frames']['flustered']
        for direct in (False, True):
            chosen = render('guard', entry, direct)
            self.assertIs(chosen, self.original)
            self.assertNotEqual(chosen['840']['frames']['flustered']['file'],
                                chosen['840']['frames']['anxious']['file'])
        self.front['760']['frames']['flustered'] = profiles('front')['760']['frames']['flustered']
        self.env['_r13_player_facing_ready'].clear()
        self.front_entry['status'] = 'HOLD_MISSING_FLUSTERED'
        for direct in (False, True):
            self.assertIs(render('guard', entry, direct), self.original)

    def test_guard_missing_master_does_not_partially_replace_beat(self):
        entry = self.guard()
        self.env['renpy'].loadable = lambda path: not path.endswith('/760/joy.webp')
        render = self.env['r13_dialogue_render_profiles']
        for direct in (False, True):
            self.assertIs(render('guard', entry, direct), self.original)

    def test_missing_flustered_keeps_original_flustered_without_emotion_substitution(self):
        del self.front['760']['frames']['flustered']
        chosen = self.render()
        self.assertIs(chosen, self.original)
        self.assertIn('/flustered.webp', chosen['840']['frames']['flustered']['file'])
        self.assertNotEqual(chosen['840']['frames']['flustered']['file'], chosen['840']['frames']['anxious']['file'])

    def test_hold_wrong_gaze_and_missing_source_fail_closed(self):
        for field, value in [('status', 'HOLD_MISSING_FLUSTERED'), ('gaze', 'paper')]:
            original = self.front_entry[field]
            self.front_entry[field] = value
            self.assertIs(self.render(), self.original)
            self.front_entry[field] = original
        self.env['renpy'].loadable = lambda path: not path.endswith('/760/joy.webp')
        self.assertIs(self.render(), self.original)

    def test_readiness_is_memoized_without_rebuilding_profiles(self):
        self.assertIs(self.render(), self.front)
        count = len(self.loads)
        self.assertEqual(count, 18)
        self.assertIs(self.render(), self.front)
        self.assertEqual(len(self.loads), count)

    def test_unlisted_person_uses_original_profiles(self):
        self.assertIs(self.env['r13_dialogue_render_profiles']('other', dict(profiles=self.original), True), self.original)

    def test_meeting_only_solo_focus_can_use_front_source(self):
        state = self.env['store']
        state.r13_meeting_active = True
        state.r13_meeting_focus = 'actor'
        self.assertIs(self.render(), self.original)
        self.env['R13_MEETING_SOLO'] = True
        self.assertIs(self.render(), self.front)
        state.r13_meeting_focus = 'other'
        self.assertIs(self.render(), self.original)
        self.assertIs(self.render(False), self.original)

    def test_authored_work_pose_and_thought_keep_existing_paths(self):
        work = profiles('work')
        self.env['R13_DIALOGUE_POSE_SOURCE']['people']['actor'] = dict(pose_profiles=dict(write_notes=dict(profiles=work)))
        get = self.env['r13_dialogue_source_profile']
        self.assertIs(get('actor', 'write_notes', 840), work['840'])
        self.assertIs(get('actor', 'neutral', 840), self.front['840'])
        self.env['store'].r13_thought_active = True
        self.assertIsNone(get('actor', 'neutral', 840))
        self.assertIs(get('actor', 'write_notes', 840), work['840'])

    def test_front_scale_preserves_source_and_relative_geometry_without_dot_grid(self):
        get = self.env['r13_dialogue_source_profile']
        scaled = get('actor', 'neutral', 1302)
        ratio = 1302 / 840
        self.assertEqual(scaled['canvas'], [round(500 * ratio), round(906 * ratio)])
        for slot in SLOTS:
            self.assertEqual(scaled['frames'][slot]['file'], self.front['840']['frames'][slot]['file'])
            self.assertEqual(scaled['frames'][slot]['offset'], [round(16 * ratio), round(22 * ratio)])
            self.assertAlmostEqual(scaled['frames'][slot]['scale'], ratio)
            self.assertFalse(scaled['frames'][slot]['nearest'])

    def test_registry_reuses_matching_emotions_and_never_adds_side_reaction(self):
        data = json.loads((ROOT / 'game/assets/room13-dialogue-player-facing.json').read_text())['people']
        self.assertEqual(set(data), PEOPLE | NEW_PEOPLE)
        for who, entry in data.items():
            self.assertEqual(entry['gaze'], 'player')
            self.assertTrue(entry['status'] == 'approved_runtime' or entry['status'].startswith('HOLD'))
            for height, profile in entry['profiles'].items():
                frames = profile['frames']
                self.assertNotIn('surprise_react', frames)
                self.assertTrue(SLOTS - {'flustered'} <= set(frames))
                if entry['status'] == 'approved_runtime':self.assertEqual(set(frames), SLOTS)
                for slot, frame in frames.items():
                    path = ROOT / 'game' / frame['file']
                    self.assertTrue(path.is_file(), (who, height, slot))
                    if slot == 'flustered':self.assertEqual(path.name, who + '-flustered.webp')
                    else:self.assertEqual(path.name, slot + '.webp')

    def test_reviewed_talk_beat_keeps_front_gaze_and_the_authored_surprise(self):
        plan=dict(person='actor',talk='surprise_talk',react='surprise_react',settled=False,duration=.35)
        self.env['store'].r13_dialogue_beat=plan
        self.env['r13_dialogue_beat_ready']=lambda person:person=='actor'
        self.env['R13DialogueBeat']=lambda actual,profile:(actual,profile)
        actual,profile=self.env['r13_dialogue_beat_art']('actor',840)
        self.assertIs(profile,self.front['840'])
        self.assertEqual(actual['talk'],'surprise_talk')
        self.assertIsNone(actual['react'])
        self.assertTrue(actual['settled'])
        self.assertEqual(plan['react'],'surprise_react')
        self.assertFalse(plan['settled'])
        self.assertIsNone(self.env['r13_dialogue_beat_art']('other',840))

    def test_question_portrait_uses_complete_front_set_and_rejects_incomplete_set(self):
        text=(ROOT/'game/room13_fullbody_dialogue.rpy').read_text().split('init 58 python:',1)[1]
        tree=ast.parse(textwrap.dedent(text))
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_question_portrait_height')
        exec(compile(ast.Module(body=[function],type_ignores=[]),'질문 전신 크기','exec'),self.env)
        pick=self.env['r13_question_portrait_height']
        self.assertEqual(pick('actor'),560)
        self.assertEqual(pick('other'),840)
        self.env['R13_DIALOGUE_POSE_SOURCE']['people']['actor']=dict(pose_profiles=dict(chair_listen=dict(profiles=profiles('work'))))
        self.assertEqual(pick('actor','chair_listen'),840)
        self.env['store'].r13_thought_active=True
        self.assertEqual(pick('actor'),840)
        self.env['store'].r13_thought_active=False
        del self.front['760']['frames']['flustered']
        self.env['_r13_player_facing_ready'].clear()
        self.assertEqual(pick('actor'),840)

    def test_panseol_named_tired_frame_keeps_its_expression(self):
        extra=json.loads((ROOT/'game/assets/room13-dialogue-talk-art-extra.json').read_text())['people']['npc_panseol']
        self.env['R13_DIALOGUE_TALK_ART']['people']['npc_panseol']=extra
        source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_dialogue_source_neutral')
        self.env.update(r13_fullbody_emotion=lambda p:'neutral',Fixed=lambda art,**kwargs:art,
                        Transform=lambda file,**kwargs:dict(file=file,**kwargs))
        exec(compile(ast.Module(body=[function],type_ignores=[]),'이름 있는 피곤 표정','exec'),self.env)
        profile=self.env['r13_dialogue_source_profile']('npc_panseol','tired',840)
        self.assertIn('tired',profile['frames'])
        art=self.env['r13_dialogue_source_neutral']('npc_panseol','tired',840)
        self.assertEqual(art['file'],profile['frames']['tired']['file'])
        self.assertNotEqual(art['file'],profile['frames']['neutral']['file'])
        self.env['store'].r13_thought_active=True
        self.assertIsNone(self.env['r13_dialogue_source_profile']('npc_panseol','tired',840))

    def test_panseol_tired_is_authored_only_when_its_existing_art_is_available(self):
        source=(ROOT/'game/room13_fullbody_dialogue.rpy').read_text().split('init 58 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_fullbody_authored_pose')
        self.env.update(R13_FULLBODY_DIALOGUE=True,R13_FULLBODY_FILES={'approved-tired'},
                        R13_FULLBODY=dict(people={'npc_panseol':dict(images=dict(tired=dict(file='approved-tired'))),
                                                 'other':dict(images=dict(tired=dict(file='approved-tired')))}))
        exec(compile(ast.Module(body=[function],type_ignores=[]),'판설 전용 표정 범위','exec'),self.env)
        pick=self.env['r13_fullbody_authored_pose']
        self.assertTrue(pick('npc_panseol','tired'))
        self.assertFalse(pick('other','tired'))
        self.assertFalse(pick('npc_panseol','neutral'))
        self.env['R13_FULLBODY_FILES'].clear()
        self.assertFalse(pick('npc_panseol','tired'))


    def test_guard_pixel_offsets_fit_all_exact_profiles(self):
        # Ren'Py는 float 위치를 상대 비율로 해석하므로 픽셀 좌표는 정수여야 한다.
        from PIL import Image
        guard=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())['people']['guard']
        for height,profile in guard['profiles'].items():
            for slot,frame in profile['frames'].items():
                with self.subTest(height=height,slot=slot):
                    self.assertTrue(all(type(n) is int for n in frame['offset']))
                    with Image.open(ROOT/'game'/frame['file']) as im:
                        box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
                    self.assertIsNotNone(box)
                    x0,y0,x1,y1=box;scale=frame['scale'];ox,oy=frame['offset']
                    self.assertAlmostEqual(ox+(x0+x1)*scale/2,profile['canvas'][0]/2,delta=1)
                    self.assertAlmostEqual(oy+y1*scale,profile['canvas'][1]-24,delta=1)
                    self.assertGreaterEqual(ox+x0*scale,0)
                    self.assertGreaterEqual(oy+y0*scale,0)
                    self.assertLessEqual(ox+x1*scale,profile['canvas'][0])


if __name__ == '__main__':
    unittest.main()
