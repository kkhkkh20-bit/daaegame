# 2026-10-24 수첩 목표 칸 (소유자 "추천안대로"; 시안 docs/reviews/goal-strip-20261024/목표_닫힘.png,
# 목표_펼침_14일.png, 목표_펼침_11일전예시.png, 생성 dev/make_goal_strip_mockup.py; 설계 docs/design/PRICE_DESIGN.md
# 「최종 목표를 상기시킨다」).
# 새 세계(v111) 기록 화면 자료 탭의 탭 줄 오른쪽 빈자리에 「목표 ●●● 지금 단계」 칸을 두고, 누르면 세 단계와
# 그날의 한 줄이 펼쳐진다. 다시 누르거나 바깥을 누르면 닫힌다.
# 이야기 조건은 새로 만들지 않는다. 단계와 한 줄은 이미 있는 값으로만 고른다:
#   장면 진입 표식 v111:entered:<장면> (r13_v111_scene), 엄마 만남 family_reunited (11일 D11_S02 끝에서 True),
#   그리고 아래 세 줄을 실제로 지났다는 표식 v111:line:<줄 id> (r13_before_line 이 그 줄의 대화를 시작할 때 남김).
#   표식이 없는 옛 저장은 그 줄 뒤에 반드시 오는 장면에 들어갔는지로 판정한다.
# 보여 주기만 한다: 자료·값·진행을 바꾸지 않는다.
init 337 python:
    R13_GOAL_STEPS=("마을을 조사한다",("엄마를 찾는다","엄마를 지킨다"),"셋이 나간다")
    # ①은 1일 입구를 지나 여관에 들어서면(장면 D01_S05) 마친 것으로 친다.
    R13_GOAL_GATE_PASSED="MS14_D01_S05"
    # 지났는지 보는 대사: 이름 -> (줄 id, 그 줄 뒤에 반드시 오는 장면 — 옛 저장 판정용)
    R13_GOAL_LINES=dict(
        room13_empty=("MS14_D01_S05_L0016","MS14_D02_S01"),   # 1일 13호실 빈방 「엄마?」
        bami_river=("MS14_D04_S02_L0017","MS14_D04_S03"),     # 4일 밤이 「이 사람…… 강 쪽에서 봤어요.」
        pass_blocked=("MS14_D11_S00_L0002","MS14_D11_S01"),   # 11일 까로 「바깥 고개가 막혔대요.」
        list_seen13=("MS14_D13_S02_L0013","MS14_D13_S03"),    # 13일 광장 너울 「부인도 명단에 있소. 여기 적혀 있소.」
    )
    # 칸 아래 한 줄: (시작 날, 끝 날, 지나야 하는 것, 문장). 뒤에서부터 조건이 맞는 첫 줄을 쓴다.
    # 조건이 안 맞으면 앞 줄로 내려간다(예: 4일인데 밤이 대화 전이면 1~3일 문장). 문장은 소유자 승인안 그대로.
    R13_GOAL_NOTES=(
        (1,3,"room13_empty","엄마는 여관 13호실에서 기다린다고 했다. 13호실은 비어 있었다."),
        (4,10,"bami_river","밤이가 강 쪽에서 엄마를 봤다고 했다."),
        (11,12,"pass_blocked","바깥 고개가 막혔다. 걸어서도 못 나간다."),
        # 2026-10-24 행동 검수 8(소유자 승인): 「셋이 함께 남아야 한다」가 13일 촌장의 거래(가족 셋만 물러나기)를
        # 권하는 말로 읽혔다. 문장을 바꾸고, 아빠가 광장에서 명단 종이를 처음 보는 줄(D13_S02_L0013)부터 보인다.
        # 그 전 13일 아침과 입구 경비실(같은 D13_S02 장면)에서는 11~12일 문장이 남는다.
        (13,14,"list_seen13","명단에 빈칸이 있는 한, 다음은 누구든 될 수 있다."),
    )
    # 2026-10-24 행동 검수 8(소유자 승인): 엄마는 13일 명단에 오른다. 만났다고 곧바로 「엄마를 지킨다 — 마침」으로
    # 두면 13일 사실과 어긋난다. 13일 수레 일이 다 지나간 뒤(14일 장면에 들어선 뒤)에야 ③으로 넘긴다.
    R13_GOAL_GUARD_DONE="MS14_D14_S01"
    R13_GOAL_GOLD="#8d4b2d"
    R13_GOAL_INK="#503525"
    R13_GOAL_DIM="#96846e"
    R13_GOAL_RED="#781c24"
    R13_GOAL_RULE="#5a4632"

    def r13_goal_active():
        return r13_v111_active()

    def r13_goal_scene_reached(scene):
        """그 장면 또는 그 뒤 장면(기록된 장면 순서)에 들어간 적이 있다."""
        order=R13_DRAWER_SCENE_INDEX
        target=order.get(scene)
        if target is None:return False
        flags=(store.room13 or {}).get("flags",[])
        for flag in flags:
            if isinstance(flag,str) and flag.startswith("v111:entered:") and order.get(flag[13:],-1)>=target:return True
        return False

    def r13_goal_passed(mark):
        if mark.startswith("scene:"):return r13_goal_scene_reached(mark[6:])
        rid,after=R13_GOAL_LINES[mark]
        return r13_has("v111:line:"+rid) or r13_goal_scene_reached(after)

    def r13_goal_state():
        """(단계 이름 셋, 지금 단계 번호 0~2, 아래 한 줄 또는 None)."""
        met=r13_v111_value("family_reunited") is True
        steps=[R13_GOAL_STEPS[0],R13_GOAL_STEPS[1][1 if met else 0],R13_GOAL_STEPS[2]]
        current=2 if met and r13_goal_scene_reached(R13_GOAL_GUARD_DONE) else (1 if met or r13_goal_scene_reached(R13_GOAL_GATE_PASSED) else 0)
        day=(store.room13 or {}).get("day") or 1
        note=None
        for first,last,mark,text in reversed(R13_GOAL_NOTES):
            if day>=first and r13_goal_passed(mark):
                note=text;break
        return steps,current,note

    def r13_goal_mark_line(identity):
        """대화가 그 줄을 시작하면 표식을 남긴다(대화 건너뛰기로 넘겨도 그 줄의 대화는 시작된 것으로 친다)."""
        if not isinstance(identity,str) or not identity.startswith("v111:") or not r13_v111_active():return
        parts=identity.split(":")
        for rid,after in R13_GOAL_LINES.values():
            if rid in parts and not r13_has("v111:line:"+rid):r13_flag("v111:line:"+rid)

    _r13_goal_before_line=r13_before_line
    def r13_before_line(identity,index,text):
        key=_r13_goal_before_line(identity,index,text)
        r13_goal_mark_line(identity)
        return key

    def r13_goal_text_width(text,size):
        return int(r13_ev_text_units(text)*size)+2

    def r13_goal_pill_layout(left,right,touch):
        """칸이 들어갈 자리(left~right)에 맞춰 무엇을 보일지 정한다. 자리가 좁으면 이름 → 점 순서로 뺀다.
        PC 는 시안처럼 한 줄, 휴대폰은 88px 높이 안에 두 줄(위: 목표와 점, 아래: 지금 단계)."""
        steps,current,note=r13_goal_state()
        label=steps[current]
        avail=right-left
        pad=8 if touch else 12
        word_size=r13_read_size(18,20) if touch else r13_read_size(17,20)
        word_w=r13_goal_text_width("목표",word_size)
        pitch=18 if touch else 15
        dots_w=2*pitch+(14 if touch else 12)
        floor=r13_ev_small_size() if touch else r13_read_size(15,18)
        base=r13_read_size(20,22) if touch else r13_read_size(19,22)
        if touch:
            row1=pad+word_w+8+dots_w+pad
            label_size=min(base,(avail-2*pad)//max(1,r13_ev_text_units(label)))
            width=max(row1,(pad+r13_goal_text_width(label,label_size)+pad) if label_size>=floor else 0)
            if row1<=avail:
                return dict(x=left,w=min(avail,max(width,row1,245)),stacked=False,word=word_size,dots=True,label=(label if label_size>=floor else None),
                    label_size=label_size,pad=pad,word_w=word_w,pitch=pitch,steps=steps,current=current,note=note)
            if pad+max(word_w,dots_w)+pad<=avail:
                return dict(x=left,w=avail,stacked=True,word=word_size,dots=True,label=None,label_size=0,pad=pad,word_w=word_w,pitch=pitch,
                    steps=steps,current=current,note=note)
            return None
        label_x=pad+word_w+10+dots_w+10
        label_size=min(base,int((avail-label_x-pad)/max(1,r13_ev_text_units(label))))
        show_label=label_size>=floor
        width=(label_x+r13_goal_text_width(label,label_size)+pad) if show_label else (pad+word_w+10+dots_w+pad)
        if width>avail:
            if pad+word_w+pad>avail:return None
            return dict(x=left,w=avail,stacked=False,word=word_size,dots=False,label=None,label_size=0,pad=pad,word_w=word_w,pitch=pitch,
                steps=steps,current=current,note=note)
        # 시안 폭(약 245px)을 넘지 않게, 자리가 넉넉해도 이름 끝에서 닫는다.
        return dict(x=left,w=max(width,min(245,avail)) if show_label else width,stacked=False,word=word_size,dots=True,
            label=(label if show_label else None),label_size=label_size,label_x=label_x,pad=pad,word_w=word_w,pitch=pitch,
            steps=steps,current=current,note=note)

    def r13_goal_alt(steps,current,note,opened):
        parts=["목표, 지금 단계 %d. %s"%(current+1,steps[current])]
        parts.append("펼친 판 닫기" if opened else "눌러서 세 단계 보기")
        return ". ".join(parts)

    def r13_goal_card_alt(steps,current,note):
        rows=[]
        for index,label in enumerate(steps):
            rows.append("%d. %s, %s"%(index+1,label,"지금" if index==current else ("마침" if index<current else "남음")))
        if note:rows.append(note)
        return "목표. "+". ".join(rows)

    class R13GoalDot(renpy.Displayable):
        """목표 점 하나: 지난 단계 금색 채움, 지금 단계 버건디(금 테두리), 남은 단계 빈 원."""
        def __init__(self,state,radius=5,**kwargs):
            super(R13GoalDot,self).__init__(**kwargs)
            self.state=state;self.radius=radius
        def render(self,width,height,st,at):
            d=self.radius*2+2;r=renpy.Render(d,d);c=r.canvas();center=(self.radius+1,self.radius+1)
            if self.state=="done":c.circle(R13_GOAL_GOLD,center,self.radius)
            elif self.state=="now":
                c.circle(R13_GOAL_RED,center,self.radius)
                c.circle(R13_GOAL_GOLD,center,self.radius,1)
            else:c.circle(R13_GOAL_GOLD,center,self.radius,1)
            return r

    def r13_goal_dot_state(index,current):
        return "done" if index<current else ("now" if index==current else "todo")

# 탭 줄 오른쪽 칸과 펼친 판. r13_records 의 증거 서랍(자료 탭) 맨 끝에서 쓴다 — 다른 것 위에 그려야 한다.
# tabs_right: 마지막 탭의 오른쪽 끝, chips_left: 오른쪽 칩(이번 사건 …)의 왼쪽 끝.
screen r13_goal_strip(tabs_right,chips_left):
    default goal_open=False
    if r13_goal_active():
        $ touch=r13_touch_ui()
        $ layout=r13_goal_pill_layout(tabs_right+10,chips_left-(6 if touch else 8),touch)
        if layout:
            $ pill_y=16 if touch else 44
            $ pill_h=88 if touch else 42
            $ dot_r=6 if touch else 5
            if goal_open:
                # 바깥을 누르면 닫힌다. 판 아래 모든 것보다 위, 칸과 판보다는 아래.
                button:
                    style "r13ev_tab_button"
                    xpos 0 ypos 0 xysize (1280,720)
                    action SetLocalVariable("goal_open",False) alt "목표 판 닫기"
            button:
                id "r13_goal_pill"
                style "r13ev_chip_button"
                xpos layout["x"] ypos pill_y xysize (layout["w"],pill_h) padding (0,0)
                # 펼쳐도 버건디로 칠하지 않는다 — 지금 단계 점(버건디)이 바탕에 묻힌다.
                action ToggleLocalVariable("goal_open")
                alt r13_goal_alt(layout["steps"],layout["current"],layout["note"],goal_open)
                if layout["stacked"]:
                    vbox:
                        xalign .5 yalign .5 spacing 6
                        text "목표" size layout["word"] color R13_GOAL_GOLD font r13_ui_font() xalign .5
                        hbox:
                            xalign .5 spacing (layout["pitch"]-2*dot_r-2)
                            for index in range(3):
                                add R13GoalDot(r13_goal_dot_state(index,layout["current"]),dot_r) yalign .5
                elif touch and layout["label"]:
                    vbox:
                        xpos layout["pad"] yalign .5 spacing 8
                        hbox:
                            spacing 8
                            text "목표" size layout["word"] color R13_GOAL_GOLD font r13_ui_font() yalign .5
                            hbox:
                                yalign .5 spacing (layout["pitch"]-2*dot_r-2)
                                for index in range(3):
                                    add R13GoalDot(r13_goal_dot_state(index,layout["current"]),dot_r) yalign .5
                        text layout["label"] size layout["label_size"] color R13_GOAL_INK font r13_ui_font()
                else:
                    hbox:
                        xpos layout["pad"] yalign .5 spacing (8 if touch else 10)
                        text "목표" size layout["word"] color R13_GOAL_GOLD font r13_ui_font() yalign .5
                        if layout["dots"]:
                            hbox:
                                yalign .5 spacing (layout["pitch"]-2*dot_r-2)
                                for index in range(3):
                                    add R13GoalDot(r13_goal_dot_state(index,layout["current"]),dot_r) yalign .5
                        if layout["label"]:
                            text layout["label"] size layout["label_size"] color R13_GOAL_INK font r13_ui_font() yalign .5
            if goal_open:
                $ step_size=r13_read_size(24,26) if touch else r13_read_size(21,24)
                $ note_size=r13_read_size(20,22) if touch else r13_read_size(16,19)
                $ card_w=(560 if touch else 434)
                $ card_x=min(layout["x"],1240-card_w)
                button:
                    id "r13_goal_card"
                    style "r13ev_chip_button"
                    xpos card_x ypos (pill_y+pill_h+(6 if touch else 7)) xsize card_w
                    background Fixed(R13ControlSurface(),R13ControlSurface()) hover_background Fixed(R13ControlSurface(),R13ControlSurface())
                    padding ((20,16,20,16) if touch else (19,14,19,12))
                    action NullAction()
                    alt r13_goal_card_alt(layout["steps"],layout["current"],layout["note"])
                    vbox:
                        spacing (10 if touch else 8)
                        for index,label in enumerate(layout["steps"]):
                            $ state=r13_goal_dot_state(index,layout["current"])
                            hbox:
                                spacing (14 if touch else 13)
                                add R13GoalDot(state,(8 if touch else 6)) yalign .5
                                text (label+("  ← 지금" if state=="now" else "")) size step_size font r13_ui_font() yalign .5 color ("#8a7664" if state=="todo" else "#493323")
                        if layout["note"]:
                            add Solid(R13_GOAL_RULE) xsize (card_w-38) ysize 1 yoffset 2
                            text layout["note"] size note_size color "#80654e" font r13_ui_font() xsize (card_w-40) yoffset 2
