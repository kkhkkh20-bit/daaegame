# 자료 대조 통합 화면 (2026-10-27 UX 인계서 D01·D02·D03·D06, 구조 시안 A·B·C).
#   「대조 화면 → 자료함 → 상세 → 자료함 → 대조 화면」 왕복을 없앤다. 한 화면에 실제 발언(왼쪽), 보유 자료 목록
#   (가운데, 체크로 고르고 이름을 눌러 읽는다), 열어 본 자료 상세(오른쪽), 고른 자료 칩과 주 행동 하나(아래)를 둔다.
#   시범 쟁점 셋(1일 입구, 1일 두 편지, 7일 화재 첫 추궁)에서만 쓰고, 나머지 쟁점과 옛 캠페인은 기존
#   r13_crisis_proof / r13_book 으로 간다(room13_v111.rpy r13_v111_proof_again).
#
#   바꾸지 않는 것(인계서 13장): v111_claim="v111:"+key 와 room13["arguments"][v111_claim], 정답 판정
#   (r13_v111_proof_accepts·R13_PROOF_ALTERNATES·R13_PROOF_EXTRAS·r13_v111_proof_kept), 기회(r13_v111_proof_chances·
#   r13_nw_retry). 이 파일은 정답 함수를 부르지 않는다 — 목록은 이번 회차 보유 자료(room13["evidence"])에서 기존
#   catalog 적격성으로만 뽑고, 획득 순서(최신 먼저)로 놓는다. 정답 ID·미획득 자료·정답 개수는 어디에도 내지 않는다.
#   읽기·체크·탭·비교·복귀·빈 제출은 기회를 쓰지 않는다 — 제출(「근거 제시」/「비교 마치기」)만 "argue" 를 돌려 주고,
#   판정은 호출한 라벨이 기존 그대로 한다.
#
#   첫 블록(init 350)은 표시 문맥 표와 순수 선택 계산이다. store·renpy 를 쓰지 않아 dev/test_proof_workspace.py 가
#   Ren'Py 없이 그대로 실행한다. store 에 기대는 것은 다음 블록(init 351)에 둔다.
init 350 python:
    # 쟁점 key → 표시 문맥. quote_when: ("flag", 플래그) 는 r13_has, ("value", 값 키) 는 r13_v111_value 가 True 일 때만
    # 발언을 보인다. None 은 늘 보인다. 정답 ID·미획득 자료·미래 대사는 여기 넣지 않는다.
    R13_PW_CONTEXT={
        "함께 들어갈 근거를 고른다":dict(mode="proof",speaker="돌목",
            quote="종이엔 그렇게 적혀 있소. 일꾼은 본인만. 아이는 안 되오.",
            quote_when=("flag","v111:entered:MS14_D01_S02")),
        # 두 편지: 인물의 해설 없이 문서 둘을 직접 읽는다. 의문 한 줄만.
        "두 편지를 나란히 본다":dict(mode="compare",speaker=None,
            quote="두 편지를 직접 읽고 견준다. 무엇이 같고, 무엇이 다른가.",
            quote_when=None),
        "불이 시작된 곳과 진술을 대조한다":dict(mode="proof",speaker="보리",
            quote="불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소.",
            quote_when=("value","bori_nubi_door_witness_heard")),
    }
    R13_PW_TABS=(("all","전체"),("now","이번 사건"),("past","지난 사건"),("person","사람별"))
    R13_PW_COMPARE_LIMIT=2

    def r13_pw_context(key):
        """시범 쟁점이면 문맥 dict, 아니면 None(호출자가 기존 화면으로 폴백)."""
        return R13_PW_CONTEXT.get(key)

    def r13_pw_quote_visible(spec,has,value):
        """발언을 보일지. has(flag)·value(key) 는 호출자가 넘기는 조회 함수라 시험에서 바꿔 끼울 수 있다."""
        when=(spec or {}).get("quote_when")
        if not when:return True
        kind,name=when
        if kind=="flag":return bool(has(name))
        return value(name) is True

    def r13_pw_order(keys,days):
        """보유 목록을 획득한 날(최신 먼저)로 놓는다. 같은 날은 원래 목록 순서(획득 순서)를 지킨다.
        날을 모르는 자료는 가장 오래된 것으로 본다. 정답 함수로 정렬하지 않는다."""
        indexed=list(enumerate(keys))
        def day_of(key):
            day=days.get(key) if days else None
            return day if isinstance(day,int) else -1
        indexed.sort(key=lambda pair:(-day_of(pair[1]),pair[0]))
        return [key for _,key in indexed]

    def r13_pw_toggle(chosen,key,owned,mode):
        """체크 켜기·끄기. (새 선택 목록, 교체 대기 자료).
        보유하지 않은 자료는 무시한다. compare 는 둘까지만 — 셋째를 고르면 선택은 그대로 두고 교체 대기로 돌려 준다
        (처음 것을 자동으로 버리지 않는다). 일반 proof 에는 개수 제한이 없다."""
        chosen=list(chosen or ())
        if key not in (owned or ()):return chosen,None
        if key in chosen:
            return [k for k in chosen if k!=key],None
        if mode=="compare" and len(chosen)>=R13_PW_COMPARE_LIMIT:
            return chosen,key
        return chosen+[key],None

    def r13_pw_replace(chosen,old,new,owned):
        """교체 대기 자료를 고른 자리에 넣는다. 자리가 없거나 보유하지 않은 자료면 그대로."""
        chosen=list(chosen or ())
        if old not in chosen or new not in (owned or ()) or new in chosen:return chosen
        return [new if k==old else k for k in chosen]

    def r13_pw_remove(chosen,key):
        return [k for k in (chosen or ()) if k!=key]

    def r13_pw_submit_ok(chosen,mode):
        """주 행동이 눌리는가. 빈 제출은 막는다(기회를 쓰지 않는다). compare 는 정확히 둘."""
        n=len(chosen or ())
        if mode=="compare":return n==R13_PW_COMPARE_LIMIT
        return n>0

    def r13_pw_pair_from_chosen(chosen,mode):
        """compare 에서 「나란히 보기」가 펼칠 두 자료. 둘이 아니면 None."""
        if mode=="compare" and len(chosen or ())==R13_PW_COMPARE_LIMIT:return (chosen[0],chosen[1])
        return None

    def r13_pw_pair_fill(pair,key):
        """읽기용 쌍의 빈 자리를 채운다. 제출 묶음과는 별개다."""
        a,b=(tuple(pair or ())+(None,None))[:2]
        if key is None or key in (a,b):return (a,b)
        if a is None:return (key,b)
        if b is None:return (a,key)
        return (a,b)

    def r13_pw_pair_live(pair,owned):
        """없는 자료가 든 쌍은 정리한다. 둘 다 있을 때만 나란히 읽는다."""
        if not pair:return None
        a,b=(tuple(pair)+(None,None))[:2]
        a=a if a in (owned or ()) else None
        b=b if b in (owned or ()) else None
        if a is None and b is None:return None
        return (a,b)

    def r13_pw_main_label(mode):
        return "비교 마치기" if mode=="compare" else "근거 제시"

