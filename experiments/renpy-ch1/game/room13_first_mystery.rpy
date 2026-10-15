# A small, complete deduction loop using the existing E04/E37/E05 facts.
# Screen selections are rollback/save-local; only a completed activity spends time.
init 76 python:
    R13_PLAN_ENDPOINTS=("books","flue","kitchen","stove")

    def r13_plan_pair(selected,key):
        if key not in R13_PLAN_ENDPOINTS:return tuple(selected)
        if key in selected:return tuple(k for k in selected if k!=key)
        return tuple((list(selected)+[key])[-2:])

    def r13_plan_check(stage,gap=None,endpoints=(),reason=None):
        if stage==0:
            if gap=="books":return True,"책장 뒤에 실내에서 잰 폭에 포함되지 않은 공간이 남는다."
            return False,"창문 쪽 기준은 같다. 외벽의 끝까지 실내의 폭을 나란히 놓아 보자."
        if stage==1:
            if set(endpoints)=={"books","kitchen"}:return True,"붉은 선은 주방의 걸쇠 표시에서 13호 책장 아래까지 이어진다."
            return False,"회색 관과 붉은 선이 겹친다. 색이 바뀌는 갈림길에서 다른 선으로 옮겨 타지 않았나?"
        if stage==2:
            if reason=="latch":return True,"주방에서 책장 쪽 걸쇠를 움직이는 구조다. 지금도 작동하는지는 현장에서 확인하자."
            return False,"보온용 빈 벽이라면 두 끝의 걸쇠 표시가 설명되지 않는다. 붉은 선의 시작과 끝을 다시 보자."
        return False,"비교할 부분을 선택하자."

    def r13_plan_has_lens():
        return "magnifier" in (store.room13 or {}).get("inspection_items",{}).get("inventory",[])

    def r13_first_mystery_notes():
        s=store.room13 or {};f=set(s.get("flags",[]));e=set(s.get("evidence",[]));rows=[]
        rows.append(dict(title="아내는 이곳에서 어디로 갔을까?",fact="아내의 편지를 따라왔다."+(" 13호 이불에는 집에서 보던 바느질이 남아 있다." if "E03" in e else ""),question="누가 마지막으로 만났을까?",hint="여관 할머니에게 먼저 묻고, 머물렀던 방을 직접 살펴보자.",keys=[k for k in ("E01","E03") if k in e]))
        if r13_secret_route_available() and ("inn_front_door_claim" in f or "observed:room13:books" in f or "E04" in e or "E37" in e):
            fact="할머니는 방에 복도 쪽 문밖에 없다고 했다." if "inn_front_door_claim" in f else "책장 아래에 책처럼 생긴 손잡이가 있다." if "observed:room13:books" in f else "보수 도면에는 주방과 13호를 잇는 선이 있다."
            question="책장은 왜 움직이지 않을까?";hint="방의 책장과 수리점의 보수 도면을 비교해 볼 만하다."
            if "E04" in e:
                fact+=" 도면에는 책장 뒤 빈 공간과 주방에서 이어지는 연결선이 있다."
                question="종이에 그린 장치가 지금도 움직일까?";hint="도면을 부리에게 보여 주거나, 표시된 두 끝을 현장에서 확인하자."
            if "E37" in e:
                fact+=" 주방 레버를 올린 뒤 책장 뒤 문이 실제로 열렸다."
                question="할머니는 이 문을 어떻게 설명할까?";hint="작동을 확인한 기록을 할머니에게 보여 주자."
            if "inn_claim_retracted" in f:
                fact+=" 할머니는 다른 문이 있다는 것을 인정했다."
                question="아내도 이 길을 이용했을까?";hint="문이 있다는 것과 누가 드나들었는지는 별개다. 통로 안의 흔적을 살펴보자."
            rows.append(dict(title="확인한 다른 출입구" if "inn_claim_retracted" in f else "13호실에는 문이 하나뿐일까?",fact=fact,question=question,hint=hint,keys=[k for k in ("E04","E37","E05") if k in e]))
        return rows

    class R13PlanDrawing(renpy.Displayable):
        def __init__(self,stage=0,selected=None,lens=False,**kwargs):
            super(R13PlanDrawing,self).__init__(**kwargs)
            self.stage=stage;self.selected=selected;self.lens=lens
        def render(self,width,height,st,at):
            r=renpy.Render(700,360);c=r.canvas()
            c.rect("#ede3ca",(0,0,700,360))
            for x in range(20,700,20):c.line("#dcd0b7",(x,0),(x,360),1)
            for y in range(20,360,20):c.line("#dcd0b7",(0,y),(700,y),1)
            if self.stage==0:
                c.rect("#7f735b",(70,95,560,65),4)
                c.rect("#7f735b",(70,215,425,65),4)
                c.line("#8b7661",(70,80),(70,308),3)
                c.line("#8b7661",(630,80),(630,308),3)
                c.line("#8b7661",(495,200),(495,308),3)
                if self.selected=="books":c.rect("#b4853b",(498,218,129,59),4)
                elif self.selected=="window":c.rect("#b4853b",(74,218,100,59),4)
                elif self.selected=="center":c.rect("#b4853b",(240,218,120,59),4)
            else:
                # Two floor bands, service void on the right, independent flue.
                c.rect("#7f735b",(45,40,600,265),4)
                c.line("#7f735b",(45,175),(645,175),4)
                c.line("#7f735b",(530,40),(530,305),3)
                c.lines("#777e78",False,[(455,278),(455,68),(300,68)],9)
                c.lines("#a44f3e",False,[(200,272),(579,272),(579,108),(220,108)],5)
                for x,y in ((200,272),(220,108)):
                    c.rect("#a44f3e",(x-10,y-10,20,20),3)
                    if self.lens:
                        c.lines("#563d2b",False,[(x-16,y+18),(x+16,y+18),(x+16,y-18)],4)
                if self.lens:c.rect("#b4853b",(552,84,53,210),3)
            return r

    # Preserve the original activity reward/cost and later case gates.
    ROOM13["activities"]["map"]["special"]="first_plan_comparison"
    ROOM13["activities"]["map"]["title"]="보수 도면을 읽고 기록한다"
    ROOM13["topics"]["mystery:door"]=dict(npc="granny",title="13호실에 다른 문도 있습니까?",day=[1,4],need=["lodging"],give=[],flags=["inn_front_door_claim"],lines=[
        ("dad","13호실에 복도 쪽 말고 다른 문도 있습니까?"),("granny","13호실 문은 복도 쪽 문밖에 없어요. 책장은 무거우니 아이가 기대지 않게 해 주세요.")])
    ROOM13["objects"]["room13"]["bed"]["text"]="이불 안쪽을 붉은 실로 기웠다. 매듭을 두 번 감은 모양까지, 집에서 아내가 하던 바느질과 같다."
    ROOM13["evidence"]["E03"]["establishes"]="13호 이불 안쪽에 집에서 보던 엄마의 바느질과 같은 매듭이 남아 있다"
    _r13_mystery_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        lines=_r13_mystery_topic_lines(key)
        if key=="mystery:door" and r13_has("inn_claim_retracted"):
            return [("dad","책장 뒤 문은 예전에 세탁물을 나르던 길이라고 하셨지요?"),
                ("granny","그래요. 손님이 쓰는 문은 아니라고 아까 말씀드렸잖아요.")]
        return lines

    _r13_mystery_finish_action=r13_finish_action
    def r13_finish_action(key):
        done=key in store.room13.get("done",[])
        _r13_mystery_finish_action(key)
        if key=="map" and not done:r13_flag("first_plan_read","first_plan_compared")

    _r13_mystery_present=r13_present
    def r13_present(person,key,identity=False):
        owns=key in store.room13.get("evidence",[])
        old_flags=set(store.room13.get("flags",[]))
        response=_r13_mystery_present(person,key,identity)
        if not owns or store.room13.get("day",1)>4:return response
        if person=="buri" and key=="E04" and bool({"first_plan_read","first_plan_compared"}&old_flags):
            if "plan_reviewed_with_buri" in old_flags:return [("buri","도면에 표시해 둔 두 끝을 보세요. 한쪽 걸쇠를 풀어도 반대쪽 문은 직접 밀어야 열려요.")]
            r13_flag("plan_reviewed_with_buri")
            return [("dad","도면에 붉게 덧그린 선은 무엇입니까?"),
                ("buri","회색 선은 배관이에요. 붉은 선은 금속 줄이고요.",{"expression":"neutral"}),
                ("dad","두 층 사이에 금속 줄이 왜 필요합니까?"),
                ("buri","멀리 있는 걸쇠를 당길 때 쓰죠. 실제 장치가 아직 남아 있는지는 직접 봐야 해요.")]
        if person=="granny" and key=="E04" and "inn_front_door_claim" in old_flags:
            return [("granny","어머, 옛 도면까지 구해 오셨네.",{"expression":"thinking"}),
                ("dad","도면을 보면 책장 뒤에 공간이 있습니다. 그런데 문은 하나뿐이라고 하셨지요?"),
                ("granny","낡은 집은 손본 데가 많아요. 종이에 그린 거랑 지금 집이 같겠어요?",{"expression":"neutral"})]
        if person=="granny" and key in ("E37","E05") and "inn_front_door_claim" in old_flags:
            if "inn_claim_retracted" in old_flags:return [("granny","그건 세탁물을 나르던 문이에요. 아까 말씀드린 대로예요.")]
            r13_flag("inn_claim_retracted")
            return [("dad","주방 레버를 올리고 책장 손잡이를 움직였습니다. 그랬더니 뒤쪽 문이 열리더군요."),
                ("granny","……그 문을 여셨어요?",{"expression":"distressed"}),
                ("dad","13호실 문은 복도 쪽 문밖에 없다고 하셨는데요."),
                ("granny","손님이 쓰는 문 말이에요. 예전에는 세탁물을 그 문으로 날랐지요.",{"expression":"neutral"}),
                ("dad","제 아내도 그 길을 썼습니까?"),("granny","부인이 그 길을 쓰는 건 못 봤어요."),
                ("dad","그럼 제가 직접 확인하겠습니다.")]
        return response

