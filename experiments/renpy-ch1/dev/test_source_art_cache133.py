"""정적 승인 원화 재사용이 표정·크기·도구함 교체를 섞지 않는지 확인한다."""
import ast
import copy
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

SOURCE=Path(__file__).resolve().parents[1]/'game/systems/room13_dialogue_beats.rpy'


class StaticSourceCache(unittest.TestCase):
    def setUp(self):
        tree=ast.parse(textwrap.dedent(SOURCE.read_text().split('init 170 python:\n',1)[1]))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_dialogue_source_neutral')
        self.profile={'canvas':[640,840],'frames':{
            'neutral':{'file':'approved/neutral.webp','offset':[12,20],'scale':.5},
            'angry':{'file':'approved/angry.webp','offset':[12,20],'scale':.5},
        }}
        self.available={'approved/neutral.webp','approved/angry.webp'}
        self.revision=0
        self.made=[]
        def make(kind):
            def factory(*args,**kwargs):
                result=SimpleNamespace(kind=kind,args=args,kwargs=kwargs)
                self.made.append(result)
                return result
            return factory
        self.env=dict(
            r13_dialogue_source_profile=lambda *args:self.profile,
            r13_fullbody_key=lambda pose:pose,
            r13_fullbody_emotion=lambda pose:pose,
            r13_asset_revision=lambda:self.revision,
            R13_DIALOGUE_SOURCE_ART_CACHE={},
            R13_DIALOGUE_SOURCE_ART_CACHE_LIMIT=48,
            Fixed=make('fixed'),Transform=make('transform'),Text=make('text'),
            r13_pixel_scale=make('pixel'),
            renpy=SimpleNamespace(loadable=lambda name:name in self.available,log=lambda *args:None),
            r13_dialogue_pose_source=lambda *args:{},
            R13_DIALOGUE_TALK_ART={'people':{'test':{'profiles':{'840':self.profile}}}},
        )
        exec(compile(ast.Module(body=[node],type_ignores=[]),'정적 원화 캐시','exec'),self.env)
        self.draw=self.env['r13_dialogue_source_neutral']

    def test_identical_source_is_built_once_across_repeated_predictions(self):
        original=copy.deepcopy(self.profile)
        arts=[self.draw('test','neutral',840) for _ in range(100)]
        self.assertTrue(all(art is arts[0] for art in arts))
        self.assertEqual([n.kind for n in self.made],['transform','fixed'])
        self.assertEqual(self.profile,original)

    def test_expression_size_and_frame_geometry_get_separate_art(self):
        neutral=self.draw('test','neutral',840)
        self.assertIsNot(self.draw('test','angry',840),neutral)
        variants=[
            lambda:self.profile['frames']['neutral'].update(file='approved/other.webp'),
            lambda:self.profile['frames']['neutral'].update(offset=[13,20]),
            lambda:self.profile['frames']['neutral'].update(scale=.6),
            lambda:self.profile['frames']['neutral'].update(nearest=True),
            lambda:self.profile.update(canvas=[640,560]),
            lambda:self.profile.update(pixel_grid=2),
            lambda:self.profile['frames']['neutral'].update(native_detail=True),
        ]
        for change in variants:
            with self.subTest(change=variants.index(change)):
                self.profile=copy.deepcopy({'canvas':[640,840],'frames':{
                    'neutral':{'file':'approved/neutral.webp','offset':[12,20],'scale':.5}}})
                self.available.add('approved/other.webp')
                change()
                self.assertIsNot(self.draw('test','neutral',840),neutral)

    def test_asset_revision_invalidates_same_path_without_changing_frame(self):
        first=self.draw('test','neutral',840)
        self.revision+=1
        second=self.draw('test','neutral',840)
        self.assertIsNot(first,second)
        self.assertIs(self.draw('test','neutral',840),second)
        self.assertEqual(first.args[0].kwargs,second.args[0].kwargs)

    def test_native_detail_does_not_borrow_pixel_grid_result(self):
        self.profile['pixel_grid']=2
        pixel=self.draw('test','neutral',840)
        self.assertEqual(pixel.kind,'pixel')
        self.profile['frames']['neutral']['native_detail']=True
        native=self.draw('test','neutral',840)
        self.assertEqual(native.kind,'fixed')
        self.assertIsNot(pixel,native)

    def test_cache_has_fixed_upper_bound(self):
        self.env['R13_DIALOGUE_SOURCE_ART_CACHE_LIMIT']=4
        for i in range(30):
            self.profile['frames']['neutral']['offset']=[i,20]
            self.draw('test','neutral',840)
            self.assertLessEqual(len(self.env['R13_DIALOGUE_SOURCE_ART_CACHE']),4)

    def test_unavailable_preferred_source_cannot_use_earlier_cached_art(self):
        first=self.draw('test','neutral',840)
        self.available.clear()
        unavailable=self.draw('test','neutral',840)
        self.assertIsNot(unavailable,first)
        self.assertEqual(unavailable.args[0].kind,'text')
        self.available.add('approved/neutral.webp')
        self.assertIs(self.draw('test','neutral',840),first)

    def test_missing_source_profile_keeps_existing_none_contract(self):
        self.env['r13_dialogue_source_profile']=lambda *args:None
        self.assertIsNone(self.draw('test','neutral',840))
        self.assertFalse(self.made)
        self.assertFalse(self.env['R13_DIALOGUE_SOURCE_ART_CACHE'])


if __name__=='__main__':unittest.main()
