# Dialogue close-ups from the 43-character full-body expression set (0.18.5).
# Presentation only: no clock, evidence, relationship or schedule changes.
#
# - Data: assets/room13-fullbody-dialogue.json (dev/import_fullbody_expressions.py)
#   and assets/room13-fullbody-line-emotions.json (hand-authored per line).
# - One fixed crop and one scale per character for every expression, so a
#   change of expression never moves or resizes the body.
# - The older dialogue busts (room13-portraits.json), profile avatars and world
#   sprites stay as they are; the busts remain the fallback when a character
#   or file is missing, and the gate waiting window still uses Daram's bust.
# - No mouth or idle animation is added (r13_idle_art stays static). Daram's
#   eyes blink (0.18.29, room13_dot_fx.rpy) when the motion option is on.
init 58 python:
    R13_FULLBODY_DIALOGUE = True
    R13_FULLBODY = json.load(renpy.file("assets/room13-fullbody-dialogue.json")) if renpy.loadable("assets/room13-fullbody-dialogue.json") else {"people":{}}
    R13_FULLBODY_LINES = json.load(renpy.file("assets/room13-fullbody-line-emotions.json")) if renpy.loadable("assets/room13-fullbody-line-emotions.json") else {"lines":{},"legacy_map":{}}
    R13_FULLBODY_EMOTIONS = ("neutral","joy","flustered","angry","anxious","surprise")
    # Checked once: renpy.loadable per call is slow on the web build, and
    # prediction asks for close-ups many times per interaction.
    R13_FULLBODY_FILES = {image["file"] for entry in R13_FULLBODY.get("people",{}).values()
        for image in list(entry["images"].values())+list(entry.get("poses",{}).values()) if renpy.loadable(image["file"])}
    R13_FULLBODY_NEW = ("joy","flustered","angry","anxious","surprise")
    # Existing engine keys -> full-body expression. "thinking" has no full-body
    # image and stays neutral; authored per-line choices override this.
    R13_FULLBODY_LEGACY = dict(R13_FULLBODY_LINES.get("legacy_map") or {
        "neutral":"neutral","thinking":"neutral","distressed":"anxious",
        "expressive":"joy","panic":"surprise","breakdown":"anxious","joy":"joy"})
    # New key -> nearest older key, for profile avatars and bust fallback.
    R13_FULLBODY_TO_LEGACY = {"neutral":"neutral","joy":"expressive","surprise":"expressive",
        "flustered":"distressed","angry":"distressed","anxious":"distressed"}
    R13_FULLBODY_PLAIN = set(R13_FULLBODY_LEGACY)|set(R13_FULLBODY_EMOTIONS)
    # Share of the dialogue height given to the whole standing figure. The
    # figure is top-aligned; legs continue behind the dialogue panel.
    R13_FULLBODY_FIGURE = 1.05
    R13_FULLBODY_TOP_PAD = 12
    # Per-character adjustments found in the in-game check (figure multiplier):
    # tall ears/hair push these faces down to the large-text dialogue panel.
    R13_FULLBODY_TUNING = {"bami":.88,"doto":.92}

    def r13_fullbody_key(pose):
        key=pose or "neutral"
        if key.startswith("interview_"):key=key[10:]
        return key

    def r13_fullbody_emotion(pose):
        key=r13_fullbody_key(pose)
        if key in R13_FULLBODY_EMOTIONS:return key
        return R13_FULLBODY_LEGACY.get(key,"neutral")

    def r13_fullbody_spec(person,pose="neutral"):
        if not R13_FULLBODY_DIALOGUE:return None
        entry=R13_FULLBODY.get("people",{}).get(person)
        if not entry:return None
        # 0.18.89: an authored pose picture (door_peek, kneel_stone...) has its own file and
        # crop; the scale stays the character's (r13_fullbody_scale uses the entry's figure).
        posed=entry.get("poses",{}).get(r13_fullbody_key(pose))
        if posed and posed["file"] in R13_FULLBODY_FILES:
            return dict(file=posed["file"],crop=posed["crop"],figure=posed["figure"],emotion=r13_fullbody_key(pose),fit=posed.get("fit",1.0))
        emotion=r13_fullbody_emotion(pose)
        # 0.18.92: an expression the package drew beyond the six (bami "thinking") is used by name.
        key=r13_fullbody_key(pose)
        if key not in R13_FULLBODY_EMOTIONS and key in entry["images"]:emotion=key
        image=entry["images"].get(emotion) or entry["images"].get("neutral")
        if not image or image["file"] not in R13_FULLBODY_FILES:return None
        return dict(file=image["file"],crop=entry["crop"],figure=entry["figure"],emotion=emotion,image=image)

    def r13_fullbody_scale(person,height):
        entry=R13_FULLBODY["people"][person]
        figure_height=float(max(1,entry["figure"][3]))
        scale=height*R13_FULLBODY_FIGURE*R13_FULLBODY_TUNING.get(person,1.0)/figure_height
        # Topic lists start 200px right of the portrait centre.
        max_width=880.0 if height>=800 else 400.0
        cap=max_width/max(1,entry["crop"][2])
        # 0.18.92 (owner): pixel-art expressions (2x2 px cells) are drawn at a whole number of
        # screen pixels per art cell, the nearest to the usual size (never smoothed or stretched).
        pixel=entry.get("pixel")
        if pixel:
            unit=float(pixel["u"])*pixel["cell"]
            # 0.18.99: proposal preview only (docs/PIXEL_UNIFY_PROPOSAL_20261016.md). Default None =
            # unchanged; a QA test may set one fixed number of screen pixels per art cell.
            fixed=getattr(store,"r13_pixel_k_preview",None)
            if fixed:return float(fixed)/unit
            k=max(1,int(round(scale*unit)))
            while k>1 and k/unit>cap:k-=1
            return k/unit
        return min(scale,cap)

    def r13_fullbody_mapped_art(person,emotion,image,crop,scale,width,height):
        """0.18.92: a picture stored in its own pixels with a map [u, ox, oy] to the character's
        reference canvas (dev/apply_expression_acting.py). Drawn into a box of the reference crop's
        size, so position and size code is the same as for every other close-up. Pixel art
        ("cell": 2) is scaled by a whole number of screen pixels per cell and never resampled
        through the 3px grid; other pictures use the usual grid."""
        u,ox,oy=image["map"]
        fx,fy,fw,fh=image["crop"]
        s=scale*u
        w,h=max(1,int(round(fw*s))),max(1,int(round(fh*s)))
        # Eye blink pieces (room13_dot_fx.rpy) sit on the uncropped picture, in its own pixels.
        piece=Crop((fx,fy,fw,fh),r13_blink_art(person,emotion,image["file"]))
        if image.get("cell"):
            piece=Transform(piece,size=(w,h),nearest=True,subpixel=False)
        else:
            piece=r13_pixel_scale(piece,w,h,R13_CLOSE_PIXEL_GRID)
        dx=int(round((ox+u*fx-crop[0])*scale));dy=int(round((oy+u*fy-crop[1])*scale))
        return Fixed(Transform(piece,xpos=dx,ypos=dy),xysize=(max(1,int(round(width))),max(1,int(round(height)))))

    # One displayable per character/expression/size: screens and statement
    # prediction re-evaluate r13_close_art often, and a fresh Flatten each
    # time forces a new render-to-texture (this stalled the web build).
    R13_FULLBODY_ART_CACHE={}

    def r13_fullbody_close_art(person,pose,height,speaking=False,entrance=False):
        spec=r13_fullbody_spec(person,pose)
        if not spec:return None
        key=(person,spec["emotion"],int(height))
        result=R13_FULLBODY_ART_CACHE.get(key)
        if result is None:
            scale=r13_fullbody_scale(person,height)*spec.get("fit",1.0)
            width=spec["crop"][2]*scale;native_height=spec["crop"][3]*scale
            image=spec.get("image") or {}
            if image.get("map"):
                result=r13_fullbody_mapped_art(person,spec["emotion"],image,spec["crop"],scale,width,native_height)
            else:
                # Eye blink pieces (room13_dot_fx.rpy) sit on the uncropped picture.
                art=Crop(tuple(spec["crop"]),r13_blink_art(person,spec["emotion"],spec["file"]))
                result=r13_pixel_scale(art,width,native_height,R13_CLOSE_PIXEL_GRID)
            result=r13_idle_art(result,person,pose,None,int(round(width)),int(round(native_height)),contact="dialogue_bust",speaking=speaking)
            if len(R13_FULLBODY_ART_CACHE)>=24:R13_FULLBODY_ART_CACHE.clear()
            R13_FULLBODY_ART_CACHE[key]=result
        return At(result,r13_actor_enter(r13_appearance_duration())) if entrance else result

    R13_FULLBODY_CENTRE = json.load(renpy.file("assets/room13-fullbody-centre.json")) if renpy.loadable("assets/room13-fullbody-centre.json") else {}

    def r13_close_x(person,pose="interview_neutral",height=840):
        """Screen x for the close-up's centre: the head and torso, not the crop box, sit at 640
        (dev/fullbody_centre.py). Same value in dialogue and on the question screen."""
        spec=r13_fullbody_spec(person,pose)
        if not spec:return 640
        return int(round(640-R13_FULLBODY_CENTRE.get(person,0)*r13_fullbody_scale(person,height)*spec.get("fit",1.0)))

    def r13_fullbody_close_y(person,height,top,pose):
        spec=r13_fullbody_spec(person,pose)
        if not spec:return None
        scale=r13_fullbody_scale(person,height)*spec.get("fit",1.0)
        above=spec["figure"][1]-spec["crop"][1]
        return int(top+R13_FULLBODY_TOP_PAD*height/840.0-above*scale)

    def r13_fullbody_line_emotion(identity,index,person,text,expression,pose):
        # Only plain emotion poses become full-body expressions; authored
        # acting poses (chairs, props, activities) keep their own meaning.
        if pose not in R13_FULLBODY_PLAIN:return None
        cue=R13_FULLBODY_LINES.get("lines",{}).get(identity,{}).get(str(index))
        if cue and cue.get("person")==person and cue.get("text")==text and cue.get("emotion") in R13_FULLBODY_EMOTIONS:
            return cue["emotion"]
        if pose in R13_FULLBODY_NEW:return pose
        if expression in R13_FULLBODY_NEW:return expression
        return None

    def r13_fullbody_refresh_after_load():
        # A save keeps the displayable it was drawn with (older saves: a bust).
        # Redraw only the current conversation partner with the same speaker,
        # expression and pose; the line, choice and scene stay as saved.
        if not R13_FULLBODY_DIALOGUE or "r13_visitor" not in renpy.get_showing_tags():return
        choice_screen=renpy.get_screen("choice")
        actor=choice_screen.scope.get("choice_actor") if choice_screen else store.r13_motion_person
        if actor not in CAST or not r13_fullbody_spec(actor,store.r13_current_pose):return
        pose=choice_screen.scope.get("choice_pose",store.r13_current_pose) if choice_screen else store.r13_current_pose
        saved_speaker=store.dialogue_speaker
        renpy.hide("r13_visitor")
        r13_speaker(actor,store.dialogue_expression,pose)
        store.dialogue_speaker=saved_speaker
