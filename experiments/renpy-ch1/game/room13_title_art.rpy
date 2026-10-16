# Title artwork is a clean plate. All labels and controls are real engine UI.
init 60 python:
    class R13TitleLink(renpy.Displayable):
        """Small cut-paper tabs designed for the illustrated winter title."""
        def __init__(self,focused=False,disabled=False,primary=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
            self.primary=primary
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h);c=out.canvas()
            def tab(inset,dy,color):
                x=inset;y=inset+dy;r=10
                c.polygon(color,[(x+r,y),(w-x-r,y),(w-x-3,y+4),(w-x,y+r),
                    (w-x,h-inset-r+dy),(w-x-4,h-inset-3+dy),(w-x-r,h-inset+dy),
                    (x+r,h-inset+dy),(x+3,h-inset-4+dy),(x,h-inset-r+dy),(x,y+r),(x+4,y+3)])
            tab(1,3,(14,20,29,100))
            tab(1,0,(88,54,43,255) if not self.primary else (192,151,100,255))
            face=(231,210,168,255) if not self.disabled else (158,160,154,235)
            if self.primary:face=(116,54,65,255)
            tab(3,-1,face)
            c.rect((255,240,203,70),(14,4,w-28,1))
            if self.focused:
                # Focus light belongs only below the paper, never above it.
                c.rect((228,183,112,140),(13,h-4,w-26,2))
                c.rect((255,221,165,220),(19,h-3,w-38,1))
            return out

    def r13_title_save_line(slot):
        if not slot:
            return '저장된 여정 없음'
        data=renpy.slot_json(slot) or {}
        day=data.get('r13_day')
        return ('%d일째 · 최근 저장' % day) if isinstance(day,int) else '최근 저장된 여정'

init 81:
    style r13_title_button is r13_button:
        xsize 286 ysize 50
        background R13TitleLink()
        hover_background R13TitleLink(True)
        selected_background R13TitleLink(True)
        selected_hover_background R13TitleLink(True)
        insensitive_background R13TitleLink(disabled=True)
        padding (24,9)
        xalign .5
    style r13_title_button_text is r13_button_text:
        font r13_ui_font()
        size 22
        bold False
        color '#4c362e'
        hover_color '#3b2725'
        selected_color '#3b2725'
        insensitive_color '#596063'
        outlines []
        xalign .5 yalign .5 text_align .5
    style r13_title_primary is r13_title_button:
        xsize 326 ysize 62
        background R13TitleLink(primary=True)
        hover_background R13TitleLink(True,primary=True)
        selected_background R13TitleLink(True,primary=True)
        selected_hover_background R13TitleLink(True,primary=True)
        padding (24,14)
    style r13_title_primary_text is r13_title_button_text:
        size 25
        color '#fff0d2'
        hover_color '#fff7e8'
        selected_color '#fff7e8'
