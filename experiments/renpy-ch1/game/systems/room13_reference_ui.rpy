# Small drawn controls; no borrowed reference artwork or additional bitmap assets.
init 79 python:
    class R13ReferenceChoice(renpy.Displayable):
        def __init__(self,hover=False,number=None,**kwargs):
            super(R13ReferenceChoice,self).__init__(**kwargs)
            self.hover=hover
            self.number=number
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(42,int(height))
            r=renpy.Render(w,h)
            panel=R13InkPanel(focused=self.hover,alpha="f5" if self.hover else "e6",slim=True) if getattr(store,"r13_ui_preview",False) else R13InkPanel(focused=self.hover)
            r.blit(renpy.render(panel,w,h,st,at),(0,0))
            c=r.canvas()
            c.rect("#626b60" if self.hover else "#2b3230",(10,10,44,h-20))
            if self.number is not None:
                t=renpy.render(Text(str(self.number),size=r13_read_size(24,28),font=r13_ui_font(),color="#eee7ce",bold=False),60,h,st,at)
                tw,th=t.get_size()
                r.blit(t,(int(32-tw/2),int((h-th)/2)))
            return r

    # Summaries live in room13_question_summaries.rpy (init 78).
    def r13_question_summary(title):
        return globals().get("R13_QUESTION_SUMMARIES",{}).get(title,title)

    def r13_choice_context():
        # The last line shown before a menu, so the choice reads as an answer to it.
        for entry in reversed(getattr(store,"_history_list",[]) or []):
            what=getattr(entry,"what",None)
            if what:
                text=renpy.filter_text_tags(what,allow=["b","i","u","color"])
                return (getattr(entry,"who",None) or "",text)
        return None

    def r13_reference_list_height(entries,width,spacing=24,cap=540,row=42,size=None):
        if not entries:
            notice=Text("지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.",size=r13_read_size(22,28),xsize=width-55)
            return int(renpy.render(notice,width-55,720,0,0).get_size()[1])+20
        total=spacing*max(0,len(entries)-1)
        for label,action,was_read in entries:
            caption=r13_question_caption(label,was_read,False)
            inner=width-99 if row<=42 else width-115
            text=Text(caption,size=size or (r13_read_size(22,28) if row<=42 else r13_read_size(23,28)),font=r13_ui_font(),xsize=inner)
            height=renpy.render(text,inner,720,0,0).get_size()[1]
            total+=max(row,height+16)
        # Render sizes can be floats; a float ypos would be read as a screen fraction.
        # Up to about seven one-line topics fit without a half-cut last row.
        return int(min(cap,total))

    def r13_question_bounds(entries,width=760):
        row=64 if persistent.room13_large_text else 56
        # 0.18.50 (owner): a long list rises over the face rather than showing a scroll bar.
        height=r13_reference_list_height(entries,width-23,12,500,row,r13_read_size(24,30))+4
        top=max(96,350-height//2)
        return top,min(610,top+height)

init 80:
    style r13_footer_button is button:
        xsize 96
        ysize 40
        padding (8,4)
        background None
        hover_background Solid("#2c524c")
    style r13_footer_button_text is text:
        font "assets/Galmuri11.ttf"
        size 20
        color "#e9e2cf"
        hover_color "#ffe39a"
        insensitive_color "#6d7b77"
        xalign .5
        yalign .5
