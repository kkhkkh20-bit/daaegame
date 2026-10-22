import textwrap
import unittest
from pathlib import Path

GAME = Path(__file__).resolve().parents[1] / 'game'


class NWMeetingFraming(unittest.TestCase):
    def setUp(self):
        base = (GAME / 'room13_meeting_camera.rpy').read_text()
        nw = (GAME / 'room13_v111_meeting_stage.rpy').read_text()
        self.env = {}
        for source, start, end in (
            (base, '    def r13_meeting_portrait_x', '    def r13_meeting_world_tiles'),
            (nw, '    def r13_nw_meeting_session', '    _r13_nw_meeting_orbit_height'),
            (nw, '    _r13_nw_meeting_portrait_x', '    _r13_nw_meeting_plate'),
        ):
            exec(textwrap.dedent(source[source.index(start):source.index(end)]), self.env)
        self.position = self.env['r13_meeting_portrait_x']

    def test_safe_faces_preserve_orbit_with_cropped_canvas(self):
        for x in (-80, 950):
            self.assertEqual(self.position('nw_room13', x, 400), x)

    def test_minimum_face_correction_at_both_edges(self):
        self.assertAlmostEqual(self.position('nw_room13', -200, 400), -86)
        self.assertEqual(self.position('nw_room13', 1100, 400), 966)
        for width in (240, 400, 600):
            left = self.position('nw_room13', -500, width)
            right = self.position('nw_room13', 1400, width)
            self.assertAlmostEqual(left + width * .275, 24)
            self.assertAlmostEqual(right + width * .725, 1256)

    def test_focus_untouched_even_during_pan(self):
        for x in (-200, 440, 1100):
            self.assertEqual(self.position('nw_room13', x, 400, True), x)

    def test_non_nw_unchanged(self):
        for session in ('round', 'field', 'stone', None):
            for x in (-200, 1100):
                self.assertEqual(self.position(session, x, 400), x)


if __name__ == '__main__':
    unittest.main()
