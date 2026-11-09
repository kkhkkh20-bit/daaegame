"""서류 검색의 새 진입은 퀴즈·획득 효과 없이 기존 원본 조사로 돌아간다."""
import ast
import copy
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/room13_v111_gate_shelf.rpy'


class GateShelf138(unittest.TestCase):
    def test_legacy_weekday_names_still_follow_the_saved_day_without_changing_it(self):
        state=SimpleNamespace(room13=dict(day=1,evidence=['V111:E02'],v111=dict(values={})))
        env=dict(store=state,r13_weekday=lambda day:('목','금','토','일','월','화','수')[day%7])
        source=SOURCE.read_text().split('init 360 python:',1)[1].split('\nlabel ',1)[0]
        exec(compile(ast.parse(textwrap.dedent(source)),str(SOURCE),'exec'),env)
        before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_gate_shelf_days'](),['목요일','금요일','토요일'])
        self.assertEqual(state.room13,before)
        state.room13['day']=2
        self.assertEqual(env['r13_gate_shelf_days'](),['금요일','토요일','일요일'])

    def test_new_entry_returns_to_the_existing_single_acquisition_and_keeps_legacy_choice(self):
        source=SOURCE.read_text()
        fresh=source.split('label r13_v111_gate_shelf_pick:',1)[1].split('\nlabel ',1)[0]
        self.assertNotIn('display_menu',fresh)
        self.assertIn('\n    return',fresh)
        for effect in ('r13_grant(','r13_v111_commit(','r13_v111_set(','r13_v111_time('):
            self.assertNotIn(effect,fresh)
        legacy=source.split('label r13_v111_gate_shelf_menu:',1)[1]
        self.assertIn('renpy.display_menu',legacy)
        self.assertIn('jump r13_v111_gate_shelf_menu',legacy)
        self.assertIn('if r13_gate_shelf_pick=="today":',legacy)
        for effect in ('r13_grant(','r13_v111_commit(','r13_v111_set('):
            self.assertNotIn(effect,legacy)


if __name__=='__main__':unittest.main()
