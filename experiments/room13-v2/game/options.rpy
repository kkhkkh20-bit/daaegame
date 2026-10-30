# 다람탐정 v2(1일 시범) 설정.
# 지금 판(renpy-ch1)과 저장이 섞이지 않게 저장 폴더 이름을 따로 둔다.
define config.name = "다람탐정 v2 · 1일 시범"
define config.version = "v2-pilot-1"
define config.save_directory = "room13-v2"
define build.name = "room13_v2"
# 건너뛰기는 읽지 않은 줄도 넘기고 다음 고르는 화면에서 멈춘다(엔진이 고르는 화면 앞에서 choice_for_skipping 을 부른다).
default preferences.skip_unseen = True
default preferences.skip_after_choices = False

init python:
    gui.init(1280, 720)
    config.main_menu_music = "assets/bgm-title.mp3"
    config.default_music_volume = 0.75
    config.default_sfx_volume = 0.7
    # 지금 판과 같은 기본 대사 속도(0.20.4 소유자 「빠르게」).
    config.default_text_cps = 55
    config.window = "auto"
    config.rollback_enabled = True
    # 도트 그림은 이웃 화소 그대로 키운다(지금 판과 같다).
    config.nearest_neighbor = True
    config.enter_transition = Dissolve(0.12)
    config.exit_transition = Dissolve(0.12)
    config.after_load_transition = Dissolve(0.2)
    # 오른쪽 클릭·Esc 는 설정창(저장·불러오기는 그 아래 줄).
    config.game_menu_action = [FileTakeScreenshot(), Show("v2_settings")]
    config.quit_action = Quit(confirm=False)
    config.has_autosave = False
    config.autosave_on_choice = False
    renpy.music.register_channel("amb", "sfx", loop=True)
    renpy.music.register_channel("ride", "sfx", loop=True)
    renpy.music.register_channel("hooves", "sfx", loop=True)
    build.classify("**.py", None)
    build.classify("**/__pycache__/**", None)
    build.classify("tests/**", None)
