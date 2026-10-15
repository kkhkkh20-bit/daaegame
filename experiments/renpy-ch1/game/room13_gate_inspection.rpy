# The two records share one physical bundle on the gate shelf. Legacy object
# keys and their checkmarks survive; only their separate scene hitboxes retire.
init 63 python:
    R13_GATE_DOCUMENTS = {
        "G1": dict(object="booth", tab="예약 원본", heading="예약 원본 · 함께 온 사람 수", text="예약한 사람: 다돌과 한 명 더. 모두 2명."),
        "G3": dict(object="ledger", tab="옮겨 쓴 이름 목록", heading="옮겨 쓴 이름 목록 · 함께 온 사람 수", text="방문자: 다돌. 총 인원: 1명."),
    }
    # 0.18.21 (owner): no document popup. The guard hands over his own list (G3) in conversation;
    # clicking the shelf finds the original (G1) in a short scene, like the posted rules.
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
    if "G1" in room13["evidence"]:
        call r13_lines([("dad","(선반의 예약 서류 묶음. 우리 예약 원본은 이미 확인했다.)",{"thought":True})],"gate:shelf:again")
        return
    call r13_lines([(None,"초소 선반에 예약 서류 묶음이 날짜별로 꽂혀 있었다."),
        (None,"월요일 묶음을 넘기자 낯익은 글씨가 나왔다. 신청할 때 내가 쓴 예약 서류다."),
        ("dad","(예약한 사람 다돌 외 한 명. 모두 2명.)",{"thought":True}),
        ("daram","아빠, 거기 ‘외 한 명’이 나야?"),
        ("dad","응. 여기엔 분명히 두 사람으로 적혀 있어.")],"gate:shelf:find")
    $ r13_gate_record_document("G1")
    return
