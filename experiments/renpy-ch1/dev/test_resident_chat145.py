"""일반 주민의 기존 일상 대화만 현재 본편에 연결하고 옛 사건 효과는 실행하지 않는다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_v111_resident_talk.rpy'


def assignment(filename,name):
    source=(ROOT/'game'/filename).read_text().split(' python:\n',1)[1]
    # 선언 상수는 뒤의 라벨 문법을 파싱하기 전에 읽는다.
    source=source.split('\nlabel ',1)[0].split('\ninit ',1)[0]
    tree=ast.parse(textwrap.dedent(source))
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    return ast.literal_eval(node.value)


def environment(person='resident_seol',day=2):
    topics=json.loads((ROOT/'game/room13-content.json').read_text())['topics']
    wording=assignment('room13_conversations.rpy','R13_LIFE_QUESTION_WORDING')
    for who in ('resident_seol','resident_yeoni'):
        for suffix,title in zip(('work','after','crisis'),wording[who]):topics['life:'+who+':'+suffix]['title']=title
    rows=assignment('room13_conversations.rpy','R13_EARLY_CONVERSATIONS')
    _,who,title,lines,read_after=next(row for row in rows if row[0]=='yeoni_seam')
    topics['smalltalk:yeoni_seam']=dict(npc=who,title=title,lines=[('dad',title)]+lines,day=[1,4],need=[],give=[],flags=[],cost=0,read_after=[])
    # 실제 구 토픽 등록 호출의 인자를 읽는다.
    source=(ROOT/'game/systems/room13_new_cast.rpy').read_text().split('init 145 python:\n',1)[1].split('\nlabel ',1)[0].split('\ninit ',1)[0]
    tree=ast.parse(textwrap.dedent(source))
    call=next(n.value for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
              and isinstance(n.value.func,ast.Name) and n.value.func.id=='_r13_nc_topic' and n.value.args[0].value=='hyeoni:song')
    args=[ast.literal_eval(a) for a in call.args];kwargs={k.arg:ast.literal_eval(k.value) for k in call.keywords}
    topics[args[0]]=dict(npc=args[1],title=args[2],lines=args[3],day=list(kwargs['day']),need=[],give=[],flags=[],not_flags=[])
    state=SimpleNamespace(room13=dict(day=day,period=0,location='square',evidence=[],flags=[],
                                    v111=dict(gate='registered_menu',values={})))
    values=state.room13['v111']['values'];old_calls=[]
    env=dict(store=state,ROOM13=dict(topics=topics),MS14_SPEAKERS={},winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
             r13_v111_active=lambda:True,r13_v111_value=lambda k:values.get(k),
             r13_v111_set=lambda k,v:values.__setitem__(k,v),r13_v111_tense_context=lambda:None,
             r13_v111_person_alive=lambda p:True,r13_v111_actor_ready=lambda p:True,
             r13_visible_people=lambda:[person],r13_v111_binding=lambda:dict(options=[]),
             Return=lambda value:SimpleNamespace(value=value),
             r13_hyeoni_verses=lambda:old_calls.append('song') or ['old story-dependent verse'],
             r13_v111_questions=lambda p:old_calls.append(('questions',p)) or [],
             r13_v111_has_business=lambda p:old_calls.append(('business',p)) or False)
    block=SOURCE.read_text().split('init 358 python:\n',1)[1].split('\nlabel ',1)[0]
    exec(textwrap.dedent(block),env)
    return env,state,old_calls


class ResidentChat145(unittest.TestCase):
    def test_unverified_later_owl_claim_never_opens_as_daily_chat(self):
        env,state,calls=environment('resident_owlgp',5)
        self.assertEqual(env['r13_v111_resident_topics']('resident_owlgp'),[])
        self.assertNotIn('life:resident_owlgp:after',env['R13_V111_RESIDENT_TOPICS'])

    def test_three_residents_offer_existing_own_dialogue_instead_of_dads_idle_thought(self):
        for person,key in (('resident_seol','life:resident_seol:work'),('resident_yeoni','smalltalk:yeoni_seam'),('resident_hyeoni','hyeoni:song'),('resident_badook','life:resident_badook:work'),('resident_owlgp','life:resident_owlgp:work')):
            with self.subTest(person=person):
                env,state,_=environment(person)
                before=copy.deepcopy(state.room13);source=copy.deepcopy(env['ROOM13']['topics'])
                rows=env['r13_v111_questions'](person)
                self.assertEqual(len(rows),1)
                self.assertEqual(rows[0][1].value,('resident_chat',key))
                self.assertFalse(rows[0][2])
                self.assertTrue(env['r13_v111_has_business'](person))
                self.assertEqual(state.room13,before)
                self.assertEqual(env['ROOM13']['topics'],source)
                if key!='hyeoni:song':
                    packets=env['r13_v111_resident_chat_lines'](key)
                    self.assertIn(person,[p[0] for p in packets])
                    self.assertTrue(all(p[0] in ('dad',person,None) for p in packets))
                    self.assertEqual(packets,env['ROOM13']['topics'][key]['lines'])

    def test_read_marks_reopen_and_serialize_without_story_effects(self):
        env,state,_=environment('resident_yeoni');key='smalltalk:yeoni_seam'
        before=copy.deepcopy(state.room13)
        env['r13_v111_resident_chat_read'](key)
        rows=env['r13_v111_questions']('resident_yeoni')
        self.assertTrue(rows[0][2]);self.assertTrue(env['r13_v111_has_business']('resident_yeoni'))
        self.assertEqual(state.room13['evidence'],before['evidence']);self.assertEqual(state.room13['flags'],before['flags'])
        self.assertEqual(set(state.room13['v111']['values']),{'resident_chat_read:'+key})
        self.assertEqual(json.loads(json.dumps(state.room13)),state.room13)
        after=copy.deepcopy(state.room13)
        env['r13_v111_resident_chat_lines'](key);env['r13_v111_resident_chat_read'](key)
        self.assertEqual(state.room13,after)
        packets=env['r13_v111_resident_chat_lines'](key)
        original_first=copy.deepcopy(env['ROOM13']['topics'][key]['lines'][0])
        packets[0]=('dad','tamper')
        self.assertEqual(env['ROOM13']['topics'][key]['lines'][0],original_first)

    def test_first_four_days_and_later_three_days_use_their_own_existing_topics(self):
        for person in ('resident_seol','resident_yeoni'):
            for day in (1,4,5,7,8,14):
                env,_,_=environment(person,day)
                rows=env['r13_v111_resident_topics'](person)
                if day>=8:self.assertEqual(rows,[])
                else:
                    self.assertEqual(len(rows),1)
                    self.assertEqual(rows[0]['key'].split(':')[-1],'after' if day>=5 else 'work' if person=='resident_seol' else 'yeoni_seam')
        env,_,_=environment('resident_hyeoni',1)
        self.assertEqual(env['r13_v111_resident_topics']('resident_hyeoni'),[])

    def test_current_physical_presence_and_crisis_guards_are_rechecked_at_execution(self):
        for negative in ('inactive','travel','fire','tense','meeting','live_meeting','cut','aftermath','ending','dead','departed','busy','absent','not_visible','story_question'):
            with self.subTest(negative=negative):
                env,state,_=environment();key='life:resident_seol:work'
                if negative=='inactive':env['r13_v111_active']=lambda:False
                if negative=='travel':state.room13['v111']['gate']='travel'
                if negative=='fire':state.room13['location']='v111_fire'
                if negative=='tense':env['r13_v111_tense_context']=lambda:'piko'
                if negative in ('meeting','live_meeting','cut','aftermath','ending'):
                    setattr(state,dict(meeting='r13_meeting_active',live_meeting='r13_meeting_live_active',cut='r13_cg_active',aftermath='r13_aftermath_active',ending='r13_ending_story_active')[negative],True)
                if negative=='dead':env['r13_v111_person_alive']=lambda p:False
                if negative=='departed':state.room13['v111']['values']['departed:resident_seol']=True
                if negative=='busy':state.room13['v111']['values']['busy:resident_seol']='medical_call'
                if negative=='absent':env['r13_v111_actor_ready']=lambda p:False
                if negative=='not_visible':env['r13_visible_people']=lambda:[]
                if negative=='story_question':env['r13_v111_binding']=lambda:dict(options=[dict(person='resident_seol',location='square')])
                before=copy.deepcopy(state.room13)
                self.assertEqual(env['r13_v111_resident_topics']('resident_seol'),[])
                self.assertEqual(env['r13_v111_resident_chat_lines'](key),[])
                env['r13_v111_resident_chat_read'](key)
                self.assertEqual(state.room13,before)

    def test_nonwhitelisted_and_mutated_legacy_quests_never_become_side_topics(self):
        for field,value in (('give',['E35']),('flags',['old-story']),('need',['old-story']),('read_after',['old-read']),('special','old-label'),('cost',1)):
            env,state,_=environment();key='life:resident_seol:work'
            env['ROOM13']['topics'][key][field]=value
            before=copy.deepcopy(state.room13)
            self.assertEqual(env['r13_v111_resident_topics']('resident_seol'),[])
            self.assertEqual(env['r13_v111_resident_chat_lines'](key),[])
            self.assertEqual(state.room13,before)
        env,_,_=environment('resident_yeoni')
        for key in ('yeoni_goods','smalltalk:seol_rope','life:resident_seol:crisis','not-a-topic'):
            self.assertIsNone(env['r13_v111_resident_chat_spec'](key))

    def test_singer_uses_only_existing_weather_verse_and_keeps_legacy_delegate(self):
        env,state,calls=environment('resident_hyeoni')
        state.room13['flags']=['mom_hideout_found','ev_e_done','tools_sold','ep3_bell_seen']
        state.room13['case_state']='occurred'
        before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_hyeoni_verses'](),[env['R13_V111_RESIDENT_WINTER_VERSE']])
        self.assertIn(env['R13_V111_RESIDENT_WINTER_VERSE'],(ROOT/'game/systems/room13_new_cast.rpy').read_text())
        self.assertEqual(calls,[]);self.assertEqual(state.room13,before)
        env['r13_v111_active']=lambda:False
        self.assertEqual(env['r13_hyeoni_verses'](),['old story-dependent verse']);self.assertEqual(calls,['song'])

    def test_inactive_wrappers_preserve_the_existing_alias_chain(self):
        env,_,_=environment()
        action=SimpleNamespace(value='old-action');old_rows=[('old-question',action,True)]
        env['_r13_resident_questions']=lambda p:list(old_rows)
        env['_r13_resident_business']=lambda p:True
        env['r13_v111_active']=lambda:False
        self.assertEqual(env['r13_v111_questions']('resident_seol'),old_rows)
        self.assertTrue(env['r13_v111_has_business']('resident_seol'))
        self.assertEqual(env['r13_v111_resident_topics']('resident_seol'),[])

    def test_confirmed_speaker_names_and_reused_legacy_identities_are_explicit(self):
        env,_,_=environment()
        self.assertEqual(env['MS14_SPEAKERS'],{'설이':'resident_seol','현이':'resident_hyeoni','여니':'resident_yeoni'})
        source=SOURCE.read_text()
        self.assertIn('call r13_hyeoni_song',source)
        self.assertIn('r13_v111_resident_chat_lines(key),"topic:"+key',source)
        self.assertNotIn('r13_finish_topic(',source)
        self.assertNotIn('r13_tick(',source)
        self.assertNotIn('r13_grant(',source)


if __name__=='__main__':unittest.main()
