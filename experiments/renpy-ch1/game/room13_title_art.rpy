# A quiet, full-bleed winter title. Decoration is presentation-only.
init 60 python:
    class R13TitleVeil(renpy.Displayable):
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            for x in range(min(w,690)):
                u=max(0.0,1.0-x/690.0)
                c.rect((6,18,24,int(172*u*u)),(x,0,1,h))
            for y in range(max(0,h-105),h):
                c.rect((6,18,24,int(92*(y-(h-105))/105.0)),(0,y,w,1))
            return out

    class R13TitleSnow(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(1280,720)
            if not persistent.room13_motion:
                return out
            c=out.canvas()
            for i in range(28):
                x=int(((i*193+91)-st*(5+i%4))%1280)
                y=int(((i*113+27)+st*(10+i%6))%720)
                size=1+i%2
                c.rect((226,239,238,62 if x<510 else 112),(x,y,size,size))
            renpy.redraw(self,.1)
            return out

    class R13TitleLink(renpy.Displayable):
        def __init__(self,focused=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h);c=out.canvas()
            if self.focused:
                for x in range(w):
                    c.rect((205,177,111,int(27*(1.0-x/float(w)))),(x,0,1,h))
                c.polygon(R13_UI_COLORS["menu_accent"],[(3,h//2),(9,h//2-5),(15,h//2),(9,h//2+5)])
                c.line(R13_UI_COLORS["menu_accent"],(34,h-6),(min(w-18,192),h-6),1)
            return out

init 81:
    style r13_title_button is r13_button:
        xsize 356 ysize 58
        background R13TitleLink()
        hover_background R13TitleLink(True)
        insensitive_background None
        padding (34,7)
    style r13_title_button_text is r13_button_text:
        font r13_ui_font()
        size 33
        color R13_UI_COLORS["menu_text"]
        hover_color R13_UI_COLORS["menu_accent"]
        insensitive_color R13_UI_COLORS["menu_disabled"]
        outlines []
        xalign 0.0 text_align 0.0

    style r13_title_primary is r13_title_button:
        background R13TitleLink()
        hover_background R13TitleLink(True)
        insensitive_background None
    style r13_title_primary_text is r13_title_button_text:
        color R13_UI_COLORS["menu_accent"]
        hover_color R13_UI_COLORS["menu_accent"]
        size 33

    style r13_title_aux is r13_title_button:
        xsize 150 ysize 48 padding (8,10)
        hover_background R13TitleLink()
    style r13_title_aux_text is r13_title_button_text:
        size 20
        color R13_UI_COLORS["menu_secondary"]
        hover_color R13_UI_COLORS["menu_accent"]
