# 0.18.99 3번 시안 적용 (소유자 2026-10-17 "3번 시안 다 좋아 적용해줘")
#  ① 반박 컷인 "그 말, 맞지 않습니다!"   (회의에서 발언 하나를 무너뜨린 순간)
#  ② 기록 거름: 0.19.2에 한 줄로 합침(room13_notebook.rpy r13_material_filters). 보여줄 때는 관련 자료를 앞에.
#  ③ 큰 글씨(휴대폰 기본값)에서 아래 단추·기록 단추를 크게
#  ④ 다시 시작할 아침: 하루를 처음 자유롭게 움직이는 때 숨은 저장을 남기고, 그 아침으로 돌아간다
#  ⑤ 이번 겨울의 이름 판: 결말 뒤 구한 사람·잃은 사람·에피소드별 결과
default persistent.r13_mornings = {}

init 172 python:
    import random as _r13_random
    import re as _r13_re

    def r13_big_ui():
        return bool(persistent.room13_large_text)

    # ① -------------------------------------------------------------
    def r13_cutin_music_pause(on):
        try:renpy.music.set_pause(on,channel="music")
        except Exception:pass

    # ② -------------------------------------------------------------
    def r13_record_related(key,person):
        name=R13_NAMES.get(person)
        ev=ROOM13["evidence"].get(key)
        if not name or not ev:return False
        pending=getattr(store,"r13_present_priority",None)
        if pending and pending[0]==person and key in pending[1]:return True
        src=(store.room13 or {}).get("records",{}).get(key,{}).get("source","") or ""
        return name in " ".join((ev.get("name",""),ev.get("establishes",""),str(src)))

    def r13_record_related_first(entries,person):
        """Present screen: records naming the person (or queued for them) come first; nothing is hidden."""
        rel=[k for k in entries if r13_record_related(k,person)]
        return rel+[k for k in entries if k not in rel]

    def r13_book_person(target,hearing):
        if hearing:
            claim=getattr(store,"r13_meeting_claim",None);sid=getattr(store,"r13_debate_selected",None)
            if claim and sid:
                try:return r13_debate_statement(claim,sid)["who"]
                except Exception:return None
            return None
        return target if target in R13_NAMES else None

    # ④ -------------------------------------------------------------
    R13_DAY_TAGS = {1:"도착",2:"①",3:"①②",4:"①②③",5:"②③",6:"③",7:"13호 사건",
        8:"④",9:"④",10:"④ 재판",11:"⑤",12:"⑤",13:"⑥",14:"제단"}

    def r13_morning_slot(day):
        return "r13morning-%d"%day

    def r13_morning_record():
        rec=persistent.r13_mornings
        return rec if isinstance(rec,dict) else {}

    def r13_morning_due():
        s=store.room13
        if not s or not getattr(store,"room13_mode",False) or getattr(store,"r13_meeting_active",False):return False
        if not r13_shortcut_field():return False
        rec=r13_morning_record();tok=s.get("run_token")
        return not (tok and rec.get("token")==tok and s.get("day",1) in rec.get("days",[]))

    def r13_morning_snapshot():
        if not r13_morning_due():return
        if not store.room13.get("run_token"):
            r13_edit(run_token="%012x"%_r13_random.getrandbits(48))
            renpy.retain_after_load()
        tok=store.room13["run_token"];day=store.room13.get("day",1)
        rec=dict(r13_morning_record())
        if rec.get("token")!=tok:rec=dict(token=tok,days=[])
        try:
            renpy.save(r13_morning_slot(day),extra_info="%d일 아침"%day)
        except Exception:
            return
        rec["days"]=sorted(set(rec.get("days",[]))|{day})
        persistent.r13_mornings=rec
        renpy.save_persistent()

    def r13_morning_days():
        s=store.room13 or {}
        rec=r13_morning_record()
        if not s.get("run_token") or rec.get("token")!=s.get("run_token"):return []
        return [d for d in rec.get("days",[]) if renpy.can_load(r13_morning_slot(d))]

    def r13_morning_restore(day):
        # Later mornings belong to the timeline being left; take them again when reached.
        rec=dict(r13_morning_record());rec["days"]=[d for d in rec.get("days",[]) if d<=day]
        persistent.r13_mornings=rec
        renpy.save_persistent()
        renpy.load(r13_morning_slot(day))

    config.overlay_screens.append("r13_morning_watch")

    # ⑤ -------------------------------------------------------------
    # (번호, 이름, 회의, 자료 앞 글자, 사건이 시작됐다는 표식, 이 사건에서 구하거나 잃을 수 있는 사람)
    R13_BOARD_EPISODES = (
        ("①","등 도둑","Q1","L",("lt_open","lt_dawn","lt_done"),("resident_piko","resident_librarian")),
        ("②","다람 탐정단","Q2","K",("kd_started","kd_done"),()),
        ("③","장작 창고의 불","Q3","F",("wf_fire","wf_done"),("kid_kkomi",)),
        ("④","13호의 밤","Q4","N",("nt_night8","nt_dawn8","nt_after"),("resident_lamplighter","resident_ttadak")),
        ("⑤","겨울 수프","Q5","Y",("ws_soup","ws_long_night","ws_done"),("resident_teacher","resident_nero","kid_dodam","kid_kkam","kid_mong","kid_bang","kid_kkomi")),
        ("⑥","끌려가는 수레","Q6","V",("cv_morning","cart_stopped"),("resident_badook",)),
    )

    def r13_board_keys(prefix):
        pat=_r13_re.compile(prefix+r"\d\d$")
        return [k for k in ROOM13["evidence"] if pat.match(k)]

    def r13_board_meeting_held(claim):
        if claim not in R13_DEBATE:return False
        d=r13_debate_state()
        return (claim in (store.room13 or {}).get("propositions",[]) or bool(d["broken"].get(claim))
            or bool(d["pressed"].get(claim)) or r13_debate_closed(claim))

    def r13_board_status(claim,person):
        """그 사건 칸에서의 결과. ③에서 구한 꼬미가 ⑤에서 숨지면 ③은 구함, ⑤는 잃음(0.19.15)."""
        if person=="kid_kkomi" and claim=="Q5":
            return "dead" if r13_has("kkomi_dead_soup") else None
        if person=="kid_kkomi" and claim=="Q3" and r13_has("kkomi_dead_soup"):
            return "saved"
        if person in ("kid_kkam","kid_mong","kid_bang") and claim!="Q5":
            return None
        return r13_rel_status(person)[0]

    def r13_board_result(claim,people):
        s=store.room13 or {}
        parts=[]
        if claim in s.get("propositions",[]):
            point=R13_DEBATE.get(claim,{}).get("conclusion",{}).get("point")
            parts.append(("%s 입증"%R13_NAMES.get(point["who"],"")) if point else "밤이 무죄" if claim=="Q2" else "입증")
        elif r13_board_meeting_held(claim):
            parts.append("입증 못 함")
        if claim=="Q2":
            if r13_has("bami_taken"):parts.append("밤이 끌려감")
            if r13_has("musoe_gone"):parts.append("무쇠 할아버지 떠남")
        if claim=="Q6":
            if r13_has("cart_stopped"):parts.append("수레 멈춤")
            elif r13_has("cv_night"):parts.append("수레 떠남")
        saved=[R13_NAMES.get(p,p) for p in people if r13_board_status(claim,p)=="saved"]
        lost=[R13_NAMES.get(p,p) for p in people if r13_board_status(claim,p)=="dead"]
        if saved:parts.append("·".join(saved)+" 구함")
        if lost:parts.append("·".join(lost)+" 잃음")
        return " · ".join(parts) or "—"

    def r13_board_rows():
        s=store.room13 or {}
        owned=set(s.get("evidence",[]))
        rows=[]
        for mark,title,claim,prefix,started,people in R13_BOARD_EPISODES:
            keys=r13_board_keys(prefix)
            found=sum(1 for k in keys if k in owned)
            reached=found>0 or any(r13_has(f) for f in started)
            if r13_board_meeting_held(claim):
                done,total=r13_debate_progress(claim);left=str(total-done)
            else:
                left="—"
            rows.append(dict(mark=mark,title=title,reached=reached,
                found=("%d / %d"%(found,len(keys)) if reached else "—"),left=(left if reached else "—"),
                result=(r13_board_result(claim,people) if reached else "지나치지 않았다")))
        return rows

    def r13_board_people(kind):
        pool=R13_REL_SAVED if kind=="saved" else R13_REL_DEAD
        return [p for p in pool if p in R13_NAMES and r13_rel_status(p)[0]==kind]

