# Approved moonlit square cover; menu labels remain real keyboard/touch controls.
init 60 python:
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

init 81:
    style r13_title_button is r13_button:
        xsize 146 ysize 82
        background R13TitleLink()
        hover_background R13TitleLink(True)
        selected_background R13TitleLink(True)
        selected_hover_background R13TitleLink(True)
        insensitive_background R13TitleLink(disabled=True)
        padding (8,16,8,28)
    style r13_title_button_text is r13_button_text:
        font "assets/Room13TitleSerif.otf"
        size 23
        bold False
        color '#f2ead8'
        hover_color '#fff5dc'
        selected_color '#fff5dc'
        insensitive_color '#939bb1'
        outlines [(1,'#1c264c90',0,1)]
        xalign .5 yalign .5 text_align .5
