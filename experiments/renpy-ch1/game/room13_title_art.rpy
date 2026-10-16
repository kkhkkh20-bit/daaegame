# Title artwork is a clean plate. All labels and controls are real engine UI.
init 60 python:
    class R13TitleVeil(renpy.Displayable):
        """Book-cover shadows: keep the inn lights visible on the right."""
        def render(self,width,height,st,at):
            w,h=1280,720
            out=renpy.Render(w,h); c=out.canvas()
            for x in range(0,920,2):
                u=max(0.0,1.0-x/920.0)
                c.rect((9,12,23,int(205*u*u)),(x,0,2,h))
            for y in range(0,110,2):
                a=int(108*(1.0-y/110.0)**2)
                c.rect((8,10,18,a),(0,y,w,2))
                c.rect((8,10,18,a),(0,h-y-2,w,2))
            # Fine, quiet book-cover rules. No paper grain or random scratches.
            edge=(185,159,111,85); inner=(185,159,111,30)
            c.rect(edge,(36,32,1208,1)); c.rect(edge,(36,687,1208,1))
            c.rect(inner,(40,36,1200,1)); c.rect(inner,(40,683,1200,1))
            for x in (36,1243):
                c.rect(edge,(x,32,1,55)); c.rect(edge,(x,633,1,55))
            for x in (54,1226):
                c.polygon((190,163,116,140),[(x,28),(x+4,32),(x,36),(x-4,32)])
                c.polygon((190,163,116,140),[(x,683),(x+4,687),(x,691),(x-4,687)])
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
        def __init__(self,focused=False,disabled=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h);c=out.canvas()
            c.polygon((26,20,24,220 if self.focused else 135),[(0,0),(w-8,0),(w,8),(w,h),(0,h)])
            c.rect((181,151,105,25 if self.disabled else 65),(0,h-1,w,1))
            if self.focused:
                # The warm selection light sits underneath the button only.
                c.rect((149,100,49,75),(0,h-5,w,4))
                c.rect((222,186,120,220),(0,h-2,w,2))
                c.polygon((221,185,123,255),[(17,h//2),(21,h//2-4),(25,h//2),(21,h//2+4)])
            return out

    def r13_title_save_line(slot):
        if not slot:
            return '저장된 여정 없음'
        data=renpy.slot_json(slot) or {}
        day=data.get('r13_day')
        return ('%d일째 · 최근 저장' % day) if isinstance(day,int) else '최근 저장된 여정'

init 81:
    style r13_title_button is r13_button:
        xsize 320 ysize 50
        background R13TitleLink()
        hover_background R13TitleLink(True)
        selected_background R13TitleLink(True)
        selected_hover_background R13TitleLink(True)
        insensitive_background R13TitleLink(disabled=True)
        padding (38,10)
    style r13_title_button_text is r13_button_text:
        font r13_ui_font()
        size 22
        bold False
        color '#f4e7c4'
        hover_color '#f6dfac'
        selected_color '#f6dfac'
        insensitive_color '#8d8276'
        outlines []
        xalign .0 yalign .5 text_align .0

    style r13_title_aux is r13_title_button:
        xsize 116 ysize 44 padding (8,10)
        hover_background None
        selected_background None
        selected_hover_background None
    style r13_title_aux_text is r13_title_button_text:
        size 18
        color '#c2c9b5'
        hover_color '#f6dfac'
