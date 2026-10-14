# Fourteen-day playable scenario, separate from the archived thirteen-bed case.
default winter_mode = False
default winter = None
default winter_line = None
default winter_actor = None
default winter_presentation = None
default winter_claim_index = 0
default winter_pressure = 0
default winter_selected = []
default winter_hearing_id = None
default winter_hearing_wins = []
default winter_choice = None
default winter_action_id = None
default winter_feedback = ""
default winter_dialogue_index = 0
default persistent.winter_endings = []

image winter_visitor = Null()

# Conversation camera uses a foreground portrait. Full-body source art and
# small exploration actors remain separate; the dialogue window masks the legs.
transform winter_portrait_close:
    xpos 640
    xanchor 0.5
    ypos 65
    size (660,880)
    fit "contain"

transform winter_portrait_question:
    xpos 640
    xanchor 0.5
    ypos 65
    size (600,800)
    fit "contain"


define winter_guard = Character("경비 돌목",cb_who_id="guard")
define winter_mom = Character("엄마",cb_who_id=None)
define winter_mayor = Character("촌장",cb_who_id=None)

init 45 python:
    WINTER_NAMES=dict(NAMES, mom="엄마", guard="돌목", mayor="촌장")
    for key,spec in VILLAGE_PEOPLE["profiles"].items():WINTER_NAMES[key]=spec["name"]
    WINTER_CHARS=dict(SOURCE_CHARS,mom=winter_mom,guard=winter_guard,mayor=winter_mayor)
    for key in VILLAGE_PEOPLE["profiles"]:
        WINTER_CHARS[key]=Character(WINTER_NAMES[key],cb_who_id=key)
    WINTER_MUSIC={"calm":"assets/travel.mp3","search":"assets/search.mp3","night":"assets/night.mp3","hearing":"assets/source-serious-context-v4.mp3","quiet":None}

    def winter_background(key):
        if key=="winter":return Transform("assets/winter-gate-clean.png",size=(1280,720))
        if key=="winter_carriage":return Transform("assets/winter-carriage.png",size=(1280,720))
        if key.startswith("winter_"):
            index=("square","post","workshop","passage").index(key[7:])
            return Transform(Crop(((index%2)*768,(index//2)*512,768,512),"assets/winter-places.webp"),size=(1280,720))
        return "bg "+key

    def winter_prepare(bg,title,mood):
        store.winter_presentation=dict(bg=bg,title=title,mood=mood)
        store.place=title
        store.clock_text=winter_clock(store.winter)
        store.dialogue_speaker=None
        store.dialogue_expression="neutral"
        store.winter_actor=None
        store.winter_line=None
        source_pulse(False)
        renpy.music.stop(channel="scene_fx")
        renpy.music.stop(channel="typing")

    def winter_speaker(who):
        store.winter_actor=who if who in CAST and who not in ("dad","daram") else None
        store.dialogue_expression="neutral"
        if store.winter_presentation and store.winter_presentation["bg"]=="winter_carriage":
            renpy.hide("winter_visitor")
            return
        if store.winter_actor:
            renpy.show(who+" interview_neutral",tag="winter_visitor",at_list=[winter_portrait_close])
        elif who in ("mom","mayor"):renpy.hide("winter_visitor")

    def winter_observe():
        return dict(state=winter_copy.deepcopy(store.winter),line=store.winter_line,
            actor=store.winter_actor,presentation=store.winter_presentation,
            entry=bool(renpy.get_screen("winter_entry_hub")),calendar=bool(renpy.get_screen("winter_calendar")),topic_tab=store.winter_topic_tab,
            hub=bool(renpy.get_screen("winter_hub")),map=bool(renpy.get_screen("winter_map")),
            board=bool(renpy.get_screen("winter_board")),choice=bool(renpy.get_screen("choice")),
            confirm=bool(renpy.get_screen("winter_confirm")),evidence=bool(renpy.get_screen("winter_evidence")),
            ending=bool(renpy.get_screen("winter_end")),claim_index=store.winter_claim_index,
            hearing=store.winter_hearing_id,pressure=store.winter_pressure,
            evidence_page=(renpy.get_screen("winter_evidence").scope.get("page_index") if renpy.get_screen("winter_evidence") else None),
            evidence_selected=(renpy.get_screen("winter_evidence").scope.get("selection",[]) if renpy.get_screen("winter_evidence") else []),
            options=winter_options(store.winter) if store.winter else [],
            whereabouts={who:winter_where(store.winter,who) for who in WINTER_SCHEDULES} if store.winter else {},
            topics=bool(renpy.get_screen("winter_topics")),target_kind=store.winter_target_kind,target_id=store.winter_target_id,
            topic_options=winter_display_topics(store.winter,store.winter_target_kind,store.winter_target_id,store.winter_topic_tab) if renpy.get_screen("winter_topics") else [],
            people=winter_people(store.winter) if store.winter else [],
            goal=winter_goal(store.winter) if store.winter else None,
            saving=bool(renpy.get_screen("save")),loading=bool(renpy.get_screen("load")),menu=bool(renpy.get_screen("pause_menu")),
            saved_slots=[s[0] for s in renpy.list_saved_games()],
            music=renpy.music.get_playing(),pulse=renpy.music.get_playing(channel="pulse"),
            portrait=store.dialogue_speaker,typing=renpy.music.get_playing(channel="typing"))

label winter_scene(bg,title,mood="search"):
    window hide
    hide winter_visitor
    hide visitor
    $ winter_prepare(bg,title,mood)
    scene black with Dissolve(.18)
    $ winter_music = WINTER_MUSIC[mood]
    if winter_music:
        if renpy.music.get_playing()!=winter_music:
            $ renpy.music.play(winter_music,fadeout=.2,fadein=.3)
    else:
        stop music fadeout .2
    $ renpy.pause(.3,hard=True)
    scene expression winter_background(bg) with Dissolve(.25)
    return

label winter_lines(entries,identity="dialogue"):
    $ winter_dialogue_index=0
    while winter_dialogue_index<len(entries):
        $ winter_packet=entries[winter_dialogue_index]
        $ winter_line=identity+":"+str(winter_dialogue_index)
        $ winter_speaker(winter_packet[0])
        $ winter_say=WINTER_CHARS.get(winter_packet[0],source_thought)
        $ winter_say(winter_packet[1])
        $ winter_dialogue_index+=1
    $ winter_line=None
    hide winter_visitor
    return

label start:
    jump room13_start

label winter_start:
    $ room13_mode=False
    hide screen r13_hud
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ typing_allowed=True
    hide screen hud
    hide screen source_world
    hide screen source_proof
    show screen winter_hud
    jump winter_arrival

label winter_day:
    if winter["day"]==14:
        jump winter_final
    if str(winter["day"]) in WINTER["events"]:
        call winter_scene("front","여관 · 아침","calm")
        call winter_lines(winter_morning(winter),"morning"+str(winter["day"]))
    if winter["day"]==6 and winter["witness"]=="detained":
        call winter_lines([("granny","누비가 오늘 오지 않았어요. 집에는 구금 통지가 붙었대요."),("dad","이송 전에 찾을 시간이 남았겠군요.")],"missing")
    if winter["day"]==8 and winter["witness"]=="dead":
        call winter_lines([("granny","누비 집의 통지가 없어졌어요. 누가 데려갔는지도 말을 안 해요."),("dad","명단과 가동 기록을 확인하겠습니다.")],"absence")
    jump winter_roam

label winter_roam:
    $ winter_location=WINTER["places"][winter["location"]]
    call winter_scene(winter_location["bg"],winter_location["name"],"calm" if winter["location"]=="inn" else "search")
    if winter["location"]=="inn" and winter_has(winter,"plaza_plan_shared") and not winter_has(winter,"plaza_plan_echo_seen"):
        call winter_information_echo
label winter_field:
    window hide
    hide winter_visitor
    call screen winter_hub
    $ winter_choice=_return
    if isinstance(winter_choice,tuple):
        $ winter_target_kind,winter_target_id=winter_choice
        if winter_target_kind=="person":
            jump winter_talk
        if winter_target_kind=="object":
            jump winter_object
        if winter_target_kind=="empty":
            $ winter=winter_inspection_mark(winter,"empty:%d:%d"%(winter_target_id[0]//80,winter_target_id[1]//80),winter_target_id)
            call winter_lines([(None,"발밑과 벽을 살폈다. 이 자리에는 따로 눈에 띄는 흔적이 없다.")],"empty")
            jump winter_field
    if winter_choice=="map":
        call screen winter_map
        $ winter=winter_move(winter,_return)
        jump winter_roam
    if winter_choice=="look":
        call winter_lines([(None,winter_local_look(winter))],"look")
        jump winter_field
    if winter_choice=="wait":
        if winter_period(winter)<3:
            call screen winter_confirm("%s → %s\n다음 시간대까지 기다릴까요?"%(winter_period_name(winter),winter_time_target(winter)))
            if _return:
                $ winter=winter_wait(winter)
        jump winter_field
    if winter_choice=="rest":
        if not winter_has(winter,"inn_registered"):
            call winter_lines([("dad","먼저 접수대에 방을 부탁하자. 짐도 맡겨야지.")],"need_room")
            jump winter_field
        call screen winter_confirm("%s입니다. 오늘 남은 일정을 마치고 여관에서 밤을 보낼까요?"%winter_period_name(winter))
        if _return:
            jump winter_night
        jump winter_field
    jump winter_field

label winter_action_run:
    $ winter_action=WINTER["actions"][winter_action_id]
    if not winter_can_act(winter,winter_action_id):
        return
    if winter_action_id in ("lamp_confidence","mother_send_reply") and not winter_private_conversation(winter,"resident_lamplighter"):
        call winter_lines([("resident_lamplighter","지금은 듣는 사람이 있어. 아까 그 말은 넣어 둬.")],"private_topic_deferred")
        return
    if winter_action_id=="buri_mother":
        call winter_buri_approach
        if not _return:
            return
    if winter_action["cost"]:
        call screen winter_confirm(winter_action["time_reason"]+"\n마치고 돌아오면 "+winter_time_target(winter).replace(" 일정 마침", "이 깊어집니다")+".")
        if not _return:
            return
    if winter_action_id=="hidden":
        menu:
            "두 목격이 모두 사실이라면?"
            "지하 연결로가 있는지 도면과 흔적을 비교한다":
                pass
            "둘 중 하나가 거짓말했을 것이다":
                call winter_lines([("dad","가능하지만 아직 누구의 말이 틀렸는지는 몰라. 두 기록이 함께 성립할 길도 확인하자.")],"hypothesis")
                return
    if winter_action["cost"]:
        call winter_lines(winter_action.get("arrival",[]),"depart:"+winter_action_id)
        window hide
        hide winter_visitor
        scene black with Dissolve(.3)
        $ renpy.pause(.45,hard=True)
        scene expression winter_background(WINTER["places"][winter["location"]]["bg"]) with Dissolve(.3)
    $ winter_evidence_before=list(winter["evidence"])
    call winter_lines(winter_action_lines(winter,winter_action_id),winter_action_id)
    if winter_action_id in ("room_reason","ration_compare","ration_share","mother_reply_reason","plaza_plans"):
        call winter_exploration_decision
        if not _return:
            return
    $ winter=winter_apply(winter,winter_action_id)
    $ clock_text=winter_clock(winter)
    if winter_action["cost"]:
        call winter_lines([(None,winter_action["aftermath"])],"return:"+winter_action_id)
    if winter_action_id=="mother":
        if winter_has(winter,"mother_secure"):
            call winter_lines([("mom","오는 길에 누가 따라오지는 않았어?"),("dad","교대를 확인하고 다른 길로 왔어. 오늘은 여기서 이야기하자.")],"mother_safe")
        else:
            call winter_lines([(None,"통로 바깥에서 발소리가 멈췄다."),("mom","문 닫아. 여기까지 따라왔어."),("dad","순찰 시간을 알아내서 은신처를 옮겨야 해.")],"mother_traced")
    if winter_action_id=="witness":
        menu:
            "누비의 말을 누구에게 전할까?"
            "이름은 감추고 가족을 지킬 방법을 찾는다":
                $ winter=winter_flag(winter,"kept_private")
            "체류 담당자에게 누비의 이름과 목격을 알린다":
                $ winter=winter_note_presentation(winter,"seryeon",["witness"],True)
                $ winter=winter_prepare_response(winter,"seryeon",["witness"],True)
                $ winter=winter_flag(winter,"witness_exposed")
                call winter_lines([("seryeon","직접 확인해 보겠습니다. 어느 집이라고요?"),("dad","확인하되, 그분이 불이익을 받으면 안 됩니다."),("seryeon","그 점도 전달하지요.")],"disclosure")
                $ winter=dict(winter,witness="detained")
    if winter_action_id=="death" and winter["witness"]=="dead":
        call winter_lines([("dad","누비의 번호도 있어. 추출은 이미 끝났어."),("daram","……집으로 돌아간 게 아니었네.")],"witness_death")
    if winter_action["give"]:
        $ winter_new_evidence=[key for key in winter["evidence"] if key not in winter_evidence_before]
        while winter_new_evidence:
            $ winter_found_key=winter_new_evidence.pop(0)
            call winter_found_card(winter_found_key)
    return

label winter_night:
    if winter_has(winter,"family_reported") and not winter_has(winter,"report_night_resolved"):
        $ winter=winter_flag(winter,"report_night_resolved")
        if not winter_shelter_supported(winter):
            jump winter_early_loss
        call winter_lines([("granny","경비가 너희 이름을 받아 갔어요. 오늘은 문 안에 있어요."),("nabi","소리 지른 일은 잘했다 못 하겠어. 그래도 아이를 따로 데려가게 둘 순 없지."),(None,"여관에 남은 주민들이 문 앞에 의자를 놓았다. 신고가 사라진 것은 아니지만, 경비는 혼자 둘을 데려가지 못했다.")],"report_shelter")
    if winter["day"] in (3,6):
        call winter_hearing("granny" if winter["day"]==3 else "witness")
    call winter_scene("front","여관 · 잠긴 현관","night")
    if winter["day"]==1:
        call winter_lines([("granny","밤에 누가 불러도 내가 나갈 거예요. 두 분은 방에 있어요."),("dad","경비가 와도요?"),("granny","누가 와도요.")],"night_warning")
        $ renpy.music.stop(fadeout=.2)
        play sound "assets/source-tap.wav" volume .28
        call winter_lines([(None,"문 아래에서 세 번, 긁는 소리가 났다."),(None,"……추워."),("daram","아빠, 누가 왔어."),("dad","여기 같이 있자."),("granny","알아요. 거기 있어요."),(None,"작은 배식구가 열렸다. 그릇이 바닥에 닿는 소리 뒤로 발소리가 멀어졌다.")],"night_visitor")
        call winter_lines([("neoul","할머니. 장부와 열쇠를 확인하겠습니다."),("granny","손님들은 방에 있어요. 이름을 읽지는 말아요."),("daram","여기서도 이름을 확인해?")],"night_search")
    elif winter["day"]==2:
        call winter_lines([("daram","내일 할머니 데려가면 우리도 나가야 해?"),("dad","그렇게 못 하게 기록을 가져갈 거야."),("daram","나도 이불 본 거 말할게." if winter_has(winter,"bed") else "내일 나도 같이 알아볼래.")],"night2")
    elif winter["day"]==4:
        call winter_lines([("daram","아침에 도토 씨가 그랬잖아. 자기 이름이 생각 안 났다고."),("dad","밤에 그랬다고 했지."),("daram","오늘 밤에도 그러면 어떡해?")],"night4")
    elif winter["day"]==7:
        call winter_lines([(None,"난방관이 울리고 복도 불이 두 번 꺼졌다."),("daram","아빠, 문 잠갔지?"),("dad","응. 여기 있어.")],"night7")
    else:
        call winter_lines([("daram","오늘 적은 거, 내가 읽어 줄까?"),("dad","그래. 빠진 게 있는지 같이 보자.")],"night_review")
    $ winter=winter_next_day(winter)
    jump winter_day

label winter_hearing(hearing):
    $ winter_hearing_id=hearing
    $ winter_claim_index=0
    $ winter_pressure=0
    $ winter_hearing_wins=[]
    call winter_scene("council",WINTER["claims"][hearing]["title"],"hearing")
    call winter_lines(winter_hearing_opening(winter,hearing),"hearing_open")
    call winter_lines(winter_support_lines(winter),"hearing_support")
    while winter_claim_index<len(WINTER["claims"][hearing]["claims"]) and winter_pressure<winter_hearing_limit(winter):
        $ winter_claim=winter_prepared_claim(winter,hearing,winter_claim_index)
        $ winter_speaker(winter_claim["who"])
        $ renpy.show(winter_claim["who"]+" interview_neutral",tag="winter_visitor",at_list=[winter_portrait_question])
        call screen winter_board(winter_claim)
        $ winter_choice=_return
        if winter_choice=="press":
            call winter_lines([(winter_claim["who"],winter_claim["press"])],"press")
        elif winter_choice=="present":
            $ winter_selected=[]
            call screen winter_evidence(True)
            if _return:
                if winter_proves(winter,winter_claim,winter_selected):
                    $ winter=winter_mark(winter,winter_claim["id"])
                    $ winter_hearing_wins=winter_hearing_wins+[winter_claim["id"]]
                    call winter_lines([("neoul",winter_claim["win"])],"proved")
                    $ winter_claim_index+=1
                else:
                    $ winter_pressure+=1
                    call winter_lines([("neoul",winter_reason_feedback(winter,winter_claim,winter_selected))],"not_proved")
        else:
            $ winter_pressure+=1
            $ winter_claim_index+=1
    if hearing=="granny":
        $ winter=dict(winter,first_result=("protected" if "theft" in winter_hearing_wins else "restricted"))
        if winter["first_result"]=="protected":
            call winter_lines([("granny","내 방에서 자는 사람을 지키려던 건데, 내가 도움을 받았네."),("daram","내일도 여기서 밥 먹어도 되죠?")],"granny_won")
        else:
            call winter_lines([("neoul","즉시 이송은 보류합니다. 다만 여관 장부를 매일 확인하겠습니다."),("granny","방은 안 뺏겨요. 겁먹지 말아요.")],"granny_lost")
    if hearing=="witness":
        $ winter=dict(winter,second_result=("preserved" if "transfer" in winter_hearing_wins else "contested"))
        if winter["second_result"]=="preserved":
            call winter_lines([("neoul","원본 번호와 오늘 발언을 남겼습니다. 외부 이송이라고 공고한 사람의 내부 인계도 따로 확인하겠습니다.")],"second_result")
        else:
            call winter_lines([("neoul","운반 설명을 뒤집을 자료가 부족합니다. 이의는 남기지만 지시서 회수는 보류하지 못했습니다."),("dad","그럼 원본이 어디로 가는지부터 확인하겠습니다.")],"second_contested")
    hide winter_visitor
    $ winter_hearing_id=None
    return

label winter_final:
    call winter_scene("front","여관 · 식어 버린 난방관","search")
    call winter_lines([(None,"새벽에 멎은 난방관은 아침이 되어도 울리지 않았다."),("granny","장작불까지 꺼진 건 아니에요. 다들 난로 가까이 앉아요."),("nabi","광장에도 사람들이 모였어. 촌장이 오늘 해 지기 전에 돌을 깨워야 한대."),("daram","그래서 사람을 데려가겠대요?"),("nabi","응. 돌에 돌려보내야 한다고. 명부를 들고 집마다 돌고 있어."),("dad","문을 잠가 주세요. 누구를 어디로 데려가는지, 사람들 앞에서 묻겠습니다."),(None,"낮 동안 주민들이 광장 회관으로 모였다. 경비들은 출입문 옆에서 명부를 펼쳤다.")],"stone_crisis")
    $ winter=dict(winter,period=2)
    call winter_hearing("final")
    $ winter=dict(winter,ending=winter_ending(winter))
    if all(k in winter["marks"] for k in ("frame","destination","power","death")):
        call winter_lines([("seryeon","그럼 저 시설을 멈추고, 오늘 밤은 어떻게 버팁니까?"),("granny","사람을 죽였다는 말에 대답부터 해야죠."),("seryeon","우리 아이들도 여기 있어요. 돌이 멎으면 그 아이들은 누가 지킵니까?")],"last_counter")
        if winter_has(winter,"repair") and winter_has(winter,"fuel") and winter.get("records",{}).get("repair",{}).get("day",99)<=11:
            call winter_lines([("buri","여관에 장작을 옮겨 뒀어. 집마다 난방을 돌리는 건 멈추고, 한곳에 모이면 돼."),("mom","말을 유지하는 회로는 따로 살릴 수 있어요. 밤마다 측정한 값도 여기 있습니다."),("dad","사람을 넘겨주지 않고 버틸 준비를 했습니다. 지금 문부터 막아 주세요.")],"prepared_answer")
        else:
            call winter_lines([("dad","오늘 밤 버틸 방법은 아직 다 마련하지 못했습니다. 그래도 저 사람들을 데려가게 둘 수는 없습니다."),("granny","내 난로라도 함께 쓸 거예요. 사람부터 놓아요.")],"unprepared_answer")
    call winter_scene("front","여관 · 그날 밤","quiet")
    if winter["ending"]=="truth":
        call winter_lines([("neoul","호송하지 않겠습니다. 목적지도 혐의도 거짓이었습니다."),("resident_nubi","제가 본 것도 같아요. 가족은 안전한 곳에 있습니다. 이제 이름을 적어도 됩니다."),("buri","난방 회로는 줄일 수 있어. 대신 여관에 모여야 해."),("mom","언어 유지 회로부터 안정시킬게요. 완전한 수리는 아니에요. 시간을 버는 거예요."),("daram","아빠. 오늘은 다 같이 밥 먹는 거야?"),("dad","응. 자리를 더 만들자."),("mom","이 개조 표시, 다른 지역의 정비 기록에서도 봤어. 누가 같은 방법을 전한 걸까.")],"ending_truth")
    elif winter["ending"]=="family":
        call winter_lines([("karo","눈보라가 잦아들었어요. 낮에 걸어 확인한 낮은 길로 갑시다. 다시 쌓이기 전에."),("mom","자료는 챙겼어. 돌아와서 밝힐 방법을 찾자."),("daram","엄마 손은 내가 잡을게. 아빠는 내 손 잡아."),(None,"세 사람은 낮은 고개를 넘었다. 마을의 불빛은 아직 꺼지지 않았다.")],"ending_family")
    elif winter["ending"]=="exposure":
        call winter_lines([("neoul","이송을 중지합니다. 목적지가 확인될 때까지 문을 열지 않겠습니다."),("granny","오늘은 막았어요. 내일도 막으려면 더 알아야겠지요."),("daram","아빠. 아직 못 찾은 게 있지."),("dad","응. 여기서 멈추지는 않을 거야.")],"ending_exposure")
    elif winter["ending"]=="flight":
        call winter_lines([("karo","바람이 멎었어요. 확인해 둔 낮은 길은 걸을 수 있어요. 둘이라도 지금 나가야 해요."),("daram","엄마는?"),("dad","밖에서 도움을 구하자. 편지 원본과 기록은 갖고 있어."),(None,"마차가 가지 못하는 길로 두 사람은 떠났다. 세 번째 자리는 비어 있었다.")],"ending_flight")
    else:
        call winter_lines([("neoul","시설에서 확인하겠답니다. 아이는 다른 경비에게……"),("dad","아이는 내 옆에 두십시오."),("daram","아빠 손 안 놓을 거야."),(None,"누군가 다람의 팔을 붙잡았다. 둘 사이로 문이 닫혔다.")],"ending_separated")
    $ persistent.winter_endings=list(set(persistent.winter_endings+[winter["ending"]]))
    $ renpy.save_persistent()
    call screen winter_end
    return
