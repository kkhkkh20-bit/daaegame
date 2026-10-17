# 0.18.91 수첩 · 관계도 (소유자 2026-10-17 승인 시안 docs/relation-mock 참고)
# - 만난 주민의 얼굴을 자리표(6×5)에 놓고, 알게 된 관계만 선으로 잇는다.
#   가족=금색 굵은 선, 함께 일함·도움=푸른 선, 의심·갈등=붉은 점선.
# - 숨짐: 회색 얼굴 + 붉은 X + 이름 취소선 + 언제. 구함: 초록 테두리. 행방 모름: 흐림.
# - 관계는 그 사실을 알게 된 뒤(자료·대화·장면 표식)에만 생긴다. 이야기 판정에는 쓰지 않는다.
init 166 python:
    R13_REL_DEAD = dict(R13_DEATH_FLAGS)
    R13_REL_DEAD.update({"resident_lamplighter":"chorong_dead","resident_ttadak":"ttadak_dead",
        "kid_kkomi":"kkomi_dead","kid_dodam":"dodam_dead","npc_pandol":"pandol_dead"})
    R13_REL_GONE = {"resident_musoe":("musoe_gone","강으로 떠남")}
    R13_REL_SAVED = {"resident_piko":"piko_survived","resident_librarian":"lt_lib_saved",
        "resident_lamplighter":"nt_chorong_safe","resident_ttadak":"nt_ttadak_safe","resident_nero":"nero_alive",
        "resident_teacher":"teacher_alive","kid_kkomi":"wf_kkomi_saved","resident_badook":"cv_badook_safe"}
    R13_REL_STAMPED = set(R13_REL_DEAD.values())|set(R13_REL_SAVED.values())|set(v[0] for v in R13_REL_GONE.values())

    # 언제 숨졌는지/구했는지: 그 표식이 처음 세워진 날과 때를 적어 둔다.
    _r13_rel_flag=r13_flag
    def r13_flag(*keys):
        new=[k for k in keys if k in R13_REL_STAMPED and not r13_has(k)]
        _r13_rel_flag(*keys)
        if new:
            n=winter_copy.deepcopy(store.room13);dates=dict(n.get("rel_dates",{}))
            for k in new:dates[k]=(n.get("day",1),n.get("period",0))
            n["rel_dates"]=dates;store.room13=n

    def r13_rel_when(flag):
        when=(store.room13 or {}).get("rel_dates",{}).get(flag)
        if not when:return ""
        return "%d일 %s "%(when[0],("아침","낮","저녁","밤")[min(3,when[1])])

    def r13_rel_status(person):
        """(kind, label) — kind: dead | gone | saved | missing | with | None."""
        s=store.room13 or {}
        flag=R13_REL_DEAD.get(person)
        if flag and r13_has(flag):return "dead",r13_rel_when(flag)+"숨짐"
        gone=R13_REL_GONE.get(person)
        if gone and r13_has(gone[0]):return "gone",gone[1]
        flag=R13_REL_SAVED.get(person)
        if flag and r13_has(flag):return "saved",r13_rel_when(flag)+"구함"
        if person=="mom":
            return (None,"") if (s.get("mom_state")=="reunited" or r13_has("mom_reunited")) else ("missing","아직 못 만남")
        if person=="daram":
            return ("with","함께 있음") if s.get("daram_state") in ("with_dad","rescued") else ("missing","떨어져 있음")
        return None,""

    def _r13_rel_any(*keys):
        return lambda:any(r13_has(k) for k in keys)

    # (가, 나, 종류, 선 위의 말, 알게 되는 조건)
    R13_RELATIONS = [
        ("daram","mom","family","가족",lambda:True),
        ("granny","resident_tosil","family","함께 산다",lambda:True),
        ("granny","nabi","work","거둬 준 빚",_r13_rel_any("W2")),
        ("resident_lamplighter","mom","work","엄마의 편지를 전함",_r13_rel_any("N05","N06","E19")),
        ("resident_tok","resident_ttadak","work","판자 버릇을 앎",_r13_rel_any("nt_ttadak_safe","ttadak_dead")),
        ("resident_ttadak","resident_nero","work","천막에 댈 판자",_r13_rel_any("st_ttadak_boards")),
        ("resident_tok","resident_piko","work","3번 등 밑에서 잠",_r13_rel_any("L00")),
        ("resident_musoe","resident_somi","family","할아버지와 손녀",_r13_rel_any("K05")),
        ("resident_nero","resident_musoe","work","천막에 숨겨 줌",_r13_rel_any("somi_secret")),
        ("resident_bori","kid_dodam","family","아빠와 아들",_r13_rel_any("st_dodam_seen")),
        ("resident_teacher","kid_kkomi","work","반장",_r13_rel_any("st_kkomi_class_seen")),
        ("resident_lamplighter","resident_badook","work","밤 순회를 함께",_r13_rel_any("st_chorong_after")),
        ("resident_siluk","resident_madam","suspect","등 조각을 팔고 삼",_r13_rel_any("L09")),
        ("granny","neoul","suspect","편지를 가져오라 부탁",_r13_rel_any("N02")),
        ("granny","resident_ttadak","suspect","새벽 통로를 미리 들음",_r13_rel_any("N03")),
        ("resident_ppul","granny","suspect","명령서를 감쌈",_r13_rel_any("V06")),
    ]

    # 자리표 (열, 줄): 여관 왼쪽 · 가족과 질서 가운데 · 등불·광장·아랫길 오른쪽 · 학교 왼쪽 아래.
    R13_REL_SLOTS = {
        "granny":(0,0),"nabi":(1,0),"resident_tosil":(0,1),"buri":(1,1),"resident_owlgp":(0,2),"resident_tori":(1,2),
        "daram":(2,0),"mom":(3,0),"neoul":(2,2),"guard":(3,2),"resident_badook":(2,3),"resident_ppul":(3,3),
        "resident_lamplighter":(4,0),"resident_ttadak":(5,0),"resident_tok":(4,1),"resident_piko":(5,1),
        "resident_librarian":(4,2),"resident_nero":(5,2),"resident_siluk":(4,3),"resident_madam":(5,3),
        "resident_musoe":(4,4),"resident_somi":(5,4),
        "resident_teacher":(0,3),"resident_bori":(1,3),"kid_kkomi":(0,4),"kid_dodam":(1,4),
    }
    R13_REL_COLS, R13_REL_ROWS, R13_REL_CELL = 6, 5, (88, 88)
    R13_REL_KIND = {"family":("#b2862e",5,False),"work":("#4e6f8f",3,False),"suspect":("#a2401f",3,True)}

    def r13_rel_edges():
        shown=set(r13_rel_people())
        return [(a,b,k,l) for a,b,k,l,ok in R13_RELATIONS if a in shown and b in shown and ok()]

    def r13_rel_people():
        met=set(r13_met_people())|{"daram","mom"}
        linked=set()
        for a,b,k,l,ok in R13_RELATIONS:
            if a in met and b in met and ok():linked|={a,b}
        people=[p for p in R13_REL_SLOTS if p in met]
        people+=[p for p in met if p not in R13_REL_SLOTS and (p in linked or r13_rel_status(p)[0])]
        return people

    def r13_rel_layout():
        """person -> (x, y) slot origin inside the graph area."""
        used={};free=[(c,r) for r in range(R13_REL_ROWS) for c in range(R13_REL_COLS)]
        people=r13_rel_people()
        for p in people:
            if p in R13_REL_SLOTS:
                used[p]=R13_REL_SLOTS[p];free.remove(R13_REL_SLOTS[p])
        for p in people:
            if p not in used and free:used[p]=free.pop(0)
        return {p:(c*R13_REL_CELL[0],r*R13_REL_CELL[1]) for p,(c,r) in used.items()}

    def r13_rel_counts():
        people=r13_rel_people();kinds=[r13_rel_status(p)[0] for p in people]
        return dict(all=len(people),alive=sum(1 for k in kinds if k not in ("dead","gone")),
            dead=kinds.count("dead"),saved=kinds.count("saved"))

    def r13_rel_match(person,filt):
        kind=r13_rel_status(person)[0]
        if filt=="alive":return kind not in ("dead","gone")
        if filt=="dead":return kind in ("dead","gone")
        if filt=="saved":return kind=="saved"
        return True

    def r13_rel_lines_of(person):
        return [(b if a==person else a,k,l) for a,b,k,l in r13_rel_edges() if person in (a,b)]

    class R13RelLines(renpy.Displayable):
        """Relation lines between face centres; dashed for suspicion. The selected person's lines are bold."""
        def __init__(self,edges,layout,selected=None,**kwargs):
            super(R13RelLines,self).__init__(**kwargs)
            self.edges=edges;self.layout=layout;self.selected=selected
        def render(self,width,height,st,at):
            w=R13_REL_COLS*R13_REL_CELL[0];h=R13_REL_ROWS*R13_REL_CELL[1]
            rv=renpy.Render(w,h);canvas=rv.canvas()
            for a,b,kind,label in self.edges:
                if a not in self.layout or b not in self.layout:continue
                color,width_,dashed=R13_REL_KIND[kind]
                if self.selected and self.selected not in (a,b):color=color+"66"
                x1,y1=self.layout[a][0]+44,self.layout[a][1]+28
                x2,y2=self.layout[b][0]+44,self.layout[b][1]+28
                if not dashed:
                    canvas.line(color,(x1,y1),(x2,y2),width_)
                    continue
                length=max(1.0,((x2-x1)**2+(y2-y1)**2)**.5);step=12.0;i=0.0
                while i<length:
                    j=min(length,i+7.0)
                    canvas.line(color,(x1+(x2-x1)*i/length,y1+(y2-y1)*i/length),(x1+(x2-x1)*j/length,y1+(y2-y1)*j/length),width_)
                    i+=step
            return rv

