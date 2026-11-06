# 피코의 죽음은 화면 안에서 아빠에게 들은 주민만 안다. 자료·시간·추리 판정은 바꾸지 않는다.
init 354 python:
    R13_PIKO_NEWS_PEOPLE=("nabi","buri")

    def r13_piko_news_available(person):
        if person not in R13_PIKO_NEWS_PEOPLE or not r13_v111_active():return False
        if r13_v111_value("piko_alive") is not False or not r13_v111_owned("E09"):return False
        if r13_v111_value("busy:"+person):return False
        if not r13_v111_actor_ready(person) or person not in r13_visible_people():return False
        if getattr(store,"r13_meeting_active",False) or getattr(store,"r13_meeting_live_active",False):return False
        if (store.room13.get("v111") or {}).get("scene")=="MS14_D03_S05":return False
        if r13_v111_tense_context()=="event":return False
        return True

    def r13_piko_report_due(person):
        return ((store.room13 or {}).get("day")==3 and r13_piko_news_available(person)
                and not r13_v111_value("piko_news3:"+person))

    def r13_piko_report_lines(person):
        # 조회·예측은 정보를 저장하지 않는다. 실제 라벨의 대화 반환 뒤에만 아래에서 표시한다.
        if person=="nabi":
            rows=[
                dict(speaker="아빠",text="나비 씨. 피코 씨가 오늘 아침 광장에서 숨진 채 발견됐습니다.",expression="anxious"),
                dict(speaker=None,text="나비가 빈 그릇을 겹치다가 하나를 따로 내려놓는다."),
                dict(speaker="나비",text="……어제 그 화가요?",expression="anxious"),
                dict(speaker="아빠",text="네. 광장에서 보고 왔습니다.",expression="anxious"),
                dict(speaker="나비",text="그릇은 제가 치울게요. 여기 잠깐 앉으세요.",expression="anxious"),
            ]
        elif person=="buri":
            rows=[
                dict(speaker="아빠",text="피코 씨가 오늘 아침 광장에서 숨진 채 발견됐습니다.",expression="anxious"),
                dict(speaker="부리",text="……죽었다는 말이에요?",expression="anxious"),
                dict(speaker="아빠",text="네. 광장에서 보고 왔습니다.",expression="anxious"),
                dict(speaker="부리",text="……알겠어요.",expression="anxious"),
            ]
        else:return []
        return [r13_nw_added_line(dict(row,id="NW_PIKO_NEWS_%s_%02d"%(person.upper(),i),
                                     kind="narration" if row["speaker"] is None else "dialogue"))
                for i,row in enumerate(rows)]

    def r13_piko_echo_lines(person):
        day=(store.room13 or {}).get("day")
        if day not in (3,4) or not r13_piko_news_available(person):return []
        if not r13_v111_value("piko_news3:"+person):return []
        # 현재 사건·필수 질문·자료 반응·바쁜 일은 짧은 잔향보다 먼저다.
        if r13_v111_tense_context() or r13_v111_has_business(person):return []
        if person=="nabi":
            if day==3:
                rows=[dict(speaker=None,text="나비가 빈 의자를 탁자에 밀어 넣으려다 그대로 둔다."),
                      dict(speaker="나비",text="잠깐 앉으셔도 돼요. 치우는 건 제가 할게요.")]
            else:
                rows=[dict(speaker=None,text="나비가 행주를 접어 식탁 쪽에 놓는다."),
                      dict(speaker="나비",text="그 노란 자국, 닦아도 남네요.")]
        else:
            if day==3:
                rows=[dict(speaker="아빠",text="……잠깐 괜찮으세요?"),
                      dict(speaker="부리",text="다른 말은 아직 못 하겠어요. 물어볼 게 있으면 물어요.")]
            else:
                rows=[dict(speaker=None,text="부리가 문을 닫으려다 나를 보고 손잡이를 놓는다."),
                      dict(speaker="부리",text="말할 거면 해요. 문은 나중에 닫을게요.")]
        return [r13_nw_added_line(dict(row,id="NW_PIKO_ECHO_%s_%s_%02d"%(person.upper(),day,i),
                                     kind="narration" if row["speaker"] is None else "dialogue",
                                     expression="anxious")) for i,row in enumerate(rows)]

    _r13_piko_news_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        rows=r13_piko_echo_lines(person)
        return rows if rows else _r13_piko_news_idle_lines(person)

label r13_piko_report(person):
    if r13_piko_report_due(person):
        call r13_lines(r13_piko_report_lines(person),"v111:piko_news3:"+person)
        # 다른 사건처럼 의도적 대화 건너뛰기도 세계 안에서는 전달을 마친 것으로 취급한다.
        $ r13_v111_set("piko_news3:"+person,True)
        return True
    return False
