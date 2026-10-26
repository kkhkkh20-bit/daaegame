# Delivered B faces keep the authored speaker/expression; missing neutral stays empty.
init 171 python:
    R13_BDIALOGUE_FACES = json.load(renpy.file("assets/room13-dialogue-b-faces.json"))
    # 2026-10-26 소유자: 얼굴 스티커는 쓰지 않는다. 파일과 연결표는 남기고 화면에만 내지 않는다.
    R13_BDIALOGUE_FACES_ON = False

    def r13_bdialogue_face(person, expression):
        if not person or person == "dad" or not globals().get("R13_BDIALOGUE_FACES_ON", True):
            return None
        # Match the same aliases as the existing full-body renderer.
        expression = {"surprise": "surprise_talk", "flustered": "anxious"}.get(expression, expression)
        path = R13_BDIALOGUE_FACES.get(person, {}).get(expression)
        return path if path and renpy.loadable(path) else None
