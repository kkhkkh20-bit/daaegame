# Authored D01 labels; all game state belongs to the existing room13 store.
# No parallel runtime store or new selection screen.

init 210 python:
    PB01_DATA = json.load(renpy.file("production-basis01-d01.json"))
    if PB01_DATA["version"] != "DT_STORY_1.1_PRODUCTION_BASIS_01_20261020":
        raise ValueError("Unsupported story basis")
    PB01_BLOCKS = {b["id"]: b for s in PB01_DATA["scenes"] for b in s["blocks"]}
    PB01_RECORDS = {r["id"]: r for b in PB01_BLOCKS.values() for r in b["records"]}
    PB01_SPEAKERS = {"아빠":"dad", "다람":"daram", "까로":"karo", "돌목":"guard"}
    PB01_TITLES = {"E01":"초대 편지", "E02":"초소 입장 명단", "E03":"다돌이 낸 방문 신청서", "E04":"겨울철 입장 규칙", "E05":"현장 정정 기록"}
    PB01_DOCUMENTS = {"E01":"MS14_D01_S01_L9101", "E02":"MS14_D01_S02_L0019", "E03":"MS14_D01_S03_L0002", "E04":"MS14_D01_S03_L0007", "E05":"MS14_D01_S04_L9101"}
    for pb01_key, pb01_record_id in PB01_DOCUMENTS.items():
        key = "PB01:" + pb01_key
        ROOM13["evidence"][key] = dict(id=key, name=PB01_TITLES[pb01_key], kind="기록", establishes=PB01_RECORDS[pb01_record_id]["text"], does_not_establish="", current_run_only=True, retained_on_show=True)
        R13_RECORD_SHORT[key] = PB01_TITLES[pb01_key]

    def pb01_active():
        return (store.room13 or {}).get("campaign_id") == "production_basis01"

    def pb01_lines(block_id, record_ids=None):
        # Read-only projection; never evaluates when/requires or applies effects.
        return [(PB01_SPEAKERS.get(r.get("speaker")), r["text"], dict(no_lead=True, source_record_id=r["id"])) for r in PB01_BLOCKS[block_id]["records"] if r["player_visible"] and r["kind"] != "choice" and (record_ids is None or r["id"] in record_ids)]

    def pb01_menu(caption, options):
        r13_end_skip_modes()
        _preferences.afm_enable = False
        return renpy.display_menu([(caption, None)] + options)

    def pb01_entry_questions():
        actions = ["compare", "lodging", "submit", "hint", "reason"]
        guards = [dict(need=["PB01:E03"]), dict(need=["PB01:E03"]), dict(not_flags=["pb01:gate_basis_proven"]), {}, dict(need=["pb01:purpose_difference_known"], not_flags=["pb01:reason_heard"])]
        return [(o["label"], Return(("entry", a)), False) for o,a,g in zip(PB01_RECORDS["MS14_D01_S03_L0008"]["options"],actions,guards) if r13_available(g)]

    def pb01_gate_block(key):
        pending = store.r13_present_priority
        selected = set(pending[1]) if pending and pending[0] == "guard" else set()
        if key in ("PB01:E03", "PB01:E04") and selected == {"PB01:E03", "PB01:E04"} and r13_available(dict(need=["PB01:E02","PB01:E03","PB01:E04"])):
            return "MS14_D01_S03_B004" if r13_has("pb01:purpose_difference_known") else "MS14_D01_S03_B005"
        return "MS14_D01_S03_B006"

    def pb01_present_lines(key, identity=False):
        # Existing final r13_present wrapper calls this for this scene only.
        # Keep the original presentation/history chain; replace its reply data.
        _r13_sling_confidence_present("guard", key, identity)
        return pb01_lines(pb01_gate_block(key))

    def pb01_compare_feedback(selected):
        if not r13_available(dict(need=["PB01:E02","PB01:E03"])):
            return _r13_tm_compare(selected)
        r13_flag("pb01:purpose_difference_known")
        return "\n\n".join(ROOM13["evidence"][key]["establishes"] for key in ("PB01:E02","PB01:E03"))

    def pb01_carriage_background():
        path = "assets/room13-pixel-carriage-empty-winter.webp"
        if not r13_has("pb01:village_revealed"):
            return Composite((1280,720),(272,0),Transform(Crop((650,0,736,780),path),nearest=True))
        return Transform(path,size=(1280,720),nearest=True)