screen r13_plan_comparison():
    modal True
    zorder 90
    default stage=0
    default gap=None
    default endpoints=()
    default reason=None
    default feedback="외벽과 실내를 같은 비율로 줄여 옮겼다. 폭이 맞지 않는 곳을 짚어 보자."
    default hint=False
    default lens=False
    add Solid("#102725f5")
    text "13호실 · 도면 맞춰 보기" style "r13_title_text" xpos 40 ypos 26 color "#efd4a1"
    text ("%d / 3 · "% (stage+1)+("빈 공간 찾기","연결선 따라가기","가설 세우기")[stage]) xpos 40 ypos 81 size r13_read_size(22,26) color "#d4dfd8"
    frame:
        area (32,127,730,425) padding (15,15) background R13PaperPanel()
        add R13PlanDrawing(stage,gap,lens)
    if stage==0:
        text "외벽에서 확인한 폭" xpos 110 ypos 160 size 24 color "#493e2d"
        text "방 안에서 확인한 폭" xpos 110 ypos 314 size 24 color "#493e2d"
        for value,title,x,w in (("window","창문 쪽",112,128),("center","방 가운데",280,150),("books","책장 뒤",544,130)):
            button:
                area (x,432,w,48) padding (10,6)
                background Solid("#b4853b55" if gap==value else "#00000000")
                hover_background Solid("#b4853b33")
                action SetScreenVariable("gap",value)
                text title color "#493e2d" size r13_read_size(23,27) yalign .5 xalign .5
        for value,x,w in (("window",112,128),("center",280,150),("books",544,130)):
            button:
                area (x,354,w,70) padding (0,0) background None hover_background Solid("#b4853b33")
                action SetScreenVariable("gap",value)
                alt {"window":"창문 쪽 폭","center":"방 가운데 폭","books":"책장 뒤 빈 폭"}[value]
        text "두 그림은 창문 쪽 기준을 맞춰 놓았다." xpos 64 ypos 487 size 22 color "#536158"
    else:
        text "2층 · 13호실" xpos 102 ypos 179 size 23 color "#493e2d"
        text "1층 · 주방" xpos 102 ypos 320 size 23 color "#493e2d"
        for key,title,x,y in (("books","책장 아래",135,254),("flue","굴뚝 관",350,181),("kitchen","선반 아래",145,410),("stove","화덕",425,410)):
            textbutton title:
                style "r13_paper_tab_button" xpos x ypos y xsize 180 ysize 60 text_size r13_read_size(22,26)
                background R13PaperPanel(key in endpoints)
                sensitive stage==1 action SetScreenVariable("endpoints",r13_plan_pair(endpoints,key))
        text "회색: 배관    붉은색: 나중에 덧그린 선" xpos 64 ypos 487 size 22 color "#536158"
    frame:
        area (786,127,462,425) padding R13_UI_PADDING["panel"] background R13ActionPanel()
        viewport:
            xsize 414 ysize 385 mousewheel True draggable True scrollbars "vertical"
            vbox:
                spacing 16
                if stage==0:
                    text "어느 쪽에 남는 공간이 있을까?" size r13_read_size(25,29) color "#fff2cf" xsize 405
                elif stage==1:
                    text "붉은 선의 양 끝을 골라 보자." size r13_read_size(25,29) color "#fff2cf" xsize 405
                    if r13_plan_has_lens():
                        textbutton ("돋보기 내려놓기" if lens else "돋보기로 겹친 선 보기"):
                            style "r13_action_button" xsize 410 yminimum 58 text_size 21 action ToggleScreenVariable("lens")
                        if lens:
                            text "두 끝에 작은 걸쇠 고리가 그려져 있다. 굵은 회색 관은 그 아래로 지난다." size 21 color "#efd4a1" xsize 400
                else:
                    text "이 빈 공간과 선은 무엇일까?" size r13_read_size(25,29) color "#fff2cf" xsize 405
                    for key,title in (("insulation","열을 가두는 이중 벽이다"),("latch","아래층에서 위층 잠금을 푸는 장치다")):
                        textbutton title:
                            style "r13_action_button" xsize 410 yminimum 84 text_size r13_read_size(22,26)
                            selected reason==key action SetScreenVariable("reason",key)
                textbutton ("도움말 접기" if hint else "생각이 막혔다면"):
                    style "r13_action_button" xsize 410 ysize 56 text_size 21 action ToggleScreenVariable("hint")
                if hint:
                    text ("왼쪽 시작점은 같다. 두 폭의 오른쪽 끝을 비교하자.","갈림길에서도 붉은색만 따라가 보자.","보온용 벽에도 움직이는 걸쇠가 필요할까?")[stage] size 21 color "#d4dfd8" xsize 400
    text feedback xpos 40 ypos 565 xsize 1192 size r13_read_size(22,26) color "#efd4a1"
    textbutton "돌아가기":
        style "r13_action_button" xpos 40 ypos 641 xsize 235 ysize 62 text_size 24 action Return(False)
    text ("완료하면 "+r13_time_target()+" · 취소하면 시간은 흐르지 않는다") xpos 299 ypos 659 size 20 color "#d4dfd8"
    textbutton ("이 가설로 기록" if stage==2 else "선택한 부분 비교"):
        style "r13_action_button" xpos 905 ypos 641 xsize 335 ysize 62 text_size 24
        sensitive (gap is not None if stage==0 else len(endpoints)==2 if stage==1 else reason is not None)
        action ([SetScreenVariable("feedback",r13_plan_check(stage,gap,endpoints,reason)[1]),SetScreenVariable("hint",False),SetScreenVariable("stage",stage+1)] if stage<2 and r13_plan_check(stage,gap,endpoints,reason)[0] else Return(True) if stage==2 and r13_plan_check(stage,gap,endpoints,reason)[0] else SetScreenVariable("feedback",r13_plan_check(stage,gap,endpoints,reason)[1]))
    key "game_menu" action Return(False)

