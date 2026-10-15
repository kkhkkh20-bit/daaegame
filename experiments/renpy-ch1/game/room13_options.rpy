# Options change presentation only. They never write campaign, evidence, saves,
# learned dialogue, ending history or the in-game clock.
default persistent.room13_typing_sound = True

init 70 python:
    def r13_set_option(name, value):
        if name not in ("room13_typing_sound", "room13_motion"):
            return
        setattr(persistent, name, value)
        if name == "room13_typing_sound" and not value:
            renpy.music.stop(channel="typing")
        renpy.save_persistent()
        renpy.restart_interaction()

    def r13_test_option_sound():
        if preferences.get_mute("sfx") or preferences.get_volume("sfx") <= 0:
            renpy.notify("효과음이 꺼져 있어요. 음량과 켜짐 상태를 확인해 주세요.")
            return
        renpy.music.play("assets/sfx-click.wav", channel="sound", loop=False)

    def r13_reset_options():
        preferences.set_volume("music", config.default_music_volume)
        preferences.set_volume("sfx", config.default_sfx_volume)
        preferences.set_mute("music", False)
        preferences.set_mute("sfx", False)
        preferences.text_cps = config.default_text_cps
        preferences.afm_time = 15
        # 0.18.46: reset also turns auto-forward off, so lines do not advance on their own after
        # the menu closes.
        preferences.afm_enable = False
        persistent.room13_text_small = False
        persistent.room13_large_text = bool(renpy.variant("small"))
        persistent.room13_large_text_auto = True
        persistent.room13_window_alpha = "d4"
        persistent.room13_motion = True
        persistent.room13_typing_sound = True
        store.r13_fast_read = False
        store.r13_fast_all = False
        renpy.stop_skipping()
        renpy.save_persistent()
        renpy.restart_interaction()
        renpy.notify("옵션을 기본값으로 돌렸어요. 진행 기록은 그대로입니다.")
