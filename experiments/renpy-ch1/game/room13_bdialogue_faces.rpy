# Delivered B faces keep the authored speaker/expression; missing neutral stays empty.
init 171 python:
    R13_BDIALOGUE_FACES = json.load(renpy.file("assets/room13-dialogue-b-faces.json"))

    def r13_bdialogue_face(person, expression):
        if not person or person == "dad":
            return None
        # Match the same aliases as the existing full-body renderer.
        expression = {"surprise": "surprise_talk", "flustered": "anxious"}.get(expression, expression)
        path = R13_BDIALOGUE_FACES.get(person, {}).get(expression)
        return path if path and renpy.loadable(path) else None