label r13_compare_first_plan:
    if "map" in room13.get("done",[]) or room13["period"]>=3 or "map" not in [a for a,spec in r13_actions()]:
        return False
    window hide
    hide r13_visitor
    call screen r13_plan_read
    if not _return:
        return False
    # Reading alone records nothing; the three-step comparison is the deduction.
    call screen r13_plan_comparison
    if not _return:
        return False
    call r13_lines([("dad","(책장 뒤 빈 공간과 주방 걸쇠를 잇는 덧그린 선. 방에 돌아가서 지금도 움직이는지 확인하자.)",{"thought":True})],"mystery:plan:compared")
    return True

screen r13_plan_read():
    modal True
    zorder 85
    default page=0
    default lens=False
    add Solid("#102725f5")
    text "여관 보수 도면" xpos 46 ypos 36 size 32 color "#efd4a1"
    hbox:
        xpos 46 ypos 94 spacing 14
        textbutton "치수 스케치" style "r13_action_button" selected page==0 action SetScreenVariable("page",0)
        textbutton "보수 기록" style "r13_action_button" selected page==1 action SetScreenVariable("page",1)
    add R13PlanDrawing(page,None,lens) xpos 46 ypos 180
    if page==0:
        text "외벽" xpos 132 ypos 246 color "#493e2d" size 23
        text "방 안" xpos 132 ypos 366 color "#493e2d" size 23
        text "창문" xpos 128 ypos 489 color "#493e2d" size 21
        text "책장" xpos 565 ypos 489 color "#493e2d" size 21
    else:
        text "2층 · 13호실" xpos 100 ypos 233 color "#493e2d" size 23
        text "1층 · 주방" xpos 100 ypos 372 color "#493e2d" size 23
    frame:
        area (780,180,450,360) padding (24,24)
        background R13ActionPanel()
        vbox:
            spacing 24
            text ("치수 기록" if page==0 else "여백의 메모") size 27 color "#efd4a1"
            text ("외벽과 실내를 같은 비율로 줄여 옮긴 그림이다. 창문 쪽 끝에는 같은 기준선이 그어져 있다." if page==0 else "회색: 기존 배관\n붉은색: 나중에 덧그린 선\n\n두 층을 가로지르는 선 옆에 작은 기호가 남아 있다.") size r13_read_size(24,28) color "#eee5d5" xsize 402 line_spacing 8
    if r13_plan_has_lens():
        textbutton ("돋보기 내려놓기" if lens else "돋보기로 보기") style "r13_action_button" xpos 780 ypos 554 action SetScreenVariable("lens",not lens)
    textbutton "돌아가기" style "r13_action_button" area (46,640,260,58) action Return(False)
    textbutton "실제 폭과 맞춰 본다" style "r13_action_button" area (910,640,320,58) action Return(True)
    text ("맞춰 보기를 마치면 "+r13_time_target()) xpos 350 ypos 658 size 22 color "#d4dfd8"
    key "game_menu" action Return(False)

