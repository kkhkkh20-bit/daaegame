"""Execute actual source helpers and extracted Ren'Py menu/dispatch statements.

No Ren'Py process, visuals, save-load UI or click-path assertion. Only unrelated
rendering/notification and calendar context are isolated. Existing topic data,
availability, presentation, compare, grant and finish semantics are production.
Set R13_PROJECT_ROOT to a fully composed project to rerun on integration.
"""
import ast
import copy
import json
import os
import re
import textwrap
import types
import unittest
from pathlib import Path

DEFAULT_ROOT=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='dev' else Path(__file__).with_name('validation-project')
ROOT=Path(os.environ.get('R13_PROJECT_ROOT',str(DEFAULT_ROOT)))
GAME=ROOT/'game'

def load_function(ns,relative,name):
    lines=(GAME/relative).read_text().splitlines(True)
    start=next(i for i,line in enumerate(lines) if line.startswith('    def '+name+'('))
    end=start+1
    while end<len(lines):
        if lines[end].strip() and not lines[end].startswith('        '):break
        end+=1
    exec(compile(textwrap.dedent(''.join(lines[start:end])),relative,'exec'),ns)

def load_poc_topic(ns):
    text=(GAME/'systems/room13_poc_route.rpy').read_text().split('init 100 python:\n',1)[1].split('\nlabel ',1)[0]
    tree=ast.parse(textwrap.dedent(text))
    witness=next(n for n in tree.body if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=="R13_POC_WITNESSES")
    loop=next(n for n in tree.body if isinstance(n,ast.For) and ast.unparse(n.iter)=="R13_POC_WITNESSES.items()")
    ns["R13_RECORD_SHORT"]={}
    exec(compile(ast.Module(body=[witness,loop],type_ignores=[]),"poc-evidence","exec"),ns)
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and
              ast.unparse(n.targets[0])=="ROOM13['topics']['poc:granny_letter']")
    exec(compile(ast.Module(body=[node],type_ignores=[]),'poc-topic','exec'),ns)

def menu_branches(ns):
    """Read conditions and executable bodies from the real Ren'Py menu."""
    source=(GAME/'systems/room13_granny_reply.rpy').read_text().split('label r13_granny_warning_reply:\n',1)[1]
    before,menu=source.split('    menu:\n',1)
    for line in before.splitlines():
        if line.strip().startswith('$ '):exec(line.strip()[2:],ns)
    choices=[]
    for line in menu.splitlines():
        match=re.fullmatch(r'        "([^"]+)"(?: if (.+))?:',line)
        if match:
            choices.append([match[1],not match[2] or bool(eval(match[2],ns)),[]])
        elif line.strip():choices[-1][2].append(line.strip())
    return choices

def choose(ns,index):
    title,visible,statements=menu_branches(ns)[index]
    if not visible:raise ValueError('The source menu hides this choice: '+title)
    spoken=[]
    for statement in statements:
        if statement.startswith('call r13_lines('):
            # Same literal arguments, with the UI renderer replaced by collection.
            args=statement[len('call r13_lines('):-1]
            spoken.append(eval('('+args+')',ns))
        elif statement.startswith('return '):return eval(statement[7:],ns),spoken
        elif statement.startswith('$ '):exec(statement[2:],ns)
        else:raise AssertionError(('Unhandled production statement',statement))
    raise AssertionError('Source branch lacks return')

