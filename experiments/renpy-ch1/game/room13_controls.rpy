# Shared controls: composition, geometry and state treatment live here.
init 110 python:
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
                text message size r13_read_size(26,28) xsize 880 color "#493b30"
                hbox:
                    spacing 25
                    textbutton yes:
                        id "r13_confirm_yes"
                        style "r13_confirm_button"
                        yminimum r13_control_height() text_size r13_read_size(25,28)
                        action Return(True) sensitive ready
                    textbutton no:
                        id "r13_confirm_no"
                        style "r13_confirm_button"
                        yminimum r13_control_height() text_size r13_read_size(25,28)
                        action Return(False) sensitive ready
        add R13ConfirmSeal() xpos 912 ypos -20

init 111:
    style r13_confirm_button is r13_button:
        background R13PaperFrame()
        hover_background Transform(R13PaperFrame(),matrixcolor=BrightnessMatrix(.05))
        insensitive_background R13PaperFrame()
        padding (18,12)
        xmaximum 430
    style r13_confirm_button_text is r13_button_text:
        size 25

screen r13_control(caption,icon,command,enabled=True,chosen=False,primary=False,width=None,height=None,label_size=None,icon_size=None,control_id=None):
    $ ch=height or r13_control_height()
    $ cw=width or R13_CONTROL["width"]
    button:
        id (control_id or ("r13_control_"+caption))
        xsize cw ysize ch padding (R13_CONTROL["padding"],8)
        background R13ControlSurface(primary=primary,chosen=chosen)
        hover_background R13ControlSurface(primary=primary,chosen=chosen,hovered=True)
        selected_background R13ControlSurface(primary=primary,chosen=True)
        insensitive_background R13ControlSurface(disabled=True)
        action command sensitive enabled selected chosen alt (caption or "메뉴")
        hbox:
            align (.5,.5) spacing R13_CONTROL["icon_gap"]
            if icon:
                add R13AntiqueIcon(icon,size=icon_size or R13_CONTROL["icon"]) yalign .5 alpha (1.0 if enabled else .5)
            text caption:
                font r13_ui_font() size (label_size or r13_read_size(R13_CONTROL["text"],R13_CONTROL["large_text"]))
                color ("#a79c8c" if not enabled else "#fff4df" if primary else "#f2d28d" if chosen else "#fff4df")
                yalign .5

screen r13_footer_control(column,caption,icon,command,enabled=True,chosen=False,primary=False):
    fixed:
        area (r13_control_x(column),r13_control_y(),R13_CONTROL["width"],r13_control_height())
        use r13_control(caption,icon,command,enabled,chosen,primary)

# Real-engine specimen, for inspecting all common states together.
screen r13_control_specimen():
    modal True
    add Solid("#221e1b")
    text "다람탐정 · 공통 UI" pos (28,28) size 32 color "#f2d28d" font r13_ui_font()
    text "같은 재질 · 같은 높이 · 같은 중심선" pos (28,80) size 23 color "#fff4df" font r13_ui_font()
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
            text "대사 · 안내 패널" size 26 color "#f2d28d" font r13_ui_font()
            text "버튼과 안내를 구별하고,\n아이콘과 글씨는 같은 중심에 놓습니다." size 23 color "#fff4df" font r13_ui_font()
    frame:
        area (644,280,608,180) padding (24,20) background R13PaperFrame()
        vbox:
            spacing 16
            text "기록 · 발언 카드" size 26 color "#493b30" font r13_ui_font()
            text "읽는 내용은 종이 위에,\n누르는 행동은 공통 버튼으로 표시합니다." size 23 color "#493b30" font r13_ui_font()
    for col,(caption,icon) in enumerate([("더보기","settings"),("발언 선택","testimony"),("되묻기","dialogue"),("자료 보여주기","present"),("기록","record")]):
        use r13_footer_control(col,caption,icon,NullAction(),primary=col==3)
    key "game_menu" action Hide("r13_control_specimen")
