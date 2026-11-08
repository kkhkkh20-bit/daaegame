# 1부 회의의 제출·답변·실물 대조. 이야기 값과 정답 판정은 원래 proof 라벨이 소유한다.
init 322 python:
    R13_NW_FEEDBACK_MEETINGS=("gate","lamp","gate_post","fire")

    def r13_nw_knife_record_art(key):
        # 파편만 얻은 때에는 파편만 보인다. 칼 전체와의 관계는 실제 대조한 자료에만 있다.
        crop={"V111:E32":(1750,290,360,220),"V111:E33":(40,180,2100,370)}.get(key)
        return Crop(crop,"assets/room13-meeting-knife-tip-match.webp") if crop else None

    def r13_nw_line_beat(options,person,cue):
        explicit=options.get("beat")
        if explicit in R13_MEETING_BEATS:return explicit
        if cue and cue.get("remaining",0)>0:
            if not cue.get("accepted"):return "reversal"
            return "explain" if person in (None,"dad") else "reaction"
        return "listen"

    def r13_nw_direct_audio(beat):
        claim=getattr(store,"r13_meeting_claim",None)
        if r13_nw_meeting_key(claim) not in R13_NW_FEEDBACK_MEETINGS:return
        # 장소에서 재생하던 곡과 위치를 유지한다. 짧게 낮춘 볼륨은 다음 발언·회의 끝에 복구한다.
        saved=getattr(store,"r13_meeting_direction_return_audio",{}) or {}
        if not saved:
            saved={channel:dict(path=renpy.music.get_playing(channel=channel),
                volume=r13_meeting_channel_gain(channel),paused=renpy.music.get_pause(channel=channel))
                for channel in ("music","ambience")}
            store.r13_meeting_direction_return_audio=saved
        gain=R13_MEETING_BEATS.get(beat,R13_MEETING_BEATS["listen"])[1]
        renpy.music.set_volume(saved["music"]["volume"]*gain,delay=.14,channel="music")

default r13_nw_comparison = None

screen r13_nw_submit_accent(materials):
    zorder 96
    use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
    use r13_meeting_chrome(r13_meeting_claim)
    add Solid("#11182055")
    frame:
        area (120,270,1040,250) padding (24,20) background r13_field_paper()
        vbox:
            spacing 18
            text "자료 제시" font R13_UI_BOLD_FONT size r13_type("title") color r13_type_color("ink")
            hbox:
                spacing 12
                for material in materials[:4]:
                    vbox:
                        xsize 232 spacing 8
                        add Transform(r13_record_icon(material),xysize=(72,72),fit="contain",nearest=True) xalign .5
                        text r13_catalog_title(material) font R13_UI_BOLD_FONT size r13_type("small") color r13_type_color("ink") xsize 232 text_align .5 layout "subtitle"

screen r13_nw_knife_comparison():
    # 결합을 고른 뒤에만 보여 주는 실물 확대. 글과 버튼을 그림 안에 굽지 않는다.
    frame:
        area (110,120,1060,420) padding (24,20) background r13_field_paper()
        text "칼과 파편의 깨진 면" font R13_UI_BOLD_FONT size r13_type("title") color r13_type_color("ink")
        add Transform(Crop((40,180,2100,370),"assets/room13-meeting-knife-tip-match.webp"),xysize=(1000,176),fit="contain",nearest=True) pos (6,42)
        text "실룩이 내보인 칼" pos (12,216) font R13_UI_BOLD_FONT size r13_type("small") color r13_type_color("muted")
        text "안쪽 틈에서 꺼낸 파편" pos (650,216) xsize 350 text_align 1.0 font R13_UI_BOLD_FONT size r13_type("small") color r13_type_color("muted")
        add Solid("#c9a86a88") pos (12,250) xysize (984,2)
        add Transform(Crop((1630,290,270,220),"assets/room13-meeting-knife-tip-match.webp"),xysize=(230,120),fit="contain",nearest=True) pos (20,260)
        vbox:
            pos (300,274) spacing 10 xsize 670
            text "맞닿은 단면 확대" font R13_UI_BOLD_FONT size r13_type("body") color r13_type_color("ink")
            text "깨진 면과 칼날을 갈아 낸 선을 함께 본다." font R13_UI_FONT size r13_type("body") color r13_type_color("ink") xsize 670

label r13_nw_proof_feedback(key,accepted):
    # 입구는 조사 대기에서 바로 자료창을 연다. 그 경로도 제출 뒤에는 실제 회의 무대를 쓴다.
    if not r13_meeting_active and r13_nw_pending in R13_NW_FEEDBACK_MEETINGS:
        $ r13_nw_stage_begin(r13_nw_pending)
    if not r13_meeting_active or r13_nw_meeting_key(r13_meeting_claim) not in R13_NW_FEEDBACK_MEETINGS:
        return
    $ r13_nw_submission_serial+=1
    $ r13_nw_submit_cue=dict(key=key,accepted=accepted,remaining=2)
    if not renpy.is_skipping() and not r13_fast_all:
        $ r13_nw_direct_audio("select")
        show screen r13_nw_submit_accent(tuple(room13["arguments"].get(v111_claim,())))
        $ renpy.pause(.48 if persistent.room13_motion else .24)
        hide screen r13_nw_submit_accent
    return
