style default:
    font R13_UI_FONT
    size 25
    color "#f3e7ce"
    # Break Korean at spaces, never inside a word (비/켜).
    language "korean-with-spaces"
style button:
    background Solid("#30261fed")
    hover_background Solid("#65503d")
    insensitive_background Solid("#282421")
    padding (18,12)
style button_text:
    color "#f3e7ce"
    hover_color "#ffdc91"
    insensitive_color "#91877a"
    size 24
style frame:
    background Solid("#201b18ef")
    padding (24,20)
style say_dialogue:
    size 29
    line_spacing 9
style say_label:
    size 25
    bold True
style bar:
    left_bar Solid("#b39060")
    right_bar Solid("#4f4034")
    thumb Solid("#f5e8cf",xsize=14,ysize=30)
    thumb_shadow None
style slider is bar
style scrollbar:
    base_bar Solid("#4f4034")
    thumb Solid("#b39060",xsize=14,ysize=42)

# A vertical scrollbar without its own width can consume the complete Side,
# leaving the evidence viewport at zero width even though its rows exist.
style vscrollbar:
    xsize 10
    base_bar Solid("#4f4034")
    thumb Solid("#b39060",xsize=10,ysize=42)
    bar_vertical True

# One topic style shared by town residents and the investigation interviews.
screen topic_banner(caption, topic_action, done=False, enabled=True):
    button:
        xsize 560 ysize 58 padding (3,3)
        background Solid("#bca579") hover_background Solid("#f0d391")
        action topic_action
        sensitive enabled
        fixed:
            add Solid("#293c39" if done else "#385952")
            add Solid("#dfd2af",xsize=10)
            text (("{s}"+caption+"{/s}") if done else caption) size 23 xalign .5 yalign .5 color ("#bbcbd0" if done else "#fff4d9")
            if done:
                add TopicTick() xpos 514 yalign .5

screen main_menu():
    tag menu
    style_prefix "r13"
    $ title_continue = r13_continue_slot()
    $ title_has_save = bool(r13_save_slots())
    default title_focus = ("continue" if r13_continue_slot() else "new")
    # 승인된 B 메인 납품 좌표. 배경에 합쳐진 조명에는 구판 title light rig를 얹지 않는다.
    add Transform(r13_asset_path("file:assets/ui-b-main/b_main_background_postcard.png"), zoom=1280.0/1672)
    add Transform(r13_asset_path("file:assets/ui-b-main/b_logo.png"), zoom=.85) xpos -18 ypos 10
    # Approved single transparent ensemble sticker; preserve its original ratio.
    add Transform(r13_asset_path("file:assets/ui-b-main/b_main_cast_poster_plain.png"),zoom=610.0/1402) xpos 754 ypos 80
    fixed:
        at r13_title_menu_in
        hbox:
            xpos 44 ypos 616 spacing 14
            use r13_cover_button("이어하기","continue","acorn",184,(r13_load_action(title_continue) if title_continue is not None else NullAction()),title_focus,title_continue is not None,title_continue is not None)
            use r13_cover_button("처음부터","new","book",184,Start(),title_focus,True,title_continue is None)
            use r13_cover_button("불러오기","load","record",184,ShowMenu("load"),title_focus,title_has_save)
            use r13_cover_button("설정","settings","settings",184,ShowMenu("pause_menu"),title_focus)
    textbutton "음악 출처":
        xpos 44 ypos 696 padding (4,2) background None
        text_font R13_UI_FONT text_size (r13_type("small") if R13_TYPE_V2 else 14) text_color "#c5c6d2" text_hover_color "#fff0ce"
        action Show("r13_music_credits")
    text config.version xpos 1172 ypos 674 font r13_ui_font() size (r13_type("small") if R13_TYPE_V2 else 13) color "#b2b8b8"

