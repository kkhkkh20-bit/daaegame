# First-run investigation: reading -> owned-record comparison -> presentation
# -> an explicit follow-up conversation. General movement never spends time.
init 97 python:
    ROOM13["evidence"]["E01"].update(establishes="할머니가 아내의 소식이 끊겼다며 가족에게 보낸 편지다. 이 편지를 받고 다람이와 마을에 왔다.",does_not_establish="")
    ROOM13["evidence"]["E03"].update(establishes="13호실 이불 안쪽의 붉은 매듭은 집에서 보던 엄마의 바느질과 닮았다. 다람이도 익숙한 모양이라고 했다.",does_not_establish="")
    ROOM13["evidence"]["M01"]["establishes"]="다람이 이름 옆에 도토리가 그려진 메모. ‘아빠랑 도착하면 이 방에 짐을 놓아. 내가 없으면 등불을 돌보는 분에게 내 소식을 물어봐.’라고 적혀 있다."
    ROOM13["evidence"]["J02"]=dict(id="J02",name="초롱이 마지막으로 본 엄마",kind="증언",
        establishes="초롱은 엄마와 여관 앞에서 이야기했다고 했다. 가족을 기다린다는 말을 들었고, 헤어진 뒤 엄마가 우체국 쪽 길로 가는 것을 봤다. 우체국 안에 들어갔는지는 보지 못했다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"]["J02"]="resident_lamplighter"
    R13_RECORD_SHORT["J02"]="초롱의 목격담"
    ROOM13["evidence"]["J03"]=dict(id="J03",name="세련이 확인한 엄마의 방문",kind="증언",
        establishes="세련은 엄마가 우체국에서 반송품의 도착 여부를 물었다고 했다. 당시 물건은 아직 도착하지 않았다. 세련은 그 뒤 엄마가 어디로 갔는지는 모른다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"]["J03"]="seryeon"
    R13_RECORD_SHORT["J03"]="엄마의 우체국 방문"
    ROOM13["topics"]["intro:direction"]=dict(npc="daram",title="다람아, 어디부터 살펴볼까?",day=[1,3],need=["lodging"],give=[],flags=[],lines=[("daram","엄마가 남긴 것부터 같이 보자.")])
    ROOM13["topics"]["intro:lamplighter_mother"]=dict(npc="resident_lamplighter",title="아내를 마지막으로 어디에서 보셨습니까?",day=[2,3],need=["intro:memo_shown"],give=["J02"],flags=[],lines=[
        ("dad","아내를 마지막으로 어디에서 보셨습니까?"),
        ("resident_lamplighter","여관 앞에서요. 등을 손질하다가 잠깐 이야기를 나눴어요."),
        ("dad","아내와 무슨 이야기를 하셨습니까?"),
        ("resident_lamplighter","가족이 온다고 했어요. 아이에게 도토리 모양을 그려 준다는 이야기도요."),
        ("dad","이야기를 나눈 뒤에 아내는 어디로 갔습니까?"),
        ("resident_lamplighter","우체국 쪽 길로 갔어요. 안으로 들어가는 것까지 보지는 못했고요."),
        ("dad","우선 우체국 쪽에서 아내가 들른 흔적을 찾아보겠습니다.")])
    ROOM13["topics"]["intro:post_visit"]=dict(npc="seryeon",title="아내가 여기서 무엇을 찾았습니까?",day=[2,3],need=["J02","intro:post_letter","intro:post_memo"],give=["J03"],flags=["mother_first_lead_checked"],lines=[
        ("seryeon","여관에서 보낸 편지와 가족에게 남긴 메모군요. 말씀하신 분이 누구인지 알겠어요."),
        ("dad","아내가 이 우체국에서 무엇을 찾았습니까?"),
        ("seryeon","반송되는 물건이 도착했는지 물었어요. 그때는 그 물건이 아직 오지 않았고요."),
        ("dad","아내가 그 뒤에 어디로 갔는지도 보셨습니까?"),
        ("seryeon","어디로 가는지는 못 봤어요. 창구 안에서 다른 우편을 정리하고 있었으니까요."),
        ("dad","우체국에 들렀다는 것까지는 확인됐군요. 그다음에 만난 사람도 찾아보겠습니다.")])

    _r13_intro_compare=r13_compare_result
    def r13_compare_result(selected):
        owned=set((store.room13 or {}).get("evidence",[]))
        if store.room13.get("life_poc") and len(selected)==2 and set(selected)<=owned:
            if set(selected)=={"E01","M01"}:
                r13_flag("mother_expected_family")
                return "(할머니가 보낸 편지를 받고 우리는 이 마을에 왔다. 엄마의 메모도 다람이와 내가 도착할 것을 전제로 쓰여 있다. 엄마도 우리가 올 것을 알고 있었던 것 같다. 그런데 왜 기다리던 방에는 없을까?)"
            if set(selected)=={"M01","J02"}:
                return "(메모는 등불을 돌보는 사람에게 물어보라고 했다. 초롱은 아내를 만났고 가족을 기다린다는 말을 들었다. 마지막으로 본 방향은 우체국 쪽이지만, 정말 우체국 안에 들어갔을까?)"
            if set(selected)=={"J02","J03"}:
                return "(초롱이 본 방향과 세련이 확인한 방문이 이어진다. 아내는 우체국에 들러 반송품을 물었다. 그 뒤 어디로 갔는지는 둘 다 보지 못했다. 우체국을 나온 엄마를 본 사람이 있을까?)"
        return _r13_intro_compare(selected)

    _r13_intro_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13
        if s.get("life_poc") and key in s.get("evidence",[]) and s.get("case_state")=="pending":
            if key=="M01" and person=="resident_lamplighter" and 2<=s["day"]<=4:
                if s["day"]==3:
                    # The existing day-three envelope route must still unlock.
                    _r13_intro_present(person,key,identity)
                r13_flag("intro:memo_shown")
                return [("dad","아내가 이 메모에 등불을 돌보는 분께 물어보라고 적었습니다."),
                    (person,"도토리 그림 이야기를 하던 분이군요. 여관 앞에서 만났어요. 무엇이 궁금하십니까?")]
            if key=="M01" and person=="daram":
                return [("daram","엄마가 나한테 쓰는 도토리 표시야. 아빠랑 내가 올 것도 적어 놨네."),
                    ("dad","할머니 편지와 같이 읽어 보자. 엄마가 누구에게 소식을 맡겼는지도 알아봐야겠어.")]
            if key=="E01" and person=="granny":
                return [(person,"제가 보낸 편지예요. 아내분이 물건을 두고 돌아오지 않아서 가족께 소식을 전해야겠다고 생각했어요."),
                    ("dad","13호실에 남긴 것을 살펴보고 다시 여쭤보겠습니다.")]
            if key=="J02" and person=="seryeon":
                return [("dad","아내가 우체국 쪽으로 갔다고 초롱에게 들었습니다. 여기 들렀습니까?"),
                    (person,"그분의 우편을 확인하려면 가족이라는 자료부터 보여 주세요. 다른 분이 보셨다는 말만으로는 내드릴 수 없어요."),
                    ("dad","가져온 자료를 보여 드리겠습니다.")]
            if person=="seryeon" and key in ("E01","M01") and r13_has("J02"):
                r13_flag("intro:post_letter" if key=="E01" else "intro:post_memo")
                if r13_has("intro:post_letter") and r13_has("intro:post_memo"):
                    return [(person,"편지와 메모를 함께 보니 말씀하신 분이 누구인지 알겠어요. 방문하셨을 때 무슨 일이 있었는지 물어보세요.")]
                return [(person,"여관에서 온 편지군요. 가족에게 남긴 글도 있으면 함께 보여 주세요." if key=="E01" else "가족에게 남긴 메모군요. 여관에서 받으신 편지도 함께 보여 주시겠어요?")]
        return _r13_intro_present(person,key,identity)

    def r13_intro_direction_lines():
        s=store.room13
        if r13_has("J03"):
            return [("daram","엄마가 우체국에 간 건 맞는데, 그 뒤에 어디로 갔는지는 아직 모르는 거네."),("dad","응. 엄마가 여기 머무는 동안 날마다 마주친 사람이 있었을 거야.")]
        if r13_has("J02"):
            return [("daram","초롱 아저씨는 엄마가 우체국 쪽으로 가는 것만 봤대. 정말 안에 들어갔을까?"),("dad","창구에서는 아무한테나 손님 이야기를 해 주지 않겠지.")]
        if r13_has("mother_lamplighter_lead"):
            return [("daram","등불 돌보는 분이 초롱 아저씨래. 그 아저씨도 엄마를 알까?"),("dad","엄마 이름만 대면 모를 수도 있어. 엄마가 우리한테 뭐라고 남겼는지 다시 떠올려 보자.")]
        if r13_has("M01"):
            return [("daram","엄마 메모에 나온 ‘등불을 돌보는 분’은 누구일까?"),("dad","이 마을 사람들은 알겠지. 그런데 누구한테 물어볼까?")]
        if not r13_has("E03"):
            return [("daram","이불 안쪽 바느질이 엄마 것하고 닮았어. 책상에도 접힌 종이가 있어."),("dad","이불 바느질이랑 접힌 종이, 둘 다 직접 살펴보자.")]
        return [("daram","책상 위의 접힌 종이도 읽어 보자. 엄마가 남긴 걸지도 몰라.")]

    _r13_intro_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        if key=="intro:direction":return r13_intro_direction_lines()
        return _r13_intro_topic_lines(key)

    def r13_intro_goal():
        s=store.room13
        if s["day"]==1:
            if not r13_has("entry_corrected"):return "둘이 예약했는데, 왜 이름이 하나만 적혔을까?"
            if not r13_has("lodging"):
                return "편지를 보낸 여관 할머니는 엄마 소식을 알고 있을까?"
            if not r13_has("M01") or not r13_has("E03"):
                return "엄마가 머물던 13호실에는 무엇이 남아 있을까?"
            if not r13_has("mother_lamplighter_lead"):return "메모에 적힌 ‘등불을 돌보는 분’은 누구일까?"
            if r13_has("mother_expected_family"):return "엄마는 우리가 올 걸 알고 있었다. 그런데 왜 기다리지 않았을까?"
            return "엄마는 왜 13호실을 비우고 돌아오지 않았을까?"
        if not r13_has("livelihood_open"):return "까로 아저씨의 마차는 언제 고쳐질까?"
        if r13_has("J03"):return "우체국을 나온 엄마는 누구를 만났을까?"
        if r13_has("J02"):return "엄마는 정말 우체국 안에 들어갔을까?"
        if r13_has("mother_lamplighter_lead"):return "초롱은 엄마를 알아볼까? 마지막으로 언제 봤을까?"
        return "메모에 적힌 ‘등불을 돌보는 분’은 누구일까?"

    _r13_intro_topics=r13_topics
    def r13_topics(person):
        rows=_r13_intro_topics(person)
        if not store.room13.get("life_poc"):
            return [(key,spec) for key,spec in rows if not key.startswith("intro:")]
        return [(key,spec) for key,spec in rows if not key.startswith("intro:") or (store.room13.get("case_state")=="pending" and (key!="intro:direction" or r13_home_with_daram()))]

    _r13_intro_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_intro_notes()
        if not store.room13.get("life_poc") or store.room13.get("case_state")!="pending":return rows
        if r13_has("J03"):
            rows[0]=dict(title="우체국 다음에는 누구를 만났을까?",fact="엄마가 우체국에 들러 반송품을 물었다는 사실을 확인했다. 그 뒤의 행선지는 아직 모른다.",question="엄마가 여관에 돌아오거나 다른 사람을 만난 흔적이 있을까?",hint="엄마가 날마다 마주쳤을 사람은 누구일까? 여관에서 함께 지낸 사람이나 마을 일을 하는 사람을 떠올려 보자.",keys=["J02","J03"])
        elif r13_has("J02"):
            rows[0]=dict(title="엄마가 우체국에 들렀을까?",fact="초롱은 엄마와 대화했고, 우체국 쪽으로 걸어가는 것을 봤다고 했다.",question="우체국 안에 들른 기록도 있을까?",hint="창구는 손님 이야기를 아무에게나 해 주지 않는다. 가족이라는 것을 무엇으로 보여 줄 수 있을까?",keys=["M01","J02"])
        elif r13_has("mother_lamplighter_lead"):
            rows[0]=dict(title="초롱은 엄마를 언제 만났을까?",fact="메모를 보여 주자 등불을 돌보는 사람은 초롱이라고 알려 주었다.",question="엄마를 만났으며, 마지막으로 어디에서 봤을까?",hint="이름만으로는 엄마를 알아보지 못할 수 있다. 초롱은 오전에는 수리점, 오후에는 광장, 저녁에는 입구에서 등불을 돌본다.",keys=["M01"])
        return rows

