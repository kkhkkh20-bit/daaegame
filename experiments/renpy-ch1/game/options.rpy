define config.name = "다람탐정 · 눈에 갇힌 마을"
define config.version = "0.18.29"
# Literal early definition selects the persistent web save mount.
define config.save_directory = "daaegame-renpy-village-ch1-06"

default inventory = []
default inspected = []
default visited = []
default stage = "arrival"
default current_location = "front"
default place = "마차 안"
default clock_text = "해 질 무렵"
default target = None
default typing_allowed = True
default dialogue_speaker = None
default dialogue_expression = "neutral"
default lamp_ready = False
default somsom_found = False
default archive_permission = False
default archive_open = False
default digit_code = [0, 0, 0, 0]
default code_error = False
default speaker = "seryeon"
default meeting_first = None
default comparison_topic = None
default resolved_topics = []
default clock_rotated = False
default clock_demonstrated = False
default showdown_issue = "place"
default wrong_attempts = 0
default conclusion_attempts = 0
default case_resolved = False
default mother_clue = False
default test_complete = False

init python:
    import json
    class TopicTick(renpy.Displayable):
        def render(self,width,height,st,at):
            rendered=renpy.Render(26,26)
            rendered.canvas().lines("#b7d6b4",False,[(3,13),(10,20),(23,4)],4)
            return rendered
    class VillagePaths(renpy.Displayable):
        def render(self,width,height,st,at):
            rendered=renpy.Render(1280,720)
            canvas=rendered.canvas()
            for start,end in (("gate","fountain"),("fountain","lane"),("fountain","post"),("post","inn"),("lane","inn")):
                x1,y1=ARRIVAL_PLACES[start][2]
                x2,y2=ARRIVAL_PLACES[end][2]
                points=[(x1,y1),(int((x1+x2)/2),int((y1+y2)/2)+18),(x2,y2)]
                canvas.lines("#d4bc8b",False,points,13)
                canvas.lines("#9b7d53",False,points,3)
            return rendered
    gui.init(1280,720)
    config.has_voice = True
    config.main_menu_music = "assets/bgm-title.mp3"
    config.main_menu_music_fadein = 1.2
    config.default_music_volume = 0.75
    config.default_sfx_volume = 0.7
    config.default_text_cps = 34
    config.window = "auto"
    config.window_show_transition = Dissolve(0.12)
    config.window_hide_transition = Dissolve(0.12)
    config.game_menu_action = ShowMenu("pause_menu")
    config.rollback_enabled = True
    config.nearest_neighbor = True
    config.gl2 = True
    config.enter_transition = Dissolve(0.12)
    config.exit_transition = Dissolve(0.12)
    config.after_load_transition = Fade(0.12,0.12,0.2)
    build.name = "daram_renpy_small_ch1"
    build.version = "0.18.29"
    build.classify("game/assets/room13-painted-*.png", None)
    build.classify("game/assets/room13-painted-layouts.json", None)
    build.classify("game/assets/*.txt", "all")
    build.classify("game/assets/*.json", "all")
    # Superseded single-scene drafts; the final inn atlas supplies these rooms.
    build.classify("game/assets/room13-hall.png", None)
    build.classify("game/assets/room13-passage.png", None)
    build.classify("**.py", None)
    build.classify("**/__pycache__/**", None)
    build.classify("**/*.pyc", None)
    build.classify("story-room13/**", None)
    build.classify("dev/**", None)
    build.classify("*_WORK_STATUS.json", None)
    build.classify("*_QA_REPORT.json", None)
    build.classify("QA_REPORT.json", None)
    build.classify("qa*/**", None)
    build.classify("review/**", None)
    build.classify("art/**", None)
    build.classify("audio/**", None)
    build.classify("**.log", None)
    build.classify("**/saves/**", None)
    build.classify("**/cache/**", None)
    build.classify("**.txt", None)
    renpy.music.register_channel("typing", mixer="sfx", loop=True, stop_on_mute=True)

    def text_audio(event, interact=True, who_id=None, **kwargs):
        if getattr(store,"room13_mode",False):
            if event == "begin":
                store.dialogue_speaker = who_id
            # Room13 uses actual revealed glyphs; never loop a sound by duration.
            renpy.music.stop(channel="typing")
            return
        if event == "begin":
            store.dialogue_speaker = who_id
        if event == "show_done" and interact and store.typing_allowed and persistent.room13_typing_sound and not renpy.is_skipping():
            renpy.music.play("assets/type.wav", channel="typing", loop=True)
        elif event in ("slow_done", "end"):
            renpy.music.stop(channel="typing")

    def r13_title_music():
        # Explicit gesture also unlocks audio in browsers that block autoplay.
        _preferences.set_mute("music", False)
        renpy.music.play(config.main_menu_music, if_changed=True, fadein=.4)

    def stop_menu_typing():
        if any(renpy.get_screen(s) for s in ("pause_menu", "save", "load", "evidence_book", "winter_evidence", "winter_confirm", "winter_hub", "winter_board", "winter_topics")):
            renpy.music.stop(channel="typing")
    config.interact_callbacks.append(stop_menu_typing)
    config.character_callback = text_audio

    CAST = json.load(renpy.file("assets/cast.json"))
    NAMES = {"dad":"아빠", "daram":"다람", "granny":"할머니", "seryeon":"세련", "nabi":"나비", "bami":"밤이", "doto":"도토", "buri":"부리", "karo":"까로", "neoul":"너울"}
    for person, states in CAST.items():
        for state_name, spec in states.items():
            renpy.image(person + " " + state_name, Transform(Crop(tuple(spec["crop"]), spec["file"]),nearest=spec.get("nearest",True)))

    LOCATIONS = {
        "front":("여관 접수대", "bg front", "granny",625,563),
        "kitchen":("부엌", "bg kitchen", "nabi",965,560),
        "plaza":("마을 입구", "bg approach", "karo",820,590),
        "hall":("2층 복도", "bg hall", "bami",825,110),
        "doto":("도토의 방", "bg doto", "doto",1030,560),
        "room":("열세 번째 침대", "bg room",None,0,0),
    }
    MAP_POINTS = {"plaza":(160,390), "front":(425,310), "kitchen":(660,430), "hall":(700,175), "doto":(950,210), "room":(960,410)}
    EVIDENCE = {
        "pouch":("주머니와 빈 계약서", "발견 당시 봉인 온전. 너울이 열어 센 돈은 백 냥. 여관 매도인 서명은 비어 있다.", "assets/pouch.png"),
        "flour":("이불의 하얀 손자국", "이불 끝에 남은 밀가루 손자국. 누군가 이불을 편 흔적이다.", "assets/flour-world.png"),
        "kitchen":("나비가 편 이불", "나비는 밤 11시 반죽을 하다 할머니 부탁으로 이불을 폈다. 그 뒤 부엌으로 돌아갔다.", "nabi neutral"),
        "clock":("숫자 없는 벽시계", "숫자가 없어 위아래를 뒤집으면 바늘 방향도 반대로 보인다.", "assets/clock-base.png"),
        "fur":("솜솜의 붉은 자국", "털에 세련의 글씨와 별 끝이 거꾸로 눌려 찍혔다. 주머니 봉인띠의 덜 마른 도장과 같다.", "clue fur"),
        "record":("너울의 공개 기록", "「안 쓰는 방에서 작은 손님 발견」. 침대 밑이나 상자 뒤라는 위치는 발표하지 않았다.", "assets/record.png"),
        "seal":("끊어지지 않은 봉인", "너울과 나비가 온전한 봉인을 확인한 뒤 개봉했다. 세련도 자신이 밤 11시에 한 봉인이라고 확인했다. 안에는 백 냥.", "assets/seal.png"),
        "karo":("놓친 마차", "세련은 어제 오후 노름판에서 마차를 놓쳤다. 까로는 잃은 돈의 액수를 보지 못했다.", "karo neutral"),
    }
    EVIDENCE["bami"] = ("밤이의 목격담", "거꾸로 매달린 밤이: 6시 반쯤 세련이 붉은 주머니를 들고 끝방으로 갔다 빈손으로 돌아왔다. 새벽 5시에는 잠들었다.", "bami neutral")
    EVIDENCE["snow"] = ("도토의 날씨 일지", "「자정, 첫눈」. 종이 열두 번 울렸다. 그때 복도에 밤이가 깨어 있었다.", "assets/notebook.png")
    EVIDENCE["registry"] = ("작은 손님의 기록", "첫눈마다 「작은 손님, 베개 구석」. 이름 없는 겨울잠 손님을 재운 장부.", "assets/notebook.png")

    def acquire(key):
        if key not in store.inventory:
            store.inventory.append(key)
            renpy.notify("수첩에 기록했다: " + EVIDENCE[key][0])

    def mark_seen(key):
        if key not in store.inspected:
            store.inspected.append(key)

    def available_locations():
        return ["plaza","front","kitchen"] if store.stage == "arrival" else list(LOCATIONS)

    def search_ready():
        return store.lamp_ready and "registry" in store.inventory

    def council_ready():
        return store.somsom_found and all(k in store.inventory for k in ("pouch","clock","bami","snow","registry","fur","record","seal"))

    def current_goal():
        if store.stage == "arrival":
            return "마을을 둘러보거나 방으로 올라가자." if "granny_arrival" in store.inspected else "여관에 방을 잡자."
        if store.stage == "aftermath": return "떠나기 전에 주민들과 다시 이야기하자."
        if not store.somsom_found: return "할머니가 감추는 손님은 누구일까?"
        return "목격 시각과 주머니의 흔적을 확인하자."

    def evidence_text(key):
        if key == "bami" and "clock" in store.resolved_topics:
            return "정정된 목격 시각: 자정. 시계를 거꾸로 읽어 6시 반이라 했다. 그때 세련은 주머니를 들고 끝방에 갔다가 빈손으로 돌아왔다."
        return EVIDENCE[key][1]

    def council_quote(person):
        quotes = {
            "granny":"내가 입을 다문 건 돈 때문이 아니야. 그 손님에게 약속한 게 있어.",
            "seryeon":"쥐와 제 주머니는 아무 관계가 없습니다.",
            "nabi":"이불은 내가 폈어. 그런데 그게 돈을 훔쳤다는 말은 아니잖아.",
            "bami":"아침 여섯 시 반쯤이었어. 그 손님은 빈손으로 돌아왔고.",
            "doto":"첫눈은 자정이었어요. 내가 틀렸다면 공책 한 권을 다 버려야 해요.",
            "buri":"차가우면 끝인 줄 알았지. 살아 있는 건 장치랑 다르더군.",
            "karo":"정오 차는 기다릴 수 있어. 다만 없는 돈까지 실어 줄 순 없지.",
            "neoul":"의심은 들었어. 이제 누구 말이 증거와 맞는지 보자.",
        }
        if person == "bami" and "clock" in store.resolved_topics:
            return "시계를 거꾸로 읽었어. 내가 본 건 자정이야."
        if person == "seryeon" and "contact" in store.resolved_topics:
            return "주머니가 닿았다고 제가 돈을 훔친 건 아니죠."
        return quotes[person]

    def trial_state():
        def opened(s): return bool(renpy.get_screen(s))
        return dict(stage=store.stage, location=store.current_location, inventory=list(store.inventory), inspected=list(store.inspected),
            visited=list(store.visited), lamp=store.lamp_ready, found=store.somsom_found, permission=store.archive_permission,
            archive=store.archive_open, speaker=store.speaker, first=store.meeting_first, topic=store.comparison_topic,
            resolved=list(store.resolved_topics), showdown=store.showdown_issue, wrong=store.wrong_attempts,
            conclusion_attempts=store.conclusion_attempts, complete=store.test_complete, case_resolved=store.case_resolved, mother=store.mother_clue,
            music=renpy.music.get_playing(), music_position=renpy.music.get_pos(), typing=renpy.music.get_playing(channel="typing"),
            music_volume=_preferences.get_volume("music"), music_mute=_preferences.get_mute("music"),
            explore=opened("explore"), map=opened("village_map"), council=opened("council"), duel=opened("duel"),
            code=opened("chest_lock"), digits=list(store.digit_code), code_error=store.code_error, clock_demo=opened("clock_compare"),
            rotated=store.clock_rotated, clock_done=store.clock_demonstrated, choice=opened("choice"),
            evidence=opened("evidence_book"), menu=opened("pause_menu"), saving=opened("save"), loading=opened("load"),
            completion=opened("trial_complete"), input_ready=(renpy.get_screen("explore").scope.get("input_ready") if opened("explore") else None),
            saved_slots=[s[0] for s in renpy.list_saved_games()])