# ① ---------------------------------------------------------------
transform r13_cutin_shake:
    xoffset 0
    linear .04 xoffset -10
    linear .04 xoffset 9
    linear .04 xoffset -6
    linear .04 xoffset 4
    linear .04 xoffset 0

transform r13_cutin_banner(motion=True):
    rotate -6 xanchor .5 yanchor .5 xpos 640 ypos 300
    alpha 1.0
    xoffset (-1500 if motion else 0)
    easein (.14 if motion else 0) xoffset 0

transform r13_cutin_card(motion=True):
    alpha (0.0 if motion else 1.0)
    pause (.12 if motion else 0)
    linear (.08 if motion else 0) alpha 1.0

screen r13_rebuttal_cutin(struck):
    zorder 150
    $ motion=bool(persistent.room13_motion)
    fixed:
        if motion:
            at r13_cutin_shake
        add Solid("#00000038")
        for angle in range(0,180,12):
            add Transform(Solid("#fff3d2",xsize=1700,ysize=5),rotate=angle,alpha=.55) xanchor .5 yanchor .5 xpos 640 ypos 330
        fixed:
            xysize (1700,150)
            at r13_cutin_banner(motion)
            add Solid("#d9a648",xsize=1700,ysize=150)
            add Solid("#8a2f1f",xsize=1700,ysize=128) ypos 11
            text "그 말, 맞지 않습니다!" xalign .5 yalign .5 size 74 color "#fff3dc" font r13_ui_font() outlines [(4,"#3a1a10",0,3)]
        frame:
            xalign .5 ypos 430 padding (22,12) background R13PaperFrame()
            at r13_cutin_card(motion)
            text ("{s}"+struck+"{/s}") size r13_read_size(25,29) color "#7a2c1c" font r13_ui_font() xmaximum 900