screen r13_entry_daram_topics():
    style_prefix "r13"
    modal True
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    $ questions=[("우리 이름이 적힌 종이를 같이 볼까?",Return("look"),r13_has("question_read:entry:daram:look")),("아빠랑 같이 들어가고 싶은 거지?",Return("together"),r13_has("question_read:entry:daram:together"))]
    if r13_has("G1") and r13_has("G3"):
        $ questions.insert(1,("두 기록을 같이 읽어 볼까?",Return("compare"),r13_has("question_read:entry:daram:compare")))
    use r13_question_list("daram","neutral","다람이와 이야기",questions,ready,return_action=Return("back"))
    use r13_toolbar(investigate_action=Return("back"),person="daram",mode="talk",ready=ready)

label r13_entry_daram_menu:
    window hide
    hide r13_visitor
    call screen r13_entry_daram_topics
    $ r13_entry_daram_choice=_return
    if r13_entry_daram_choice=="back":
        return
    if r13_entry_daram_choice=="look":
        if r13_has("G1"):
            call r13_lines([("dad","예약 종이에 ‘다돌 외 한 사람’이라고 적혀 있네."),("daram","다돌은 아빠 이름이잖아. 그럼 나머지 한 사람은 나지?"),("dad","응. 초소에서 옮겨 적은 명단도 같이 확인해 보자.")],"entry:daram:original")
        else:
            call r13_lines([("daram","선반에 종이 묶음이 여러 개 있어. 날짜가 적혀 있네."),("daram","우리 오늘 왔잖아. 오늘이 무슨 요일이지?")],"entry:daram:look:v2")
    elif r13_entry_daram_choice=="compare":
        call r13_lines([("daram","아빠 이름은 예약 종이랑 명단에 다 있는데, 내 이름도 둘 다 있을까?"),("dad","예약 종이와 명단을 나란히 놓고 대조해 보자.")],"entry:daram:compare")
        call screen r13_record_compare(called=True)
    elif r13_entry_daram_choice=="together":
        call r13_lines([("daram","엄마 만나러 같이 왔는데 아빠만 먼저 들어가면 안 돼."),("dad","걱정 마. 같이 들어갈 거야. 우리 둘이 함께 예약했다는 기록을 보여 드리자.")],"entry:daram:together")
    $ r13_flag("question_read:entry:daram:"+r13_entry_daram_choice)
    jump r13_entry_daram_menu