# Two-line panels end 16px above the unchanged shared gameplay footer.
# Tops are expressed against the historical bottom=632 coordinate.
define R13_SAY_TOP_NORMAL = 528
define R13_SAY_TOP_LARGE = 520
init python:
    def _r13_say_size():
        return 31 if r13_touch_ui() else r13_read_size(28,31)

    def _r13_say_top(what=None):
        large=bool(persistent.room13_large_text) or r13_touch_ui()
        top=R13_SAY_TOP_LARGE if large else R13_SAY_TOP_NORMAL
        size=_r13_say_size()
        # r13_lines paginates two lines per click. Keep a safety expansion for
        # direct say / old-save notices outside that path; never crop their text.
        lines=_r13_say_lines(what,size,1028) if isinstance(what,str) else 1
        if lines>2:
            top-=(lines-2)*(size+7)
        if getattr(store,"r13_field_reading",False):return max(300,top+72)
        return max(300,top+r13_control_y()-16-632)

    import re as _r13_say_re
    def _r13_say_lines(what,size,width=756):
        """Rendered lines of a dialogue text: each written line wraps at the window width (Hangul
        and other wide glyphs count one em, Latin, digits and spaces half)."""
        per=width/float(size)
        total=0
        for line in _r13_say_re.sub(r"\{[^{}]*\}","",what).split("\n"):
            em=sum(1.0 if ord(ch)>0x2e7f else 0.55 for ch in line)
            total+=max(1,int(-(-em//per)))
        return total

screen say(who,what):
    if room13_mode:
        $ who = r13_speaker_label(who)
    # 0.19.97: the opening narration on black (room13_coach_cut.rpy) — white text, no panel.
    if room13_mode and r13_black_card:
        add Solid("#000")
        r13_dialogue_text what id "what" style "say_dialogue" xalign .5 yalign .46 xmaximum 980 text_align .5 layout "subtitle" size r13_read_size(26,30) line_spacing 8 font r13_ui_font() color "#e9e1d2"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        use r13_toolbar(mode="line")
    elif room13_mode and r13_meeting_active and r13_meeting_claim in R13_DEBATE and not r13_nw_meeting_claim(r13_meeting_claim):
        use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
        use r13_meeting_chrome(r13_meeting_claim)
        window:
            id "window"
            area (80,r13_control_y()-148,1120,132) background Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-dialogue/b_panel_dialogue.png")),48,24,64,24) padding (56,50,28,14)
            r13_dialogue_text what id "what" style "say_dialogue" size r13_read_size(23,29) line_spacing 5 xsize 1036 font R13_UI_BOLD_FONT color "#4b3420"
        if who:
            frame:
                xpos 104 ypos (r13_control_y()-158) padding (16,5,24,7)
                background Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6)
                text who id "who" size r13_read_size(24,26) color "#fff3df" font R13_UI_BOLD_FONT xmaximum 1000 outlines []
        text "▸" xpos 1160 ypos (r13_control_y()-48) size 24 color "#4b3420"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        if r13_nw_meeting_claim(r13_meeting_claim):
            use r13_toolbar(mode="line")
        else:
            use r13_meeting_tools(r13_meeting_claim,r13_meeting_live_target())
        key "K_h" action Show("r13_backlog")
    else:
        # Approved B notebook dialogue; retain existing controls and story state.
        key "K_h" action Show("r13_backlog")
        # 2026-10-27 소유자: 회의(오답 뒤) 상태로 돌아온 현장에서 규칙판을 읽어도 돌목·다람 무대가 떴다.
        # 현장 물건 설명(r13_field_reading)은 무대 없이 현장 그대로 읽는다.
        if r13_meeting_active and r13_nw_meeting_claim(r13_meeting_claim) and not r13_field_reading:
            use r13_meeting_stage(r13_meeting_claim,r13_meeting_focus_person(r13_meeting_claim),True)
            use r13_meeting_chrome(r13_meeting_claim)
        $ b_face = r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)) if who and r13_packet and not r13_thought_active and "r13_visitor" not in renpy.get_showing_tags() else None
        $ b_text_x = 222 if b_face else 120
        $ b_text_width = 988 if b_face else 1090
        $ b_text_top = r13_night_say_top(what)
        add Transform(Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-dialogue/b_panel_dialogue.png")),48,24,64,24),xysize=(1220,714-(b_text_top-38)),alpha=r13_night_shade_alpha()) xpos 30 ypos (b_text_top-38)
        if b_face:
            add Transform(b_face,xysize=(112,112)) xpos 70 ypos (b_text_top-10)
        window:
            id "window"
            xpos b_text_x ypos b_text_top xsize b_text_width yminimum 40
            background None padding (0,0)
            r13_dialogue_text what id "what" style "say_dialogue" size r13_night_say_size() line_spacing 4 xsize b_text_width font R13_UI_BOLD_FONT color r13_night_text_color() outlines []
        if who:
            $ r13_name_track(who)
            hbox:
                xpos b_text_x ypos (r13_night_say_top(what)-60) spacing 12
                # 2026-10-26 소유자: 이름표가 스르륵 생기면 이상하다. 화자가 바뀌면 바로 보인다(r13_name_fade 는 쓰지 않음).
                frame:
                    background Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6) padding (22,8,36,10) yalign .5
                    # 2026-10-27 타이포 시안(R13_TYPE_V2): 이름은 title, 화면 밖 목소리는 body. 꺼지면 이전 값 그대로.
                    text who id "who" color (r13_type_color("inverse") if R13_TYPE_V2 else "#fff3df") font R13_UI_BOLD_FONT size (r13_type("title") if R13_TYPE_V2 else r13_read_size(27,30)) xmaximum 640 outlines []
                if r13_offscreen_voice(who):
                    text r13_offscreen_voice(who) yalign .5 size (r13_type("body") if R13_TYPE_V2 else r13_read_size(20,22)) color (r13_type_color("inverse") if R13_TYPE_V2 else "#fff3df") font r13_ui_font() outlines [(1,"#30261f",0,0)]
        # Next-line mark at the end of the controls row (mockup: "더보기 ▸").
        if r13_fx_active():
            text "▸" xanchor 1.0 xpos R13_CONCEPT_RIGHT yanchor .5 ypos r13_night_control_y() size 22 color "#4b3420" at r13_next_glow
        else:
            text "▸" xanchor 1.0 xpos R13_CONCEPT_RIGHT yanchor .5 ypos r13_night_control_y() size 22 color "#4b3420"
        timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)
        if r13_field_reading:
            pass
        elif place != "마차 안" and not r13_cg_active:
            use r13_toolbar(mode="line")
        else:
            use r13_playback_footer()


