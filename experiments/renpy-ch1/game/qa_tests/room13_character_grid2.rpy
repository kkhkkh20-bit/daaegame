# PREVIEW-ONLY infrastructure. No automatic activation or image replacement.
# One cell = 2x2 virtual pixels on the 1280x720 game canvas.
# Never wrap say/UI/background layers. Compose character geometry FIRST.
init 176 python:
    import math as r13_grid2_math
    R13_CHARACTER_GRID2_PREVIEW = False

    def r13_grid2_snap(value):
        return int(r13_grid2_math.floor(float(value) / 2.0 + 0.5)) * 2

    def r13_grid2_final_character_layer(character_layer):
        """Child must be a transparent 1280x720 character-only composition.
        Include crop, body reactions, entrance, perspective, position and camera
        INSIDE this child. Do not scale/move the returned output afterward.
        This is a format proof, not a pixel-art authoring substitute.
        """
        if not R13_CHARACTER_GRID2_PREVIEW:
            return character_layer
        full = Fixed(character_layer, xysize=(1280, 720))
        low = Transform(full, xysize=(640, 360), nearest=True,
                        subpixel=False, rotate_pad=False)
        # Force a real low-resolution texture; consecutive scale transforms
        # alone can collapse and retain fine source pixels.
        texture = Flatten(low)
        return Transform(texture, xysize=(1280, 720), nearest=True,
                         subpixel=False, rotate_pad=False)

    def r13_grid2_source_art(art, width, height):
        """Direct source geometry only. Bypass legacy grid before final pass.
        Do not call this on already-low-res proof boards or manufactured 560px
        exports where higher-resolution approved source art is available.
        """
        return Transform(art, size=(max(1,int(round(width))),max(1,int(round(height)))),
                         nearest=True, subpixel=False, rotate_pad=False)
