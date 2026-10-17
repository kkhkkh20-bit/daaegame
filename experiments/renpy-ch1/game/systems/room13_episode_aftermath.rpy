# Episode aftermaths read completed outcomes; they never award evidence or move time.
# Saved UI progress keeps a mid-cutscene save on the same authored branch.
default r13_aftermath_active = False
default r13_aftermath_episode = None
default r13_aftermath_frames = []
default r13_aftermath_index = 0

init 175 python:
    import json as r13_aftermath_json
    with renpy.file("assets/room13-episode-aftermath.json") as r13_aftermath_file:
        R13_AFTERMATH = r13_aftermath_json.load(r13_aftermath_file)["frames"]
    R13_AFTERMATH_TITLES = dict(ep1="조각을 되돌린 뒤",ep2="이름을 부른 뒤",ep2_clinic="이틀 뒤, 진료소",ep3="불이 꺼진 뒤",ep4="등을 켠 뒤",ep5="수프가 식은 뒤",ep6="수레가 지난 뒤")

    def r13_episode_aftermath_frames(episode,state=None):
        """Pure branch selection. Death/absence always outranks an earlier rescue flag."""
        s=room13 if state is None else state
        flags=set(s.get("flags",[]))
        has=lambda f:f in flags
        child=s.get("daram_state") in ("with_dad","rescued")
        keys=[]
        if episode=="ep1":
            keys.append("piko_dead" if has("piko_dead") else "piko_saved")
            keys.append("tok_detained" if has("tok_detained") and not has("tok_cleared") else "tok_free")
            if has("siluk_handed"):keys.append("siluk_handed")
            elif has("siluk_debt_cleared"):keys.append("siluk_debt")
            if has("madam_store_opened") and not has("siluk_debt_cleared"):keys.append("madam_open")
        elif episode=="ep2":
            if has("kd_shoes_only"):keys.append("musoe_shoes")
            elif has("kd_farewell_seen"):keys.append("musoe_farewell")
            elif has("kd_seori"):keys.append("clinic_empty" if has("musoe_gone") else "musoe_clinic")
            if has("bami_taken"):keys.append("bami_taken")
            elif has("bami_safe"):keys.append("bami_safe")
            if has("kd_named"):keys.append("somi_silent")
        elif episode=="ep2_clinic":
            keys.append("clinic_empty")
        elif episode=="ep3":
            if has("wf_missed"):keys.append("shed_empty")
            elif has("kkomi_dead"):
                keys.append("kkomi_dead" if child else "shed_empty")
            else:keys.append("kkomi_saved" if child else "kkomi_alone")
            if has("bori_taken") and not has("wf_bori_freed"):keys.append("bori_taken")
            elif has("bori_adopts") and not has("soup_kids_dead"):keys.append("bori_adopts")
            if has("nubi_kids_with_nabi"):keys.append("nabi_children")
        elif episode=="ep4":
            if has("chorong_dead"):keys.append("chorong_dead")
            elif has("nt_chorong_half"):keys.append("chorong_hurt")
            elif has("nt_chorong_safe"):keys.append("chorong_safe")
            if has("ttadak_dead"):keys.append("ttadak_dead")
            elif has("nt_ttadak_half"):keys.append("ttadak_hurt")
            elif has("nt_ttadak_safe"):keys.append("ttadak_safe")
            if has("nt_ttadak_proven"):keys.append("granny_goodbye")
            if has("owl_hat") and child:keys.append("owl_hat")
        elif episode=="ep5":
            if has("soup_kids_dead"):keys.extend(("soup_empty","bori_shoe"))
            elif has("ws_some_alive") or has("dodam_dead"):keys.append("soup_three")
            elif has("ws_kids_alive"):
                keys.append("dodam_sick" if has("dodam_sick") else "soup_alive")
                if has("bori_adopts"):keys.append("bori_four")
            if has("portrait_finished_by_daram") and has("mom_reunited") and child:keys.append("mom_portrait")
        elif episode=="ep6":
            if has("neoul_gone"):keys.append("cart_unrest")
            elif has("cart_stopped"):
                keys.append("cart_safe" if has("cv_badook_safe") and not (has("badook_dead") or has("badook_hurt")) else "guldol_free")
            elif has("cv_family_only"):
                keys.append("cart_family")
                if has("ws_cart_truth") and not has("pandol_dead"):keys.append("pandol_family")
                keys.append("cart_left")
            elif has("cart_left"):keys.append("cart_skipped" if has("cv_skipped") else "cart_left")
            if has("badook_dead"):keys.append("badook_dead")
            elif has("badook_hurt"):keys.append("badook_hurt")
            if has("cv_granny_tomorrow"):keys.append("order_tomorrow")
        result=[]
        for key in keys:
            frame=dict(R13_AFTERMATH[key],id=key)
            # A farewell was witnessed, not undone; do not imply the missing child watched it.
            if key=="musoe_farewell" and not child:
                frame["caption"]="무쇠 할아버지는 솜이의 이름을 손바닥에 적어 두었다. 강가의 작별 뒤에도 그 이름이 남았다."
            if key=="chorong_dead" and not has("nt_lit_lamps"):
                frame["caption"]="초롱은 돌아오지 못했다. 그가 켜던 등과, 그를 기다리던 어머니가 남았다."
            result.append(frame)
        return result

    def r13_aftermath_actor(actor,height):
        person=actor["person"]
        profile=R13_DIALOGUE_TALK_ART["people"][person]["profiles"]["760"]
        frame=profile["frames"].get(actor.get("emotion","neutral"),profile["frames"]["neutral"])
        canvas=tuple(profile["canvas"])
        source=Fixed(Transform(frame["file"],xpos=frame["offset"][0],ypos=frame["offset"][1],nearest=False),xysize=canvas)
        return Transform(source,xysize=(int(canvas[0]*height/canvas[1]),height),nearest=False)

    def r13_aftermath_art(frame,wide=False):
        if "file" in frame:
            picture=frame["file"]
            if "rect" in frame:picture=Crop(tuple(frame["rect"]),picture)
            picture=Transform(picture,xysize=(1280,720),nearest=False)
        else:
            picture=r13_background(frame["background"])
            actors=frame.get("actors",[])
            layers=[picture,Solid("#101e2b22")]
            # Cast layers use approved source profiles, never regenerated faces.
            for i,actor in enumerate(actors):
                h=430 if actor["person"].startswith("kid_") else 530
                x=640+(i-(len(actors)-1)/2.0)*min(260,900.0/max(1,len(actors)))
                layers.append(Transform(r13_aftermath_actor(actor,h),xcenter=int(x),ypos=510-h))
            picture=Fixed(*layers,xysize=(1280,720))
        return Transform(picture,xysize=((1344,756) if wide else (1280,720)),nearest=False)