screen choice(items):
    style_prefix "r13"
    modal True
    default choice_ready = False
    timer .35 action SetScreenVariable("choice_ready", True)
    # Talking with someone: the person stands on the left and the choices sit on
    # the right, like the question screen (owner, 0.18.6).
    default choice_visitor = room13_mode and "r13_visitor" in renpy.get_showing_tags()
    default choice_actor = (r13_motion_person if choice_visitor else (r13_last_partner if room13_mode and r13_last_partner in CAST else None))
    default choice_pose = (r13_directed_pose if choice_visitor and r13_directed_pose else r13_current_pose if choice_visitor else "interview_neutral") if room13_mode else "neutral"
    if room13_mode and r13_meeting_active:
        use r13_meeting_choices(items,choice_ready)
        if r13_nw_meeting_claim(r13_meeting_claim):
            use r13_toolbar(mode="line",ready=choice_ready)
    elif room13_mode:
        on "show" action Function(r13_choice_layout,choice_actor,choice_pose,True)
        on "hide" action Function(r13_choice_layout,choice_actor,choice_pose,False)
        # A menu caption (no action) is the question being asked: shown as a heading, never as
        # a numbered choice (0.18.41).
        $ choice_entries=[(item.caption,item.action,False) for item in items if item.action is not None]
        $ choice_caption=" ".join(item.caption for item in items if item.action is None)
        if len(choice_entries)==1:
            # 2026-10-27 소유자: "선택지 하나짜리 선택지창이 존재하면 안 되지". 조건 때문에 하나만 남은 메뉴
            # (13일 가족 제안은 조건을 묻기 전까지 「조건을 더 묻는다」뿐)는 고를 것이 없으므로 창을 띄우지 않고 그 길로 간다.
            timer .01 action choice_entries[0][1]
        else:
            use r13_question_list(choice_actor,choice_pose,"선택",choice_entries,choice_ready,caption=choice_caption,actor_x=272,list_left=(500 if choice_actor else 190),list_width=(744 if choice_actor else 940),animate=False)
            use r13_toolbar(mode="line",ready=choice_ready)


# Options: three tabs (소리 / 화면 / 게임), one page each, no scrolling,
# large touch targets in the game's own panel style (dark green, gold edge).
default persistent.room13_text_small = False
default persistent.room13_window_alpha = "d4"
default persistent.room13_option_tab = "sound"

init python:
    def r13_set_text_size(size):
        persistent.room13_text_small=(size=="small")
        persistent.room13_large_text=(size=="large")
        renpy.save_persistent()
        renpy.restart_interaction()

    def r13_text_size():
        return "large" if persistent.room13_large_text else "small" if persistent.room13_text_small else "normal"

    def r13_toggle_fullscreen():
        # Web only: Android browsers allow it; iOS Safari ignores the request.
        if renpy.emscripten:
            import emscripten
            emscripten.run_script("(function(){var d=document;if(d.fullscreenElement){d.exitFullscreen&&d.exitFullscreen();}else{var e=d.documentElement;(e.requestFullscreen||e.webkitRequestFullscreen||function(){}).call(e);}})();")
        else:
            renpy.run(Preference("display","toggle"))

