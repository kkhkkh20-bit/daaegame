# Approved moonlit square cover; menu labels remain real keyboard/touch controls.
init 60 python:
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
        """Quiet underline, with warm focus light confined below the label."""
        def __init__(self,focused=False,disabled=False,primary=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h);c=out.canvas()
            y=h-20;mid=w//2
            if self.focused and not self.disabled:
                for spread,alpha in ((5,12),(3,22),(1,40)):
                    c.rect((255,196,109,alpha),(23,y-spread,w-46,2*spread+2))
                color=(255,210,132,255)
            else:
                color=(173,182,205,125 if not self.disabled else 55)
            c.rect(color,(23,y,mid-30,1))
            c.rect(color,(mid+7,y,w-mid-30,1))
            for dx,dy in ((0,-3),(-3,0),(3,0),(0,3)):
                x=mid+dx;yy=y+dy
                c.polygon(color,[(x,yy-2),(x+2,yy),(x,yy+2),(x-2,yy)])
            return out

screen r13_cover_button(caption,key,icon,width,command,focus,enabled=True,first=False):
    $ state_icon=Transform(Crop((16,16,32,32),r13_field_icon(icon)),zoom=30.0/32,alpha=1.0 if enabled else .45)
    use r13_state_button(caption,command,width,76,family="primary" if focus==key and enabled else "standard",enabled=enabled,icon=state_icon,text_size=28,control_id="r13_cover_"+key,first=first,hover_action=SetScreenVariable("title_focus",key))

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
        size 25
        bold False
        color '#503a2c'
        hover_color '#fff5df'
        selected_color '#fff5df'
        insensitive_color '#948573'
        outlines []
        xalign .5 yalign .5 text_align .5
