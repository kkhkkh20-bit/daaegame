# Quiet paper, ink and brass. Material planes deliberately have no grain/noise.
init 58 python:
    class R13StonePanel(renpy.Displayable):
        """Opaque, chamfered casing with broad lit and shaded bevel planes."""
        def __init__(self,focused=False,disabled=False,alpha="ff",corner=None,dark=False,**kwargs):
            super(R13StonePanel,self).__init__(**kwargs)
            self.focused=focused
            self.disabled=disabled
            self.alpha=alpha
            self.corner=corner
            self.dark=dark
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            r=renpy.Render(w,h);c=r.canvas()
            cut=min(self.corner or (24 if h>300 else 16 if h>90 else 10),max(2,min(w,h)//3))
            bevel=min(8,max(3,min(w,h)//6))
            def contour(inset):
                d=max(2,cut-inset//2)
                return [(inset+d,inset),(w-inset-d-1,inset),
                        (w-inset-1,inset+d),(w-inset-1,h-inset-d-1),
                        (w-inset-d-1,h-inset-1),(inset+d,h-inset-1),
                        (inset,h-inset-d-1),(inset,inset+d)]
            outer=contour(2);inner=contour(bevel+2)
            # Draw broad solid facets, not concentric hairline borders.
            c.polygon('#202122',contour(0))
            lights=['#a9aaa5','#8c8e8a','#666966','#343637',
                    '#292c2d','#424544','#757975','#a0a39d']
            for i in range(8):
                j=(i+1)%8
                c.polygon(lights[i],[outer[i],outer[j],inner[j],inner[i]])
            fill=('#414345' if self.disabled else '#414548' if self.dark else '#626564' if self.focused else '#505354')
            c.polygon(fill+self.alpha,inner)
            c.lines('#303333',True,inner,2)
            if self.focused:
                # Restrained ivory accent is a focus state, never an extra gold frame.
                c.line('#e4d5a1',inner[0],inner[1],2)
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
