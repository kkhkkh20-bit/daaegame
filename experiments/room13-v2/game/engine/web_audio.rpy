# 웹 로딩창 음악 넘겨받기(지금 판 systems/room13_loading_audio.rpy 와 같은 일).
# 로딩창(HTML)이 메인화면 음악을 먼저 튼다. Ren'Py 의 첫 화면이 뜨면 그 위치부터 이어 틀고 HTML 쪽은 끈다.
# 넘겨받지 않으면 같은 음악이 두 겹으로 난다. 데스크톱·시험에서는 아무것도 하지 않는다.

init python:
    if renpy.emscripten:
        import emscripten

        def v2_loading_audio_handoff():
            if config.main_menu_music not in (renpy.music.get_loop(channel="music") or []):
                return
            position = float(emscripten.run_script_string("String(window.r13LoadingAudio ? window.r13LoadingAudio.handoff() : 0)"))
            if position > 0:
                renpy.music.play("<from %.3f>%s" % (position, config.main_menu_music), fadein=0)
            config.interact_callbacks.remove(v2_loading_audio_handoff)

        config.interact_callbacks.append(v2_loading_audio_handoff)
