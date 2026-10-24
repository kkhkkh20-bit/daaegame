# 2026-10-24 수첩 목표 칸(소유자 "추천안대로", 시안 docs/reviews/goal-strip-20261024/).
# 단계 판정·아래 한 줄 표를 값으로 확인하고, 5일 상태와 14일 상태의 닫힘·펼침을 PC·휴대폰으로 찍는다.
init python:
    import os
    def qa_goal_log(text):
        with open(os.path.join(config.basedir,"qa_result.txt"),"a",encoding="utf-8") as out:out.write(text+"\n")
    def qa_goal_dump(tag):
        steps,current,note=r13_goal_state()
        qa_goal_log("%s: 단계 %s / 지금 %d(%s) / 한 줄 %s"%(tag," · ".join(steps),current+1,steps[current],note))
    def qa_goal_unflag(*keys):
        n=winter_copy.deepcopy(store.room13)
        n["flags"]=[k for k in n["flags"] if k not in keys]
        store.room13=n
    def qa_goal_note():
        return r13_goal_state()[2]
    def qa_goal_open():
        return renpy.get_widget("r13_records","r13_goal_card") is not None
    def qa_goal_day5():
        # 1일 입구를 지나 여관에 들고(D01_S05), 4일 밤이 대화를 지난 5일 아침. 엄마는 아직 못 만났다.
        r13_flag("v111:entered:MS14_D01_S05","v111:entered:MS14_D02_S01","v111:entered:MS14_D04_S02")
        r13_goal_mark_line("v111:room_empty:MS14_D01_S05_L0016")
        r13_goal_mark_line("v111:MS14_D04_S02_L0017")
        r13_v111_set("day",5)
        r13_edit(day=5,location="square",period=0)
    def qa_goal_day14():
        qa_drawer_day14()
        r13_flag("v111:entered:MS14_D01_S05","v111:entered:MS14_D11_S02","v111:entered:MS14_D13_S01","v111:entered:MS14_D14_S01")
        r13_v111_set("family_reunited",True)
        r13_v111_set("day",14)
        r13_edit(day=14,location="school",period=1)
    def qa_goal_legacy_ok():
        """v111 이 꺼진 판에서는 목표 칸이 나오지 않는다(서랍도 꺼져 기록 화면이 그 자리에 오지 않는다)."""
        global r13_v111_active
        real=r13_v111_active
        r13_v111_active=lambda:False
        try:
            return not r13_goal_active() and not r13_drawer_active()
        finally:
            r13_v111_active=real

