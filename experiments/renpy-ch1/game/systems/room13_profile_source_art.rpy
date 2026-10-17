# Approved neutral faces for record/profile icons only. World poses stay pixel art.
init 174 python:
    R13_PROFILE_SOURCE_ART = json.load(renpy.file("assets/room13-profile-source-art.json"))

    def r13_profile_nearest(person):
        # Held/excluded characters keep their existing pixel profile treatment.
        return person not in R13_PROFILE_SOURCE_ART["people"]

    for _r13_profile_person, _r13_profile_spec in R13_PROFILE_SOURCE_ART["people"].items():
        renpy.image(_r13_profile_person+" avatar_neutral",
            Transform(_r13_profile_spec["file"],nearest=False,subpixel=True))
