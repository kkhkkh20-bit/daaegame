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
    # 2026-10-27 소유자: 너무 눈에 띄고 길다 — 제목 한 줄과 생각 두 줄만. 스크롤·「모은 자료 보기」는 뺐다(기록에 있다).
    $ panel_height=136
    $ signature=tuple([thought]+[n["title"] for n in notes])
    if not renpy.get_screen("r13_evidence_found"):
        fixed:
            area (336,84,160,88 if r13_touch_ui() else 64)
            use r13_field_top_button("새 생각" if thought not in r13_thought_toasted and thought not in r13_thoughts_seen else "생각","dialogue",[ToggleVariable("r13_goal_open"),SetVariable("r13_thoughts_seen",tuple(sorted(set(r13_thoughts_seen)|set(signature))))],ready,width=160,chosen=r13_goal_open)
            if any(item not in r13_thoughts_seen for item in signature):
                add Solid("#d7ad61") xpos 142 ypos 17 xsize 6 ysize 6
        if ready and not r13_goal_open and thought not in r13_thoughts_seen and thought not in r13_thought_toasted:
            timer 2.4 action SetVariable("r13_thought_toasted",tuple(r13_thought_toasted)+(thought,))
        # 질문 화면이 열리면 생각 판은 겹치지 않게 숨긴다.
        if r13_goal_open and not renpy.get_screen("r13_topics"):
            button:
                area (0,0,1280,650) background None
                action SetVariable("r13_goal_open",False)
                alt "생각 접기"
            frame:
                area (24,160,520,panel_height) padding (20,14) background r13_field_paper()
                fixed:
                    xsize 480 ysize (panel_height-28)
                    text "아빠의 생각" size r13_type("small") color "#765426" font R13_UI_BOLD_FONT
                    textbutton "접기":
                        xpos 420 ypos -4 text_size r13_type("small") text_color "#765426" text_font R13_UI_BOLD_FONT
                        action SetVariable("r13_goal_open",False)
                    text thought ypos 34 size r13_type("body") color "#3f5467" xsize 480 font R13_UI_BOLD_FONT line_spacing 2
