# Four read-only epilogue scenes per ending. The father remains the camera.
default r13_ending_story_active = False
default r13_ending_story_index = 0

init 58 python:
    import json as r13_ending_json
    import functools as r13_ending_functools
    with renpy.file("assets/room13-ending-stories.json") as r13_ending_file:
        R13_ENDING_STORIES=r13_ending_json.load(r13_ending_file)["endings"]

    def r13_ending_story_frame(key,index):
        frame=dict(R13_ENDING_STORIES[key][index])
        if key=="E4" and index==1:
            if not r13_has("supplies_ready"):
                frame["caption"]="수첩에 적힌 곡물로는 배를 채울 수 없었다. 학교로 옮기지 못한 장작도 불이 되지 못했다."
            elif not r13_has("patient_transport"):
                frame["caption"]="물자는 모았지만, 스스로 걷지 못하는 사람을 옮길 손이 모자랐다. 빈집들을 다시 돌아야 했다."
            else:
                frame["caption"]="모아 둔 물자는 있었다. 그래도 준비한 일을 모두가 함께 실행하는 데까지 이르지는 못했다."
        if key=="E4" and index==2 and "F1" not in room13.get("propositions",[]):
            frame["caption"]="회복을 뒷받침할 기록은 끝내 인정받지 못했다. 환자들의 자리를 지키는 일도 아직 남아 있었다."
        if key=="E5" and index==2:
            if room13.get("victim_state")=="dead":
                frame["caption"]="새로운 일을 시작해도 잃은 사람은 돌아오지 않았다. 그날의 기록과 책임은 함께 남겼다."
            else:
                frame["caption"]="막아 낸 일과 아직 밝혀야 할 일은 따로 남았다. 살아 돌아왔다고 잘못까지 지워지지는 않았다."
        return frame

    def r13_ending_story_art(key,index,wide=False):
        frame=R13_ENDING_STORIES[key][index]
        return Transform(Crop(tuple(frame["rect"]),frame["file"]),xysize=((1344,756) if wide else (1280,720)),nearest=True)

    def r13_ending_camera_tick(trans,st,at,direction=1):
        u=min(1.0,max(0.0,st/10.0));ease=u*u*(3-2*u)
        trans.xoffset=int(round(-32+direction*18*(2*ease-1)))
        trans.yoffset=int(round(-18+4*(2*ease-1)))
        return .033 if u<1 else None

transform r13_ending_camera(direction=1):
    subpixel False
    nearest True
    function r13_ending_functools.partial(r13_ending_camera_tick,direction=direction)

transform r13_ending_caption_reveal:
    alpha 0.0
    linear .4 alpha 1.0

screen r13_ending_story_view(key,index):
    style_prefix "r13"
    modal True
    zorder 150
    default ready=False
    timer .45 action SetScreenVariable("ready",True)
    $ frame=r13_ending_story_frame(key,index)
    if persistent.room13_motion:
        add r13_ending_story_art(key,index,True) at r13_ending_camera(1 if index%2==0 else -1)
    else:
        add r13_ending_story_art(key,index)
    add Solid("#111b2240") ysize 52
    add Solid("#111b2220") ypos 482 ysize 20
    add Solid("#111b2240") ypos 502 ysize 20
    add Solid("#111b2270") ypos 522 ysize 20
    add Solid("#111b22d9") ypos 542 ysize 178
    text R13_ENDINGS[key]["title"] xpos 48 ypos 16 size 21 color "#f1dfb8"
    button:
        area (0,52,1280,450) background None
        action Return("next") sensitive ready
        alt "다음 장면"
    fixed:
        if persistent.room13_motion:
            at r13_ending_caption_reveal
        text frame["heading"] xpos 76 ypos 548 size r13_read_size(21,24) color "#dfbd7e"
        text frame["caption"] xpos 76 ypos 581 xsize 1128 size r13_read_size(25,29) color "#fff0d0" line_spacing 4
    textbutton "‹ 이전":
        style "r13_action_button" area (76,654,144,52) text_size 21
        action Return("previous") sensitive ready and index>0
    text ("%02d / 04"%(index+1)) xcenter 640 ypos 670 size 18 color "#d4cbb7"
    textbutton ("여정의 기록 ›" if index==3 else "다음 장면 ›"):
        style "r13_action_button" area (984,654,220,52) text_size 22
        action Return("next") sensitive ready
    if ready:
        key "K_RETURN" action Return("next")
        key "K_SPACE" action Return("next")
        key "K_RIGHT" action Return("next")
        if index>0:
            key "K_LEFT" action Return("previous")

label r13_ending_story(key):
    $ r13_ending_story_active=True
    $ r13_ending_story_index=0
    $ r13_fast_read=False
    $ r13_fast_all=False
    $ renpy.config.skipping=None
    $ renpy.music.stop(channel="typing")
    $ renpy.music.stop(channel="scene_fx",fadeout=.3)
    $ renpy.music.stop(channel="ambience",fadeout=1.0)
    $ renpy.music.play(R13_BGM["ending"],fadeout=1.2,fadein=1.4,if_changed=True)
    while r13_ending_story_index<4:
        if persistent.room13_motion:
            scene expression r13_ending_story_art(key,r13_ending_story_index) with Dissolve(.6)
        else:
            scene expression r13_ending_story_art(key,r13_ending_story_index)
        call screen r13_ending_story_view(key,r13_ending_story_index)
        if _return=="previous":
            $ r13_ending_story_index=max(0,r13_ending_story_index-1)
        else:
            $ r13_ending_story_index+=1
    $ r13_ending_story_index=3
    $ r13_ending_story_active=False
    return
