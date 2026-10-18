# Consistent reading priority, question marks and compact controls with larger hit boxes.
init 79 python:
    class R13CompactTouchSurface(renpy.Displayable):
        def __init__(self,color,band=44,**kwargs):
            super(R13CompactTouchSurface,self).__init__(**kwargs)
            self.color=color
            self.band=band
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));band=min(h,self.band)
            rv=renpy.Render(w,h)
            rv.canvas().rect(self.color,(0,h-band,w,band))
            return rv

    def r13_footer_width(count):
        return 16+count*104+max(0,count-1)*8

    def r13_question_caption(title,was_read,summarize=True,mark_unread=False):
        label=r13_question_summary(title) if summarize else title
        return ("{font=assets/Room13Sans.ttf}✓{/font}  {s}"+label+"{/s}") if was_read else (("{font=assets/Room13Sans.ttf}{color=#d9b269}{size=10}●{/size}{/color}{/font}  " if mark_unread else "")+label)

    def r13_record_heading_size(name):
        size=r13_read_size(24,29)
        minimum=r13_read_size(20,23)
        while size>minimum:
            width=renpy.render(Text(name,font=r13_ui_font(),size=size),2400,120,0,0).get_size()[0]
            if width<=692:break
            size-=1
        return size

    def r13_feedback_in_conversation():
        return any(renpy.get_screen(name) for name in ("say","r13_topics","r13_entry_topics","r13_entry_karo_topics","choice"))

# Footer geometry and text alignment are owned by room13_controls.rpy / room13_typography.rpy.
