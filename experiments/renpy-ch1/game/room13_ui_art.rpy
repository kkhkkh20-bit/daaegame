# Travel folio, warm paper and ink. Clean colour planes without grain/noise.
init 58 python:
    # 0.19.99 (owner 2026-10-22: "갈색 톤으로 하고 ... 쭉쭉 가보자"): every dark panel and
    # every control uses the same brown pieces as the dialogue and settings windows
    # (game/assets/ui-night/, dev/make_night_ui_assets.py). Class names stay for old saves.
    R13_UI_PIECES="assets/ui-night/"
    class R13InkPanel(renpy.Displayable):
        """Brown panel with a thin gold edge (9-slice). focused/disabled change the shade only."""
        def __init__(self,focused=False,disabled=False,alpha="ff",corner=None,dark=False,slim=False,**kwargs):
            super(R13InkPanel,self).__init__(**kwargs)
            self.focused=focused;self.disabled=disabled
            self.alpha=alpha;self.corner=corner;self.dark=dark;self.slim=slim
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            r=renpy.Render(w,h)
            try:a=int(self.alpha,16)/255.0
            except Exception:a=1.0
            if self.disabled:
                face=Frame(R13_UI_PIECES+"opt_btn_insensitive.png",16,16)
            else:
                face=Frame(R13_UI_PIECES+"panel_small.png",12,12)
                if self.focused:face=Transform(face,matrixcolor=BrightnessMatrix(.08))
            r.blit(renpy.render(Transform(face,alpha=a,xysize=(w,h)),w,h,st,at),(0,0))
            return r

    class R13ControlSurface(renpy.Displayable):
        """A whole control, never a small band inside a larger invisible button."""
        def __init__(self,primary=False,chosen=False,hovered=False,disabled=False,**kwargs):
            super(R13ControlSurface,self).__init__(**kwargs)
            self.primary=primary;self.chosen=chosen;self.hovered=hovered;self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h)
            # Same pieces as the settings buttons: chosen/primary = burgundy, hover = lighter brown.
            name=("insensitive" if self.disabled else "selected" if self.primary or self.chosen
                else "hover" if self.hovered else "idle")
            face=Frame(R13_UI_PIECES+"opt_btn_%s.png"%name,16,16)
            if self.primary and self.hovered:face=Transform(face,matrixcolor=BrightnessMatrix(.08))
            if name=="idle":face=Transform(face,alpha=1.0)
            r.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
            return r

    class R13PaperFrame(renpy.Displayable):
        """Clean inset paper card. Flat colour groups, no texture or metal casing."""
        def __init__(self,corner=6,ink=False,**kwargs):
            super(R13PaperFrame,self).__init__(**kwargs)
            self.corner=corner;self.ink=ink
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            # Edge patina is broad, bounded shading, never speckled texture.
            c.rect('#806249',(0,2,w,max(1,h-2)))
            c.rect('#bea077',(1,0,max(1,w-2),max(1,h-3)))
            c.rect('#d9be91',(3,2,max(1,w-6),max(1,h-6)))
            c.rect('#66513d' if self.ink else '#e5cea5',(6,5,max(1,w-12),max(1,h-13)))
            c.rect('#4a3b30' if self.ink else '#f0dfbd',(10,9,max(1,w-20),max(1,h-22)))
            c.line('#fff0cf',(6,4),(w-7,4),1)
            c.line('#a48861',(5,h-5),(w-6,h-5),1)
            return r

    class R13TravelSheet(renpy.Displayable):
        """Open travel folio: outer cover, paper leaves, spine and index margin."""
        def __init__(self,spine=True,**kwargs):
            super(R13TravelSheet,self).__init__(**kwargs)
            self.spine=spine
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            # Slim walnut cover supports the parchment; the writing face stays clean.
            c.rect('#241c1888',(4,6,w-4,h-6))
            c.rect('#3c2d24',(0,0,w-4,h-5))
            c.rect('#77523a',(3,2,w-10,h-10))
            c.line('#a17b50',(9,3),(w-16,3),1)
            c.line('#4c3527',(12,h-8),(w-18,h-8),2)
            c.rect('#ad895e',(8,7,w-22,h-23))
            c.rect('#d2b584',(11,9,w-28,h-28))
            c.rect('#e7cea3',(15,12,w-36,h-35))
            c.rect('#f0dfbd',(21,17,w-48,h-47))
            c.line('#fff0d0',(18,13),(w-28,13),2)
            # A turned lower corner, outside all text and controls.
            c.polygon('#c4a273',[(w-44,h-25),(w-22,h-47),(w-22,h-25)])
            c.polygon('#fae9c6',[(w-44,h-25),(w-44,h-47),(w-22,h-47)])
            if self.spine:
                c.rect('#c4a67c',(226,18,10,h-48))
                c.line('#9b7b53',(230,21),(230,h-32),1)
                c.line('#fff0ce',(237,21),(237,h-32),2)
                c.line('#b99b75',(252,h-94),(w-38,h-94),1)
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
        def __init__(self, focused=False, dark=False, transferable=False, remembered=False, **kwargs):
            super(R13PaperPanel,self).__init__(**kwargs)
            self.focused=focused
            self.dark=dark
            self.transferable=transferable
            self.remembered=remembered
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            c.rect('#161e2138',(3,4,max(1,w-3),max(1,h-4)))
            points=[(0,0),(w-1,0),(w-1,h-1),(0,h-1)]
            fill=('#3c3431' if self.dark else '#f7e7c8' if self.focused else '#e2cca8')
            c.polygon(fill,points)
            if getattr(self,"remembered",False):
                for x in range(0,w,10):
                    c.line('#baa07b',(x,0),(min(x+5,w-1),0),2)
                    c.line('#baa07b',(x,h-1),(min(x+5,w-1),h-1),2)
                for y in range(0,h,10):
                    c.line('#baa07b',(0,y),(0,min(y+5,h-1)),2)
                    c.line('#baa07b',(w-1,y),(w-1,min(y+5,h-1)),2)
            else:
                c.lines('#b58b2f' if self.transferable else '#9a634d' if self.focused else '#baa07b',True,points,3 if self.focused else 2)
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

transform r13_portrait_close(top=110,x=640):
    xpos x
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

init 58 python:
    class R13StripCell(renpy.Displayable):
        def __init__(self,active=False,**kwargs):
            super(R13StripCell,self).__init__(**kwargs)
            self.active=active
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h)
            if self.active:
                c=r.canvas();c.rect("#60503b",(5,5,max(1,w-10),max(1,h-10)))
                c.rect("#b58c48",(6,h-7,max(1,w-12),2))
                c.rect("#e6bd69",(6,h-5,max(1,w-12),2))
            return r