label pb01_start:
    $ r13_edit(campaign_id="production_basis01", location="carriage")
    call r13_carriage
    $ r13_edit(location="gate")
    $ r13_note_encounter("guard"); r13_note_encounter("daram"); r13_note_encounter("karo")
    call r13_scene("winter", "눈에 막힌 입구", "calm")
    call r13_lines(pb01_lines("MS14_D01_S02_B001"), "MS14_D01_S02_B001")
    $ r13_grant(["PB01:E02"], "MS14_D01_S02_L0019")
    $ r13_choice = pb01_menu(PB01_RECORDS["MS14_D01_S02_L0022"]["text"], [(o["label"],o["id"]) for o in PB01_RECORDS["MS14_D01_S02_L0022"]["options"]])
    if r13_choice == "MS14_D01_S02_L0022_O1":
        call r13_lines(pb01_lines("MS14_D01_S02_B002"), "MS14_D01_S02_B002")
    elif r13_choice == "MS14_D01_S02_L0022_O2":
        call r13_lines(pb01_lines("MS14_D01_S02_B003"), "MS14_D01_S02_B003")
    else:
        $ raise ValueError("Unknown arrival option")
    $ r13_choice = pb01_menu("", [("자료를 확인한다", "inspect")])
    jump r13_entry

label r13_pb01_carriage:
    call r13_scene("winter_carriage", "마차 안", "travel")
    $ r13_camera = "detail"
    call r13_lines(pb01_lines("MS14_D01_S01_B001"), "MS14_D01_S01_B001")
    $ r13_choice = pb01_menu("", [("편지를 펼친다", "open")])
    $ r13_grant(["PB01:E01"], "MS14_D01_S01_L0010")
    call r13_lines(pb01_lines("MS14_D01_S01_B002"), "MS14_D01_S01_B002")
    while not r13_has("pb01:letter_closed"):
        $ r13_choice = pb01_menu(PB01_RECORDS["MS14_D01_S01_L0014"]["text"], [(o["label"],o["id"]) for o in PB01_RECORDS["MS14_D01_S01_L0014"]["options"]])
        if r13_choice == "MS14_D01_S01_L0014_O1":
            call r13_lines(pb01_lines("MS14_D01_S01_B003"), "MS14_D01_S01_B003")
            $ r13_flag("pb01:K01a")
        elif r13_choice == "MS14_D01_S01_L0014_O2":
            call r13_lines(pb01_lines("MS14_D01_S01_B004"), "MS14_D01_S01_B004")
            $ r13_flag("pb01:K01b")
        elif r13_choice == "MS14_D01_S01_L0014_O3":
            $ r13_flag("pb01:letter_closed")
        else:
            $ raise ValueError("Unknown letter option")
    if r13_has("pb01:K01a") or r13_has("pb01:K01b"):
        call r13_lines(pb01_lines("MS14_D01_S01_B005"), "MS14_D01_S01_B005")
    else:
        call r13_lines(pb01_lines("MS14_D01_S01_B006"), "MS14_D01_S01_B006")
    call r13_lines(pb01_lines("MS14_D01_S01_B007"), "MS14_D01_S01_B007")
    $ r13_flag("pb01:village_revealed")
    scene expression r13_background("winter_carriage")
    $ r13_choice = pb01_menu("", [("마차에서 내린다", "dismount")])
    return

label r13_pb01_documents:
    call r13_lines(pb01_lines("MS14_D01_S03_B001", ["MS14_D01_S03_L0002","MS14_D01_S03_L0003","MS14_D01_S03_L0004","MS14_D01_S03_L0005","MS14_D01_S03_L0006"]), "MS14_D01_S03_B001:original")
    $ r13_grant(["PB01:E03"], "MS14_D01_S03_L0002")
    $ r13_flag("observed:gate:gate_documents")
    return

label r13_pb01_rules:
    call r13_lines(pb01_lines("MS14_D01_S03_B001", ["MS14_D01_S03_L0007"]), "MS14_D01_S03_B001:rules")
    $ r13_grant(["PB01:E04"], "MS14_D01_S03_L0007")
    $ r13_flag("observed:gate:rules")
    return

