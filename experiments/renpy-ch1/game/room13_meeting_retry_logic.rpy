# 회의 첫 쟁점 직전의 상태를 저장한다. 다시 고르면 그 회의 안의 변경만 되돌린다.
default r13_meeting_checkpoint_state = None

init 324 python:
    R13_MEETING_RESTART_LABELS = {'gate': 'r13_v111_gate_proof', 'lamp': 'r13_v111_trial_repair', 'gate_post': 'r13_v111_proof5', 'fire': 'r13_v111_nubi_proof7', 'room13': 'r13_v111_wound_proof10', 'records': 'r13_v111_authority_proof10', 'hypothesis': 'r13_v111_hyp0_menu11', 'soup': 'r13_v111_seal_proof12', 'blanket': 'r13_v111_mending_proof13', 'piko': 'r13_v111_rein_ledger13p', 'altar': 'r13_v111_altar1_proof14'}

    def r13_meeting_checkpoint(meeting):
        old = store.r13_meeting_checkpoint_state
        if old and old["meeting"] == meeting:
            return
        # 구형 저장의 첫 쟁점 재진입을 새 회의 시작으로 오인하지 않는다.
        if store.room13.get("v111",{}).get("values",{}).get("tries:"+meeting,0):
            return
        store.r13_meeting_checkpoint_state = dict(
            meeting=meeting, room=winter_copy.deepcopy(store.room13),
            locals=winter_copy.deepcopy({k:v for k,v in vars(store).items() if k.startswith("v111_")}))

    # 2026-10-27 외부 리뷰 R08: 복원이 room 전체를 되돌려 체크포인트 뒤 조사로 얻은 자료(방문 신청 원본 등)까지 지웠다.
    # 자료·기록·읽은 주제·관찰·조사 표식은 지금 것을 두고, 회의 상태(논증·기회·쟁점 진행)만 체크포인트로 돌린다.
    R13_MEETING_RESTORE_KEEP = ("evidence", "records", "read_topics", "observations", "checks")

    def r13_meeting_restore_keep(current, restored):
        for key in R13_MEETING_RESTORE_KEEP:
            if key in current:
                restored[key] = winter_copy.deepcopy(current[key])
        # 관찰 깃발(observed:…)과 얻은 자료의 변형 값(E03.variant)도 조사 결과라 남긴다. 회의 안의 applied 깃발은 되돌린다.
        for flag in current.get("flags", []):
            if flag.startswith("observed:") and flag not in restored.get("flags", []):
                restored.setdefault("flags", []).append(flag)
        values = current.get("v111", {}).get("values", {})
        kept = restored.get("v111", {}).get("values")
        if kept is not None:
            for key, value in values.items():
                if key.endswith(".variant") and key not in kept:
                    kept[key] = winter_copy.deepcopy(value)
        return restored

    def r13_meeting_restore(meeting):
        checkpoint = store.r13_meeting_checkpoint_state
        if not checkpoint or checkpoint["meeting"] != meeting:
            return False
        store.room13 = r13_meeting_restore_keep(store.room13, winter_copy.deepcopy(checkpoint["room"]))
        for key in list(vars(store)):
            if key.startswith("v111_") and key not in checkpoint["locals"]:
                setattr(store,key,None)
        for key,value in checkpoint["locals"].items():
            setattr(store,key,winter_copy.deepcopy(value))
        store.r13_nw_wrong_pending = None
        store.v111_last_presented = []
        store.v111_claim = None
        return True

    def r13_meeting_exhausted(meeting):
        # 구형 중간 저장에는 첫 쟁점 체크포인트가 없다. 과거 상태를 지어내지 않는다.
        checkpoint = store.r13_meeting_checkpoint_state
        if not checkpoint or checkpoint["meeting"] != meeting:
            return
        answer = renpy.call_screen("r13_meeting_retry_choice")
        # 2026-10-27: 되돌아갈 수 있는 범위 안내는 처음 본 한 번으로 줄인다.
        r13_recovery_retry_seen()
        # 화면 자체가 마지막 속말을 보여 주므로 뒤 대사 묶음에 중복 삽입하지 않는다.
        store.r13_nw_wrong_pending = None
        if answer == R13_MEETING_RETRY_RETRY and r13_meeting_restore(meeting):
            # 소진 전 알림이 새 회의의 기회 표시와 겹치지 않게 지운다.
            renpy.hide_screen("notify")
            renpy.jump(R13_MEETING_RESTART_LABELS[meeting])
