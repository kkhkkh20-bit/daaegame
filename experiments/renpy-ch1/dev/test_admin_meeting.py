"""Pure-Python fixture/guard checks; native Replay restoration needs runtime QA."""
import ast
import copy
import json
import textwrap
import types
import unittest
from pathlib import Path
import test_meeting_flow

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_admin_meeting.rpy'

def function(path,name,env):
    text=path.read_text()
    start=text.index('    def '+name+'(')
    tail=text[start:]
    lines=tail.splitlines()
    end=next((i for i,line in enumerate(lines[1:],1) if line.strip() and not line.startswith('        ')),len(lines))
    exec(textwrap.dedent('\n'.join(lines[:end])),env)

class AdminMeeting(unittest.TestCase):
    def setUp(self):
        fixture=test_meeting_flow.MeetingFlow();fixture.setUp()
        self.env=fixture.env;self.store=fixture.store
        self.env.update(ROOM13=json.loads((ROOT/'game/room13-content.json').read_text()),R13_TRIAL_DAY=7)
        function(ROOT/'game/room13_rules.rpy','r13_new',self.env)
        src=SOURCE.read_text().split('init 180 python:\n',1)[1].split('\nscreen ',1)[0]
        exec(textwrap.dedent(src),self.env)

    def test_c2_is_first_and_only_actual_trial_claims_are_selectable(self):
        self.assertEqual(self.env['R13_ADMIN_MEETINGS'],('C2','C1','C3','C4'))
        for claim in self.env['R13_ADMIN_MEETINGS']:
            self.assertIn(claim,self.env['R13_DEBATE'])
        with self.assertRaises(ValueError):self.env['r13_admin_meeting_fixture']('F4')

    def test_fresh_fixture_preserves_progress_and_selected_claim_is_unproved(self):
        before=copy.deepcopy(self.store.room13)
        n=self.env['r13_admin_meeting_fixture']('C2')
        self.assertEqual(self.store.room13,before)
        self.assertEqual((n['day'],n['period'],n['location'],n['case_state'],n['daram_state']),(7,2,'dining','occurred','held'))
        self.assertEqual(n['propositions'],['C1']);self.assertEqual(n['arguments'],{})
        self.assertNotIn('debate',n)
        self.assertIn('bami_consent',n['flags'])
        self.assertEqual(set(n['evidence']),set(self.env['ROOM13']['evidence']))
        self.assertEqual(set(n['records']),set(n['evidence']))

    def test_every_selection_can_be_engaged_without_prebreaking_statements(self):
        for claim in self.env['R13_ADMIN_MEETINGS']:
            self.store.room13=self.env['r13_admin_meeting_fixture'](claim)
            self.assertTrue(self.env['r13_debate_engageable'](claim),claim)
            self.assertFalse(self.env['r13_debate_ready'](claim),claim)

    def test_restart_builds_independent_clean_state(self):
        a=self.env['r13_admin_meeting_fixture']('C2')
        a['propositions'].append('C2');a['evidence'].clear();a['flags'].append('changed')
        b=self.env['r13_admin_meeting_fixture']('C2')
        self.assertEqual(b['propositions'],['C1']);self.assertTrue(b['evidence'])
        self.assertNotIn('changed',b['flags'])

    def test_c2_uses_real_changed_dialogue_and_counter_not_a_fake_result(self):
        self.store.room13=self.env['r13_admin_meeting_fixture']('C2')
        result,rows=self.env['r13_debate_judge']('C2','s1','E08')
        self.assertEqual(result,'break')
        self.assertIn('어느 상처를 누가 냈는지는',rows[0][1])
        self.assertTrue(self.env['r13_debate_counter']('C2','s3'))
        self.assertEqual(self.store.room13['propositions'],['C1'])

    def test_no_autosave_request_in_test_but_normal_autosave_remains(self):
        calls=[]
        self.env['renpy']=types.SimpleNamespace(is_skipping=lambda:False,force_autosave=lambda **kw:calls.append(kw))
        function(ROOT/'game/systems/room13_convenience.rpy','r13_autosave_now',self.env)
        self.store.r13_admin_meeting_test=True;self.env['r13_autosave_now']()
        self.assertEqual(calls,[])
        self.store.r13_admin_meeting_test=False;self.env['r13_autosave_now']()
        self.assertEqual(len(calls),1)

    def test_read_history_is_not_written_in_test(self):
        self.env['persistent']=types.SimpleNamespace(room13_read=['old'])
        function(ROOT/'game/room13_rules.rpy','r13_remember_line',self.env)
        self.store.r13_admin_meeting_test=True;self.env['r13_remember_line']('test')
        self.assertEqual(self.env['persistent'].room13_read,['old'])
        self.store.r13_admin_meeting_test=False;self.env['r13_remember_line']('normal')
        self.assertEqual(self.env['persistent'].room13_read,['old','normal'])

    def test_optional_quick_keys_require_registered_events(self):
        src=SOURCE.read_text()
        for event in ("quick_save", "quick_load"):
            expected='    if "'+event+'" in config.keymap:'+chr(10)+'        key "'+event+'" action NullAction()'
            self.assertIn(expected,src)
        self.assertIn('$ _autosave=False',src)
        self.assertIn('action Replay("r13_admin_meeting_replay"',src)

    def test_replay_and_exit_contract_and_no_campaign_jump(self):
        src=SOURCE.read_text()
        self.assertIn('action Replay("r13_admin_meeting_replay"',src)
        self.assertIn('if not _in_replay or not persistent.room13_admin',src)
        self.assertIn('$ _autosave=False',src)
        self.assertIn('call r13_debate_run(r13_admin_meeting_claim)',src)
        self.assertIn('action EndReplay(confirm=False)',src)
        self.assertNotIn('Jump(',src)
        self.assertNotIn('call r13_argument(',src)
        self.assertNotIn('r13_grant(',src)
        self.assertNotIn('persistent.room13_admin=',src)

if __name__=='__main__':unittest.main()
