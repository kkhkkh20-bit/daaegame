# Shared controls: composition, geometry and state treatment live here.
init 110 python:
    # 자료를 읽고 돌아가는 보조 행동도 질문지와 같은 가는 갈색 종이 판을 쓴다.
    # 명시한 자료창 ID만 적용해 현장·메뉴·선택 탭의 기존 표현은 보존한다.
    R13_SOFT_SUPPORT_CONTROLS=frozenset((
        "r13_pw_prev","r13_pw_next","r13_pw_back_list","r13_pw_investigate",
        "r13_pw_observe","r13_pw_press","r13_pw_origin","r13_pw_fold",
        "r13_pw_enlarge","r13_pw_swap_cancel",
        "r13_fire_site","r13_fire_words","r13_fire_investigate",
        "r13_fire_sources","r13_fire_materials","r13_fire_back",
        "r13_fire_sources_change","r13_fire_clear","r13_fire_prev",
        "r13_fire_next","r13_fire_origin","r13_fire_press",
        "r13_fire_recheck_picture",
    ))

    def r13_control_soft_support(control_id,primary=False):
        # 제출은 같은 ID를 재사용하더라도 주 행동의 빨강을 유지한다.
        return not primary and control_id in R13_SOFT_SUPPORT_CONTROLS

    class R13ConfirmPaper(renpy.Displayable):
        """Approved confirmation card: existing paper rim over a shallow shadow."""
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h)
            r.canvas().rect("#251e1748",(5,6,max(1,w-5),max(1,h-6)))
            r.blit(renpy.render(R13PaperFrame(),max(1,w-5),max(1,h-6),st,at),(0,0))
            return r

    class R13ConfirmSeal(renpy.Displayable):
        """Small raised rim around the same day/night dial used by the date card."""
        def render(self,width,height,st,at):
            r=renpy.Render(58,60);c=r.canvas()
            c.circle("#251e1760",(30,32),27)
            c.circle("#806249",(28,28),27)
            c.circle("#f4dfac",(28,27),25)
            c.circle("#bea077",(28,29),23)
            r.blit(renpy.render(R13TimeDial(),40,40,st,at),(8,8))
            return r

screen r13_confirmation_card(message,yes,no,ready):
    fixed:
        align (.5,.5) fit_first True
        frame:
            id "r13_confirm_card"
            xsize 950 padding (32,32) background R13ConfirmPaper()
            vbox:
                spacing 25
                text message size r13_type("emphasis") xsize 880 color "#493b30"
                hbox:
                    spacing 25
                    textbutton yes:
                        id "r13_confirm_yes"
                        style "r13_confirm_button"
                        yminimum r13_control_height() text_size r13_type("body")
                        action Return(True) sensitive ready
                    textbutton no:
                        id "r13_confirm_no"
                        style "r13_confirm_button"
                        yminimum r13_control_height() text_size r13_type("body")
                        action Return(False) sensitive ready
        add R13ConfirmSeal() xpos 912 ypos -20

init 111:
    style r13_confirm_button is r13_button:
        background R13ControlSurface()
        hover_background R13ControlSurface(hovered=True)
        insensitive_background R13ControlSurface(disabled=True)
        padding (18,12)
        xsize 427
        xmaximum 427
    style r13_confirm_button_text is r13_button_text:
        font R13_UI_BOLD_FONT
        color "#493323"
        size r13_type("body")

screen r13_control(caption,icon,command,enabled=True,chosen=False,primary=False,width=None,height=None,label_size=None,icon_size=None,control_id=None):
    $ ch=height or r13_control_height()
    $ cw=width or R13_CONTROL["width"]
    $ soft_support=r13_control_soft_support(control_id,primary)
    button:
        id (control_id or ("r13_control_"+caption))
        xsize cw ysize ch padding (R13_CONTROL["padding"],8)
        background (R13SoftButtonSurface(chosen=chosen) if soft_support else R13ControlSurface(primary=primary,chosen=chosen))
        hover_background (R13SoftButtonSurface(chosen=chosen,hovered=True) if soft_support else R13ControlSurface(primary=primary,chosen=chosen,hovered=True))
        selected_background (R13SoftButtonSurface(chosen=True) if soft_support else R13ControlSurface(primary=primary,chosen=True))
        insensitive_background (R13SoftButtonSurface(disabled=True) if soft_support else R13ControlSurface(disabled=True))
        action command sensitive enabled selected chosen alt (caption or "메뉴")
        hbox:
            align (.5,.5) spacing R13_CONTROL["icon_gap"]
            if icon in R13_SUPPLIED_UI_ICONS:
                add R13AntiqueIcon(icon,size=icon_size or R13_CONTROL["icon"]) yalign .5 alpha (1.0 if enabled else .5)
            text caption:
                font R13_UI_BOLD_FONT size (label_size or r13_read_size(R13_CONTROL["text"],R13_CONTROL["large_text"]))
                color (("#8b8175" if not enabled else "#4b3420") if soft_support else "#978572" if not enabled else "#fff7e8" if primary or chosen else "#493323")
                hover_color ("#4b3420" if soft_support else "#fff7e8" if primary or chosen else "#793e2a")
                yalign .5

screen r13_footer_control(column,caption,icon,command,enabled=True,chosen=False,primary=False):
    fixed:
        area (r13_control_x(column),r13_control_y(),R13_CONTROL["width"],r13_control_height())
        use r13_control(caption,icon,command,enabled,chosen,primary)

# Real-engine specimen, for inspecting all common states together.
screen r13_control_specimen():
    modal True
    add Solid("#221e1b")
    text "다람탐정 · 공통 UI" pos (28,28) size r13_type("title") color "#f2d28d" font r13_ui_font()
    text "같은 재질 · 같은 높이 · 같은 중심선" pos (28,80) size r13_type("small") color "#fff4df" font r13_ui_font()
    for col,(caption,icon,enabled,chosen,primary) in enumerate([
        ("기본 행동","investigate",True,False,False),
        ("선택한 항목","dialogue",True,True,False),
        ("자료 보여주기","present",True,False,True),
        ("비활성","record",False,False,False),
        ("기록","record",True,False,False)]):
        fixed:
            area (r13_control_x(col),150,232,r13_control_height())
            use r13_control(caption,icon,NullAction(),enabled,chosen,primary)
    frame:
        area (28,280,592,180) padding (24,20) background R13InkPanel(alpha="e6",slim=True)
        vbox:
            spacing 16
            text "대사 · 안내 패널" size r13_type("emphasis") color "#f2d28d" font r13_ui_font()
            text "버튼과 안내를 구별하고,\n아이콘과 글씨는 같은 중심에 놓습니다." size r13_type("small") color "#fff4df" font r13_ui_font()
    frame:
        area (644,280,608,180) padding (24,20) background R13PaperFrame()
        vbox:
            spacing 16
            text "기록 · 발언 카드" size r13_type("emphasis") color "#493b30" font r13_ui_font()
            text "읽는 내용은 종이 위에,\n누르는 행동은 공통 버튼으로 표시합니다." size r13_type("small") color "#493b30" font r13_ui_font()
    for col,(caption,icon) in enumerate([("더보기","settings"),("발언 선택","testimony"),("되묻기","dialogue"),("자료 보여주기","present"),("기록","record")]):
        use r13_footer_control(col,caption,icon,NullAction(),primary=col==3)
    key "game_menu" action Hide("r13_control_specimen")
