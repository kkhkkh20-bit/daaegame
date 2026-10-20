# Native-engine checks. This directory is excluded from release builds.
init 998 python:
    MS14_QA_REAL_BOOK = renpy.display.screen.get_screen_variant("r13_book")

init 900 python:
    def ms14_qa_reach(target, afternoon="shelter", stone=0, custody=0):
        state=ms14_rt.new_state(MS14_DATA)
        for _ in range(1000):
            key=state["node"]
            if key==target:return state
            node=MS14_DATA["nodes"][key]
            if node["kind"]=="proof":
                for evidence in node["correct"]:state=ms14_rt.select(state,evidence)
                state=ms14_rt.submit(state,node)
            elif node["kind"]=="choice":
                index=0
                if key=="letter_menu":index=2
                elif key=="gate_choice":index=1
                elif key=="gate_investigate":
                    index=0 if "E03" not in state["evidence"] else (1 if "E04" not in state["evidence"] else 5)
                elif key in ("registered_menu","post_menu"):index=1
                elif key=="lamp_observe":index=next((i for i in range(4) if not state["values"]["lamp_part_"+str(i)]),4)
                elif key=="afternoon":index=0 if afternoon=="shelter" else 1
                elif key=="stone_choice":index=stone
                elif key=="custody_choice":index=custody
                elif key=="d4_field":index=next((i for i,k in enumerate(("fence","tracks","bucket")) if not state["values"]["d4_"+k+"_seen"]),3)
                elif key=="d5_rebuttal_menu":index=1
                elif key=="d5_review_choice":index=1
                state=ms14_rt.choose(state,node,index)
            elif node["kind"]=="block":
                for rid in node["records"][state["cursor"]:]:state=ms14_rt.finish_record(state,MS14_DATA["records"][rid])
                state=ms14_rt.enter(state,node["next"])
            elif node["kind"]=="branch":
                state=ms14_rt.enter(state,ms14_rt.branch_target(state,node))
            elif node["kind"]=="mark":state=ms14_rt.enter(ms14_rt.apply(state,key,node["operations"]),node["next"])
            elif node["kind"]=="read":state=ms14_rt.enter(state,node["next"])
            else:raise Exception("QA unexpected route: "+key)
        raise Exception("QA target unreachable: "+target)

label ms14_qa_at(target,afternoon="shelter",stone=0,custody=0):
    $ ms14=ms14_qa_reach(target,afternoon,stone,custody)
    $ ms14_village_visible=True
    jump ms14_run

testcase ms14_opening:
    pause 2.0
    click "처음부터"
    pause 2.0
    assert eval (ms14 is not None and ms14["node"]=="start")
    screenshot "ms14_opening.png"
    click pos (640,600) until "편지를 펼친다" timeout 40
    assert eval ("E01" not in ms14["evidence"])
    screenshot "ms14_letter_input.png"
    click "편지를 펼친다"
    click pos (640,600) until "편지를 접는다" timeout 40
    assert eval ("E01" in ms14["evidence"])
    click "마지막 줄을 본다"
    click pos (640,600) until "편지를 접는다" timeout 30
    assert eval (ms14["values"]["K01a"])
    click "편지를 접는다"
    click pos (640,600) until "마차에서 내린다" timeout 40
    assert eval ms14_village_visible
    screenshot "ms14_village_reveal.png"

testcase ms14_gate:
    pause 2.0
    click "처음부터"
    pause 1.0
    run Jump("ms14_qa_gate_setup")
    pause 1.0
    assert eval ("E03" not in ms14["evidence"] and "E04" not in ms14["evidence"])
    screenshot "ms14_gate_investigate.png"
    click "신청 원본을 읽는다"
    click pos (640,600) until eval (ms14["node"]=="gate_investigate") timeout 40
    pause 0.6
    assert eval ("E03" in ms14["evidence"] and "E04" not in ms14["evidence"])
    click "겨울철 입장 규칙을 읽는다"
    click pos (640,600) until eval (ms14["node"]=="gate_investigate") timeout 40
    pause 0.6
    assert eval ("E04" in ms14["evidence"] and not ms14["values"]["gate_basis_proven"])
    click "다른 항목을 본다"
    pause 0.6
    screenshot "ms14_gate_ready.png"

label ms14_qa_gate_setup:
    jump expression "ms14_qa_gate_enter"
label ms14_qa_gate_enter:
    call ms14_qa_at("gate_investigate")
    return

testcase ms14_present:
    pause 2.0
    click "처음부터"
    pause 1.0
    run Jump("ms14_qa_present_setup")
    pause 1.0
    click "자료를 고른다"
    pause 1.0
    screenshot "ms14_proof_notebook.png"
    assert screen "r13_book"

label ms14_qa_present_setup:
    # Existing helper init 999 substitutes a tiny evidence-return screen. Restore
    # the captured production screen for this UI check, leaving legacy tests alone.
    $ renpy.display.screen.screens[("r13_book",None)] = MS14_QA_REAL_BOOK
    call ms14_qa_at("trial_latch")
    return

testcase ms14_somi:
    pause 2.0
    click "처음부터"
    pause 1.0
    run Jump("ms14_qa_somi_setup")
    pause 1.0
    click pos (640,600) until eval (r13_packet[0]=="resident_nero") timeout 30
    pause 0.5
    screenshot "ms14_somi.png"
    assert eval (ms14["values"]["nero_met_day2"] and ms14["values"]["carried_dry_blankets"]==2)

label ms14_qa_somi_setup:
    call ms14_qa_at("somi4","nero",0,1)
    return

testcase ms14_skip_save:
    pause 2.0
    click "처음부터"
    pause 1.0
    click "현재 대화 건너뛰기"
    pause 0.4
    click "건너뛰기"
    pause 0.6
    assert eval (ms14["node"]=="letter_open" and "E01" not in ms14["evidence"])
    $ renpy.save("qa-ms14-before-letter","ms14")
    assert eval renpy.can_load("qa-ms14-before-letter")
    click "편지를 펼친다"
    click pos (640,600) until eval (ms14["node"]=="letter_menu") timeout 40
    assert eval ("E01" in ms14["evidence"])
    run Function(renpy.load,"qa-ms14-before-letter")
    pause 0.7
    assert eval (ms14["node"]=="letter_open" and "E01" not in ms14["evidence"])
    screenshot "ms14_save_restored.png"
