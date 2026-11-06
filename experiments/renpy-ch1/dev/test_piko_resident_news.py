"""아빠의 실제 보고와 주민별 청취를 분리하고 현재 업무·사건을 먼저 둔다."""
import copy
import json
from pathlib import Path
import textwrap
from types import SimpleNamespace
import unittest


ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/"game/room13_piko_reactions.rpy").read_text()


class PikoResidentNews(unittest.TestCase):
    def make(self, day=3, alive=False):
        room=dict(day=day,location="workshop",evidence=["V111:E09"],flags=[],
                  v111=dict(scene="MS14_D03_S03",values={"piko_alive":alive,"elapsed_minutes":30}))
        store=SimpleNamespace(room13=room,r13_meeting_active=False,r13_meeting_live_active=False,
                              r13_conv_skip_run=False)
        ready={"nabi","buri"};visible=["nabi","buri"];business=set();context=[None];writes=[]
        def value(key):return room["v111"]["values"].get(key)
        def set_value(key,val):
            writes.append((key,val));room["v111"]["values"][key]=val
        env=dict(store=store,r13_v111_active=lambda:True,r13_v111_value=value,r13_v111_set=set_value,
                 r13_v111_owned=lambda key:"V111:"+key in room["evidence"],
                 r13_v111_actor_ready=lambda person:person in ready,r13_visible_people=lambda:list(visible),
                 r13_v111_tense_context=lambda:context[0],r13_v111_has_business=lambda person:person in business,
                 r13_nw_added_line=lambda row:dict(row),r13_v111_idle_lines=lambda person:[("original",person)])
        code=SOURCE.split("init 354 python:\n",1)[1].split("\nlabel ",1)[0]
        exec(compile(textwrap.dedent(code),"피코 소식과 잔향","exec"),env)
        return env,store,ready,visible,business,context,writes

    def finish(self, env, person):
        # 라벨이 r13_lines에서 정상 반환한 뒤 실행하는 유일한 쓰기다.
        tail=SOURCE.split("label r13_piko_report(person):",1)[1]
        code=next(line.strip()[2:] for line in tail.splitlines() if line.strip().startswith("$ "))
        exec(code,dict(env,person=person))

    def test_report_requires_current_confirmed_death_and_actual_available_resident(self):
        cases=("alive","unknown_life","no_portrait","day2","day4","absent","not_ready",
               "busy","meeting","live_meeting","large_event","lamp_meeting_scene","legacy")
        for case in cases:
            with self.subTest(case=case):
                env,s,ready,visible,_,context,writes=self.make()
                if case=="alive":s.room13["v111"]["values"]["piko_alive"]=True
                if case=="unknown_life":s.room13["v111"]["values"]["piko_alive"]=None
                if case=="no_portrait":s.room13["evidence"]=[]
                if case=="day2":s.room13["day"]=2
                if case=="day4":s.room13["day"]=4
                if case=="absent":visible.remove("buri")
                if case=="not_ready":ready.remove("buri")
                if case=="busy":s.room13["v111"]["values"]["busy:buri"]="school_transport"
                if case=="meeting":s.r13_meeting_active=True
                if case=="live_meeting":s.r13_meeting_live_active=True
                if case=="large_event":context[0]="event"
                if case=="lamp_meeting_scene":s.room13["v111"]["scene"]="MS14_D03_S05"
                if case=="legacy":env["r13_v111_active"]=lambda:False
                self.assertFalse(env["r13_piko_report_due"]("buri"))
                self.assertEqual(writes,[])
        env,*_=self.make()
        self.assertTrue(env["r13_piko_report_due"]("buri"))
        self.assertFalse(env["r13_piko_report_due"]("guard"))

    def test_preview_and_line_generation_never_spread_the_news(self):
        env,s,*rest=self.make();writes=rest[-1]
        before=copy.deepcopy(s.room13)
        for person in ("nabi","buri"):
            for _ in range(3):
                self.assertTrue(env["r13_piko_report_due"](person))
                self.assertTrue(env["r13_piko_report_lines"](person))
                self.assertEqual(env["r13_piko_echo_lines"](person),[])
        self.assertEqual(s.room13,before)
        self.assertEqual(writes,[])

    def test_only_label_return_commits_one_resident_and_mid_call_save_stays_unheard(self):
        env,s,*rest=self.make();writes=rest[-1]
        tail=SOURCE.split("label r13_piko_report(person):",1)[1]
        self.assertLess(tail.index("call r13_lines("),tail.index('$ r13_v111_set("piko_news3:"'))
        before=copy.deepcopy(s.room13)
        env["r13_piko_report_lines"]("buri")
        mid_call_save=copy.deepcopy(s.room13)
        self.assertEqual(mid_call_save,before)
        self.finish(env,"buri")
        expected=copy.deepcopy(before)
        expected["v111"]["values"]["piko_news3:buri"]=True
        self.assertEqual(s.room13,expected,"그 주민의 청취 외에 자료·시간·생사·판정을 쓰지 않는다")
        self.assertFalse(env["r13_piko_report_due"]("buri"))
        self.assertTrue(env["r13_piko_report_due"]("nabi"))
        s.room13.clear();s.room13.update(mid_call_save)
        self.assertTrue(env["r13_piko_report_due"]("buri"),"도중 저장을 불러오면 대화 완료 전 상태다")
        s.r13_conv_skip_run=True
        self.finish(env,"buri")
        self.assertFalse(env["r13_piko_report_due"]("buri"),"의도적인 건너뛰기는 기존 사건처럼 전달을 완료한다")
        self.assertEqual(writes,[("piko_news3:buri",True)]*2)

    def test_heard_resident_keeps_short_echo_through_day7_without_new_writes(self):
        for person in ("nabi","buri"):
            for day in range(3,8):
                with self.subTest(person=person,day=day):
                    env,s,*_=self.make(day=day)
                    s.room13["v111"]["values"]["piko_news3:"+person]=True
                    before=copy.deepcopy(s.room13)
                    rows=env["r13_v111_idle_lines"](person)
                    self.assertEqual(len(rows),2)
                    self.assertTrue(all(row["id"].startswith("NW_PIKO_ECHO_") for row in rows))
                    self.assertEqual(s.room13,before)
                    self.assertEqual(env["r13_v111_idle_lines"](person),rows)
                    s.room13["day"]=8
                    self.assertEqual(env["r13_v111_idle_lines"](person),[("original",person)])

    def test_custody_reaction_uses_only_buris_completed_personal_hearing(self):
        ids=[]
        for decision in (None,'report','transfer'):
            env,s,_,_,business,_,writes=self.make()
            s.room13['v111']['values']['piko_news3:buri']=True
            if decision:s.room13['v111']['values']['piko_custody_heard3:buri']=decision
            before=copy.deepcopy(s.room13)
            rows=env['r13_piko_echo_lines']('buri')
            text=' '.join(r['text'] for r in rows)
            ids.append(rows[0]['id'])
            if decision=='report':self.assertIn('돌 가져간 일은 남겨',text)
            elif decision=='transfer':self.assertIn('언제 돌아오느냐고',text)
            else:self.assertNotIn('실룩',text)
            self.assertEqual(s.room13,before)
            self.assertEqual(writes,[])
            self.assertEqual(env['r13_piko_echo_lines']('nabi'),[])
            business.add('buri')
            self.assertEqual(env['r13_v111_idle_lines']('buri'),[('original','buri')])
        self.assertEqual(len(set(ids)),3)

    def test_actual_shelter_and_complete_portrait_operations_do_not_gate_custody_on_death(self):
        # 식당 보호는 등 결박과 독립이다. 기존 정본의 실제 두 commit을 적용해 생존·도난 상태를 만든다.
        records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
        for day in range(3,8):
            for decision in ('report','transfer'):
                with self.subTest(day=day,decision=decision):
                    env,s,*rest=self.make(day=day)
                    values=s.room13['v111']['values']
                    s.room13['evidence']=[]
                    for rid in ('MS14_D02_S04_L0038','MS14_D03_S01_L0039'):
                        for op in records[rid]['operations']:
                            if op['op']=='set':values[op['field']]=op['value']
                            elif op['op']=='acquire':s.room13['evidence'].append('V111:'+op['key'])
                    self.assertIs(values['piko_sheltered'],True)
                    self.assertIs(values['piko_alive'],True)
                    self.assertFalse(values.get('lamp_bound2'))
                    self.assertNotIn('piko_news3:buri',values)
                    values['piko_custody_heard3:buri']=decision
                    before=copy.deepcopy(s.room13)
                    rows=env['r13_v111_idle_lines']('buri')
                    self.assertEqual(len(rows),2)
                    self.assertTrue(all('_'+decision.upper()+'_' in r['id'] for r in rows))
                    self.assertFalse(env['r13_piko_report_due']('buri'))
                    self.assertEqual(env['r13_piko_echo_lines']('nabi'),[])
                    self.assertEqual(before,s.room13)
                    self.assertEqual(rest[-1],[])

    def test_custody_memory_describes_past_decision_not_current_custody_life_or_child_handoff(self):
        for decision in ('report','transfer'):
            for status,listed,alive in (('reporting_obligation',False,True),
                                         ('supervised_compulsory_labor',True,True),
                                         ('released',True,False)):
                with self.subTest(decision=decision,status=status,alive=alive):
                    env,s,*_=self.make(day=7,alive=True)
                    s.room13['v111']['values'].update({
                        'piko_custody_heard3:buri':decision,'silluk_status':status,
                        'listed:resident_siluk':listed,'alive:resident_siluk':alive,
                        'silluk.children.location':'workshop_with_buri'})
                    before=copy.deepcopy(s.room13)
                    rows=env['r13_piko_echo_lines']('buri')
                    text=' '.join(r['text'] for r in rows)
                    self.assertEqual(len(rows),2)
                    self.assertNotIn('내일',text)
                    self.assertNotIn('오늘',text)
                    self.assertNotIn('돌아왔',text)
                    self.assertNotIn('아이들한테 돌아가게 했',text)
                    self.assertEqual(before,s.room13)

    def test_custody_memory_needs_actual_hearing_and_yields_to_absence_business_and_events(self):
        for case in ('unheard','other_person','busy','business','event','piko_event',
                     'meeting','lamp_scene','absent','dead_or_not_ready','attempt','day2','day8'):
            with self.subTest(case=case):
                env,s,ready,visible,business,context,writes=self.make(day=6,alive=True)
                s.room13['v111']['values']['piko_custody_heard3:buri']='transfer'
                person='buri'
                if case=='unheard':s.room13['v111']['values'].pop('piko_custody_heard3:buri')
                if case=='other_person':person='nabi'
                if case=='busy':s.room13['v111']['values']['busy:buri']='family_work'
                if case=='business':business.add('buri')
                if case=='event':context[0]='event'
                if case=='piko_event':context[0]='piko'
                if case=='meeting':s.r13_meeting_active=True
                if case=='lamp_scene':s.room13['v111']['scene']='MS14_D03_S05'
                if case=='absent':visible.remove('buri')
                if case=='dead_or_not_ready':ready.remove('buri')
                if case=='attempt':s.room13['v111']['values']['lamp_bound2']=True
                if case=='day2':s.room13['day']=2
                if case=='day8':s.room13['day']=8
                before=copy.deepcopy(s.room13)
                self.assertEqual(env['r13_piko_echo_lines'](person),[])
                self.assertEqual(before,s.room13)
                self.assertEqual(writes,[])

    def test_nabi_missed_day3_can_hear_once_later_with_accurate_dates_and_no_place_assumptions(self):
        for day,when in ((4,'어제 아침'),(5,'며칠 전 아침'),(6,'며칠 전 아침'),(7,'며칠 전 아침')):
            with self.subTest(day=day):
                env,s,*rest=self.make(day=day)
                s.room13['location']='school'
                before=copy.deepcopy(s.room13)
                self.assertTrue(env['r13_piko_report_due']('nabi'))
                self.assertFalse(env['r13_piko_report_due']('buri'))
                self.assertEqual(env['r13_piko_echo_lines']('nabi'),[])
                rows=env['r13_piko_report_lines']('nabi')
                text=' '.join(r['text'] for r in rows)
                self.assertIn(when,text)
                self.assertNotIn('오늘 아침',text)
                self.assertNotIn('어제 그 화가',text)
                self.assertNotIn('그릇',text)
                self.assertNotIn('식탁',text)
                self.assertNotIn('보고 왔습니다',text)
                self.assertEqual(before,s.room13)
                self.finish(env,'nabi')
                self.assertFalse(env['r13_piko_report_due']('nabi'))
                self.assertTrue(env['r13_piko_echo_lines']('nabi'))
                expected=copy.deepcopy(before)
                expected['v111']['values']['piko_news3:nabi']=True
                self.assertEqual(expected,s.room13)
                self.assertEqual(rest[-1],[('piko_news3:nabi',True)])

    def test_late_nabi_report_waits_for_required_business_and_is_not_automatic_knowledge(self):
        for day in range(4,8):
            for case in ('alive','unknown_life','no_portrait','business','busy','absent','not_ready',
                         'event','piko_event','meeting','live_meeting','lamp_scene','already_heard'):
                with self.subTest(day=day,case=case):
                    env,s,ready,visible,business,context,writes=self.make(day=day)
                    values=s.room13['v111']['values']
                    if case=='alive':values['piko_alive']=True
                    if case=='unknown_life':values['piko_alive']=None
                    if case=='no_portrait':s.room13['evidence']=[]
                    if case=='business':business.add('nabi')
                    if case=='busy':values['busy:nabi']='witness_work'
                    if case=='absent':visible.remove('nabi')
                    if case=='not_ready':ready.remove('nabi')
                    if case=='event':context[0]='event'
                    if case=='piko_event':context[0]='piko'
                    if case=='meeting':s.r13_meeting_active=True
                    if case=='live_meeting':s.r13_meeting_live_active=True
                    if case=='lamp_scene':s.room13['v111']['scene']='MS14_D03_S05'
                    if case=='already_heard':values['piko_news3:nabi']=True
                    before=copy.deepcopy(s.room13)
                    self.assertFalse(env['r13_piko_report_due']('nabi'))
                    self.assertEqual(before,s.room13)
                    self.assertEqual(writes,[])
        for day in (2,8):
            env,*_=self.make(day=day)
            self.assertFalse(env['r13_piko_report_due']('nabi'))

    def test_existing_hub_consumes_first_report_return_before_idle_echo(self):
        # 실제 person 클릭의 같은 실행 블록을 점검한다. 첫 보고 반환 뒤의 idle은 다음 클릭까지 보류된다.
        hub=(ROOT/'game/room13_v111.rpy').read_text()
        start=hub.index('            call r13_piko_report(v111_person)')
        end=hub.index('        elif v111_person in r13_visible_people():',start)
        part=hub[start:end]
        self.assertIn('$ v111_piko_reported=bool(_return)',part)
        self.assertIn('            if not v111_piko_reported:',part)
        self.assertLess(part.index('if not v111_piko_reported:'),part.index('call r13_lines(r13_v111_idle_lines('))
        label=SOURCE.split('label r13_piko_report(person):',1)[1]
        self.assertLess(label.index('call r13_lines('),label.index('$ r13_v111_set("piko_news3:"'))
        self.assertLess(label.index('$ r13_v111_set("piko_news3:"'),label.index('return True'))

    def test_busy_resident_current_event_and_required_business_outrank_echo(self):
        for case in ("unheard","busy","business","tense","meeting","missing","alive"):
            with self.subTest(case=case):
                env,s,_,visible,business,context,_=self.make()
                s.room13["v111"]["values"]["piko_news3:buri"]=True
                if case=="unheard":s.room13["v111"]["values"].pop("piko_news3:buri")
                if case=="busy":s.room13["v111"]["values"]["busy:buri"]="family_walk"
                if case=="business":business.add("buri")
                if case=="tense":context[0]="event"
                if case=="meeting":s.r13_meeting_active=True
                if case=="missing":visible.remove("buri")
                if case=="alive":s.room13["v111"]["values"]["piko_alive"]=True
                self.assertEqual(env["r13_v111_idle_lines"]("buri"),[("original","buri")])


if __name__=="__main__":unittest.main()