screen r13_episode_aftermath_view():
    style_prefix "r13"
    modal True
    zorder 150
    default ready=False
    timer .45 action SetScreenVariable("ready",True)
    $ frame=r13_aftermath_frames[r13_aftermath_index]
    $ count=len(r13_aftermath_frames)
    if persistent.room13_motion:
        add r13_aftermath_art(frame,True) at r13_ending_camera(1 if r13_aftermath_index%2==0 else -1)
    else:
        add r13_aftermath_art(frame)
    add Solid("#111b2240") ysize 52
    add r13_dialogue_frame() xpos 80 ypos 510 xsize 1120 ysize 112
    text ("후일담 · "+R13_AFTERMATH_TITLES[r13_aftermath_episode]) xpos 48 ypos 16 size 21 color "#f1dfb8"
    # Match dialogue click targets, including its bottom half, for touch and auto QA.
    button:
        area (0,52,1280,570) background None
        action Return("next") sensitive ready
        alt "다음 장면"
    fixed:
        if persistent.room13_motion:
            at r13_ending_caption_reveal
        frame:
            xpos 94 ypos 484 padding (14,5) background R13InkPanel()
            text frame["heading"] font r13_ui_font() size r13_read_size(18,22) color R13_SPEAKER_COLOR
        text frame["caption"] xpos 104 ypos 530 xsize 1072 size r13_read_size(23,29) font r13_ui_font() color r13_role_color("narration") line_spacing 5
    textbutton "‹ 이전":
        style "r13_action_button" area (76,630,144,82) text_size 21 text_yalign .5
        action Return("previous") sensitive ready and r13_aftermath_index>0
    text ("%02d / %02d"%(r13_aftermath_index+1,count)) xcenter 640 ypos 670 size 18 color "#f1dfb8" outlines [(1,"#211a16",0,1)]
    textbutton ("이야기로 돌아가기 ›" if r13_aftermath_index==count-1 else "다음 장면 ›"):
        style "r13_action_button" area (930,630,274,82) text_size 22 text_yalign .5
        action Return("next") sensitive ready
    if ready:
        key "K_RETURN" action Return("next")
        key "K_SPACE" action Return("next")
        key "K_RIGHT" action Return("next")
        if r13_aftermath_index>0:
            key "K_LEFT" action Return("previous")

label r13_episode_aftermath(episode):
    $ r13_aftermath_episode=episode
    $ r13_aftermath_frames=r13_episode_aftermath_frames(episode)
    $ r13_aftermath_index=0
    $ r13_aftermath_active=True
    $ r13_end_skip_modes()
    $ renpy.music.stop(channel="typing")
    while r13_aftermath_index<len(r13_aftermath_frames):
        call screen r13_episode_aftermath_view
        if _return=="previous":
            $ r13_aftermath_index=max(0,r13_aftermath_index-1)
        else:
            $ r13_aftermath_index+=1
    $ r13_aftermath_active=False
    return
