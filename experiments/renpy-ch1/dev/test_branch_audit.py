"""dev/branch_audit.py 시험: 작은 가짜 대본으로 각 검사가 잡는 것과 안 잡는 것을 본다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import branch_audit as ba  # noqa: E402

SPEAKERS = {'아빠': 'dad', '피코': 'resident_piko', '다람': 'daram', '너울': 'neoul', '나비': 'nabi'}


def rec(rid, speaker, text, kind='dialogue', ops=()):
    return {rid: dict(id=rid, kind=kind, speaker=speaker, text=text, player_visible=True, operations=list(ops))}


def make_game(story, records, patches=None, when=None, scene_actors=None, initial=None, reactions=None):
    src = 'R13_NW_WHEN={\n' + ''.join('    "%s":lambda:%s,\n' % kv for kv in (when or {}).items()) + '}\n'
    ws, wa = ba.parse_when(src)
    allrec = {}
    for r in records:
        allrec.update(r)
    return ba.Game(records=allrec, patches=patches or {}, initial=initial or {'day': 1, 'piko_alive': True},
                   speakers=dict(SPEAKERS), life={'resident_piko': 'piko_alive'}, lives=[('resident_piko', 'piko_alive')],
                   listable=['daram', 'nabi'], fates=['fate_piko'], fate_results={}, when_src=ws, when=wa,
                   scene_actors=scene_actors or {}, story={'t.rpy': story}, reactions=reactions or {})


FORK = """label r13_v111_start:
    $ r13_v111_set("day",2)
    menu:
        '들인다':
            $ r13_fork_set_fate('fate_piko','saved')
        '두고 간다':
            $ r13_fork_set_fate('fate_piko','lost')
            $ r13_v111_set('piko_alive',False)
    $ r13_v111_set("day",3)
"""


def run(game, check=None):
    res = ba.audit(game)
    return [f for f in res['findings'] if check is None or f['check'] == check], res


class SpeakerAfterDeath(unittest.TestCase):
    def test_dead_speaker_on_lost_path_is_certain(self):
        story = FORK + "    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')\n"
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', '피코', '그림 보여 줄게요.')]), 'D')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['grade'], '확실')
        self.assertIn('fate_piko=lost', found[0]['paths'])

    def test_guard_and_when_clear_the_line(self):
        story = FORK + """    if r13_v111_value('piko_alive'):
        call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0002']),'y')
"""
        patches = {3: dict(replace={}, before={}, after={'MS14_D03_S01_L0002': [
            dict(id='NW_T_01', speaker='피코', text='고마워요.', when='piko_alive')]}, drop=[], blocks={})}
        game = make_game(story, [rec('MS14_D03_S01_L0001', '피코', '그림 보여 줄게요.'),
                                 rec('MS14_D03_S01_L0002', None, '아침이다.', kind='narration')],
                         patches=patches, when={'piko_alive': 'r13_v111_value("piko_alive") is not False'})
        found, _ = run(game, 'D')
        self.assertEqual(found, [])

    def test_unpartitioned_death_is_suspect(self):
        # 갈림 결과를 적지 않고 죽음만 갈리면, 같은 경로 안에서 「죽었을 수 있음」(의심).
        story = """label r13_v111_start:
    $ r13_v111_set("day",3)
    menu:
        '가':
            $ r13_v111_set('piko_alive',False)
        '나':
            pass
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')
"""
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', '피코', '그림 보여 줄게요.')]), 'D')
        self.assertEqual([f['grade'] for f in found], ['의심'])

    def test_called_label_effects_reach_the_caller(self):
        story = """label r13_v111_start:
    $ r13_v111_set("day",3)
    call r13_v111_kill
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')
    return

label r13_v111_kill:
    $ r13_v111_set('piko_alive',False)
    return
"""
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', '피코', '그림 보여 줄게요.')]), 'D')
        self.assertEqual([f['grade'] for f in found], ['확실'])


class NameMention(unittest.TestCase):
    def story(self, text_day4):
        # 「죽은 날」은 그 사람이 죽은 상태로 처음 대사가 나오는 날이다(3일 아침 장면).
        return FORK + """    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'w')
    $ r13_v111_set("day",4)
    call r13_lines(r13_v111_lines(['MS14_D04_S01_L0001']),'x')
""", [rec('MS14_D03_S01_L0001', None, '아침이다.', kind='narration'), rec('MS14_D04_S01_L0001', '다람', text_day4)]

    def test_present_tense_mention_after_death(self):
        story, recs = self.story('피코 아저씨한테 물어보자.')
        found, _ = run(make_game(story, recs), 'D')
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]['mention'], '피코')
        self.assertEqual(found[0]['grade'], '의심')

    def test_past_tense_mention_is_fine(self):
        story, recs = self.story('피코 아저씨는 그 밤에 얼었어.')
        found, _ = run(make_game(story, recs), 'D')
        self.assertEqual(found, [])

    def test_same_day_as_death_is_not_checked(self):
        story = FORK + "    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')\n"
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', '다람', '피코 아저씨 손이 차가워.')]), 'D')
        self.assertEqual(found, [])


class SceneCast(unittest.TestCase):
    STORY = """label r13_v111_start:
    $ r13_v111_set("day",2)
    $ r13_v111_arrive(['daram'])
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0001']),'x')
    $ r13_v111_arrive(['nabi'])
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0002']),'y')
"""

    def test_speaker_missing_from_scene_and_stage(self):
        recs = [rec('MS14_D02_S01_L0001', '나비', '국 식어요.'), rec('MS14_D02_S01_L0002', '나비', '국 식어요, 정말.')]
        found, _ = run(make_game(self.STORY, recs, scene_actors={'MS14_D02_S01': {'dad', 'daram'}}), 'E')
        self.assertEqual([f['id'] for f in found], ['MS14_D02_S01_L0001'])

    def test_scene_without_cast_info_is_skipped(self):
        recs = [rec('MS14_D02_S01_L0001', '나비', '국 식어요.'), rec('MS14_D02_S01_L0002', '나비', '국 식어요, 정말.')]
        found, _ = run(make_game(self.STORY, recs), 'E')
        self.assertEqual(found, [])


class FateWords(unittest.TestCase):
    def test_word_of_one_result_on_the_other_path(self):
        story = FORK + "    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')\n"
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', None, '코가 빈 초상이 벽에 걸려 있다.', kind='narration')]), 'F')
        self.assertEqual(len(found), 1)
        self.assertIn('saved', found[0]['conflict'])

    def test_word_guarded_to_its_own_result(self):
        story = FORK + """    if r13_v111_value('piko_alive') is False:
        call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')
