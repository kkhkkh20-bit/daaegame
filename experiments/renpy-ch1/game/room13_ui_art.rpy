# Quiet paper, ink and brass. Material planes deliberately have no grain/noise.
init 58 python:
    class R13StonePanel(renpy.Displayable):
        """Flat charcoal infill with a stepped, layered slate rim; no grain."""
        def __init__(self,focused=False,disabled=False,alpha="ff",corner=None,**kwargs):
            super(R13StonePanel,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
            self.alpha=alpha
            self.corner=corner
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            r=renpy.Render(w,h);c=r.canvas()
            cut=self.corner or (22 if w>1000 and h>300 else 14 if h>100 else 7)
            def ring(n):
                d=max(2,cut-n//2)
                return [(n+d,n),(w-n-d-1,n),(w-n-1,n+d),
                        (w-n-1,h-n-d-1),(w-n-d-1,h-n-1),
                        (n+d,h-n-1),(n,h-n-d-1),(n,n+d)]
            fill=('#444641' if self.disabled else '#66685e' if self.focused else '#555751')+self.alpha
            c.polygon(fill,ring(5))
            c.lines('#252724',True,ring(1),3)
            c.lines('#b6b7a6' if self.focused else '#7d8075',True,ring(3),3)
            c.lines('#353832',True,ring(6),2)
            c.line('#ded6ad' if self.focused else '#aaa99a',(cut+3,3),(w-cut-4,3),2)
            c.line('#565c58',(3,cut+3),(3,h-cut-4),2)
            c.line('#1f2424',(cut+5,h-3),(w-cut-5,h-3),2)
            return r

    class R13StonePaperPanel(renpy.Displayable):
        def __init__(self,corner=16,**kwargs):
            super(R13StonePaperPanel,self).__init__(**kwargs)
            self.corner=corner
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            r=renpy.Render(w,h)
            r.blit(renpy.render(R13StonePanel(alpha="ff",corner=self.corner),w,h,st,at),(0,0))
            d=max(2,self.corner-10)
            r.canvas().polygon('#e7e4d5',[(10+d,10),(w-10-d,10),(w-10,10+d),(w-10,h-10-d),(w-10-d,h-10),(10+d,h-10),(10,h-10-d),(10,10+d)])
            return r

    class R13StoneTouchSurface(renpy.Displayable):
        # Keep a 64px touch target while the visible control is only 44px high.
        def __init__(self,focused=False,disabled=False,band=44,**kwargs):
            super(R13StoneTouchSurface,self).__init__(**kwargs)
            self.focused=focused;self.disabled=disabled;self.band=band
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));band=min(h,self.band)
            r=renpy.Render(w,h)
            r.blit(renpy.render(R13StonePanel(self.focused,self.disabled),w,band,st,at),(0,h-band))
            return r

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
            c.lines('#a8ada1' if self.focused else '#737975',True,points,3 if self.focused else 2)
            return out

    class R13ActionPanel(R13StonePanel):
        pass

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