label r13_rebuttal_cutin_play(claim,sid):
    if renpy.is_skipping() or r13_fast_all:
        return
    $ r13_cutin_text=r13_debate_statement(claim,sid)["text"].replace("【","").replace("】","")
    show screen r13_rebuttal_cutin(r13_cutin_text)
    $ source_fx("impact")
    $ r13_cutin_music_pause(True)
    $ renpy.pause(.9 if persistent.room13_motion else .6)
    hide screen r13_rebuttal_cutin
    $ r13_cutin_music_pause(False)
    return

# ④ ---------------------------------------------------------------
screen r13_morning_watch():
    if room13_mode and r13_morning_due():
        timer .4 action Function(r13_morning_snapshot)

screen r13_morning_pick():
    style_prefix "r13"
    modal True
    zorder 120
    $ days=r13_morning_days()
    $ today=(room13 or {}).get("day",1)
    default pick=None
    default asking=False
    $ chosen=pick if pick in days else (max(days) if days else None)
    add Solid("#0b151bb0")
    frame:
        area (140,70,1000,560) padding (30,24) background R13PaperFrame()
        vbox:
            spacing 12
            text "다시 시작할 아침" size 32 color "#6c512a" font r13_ui_font()
            text "지나온 날의 아침으로 돌아간다. 그 뒤에 얻은 기록과 결과는 사라지고, 그날 아침의 수첩으로 다시 시작한다." size r13_read_size(17,20) color "#795d40" xsize 930
            grid 7 2:
                spacing 12
                for day in range(1,15):
                    $ ok=day in days
                    button:
                        xsize 120 ysize 112 padding (6,8)
                        background R13PaperPanel(chosen==day)
                        action ([SetScreenVariable("pick",day),SetScreenVariable("asking",False)] if ok else NullAction()) sensitive ok
                        vbox:
                            xalign .5 yalign .5 spacing 6
                            text ("%d일"%day) size r13_read_size(28,32) color ("#493b30" if ok else "#a99a83") xalign .5
                            text (R13_DAY_TAGS.get(day,"") if ok else ("아직" if day>today else "기록 없음")) size r13_read_size(15,18) color ("#65503b" if ok else "#a99a83") xalign .5
            # The confirmation lives inside this panel: Ren'Py's confirm screen would sit under it.
            if asking and chosen:
                text ("%d일 아침으로 돌아갈까요? 지금 진행은 저장하지 않으면 사라집니다."%chosen) size r13_read_size(19,22) color "#8a2f1f" xalign .5
            hbox:
                xalign .5 spacing 16
                if asking and chosen:
                    textbutton "돌아간다":
                        style "r13_action_button" xsize 260 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                        action Function(r13_morning_restore,chosen)
                    textbutton "그만두기":
                        style "r13_action_button" xsize 200 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                        action SetScreenVariable("asking",False)
                else:
                    textbutton (("%d일 아침부터"%chosen) if chosen else "돌아갈 아침이 없다"):
                        style "r13_action_button" xsize 260 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                        sensitive chosen is not None
                        action SetScreenVariable("asking",True)
                    textbutton "돌아가기":
                        style "r13_action_button" xsize 200 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                        action Hide("r13_morning_pick")
    key "game_menu" action (SetScreenVariable("asking",False) if asking else Hide("r13_morning_pick"))

