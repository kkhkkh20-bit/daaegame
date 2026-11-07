"""실제 승인69명·문맥10종을 source 선택부터 질문 발 정렬까지 함께 검증한다."""
import ast
import copy
import json
from pathlib import Path
import textwrap
import types
import unittest

from build_dialogue_size_fit import OUT, alpha_bounds, build, visible

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'


def data(name):
    return json.loads((GAME / 'assets' / name).read_text())


def nodes(path, names):
    source = (GAME / path).read_text().split(' python:', 1)[1]
    return [n for n in ast.parse(textwrap.dedent(source)).body if isinstance(n, ast.FunctionDef) and n.name in names]


def execute(env, path, names):
    exec(compile(ast.Module(body=nodes(path, names), type_ignores=[]), path, 'exec'), env)


class DialogueSizeFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = json.loads(OUT.read_text())

    def environment(self):
        talk = data('room13-dialogue-talk-art.json')
        talk['people'].update(data('room13-dialogue-talk-art-extra.json')['people'])
        plain = {'neutral', 'joy', 'angry', 'anxious', 'flustered', 'surprise', 'surprise_talk',
                 'thinking', 'distressed', 'expressive', 'panic', 'breakdown'}
        env = dict(store=types.SimpleNamespace(r13_meeting_active=False, r13_meeting_focus=None,
                       r13_thought_active=False, r13_dialogue_beat=None),
            renpy=types.SimpleNamespace(loadable=lambda p: (GAME / p).is_file()),
            R13_DIALOGUE_SIZE_FIT=self.table, _r13_dialogue_size_cache={},
            R13_DIALOGUE_TALK_ART=talk, R13_DIALOGUE_PLAYER_FACING=data('room13-dialogue-player-facing.json'),
            R13_DIALOGUE_POSE_SOURCE=data('room13-dialogue-pose-source-art.json'),
            R13_DIALOGUE_CONTEXT_ART=data('room13-dialogue-context-art.json'),
            R13_CLOSEUP_SMOOTH=True, R13_CLOSEUP_SMOOTH_TABLE=data('room13-closeup-smooth.json'),
            _r13_closeup_smooth_cache={}, _r13_player_facing_ready={},
            R13_DIALOGUE_B_ART_ON=False, R13_MEETING_SOLO=True, R13_FULLBODY_PLAIN=plain,
            r13_fullbody_key=lambda p: p.removeprefix('interview_'),
            R13DialogueBeat=lambda plan, profile: (plan, profile),
            _r13_context_beat_art=lambda *a: None,
            r13_close_y=lambda *a: 122, R13_QUESTION_FEET_LINE=704)
        execute(env, 'systems/room13_dialogue_beats.rpy', {
            'r13_dialogue_size_profiles', 'r13_closeup_smooth_profiles', 'r13_dialogue_fit_profile',
            'r13_dialogue_pose_source', 'r13_dialogue_player_profiles', 'r13_dialogue_render_profiles',
            'r13_dialogue_source_profile'})
        execute(env, 'room13_fullbody_dialogue.rpy', {
            'r13_question_portrait_height', 'r13_question_close_y', 'r13_dot_feet'})
        execute(env, 'systems/room13_dialogue_context_art.rpy', {'r13_dialogue_beat_art'})
        return env

    def test_generated_table_matches_sources_and_preserves_normal_840(self):
        self.assertEqual(build(), self.table)
        self.assertEqual(len(self.table['people']), 69)
        self.assertEqual(len(self.table['contexts']), 10)
        for who in ('daram', 'karo', 'resident_bori'):
            row = self.table['people'][who]
            self.assertTrue(row['preserved_840'])
            raw = data('room13-dialogue-player-facing.json')['people'][who]['profiles']['840']
            self.assertEqual(row['profiles']['840']['canvas'], raw['canvas'])
            self.assertEqual(row['profiles']['840']['frames'], raw['frames'])

    def test_all_runtime_sources_use_final_smooth_geometry_and_proportional_760(self):
        env = self.environment(); get = env['r13_dialogue_source_profile']
        for who, row in self.table['people'].items():
            with self.subTest(person=who):
                p = get(who, 'neutral', 840)
                self.assertIs(p, row['profiles']['840'])
                target = row['target_height_840']
                neutral = visible(p['frames']['neutral'])
                self.assertAlmostEqual(neutral, target, delta=target * .020001)
                p760 = get(who, 'neutral', 760); p1302 = get(who, 'neutral', 1302)
                for slot, frame in p['frames'].items():
                    self.assertAlmostEqual(visible(p760['frames'][slot]), visible(frame) * 760 / 840, places=5)
                    self.assertEqual(p1302['frames'][slot]['file'], frame['file'])
                    self.assertAlmostEqual(p1302['frames'][slot].get('scale', 1), frame.get('scale', 1) * 1.55)
                # rawdot를 먼저 원본으로 바꾼 뒤 크기를 맞추므로 표의 파일과 실제 파일이 같다.
                self.assertEqual({f['file'] for f in p['frames'].values()},
                    {f[0] for f in row['input_profiles']['840']['frames'].values()})

    def test_all_questions_fit_708_and_keep_stature_and_common_child_aliases(self):
        env = self.environment()
        for who, row in self.table['people'].items():
            with self.subTest(person=who):
                self.assertEqual(env['r13_question_portrait_height'](who), 560)
                p = env['r13_dialogue_source_profile'](who, 'neutral', 560)
                top = env['r13_question_close_y'](who, 560)
                for f in p['frames'].values():
                    b = alpha_bounds(f['file']); scale = f.get('scale', 1)
                    self.assertGreater(top + f['offset'][1] + b[1] * scale, 0)
                    self.assertLessEqual(top + f['offset'][1] + b[3] * scale, 708.000001)
                self.assertAlmostEqual(visible(p['frames']['neutral']), row['question_visible_height'])
        for who in ('v111_child', 'v111_siluk_child', 'kid_nubi3'):
            row = self.table['people'][who]
            self.assertTrue(row['child'])
            self.assertAlmostEqual(row['question_visible_height'], 560 * 2 / 3)
        self.assertAlmostEqual(self.table['people']['kid_dodam']['question_visible_height'], 560 * 2 / 3 * 132 / 165)
        self.assertAlmostEqual(self.table['people']['karo']['question_visible_height'], 560 * 230 / 210)

    def test_ten_contexts_keep_slot_and_general_size_even_when_retained_in_question(self):
        env = self.environment(); get = env['r13_dialogue_source_profile']
        raw = env['R13_DIALOGUE_CONTEXT_ART']['entries']
        for key, row in self.table['contexts'].items():
            who = row['person']; slot = raw[key]['slot']
            plan = dict(person=who, talk=slot, react=None, settled=True, context_key=key)
            env['store'].r13_dialogue_beat = plan
            for h in (560, 760, 840, 1302):
                chosen, p = env['r13_dialogue_beat_art'](who, h)
                self.assertIs(chosen, plan)
                self.assertEqual(p['frames'][slot]['file'], raw[key]['profiles']['840' if h == 1302 else str(h)]['frames'][slot]['file'])
                self.assertAlmostEqual(visible(p['frames'][slot]), visible(get(who, 'neutral', h)['frames']['neutral']), places=5)
            # 실제 close_art는 이 문맥을 유지하지만 질문 helper는 일반프로필을 읽는다.
            self.assertEqual(env['r13_question_portrait_height'](who), 560)
            y = env['r13_question_close_y'](who, 560)
            p = env['r13_dialogue_beat_art'](who, 560)[1]
            for f in p['frames'].values():
                b = alpha_bounds(f['file'])
                self.assertLessEqual(y + f['offset'][1] + b[3] * f['scale'], 708.000001)
        # 일반560 재배치와 별개로 원래 다람8문맥의 발 기준도 계속 읽는다.
        for key, row in raw.items():
            if row['person'] != 'daram' or 'question_top' not in row['profiles']['560']:
                continue
            env['store'].r13_dialogue_beat = dict(person='daram', talk=row['slot'], context_key=key)
            y = env['r13_question_close_y']('daram', 560)
            self.assertEqual(y, row['profiles']['560']['question_top'])
            for f in row['profiles']['560']['frames'].values():
                self.assertLessEqual(y + f['offset'][1] + alpha_bounds(f['file'])[3] * f.get('scale', 1), 708)

    def test_authored_poses_and_thought_and_multi_person_meeting_are_unchanged(self):
        env = self.environment(); get = env['r13_dialogue_source_profile']
        posed = env['R13_DIALOGUE_POSE_SOURCE']['people']
        for who, entry in posed.items():
            for pose, e in (entry.get('pose_profiles') or {entry.get('poses', [''])[0]: entry}).items():
                self.assertIs(get(who, pose, 840), e['profiles']['840'])
                self.assertEqual(env['r13_question_portrait_height'](who, pose), 840)
        for pose in ('chair_listen', 'chair_read'):
            p = get('seryeon', pose, 840)
            y = env['r13_question_close_y']('seryeon', 840, 110, pose)
            for f in p['frames'].values():
                self.assertLessEqual(y + f['offset'][1] + alpha_bounds(f['file'])[3] * f.get('scale', 1), 708)
        env['store'].r13_thought_active = True
        self.assertIsNone(get('granny', 'neutral', 840))
        self.assertEqual(env['r13_question_portrait_height']('granny'), 840)
        env['store'].r13_thought_active = False
        env['store'].r13_meeting_active = True
        env['store'].r13_meeting_focus = 'other'
        p = get('granny', 'neutral', 840)
        self.assertNotIn('size_fit_revision', p)
        env['store'].r13_meeting_focus = 'granny'
        self.assertIs(get('granny', 'neutral', 840), self.table['people']['granny']['profiles']['840'])
        for who in ('guard', 'resident_kkwak'):
            env['store'].r13_meeting_focus = who
            self.assertIs(get(who, 'neutral', 840), self.table['people'][who]['profiles']['840'])
            env['store'].r13_meeting_focus = 'other'
            self.assertNotIn('size_fit_revision', get(who, 'neutral', 840))

    def test_cache_reuses_objects_and_rejects_changed_source_geometry(self):
        env = self.environment(); normalize = env['r13_dialogue_size_profiles']
        raw = env['R13_DIALOGUE_PLAYER_FACING']['people']['granny']['profiles']
        first = normalize('granny', raw)
        self.assertIs(first, normalize('granny', raw))
        changed = copy.deepcopy(raw)
        changed['840']['frames']['neutral']['offset'][0] += 1
        self.assertIs(normalize('granny', changed), changed)
        # 활성 다람8·비연결04/07 등 지정하지 않은 문맥은 그림·프로필을 건드리지 않는다.
        contexts = env['R13_DIALOGUE_CONTEXT_ART']['entries']
        for key, row in contexts.items():
            if key not in self.table['contexts']:
                self.assertIs(normalize(row['person'], row['profiles'], key), row['profiles'])

    def test_old_save_refresh_can_redraw_source_only_minor_and_keeps_world_and_authored_pose(self):
        env = self.environment(); events = []
        state = env['store']; state.r13_motion_person = 'v111_child'
        state.r13_current_pose = 'neutral'; state.dialogue_speaker = None; state.dialogue_expression = 'joy'
        state.r13_camera = 'stage'
        env.update(R13_FULLBODY_DIALOGUE=True, R13_FULLBODY_ART_CACHE={}, CAST={'v111_child': {}},
            r13_fullbody_spec=lambda *a: None, r13_say_actor_h=lambda: 1302,
            r13_speaker=lambda *args: events.append(args))
        env['renpy'].get_showing_tags = lambda: ['r13_visitor']
        env['renpy'].get_screen = lambda *a: None
        env['renpy'].hide = lambda *a: None
        execute(env, 'room13_fullbody_dialogue.rpy', {'r13_fullbody_refresh_after_load'})
        refresh = env['r13_fullbody_refresh_after_load']
        refresh()
        self.assertEqual(events, [('v111_child', 'joy', 'neutral')])
        state.r13_camera = 'world'; refresh()
        self.assertEqual(len(events), 1)
        state.r13_camera = 'stage'; state.r13_current_pose = 'explicit_work'
        refresh()
        self.assertEqual(len(events), 1)
        env['r13_fullbody_spec'] = lambda *a: {'file': 'existing_work_art'}
        refresh()
        self.assertEqual(events[-1], ('v111_child', 'joy', 'explicit_work'))

    def test_head_cache_tracks_the_actual_normalized_context_geometry(self):
        env = self.environment()
        env['R13_DIALOGUE_SIZE_FIT'] = copy.deepcopy(self.table)
        env['store'].r13_dialogue_beat = dict(person='bami', context_key='bami:small_relief',
                                              talk='small_relief', react=None)
        calls = []
        def surface(*args):
            calls.append(True)
            return types.SimpleNamespace(get_bounding_rect=lambda **kw:
                types.SimpleNamespace(top=50 * len(calls), height=700))
        env.update(_R13_SAY_DRAWN_TOP={}, r13_close_art=lambda *a: None)
        env['renpy'].render_to_surface = surface
        execute(env, 'systems/room13_say_actor.rpy', {'_r13_say_drawn_headtop'})
        get = env['_r13_say_drawn_headtop']
        self.assertEqual(get('bami', 'neutral', 1302), 50)
        self.assertEqual(get('bami', 'neutral', 1302), 50)
        row = env['R13_DIALOGUE_SIZE_FIT']['contexts']['bami:small_relief']['profiles']['840']
        row['frames']['small_relief']['scale'] *= .99
        self.assertEqual(get('bami', 'neutral', 1302), 100)


if __name__ == '__main__':
    unittest.main()
