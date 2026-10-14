default r13_carriage_skip = False

# Full campaign entry and first-week scenes; continuation is in room13_week2.rpy.
label r13_scene(bg,title,mood="calm"):
    $ r13_cg_active = False
    window hide
    hide r13_visitor
    hide winter_visitor
    hide visitor
    $ dialogue_speaker=None
    $ dialogue_expression="neutral"
    $ place=title
    $ r13_camera="stage"
    $ source_pulse(False)
    $ renpy.music.stop(channel="typing")
    $ renpy.music.stop(channel="scene_fx")
    if r13_scene_key==r13_scene_identity(bg,title,mood):
        return
    scene black with Dissolve(.18)
    call r13_arrival(bg,title,mood)
    $ r13_music={"calm":"assets/town-bright.mp3","travel":"assets/travel.mp3","search":"assets/search.mp3","night":"assets/night.mp3","hearing":"assets/source-serious-context-v4.mp3","quiet":None}[mood]
    if r13_music:
        if renpy.music.get_playing()!=r13_music:
            $ renpy.music.play(r13_music,fadeout=.2,fadein=.2)
    else:
        stop music fadeout .2
    $ renpy.pause(.25)
    scene expression r13_background(bg) with Dissolve(.25)
    $ r13_scene_key=r13_scene_identity(bg,title,mood)
    return

label r13_lines(entries,identity):
    $ r13_index=0
    while r13_index<len(entries) and not (identity==R13_CARRIAGE_IDENTITY and r13_carriage_skip):
        $ r13_packet=entries[r13_index]
        $ r13_thought_active=bool(len(r13_packet)>2 and isinstance(r13_packet[2],dict) and r13_packet[2].get("thought"))
        $ r13_expression,r13_directed_pose=r13_line_performance(identity,r13_index,r13_packet)
        if r13_thought_active:
            $ r13_expression,r13_directed_pose="thinking","thinking"
        $ r13_speaker(r13_packet[0],r13_expression,r13_directed_pose)
        $ r13_read_id=r13_before_line(identity,r13_index,r13_packet[1])
        # Isolate this line from the previous loop increment when record UI
        # changes are retained by an immediate save during the say interaction.
        $ renpy.checkpoint()
        $ R13_CHARS.get(r13_packet[0],source_thought)(r13_packet[1])
        if not (identity==R13_CARRIAGE_IDENTITY and r13_carriage_skip):
            $ r13_remember_line(r13_read_id)
        $ r13_index+=1
    hide r13_visitor
    $ dialogue_speaker=None
    $ r13_thought_active=False
    return

label room13_start:
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
    call r13_carriage
    $ r13_grant(["E01"],"여행 중 가지고 온 편지")
    $ r13_edit(period=1)
    call r13_scene("winter","눈에 막힌 입구","calm")
    $ r13_note_encounter("karo")
    $ r13_note_encounter("guard")
    $ r13_note_encounter("daram")
    call r13_lines([('karo', '도착했어요. 발판이 얼었으니 천천히 내려요.'), ('daram', '까로 아저씨, 이 가방도 내려 주세요.'), (None, '까로가 가방을 내려놓고 바퀴 아래를 들여다봤다. 나는 다람이의 손을 잡고 발판에서 내려왔다.'), ('dad', '무슨 문제 있습니까?'), ('karo', '축에 금이 갔네요. 짐부터 내리고 살펴봐야겠습니다.'), ('dad', '도와드릴까요?'), ('karo', '접수부터 하고 오세요. 짐은 제가 볼게요. 저쪽 초소에서 방문 확인을 받으시면 됩니다.')],"entry:karo:arrival")
    call r13_lines([('guard', '안녕하십니까. 무슨 일로 방문하셨습니까?'), ('dad', '아내를 찾으러 왔습니다. 여기 여관에서 편지를 보내 주셔서요. 방문 신청도 해 두었습니다.'), (None, '나는 편지와 방문 신청 종이를 건넸다. 경비가 초소의 이름 목록을 펼쳤다.'), ('guard', '다돌 님, 맞으십니까?'), ('dad', '네. 이 아이는 제 딸이고요.'), ('daram', '다람이예요.'), ('guard', '잠시만요. 이름 목록에는 다돌 님 한 분으로 되어 있네요.'), ('dad', '두 명으로 예약했는데요. 아이와 같이요.'), (None, '경비가 신청 종이와 이름 목록을 나란히 놓았다.'), ('guard', '제가 받은 이름 목록에는 한 분만 적혀 있습니다. 예약할 때 내신 서류를 확인해야겠네요.'), ('dad', '확인하는 동안 어디에 있으면 됩니까?'), ('guard', '대기소 앞에서 두 분 함께 기다려 주십시오.'), ('daram', '아빠, 오래 걸려?'), ('dad', '여쭤볼게. 얼마나 걸립니까?'), ('guard', '담당자가 돌아오는 건 저녁입니다. 기다리시면 제가 맞춰 봐 드리겠습니다.'), ('dad', '그 전에 확인할 방법은 없습니까?'), ('guard', '선반에 예약 서류가 있습니다. 직접 확인해 보시겠습니까?'), ('dad', '알겠습니다. 다람아, 아빠랑 여기서 확인하자.')],"entry:arrival")
label r13_entry:
    hide r13_visitor
    $ dialogue_speaker=None
    window hide
    call screen r13_hub(entry=True)
    $ r13_choice=_return
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
    if r13_choice != ("entry","back"):
        $ r13_speaker("guard","neutral")