transform r13_rel_gray:
    matrixcolor SaturationMatrix(0.0)*BrightnessMatrix(-0.12)

transform r13_rel_faded:
    alpha .45

screen r13_relations_content(owner,selected,filt):
    $ layout=r13_rel_layout()
    $ edges=r13_rel_edges()
    $ people=r13_rel_people()
    $ selected=selected if selected in people else next((p for p in people if r13_rel_status(p)[0]=="dead"),"daram")
    $ counts=r13_rel_counts()
    hbox:
        xpos 280 ypos 84 spacing 8
        for key,title in (("all","전체 %d"%counts["all"]),("alive","살아 있음 %d"%counts["alive"]),("dead","숨짐 %d"%counts["dead"]),("saved","구함 %d"%counts["saved"])):
            textbutton title style "r13_paper_tab_button" xsize 124 ysize 38 text_size 16 selected filt==key action Function(r13_record_select,owner,"rel_filter",key)
    add R13PaperFrame() xpos 278 ypos 128 xsize 536 ysize 452
    fixed:
        xpos 286 ypos 138 xsize R13_REL_COLS*R13_REL_CELL[0] ysize R13_REL_ROWS*R13_REL_CELL[1]
        add R13RelLines(edges,layout,selected)
        for who in people:
            $ x,y=layout[who]
            $ kind,label=r13_rel_status(who)
            button:
                xpos x ypos y xysize R13_REL_CELL padding (0,0) background None
                action Function(r13_record_select,owner,"rel_sel",who)
                at (r13_rel_faded if not r13_rel_match(who,filt) else None)
                fixed:
                    xysize R13_REL_CELL
                    if who==selected:
                        add Solid("#e2a93b") xpos 13 ypos -3 xysize (62,62)
                    add Solid({"dead":"#8b8b8b","saved":"#3f7a4a","with":"#b2862e"}.get(kind,"#6b5137")) xpos 16 ypos 0 xysize (56,56)
                    add Solid("#e9dbb9") xpos 18 ypos 2 xysize (52,52)
                    if kind=="dead":
                        add Transform(r13_art(who,"avatar_neutral"),xysize=(52,52),fit="contain",nearest=True) at r13_rel_gray xpos 18 ypos 2
                        add Transform(Solid("#a2401f"),xysize=(64,6),rotate=45) xpos 14 ypos 0
                        add Transform(Solid("#a2401f"),xysize=(64,6),rotate=-45) xpos 14 ypos 0
                    elif kind in ("gone","missing"):
                        add Transform(r13_art(who,"avatar_neutral"),xysize=(52,52),fit="contain",nearest=True,alpha=.6) xpos 18 ypos 2
                    else:
                        add Transform(r13_art(who,"avatar_neutral"),xysize=(52,52),fit="contain",nearest=True) xpos 18 ypos 2
                    text (("{s}"+R13_NAMES.get(who,who)+"{/s}") if kind=="dead" else R13_NAMES.get(who,who)) xpos 44 xanchor .5 ypos 57 size 15 color ("#8a8178" if kind in ("dead","gone") else "#493b30") outlines [(2,"#f4ead2",0,0)]
                    if label:
                        text label xpos 44 xanchor .5 ypos 73 size 12 color {"dead":"#7a2e22","saved":"#3f7a4a","with":"#8a6420"}.get(kind,"#5d6a8a") outlines [(2,"#f4ead2",0,0)]
        for a,b,kind,lab in edges:
            # Neighbouring faces leave no room for a label; the detail list names every line.
            if selected in (a,b) and a in layout and b in layout and abs(layout[a][0]-layout[b][0])+abs(layout[a][1]-layout[b][1])>R13_REL_CELL[0]*1.5:
                $ mx=(layout[a][0]+layout[b][0])//2+44
                $ my=(layout[a][1]+layout[b][1])//2+28
                frame:
                    xpos mx ypos my xanchor .5 yanchor .5 padding (4,1) background Solid("#f4ead2e6")
                    text lab size 13 color R13_REL_KIND[kind][0]
    use r13_relation_detail(selected)
    hbox:
        xpos 282 ypos 590 spacing 14
        for kind,title in (("family","가족"),("work","함께 일함·도움"),("suspect","의심·갈등")):
            hbox:
                spacing 5
                add Solid(R13_REL_KIND[kind][0]) xysize (22,4 if kind!="family" else 6) yalign .5
                text title size 14 color "#65503b"
        text "{color=#7a2e22}✕ 숨짐{/color}  {color=#3f7a4a}초록 · 구함{/color}  {color=#5d6a8a}흐림 · 행방 모름{/color}" size 14

