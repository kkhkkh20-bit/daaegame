# 0.18.91 수첩 · 관계도 (소유자 2026-10-17 승인 시안 docs/relation-mock 참고)
# - 만난 주민의 얼굴을 자리표(6×5)에 놓고, 알게 된 관계만 선으로 잇는다.
#   가족=금색 굵은 선, 함께 일함·도움=푸른 선, 의심·갈등=붉은 점선.
# - 숨짐: 회색 얼굴 + 붉은 X + 이름 취소선 + 언제. 구함: 초록 테두리. 행방 모름: 흐림.
# - 관계는 그 사실을 알게 된 뒤(자료·대화·장면 표식)에만 생긴다. 이야기 판정에는 쓰지 않는다.
init 166 python:
    R13_REL_DEAD = dict(R13_DEATH_FLAGS)
    R13_REL_DEAD.update({"resident_lamplighter":"chorong_dead","resident_ttadak":"ttadak_dead",
        "kid_kkomi":"kkomi_dead","kid_dodam":"dodam_dead","npc_pandol":"pandol_dead",
        # 0.19.15: ⑤ 수프에서 아무도 깨우지 못한 판(soup_kids_dead)에는 깜이·몽이·방울도 숨진다.
        "kid_kkam":"soup_kids_dead","kid_mong":"soup_kids_dead","kid_bang":"soup_kids_dead"})
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
        # 0.18.99 더한 관계 (모두 이미 있는 자료·장면에서 알게 되는 것)
        ("granny","mom","suspect","엄마 이름으로 편지를 씀",_r13_rel_any("J06","N06")),
        ("mom","resident_guldol","work","밤새 돌을 함께 지켜봄",_r13_rel_any("Y07")),
        ("resident_nubi","kid_nubi1","family","엄마와 큰아이",_r13_rel_any("F11")),
        ("resident_nubi","neoul","suspect","아이들 몫을 주겠다는 약속",_r13_rel_any("F12","F01")),
        ("resident_teacher","kid_saemi","work","담임",_r13_rel_any("Y13")),
        ("resident_seori","resident_teacher","suspect","약장 출입 명단",_r13_rel_any("Y12")),
        ("resident_eunho","resident_guseul","work","다른 장부를 꺼내 옴",_r13_rel_any("V03")),
        ("resident_badook","guard","work","같은 순찰",lambda:True),
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
    R13_REL_COLS, R13_REL_ROWS, R13_REL_CELL = 6, 5, (96, 82)
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
        # 0.19.2 (owner): everyone actually met appears (Karo, 꽥순 …), not only the seated cast.
        people+=[p for p in met if p not in R13_REL_SLOTS]
        return people

    def r13_rel_face(person):
        """0.19.2 (owner): no picture of Mom on the chart until the family has met her."""
        if person=="mom" and r13_rel_status("mom")[0]=="missing":
            return Fixed(Solid("#d9c7a2"),Text("?",size=40,color="#7d6a52",xalign=.5,yalign=.5,font=r13_ui_font()),xysize=(80,80))
        return r13_art(person,"avatar_neutral")

    def r13_rel_layout():
        """person -> (x, y) slot origin inside the graph area."""
        used={};free=[(c,r) for r in range(R13_REL_ROWS) for c in range(R13_REL_COLS)]
        people=r13_rel_people()
        for p in people:
            if p in R13_REL_SLOTS:
                used[p]=R13_REL_SLOTS[p];free.remove(R13_REL_SLOTS[p])
        # 0.19.8: more people than cells raised KeyError on the full chart. People with a known relation
        # get the free cells first; the rest stay in the face row under the chart.
        linked={x for a,b,k,l in r13_rel_edges() for x in (a,b)}
        for p in sorted(people,key=lambda p:p not in linked):
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
        def __init__(self,edges,layout,selected=None,centres=None,**kwargs):
            super(R13RelLines,self).__init__(**kwargs)
            self.edges=edges;self.layout=layout;self.selected=selected;self.centres=centres or {}
        def render(self,width,height,st,at):
            w=R13_REL_COLS*R13_REL_CELL[0];h=R13_REL_ROWS*R13_REL_CELL[1]
            rv=renpy.Render(w,h);canvas=rv.canvas()
            for a,b,kind,label in self.edges:
                if a not in self.layout or b not in self.layout:continue
                color,width_,dashed=R13_REL_KIND[kind]
                active=self.selected in (a,b)
                if self.selected and not active:color=color+"44"
                width_=width_+1 if active else max(2,width_-1)
                ax,ay=self.centres.get(a,(48,28));bx,by=self.centres.get(b,(48,28))
                x1,y1=self.layout[a][0]+ax,self.layout[a][1]+ay
                x2,y2=self.layout[b][0]+bx,self.layout[b][1]+by
                if not dashed:
                    canvas.line(color,(x1,y1),(x2,y2),width_)
                    continue
                length=max(1.0,((x2-x1)**2+(y2-y1)**2)**.5);step=12.0;i=0.0
                while i<length:
                    j=min(length,i+7.0)
                    canvas.line(color,(x1+(x2-x1)*i/length,y1+(y2-y1)*i/length),(x1+(x2-x1)*j/length,y1+(y2-y1)*j/length),width_)
                    i+=step
            return rv

    class R13RelKey(renpy.Displayable):
        def __init__(self,kind,**kwargs):
            super(R13RelKey,self).__init__(**kwargs)
            self.kind=kind
        def render(self,width,height,st,at):
            rv=renpy.Render(28,12);c=rv.canvas()
            color,weight,dashed=R13_REL_KIND[self.kind]
            if dashed:
                for x in (0,11,22):c.line(color,(x,6),(min(27,x+6),6),3)
            else:c.line(color,(0,6),(27,6),3 if self.kind=="family" else 2)
            return rv

