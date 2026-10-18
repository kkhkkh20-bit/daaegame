"""Engine-free contracts for the isolated Piko patch; not a Ren'Py playthrough."""
import ast
import copy
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'game/systems/room13_piko_causality.rpy'
LAMP = ROOT / 'game/systems/room13_ep1_lamp_thief.rpy'
RULES = ROOT / 'game/room13_rules.rpy'

def init_body(path):
    source = path.read_text()
    return textwrap.dedent(source.split('init 205 python:\n', 1)[1].split('\nlabel ', 1)[0])

def load_finish_topic(env):
    lines=RULES.read_text().splitlines()
    start=next(i for i,l in enumerate(lines) if l.startswith('    def r13_finish_topic('))
    end=next(i for i in range(start+1,len(lines)) if lines[i].startswith('    def '))
    exec(compile(textwrap.dedent('\n'.join(lines[start:end])), str(RULES), 'exec'),env)

class PikoContracts(unittest.TestCase):
    def setUp(self):
        self.store=SimpleNamespace(room13=dict(day=3,period=0,location='square',flags=['lt_dawn','piko_dead'],evidence=['L00','L06'],read_topics=[],topic_transcripts={},dialogue_dates={}),r13_meeting_active=False,r13_topic_shown=None)
        self.topics={key:dict(npc='resident_lamplighter',title='old '+key,give=[],flags=[]) for key in ('lamplighter_guarded','smalltalk:lamplighter_check')}
        self.notes=[dict(title='3번 등에서 무슨 일이 있었을까?',hint='회의는 4일 오전부터 오후까지 광장에서 열린다.',fact='피코가 쓰러졌다.'),dict(title='다른 메모',hint='그대로')]
        self.e={'store':self.store,'ROOM13':{'topics':self.topics},'R13_NAMES':{'resident_lamplighter':'초롱'},'winter_copy':copy,
            'R13_MEETING_CLOCK':[('Q1','lt_dawn','lt_done',(4,1),'광장 회의',None),('Q3','wf_fire','wf_done',(7,1),'학교 회의',(6,2,'학교'))],
            'r13_has':lambda f:f in self.store.room13.get('flags',[]) or f in self.store.room13.get('evidence',[]),
            'r13_q1_notes':lambda:self.notes,
            'r13_topic_current_context':lambda k:'doto-front-door-known' if k=='doto_corridor' else None,
            'r13_topic_current_lines':lambda k:[('baseline',k)],
            'r13_calendar_topic_seen':lambda k,s:'baseline-seen',
            'r13_topics':lambda p:list(self.topics.items()),
            'r13_calendar_key':lambda p:'test-context',
            'r13_grant':lambda *args:None,
            'r13_flag':lambda *flags:self.store.room13['flags'].extend(f for f in flags if f not in self.store.room13['flags'])}
        exec(compile(init_body(MODULE),str(MODULE),'exec'),self.e)
        self.e['r13_topic_current_fresh']=lambda k:self.store.room13.get('current_topic_contexts',{}).get(k)!=self.e['r13_topic_current_context'](k)
        load_finish_topic(self.e)
    def call(self,name,*args):return self.e[name](*args)
    def hastext(self,rows):return '\n'.join(r[1] for r in rows)
    def test_notice_window_and_terminal_states(self):
        for day,period,expected in [(2,2,False),(3,0,True),(3,3,True),(4,0,True),(4,1,True),(4,2,False),(5,0,False)]:
            self.store.room13.update(day=day,period=period)
            self.assertEqual(self.call('r13_piko_notice_due'),expected,(day,period))
        self.store.room13.update(day=3,period=0)
        for flag in ('lt_done','lt_q1_notice'):
            self.store.room13['flags'].append(flag)
            self.assertFalse(self.call('r13_piko_notice_due'))
            self.store.room13['flags'].remove(flag)
        self.store.room13['flags'].remove('lt_dawn')
        self.assertFalse(self.call('r13_piko_notice_due'))
    def test_notice_only_here_and_not_mid_meeting(self):
        self.assertTrue(self.call('r13_piko_notice_here'))
        self.store.room13['location']='workshop';self.assertFalse(self.call('r13_piko_notice_here'))
        self.store.room13['location']='square';self.store.r13_meeting_active=True
        self.assertFalse(self.call('r13_piko_notice_here'))
    def test_display_queries_never_mutate_save(self):
        before=copy.deepcopy(self.store.room13)
        for _ in range(3):
            self.call('r13_piko_notice_due');self.call('r13_piko_notice_lines',True);self.call('r13_q1_notes')
            self.call('r13_topics','resident_lamplighter');self.call('r13_topic_current_lines','lamplighter_guarded')
        self.assertEqual(self.store.room13,before)
    def test_notice_idempotency_after_completion(self):
        self.assertTrue(self.call('r13_piko_notice_here'))
        self.e['r13_flag']('lt_q1_notice')
        self.assertFalse(self.call('r13_piko_notice_here'))
        self.assertEqual(self.store.room13['flags'].count('lt_q1_notice'),1)
    def test_recovery_uses_today_not_tomorrow_on_day_four(self):
        self.store.room13['day']=4
        text=self.hastext(self.call('r13_piko_notice_lines',True))
        self.assertIn('오늘 아침부터 오후까지',text);self.assertNotIn('내일',text)
        self.assertNotIn('옮겼다',text);self.assertNotIn('돌아가셨어',text)
    def test_l13_alone_proves_prior_meeting(self):
        self.store.room13['evidence']=['L12']
        self.assertNotIn('본 적이 있다',self.call('r13_piko_mother_purpose'))
        self.assertIn('있을까',self.call('r13_piko_mother_purpose'))
        self.store.room13['evidence'].append('L13')
        self.assertIn('본 적이 있다',self.call('r13_piko_mother_purpose'))
    def test_alive_notice_has_no_death_or_funeral(self):
        self.store.room13['flags']=['lt_dawn','piko_survived']
        text=self.hastext(self.call('r13_piko_notice_lines'))
        for word in ('돌아가셨','죽었','장례','시체','범인은','탐정님'):
            self.assertNotIn(word,text)
    def test_clock_gates_q1_only(self):
        self.assertEqual(self.e['R13_MEETING_CLOCK'][0][1],'lt_q1_notice')
        self.assertEqual(self.e['R13_MEETING_CLOCK'][0][3],(4,1))
        self.assertEqual(self.e['R13_MEETING_CLOCK'][1][1],'wf_fire')
    def test_notes_hide_unheard_notice_without_mutating_base(self):
        original=copy.deepcopy(self.notes)
        rows=self.call('r13_q1_notes')
        self.assertNotIn('회의',rows[0]['hint']);self.assertEqual(self.notes,original)
        self.e['r13_flag']('lt_q1_notice');self.assertEqual(self.call('r13_q1_notes'),original)
    def test_existing_doto_context_and_unrelated_lines_preserved(self):
        self.assertEqual(self.call('r13_topic_current_context','doto_corridor'),'doto-front-door-known')
        self.assertEqual(self.call('r13_topic_current_lines','doto_corridor'),[('baseline','doto_corridor')])
        self.assertEqual(self.call('r13_calendar_topic_seen','doto_corridor',{}),'baseline-seen')
    def test_post_dawn_context_does_not_leak_before_discovery(self):
        self.store.room13['flags']=[]
        self.assertIsNone(self.call('r13_topic_current_context','lamplighter_guarded'))
        self.assertEqual(self.call('r13_topic_current_lines','lamplighter_guarded'),[('baseline','lamplighter_guarded')])
    def test_new_knowledge_opens_one_new_context(self):
        key='smalltalk:lamplighter_check'
        first=self.call('r13_topic_current_context',key)
        self.store.room13['current_topic_contexts']={key:first}
        self.assertTrue(self.call('r13_calendar_topic_seen',key,{}))
        self.store.room13['evidence'].append('L15')
        self.assertNotEqual(first,self.call('r13_topic_current_context',key))
        self.assertFalse(self.call('r13_calendar_topic_seen',key,{}))
    def test_unseen_reversal_is_not_leaked(self):
        text=self.hastext(self.call('r13_topic_current_lines','smalltalk:lamplighter_check'))
        self.assertIn('미지근',text)
        self.assertNotIn('조각은 안에',text);self.assertNotIn('동튼 뒤',text)
        self.assertNotIn('한 바퀴만',text);self.assertNotIn('꺼진 등이라도',text)
    def test_followup_is_location_neutral_not_fake_current_lamp_repair(self):
        for place in ('square','workshop','gate'):
            self.store.room13['location']=place
            text=self.hastext(self.call('r13_topic_current_lines','lamplighter_guarded'))
            self.assertIn('3번 등',text);self.assertNotIn('연결선',text);self.assertNotIn('떨어져서',text)
    def test_titles_change_without_changing_topic_records(self):
        original=copy.deepcopy(self.topics)
        rows=self.call('r13_topics','resident_lamplighter')
        self.assertIn('3번 등',rows[0][1]['title']);self.assertEqual(self.topics,original)
    def test_finish_followup_preserves_first_transcript_and_date(self):
        key='smalltalk:lamplighter_check'
        s=self.store.room13;s['read_topics']=[key]
        s['topic_transcripts'][key]=[['resident_lamplighter','old exact testimony',False]]
        s['dialogue_dates'][key]={'day':1,'period':2}
        old=copy.deepcopy((s['topic_transcripts'],s['dialogue_dates']))
        self.store.r13_topic_shown=self.call('r13_topic_current_lines',key)
        self.call('r13_finish_topic',key)
        self.assertEqual((self.store.room13['topic_transcripts'],self.store.room13['dialogue_dates']),old)
        self.assertIn(key,self.store.room13['current_topic_contexts'])
        self.assertEqual(len(self.call('r13_topic_current_lines',key)),1)
    def test_old_one_round_claim_is_acknowledged_only_when_recorded(self):
        key='smalltalk:lamplighter_check'
        self.store.room13['topic_transcripts'][key]=[['resident_lamplighter','네. 해 지고 한 바퀴만 돌아요. 그다음엔 집에 가서 자요.',False]]
        text=self.hastext(self.call('r13_topic_current_lines',key))
        self.assertIn('전에 해 지고 한 바퀴만',text)
        self.assertIn('그날은 새벽에도',text)
        self.store.room13['topic_transcripts']={}
        self.assertNotIn('전에 해 지고 한 바퀴만',self.hastext(self.call('r13_topic_current_lines',key)))
    def test_unread_topic_archives_first_current_lines_once(self):
        key='lamplighter_guarded';rows=self.call('r13_topic_current_lines',key)
        self.store.r13_topic_shown=rows;self.call('r13_finish_topic',key)
        saved=copy.deepcopy(self.store.room13['topic_transcripts'][key])
        self.assertEqual(saved[0][1],rows[0][1])
        self.store.room13['evidence'].append('L16')
        self.store.r13_topic_shown=self.call('r13_topic_current_lines',key);self.call('r13_finish_topic',key)
        self.assertEqual(self.store.room13['topic_transcripts'][key],saved)
    def test_patch_keeps_branch_grants_and_optional_funeral_condition(self):
        source=LAMP.read_text()
        self.assertIn('if r13_has("piko_sheltered"):',source)
        self.assertIn('r13_flag("piko_survived")',source);self.assertIn('r13_flag("piko_dead")',source)
        self.assertEqual(source.count('r13_grant(["L13"]'),1)
        self.assertIn('if _e1d==3 and _e1p==2 and _e1loc=="square" and r13_has("piko_dead") and not r13_has("lt_funeral"):',source)
        self.assertNotIn('lt_funeral_pending',source)
    def test_notice_precedes_both_checkpoints(self):
        source=LAMP.read_text()
        dawn=source.split('label r13_ep1_dawn:',1)[1].split('label r13_ep1_accused:',1)[0]
        self.assertLess(dawn.index('call r13_piko_notice'),dawn.index('r13_q1_checkpoint("investigation")'))
        meeting=source.split('label r13_ep1_meeting:',1)[1]
        self.assertLess(meeting.index('call r13_piko_notice'),meeting.index('r13_q1_checkpoint("meeting")'))
    def test_no_phantom_asset_or_incorrect_canonical_address(self):
        self.assertNotIn('"cut"',MODULE.read_text())
        self.assertNotIn('"cut"',LAMP.read_text().split('label r13_ep1_dawn:',1)[1].split('label r13_ep1_accused:',1)[0])
        self.assertNotIn('아저씨',LAMP.read_text())
    def test_new_module_has_no_reward_time_or_archive_write(self):
        tree=ast.parse(init_body(MODULE))
        calls={n.func.id for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
        self.assertFalse(calls & {'r13_grant','r13_tick','r13_cash','r13_edit','r13_flag'})
        assignments=[ast.unparse(target) for node in ast.walk(tree) if isinstance(node,ast.Assign) for target in node.targets]
        self.assertFalse(any('topic_transcripts' in target for target in assignments))
    def test_label_commits_notice_only_after_lines(self):
        label=MODULE.read_text().split('label r13_piko_notice',1)[1]
        self.assertLess(label.index('if not r13_piko_notice_here'),label.index('call r13_lines'))
        self.assertLess(label.index('call r13_lines'),label.index('r13_flag("lt_q1_notice")'))

if __name__=='__main__':unittest.main(verbosity=2)
