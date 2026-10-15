# The two records share one physical bundle on the gate shelf. Legacy object
# keys and their checkmarks survive; only their separate scene hitboxes retire.
init 63 python:
    R13_GATE_DOCUMENTS = {
        "G1": dict(object="booth", tab="예약 원본", heading="예약 원본 · 함께 온 사람 수", text="예약한 사람: 다돌과 한 명 더. 모두 2명."),
        "G3": dict(object="ledger", tab="옮겨 쓴 이름 목록", heading="옮겨 쓴 이름 목록 · 함께 온 사람 수", text="방문자: 다돌. 총 인원: 1명."),
    }
    # 0.18.21 (owner): the two papers are earned separately. The guard hands over his own list (G3)
    # in conversation; the original (G1) is one of several reservation bundles on the shelf,
    # filed by arrival day. Picking another bundle only shows someone else's reservation.
    R13_GATE_BUNDLES = (
        ("sat", "토요일 도착 예정", None, "예약한 사람    솔 외 두 명\n\n모두    3명\n\n가는 곳    광장 뒤 세 번째 집"),
        ("mon", "월요일 도착 예정", "G1", "예약한 사람    다돌 외 한 명\n\n모두    2명\n\n가는 곳    마을 여관"),
        ("wed", "수요일 도착 예정", None, "예약한 사람    광산 인부 무리\n\n모두    4명\n\n가는 곳    마을 입구 숙소"),
    )
    ROOM13["objects"]["gate"]["gate_documents"] = dict(
        rect=list(R13_WORLD_LAYOUTS.get("gate",{}).get("documents",[1034,342,159,111])), text="초소 선반에 예약 서류 묶음이 도착 날짜별로 꽂혀 있다.",
        need=[], give=[], flags=[], inspection_bundle="gate_documents")
    for r13_gate_legacy_key in ("booth", "ledger"):
        ROOM13["objects"]["gate"][r13_gate_legacy_key]["inspection_child"] = "gate_documents"
    # A timed activity on a hidden child object can never be started (0.16 interview bug).
    assert not [k for k in globals().get("R13_CONTEXT_ACTIVITIES",{}) if ROOM13["objects"].get(k[0],{}).get(k[1],{}).get("inspection_child")]
    R13_OBJECT_NAMES["gate_documents"] = "초소 서류"

    def r13_gate_document_art():
        # Enlarge the shelf from the actual adopted gate background. Text is
        # rendered separately; no invented replacement document art is used.
        layout=R13_WORLD_LAYOUTS.get("gate",{})
        if layout:
            # World coordinates stay independent of the player camera offset.
            crop=tuple(layout["documents_crop"])
            return Transform(Crop(crop,r13_world_background("gate")),xysize=(468,int(round(468.0*crop[3]/crop[2]))),nearest=True)
        return Transform(Crop((1026,328,182,140),r13_background("winter")),size=(468,360),nearest=True)

    def r13_gate_record_document(key):
        if store.room13["location"] != "gate" or key not in R13_GATE_DOCUMENTS:
            return False
        object_key=R13_GATE_DOCUMENTS[key]["object"]
        rect=ROOM13["objects"]["gate"][object_key]["rect"]
        r13_mark(object_key,rect[0]+rect[2]//2,rect[1]+rect[3]//2)
        r13_flag("observed:gate:"+object_key)
        if key in store.room13["evidence"]:
            return False
        r13_grant([key],"초소 선반의 서류를 확대해 직접 확인")
        if all(item in store.room13["evidence"] for item in ("G1","G3")):
            rect=ROOM13["objects"]["gate"]["gate_documents"]["rect"]
            r13_mark("gate_documents",rect[0]+rect[2]//2,rect[1]+rect[3]//2)
        return True

    def r13_gate_record_comparison():
        if not all(key in store.room13["evidence"] for key in ("G1","G3")):
            return False
        r13_flag("gate_documents_compared")
        return True

    def r13_visible_check(key, point):
        # Old-save child marks remain stored, but are never separate field ticks.
        return key not in ("gate:booth", "gate:ledger", "gate:gate_documents")

    def r13_gate_bundle_check_point():
        # Synthesize the same single mark for old saves with both records.
        if store.room13["location"] != "gate" or not all(item in store.room13["evidence"] for item in ("G1","G3")):
            return None
        x,y,w,h=ROOM13["objects"]["gate"]["gate_documents"]["rect"]
        return (x+w//2,y+h//2)

init 67 python:
    # Runs after the existing family-desk visibility wrapper. Direct legacy
    # calls still reach the popup through r13_object's early interception.
    r13_before_gate_bundle_visible = r13_object_visible
    def r13_object_visible(spec):
        if spec.get("inspection_child") == "gate_documents":
            return False
        return r13_before_gate_bundle_visible(spec)

label r13_inspect_gate_documents(start_key=None):
    $ r13_flag("observed:gate:gate_documents")
    while True:
        call screen r13_gate_document_inspection()
        if _return not in [b[0] for b in R13_GATE_BUNDLES]:
            return
        $ r13_gate_selected=_return
        call screen r13_gate_document_read(r13_gate_selected)
        if _return:
            $ r13_gate_key=dict((b[0],b[2]) for b in R13_GATE_BUNDLES)[r13_gate_selected]
            if r13_gate_key:
                $ r13_gate_record_document(r13_gate_key)
            else:
                call r13_lines([("dad","(우리 예약이 아니다. 묶음을 제자리에 꽂아 두었다.)",{"thought":True})],"gate:bundle:other")
    return

screen r13_gate_document_inspection(initial="G1"):
    style_prefix "r13"
    modal True
    zorder 70
    add Solid("#081311d9")
    frame:
        area (160,100,960,520) padding (30,26)
        background R13ActionPanel()
        vbox:
            spacing 22
            text "초소 선반" size 30 color "#fff2cf"
            text "예약 서류 묶음이 도착 날짜별로 꽂혀 있다." size 23 color "#d0d7cc"
            for bid,label,gkey,body in R13_GATE_BUNDLES:
                textbutton label + (" · 읽음" if gkey and gkey in room13["evidence"] else ""):
                    style "r13_action_button" xsize 900 ysize 90
                    action Return(bid)
            textbutton "현장으로 돌아가기" style "r13_action_button" xsize 270 ysize 60 action Return(False)
    key "game_menu" action Return(False)

screen r13_gate_document_read(key):
    style_prefix "r13"
    modal True
    zorder 75
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    add Solid("#081311e8")
    frame:
        area (300,62,680,584) padding (40,32)
        background R13PaperPanel(False)
        vbox:
            spacing 28
            $ bundle=dict((b[0],b) for b in R13_GATE_BUNDLES)[key]
            text bundle[1] size 34 color "#765426"
            text "마을 방문 예약" size 23 color "#60695c"
            add Solid("#b5a27c",xsize=600,ysize=1)
            text bundle[3] size r13_read_size(28,32) color "#342a23" line_spacing 8
            text "받아 둔 원본" size 21 color "#60695c"
    textbutton "확인":
        style "r13_action_button" area (774,570,170,58)
        action Return(True) sensitive ready
    textbutton "돌아가기":
        style "r13_action_button" area (338,570,170,58)
        action Return(False)
    key "game_menu" action Return(False)
