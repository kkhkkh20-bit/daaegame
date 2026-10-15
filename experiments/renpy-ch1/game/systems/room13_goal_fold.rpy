# Player-opened field thoughts; question discoveries never open the panel.
default r13_goal_open=False
default r13_thoughts_seen = ()

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
    $ thought = "편지는 이곳에서 왔다. 그런데 아내는 어디에 있을까." if goal.startswith("편지를 보낸 여관") else goal
    $ panel_height=min(430,256+len(notes)*52)
    $ signature=tuple([thought]+[n["title"] for n in notes])
    if not renpy.get_screen("r13_evidence_found"):
        fixed:
            xpos 1048 ypos 664 xsize 112 ysize 56
            use r13_antique_button("생각","dialogue",[ToggleVariable("r13_goal_open"),SetVariable("r13_thoughts_seen",tuple(sorted(set(r13_thoughts_seen)|set(signature))))],enabled=ready,compact=True,width=112,chosen=r13_goal_open)
            if any(item not in r13_thoughts_seen for item in signature):
                add Solid("#d7ad61") xpos 94 ypos 17 xsize 6 ysize 6
        if r13_goal_open:
            button:
                area (0,0,1280,650) background None
                action SetVariable("r13_goal_open",False)
                alt "생각 접기"
            frame:
                area (624,644-panel_height,624,panel_height) padding (24,20) background R13PaperFrame()
                fixed:
                    xsize 576 ysize (panel_height-40)
                    text "아빠의 생각" size 26 color "#493b30"
                    textbutton "접기":
                        xpos 480 ypos 0 text_size 20 text_color "#765426"
                        action SetVariable("r13_goal_open",False)
                    viewport:
                        xpos 0 ypos 64 xsize 566 ysize (panel_height-164)
                        mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 16
                            text thought size r13_read_size(22,24) color "#496579" xsize 542
                            for i,note in enumerate(notes):
                                button:
                                    xsize 542 padding (10,8)
                                    background None hover_background Solid("#b28d4925")
                                    action [SetVariable("r13_goal_open",False),Show("r13_learning_notes",focus=i)] sensitive ready
                                    text note["title"] size r13_read_size(20,22) color "#65503b" xsize 516
                    text "자세한 내용은 기록 · 조사 메모에서" ypos (panel_height-74) size 18 color "#796a52"
