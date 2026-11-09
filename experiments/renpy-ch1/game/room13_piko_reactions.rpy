# 피코의 사망 소식과 처리 결과는 실제로 들은 주민만 기억한다. 자료·시간·추리 판정은 바꾸지 않는다.
init 354 python:
    R13_PIKO_NEWS_PEOPLE=("nabi","buri")

    def r13_piko_resident_available(person):
        if person not in R13_PIKO_NEWS_PEOPLE or not r13_v111_active():return False
        if r13_v111_value("busy:"+person):return False
        if not r13_v111_actor_ready(person) or person not in r13_visible_people():return False
        if getattr(store,"r13_meeting_active",False) or getattr(store,"r13_meeting_live_active",False):return False
        if (store.room13.get("v111") or {}).get("scene")=="MS14_D03_S05":return False
        if r13_v111_tense_context()=="event":return False
        return True

    def r13_piko_news_available(person):
        return (r13_piko_resident_available(person) and r13_v111_value("piko_alive") is False
                and r13_v111_owned("E09"))

    def r13_piko_current_activity(person):
        # 사람에게 직접 붙은 질문뿐 아니라, 함께 하던 물건 조사·인계도 현재 대화다.
        # 예: 나비와 보급판을 읽는 중에는 식탁 조사나 다람의 출발 질문이 남아 있다.
        # 자유 탐색의 종료 질문은 진행 중인 업무가 아니다. 주민 본인의 질문은 기존 business가 맡는다.
        if (store.room13.get("v111") or {}).get("gate")=="free_day7":return False
        binding=r13_v111_binding()
        participants=binding.get("people",[])+(store.room13.get("v111") or {}).get("people",[])
        if person not in participants:return False
        here=store.room13.get("location")
        return any(option.get("location")==here and any(option.get(kind) for kind in ("person","object","move","present"))
                   for option in binding.get("options",[]))

    def r13_piko_required_business(person):
        # 선택 가능한 일상·의뢰 질문은 소식을 전할 일을 영구히 막지 않는다.
        return globals().get("r13_v111_required_business",r13_v111_has_business)(person)

    def r13_piko_report_due(person):
        day=(store.room13 or {}).get("day")
        if not r13_piko_news_available(person) or r13_v111_value("piko_news3:"+person):return False
        if day==3:return True
        # 3일에 식당을 찾지 않은 경우도 실제 대면으로만 전한다. 필수 문답과 당면 사건은 먼저다.
        return (person=="nabi" and day in (4,5,6,7) and not r13_v111_tense_context()
                and not r13_piko_required_business(person) and not r13_piko_current_activity(person))

    def r13_piko_report_lines(person):
        # 조회·예측은 정보를 저장하지 않는다. 실제 라벨의 대화 반환 뒤에만 아래에서 표시한다.
        day=(store.room13 or {}).get("day")
        when="오늘 아침" if day==3 else "어제 아침" if day==4 else "며칠 전 아침"
        if person=="nabi":
            rows=[
                dict(speaker="아빠",text="나비 씨. 피코 씨가 %s 광장에서 숨진 채 발견됐습니다."%when,expression="anxious"),
                dict(speaker=None,text="나비가 빈 그릇을 겹치다가 하나를 따로 내려놓는다." if day==3 else "나비가 앞치마를 쥐고 내 쪽으로 돌아선다."),
                dict(speaker="나비",text="……어제 그 화가요?" if day==3 else "……의자에 노란 물감 묻혔던 그 화가요?",expression="anxious"),
                dict(speaker="아빠",text="네. 광장에서 보고 왔습니다." if day==3 else "네. 그날 광장에서 직접 봤습니다.",expression="anxious"),
                dict(speaker="나비",text="그릇은 제가 치울게요. 여기 잠깐 앉으세요." if day==3 else "여기 잠깐 계세요. 저도 숨 좀 돌릴게요.",expression="anxious"),
            ]
        elif person=="buri":
            rows=[
                dict(speaker="아빠",text="피코 씨가 %s 광장에서 숨진 채 발견됐습니다."%when,expression="anxious"),
                dict(speaker="부리",text="……죽었다는 말이에요?",expression="anxious"),
                dict(speaker="아빠",text="네. 광장에서 보고 왔습니다." if day==3 else "네. 그날 광장에서 직접 봤습니다.",expression="anxious"),
                dict(speaker="부리",text="……알겠어요.",expression="anxious"),
            ]
        else:return []
        return [r13_nw_added_line(dict(row,id="NW_PIKO_NEWS_%s_%02d"%(person.upper(),i),
                                     kind="narration" if row["speaker"] is None else "dialogue"))
                for i,row in enumerate(rows)]

    def r13_piko_echo_lines(person):
        day=(store.room13 or {}).get("day")
        if day not in (3,4,5,6,7) or not r13_piko_resident_available(person):return []
        # 현재 사건·필수 질문·자료 반응·바쁜 일은 짧은 잔향보다 먼저다.
        if r13_v111_tense_context() or r13_piko_required_business(person) or r13_piko_current_activity(person):return []
        # 처리 결과는 피코가 살아 있는 도난판에도 직접 들었다. 사망 소식과 별개의 기억이다.
        custody=r13_v111_value("piko_custody_heard3:buri") if person=="buri" and not r13_v111_value("lamp_bound2") else None
        if custody not in ("report","transfer"):custody=None
        if custody=="report":
            # 당시 결정만 돌아본다. 현재 귀가·보고 이행·명단 해제는 확인하지 않은 일이다.
            rows=[dict(speaker="아빠",text="실룩 씨를 바로 데려가지 못하게 한 일이 마음에 남습니다."),
                  dict(speaker="부리",text="돌 가져간 일은 남겨 둬요. 다시 나오기로 했다는 말도요.")]
        elif custody=="transfer":
            rows=[dict(speaker="아빠",text="실룩 씨를 데려가게 한 결정이 마음에 남습니다."),
                  dict(speaker="부리",text="언제 돌아오느냐고 물었는데, 대답을 못 들었죠. 그게 마음에 걸려요.")]
        elif not r13_piko_news_available(person) or not r13_v111_value("piko_news3:"+person):return []
        elif person=="nabi":
            if day==3:
                rows=[dict(speaker=None,text="나비가 빈 의자를 탁자에 밀어 넣으려다 그대로 둔다."),
                      dict(speaker="나비",text="잠깐 앉으셔도 돼요. 치우는 건 제가 할게요.")]
            elif day==4 and store.room13.get("location")=="dining":
                rows=[dict(speaker=None,text="나비가 행주를 접어 식탁 쪽에 놓는다."),
                      dict(speaker="나비",text="그 노란 자국, 닦아도 남네요.")]
            else:
                rows=[dict(speaker="아빠",text="피코 씨 얘기를 들어 주셔서 고맙습니다."),
                      dict(speaker="나비",text="그 의자의 노란 자국이 자꾸 생각나요.")]
        else:
            if day==3:
                rows=[dict(speaker="아빠",text="……잠깐 괜찮으세요?"),
                      dict(speaker="부리",text="다른 말은 아직 못 하겠어요. 물어볼 게 있으면 물어요.")]
            elif day==4:
                rows=[dict(speaker=None,text="부리가 문을 닫으려다 나를 보고 손잡이를 놓는다."),
                      dict(speaker="부리",text="말할 거면 해요. 문은 나중에 닫을게요.")]
            else:
                rows=[dict(speaker="아빠",text="피코 씨 일로 말씀드렸던 게 마음에 남습니다."),
                      dict(speaker="부리",text="들은 말은 기억해요. 더 물어볼 게 있으면 물어요.")]
        return [r13_nw_added_line(dict(row,id="NW_PIKO_ECHO_%s_%s%s_%02d"%(person.upper(),day,("_"+custody.upper()) if custody else "",i),
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
