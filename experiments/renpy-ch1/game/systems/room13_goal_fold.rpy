# Player-opened field thoughts; question discoveries never open the panel.
default r13_goal_open=False
default r13_thoughts_seen = ()
# 0.18.75 (design review #5): a changed thought is shown once for a few seconds, not only as a dot.
default r13_thought_toasted = ()

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
    $ notes=[] if r13_v111_active() else r13_first_mystery_notes()
    $ thought = "편지는 이곳에서 왔다. 그런데 아내는 어디에 있을까." if goal.startswith(("편지를 보낸 여관","엄마가 기다린다던 여관")) else goal
    $ panel_height=280
    $ signature=tuple([thought]+[n["title"] for n in notes])
    if not renpy.get_screen("r13_evidence_found"):
        fixed:
            area (336,84,160,88 if r13_touch_ui() else 64)
            use r13_field_top_button("새 생각" if thought not in r13_thought_toasted and thought not in r13_thoughts_seen else "생각","dialogue",[ToggleVariable("r13_goal_open"),SetVariable("r13_thoughts_seen",tuple(sorted(set(r13_thoughts_seen)|set(signature))))],ready,width=160,chosen=r13_goal_open)
            if any(item not in r13_thoughts_seen for item in signature):
                add Solid("#d7ad61") xpos 142 ypos 17 xsize 6 ysize 6
        if ready and not r13_goal_open and thought not in r13_thoughts_seen and thought not in r13_thought_toasted:
            timer 2.4 action SetVariable("r13_thought_toasted",tuple(r13_thought_toasted)+(thought,))
        if r13_goal_open:
            button:
                area (0,0,1280,650) background None
                action SetVariable("r13_goal_open",False)
                alt "생각 접기"
            frame:
                area (24,188,624,panel_height) padding (24,20) background r13_field_paper()
                fixed:
                    xsize 576 ysize (panel_height-40)
                    text "아빠의 생각" size r13_type("emphasis") color "#493b30" font R13_UI_BOLD_FONT
                    textbutton "접기":
                        xpos 480 ypos 0 text_size r13_type("small") text_color "#765426" text_font R13_UI_BOLD_FONT
                        action SetVariable("r13_goal_open",False)
                    viewport:
                        xpos 0 ypos 64 xsize 566 ysize (panel_height-164)
                        mousewheel True draggable True scrollbars "vertical"
                        vbox:
                            spacing 16
                            text thought size r13_type("small") color "#496579" xsize 542
                    textbutton ("모은 자료 보기" if r13_v111_active() else "조사 메모 열기 · 의문 %d개"%len(notes)):
                        ypos (panel_height-86) xsize 390 ysize 56
                        text_size r13_type("small") text_color "#765426" background None hover_background Solid("#b28d4925")
                        action [SetVariable("r13_goal_open",False),(Show("r13_records",initial_tab="evidence") if r13_v111_active() else Show("r13_learning_notes"))] sensitive ready
