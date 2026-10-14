# Quiet paper, ink and brass. Material planes deliberately have no grain/noise.
init 58 python:
    class R13PaperPanel(renpy.Displayable):
        def __init__(self, focused=False, dark=False, **kwargs):
            super(R13PaperPanel,self).__init__(**kwargs)
            self.focused=focused
            self.dark=dark
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            c.rect('#161e2138',(3,4,max(1,w-3),max(1,h-4)))
            points=[(0,0),(w-1,0),(w-1,h-1),(0,h-1)]
            fill=('#203439' if self.dark else '#fff4dd' if self.focused else '#f1eadb')
            c.polygon(fill,points)
            c.lines('#dfbc76' if self.focused else '#8b8069',True,points,2 if self.focused else 1)
            return out

    class R13ActionPanel(renpy.Displayable):
        def __init__(self,focused=False,disabled=False,**kwargs):
            super(R13ActionPanel,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            fill='#263238' if self.disabled else '#3b5541' if self.focused else '#172e2c'
            edge='#657475' if self.disabled else '#edcc88' if self.focused else '#b69762'
            # Stepped four-pixel corners echo the sprite grid without decorative noise.
            c.rect(fill,(4,0,max(1,w-8),h))
            c.rect(fill,(0,4,w,max(1,h-8)))
            c.rect(edge,(4,0,max(1,w-8),2))
            c.rect(edge,(4,h-2,max(1,w-8),2))
            c.rect(edge,(0,4,2,max(1,h-8)))
            c.rect(edge,(w-2,4,2,max(1,h-8)))
            if self.focused:c.rect('#edcc88',(8,6,4,max(1,h-12)))
            return out

    class R13NotebookPaper(renpy.Displayable):
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            c.rect('#302f2bf5',(0,0,w,h))
            c.rect('#f4ecdc',(24,16,w-48,h-32))
            c.rect('#d6c9af',(587,16,12,h-32))
            c.line('#b5a587',(587,25),(587,h-25),1)
            c.line('#fffaed',(600,25),(600,h-25),1)
            c.line('#c1ab81',(45,129),(w-46,129),1)
            c.line('#c1ab81',(45,h-86),(w-46,h-86),1)
            return out

    def r13_ui_font():
        return 'assets/Galmuri11.ttf'

init 61:
    style r13_text is default:
        color '#38392f'
        font r13_ui_font()
        outlines []
    style r13_button is button:
        background R13PaperPanel()
        hover_background R13PaperPanel(True)
        selected_background R13PaperPanel(True)
        insensitive_background R13PaperPanel()
        padding (18,12)
    style r13_button_text is button_text:
        color '#384338'
        hover_color '#1d3029'
        selected_color '#71451f'
        insensitive_color '#999487'
        font r13_ui_font()
        outlines []
    style r13_frame is frame:
        background R13PaperPanel()
    style r13_scrollbar is scrollbar:
        base_bar Solid('#d9d0bf')
        thumb Solid('#a89571',xsize=7,ysize=42)
    style r13_vscrollbar is r13_scrollbar:
        xsize 7
        bar_vertical True
    style r13_label_text is r13_text
    style r13_say_dialogue is say_dialogue:
        font r13_ui_font()
        color '#fcf3df'
    style r13_say_label is say_label:
        font r13_ui_font()
        color '#ebcd8a'

init 62:
    style r13_action_button is r13_button:
        background R13ActionPanel()
        hover_background R13ActionPanel(True)
        insensitive_background R13ActionPanel(disabled=True)
        padding (16,12)
    style r13_action_button_text is r13_button_text:
        color "#fff4df"
        hover_color "#ffffff"
        insensitive_color "#c3cecb"
        size 23
        xalign 0.5

transform r13_portrait_close(top=110):
    xpos 640
    xanchor 0.5
    ypos top
    nearest True
    rotate_pad False

init 62:
    style r13_bar is bar:
        left_bar Solid("#bd9b61")
        right_bar Solid("#14292f")
        thumb Solid("#fff0ce",xsize=14)
        thumb_offset 0
