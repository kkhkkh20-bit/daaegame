default r13_carriage_skip = False
# 0.18.46 (owner): "건너뛰기" ends the current conversation block at once. Grants, flags and
# progress after the block still run; only the remaining lines are not shown.
default r13_conv_skip = False

# Full campaign entry and first-week scenes; continuation is in room13_week2.rpy.
label r13_scene(bg,title,mood="calm"):
    $ r13_meeting_direct_end()
    $ r13_cg_active = False
    $ r13_last_partner = None
    window hide
    hide r13_visitor
    hide winter_visitor
    hide visitor
    $ dialogue_speaker=None
    $ dialogue_expression="neutral"
    $ place=title
    $ r13_scene_bg=bg
    $ r13_camera="stage"
    $ source_pulse(False)
    $ renpy.music.stop(channel="typing")
    $ renpy.music.stop(channel="scene_fx")
    if r13_scene_key==r13_scene_identity(bg,title,mood):
        return
    scene black with Dissolve(.18)
    call r13_arrival(bg,title,mood)
    $ r13_music=r13_sound_scene_music(bg,title,mood)
    if r13_music:
        if renpy.music.get_playing()!=r13_music:
            $ renpy.music.play(r13_music,fadeout=.2,fadein=.2)
    else:
        stop music fadeout .2
    # 0.18.91: a quiet scene keeps its place music low instead of silence.
    $ renpy.music.set_volume(.5 if mood=="quiet" else 1.0,delay=.6,channel="music")
    $ renpy.pause(.25)
    # A new day or time slot fades in through a 4x4 dither (systems/room13_dot_fx.rpy).
    scene expression r13_background(bg) with r13_scene_transition()
    $ r13_scene_key=r13_scene_identity(bg,title,mood)
    return

label r13_lines(entries,identity,binding_route=None):
    $ r13_index=0; r13_dialogue_binding=r13_bind_dialogue_rows(entries,identity,binding_route,R13_DIALOGUE_BINDINGS)
    $ r13_conv_skip=False
    while r13_index<len(entries) and not r13_conv_skip and not r13_meeting_live_should_stop(identity) and not ((identity==R13_CARRIAGE_IDENTITY or (r13_v111_active() and place=="마차 안")) and r13_carriage_skip):
        $ r13_packet=r13_dead_stand_in_packet(r13_pov_packet(entries[r13_index]),identity)
        $ r13_thought_active=bool(len(r13_packet)>2 and isinstance(r13_packet[2],dict) and r13_packet[2].get("thought"))
        $ r13_expression,r13_directed_pose=r13_line_performance(identity,r13_index,r13_packet)
        $ r13_expression,r13_directed_pose=r13_meeting_direct_line(identity,r13_index,r13_packet,r13_expression,r13_directed_pose)
        if r13_thought_active:
            $ r13_expression,r13_directed_pose="thinking","thinking"
        $ r13_dialogue_beat_begin(identity,r13_index,r13_packet,r13_directed_pose)
        # 0.18.56 (owner): someone who "comes over" in the opening narration is on screen
        # from that line, not only from their first spoken line.
        # 2026-10-27 소유자: 아빠 생각(괄호) 줄인데 뒤에 말할 다람이 미리 서 있었다. 생각 줄에서는 아무도 세우지 않는다.
        if r13_packet[0] in (None,r13_viewpoint()) and not r13_thought_active and "r13_visitor" not in renpy.get_showing_tags() and not (len(r13_packet)>2 and isinstance(r13_packet[2],dict) and r13_packet[2].get("no_lead")):
            $ r13_lead=next((p[0] for p in entries[r13_index:] if p[0] not in (None,r13_viewpoint()) and p[0] in CAST and not (len(p)>2 and isinstance(p[2],dict) and p[2].get("thought"))),None)
            if r13_lead:
                $ r13_speaker(r13_lead,"neutral")
        # 0.18.89: a narration line can bring someone on screen who has no line of their
        # own (e.g. {"show":"chorong_mother","pose":"offer_lantern"}); narration keeps them.
        if r13_packet[0] is None and len(r13_packet)>2 and isinstance(r13_packet[2],dict) and r13_packet[2].get("show") in CAST:
            $ r13_speaker(r13_packet[2]["show"],r13_packet[2].get("expression","neutral"),r13_packet[2].get("pose") or r13_packet[2].get("expression","neutral"))
        # 0.18.89: picture book / scene cut for this line (systems/room13_ep_art.rpy).
        $ r13_ep_line_art(r13_packet)
        $ r13_speaker(r13_packet[0],r13_expression,r13_directed_pose)
        if r13_packet[0] not in (None,r13_viewpoint()) and not r13_thought_active:
            $ r13_last_partner=r13_packet[0]
        $ r13_meeting_prepare_live_line(identity)
        $ r13_read_id=r13_before_line(identity,r13_index,r13_packet[1])
        # Isolate this line from the previous loop increment when record UI
        # changes are retained by an immediate save during the say interaction.
        $ renpy.checkpoint()
        # Four or more lines on screen: show two lines per click (systems/room13_linebreak.rpy).
        $ r13_pages=r13_dialogue_pages(r13_packet[1])
        $ r13_page_i=0
        while r13_page_i<len(r13_pages) and not r13_conv_skip and not r13_meeting_live_should_stop(identity) and not ((identity==R13_CARRIAGE_IDENTITY or (r13_v111_active() and place=="마차 안")) and r13_carriage_skip):
            $ R13_CHARS.get(r13_packet[0],source_thought)(r13_line_markup(r13_pages[r13_page_i]))
            $ r13_dialogue_beat_settle()
            $ r13_page_i+=1
        if not r13_meeting_live_should_stop(identity) and not ((identity==R13_CARRIAGE_IDENTITY or (r13_v111_active() and place=="마차 안")) and r13_carriage_skip):
            $ r13_remember_line(r13_read_id)
            $ r13_meeting_mark_heard(identity,r13_index)
        $ r13_index+=1
    $ r13_dialogue_beat_settle()
    hide r13_visitor
    $ r13_ep_line_art_clear()
    $ dialogue_speaker=None
    $ r13_thought_active=False
    $ r13_conv_skip=False
    return

label room13_start:
    $ r13_meeting_direct_end()
    $ r13_meeting_direction_seen=[]
    $ room13_mode=True
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ room13=r13_new()
    $ r13_world_cameras={}
    $ r13_inspection_location=None
    $ r13_prepare_history()
    $ room13["learning_archive"] = r13_learning_archive_seed()
    $ r13_scene_key=None
    $ r13_upgrade()
    $ typing_allowed=True
    hide screen winter_hud
    hide screen hud
    hide screen source_world
    hide screen source_proof
    hide screen r13_handoff
    hide screen r13_book
    hide screen r13_calendar
    show screen r13_hud
    jump r13_v111_start # Updated story; original labels remain available to old saves.
    call r13_carriage
    $ r13_grant(["E01"],"여행 중 가지고 온 편지")
    $ r13_edit(period=1)
    call r13_scene("winter","눈에 막힌 입구","calm")
    $ r13_note_encounter("karo")
    $ r13_note_encounter("guard")
    $ r13_note_encounter("daram")
    call r13_lines([('daram', '안아 주지는 마.'), ('dad', '손만 잡을게.'), ('karo', '큰 짐은 두고 가세요. 축에 금이 갔네. 돌아가는 건 수리부터 해야겠어요.'), ('dad', '어디로 가면 됩니까?'), ('karo', '초소요. 방문 확인 먼저.')],"entry:karo:arrival")
    call r13_lines([('guard', '성함.'), ('dad', '다돌입니다. 딸하고 왔습니다.'), ('guard', '아버지만 들어가실 수 있소. 아이는 일꾼으로 받을 수 없소.'), ('dad', '일꾼이요? 아내 만나러 왔는데요.'), ('guard', '내게 온 종이엔 그렇게 적혀 있소.'), ('dad', '그럼 얘는 어쩌고요?'), ('guard', '혼자 두라는 말 아니오. 둘 다 여기서 기다리시오.'), ('daram', '아빠, 나 때문에 못 들어가?'), ('dad', '아니야. 잘못 적힌 게 있나 봐. 같이 보자.')],"entry:arrival")
