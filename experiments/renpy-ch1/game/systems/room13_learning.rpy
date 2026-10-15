# Learning follows an owned observation. These helpers never grant clues,
# advance time, or write flags simply because a menu is opened.
init 98 python:
    R13_PUBLIC_ROLES = {
        "dad":"다람이의 아빠", "daram":"함께 온 딸", "mom":"찾고 있는 엄마",
        "guard":"입구 경비", "karo":"마부", "granny":"여관 주인",
        "nabi":"여관 식사 준비", "buri":"수리점", "seryeon":"우체국",
        "doto":"장부 정리", "bami":"여관에 있는 아이", "neoul":"경비",
        "resident_tori":"수선", "resident_bori":"장작 운반", "resident_yeoni":"옷 수선",
        "resident_kongi":"가게 심부름", "resident_kkwak":"물 나르기",
        "resident_librarian":"사서", "resident_owlgp":"마을 어르신", "resident_teacher":"학교",
        "resident_nero":"마을 밖 노동", "resident_seol":"종 관리", "resident_ppul":"촌장",
        "resident_tok":"부품 손질", "resident_sling":"우편 배달", "resident_momo":"박물관",
        "resident_ttadak":"건물 수리", "resident_piko":"그림", "resident_mungchi":"짐 운반",
        "resident_madam":"물자 나누기", "resident_siluk":"수레 운반", "resident_musoe":"도구 손질",
        "resident_somi":"진료", "resident_seori":"사실 확인", "resident_ubak":"측정",
        "resident_nubi":"세탁", "resident_eunho":"상점", "resident_guseul":"물품 확인",
        "resident_badook":"순찰", "resident_lamplighter":"등불 돌보기",
    }

    def r13_person_caption(person):
        name=R13_NAMES.get(person,person or "")
        role=R13_PUBLIC_ROLES.get(person)
        return name+" · "+role if role else name

    def r13_learning_archive_seed():
        return [k for k in (getattr(persistent,"room13_knowledge",[]) or []) if k in ROOM13["evidence"]]

    def r13_learning_archive_keys(state=None):
        # Each run starts from zero (owner's rule, systems/room13_no_carryover.rpy):
        # no earlier-run record is shown, whatever an old save holds.
        return []

    def r13_learning_time_text(cost=0,state=None,ending=False):
        s=(store.room13 or {}) if state is None else state
        if ending:return "시간 소모 없음 · 이번 여정이 끝날 수 있음"
        if not cost:return "시간 소모 없음"
        period=min(3,max(0,int(s.get("period",0))))
        if period>=3:return "오늘은 더 진행할 시간이 없음"
        target=("오후","저녁","늦은 저녁")[min(2,period+int(cost)-1)]
        return "한나절 사용 · 끝나면 "+target

    def r13_learning_lodging_preview(state=None,additional=0):
        s=(store.room13 or {}) if state is None else state
        wallet=r13_wallet(s)
        fee=0 if s.get("day",1)==1 or s.get("day",1) in wallet["settled"] else 10
        cash=wallet["cash"]+additional
        paid=min(cash,fee)
        return dict(fee=fee,paid=paid,left=cash-paid,added_debt=fee-paid,debt=wallet["debt"]+fee-paid)

    def r13_learning_settlement_text(state=None,additional=0,compact=False):
        p=r13_learning_lodging_preview(state,additional)
        if not p["fee"]:return "오늘 숙식비 없음 · 가진 돈 %d냥"%p["left"]
        if p["added_debt"]:
            text="밤 정산: %d냥 납부 · %d냥 외상"%(p["paid"],p["added_debt"])
            return text if compact else text+" · 돈이 모자라도 잘 수 있음"
        return "밤 정산: 숙식비 10냥 · 남는 돈 %d냥"%p["left"]

    def r13_learning_sleep_text():
        s=store.room13 or {}
        # On day four sleep can enter the existing evening event; do not promise
        # that confirmation will skip directly to tomorrow.
        event_night=s.get("day")==4 and s.get("case_state")=="pending"
        if event_night:return "오늘 찾은 것은 기록에 남아 있다. 오늘 조사를 마치고 저녁을 맞을까요?"
        text="오늘 찾은 것은 기록에 남아 있다. 잠들면 다음 날 아침이 됩니다."
        if s.get("life_poc") or "livelihood_open" in s.get("flags",[]):
            text+="\n"+r13_learning_settlement_text(s)
        if s.get("period",0)<2:
            text+="\n아직 남은 낮 시간은 쓰지 않고 하루를 마칩니다."
        return text

    R13_JOB_CONTEXT = {
        "kitchen":"나비와 손님들의 식기를 정리한다.",
        "delivery":"까로와 집마다 다른 짐표를 살핀다.",
        "repair":"부리와 실제 부품 수를 맞춘다.",
    }

    def r13_learning_job_context(key,state=None):
        s=(store.room13 or {}) if state is None else state
        flags=set(s.get("flags",[]));read=set(s.get("read_topics",[]))
        # The board says only what the job is (owner, 0.18.16): no remaining-question or trick hints.
        return R13_JOB_CONTEXT.get(key,"")

    def r13_learning_record_status(key):
        s=store.room13 or {}
        if key=="E10":
            return "이름 공개 허락 있음 · 회의에서 사용 가능" if "bami_consent" in s.get("flags",[]) else "내용은 전할 수 있음 · 회의에서 쓰려면 밤이의 이름 공개 허락 필요"
        if ROOM13["evidence"][key]["kind"]=="증언":
            who=ROOM13.get("evidence_sources",{}).get(key)
            return "말한 사람: "+R13_NAMES.get(who,"기록에 적힌 발언자")
        return "직접 조사해 기록한 물건·문서·관찰"

    R13_LEARNING_TERMS = (
        dict(title="돌에 남은 힘",need=["E21"],text="장치를 돌리는 데 쓰이고, 쓰면 줄어드는 양이다. 기록에서는 얼마나 남았는지와 얼마나 오래 버텼는지를 함께 본다."),
        dict(title="힘을 옮긴다는 것",need=["E23"],text="다른 돌의 남은 힘을 한곳으로 모으는 일이다. 이번 관찰에서는 준 돌의 힘이 줄고, 받은 돌의 빛이 고르게 유지됐다. 모두 합한 양은 늘지 않았다."),
        dict(title="더 많이 쓰는 저녁",need=["E24"],text="낮에 버텼다는 사실만으로 밤도 버틴다고 할 수는 없다. 더 많이 쓸 때의 지속 시간과 새어 나간 양도 확인한 기록이다."),
        dict(title="환자의 회복과 ‘야생화’",need=["E20"],text="‘야생화’는 말과 판단을 잃어가는 상태를 가리키는 마을의 표현이다. 회복 관찰은 일부 환자에게 돌아오는 반응이 있었다는 자료다. 모두가 회복한다는 뜻까지 확인한 것은 아니다."),
        dict(title="‘희생’이라는 말",need=["E22"],text="시설의 원래 기록에서 말하는 ‘희생’은 사람의 죽음이다. 사람에게서 힘을 뽑아도 힘이 잠깐만 오른다는 내용까지 함께 적혀 있다."),
        dict(title="룬 · 옛 장치에 남은 문자",need=["E30"],text="엄마가 연구한 오래된 문자와 장치의 사용 흔적이다. 문자의 이름을 외우는 것보다, 연구에서 무엇을 알아냈고 실제로 무엇을 확인했는지 나눠 보는 것이 중요하다."),
    )

    def r13_learning_terms(state=None):
        s=(store.room13 or {}) if state is None else state
        owned=set(s.get("evidence",[]))
        return [dict(note) for note in R13_LEARNING_TERMS if set(note["need"])<=owned]

    _r13_learning_record_entries=r13_record_entries
    def r13_record_entries(category="evidence",archive=False,present=False,order="acquired",favorite_only=False):
        entries=_r13_learning_record_entries(category,archive,present,order,favorite_only)
        if archive and not present:
            allowed=set(r13_learning_archive_keys())
            return [key for key in entries if key in allowed]
        return entries

    _r13_learning_mystery_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        s=store.room13 or {}
        rows=_r13_learning_mystery_notes()
        if s.get("life_poc") and "entry_corrected" not in s.get("flags",[]):
            owned=set(s.get("evidence",[]))
            rows=[dict(title="둘이 예약했는데 왜 한 명으로 적혔을까?",fact="경비가 받은 이름 목록에는 아빠 한 명만 적혀 있다고 했다.",question="예약할 때 낸 원본도 한 명으로 되어 있을까?",hint="선반의 서류를 읽고, 다람이와 함께 원본과 옮긴 목록을 비교해 보자.",keys=[k for k in ("G1","G3") if k in owned])]
        return rows

