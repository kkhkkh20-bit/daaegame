# Small drawn controls; no borrowed reference artwork or additional bitmap assets.
init 79 python:
    class R13ReferenceChoice(renpy.Displayable):
        def __init__(self,hover=False,**kwargs):
            super(R13ReferenceChoice,self).__init__(**kwargs)
            self.hover=hover
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(42,int(height))
            r=renpy.Render(w,h);c=r.canvas()
            c.rect("#236078",(0,0,w,h))
            c.polygon("#eef1e7",((0,0),(28,0),(58,h),(0,h)))
            c.rect("#eed17a" if self.hover else "#dce6dc",(0,0,w,h),3 if self.hover else 1)
            return r

    def r13_reference_list_height(entries,width):
        if not entries:
            notice=Text("지금 더 물을 이야기는 없다.\n가지고 온 자료를 보여줄 수도 있다.",size=r13_read_size(22,28),xsize=width-55)
            return int(renpy.render(notice,width-55,720,0,0).get_size()[1])+20
        total=24*max(0,len(entries)-1)
        for label,action,was_read in entries:
            caption=("{font=assets/Room13Sans.ttf}✓{/font}  "+label) if was_read else label
            text=Text(caption,size=r13_read_size(22,28),font=r13_ui_font(),xsize=width-99)
            height=renpy.render(text,width-99,720,0,0).get_size()[1]
            total+=max(42,height+12)
        # Render sizes can be floats; a float ypos would be read as a screen fraction.
        return int(min(382,total))

init 80:
    style r13_footer_button is button:
        xsize 96
        ysize 40
        padding (8,4)
        background None
        hover_background Solid("#b8d6df")
    style r13_footer_button_text is text:
        font "assets/Room13Sans.ttf"
        size 20
        color "#285265"
        hover_color "#123b50"
        xalign .5
        yalign .5
