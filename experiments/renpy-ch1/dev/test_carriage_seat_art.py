"""마차 표정은 승인 원본으로 그리며 착석 크기·명시 표정·아빠 시점은 유지한다."""
import ast
from pathlib import Path
import textwrap
import types
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


class CarriageSeatArt(unittest.TestCase):
    def setUp(self):
        source = (ROOT / 'game/room13_carriage_direction.rpy').read_text()
        tree = ast.parse(textwrap.dedent(source.split('init 306 python:', 1)[1].split('\ndefault ', 1)[0]))
        self.shown = []
        self.base_calls = []
        self.tags = {'r13_carriage_background', 'r13_visitor'}
        self.state = types.SimpleNamespace(place='마차 안', r13_meeting_active=False,
                                           r13_motion_person='daram', r13_carriage_seat_shown='quiz')
        self.env = dict(store=self.state, Transform=lambda art=None, **kw: dict(art=art, **kw),
                        CAST={'daram': {'avatar_joy': {}, 'avatar_angry': {}, 'avatar_flustered': {}}},
                        renpy=types.SimpleNamespace(get_showing_tags=lambda: self.tags,
                                                    show=lambda *args, **kw: self.shown.append((args, kw))),
                        r13_viewpoint=lambda: 'dad',
                        r13_speaker=lambda *args: self.base_calls.append(args),
                        r13_line_performance=lambda *args: ('base', 'base'))
        exec(compile(tree, '마차 표정 렌더', 'exec'), self.env)

    def test_all_emotions_use_unchanged_approved_masters_and_legacy_files_remain(self):
        for seat in self.env['R13_CARRIAGE_SEATS']:
            art = self.env['r13_carriage_daram_seat_art'](seat)
            path = ROOT / 'game' / art['art']
            approved = ROOT / 'art/carriage-seat-dot-20261026/originals' / path.name
            self.assertEqual(path.read_bytes(), approved.read_bytes(), seat)
            with Image.open(path) as image:self.assertEqual(image.size, (720, 1100))
            with Image.open(ROOT / 'game/assets' / path.name) as legacy:
                self.assertEqual(legacy.size, (149, 227))

    def test_single_smooth_downscale_preserves_seat_height_and_body_placement(self):
        for seat in self.env['R13_CARRIAGE_SEATS']:
            art = self.env['r13_carriage_daram_seat_art'](seat)
            self.assertFalse(art['nearest'])
            self.assertLess(art['zoom'], 1)
            self.assertAlmostEqual(1100 * art['zoom'], 227 * 3)
            self.assertLess(abs(720 * art['zoom'] - 149 * 3), 2)
            with Image.open(ROOT / 'game' / art['art']) as high:
                high_box = high.convert('RGBA').getbbox()
            with Image.open(ROOT / 'game/assets' / Path(art['art']).name) as low:
                low_box = low.convert('RGBA').getbbox()
            for axis, (a, b) in enumerate(zip(high_box, low_box)):
                self.assertLess(abs(a * art['zoom'] - b * 3), 5, (seat, axis))

    def test_authored_seated_emotions_are_not_collapsed_to_generic_faces(self):
        pick = self.env['r13_carriage_seat']
        for seat in ('quiz', 'pout', 'angry', 'secret', 'neutral', 'joy', 'bravado', 'wistful'):
            self.assertEqual(pick('seat_' + seat), seat)
        packet = ('daram', '엄마한테는 비밀이야.', {'expression': 'flustered', 'pose': 'seat_secret'})
        self.assertEqual(self.env['r13_line_performance']('opening', 0, packet), ('flustered', 'seat_secret'))

    def test_a_new_seat_changes_only_daram_at_the_existing_position(self):
        self.env['r13_speaker']('daram', 'angry', 'seat_pout')
        self.assertEqual(self.state.r13_carriage_seat_shown, 'pout')
        self.assertEqual(len(self.shown), 1)
        _, shown = self.shown[0]
        self.assertTrue(shown['what']['art'].endswith('seat-pout.webp'))
        self.assertEqual(shown['tag'], 'r13_visitor')
        self.assertEqual(shown['at_list'][0], dict(art=None, xanchor=.5, xpos=540, yanchor=0, ypos=96))

    def test_dad_reply_preserves_darams_last_seat_without_drawing_dad(self):
        self.env['r13_speaker']('dad', 'neutral')
        self.assertEqual(self.state.r13_carriage_seat_shown, 'quiz')
        self.assertFalse(self.shown)
        self.assertEqual(self.base_calls, [('dad', 'neutral', None)])

    def test_restoring_an_empty_seat_uses_the_same_high_detail_face(self):
        self.tags.remove('r13_visitor')
        self.env['r13_speaker']('dad', 'neutral')
        self.assertEqual(len(self.shown), 1)
        self.assertTrue(self.shown[0][1]['what']['art'].endswith('seat-quiz.webp'))
        self.assertFalse(self.shown[0][1]['what']['nearest'])


if __name__ == '__main__':
    unittest.main()