screen r13_learning_notes():
    modal True
    zorder 97
    default tab="questions"
    default expanded=None
    add Solid("#102725fa")
    text "조사 메모" style "r13_title_text" xpos 48 ypos 30 color "#efd4a1"
    hbox:
        xpos 48 ypos 94 spacing 14
        for key,title in (("questions","지금 궁금한 것"),("observations","자세히 본 것"),("world","알게 된 세계")):
            if key!="world" or r13_learning_terms():
                textbutton title:
                    style "r13_action_button" xsize 280 ysize 48 text_size r13_read_size(22,27)
                    selected tab==key action [SetScreenVariable("tab",key),SetScreenVariable("expanded",None)]
    viewport:
        area (48,168,1184,444) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 16
            if tab=="questions":
                for i,note in enumerate(r13_first_mystery_notes()):
                    frame:
                        xsize 1144 padding R13_UI_PADDING["panel"] background R13ActionPanel()
                        vbox:
                            spacing 12
                            text note["title"] style "r13_key_text" size r13_read_size(26,31) color "#efd4a1" xsize 1088
                            text ("확인한 것 · "+note["fact"]) size r13_read_size(23,28) color "#fff2cf" xsize 1088
                            text ("모르는 것 · "+note["question"]) size r13_read_size(23,28) color "#a8cdec" xsize 1088
                            $ owned_keys=[k for k in note["keys"] if k in room13.get("evidence",[])]
                            if owned_keys:
                                text ("함께 볼 기록 · "+" / ".join(R13_RECORD_SHORT.get(k,ROOM13["evidence"][k]["name"]) for k in owned_keys)) size r13_read_size(20,25) color "#d4dfd8" xsize 1088
                            textbutton ("접기" if expanded==i else "막혔다면 생각 정리"):
                                style "r13_action_button" xsize 300 ysize 48 text_size r13_read_size(21,26)
                                action SetScreenVariable("expanded",None if expanded==i else i)
                            if expanded==i:
                                text note["hint"] size r13_read_size(22,27) color "#d4dfd8" xsize 1088
            elif tab=="observations":
                for note in r13_tool_notes():
                    frame:
                        xsize 1144 padding R13_UI_PADDING["panel"] background R13ActionPanel()
                        vbox:
                            spacing 12
                            text note["title"] style "r13_key_text" size r13_read_size(26,31) color "#efd4a1"
                            text note["summary"] size r13_read_size(23,28) color "#fff2cf" xsize 1088
                            text ("질문 완료 · "+R13_NAMES[note["person"]] if note["topic"] in room13.get("read_topics",[]) else note["followup"]) size r13_read_size(21,26) color "#d4dfd8" xsize 1088
                if not r13_tool_notes():
                    text "돋보기로 자세히 살핀 내용이 여기에 모입니다." size r13_read_size(23,28) color "#d4dfd8"
            else:
                for note in r13_learning_terms():
                    frame:
                        xsize 1144 padding R13_UI_PADDING["panel"] background R13ActionPanel()
                        vbox:
                            spacing 12
                            text note["title"] style "r13_key_text" size r13_read_size(26,31) color "#efd4a1"
                            text note["text"] size r13_read_size(23,28) color "#fff2cf" xsize 1088
    text "기록을 읽고 정리해도 시간은 흐르지 않습니다." xpos 48 ypos 658 size r13_read_size(19,23) color "#d4dfd8"
    textbutton "닫기" style "r13_action_button" area (970,642,260,62) text_size r13_read_size(23,28) action Hide("r13_learning_notes")
    key "game_menu" action Hide("r13_learning_notes")