# store 에 기대는 도우미와 화면.
default r13_pw_views = {}   # 쟁점(claim)별 UI 기억: 탭·열어 본 자료·발언 접힘. 구 저장에는 없어도 기본값으로 연다.

init 351 python:
    def r13_pw_active(key):
        return r13_v111_active() and r13_pw_context(key) is not None

    def r13_pw_quote_visible_now(key):
        spec=r13_pw_context(key)
        return r13_pw_quote_visible(spec,r13_has,r13_v111_value)

    def r13_pw_entries():
        """이번 회차에 보유한, 제시 적격인 자료. 물건(bag:/tool:)은 근거가 아니라 뺀다(hearing=True 와 같은 기준).
        서랍이 켜진 이야기(v111)는 결과 쪽지 접기를 그대로 따른다(접히는 쪽지는 제시에 쓰이지 않는 것만이다)."""
        keys=[k for k in r13_catalog_entries(False,True) if r13_catalog_can_present(k,True)]
        if r13_drawer_active():keys=r13_drawer_visible(keys)
        records=(store.room13 or {}).get("records",{}) or {}
        days=dict((k,(records.get(k) or {}).get("day")) for k in keys)
        return r13_pw_order(keys,days)

    def r13_pw_sections(tab,entries):
        """[(묶음 제목 또는 None, 자료 목록)]. 전체는 한 묶음, 보조 탭은 기존 서랍의 분류(새 사실을 더하지 않는다)."""
        if tab=="now" and r13_drawer_active():return [(None,r13_drawer_now(entries))]
        if tab=="past" and r13_drawer_active():
            return [(r13_drawer_case_title(case),keys) for case,keys in r13_drawer_cases(entries)]
        if tab=="person" and r13_drawer_active():
            return [(R13_NAMES.get(person,person),keys) for person,keys in r13_drawer_people(entries)]
        return [(None,list(entries))]

    def r13_pw_set_arguments(claim,chosen):
        # 기존 방식 그대로: room13 을 복사해 arguments 만 바꾼다. 보유 사실·기회·판정은 손대지 않는다.
        copy=winter_copy.deepcopy(store.room13)
        copy["arguments"][claim]=list(chosen)
        store.room13=copy

    def r13_pw_toggle_action(claim,key,mode):
        owned=r13_pw_entries()
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        new,pending=r13_pw_toggle(chosen,key,owned,mode)
        if pending:
            renpy.set_screen_variable("replace_pending",pending,screen="r13_proof_workspace")
        elif new!=chosen:
            r13_pw_set_arguments(claim,new)
        renpy.restart_interaction()

    def r13_pw_replace_action(claim,old,new):
        owned=r13_pw_entries()
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        r13_pw_set_arguments(claim,r13_pw_replace(chosen,old,new,owned))
        renpy.set_screen_variable("replace_pending",None,screen="r13_proof_workspace")
        renpy.restart_interaction()

    def r13_pw_remove_action(claim,key):
        chosen=list((store.room13.get("arguments") or {}).get(claim,[]))
        r13_pw_set_arguments(claim,r13_pw_remove(chosen,key))
        renpy.restart_interaction()

    def r13_pw_remember_pair(claim,pair):
        # D08: 관찰 뒤 대사를 보이고 돌아오면 같은 쌍이 펼쳐져 있어야 한다. 「목록으로」가 지운다.
        views=dict(store.r13_pw_views or {});row=dict(views.get(claim,{}));row["pair"]=tuple(pair) if pair else None;views[claim]=row;store.r13_pw_views=views
    def r13_pw_remember(claim,tab,detail,quote_open):
        views=dict(store.r13_pw_views or {})
        row=dict(views.get(claim,{}));row.update(tab=tab,detail=detail,quote_open=quote_open);views[claim]=row  # D08 의 pair 기억은 남긴다
        store.r13_pw_views=views

    def r13_pw_open_detail(key):
        """이름을 누르면 읽는다. 읽어도 선택되지 않는다. 읽기용 쌍의 빈 자리가 있으면 그 자리에 채운다."""
        pair=renpy.get_screen("r13_proof_workspace").scope.get("pair")
        if pair and None in (tuple(pair)+(None,None))[:2]:
            renpy.set_screen_variable("pair",r13_pw_pair_fill(pair,key),screen="r13_proof_workspace")
        else:
            renpy.set_screen_variable("detail",key,screen="r13_proof_workspace")
        renpy.set_screen_variable("origin_open",False,screen="r13_proof_workspace")
        if key in (store.room13 or {}).get("evidence",[]):r13_record_update_ui("seen",key,True)
        renpy.restart_interaction()

    def r13_pw_id(prefix,key):
        return prefix+str(key).replace("V111:","").replace(":","_")

    def r13_pw_card_height():
        # 이름 두 줄 + 「N일 · 장소」 꼬리표가 들어가야 해서 PC 보통도 72 다(64 에서는 셋째 줄이 칸 밖으로 나갔다).
        return 88 if r13_touch_ui() else (80 if persistent.room13_large_text else 72)

    def r13_pw_chip_height():
        return 64 if r13_touch_ui() else 40

    def r13_pw_tab_height():
        return 88 if r13_touch_ui() else 40

    def r13_pw_small():
        return r13_nb_small_size()

    def r13_pw_body():
        return r13_nb_body_size()

    def r13_pw_quote_height(text,width):
        return r13_proof_text_size(text,r13_nb_emphasis_size(),width)[1]

    def r13_pw_layout(quote_open,quote_text):
        """자리 계산. PC: 왼쪽 발언 열 · 가운데 목록 · 오른쪽 상세, 위에 탭 줄, 아래에 칩 줄과 버튼 줄.
        휴대폰: 위 한 줄(발언 접기 버튼 + 탭), 본문 한 영역(목록 또는 상세), 아래 칩 줄과 버튼 줄.
        전체 화면은 스크롤하지 않는다 — 목록·상세만 뷰포트다."""
        touch=r13_touch_ui()
        L=dict(touch=touch,left=R13_NB_LEFT,right=R13_NB_RIGHT,width=R13_NB_WIDTH,top=R13_NB_TOP)
        L["footer_y"]=r13_nb_footer_y()
        L["chip_h"]=r13_pw_chip_height()
        L["chips_y"]=L["footer_y"]-(8 if touch else 12)-L["chip_h"]
        L["body_bottom"]=L["chips_y"]-8
        L["tab_h"]=r13_pw_tab_height()
        if touch:
            L["fold_w"]=372
            L["tab_x"]=L["left"]+L["fold_w"]+16
            L["tab_w"]=(L["right"]-L["tab_x"]-24)//4
            L["tab_gap"]=8
            qh=(r13_pw_quote_height(quote_text,L["width"]-32)+24) if (quote_open and quote_text) else 0
            L["quote_y"]=L["top"]+L["tab_h"]+8
            L["quote_h"]=qh
            L["body_top"]=L["quote_y"]+(qh+8 if qh else 0)
            L["list_x"]=L["left"];L["list_w"]=L["width"]
            L["detail_x"]=L["left"];L["detail_w"]=L["width"]
            L["cols"]=1 if persistent.room13_large_text else 2
        else:
            L["quote_x"]=L["left"];L["quote_w"]=268
            L["list_x"]=424;L["list_w"]=340
            L["detail_x"]=788;L["detail_w"]=L["right"]-788
            L["tab_x"]=L["list_x"];L["tab_w"]=0;L["tab_gap"]=6
            L["body_top"]=L["top"]+L["tab_h"]+12
            L["cols"]=1
        L["body_h"]=max(60,L["body_bottom"]-L["body_top"])
        L["card_h"]=r13_pw_card_height()
        return L

    def r13_pw_tab_boxes(L):
        """탭 칩의 (x, 폭). PC 는 글자 길이대로, 휴대폰은 네 칸 균등."""
        small=r13_pw_small()
        out=[];x=L["tab_x"]
        for key,title in R13_PW_TABS:
            w=L["tab_w"] or (len(title)*small+22)
            out.append((key,title,x,w));x+=w+L["tab_gap"]
        return out

    def r13_pw_help(mode,chances,count):
        if mode=="compare":
            return "두 편지를 체크하고 「나란히 보기」로 읽은 뒤 「비교 마치기」."
        if not count:
            return "체크로 근거를 고르고, 이름을 누르면 오른쪽에서 읽습니다."
        if chances:
            return "고른 근거가 맞으면 「근거 제시」. 잘못 내면 기회를 1회 씁니다."
        return "고른 근거가 맞으면 「근거 제시」를 누릅니다."