label r13_entry_dispatch:
    if r13_choice==("entry","explain"):
        call r13_lines([('dad', '저희가 낸 신청과 이 이름 목록이 다른 거군요.'), ('guard', '예. 제가 받은 이름 목록에는 한 분뿐입니다. 초소에 있는 예약 원본과 맞춰 봐야 합니다.'), ('dad', '제 이름이 적힌 예약표를 볼 수 있습니까?'), ('guard', '예. 선반에 원본과 초소 이름 목록을 놓아 두었습니다.')],"entry:explain")
        $ r13_flag("question_read:entry:explain")
    elif r13_choice[0]=="object":
        call r13_object(r13_choice[1])
    elif r13_choice[0]=="empty":
        $ r13_mark("empty:%d:%d"%(r13_choice[1][0]//70,r13_choice[1][1]//70),*r13_choice[1])
        call r13_lines([(None,"흩날리는 눈을 털어 냈다. 눈에 띄는 흔적은 없다.")],"entry:empty")
    elif r13_choice[1]=="argue":
        call screen r13_book("guard",present=True)
        $ r13_item=_return
        if r13_item:
            show screen r13_material_corner(r13_item)
        if r13_item in ("G1","G3"):
            if r13_item == "G1":
                call r13_lines([("dad","제 예약표입니다. 여기 적힌 인원을 봐 주시겠습니까?"),("guard","다돌 님과 한 분 더…… 모두 두 분이네요. 제 목록에는 다돌 님 한 분만 적혀 있습니다."),("dad","예약이 아니라, 옮겨 적은 쪽이 달랐던 거군요."),("guard","네. 제가 잘못 옮겼습니다. 두 분으로 고치겠습니다. 기다리게 해서 죄송합니다."),("daram","아빠, 이제 같이 들어가는 거지?"),("dad","응. 같이 가자.")],"entry:corrected:v2")
                jump r13_entry_done
            else:
                call r13_lines([("dad","이 목록에는 제 이름만 있군요."),("guard","예. 예약 서류에서 옮겨 적었습니다. 원본도 확인해 보시겠습니까?")],"entry:copy:v2")
        elif r13_item == "G2":
            call r13_lines([("guard","그건 초소에서 아이를 넘겨줄 때 지킬 안내입니다. 예약한 사람 수는 예약표에서 확인할 수 있습니다.")],"entry:rules:v2")
        elif r13_item:
            call r13_lines([("guard","숙소에서 보낸 편지군요. 다만 이 편지만으로 들어온 사람 목록을 고칠 수는 없습니다. 원본을 봐야 합니다.")],"entry:letter")
        hide screen r13_material_corner
    elif r13_choice[1]=="wait":
        call screen r13_confirm("대기소 앞에서 원본 담당자가 돌아오기를 기다린다. 저녁까지 시간이 흐른다.")
        if _return:
            $ r13_flag("question_read:entry:wait")
            $ r13_tick()
            call r13_scene("winter","눈에 막힌 입구","calm")
            call r13_lines([("guard","원본은 두 분인데 제가 한 분으로 옮겨 적었습니다. 바로잡았으니 함께 들어가세요."),("daram","아빠, 이제 손이 잘 안 펴져."),("dad","오래 기다리게 했네. 손 줘. 같이 가자.")],"entry:wait")
            jump r13_entry_done
    if r13_choice[0]=="entry" and r13_choice[1] in ("explain","argue","wait"):
        jump r13_entry_guard_menu
    jump r13_entry

label r13_entry_person(person):
    if person in ("daram", "karo"):
        $ r13_note_encounter(person)
    if person=="daram":
        call r13_lines([('daram', '아빠, 엄마도 여기서 이름 썼을까?'), ('dad', '들어오실 때 확인하셨겠지.'), ('daram', '그럼 내 이름도 잘 써 달라고 해.'), ('dad', '응. 빠지지 않았는지 같이 보자.')],"entry:daram:waiting")
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
        call r13_lines([('dad', '아까 보신 축은 수리가 되겠습니까?'), ('karo', '고쳐야죠. 금 간 자리를 묶어 놓았는데, 이대로 손님을 태우지는 못해요.'), ('dad', '수리되면 돌아갈 수 있습니까?'), ('karo', '마차만 고쳐선 안 됩니다. 고개도 눈에 막혔어요. 길이 열리면 먼저 말씀드릴게요.')],"entry:karo:road")
        $ r13_flag("road_known")
    elif r13_entry_karo_choice=="witness":
        call r13_lines([('dad', '까로 씨, 두 사람을 태워 오셨다는 말씀을 해 주실 수 있습니까? 목록에서 아이가 빠져서요.'), ('karo', '그럼요. 제 마차에 두 분 다 탔습니다. 짐도 제가 내려 드렸고요.'), ('guard', '함께 오신 건 알겠습니다. 목록을 고치려면 예약 원본과 맞춰 봐야 합니다.'), ('dad', '알겠습니다. 그럼 원본부터 보겠습니다.'), ('karo', '저는 짐하고 같이 있을게요. 확인 끝나면 불러 주세요.')],"entry:karo:witness")
    elif r13_entry_karo_choice=="bags":
        call r13_lines([("karo","이 담요 밑에 둘게요. 눈에 젖으면 방에 가서도 한참 말려야 하니까.")],"entry:karo:bags")
    elif r13_entry_karo_choice=="present":
        call screen r13_book("karo",present=True)
        $ r13_item=_return
        if r13_item:
            call screen r13_confirm("까로에게 「"+ROOM13["evidence"][r13_item]["name"]+"」을 보여줄까요? 원본은 기록에 남습니다.","보여준다","취소한다")
            if _return:
                $ r13_reaction=r13_present("karo",r13_item)
                show screen r13_material_corner(r13_item)
                call r13_lines(r13_reaction,"entry:karo:present:"+r13_item)
                hide screen r13_material_corner
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
    call r13_lines([("karo","짐은 여관까지 옮겨 드릴게요. 마차는 여기 세워 둬야겠네요."),("daram","……가방은 내가 들게. 아빠 손 시려.")],"entry:departure")
    if room13.get("life_poc"):
        call r13_lines([("daram","아빠, 이제 엄마가 있던 여관부터 가 보자."),("dad","그래. 편지를 보내신 할머니께 여쭤보자.")],"life:arrival:direction") from r13_intro_direction_return
    jump r13_roam

label r13_carriage:
    $ r13_carriage_skip = False
    call r13_scene("winter_carriage","마차 안","travel")
    call r13_lines([(None, '덜컹. 바퀴가 돌부리를 넘자, 맞은편 등받이 뒤에서 무언가 불쑥 솟아올랐다.'), ('daram', '왁! 놀랐지? 놀랐지, 아빠?', 'joy'), ('dad', '깜짝이야. 언제부터 거기 숨어 있었어?'), ('daram', '아빠가 편지 읽을 때부터! 하나도 몰랐지?', 'expressive'), ('dad', '몰랐어. 우리 다람이 숨기 대장이네.'), ('daram', '헤헤. 그리고 이거 봐. 과자 봉지에서 엄청 큰 게 나왔어!', 'joy'), (None, '다람이가 손바닥만 한 과자를 내 코앞에 내밀었다.'), ('dad', '그게 봉지 안에 들어 있었어? 아껴 먹어야겠네.'), ('daram', '아니지! 이렇게 큰 건 첫입에 먹어 줘야 돼!', 'expressive'), ('dad', '천천히. 아무도 안 뺏어 먹어.'), ('daram', '아빠가 보고 있잖아.'), ('dad', '들켰네.'), (None, '다람이가 웃으며 과자를 베어 물었다. 부스러기 몇 개가 내 무릎에 떨어졌다.'), ('daram', '엄마한테도 주고 싶다. 이렇게 큰 거.', 'thinking'), ('dad', '그래. 곧 만날 수 있을 거야.'), (None, '나는 무릎 위의 편지를 접어 주머니에 넣었다.'), ('daram', '아빠, 엄마가 있던 마을은 커?'), ('dad', '아빠도 처음 가 봐. 까로 아저씨한테 여쭤볼까?'), ('daram', '아저씨! 아직 멀었어요?', 'expressive'), ('karo', '저 굽이만 지나면 지붕들이 보일 겁니다.'), (None, '다람이가 과자 봉지를 품에 안고 창문 쪽으로 몸을 붙였다.'), ('daram', '엄마가 있던 집도 보여요?'), ('karo', '여관은 마을 안쪽에 있어요. 제가 안내해 드리죠.'), ('daram', '아빠, 도착하면 거기부터 가자.'), ('dad', '응. 가서 엄마 소식부터 물어보자.'), ('daram', '내가 물어봐도 돼?', 'thinking'), ('dad', '그럼. 아빠랑 같이 여쭤보자.')],R13_CARRIAGE_IDENTITY)
    $ persistent.room13_opening_seen=True
    $ r13_carriage_skip = False
    return

label r13_day:
    if room13["day"]==4 and not r13_has("elder_appointment"):
        call r13_scene("hall","여관 계단","calm")
        call r13_lines([("resident_owlgp","저녁에 댁 방으로 들르겠소. 부인에게 받은 걸 돌려드려야지."),("dad","아내에 관한 겁니까?"),("resident_owlgp","보관해 둔 기록이오. 그분이 지금 어디 있는지는 나도 모르오."),("granny","되돌아온 짐 찾으러 나가신다면서요. 내가 아이하고 있어 줄게요."),("daram","받아만 둘게. 아빠 오면 같이 보자."),("dad","가능하면 그 전에 돌아오겠습니다."),("resident_owlgp","물건만 전해 두리다. 이야기는 같이 합시다.")],"day4:appointment:v3")
        $ r13_flag("elder_appointment")
    if room13["day"]==5 and room13["case_state"]=="occurred" and not r13_has("trial_notice"):
        call r13_scene("front","여관 접수대","quiet")
        call r13_lines([("neoul","일요일에 주민 앞에서 사건을 다룹니다. 아이는 그때까지 보호실에 둡니다."),("dad","결정도 나기 전에 가두기부터 합니까?"),("neoul","현장에 있던 아이를 데려가면 다른 사람들이 가만있지 않습니다. 만나러 오는 건 막지 않겠습니다."),(None,"바로잡은 입장 기록 원본은 돌려받았다. 함께 들어올 수 있다고 확인받은 것과, 지금 아이에게 씌워진 살인 의심은 다른 문제였다.")],"day5:notice")
        $ r13_flag("trial_notice")
    if room13["day"]==7:
        jump r13_trial
    if room13["day"]>=8:
        jump r13_week2_day
    jump r13_roam

label r13_roam:
    $ r13_upgrade()
    if room13.get("revision_restart_required"):
        jump r13_revision_resume
    if 5<=room13["day"]<8 and room13["case_state"]=="occurred":
        call r13_mother_intervention
    if room13["day"]>=8:
        call r13_week2_events
    if room13["day"]==4 and room13["period"]>=2 and room13["case_state"]=="pending":
        jump r13_case_choice
    $ place=R13_PLACES[room13["location"]][0]
    call r13_scene(R13_PLACES[room13["location"]][1],place,"night" if room13["period"]>=2 else "search" if room13["case_state"]=="occurred" else "calm")
label r13_field:
    window hide
    hide r13_visitor
    call screen r13_hub
    $ r13_choice=_return
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
        call r13_lines([(None,"발밑과 벽을 살폈다. 이 자리에는 따로 눈에 띄는 흔적이 없다.")],"field:empty:"+room13["location"])
        jump r13_field
    if r13_choice[0]=="person":
        $ r13_target=r13_choice[1]
        call r13_talk
        jump r13_roam
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
    if r13_choice[1]=="map":
        call screen r13_map
        if _return and _return in r13_places() and _return!=room13["location"]:
            $ r13_edit(location=_return)
            jump r13_roam
        jump r13_field
    jump r13_field

label r13_object(key):
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
    if r13_spec.get("special"):
        call r13_object_mechanism(r13_spec["special"])
    elif room13["case_state"]=="occurred" and room13["location"]=="hall" and key=="door":
        call r13_observe([(None,"복도 맨 끝의 13호 문. 복도에서 마주 보아 왼쪽 문틀의 빗장 받이가 뜯겨 있다. 오른쪽 경첩은 붙어 있고, 문짝은 방 안으로 밀려 열렸다."),("dad","문에 유리는 없어. 방의 창문은 반대편 바깥벽에 있지.")],"object:case:door:v4")
    elif room13["case_state"]=="occurred" and room13["location"]=="room13" and key=="floor":
        call r13_observe([(None,"촛농과 피가 남은 자리를 다시 보았다. 처음 보존한 기록이 있어야 자국이 겹친 순서를 확인할 수 있다.")],"object:case:floor")
    elif room13["daram_state"]=="held" and room13["location"]=="room13" and key=="bed":
        call r13_observe([(None,"이불 안쪽을 붉은 실로 기웠다. 집에서 보던 매듭과 닮았다. 누가 언제 썼는지는 따로 확인해야 한다.")],"object:case:bed")
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
            call r13_lines([(None, '밤이는 나를 보기 전에 복도를 살폈다. 나는 그 순서가 마음에 걸렸다.'), ('bami', '누가 제가 처마에 있었다고 했대요. 제 이름 말씀하셨어요?'), ('dad', '……다시 혼자 두지는 않을게.'), ('bami', '또 약속이네요.'), (None, '밤이가 문 쪽으로 몸을 돌렸다. 내 대답은 그 등 뒤에 남았다.'), ('bami', '탐정님 안 계실 때 숨는 건 저예요. 이번에는 말만 하지 마세요.')],"greeting:bami:pressured")
        elif r13_target not in R13_OPENING_SCENES["first_meetings"] and r13_target=="buri" and room13["victim_state"]=="dead":
            call r13_lines([("buri","수리하러 오신 거 아니죠. 할아버지 이름을 꺼내실 거면 먼저 말씀해 주세요.")],"greeting:buri:bereaved")
        elif r13_target in R13_OPENING_SCENES["first_meetings"]:
            $ r13_opening_lines = r13_conversation_opening(r13_target, r13_first_encounter)
            call r13_lines(r13_opening_lines,"greeting:opening:"+r13_encounter_key+(":first" if r13_first_encounter else ":return")) from r13_dialogue_opening_return
        elif r13_target not in R13_CORE_PEOPLE:
            call r13_lines([(None,r13_activity_text(r13_target))],"greeting:activity:"+r13_target)
        else:
            call r13_lines([(r13_target,R13_GREETING[r13_target])],"greeting:"+r13_target)
        $ r13_flag(r13_encounter_key)
label r13_person_actions:
    # Old saves can still resume this label; the extra command page is gone.
    jump r13_talk_menu
label r13_talk_menu:
    $ r13_present_origin="topics"
    window hide
    hide r13_visitor
    call screen r13_topics(r13_target)
    $ r13_topic=_return
label r13_talk_dispatch:
    if r13_topic=="back":
        return
    $ r13_speaker(r13_target,"neutral")
    if r13_topic=="shop:eunho":
        call r13_lines([("resident_eunho","필요한 게 있으면 골라 보세요. 값은 정해진 대로 받습니다.")],"shop:eunho:open")
        call screen r13_shop
        jump r13_talk_menu
    if r13_topic=="home:records":
        call r13_lines([("dad","오늘 찾은 걸 같이 볼까?"),("daram","응. 내가 본 것도 말해 줄게.")],"home:records")
        call screen r13_record_compare(called=True)
        jump r13_talk_menu
    if r13_topic=="present":
        call screen r13_book(r13_target,present=True)
        $ r13_item=_return
        if not r13_item:
            if r13_present_origin=="actions":
                jump r13_person_actions
            jump r13_talk_menu
        if r13_item:
            $ r13_disclose_name=False
            if r13_item=="E10":
                call r13_lines([(None,"밤이는 경비가 찾아오는 것을 두려워했다. 이 기록의 이름과 숨어 있던 자리를 알리면 상대도 밤이를 찾아갈 수 있다. 본 내용만 전할지, 누구인지까지 밝힐지 내가 정해야 한다.")],"disclosure:bami:warning")
                menu:
                    "관찰 내용만 설명한다":
                        $ r13_disclose_name=False
                    "밤이의 이름까지 밝힌다":
                        $ r13_disclose_name=True
                    "보여 주지 않는다":
                        if r13_present_origin=="actions":
                            jump r13_person_actions
                        jump r13_talk_menu
            if r13_item in ROOM13.get("sensitive",{}):
                call r13_lines([(None,ROOM13["sensitive"][r13_item])],"sensitive:"+r13_item)
            call screen r13_confirm(R13_NAMES[r13_target]+"에게 「"+ROOM13["evidence"][r13_item]["name"]+"」의 "+("발언자 이름과 관찰 내용" if r13_item=="E10" and r13_disclose_name else "이름을 뺀 관찰 내용" if r13_item=="E10" else "내용")+"을 보여줄까요? 원본은 수첩에 남습니다.","보여준다","취소한다")
            if _return:
                $ r13_reaction=r13_present(r13_target,r13_item,r13_disclose_name)
                show screen r13_material_corner(r13_item)
                call r13_lines(r13_reaction,"present:"+r13_target+":"+r13_item+":"+str(r13_disclose_name))
                hide screen r13_material_corner
            elif r13_present_origin=="actions":
                jump r13_person_actions
        jump r13_talk_menu
    if r13_topic=="buri_consent":
        call r13_lines([(None, '부리는 공구를 놓았지만 나를 보지는 않았다.'), ('buri', '밖에서는 할아버지가 아이를 잡아먹으려 했대요.'), ('dad', '그렇게 말한 적 없습니다.'), ('buri', '누군가는 했어요. 다람이를 구하려고요.'), (None, '내가 딸 이야기를 꺼내려 하자 부리가 먼저 고개를 들었다.'), ('dad', '저도 제 아이가 왜 다쳤는지 알아야 합니다.'), ('buri', '그럼 물어보세요. 할아버지가 무슨 사람이었다고 먼저 정하지 마시고요.')],"buri:consent:opening")
        $ r13_speaker("buri","neutral")
        menu:
            "확인한 상처만 이야기하고, 앓던 병을 밝힐지는 가족에게 묻는다":
                if r13_has("buri_refused"):
                    if r13_has("E08"):
                        call r13_lines([("dad","제가 한 말도 바로잡겠습니다. 실제 기록에는 팔을 잡은 흔적과 머리의 부상을 따로 적었습니다. 어르신이 무엇을 하려 했는지는 아직 모릅니다."),("buri","고친 것도 같이 남겨 주세요. 저한테만 하시는 말씀이면 소용없어요.")],"buri:consent:repair")
                        $ r13_edit(flags=[f for f in room13["flags"] if f!="buri_refused"])
                    else:
                        call r13_lines([("buri","확인하셨다는 기록부터 가져와 주세요. 그다음에 들을게요.")],"buri:consent:needs_record")
                        jump r13_talk_menu
                call r13_lines([('dad', '확인하지 않은 말은 쓰지 않겠습니다.'), ('buri', '지금은요. 다른 사람들 앞에서는요?'), ('dad', '그때도. 제가 다르게 말하면 바로잡겠습니다.'), (None, '부리는 대답하지 않았다. 나는 그 침묵을 허락으로 받아들일 뻔했다.'), ('buri', '저한테만 하시는 말씀이면 소용없어요.'), (None, '부리가 작업대 한쪽을 비웠다. 사람 하나 앉을 만큼이었다.'), ('buri', '기록을 확인하는 건 그다음이에요.')],"buri:consent:accepted")
                $ r13_finish_topic(r13_topic)
            "어르신이 위험했다는 걸 공개해야 아이를 구할 수 있다":
                call r13_lines([('buri', '제 할아버지를 괴물로 만들면 탐정님 아이가 돌아오나요?'), ('dad', '아이를 구해야 합니다.'), ('buri', '저도 알아요. 그 말 모르는 사람처럼 말씀하지 마세요.'), (None, '부리가 공구를 집어 들었다. 작업대에는 빈자리가 있었지만, 내 쪽으로는 비켜 주지 않았다.'), ('buri', '지금은 나가 주세요.')],"buri:consent:refused")
                $ r13_flag("buri_refused")
                return
            "지금은 자리를 비켜 준다":
                return
        jump r13_talk_menu
    if ROOM13["topics"][r13_topic].get("special"):
        if r13_topic in room13["read_topics"]:
            call r13_lines(r13_conversation_topic_lines(r13_topic),"topic:review:"+r13_topic)
        else:
            call r13_topic_choice(r13_topic)
            if _return:
                $ r13_finish_topic(r13_topic)
        jump r13_talk_menu
    call r13_lines(r13_conversation_topic_lines(r13_topic),"topic:"+r13_topic)
    $ r13_finish_topic(r13_topic)
    jump r13_talk_menu

label r13_first_night:
    if room13.get("life_poc"):
        call r13_life_first_night
        return
    call r13_scene("council","여관 식당","calm")
    call r13_lines([("nabi","탐정님, 뜨거워요. 그릇 밑으로 잡으세요."),("daram","아빠 건 제가 가져갈게요."),("nabi","두 번 오면 되잖아. 한 번에 다 들지 말고.")],"night1:meal")
    $ source_fx("knock")
    call r13_lines([(None,"현관을 두드리는 같은 박자의 소리가 이어졌다. 손님 한 명이 말없이 커튼을 쳤다."),("daram","누가 왔어요."),("granny","경비가 보고 있어."),("daram","문을 못 여는 것 같은데."),("nabi","……식기 전에 먹어.")],"night1:knocking")
    menu:
        "현관을 살핀다":
            call r13_lines([(None,"주민 한 명이 자기 집 방향을 말하지 못하고 있었다. 경비가 목덜미에 번호표를 달아 데려갔다. 누구도 소리를 지르지 않았다.")],"night1:look")
            $ r13_flag("first_patient_seen")
        "다람이 옆에 앉는다":
            call r13_lines([("daram","우리도 길 잃으면 저기로 가?"),("dad","길을 모르면 같이 물어보자.")],"night1:stay")
    $ r13_flag("night1_seen")
    return

label r13_case_choice:
    call r13_scene("hall","목요일 저녁 · 여관 2층 복도","night")
    call r13_lines([("karo","되돌아온 짐이 마을 바깥 초소에 도착했어요. 확인하러 가실 거죠?"),("daram","할아버지 물건은 내가 받아둘게. 방에서 같이 기다릴게."),(None,"계단 아래에서 할머니가 고개를 끄덕였다. 아이는 자기가 봐 주겠다는 얼굴이었다."),("dad","(짐을 받으러 갈까, 아이 곁에 남을까.)",{"thought":True})],"case:appointment:v4")
    menu:
        "되돌아온 짐은 미루고 방에서 함께 기다린다":
            $ r13_flag("father_accompanied")
            jump r13_prevented
        "통로에 사람을 세우고 나비에게 동행을 부탁한다" if r13_has("E05") and r13_has("E18"):
            $ r13_flag("route_watched")
            jump r13_prevented
        "까로와 되돌아온 짐을 확인하러 간다":
            call r13_lines([("dad","할머니하고 있어. 돌아와서 함께 보자."),("daram","금방 와?"),("dad","받는 대로 올게.")],"case:separate:v4")
    call r13_scene("winter","바깥 초소 · 되돌아온 짐","night")
    call r13_lines([("karo","봉투 위 날짜를 봐요. 이건 부인이 여기 오기 전에 보냈던 물건 같네요."),(None,"오래된 우체국 날짜 도장이 젖어 있었다. 안에는 우리가 보냈던 장갑과 맡김표가 있었다."),("dad","이걸 받으러 오라고 한 사람은요?"),("karo","전달은 여관에서 했죠. 지금 연락인 줄 알았는데…….")],"case:father:parcel:v3")
    $ r13_grant(["E34"],"까로와 바깥 초소에서 되돌아온 짐을 직접 확인")
    call r13_scene("hall","여관 2층 · 연기가 새는 문","quiet")
    call r13_cinematic("return")
    $ source_fx("knock")
    call r13_lines([(None,"계단 위에서 나무를 두드리는 소리가 들렸다. 우리 방 문 아래로 연기가 샜다."),("nabi","다람아, 거기 있어. 문에서 떨어져!"),("dad","무슨 일이에요?"),("doto","안의 빗장이 안 풀립니다. 비명 듣고 바로 왔는데."),("dad","다람아!"),("daram","아빠…… 나 여기."),("granny","비켜요. 공구 가져왔어."),(None,"도토가 지렛대를 받아 문틀 틈에 밀어 넣었다. 너울과 함께 문을 받쳤다.")],"case:father:return:v3")
    $ source_fx("impact")
    $ r13_edit(case_state="occurred",victim_state="dead",location="room13",kitchen_switch=False,passage_open=False)
    call r13_scene("room","여관 2층 · 13호 구조 직후","quiet")
    call r13_cinematic("rescue")
    call r13_lines([(None,"빗장 고정부가 뜯겨 나갔다. 너울이 작은 깔개 위로 젖은 천을 덮었다. 침대는 타지 않았다."),("dad","다람아. 나와도 돼. 아빠가 잡아 줄게."),(None,"침대 아래에서 다람이가 손을 뻗었다. 그 옆 바닥에 어르신이 쓰러져 있었다."),("daram","내가 때렸어."),("dad","어디 다쳤어?"),("daram","아빠, 내가 때렸다고."),(None,"아이의 손목에 눌린 자국이 보였다. 촛대는 바닥에서 두 부분으로 갈라져 있었다.")],"case:discovery:v3")
    menu:
        "아이를 안고 너울에게 바닥 모습과 물건을 거둔 순서를 남겨 달라고 한다":
            call r13_lines([("dad","아이는 제가 데리고 나가겠습니다. 사람부터 살피되 물건을 옮긴 자리는 남겨 주세요."),("neoul","문 앞을 막겠습니다. 도토 씨, 지금 보이는 자국부터 그려 주십시오.")],"case:preserve:v3")
            $ r13_flag("floor_preserved")
            $ r13_grant(["E33"],"구한 직후 너울·도토가 남긴 방 그림과 봉해 둔 물건")
        "아이를 데리고 나와 진료할 사람을 부른다":
            call r13_lines([("buri","할아버지! 비켜요!"),("neoul","발밑에 물건이 있습니다."),(None,"사람들이 어르신 곁으로 모였다. 너울이 촛대를 거둬 갔지만 바닥의 자국은 이미 여러 발에 겹쳐졌다.")],"case:unpreserved:v3")
    call r13_lines([("resident_seori","숨이 없습니다. 아이 팔도 보겠습니다."),(None,"촛대의 휘어진 장식 고리에 금속 조각이 걸려 있었다. 너울이 그대로 싸서 봉해 두었다."),("daram","내가 놓으라고 했어. 그런데 안 놔서……."),("granny","아이를 잡아당기지 말아요. 얘도 떨잖아."),("neoul","확인할 때까지 초소 보호실에 둡니다."),("dad","아이만요?"),("neoul","아버님은 까로 씨와 밖에 있던 게 확인됐습니다."),("dad","아이를 만나겠습니다. 아이 말은 고치지 말고 그대로 남겨 주세요.")],"case:sealing:v3")
    $ r13_grant(["E07","E08","E14"],"구한 직후 봉해 둔 범행 도구와 처음 살핀 진료 기록")
    $ r13_flag("family_room_unusable")
    $ r13_edit(daram_state="held",period=3,location="inn")
    call r13_lines([("nabi","짐은 옆방으로 옮겨둘게요. 오늘부터는 거기서 쉬세요."),(None,"13호 열쇠를 내려놓았다. 다람이가 가져오겠다고 했던 가방만 손에 남았다.")],"case:displaced:v3")
    jump r13_roam

label r13_prevented:
    call r13_scene("room","13호실","night")
    if r13_has("route_watched"):
        call r13_lines([(None,"나비에게 아이 곁을 부탁하고, 어르신에게 통로를 알고 있다고 전했다. 문은 열린 채였다."),("resident_owlgp","그럼 여기서 기다리지 맙시다. 아래로 내려가요.")],"case:prevented:watch")
    else:
        call r13_lines([("resident_owlgp","되돌아온 짐 찾으러 간 줄 알았소."),("dad","그건 내일도 확인할 수 있습니다."),("daram","같이 왔어요. 보여 준다는 거, 이제 봐도 돼요?"),(None,"어르신의 손이 잠깐 떨렸다. 옆에 앉아 기다리자 쥐고 있던 봉투를 놓았다."),("resident_owlgp","아래에서 이야기합시다. 이 방은 답답해.")],"case:prevented:accompany")
    call r13_lines([("granny","다 같이 계셨네. 아이하고 있으려고 왔어요. 차라도 내올까요?"),("dad","식당에서 함께 마시겠습니다."),(None,"그날 13호에서는 아무도 죽지 않았다. 누군가의 범행을 막았다는 증거까지 얻은 것은 아니다.")],"case:prevented:result")
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
    call r13_lines([("seryeon","부엉이 어르신이 발견된 방은 안에서 잠겨 있었습니다. 안에는 다람 양이 있었습니다."),("buri","이름으로 말씀해 주세요. 그냥 ‘죽은 사람’이라고 하지 마시고요."),("resident_seori","오늘 확인할 것은 아이가 그 죽음에 책임이 있는지입니다. 소문을 본 일처럼 말하지 마십시오."),("resident_ppul","아이가 위험하다면 다른 아이들부터 지켜야 합니다."),("dad","위험하다는 판단도 확인한 사실로 해주십시오.")],"trial:opening")
label r13_trial_choose:
    # 반론할 자료가 없는 논점은 선택지 없이 지나가고, 남은 논점이 없으면 바로 판결이다.
    $ r13_trial_pending=[c for c in r13_case_available() if c not in room13["propositions"] and not r13_debate_closed(c)]
    $ r13_trial_gap=next((c for c in r13_trial_pending if not r13_debate_arguable(c)),None)
    if r13_trial_gap:
        call r13_argument(r13_trial_gap) from r13_trial_gap_return
        jump r13_trial_choose
    if not r13_trial_pending:
        jump r13_verdict
    menu:
        "어느 주장을 다룰까?"
        "정문이 잠겼으니 아이만 그럴 수 있었다는 주장" if "C1" in r13_trial_pending:
            call r13_argument("C1")
        "다람이의 방어가 죽음의 원인이라는 주장" if "C2" in r13_trial_pending:
            call r13_argument("C2")
        "할머니는 그때 식당에 있었다는 말" if "C3" in r13_trial_pending:
            call r13_argument("C3")
        "할머니가 도우러 들어갔을 뿐이라는 변명" if "C4" in r13_trial_pending:
            call r13_argument("C4")
    jump r13_trial_choose

label r13_argument(claim):
    $ r13_claim=claim
    if claim=="C1":
        call r13_lines([("seryeon","복도에 있던 사람들은 아무도 들어가지 않았다고 합니다."),("dad","그분들이 본 문이 어느 문인지 확인하고 싶습니다.")],"trial:C1:start")
    elif claim=="C2":
        call r13_lines([("resident_ppul","겁을 먹은 건 알겠습니다. 하지만 맞은 사람이 죽었습니다."),("buri","할아버지가 먼저 손을 잡았다는 것도 지금은 듣겠어요. 그다음은요?")],"trial:C2:start")
    elif claim=="C3":
        call r13_lines([("granny","비명이 들릴 때 나는 식당에 있었어요. 다들 봤잖아요.")],"trial:C3:start")
    else:
        if r13_has("granny_prepared:E09"):
            call r13_lines([("granny","아버님이 보여 준 자국도 오래된 것일 수 있다고 했죠. 들어갔다고 해도 도우려던 건지 어떻게 알아요?")],"trial:C4:prepared")
        elif any(r13_has("granny_prepared:"+e) for e in ("E13","E14","E35","E36")):
            call r13_lines([("granny","브로치를 조사하신다기에 말씀드려요. 그분을 오후에 도왔을 때 떨어졌을 수도 있잖아요.")],"trial:C4:prepared_pin")
        else:
            call r13_lines([("granny","잠깐 주방에 갔다고 내가 그 방에 갔다는 건가요? 갔더라도 아픈 분을 도우려던 거라면요?")],"trial:C4:start")
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
            "앞문만 본 사람의 말로, 다른 길로 드나든 것까지 없었다고 할 수는 없다":
                call r13_lines([("resident_seori","정문 말고도 드나들 길이 있었군요. 아이만 들어갈 수 있었다는 말은 고치십시오."),("seryeon","그 안에 어머니 물건도 있었다면서요. 그날 들어간 사람은 어머니입니까?")],"trial:C1:counter")
                menu:
                    "오래된 생활 흔적은 그날 출입했다는 증거가 아니다":
                        call r13_lines([("resident_seori","맞습니다. 그날 누가 드나들었는지는 따로 확인해야 합니다.")],"trial:C1:done")
                        return True
                    "엄마는 절대 그럴 사람이 아니다":
                        call r13_lines([("seryeon","가족을 믿는다는 답변으로 출입 여부가 확인되지는 않습니다.")],"trial:C1:wrong")
            "통로가 있으니 할머니가 범인이다":
                call r13_lines([("resident_seori","통로가 있으니 드나들 수 있었다는 건 알 수 있습니다. 하지만 누가 썼는지는 아직 밝혀지지 않았습니다.")],"trial:C1:overreach")
    elif claim=="C2":
        menu:
            "촛대가 부서진 순서와 상처를 이어 보면?"
            "목숨을 앗아 간 상처는 촛대가 갈라진 뒤 생겼다. 그때 아이가 어디 있었는지 맞춰 본다":
                call r13_lines([("seryeon","첫 공격 때문에 나중에 쓰러졌을 가능성은요?"),("dad","팔의 상처만으로는 목숨을 앗아 간 머리 상처를 설명할 수 없습니다. 떨어져 나간 촛대 윗부분이 다시 쓰였습니다. 그 사이 아이가 어디 있었는지, 누가 다른 길로 드나들었는지 함께 봐야 합니다."),("resident_seori","나온 관찰과 방의 기록을 함께 보면, 아이가 했다고 확인된 일과 어르신을 죽게 한 공격은 같은 일이라고 적을 수 없습니다."),("daram","그럼…… 내가 때린 건?"),("dad","그건 네가 손을 놓게 하려고 한 일이야. 죽게 한 공격과는 달라.")],"trial:C2:done")
                return True
            "다람이는 착한 아이니 사람을 죽일 수 없다":
                call r13_lines([("buri","할아버지도 착한 사람이었어요. 그런 말로 끝내지 말아요.")],"trial:C2:wrong")
    elif claim=="C3":
        menu:
            "나비의 참인 목격과 통로 이동 시간을 연결하면?"
            "첫 비명 때 식당에 있었지만 나중 공격 시간은 비어 있다":
                call r13_lines([("nabi","제가 본 건 처음 비명 때였어요. 그 뒤 주방 안까지 본 건 아니에요."),("granny","그러니까 내가 잠깐 안 보였다는 게 전부잖아요."),("resident_seori","어르신이 해를 입었을 수 있는 시간 내내 다른 곳에 있었다는 증거는 되지 못합니다. 실제로 손을 댔는지 이어서 보겠습니다.")],"trial:C3:done")
                return True
            "나비가 할머니 편이므로 전부 거짓말이다":
                call r13_lines([("nabi","제가 같이 있던 것까지 없던 일로 만들지는 마세요.")],"trial:C3:wrong")
    else:
        menu:
            "핀 조각과 그날 뒷정리 기록으로 어떤 변명을 막을까?"
            "첫 비명 뒤에 있던 핀과, 거둬 올 때의 범행 도구를 이어서 ‘구하다가 만졌다’는 말을 뒤집는다":
                call r13_lines([("dad","나비가 첫 비명 때 잠가 준 핀입니다. 구한 직후 봉해 둔 범행 도구에 그 조각이 끼어 있었어요. 거둬 간 뒤에 묻은 게 아닙니다."),("granny","그래서 들어갔다고 해도, 도와달라고 한 거라면요?"),("dad","내려친 쪽으로 눌린 고리 안에서 핀도 함께 휘었습니다. 주워 들다가 나중에 들어간 조각이 아닙니다. 첫 비명 때는 목도리에 있던 것이죠."),("resident_seori","전날 어르신이 크게 변할 낌새를 알았던 것도 확인됐습니다. 위험을 모르고 둘만 두었다는 설명 역시 기록과 다릅니다. 방에서 나온 자료와는 따로 남기겠습니다."),("granny","……."),("resident_seori","대답하지 않으셔도, 모은 자료로 판단하겠습니다.")],"trial:C4:done")
                return True
            "핀 주인이니 다른 자료는 필요 없다":
                call r13_lines([("resident_seori","물건 주인과 범인은 같은 뜻이 아닙니다. 언제 어떻게 옮겨 갔는지 밝혀야 합니다.")],"trial:C4:wrong")
    return False

label r13_verdict:
    if "C2" in room13["propositions"]:
        $ r13_edit(daram_state="with_dad",trial_result="cleared")
        call r13_lines([("resident_seori","다람 양이 죽였다는 의심을 받치던 설명은 더 이상 설 수 없습니다. 아이를 풀어 주십시오."),("resident_ppul","가족에게 돌려보내겠습니다. 남은 사안은 따로 기록하시오.")],"verdict:cleared")
        if "C4" in room13["propositions"]:
            $ r13_edit(granny_state="detained",trial_result="culprit_proven")
            call r13_lines([("resident_seori","할머니가 손을 대고 그것을 숨긴 일, 어르신을 죽게 한 일은 따로 확인됐습니다. 증거를 망치지 못하도록 할머니를 붙잡아 두십시오."),("neoul","일어나시죠.")],"verdict:culprit")
        call r13_lines([("daram","할아버지는 이제 못 만나지."),("dad","응."),("daram","나 안 죽였다고 말하고 싶은데."),("dad","부리한테도, 네가 준비되면 말하자.")],"verdict:child")
    else:
        $ r13_edit(daram_state="held",trial_result="detained")
        call r13_lines([("resident_seori","뒤집힌 부분은 남겼습니다. 하지만 오늘 모은 것만으로는 아이를 풀어 달라는 요청이 받아들여지지 않았습니다."),("resident_ppul","추가 확인은 보호시설에서 하겠습니다."),("dad","확인하지 못한 일을 아이 죄로 못 박지 마십시오."),("daram","아빠는 못 와?"),("neoul","오늘은 여기까지입니다."),("dad","다시 올게. 어디로 옮기면 꼭 남겨 줘."),("daram","아빠도. 못 오면…… 누가 온다고 말해 줘.")],"verdict:held")
    $ r13_edit(trial_ended=True,period=3)
    jump r13_week2_opening

label r13_prevention_hearing:
    call r13_lines([("seryeon","아이가 함께 들어왔다는 기록과, 따로 맡아 달라는 요청을 확인하겠습니다."),("resident_owlgp","아이는 나와 함께 있었소. 죽은 사람도, 아이가 저지른 살인도 없소. 없는 사건을 만들지는 맙시다."),("granny","낯선 아이를 따로 보호하자는 뜻이었어요."),("dad","보호자는 여기 있습니다. 입구에서 함께 등록한 원본도 있고요.")],"prevention:hearing")
    menu:
        "바로잡은 입장 기록 원본을 직접 보여 준다":
            call screen r13_book("resident_seori",present=True,hearing=True)
            if _return=="E02":
                call r13_lines([("resident_seori","아빠와 딸이 함께 들어왔다는 기록은 그대로 인정됩니다. 따로 떼어 놓으라는 요청은 이유가 없다고 봅니다.")],"prevention:registered")
            else:
                call r13_lines([("resident_owlgp","초소 원본을 여기서 직접 맞춰 봅시다. 아이를 떼어 놓고 볼 일이 아니오."),(None,"초소 담당자를 불러 원본을 확인했다. 그동안 부녀는 함께 기다렸다.")],"prevention:independent_check")
        "어르신과 함께 사람들 앞에서 맞춰 보자고 한다":
            call r13_lines([("resident_owlgp","내가 같이 있었소. 원본과 확인한 사람을 함께 부르시오."),("resident_seori","사람들 앞에서 맞춰 보기 전까지 가족을 떼어 놓지 마십시오.")],"prevention:witness")
    $ r13_edit(trial_result="prevention_hearing",trial_ended=True,daram_state="with_dad",period=3)
    jump r13_week2_opening

