# Approaching general events is a choice (owner, 0.18.19).
#   Arriving no longer starts a long ordinary event. The scene shows what is happening as a marker;
#   clicking it enters the event. Passing by lets the event run on its own schedule: when the time
#   slot ends, the outcome is that of the event's own "look away" branch, and Dad hears of it later.
#   Events about 다람이's safety or an accident right in front of Dad still start by themselves.
init 124 python:
    # label: (marker text, flags when passed by, what Dad hears later)
    R13_EVENT_OFFERS={
        "r13_w1c_portrait":("광장 구석에서 피코가 판자에 물감을 문지르고 있다",["ev_g_done"],"광장 구석의 그림 장수는 저녁 전에 자리를 걷었다고 했다."),
        "r13_w1c_letters":("우체국 안쪽에서 슬링이 봉투를 김에 쐬고 있다",["ev_l_done","warning_exposed"],"우체국 화덕 위에서 누군가 봉투를 김에 쐬고 있었다는 말을 들었다."),
        "r13_w1c_extension":("여관 뒷벽에서 따닥이 판자를 덧대고 있다",["ev_i_done"],"여관 뒷벽 공사는 그날 끝났다고 했다."),
        "r13_w1c_seal":("봉해 둔 13호 문 앞에서 뭉치가 서성인다",["ev_s_done","family_items_lost"],"봉해 둔 13호에서 누군가 물건을 꺼내 갔다는 말을 들었다."),
        "r13_w1c_testimony":("실룩이 사람들 사이를 오가며 귓속말을 한다",["ev_t_done"],"실룩이 재판에 쓸 증언을 팔러 다닌다는 말이 돌았다."),
        "r13_b3_ration":("배급대 앞에서 줄이 멈춰 있다",["ev_e_done","bori_punished"],"배급대 앞에서 보리가 빈 수레로 돌아갔다는 말을 들었다."),
        "r13_b3_pages":("사서 선생님이 우체국 구석에서 옛 장부를 묶고 있다",["ev_u_done","pages_sold"],"우체국 구석의 옛 장부가 은호의 자루로 넘어갔다고 했다."),
        "r13_w2e_bell":("종탑 아래에서 설이와 너울이 다투고 있다",["w2e_k_done","w2_bell_silent"],"그날 밤 불이 꺼진 두 집 사람들은 아침이 되어서야 학교에 왔다고 했다."),
        "r13_w2e_numbers":("수리점 작업대에 계측 장부가 펼쳐져 있다",["w2e_p_done","numbers_forged"],"수리점 계측 장부에서 숫자 하나가 지워졌다는 말을 들었다."),
        "r13_w2e_tools":("부리가 할아버지 공구함 앞에 서 있다",["w2e_w_done","tools_sold"],"부리의 할아버지 공구함이 은호의 자루로 넘어갔다고 했다."),
        "r13_ep3_bell":("광장의 등이 한꺼번에 깜빡인다. 종탑 아래가 소란스럽다",["ep3_bell_seen","stone_hidden","bori_child_sick"],"그날 밤 종은 울리지 않았다. 아침에 보리네 아이가 열이 난다는 말을 들었다."),
        "r13_ep4_accused":("수리점 앞에 사람들이 모여 있다",["ep4_seen","ep4_open"],"수리점 앞에서 너울이 톡을 몰아세웠다는 말을 들었다."),
        "r13_ev_b_store":("창고 앞에서 백 부인이 누군가를 몰아세우고 있다",[],""),
    }

    def r13_offer(label):
        s=store.room13
        offers=dict(s.get("offers",{}))
        if label in offers:return
        offers[label]=dict(day=s["day"],period=s["period"],location=s["location"])
        r13_edit(offers=offers)
        # Screen tests written before 0.18.19 expect the old start-on-arrival.
        if "qa_auto_offer" in s.get("flags",[]):renpy.call("r13_take_offer",label)

    def r13_offers_here():
        s=store.room13 or {}
        return [(k,R13_EVENT_OFFERS[k][0]) for k,o in s.get("offers",{}).items()
            if k in R13_EVENT_OFFERS and o["day"]==s.get("day") and o["period"]==s.get("period") and o["location"]==s.get("location")]

    def r13_offers_tick():
        """Offers whose time slot has passed run without Dad: apply the look-away outcome."""
        s=store.room13;offers=dict(s.get("offers",{}));news=list(s.get("offer_news",[]));changed=False
        for k,o in list(offers.items()):
            if (o["day"],o["period"])!=(s["day"],s["period"]):
                text,flags,heard=R13_EVENT_OFFERS.get(k,("",[],""))
                if flags:r13_flag(*flags)
                if k=="r13_w2e_tools" and not r13_has("tok_cleared"):r13_flag("tools_missing")
                if heard:news.append(heard)
                offers.pop(k);changed=True
        if changed:r13_edit(offers=offers,offer_news=news)

label r13_offer_news:
    $ r13_offers_tick()
    if room13.get("offer_news"):
        $ _news=list(room13["offer_news"])
        $ r13_edit(offer_news=[])
        call r13_lines([(None,n) for n in _news],"offer:news:%d:%d"%(room13["day"],room13["period"]))
    return

label r13_take_offer(label):
    $ _o=dict(room13.get("offers",{}))
    $ _o.pop(label,None)
    $ r13_edit(offers=_o)
    call expression label
    return _return

screen r13_event_offers(ready=False):
    $ offers=r13_offers_here()
    if offers:
        vbox:
            xpos 24 ypos 236 spacing 8
            for key,text in offers:
                textbutton ("! "+text):
                    style "r13_action_button" xmaximum 620 padding (14,8) text_size r13_read_size(19,23)
                    action Return(("offer",key)) sensitive ready
                    tooltip "가까이 가서 본다"