# The same folio and left index as the records. Settings apply immediately.
init python:
    def r13_opt_size():
        # 2026-10-27 타이포 시안: 켜지면 설정 본문은 body 단계(단계표가 휴대폰 값을 따로 가진다).
        # 화면 줄은 r13_opt_size() 토큰만 쓰므로(dev/test_settings_type_scale.py) 여기서만 바꾼다.
        # 0.20.7 (UI review: phone text about 11px): +4 on a touch screen.
        if R13_TYPE_V2:return r13_type("body")
        return r13_read_size(22,26)+(4 if globals().get("r13_touch_ui",lambda:False)() else 0)

    def r13_opt_title_size():
        # 2026-10-27 타이포 시안: 설정 제목은 subtitle 단계.
        if R13_TYPE_V2:return r13_type("subtitle")
        return r13_read_size(30,34)

    def r13_opt_row_height():
        return max(96 if globals().get("r13_touch_ui",lambda:False)() else 76,112 if persistent.room13_large_text else 76)

style r13opt_text is text:
    font r13_ui_font() color "#4b3420" line_spacing 2
# Approved B options artwork; crops remove only the transparent delivery margin.
style r13opt_button is button:
    background r13_sticker_button() hover_background r13_sticker_button(focused=True)
    selected_background r13_sticker_button(primary=True)
    selected_hover_background r13_sticker_button(primary=True,focused=True)
    insensitive_background r13_sticker_button(disabled=True)
    selected_foreground None
    padding (10,4) ysize 52
style r13opt_button variant "touch":
    ysize 88
style r13opt_button_text is text:
    font R13_UI_BOLD_FONT color "#4b3420" hover_color "#4b3420" selected_color "#fff6e2" insensitive_color "#8f8778"
    xalign .5 yalign .5 text_align .5 line_spacing 2
