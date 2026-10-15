# Title artwork is a clean plate. All labels and controls are real engine UI.
init 60 python:
    class R13TitleVeil(renpy.Displayable):
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            # The plate already has a dark left wall; avoid a second opaque panel.
            for x in range(min(w,480)):
                u=max(0.0,1.0-x/480.0)
                c.rect((6,18,24,int(38*u*u)),(x,0,1,h))
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
                c.rect((226,239,238,42 if x<430 else 105),(x,y,size,size))
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
                out.blit(renpy.render(R13StonePanel(focused=True),w,h,st,at),(0,0))
                c.polygon('#e5ddbf',[(20,h//2),(26,h//2-6),(32,h//2),(26,h//2+6)])
            return out

    def r13_title_save_line(slot):
        if not slot:
            return '저장된 여정 없음'
        data=renpy.slot_json(slot) or {}
        day=data.get('r13_day')
        return ('%d일째 · 최근 저장' % day) if isinstance(day,int) else '최근 저장된 여정'

init 81:
    style r13_title_button is r13_button:
        xsize 264 ysize 54
        background R13TitleLink()
        hover_background R13TitleLink(True)
        selected_background R13TitleLink(True)
        selected_hover_background R13TitleLink(True)
        insensitive_background None
        padding (48,10,12,10)
    style r13_title_button_text is r13_button_text:
        font r13_ui_font()
        size 28
        bold False
        color '#f4e7c4'
        hover_color '#f6dfac'
        selected_color '#f6dfac'
        insensitive_color '#939e99'
        outlines []
        xalign 0.0 yalign .5 text_align 0.0

    style r13_title_aux is r13_title_button:
        xsize 116 ysize 44 padding (8,10)
        hover_background None
        selected_background None
        selected_hover_background None
    style r13_title_aux_text is r13_title_button_text:
        size 18
        color '#c2c9b5'
        hover_color '#f6dfac'
