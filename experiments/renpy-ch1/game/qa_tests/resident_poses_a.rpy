# 주민 생활 동작 A안 교체 확인 (2026-10-24). 일하는 자리에서 새 그림이 기존 발 자리·크기로 서는지 캡처한다.
# 장면 조건은 기존 시험(map_actions 등)과 같은 깃발을 쓴다. 이야기 상태는 바꾸지 않는다.
init 999 python:
    R13_QA_POSES_A_FLAGS=("+w1c","ev_l_done","ev_g_done","ev_i_done","+offers","ep1_patrol_seen","ep1_eaves_seen","ev_a_done","lodging","entry_corrected")

    def r13_qa_poses_a_on_stage():
        return [(a["person"],a["pose"]) for a in r13_stage_people() if (r13_acting_spec(a["person"],a["pose"]) or {}).get("resident_pose_a")]

    def r13_qa_poses_a_focus():
        # 새 그림 인물이 화면 가운데 오도록 카메라를 옮긴다. 인물이 없으면 그대로 둔다.
        loc=store.room13["location"];actors=[a for a in r13_stage_people() if (r13_acting_spec(a["person"],a["pose"]) or {}).get("resident_pose_a")]
        if actors and r13_world_width()>1280:
            cx=sum(a["x"]+a["width"]/2.0 for a in actors)/len(actors)
            store.r13_world_cameras[loc]=int(max(0,min(r13_world_width()-1280,cx-640)))
        renpy.restart_interaction()

    def r13_qa_poses_a_report(tag):
        found=r13_qa_poses_a_on_stage()
        hits=[]
        for a in r13_stage_people():
            if (a["person"],a["pose"]) in found:
                hits.append("%s:%s rect=%s" % (a["person"],a["pose"],a["rect"]))
        r13_qa_note("poses_a %s day=%s period=%s loc=%s -> %s" % (tag,store.room13["day"],store.room13["period"],store.room13["location"],"; ".join(hits) or "없음"))
        return found

    def r13_qa_poses_a_changed():
        return len(R13_RESIDENT_POSES_A_CHANGED)

screen r13_qa_poses_a_meeting():
    # 식당 원탁 넓은 장면과 같은 그리기(높이 230, 비율 유지, nearest)로 착석 그림 일곱을 나란히 둔다.
    add r13_meeting_plate("trial",False)
    $ seated=list(R13_MEETING_SEATED)
    for i,who in enumerate(seated):
        $ cx,edge=r13_meeting_seat_position(i,len(seated),"trial")
        add Transform(r13_meeting_actor(who,None,cx,seated=True),ysize=230,fit="contain",nearest=True) xcenter cx ypos edge+95-230

testcase resident_poses_a:
    pause 2.0
    click "처음부터"
    pause 3.0
    assert eval (r13_qa_poses_a_changed()>=40)
    run Call("r13_qa_roam",dict(day=2,period=0,location="market",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("market_morning")
    screenshot "poses_a_market_morning.png"
    run Call("r13_qa_roam",dict(day=2,period=0,location="workshop",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("workshop_morning")
    screenshot "poses_a_workshop_morning.png"
    run Call("r13_qa_roam",dict(day=2,period=0,location="kitchen",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("kitchen_morning")
    screenshot "poses_a_kitchen_morning.png"
    run Call("r13_qa_roam",dict(day=2,period=0,location="gate",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("gate_morning")
    screenshot "poses_a_gate_morning.png"
    run Call("r13_qa_roam",dict(day=3,period=1,location="inn",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("inn_afternoon")
    screenshot "poses_a_inn_afternoon.png"
    run Call("r13_qa_roam",dict(day=7,period=0,location="post",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("post_morning_d7")
    screenshot "poses_a_post_morning.png"
    run Call("r13_qa_roam",dict(day=3,period=2,location="square",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("square_evening")
    screenshot "poses_a_square_evening.png"
    run Call("r13_qa_roam",dict(day=2,period=1,location="river",life_poc=True),R13_QA_POSES_A_FLAGS,(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_poses_a_focus()
    pause 1.2
    $ r13_qa_poses_a_report("river_afternoon")
    screenshot "poses_a_river_afternoon.png"
    run Show("r13_qa_poses_a_meeting")
    pause 1.0
    screenshot "poses_a_meeting_seats.png"
    run Hide("r13_qa_poses_a_meeting")
    $ r13_qa_note("poses_a done changed=%d" % r13_qa_poses_a_changed())

testcase resident_poses_a_kids:
    run Jump('r13_qa_life_school')
    pause 1.0
    $ r13_qa_poses_a_report("school_play")
    screenshot "poses_a_school_play.png"
