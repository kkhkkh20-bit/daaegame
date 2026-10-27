# 임시 화면 시험(공개 전 삭제): 생활 동작 도트 배치 확인용. 2026-10-27.
init python:
    def qa_life_dump(path):
        # 배치표가 다루는 장소·날짜·시간대마다 r13_stage_people 결과(인물·자세·자리)를 적는다.
        import json,os
        saved=winter_copy.deepcopy(store.room13)
        out={}
        for loc in ("gate","square","inn","dining","school","workshop","clinic","store","post","market","river","forest"):
            for d in (1,2,3,4,5,7,9,10,12,14):
                for q in range(3):
                    n=winter_copy.deepcopy(saved)
                    n.update(day=d,period=q,location=loc,case_state="occurred" if d>=5 else "pending",week2_started=d>=8,granny_state="trusted",victim_state="alive" if d<5 else "dead")
                    store.room13=n
                    store.r13_inspection_location=None
                    try:
                        rows=[dict(person=a["person"],pose=a["pose"],x=a["x"],y=a["y"],w=a["width"],h=a["height"],contact=a.get("contact"),slot=a.get("slot"),dot=bool(a.get("dot")),life=a.get("field_life")) for a in r13_stage_people()]
                    except Exception as e:
                        rows="ERR "+repr(e)
                    out["%s/%d/%d"%(loc,d,q)]=rows
        store.room13=saved
        open(path,"w").write(json.dumps(out,ensure_ascii=False,indent=0))

    def qa_life_go(day,period,location,camera=None):
        # 허브 화면은 room13 을 그때그때 읽으므로 상태만 바꾸고 화면을 다시 그린다.
        extra=dict(case_state="occurred" if day>=5 else "pending",week2_started=day>=8,granny_state="trusted",victim_state="alive" if day<5 else "dead")
        r13_edit(day=day,period=period,location=location,**extra)
        store.r13_inspection_location=None
        cams=dict(getattr(store,"r13_world_cameras",{}) or {})
        if camera is not None:cams[location]=camera
        store.r13_world_cameras=cams
        renpy.restart_interaction()

testcase zz_life:
    # 실제 첫날 경로(처음부터 -> 편지 -> 1일 입구 허브)에서 입구 세 시간대만 찍는다. 다른 장소는 r13_edit 로 옮기면
    # 장소 이름표·이야기 바인딩(돌목·다람 동행)이 그대로 남아 실제 화면과 달라지므로 zz_life_roam* 에서 실제 이동(r13_roam)으로 찍는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    screenshot "life_gate_d1_p0.png"
    run Function(qa_life_dump,"/tmp/room13-qa/life_dump_after.json")
    run Function(qa_life_go,1,1,"gate")
    pause 1.0
    screenshot "life_gate_d1_p1.png"
    run Function(qa_life_go,1,2,"gate")
    pause 1.0
    screenshot "life_gate_d1_p2.png"

testcase zz_life_roam:
    # 생활 일정만 있는 상태(이야기 바인딩 없음)에서 장소마다 다시 세워 찍는다. 카메라는 장면을 새로 열기 전에 둔다.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("entry_corrected","lodging"))
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_world_cameras={"square":0}
    run Call("r13_qa_goto",2,0,"square")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_square_d2_p0_left.png"
    $ r13_world_cameras={"square":640}
    run Call("r13_qa_goto",1,1,"square")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_square_d1_p1_right.png"
    $ r13_world_cameras={"square":320}
    run Call("r13_qa_goto",4,1,"square")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_square_d4_p1.png"
    $ r13_world_cameras={"inn":0}
    run Call("r13_qa_goto",1,0,"inn")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_inn_d1_p0_left.png"
    $ r13_world_cameras={"inn":640}
    run Call("r13_qa_goto",9,1,"inn")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_inn_d9_p1.png"
    $ r13_world_cameras={"inn":0}
    run Call("r13_qa_goto",2,2,"inn")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_inn_d2_p2_left.png"
    $ r13_world_cameras={"dining":0}
    run Call("r13_qa_goto",2,2,"dining")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_dining_d2_p2.png"
    $ r13_world_cameras={"school":0}
    run Call("r13_qa_goto",14,2,"school")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_school_d14_p2.png"
    run Call("r13_qa_goto",14,0,"school")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_school_d14_p0.png"
    $ r13_world_cameras={"workshop":0}
    run Call("r13_qa_goto",1,1,"workshop")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_workshop_d1_p1.png"
    $ r13_world_cameras={"clinic":0}
    run Call("r13_qa_goto",1,1,"clinic")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_clinic_d1_p1.png"
    $ r13_world_cameras={"store":320}
    run Call("r13_qa_goto",1,0,"store")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_store_d1_p0.png"
    run Call("r13_qa_goto",2,1,"store")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_store_d2_p1.png"
    $ r13_world_cameras={"post":880}
    run Call("r13_qa_goto",1,0,"post")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_post_d1_p0.png"

testcase zz_life_roam2:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("entry_corrected","lodging","+offers"))
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    run Function(qa_life_dump,"/tmp/room13-qa/life_dump_roam.json")
    $ r13_world_cameras={"post":880}
    run Call("r13_qa_goto",7,1,"post")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_post_d7_p1.png"
    $ r13_world_cameras={"market":880}
    run Call("r13_qa_goto",2,0,"market")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_market_d2_p0.png"
    run Call("r13_qa_goto",2,1,"market")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_market_d2_p1.png"
    $ r13_world_cameras={"river":0}
    run Call("r13_qa_goto",2,0,"river")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_river_d2_p0.png"
    $ r13_world_cameras={"forest":880}
    run Call("r13_qa_goto",2,0,"forest")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_forest_d2_p0.png"
    run Call("r13_qa_goto",7,0,"forest")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_forest_d7_p0.png"
    run Call("r13_qa_goto",2,1,"forest")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_forest_d2_p1.png"
    $ r13_world_cameras={}
    run Call("r13_qa_goto",5,1,"gate")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_gate_d5_p1.png"
    run Call("r13_qa_goto",1,0,"gate")
    click pos (900,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "roam_gate_d1_p0.png"

