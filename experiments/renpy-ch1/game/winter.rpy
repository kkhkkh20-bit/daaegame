# Ten-day playable scenario, separate from the archived thirteen-bed case.
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

define winter_guard = Character("경비",cb_who_id=None)
define winter_mom = Character("엄마",cb_who_id=None)
define winter_mayor = Character("촌장",cb_who_id=None)

init 45 python:
    WINTER_NAMES=dict(NAMES, mom="엄마", guard="경비", mayor="촌장")
    for key,spec in VILLAGE_PEOPLE["profiles"].items():WINTER_NAMES[key]=spec["name"]
    WINTER_CHARS=dict(SOURCE_CHARS,mom=winter_mom,guard=winter_guard,mayor=winter_mayor)
    for key in VILLAGE_PEOPLE["profiles"]:
        WINTER_CHARS[key]=Character(WINTER_NAMES[key],cb_who_id=key)
    WINTER_MUSIC={"calm":"assets/travel.mp3","search":"assets/search.mp3","night":"assets/night.mp3","hearing":"assets/source-serious-context-v4.mp3","quiet":None}

    def winter_background(key):
        if key=="winter":return Transform("assets/winter-gate.webp",size=(1280,720))
        return "bg "+key

    def winter_prepare(bg,title,mood):
        store.winter_presentation=dict(bg=bg,title=title,mood=mood)
        store.place=title
        store.clock_text="%d일째 · 이송 심의까지 %d일"%(store.winter["day"],10-store.winter["day"])
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
        if store.winter_actor:
            renpy.show(who+" interview_neutral",tag="winter_visitor",at_list=[portrait_close])
        elif who in ("mom","guard","mayor",None):renpy.hide("winter_visitor")

    def winter_observe():
        return dict(state=winter_copy.deepcopy(store.winter),line=store.winter_line,
            actor=store.winter_actor,presentation=store.winter_presentation,
            hub=bool(renpy.get_screen("winter_hub")),map=bool(renpy.get_screen("winter_map")),
            board=bool(renpy.get_screen("winter_board")),choice=bool(renpy.get_screen("choice")),
            confirm=bool(renpy.get_screen("winter_confirm")),evidence=bool(renpy.get_screen("winter_evidence")),
            ending=bool(renpy.get_screen("winter_end")),claim_index=store.winter_claim_index,
            hearing=store.winter_hearing_id,pressure=store.winter_pressure,
            evidence_page=(renpy.get_screen("winter_evidence").scope.get("page_index") if renpy.get_screen("winter_evidence") else None),
            evidence_selected=(renpy.get_screen("winter_evidence").scope.get("selection",[]) if renpy.get_screen("winter_evidence") else []),
            options=winter_options(store.winter) if store.winter else [],
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
    jump winter_start

label winter_start:
    $ winter_mode=True
    $ winter=winter_new()
    $ source_mode=False
    $ typing_allowed=True
    hide screen hud
    hide screen source_world
    hide screen source_proof
    show screen winter_hud
    call winter_scene("winter","눈에 막힌 마을 입구","quiet")
    call winter_lines([("daram","아빠, 조금만 내려와."),("dad","팔 저린데."),("daram","조금만 더."),(None,"마차가 멎었다. 창문 밖에서 손바닥이 나무를 두드렸다."),("karo","여관 손님 둘이에요. 문 좀 열어줘요."),("guard","체류 서류부터."),("dad","이 편지를 받고 왔습니다."),("guard","아이 이름은?"),("dad","다람입니다."),("guard","명단에는 한 명인데."),("daram","우리 내려?"),("guard","아이는 저쪽에서 확인합니다."),("dad","같이 가겠습니다."),("guard","보호자는 여기 남으세요."),(None,"반대편 문이 열렸다. 경비가 다람의 가방을 들어 내렸다."),("daram","그거 내 건데."),("dad","가방 내려놓으세요.")],"gate")
    menu:
        "다람을 내 뒤로 데려온다":
            $ winter=winter_flag(winter,"protected_daram")
            call winter_lines([("dad","아이에게서 떨어지세요."),("karo","짐은 내가 내릴게요. 애가 놀랐잖아요.")],"gate_protect")
        "책임자를 불러 달라고 한다":
            $ winter=winter_flag(winter,"asked_rule")
            call winter_lines([("dad","분리하라는 규정과 책임자를 확인하겠습니다."),("guard","미등록 체류자 확인입니다. 안쪽에 연락하겠습니다.")],"gate_rule")
        "까로에게 함께 왔다고 말해 달라고 한다":
            $ winter=winter_flag(winter,"karo_guarantee")
            call winter_lines([("dad","까로 씨. 같이 왔다고 확인해 주시겠습니까?"),("karo","내 운송 기록에 두 명입니다. 여기요.")],"gate_karo")
    call winter_lines([("guard","둘 다 여관으로 보내랍니다."),("dad","누가 확인했습니까?"),("guard","체류 담당자가 기다립니다."),("daram","아빠. 나 이름 말하면 안 됐어?"),("dad","아니. 넌 잘못한 거 없어.")],"gate_release")
    call winter_scene("front","여관 · 접수대","calm")
    play sound "assets/door.wav" volume .35
    call winter_lines([("granny","불 가까이 앉아요. 바닥 젖는 건 괜찮으니까."),("dad","감사합니다."),("daram","나도 방 고를래."),("dad","여기서 몸 녹이고 있어도 돼."),("daram","같이 볼래."),("dad","이 사람을 찾습니다."),("granny","……그 방을 쓰던 분이네요."),("daram","지금도 있어요?"),("granny","지금은 없어요."),("daram","그 방, 우리가 써도 돼요?")],"inn")
    call winter_lines([("seryeon","명부가 잘못 전달됐습니다. 아이까지 놀라게 했네요."),("dad","다시 그런 일은 없습니까?"),("seryeon","제가 두 분 체류를 맡겠습니다. 찾으시는 분의 소식도 알아보죠."),("granny","방 보증은 내가 해요. 명부는 여기 두고 가요."),("seryeon","물론입니다. 열흘 뒤 체류 심의 전까지는요."),("karo","고갯길은 막혔어요. 차가 나갈 수 있게 되면 먼저 알려 드릴게요."),("daram","그때 엄마 자리도 남겨 주세요.")],"sponsor")
    jump winter_day

label winter_day:
    if winter["day"]==10:
        jump winter_final
    if str(winter["day"]) in WINTER["events"]:
        call winter_scene("front","여관 · 아침","calm")
        call winter_lines(WINTER["events"][str(winter["day"])],"morning"+str(winter["day"]))
    if winter["day"]==6 and winter["witness"]=="detained":
        call winter_lines([("granny","누비가 오늘 오지 않았어요. 집에는 구금 통지가 붙었대요."),("dad","이송 전에 찾을 시간이 남았겠군요.")],"missing")
    if winter["day"]==8 and winter["witness"]=="dead":
        call winter_lines([("granny","누비 집의 통지가 없어졌어요. 누가 데려갔는지도 말을 안 해요."),("dad","명단과 가동 기록을 확인하겠습니다.")],"absence")
    jump winter_roam

label winter_roam:
    $ winter_location=WINTER["places"][winter["location"]]
    call winter_scene(winter_location["bg"],winter_location["name"],"calm" if winter["location"]=="inn" else "search")
    call screen winter_hub
    $ winter_choice=_return
    if winter_choice=="map":
        call screen winter_map
        $ winter=winter_move(winter,_return)
        jump winter_roam
    if winter_choice=="look":
        call winter_lines([(None,winter_location["look"])],"look")
        jump winter_roam
    if winter_choice=="rest":
        call screen winter_confirm("남은 행동 %d회를 마치고 오늘 밤을 보낼까요?"%winter["ap"])
        if _return:
            jump winter_night
        jump winter_roam
    $ winter_action_id=winter_choice
    $ winter_action=WINTER["actions"][winter_action_id]
    call screen winter_confirm(winter_action["name"]+" · 행동 1회")
    if not _return:
        jump winter_roam
    if winter_action_id=="hidden":
        menu:
            "두 목격이 모두 사실이라면?"
            "지하 연결로가 있는지 도면과 흔적을 비교한다":
                pass
            "둘 중 하나가 거짓말했을 것이다":
                call winter_lines([("dad","가능하지만 아직 누구의 말이 틀렸는지는 몰라. 두 기록이 함께 성립할 길도 확인하자.")],"hypothesis")
                jump winter_roam
    call winter_lines(winter_action["lines"],winter_action_id)
    $ winter=winter_apply(winter,winter_action_id)
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
                $ winter=winter_flag(winter,"witness_exposed")
                call winter_lines([("seryeon","직접 확인해 보겠습니다. 어느 집이라고요?"),("dad","확인하되, 그분이 불이익을 받으면 안 됩니다."),("seryeon","그 점도 전달하지요.")],"disclosure")
                $ winter=dict(winter,witness="detained")
    if winter_action_id=="death" and winter["witness"]=="dead":
        call winter_lines([("dad","누비의 번호도 있어. 추출은 이미 끝났어."),("daram","……집으로 돌아간 게 아니었네.")],"witness_death")
    if winter_action["give"]:
        $ renpy.notify("수첩에 기록했습니다. 다시 읽기는 행동을 쓰지 않습니다.")
    jump winter_roam

label winter_night:
    if winter["day"] in (3,6):
        call winter_hearing("granny" if winter["day"]==3 else "witness")
    call winter_scene("front","여관 · 잠긴 현관","night")
    if winter["day"]==1:
        call winter_lines([("granny","밤에 누가 불러도 내가 나갈 거예요. 두 분은 방에 있어요."),("dad","경비가 와도요?"),("granny","누가 와도요.")],"night_warning")
        $ renpy.music.stop(fadeout=.2)
        play sound "assets/source-tap.wav" volume .28
        call winter_lines([(None,"문 아래에서 세 번, 긁는 소리가 났다."),(None,"……추워."),("daram","아빠, 누가 왔어."),("dad","여기 같이 있자."),("granny","알아요. 거기 있어요."),(None,"작은 배식구가 열렸다. 그릇이 바닥에 닿는 소리 뒤로 발소리가 멀어졌다.")],"night_visitor")
        call winter_lines([("neoul","할머니. 장부와 열쇠를 확인하겠습니다."),("granny","손님들은 방에 있어요. 이름을 읽지는 말아요."),("daram","아빠. 아까 그 사람들이야.")],"night_search")
    elif winter["day"]==2:
        call winter_lines([("daram","내일 할머니 데려가면 우리도 나가야 해?"),("dad","그렇게 못 하게 기록을 가져갈 거야."),("daram","나도 이불 본 거 말할게.")],"night2")
    elif winter["day"]==4:
        call winter_lines([("daram","오늘 광장에서 그 아저씨가 자기 이름을 못 말했어."),("dad","밤이 되면 더 심해진다고 했지."),("daram","밖에 나가서 그렇게 된 게 아닐 수도 있겠다.")],"night4")
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
    call winter_lines([("neoul","확인한 자료를 두 개씩 함께 제시해 주세요. 어떤 말을 반박하는지도 남기겠습니다.")],"hearing_open")
    while winter_claim_index<len(WINTER["claims"][hearing]["claims"]) and winter_pressure<3:
        $ winter_claim=WINTER["claims"][hearing]["claims"][winter_claim_index]
        $ winter_speaker(winter_claim["who"])
        $ renpy.show(winter_claim["who"]+" interview_neutral",tag="winter_visitor",at_list=[portrait_question])
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
                    call winter_lines([("neoul","관련은 있을 수 있지만, 이 두 자료로 지금의 주장을 뒤집지는 못합니다. 다른 설명이 남아 있습니다.")],"not_proved")
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
        call winter_lines([("neoul","접수 결과는 최종 심의에도 남깁니다. 이송은 열흘째입니다.")],"second_result")
    hide winter_visitor
    $ winter_hearing_id=None
    return

label winter_final:
    call winter_hearing("final")
    $ winter=dict(winter,ending=winter_ending(winter))
    call winter_scene("front","열흘째 밤","quiet")
    if winter["ending"]=="truth":
        call winter_lines([("neoul","호송하지 않겠습니다. 목적지도 혐의도 거짓이었습니다."),("resident_nubi","제가 본 것도 같아요. 가족은 안전한 곳에 있습니다. 이제 이름을 적어도 됩니다."),("buri","난방 회로는 줄일 수 있어. 대신 여관에 모여야 해."),("mom","언어 유지 회로부터 안정시킬게요. 완전한 수리는 아니에요. 시간을 버는 거예요."),("daram","아빠. 오늘은 다 같이 밥 먹는 거야?"),("dad","응. 자리를 더 만들자."),("mom","이 개조 표시, 다른 지역의 정비 기록에서도 봤어. 누가 같은 방법을 전한 걸까.")],"ending_truth")
    elif winter["ending"]=="family":
        call winter_lines([("karo","지금 나가야 해요. 눈이 다시 쌓이기 전에."),("mom","자료는 챙겼어. 돌아와서 밝힐 방법을 찾자."),("daram","엄마 손은 내가 잡을게. 아빠는 내 손 잡아."),(None,"세 사람은 낮은 고개를 넘었다. 마을의 불빛은 아직 꺼지지 않았다.")],"ending_family")
    elif winter["ending"]=="exposure":
        call winter_lines([("neoul","이송을 중지합니다. 목적지가 확인될 때까지 문을 열지 않겠습니다."),("granny","오늘은 막았어요. 내일도 막으려면 더 알아야겠지요."),("daram","아빠. 아직 못 찾은 게 있지."),("dad","응. 여기서 멈추지는 않을 거야.")],"ending_exposure")
    elif winter["ending"]=="flight":
        call winter_lines([("karo","둘이라도 지금 나가야 해요."),("daram","엄마는?"),("dad","밖에서 도움을 구하자. 편지 원본과 기록은 갖고 있어."),(None,"마차가 가지 못하는 길로 두 사람은 떠났다. 세 번째 자리는 비어 있었다.")],"ending_flight")
    else:
        call winter_lines([("neoul","심의 결과, 분리 확인을 집행합니다."),("dad","아이는 내 옆에 두십시오."),("daram","아빠 손 안 놓을 거야."),(None,"닫히는 문 너머로 열쇠가 돌아갔다.")],"ending_separated")
    $ persistent.winter_endings=list(set(persistent.winter_endings+[winter["ending"]]))
    $ renpy.save_persistent()
    call screen winter_end
    return
