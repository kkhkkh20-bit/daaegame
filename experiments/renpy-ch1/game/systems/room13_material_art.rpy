# Original, clean inventory illustrations. Read-only: drawing never grants a record
# or changes the distinction between evidence, a gift and a borrowed tool.
init 150 python:
    import json as r13_material_json
    with renpy.file("assets/room13-material-icons079.json") as r13_material_file:
        R13_MATERIAL_ART=r13_material_json.load(r13_material_file)["icons"]

    def r13_material_art(key):
        spec=R13_MATERIAL_ART.get(key)
        if spec is None:return None
        # One logical sprite size for a stable dot scale in 60px lists and
        # enlarged details. Nearest sampling is retained at both UI sizes.
        return Transform(Crop(tuple(spec["crop"]),spec["file"]),xysize=(64,64),fit="contain",nearest=True)