screen r13_mystery_notebook():
    modal True
    zorder 96
    default expanded=None
    add Solid("#102725fa")
    text "추리 메모" style "r13_title_text" xpos 48 ypos 30 color "#efd4a1"
    text "확인한 사실과 아직 풀리지 않은 질문" xpos 260 ypos 46 size 23 color "#d4dfd8"
    viewport:
        area (48,108,1184,496) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 18
            for i,note in enumerate(r13_first_mystery_notes()):
                frame:
                    xsize 1144 padding R13_UI_PADDING["panel"] background R13ActionPanel()
                    vbox:
                        spacing 13
                        text note["title"] size r13_read_size(28,32) color "#efd4a1" xsize 1088
                        text ("확인 · "+note["fact"]) size r13_read_size(23,28) color "#fff2cf" xsize 1088
                        text ("의문 · "+note["question"]) size r13_read_size(24,29) color "#a8cdec" xsize 1088
                        if note["keys"]:
                            text ("함께 볼 기록 · "+" / ".join(R13_RECORD_SHORT.get(k,ROOM13["evidence"][k]["name"]) for k in note["keys"])) size r13_read_size(21,25) color "#d4dfd8" xsize 1088
                        textbutton ("생각 정리 접기" if expanded==i else "생각 정리"):
                            style "r13_action_button" xsize 260 ysize 56 text_size 22 action SetScreenVariable("expanded",None if expanded==i else i)
                        if expanded==i:
                            text note["hint"] size r13_read_size(22,27) color "#d4dfd8" xsize 1088
    textbutton "닫기" style "r13_action_button" xpos 930 ypos 642 xsize 300 ysize 62 text_size 24 action Hide("r13_mystery_notebook")
    key "game_menu" action Hide("r13_mystery_notebook")
