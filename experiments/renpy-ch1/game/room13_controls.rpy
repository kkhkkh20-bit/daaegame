# Shared controls: composition, geometry and state treatment live here.
screen r13_control(caption,icon,command,enabled=True,chosen=False,primary=False,width=232,height=None,label_size=None,icon_size=None,control_id=None):
    $ ch=height or r13_control_height()
    button:
        id (control_id or ("r13_control_"+caption))
        xsize width ysize ch padding (16,8)
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
                color ("#a79c8c" if not enabled else "#f2d28d" if primary or chosen else "#fff4df")
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
