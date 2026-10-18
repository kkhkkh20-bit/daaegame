"""Source-level integration for the new Sling disclosure design.

Executes actual final presentation/topic/line/completion provider chains, production
helpers and bounded source label control flow. Only rendering/audio/calendar and
unrelated catalogue UI endpoints are stand-ins. This is not a Ren'Py game run.
Explicit conversation skip retains the game's normal-return completion contract;
menu cancellation and interrupted calls are tested separately.
"""
import ast
import copy
import functools
import json
import re
import textwrap
import unittest
from pathlib import Path
import test_sling_choice_flow as flow

ROOT = Path(__file__).resolve().parents[1]
CONF = flow.CONFIDENCE

@functools.lru_cache(maxsize=1)
def init_blocks():
    blocks=[]
    for path in (ROOT/'game').rglob('*.rpy'):
        text=path.read_text(encoding='utf-8')
        wanted=('r13_present','r13_topics','r13_conversation_topic_lines','r13_finish_topic')
        constants=('R13_TOOL_DISCOVERIES','R13_DARAM_HOME_KEYS','R13_NIGHT_TALKS','R13_NIGHT_TALK_COND','R13_QUESTION_LEADS','R13_Q1_NEW_TOPICS','R13_CONTACT_RECORDS')
        if str(path.relative_to(ROOT/'game'))!=flow.CASES and not any('def '+name+'(' in text for name in wanted) and not any(name+'=' in text or name+' =' in text for name in constants):continue
        for match in re.finditer(r'^init(?:\s+(-?\d+))?\s+python:\s*\n',text,re.M):
            lines=[]
            for line in text[match.end():].splitlines(True):
                if line.strip() and not line.startswith((' ','\t')):break
                lines.append(line)
            tree=ast.parse(textwrap.dedent(''.join(lines)))
            blocks.append((int(match[1] or 0),str(path.relative_to(ROOT/'game')),match.start(),tree))
    return sorted(blocks,key=lambda row:row[:3])

def execute(ns,node,path):
    exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),ns)

def assignment(ns,name):
    for priority,path,start,tree in init_blocks():
        for node in tree.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
                execute(ns,node,path)
                return
    raise AssertionError('Missing production constant: '+name)

def chains(ns,names):
    trace={name:[] for name in names}
    for priority,path,start,tree in init_blocks():
        if path==CONF:continue
        for node in tree.body:
            if isinstance(node,ast.Assign) and isinstance(node.value,ast.Name) and node.value.id in names:
                execute(ns,node,path)
            elif isinstance(node,ast.FunctionDef) and node.name in names:
                execute(ns,node,path);trace[node.name].append((priority,path))
    return trace

