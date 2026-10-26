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
            # Navy notebook cover retains contrast for existing light-text overlays.
            # The outer sticker stays ivory; only the inset cover receives the navy tint.
            face=r13_sticker_button(focused=self.focused,disabled=self.disabled)
            r.blit(renpy.render(Transform(face,alpha=a,xysize=(w,h)),w,h,st,at),(0,0))
            inset=Transform(r13_sticker_button(),matrixcolor=TintMatrix("#263953"),alpha=a,xysize=(max(1,w-10),max(1,h-10)))
            r.blit(renpy.render(inset,max(1,w-10),max(1,h-10),st,at),(5,5))
            return r

    class R13ControlSurface(renpy.Displayable):
        """A whole control, never a small band inside a larger invisible button."""
        def __init__(self,primary=False,chosen=False,hovered=False,disabled=False,**kwargs):
            super(R13ControlSurface,self).__init__(**kwargs)
            self.primary=primary;self.chosen=chosen;self.hovered=hovered;self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h)
            face=r13_sticker_button(primary=self.primary or self.chosen,focused=self.hovered,disabled=self.disabled)
            r.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
            return r

    class R13SoftButtonSurface(renpy.Displayable):
        """2026-10-26 시안: 눈이 덜 피로한 보조 버튼 판. 연한 종이 바탕에 가는 갈색 테두리, 올리면 빨강."""
        def __init__(self,hovered=False,chosen=False,disabled=False,**kwargs):
            super(R13SoftButtonSurface,self).__init__(**kwargs)
            self.hovered=hovered;self.chosen=chosen;self.disabled=disabled
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            edge="#c9b49a" if self.disabled else "#a3352c" if (self.hovered or self.chosen) else "#b39572"
            face="#efe6d6" if self.disabled else "#f3dfbb" if (self.hovered or self.chosen) else "#f8efdf"
            rad=min(10,h//3)
            for (x,y,ww,hh,col) in ((0,0,w,h,edge),(2,2,w-4,h-4,face)):
                c.rect(col,(x+rad,y,ww-2*rad,hh));c.rect(col,(x,y+rad,ww,hh-2*rad))
                for cx,cy in ((x+rad,y+rad),(x+ww-rad-1,y+rad),(x+rad,y+hh-rad-1),(x+ww-rad-1,y+hh-rad-1)):
                    c.circle(col,(cx,cy),rad)
            return r

    class R13PaperFrame(renpy.Displayable):
        """Clean inset paper card. Flat colour groups, no texture or metal casing."""
        def __init__(self,corner=6,ink=False,**kwargs):
            super(R13PaperFrame,self).__init__(**kwargs)
            self.corner=corner;self.ink=ink
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            face=r13_sticker_button()
            if self.ink:face=Transform(face,matrixcolor=TintMatrix("#263953"))
            r.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
            return r

    class R13TravelSheet(renpy.Displayable):
        """Open travel folio: outer cover, paper leaves, spine and index margin."""
        def __init__(self,spine=True,**kwargs):
            super(R13TravelSheet,self).__init__(**kwargs)
            self.spine=spine
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h);c=r.canvas()
            face=Frame(Crop((35,25,550,245),r13_asset_path("file:assets/ui-b-main/b_main_panel.png")),44,28)
            r.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
            if self.spine:
                c.line("#bda580",(238,26),(238,h-30),2)
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

    class R13DiaryPanel(renpy.Displayable):
        """Fixed corners and rings; the blank centre alone expands."""
        def render(self,width,height,st,at):
            w,h=max(1,int(width)),max(1,int(height))
            out=renpy.Render(w,h)
            face=Frame(r13_asset_path("file:assets/ui-field-stickers/diary.png"),26,26)
            out.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
            # 일정한 간격의 옅은 종이 결. 패널 크기와 무관하게 결의 크기를 유지한다.
            c=out.canvas()
            for y in range(28,max(29,h-28),11):
                for x in range(28,max(29,w-28),29):
                    c.line("#a8783210",(x,y),(min(x+5,w-27),y),1)
            ring=renpy.render(r13_asset("file:assets/ui-field-stickers/ring.png"),28,34,st,at)
            for y in (.25,.5,.75):out.blit(ring,(0,int(h*y)-17))
            return out

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
            face=r13_sticker_button(focused=self.focused)
            if self.dark:face=Transform(face,matrixcolor=TintMatrix("#263953"))
            out.blit(renpy.render(Transform(face,xysize=(w,h)),w,h,st,at),(0,0))
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
        return R13_UI_FONT

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
        font R13_UI_BOLD_FONT
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
