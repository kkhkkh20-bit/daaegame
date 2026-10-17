# Approved 2026-10-17 front-left threequarter; rejected side-profile source is not imported.
init 178 python:
    R13_SEORI_MAP_REVIEW=json.load(renpy.file("assets/room13-seori-review-art.json"))
    _sr=R13_SEORI_MAP_REVIEW
    if renpy.loadable(_sr["spec"]["file"]):
        R13_ACTING.setdefault(_sr["person"],{})[_sr["pose"]]=_sr["spec"]
        CAST[_sr["person"]][_sr["pose"]]=_sr["spec"]
        renpy.image(_sr["person"]+" "+_sr["pose"],Transform(Crop(tuple(_sr["spec"]["crop"]),_sr["spec"]["file"]),nearest=True))
