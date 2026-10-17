# 포가튼 시티형 시간 흐름 (소유자 승인 2026-10-17, 노션 「Room13 시간 흐름 레퍼런스와 개선안 A·B·C」 시안 v4)
# - 날짜는 세계 일정표다(1일 금요일, 13호 사건 7일, 재판 10일, 2주차 11일~). 하루는 0 오전 · 1 오후 · 2 저녁 · 3 늦은 저녁(밤).
# - 대화·조사·이동·자료 보여주기는 시간을 쓰지 않는다. 조사 활동(ROOM13["activities"])의 cost는 모두 0이다.
# - 시간은 셋으로만 흐른다.
#   1. 사건을 끝냈을 때: 사건 제안(R13_EVENT_OFFERS)이나 에피소드 장면이 끝나면 다음 시간대(+1, 밤에서는 그대로).
#      장면 안에서는 r13_event_tick()을 부른다. r13_take_offer는 장면이 시간을 넘기지 않았으면 끝날 때 한 칸 넘긴다.
#   2. "오후까지/저녁까지 기다린다"(장소 화면 오른쪽 아래, 오전·오후에만).
#   3. 잠(기존 그대로).
# - 사건이 있는 사람: 장소 화면에는 이름표 옆 ! 하나. 그 사람 대화 선택지 끝에 ! 사건 줄과 결과 꼬리표("끝나면 오후가 됩니다").
# - 시간이 넘어가면 시간대 카드가 잠깐 뜬다(입력을 막지 않는다). 열린 일은 기존 "생각" 접기 안에 적는다.
default r13_tf_event_handled = False

