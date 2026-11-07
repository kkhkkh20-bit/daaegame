"""판설·아랫길 노인의 기존 원본 연결과 미확인 단역의 보존 경계를 검사한다."""
import ast
import json
from pathlib import Path
import textwrap
import types
import unittest

from PIL import Image

from build_closeup_smooth import APPROVED_EXTRA_MASTERS, build_table

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'


class ExtraDialogueSources(unittest.TestCase):
    def setUp(self):
        self.extra=json.loads((GAME/'assets/room13-dialogue-talk-art-extra.json').read_text())
        self.table=json.loads((GAME/'assets/room13-closeup-smooth.json').read_text())
        text=(GAME/'systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:',1)[1]
        tree=ast.parse(textwrap.dedent(text))
        names={'r13_closeup_smooth_profiles','r13_dialogue_fit_profile'}
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
        self.env=dict(R13_CLOSEUP_SMOOTH_TABLE=self.table,_r13_closeup_smooth_cache={},
                      renpy=types.SimpleNamespace(loadable=lambda path:(GAME/path).is_file()))
        exec(compile(ast.Module(body=funcs,type_ignores=[]),'기존 원본 변환','exec'),self.env)

    def test_source_mapping_is_reproducible(self):
        self.assertEqual(build_table(),self.table)

    def test_all_existing_emotions_resolve_to_the_same_approved_original(self):
        for who,masters in APPROVED_EXTRA_MASTERS.items():
            entry=self.extra['people'][who]
            converted_profiles=self.env['r13_closeup_smooth_profiles'](who,entry['profiles'])
            for height,profile in entry['profiles'].items():
                converted=converted_profiles[height]
                self.assertTrue(converted['smooth'])
                self.assertEqual(converted['canvas'],profile['canvas'])
                self.assertEqual(set(converted['frames']),set(profile['frames']))
                for slot,old in profile['frames'].items():
                    master=masters[Path(old['file']).stem]
                    self.assertEqual(converted['frames'][slot]['file'],master)
                    self.assertTrue(old['file'].startswith('assets/dialogue-dot-v2/'+who+'/'))
                    self.assertFalse(converted['frames'][slot]['nearest'])
                    with Image.open(GAME/master) as image:self.assertEqual(image.size,(1024,1536))

    def test_source_conversion_preserves_foot_anchor_and_silhouette_within_one_dot(self):
        for who in APPROVED_EXTRA_MASTERS:
            converted_profiles=self.env['r13_closeup_smooth_profiles'](who,self.extra['people'][who]['profiles'])
            for height,profile in self.extra['people'][who]['profiles'].items():
                converted=converted_profiles[height]
                for slot,old in profile['frames'].items():
                    new=converted['frames'][slot]
                    for axis in (0,1):
                        self.assertAlmostEqual(old['offset'][axis]+old['anchor'][axis],
                                               new['offset'][axis]+new['anchor'][axis]*new['scale'])
                    with Image.open(GAME/old['file']) as image:
                        before=image.convert('RGBA').getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                    with Image.open(GAME/new['file']) as image:
                        after=image.convert('RGBA').getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
                    for a,b in zip(before,after):
                        self.assertLessEqual(abs(a-b*new['scale']),profile['dot_scale']+1,(who,height,slot))
            large=self.env['r13_dialogue_fit_profile'](converted_profiles,1302)
            for frame in large['frames'].values():self.assertLess(frame['scale'],1)

    def test_unverified_minor_art_keeps_its_existing_roles_and_six_emotions(self):
        note=self.extra['source_resolution_notes']['unverified_high_resolution_sources']
        self.assertEqual(set(note['art_ids']),{'v111_patrol','v111_resident','v111_child'})
        self.assertEqual(len(note['people']),8)
        slots={'neutral','joy','angry','anxious','flustered','surprise_talk','surprise_react'}
        for who in note['people']:
            for profile in self.extra['people'][who]['profiles'].values():
                self.assertEqual(set(profile['frames']),slots)
                for frame in profile['frames'].values():
                    self.assertNotIn(frame['file'],self.table)
                    self.assertTrue((GAME/frame['file']).is_file())
                self.assertEqual(profile['frames']['surprise_react']['file'],profile['frames']['surprise_talk']['file'])


if __name__=='__main__':unittest.main()