# 체크 상자: 선택은 체크 + 테두리로 보인다(색만으로 구별하지 않는다). 새 재질 없이 잉크 선과 크림 면.
screen r13_pw_checkbox(on,size=30):
    frame:
        xysize (size,size) padding (2,2) background Solid(r13_nb_accent() if on else r13_nb_ink()) yalign .5
        frame:
            xysize (size-4,size-4) padding (0,0) background Solid("#f5ecd9")
            if on:
                text "✓" align (.5,.5) size (size-8) color r13_nb_accent() font R13_UI_BOLD_FONT

# 자료 한 장: 왼쪽 체크 영역(선택), 나머지(그림·이름)는 상세를 읽는 영역. 둘은 시각적으로 갈라져 있다.
screen r13_pw_card(claim,key,mode,w,h,chosen,is_detail,ready):
    $ check_w=56
    $ thumb=h-28
    $ name_w=w-check_w-thumb-30
    $ label_size=min(22,r13_pw_small())
    frame:
        xysize (w,h) padding (0,0) background (Solid(r13_nb_accent()) if chosen else (Solid("#c9a86a99") if is_detail else None))
        frame:
            xpos 3 ypos 3 xysize (w-6,h-6) padding (0,0) background r13_field_paper()
            button:
                id r13_pw_id("r13_pw_check_",key)
                xpos 0 ypos 0 xysize (check_w,h-6) padding (0,0) background None hover_background Solid("#8d4b2d14")
                action Function(r13_pw_toggle_action,claim,key,mode) sensitive ready
                alt (("선택 해제 · " if chosen else "선택 · ")+r13_catalog_title(key))
                use r13_pw_checkbox(chosen,30)
            add Solid("#c9a86a66") xpos check_w ypos 8 xsize 1 ysize (h-22)
            button:
                id r13_pw_id("r13_pw_open_",key)
                xpos (check_w+1) ypos 0 xysize (w-6-check_w-1,h-6) padding (0,0) background None hover_background Solid("#8d4b2d14")
                action Function(r13_pw_open_detail,key) sensitive ready
                alt ("읽기 · "+r13_catalog_title(key))
                fixed:
                    xysize (w-6-check_w-1,h-6)
                    add r13_evidence_picture(key,thumb) xpos 8 yalign .5
                    $ name=r13_ev_two_lines(r13_catalog_title(key),name_w,label_size,2)
                    vbox:
                        xpos (thumb+18) yalign .5 spacing 1
                        text name xsize name_w size label_size color r13_nb_ink() font R13_UI_BOLD_FONT line_spacing -1
                        # 꼬리표는 이름이 한 줄일 때(또는 휴대폰 88 칸)만 — 두 줄 이름 아래 붙이면 칸 밖으로 나간다.
                        if r13_drawer_tag(key) and ("\n" not in name or h>=88):
                            text r13_drawer_tag(key) size max(14,label_size-6) color r13_nb_muted() font R13_UI_BOLD_FONT xsize name_w