style r13opt_bar is bar:
    ysize 36
    left_bar Frame(Crop((16,8,280,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_fill.png")),10,0)
    right_bar Frame(Crop((16,8,280,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_track.png")),10,0)
    thumb Crop((16,16,36,36),r13_asset_path("file:assets/ui-b-options/b_opt_bar_thumb.png")) thumb_offset 0
style r13opt_tab_button is button:
    background None hover_background None selected_background None padding (0,0)
style r13opt_tab_button_text is text:
    font R13_UI_BOLD_FONT color "#4b3420" hover_color "#4b3420" selected_color "#4b3420" xpos 62 yalign .5

style r13opt_footer_button is r13opt_button:
    padding (10,4)
style r13opt_footer_button_text is r13opt_button_text:
    hover_color "#4b3420"
style r13opt_close_button is r13opt_footer_button:
    background r13_sticker_button(primary=True)
    hover_background r13_sticker_button(primary=True,focused=True)
style r13opt_close_button_text is r13opt_footer_button_text:
    color "#fff6e2" hover_color "#fff6e2"

init -1 python:
    def r13_opt_marks():
        # The two small gold diamonds on a chosen option (mockup).
        d=r13_asset_path("file:assets/ui-night/diamond.png")
        return Fixed(Transform(d,xpos=8,yalign=.5),Transform(d,xalign=1.0,xoffset=-8,yalign=.5))

init python:
    # 2026-10-27 소유자: "옵션창 버튼 크기가 뒤죽박죽" -> "적용해". 폭을 줄마다 따로 적어 132~300px 아홉 가지가
    # 섞였다. 선택 버튼 한 칸 136, 단독 버튼 두 칸 284(136x2+12), 아래 줄 다섯은 206 을 218 간격으로 둔다.

    def r13_opt_button_height():
        # Match the rendered button in both native touch and short browser windows.
        return 88 if r13_touch_ui() else 52

screen r13_opt_row(label,description=""):
    fixed:
        xsize 844 ysize r13_opt_row_height()
        vbox:
            xpos 0 yalign .5 xsize 232 spacing 4
            text label font R13_UI_TYPE["button"]["font"] size (r13_opt_size()+2) color "#4b3420"
            if description:
                text description size (r13_opt_size()-4) color "#765b3e" xsize 232
        hbox:
            xpos 248 ypos ((r13_opt_row_height()-r13_opt_button_height())//2) spacing 12
            transclude
        add Solid("#c9a86a40") xpos 0 ypos (r13_opt_row_height()-1) xsize 844 ysize 1

    tag menu
    modal True
    zorder 50
    style_prefix "r13opt"
    default typing_preview = R13TypingPreview()
    default tab=(persistent.room13_option_tab if persistent.room13_option_tab in ("sound","screen","reading") else "reading")
    add Solid("#05070fa6")
    # Unscaled full panel: preserve the three rings and all border pixels.
    add r13_asset("file:assets/ui-b-options/b_opt_panel.png") xpos -4 ypos -4
    # Supplied diary stickers: uniform scales, decorative only, clear of controls.
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_gingham_tape.png"),zoom=120.0/464,rotate=-7) xpos 850 ypos 38
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_star.png"),zoom=44.0/368,rotate=10) xpos 1014 ypos 58
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_emphasis.png"),zoom=40.0/432,rotate=12) xpos 1070 ypos 72
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_acorn.png"),zoom=84.0/437,rotate=-9) xpos 116 ypos 410
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_letter.png"),zoom=64.0/408,rotate=8) xpos 216 ypos 406
    add Transform(r13_asset_path("file:assets/ui-b-options/daram_diary_sticker_magnifier.png"),zoom=64.0/422,rotate=-10) xpos 216 ypos 460
    # Keep the index clear of the unscaled binder rings.
    add Crop((16,16,150,44),r13_asset_path("file:assets/ui-b-options/b_opt_title_tape.png")) xpos 96 ypos 42
    text "설정" xpos 120 ypos 42 font R13_UI_BOLD_FONT size (r13_opt_title_size()+8) color "#4b3420"
    vbox:
        xpos 96 ypos 136 spacing 0
        for key,name in (("reading","읽기"),("sound","소리"),("screen","화면")):
            fixed:
                xsize 200 ysize (88 if r13_touch_ui() else 76)
                add Frame(Crop((16,16,206,62),r13_asset_path("file:assets/ui-b-options/b_opt_tab_selected.png") if tab==key else r13_asset_path("file:assets/ui-b-options/b_opt_tab.png")),32,20) xpos 0 yalign .5 xysize (200,62)
                add Crop((18,18,28,28),r13_asset_path("file:"+("assets/ui-b-options/b_icon_opt_%s.png"%key))) xpos 28 yalign .5
                textbutton name style "r13opt_tab_button":
                    xsize 200 ysize (88 if r13_touch_ui() else 76) text_size (r13_opt_title_size()-2)
                    text_style "r13opt_tab_button_text"
                    selected tab==key
                    action [SetScreenVariable("tab",key),SetField(persistent,"room13_option_tab",key),Function(renpy.save_persistent)]
    add Solid("#c9a86a66") xpos 305 ypos 56 xsize 1 ysize (472 if r13_touch_ui() else 496)
    text "변경한 설정은 바로 적용됩니다." xpos 347 ypos 52 size (r13_opt_size()-3) color "#765b3e"
    imagebutton:
        idle r13_asset("file:assets/ui-b-options/b_opt_close.png") hover Transform(r13_asset_path("file:assets/ui-b-options/b_opt_close.png"),matrixcolor=BrightnessMatrix(.15))
        xpos 1130 ypos 48 xysize (64,64) padding (0,0) action Return() alt "닫기"
    viewport:
        id "r13_settings_body"
        area (347,92,854,(436 if r13_touch_ui() else 460)) mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
        vbox:
            spacing 0
            if tab=="sound":
                use r13_opt_row("배경음", "음악의 크기"):
                    bar value Preference("music volume") style "r13opt_bar" xsize 280 ysize 36 yalign .5 id "music_volume"
                    text ("%d%%"%r13_mixer_percent("music")) id "music_volume_percent" size r13_opt_size() xsize 64 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("music") else "소리 켜짐"):
                        ysize r13_opt_button_height()
                        xsize 136 selected not _preferences.get_mute("music") action Preference("music mute","toggle") text_size r13_opt_size()
                use r13_opt_row("효과음", "문·버튼·조사 소리"):
                    bar value Preference("sound volume") style "r13opt_bar" xsize 280 ysize 36 yalign .5 id "fx_volume"
                    text ("%d%%"%r13_mixer_percent("sfx")) id "fx_volume_percent" size r13_opt_size() xsize 64 yalign .5
                    textbutton ("음소거 중" if _preferences.get_mute("sfx") else "소리 켜짐"):
                        ysize r13_opt_button_height()
                        xsize 136 selected not _preferences.get_mute("sfx") action Preference("sound mute","toggle") text_size r13_opt_size()
                use r13_opt_row("대사 타이핑 소리", "글자가 나타날 때 나는 소리"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize 136 selected persistent.room13_typing_sound==value action Function(r13_set_option,"room13_typing_sound",value) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("소리 확인", "효과음 음량을 적용해 재생"):
                    textbutton "효과음 듣기" xsize 284 action Function(r13_test_option_sound) text_size r13_opt_size() ysize r13_opt_button_height()
                    textbutton "음악 출처" xsize 284 action Show("r13_music_credits") text_size r13_opt_size() ysize r13_opt_button_height()
                null height 12
                text "음소거 중이거나 음량이 0%이면 소리가 나지 않습니다." xpos 248 size (r13_opt_size()-3) color "#765b3e"
            elif tab=="reading":
                use r13_opt_row("글자 크기", "대사와 메뉴에 함께 적용"):
                    for key,name in (("small","작게"),("normal","보통"),("large","크게")):
                        textbutton name id ("r13_text_size_"+key) xsize 136 selected r13_text_size()==key action Function(r13_set_text_size,key) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("대사 표시 속도", "글자가 나타나는 빠르기"):
                    for speed_title,speed_value in (("느리게",24),("보통",34),("빠르게",55),("즉시",0)):
                        textbutton speed_title id ("r13_text_speed_%d"%speed_value) xsize 136 action [Preference("text speed",speed_value),Function(typing_preview.restart)] selected _preferences.text_cps==speed_value text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("자동 넘김 대기", "다음 대사까지 대기"):
                    for value,name in ((0,"수동"),(5,"짧게"),(15,"보통"),(25,"길게")):
                        textbutton name xsize 136 action Preference("auto-forward time",value) selected (_preferences.afm_time==0 if value==0 else (0<_preferences.afm_time<10) if value==5 else (10<=_preferences.afm_time<20) if value==15 else _preferences.afm_time>=20) text_size r13_opt_size() ysize r13_opt_button_height()
                hbox:
                    spacing 12
                    textbutton "다시 보기" id "r13_preview_replay" xsize 284 text_size r13_opt_size() action Function(typing_preview.restart) ysize r13_opt_button_height()
                    frame:
                        xsize 548 ysize 88 padding (18,12) background r13_sticker_button()
                        add typing_preview
            else:
                null height 0
                frame:
                    xsize 824 ysize 76 padding (26,16) background Frame(Crop((16,16,860,110),r13_asset_path("file:assets/ui-b-options/b_opt_preview_box.png")),26,16)
                    text "대사창 미리보기 · 바꾼 진하기가 적용됩니다." font R13_UI_BOLD_FONT size r13_opt_size() color "#4b3420" xsize 772
                use r13_opt_row("대사창 진하기", "배경이 비쳐 보이는 정도"):
                    for value,name in (("99","연하게"),("d4","보통"),("f5","진하게")):
                        textbutton name xsize 136 selected persistent.room13_window_alpha==value action [SetField(persistent,"room13_window_alpha",value),Function(renpy.save_persistent)] text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("화면 움직임", "눈·불빛·인물의 짧은 반응"):
                    for value,name in ((True,"켜기"),(False,"끄기")):
                        textbutton name xsize 136 selected persistent.room13_motion==value action Function(r13_set_option,"room13_motion",value) text_size r13_opt_size() ysize r13_opt_button_height()
                use r13_opt_row("전체 화면", "지원 기기에서 전환"):
                    textbutton "전체 화면 전환" xsize 284 action Function(r13_toggle_fullscreen) text_size r13_opt_size() ysize r13_opt_button_height()
                # 0.18.50 (owner): test tool behind a PIN (systems/room13_admin.rpy).
                use r13_opt_row("관리자 도구", "핀 번호를 넣으면 켜짐"):
                    if persistent.room13_admin:
                        text "켜짐 · 마을 화면 위쪽 ‘관리자’" xsize 330 size r13_opt_size() color "#765b3e" yalign .5
                        textbutton "끄기" xsize 136 action Function(r13_admin_toggle) text_size r13_opt_size() ysize r13_opt_button_height()
                    else:
                        textbutton "핀 번호로 켜기" xsize 284 action Show("r13_admin_pin") text_size r13_opt_size() ysize r13_opt_button_height()
    text ("v"+config.version) xpos 120 ypos (516 if r13_touch_ui() else 540) size (r13_opt_size()-6) color "#8f8778"
    add Crop((16,16,1080,6),r13_asset_path("file:assets/ui-b-options/b_opt_divider.png")) xpos 112 ypos (536 if r13_touch_ui() else 560)
    textbutton "설정 초기화" style "r13opt_footer_button":
        ysize r13_opt_button_height()
        xpos 112 ypos (552 if r13_touch_ui() else 576) xsize 206 text_size r13_opt_size()
        action Confirm("읽기·소리·화면 설정을 기본값으로 돌릴까요? 게임 진행과 저장은 유지됩니다.",Function(r13_reset_options))
    if not main_menu:
        textbutton "메인화면" style "r13opt_footer_button":
            ysize r13_opt_button_height()
            xpos 330 ypos (552 if r13_touch_ui() else 576) xsize 206 text_size r13_opt_size()
            action Confirm("메인화면으로 돌아가시겠습니까?\n저장하지 않은 게임 진행은 사라집니다.",MainMenu(confirm=False))
    # 0.19.2: 단축키 안내는 「더보기」에서 설정 안으로 옮겼다.
    textbutton "단축키 PC" style "r13opt_footer_button":
        ysize r13_opt_button_height()
        xpos 548 ypos (552 if r13_touch_ui() else 576) xsize 206 text_size r13_opt_size() action Show("r13_shortcut_help")
    # 0.20.3 (owner 2026-10-22: "저장버튼이 어차피 빈번한 게임이 아니니 옵션에 넣어줘도 되고").
    if not main_menu:
        textbutton "저장 · 불러오기" style "r13opt_footer_button":
            ysize r13_opt_button_height()
            xpos 766 ypos (552 if r13_touch_ui() else 576) xsize 206 text_size r13_opt_size() action ShowMenu("save")  # 0.20.7: wider so it stays on one line on a phone
    textbutton "닫기" style "r13opt_close_button":
        ysize r13_opt_button_height()
        xpos 984 ypos (552 if r13_touch_ui() else 576) xsize 206 text_size r13_opt_size() action Return()
    key "game_menu" action Return()

screen save():
    tag menu
    zorder 50
    use file_slots("저장",True)

screen load():
    tag menu
    zorder 50
    use file_slots("불러오기",False)

init python:
    # Each save remembers where the story stood, shown on the slot instead of
    # only the real-world clock.
    def r13_save_json(d):
        try:
            if getattr(store,"room13_mode",False) and getattr(store,"room13",None):
                d["r13_where"]=r13_clock()+" · "+R13_PLACES[store.room13["location"]][0]
                # 0.18.46: which point of the story, and the last line shown, so a slot can be
                # told apart from the one saved just before a choice.
                d["r13_stage"]=r13_save_stage()
                d["r13_last"]=r13_save_last_line()
        except Exception:
            pass
    config.save_json_callbacks.append(r13_save_json)

    def r13_save_stage():
        s=store.room13 or {}
        if s.get("ending"):return "결말"
        if s.get("finale_started"):return "14일째 제단"
        goal=r13_campaign_goal() if s.get("day",1)>=2 else None
        return goal or ("재판 뒤" if s.get("trial_ended") else "")

    def r13_save_last_line(limit=34):
        for entry in reversed(getattr(store,"_history_list",[]) or []):
            what=getattr(entry,"what",None)
            if what:
                text=renpy.filter_text_tags(what,allow=[]).replace("\n"," ")
                who=getattr(entry,"who",None)
                text=(who+": "+text) if who else text
                return text if len(text)<=limit else text[:limit-1]+"…"
        return ""

    def r13_slot_info(slot,key):
        return (renpy.slot_json(slot) or {}).get(key,"")

    def r13_load_confirm(slot):
        """Same path for every slot, autosave included: a running game asks before losing progress."""
        load=r13_load_action(slot)
        if main_menu or r13_save_status(renpy.slot_json(slot))!="compatible":return load
        return Confirm("저장하지 않은 진행은 사라진다. 불러올까?",load)

    def r13_slot_where(slot):
        json=renpy.slot_json(slot)
        return (json or {}).get("r13_where","")

    def r13_slot_action(page,number,saving):
        slot="%s-%s"%(page,number)
        if saving:
            save=[FileSave(number,confirm=False,page=str(page)),Function(source_fx,"save")]
            return Confirm("이 칸에는 이미 저장이 있다. 덮어쓸까?",save) if renpy.can_load(slot) else save
        # Compatibility review (r13_load_action) decides how a save opens;
        # in a running game a compatible load also asks before losing progress.
        return r13_load_confirm(slot)

screen file_slots(title,saving):
    modal True
    style_prefix "r13"
    default page=persistent.r13_save_page or 1
    add Solid("#0b151bf2" if room13_mode or main_menu else "#110d0af5")
    frame:
        xpos 60 ypos 40 xsize 1160 ysize 640
        vbox:
            spacing 14
            hbox:
                spacing 24
                text title size (r13_type("title") if R13_TYPE_V2 else 34) color ("#765426" if room13_mode or main_menu else "#ffdc91") yalign .5
                for p in (1,2,3):
                    textbutton ("%d쪽"%p):
                        action [SetLocalVariable("page",p),SetField(persistent,"r13_save_page",p)]
                        selected page==p text_size (r13_type("body") if R13_TYPE_V2 else 21) padding (14,6)
                # 0.19.2: 「더보기 → 저장 · 불러오기」 하나로 들어와 여기서 바꾼다.
                if not main_menu:
                    textbutton ("불러오기로 ›" if saving else "저장으로 ›"):
                        action ShowMenu("load" if saving else "save") text_size (r13_type("body") if R13_TYPE_V2 else 21)
                if not saving:
                    textbutton "최근 자동저장":
                        action r13_load_confirm("auto-1")
                        sensitive FileLoadable(1,page="auto")
                        text_size (r13_type("body") if R13_TYPE_V2 else 21)
            grid 2 3:
                spacing 14
                for i in range(6):
                    $ slot="%d-%d"%(page,i+1)
                    button:
                        xsize 556 ysize 150 padding (10,10)
                        action r13_slot_action(page,i+1,saving)
                        sensitive (saving or renpy.can_load(slot))
                        hbox:
                            spacing 14
                            add FileScreenshot(i+1,page=str(page)) xsize 192 ysize 108 yalign .5
                            # 0.18.46: read the story point first (day, time, place), then where in
                            # the story and the last line; slot number and real time come last.
                            vbox:
                                spacing 3 yalign .5
                                if renpy.can_load(slot):
                                    text (r13_slot_where(slot) or "%d쪽 %d번"%(page,i+1)) size (r13_type("body") if R13_TYPE_V2 else r13_read_size(21,25)) color ("#765426" if room13_mode or main_menu else "#ffdc91") xsize 320
                                    if r13_slot_info(slot,"r13_stage"):
                                        text r13_slot_info(slot,"r13_stage") size (r13_type("small") if R13_TYPE_V2 else r13_read_size(17,21)) xsize 320
                                    if r13_slot_info(slot,"r13_last"):
                                        text ("“"+r13_slot_info(slot,"r13_last")+"”") size (r13_type("small") if R13_TYPE_V2 else r13_read_size(16,20)) color "#5d6a66" xsize 320
                                    text ("%d쪽 %d번 · "%(page,i+1)+FileTime(i+1,format="%m-%d %H:%M",page=str(page))+" · "+r13_save_caption(renpy.slot_json(slot))) size (r13_type("small") if R13_TYPE_V2 else r13_read_size(14,17)) color "#7d8c90" xsize 320
                                else:
                                    text ("%d쪽 %d번 · 비어 있음"%(page,i+1)) size (r13_type("body") if R13_TYPE_V2 else r13_read_size(20,24))
            hbox:
                spacing 18
                textbutton "돌아가기" action Return()
                if not saving:
                    textbutton "이전 저장 정리" action Show("r13_save_cleanup",scope="old") text_size (r13_type("body") if R13_TYPE_V2 else 20)
                    textbutton "모든 진행 저장 정리" action Show("r13_save_cleanup",scope="all") text_size (r13_type("body") if R13_TYPE_V2 else 20)

screen notify(message):
    style_prefix ("r13" if room13_mode else "")
    zorder 100
    if room13_mode:
        # One notice spot (0.18.33): top right under the date plate, like the new-record card.
        # The top-left corner holds the place tag; the top centre holds titles and the work button.
        frame:
            xanchor 1.0 xpos 1256 ypos 92 xmaximum 424 padding (18,12)
            background R13ActionPanel()
            text message size (r13_type("body") if R13_TYPE_V2 else 21) color (r13_type_color("inverse") if R13_TYPE_V2 else "#fff2d9") xmaximum 388
    else:
        frame:
            xalign 0.5 ypos 98
            text message size 21
    timer 2.2 action Hide("notify")

screen confirm(message,yes_action,no_action):
    style_prefix ("r13" if room13_mode else "")
    modal True
    zorder 100
    add Solid("#000000bb")
    frame:
        xalign 0.5 yalign 0.5 xsize 900
        vbox:
            spacing 20
            text message
            hbox:
                spacing 30
                textbutton "예" action yes_action
                textbutton "아니요" action no_action