label r13_entry:
    hide r13_visitor
    $ dialogue_speaker=None
    window hide
    call screen r13_hub(entry=True)
    $ r13_choice=_return
    # 0.18.79: a hub result is always a (kind, value) pair. Anything else is not a choice:
    # show the same screen again (no time, record or story step), and stop with an error after
    # repeated bad results instead of looping (systems/room13_boot_guard.rpy).
    if not r13_screen_choice_ok(r13_choice,"r13_hub:entry"):
        jump r13_entry
    if r13_choice[0]=="person":
        if r13_choice[1]=="guard":
            jump r13_entry_guard_menu
        else:
            call r13_entry_person(r13_choice[1])
            jump r13_entry
    if r13_choice==("entry","talk"):
        jump r13_entry_guard_menu
    jump r13_entry_dispatch

label r13_entry_guard_menu:
    $ r13_note_encounter("guard")
    window hide
    hide r13_visitor
    $ dialogue_speaker=None
    call screen r13_entry_topics
    $ r13_choice=_return
    if not r13_screen_choice_ok(r13_choice,"r13_entry_topics"):
        jump r13_entry_guard_menu
    if r13_choice != ("entry","back"):
        $ r13_speaker("guard","neutral")
label r13_entry_dispatch:
    if r13_choice==("entry","explain"):
        call r13_lines([(None, '초소 입장 명단: 같은 도착일 / 다돌 / 신청 2명 / 신규 일꾼 본인 1명 / 동행 아동 모집 제외 / 내일부터 장작 운반 / 처리 너울.'), ('dad', '장작이요? 그런 신청 안 했습니다. 제가 낸 종이부터 보여 주세요.'), ('guard', '날짜와 이름을 찾으면 되오. 잠깐 기다리시오.')],"entry:explain:v2")
        $ r13_flag("question_read:entry:explain")
        # The list is earned by asking for it; granted after the lines (0.18.22).
        $ r13_grant(["G3"],"돌목이 직접 보여 준 초소 명단")
    elif r13_choice[0]=="object":
        call r13_object(r13_choice[1])
    elif r13_choice[0]=="empty":
        $ r13_mark("empty:%d:%d"%(r13_choice[1][0]//70,r13_choice[1][1]//70),*r13_choice[1])
        call r13_lines([(None,"흩날리는 눈을 털어 냈다. 특별히 눈에 띄는 흔적은 없다.")],"entry:empty")
    elif r13_choice[1]=="argue":
        call screen r13_book("guard",present=True)
        $ r13_item=_return
        if r13_catalog_object(r13_item):
            call r13_show_catalog_object("guard",r13_item)
            jump r13_entry_guard_menu
        if r13_item:
            show screen r13_material_corner(r13_item)
        if r13_item in ("G1","G3"):
            if r13_item == "G1" and all(key in room13["evidence"] for key in ("G2","G3")):
                call r13_lines([('dad', '가족 방문이고 둘이 잘 방도 확인됐습니다. 저 규칙대로 딸도 들여보내 주세요.'), ('guard', '가족 방문을 일꾼으로 옮겨 놨군.'), ('dad', '네. 그래서 아이가 빠졌습니다.'), ('guard', '여기서 고치겠소.')],"entry:corrected:v2")
                jump r13_entry_done
            else:
                call r13_lines([('guard', '둘인 건 봤소. 가족을 만나러 왔는지, 둘이 잘 방은 있는지도 확인해야 하오.')],"entry:copy:v2")
        elif r13_item == "G2":
            call r13_lines([('guard', '같이 온 건 알겠소. 둘이 묵을 방은 확인됐소?')],"entry:rules:v2")
        elif r13_item:
            call r13_lines([('dad', '이 편지도 있습니다.'), ('guard', '초대받은 건 알겠소. 두 사람이 묵을 방도 확인해야 하오.'), ('dad', '여관으로 신청했습니다. 원본을 찾아 주십시오.')],"entry:letter")
        hide screen r13_material_corner
    elif r13_choice[1]=="wait":
        call screen r13_confirm("대기소 앞에서 원본 담당자가 돌아오기를 기다린다.")
        if _return:
            $ r13_flag("question_read:entry:wait")
            call r13_scene("winter","눈에 막힌 입구","calm")
            call r13_lines([('dad', '가족 방문이고 둘이 잘 방도 확인됐습니다. 저 규칙대로 딸도 들여보내 주세요.'), ('guard', '가족 방문을 일꾼으로 옮겨 놨군.'), ('dad', '네. 그래서 아이가 빠졌습니다.'), ('guard', '여기서 고치겠소.')],"entry:wait")
            jump r13_entry_done
    if r13_choice[0]=="entry" and r13_choice[1] in ("explain","argue","wait"):
        jump r13_entry_guard_menu
    jump r13_entry

label r13_entry_person(person):
    if person in ("daram", "karo"):
        $ r13_note_encounter(person)
    if person=="daram":
        call r13_lines([('daram', '여기 아빠 이름.'), ('dad', '맞아. 날짜도 같네.'), ('daram', '‘외 한 명’은 나야? 내 이름도 썼는데.'), ('dad', '아래에 있네. 다람. 둘이 온다고 제대로 썼어.')],"entry:daram:waiting")
        call r13_entry_daram_menu from r13_entry_daram_questions_return
        return
    if person!="karo":
        $ r13_target=person
        call r13_talk
        return
label r13_entry_karo_menu:
    window hide
    hide r13_visitor
    call screen r13_entry_karo_topics
    $ r13_entry_karo_choice=_return
    if r13_entry_karo_choice != "back":
        $ r13_speaker("karo","neutral")
    if r13_entry_karo_choice=="road":
        call r13_lines([('dad', '아까 보신 마차 바퀴 축은 수리가 되겠습니까?'), ('karo', '고쳐야죠. 금 간 곳을 우선 묶어 두긴 했는데, 이대로 손님을 태울 수는 없어요.'), ('dad', '수리가 끝나면 바로 돌아갈 수 있습니까?'), ('karo', '마차만 고친다고 갈 수 있는 게 아닙니다. 고갯길도 폭설로 막혔거든요. 길이 열리면 가장 먼저 알려 드릴게요.')],"entry:karo:road")
        $ r13_flag("road_known")
    elif r13_entry_karo_choice=="witness":
        call r13_lines([('dad', '까로 씨, 저희 두 사람을 태워 오셨다고 증언해 주실 수 있습니까? 명단에서 아이 이름이 빠져서요.'), ('karo', '그럼요. 제 마차에 두 분 다 타셨습니다. 짐도 제가 직접 내려 드렸고요.'), ('guard', '함께 타고 오신 건 알겠습니다. 하지만 명단을 고치려면 예약 서류 원본과 대조해 봐야 합니다.'), ('dad', '알겠습니다. 그럼 원본 서류부터 찾아보겠습니다.'), ('karo', '아, 손님 예약 서류는 아까 제가 초소에 넘겼어요. 선반 금요일 묶음에 끼워 두더라고요.'), ('karo', '저는 여기서 짐을 지키고 있을게요. 확인이 끝나면 불러 주세요.')],"entry:karo:witness:v2")
    elif r13_entry_karo_choice=="bags":
        call r13_lines([("karo","가방은 이 담요 밑에 넣어 둘게요. 눈에 젖으면 방에 가서도 한참 말려야 하니까요.")],"entry:karo:bags")
    elif r13_entry_karo_choice=="present":
        call screen r13_book("karo",present=True)
        $ r13_item=_return
        if r13_catalog_object(r13_item):
            call r13_show_catalog_object("karo",r13_item)
        elif r13_item:
            $ r13_defer_grants=True
            $ r13_reaction=r13_present("karo",r13_item)
            $ r13_defer_grants=False
            show screen r13_material_corner(r13_item)
            call r13_lines(r13_reaction,"entry:karo:present:"+r13_item, binding_route="dynamic:013")
            hide screen r13_material_corner
            $ r13_flush_grants()
    elif r13_entry_karo_choice=="back":
        hide r13_visitor
        $ dialogue_speaker=None
        return
    if r13_entry_karo_choice in ("road","witness","bags"):
        $ r13_flag("question_read:entry:karo:"+r13_entry_karo_choice)
    jump r13_entry_karo_menu

label r13_entry_done:
    hide screen r13_material_corner
    $ r13_inspection_location=None
    $ r13_grant(["E02"],"원본과 맞춰 보고 바로잡은 입장 기록")
    $ r13_flag("entry_corrected")
    call r13_lines([(None, '여관에 들어간 뒤 묵는 곳을 옮기면 알려 주시오.'), ('dad', '아내 만나고 정하겠습니다.'), (None, '부인이 나타나도 여관에 먼저 연락해 달라고 했소, 돌목 씨.'), ('guard', '지금은 이 두 사람 등록 중이오.')],"entry:departure")
    if room13.get("life_poc"):
        call r13_lines([("daram","아빠, 이제 빨리 여관 가자. 엄마가 기다릴 거야."),("dad","그래. 13호실이라고 했지.")],"life:arrival:direction") from r13_intro_direction_return
    jump r13_roam

label r13_carriage:
    $ r13_carriage_skip = False
    call r13_carriage_departure
    call r13_lines([(None, '다람이 과자 봉지를 외투 안쪽으로 당긴다.'), ('dad', '아빠는 안 잡아 줘?', {'carriage_jolt':True}), ('daram', '아빠는 안 부서지잖아.'), ('dad', '부서질 수도 있는데.'), (None, '아이가 내 소매를 붙잡았다. 빈손으로만.'), ('dad', '많이 남았어?'), ('daram', '하나. 엄마 거.'), ('dad', '제일 큰 거네.'), ('daram', '엄마는 못 먹었잖아.'), ('daram', '또 읽어?', {'carriage_letter':True}), ('dad', '방 번호.'), ('daram', '십삼 호. 내가 외웠어. 아빠는 짐 들어.'), ('daram', '오늘은 엄마랑 자?', {'carriage_letter':False}), ('dad', '엄마부터 만나 보자.'), ('daram', '만나면 내가 가운데야.'), ('karo', '지붕 보입니다. 일어나지 마요. 아직 안 섰어요.', {'carriage_reveal':True}), (None, '다람이를 데리고 와 줘. 여관 13호실에서 기다릴게.')],R13_CARRIAGE_IDENTITY, binding_route="dynamic:016")
    $ persistent.room13_opening_seen=True; r13_carriage_finish()
    $ r13_carriage_skip = False
    return

label r13_day:
    if room13["day"]==R13_CASE_DAY and not r13_has("elder_appointment"):
        call r13_scene("hall","여관 계단","calm")
        call r13_lines([("resident_owlgp","저녁에 댁이 묵는 방으로 들르겠소. 부인에게 맡아 둔 물건을 돌려드려야겠소."),("dad","제 아내에 관한 물건입니까?"),("resident_owlgp","보관해 달라고 맡긴 기록이오. 부인이 지금 어디 있는지는 나도 모르오."),("granny","되돌아온 짐을 찾으러 마을 입구에 나가신다면서요. 그동안 내가 아이랑 같이 있어 줄게요."),("daram","할아버지 물건은 받아만 둘게. 아빠 돌아오면 같이 열어 보자."),("dad","가능하면 할아버지가 오시기 전에 돌아오겠습니다."),("resident_owlgp","물건만 먼저 전해 두리다. 자세한 이야기는 다 같이 모여서 합시다.")],"day4:appointment:v3")
        $ r13_flag("elder_appointment")
    if room13["day"]==R13_CASE_DAY+1 and room13["case_state"]=="occurred" and not r13_has("trial_notice"):
        call r13_scene("front","여관 접수대","quiet")
        call r13_lines([("neoul","일요일에 주민들을 모아 놓고 이번 사건을 다룰 겁니다. 아이는 그때까지 초소 보호실에 격리해 둡니다."),("dad","범인인지 밝혀지지도 않았는데 아이를 가두기부터 합니까?"),("neoul","사건 현장에 단둘이 있던 아이를 그냥 데려가시면 마을 사람들이 가만있지 않습니다. 면회하러 오시는 건 막지 않겠습니다."),(None,"인원수를 바로잡은 출입 기록 원본은 돌려받았다. 하지만 두 사람이 함께 들어왔다는 증명과, 지금 아이가 받는 살인 혐의는 별개의 문제였다.")],"day5:notice")
        $ r13_flag("trial_notice")
    if room13["day"]==R13_TRIAL_DAY:
        jump r13_trial
    if room13["day"]>=R13_WEEK2_DAY:
        jump r13_week2_day
    jump r13_roam

label r13_roam:
    $ r13_life_field_active=False; r13_upgrade()
    if room13.get("revision_restart_required"):
        jump r13_revision_resume
    # 0.18.83: 사건 다음 날 엄마가 진료소에 나타나던 장면(r13_mother_intervention)은 부르지 않는다.
    #   새 이야기에서 엄마는 11일 새벽에 처음 다시 만난다(에피소드 ⑤). 그사이 소식은 초롱의 편지로 온다(④).
    if room13["day"]>=R13_WEEK2_DAY:
        call r13_week2_events
    # Evening missions (systems/room13_evening.rpy): once per evening, pick where to go.
    call r13_evening_auto
    if _return and _return!=room13["location"]:
        $ r13_edit(location=_return)
        jump r13_roam
    # Town events (systems/room13_town_events.rpy); a night locked away ends the day.
    call r13_town_events
    if _return=="day":
        jump r13_day
    if room13["day"]==R13_CASE_DAY and room13["period"]>=2 and room13["case_state"]=="pending":
        jump r13_case_choice
    $ place=R13_PLACES[room13["location"]][0]
    call r13_scene(R13_PLACES[room13["location"]][1],place,"night" if room13["period"]>=2 else "search" if room13["case_state"]=="occurred" else "calm")
label r13_field:
    window hide
    $ renpy.hide("r13_visitor"); r13_life_field_active=True
    call screen r13_hub
    $ r13_choice=_return; r13_life_field_active=r13_life_choice_is_group(r13_choice)
    if not r13_screen_choice_ok(r13_choice,"r13_hub"):
        jump r13_field
    if r13_choice[0]=="livelihood":
        call r13_livelihood
        jump r13_roam
    if r13_choice[0]=="sleep":
        call r13_sleep_in_room
        if _return=="slept":
            jump r13_day
        elif _return=="case":
            jump r13_case_choice
        jump r13_roam
    if r13_choice[0]=="offer":
        call r13_take_offer(r13_choice[1])
        if _return=="day":
            jump r13_day
        jump r13_roam
    if r13_choice[0]=="object":
        call r13_object(r13_choice[1])
        call r13_object_options(r13_choice[1])
        if _return=="slept":
            jump r13_day
        elif _return=="case":
            jump r13_case_choice
        jump r13_roam
    if r13_choice[0]=="empty":
        $ r13_mark("empty:%d:%d"%(r13_choice[1][0]//70,r13_choice[1][1]//70),*r13_choice[1])
        call r13_lines([(None,"발밑과 벽면을 꼼꼼히 살폈다. 이 자리에는 특별히 눈에 띄는 흔적이 없다.")],"field:empty:"+room13["location"], binding_route="dynamic:019")
        jump r13_field
    if r13_choice[0] in ("person","life_group","life_child"):
        $ r13_target=r13_choice[1]
        call r13_life_field_person_dispatch
        jump expression ("r13_field" if r13_choice[0] in ("life_group","life_child") else "r13_roam")
    if r13_choice[0]=="travel":
        $ r13_destination=r13_local_destination(r13_choice[1])
        if r13_destination=="outside":
            call screen r13_map(initial_region="village")
            if _return and _return in r13_places() and _return!=room13["location"]:
                $ r13_edit(location=_return)
                jump r13_roam
        elif r13_destination:
            $ r13_edit(location=r13_destination)
            jump r13_roam
        jump r13_field
    if r13_choice[1] in ("doorway","room_inside"):
        $ r13_destination="hall" if r13_choice[1]=="doorway" else "room13"
        if r13_destination in r13_places():
            $ r13_edit(location=r13_destination)
            jump r13_roam
        jump r13_field
    if r13_choice[1]=="people":
        call screen r13_nearby
        if _return:
            $ r13_target=_return
            call r13_talk
        jump r13_roam
    if r13_choice[1]=="evening":
        call r13_evening_board
        if _return and _return!=room13["location"]:
            $ r13_edit(location=_return)
        jump r13_roam
    if r13_choice[1]=="map":
        call screen r13_map
        if _return and _return in r13_places() and _return!=room13["location"]:
            $ r13_edit(location=_return)
            jump r13_roam
        jump r13_field
    jump r13_field

label r13_object(key):
    if key=="door" and r13_life_door_available():
        call r13_life_door
        return
    if key=="mother_note" and room13.get("life_poc"):
        call r13_mother_note
        return
    if room13["location"]=="gate" and key in ("booth","ledger","gate_documents"):
        call r13_inspect_gate_documents(key)
        return
    if key in ("desk", "letters", "notebook", "cup") and r13_inspection_available():
        call r13_inspect_desk
        return
    $ r13_spec=ROOM13["objects"][room13["location"]][key]
    if not r13_object_visible(r13_spec):
        return
    $ r13_was_observed=r13_has("observed:"+room13["location"]+":"+key)
    $ r13_rect=r13_spec["rect"]
    $ r13_mark(key,r13_rect[0]+r13_rect[2]//2,r13_rect[1]+r13_rect[3]//2)
    $ r13_flag("observed:"+room13["location"]+":"+key)
    if r13_spec.get("call_label"):
        # 0.18.61: a place object that runs its own scene (systems/room13_new_places.rpy).
        call expression r13_spec["call_label"]
    elif r13_spec.get("special"):
        call r13_object_mechanism(r13_spec["special"])
    elif room13["case_state"]=="occurred" and room13["location"]=="hall" and key=="door":
        call r13_observe([(None,"복도 맨 끝에 있는 13호실 문. 복도에서 바라봤을 때 왼쪽 문틀의 잠금쇠 고정부가 뜯겨 나가 있다. 오른쪽 경첩은 멀쩡하고, 문짝은 방 안쪽으로 밀려 열려 있었다."),("dad","방문에는 유리창이 없어. 창문은 맞은편 바깥쪽 벽에만 나 있지.")],"object:case:door:v4")
    elif room13["case_state"]=="occurred" and room13["location"]=="room13" and key=="floor":
        call r13_observe([(None,"바닥에 굳은 촛농과 핏자국을 다시 살폈다. 현장을 처음 발견했을 때 기록해 둔 자료가 있어야 어떤 자국이 먼저 생겼는지 순서를 알 수 있다.")],"object:case:floor")
    elif room13["daram_state"]=="held" and room13["location"]=="room13" and key=="bed":
        call r13_observe([(None,"이불 안쪽이 붉은 실로 기워져 있다. 집에서 아내가 바느질할 때 쓰던 매듭 모양과 닮았다. 누가 언제 꿰맨 것인지는 따로 알아봐야 한다.")],"object:case:bed")
    else:
        $ r13_observation_text=r13_spec.get("time_text",[r13_spec["text"]]*3)[min(room13["period"],2)]
        $ r13_observation_entries=[(None,r13_observation_text)]
        if r13_spec.get("child_remark") and room13["daram_state"] in ("with_dad","rescued"):
            $ r13_observation_entries.append(("daram",r13_spec["child_remark"]))
        call r13_observe(r13_observation_entries,"object:"+room13["location"]+":"+key+(":"+r13_daylight() if r13_spec.get("time_text") else ""))
    $ r13_grant(r13_spec["give"],R13_PLACES[room13["location"]][0]+" 직접 조사")
    $ r13_flag(*r13_spec.get("flags",[]))
    $ r13_revisit_lines=r13_discovery_observation_feedback(room13["location"],key,r13_was_observed)
    if r13_revisit_lines:
        call r13_observe(r13_revisit_lines,"object:revisit:"+room13["location"]+":"+key)
    return

label r13_talk:
    call r13_notice_before_talk(r13_target) from r13_notice_before_talk_return
    if not _return:
        return
    $ r13_first_encounter = r13_target not in r13_met_people()
    $ r13_note_encounter(r13_target)
    $ r13_encounter_key=r13_calendar_key(r13_target)
    if not r13_has(r13_encounter_key):
        # Keep the latest selected-person close-up while calendar greetings change.
        $ r13_speaker(r13_target,"neutral")
        if r13_target not in R13_OPENING_SCENES["first_meetings"] and r13_target=="bami" and r13_has("bami_pressured"):
            call r13_lines([(None, '밤이는 나를 쳐다보기 전에 복도 양옆부터 경계하며 살폈다. 나는 그 행동이 마음에 걸렸다.'), ('bami', '누가 제가 그날 밤 처마 밑에 있었다고 말했대요. 아저씨가 제 이름을 말씀하셨어요?'), ('dad', '……다시는 너를 위험 속에 혼자 두지 않을게.'), ('bami', '말뿐인 약속은 또 하시네요.'), (None, '밤이가 방문 쪽으로 휙 몸을 돌렸다. 내 대답은 아이의 등 뒤에 힘없이 남았다.'), ('bami', '아저씨가 안 계실 때 경비들을 피해 숨어야 하는 건 저예요. 이번에는 말로만 약속하지 마세요.')],"greeting:bami:pressured")
        elif r13_target not in R13_OPENING_SCENES["first_meetings"] and r13_target=="buri" and room13["victim_state"]=="dead":
            call r13_lines([("buri","물건 수리하러 오신 거 아니죠. 돌아가신 할아버지 이야기를 꺼내실 거면 용건부터 먼저 말씀해 주세요.")],"greeting:buri:bereaved")
        elif r13_target in R13_OPENING_SCENES["first_meetings"]:
            $ r13_opening_lines = r13_conversation_opening(r13_target, r13_first_encounter)
            call r13_lines(r13_opening_lines,"greeting:opening:"+r13_encounter_key+(":first" if r13_first_encounter else ":return"), binding_route="dynamic:022") from r13_dialogue_opening_return
        elif r13_target not in R13_CORE_PEOPLE:
            call r13_lines([(None,r13_activity_text(r13_target))],"greeting:activity:"+r13_target, binding_route="dynamic:023")
        else:
            call r13_lines([(r13_target,R13_GREETING[r13_target])],"greeting:"+r13_target, binding_route="dynamic:024")
        $ r13_flag(r13_encounter_key)
label r13_person_actions:
    # Old saves can still resume this label; the extra command page is gone.
    jump r13_talk_menu
label r13_talk_menu:
    $ r13_present_origin="topics"
    window hide
    hide r13_visitor
    $ r13_remember_topic_order(r13_target)
    call screen r13_topics(r13_target)
    $ r13_topic=_return
label r13_talk_dispatch:
    if r13_topic=="back":
        return
    $ r13_speaker(r13_target,"neutral")
    if r13_topic in R13_TOPIC_LABELS:
        call expression R13_TOPIC_LABELS[r13_topic]
        if _return=="roam":
            return
        jump r13_talk_menu
    if r13_topic=="shop:eunho":
        call r13_lines([("resident_eunho","필요한 물건이 있으면 골라 보십시오. 가격은 정해진 대로만 받습니다.")],"shop:eunho:open")
        call screen r13_shop
        jump r13_talk_menu
    if r13_topic=="home:records":
        call r13_lines([("dad","오늘 우리가 알아낸 단서들을 같이 정리해 볼까?"),("daram","응. 내가 본 것도 아빠한테 다 말해 줄게.")],"home:records")
        call screen r13_records(close_action=Return())
        jump r13_talk_menu
    if r13_topic=="present":
        call screen r13_book(r13_target,present=True)
        $ r13_item=_return
        if not r13_item:
            if r13_present_origin=="actions":
                jump r13_person_actions
            jump r13_talk_menu
        if r13_catalog_object(r13_item):
            call r13_show_catalog_object(r13_target,r13_item)
            jump r13_talk_menu
        if r13_item:
            $ r13_disclose_name=False
            if r13_item=="E10":
                call r13_lines([(None,"밤이는 경비가 찾아올까 봐 겁내고 있었다. 기록에는 그 아이의 이름과 숨어 있던 자리가 적혀 있다. 그것까지 알려 주면 상대도 밤이를 찾아갈 수 있다. 본 것만 전할지, 본 사람이 누구인지까지 밝힐지는 내가 정해야 한다.")],"disclosure:bami:warning")
                menu:
                    "목격한 내용만 설명한다":
                        $ r13_disclose_name=False
                    "목격자인 밤이의 이름까지 밝힌다":
                        $ r13_disclose_name=True
                    "기록을 보여 주지 않는다":
                        if r13_present_origin=="actions":
                            jump r13_person_actions
                        jump r13_talk_menu
            if r13_item in ROOM13.get("sensitive",{}):
                call r13_lines([(None,ROOM13["sensitive"][r13_item])],"sensitive:"+r13_item, binding_route="dynamic:028")
            $ r13_defer_grants=True
            $ r13_reaction=r13_present(r13_target,r13_item,r13_disclose_name)
            $ r13_defer_grants=False
            show screen r13_material_corner(r13_item)
            call r13_lines(r13_reaction,"present:"+r13_target+":"+r13_item+":"+str(r13_disclose_name), binding_route="dynamic:029")
            hide screen r13_material_corner
            $ r13_flush_grants()
            if r13_granny_warning_asked(r13_target,r13_item,r13_reaction):
                call r13_granny_warning_reply
                if _return:
                    $ r13_topic=_return
                    jump r13_talk_dispatch
        jump r13_talk_menu
    if r13_topic=="buri_consent":
        call r13_lines([(None, '부리는 손에 든 공구를 내려놓았지만 내 쪽을 쳐다보지는 않았다.'), ('buri', '밖에서는 다들 할아버지가 아이를 잡아먹으려 했다고 수군거려요.'), ('dad', '나는 그렇게 말한 적이 없어.'), ('buri', '누군가는 그렇게 말했어요. 다람이를 살인 혐의에서 구하려고요.'), (None, '내가 딸아이 이야기를 꺼내려 하자 부리가 먼저 고개를 들어 나를 보았다.'), ('dad', '나도 우리 아이가 그 방에서 왜 다쳤는지 진실을 알아야 해.'), ('buri', '그럼 저한테 직접 물어보세요. 할아버지가 어떤 사람이었는지 미리 정해 놓고 묻지는 마시고요.')],"buri:consent:opening")
        $ r13_speaker("buri","neutral")
        menu:
            "확인한 상처만 말하고, 병은 가족에게 맡긴다":
                if r13_has("buri_refused"):
                    if r13_has("E08"):
                        call r13_lines([("dad","내가 한 말도 바로잡을게. 기록에는 팔을 잡은 흔적과 머리 부상이 따로 적혀 있어. 그러니 할아버지가 무엇을 하려 했는지는 아직 몰라."),("buri","그렇게 바로잡은 내용도 기록에 꼭 남겨 주세요. 여기서 저한테만 말로 하시는 거라면 아무 소용 없어요.")],"buri:consent:repair")
                        $ r13_edit(flags=[f for f in room13["flags"] if f!="buri_refused"])
                    else:
                        call r13_lines([("buri","사실대로 적으셨다는 그 기록부터 직접 가져와 보여 주세요. 그다음에 이야기를 들을게요.")],"buri:consent:needs_record")
                        jump r13_talk_menu
                call r13_lines([('dad', '직접 확인하지 않은 추측은 기록에 적지 않을게.'), ('buri', '지금 제 앞에서만요? 나중에 다른 마을 사람들 앞에서는요?'), ('dad', '사람들 앞에서도 마찬가지야. 그때 다르게 말하면 바로잡을게.'), (None, '부리는 대답하지 않았다. 나는 그 침묵을 허락의 뜻으로 착각할 뻔했다.'), ('buri', '그 말, 사람들 앞에서도 꼭 지키세요.'), (None, '부리가 작업대 한쪽의 공구들을 치워 자리를 비웠다. 사람 한 명이 걸터앉을 만한 공간이었다.'), ('buri', '기록은 그 자리에 앉아서 같이 봐요.')],"buri:consent:accepted")
                $ r13_finish_topic(r13_topic)
            "아이를 위해 어르신의 위험을 공개한다":
                call r13_lines([('buri', '우리 할아버지를 괴물로 만들면 탐정님 아이가 무사히 돌아오나요?'), ('dad', '나는 어떻게든 우리 아이를 구해야 해.'), ('buri', '그 마음은 저도 알아요. 제가 그걸 모르는 사람인 것처럼 말씀하지 마세요.'), (None, '부리가 다시 공구를 집어 들었다. 작업대 한쪽에 빈자리가 있었지만, 내게 앉으라고 내어 주지는 않았다.'), ('buri', '지금은 그만 나가 주세요.')],"buri:consent:refused")
                $ r13_flag("buri_refused")
                return
            "더 말하지 않고 자리를 비켜 준다":
                return
        jump r13_talk_menu
    if ROOM13["topics"][r13_topic].get("special"):
        if r13_topic in room13["read_topics"]:
            call r13_topic_review(r13_topic)
        else:
            call r13_topic_choice(r13_topic)
            if _return:
                $ r13_finish_topic(r13_topic)
        jump r13_talk_menu
    if r13_topic in room13["read_topics"] and r13_topic_current_context(r13_topic) is None:
        # Historical testimony stays verbatim; live companion/corrected topics do not.
        call r13_topic_review(r13_topic)
        $ r13_finish_topic(r13_topic)
        jump r13_talk_menu
    $ r13_topic_rows=r13_topic_current_lines(r13_topic) if r13_topic_current_context(r13_topic) is not None else r13_conversation_topic_lines(r13_topic)
    call r13_lines(r13_topic_rows,"topic:"+r13_topic, binding_route="dynamic:035")
    $ r13_topic_shown=r13_topic_rows
    $ r13_finish_topic(r13_topic)
    jump r13_talk_menu

label r13_first_night:
    if room13.get("life_poc"):
        call r13_life_first_night
        return
    call r13_scene("council","여관 식당","calm")
    call r13_lines([("nabi","탐정님, 그릇이 뜨거워요. 밑받침을 잡고 드세요."),("daram","아빠 밥그릇은 제가 가져갈게요."),("nabi","두 번 왔다 갔다 하면 되잖아. 무리해서 한 번에 다 들지 말고.")],"night1:meal")
    $ source_fx("knock")
    call r13_lines([(None,"식당 현관문을 일정한 박자로 둔탁하게 두드리는 소리가 이어졌다. 식사하던 손님 한 명이 말없이 창문 커튼을 쳤다."),("daram","밖에 누가 왔나 봐요."),("granny","경비들이 알아서 살피고 있어. 신경 쓰지 마라."),("daram","스스로 문을 못 여는 것 같은데요."),("nabi","……밥 식기 전에 얼른 먹어.")],"night1:knocking")
    menu:
        "현관 밖을 살핀다":
            call r13_lines([(None,"주민 한 명이 자기 집이 어느 쪽인지 말하지 못했다. 경비가 그 주민의 목덜미에 번호표를 달고 어디론가 데려갔다. 지켜보던 사람 중 아무도 소리를 지르지 않았다.")],"night1:look")
            $ r13_flag("first_patient_seen")
        "다람이 옆에 앉는다":
            call r13_lines([("daram","아빠, 우리도 길 잃어버리면 저 아저씨처럼 저기로 끌려가?"),("dad","길을 모르겠으면 혼자 헤매지 말고 아빠랑 같이 물어보자.")],"night1:stay")
    $ r13_flag("night1_seen")
    return

label r13_case_choice:
    # Week-1 case L (systems/room13_week1_cases.rpy): a planted letter empties the inn that night.
    if r13_has("fake_letter_planted") and not r13_has("fake_letter_night") and not r13_has("granny_knows_found_out"):
        call r13_w1c_fake_night
        jump r13_roam
    call r13_scene("hall","목요일 저녁 · 여관 2층 복도","night")
    call r13_lines([("karo","되돌아온 짐이 마을 바깥 초소에 도착했어요. 지금 확인하러 가실 거죠?"),("daram","할아버지 물건은 내가 대신 받아 둘게. 방에서 기다리고 있을게."),(None,"계단 아래에서 할머니가 웃으며 고개를 끄덕였다."),("granny","엄마 물건은 할아버지가 직접 보여 주실 거야. 할아버지 오시면 둘이 먼저 보고 있으렴. 할머니는 식당을 봐야 해서."),("dad","(되돌아온 짐을 받으러 초소에 갈까, 아니면 아이 곁에 남을까.)",{"thought":True})],"case:appointment:v4")
    menu:
        "되돌아온 짐은 미루고 방에서 함께 기다린다":
            $ r13_flag("father_accompanied")
            jump r13_prevented
        "통로를 지키고 나비에게 동행을 부탁한다" if r13_has("E05") and r13_has("E18"):
            $ r13_flag("route_watched")
            jump r13_prevented
        "까로와 되돌아온 짐을 확인하러 간다":
            call r13_lines([("dad","할아버지 오시면 같이 보고 있어. 아빠가 짐 받아서 돌아오면 함께 보자."),("daram","아빠, 금방 와?"),("dad","짐 받는 대로 바로 올게.")],"case:separate:v4")
    call r13_scene("winter","바깥 초소 · 되돌아온 짐","night")
    call r13_lines([("karo","봉투에 찍힌 날짜 좀 보세요. 부인이 이 마을에 오기 전에 보낸 물건 같네요."),(None,"봉투에 찍힌 오래된 우체국 날짜 도장은 젖어 있었다. 봉투 안에는 우리가 보냈던 장갑과 맡김표가 들어 있었다."),("dad","이 짐을 받으러 오라고 전한 사람은 누굽니까?"),("karo","여관에서 전해 줬어요. 저는 최근에 온 연락인 줄 알았는데…….")],"case:father:parcel:v3")
    $ r13_grant(["E34"],"까로와 바깥 초소에서 되돌아온 짐을 직접 확인")
    # Owner decision 2026-10-15: a changed lever or wedged panel makes Granny call off the plan.
    if r13_plan_noticed():
        jump r13_case_noticed
    call r13_scene("hall","여관 2층 · 연기가 새는 문","quiet")
    call r13_cinematic("return")
    $ source_fx("knock")
    call r13_lines([(None,"그때 계단 위에서 나무를 두드리는 소리가 들렸다. 우리 방 문틈 아래로 연기가 새어 나왔다."),("nabi","다람아, 그 안에 가만히 있어. 문에서 떨어져!"),("dad","무슨 일이니? 왜 문을 못 여는 거니?"),("doto","방 안쪽 빗장이 안 풀립니다. 비명을 듣고 바로 달려왔는데요."),("dad","다람아!"),("daram","아빠…… 나 여기 있어."),("granny","다들 비켜요. 공구 가져왔어요."),(None,"도토가 할머니에게서 지렛대를 받아 문틀 틈에 밀어 넣었다. 너울과 함께 문을 받쳤다.")],"case:father:return:v3")
    $ source_fx("impact")
    $ r13_edit(case_state="occurred",victim_state="dead",location="room13",kitchen_switch=False,passage_open=False)
    call r13_scene("room","여관 2층 · 13호 구조 직후","quiet")
    call r13_cinematic("rescue")
    call r13_lines([(None,"빗장을 걸어 두던 잠금쇠가 뜯겨 나갔다. 너울이 연기 나는 작은 깔개 위에 젖은 천을 덮었다. 다행히 침대에는 불이 옮겨붙지 않았다."),("dad","다람아, 이제 나와도 돼. 아빠가 손 잡아 줄게."),(None,"침대 아래에서 다람이가 손을 뻗었다. 그 바로 옆 바닥에는 어르신이 쓰러져 있었다."),("daram","내가 할아버지를 때렸어."),("dad","너는 어디 다쳤어?"),("daram","아빠, 내가 때렸다니까."),(None,"아이 손목에는 세게 눌린 자국이 있었다. 바닥에 떨어진 촛대는 두 동강 나 있었다.")],"case:discovery:v3")
    menu:
        "아이를 안고, 현장 기록을 부탁한다":
            call r13_lines([("dad","아이는 제가 데리고 나가겠습니다. 쓰러진 분부터 살피되, 물건을 옮기면 원래 있던 자리를 표시해 두세요."),("neoul","문 앞은 제가 막겠습니다. 도토 씨, 바닥에 지금 보이는 자국부터 그려 주십시오.")],"case:preserve:v3")
            $ r13_flag("floor_preserved")
            $ r13_grant(["E33"],"구한 직후 너울·도토가 남긴 방 그림과 봉해 둔 물건")
        "아이를 데리고 나와 진료할 사람을 부른다":
            call r13_lines([("buri","할아버지! 비켜요!"),("neoul","조심하십시오. 발밑에 떨어진 물건이 있습니다."),(None,"사람들이 쓰러진 어르신 곁으로 몰려들었다. 너울이 촛대를 거둬 갔다. 하지만 바닥의 자국은 이미 여러 사람의 발자국에 덮여 있었다.")],"case:unpreserved:v3")
    call r13_lines([("resident_seori","어르신은 숨을 쉬지 않습니다. 아이 팔도 보겠습니다."),(None,"촛대의 휘어진 장식 고리에 작은 금속 조각이 걸려 있었다. 너울은 조각에 손대지 않고 촛대째 싸서 봉했다."),("daram","내가 놓으라고 했어. 그런데 할아버지가 안 놔줘서……."),("granny","아이를 잡아당기지 말아요. 얘도 지금 떨고 있잖아요."),("neoul","확인이 끝날 때까지 아이는 초소 보호실에 두겠습니다."),("dad","아이만 데려가는 겁니까?"),("neoul","아버님은 그 시간에 까로 씨와 마을 밖에 계셨다는 게 확인됐습니다."),("dad","아이를 직접 만나겠습니다. 아이가 한 말은 고치지 말고 그대로 기록에 남겨 주십시오.")],"case:sealing:v3")
    $ r13_grant(["E07","E08","E14"],"구한 직후 봉해 둔 촛대 두 조각과 처음 살핀 진료 기록")
    $ r13_flag("family_room_unusable")
    $ r13_edit(daram_state="held",period=3,location="inn")
    call r13_lines([("nabi","짐은 옆방으로 옮겨 둘게요. 오늘부터는 옆방에서 묵으세요."),(None,"나는 13호 열쇠를 내려놓았다. 손에는 다람이가 가져오겠다고 했던 가방만 남았다.")],"case:displaced:v3")
    jump r13_roam

label r13_prevented:
    call r13_scene("room","13호실","night")
    if r13_has("route_watched"):
        call r13_lines([(None,"나는 나비에게 아이를 부탁했다. 그리고 어르신에게 통로를 알고 있다고 말했다. 방문은 열어 둔 채였다."),("resident_owlgp","그럼 이 방에서 기다리지 맙시다. 아래층으로 내려갑시다.")],"case:prevented:watch")
    else:
        call r13_lines([("resident_owlgp","댁은 되돌아온 짐을 찾으러 간 줄 알았소."),("dad","되돌아온 짐은 내일 확인해도 됩니다."),("daram","아빠랑 같이 왔어요. 할아버지가 보여 주신다던 물건, 이제 봐도 돼요?"),(None,"어르신의 손이 잠깐 떨렸다. 내가 옆에 앉아 기다리자, 어르신은 쥐고 있던 봉투를 내려놓았다."),("resident_owlgp","아래층에서 이야기합시다. 이 방은 너무 답답하오.")],"case:prevented:accompany")
    call r13_lines([("granny","다들 여기 계셨네요. 아이 곁에 있어 주려고 올라왔어요. 차라도 내올까요?"),("dad","차는 아래층 식당에서 다 함께 마시겠습니다."),(None,"그날 13호에서는 아무도 죽지 않았다. 그렇다고 누군가 하려던 일을 막았다는 증거를 얻은 것은 아니었다.")],"case:prevented:result")
    $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",period=3,location="inn")
    $ r13_flag("victim_protected")
    $ r13_grant(["E17"],"살아 있는 어르신이 간직해 온 베낀 기록")
    jump r13_roam

label r13_trial:
    if room13["trial_ended"]:
        jump r13_week2_opening
    call r13_scene("council","일요일 · 여관 공동 식당","hearing")
    if room13["case_state"]=="prevented":
        jump r13_prevention_hearing
    $ r13_meeting_claim="C1"
    $ r13_meeting_intro=True
    $ r13_meeting_active=True
    call r13_lines([("seryeon","부엉이 어르신이 발견된 13호는 안에서 잠겨 있었습니다. 그 안에는 다람 양이 있었습니다."),("buri","그냥 ‘발견된 사람’처럼 말하지 마세요. 우리 할아버지예요."),("resident_seori","오늘 확인할 것은 아이가 그 죽음에 책임이 있는지입니다. 소문을 본 일처럼 말하지 마십시오."),("resident_ppul","아이가 위험하다면 마을의 다른 아이들부터 지켜야 합니다."),("dad","아이가 위험하다는 판단도 확인된 사실에 근거해 주십시오.")],"trial:opening")
    $ r13_meeting_active=False
    $ r13_meeting_intro=False
label r13_trial_choose:
    # 반론할 자료가 없는 논점은 선택지 없이 지나가고, 남은 논점이 없으면 바로 판결이다.
    $ r13_trial_pending=[c for c in r13_case_available() if c not in room13["propositions"] and not r13_debate_closed(c)]
    $ r13_trial_gap=next((c for c in r13_trial_pending if not r13_debate_engageable(c)),None)
    if r13_trial_gap:
        call r13_argument(r13_trial_gap) from r13_trial_gap_return
        jump r13_trial_choose
    if not r13_trial_pending:
        jump r13_verdict
    window hide
    hide r13_visitor
    call screen r13_meeting_agenda(r13_trial_pending)
    $ r13_choice=_return
    if r13_choice in r13_trial_pending:
        call r13_argument(r13_choice)
    jump r13_trial_choose

label r13_argument(claim):
    $ r13_meeting_claim=claim
    $ r13_meeting_active=True
    $ r13_meeting_focus_change(claim,r13_debate_statements(claim)[0]["who"])
    $ r13_claim=claim
    if claim=="C1":
        call r13_lines([("seryeon","복도에 있던 사람들은 아무도 그 방에 들어가지 않았다고 합니다."),("dad","복도에 있던 분들이 지켜본 문이 어느 문인지 확인하고 싶습니다.")],"trial:C1:start")
    elif claim=="C2":
        call r13_lines([("resident_ppul","아이가 겁을 먹은 건 알겠습니다. 하지만 아이에게 맞은 사람이 죽었습니다."),("buri","할아버지가 먼저 아이 손을 잡았다는 말도 지금은 들을게요. 그다음엔 무슨 일이 있었는데요?")],"trial:C2:start")
    elif claim=="C3":
        call r13_lines([("granny","비명이 들렸을 때 나는 식당에 있었어요. 다들 나를 봤잖아요.")],"trial:C3:start")
    else:
        if r13_has("granny_prepared:E09"):
            call r13_lines([("granny","아버님이 보여 준 자국도 오래된 것일 수 있다고 했죠. 누가 그 길로 들어갔다 해도, 어르신을 도우려던 건지 아닌지 어떻게 알아요?")],"trial:C4:prepared")
        elif any(r13_has("granny_prepared:"+e) for e in ("E13","E14","E35","E36")):
            call r13_lines([("granny","브로치를 조사하신다니까 말씀드리는데요. 오후에 어르신을 도와드릴 때 떨어졌을 수도 있잖아요.")],"trial:C4:prepared_pin")
        else:
            call r13_lines([("granny","잠깐 주방에 갔다고 해서 내가 13호에 갔다는 건가요? 갔다 해도 아픈 분을 도우려던 거라면요?")],"trial:C4:start")
label r13_argument_menu:
    # 공개 회의 엔진(systems/room13_debate.rpy). 입증은 r13_prove로만 남는다.
    call r13_debate_run(r13_claim) from r13_argument_debate_return
    $ r13_argument_result=_return
    if r13_argument_result is True and r13_claim=="C4":
        call r13_cinematic("proof")
    return r13_argument_result

# r13_link_reason은 0.16.2 이전 저장의 복귀 지점을 위해 남겨 둔다. 새 흐름은 쓰지 않는다.
label r13_link_reason(claim):
    if claim=="C1":
        menu:
            "도면과 실제 통로 조사를 어떻게 연결할까?"
            "정문만 봐서는 다른 길을 배제할 수 없다":
                call r13_lines([("resident_seori","정문 말고도 방에 드나들 길이 있었군요. 아이만 들어갈 수 있었다는 말은 고치십시오."),("seryeon","그 통로에 아이 어머니 물건도 있었다면서요. 그날 그 길로 들어간 사람이 부인입니까?")],"trial:C1:counter")
                menu:
                    "오래된 흔적은 그날의 출입 증거가 아니다":
                        call r13_lines([("resident_seori","맞습니다. 그날 실제로 누가 드나들었는지는 따로 확인해야 합니다.")],"trial:C1:done")
                        return True
                    "엄마는 절대 그럴 사람이 아니다":
                        call r13_lines([("seryeon","가족을 믿는다는 대답만으로는 그날 출입했는지 확인할 수 없습니다.")],"trial:C1:wrong")
            "통로가 있으니 할머니가 범인이다":
                call r13_lines([("resident_seori","통로가 있으니 누군가 드나들 수 있었다는 건 알겠습니다. 하지만 누가 그 통로를 썼는지는 아직 밝혀지지 않았습니다.")],"trial:C1:overreach")
    elif claim=="C2":
        menu:
            "촛대가 부서진 순서와 상처를 이어 보면?"
            "죽게 한 상처는 촛대가 갈라진 뒤에 생겼다":
                call r13_lines([("seryeon","아이의 첫 공격 때문에 어르신이 나중에 쓰러졌을 가능성은요?"),("dad","팔의 상처로는 목숨을 앗아 간 머리 상처가 설명되지 않습니다. 떨어져 나간 촛대 윗부분이 그 뒤에 한 번 더 쓰였습니다. 그사이 아이가 어디 있었는지, 누가 다른 길로 드나들었는지 함께 봐야 합니다."),("resident_seori","지금까지 나온 관찰과 방의 기록을 함께 봤습니다. 아이가 한 것으로 확인된 일과 어르신을 죽게 한 공격은 같은 일로 적을 수 없습니다."),("daram","그럼…… 내가 때린 건 어떻게 돼?"),("dad","그건 네가 붙잡힌 손을 빼려고 한 일이야. 사람을 죽게 한 공격과는 달라.")],"trial:C2:done")
                return True
            "다람이는 착한 아이니 사람을 죽일 수 없다":
                call r13_lines([("buri","할아버지도 착한 사람이었어요. 그런 말로 대충 끝내지 마세요.")],"trial:C2:wrong")
    elif claim=="C3":
        menu:
            "나비의 참인 목격과 통로 이동 시간을 연결하면?"
            "식당에 있던 건 첫 비명 때뿐이다":
                call r13_lines([("nabi","제가 할머니를 본 건 첫 비명 때뿐이에요. 그 뒤로 주방 안까지 들여다본 건 아니에요."),("granny","그러니까 내가 잠깐 안 보였다는 것 말고는 아무것도 없잖아요."),("resident_seori","그것만으로는 어르신이 해를 입었을 수 있는 시간 내내 다른 곳에 있었다는 증거가 되지 못합니다. 실제로 손을 댔는지는 이어서 보겠습니다.")],"trial:C3:done")
                return True
            "나비가 할머니 편이므로 전부 거짓말이다":
                call r13_lines([("nabi","제가 할머니와 같이 있었던 시간까지 없던 일로 만들지는 마세요.")],"trial:C3:wrong")
    else:
        menu:
            "핀 조각과 그날 뒷정리 기록으로 어떤 변명을 막을까?"
            "핀과 도구로 ‘구하다 만졌다’를 반박한다":
                call r13_lines([("dad","첫 비명 때 나비가 채워 준 핀입니다. 구조 직후 봉해 둔 촛대 조각에 그 핀 조각이 끼어 있었습니다. 그러니 도구를 거둬 간 뒤에 들어간 게 아닙니다."),("granny","그래서 내가 들어갔다고 해도, 어르신이 도와달라고 한 거라면요?"),("dad","내려친 방향으로 눌린 고리 안에서 핀도 같이 휘었습니다. 주워 들다가 나중에 끼어든 조각이 아닙니다. 첫 비명 때만 해도 그 핀은 목도리에 달려 있었습니다."),("resident_seori","할머니가 전날 어르신이 크게 변할 낌새를 알고 있었다는 것도 확인됐습니다. 위험을 모른 채 둘만 두었다는 설명도 기록과 다릅니다. 이 사실은 방에서 나온 자료와 따로 남기겠습니다."),("granny","……."),("resident_seori","대답하지 않으셔도 됩니다. 지금까지 모은 자료로 판단하겠습니다.")],"trial:C4:done")
                return True
            "핀 주인이니 다른 자료는 필요 없다":
                call r13_lines([("resident_seori","물건의 주인이 곧 범인인 것은 아닙니다. 그 물건이 언제 어떻게 옮겨 갔는지 밝혀야 합니다.")],"trial:C4:wrong")
    return False

label r13_verdict:
    if "C2" in room13["propositions"]:
        $ r13_edit(daram_state="with_dad",trial_result="cleared")
        call r13_lines([("resident_seori","다람 양이 죽였다는 의심을 뒷받침하던 설명은 더 이상 성립하지 않습니다. 아이를 풀어 주십시오."),("resident_ppul","아이는 가족에게 돌려보내겠습니다. 남은 사안은 따로 기록하시오.")],"verdict:cleared")
        if "C4" in room13["propositions"]:
            $ r13_edit(granny_state="detained",trial_result="culprit_proven")
            call r13_lines([("resident_seori","할머니가 어르신에게 손을 대고 그 사실을 숨긴 일, 어르신을 죽게 한 일은 따로 확인됐습니다. 증거를 훼손하지 못하도록 할머니를 붙잡아 두십시오."),("neoul","할머니, 일어나시오.")],"verdict:culprit")
        call r13_lines([("daram","이제 할아버지는 다시 못 만나지."),("dad","응."),("daram","나 할아버지 안 죽였다고 말하고 싶은데."),("dad","부리한테도 네가 준비되면 그때 같이 말하자.")],"verdict:child")
    else:
        $ r13_edit(daram_state="held",trial_result="detained")
        call r13_lines([("resident_seori","뒤집힌 부분은 기록에 남겼습니다. 하지만 오늘 모은 자료만으로는 아이를 풀어 달라는 요청이 받아들여지지 않았습니다."),("resident_ppul","추가 확인은 아이를 보호시설로 옮겨서 하겠습니다."),("dad","확인하지 못한 일까지 아이 죄로 못 박지 마십시오."),("daram","아빠는 같이 못 와?"),("neoul","오늘은 여기까지입니다."),("dad","다시 올게. 다른 데로 옮겨지면 꼭 말 남겨 줘."),("daram","아빠도. 아빠가 못 오면…… 누가 대신 오는지 말해 줘.")],"verdict:held")
    $ r13_record_trial_notes()
    # 재판 뒤: 따닥의 일, 부리의 모자, 초롱의 등 (systems/room13_ep4_night13.rpy).
    call r13_nt_after_trial
    $ r13_edit(trial_ended=True,period=3)
    jump r13_week2_opening

label r13_prevention_hearing:
    call r13_lines([("seryeon","아이가 함께 들어왔다는 기록과, 따로 맡아 달라는 요청을 확인하겠습니다."),("resident_owlgp","아이는 나와 함께 있었소. 죽은 사람도, 아이가 저지른 살인도 없소. 없는 사건을 만들지는 맙시다."),("granny","낯선 아이를 가족과 따로 떼어 보호하자는 뜻이었어요."),("dad","아이 보호자는 여기 있습니다. 마을 입구 초소에서 함께 등록한 원본도 있고요.")],"prevention:hearing")
    menu:
        "바로잡은 입장 기록 원본을 직접 보여 준다":
            call screen r13_book("resident_seori",present=True,hearing=True)
            if _return=="E02":
                call r13_lines([("resident_seori","아빠와 딸이 함께 들어왔다는 기록은 그대로 인정됩니다. 따로 떼어 놓자는 요청은 근거가 없다고 봅니다.")],"prevention:registered")
            else:
                call r13_lines([("resident_owlgp","초소 원본을 여기서 직접 대조해 봅시다. 아이를 떼어 놓고 볼 일이 아니오."),(None,"초소 담당자를 불러 원본을 확인했다. 그동안 우리 부녀는 떨어지지 않고 함께 기다렸다.")],"prevention:independent_check")
        "사람들 앞에서 원본을 대조하자고 한다":
            call r13_lines([("resident_owlgp","그날 아이는 나와 같이 있었소. 원본과 그걸 확인한 사람을 함께 부르시오."),("resident_seori","사람들 앞에서 원본을 대조하기 전까지 가족을 떼어 놓지 마십시오.")],"prevention:witness")
    $ r13_record_trial_notes(prevention=True)
    $ r13_edit(trial_result="prevention_hearing",trial_ended=True,daram_state="with_dad",period=3)
    jump r13_week2_opening

