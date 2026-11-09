# Approved moonlit square cover; menu labels remain real keyboard/touch controls.
init 60 python:
    R13_TITLE_ART = json.load(renpy.file("assets/room13-title-layout.json"))
    renpy.register_shader("r13.title_portrait_fade",
        variables="varying vec2 v_tex_coord;",
        fragment_300="gl_FragColor *= 1.0 - smoothstep(0.82, 1.0, v_tex_coord.y);")
    renpy.register_shader("r13.title_menu_shade",
        variables="varying vec2 v_tex_coord;",
        fragment_300="""
            float across = 1.0 - smoothstep(0.5, 0.72, v_tex_coord.x);
            float below = smoothstep(0.75, 0.87, v_tex_coord.y);
            gl_FragColor *= across * below;
        """)

    def r13_title_menu_shade():
        return Transform(Solid("#0f1c449b"), xysize=(1280,720),
                         mesh=True, shader="r13.title_menu_shade")

    class R13TitleLink(renpy.Displayable):
        """메인 메뉴도 게임 안에서 쓰는 납품 B 버튼 상태를 공유한다."""
        def __init__(self,focused=False,disabled=False,primary=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused;self.disabled=disabled;self.primary=primary
            self.face=r13_supplied_button_surface(primary=primary,focused=focused,chosen=focused,disabled=disabled)
        def visit(self):
            return [self.face]
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            return renpy.render(Transform(self.face,xysize=(w,h)),w,h,st,at)

screen r13_cover_button(caption,key,icon,width,command,focus,enabled=True,first=False):
    $ state_icon=Transform(R13AntiqueIcon(icon,size=32) if icon in ("record","settings") else Crop((16,16,32,32),r13_field_icon(icon)),matrixcolor=(ColorizeMatrix("#c6a574","#fff0cd") if key=="new" else None))
    button:
        id ("r13_cover_"+key)
        style "empty"
        xysize (width,76) padding (0,0)
        background R13TitleLink(focused=focus==key,disabled=not enabled,primary=key=="new")
        hover_background R13TitleLink(focused=True,primary=key=="new")
        insensitive_background R13TitleLink(disabled=True,primary=key=="new")
        action command sensitive enabled default_focus first alt caption
        hovered SetScreenVariable("title_focus",key)
        activate_sound ("<volume 0.65>"+r13_asset_path("file:assets/diary-sounds/paper-selection.mp3"))
        hbox:
            align (.5,.5) spacing 20
            add state_icon alpha (1.0 if enabled else .42) yalign .5
            text caption:
                font R13_UI_FONT size r13_type("display") yalign .5
                color ("#8b8175" if not enabled else "#fff0cd" if key=="new" else "#493324") hover_color ("#fff4db" if key=="new" else "#793e2a")

# B 메인 전용 스타일. 이전 화면/저장 호환용 스타일.
init 81:
    style r13_title_button is r13_button:
        xsize 240 ysize 84
        background Transform(r13_asset_path("file:assets/ui-b-main/b_button.png"), xysize=(240,84))
        hover_background Transform(r13_asset_path("file:assets/ui-b-main/b_button_primary.png"), xysize=(240,84))
        selected_background Transform(r13_asset_path("file:assets/ui-b-main/b_button_primary.png"), xysize=(240,84))
        selected_hover_background Transform(r13_asset_path("file:assets/ui-b-main/b_button_primary.png"), xysize=(240,84))
        insensitive_background Transform(r13_asset_path("file:assets/ui-b-main/b_button.png"), xysize=(240,84), alpha=.55)
        focus_mask True
        # Transparent delivery margins must not overlap the next row/column.
        focus_rect (24,16,192,52)
        padding (24,14)
    style r13_title_button_text is r13_button_text:
        font R13_UI_FONT
        size r13_type("body")
        bold False
        color '#503a2c'
        hover_color '#fff5df'
        selected_color '#fff5df'
        insensitive_color '#948573'
        outlines []
        xalign .5 yalign .5 text_align .5