define dad = Character("아빠",color="#eddbb2",cb_who_id="dad")
define daram = Character("다람",color="#ffbd76",cb_who_id="daram")
define granny = Character("할머니",color="#e8ca9a",cb_who_id="granny")
define seryeon = Character("세련",color="#d8c5ad",cb_who_id="seryeon")
define nabi = Character("나비",cb_who_id="nabi")
define bami = Character("밤이",cb_who_id="bami")
define doto = Character("도토",cb_who_id="doto")
define buri = Character("부리",cb_who_id="buri")
define karo = Character("까로",cb_who_id="karo")
define neoul = Character("너울",cb_who_id="neoul")

image bg carriage = Transform("assets/carriage.png",size=(1280,720))
image bg approach = Transform("assets/approach.png",size=(1280,720))
image bg room = Transform("assets/room.png",size=(1280,720))
image bg front = Transform("assets/front.png",size=(1280,720))
image bg kitchen = Transform("assets/kitchen.png",size=(1280,720))
image bg hall = Transform("assets/hall.png",size=(1280,720))
image bg doto = Transform("assets/doto-room.png",size=(1280,720))
image bg council = Transform("assets/council.png",size=(1280,720))
image bg post = Transform("assets/outdoor-post.png",size=(1280,720))
image bg inn = Transform("assets/outdoor-inn.png",size=(1280,720))
image cg pouch = Transform("assets/pouch.png",size=(1280,720))
image cg somsom = Transform("assets/somsom.png",size=(1280,720))
image clue fur = Composite((512,512), (0,0), Transform(Crop((835,445,130,130),"assets/somsom.png"),size=(512,512)), (0,0), "assets/fur-stamp.png")

transform portrait_close:
    xalign 0.5
    yanchor 1.0
    ypos 551
    size (340,440)
    fit "contain"
    alpha 0.0
    ease 0.15 alpha 1.0

# Topic selection uses the same full-body interview art beside the choices.
# Spoken dialogue keeps portrait_close at the centre of the scene.
transform portrait_question:
    xpos 950
    yanchor 1.0
    ypos 551
    size (300,440)
    fit "contain"
    alpha 0.0
    ease 0.15 alpha 1.0

transform thumbnail:
    size (112,72)

transform resident_world:
    xanchor 0.5
    yanchor 1.0
    zoom 0.64

transform table_world:
    size (1130,390)
    xpos 75
    ypos 270
