# Transfer HTML loading music before Ren'Py's first interaction/audio periodic.
init 90 python:
    if renpy.emscripten:
        import emscripten

        def r13_loading_audio_handoff():
            if config.main_menu_music not in (renpy.music.get_loop(channel="music") or []):
                return
            position = float(emscripten.run_script_string("String(window.r13LoadingAudio ? window.r13LoadingAudio.handoff() : 0)"))
            if position > 0:
                renpy.music.play("<from %.3f>%s" % (position, config.main_menu_music), fadein=0)
            config.interact_callbacks.remove(r13_loading_audio_handoff)

        config.interact_callbacks.append(r13_loading_audio_handoff)