class EarnedDisclosure(unittest.TestCase):
    def setUp(self):
        self.f=flow.SlingChoiceFlow();self.f.setUp()
        self.n=self.f.n;self.store=self.f.store
        self.s.update(resident_knowledge={},done=[],life_poc=True,question_cues={})
        # Full authored content, plus actual memory/new-topic specs loaded below.
        self.n['ROOM13']=json.loads((ROOT/'game/room13-content.json').read_text())
        self.n['ROOM13']['topics'].setdefault('somi_after_hostile',{})
        self.n['ROOM13']['topics'].setdefault('siluk_cold',{})
        self.n.update(R13_RESIDENTS={},R13_CORE_PEOPLE=('granny','nabi','buri','bami','seryeon','karo','daram'),
            R13_CALENDAR={},R13_TOPIC_FLAG_LINES={},R13_OPENING_SCENES={'with_daram':{},'first_meetings':{}},
            R13_DIALOGUE_EXPAND=json.loads((ROOT/'game/room13-dialogue-expand.json').read_text()),
            r13_fx_cue=lambda *a:None, r13_catalog_entries=lambda:[],r13_topic_current_fresh=lambda k:False)
        for name in ('R13_TOOL_DISCOVERIES','R13_DARAM_HOME_KEYS','R13_NIGHT_TALKS','R13_NIGHT_TALK_COND','R13_QUESTION_LEADS','R13_Q1_NEW_TOPICS','R13_CONTACT_RECORDS'):
            assignment(self.n,name)
        for relative,names in (
            ('room13_rules.rpy',('r13_dialogue_granny_reply',)),
            ('room13_home.rpy',('r13_home_with_daram',)),
            ('room13_week2_rules.rpy',('r13_w2_present',)),
            ('systems/room13_poc_route.rpy',('r13_poc_active','r13_poc_helped')),
            ('systems/room13_question_discovery.rpy',('r13_question_lead_known','r13_question_discovered','r13_contact_presentations')),
            ('systems/room13_q1_arguments.rpy',('r13_q1_v2','r13_q1_topic_available')),
            ('systems/room13_dialogue_expand.rpy',('r13_expand_norm',))):
            for name in names:flow.load_function(self.n,relative,name)
        # Authored memory specs and independent direct Granny topics, not test copies.
        block=flow.source(flow.MEMORY).split('init 114 python:\n',1)[1].split('\nlabel ',1)[0]
        exec(compile(textwrap.dedent(block),flow.MEMORY,'exec'),self.n)
        self.n['ROOM13']['topics']={k:v for k,v in self.n['ROOM13']['topics'].items() if 'npc' in v}
        for priority,path,start,tree in init_blocks():
            if path==flow.CASES:
                execute(self.n,tree.body[0],path) # actual H7/H8/H9 evidence specs
            if path=='systems/room13_present_flow.rpy':
                for node in tree.body:
                    if isinstance(node,ast.Assign) and ast.unparse(node).startswith("ROOM13['evidence']["):
                        execute(self.n,node,path)
            if path=='systems/room13_use_knowledge.rpy':
                for node in tree.body:
                    if isinstance(node,ast.Expr) and ast.unparse(node).startswith("ROOM13['topics'].update("):
                        execute(self.n,node,path)
        self.trace=chains(self.n,('r13_present','r13_topics','r13_conversation_topic_lines','r13_finish_topic'))
        # These helpers all have one later wrapper; retain its actual alias/order too.
        self.n['_r13_pf_w2_present']=self.n['r13_w2_present']
        flow.load_function(self.n,'systems/room13_present_flow.rpy','r13_w2_present')
        self.n['_r13_qa_contact']=self.n['r13_contact_presentations']
        flow.load_function(self.n,'systems/room13_q1_arguments.rpy','r13_contact_presentations')
        block=flow.source(CONF).split('init 206 python:\n',1)[1].split('\nlabel ',1)[0]
        exec(compile(textwrap.dedent(block),CONF,'exec'),self.n)
        self.before_present=self.n['_r13_sling_confidence_present']
        self.before_topics=self.n['_r13_sling_confidence_topics']
        self.n['r13_lines']=self.show
        self.mode='normal'
        self.f.runner=flow.SourceBranches(self.n,(flow.CASES,flow.MEMORY,CONF),self.f.choose)
    @property
    def s(self):return self.store.room13
    def show(self,rows,identity,**kw):
        self.f.show(rows,identity,**kw)
        if identity=='sling:confidence:confront' and self.mode=='interrupt':raise RuntimeError('simulated interrupted live call')
        # explicit conversation skip also returns normally, exactly as r13_lines.
    def flag(self,*keys):self.n['r13_flag'](*keys)
    def own(self,*keys):
        for key in keys:
            if key not in self.s['evidence']:self.s['evidence'].append(key)
    def present(self,key,person='resident_sling'):return self.n['r13_present'](person,key)
    def topics(self):return [key for key,spec in self.n['r13_topics']('resident_sling')]
    def label(self,name,*choices):
        self.f.choices=list(choices);self.f.runner.run(name);self.assertEqual([],self.f.choices)
    def no_disclosure(self):
        for key in ('H9','know_granny_reads','sling_confession_heard','sling_confront_completed'):
            self.assertFalse(self.n['r13_has'](key),key)
    def ready(self,route=('J06',)):
        self.own(*route)
        for key in route:self.present(key)
        self.label('r13_sling_protect_confidence')
        self.assertTrue(self.n['r13_sling_confront_ready']())
    def complete(self):self.label('r13_sling_earned_confront','편지 일을 끝까지 듣는다')

    def test_actual_final_chain_and_contact_candidates(self):
        self.assertEqual(21,len(self.trace['r13_present']))
        self.assertEqual(23,len(self.trace['r13_topics']))
        self.assertEqual(10,len(self.trace['r13_conversation_topic_lines']))
        self.assertEqual(5,len(self.trace['r13_finish_topic']))
        self.own('E18','J08','J06')
        self.assertTrue({'E18','J08','J06'}<=set(self.n['r13_contact_presentations']('resident_sling')))
        before=copy.deepcopy(self.s)
        for _ in range(3):
            self.topics();self.n['r13_contact_presentations']('resident_sling');self.n['r13_sling_confront_lines']()
        self.assertEqual(before,self.s);self.no_disclosure()

    def test_new_start_questions_all_refuse_real_name(self):
        f=self.f
        for route in ((f.CATCH,f.STOP),(f.WHO,f.STOP),(f.REPORT,f.LISTEN,f.STOP)):
            with self.subTest(route=route):
                self.setUp();self.f.run_letters(*route)
                self.no_disclosure();self.assertNotIn('할머니',str(self.f.lines))
                self.assertTrue(self.n['r13_sling_nonpaid_trust']())
                self.assertNotIn('sling:letter_requester',self.topics())
                self.assertEqual(3,self.f.money())

    def test_owned_only_is_never_shown_or_automatically_disclosed(self):
        for papers in (('E18','J08'),('J06',)):
            with self.subTest(papers=papers):
                self.setUp();self.own(*papers);self.flag('sling_nonpaid_trust','sling_job_pressure_heard')
                before=copy.deepcopy(self.s)
                self.assertFalse(self.n['r13_sling_confront_ready']());self.assertEqual([],self.n['r13_sling_confront_lines']())
                self.assertNotIn('sling:letter_requester',self.topics());self.label('r13_sling_earned_confront')
                self.assertEqual(before,self.s);self.no_disclosure()

    def test_e18_j08_orders_require_both_shown_and_nonpaid_relationship(self):
        for order in (('E18','J08'),('J08','E18')):
            for trust_first in (False,True):
                with self.subTest(order=order,trust_first=trust_first):
                    self.setUp();self.own(*order)
                    if trust_first:self.f.run_letters(self.f.CATCH,self.f.STOP)
                    first=self.present(order[0]);self.assertNotIn('할머니',str(first))
                    self.assertFalse(self.n['r13_sling_confront_ready']())
                    second=self.present(order[1]);self.assertNotIn('할머니',str(second));self.no_disclosure()
                    if not trust_first:
                        self.assertFalse(self.n['r13_sling_confront_ready']())
                        self.assertIn('sling:protect_confidence',self.topics());self.label('r13_sling_protect_confidence')
                    self.assertIn('sling:letter_requester',self.topics())
                    self.complete();self.assertTrue(self.n['r13_has']('H9'))
                    self.assertIn('여관 할머니가 시켰어요',str(self.f.lines[-1]))
                    self.assertIn('왜 필요한지는 말씀 안 하셨어요',str(self.f.lines[-1]))
                    self.assertEqual(3,self.f.money())

    def test_j06_alternate_no_unshown_e18_echo(self):
        self.ready();rows=self.n['r13_sling_confront_lines']()
        self.assertIn('보여 드린 기록',str(rows));self.assertNotIn('행선지',str(rows))
        self.assertNotIn('E18',self.s['resident_knowledge']['resident_sling'])
        self.no_disclosure();self.complete();self.assertEqual(1,self.s['evidence'].count('H9'))

    def test_j08_first_without_event_establishes_only_anonymous_pressure(self):
        self.own('J08');rows=self.present('J08')
        self.assertIn('베껴 오라는 부탁',str(rows));self.assertIn('일자리를',str(rows));self.assertNotIn('할머니',str(rows))
        self.assertIn('sling:protect_confidence',self.topics());self.label('r13_sling_protect_confidence')
        self.assertNotIn('편지를 연 일',str(self.f.lines));self.assertFalse(self.n['r13_sling_confront_ready']())

    def test_portrait_awards_testimony_but_does_not_show_it(self):
        self.own('P01','E18');self.present('P01');self.present('E18')
        self.assertTrue(self.n['r13_has']('J08'));self.assertTrue(self.n['r13_has']('portrait_known'))
        self.f.run_letters(self.f.PORTRAIT,self.f.SEND)
        self.assertFalse(self.n['r13_sling_confront_ready']());self.no_disclosure()
        self.present('J08');self.assertTrue(self.n['r13_sling_confront_ready']())

    def test_payment_alone_not_trust_but_free_promise_after_payment_works(self):
        self.f.run_letters(self.f.CATCH,self.f.PAY,self.f.SEND)
        self.own('J06');self.present('J06')
        self.assertEqual(0,self.f.money());self.assertFalse(self.n['r13_sling_confront_ready']())
        self.assertIn('sling:protect_confidence',self.topics());self.label('r13_sling_protect_confidence')
        self.complete();self.assertEqual(0,self.f.money());self.assertEqual(1,len(self.n['r13_wallet'](self.s)['ledger']))

    def test_unowned_wrong_recipient_and_single_paper_never_unlock(self):
        self.flag('sling_nonpaid_trust')
        before=copy.deepcopy(self.s);self.present('J06');self.assertEqual(before,self.s)
        self.own('J06','E18','J08');self.present('J06','granny');self.present('E18')
        self.assertFalse(self.n['r13_sling_confront_ready']());self.no_disclosure()

    def test_cancel_and_true_interruption_never_commit_live_confession(self):
        self.ready();before=copy.deepcopy(self.s)
        self.label('r13_sling_earned_confront','지금은 더 묻지 않는다')
        self.assertEqual(before,self.s)
        self.mode='interrupt'
        with self.assertRaisesRegex(RuntimeError,'interrupted'):self.complete()
        self.assertEqual(before,self.s);self.no_disclosure()
        self.mode='normal';self.complete();self.assertTrue(self.n['r13_has']('H9'))

    def test_normal_explicit_skip_return_matches_existing_completion_contract(self):
        self.ready();self.mode='explicit_skip';self.complete()
        self.assertTrue(self.n['r13_has']('H9'));self.assertTrue(self.n['r13_has']('sling_confront_completed'))
        self.assertIn('sling:letter_requester',self.s['read_topics'])
        self.assertTrue(self.s['topic_transcripts']['sling:letter_requester'])
        actual=flow.source('room13.rpy').split('label r13_lines(',1)[1].split('\nlabel ',1)[0]
        self.assertIn('and not r13_conv_skip',actual)
        self.assertTrue(actual.rstrip().endswith('$ r13_conv_skip=False\n    return'))

    def test_real_h9_legacy_never_forgets_or_duplicates(self):
        for oldkey in ('H9','know_granny_reads','sling_confession_heard'):
            with self.subTest(oldkey=oldkey):
                self.setUp();self.own('H9') if oldkey=='H9' else self.flag(oldkey)
                self.f.run_letters(self.f.CATCH,self.f.STOP)
                self.assertIn('할머니',str(self.f.lines));self.assertNotIn('이름은 말 못',str(self.f.lines))
                self.assertTrue(self.n['r13_sling_knows_requester']())
                if oldkey=='H9':
                    self.label('r13_sling_earned_confront');self.assertEqual(1,self.s['evidence'].count('H9'))
                else:
                    self.assertFalse(self.n['r13_has']('H9'));self.assertTrue(self.n['r13_sling_confront_ready']())
                    self.complete();self.assertEqual(1,self.s['evidence'].count('H9'))
                before=copy.deepcopy(self.s);self.store.room13=json.loads(json.dumps(self.s))
                self.label('r13_sling_earned_confront');self.assertEqual(before,self.s)

    def test_known_flag_boundary_preview_show_cancel_preserve_fact_without_h9(self):
        self.flag('know_granny_reads');self.own('J06')
        before=copy.deepcopy(self.s)
        self.topics();rows=self.n['r13_sling_confront_lines']();self.assertIn('전에 말씀하신',str(rows))
        self.assertEqual(before,self.s)
        shown=self.present('J06');self.assertNotIn('말 못',str(shown));self.assertFalse(self.n['r13_has']('H9'))
        self.label('r13_sling_earned_confront','지금은 더 묻지 않는다');self.assertTrue(self.n['r13_has']('know_granny_reads'))
        self.assertFalse(self.n['r13_has']('H9'));self.complete();self.assertTrue(self.n['r13_has']('H9'))

    def test_report_refusal_then_nonpaid_apology_unlocks_without_h9_cycle(self):
        self.f.run_letters(self.f.REPORT,self.f.PROCEED)
        self.own('J06');reply=self.present('J06')
        self.assertIn('경비에게',str(reply));self.assertNotIn('할머니',str(reply))
        self.assertNotIn('sling:letter_requester',self.topics());self.assertNotIn('sling:protect_confidence',self.topics())
        self.assertIn('grudge_fix:sling',self.topics());self.n['r13_topic']='grudge_fix:sling'
        self.label('r13_grudge_fix');self.assertFalse(self.n['r13_has']('H9'))
        self.assertFalse(self.n['r13_has']('letters_safe'));self.assertTrue(self.n['r13_sling_confront_ready']())
        self.complete();self.assertTrue(self.n['r13_has']('H9'));self.assertEqual(3,self.f.money())

    def test_final_memory_provider_never_resurrects_stale_expansion(self):
        self.flag('sling_hostile','rumor:fair')
        for key in ('grudge_cold:sling','grudge_fix:sling'):
            rows=self.n['r13_conversation_topic_lines'](key)
            self.assertTrue(rows);self.assertNotIn('할머니',str(rows));self.assertNotIn('시킨 사람',str(rows))
        self.label('r13_sling_grudge_reason');self.no_disclosure()
        self.assertNotIn('할머니',str(self.f.lines));self.assertFalse(self.n['r13_sling_confront_ready']())

    def test_earned_fake_followup_retains_failure_and_payoff(self):
        self.ready();self.complete();self.assertIn('sling:fake_letter',self.topics())
        self.label('r13_sling_fake_followup');self.assertTrue(self.n['r13_has']('fake_letter_planted'))
        self.s.update(day=7,period=2);self.label('r13_w1c_events','할머니를 따라간다')
        self.assertTrue(self.n['r13_has']('E17'));self.assertEqual('prevented',self.s['case_state'])
        self.setUp();self.ready();self.complete();self.flag('granny_knows_found_out')
        self.label('r13_sling_fake_followup');self.assertFalse(self.n['r13_has']('fake_letter_planted'))
        self.assertNotIn('sling:fake_letter',self.s['read_topics'])

    def test_legacy_fake_route_needs_no_new_papers_or_paid_support(self):
        self.flag('know_granny_reads');self.assertIn('sling:fake_letter',self.topics())
        self.label('r13_sling_fake_followup');self.assertTrue(self.n['r13_has']('fake_letter_planted'))
        self.assertFalse(self.n['r13_has']('H9'));self.assertEqual(3,self.f.money())

    def test_late_independent_direct_evidence_and_existing_granny_topics_unchanged(self):
        for key in ('E05','E09','E10','E13','E14','E18','E35','E36'):
            with self.subTest(key=key):
                self.setUp();self.s.update(day=8,case_state='occurred');self.own(key)
                initial=copy.deepcopy(self.s);prior=self.before_present('granny',key);priorstate=copy.deepcopy(self.s)
                self.store.room13=initial;current=self.present(key,'granny')
                self.assertEqual(prior,current);self.assertEqual(priorstate,self.s);self.assertFalse(self.n['r13_has']('H9'))
        self.setUp();self.own('H9');self.flag('know_granny_reads')
        prior=[k for k,s in self.before_topics('granny')];current=[k for k,s in self.n['r13_topics']('granny')]
        self.assertEqual(prior,current);self.assertIn('granny_letter_confront',current);self.assertIn('granny_letter_ask',current)

if __name__=='__main__':unittest.main()