# 열어 본 자료 상세: 기존 부품(제목 꼬리표·그림 상자·관찰 사실·쪽지)을 다시 쓴다. 긴 원문은 「출처 펼치기」 안.
screen r13_pw_detail(claim,key,mode,x,y,w,h,origin_open,can_pair,ready):
    $ small=r13_pw_small()
    $ bh=r13_ev_button_height()
    $ inner=w-24
    $ pic=min(inner,180 if not r13_touch_ui() else 120)   # PC 180: 관찰 사실 세 줄이 스크롤 없이 보인다
    # 읽기 조작(출처 펼치기·나란히 놓기)은 뷰포트 밖 아래 한 줄에 고정한다 — 긴 상세에서 스크롤 끝까지 내려가야 보이면 안 된다.
    $ buttons=[("출처 접기" if origin_open else "출처 펼치기",SetScreenVariable("origin_open",not origin_open),"r13_pw_origin")]
    if can_pair:
        # 일반 proof 의 읽기용 나란히 놓기. 제출 묶음은 그대로다(D03·T09).
        $ buttons.append(("⇆ 나란히 놓기",[SetScreenVariable("pair",(key,None)),SetScreenVariable("detail",None)],"r13_pw_pair"))
    $ bw=(w-8*(len(buttons)-1))//len(buttons)
    for index,(caption,action,control_id) in enumerate(buttons):
        fixed:
            xpos (x+index*(bw+8)) ypos (y+h-bh) xysize (bw,bh)
            use r13_control(caption,None,action,enabled=ready,width=bw,height=bh,label_size=r13_ev_label_size(caption,bw),control_id=control_id)
    viewport:
        id "r13_pw_detail"
        area (x,y,w,h-bh-8) mousewheel True draggable True scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        vbox:
            xsize inner spacing 10
            if r13_touch_ui():
                # 휴대폰(D06): 본문이 낮아 그림 아래 관찰 사실이 스크롤 뒤로 숨었다. 그림은 왼쪽, 제목·사실은 오른쪽에 나란히.
                hbox:
                    spacing 14
                    fixed:
                        xysize (pic,pic)
                        use r13_evidence_picture_box(key,pic)
                    vbox:
                        xsize (inner-pic-14) spacing 8
                        use r13_evidence_heading(key,inner-pic-14,(r13_nb_heading_size()))
                        use r13_evidence_fact_list(key,inner-pic-14)
            else:
                use r13_evidence_heading(key,inner,(r13_nb_heading_size()))
                fixed:
                    xsize inner ysize pic
                    fixed:
                        xpos ((inner-pic)//2) xysize (pic,pic)
                        use r13_evidence_picture_box(key,pic)
                use r13_evidence_fact_list(key,inner)
            if r13_drawer_active():
                use r13_drawer_note_blocks(key,inner)
            if origin_open:
                $ ev=r13_catalog_record(key)
                text ("들은 말" if ev.get("kind")=="증언" else "확인한 내용") size small color r13_nb_accent() font R13_UI_BOLD_FONT
                text r13_material_body(ev) size r13_ev_fact_size() color r13_nb_ink() font R13_UI_BOLD_FONT xsize inner
                text r13_catalog_origin(key) size small color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner
                if key in room13.get("records",{}):
                    text ("얻은 곳: "+r13_record_source_label(key)) size small color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner

# 두 자료를 나란히: 같은 폭 두 열, 각 열만 스크롤. 맞는지 아닌지는 표시하지 않는다.
# 2026-10-27 D08: 두 편지 나란히 보기에서 「눈에 띄는 부분을 짚어 본다」. 두 문서 위에 같은 모양의 구역 넷(머리글·본문·끝부분·여백)을
# 열고 하나를 고르면 ("observe",구역) 을 돌려준다. 정답 구역을 미리 강조하지 않는다. 기회를 쓰지 않는다.
init 350 python:
    R13_PW_OBSERVE_KEY="두 편지를 나란히 본다"
    def r13_pw_observe_spots(pic):
        return [("head","머리글",(0,0,pic,int(pic*.25))),("body","본문",(0,int(pic*.25),int(pic*.7),int(pic*.5))),
                ("tail","끝부분",(int(pic*.7),int(pic*.6),pic-int(pic*.7),pic-int(pic*.6))),("margin","여백",(0,int(pic*.75),int(pic*.7),pic-int(pic*.75)))]
    def r13_pw_observe_available(key,pair):
        return key==R13_PW_OBSERVE_KEY and bool(pair) and len(pair)==2 and all(k in ("V111:E01","V111:E06") for k in pair)

screen r13_pw_pair(pair,x,y,w,h,observe=False,ready=True):
    $ small=r13_pw_small()
    $ col_w=(w-16)//2
    $ inner=col_w-24
    $ pic=min(inner,160 if not r13_touch_ui() else 110)
    $ title_size=r13_nb_heading_size()
    text "나란히 놓기 · 두 자료를 함께 봅니다. 맞는지 아닌지는 표시하지 않습니다." xpos x ypos y xsize w size small color r13_nb_muted() font R13_UI_BOLD_FONT
    $ top=y+small+10
    add Solid("#c9a86a66") xpos (x+col_w+8) ypos top xsize 1 ysize (h-(top-y))
    for column,key in enumerate((tuple(pair)+(None,None))[:2]):
        viewport:
            id ("r13_pw_pair_%d"%column)
            area ((x if column==0 else x+col_w+16),top,col_w,h-(top-y))
            mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize inner spacing 8
                if key is not None:
                    use r13_evidence_heading(key,inner,title_size)
                    fixed:
                        xsize inner ysize pic
                        fixed:
                            xpos ((inner-pic)//2) xysize (pic,pic)
                            use r13_evidence_picture_box(key,pic)
                            if observe:
                                for spot_id,spot_name,(sx,sy,sw,sh) in r13_pw_observe_spots(pic):
                                    button:
                                        id r13_pw_id("r13_pw_spot_%d_"%column,spot_id)
                                        area (sx,sy,sw,sh) padding (0,0)
                                        background Solid("#a63a2e22") hover_background Solid("#a63a2e55")
                                        action Return(("observe",spot_id)) sensitive ready alt (spot_name+" 짚기")
                                        text spot_name size r13_type("small") color r13_nb_accent() font R13_UI_BOLD_FONT xpos 4 ypos 2
                    use r13_evidence_fact_list(key,inner)
                else:
                    text ("%d번 자리"%(column+1)) size title_size color r13_nb_muted() font R13_UI_BOLD_FONT
                    text "목록에서 함께 볼 자료의 이름을 누르세요." size r13_ev_fact_size() color r13_nb_muted() font R13_UI_BOLD_FONT xsize inner

# 고른 자료 칩 줄. × 로 그 선택만 해제한다. compare 에서 셋째를 고르면 여기서 바꿀 자리를 고른다.
screen r13_pw_chips(claim,chosen,mode,L,replace_pending,ready):
    $ small=r13_pw_small()
    $ ch=L["chip_h"]
    $ short=10 if L["touch"] else 12
    viewport:
        area (L["left"],L["chips_y"],L["width"],ch) mousewheel False draggable True xinitial 0
        hbox:
            spacing 8 ysize ch
            if replace_pending:
                text ("「"+r13_evidence_short(replace_pending,short)+"」와 바꿀 자료:") size small color r13_nb_accent() font R13_UI_BOLD_FONT yalign .5
                for key in chosen:
                    button:
                        id r13_pw_id("r13_pw_swap_",key)
                        ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                        action Function(r13_pw_replace_action,claim,key,replace_pending) sensitive ready alt ("바꾸기 · "+r13_catalog_title(key))
                        text (r13_evidence_short(key,short)+"  ⇆") size small color r13_nb_ink() font R13_UI_BOLD_FONT yalign .5
                button:
                    id "r13_pw_swap_cancel"
                    ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                    action SetScreenVariable("replace_pending",None) sensitive ready alt "취소"
                    text "취소" size small color r13_nb_muted() font R13_UI_BOLD_FONT yalign .5
            else:
                text (("고른 자료 %d"%len(chosen)) if chosen else ("고른 자료 없음 · 목록의 체크로 고릅니다" if not L["touch"] else "고른 자료 없음")) size small color r13_nb_muted() font R13_UI_BOLD_FONT yalign .5
                for key in chosen:
                    button:
                        id r13_pw_id("r13_pw_chip_",key)
                        ysize ch padding (12,0) background r13_field_paper() hover_background r13_field_paper(hover=True)
                        action Function(r13_pw_remove_action,claim,key) sensitive ready alt ("선택 해제 · "+r13_catalog_title(key))
                        hbox:
                            spacing 10 yalign .5
                            text r13_evidence_short(key,short) size small color r13_nb_ink() font R13_UI_BOLD_FONT yalign .5
                            text "×" size (small+4) color r13_nb_accent() font R13_UI_BOLD_FONT yalign .5

screen r13_proof_workspace(claim,key,can_press=False,investigate=False,chances=None):
    style_prefix "r13"
    modal True
    zorder 50
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ ctx=r13_pw_context(key) or dict(mode="proof",speaker=None,quote=None,quote_when=None)
    $ mode=ctx["mode"]
    $ remembered=(r13_pw_views or {}).get(claim,{})
    default tab=remembered.get("tab","all")
    default detail=remembered.get("detail")
    # 2026-10-27 외부 리뷰 R03(확인): 휴대폰 844x390 「나란히 보기」에서 본문 읽기 영역이 약 95px 뿐이었다. 휴대폰은 발언 틀을 접은 채 열어
    # 본문이 그만큼 늘어나게 한다(접힘이면 r13_pw_layout 의 quote_h 가 0). PC 는 왼쪽 열이라 그대로. 펼친 기억은 그대로 따른다.
    default quote_open=remembered.get("quote_open",not r13_touch_ui())
    default pair=remembered.get("pair")
    default observe=False
    default origin_open=False
    default replace_pending=None
    on "hide" action Function(r13_pw_remember,claim,tab,detail,quote_open)
    $ owned=r13_pw_entries()
    $ stored=list(room13["arguments"].get(claim,[]))
    $ chosen=[k for k in stored if k in owned]
    $ detail=detail if detail in owned else None
    $ live_pair=r13_pw_pair_live(pair,owned)
    $ pair_open=bool(live_pair and None not in live_pair)
    $ pair_waiting=bool(live_pair and not pair_open)
    $ replace_pending=replace_pending if (replace_pending in owned and mode=="compare") else None
    $ quote_text=ctx["quote"] if (ctx["quote"] and r13_pw_quote_visible_now(key)) else None
    $ title=R13_PROOF_TITLES.get(key,key)
    $ L=r13_pw_layout(quote_open,quote_text)
    $ touch=L["touch"]
    $ small=r13_pw_small()
    $ ink=r13_nb_ink()
    $ muted=r13_nb_muted()
    $ accent=r13_nb_accent()
    $ sections=r13_pw_sections(tab,owned)
    $ show_list=not pair_open and not (touch and detail)
    use r13_notebook_shell("자료 대조",close_action=(Return("investigate") if investigate else None),stamp=chances)
    # 발언 ------------------------------------------------------------
    if touch:
        # 휴대폰: 위 한 줄에 발언 접기 버튼과 탭. 발언은 펼치면 아래 틀에 보이고 본문이 그만큼 내려간다.
        button:
            id "r13_pw_fold"
            xpos L["left"] ypos L["top"] xysize (L["fold_w"],L["tab_h"]) padding (12,4) background r13_field_paper() hover_background r13_field_paper(hover=True)
            action SetScreenVariable("quote_open",not quote_open) sensitive (ready and bool(quote_text)) alt "발언 펼치기"
            vbox:
                yalign .5 spacing 2
                text r13_ev_two_lines(title,L["fold_w"]-32,small,1) xsize (L["fold_w"]-32) size small color ink font R13_UI_BOLD_FONT line_spacing -1
                if quote_text:
                    text ((ctx["speaker"]+"의 말 · " if ctx["speaker"] else "의문 · ")+("접기" if quote_open else "펼치기")) size max(14,small-6) color accent font R13_UI_BOLD_FONT
        if quote_text and quote_open:
            frame:
                xpos L["left"] ypos L["quote_y"] xysize (L["width"],L["quote_h"]) padding (16,10) background r13_field_paper()
                text ((("{color=%s}"%accent)+ctx["speaker"]+"{/color}  ") if ctx["speaker"] else "")+quote_text size r13_nb_emphasis_size() color ink font R13_UI_BOLD_FONT xsize (L["width"]-32)
    else:
        vbox:
            xpos L["quote_x"] ypos L["top"] xsize L["quote_w"] spacing 10
            text title size r13_nb_heading_size() color ink font R13_UI_BOLD_FONT xsize L["quote_w"]
            add Solid("#c9a86a99") xsize L["quote_w"] ysize 1
            if quote_text:
                text ((ctx["speaker"]+"의 말") if ctx["speaker"] else "의문") size small color accent font R13_UI_BOLD_FONT
                text quote_text size r13_nb_body_size() color ink font R13_UI_BOLD_FONT xsize L["quote_w"]
            # 왼쪽 열이 길면(쟁점 제목 세 줄 + 발언) 도움말이 아래 칩 줄과 겹쳤다. 고른 자료가 없을 때의 도움말은
            # 칩 줄(「고른 자료 없음 · 목록의 체크로 고릅니다」)이 이미 말하므로 여기서는 뺀다.
            if r13_pw_help(mode,chances,len(chosen)) and (mode=="compare" or chosen):
                text r13_pw_help(mode,chances,len(chosen)) size small color muted font R13_UI_BOLD_FONT xsize L["quote_w"]
            if pair_waiting:
                text "목록에서 함께 볼 자료의 이름을 누르세요." size small color accent font R13_UI_BOLD_FONT xsize L["quote_w"]
        add Solid("#c9a86a66") xpos 412 ypos L["top"] xsize 1 ysize (L["body_bottom"]-L["top"])
        add Solid("#c9a86a66") xpos 776 ypos L["body_top"] xsize 1 ysize (L["body_bottom"]-L["body_top"])
    # 탭 ------------------------------------------------------------
    if show_list or (touch and not pair_open):
        for tab_key,tab_title,tx,tw in r13_pw_tab_boxes(L):
            textbutton tab_title:
                id ("r13_pw_tab_"+tab_key)
                style "r13ev_chip_button" text_style "r13ev_chip_button_text"
                xpos tx ypos L["top"] xsize tw ysize L["tab_h"]
                text_size min(small,(tw-12)//max(1,len(tab_title))) selected (tab_key==tab)
                action [SetScreenVariable("tab",tab_key)]+([SetScreenVariable("detail",None)] if touch else []) sensitive ready
    # 본문 ------------------------------------------------------------
    if pair_open:
        use r13_pw_pair(live_pair,L["list_x"],L["body_top"],(L["right"]-L["list_x"]),L["body_h"],observe,ready)
    elif touch and detail:
        use r13_pw_detail(claim,detail,mode,L["detail_x"],L["body_top"],L["detail_w"],L["body_h"],origin_open,(mode=="proof" and len(owned)>1),ready)
    else:
        $ cols=L["cols"]
        $ card_w=(L["list_w"]-20-8*(cols-1))//cols
        viewport:
            id "r13_pw_list"
            area (L["list_x"],L["body_top"],L["list_w"],L["body_h"]) mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize (L["list_w"]-20) spacing 8
                for header,keys in sections:
                    if header:
                        text header size small color accent font R13_UI_BOLD_FONT xsize (L["list_w"]-20)
                    for row in range(0,len(keys),cols):
                        hbox:
                            spacing 8
                            for k in keys[row:row+cols]:
                                use r13_pw_card(claim,k,mode,card_w,L["card_h"],(k in chosen),(k==detail and not touch),ready)
                if not any(keys for _,keys in sections):
                    text ("아직 모은 자료가 없습니다." if not owned else "이 분류에 해당하는 자료가 없습니다.") size small color muted font R13_UI_BOLD_FONT xsize (L["list_w"]-20)
        if not touch:
            if detail:
                use r13_pw_detail(claim,detail,mode,L["detail_x"],L["body_top"],L["detail_w"],L["body_h"],origin_open,(mode=="proof" and len(owned)>1 and not pair_waiting),ready)
            else:
                text ("목록에서 자료 이름을 누르면 여기서 읽습니다." if not pair_waiting else "함께 볼 자료의 이름을 목록에서 누르세요.") xpos L["detail_x"] ypos (L["body_top"]+40) xsize L["detail_w"] text_align .5 size r13_ev_fact_size() color muted font R13_UI_BOLD_FONT
    # 고른 자료 칩 ----------------------------------------------------
    use r13_pw_chips(claim,chosen,mode,L,replace_pending,ready)
    # 버튼 줄: 주 행동은 하나(빨강). 나머지는 공통 부품. 빈 선택이면 주 행동은 비활성이고 키 입력도 받지 않는다.
    $ buttons=[]
    if pair_open or (touch and detail):
        $ buttons.append(("목록으로",[Function(r13_pw_remember_pair,claim,None),SetScreenVariable("observe",False),SetScreenVariable("pair",None),SetScreenVariable("detail",(live_pair[0] if (pair_open and not touch) else None))],True,False,"r13_pw_back_list"))
    if can_press:
        $ buttons.append(("되묻는다",Return("press"),True,False,"r13_pw_press"))
    if investigate:
        $ buttons.append(("조사 계속",Return("investigate"),True,False,"r13_pw_investigate"))
    if pair_open and r13_pw_observe_available(key,live_pair if live_pair else pair):
        $ buttons.append((("다시 본다" if r13_v111_value("letter_tail_observed") else "눈에 띄는 부분을 짚어 본다") if not observe else "짚기 그만",[Function(r13_pw_remember_pair,claim,pair),ToggleScreenVariable("observe")],True,False,"r13_pw_observe"))
    if mode=="compare" and not pair_open:
        $ buttons.append(("나란히 보기",SetScreenVariable("pair",r13_pw_pair_from_chosen(chosen,mode)),bool(r13_pw_pair_from_chosen(chosen,mode)),False,"r13_pw_side"))
    $ buttons.append((r13_pw_main_label(mode),Return("argue"),r13_pw_submit_ok(stored,mode) and r13_pw_submit_ok(chosen,mode),True,"r13_pw_submit"))
    $ bw=((L["width"]-16*(len(buttons)-1))//len(buttons)) if touch else (200 if len(buttons)>3 else 232)
    $ bw=min(bw,264) if touch else bw
    $ bx=L["right"]-(bw*len(buttons)+16*(len(buttons)-1))
    # 버튼 줄 왼쪽에는 글을 두지 않는다 — 안내는 왼쪽 발언 열(PC)·발언 틀(휴대폰)에 있고, 짧은 폭에 넣으면 종이 밖으로 넘친다.
    for index,(caption,action,enabled,primary,control_id) in enumerate(buttons):
        fixed:
            xpos (bx+index*(bw+16)) ypos L["footer_y"] xysize (bw,r13_control_height())
            use r13_control(caption,None,action,enabled=(ready and enabled),primary=primary,width=bw,control_id=control_id)
