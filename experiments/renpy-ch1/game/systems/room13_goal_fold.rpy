# The field's one-line question folds open into every open question (owner, 0.18.21).
#   ▼ beside the faint line lists the 조사 메모 titles; picking one opens 조사 메모 at that card.
default r13_goal_open=False

init 60 python:
    class R13FoldArrow(renpy.Displayable):
        """Stepped pixel triangle: down when folded (more below), up when open. No font glyph."""
        def __init__(self,opened=False,color="#eee5d5",size=14,**kwargs):
            super(R13FoldArrow,self).__init__(**kwargs)
            self.opened=opened;self.color=color;self.size=size
        def render(self,width,height,st,at):
            n=self.size;r=renpy.Render(n,n);c=r.canvas();step=2
            rows=n//(2*step);top=(n-rows*step*2)//2
            for i in range(rows):
                # Row i is the i-th widest: at the top for ▼ (folded), at the bottom for ▲ (open).
                w=n-2*step*i;y=top+(rows-1-i if self.opened else i)*step*2
                c.rect(self.color,((n-w)//2,y,w,step*2))
            return r

screen r13_goal_fold(goal,ready=False):
    $ notes=r13_first_mystery_notes()
    vbox:
        xpos 24 ypos 178 spacing 4
        hbox:
            spacing 0
            button:
                padding (12,8) ysize r13_read_size(41,47) background Solid("#102725b0") hover_background Solid("#1d3b38e0")
                action Show("r13_learning_notes") sensitive ready
                tooltip "조사 메모 열기"
                text goal size r13_read_size(20,24) color "#eee5d5" yalign .5
            if notes:
                button:
                    padding (12,8) ysize r13_read_size(41,47) background Solid("#102725b0") hover_background Solid("#1d3b38e0")
                    action ToggleVariable("r13_goal_open") sensitive ready
                    tooltip ("궁금한 것 접기" if r13_goal_open else "궁금한 것 %d개 펼치기"%len(notes))
                    alt ("궁금한 것 접기" if r13_goal_open else "궁금한 것 펼치기")
                    hbox:
                        spacing 6 yalign .5
                        add R13FoldArrow(r13_goal_open) yalign .5
                        text str(len(notes)) size r13_read_size(17,20) color "#eee5d5b0" yalign .5
        if r13_goal_open and notes:
            frame:
                padding (8,8) background Solid("#0c1f1ee8") xmaximum 640
                vbox:
                    spacing 2
                    for i,note in enumerate(notes[:6]):
                        button:
                            xsize 620 padding (10,7) background None hover_background Solid("#ffffff1c")
                            action [SetVariable("r13_goal_open",False),Show("r13_learning_notes",focus=i)] sensitive ready
                            tooltip "조사 메모에서 보기"
                            hbox:
                                spacing 10
                                text "·" size r13_read_size(19,23) color "#efd4a1"
                                text note["title"] size r13_read_size(19,23) color "#eee5d5" xsize 580
                    if len(notes)>6:
                        textbutton ("나머지 %d개는 조사 메모에서"%(len(notes)-6)):
                            padding (10,6) text_size r13_read_size(17,20) text_color "#d4dfd8"
                            action [SetVariable("r13_goal_open",False),Show("r13_learning_notes")] sensitive ready
