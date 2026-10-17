"""Regression coverage for explicit narration actors and retired dialogue beats."""
import ast
import json
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace
from test_dialogue_beats import functions

ROOT = Path(__file__).resolve().parents[1]


class NarrationActor(unittest.TestCase):
    def setUp(self):
        self.env = functions()
        self.people = json.loads((ROOT / 'game/assets/room13-dialogue-talk-art.json').read_text())['people']

    def plan(self, meta, speaker=None):
        return self.env['r13_dialogue_narration_plan']((speaker, '아빠가 빵 사 왔어요! 진짜 빵이에요!', meta), self.people)

    def test_explicit_child_joy_and_anxious_use_requested_approved_slot(self):
        for emotion in ('joy', 'anxious'):
            plan = self.plan({'show': 'kid_siluk2', 'expression': emotion})
            self.assertEqual((plan['person'], plan['talk']), ('kid_siluk2', emotion))
            self.assertTrue(plan['settled'])

    def test_authored_pose_and_ordinary_speech_are_not_overridden(self):
        for meta, speaker in [({'show':'kid_kkomi','expression':'surprise','pose':'door_peek'}, None),
                              ({'show':'kid_siluk2'}, None),
                              ({'show':'kid_siluk2','expression':'joy'}, 'daram'),
                              ({'show':'not_registered','expression':'joy'}, None)]:
            self.assertIsNone(self.plan(meta, speaker))

    def test_narration_surprise_stays_front_and_unapproved_art_is_rejected(self):
        self.assertEqual(self.plan({'show':'kid_siluk2','expression':'surprise'})['talk'], 'surprise_talk')
        self.people['kid_siluk2']['gaze'] = 'side'
        self.assertIsNone(self.plan({'show':'kid_siluk2','expression':'joy'}))

    def test_line_resolves_beat_before_show_and_does_not_clear_it_afterward(self):
        source = (ROOT / 'game/room13.rpy').read_text().split('label r13_lines(',1)[1].split('\n    return',1)[0]
        begin = source.index('$ r13_dialogue_beat_begin(')
        show = source.index('$ r13_speaker(r13_packet[2]["show"]')
        speaker = source.index('$ r13_speaker(r13_packet[0]')
        self.assertLess(begin, show)
        self.assertLess(show, speaker)
        self.assertEqual(source.count('$ r13_dialogue_beat_begin('), 1)


class PortraitRefresh(unittest.TestCase):
    def setUp(self):
        source = (ROOT / 'game/room13_rules.rpy').read_text()
        body = source.split('    def r13_speaker(',1)[1].split('\n    def ',1)[0]
        node = ast.parse('def r13_speaker(' + textwrap.dedent(body))
        self.store = SimpleNamespace(room13={}, r13_current_pose='neutral', place='학교',
                                     r13_motion_person='daram', r13_camera='stage', r13_dialogue_beat=None)
        self.shown = []
        self.reactions = []
        self.entrances = []
        def close_art(who, pose, height, full, entrance):
            self.entrances.append(entrance)
            return self.store.r13_dialogue_beat['talk'] if self.store.r13_dialogue_beat else 'neutral'
        env = dict(store=self.store, CAST={'daram':{'avatar_neutral':True}, 'dad':{}},
                   renpy=SimpleNamespace(get_showing_tags=lambda:['r13_visitor'], show=lambda *a,**kw:self.shown.append(kw), hide=lambda *a:None),
                   r13_conversation_pose=lambda who,pose:pose, r13_acting_spec=lambda *a:True,
                   r13_fullbody_authored_pose=lambda *a:False, R13_FULLBODY_NEW=set(),
                   r13_fullbody_key=lambda pose:pose, R13_FULLBODY_PLAIN={'neutral','joy','angry','anxious','surprise'},
                   r13_dialogue_source_profile=lambda *a:{},
                   r13_dialogue_beat_ready=lambda who:bool(self.store.r13_dialogue_beat),
                   r13_react_kind=lambda *a:self.reactions.append(a), r13_close_art=close_art,
                   r13_portrait_close=lambda *a:None,r13_close_y=lambda *a,**kw:0,r13_close_x=lambda *a:0,
                   r13_react=lambda react,who,pose,what,at:(what,at))
        exec(compile(node, 'speaker', 'exec'), env)
        self.speaker = env['r13_speaker']

    def test_same_pose_unbound_line_replaces_joy_without_entrance_or_reaction(self):
        self.store.r13_dialogue_beat = {'talk':'joy'}
        self.speaker('daram')
        self.store.r13_dialogue_beat = None
        self.speaker('daram')
        self.assertEqual([s['what'] for s in self.shown], ['joy','neutral'])
        self.assertEqual(self.entrances, [False,False])
        self.assertEqual(self.reactions, [])

    def test_pov_and_narration_retain_partner_after_beat_is_cleared(self):
        self.store.r13_dialogue_beat = {'talk':'joy'}
        self.speaker('daram')
        self.store.r13_dialogue_beat = None
        self.speaker('dad')
        self.speaker(None)
        self.assertEqual([s['what'] for s in self.shown], ['joy'])

    def test_unchanged_authored_pose_is_not_rebuilt(self):
        self.store.r13_current_pose = 'door_peek'
        self.speaker('daram', pose='door_peek')
        self.assertEqual(self.shown, [])

if __name__ == '__main__':
    unittest.main()