label r13_pb01_entry_person:
    if person == "daram":
        if r13_has("PB01:E03"):
            call r13_lines(pb01_lines("MS14_D01_S03_B001", ["MS14_D01_S03_L0003","MS14_D01_S03_L0004","MS14_D01_S03_L0005","MS14_D01_S03_L0006"]), "MS14_D01_S03:review_original")
        else:
            call r13_lines(pb01_lines("MS14_D01_S02_B001", ["MS14_D01_S02_L0017","MS14_D01_S02_L0018"]), "MS14_D01_S02:waiting")
    elif person == "karo":
        call r13_lines(pb01_lines("MS14_D01_S02_B001", ["MS14_D01_S02_L0005","MS14_D01_S02_L0007"]), "MS14_D01_S02:karo")
    return

label r13_pb01_entry_dispatch:
    if r13_choice[0] == "object":
        call r13_object(r13_choice[1])
        jump r13_entry
    elif r13_choice == ("entry","compare") and r13_available(dict(need=["PB01:E02","PB01:E03"])):
        call r13_lines(pb01_lines("MS14_D01_S03_B002"), "MS14_D01_S03_B002")
        $ r13_flag("pb01:purpose_difference_known")
    elif r13_choice == ("entry","lodging") and r13_available(dict(need=["PB01:E03"])):
        call r13_lines(pb01_lines("MS14_D01_S03_B003"), "MS14_D01_S03_B003")
    elif r13_choice == ("entry","hint"):
        call r13_lines(pb01_lines("MS14_D01_S03_B009"), "MS14_D01_S03_B009")
    elif r13_choice == ("entry","reason") and r13_available(dict(need=["pb01:purpose_difference_known"],not_flags=["pb01:reason_heard"])):
        call r13_lines(pb01_lines("MS14_D01_S03_B010"), "MS14_D01_S03_B010")
        $ r13_flag("pb01:reason_heard", "pb01:K05")
    elif r13_choice == ("entry","submit"):
        call r13_pb01_submit
        if r13_has("pb01:gate_basis_proven"):
            jump r13_entry_done
    elif r13_choice == ("entry","argue"):
        $ r13_present_priority = None
        $ r13_end_skip_modes()
        call screen r13_book("guard",present=True)
        $ r13_item = _return
        if r13_item:
            call r13_lines(r13_present("guard",r13_item), "MS14_D01_S03:present")
    elif r13_choice[0] in ("empty",) or r13_choice == ("entry","back"):
        jump r13_entry
    else:
        $ raise ValueError("Unavailable entry input")
    jump r13_entry_guard_menu

label r13_pb01_submit:
    # Two existing notebook selections. The original contains family purpose
    # and two-person lodging; the rule is the third ground. No new field UI.
    $ r13_present_priority = None
    $ r13_end_skip_modes()
    call screen r13_book("guard",present=True)
    $ r13_item = _return
    if not r13_item:
        return
    $ r13_prepare_present("guard", [r13_item])
    call screen r13_book("guard",present=True)
    $ r13_item = _return
    if not r13_item:
        $ r13_present_priority = None
        return
    $ r13_prepare_present("guard", list(r13_present_priority[1])+[r13_item])
    call r13_lines(r13_present("guard",r13_item), "MS14_D01_S03:submit")
    if pb01_gate_block(r13_item) in ("MS14_D01_S03_B004","MS14_D01_S03_B005"):
        $ r13_flag("pb01:purpose_difference_known", "pb01:gate_basis_proven")
    $ r13_present_priority = None
    return

label r13_pb01_registered:
    if not r13_available(dict(need=["pb01:gate_basis_proven","PB01:E02","PB01:E03","PB01:E04"])):
        $ raise ValueError("Registration needs all three grounds")
    call r13_lines(pb01_lines("MS14_D01_S04_B001", ["MS14_D01_S04_L0002","MS14_D01_S04_L0003","MS14_D01_S04_L0004","MS14_D01_S04_L0005","MS14_D01_S04_L0006","MS14_D01_S04_L0008"]), "MS14_D01_S04_B001:registration")
    $ r13_grant(["PB01:E05"], "MS14_D01_S04_L0008")
    $ r13_flag("entry_corrected", "pb01:gate_registered")
    call r13_lines(pb01_lines("MS14_D01_S04_B001", ["MS14_D01_S04_L9101","MS14_D01_S04_L0009","MS14_D01_S04_L0010","MS14_D01_S04_L0011"]), "MS14_D01_S04_B001:after_registration")
    $ r13_end_skip_modes()
    $ renpy.notify("이번 플레이 구간은 여기까지입니다.")
    return