"""
        found, _ = run(make_game(story, [rec('MS14_D03_S01_L0001', None, '코가 빈 초상이 벽에 걸려 있다.', kind='narration')]), 'F')
        self.assertEqual(found, [])


class Repeats(unittest.TestCase):
    RECS = [rec('MS14_D02_S01_L0001', '나비', '국은 한 그릇씩만 드려요. 규칙이에요.'),
            rec('MS14_D02_S01_L0002', '나비', '국은 한 그릇씩만 드려요. 규칙이에요!')]

    def test_same_words_twice_in_one_run(self):
        story = """label r13_v111_start:
    $ r13_v111_set("day",2)
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0001']),'x')
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0002']),'y')
"""
        found, _ = run(make_game(story, self.RECS), 'G')
        self.assertEqual(len(found), 1)

    def test_exclusive_branches_are_not_repeats(self):
        story = """label r13_v111_start:
    $ r13_v111_set("day",2)
    menu:
        '가':
            call r13_lines(r13_v111_lines(['MS14_D02_S01_L0001']),'x')
        '나':
            call r13_lines(r13_v111_lines(['MS14_D02_S01_L0002']),'y')
"""
        found, _ = run(make_game(story, self.RECS), 'G')
        self.assertEqual(found, [])

    def test_alternative_labels_after_a_meeting_are_not_repeats(self):
        story = """label r13_v111_start:
    $ r13_v111_set("day",2)
    menu:
        '이긴다':
            jump r13_v111_won
        '진다':
            jump r13_v111_lost

label r13_v111_won:
    $ r13_nw_meeting_end('soup','win')
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0001']),'x')
    jump r13_v111_after

label r13_v111_lost:
    $ r13_nw_meeting_end('soup','lose')
    call r13_lines(r13_v111_lines(['MS14_D02_S01_L0002']),'y')
    jump r13_v111_after

label r13_v111_after:
    return
"""
        found, _ = run(make_game(story, self.RECS), 'G')
        self.assertEqual(found, [])


class Conditions(unittest.TestCase):
    def test_unreadable_condition_is_listed_not_guessed(self):
        story = """label r13_v111_start:
    $ r13_v111_set("day",3)
    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')
"""
        patches = {3: dict(replace={}, after={}, drop=[], blocks={}, before={'MS14_D03_S01_L0001': [
            dict(id='NW_T_02', speaker='피코', text='손이 떨려요.', when='odd')]})}
        game = make_game(story, [rec('MS14_D03_S01_L0001', None, '아침이다.', kind='narration')], patches=patches,
                         when={'odd': 'bool(getattr(store,"x",None))'})
        _, res = run(game)
        self.assertIn('odd', res['unknown_conds'])

    def test_replace_variants_take_the_first_match(self):
        story = FORK + "    call r13_lines(r13_v111_lines(['MS14_D03_S01_L0001']),'x')\n"
        patches = {3: dict(before={}, after={}, drop=[], blocks={}, replace={'MS14_D03_S01_L0001': [
            dict(text='피코가 웃는다.', when='piko_alive'), dict(text='빈 자리만 남았다.')]})}
        game = make_game(story, [rec('MS14_D03_S01_L0001', None, '원문.', kind='narration')], patches=patches,
                         when={'piko_alive': 'r13_v111_value("piko_alive") is not False'})
        an = ba.Analyzer(game).run()
        rows = {r.id: r for r in ba.collect_rows(game, an)}
        self.assertEqual(set(rows), {'MS14_D03_S01_L0001{piko_alive}', 'MS14_D03_S01_L0001'})
        st, _ = ba.row_state(game, an, rows['MS14_D03_S01_L0001'])
        self.assertEqual({k[0] for k in st}, {'lost'})

    def test_rule_function_with_unknown_input_gives_each_result(self):
        # 모르는 값에서 갈리는 판정 함수: 아는 값으로 정해지는 결과는 그대로, 나머지는 「알 수 없음」 조합으로.
        import ast
        src = """
    def r13_nw_pick():
        if r13_v111_value("gone"):return "left"
        if r13_v111_value("count")>=4:return "frozen"
        return "morning"
"""
        game = make_game("label r13_v111_start:\n    return\n", [])
        game.funcs = ba.parse_funcs(src, ('r13_nw_pick',))
        game.external_keys = {'count'}
        vals = ba.Values(game)
        node = ast.parse('r13_nw_pick()', mode='eval').body
        out = dict(vals.split_vs(node, {'gone': frozenset((None, True))}))
        self.assertEqual(set(out), {'left', 'frozen', 'morning'})
        self.assertEqual(out['left']['gone'], {True})
        self.assertEqual(out['morning']['gone'], {None})


if __name__ == '__main__':
    unittest.main()