screen r13_relation_detail(person):
    add R13PaperFrame() xpos 820 ypos 58 xsize 406 ysize 512
    if person:
        $ kind,label=r13_rel_status(person)
        fixed:
            xpos 842 ypos 78 xysize (110,110)
            add Solid({"dead":"#8b8b8b","saved":"#3f7a4a","with":"#b2862e"}.get(kind,"#6b5137")) xysize (110,110)
            add Solid("#e9dbb9") xpos 3 ypos 3 xysize (104,104)
            if kind=="dead":
                add Transform(r13_art(person,"avatar_neutral"),xysize=(104,104),fit="contain",nearest=True) at r13_rel_gray xpos 3 ypos 3
            else:
                add Transform(r13_art(person,"avatar_neutral"),xysize=(104,104),fit="contain",nearest=True) xpos 3 ypos 3
        text (("{s}"+R13_NAMES.get(person,person)+"{/s}") if kind=="dead" else R13_NAMES.get(person,person)) xpos 966 ypos 92 size r13_read_size(24,28) color ("#8a8178" if kind in ("dead","gone") else "#6c512a")
        text (R13_PUBLIC_ROLES.get(person) or "") xpos 966 ypos 132 size 16 color "#7d6a52" xsize 240
        if label:
            frame:
                xpos 842 ypos 200 xsize 362 padding (10,6)
                background Solid({"dead":"#7a2e22","saved":"#3f7a4a","with":"#8a6420"}.get(kind,"#5d6a8a"))
                text label size 17 color "#fff6ea"
        viewport:
            area (844,248,358,300) mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 8
                text "관계" size 17 color "#765426"
                $ rows=r13_rel_lines_of(person)
                if rows:
                    for other,k,lab in rows:
                        hbox:
                            spacing 6
                            add Solid(R13_REL_KIND[k][0]) xysize (12,4) yalign .5
                            text (R13_NAMES.get(other,other)+" · "+lab) size 16 color "#493b30" xsize 320
                else:
                    text "아직 알게 된 관계가 없다." size 16 color "#7d6a52"
                $ first=next((m for m in room13.get("encounters",[]) if isinstance(m,dict) and m.get("person")==person),None)
                if first:
                    text "처음 만남" size 17 color "#765426"
                    text ("%d일 · %s · %s"%(first["day"],("오전","오후","저녁","늦은 저녁")[first["period"]],R13_PLACES.get(first["place"],(first["place"],))[0])) size 16 color "#493b30"
    else:
        text "만난 사람이 생기면 관계도가 채워집니다." xpos 846 ypos 278 xsize 354 text_align .5 size 20 color "#625738"