init 191 python:
    R13_TF_AFTER = ("끝나면 오후가 됩니다","끝나면 저녁이 됩니다")
    R13_TF_WAIT = ("오후까지 기다린다","저녁까지 기다린다")
    # 시간대 카드의 이야기 문장(화면 꼬리표에는 "해가 기운다" 같은 말을 쓰지 않는다. 노션 v4).
    R13_TF_STORY = {
        1:"해가 기울기 시작했다. 그림자가 길어졌다.",
        2:"해가 졌다. 집집마다 등불이 켜졌다.",
        3:"밤이 깊었다. 거리의 발소리가 끊겼다.",
    }

    # 그 사람 대화 선택지에 붙는 사건 줄(24자 이하). 없으면 R13_TF_OFFER_DEFAULT.
    R13_TF_OFFER_DEFAULT = "무슨 일인지 가까이 가 본다"
    R13_OFFER_CHOICES = {
        "r13_w1c_portrait":"피코의 그림판을 들여다본다",
        "r13_w1c_letters":"김에 쐬는 봉투를 묻는다",
        "r13_w1c_extension":"덧대는 판자 일을 지켜본다",
        "r13_w1c_seal":"13호 문 앞에서 무얼 하는지 묻는다",
        "r13_w1c_testimony":"실룩의 귓속말을 엿듣는다",
        "r13_b3_pages":"묶고 있는 옛 장부를 묻는다",
        "r13_b3_pages_eunho":"자루에 담는 장부를 묻는다",
        "r13_w2e_tools":"공구함 앞에 같이 앉는다",
        "r13_ep4_accused":"수리점 앞 소동에 끼어든다",
        "r13_ev_b_store":"창고 앞 소동에 끼어든다",
        "r13_nc_tosil_friend":"과자 봉지를 보는 토실에게 간다",
        "r13_nc_mulgyeol_ice":"기우는 썰매 배로 달려간다",
        "r13_nc_solbang_herbs":"빈 바구니 사정을 묻는다",
        "r13_nc_dalgeurak_news":"바깥 소식을 들어 본다",
        "r13_st_dodam":"열 나는 아이를 같이 살핀다",
        "r13_nt_overhear":"너울의 말을 엿듣는다",
        "r13_ep1_accused":"수리점 앞 소동에 끼어든다",
        "r13_ep1_meeting":"광장 회의에 나선다",
        "r13_wf_laundry":"빨래터에 남아 지켜본다",
        "r13_wf_nabi_blame":"주저앉은 나비 곁에 간다",
        "r13_wf_nubi":"꺼진 솥 앞의 누비에게 간다",
        "r13_wf_meeting":"학교 회의에 나선다",
        "r13_ws_lowroad":"네로의 불가에 앉는다",
        "r13_ws_teacher_talk":"출석부 이야기를 듣는다",
        "r13_cv_market":"수레 쪽지를 보여 달라고 한다",
        "r13_cv_store":"쪽문 앞 뭉치에게 간다",
        "r13_cv_stable":"말 손질하는 실룩에게 간다",
        "r13_cv_hall":"명령서를 보여 달라고 한다",
    }

    # 대화 주제이면서 끝나면 시간이 흐르는 사건(장면 안에서 r13_event_tick을 부른다). key: 시간이 흐를 조건.
    R13_TF_EVENT_TOPICS = {
        "ep1:nabi_shelter":lambda:r13_has("nabi_helped") or r13_has("lt_piko_promise"),
    }

    # 조사 활동은 시간을 쓰지 않는다(0.18.5 room13_evening.rpy가 init 106에서 0으로 맞춘 뒤 더해진 활동까지).
    for _a in ROOM13["activities"].values():
        _a["cost"]=0

    class R13EventTitle(str):
        """A question-row title that marks an event row (! and the time tag on the right)."""
        def __new__(cls,text,tag=None):
            obj=str.__new__(cls,text)
            obj.r13_event=True
            obj.r13_tag=tag
            return obj

    def r13_tf_after_text(period=None):
        s=store.room13 or {}
        p=s.get("period",0) if period is None else period
        return R13_TF_AFTER[p] if 0<=p<len(R13_TF_AFTER) else None

    def r13_tf_wait_text():
        s=store.room13 or {}
        # 1일은 도착·첫날 밤 흐름이 따로 있다.
        if not s or s.get("day",1)<=1:
            return None
        p=s.get("period",0)
        return R13_TF_WAIT[p] if 0<=p<len(R13_TF_WAIT) else None

    def r13_tf_open_items():
        """열린 일: 열린 회의의 마감, 오늘 저녁 일. 알아낸 것만(표식이 선 회의만)."""
        s=store.room13 or {}
        rows=[]
        names=("오전","오후","저녁","늦은 저녁")
        for claim,opened,done,(dd,dp),name,early in R13_MEETING_CLOCK:
            if r13_has(opened) and not r13_has(done) and s.get("day",1)*4+s.get("period",0)<=dd*4+dp:
                rows.append("%s · %d일 %s까지"%(name,dd,names[dp]))
        for key,place,title,hint in r13_evening_missions():
            rows.append("오늘 저녁 · %s · %s"%(title,R13_EVENING_PLACE.get(place,place)))
        return rows

    def r13_tf_show_card(before,after):
        s=store.room13
        if not s or after==before:return
        items=r13_tf_open_items()
        card=dict(day=s["day"],weekday=r13_weekday(s["day"]),before=("오전","오후","저녁","늦은 저녁")[before],
            after=("오전","오후","저녁","늦은 저녁")[after],place=R13_PLACES.get(s.get("location"),("",))[0],
            story=R13_TF_STORY.get(after,""),urgent=items[0] if items else None)
        renpy.show_screen("r13_tf_time_card",card=card)

    def r13_tf_advance(steps=1):
        s=store.room13
        if not s:return False
        before=s["period"];target=min(3,before+max(0,int(steps)))
        if target==before:return False
        for _ in range(target-before):
            r13_tick()
        r13_tf_show_card(before,store.room13["period"])
        return True

    def r13_event_tick(steps=1):
        """An event (offer or episode scene) has ended: the next time slot. Evening stays evening until sleep
           (owner rule, docs/HANDOFF_20261017.md 1절: 저녁 이후는 그대로), so the evening's other errands stay open."""
        store.r13_tf_event_handled=True
        if steps and (store.room13 or {}).get("period",0)<2:r13_tf_advance(min(steps,2-store.room13["period"]))

    def r13_tf_offer_questions(person):
        key=r13_offer_for_person(person)
        if not key:return []
        return [(R13EventTitle(R13_OFFER_CHOICES.get(key,R13_TF_OFFER_DEFAULT),r13_tf_after_text()),Return("offer:"+key),False)]

    def r13_tf_mark_event_topics(questions,rows):
        """Event topics (R13_TF_EVENT_TOPICS) get the ! and the time tag."""
        out=[]
        for (title,action,seen),(key,spec) in zip(questions,rows):
            test=R13_TF_EVENT_TOPICS.get(key)
            if test and not seen and test():
                title=R13EventTitle(title,r13_tf_after_text())
            out.append((title,action,seen))
        return out

    def r13_tf_topic_questions(person):
        rows=r13_topics_in_order(person)
        questions=[(r13_calendar_topic_title(key,spec),Return(key),r13_calendar_topic_seen(key,spec)) for key,spec in rows]
        return r13_tf_mark_event_topics(questions,rows)+r13_tf_offer_questions(person)

    # Pressing a person with an event opens their questions; the event is a row there (! 사건 줄).
    _r13_tf_person_action=r13_person_action
    def r13_person_action(person,entry=False):
        return Return(("person",person))

