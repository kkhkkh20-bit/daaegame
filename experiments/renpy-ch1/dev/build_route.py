from pathlib import Path
root=Path(__file__).resolve().parents[1]
model=(root/'dev/recommended_model.py').read_text()
header='''# Recommended route: isolated saved state; never migrates legacy room13 facts.
default r13_recommended = None
default r13_recommended_choice = None
init 900 python:
'''
(root/'game/systems/room13_recommended_story.rpy').write_text(header+''.join('    '+line+'\n' for line in model.splitlines())+'''

init 920 python:
    _r13_rec_original_save_status = r13_save_status
    _r13_rec_original_save_caption = r13_save_caption
    _r13_rec_original_load_action = r13_load_action
    _r13_rec_original_continue_slot = r13_continue_slot
    def r13_rec_save_metadata(data):
        state = getattr(store, "r13_recommended", None)
        if state and (getattr(store, "room13", None) or {}).get("campaign_id") in ("room13_recommended_v1","room13_recommended_qa_v1"):
            data["r13_recommended_revision"] = state["revision"]
            data["r13_recommended_episode"] = state["episode"]
    config.save_json_callbacks.append(r13_rec_save_metadata)
    def r13_save_status(data):
        if data and data.get("r13_campaign") in ("room13_recommended_v1","room13_recommended_qa_v1"):
            return "compatible" if data.get("r13_recommended_revision") == r13_rec_revision else "incompatible"
        return _r13_rec_original_save_status(data)
    def r13_save_caption(data):
        if data and data.get("r13_campaign") == "room13_recommended_qa_v1":
            return "미검증 QA 전용 · %s일 · 명시 확인 후 불러오기" % data.get("r13_day")
        if data and data.get("r13_campaign") == "room13_recommended_v1":
            return "추천 검증판 · %s일 · %s" % (data.get("r13_day"), "이어갈 수 있음" if r13_save_status(data)=="compatible" else "새로 시작 필요")
        return _r13_rec_original_save_caption(data)
    def r13_continue_slot():
        slot = _r13_rec_original_continue_slot()
        if slot is None or (renpy.slot_json(slot) or {}).get("r13_campaign") != "room13_recommended_qa_v1":
            return slot
        candidates=[((renpy.slot_json(slot) or {}).get("_ctime",0),slot) for slot in r13_save_slots()
            if (renpy.slot_json(slot) or {}).get("r13_campaign") != "room13_recommended_qa_v1" and r13_save_status(renpy.slot_json(slot))=="compatible"]
        return max(candidates)[1] if candidates else None
    def r13_load_action(slot):
        data=renpy.slot_json(slot) or {}
        if data.get("r13_campaign")=="room13_recommended_qa_v1" and r13_save_status(data)=="compatible":
            return Confirm("미검증 QA 전용 저장입니다. 일반 추천판이 아니라 최종 단계 시험 상태를 불러올까요?",FileLoad(slot,slot=True,confirm=False))
        return _r13_rec_original_load_action(slot)


screen r13_recommended_setup():
    modal True
    add Solid("#172421")
    frame:
        xalign .5 yalign .5 xsize 980
        vbox:
            spacing 24
            text "추천 스토리 · 개발 검증판" size 32
            text "마차 도착과 입구 조사부터 새 추천안의 대사·조사·선택을 시험하는 별도 경로입니다. 기존 저장은 변환하지 않습니다. 직접 반출에 쓰이는 등/천 그림과 후속 회차는 검수 상태에 따라 제한됩니다." size 24
            text "아직 전체 캠페인 적용 완료가 아니며, 확인된 결과와 검수 중인 부분을 구분합니다." size 24
            text r13_rec_e456_art_status size 18
            textbutton "새 추천 이야기 시작" action Return(True)
            textbutton "제목 화면" action MainMenu(confirm=False)

screen r13_recommended_actions():
    modal True
    add Solid("#172421ef")
    frame:
        xpos 24 ypos 24 xsize 1232 ysize 646
        vbox:
            spacing 12
            text ("추천 스토리 검증판 · %d일 · 엄마 %s" % (r13_recommended["day"], r13_recommended["mother"])) size 28
            text (r13_rec_episodes[r13_recommended["episode"]]["title"]+" · 기존 저장과 분리") size 19
            if r13_recommended.get("qa_fixture"):
                text "미검증 QA 전용 · 최종 단계 시험 허용" size 19 color "#ffb76b"
            hbox:
                spacing 18
                vbox:
                    xsize 610 spacing 8
                    viewport:
                        ysize 350 mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 5
                            for key, caption in r13_rec_available(r13_recommended):
                                textbutton caption action Return(key) xsize 578 text_size 20
                    $ commands = r13_rec_controls(r13_recommended); command_rows = (len(commands)+1)//2
                    grid 2 command_rows:
                        spacing 6
                        for command, caption in commands:
                            textbutton caption xsize 285 text_size 18 action (ShowMenu("save") if command=="save" else MainMenu(confirm=True) if command=="title" else Return(command))
                        if len(commands)%2:
                            null
                vbox:
                    xsize 525 spacing 8
                    textbutton "QA 전용 새 이야기 · 미검증 gate 시험" action Return("native_qa_start") text_size 17
                    textbutton "회의 연출 시연 · 미적용" action Return("staging_preview") text_size 18
                    text "확인한 물증 · 인물 카드" size 24
                    viewport:
                        ysize 440 mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 8
                            for key in r13_recommended["facts"]:
                                textbutton r13_rec_cards[key][0] action Return("card:"+key) xsize 490 text_size 20

screen r13_recommended_cards(question):
    use r13_recommended_catalog(question)

label r13_recommended_start:
    call screen r13_recommended_setup
    $ room13_mode = True
    $ winter_mode = True
    $ winter = winter_new()
    $ source_mode = False
    $ room13 = r13_new()
    $ r13_rec_stage_memory = {}
    $ r13_recommended = r13_rec_opening_state()
    $ room13["campaign_id"] = "room13_recommended_v1"
    $ room13["day"] = r13_recommended["day"]
    $ r13_upgrade()
    $ r13_scene_key = None
    $ r13_world_cameras = {}
    $ r13_inspection_location = None
    $ room13["learning_archive"] = r13_learning_archive_seed()
    $ typing_allowed = True
    hide screen r13_hud
    hide screen winter_hud
    hide screen hud
    call r13_recommended_carriage_opening
    jump r13_recommended_hub

label r13_recommended_read_card:
    call screen r13_recommended_card_detail(r13_recommended_choice.split(":",1)[1])
    call screen r13_recommended_notebook
    if _return is not None:
        $ r13_recommended_choice = _return
        jump r13_recommended_read_card
    jump r13_recommended_hub

label r13_recommended_hub:
    $ r13_rec_stage_exit()
    if r13_recommended is None or r13_recommended.get("revision") != r13_rec_revision:
        call r13_lines([(None,"이 검증판 저장은 현재 이야기 버전과 다릅니다. 사실을 자동으로 바꾸지 않습니다. 제목 화면의 추천 스토리에서 새로 시작해 주세요.")], "recommended:version")
        return
    call r13_recommended_pick
    $ r13_recommended_choice = _return
    if r13_recommended_choice == "native_qa_start":
        jump r13_recommended_native_qa_start
    if r13_recommended_choice == "staging_preview":
        call r13_recommended_staging_admin
        jump r13_recommended_hub
    if r13_recommended_choice.startswith("card:"):
        jump r13_recommended_read_card
    if r13_recommended_choice == "evening":
        if r13_recommended["episode"] == 1 and r13_recommended["day"] == 2 and not {"heat_seen","piko_plan"} <= set(r13_recommended["done"]):
            call r13_lines([("dad","낮 점검과 피코 씨의 계획을 먼저 확인하자.")], "recommended:evening:before")
            jump r13_recommended_hub
        if r13_recommended["episode"] == 3 and r13_recommended["day"] == 5 and not r13_recommended["e3_school_handoff"]:
            menu:
                "저녁까지 기다리면 아직 하지 않은 낮 활동은 지나갑니다. 기다릴까요?"
                "아직 낮에 할 일을 한다":
                    jump r13_recommended_hub
                "저녁까지 기다린다":
                    pass
        $ r13_recommended = r13_rec_evening(r13_recommended)
        $ room13["period"] = 2
        call r13_lines([(None,"마을의 저녁 등불이 켜졌다. 낮에 보았던 곳도 지금은 다른 사람들이 쓰고 있었다.")], "recommended:evening")
        jump r13_recommended_hub
    if r13_recommended_choice == "advance":
        $ r13_recommended_block = r13_rec_block_reason(r13_recommended)
        if r13_recommended_block:
            call r13_lines([("dad",r13_recommended_block)], "recommended:day:open")
            jump r13_recommended_hub
        menu:
            "오늘을 마칠까요? 오늘 가능한 예방 행동을 놓칠 수 있습니다."
            "아직 조사한다":
                jump r13_recommended_hub
            "다음 날로 간다":
                $ r13_recommended = r13_rec_next_day(r13_recommended)
                $ room13["day"] = r13_recommended["day"]
                $ room13["period"] = r13_recommended.get("period",0)
        if r13_recommended["episode"] == 1 and r13_recommended["day"] == 3:
            call r13_scene("winter_square", "3일 아침 · 광장", "quiet")
            if r13_recommended["piko"] == "safe":
                call r13_scene("council", "3일 아침 · 여관 식당", "calm")
                call r13_lines([(None,"식당에서 피코가 붓을 털었다. 밤새 말린 초상을 다람에게 건넸다."),("resident_piko","약속한 그림이에요. 그분을 본 곳은 기록실 앞이 맞아요. 이름이나 지금 계신 곳까지는 모르지만요."),("daram","고마워요. 엄마한테 이것도 보여 줄래요." if r13_recommended["mother"]=="M2" else "고마워요. 엄마 만나면 이것도 보여 줄래요.")], "recommended:piko:portrait")
                call r13_scene("winter_square", "3일 아침 · 광장", "quiet")
                call r13_lines([(None,"식당을 나서자 광장 쪽에서 초롱의 목소리가 들렸다. 3번 등 뚜껑이 열려 있었고, 안은 비어 있었다."),("resident_lamplighter","돌이 없어졌어요. 어젯밤 여기서 주무셨으면 큰일 날 뻔했어요."),("resident_piko","어제는 우리가 자리를 옮겼죠. 제가 저기서 자려고 했다는 건 직접 말할게요."),("dad","그림도 고맙습니다. 우리가 아는 어제 일부터 함께 확인하죠.")], "recommended:piko:safe")
            else:
                call r13_lines([(None,"약속한 그림을 받으러 광장에 갔다. 초롱이 3번 등 아래에 무릎을 꿇고 있었다."),("resident_lamplighter","피코 씨, 들려요? 누구 진료소에 가 주세요!"),(None,"부리가 달려갔다. 다람이 아빠의 소매를 잡았다. 피코의 손 옆에는 어제 그리던 초상이 마른 채 놓여 있었다."),("daram","아빠, 어제 여기서 잔다고 했잖아."),("dad","응. 다람아, 아빠 곁에 있자."),(None,"서리 검사원이 와서 피코를 살폈다. 오래 살핀 뒤 고개를 저었다."),("resident_seori","너무 늦었습니다. 밤 추위를 견디지 못한 것으로 보입니다. 자세한 경과는 더 살펴야 합니다."),(None,"초롱이 피코에게 천을 덮었다. 약속한 초상은 젖지 않도록 아빠에게 건넸다."),("resident_lamplighter","이걸 드리려고 그렸다고 했어요. 돌까지 없어질 줄은 몰랐어요."),("dad","아내를 봤다고 말해 준 분이었는데…. 어제 계획과 오늘 빈 등이 어떻게 이어지는지 알고 싶습니다. 제가 직접 본 것도 있어요.")], "recommended:piko:dead")
            call r13_lines([("resident_ppul","내일 아침 식당에 모입시다. 돌이 어디로 갔는지, 누구에게 어떤 위험이 남았는지 확인해야겠소."),("resident_lamplighter","어제 점검 때 두 분도 계셨지요. 만진 곳과 안에서 본 것을 나눠 말해 주세요."),("dad","그러겠습니다. 오늘은 현물과 실제 본 사람의 말을 확인하겠습니다.")], "recommended:meeting:invitation")
        jump r13_recommended_hub
    if r13_recommended_choice == "next_episode":
        $ r13_recommended = r13_rec_begin_episode(r13_recommended, r13_rec_next_available(r13_recommended))
        $ room13["day"] = r13_recommended["day"]
        jump r13_recommended_hub
    if r13_recommended_choice == "hearing":
        jump expression r13_rec_episodes[r13_recommended["episode"]]["hearing_label"]
    $ room13["day"] = r13_recommended["day"]
    $ r13_recommended_spec = r13_rec_actions[r13_recommended_choice]
    $ r13_recommended_place = r13_recommended_spec["place"]
    $ r13_recommended_background = (r13_recommended_spec.get("background_key") or r13_rec_location_info(r13_recommended_place,r13_recommended)[1])
    call r13_scene(r13_recommended_background, r13_recommended_spec["title"], "calm")
    call r13_lines(r13_rec_action_lines(r13_recommended,r13_recommended_choice), "recommended:"+r13_recommended_choice)
    if r13_recommended_spec.get("label"):
        call expression r13_recommended_spec["label"]
        if _return is False:
            jump r13_recommended_hub
    $ r13_recommended = r13_rec_apply(r13_recommended, r13_recommended_choice)
    if r13_recommended_choice == "shelter":
        call r13_lines([(None,"세 사람의 식사가 같은 상 위에 놓였다. 다람이 이불 세 자리를 손으로 짚으며 세었다."),("daram","하나, 둘, 셋. 오늘은 아무도 다른 데 가면 안 돼."),("mom","응. 오늘은 여기 같이 있자.")], "recommended:family:complete")
    jump r13_recommended_hub

label r13_recommended_hearing:
    if not r13_rec_hearing_ready(r13_recommended):
        call r13_lines([("dad","피코 씨가 기대고 있던 등이 왜 비었는지 알고 싶어요. 따뜻한 등 안을 직접 본 일, 돌의 번호, 돌을 건네받은 사람의 말을 더 확인해야겠어요.")], "recommended:hearing:missing")
        jump r13_recommended_hub
    call r13_scene("council", "4일 · 광장의 돌 공개 회의", "calm")
    $ r13_rec_stage_enter(1)
    if "piko_container_exclusive_claim" not in r13_recommended["done"]:
        call r13_lines([("resident_ppul","돌을 받은 아이의 말은 들었소. 이제 광장의 등을 누가 열었는지 설명해 주시오."),("nabi","아이들에게 돌을 가져다준 건 맞아요. 하지만 등에서 꺼낸 건 아니에요. 밖에 놓여 있던 돌을 주워 담았어요."),("dad","그럼 돌을 담기 전이나 아이에게 주기 전에, 그 용기나 깔개 천을 다른 사람에게 맡긴 적은 있습니까?"),("nabi","아니요. 꼬미에게 빈 통을 빌린 뒤 지금까지 줄곧 제가 들고 다녔어요. 천도 저만 썼어요. 등 뚜껑을 열거나 안을 닦은 적도 없고요."),(None,"나비가 오늘 배식에 쓰던 용기와 천을 탁자 위에 놓았다. 초롱도 광장의 등을 가져와 나란히 놓았다."),("nabi","제 설명이 맞는지 이것도 봐 주세요."),("dad","그 말씀이군요. 아이에게 넘긴 일과 등에서 꺼낸 일을 구별해서 보겠습니다.")], "recommended:hearing:new-defense")
        $ r13_recommended = r13_rec_piko_hear_defense(r13_recommended)
        if "cloth_contact_matched" in r13_recommended["done"]:
            call r13_lines([("dad","먼저 맞춰 본 천 조각이 마음에 걸렸어. 이제 나비 씨가 말한 운반 과정과도 맞춰 보자.")], "recommended:hearing:prior-deduction")
    if "piko_source_claim_early" in r13_recommended["done"]:
        call r13_lines([(None,"초롱이 광장의 등을 회의 탁자에 내려놓았다."),("nabi","먼저 보여드렸던 통과 천을 다시 가져왔어요."),("dad","그때 들은 설명도 기억합니다. 밖의 돌만 담았고, 용기와 천은 혼자 쓰셨다고 했지요.")], "recommended:hearing:earlier-account")
        if "cloth_contact_matched" in r13_recommended["done"] and r13_rec_piko_geometry_ready(r13_recommended):
            menu (screen="r13_rec_stage_choice"):
                "이미 직접 확인한 대조를 어떻게 설명할까?"
                "확인한 흔적과 나비의 설명을 잇는다":
                    call r13_lines([("dad","돌을 받은 사람과 17번 번호를 먼저 확인했고, 그다음 허락받은 천을 맞춰 봤어요. 뚜껑 안쪽 조각과 이어졌지요. 꼬미가 빌려줄 때 펼친 천은 온전했고, 그날 돌을 내려놓을 때 그 모서리는 이미 찢어져 있었어요. 그 사이 혼자 쓰셨고 등 안에는 손대지 않았다고 하셨지요. 그 찢김이 뚜껑 안쪽 조각과 이어집니다. 밖의 돌만 담았다는 설명과는 맞지 않아요.")], "recommended:hearing:prior-case")
                    $ r13_recommended = r13_rec_piko_summarize_prior(r13_recommended)
                "자료를 하나씩 나란히 보여 준다":
                    pass
    if "cloth_contact_matched" not in r13_recommended["done"]:
        menu (screen="r13_rec_stage_choice"):
            "나비가 가져온 천을, 미리 확인한 등 안쪽 조각과 맞춰 볼까?"
            "허락받은 천의 찢김과 안쪽 조각을 맞춰 본다":
                call r13_recommended_contact_inspect
                if _return:
                    $ r13_recommended = r13_rec_apply(r13_recommended,"contact_match")
            "우선 들은 말과 돌의 이동부터 정리한다":
                pass
    while r13_recommended["hearing"] < len(r13_rec_hearing_steps(r13_recommended)):
        $ r13_rec_stage_step = r13_rec_hearing_steps(r13_recommended)[r13_recommended["hearing"]][1]
        $ r13_rec_stage_prompt(r13_rec_stage_step)
        call screen r13_recommended_cards(r13_rec_hearing_steps(r13_recommended)[r13_recommended["hearing"]][0])
        if _return is None:
            jump r13_recommended_hub
        $ r13_recommended, r13_recommended_feedback, r13_recommended_correct = r13_rec_present(r13_recommended, _return)
        $ r13_rec_stage_answer(r13_rec_stage_step,r13_recommended_correct)
        call r13_lines([("dad",r13_recommended_feedback)], "recommended:hearing:answer")
    if r13_recommended["verdict"] == "direct_removal":
        call r13_lines([("nabi","제가 그 천으로 돌을 들어서 용기에 넣었어요. 아이들 자리를 덥히려고 가져갔어요."),("dad","나비 씨가 돌을 옮긴 건 알겠어요. 앞으로는 가져가는 사람과 받는 사람이 함께 알려 주세요. 하지만 이걸로 피코 씨를 해치려 했다고 말할 수는 없어요."),("resident_ppul","나비는 배식을 계속 맡으시오. 공공 물자를 옮길 때는 인계 상대와 함께 확인하고 기록을 남기시오.")], "recommended:hearing:direct-removal")
    else:
        call r13_lines([("nabi","아이들이 추워서 돌을 갖다줬어요. 피코 씨에게는 자리를 옮기라고 말하지 못했어요."),("dad","아이들을 먹이는 일은 계속 맡아 주세요. 대신 공공 돌을 옮길 때는 함께 확인하고 어디에 놓았는지 알려야 합니다."),("dad","아이에게 돌을 준 건 알겠어요. 광장에서 직접 꺼냈는지는 아직 더 봐야겠어요. 두 일을 같은 말로 넘기지는 않을게요."),("resident_ppul","나비는 배식을 계속 맡으시오. 공공 물자를 옮길 때는 인계 상대와 함께 확인하고 기록을 남기시오."),("nabi","알겠어요. 오늘 아이들 식사부터 준비할게요.")], "recommended:hearing:result")
    if r13_recommended["piko"] == "safe":
        call r13_lines([("resident_piko","그때 옮겨 준 덕분에 여기서 직접 말할 수 있네요.")], "recommended:hearing:survivor")
    call r13_lines([(None,"회의가 끝나자 사람들이 자리에서 일어났다. 나비는 주방으로 돌아갔다. 다람이 아빠 손을 잡았다."),("daram","아빠, 이제 우리 할 일 하러 가자.")], "recommended:slice:end")
    jump r13_recommended_hub
''')
p = root/'game/systems/room13_recommended_story.rpy'
p.write_text(p.read_text() + (root/'dev/contact_scene.rpy').read_text())

p = root/"game/systems/room13_recommended_field.rpy"
p.write_text((root/"dev/field_ui.rpy").read_text())
