define config.name = "다람탐정 · 눈에 갇힌 마을"
define config.version = "0.20.73"
# Literal early definition selects the persistent web save mount.
define config.save_directory = "daaegame-renpy-village-ch1-06"

default place = "마차 안"
default target = None
default typing_allowed = True
default dialogue_speaker = None
default dialogue_expression = "neutral"

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
    config.default_text_cps = 55  # 0.20.4 소유자: "대사 타이핑속도 디폴트를 빠르게"
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
    build.version = "0.20.73"
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
        if any(renpy.get_screen(s) for s in ("pause_menu", "save", "load")):
            renpy.music.stop(channel="typing")
    config.interact_callbacks.append(stop_menu_typing)
    config.character_callback = text_audio

    CAST = json.load(renpy.file("assets/cast.json"))
    NAMES = {"dad":"아빠", "daram":"다람", "granny":"할머니", "seryeon":"세련", "nabi":"나비", "bami":"밤이", "doto":"도토", "buri":"부리", "karo":"까로", "neoul":"너울"}
    for person, states in CAST.items():
        for state_name, spec in states.items():
            renpy.image(person + " " + state_name, Transform(Crop(tuple(spec["crop"]), r13_asset("file:"+spec["file"])),nearest=spec.get("nearest",True)))

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