# ⑤ ---------------------------------------------------------------
screen r13_board_face(who,kind):
    fixed:
        xysize (60,60)
        add Solid("#2f7a45" if kind=="saved" else "#8d8579")
        add r13_g2_profile_transform(r13_art(who,"avatar_neutral"),xysize=(54,54),fit="contain",nearest=r13_profile_nearest(who),matrixcolor=(SaturationMatrix(0.0) if kind=="dead" else IdentityMatrix())) xpos 3 ypos 3
        if kind=="dead":
            add Transform(Solid("#b2442a",xsize=74,ysize=6),rotate=45) xanchor .5 yanchor .5 xpos 30 ypos 30
            add Transform(Solid("#b2442a",xsize=74,ysize=6),rotate=-45) xanchor .5 yanchor .5 xpos 30 ypos 30

screen r13_winter_board(key):
    style_prefix "r13"
    modal True
    zorder 75
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    $ saved=r13_board_people("saved")
    $ lost=r13_board_people("dead")
    add Solid("#111b2280")
    frame:
        area (108,48,1064,624) padding (30,22) background R13PaperFrame()
        vbox:
            spacing 10
            text "이번 겨울의 이름 판" size 34 color "#6c512a" font r13_ui_font()
            text ("결말 %s · %d일 · %s"%(key,(room13 or {}).get("day",14),R13_ENDINGS[key]["title"])) size r13_read_size(16,19) color "#795d40"
            hbox:
                spacing 40
                vbox:
                    spacing 6
                    text ("구한 사람 %d"%len(saved)) size r13_read_size(18,21) color "#2f7a45"
                    hbox:
                        spacing 8
                        for who in saved[:8]:
                            use r13_board_face(who,"saved")
                        if not saved:
                            text "—" size 22 color "#8d8579"
                vbox:
                    spacing 6
                    text ("잃은 사람 %d"%len(lost)) size r13_read_size(18,21) color "#8a2f1f"
                    hbox:
                        spacing 8
                        for who in lost[:8]:
                            use r13_board_face(who,"dead")
                        if len(lost)>8:
                            text ("+%d"%(len(lost)-8)) size 20 color "#8a2f1f" yalign .5
                        if not lost:
                            text "—" size 22 color "#8d8579"
            null height 2
            hbox:
                spacing 0
                text "에피소드" size r13_read_size(17,20) color "#795d40" min_width 220
                text "찾은 자료" size r13_read_size(17,20) color "#795d40" min_width 150
                text "깨지 못한 말" size r13_read_size(17,20) color "#795d40" min_width 150
                text "결과" size r13_read_size(17,20) color "#795d40"
            add Solid("#b39060",xsize=1000,ysize=2)
            for row in r13_board_rows():
                $ ink="#493b30" if row["reached"] else "#a99a83"
                hbox:
                    spacing 0
                    text (row["mark"]+" "+row["title"]) size r13_read_size(18,21) color ink min_width 220
                    text row["found"] size r13_read_size(18,21) color ink min_width 150
                    text row["left"] size r13_read_size(18,21) color ink min_width 150
                    text row["result"] size r13_read_size(17,20) color ink min_width 480 xmaximum 480
                add Solid("#d8c6a2",xsize=1000,ysize=1)
            text "못 찾은 자료가 무엇인지는 보여 주지 않는다. 다시 하면 그 장소를 다른 때에 찾아가 보자." size r13_read_size(15,18) color "#795d40"
            hbox:
                xalign .5 spacing 16
                textbutton "새 여정 시작":
                    style "r13_action_button" xsize 260 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                    action Return("restart") sensitive ready
                textbutton "다시 시작할 아침":
                    style "r13_action_button" xsize 260 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                    action Show("r13_morning_pick") sensitive ready and bool(r13_morning_days())
                textbutton "닫기":
                    style "r13_action_button" xsize 160 ysize (60 if r13_big_ui() else 52) text_size r13_read_size(20,24)
                    action Return("close") sensitive ready
    key "game_menu" action Return("close")
