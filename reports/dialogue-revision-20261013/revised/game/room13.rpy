# Full campaign entry and first-week scenes; continuation is in room13_week2.rpy.
label r13_scene(bg,title,mood="calm"):
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
    while r13_index<len(entries):
        $ r13_packet=entries[r13_index]
        $ r13_thought_active=bool(len(r13_packet)>2 and isinstance(r13_packet[2],dict) and r13_packet[2].get("thought"))
        $ r13_expression,r13_directed_pose=r13_line_performance(identity,r13_index,r13_packet)
        if r13_thought_active:
            $ r13_expression,r13_directed_pose="thinking","thinking"
        $ r13_speaker(r13_packet[0],r13_expression,r13_directed_pose)
        $ r13_read_id=r13_before_line(identity,r13_index,r13_packet[1])
        $ R13_CHARS.get(r13_packet[0],source_thought)(r13_packet[1])
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
    $ r13_inspection_location=None
    $ r13_prepare_history()
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
    if persistent.room13_opening_seen:
        menu:
            "마차에서 나눈 이야기를 다시 볼까?"
            "마을 입구부터 시작한다":
                pass
            "마차 장면부터 본다":
                call r13_carriage
    else:
        call r13_carriage
    $ r13_grant(["E01"],"여행 중 가지고 온 편지")
    $ r13_edit(period=1)
    call r13_scene("winter","눈에 막힌 입구","calm")
    call r13_lines([("karo","도착했어요. 발판이 얼었으니 천천히 내려요."),("daram","까로 아저씨, 이 가방도 내려 주세요."),("karo","내려 줄게. 짐은 내가 볼 테니 접수부터 하고 와요.")],"entry:karo:arrival")
    call r13_lines([("guard","성함 확인했습니다. 어른은 이쪽으로 오세요."),("daram","나는?"),("guard","저 안에서 기다리면 돼."),("dad","제 딸입니다. 함께 들어가겠습니다."),("guard","여기엔 어른 한 분만 적혀 있습니다. 아이는 확인이 끝날 때까지 따로 기다려야 합니다."),(None,"작은 대기소 안에서 손잡이가 흔들렸다. 문은 열리지 않았다."),("daram","아빠. 나 여기 있을게."),("dad","같이 확인하죠.")],"entry:arrival")
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
    window hide
    hide r13_visitor
    $ dialogue_speaker=None
    call screen r13_entry_topics
    $ r13_choice=_return
