# Production basis 01: deliberately bounded D01 slice. Existing saves retain
# their old label/IDs. A new game uses this adapter and stops at registration.
default r13_basis01_state = None
default pb01_block = None
default pb01_record = None
default pb01_i = 0
default pb01_choice = None
default pb01_selected = []

init 210 python:
    import production_basis01 as pb01
    PB01_DATA = json.load(renpy.file("production-basis01-d01.json"))
    pb01.validate(PB01_DATA)
    PB01_BLOCKS = {b["id"]: b for s in PB01_DATA["scenes"] for b in s["blocks"]}
    PB01_RECORDS = {r["id"]: r for b in PB01_BLOCKS.values() for r in b["records"]}
    PB01_TITLES = {"E01": "초대 편지", "E02": "초소 입장 명단", "E03": "다돌이 낸 방문 신청서",
                   "E04": "겨울철 입장 규칙", "E05": "현장 정정 기록"}
    PB01_EVIDENCE_RECORDS = {"E01": "MS14_D01_S01_L9101", "E02": "MS14_D01_S02_L0019",
                            "E03": "MS14_D01_S03_L0002", "E04": "MS14_D01_S03_L0007",
                            "E05": "MS14_D01_S04_L9101"}
    for pb01_key, pb01_rid in PB01_EVIDENCE_RECORDS.items():
        # Runtime namespace avoids reinterpreting old saves' E02/E03/E04.
        # Source scene, record, option and evidence IDs remain untouched in JSON.
        pb01_catalog_key = "PB01:" + pb01_key
        ROOM13["evidence"][pb01_catalog_key] = dict(id=pb01_catalog_key,
            name=PB01_TITLES[pb01_key].strip(), kind="기록",
            establishes=PB01_RECORDS[pb01_rid]["text"], does_not_establish="",
            current_run_only=True, retained_on_show=True)
        R13_RECORD_SHORT[pb01_catalog_key] = PB01_TITLES[pb01_key].strip()

    def pb01_input(action):
        store.r13_basis01_state = pb01.accept_input(store.r13_basis01_state, action)

    def pb01_carriage_background():
        path = "assets/room13-pixel-carriage-empty-winter.webp"
        if not store.r13_basis01_state["village_revealed"]:
            # A01_02: native right-seat crop, fixed scale, no invented layers.
            return Composite((1280,720),(272,0),Transform(Crop((650,0,736,780),path),nearest=True))
        return Transform(path,size=(1280,720),nearest=True)

    def pb01_commit(block, record):
        previous = store.r13_basis01_state
        updated = pb01.commit_record(previous, block, record)
        store.r13_basis01_state = updated
        gained = ["PB01:" + key for key in updated["evidence"] if key not in previous["evidence"]]
        if gained:
            # State + notebook integration run in one Ren'Py statement. No
            # acquisition effect is ever owned by presentation or a screen.
            r13_grant(gained, PB01_TITLES[updated["evidence"][-1]].strip())

    def pb01_prompt(caption, choices):
        r13_end_skip_modes()
        _preferences.afm_enable = False
        state = dict(store.r13_basis01_state)
        state["pending_input"] = caption
        store.r13_basis01_state = state
        # Existing choice screen: .35s input barrier, pagination, toolbar,
        # current approved typography, and native save/rollback semantics.
        return renpy.display_menu([(caption, None)] + choices)

    def pb01_choice_options(record_id):
        record = PB01_RECORDS[record_id]
        result = []
        for option in record["options"]:
            condition = option["when"]
            visible = {
                "always": True,
                "E03 acquired": "E03" in store.r13_basis01_state["evidence"],
                "gate_basis_proven=false": not store.r13_basis01_state["gate_basis_proven"],
                "reason_heard=false": not store.r13_basis01_state["reason_heard"],
                ("purpose_difference_known=true AND reason_heard=false"):
                    store.r13_basis01_state["purpose_difference_known"] and not store.r13_basis01_state["reason_heard"],
            }[condition]
            if visible: result.append((option["label"], option["id"]))
        return result

