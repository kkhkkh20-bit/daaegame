# 0.19.7: the web loader writes the core archive to /game.zip and Ren'Py unpacks it into /game, but the
# 17.8MB zip stayed in browser memory for the whole session. Phones (iOS especially) then had less room
# for the WebGL canvas. Once the game files are unpacked the zip is not read again.
init -999 python:
    if renpy.emscripten:
        import os as _r13_os
        try:
            if _r13_os.path.exists("/game.zip"):
                _r13_os.unlink("/game.zip")
        except Exception:
            pass
