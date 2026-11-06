"""아빠의 실제 보고와 주민별 청취를 분리하고 현재 업무·사건을 먼저 둔다."""
import copy
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

    def test_heard_resident_keeps_short_echo_on_day3_and_day4_without_new_writes(self):
        for person in ("nabi","buri"):
            for day in (3,4):
                with self.subTest(person=person,day=day):
                    env,s,*_=self.make(day=day)
                    s.room13["v111"]["values"]["piko_news3:"+person]=True
                    before=copy.deepcopy(s.room13)
                    rows=env["r13_v111_idle_lines"](person)
                    self.assertEqual(len(rows),2)
                    self.assertTrue(all(row["id"].startswith("NW_PIKO_ECHO_") for row in rows))
                    self.assertEqual(s.room13,before)
                    self.assertEqual(env["r13_v111_idle_lines"](person),rows)
                    s.room13["day"]=5
                    self.assertEqual(env["r13_v111_idle_lines"](person),[("original",person)])

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
