# Travel folio, warm paper and ink. Clean colour planes without grain/noise.
init 58 python:
    class R13InkPanel(renpy.Displayable):
        """Flat ink-brown plate, small stepped corners and a narrow lit edge."""
        def __init__(self,focused=False,disabled=False,alpha="ff",corner=None,dark=False,**kwargs):
            super(R13InkPanel,self).__init__(**kwargs)
            self.focused=focused;self.disabled=disabled
            self.alpha=alpha;self.corner=corner;self.dark=dark
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            r=renpy.Render(w,h);c=r.canvas()
            cut=min(self.corner or 6,max(1,min(w,h)//4))
            def edge(n):
                d=max(1,cut-n)
                return [(n+d,n),(w-n-d-1,n),(w-n-1,n+d),(w-n-1,h-n-d-1),
                        (w-n-d-1,h-n-1),(n+d,h-n-1),(n,h-n-d-1),(n,n+d)]
            fill=('#493f38' if self.disabled else '#292729' if self.dark else '#665047' if self.focused else '#3c3431')
            c.polygon(fill+self.alpha,edge(3))
            # Border bands leave the inner face clear for the explicit light option.
            for outer,inner,color in ((edge(0),edge(1),'#332b28'),
                    (edge(1),edge(3),'#9b8265' if self.focused else '#786959')):
                for i in range(8):
                    j=(i+1)%8
                    c.polygon(color,[outer[i],outer[j],inner[j],inner[i]])
            c.line('#d3bb90' if self.focused else '#a38d70',(cut+2,2),(w-cut-3,2),1)
            c.line('#251f1e',(cut+2,h-2),(w-cut-3,h-2),1)
            if self.focused:
                c.rect('#b9765e',(3,cut,3,max(1,h-cut*2)))
            return r

    class R13PaperFrame(renpy.Displayable):
        """Clean inset paper card. Flat colour groups, no texture or metal casing."""
        def __init__(self,corner=6,**kwargs):
            super(R13PaperFrame,self).__init__(**kwargs)
            self.corner=corner
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            c.rect('#8f7054',(0,2,w,max(1,h-2)))
            c.rect('#f0dfbc',(1,0,max(1,w-2),max(1,h-3)))
            c.rect('#d9c29b',(4,4,max(1,w-8),max(1,h-9)))
            c.line('#fff0cf',(4,4),(w-5,4),2)
            c.line('#b79a73',(5,h-6),(w-5,h-6),1)
            return r

    class R13TravelSheet(renpy.Displayable):
        """Open travel folio: outer cover, paper leaves, spine and index margin."""
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            c.rect('#2b211d88',(4,6,w-4,h-6))
            c.rect('#604637',(0,0,w-4,h-5))
            c.rect('#bca17b',(3,2,w-10,h-10))
            c.rect('#eddbb8',(6,4,w-16,h-15))
            c.line('#fff0d0',(8,5),(w-12,5),2)
            # A few deliberate edge steps, not repeated grain or distressed noise.
            c.rect('#d5bd97',(6,h-14,w-16,3))
            c.rect('#c4a67c',(226,13,10,h-38))
            c.line('#a88a64',(230,15),(230,h-26),1)
            c.line('#fff0ce',(237,15),(237,h-26),2)
            c.line('#b99b75',(252,h-94),(w-30,h-94),1)
            return r

    class R13TouchSurface(renpy.Displayable):
        # Keep a 64px touch target while the visible control is only 44px high.
        def __init__(self,focused=False,disabled=False,band=44,**kwargs):
            super(R13TouchSurface,self).__init__(**kwargs)
            self.focused=focused;self.disabled=disabled;self.band=band
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));band=min(h,self.band)
            r=renpy.Render(w,h)
            r.blit(renpy.render(R13InkPanel(self.focused,self.disabled),w,band,st,at),(0,h-band))
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
            fill=('#3c3431' if self.dark else '#f7e7c8' if self.focused else '#e2cca8')
            c.polygon(fill,points)
            c.lines('#9a634d' if self.focused else '#baa07b',True,points,3 if self.focused else 2)
            return out

    class R13ActionPanel(R13InkPanel):
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

    # Compatibility names for displayables that may occur in older save payloads.
    R13StonePanel=R13InkPanel
    R13StonePaperPanel=R13PaperFrame
    R13StoneTouchSurface=R13TouchSurface

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
        color '#493b30'
        hover_color '#724b39'
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
        right_bar Solid("#3c3431")
        thumb Solid("#fff0ce",xsize=14)
        thumb_offset 0
