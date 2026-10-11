define config.name = "다람탐정 · Ren’Py 테스트"
define config.version = "0.1.0"
# Literal define is evaluated early enough for the browser's persistent save path.
# Setting this inside init python chooses game/saves before the assignment runs.
define config.save_directory = "daaegame-renpy-prototype-20261011"

init python:
    gui.init(1280, 720)
    config.has_voice = True
    config.default_music_volume = 0.45
    config.default_sfx_volume = 0.6
    config.default_text_cps = 32
    config.window = "auto"
    config.window_show_transition = Dissolve(0.15)
    config.window_hide_transition = Dissolve(0.15)
    config.game_menu_action = ShowMenu("pause_menu")
    config.rollback_enabled = True
    config.nearest_neighbor = True
    config.gl2 = True
    config.enter_transition = Dissolve(0.15)
    config.exit_transition = Dissolve(0.15)
    config.after_load_transition = Fade(0.12, 0.12, 0.2)
    build.name = "daram_renpy_test"
    build.version = "0.1.0"
    build.classify("game/assets/font-license.txt", "all")
    build.classify("game/assets/provenance.json", "all")
    build.classify("**.py", None)
    build.classify("**.log", None)
    build.classify("**/saves/**", None)
    build.classify("**/cache/**", None)
    build.classify("**/qa-output/**", None)
    build.classify("**.md", None)
    build.classify("**.txt", None)

default inventory = []
default inspected = []
default stage = "intro"
default place = "마차 안"
default clock_text = "해 질 무렵"
default selected_evidence = None
default meeting_first = None
default meeting_proved = False
default wrong_attempts = 0
default conclusion_attempts = 0
default test_complete = False

init python:
    import json
    EVIDENCE = {
        "pouch": ("봉인된 주머니", "접힌 별 끝의 도장이 찍혀 있다. 봉인은 아직 끊어지지 않았다.", "assets/pouch.png"),
        "fur": ("솜솜의 털에 남은 자국", "붉은 별 끝이 반대로 찍혔다. 털 위의 자국과 주머니 도장을 비교할 수 있다.", "assets/somsom.png"),
        "flour": ("이불의 밀가루 손자국", "누군가 밀가루 묻은 손으로 이불을 정리했다. 주머니와 닿았다는 증거는 아니다.", "assets/room.png"),
    }

    def acquire(evidence_id):
        if evidence_id not in inventory:
            inventory.append(evidence_id)

    def trial_state():
        # Read-only snapshot used by QA through the SDK's native renpy_exec bridge.
        return dict(stage=stage, inventory=list(inventory), inspected=list(inspected),
                         first=meeting_first, proved=meeting_proved, wrong=wrong_attempts,
                         conclusion_attempts=conclusion_attempts, complete=test_complete,
                         music=renpy.music.get_playing(channel="music"),
                         menu=bool(renpy.get_screen("pause_menu")),
                         evidence_open=bool(renpy.get_screen("evidence_book")),
                         saving=bool(renpy.get_screen("save")),
                         loading=bool(renpy.get_screen("load")),
                         investigation_open=bool(renpy.get_screen("investigate")),
                         testimony_open=bool(renpy.get_screen("testimony")),
                         choice_open=bool(renpy.get_screen("choice")),
                         completed_open=bool(renpy.get_screen("trial_complete")),
                         investigation_ready=(renpy.get_screen("investigate").scope.get("input_ready") if renpy.get_screen("investigate") else None),
                         saved_slots=[s[0] for s in renpy.list_saved_games()],
                         music_position=renpy.music.get_pos(channel="music"))

define dad = Character("아빠", color="#eddbb2")
define daram = Character("다람", color="#ffbd76")
define granny = Character("할머니", color="#e8ca9a")
define seryeon = Character("세련", color="#d8c5ad")

image bg carriage = Transform("assets/carriage.png", size=(1280, 720))
image bg approach = Transform("assets/approach.png", size=(1280, 720))
image bg room = Transform("assets/room.png", size=(1280, 720))
image bg council = Transform("assets/council.png", size=(1280, 720))
image cg pouch = Transform("assets/pouch.png", size=(1280, 720))
image cg somsom = Transform("assets/somsom.png", size=(1280, 720))

# Crop at runtime using the existing approved atlas coordinates; no edited PNGs.
image daram neutral = Crop((397, 184, 220, 258), "assets/family.png")
image daram thinking = Crop((684, 184, 220, 258), "assets/family.png")
image daram expressive = Crop((1269, 184, 220, 258), "assets/family.png")
image granny neutral = Crop((399, 163, 241, 249), "assets/inn.png")
image granny distressed = Crop((1108, 163, 241, 249), "assets/inn.png")
image seryeon neutral = Crop((395, 542, 270, 277), "assets/inn.png")
image seryeon thinking = Crop((750, 542, 270, 277), "assets/inn.png")
image seryeon distressed = Crop((1104, 542, 270, 277), "assets/inn.png")

transform close_right:
    xalign 0.78
    yanchor 1.0
    ypos 560
    zoom 1.5
    alpha 0.0
    ease 0.18 alpha 1.0

transform close_left:
    xalign 0.22
    yanchor 1.0
    ypos 560
    zoom 1.5
    alpha 0.0
    ease 0.18 alpha 1.0

transform thumbnail:
    size (160, 90)