label pb01_play(block_id, record_ids=None):
    $ pb01_block = PB01_BLOCKS[block_id]
    if not pb01.allowed(r13_basis01_state, block_id):
        $ raise ValueError("Production basis block guard rejected: " + block_id)
    $ pb01_i = 0
    while pb01_i < len(pb01_block["records"]):
        $ pb01_record = pb01_block["records"][pb01_i]
        if record_ids is None or pb01_record["id"] in record_ids:
            if pb01_record["player_visible"] and pb01_record["kind"] != "choice":
                $ r13_basis01_state = dict(r13_basis01_state, record=pb01_record["id"])
                call r13_lines([(pb01.SPEAKERS.get(pb01_record.get("speaker")), pb01_record["text"], {"no_lead": True})], pb01_record["id"])
            if pb01_record["kind"] != "choice":
                $ pb01_commit(pb01_block, pb01_record)
            if pb01_record["id"] == "MS14_D01_S01_L0022":
                # Only AFTER Karo's original line: the village in the existing
                # composite carriage art is now visible for the first time.
                $ r13_basis01_state = dict(r13_basis01_state, village_revealed=True)
                scene expression r13_background("winter_carriage")
        $ pb01_i += 1
    return

label pb01_start:
    $ r13_basis01_state = pb01.new_state()
    $ room13 = dict(room13, campaign_id="production_basis01", location="carriage")
    call r13_scene("winter_carriage", "마차 안", "travel")
    # No approved seated pose: retain narration + the existing say portrait,
    # without standing a full-height body on the carriage seat.
    $ r13_camera = "detail"
    call pb01_play("MS14_D01_S01_B001")
    $ pb01_choice = pb01_prompt("", [("편지를 펼친다", "open_letter")])
    $ pb01_input(pb01_choice)
    call pb01_play("MS14_D01_S01_B002")
    while not r13_basis01_state["letter_close_selected"]:
        $ pb01_choice = pb01_prompt(PB01_RECORDS["MS14_D01_S01_L0014"]["text"], pb01_choice_options("MS14_D01_S01_L0014"))
        if pb01_choice == "MS14_D01_S01_L0014_O1":
            $ pb01_input("inspect_letter_last")
            call pb01_play("MS14_D01_S01_B003")
        elif pb01_choice == "MS14_D01_S01_L0014_O2":
            $ pb01_input("inspect_letter_hand")
            call pb01_play("MS14_D01_S01_B004")
        elif pb01_choice == "MS14_D01_S01_L0014_O3":
            $ pb01_input("close_letter")
        else:
            $ raise ValueError("Unexpected letter option")
    if r13_basis01_state["K01a"] or r13_basis01_state["K01b"]:
        call pb01_play("MS14_D01_S01_B005")
    else:
        call pb01_play("MS14_D01_S01_B006")
    call pb01_play("MS14_D01_S01_B007")
    $ pb01_choice = pb01_prompt("", [("마차에서 내린다", "dismount")])
    $ pb01_input(pb01_choice)
    $ r13_basis01_state = pb01.enter(r13_basis01_state, "MS14_D01_S02")
    $ room13 = dict(room13, location="gate")
    call r13_scene("winter", "눈에 막힌 입구", "calm")
    call pb01_play("MS14_D01_S02_B001")
    $ pb01_choice = pb01_prompt(PB01_RECORDS["MS14_D01_S02_L0022"]["text"], pb01_choice_options("MS14_D01_S02_L0022"))
    if pb01_choice == "MS14_D01_S02_L0022_O1":
        $ pb01_input("show_invitation")
        call pb01_play("MS14_D01_S02_B002")
    elif pb01_choice == "MS14_D01_S02_L0022_O2":
        $ pb01_input("request_original")
        call pb01_play("MS14_D01_S02_B003")
    else:
        $ raise ValueError("Unexpected arrival option")
    call pb01_play("MS14_D01_S02_B004")
    $ pb01_choice = pb01_prompt("", [("자료를 확인한다", "to_documents")])
    $ pb01_input(pb01_choice)
    $ r13_basis01_state = pb01.enter(r13_basis01_state, "MS14_D01_S03")
    jump pb01_gate

