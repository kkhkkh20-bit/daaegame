"""정면 대화 원본의 승인·감정 완비·화면 문맥과 원래 자세의 경계를 확인한다."""
import ast
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SLOTS = {'neutral', 'joy', 'angry', 'anxious', 'flustered', 'surprise_talk'}
PEOPLE = {'resident_piko', 'resident_bori', 'karo', 'doto', 'neoul', 'resident_siluk', 'resident_seori', 'seryeon'}


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
                  'r13_dialogue_render_profiles', 'r13_dialogue_source_profile'}
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
        self.assertEqual(set(data), PEOPLE)
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


if __name__ == '__main__':
    unittest.main()