label r13_entry_dispatch:
    if r13_choice==("entry","explain"):
        call r13_lines([("guard","제가 받은 명부에는 한 분뿐입니다. 아이 이름은 원본을 봐야 알겠군요."),("dad","그걸 확인할 동안 아이를 저 안에 혼자 두겠다는 겁니까?"),("guard","……초소에 원본과 인계 규정이 있습니다. 먼저 보시겠습니까?")],"entry:explain")
    elif r13_choice[0]=="object":
        call r13_object(r13_choice[1])
    elif r13_choice[0]=="empty":
        $ r13_mark("empty:%d:%d"%(r13_choice[1][0]//70,r13_choice[1][1]//70),*r13_choice[1])
        call r13_lines([(None,"흩날리는 눈을 털어 냈다. 눈에 띄는 흔적은 없다.")],"entry:empty")
    elif r13_choice[1]=="argue":
        call screen r13_book("guard",present=True)
        $ r13_item=_return
        if r13_item in ("G1","G2","G3"):
            call r13_lines([("guard","어느 부분이 잘못됐다는 겁니까?")],"entry:reason")
            $ r13_speaker("guard","neutral")
            menu:
                "원본에는 두 명이고, 아이 인계에는 보호자 확인이 필요합니다" if r13_has("G1") and r13_has("G2"):
                    call r13_lines([("guard","원본에는 두 분이군요. 옮겨 적다가 빠졌습니다. 정정하겠습니다."),("dad","사본도 주십시오. 제가 가지고 있겠습니다."),("daram","다람. 내 이름도 그렇게 적혀 있죠?")],"entry:corrected")
                    jump r13_entry_done
                "같이 왔으니 믿어 주십시오":
                    call r13_lines([("guard","같이 오신 건 봤습니다. 그런데 말만 듣고 명부를 고칠 수는 없습니다. 원본과 맞춰 봐야 합니다.")],"entry:insufficient")
                "다른 자료를 확인하겠습니다":
                    pass
        elif r13_item:
            call r13_lines([("guard","숙소에서 보낸 편지군요. 다만 이 편지만으로 접수 명부를 고칠 수는 없습니다. 원본을 봐야 합니다.")],"entry:letter")
    elif r13_choice[1]=="wait":
        call screen r13_confirm("대기소 앞에서 원본 담당자가 돌아오기를 기다린다. 저녁까지 시간이 흐른다.")
        if _return:
            $ r13_tick()
            call r13_scene("winter","눈에 막힌 입구","calm")
            call r13_lines([("guard","대조했습니다. 아이 이름이 빠졌더군요. 두 분 함께 들어가세요."),("daram","아빠, 이제 손이 잘 안 펴져."),("dad","오래 기다리게 했네. 손 줘. 같이 가자.")],"entry:wait")
            jump r13_entry_done
    if r13_choice[0]=="entry" and r13_choice[1] in ("explain","argue","wait"):
        jump r13_entry_guard_menu
    jump r13_entry

label r13_entry_person(person):
    if person=="daram":
        call r13_lines([("daram","아빠, 이거 안 열려."),("dad","들려. 아빠 여기 있어. 멀리 안 갈게."),("daram","응. 나 여기서 기다릴게.")],"entry:daram:waiting")
        return
    if person!="karo":
        return
label r13_entry_karo_menu:
    window hide
    hide r13_visitor
    call screen r13_entry_karo_topics
    $ r13_entry_karo_choice=_return
    if r13_entry_karo_choice=="road":
        call r13_lines([("karo","축에 금이 갔어요. 내려올 때 소리가 영 안 좋더라니."),("dad","수리하면 돌아갈 수 있습니까?"),("karo","마차만 고쳐선 안 돼요. 고개도 막혔거든요. 길이 열리면 먼저 말씀드릴게요.")],"entry:karo:road")
        $ r13_flag("road_known")
    elif r13_entry_karo_choice=="witness":
        call r13_lines([("karo","제 마차에 두 분 다 탔습니다. 그건 제가 봤어요."),("guard","동행하신 건 압니다. 여기 적힌 인원과 맞지 않아서 그러는 겁니다."),("dad","아이를 저 안에 계속 둘 순 없습니다. 장부부터 봅시다."),("karo","짐은 여기 둘게요. 확인 끝나면 불러요.")],"entry:karo:witness")
    elif r13_entry_karo_choice=="bags":
        call r13_lines([("karo","이 담요 밑에 둘게요. 눈에 젖으면 방에 가서도 한참 말려야 하니까.")],"entry:karo:bags")
    elif r13_entry_karo_choice=="back":
        hide r13_visitor
        $ dialogue_speaker=None
        return
    jump r13_entry_karo_menu

label r13_entry_done:
    $ r13_inspection_location=None
    $ r13_grant(["E02"],"원본과 대조해 정정받은 등록")
    $ r13_flag("entry_corrected")
    call r13_lines([("karo","짐은 여관까지 옮겨 드릴게요. 마차는 여기 세워 둬야겠네요."),("daram","……가방은 내가 들게. 아빠 손 시려.")],"entry:departure")
    jump r13_roam

label r13_carriage:
    call r13_scene("winter_carriage","마차 안","travel")
    call r13_lines([(None, '차가 덜컹일 때마다 창틀이 작게 울렸다. 다람이가 내 소매를 잡아당겼다.'), ('daram', '아빠. 사건이야.'), ('dad', '벌써? 아직 마을에도 안 왔는데.'), ('daram', '왼손만 얼고 있어. 오른손은 괜찮고.'), (None, '나는 다람이의 손을 잡았다. 창문 쪽 손끝이 차가웠다.'), ('dad', '이쪽으로 바람이 들어오는구나.'), ('daram', '그건 내가 먼저 찾았어. 아빠는 눈 감고 있었잖아.'), ('dad', '눈 감고 생각하고 있었지.'), ('daram', '코로 생각했어? 소리가 나던데.'), (None, '나는 대답 대신 자리를 조금 비켰다. 다람이는 웃으며 내 옆으로 붙었다.'), ('dad', '범인은 창틀이고, 해결은 내가 할게.'), (None, '접은 천을 창틀 틈에 끼웠다. 흔들리던 천 끝이 가만해졌다.'), ('daram', '그러면 나는 뭘 해?'), ('dad', '바람이 멎었는지 확인해 줘.'), (None, '다람이가 손을 펴고 잠깐 기다렸다.'), ('daram', '응. 잡았어. 아빠가.'), ('dad', '네가 먼저 찾았잖아.'), (None, '다람이는 손을 내려 편지의 구겨진 모서리를 폈다. 이번에는 장난치는 얼굴이 아니었다.'), ('daram', '엄마가 있던 방에 가는 거지?'), ('dad', '응. 편지에 적힌 곳부터 가 보자.'), ('daram', '엄마도 거기 있으면 좋겠다.'), (None, '있을 거라고 말하고 싶었다. 대신 펴지지 않는 모서리를 같이 눌렀다.'), ('dad', '나도.'), ('daram', '찾을 때는 나도 같이야.'), ('dad', '그래. 나 혼자 먼저 가지 않을게.'), ('karo', '후후, 손님. 저 앞 불빛 보이시죠? 곧 도착합니다.'), ('daram', '까로 아저씨! 도착하면 밥 먹을 데도 있어요?'), ('karo', '여관에서 물어보시면 되죠. 저는 길 안내까지 맡겠습니다.'), ('daram', '아빠, 길은 아저씨가 알아.'), ('dad', '나는 뭐 맡을까?'), ('daram', '밥. 따뜻한 것 말고 이름 있는 밥.'), ('dad', '배고픈 탐정은 까다롭네.'), ('daram', '눈 감고 생각하는 탐정도 까다로워.'), (None, '멀리 보이던 불빛이 가까워졌다. 다람이가 옆자리에 놓인 장갑 한 짝을 내 손에 얹었다.'), ('dad', '네가 끼고 있어.'), ('daram', '아빠 손도 차가워졌잖아. 다음 사건은 그거야.')],"opening:carriage:duo:v2")
    $ persistent.room13_opening_seen=True
    return

label r13_day:
    if room13["day"]==4 and not r13_has("elder_appointment"):
        call r13_scene("hall","여관 계단","calm")
        call r13_lines([("resident_owlgp","저녁에 댁 방으로 들르겠소. 부인에게 받은 걸 돌려드려야지."),("dad","아내에 관한 겁니까?"),("resident_owlgp","보관해 둔 기록이오. 그분이 지금 어디 있는지는 나도 모르오."),("granny","반송품 찾으러 나가신다면서요. 내가 아이하고 있어 줄게요."),("daram","받아만 둘게. 아빠 오면 같이 보자."),("dad","가능하면 그 전에 돌아오겠습니다."),("resident_owlgp","물건만 전해 두리다. 이야기는 같이 합시다.")],"day4:appointment:v3")
        $ r13_flag("elder_appointment")
    if room13["day"]==5 and room13["case_state"]=="occurred" and not r13_has("trial_notice"):
        call r13_scene("front","여관 접수대","quiet")
        call r13_lines([("neoul","일요일에 주민 앞에서 사건을 다룹니다. 아이는 그때까지 보호실에 둡니다."),("dad","판결 전인데 구금부터 합니까?"),("neoul","현장에 있던 아이를 데려가면 다른 사람들이 가만있지 않습니다. 면회는 막지 않겠습니다."),(None,"등록 정정 원본은 돌려받았다. 함께 입장할 권리를 확인한 것과, 지금 씌워진 혐의는 다른 문제였다.")],"day5:notice")
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
    if r13_choice[1] in ("doorway","room_inside"):
        $ r13_edit(location="hall" if r13_choice[1]=="doorway" else "room13")
        jump r13_roam
    if r13_choice[1]=="people":
        call screen r13_nearby
        if _return:
            $ r13_target=_return
            call r13_talk
        jump r13_roam
    if r13_choice[1]=="map":
        call screen r13_map
        if _return and _return!=room13["location"]:
            $ r13_edit(location=_return)
            jump r13_roam
        jump r13_field
    jump r13_field

label r13_object(key):
    $ r13_spec=ROOM13["objects"][room13["location"]][key]
    if not r13_object_visible(r13_spec):
        return
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
    return

label r13_talk:
    $ r13_first_encounter = r13_target not in r13_met_people()
    $ r13_note_encounter(r13_target)
    $ r13_encounter_key="met:"+r13_target+":"+str(room13["day"])
    if not r13_has(r13_encounter_key):
        if r13_target=="bami" and r13_has("bami_pressured"):
            call r13_lines([(None, '밤이는 나를 보기 전에 복도를 살폈다. 나는 그 순서가 마음에 걸렸다.'), ('bami', '누가 제가 처마에 있었다고 했대요. 제 이름 말씀하셨어요?'), ('dad', '……다시 혼자 두지는 않을게.'), ('bami', '또 약속이네요.'), (None, '밤이가 문 쪽으로 몸을 돌렸다. 내 대답은 그 등 뒤에 남았다.'), ('bami', '탐정님 안 계실 때 숨는 건 저예요. 이번에는 말만 하지 마세요.')],"greeting:bami:pressured")
        elif r13_target=="buri" and room13["victim_state"]=="dead":
            call r13_lines([("buri","수리하러 오신 거 아니죠. 할아버지 이름을 꺼내실 거면 먼저 말씀해 주세요.")],"greeting:buri:bereaved")
        elif r13_target in R13_OPENING_SCENES["first_meetings"]:
            $ r13_opening_lines = r13_conversation_opening(r13_target, r13_first_encounter)
            call r13_lines(r13_opening_lines,"greeting:opening:"+r13_target+(":first" if r13_first_encounter else ":return")) from r13_dialogue_opening_return
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
                call r13_lines([(None,"밤이는 경비가 찾아오는 것을 두려워했다. 이 기록의 이름과 숨어 있던 자리를 알리면 상대도 밤이를 찾아갈 수 있다. 관찰한 내용만 전할지, 신원까지 밝힐지 내가 결정해야 한다.")],"disclosure:bami:warning")
                menu:
                    "관찰 내용만 설명한다":
                        $ r13_disclose_name=False
                    "밤이의 이름까지 밝힌다":
                        $ r13_disclose_name=True
                    "제시를 취소한다":
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
            "확인한 상처만 이야기하고, 병력 공개는 가족에게 묻는다":
                if r13_has("buri_refused"):
                    if r13_has("E08"):
                        call r13_lines([("dad","제가 한 말도 바로잡겠습니다. 실제 기록에는 팔을 잡은 흔적과 머리의 부상을 따로 적었습니다. 어르신이 무엇을 하려 했는지는 아직 모릅니다."),("buri","그 정정도 같이 남겨 주세요. 저한테만 하시는 말씀이면 소용없어요.")],"buri:consent:repair")
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
            call r13_lines(ROOM13["topics"][r13_topic]["lines"],"topic:review:"+r13_topic)
        else:
            call r13_topic_choice(r13_topic)
            if _return:
                $ r13_finish_topic(r13_topic)
        jump r13_talk_menu
    call r13_lines(r13_conversation_topic_lines(r13_topic),"topic:"+r13_topic)
    $ r13_finish_topic(r13_topic)
    jump r13_talk_menu

label r13_first_night:
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
    call r13_lines([("karo","반송품이 외곽 초소에 도착했어요. 확인하러 가실 거죠?"),("daram","할아버지 물건은 내가 받아둘게. 방에서 같이 기다릴게."),("dad","할머니하고 있어. 돌아와서 함께 보자."),(None,"계단 아래에서 할머니가 고개를 끄덕였다.")],"case:appointment:v3")
    menu:
        "반송품은 미루고 방에서 함께 기다린다":
            $ r13_flag("father_accompanied")
            jump r13_prevented
        "통로에 사람을 세우고 나비에게 동행을 부탁한다" if r13_has("E05") and r13_has("E18"):
            $ r13_flag("route_watched")
            jump r13_prevented
        "까로와 반송품을 확인하러 간다":
            call r13_lines([("daram","금방 와?"),("dad","받는 대로 올게.")],"case:separate:v3")
    call r13_scene("winter","외곽 초소 · 반송품","night")
    call r13_lines([("karo","봉투 위 날짜를 봐요. 이건 부인이 여기 오기 전에 보냈던 물건 같네요."),(None,"묵은 소인이 젖어 있었다. 안에는 우리가 보냈던 장갑과 보관표가 있었다."),("dad","이걸 받으러 오라고 한 사람은요?"),("karo","전달은 여관에서 했죠. 지금 연락인 줄 알았는데…….")],"case:father:parcel:v3")
    $ r13_grant(["E34"],"까로와 외곽 초소에서 반송품을 직접 확인")
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
        "아이를 안고 너울에게 바닥과 회수 순서를 남겨 달라고 한다":
            call r13_lines([("dad","아이는 제가 데리고 나가겠습니다. 사람부터 살피되 물건을 옮긴 자리는 남겨 주세요."),("neoul","문 앞을 막겠습니다. 도토 씨, 지금 보이는 자국부터 그려 주십시오.")],"case:preserve:v3")
            $ r13_flag("floor_preserved")
            $ r13_grant(["E33"],"구조 직후 너울·도토가 남긴 현장 그림과 봉인")
        "아이를 데리고 나와 진료할 사람을 부른다":
            call r13_lines([("buri","할아버지! 비켜요!"),("neoul","발밑에 물건이 있습니다."),(None,"사람들이 어르신 곁으로 모였다. 너울이 촛대를 회수했지만 바닥의 자국은 이미 여러 발에 겹쳐졌다.")],"case:unpreserved:v3")
    call r13_lines([("resident_seori","숨이 없습니다. 아이 팔도 보겠습니다."),(None,"촛대의 휘어진 장식 고리에 금속 조각이 걸려 있었다. 너울이 그대로 싸서 봉인했다."),("daram","내가 놓으라고 했어. 그런데 안 놔서……."),("granny","아이를 잡아당기지 말아요. 얘도 떨잖아."),("neoul","확인할 때까지 초소 보호실에 둡니다."),("dad","아이만요?"),("neoul","아버님은 까로 씨와 밖에 있던 게 확인됐습니다."),("dad","면회하겠습니다. 아이 말은 고치지 말고 그대로 남겨 주세요.")],"case:sealing:v3")
    $ r13_grant(["E07","E08","E14"],"구조 직후의 흉기 봉인과 초기 진료 기록")
    $ r13_flag("family_room_unusable")
    $ r13_edit(daram_state="held",period=3,location="inn")
    call r13_lines([("nabi","짐은 옆방으로 옮겨둘게요. 오늘부터는 거기서 쉬세요."),(None,"13호 열쇠를 내려놓았다. 다람이가 가져오겠다고 했던 가방만 손에 남았다.")],"case:displaced:v3")
    jump r13_roam

label r13_prevented:
    call r13_scene("room","13호실","night")
    if r13_has("route_watched"):
        call r13_lines([(None,"나비에게 아이 곁을 부탁하고, 어르신에게 통로를 알고 있다고 전했다. 문은 열린 채였다."),("resident_owlgp","그럼 여기서 기다리지 맙시다. 아래로 내려가요.")],"case:prevented:watch")
    else:
        call r13_lines([("resident_owlgp","반송품 찾으러 간 줄 알았소."),("dad","그건 내일도 확인할 수 있습니다."),("daram","같이 왔어요. 보여 준다는 거, 이제 봐도 돼요?"),(None,"어르신의 손이 잠깐 떨렸다. 옆에 앉아 기다리자 쥐고 있던 봉투를 놓았다."),("resident_owlgp","아래에서 이야기합시다. 이 방은 답답해.")],"case:prevented:accompany")
    call r13_lines([("granny","다 같이 계셨네. 아이하고 있으려고 왔어요."),("dad","식당에서 마시겠습니다."),(None,"그날 13호에서는 아무도 죽지 않았다. 누군가의 범행을 막았다는 증거까지 얻은 것은 아니다.")],"case:prevented:result")
    $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",period=3,location="inn")
    $ r13_flag("victim_protected")
    $ r13_grant(["E17"],"살아 있는 어르신에게 받은 보관 사본")
    jump r13_roam

label r13_trial:
    if room13["trial_ended"]:
        jump r13_week2_opening
    call r13_scene("council","일요일 · 여관 공동 식당","hearing")
    if room13["case_state"]=="prevented":
        jump r13_prevention_hearing
    call r13_lines([("seryeon","부엉이 어르신이 발견된 방은 안에서 잠겨 있었습니다. 안에는 다람 양이 있었습니다."),("buri","이름으로 말씀해 주세요. 피해자라고만 하지 마시고요."),("resident_seori","오늘 확인할 것은 아이가 그 죽음에 책임이 있는지입니다. 소문을 본 일처럼 말하지 마십시오."),("resident_ppul","아이가 위험하다면 다른 아이들부터 지켜야 합니다."),("dad","위험하다는 판단도 확인한 사실로 해주십시오.")],"trial:opening")
label r13_trial_choose:
    menu:
        "어느 주장을 다룰까?"
        "정문이 잠겼으니 아이만 범행할 수 있었다는 주장" if "C1" not in room13["propositions"]:
            call r13_argument("C1")
        "다람이의 방어가 죽음의 원인이라는 주장" if "C2" not in room13["propositions"]:
            call r13_argument("C2")
        "할머니의 알리바이" if "C2" in room13["propositions"] and "C3" not in room13["propositions"]:
            call r13_argument("C3")
        "할머니가 도우러 들어갔을 뿐이라는 해명" if "C3" in room13["propositions"] and "C4" not in room13["propositions"]:
            call r13_argument("C4")
        "지금까지 확인한 사실로 판단을 요청한다":
            call screen r13_confirm("남은 논점은 입증하지 않은 채 판단을 요청합니다. 자료를 읽는 동안에는 시간이 흐르지 않습니다.","판단을 요청한다","계속 다룬다")
            if _return:
                jump r13_verdict
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
    window hide
    hide r13_visitor
    call screen r13_debate(r13_claim)
    $ r13_choice=_return
    if r13_choice=="leave":
        return
    if r13_choice=="present":
        call screen r13_book("resident_seori",present=True,hearing=True)
        $ r13_item=_return
        if not r13_item:
            if r13_present_origin=="actions":
                jump r13_person_actions
            jump r13_talk_menu
        if r13_item:
            $ r13_submit(r13_claim,r13_item)
            show screen r13_material_corner(r13_item)
            call r13_lines([("resident_seori",r13_evidence_feedback(r13_claim,r13_item))],"trial:feedback:"+r13_claim+":"+r13_item+":"+str(r13_has("bami_consent")))
            hide screen r13_material_corner
    elif r13_choice=="press":
        call r13_lines([("seryeon",R13_PRESS[r13_claim])],"trial:press:"+r13_claim)
    elif r13_choice=="argue":
        if not r13_argument_ready(r13_claim):
            call r13_lines([("resident_seori","확인된 부분은 남기겠습니다. 하지만 현재 낸 자료만으로는 이 주장의 빈틈을 모두 메우지 못했습니다. 새로 내지 않은 자료까지 판단에 넣지는 않겠습니다.")],"trial:insufficient:"+r13_claim)
        else:
            call r13_link_reason(r13_claim)
            if _return:
                $ r13_prove(r13_claim)
                if r13_claim=="C4":
                    call r13_cinematic("proof")
                return
    jump r13_argument_menu

label r13_link_reason(claim):
    if claim=="C1":
        menu:
            "도면과 실제 통로 조사를 어떻게 연결할까?"
            "앞문만 본 증언으로 다른 출입까지 부정할 수 없다":
                call r13_lines([("resident_seori","정문 외의 출입로가 있었군요. 아이만 들어갈 수 있었다는 표현은 정정하십시오."),("seryeon","그 안에 어머니 물건도 있었다면서요. 그날 들어간 사람은 어머니입니까?")],"trial:C1:counter")
                menu:
                    "오래된 생활 흔적은 그날 출입했다는 증거가 아니다":
                        call r13_lines([("resident_seori","맞습니다. 당일의 출입은 별도로 확인해야 합니다.")],"trial:C1:done")
                        return True
                    "엄마는 절대 그럴 사람이 아니다":
                        call r13_lines([("seryeon","가족을 믿는다는 답변으로 출입 여부가 확인되지는 않습니다.")],"trial:C1:wrong")
            "통로가 있으니 할머니가 범인이다":
                call r13_lines([("resident_seori","통로는 출입 가능성을 보여 줍니다. 이용자의 신원은 아직 입증되지 않았습니다.")],"trial:C1:overreach")
    elif claim=="C2":
        menu:
            "촛대의 파손 순서와 상처를 연결하면?"
            "치명상은 촛대가 갈라진 뒤 생겼다. 그때 아이의 위치를 대조한다":
                call r13_lines([("seryeon","첫 공격 때문에 나중에 쓰러졌을 가능성은요?"),("dad","팔의 흔적만으로 머리의 치명상은 설명되지 않습니다. 떨어져 분리된 촛대 윗부분이 다시 쓰였습니다. 그 사이 아이의 위치와 다른 출입을 함께 봐야 합니다."),("resident_seori","제출된 관찰과 현장 기록을 함께 보면, 아이가 했다고 확인된 행동과 사망에 이른 공격을 같은 것으로 적을 수 없습니다."),("daram","그럼…… 내가 때린 건?"),("dad","그건 네가 손을 놓게 하려고 한 일이야. 죽게 한 공격과는 달라.")],"trial:C2:done")
                return True
            "다람이는 착한 아이니 사람을 죽일 수 없다":
                call r13_lines([("buri","할아버지도 착한 사람이었어요. 그런 말로 끝내지 말아요.")],"trial:C2:wrong")
    elif claim=="C3":
        menu:
            "나비의 참인 목격과 통로 이동 시간을 연결하면?"
            "첫 비명 때 식당에 있었지만 나중 공격 시간은 비어 있다":
                call r13_lines([("nabi","제가 본 건 처음 비명 때였어요. 그 뒤 주방 안까지 본 건 아니에요."),("granny","그러니까 내가 잠깐 안 보였다는 게 전부잖아요."),("resident_seori","살해 가능 시각 전체의 알리바이로 삼을 수는 없습니다. 실제 접촉 여부를 이어서 보겠습니다.")],"trial:C3:done")
                return True
            "나비가 할머니 편이므로 전부 거짓말이다":
                call r13_lines([("nabi","제가 같이 있던 것까지 없던 일로 만들지는 마세요.")],"trial:C3:wrong")
    else:
        menu:
            "핀 조각과 수습 기록으로 어떤 해명을 막을까?"
            "첫 비명 뒤의 핀과 회수 당시 흉기를 연결해 구조 중 접촉을 반박한다":
                call r13_lines([("dad","나비가 첫 비명 때 잠가 준 핀입니다. 구조 직후 봉인한 흉기에 그 조각이 끼어 있었어요. 회수 후에 묻힌 물건은 아닙니다."),("granny","그래서 들어갔다고 해도, 도와달라고 한 거라면요?"),("dad","타격 방향으로 눌린 고리 안에서 핀도 함께 변형됐습니다. 주워 들다가 나중에 들어간 조각이 아닙니다. 첫 비명 때는 목도리에 있던 것이죠."),("resident_seori","전날 어르신의 강한 전조를 알았던 것도 확인됐습니다. 위험을 모르고 둘만 두었다는 설명 역시 기록과 다릅니다. 현장 자료와 별도로 남기겠습니다."),("granny","……."),("resident_seori","대답을 거부하셔도 확보한 자료는 판단하겠습니다.")],"trial:C4:done")
                return True
            "핀 주인이니 다른 자료는 필요 없다":
                call r13_lines([("resident_seori","물건 주인과 범인은 같은 뜻이 아닙니다. 언제 어떻게 옮겨 갔는지 입증해야 합니다.")],"trial:C4:wrong")
    return False

label r13_verdict:
    if "C2" in room13["propositions"]:
        $ r13_edit(daram_state="with_dad",trial_result="cleared")
        call r13_lines([("resident_seori","다람 양의 살인 혐의를 뒷받침하던 설명은 유지할 수 없습니다. 구금을 해제하십시오."),("resident_ppul","가족에게 돌려보내겠습니다. 남은 사안은 따로 기록하시오.")],"verdict:cleared")
        if "C4" in room13["propositions"]:
            $ r13_edit(granny_state="detained",trial_result="culprit_proven")
            call r13_lines([("resident_seori","할머니의 접촉과 은폐, 치명상에 이르는 행위는 별도로 확인됐습니다. 증거 훼손을 막기 위해 신병을 확보하십시오."),("neoul","일어나시죠.")],"verdict:culprit")
        call r13_lines([("daram","할아버지는 이제 못 만나지."),("dad","응."),("daram","나 안 죽였다고 말하고 싶은데."),("dad","부리한테도, 네가 준비되면 말하자.")],"verdict:child")
    else:
        $ r13_edit(daram_state="held",trial_result="detained")
        call r13_lines([("resident_seori","반박된 부분은 남겼습니다. 하지만 오늘 확보한 내용만으로 구금을 해제하라는 요청은 받아들여지지 않았습니다."),("resident_ppul","추가 확인은 보호시설에서 하겠습니다."),("dad","확인하지 못한 일을 아이 죄로 확정하지 마십시오."),("daram","아빠는 못 와?"),("neoul","오늘은 여기까지입니다."),("dad","다시 올게. 어디로 옮기면 꼭 남겨 줘."),("daram","아빠도. 못 오면…… 누가 온다고 말해 줘.")],"verdict:held")
    $ r13_edit(trial_ended=True,period=3)
    jump r13_week2_opening

label r13_prevention_hearing:
    call r13_lines([("seryeon","아이 등록과 별도 보호 요청을 확인하겠습니다."),("resident_owlgp","아이는 나와 함께 있었소. 죽은 사람도, 아이가 저지른 살인도 없소. 없는 사건을 만들지는 맙시다."),("granny","낯선 아이를 따로 보호하자는 뜻이었어요."),("dad","보호자는 여기 있습니다. 입구에서 함께 등록한 원본도 있고요.")],"prevention:hearing")
    menu:
        "등록 정정 원본을 직접 제시한다":
            call screen r13_book("resident_seori",present=True,hearing=True)
            if _return=="E02":
                call r13_lines([("resident_seori","부녀의 동행 등록은 유효합니다. 별도 분리 요청의 근거는 인정하지 않습니다.")],"prevention:registered")
            else:
                call r13_lines([("resident_owlgp","초소 원본을 여기서 직접 대조합시다. 아이를 떼어 놓고 볼 일이 아니오."),(None,"초소 담당자를 불러 원본을 확인했다. 그동안 부녀는 함께 기다렸다.")],"prevention:independent_check")
        "어르신과 함께 공개 대조를 요청한다":
            call r13_lines([("resident_owlgp","내가 같이 있었소. 원본과 확인한 사람을 함께 부르시오."),("resident_seori","공개 대조가 끝날 때까지 가족을 분리하지 마십시오.")],"prevention:witness")
    $ r13_edit(trial_result="prevention_hearing",trial_ended=True,daram_state="with_dad",period=3)
    jump r13_week2_opening

