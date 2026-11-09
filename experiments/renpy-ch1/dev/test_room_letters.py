"""첫 방의 책상 조사·읽기 쌍·옛 저장과 숨은 종이 기회를 확인한다."""
import ast
import copy
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
CLAIM='v111:두 편지를 나란히 본다'
PAIR=('V111:E01','V111:E06')


class RoomLetters(unittest.TestCase):
    def environment(self,owned=PAIR,views=None,screen=None,values=None,flags=()):
        state=types.SimpleNamespace(room13=dict(evidence=list(owned),arguments={CLAIM:[]},day=1,period=1),
                                    r13_pw_views=copy.deepcopy(views or {}))
        callbacks=[]
        state.room13.update(v111=dict(values=dict(values or {})),flags=list(flags))
        env=dict(store=state,renpy=types.SimpleNamespace(get_screen=lambda name:screen,restart_interaction=lambda:None),
                 config=types.SimpleNamespace(after_load_callbacks=callbacks),
                 R13_V111_STEP_GOALS={},R13_V111_RECORD_LATER={},
                 r13_v111_value=lambda key:state.room13['v111']['values'].get(key),
                 r13_has=lambda key:key in state.room13['flags'])
        source=(GAME/'systems/room13_room_letters.rpy').read_text().split('init 355 python:',1)[1]
        exec(compile(ast.parse(textwrap.dedent(source)),'첫 방 읽기','exec'),env)
        return env,state,callbacks

    def test_first_room_opens_two_owned_documents_without_selecting_or_granting(self):
        env,state,_=self.environment()
        before=copy.deepcopy(state.room13)
        self.assertTrue(env['r13_room_letters_open']())
        self.assertEqual(state.room13,before)
        row=state.r13_pw_views[CLAIM]
        self.assertEqual(row['view'],'pair')
        self.assertEqual(row['pair'],PAIR)
        self.assertEqual(row['detail'],'V111:E06')

    def test_incomplete_inventory_is_never_repaired_by_granting_or_showing_unowned(self):
        for owned in [(),('V111:E01',),('V111:E06',)]:
            env,state,_=self.environment(owned)
            before=copy.deepcopy(vars(state))
            self.assertFalse(env['r13_room_letters_open']())
            self.assertEqual(vars(state),before)

    def test_reopening_keeps_the_readers_own_pair_after_one_initial_open(self):
        env,state,_=self.environment()
        env['r13_room_letters_open']()
        state.r13_pw_views[CLAIM].update(view='single',detail='V111:E01',pair=('V111:E01',None))
        before=copy.deepcopy(state.r13_pw_views)
        self.assertFalse(env['r13_room_letters_open']())
        self.assertEqual(state.r13_pw_views,before)

    def test_only_unfinished_first_room_pair_requires_discovery(self):
        env,state,_=self.environment()
        pending=env['r13_room_letters_discovery_pending']
        self.assertTrue(pending('두 편지를 나란히 본다',PAIR))
        self.assertTrue(pending(CLAIM,tuple(reversed(PAIR))))
        for key,pair in [('함께 들어갈 근거를 고른다',PAIR),
                         ('두 편지의 초대를 대조한다',PAIR),
                         (CLAIM,('V111:E01','V111:E03')),
                         (CLAIM,('V111:E01',None)),(CLAIM,('V111:E01','V111:E01'))]:
            self.assertFalse(pending(key,pair))
        state.room13['v111']['values']['letter_tail_observed']=True
        self.assertFalse(pending(CLAIM,PAIR))

    def test_current_inquiry_does_not_require_a_spot_guess_or_grant_its_discovery(self):
        env,state,_=self.environment(values={'letter_inquiry_mode138':True})
        before=copy.deepcopy(vars(state))
        self.assertFalse(env['r13_room_letters_discovery_pending'](CLAIM,PAIR))
        self.assertFalse(env['r13_room_letters_begin_discovery'](CLAIM,PAIR))
        self.assertEqual(vars(state),before)
        self.assertNotIn('letter_tail_observed',state.room13['v111']['values'])

    def test_completed_old_saves_do_not_gain_a_new_required_step(self):
        for values,flags in [({'proof_given:두 편지를 나란히 본다':list(PAIR)},()),
                             ({},('v111:applied:MS14_D01_S05_L0031',))]:
            env,state,_=self.environment(values=values,flags=flags)
            before=copy.deepcopy(vars(state))
            self.assertFalse(env['r13_room_letters_discovery_pending'](CLAIM,PAIR))
            self.assertFalse(env['r13_room_letters_begin_discovery'](CLAIM,PAIR))
            self.assertEqual(vars(state),before)

    def test_begin_discovery_only_changes_reading_ui_and_survives_reopen(self):
        screen=types.SimpleNamespace(scope=dict(view='list',observe=False,pick_slot=0))
        env,state,_=self.environment(screen=screen)
        before=copy.deepcopy(state.room13)
        self.assertTrue(env['r13_room_letters_begin_discovery'](CLAIM,PAIR))
        self.assertEqual(state.room13,before)
        self.assertEqual(screen.scope['pair'],PAIR)
        self.assertEqual(screen.scope['view'],'pair')
        self.assertTrue(screen.scope['observe'])
        self.assertIsNone(screen.scope['pick_slot'])
        self.assertTrue(state.r13_pw_views[CLAIM]['room_letters_discovery'])

    def test_wrong_pair_does_not_receive_a_discovery_repair(self):
        env,state,_=self.environment()
        before=copy.deepcopy(vars(state))
        self.assertFalse(env['r13_room_letters_begin_discovery'](CLAIM,('V111:E01','V111:E03')))
        self.assertEqual(vars(state),before)

    def test_screen_and_legacy_return_use_the_same_no_penalty_discovery_guard(self):
        screen=(GAME/'systems/room13_proof_workspace.rpy').read_text()
        self.assertIn('r13_room_letters_begin_discovery(claim,chosen)',screen)
        self.assertIn('Function(r13_pw_submit_selected,claim)',screen)
        self.assertIn('id r13_pw_id("r13_pw_document_tail_",key)',screen)
        self.assertIn('action Return(("observe","tail")) sensitive ready',screen)
        flow=(GAME/'room13_v111.rpy').read_text().split('label r13_v111_proof_again:',1)[1]
        guard=flow.index('if _return=="argue" and r13_room_letters_discovery_pending')
        self.assertLess(guard,flow.index('r13_v111_proof_accepts('))
        self.assertNotIn('r13_nw_retry(',flow[guard:flow.index('    if _return=="argue":',guard)])

    def test_saved_open_single_document_screen_is_migrated_only_in_first_room_comparison(self):
        screen=types.SimpleNamespace(scope=dict(key='두 편지를 나란히 본다',view='single',pair=('V111:E01',None)))
        views={CLAIM:dict(view='single',detail='V111:E01',pair=('V111:E01',None))}
        env,state,callbacks=self.environment(views=views,screen=screen)
        before=copy.deepcopy(state.room13)
        callbacks[0]()
        self.assertEqual(state.room13,before)
        self.assertEqual(screen.scope['view'],'pair')
        self.assertEqual(screen.scope['pair'],PAIR)
        screen.scope.update(view='single',pair=('V111:E01',None))
        callbacks[0]()
        self.assertEqual(screen.scope['view'],'single')
        other=types.SimpleNamespace(scope=dict(key='함께 들어갈 근거를 고른다',view='single'))
        env,state,callbacks=self.environment(screen=other)
        callbacks[0]()
        self.assertEqual(state.r13_pw_views,{})
        self.assertEqual(other.scope,dict(key='함께 들어갈 근거를 고른다',view='single'))

    def test_room_note_continues_to_existing_family_facts_without_another_prop_gate(self):
        source=(GAME/'room13_v111_days123.rpy').read_text()
        note=source.split('label r13_v111_room_note:',1)[1].split('\nlabel ',1)[0]
        self.assertIn('jump r13_v111_bundle',note)
        self.assertNotIn('jump r13_v111_bundle_open',note)
        family=source.split('label r13_v111_bundle:',1)[1].split('\nlabel ',1)[0]
        self.assertIn("r13_v111_commit('MS14_D01_S05_L0022')",family)
        compare=source.split('label r13_v111_letter_compare:',1)[1].split('\nlabel ',1)[0]
        self.assertIn('r13_room_letters_open()',compare)
        self.assertIn("['E01', 'E06']",compare)
        original=json.loads((GAME/'v111/records.json').read_text())['records']['MS14_D01_S05_L0022']
        self.assertEqual(original['effects'],['acquire(E30)','under_desk_checked=true'])

    def test_hidden_paper_remains_optional_at_legacy_and_new_room_waits(self):
        bindings=json.loads((GAME/'v111/field-bindings.json').read_text())
        legacy=bindings['bundle_open']['options']
        self.assertEqual(legacy[0]['object'],'mother_note')
        self.assertEqual(legacy[0]['title'],'메모 밑 접힌 그림을 펼친다')
        for key in ('bundle_open','sleep1'):
            rows=bindings[key]['options']
            hidden=next(row for row in rows if row.get('index')==100)
            self.assertEqual(hidden['guard'],[['state','hidden_base:paper',None]])
        self.assertEqual(bindings['sleep1']['options'][0]['object'],'bed')
        source=(GAME/'room13_v111_days123.rpy').read_text()
        for label in ('bundle_open','sleep1'):
            block=source.split('label r13_v111_'+label+':',1)[1].split('\nlabel ',1)[0]
            self.assertIn('if _return==100:',block)
            self.assertIn('call r13_hidden_base_paper1',block)
            self.assertIn('jump r13_v111_'+label,block)

    def test_note_and_record_keep_same_lead_and_drawing_location(self):
        data=json.loads((GAME/'v111/newworld/d01.json').read_text())
        note=data['replace']['MS14_D01_S05_L9101']['text']
        self.assertEqual(note,data['evidence']['E06']['variants']['observed'])
        self.assertIn('초롱에게 소식을 물어봐',note)
        self.assertIn('메모 밑에 접어 두었어',note)
        self.assertIn('{image=assets/room13-acorn-ink-crooked.png}',note)
        self.assertNotIn('책상 아래',note)
        facts=json.loads((GAME/'v111/evidence-facts.json').read_text())
        self.assertIn('메모 밑',facts['E06']['observed'][1])
        self.assertIn('메모 밑',facts['E30']['observed'][1])
        self.assertNotIn('밑바닥',str(facts['E30']))


if __name__=='__main__':unittest.main()