label pb01_gate:
    $ pb01_choice = pb01_prompt("다람과 함께 들어간다.", [("신청 원본을 살펴본다", "inspect_original"), ("겨울철 입장 규칙을 살펴본다", "inspect_rules"), ("초소 입장 명단을 다시 본다", "read_processing"), ("자료를 살펴보고 함께 들어갈 이유를 제시한다", "reason"), ("수첩을 펼친다", "notebook")])
    if pb01_choice == "inspect_original":
        $ pb01_input(pb01_choice)
        call pb01_play("MS14_D01_S03_B001", ["MS14_D01_S03_L0002", "MS14_D01_S03_L0003", "MS14_D01_S03_L0004", "MS14_D01_S03_L0005", "MS14_D01_S03_L0006"])
    elif pb01_choice == "inspect_rules":
        $ pb01_input(pb01_choice)
        call pb01_play("MS14_D01_S03_B001", ["MS14_D01_S03_L0007"])
    elif pb01_choice == "read_processing":
        $ pb01_input(pb01_choice)
        call r13_lines([(None, PB01_RECORDS["MS14_D01_S02_L0019"]["text"])], "MS14_D01_S02_L0019:review")
    elif pb01_choice == "notebook":
        $ r13_end_skip_modes()
        call screen r13_book("guard", present=True)
        if _return:
            # The notebook chooses a document, not its conclusion. The player
            # still chooses the actual grounds; no selected paper auto-wins.
            jump pb01_submit
    elif pb01_choice == "reason":
        jump pb01_gate_reason
    else:
        $ raise ValueError("Unexpected gate investigation input")
    jump pb01_gate

label pb01_gate_reason:
    $ pb01_choice = pb01_prompt(PB01_RECORDS["MS14_D01_S03_L0008"]["text"], pb01_choice_options("MS14_D01_S03_L0008") + [("자료를 다시 살펴본다", "review")])
    if pb01_choice == "MS14_D01_S03_L0008_O1":
        $ pb01_input("connect")
        call pb01_play("MS14_D01_S03_B002")
    elif pb01_choice == "MS14_D01_S03_L0008_O2":
        $ pb01_input("lodging")
        call pb01_play("MS14_D01_S03_B003")
    elif pb01_choice == "MS14_D01_S03_L0008_O3":
        jump pb01_submit
    elif pb01_choice == "MS14_D01_S03_L0008_O4":
        $ pb01_input("hint")
        call pb01_play("MS14_D01_S03_B009")
    elif pb01_choice == "MS14_D01_S03_L0008_O5":
        $ pb01_input("ask_worker_reason")
        call pb01_play("MS14_D01_S03_B010")
    elif pb01_choice == "review":
        jump pb01_gate
    else:
        $ raise ValueError("Unexpected argument option")
    jump pb01_gate_reason

label pb01_submit:
    $ pb01_selected = []
label pb01_submit_fields:
    $ pb01_choice = pb01_prompt("제시할 항목을 고른다.", [(label + (" ✓" if key in pb01_selected else ""), key) for key, (ev, label) in pb01.FIELDS.items() if ev in r13_basis01_state["evidence"]] + [("까로의 승객 확인", "passenger"), ("고른 항목을 제시한다", "send"), ("돌아간다", "cancel")])
    if pb01_choice == "cancel":
        jump pb01_gate_reason
    elif pb01_choice == "send":
        $ r13_basis01_state = dict(r13_basis01_state, selected=list(pb01_selected))
        $ pb01_input("submit" if pb01.correct_submission(r13_basis01_state) else "passenger" if set(pb01_selected)=={"passenger"} else "count")
        call pb01_play(pb01.submission_block(r13_basis01_state))
        if r13_basis01_state["gate_basis_proven"]:
            $ r13_basis01_state = pb01.enter(r13_basis01_state, "MS14_D01_S04")
            call pb01_play("MS14_D01_S04_B001")
            $ r13_basis01_state = dict(r13_basis01_state, complete=True, pending_input=None)
            $ r13_end_skip_modes()
            $ renpy.notify("이번 플레이 구간은 여기까지입니다.")
            return
        jump pb01_gate_reason
    else:
        $ pb01_selected = [key for key in pb01_selected if key != pb01_choice] if pb01_choice in pb01_selected else pb01_selected + [pb01_choice]
        jump pb01_submit_fields