testcase v111_goal_strip:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_goal_dump,"1일 입구")
    # 1일 입구 앞: 아직 ① 마을을 조사한다가 지금이고, 13호실을 보기 전이라 아래 한 줄은 없다.
    assert eval (r13_goal_state()[1]==0 and qa_goal_note() is None)
    assert eval (r13_goal_state()[0]==["마을을 조사한다","엄마를 찾는다","셋이 나간다"])
    assert eval (qa_goal_legacy_ok())
    # --- 판정 표 ---
    # 입구를 지나 여관(D01_S05)에 들면 ①을 마치고 ② 엄마를 찾는다.
    $ r13_flag("v111:entered:MS14_D01_S05")
    assert eval (r13_goal_state()[1]==1 and qa_goal_note() is None)
    # 13호실 빈방 대사(D01_S05_L0016)를 지나면 1~3일 문장.
    $ r13_goal_mark_line("v111:room_empty:MS14_D01_S05_L0016")
    assert eval (qa_goal_note()=="엄마는 여관 13호실에서 기다린다고 했다. 13호실은 비어 있었다.")
    # 4일이어도 밤이 대화 전이면 1~3일 문장이 남는다. 다른 줄(L0018)로는 표식이 서지 않는다.
    $ r13_v111_set("day",4)
    $ r13_goal_mark_line("v111:MS14_D04_S02_L0018")
    assert eval (qa_goal_note()=="엄마는 여관 13호실에서 기다린다고 했다. 13호실은 비어 있었다.")
    $ r13_goal_mark_line("v111:MS14_D04_S02_L0017")
    assert eval (qa_goal_note()=="밤이가 강 쪽에서 엄마를 봤다고 했다.")
    # 옛 저장: 줄 표식이 없어도 그 줄 뒤 장면(D04_S03)에 들어갔으면 지난 것으로 친다.
    $ qa_goal_unflag("v111:line:MS14_D04_S02_L0017","v111:line:MS14_D01_S05_L0016")
    assert eval (qa_goal_note() is None)
    $ r13_flag("v111:entered:MS14_D04_S03")
    assert eval (qa_goal_note()=="밤이가 강 쪽에서 엄마를 봤다고 했다.")
    # 11일: 고개 대사(D11_S00_L0002) 전에는 앞 문장, 지나면 11~12일 문장. 엄마를 만나기 전에는 ②가 지금.
    $ r13_v111_set("day",11)
    $ r13_flag("v111:entered:MS14_D11_S00")
    assert eval (qa_goal_note()=="밤이가 강 쪽에서 엄마를 봤다고 했다." and r13_goal_state()[1]==1)
    $ r13_goal_mark_line("v111:MS14_D11_S00_L0002")
    assert eval (qa_goal_note()=="바깥 고개가 막혔다. 걸어서도 못 나간다.")
    # 엄마를 만나면(family_reunited) ②가 「엄마를 지킨다」로 바뀌고 ③ 셋이 나간다가 지금.
    $ r13_v111_set("family_reunited",True)
    assert eval (r13_goal_state()[0][1]=="엄마를 지킨다" and r13_goal_state()[1]==2)
    # 13일 장면에 들면 13~14일 문장.
    $ r13_v111_set("day",13)
    $ r13_flag("v111:entered:MS14_D13_S01")
    assert eval (qa_goal_note()=="명단에 오른 사람은 수레에 실려 간다. 셋이 함께 남아야 한다.")
    # 옛 저장(값이 없는 판): family_reunited 가 없으면 엄마를 찾는 중으로 본다.
    $ qa_goal_saved=winter_copy.deepcopy(room13)
    $ room13["v111"]["values"].pop("family_reunited",None)
    assert eval (r13_goal_state()[1]==1 and r13_goal_state()[0][1]=="엄마를 찾는다")
    $ room13=qa_goal_saved
    # 판정 표를 본 값들을 지우고 5일 상태로 다시 세운다.
    $ qa_goal_unflag(*[k for k in room13["flags"] if k.startswith("v111:line:") or k in ("v111:entered:MS14_D04_S03","v111:entered:MS14_D11_S00","v111:entered:MS14_D13_S01")])
    $ r13_v111_set("family_reunited",None)
    # --- 5일 상태 ---
    run Function(qa_goal_day5)
    run Function(qa_goal_dump,"5일")
    assert eval (r13_goal_state()[1]==1 and qa_goal_note()=="밤이가 강 쪽에서 엄마를 봤다고 했다.")
    $ r13_touch_ui=lambda: False
    $ r13_records_view={"tab":"all","detail":None,"page":0,"drawer":"now"}
    run Show("r13_records")
    pause 1.2
    assert eval (not qa_goal_open())
    screenshot "goal-01-day5-closed-pc.png"
    click id "r13_goal_pill"
    pause 0.6
    assert eval (qa_goal_open())
    screenshot "goal-02-day5-open-pc.png"
    # 다시 누르면 닫힌다.
    click id "r13_goal_pill"
    pause 0.5
    assert eval (not qa_goal_open())
    run Hide("r13_records")
    pause 0.4
    # --- 14일 상태 ---
    run Function(qa_goal_day14)
    run Function(qa_goal_dump,"14일")
    assert eval (r13_goal_state()==(["마을을 조사한다","엄마를 지킨다","셋이 나간다"],2,"명단에 오른 사람은 수레에 실려 간다. 셋이 함께 남아야 한다."))
    $ r13_records_view={"tab":"all","detail":"V111:NW_BURNT_PAGE","page":0,"drawer":"now"}
    run Show("r13_records")
    pause 1.2
    screenshot "goal-03-day14-closed-pc.png"
    click id "r13_goal_pill"
    pause 0.6
    assert eval (qa_goal_open())
    screenshot "goal-04-day14-open-pc.png"
    # 바깥을 누르면 닫힌다(판 밖, 자료 그림 위).
    click pos (520,420)
    pause 0.5
    assert eval (not qa_goal_open())
    run Hide("r13_records")
    pause 0.4
    # --- 휴대폰 ---
    $ r13_touch_ui=lambda: True
    $ r13_records_view={"tab":"all","detail":"V111:NW_BURNT_PAGE","page":0,"drawer":"now"}
    run Show("r13_records")
    pause 1.2
    screenshot "goal-05-day14-closed-touch.png"
    click id "r13_goal_pill"
    pause 0.6
    assert eval (qa_goal_open())
    screenshot "goal-06-day14-open-touch.png"
    click id "r13_goal_pill"
    pause 0.5
    run Hide("r13_records")
    pause 0.4
    # 휴대폰 5일(엄마를 찾는다 — 가장 긴 이름)
    $ r13_v111_set("family_reunited",None)
    $ qa_goal_unflag("v111:entered:MS14_D13_S01","v111:entered:MS14_D14_S01","v111:entered:MS14_D11_S02")
    $ r13_v111_set("day",5)
    $ r13_edit(day=5,location="square",period=0)
    run Function(qa_goal_dump,"휴대폰 5일")
    run Show("r13_records")
    pause 1.2
    click id "r13_goal_pill"
    pause 0.6
    screenshot "goal-07-day5-open-touch.png"
    run Hide("r13_records")
    pause 0.4
