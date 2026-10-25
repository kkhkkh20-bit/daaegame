"""Read-only fork visibility and persistent observation contracts without Ren'Py."""
import ast
import copy
import textwrap
import unittest
from types import SimpleNamespace
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ForkScreen(unittest.TestCase):
    def setUp(self):
        self.values={}
        self.store=SimpleNamespace(room13={'v111':{},'day':1},r13_meeting_active=False)
        self.persistent=SimpleNamespace(r13_fork_runs=0,r13_fork_seen={},r13_fork_endings={})
        self.saves=[]
        def capture(size):
            self.assertEqual(size,(320,180))
            return b'png'
        self.env=dict(store=self.store,persistent=self.persistent,
            renpy=SimpleNamespace(screenshot_to_bytes=capture,save_persistent=lambda:self.saves.append(True)),
            r13_v111_value=lambda key:self.values.get(key))
        source=(ROOT/'game/room13_fork_screen.rpy').read_text().split('init 322 python:\n')[1].split('\nscreen ')[0]
        exec(textwrap.dedent(source),self.env)
    def call(self,name,*args):
        return self.env['r13_fork_'+name](*args)
    def test_future_is_one_opaque_column_even_with_later_discoveries(self):
        self.persistent.r13_fork_seen[('altar','win')]={'png':b'png'}
        columns=self.call('columns')
        self.assertEqual(len(columns),2)
        self.assertEqual(columns[-1],dict(key=None,day='그 너머',rows=[]))
        self.assertEqual(len(columns[0]['rows']),1)
    def test_missed_results_are_one_lock_with_a_count_only(self):
        # 0.20.x (plan5 m4): unseen results show only "다른 결과 N", never a title or a result.
        self.values['meeting:gate']='win'
        rows=self.call('columns')[0]['rows']
        self.assertEqual([r['kind'] for r in rows],['current','locked'])
        # 0.20.5 (Codex S01): the gate has only win and lose, so one other result is left.
        self.assertEqual(rows[1]['count'],1)
        self.assertIsNone(rows[1]['title'])
        self.assertIsNone(rows[1]['result'])
        self.assertIsNone(rows[1]['record'])
        self.persistent.r13_fork_seen[('gate','lose')]={'png':b'png','run':1}
        self.assertEqual([r['kind'] for r in self.call('columns')[0]['rows']],['current','old'])
        # A meeting with three real results still counts two.
        self.values.update({'meeting:lamp':'win','meeting:gate_post':'win'})
        lamp=[c for c in self.call('columns') if c['key']=='lamp'][0]['rows']
        self.assertEqual([r['kind'] for r in lamp],['current','locked']);self.assertEqual(lamp[1]['count'],2)
        self.persistent.r13_fork_seen[('lamp','lose')]={'png':b'png','run':1}
        lamp=[c for c in self.call('columns') if c['key']=='lamp'][0]['rows']
        self.assertEqual([r['kind'] for r in lamp],['current','old','locked']);self.assertEqual(lamp[2]['count'],1)
    def test_outcomes_match_the_meeting_end_calls(self):
        import re
        found={}
        for path in sorted((ROOT/'game').glob('room13_v111_days*.rpy')):
            for meeting,rest in re.findall(r'r13_nw_meeting_end\(\s*["\'](\w+)["\']\s*,(.*)',path.read_text()):
                found.setdefault(meeting,set()).update(re.findall(r'["\'](win|partial|lose)["\']',rest.split('\n')[0]))
        for key,*_ in self.env['R13_FORK_MEETINGS']:
            expected=found.get(key)
            if key in self.env['R13_FORK_GRAND_MEETINGS']:
                # Grand remains an authored flag layered on a real win, not a new verdict.
                self.assertTrue(any(re.search(r'r13_v111_set\(["\']grand:'+key+r'["\'],\s*True\)',p.read_text()) for p in (ROOT/'game').glob('room13_v111_*.rpy')))
                expected=expected|{'grand'}
            self.assertEqual(set(self.call('outcomes',key)),expected,key)
    def test_row_tops_fit_above_the_footer(self):
        tops=self.call('row_tops',[{'kind':'current'},{'kind':'old'},{'kind':'old'}])
        self.assertEqual(tops,[200,332,464])
        self.assertLessEqual(tops[-1]+116,684-80-14)   # above the touch footer rule
        self.assertIn('$ by = 684-ch',(ROOT/'game/room13_fork_screen.rpy').read_text())
        self.assertEqual(self.call('row_tops',[{'kind':'current'},{'kind':'locked'}]),[200,332])
    def test_fate_badge_only_on_decided_fate_meetings_and_names_no_one(self):
        self.assertFalse(self.call('fate','lamp'))           # not decided yet
        self.values['meeting:lamp']='win'
        self.assertTrue(self.call('fate','lamp'))            # the badge does not depend on the result
        self.values['meeting:gate']='lose'
        self.assertFalse(self.call('fate','gate'))
        self.values.update({'meeting:gate':'win','meeting:lamp':'lose'})
        columns=self.call('columns')
        self.assertEqual([c['key'] for c in columns if c.get('fate')],['lamp'])
        self.assertEqual(self.env['R13_FORK_FATE_LINE'],'여기서 누군가의 운명이 갈렸다.')
        # The current meeting (still ahead) never carries the badge.
        self.store.r13_meeting_active=True;self.store.r13_meeting_claim='NW:fire'
        self.values['meeting:gate_post']='win'
        here=[c for c in self.call('columns') if c.get('here')]
        self.assertEqual(here[0]['key'],'fire');self.assertFalse(here[0]['fate'])
    def test_fate_screen_text_never_names_or_reveals(self):
        screen=(ROOT/'game/room13_fork_screen.rpy').read_text().split('screen r13_fork_screen():',1)[1].split('\ninit ',1)[0]
        self.assertIn('R13_FORK_FATE_LINE',screen)
        for leak in ('listed:','departed:','_alive','R13_NAMES','r13_display_name','r13_nw_listed','r13_nw_dead'):
            self.assertNotIn(leak,screen)
    def test_fate_set_matches_meeting_result_effects(self):
        """Re-derive R13_FORK_FATE: a meeting's result label writes a list name, a departure,
        custody or a death (room13_v111_days*.rpy, rules in room13_v111_newworld_rules.rpy)."""
        import re
        effect=re.compile(r'r13_nw_list\(|departed:|DARAM_DETAINED|_custody["\']\s*,\s*["\']detained|(_alive|ALIVE)["\']\s*,\s*False')
        fate=set()
        for path in sorted((ROOT/'game').glob('room13_v111_days*.rpy')):
            for block in re.split(r'\n(?=label )',path.read_text()):
                for meeting in re.findall(r'r13_nw_meeting_end\(\s*["\'](\w+)["\']',block):
                    if effect.search(block):fate.add(meeting)
        # 제단은 결과 라벨 뒤 저녁의 불타는 밤에서 운명이 갈린다.
        fate.add('altar')
        self.assertEqual(fate,set(self.env['R13_FORK_FATE']))
        self.assertTrue(set(self.env['R13_FORK_FATE'])<={m[0] for m in self.env['R13_FORK_MEETINGS']})
    def test_saved_path_changes_independently_of_persistent(self):
        self.call('record','gate','lose')
        self.values['meeting:gate']='win'
        rows=self.call('columns')[0]['rows']
        self.assertEqual(rows[0]['result'],'win')
        self.assertEqual(rows[1]['kind'],'old')
        self.values.clear()  # load an earlier save
        self.assertEqual(self.call('current'),0)
        self.assertEqual(len(self.call('columns')[0]['rows']),1)
        self.assertIn(('gate','lose'),self.persistent.r13_fork_seen)
    def test_current_row_never_shows_another_runs_picture(self):
        # 0.20.5 (Codex S02): run 1 saved, run 2 records the same result, run 1 is loaded again.
        self.call('start');saved=copy.deepcopy(self.store.room13)
        self.call('start');self.call('record','gate','win')
        self.store.room13=saved;self.values['meeting:gate']='win'
        rows=self.call('columns')[0]['rows']
        self.assertEqual(rows[0]['kind'],'current');self.assertIsNone(rows[0]['record'])
        self.store.room13['v111']['fork_run']=2
        self.assertEqual(self.call('columns')[0]['rows'][0]['record']['run'],2)
    def test_active_stage_wins_and_initial_page_contains_it(self):
        self.store.r13_meeting_active=True
        self.store.r13_meeting_claim='NW:soup'
        self.assertEqual(self.call('current'),12)   # 0.20.20: 판정 시점 칸이 회의 사이에 들어갔다
        self.assertLessEqual(self.call('initial_page'),12)
        self.assertGreater(self.call('initial_page')+6,12)
    def test_run_number_is_saved_and_reading_does_not_increment(self):
        self.call('start')
        saved=copy.deepcopy(self.store.room13)
        self.call('start')
        self.store.room13=saved
        self.call('columns')
        self.assertEqual(self.store.room13['v111']['fork_run'],1)
        self.assertEqual(self.persistent.r13_fork_runs,2)
    def test_capture_failure_is_recorded_and_latest_replaces_bytes(self):
        self.call('record','gate','win')
        self.assertEqual(self.persistent.r13_fork_seen[('gate','win')]['png'],b'png')
        def fail(size):raise RuntimeError('web')
        self.env['renpy'].screenshot_to_bytes=fail
        self.call('record','gate','win')
        self.assertIsNone(self.persistent.r13_fork_seen[('gate','win')]['png'])
        self.call('ending','true')
        self.assertIn('true',self.persistent.r13_fork_endings)
        self.assertTrue(self.saves)
    def test_meeting_hook_records_only_first_decision(self):
        source=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
        code=source.split('init 318 python:\n')[1].split('    R13_NW_LISTABLE=')[0]
        tree=ast.parse(textwrap.dedent(code))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_nw_meeting_end')
        self.env.update(R13_NW_MEETING_RESULTS=('win','partial','lose'),r13_v111_set=lambda k,v:self.values.update({k:v}))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'meeting','exec'),self.env)
        self.env['r13_nw_meeting_end']('gate','win')
        self.env['r13_nw_meeting_end']('gate','lose')
        self.assertEqual(self.values['meeting:gate'],'win')
        self.assertEqual(list(self.persistent.r13_fork_seen),[('gate','win')])
        self.assertEqual(len(self.saves),1)
    def test_capture_fallback_uses_meeting_place(self):
        self.env.update(R13_PLACES={'room13':('13호실','room'),'square':('광장','winter_square')},r13_background=lambda name:'bg:'+name)
        self.assertEqual(self.call('image',{'png':None},'room13'),'bg:room')

    def test_fate_points_show_their_own_result_names(self):
        # 0.20.20: 판정 시점 칸은 회의와 같은 줄에 있고, 결과 이름은 그 칸의 말(들임/꺼진 등…)을 쓴다.
        self.values.update({'meeting:gate':'win','fate:fate_piko':'lost'})
        col=[c for c in self.call('columns') if c['key']=='fate_piko'][0]
        self.assertEqual([r['kind'] for r in col['rows']],['current','locked'])
        self.assertEqual(self.call('result_name','fate_piko','lost'),'꺼진 등')
        self.assertTrue(col['fate'])
        self.call('set_fate','fate_piko','saved')   # 한 번 정해지면 바뀌지 않는다
        self.assertNotIn(('fate_piko','saved'),self.persistent.r13_fork_seen)
    def test_all_completed_has_no_future_and_valid_page(self):
        self.values.update({'meeting:'+m[0]:'win' for m in self.env['R13_FORK_MEETINGS']})
        self.assertEqual(self.call('current'),16)
        self.assertEqual(len(self.call('columns')),17)
        self.assertEqual(self.call('initial_page'),11)

    def test_grand_unseen_is_only_one_more_in_the_hidden_count(self):
        self.values['meeting:fire']='lose'
        fire=next(c for c in self.call('columns') if c['key']=='fire')
        self.assertEqual(fire['rows'][-1],dict(kind='locked',result=None,title=None,record=None,count=3))
        self.assertNotIn('grand',repr(fire['rows']))

    def test_grand_promotion_does_not_collect_plain_win_in_the_same_run(self):
        self.values['meeting:fire']='win'
        self.call('record','fire','win')
        self.values['grand:fire']=True
        self.call('promote_grand','fire')
        self.assertEqual(set(self.persistent.r13_fork_seen),{('fire','grand')})
        self.assertEqual(self.call('value','fire'),'grand')
        before=(copy.deepcopy(self.persistent.r13_fork_seen),len(self.saves))
        rows=next(c['rows'] for c in self.call('columns') if c['key']=='fire')
        self.assertEqual(rows[0]['result'],'grand')
        self.assertEqual(rows[-1]['count'],3)
        self.assertEqual(before,(self.persistent.r13_fork_seen,len(self.saves)))

    def test_grand_promotion_preserves_a_plain_win_from_an_older_run(self):
        old=dict(png=b'old win',run=1)
        self.persistent.r13_fork_seen[('soup','win')]=old
        self.store.room13['v111']['fork_run']=2
        self.values['meeting:soup']='win'
        self.call('record','soup','win')
        self.call('record','soup','win')
        self.values['grand:soup']=True
        self.call('promote_grand','soup')
        self.assertEqual(self.persistent.r13_fork_seen[('soup','win')],old)
        self.assertEqual(self.persistent.r13_fork_seen[('soup','grand')]['run'],2)

    def test_grand_flag_before_verdict_waits_for_an_actual_win(self):
        self.values['grand:soup']=True
        self.call('promote_grand','soup')
        self.assertFalse(self.persistent.r13_fork_seen)
        self.values['meeting:soup']='partial'
        self.call('record','soup','partial')
        self.assertEqual(self.call('value','soup'),'partial')
        self.values['meeting:soup']='win'
        self.call('record','soup','win')
        self.assertNotIn(('soup','win'),self.persistent.r13_fork_seen)
        self.assertIn(('soup','grand'),self.persistent.r13_fork_seen)

    def test_grand_observer_preserves_original_setter_and_ignores_other_state(self):
        source=(ROOT/'game/room13_fork_screen.rpy').read_text().split('init 331 python:\n')[1]
        calls=[]
        def setter(key,value):
            calls.append((key,value));self.values[key]=value
            return 'unchanged contract'
        self.env['r13_v111_set']=setter
        exec(textwrap.dedent(source),self.env)
        self.assertEqual(self.env['r13_v111_set']('unrelated',False),'unchanged contract')
        self.assertFalse(self.saves)
        self.values['meeting:fire']='win';self.call('record','fire','win')
        self.env['r13_v111_set']('grand:fire',True)
        writes=len(self.saves)
        self.env['r13_v111_set']('grand:fire',True)
        self.assertEqual(len(self.saves),writes)
        self.assertEqual(calls,[('unrelated',False),('grand:fire',True),('grand:fire',True)])
        self.assertEqual(self.values,{'unrelated':False,'meeting:fire':'win','grand:fire':True})

if __name__=='__main__':unittest.main()