class GrannyReplyChoice(unittest.TestCase):
    def setUp(self):
        self.store=types.SimpleNamespace(room13=dict(day=3,period=0,location='inn',case_state='pending',daram_state='with_dad',life_poc=True,evidence=['E01','E18'],records={},flags=['lodging'],read_topics=['granny_letter'],resident_knowledge={},propositions=[],arguments={},log=[]),r13_topic_shown=None)
        self.n=dict(store=self.store,winter_copy=copy,persistent=types.SimpleNamespace(room13_knowledge=[]),
                    ROOM13=json.loads((GAME/'room13-content.json').read_text()),R13_WEEK2_DAY=11,R13_CASE_DAY=5,R13_TRIAL_DAY=7,
                    R13_CORE_PEOPLE=['granny'],R13_RESIDENTS={},R13_NAMES={'granny':'할머니'},
                    R13_OPENING_SCENES={'with_daram':{}},R13_TOPIC_FLAG_LINES={},R13_CALENDAR={},
                    source_fx=lambda *a:None,renpy=types.SimpleNamespace(notify=lambda *a:None),
                    r13_w2_present=lambda *a:None,r13_calendar_key=lambda person:'test:day3:morning',
                    r13_topic_current_context=lambda key:None)
        n=self.n
        for name in ('r13_has','r13_flag','r13_grant','r13_available','r13_topics','r13_present','r13_finish_topic'):
            load_function(n,'room13_rules.rpy',name)
        load_poc_topic(n)
        load_function(n,'systems/room13_poc_route.rpy','r13_poc_active')
        n['_r13_poc_topics']=n['r13_topics'];load_function(n,'systems/room13_poc_route.rpy','r13_topics')
        n['_r13_poc_present']=n['r13_present'];load_function(n,'systems/room13_poc_route.rpy','r13_present')
        for name in ('r13_granny_warning_asked','r13_granny_warning_followup','r13_granny_warning_source_known'):
            load_function(n,'systems/room13_granny_reply.rpy',name)
        load_function(n,'room13_dialogue_openings_20261013.rpy','r13_conversation_topic_lines')
        n['_r13_expand_topic_lines']=n['r13_conversation_topic_lines']
        n['R13_DIALOGUE_EXPAND']=json.loads((GAME/'room13-dialogue-expand.json').read_text())
        for name in ('r13_expand_norm','r13_conversation_topic_lines'):
            load_function(n,'systems/room13_dialogue_expand.rpy',name)
        load_function(n,'room13_record_compare.rpy','r13_compare_result')
        n['_r13_poc_compare']=n['r13_compare_result'];load_function(n,'systems/room13_poc_route.rpy','r13_compare_result')

    @property
    def s(self):return self.store.room13
    def present(self):return self.n['r13_present']('granny','E18')

    def test_owned_presentation_stops_at_question_preserving_real_exposure(self):
        before=copy.deepcopy(self.s);rows=self.present()
        self.assertEqual(rows,[('granny','그분이 아직 연락을 하고 있었군요. 어디서 받았어요?')])
        self.assertTrue(self.n['r13_granny_warning_asked']('granny','E18',rows))
        self.assertIn('warning_exposed',self.s['flags'])
        self.assertIn('poc:warning_shown_granny',self.s['flags'])
        self.assertEqual(self.s['resident_knowledge']['granny'],['E18:anonymous'])
        for key in ('day','period','evidence','records','read_topics'):self.assertEqual(self.s[key],before[key])
        self.assertNotIn('poc:letter_conflict',self.s['flags']);self.assertNotIn('J06',self.s['evidence'])

    def test_unowned_presentation_cannot_expose_or_enter_menu(self):
        self.s['evidence'].remove('E18');before=copy.deepcopy(self.s)
        rows=self.present()
        self.assertEqual(rows,[(None,'내가 직접 모은 자료가 아니다.')]);self.assertEqual(self.s,before)
        self.assertFalse(self.n['r13_granny_warning_asked']('granny','E18',rows))

    def test_repeat_is_idempotent_but_still_offers_choice(self):
        self.present();before=copy.deepcopy(self.s);rows=self.present()
        self.assertEqual(self.s,before);self.assertTrue(self.n['r13_granny_warning_asked']('granny','E18',rows))

    def test_only_this_delivered_question_enters_menu(self):
        rows=self.present();f=self.n['r13_granny_warning_asked']
        self.assertFalse(f('nabi','E18',rows));self.assertFalse(f('granny','E01',rows))
        self.assertFalse(f('granny','E18',[('granny','전에 보여 준 내용은 기억합니다.')]))
        self.assertTrue(f('granny','E18',[list(rows[0])]))

    def test_followup_does_not_manufacture_comparison_or_testimony(self):
        self.present();before=copy.deepcopy(self.s)
        self.assertIsNone(self.n['r13_granny_warning_followup']());self.assertEqual(self.s,before)
        self.assertFalse(menu_branches(self.n)[2][1]);self.assertNotIn('J06',self.s['evidence'])
        with self.assertRaises(ValueError):choose(self.n,2)

    def test_existing_unread_invitation_can_continue_without_claim_upgrade(self):
        self.present();self.s['read_topics']=[]
        self.assertEqual(self.n['r13_granny_warning_followup'](),'granny_letter')
        result,spoken=choose(self.n,2)
        self.assertEqual(result,'granny_letter');self.assertEqual(spoken[0][0],[('dad','장소까지 말씀드리지는 않겠습니다.')])
        self.assertNotIn('poc:letter_conflict',self.s['flags']);self.assertNotIn('J06',self.s['evidence'])

    def test_compared_invitation_preserves_day_life_and_read_gates(self):
        self.present();self.n['r13_compare_result'](['E01','E18'])
        self.assertEqual(self.n['r13_granny_warning_followup'](),'poc:granny_letter')
        day=self.s['day'];minimum=self.n['ROOM13']['topics']['poc:granny_letter']['day'][0]
        self.s['day']=minimum-1;self.assertIsNone(self.n['r13_granny_warning_followup']());self.s['day']=day
        self.s['life_poc']=False;self.assertIsNone(self.n['r13_granny_warning_followup']());self.s['life_poc']=True
        self.s['case_state']='occurred';self.assertIsNone(self.n['r13_granny_warning_followup']());self.s['case_state']='pending'
        self.s['read_topics'].append('poc:granny_letter');self.assertIsNone(self.n['r13_granny_warning_followup']())

    def test_counterquestion_is_available_before_comparison_and_does_not_disclose(self):
        self.present();before=copy.deepcopy(self.s)
        result,spoken=choose(self.n,1)
        self.assertIsNone(result);self.assertEqual(self.s,before)
        self.assertEqual(spoken[0][0][0],('dad','어디서 받았는지는 왜 궁금하십니까?'))
        self.assertNotIn('warning_source_exposed',self.s['flags'])
        self.assertNotIn('poc:letter_conflict',self.s['flags']);self.assertNotIn('J06',self.s['evidence'])

    def test_withhold_and_exit_are_explicit_player_choices(self):
        self.present();before=copy.deepcopy(self.s)
        result,spoken=choose(self.n,3)
        self.assertIsNone(result);self.assertEqual(spoken[0][0],[('dad','장소까지 말씀드리지는 않겠습니다.')]);self.assertEqual(self.s,before)
        self.assertEqual(choose(self.n,4),('back',[]));self.assertEqual(self.s,before)
        self.assertIn('warning_exposed',self.s['flags']);self.assertNotIn('J06',self.s['evidence'])

    def test_location_knowledge_or_legacy_unprovenance_never_invents_pickup(self):
        self.present();self.s['flags']+=['warning_location','warning_sealed_held']
        self.s['evidence'].append('J18')
        self.assertFalse(self.n['r13_granny_warning_source_known']())
        self.assertFalse(menu_branches(self.n)[0][1])
        with self.assertRaises(ValueError):choose(self.n,0)

    def test_actual_pickup_routes_allow_truthful_source_only_after_e18(self):
        for pickup in ('warning','warning_keep'):
            with self.subTest(pickup=pickup):
                self.s['done']=[pickup]
                self.assertTrue(self.n['r13_granny_warning_source_known']())
                self.s['evidence'].remove('E18')
                self.assertFalse(self.n['r13_granny_warning_source_known']())
                self.s['evidence'].append('E18')
        self.s['done']=['unrelated'];self.assertFalse(self.n['r13_granny_warning_source_known']())

    def test_explicit_source_choice_records_disclosure_without_extra_claims(self):
        self.present();self.s['done']=['warning_keep'];before=copy.deepcopy(self.s)
        result,spoken=choose(self.n,0)
        self.assertIsNone(result)
        self.assertEqual(spoken[0][0][0],('dad','광장 등 밑 점검함에서 꺼냈습니다.'))
        self.assertIn('warning_source_exposed',self.s['flags']);self.assertIn('warning_exposed',self.s['flags'])
        self.assertNotIn('poc:letter_conflict',self.s['flags']);self.assertNotIn('J06',self.s['evidence'])
        for key in ('day','period','evidence','records','read_topics'):self.assertEqual(self.s[key],before[key])

    def test_explicit_followup_grants_j06_only_after_real_topic_dispatch(self):
        self.present();self.n['r13_compare_result'](['E01','E18']);self.n['r13_topic'],spoken=choose(self.n,2)
        self.assertEqual(self.n['r13_topic'],'poc:granny_letter');self.assertNotIn('J06',self.s['evidence'])
        # Execute exactly the normal fresh-topic dispatch lines, not a separate
        # shortcut that calls the award function on menu selection.
        source=(GAME/'room13.rpy').read_text()
        start=source.index('    $ r13_topic_rows=r13_topic_current_lines(')
        block=source[start:source.index('    jump r13_talk_menu',start)]
        shown=[]
        for line in block.splitlines():
            statement=line.strip()
            if statement.startswith('$ '):
                exec(statement[2:],self.n)
                # Ren'Py store globals and Python global assignments share a store.
                node=ast.parse(statement[2:]).body[0]
                if isinstance(node,ast.Assign):
                    for target in node.targets:
                        if isinstance(target,ast.Name):setattr(self.store,target.id,self.n[target.id])
            elif statement.startswith('call r13_lines('):
                expression=statement[len('call r13_lines('):-1]
                self.n['_render']=lambda rows,identity,**kw:shown.extend(rows)
                eval('_render('+expression+')',self.n)
            else:raise AssertionError(statement)
        self.assertTrue(any(row[0]=='granny' for row in shown))
        self.assertIn('J06',self.s['evidence']);self.assertIn('poc:granny_explained',self.s['flags'])
        self.assertEqual(self.s['topic_transcripts']['poc:granny_letter'],[[row[0],row[1],False] for row in shown])
        self.assertEqual((self.s['day'],self.s['period']),(3,0))

    def test_main_hook_uses_normal_dispatch_after_grants_and_not_auto_return(self):
        source=(GAME/'room13.rpy').read_text()
        expected='''            $ r13_flush_grants()
            if r13_granny_warning_asked(r13_target,r13_item,r13_reaction):
                call r13_granny_warning_reply
                if _return:
                    $ r13_topic=_return
                    jump r13_talk_dispatch
        jump r13_talk_menu'''
        self.assertIn(expected,source)

if __name__=='__main__':unittest.main(verbosity=2)
