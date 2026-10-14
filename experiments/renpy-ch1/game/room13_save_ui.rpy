# Saves are inspected through JSON metadata; never unpickle an unknown save just
# to decide whether the title's Continue button should open it.
init 100 python:
    R13_SAVE_CONTRACT=1
    R13_SAVE_SLOTS=r"^(?:[0-9]+|auto|quick)-[0-9]+$"

    def r13_save_metadata(data):
        state=getattr(store,"room13",None) or {}
        if getattr(store,"room13_mode",False):
            data["r13_contract"]=R13_SAVE_CONTRACT
            data["r13_campaign"]=state.get("campaign_id")
            data["r13_story"]=state.get("story_revision")
            data["r13_visual"]=state.get("visual_revision")
            data["r13_day"]=state.get("day")
    config.save_json_callbacks.append(r13_save_metadata)

    def r13_save_status(data):
        if not data:return "empty"
        if data.get("r13_contract") is None:return "unknown"
        if (data.get("r13_contract")!=R13_SAVE_CONTRACT or data.get("r13_campaign")!="room13_v1"
            or data.get("r13_story")!=ROOM13["story_revision"] or data.get("r13_visual")!="pixel-b-front-v3"):
            return "incompatible"
        return "compatible"

    def r13_save_slots():
        return renpy.list_saved_games(regexp=R13_SAVE_SLOTS,fast=True)

    def r13_continue_slot():
        candidates=[((renpy.slot_json(slot) or {}).get("_ctime",0),slot) for slot in r13_save_slots()
            if r13_save_status(renpy.slot_json(slot))=="compatible"]
        return max(candidates)[1] if candidates else None

    def r13_save_caption(data):
        if not data:return "비어 있음"
        status=r13_save_status(data)
        return "%s · %s"%(data.get("_version") or "버전 미상",
            {"compatible":"현재 버전에서 이어갈 수 있음","unknown":"호환 확인 전 · 새 게임 권장","incompatible":"현재 버전과 호환되지 않음"}[status])

    def r13_slot_name(slot,page=None):
        return (page or persistent._file_page or "1")+"-"+str(slot)

    def r13_load_action(slot):
        status=r13_save_status(renpy.slot_json(slot))
        if status=="compatible":return FileLoad(slot,slot=True,confirm=False)
        if status=="empty":return NullAction()
        return Show("r13_save_review",slot=slot,status=status)

    def r13_cleanup_slots(scope):
        return tuple(slot for slot in r13_save_slots() if scope=="all" or r13_save_status(renpy.slot_json(slot))!="compatible")

    def r13_delete_confirmed_saves(slots,fingerprints):
        # Only the exact snapshot displayed by the confirmation is removed.
        # Persistent preferences, read history and discoveries are never erased.
        allowed=set(r13_save_slots())
        for slot in slots:
            if slot in allowed and (renpy.slot_json(slot) or {}).get("_ctime")==fingerprints.get(slot):renpy.unlink_save(slot)
        renpy.restart_interaction()

screen r13_save_review(slot,status):
    modal True
    zorder 120
    add Solid("#07151ddf")
    frame:
        xalign .5 yalign .5 xsize 920 padding (32,28)
        background R13ActionPanel()
        vbox:
            spacing 20
            text "이전 저장 확인" size 30 color "#ebcd8a"
            text r13_save_caption(renpy.slot_json(slot)) size 24 color "#fff4df" xsize 856
            text ("이 저장은 진행 규칙이나 화면 버전이 다릅니다. 새 게임으로 시작해 주세요." if status=="incompatible" else "이 저장에는 호환 정보가 없습니다. 이전 화면이 나타날 수 있어 이어하기에서 제외했습니다. 현재 화면으로 시작하려면 처음부터 시작해 주세요.") size 25 color "#fff4df" xsize 856
            text "저장은 삭제하지 않았습니다." size 22 color "#ced9d4"
            hbox:
                spacing 16
                textbutton "돌아가기" style "r13_action_button" action Hide("r13_save_review")
                if status=="unknown":
                    textbutton "확인하고 구 저장 열기" style "r13_action_button" action [Hide("r13_save_review"),FileLoad(slot,slot=True,confirm=False)]
    key "game_menu" action Hide("r13_save_review")

screen r13_save_cleanup(scope="old"):
    modal True
    zorder 120
    default slots=r13_cleanup_slots(scope)
    default fingerprints={slot:(renpy.slot_json(slot) or {}).get("_ctime") for slot in slots}
    $ manual=sum(not slot.startswith(("auto-","quick-")) for slot in slots)
    $ autos=sum(slot.startswith("auto-") for slot in slots)
    $ quick=sum(slot.startswith("quick-") for slot in slots)
    add Solid("#07151ddf")
    frame:
        xalign .5 yalign .5 xsize 920 padding (32,28)
        background R13ActionPanel()
        vbox:
            spacing 20
            text ("모든 진행 저장 정리" if scope=="all" else "이전·미확인 저장 정리") size 30 color "#ebcd8a"
            text ("삭제 대상: 수동 %d개 · 자동 %d개 · 빠른 저장 %d개"%(manual,autos,quick)) size 25 color "#fff4df"
            text "선택한 진행 저장은 되돌릴 수 없습니다. 소리·큰 글씨 설정과 읽은 대사 표시는 유지합니다." size 25 color "#fff4df" xsize 856
            hbox:
                spacing 20
                textbutton "취소" style "r13_action_button" action Hide("r13_save_cleanup")
                textbutton "위 진행 저장 삭제" style "r13_action_button" sensitive bool(slots) action [Function(r13_delete_confirmed_saves,slots,fingerprints),Hide("r13_save_cleanup")]
    key "game_menu" action Hide("r13_save_cleanup")