transform r13_tf_card_fade:
    alpha 0.0
    linear .25 alpha 1.0
    pause 2.6
    linear .4 alpha 0.0

# 시간대 카드(시안 3): 입력을 막지 않고 잠깐 떴다 사라진다.
screen r13_tf_time_card(card):
    zorder 70
    timer 3.3 action Hide("r13_tf_time_card")
    frame at r13_tf_card_fade:
        xalign .5 ypos 190 xsize 500 padding (36,24,36,26) background R13PaperFrame()
        vbox:
            spacing 10
            hbox:
                spacing 14
                text ("%02d"%card["day"]) size 64 color "#6c512a" font r13_ui_font() yalign 1.0
                text ("일째 · %s요일"%card["weekday"]) size r13_read_size(24,28) color "#493b30" font r13_ui_font() yalign .8
            hbox:
                spacing 22
                text card["before"] size r13_read_size(30,34) color "#a88a5a" font r13_ui_font()
                text "→" size r13_read_size(30,34) color "#a88a5a" font r13_ui_font()
                text card["after"] size r13_read_size(30,34) color "#b36b25" font r13_ui_font()
            if card["place"]:
                text card["place"] size r13_read_size(22,26) color "#493b30" font r13_ui_font()
            add Solid("#b8a27a") xsize 428 ysize 2
            if card["story"]:
                text card["story"] size r13_read_size(19,23) color "#4f4236" font r13_ui_font() xsize 428
            if card["urgent"]:
                text card["urgent"] size r13_read_size(18,22) color "#a8452e" font r13_ui_font() xsize 428

# "오후까지/저녁까지 기다린다"(시안 1 C): 기록 단추 왼쪽, 오전·오후에만.
screen r13_tf_wait_button(ready=False):
    $ label=r13_tf_wait_text()
    if label:
        textbutton (label+" ›"):
            style "r13_action_button"
            xpos (998 if persistent.room13_large_text else 1038) xanchor 1.0
            ypos (650 if persistent.room13_large_text else 664)
            xsize 250 ysize (70 if persistent.room13_large_text else 56)
            text_size r13_read_size(20,23) text_xalign .5
            action Return(("menu","tf_wait")) sensitive ready
            tooltip r13_tf_after_text()

label r13_tf_wait:
    $ _tf_wait_label=r13_tf_wait_text()
    if not _tf_wait_label:
        return None
    call screen r13_confirm(_tf_wait_label+"\n"+r13_tf_after_text(),"기다린다","돌아간다")
    if _return:
        $ r13_tf_advance(1)
    return None

# 대화 선택지의 ! 사건 줄. 끝나면 r13_take_offer가 시간을 넘긴다. "day"를 돌려주면 하루가 끝난 것이다.
label r13_tf_offer_from_talk(key):
    if key not in [k for k,t in r13_offers_here()]:
        return None
    call r13_take_offer(key)
    return _return