transform r13_rel_gray:
    matrixcolor SaturationMatrix(0.0)*BrightnessMatrix(-0.12)

transform r13_rel_faded:
    alpha .45

# Presentation only: knowledge gates, status rules and fixed seats remain above.
screen r13_relations_content(owner,selected,filt,focused=True):
    $ layout=r13_rel_layout()
    $ edges=r13_rel_edges()
    $ people=r13_rel_people()
    $ selected=selected if selected in people else "daram"
    $ linked={other for other,k,lab in r13_rel_lines_of(selected)}
    $ counts=r13_rel_counts()
    text "알게 된 관계" xpos 282 ypos 66 size r13_read_size(23,26) color "#654b30"
    textbutton ("전체 관계도" if focused else "인물 중심"):
        style "r13_paper_tab_button" xpos 704 ypos 62 xsize 160 ysize 40 padding (4,0) text_size 19 text_yalign .5
        action Function(r13_record_select,owner,"rel_focus",not focused)
    hbox:
        xpos 280 ypos 104 spacing 8
        for key,title in (("all","전체 %d"%counts["all"]),("alive","살아 있음 %d"%counts["alive"]),("dead","숨짐 %d"%counts["dead"]),("saved","구함 %d"%counts["saved"])):
            textbutton title style "r13_paper_tab_button" xsize 140 ysize 40 padding (4,0) text_size r13_read_size(17,19) text_align .5 text_yalign .5 selected filt==key action Function(r13_record_select,owner,"rel_filter",key)
    add R13PaperFrame() xpos 278 ypos 150 xsize 588 ysize 428
    if focused:
        use r13_relation_focus(owner,selected,filt)
    else:
      fixed:
        xpos 284 ypos 158 xsize R13_REL_COLS*R13_REL_CELL[0] ysize R13_REL_ROWS*R13_REL_CELL[1]
        add R13RelLines(edges,layout,selected)
        for who in [p for p in people if p in layout]:
            $ x,y=layout[who]
            $ kind,label=r13_rel_status(who)
            $ faded=not r13_rel_match(who,filt)
            $ name=r13_display_name(who)
            $ two_lines=" " in name and len(name)>5
            $ face=44 if two_lines else 50
            button:
                xpos x ypos y xysize R13_REL_CELL padding (0,0) background None
                action Function(r13_record_select,owner,"rel_sel",who)
                alt (r13_display_name(who)+( " · "+label if label else ""))
                at (r13_rel_faded if faded else None)
                fixed:
                    xysize R13_REL_CELL
                    # A small paper mount keeps names legible over passing lines.
                    add R13PaperPanel(who==selected) xpos 10 ypos 0 xysize (76,78)
                    if who==selected:
                        add Solid("#ad843f") xpos 10 ypos 0 xysize (3,78)
                    if who in linked:
                        $ link_kind=next(k for other,k,lab in r13_rel_lines_of(selected) if other==who)
                        add Solid(R13_REL_KIND[link_kind][0]) xpos 10 ypos 0 xysize (76,3)
                    add Solid({"dead":"#94887b","saved":"#4d765c","with":"#ad843f"}.get(kind,"#b69b75")) xpos (46-face//2) ypos 3 xysize (face+4,face+2)
                    add Solid("#ead7b3") xpos (48-face//2) ypos 5 xysize (face,face-2)
                    if kind=="dead":
                        add Transform(r13_rel_face(who),xysize=(face,face-2),fit="contain",nearest=r13_profile_nearest(who)) at r13_rel_gray xpos (48-face//2) ypos 5
                    else:
                        add Transform(r13_rel_face(who),xysize=(face,face-2),fit="contain",nearest=r13_profile_nearest(who),alpha=.55 if kind in ("gone","missing") else 1.0) xpos (48-face//2) ypos 5
                    if kind in ("dead","saved","gone","missing"):
                        frame:
                            xpos 62 ypos 36 xysize (22,22) padding (0,0)
                            background Solid({"dead":"#874a3b","saved":"#4d765c"}.get(kind,"#726f78"))
                            if kind=="saved":
                                add R13AntiqueIcon("check",size=18) align (.5,.5)
                            else:
                                text ("×" if kind=="dead" else "?") size 20 color "#fff0d2" align (.5,.5)
                    $ node_name=name.replace(" ","\n",1) if two_lines else name
                    text (("{s}"+node_name+"{/s}") if kind=="dead" else node_name) xpos 48 xanchor .5 ypos (48 if two_lines else 57) xsize 94 text_align .5 size 16 line_spacing -2 color ("#817366" if kind in ("dead","gone") else "#493b30")
    use r13_relation_detail(owner,selected)
    hbox:
        xpos 284 ypos 599 spacing 22
        for kind,title in (("family","가족"),("work","함께 일함·도움"),("suspect","의심·갈등")):
            hbox:
                spacing 7
                add R13RelKey(kind) yalign .5
                text title size r13_read_size(16,18) color "#65503b"
    text ("아래 얼굴을 누르면 그 인물의 관계를 봅니다." if focused else "인물을 고른 뒤 「인물 중심」으로 크게 봅니다.") xpos 284 ypos 630 size r13_read_size(16,18) color "#79654e"

screen r13_relation_focus(owner,person,filt):
    $ rows=r13_rel_lines_of(person)
    $ positions=([(20,112)] if len(rows)==1 else [(20,112),(440,112)] if len(rows)==2 else [(20,12),(20,178),(440,92)] if len(rows)==3 else [(20,12),(440,12),(20,178),(440,178)])
    $ layout={person:(222,92)}
    $ layout.update({other:positions[i] for i,(other,k,lab) in enumerate(rows[:4])})
    fixed:
        xpos 284 ypos 158 xysize (576,326)
        add R13RelLines([(person,other,k,lab) for other,k,lab in rows[:4]],layout,person,{p:((66,56) if p==person else (56,40)) for p in layout})
        use r13_relation_focus_card(owner,person,222,92,True)
        for i,(other,k,lab) in enumerate(rows[:4]):
            $ nx,ny=positions[i]
            use r13_relation_focus_card(owner,other,nx,ny)
            frame:
                xpos (0 if nx<200 else 382) ypos (ny+108) xsize 194 padding (6,4) background Solid("#f0dfbd")
                text lab size r13_read_size(17,19) text_align .5 xalign .5 color R13_REL_KIND[k][0] xsize 180
        if not rows:
            text "아직 알게 된 관계가 없습니다." xpos 110 ypos 245 xsize 356 text_align .5 size r13_read_size(20,23) color "#79654e"
    # A stable index keeps unrelated residents reachable without tiny graph text.
    viewport:
        id "r13_relation_index"
        area (288,488,572,88) mousewheel "horizontal" draggable True scrollbars "horizontal" scrollbar_ysize 6 scrollbar_thumb Solid("#a89571") scrollbar_base_bar Solid("#d6bd96")
        hbox:
            spacing 6
            for who in r13_rel_people():
                $ status=r13_rel_status(who)[0]
                button:
                    xysize (76,80) padding (4,4)
                    background R13PaperPanel(who==person) hover_background R13PaperPanel(True)
                    action Function(r13_record_select,owner,"rel_sel",who)
                    alt r13_display_name(who)
                    at (r13_rel_faded if not r13_rel_match(who,filt) else None)
                    vbox:
                        spacing 4 xalign .5
                        if status=="dead":
                            add Transform(r13_rel_face(who),xysize=(44,44),fit="contain",nearest=r13_profile_nearest(who)) at r13_rel_gray xalign .5
                        else:
                            add Transform(r13_rel_face(who),xysize=(44,44),fit="contain",nearest=r13_profile_nearest(who),alpha=.55 if status in ("gone","missing") else 1.0) xalign .5
                        text (("{s}"+r13_display_name(who).split(" ")[0]+"{/s}") if status=="dead" else r13_display_name(who).split(" ")[0]) size 16 color "#493b30" xalign .5

screen r13_relation_focus_card(owner,person,x,y,primary=False):
    $ kind,label=r13_rel_status(person)
    $ compact=" " in r13_display_name(person) and len(r13_display_name(person))>5
    $ face=(64 if compact else 80) if primary else (50 if compact else 60)
    button:
        xpos x ypos y xysize ((132,132) if primary else (112,106)) padding (5,5)
        background R13PaperPanel(primary) hover_background R13PaperPanel(True)
        action Function(r13_record_select,owner,"rel_sel",person)
        alt (r13_display_name(person)+(" · "+label if label else ""))
        vbox:
            xalign .5 spacing 5
            if kind=="dead":
                add Transform(r13_rel_face(person),xysize=(face,face),fit="contain",nearest=r13_profile_nearest(person)) at r13_rel_gray xalign .5
            else:
                add Transform(r13_rel_face(person),xysize=(face,face),fit="contain",nearest=r13_profile_nearest(person),alpha=.55 if kind in ("gone","missing") else 1.0) xalign .5
            text (("{s}"+r13_display_name(person)+"{/s}") if kind=="dead" else r13_display_name(person)) size (r13_read_size(20,22) if primary else r13_read_size(18,20)) xsize (122 if primary else 102) text_align .5 color "#493b30"

screen r13_relation_detail(owner,person):
    add R13PaperFrame() xpos 878 ypos 58 xsize 348 ysize 520
    if person:
        $ kind,label=r13_rel_status(person)
        fixed:
            xpos 900 ypos 80 xysize (84,84)
            add R13PaperPanel() xysize (84,84)
            if kind=="dead":
                add Transform(r13_rel_face(person),xysize=(76,76),fit="contain",nearest=r13_profile_nearest(person)) at r13_rel_gray xpos 4 ypos 4
            else:
                add Transform(r13_rel_face(person),xysize=(76,76),fit="contain",nearest=r13_profile_nearest(person),alpha=.6 if kind in ("gone","missing") else 1.0) xpos 4 ypos 4
        text r13_display_name(person) xpos 998 ypos 85 xsize 206 size r13_read_size(24,27) color "#654b30"
        text r13_display_role(person) xpos 998 ypos 123 size r13_read_size(16,18) color "#7d6a52" xsize 206
        add Solid("#c8ac7f") xpos 900 ypos 179 xysize (302,1)
        if label:
            frame:
                xpos 900 ypos 192 xsize 302 padding (10,7)
                background Solid({"dead":"#874a3b","saved":"#4d765c","with":"#8a6c3d"}.get(kind,"#696a77"))
                text label size r13_read_size(18,20) color "#fff3dc"
        viewport:
            area (900,246,306,308) mousewheel True draggable True scrollbars "vertical" vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                $ rows=r13_rel_lines_of(person)
                text ("이어진 관계 · %d"%len(rows)) size r13_read_size(19,22) color "#765426"
                if rows:
                    for other,k,lab in rows:
                        button:
                            xsize 286 padding (10,9) background R13PaperPanel() hover_background R13PaperPanel(True)
                            action Function(r13_record_select,owner,"rel_sel",other)
                            alt (r13_display_name(other)+" · "+lab)
                            vbox:
                                spacing 5
                                hbox:
                                    spacing 9
                                    add R13RelKey(k) yalign .5
                                    text (r13_display_name(other)+"  ›") size r13_read_size(19,22) color "#493b30"
                                text lab size r13_read_size(17,20) color "#766149" xsize 264
                else:
                    text "아직 알게 된 관계가 없다." size r13_read_size(18,21) color "#7d6a52" xsize 286
                $ materials=r13_person_materials(person)
                if materials:
                    text "남긴 증언" size r13_read_size(19,22) color "#765426"
                    for record in materials:
                        textbutton (R13_RECORD_SHORT.get(record,r13_catalog_title(record))+"  ›"):
                            style "r13_paper_tab_button" xsize 286 ysize 58 text_size r13_read_size(18,20)
                            action Function(r13_open_person_material,owner,record)
                $ first=next((m for m in room13.get("encounters",[]) if isinstance(m,dict) and m.get("person")==person),None)
                if first:
                    null height 4
                    text "처음 만남" size r13_read_size(19,22) color "#765426"
                    text ("%d일 · %s\n%s"%(first["day"],("오전","오후","저녁","늦은 저녁")[first["period"]],R13_PLACES.get(first["place"],(first["place"],))[0])) size r13_read_size(18,21) color "#493b30" xsize 286
                null height 4
                use r13_person_brief(person)
    else:
        text "만난 사람이 생기면 관계도가 채워집니다." xpos 900 ypos 278 xsize 302 text_align .5 size 20 color "#625738"
