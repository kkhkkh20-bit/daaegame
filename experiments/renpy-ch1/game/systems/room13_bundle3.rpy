# 사건 묶음 3 (docs/EVENT_CATALOG.md D·E·O, 0.18.6): 저울 → 배급표 → 학교 장작이 한 줄로 이어진다.
#   D 저울    — 표준 저울추로 찾은 은호의 저울. 조용히 / 공개 / 입막음 반값 / 배급 저울까지 캐기.
#   E 배급표  — 5~6일 낮 광장. 너울이 보리를 배급 도둑으로 몬다. 배급 저울(D)·비축 장부(H1)로 누명을 벗길 수 있다.
#   O 학교 장작 — 5~6일 저녁 미션. 누명을 벗지 못한 보리가 대피소 장작을 가져간다.
#   U 기록 팔기 — 4~6일 낮 우체국. 사서가 끼니를 위해 돌의 옛 기록(W3)을 은호에게 판다. 놓치면 W3 길이 닫힌다.
# 소문의 효과: 나쁜 소문이 하나라도 있으면 은호 물건값이 1냥 오른다. 좋은 소문(rumor:fair)이 있으면 은호는 판단을 미뤄 오르지 않는다.
# 다만 저울 일로 직접 손해를 본 은호(eunho_hostile)는 사실을 바로잡기 전까지 1냥을 더 받는다(0.18.14, systems/room13_memory.rpy).
#   소문은 처음 퍼진 뒤 광장·여관·식당에 도착할 때 한 번 귓속말로 들린다.
# 모든 기록과 깃발은 이번 회차 것이다.
init 107 python:
    for _key,_name,_est,_not in (
        ("H6","배급소 저울","배급소 저울도 상점 저울과 같은 날 한 칸 무겁게 조여졌다. 은호는 백 부인의 부탁이었다고 했다.","누가 덜 받은 몫을 가져갔는지는 이 저울만으로 알 수 없다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    for _key,_name,_est,_not in (
        ("W8","집마다 다른 겨울","장작은 운반하는 사람이 먼저 지고, 배급은 장부대로 나온다. 보리 집은 장작을 나르면서도 난로가 꺼져 있었다.","보리 어머니의 기침이 추위 때문인지는 서리 검사원만 알 수 있다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(H6="배급소 저울",W8="집마다 다른 겨울")

    # D: the existing 은호 topic becomes a scene with choices; it closes once settled.
    ROOM13["topics"]["eunho_scale"]["not_flags"]=list(ROOM13["topics"]["eunho_scale"].get("not_flags",[]))+["scale_settled"]
    ROOM13["topics"].update({
        "guseul_scale":_ep_topic("resident_guseul","저울 나사를 누가 조였는지 묻는다",(2,7),need=["scale_rigged"],flags=["know_ration_scale"],not_flags=["know_ration_scale"],lines=[
            ("resident_guseul","……제가 말했다고는 하지 마세요. 사장님이 저를 가게에서 내보내면 저는 갈 데가 없거든요."),
            ("resident_guseul","가게 저울만 그런 게 아니에요. 같은 날 사장님이 배급소 저울 나사도 직접 조였어요."),
            ("resident_guseul","백 부인이 부탁했대요. 배급이 줄어야 사람들이 부인네 창고 물건을 비싸게라도 사 가니까요.")]),
        "bori_after":_ep_topic("resident_bori","배급 일 뒤로 괜찮은지 묻는다",(5,14),need=["ev_e_done"],lines=[
            ("resident_bori","괜찮다고 하면 거짓말이죠. 그래도 그날 배급대 앞에서 아무도 안 나서 줬으면 지금쯤 장작 수레까지 뺏겼을 거예요.")]),
    })
    R13_TOPIC_LABELS.update({"eunho_scale":"r13_b3_scale"})
    # U: once the pages are sold, the librarian can no longer show them; 은호 sells them back.
    ROOM13["topics"]["librarian_stone"]["not_flags"]=list(ROOM13["topics"]["librarian_stone"].get("not_flags",[]))+["pages_sold"]
    ROOM13["topics"]["eunho_pages"]=_ep_topic("resident_eunho","사서가 판 기록 장을 되산다",(4,13),need=["pages_sold"],not_flags=["know_stone_history"],lines=[])
    R13_TOPIC_LABELS.update({"eunho_pages":"r13_b3_buy_pages"})
    ROOM13["topics"]["librarian_copy"]=_ep_topic("resident_librarian","베껴 둔 돌 기록을 보여 달라고 한다",(5,13),need=["pages_copy_promised"],flags=["know_stone_history"],give=["W3"],not_flags=["know_stone_history"],
        lines=[("resident_librarian","장부를 밤새 베꼈어요. 글씨는 원본만 못해도 숫자는 그대로 옮겼어요.")]+list(ROOM13["topics"]["librarian_stone"]["lines"]))

    R13_BAD_RUMORS=("rumor:briber","rumor:troublemaker","rumor:sold_stolen","rumor:strongarm","rumor:extortion")
    R13_RUMOR_WHISPERS={
        "rumor:briber":"외지 사람이 순찰 경비 손에 돈을 쥐여 줬대.",
        "rumor:troublemaker":"그 외지 사람, 마을 일에 멋대로 손을 댄대. 너울이 눈여겨본다더라.",
        "rumor:sold_stolen":"훔친 약초를 은호 사장한테 팔아넘긴 게 그 외지 사람이래.",
        "rumor:strongarm":"여니 물건을 억지로 빼앗아 갔대. 장물이라면서.",
        "rumor:extortion":"실룩한테서 입막음 돈을 뜯었대.",
        "rumor:fair":"그 외지 사람이 사람들 몫이 공정하게 돌아가도록 나섰대.",
    }

    _r13_b3_shop_price=r13_shop_price
    def r13_shop_price(state,key):
        flags=state.get("flags",[])
        if "shop_half" in flags:
            return max(1,(R13_SHOP[key]["price"]+1)//2)
        price=_r13_b3_shop_price(state,key)
        # 은호 remembers being exposed until the facts are set straight (systems/room13_memory.rpy).
        # Otherwise he only heard rumors: bad ones raise the price; a good one makes him hold off.
        if "eunho_hostile" in flags and "eunho_reconciled" not in flags:
            price+=1
        elif any(r in flags for r in R13_BAD_RUMORS) and "rumor:fair" not in flags:
            price+=1
        return price

    R13_EVENING_MISSIONS.append(("ev_o",(5,6),"school","학교 장작더미","대피소 장작이 밤마다 줄어든다고 한다.",
        lambda:not r13_has("ev_o_done") and not r13_has("bori_cleared") and not r13_has("bori_ally")))
    R13_EVENING_PLACE.update(school="학교")

# Arrival scenes (called from r13_town_events).
label r13_b3_events:
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    if _loc in ("square","inn","dining"):
        call r13_b3_whispers
    if _d in (r13_tl(5),r13_tl(6)) and _p<=1 and _loc=="square" and room13["case_state"]=="occurred" and not r13_has("ev_e_done"):
        $ r13_offer("r13_b3_ration")
    if 4<=_d<=r13_tl(6) and _p<=1 and _loc=="post" and not r13_has("ev_u_done") and not r13_has("know_stone_history"):
        $ r13_offer("r13_b3_pages")
    if _d in (r13_tl(5),r13_tl(6)) and _p==2 and _loc=="school" and not r13_has("ev_o_done") and not r13_has("bori_cleared") and not r13_has("bori_ally"):
        call r13_b3_firewood
    return None

label r13_b3_whispers:
    $ _rumors=[r for r in R13_RUMOR_WHISPERS if r13_has(r) and not r13_has("heard:"+r)]
    if not _rumors:
        return
    call r13_ev_here("calm" if room13["period"]<2 else "night")
    while _rumors:
        $ _r=_rumors.pop(0)
        $ r13_flag("heard:"+_r)
        call r13_lines([(None,"지나가는 사람들이 낮게 수군댔다. ‘"+R13_RUMOR_WHISPERS[_r]+"’"),
            ("dad",("(좋은 말도 빨리 돈다. 듣기만 한 사람은 판단을 미루겠지. 직접 겪은 사람 마음까지 바뀌지는 않는다.)" if _r=="rumor:fair" else "(소문이 붙었다. 은호 사장 같은 사람은 이런 말에 값을 올린다.)"),{"thought":True})],"b3:whisper:"+_r)
    return

# ---- D. 은호의 저울 ----
label r13_b3_scale:
    $ _scale_lines=ROOM13["topics"]["eunho_scale"]["lines"]
    call r13_lines(_scale_lines[:1]+[("resident_eunho","……그래서, 저한테 무엇을 원하십니까?")],"b3:scale:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "“조용히 저울만 바로잡으시죠.”":
                call r13_lines(_scale_lines[1:],"b3:scale:quiet")
                $ r13_flag("shop_discount","scale_settled")
            "“사람들도 이 일은 알아야 합니다.”":
                call r13_lines([("resident_eunho","광장에 알리면 이 마을에서 제 장사는 끝납니다. 그래도 하시겠습니까?"),
                    ("dad","그래도 사람들은 자기가 그동안 얼마나 덜 받았는지는 알아야 합니다."),
                    (None,"그날 오후, 광장 게시판에 쪽지가 붙었다. 은호가 저울 바늘을 바로잡았다는 쪽지였다. 사람들이 줄을 서서 다시 무게를 달아 갔다.")],"b3:scale:public")
                $ r13_flag("scale_public","scale_settled","eunho_hostile","rumor:fair")
            "“제 물건만 반값에 주시죠.”":
                call r13_lines([("resident_eunho","……당신 물건만 반값입니다. 대신 저울 일은 다른 사람한테 한 마디도 하지 않는 겁니다."),
                    ("dad","(이러면 나만 값을 덜 내고, 다른 사람들은 계속 물건을 덜 받는다.)",{"thought":True})],"b3:scale:half")
                $ r13_flag("shop_half","scale_settled","eunho_blackmailed")
            "“배급소 저울도 조이셨습니까?”" if r13_has("know_ration_scale") and "H6" not in room13["evidence"]:
                call r13_lines([("resident_eunho","……배급소 저울 일은 구슬이 말했구려."),
                    ("resident_eunho","백 부인의 부탁이었습니다. 배급이 가벼우면 부인 창고 물건이 팔리고, 그 물건을 나르는 일은 내가 맡소."),
                    ("resident_eunho","하지만 배급소 저울은 이제 내가 손댈 수 없습니다. 저울 열쇠를 너울이 갖고 있기 때문이오.")],"b3:scale:ration")
                $ r13_grant(["H6"],"은호가 털어놓은 배급소 저울")
                $ _ep_loop=True
            "다음에 다시 이야기한다":
                pass
    return

# ---- E. 배급표 다툼 (5~6일 낮, 광장) ----
label r13_b3_ration:
    $ r13_flag("ev_e_done")
    call r13_ev_here("search")
    call r13_lines([(None,"광장 배급대 앞에서 줄이 멈춰 있었다. 너울이 보리의 수레 손잡이를 꽉 붙잡고 있었다."),
        ("neoul","배급 장부에 적힌 것보다 감자 한 자루, 장작 세 짐이 모자라오. 이번 주 배급 운반은 보리가 했소."),
        ("resident_bori","전 장부에 적힌 대로 실었어요! 배급소 저울에 단 그대로요."),
        ("neoul","그럼 저울이 거짓말이라도 한다는 거요? 다음 배급 때까지 보리네 몫은 없소.")],"b3:ration:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "도토에게 배급 장부를 보자고 한다" if not r13_has("ration_ledger_seen"):
                call r13_lines([("doto","장부에는 배급소 저울로 잰 무게만 적어요. 그러니까 저울이 맞으면 장부도 맞는 거고요."),
                    ("dad","(문제는 장부가 아니다. 저울을 봐야 한다.)",{"thought":True})],"b3:ration:ledger")
                $ r13_flag("ration_ledger_seen")
                $ _ep_loop=True
            "배급소 저울을 다시 재자고 한다" if r13_has("know_ration_scale") or "H6" in room13["evidence"]:
                call r13_lines([("dad","표준 추로 배급소 저울이 맞는지 다시 대조해 봅시다. 가게 저울은 이미 눈금이 한 칸 더 나가 있었습니다."),
                    (None,"도토가 표준 추를 올렸다. 바늘이 제 눈금보다 한 칸 더 기울었다. 줄 선 사람들이 웅성거렸다."),
                    ("doto","……한 칸이나 틀리면 집마다 감자 서너 알씩 덜 받은 거예요. 모자란 건 보리가 가져간 게 아니에요."),
                    ("neoul","배급소 저울은 내가 직접 확인하겠소. 보리는 이만 가도 좋소.")],"b3:ration:scale")
                $ r13_flag("bori_cleared","ration_fixed","rumor:fair","neoul_annoyed")
            "백 부인 비축 장부를 보여 준다" if "H1" in room13["evidence"]:
                call r13_lines([("dad","배급이 모자랐던 날마다 백 부인 창고에는 같은 물건이 그만큼 늘었습니다. 이 장부에 다 적혀 있습니다."),
                    ("resident_ppul","……이 장부는 대체 누가 쓴 거요?"),
                    ("neoul","백 부인 글씨구려. 보리는 가시오. 장부 일은 내가 부인에게 따로 묻겠소.")],"b3:ration:h1")
                $ r13_flag("bori_cleared","madam_exposed","madam_hostile","rumor:fair")
            "모자란 몫을 대신 낸다 (6냥)" if r13_cash_now()>=6:
                $ r13_cash(-6,"보리네 배급 몫")
                call r13_lines([("neoul","외지 사람이 왜 남의 집 몫을 대신 내오? ……뭐, 돈은 받겠소. 보리는 가도 좋소."),
                    ("resident_bori","이 돈은 꼭 갚을게요. 장작으로든 뭐로든요.")],"b3:ration:pay")
                $ r13_flag("bori_ally","bori_paid")
            "“보리가 가져갔다는 증거가 있습니까?”" if not r13_has("bori_defended"):
                call r13_lines([("dad","보리가 모자란 몫을 가져갔다는 증거는 없지 않습니까."),
                    ("neoul","그럼 누가 가져갔는지 증거를 대 보시오. 말만으로는 안 되오.")],"b3:ration:defend")
                $ r13_flag("bori_defended","bori_trust")
                $ _ep_loop=True
            "끼어들지 않고 지켜본다":
                call r13_lines([(None,"보리는 빈 수레를 끌고 줄 끝으로 물러났다. 아무도 보리 쪽을 쳐다보지 않았다.")],"b3:ration:watch")
                $ r13_flag("bori_punished")
    return

# ---- O. 학교 장작 (5~6일 저녁 미션) ----
label r13_b3_firewood:
    $ r13_flag("ev_o_done")
    call r13_ev_here("night")
    call r13_lines([(None,"학교 뒤 대피소 장작더미 옆에서 누군가 장작을 끈으로 묶고 있었다. 보리였다."),
        ("resident_bori","……보셨어요? 소리 지르지 마세요. 딱 한 짐만 가져가려는 거예요.")],"b3:wood:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "왜 장작을 가져가는지 묻는다" if not r13_has("bori_reason"):
                call r13_lines([("resident_bori","우리 집 배급이 끊겼어요. 엄마는 밤새 기침하고요. 장작은 매일 제가 나르는데, 정작 우리 집 난로는 꺼져 있어요."),
                    ("dad","(남의 장작을 나르는 집이 제일 춥게 지낸다.)",{"thought":True})],"b3:wood:why")
                $ r13_flag("bori_reason")
                $ r13_grant(["W8"],"학교 장작더미 옆에서 들은 보리의 사정")
                $ _ep_loop=True
            "사자 선생님을 부른다":
                call r13_lines([("resident_teacher","보리야……. 대피소 장작은 아이들 몫이야. 알잖니."),
                    ("resident_bori","알아요. 그래서 딱 한 짐만 가져가려고 했던 거예요."),
                    (None,"보리는 장작을 내려놓았다. 그러고는 뒤도 돌아보지 않고 가 버렸다.")],"b3:wood:teacher")
                $ r13_flag("teacher_trust","bori_hostile")
            "대피소 장작을 대신 나르겠다고 한다":
                call r13_lines([("dad","내일 대피소 장작은 제가 대신 날라 두겠습니다. 그러니 이 한 짐은 보리네 집으로 보내 주세요."),
                    ("resident_teacher","……그렇게 해 주신다면요. 아이들 몫이 줄지만 않으면 돼요."),
                    ("resident_bori","손님이 왜 그렇게까지 해요? ……고마워요.")],"b3:wood:labor")
                $ r13_flag("bori_ally","teacher_trust","shelter_wood_promise")
            "장작값을 대신 낸다 (6냥)" if r13_cash_now()>=6:
                $ r13_cash(-6,"보리네 장작값")
                call r13_lines([("resident_bori","……이 돈이면 사흘은 집을 데울 수 있어요. 이 돈은 꼭 갚을게요.")],"b3:wood:pay")
                $ r13_flag("bori_ally")
            "모른 척 지나간다":
                call r13_lines([(None,"등 뒤로 장작 묶는 소리가 계속 들렸다. 다음 날 아침, 대피소 장작은 한 짐이 모자랐다.")],"b3:wood:ignore")
                $ r13_flag("shelter_short")
    return

# ---- U. 사서의 기록 장 (4~6일 낮, 우체국) ----
label r13_b3_pages:
    $ r13_flag("ev_u_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"사서 선생님이 우체국 구석 책상에서 낡은 장부를 뜯고 있었다. 뜯은 장은 끈으로 묶었다. 맞은편에 은호 사장이 감자 자루를 내려놓았다."),
        ("resident_eunho","도시 수집가들은 옛 마을 기록을 좋아합니다. 이 장부 묶음이면 감자 사흘 치 값은 됩니다."),
        ("resident_librarian","……돌에 관한 기록은 이제 아무도 안 읽어요. 팔아서라도 굶지 않는 게 낫지요.")],"b3:pages:open")
    menu:
        "팔기 전에 장부를 보여 달라고 한다":
            call r13_lines([("resident_librarian","보시려면 지금 보세요. 오후면 이 장부는 도시로 가는 짐에 실려요.")],"b3:pages:read")
            call r13_lines(ROOM13["topics"]["librarian_stone"]["lines"],"b3:pages:stone")
            $ r13_grant(["W3"],"팔려 가기 전에 본 돌의 옛 기록")
            $ r13_flag("know_stone_history","pages_sold")
        "감자 값을 대신 내고 장부를 지킨다 (6냥)" if r13_cash_now()>=6:
            $ r13_cash(-6,"사서 선생님의 끼니")
            call r13_lines([("resident_eunho","돈을 받았으니 장사는 장사요. 감자는 그대로 두고 가겠습니다."),
                ("resident_librarian","……이 장부, 아무도 안 읽는다고 했지만 실은 제가 매일 읽어요. 보여 드릴게요.")],"b3:pages:save")
            call r13_lines(ROOM13["topics"]["librarian_stone"]["lines"],"b3:pages:stone")
            $ r13_grant(["W3"],"사서 선생님이 지킨 돌의 옛 기록")
            $ r13_flag("know_stone_history","librarian_trust")
        "장부를 베낄 시간을 달라고 한다":
            call r13_lines([("resident_eunho","베끼는 건 마음대로 하십시오. 저는 원본만 넘겨받으면 됩니다."),
                ("resident_librarian","그럼 오늘 밤에 장부를 베껴 둘게요. 내일 다시 와 보세요.")],"b3:pages:copy")
            $ r13_flag("pages_sold","pages_copy_promised")
        "모른 척 지나간다":
            call r13_lines([(None,"끈으로 묶인 장부는 결국 은호의 자루 위에 얹혔다.")],"b3:pages:ignore")
            $ r13_flag("pages_sold")
    return

label r13_b3_buy_pages:
    call r13_lines([("dad","사서 선생님한테 받은 장부 묶음, 아직 가지고 계십니까?"),
        ("resident_eunho","도시로 가는 짐은 모레 떠납니다. 사시려면 열두 냥입니다. 제가 치른 감자 값에 운반비를 얹은 겁니다.")],"b3:buy:open")
    menu:
        "열두 냥에 산다" if r13_cash_now()>=12:
            $ r13_cash(-12,"돌의 옛 기록 장부")
            call r13_lines([("resident_eunho","서로 좋은 거래였습니다."),
                (None,"장부 묶음을 풀자 돌에 관한 장이 나왔다.")],"b3:buy:paid")
            call r13_lines(ROOM13["topics"]["librarian_stone"]["lines"],"b3:buy:stone")
            $ r13_grant(["W3"],"은호에게서 되산 돌의 옛 기록")
            $ r13_flag("know_stone_history")
        "사서 선생님이 베낀 사본을 묻는다" if r13_has("pages_copy_promised"):
            call r13_lines([("resident_eunho","베낀 사본은 사서 선생님한테 있을 거요. 나한테는 원본만 있습니다.")],"b3:buy:copy")
            $ r13_flag("librarian_copy_ready")
        "다음에 산다":
            pass
    return
