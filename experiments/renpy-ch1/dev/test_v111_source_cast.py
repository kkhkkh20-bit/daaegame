"""본문의 임시 역할도 현장 이름표에서 중단 없이 표시한다."""
import io
import json
from pathlib import Path
import re
import textwrap
import types
import unittest

GAME = Path(__file__).resolve().parents[1] / 'game'


class SourceCastLabels(unittest.TestCase):
    def test_legacy_role_nameplates_use_registered_display_names(self):
        env = dict(json=json, R13_NAMES={}, R13_CHARS={}, Character=lambda name: name,
                   renpy=types.SimpleNamespace(file=lambda name: io.BytesIO((GAME/name).read_bytes())))
        cast = (GAME/'room13_v111_source_cast.rpy').read_text().split('init 220 python:\n', 1)[1]
        exec(textwrap.dedent(cast), env)
        source = (GAME/'room13_interaction.rpy').read_text()
        function = re.search(r'^    def r13_actor_nameplate\(actor\):\n.*?(?=^    def )', source, re.M|re.S).group()
        env.update(r13_actor_face_target=lambda actor: None, r13_world_width=lambda: 1280)
        exec(textwrap.dedent(function), env)
        for role in ('종업원', '진료 담당자'):
            with self.subTest(role=role):
                person = env['MS14_SPEAKERS'][role]
                actor = dict(person=person, rect=(100,200,80,160))
                x,y = env['r13_actor_nameplate'](actor)
                self.assertEqual(env['R13_NAMES'][person], role)
                self.assertTrue(0 <= x <= 1280 and y >= 101)


if __name__ == '__main__':
    unittest.main()
