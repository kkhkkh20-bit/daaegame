# Questions follow observations in this run, not the passage of a day.
# Existing availability still owns dates, custody, episode and meeting gates.
default r13_question_pending = None

init 190 python:
    import re as r13_question_re

    # These are authored subject cues, not matches against question titles or menus.
    # Narration is accepted only from that resident's actual notice/opening.
    R13_WORK_CUES = {
        "resident_tori":("천 끝", "바늘", "옷감"),
        "resident_bori":("장작", "무거운 짐"),
        "resident_yeoni":("수선", "바느질"),
        "nabi":("빈 그릇", "그릇을 치", "못 내려오는 사람"),
        "buri":("버릴 부품", "부품을 따로", "고장 난 부품"),
        "resident_kongi":("길을 잘", "길 안내", "샛길"),
        "doto":("장부", "받아 적"),
        "resident_kkwak":("물통", "물을 길"),
        "granny":("묵는 분이 늘", "묵어 가는 분이 늘", "손님이 늘", "이불이 모자"),
        "resident_librarian":("책을 빌", "책을 찾", "책장"),
        "resident_owlgp":("기록을", "기록하", "수첩"),
        "resident_teacher":("수업", "교실", "아이들을 가르"),
        "karo":("바퀴 축", "마차를 고", "축을 갈"),
        "resident_nero":("통행표", "표를 버", "번호표"),
        "resident_seol":("종을 치", "종 치는", "종소리"),
        "resident_ppul":("식량", "배급", "나눠 줄"),
        "resident_tok":("부품", "계측기"),
        "bami":("여기서 자", "잠자리", "몸을 숨"),
        "resident_sling":("받는 사람", "반송", "배달할"),
        "resident_momo":("보관", "쓸 수 있는 물건"),
        "resident_ttadak":("벽", "기둥", "수평"),
        "resident_piko":("그림", "붓", "물감"),
        "resident_mungchi":("상자", "무거운", "짐을 옮"),
        "resident_madam":("물자", "보관함", "자루"),
        "resident_siluk":("수레", "눈길", "짐을 싣"),
        "neoul":("문을 지", "출입", "통행"),
        "resident_musoe":("밖으로 나", "마을 밖", "고개"),
        "resident_somi":("심부름", "다녀왔", "다녀오"),
        "resident_seori":("이름", "서명", "확인한 사람"),
        "resident_ubak":("숫자", "수치", "측정"),
        "resident_nubi":("빨래", "묶음", "세탁"),
        "resident_eunho":("가격", "값을", "물건값"),
        "resident_guseul":("도장", "물건을 내", "재고"),
        "resident_badook":("순찰", "밤길", "혼자 다니"),
        "resident_lamplighter":("밝기", "밝지", "등불이 어", "등을 고"),
    }
    R13_LATER_CUES = {
        "resident_tori":(("천을 드", "천은", "가져가는 곳"),("천을 잘라", "천이 부족")),
        "resident_bori":(("우리 집 난로", "대피소"),("우리 집은", "가족이 머물")),
        "resident_yeoni":(("토리는 혼자", "토리를 보내"),("토리한테", "위험한 일")),
        "nabi":(("밥 먹으러 못", "몸이 아파"),("못 걸어오는", "그릇은 건드리지")),
        "buri":(("고칠 수 있", "수리를 부탁"),("손이 미끄", "교대로", "손을 놓으면")),
        "resident_kongi":(("빵은 안", "빵이 안"),("빵 냄새", "빵이 없")),
        "doto":(("고쳐 쓰", "장부를 고"),("지우개", "지우지 말")),
        "resident_kkwak":(("빨래할 물", "빨래는", "씻을 물"),("물속", "물가")),
        "granny":(("밖에서 주무", "여관 문 닫"),("사람들을 안으로", "받을 수 있는 인원")),
        "resident_librarian":(("땔감", "태울 종이"),("원본과 베낀", "원본을 따로")),
        "resident_owlgp":(("살려 줬", "살려 주"),("내 글씨", "글씨가 흐")),
        "resident_teacher":(("환자를 받", "교실을", "아이들을 밖"),("더 받", "교실 자리")),
        "karo":(("길이 막", "돌아갈 길"),("마차를 두고", "걸어서")),
        "resident_nero":(("이름 안 적힌", "그릇도 하나"),("이름부터", "명단")),
        "resident_seol":(("한 번 치", "길게 치"),("종소리", "듣는 사람")),
        "resident_ppul":(("불을 끄", "잘 곳"),("제 문", "내 문", "주민들이 추")),
        "resident_tok":(("안 맞", "크기가 다"),("장치 소리", "소리를 놓")),
        "bami":(("안전하", "누가 드나"),("경비가 드나", "빈방")),
        "resident_sling":(("편지가 안 닿", "문을 안 열"),("봉투 여는", "봉투를 여")),
        "resident_momo":(("그림을 가져", "돌려주"),("그림 속 장치", "실제 장치")),
        "resident_ttadak":(("허락", "지붕"),("자기 집", "무너질")),
        "resident_piko":(("무슨 색", "색을 썼"),("이 색", "색을 좋아")),
        "resident_mungchi":(("안에 든", "상자를 열"),("쌓은", "제 탓")),
        "resident_madam":(("창고에서 꺼", "이름을 쓰"),("창고 문", "남겨 둘")),
        "resident_siluk":(("시키는 대로", "짐부터 확인"),("짐부터 보여", "새로 싣")),
        "neoul":(("보호실", "제 글씨"),("기록에 이름", "제 이름")),
        "resident_musoe":(("땔감", "바치"),("솜이가", "날개")),
        "resident_somi":(("시키는 대로", "심부름"),("내려앉", "날아서")),
        "resident_seori":(("검사 기록", "고칠 줄"),("서명", "원본")),
        "resident_ubak":(("다시 잴", "틀렸을"),("스승님 앞", "먼저 말")),
        "resident_nubi":(("용기 내", "머물 곳"),("집 앞", "제 말이 밖")),
        "resident_eunho":(("제 창고", "내 창고"),("내일 제가", "오늘 다 내")),
        "resident_guseul":(("본 수량", "제가 본"),("제가 센", "나머지는")),
        "resident_badook":(("명령", "원본 기록"),("불 꺼진", "빈집")),
        "resident_lamplighter":(("어머니께 직접", "하라는 대로"),("주소는", "연락을 맡")),
    }
    R13_LIFE_CUES={"life:"+person+":work":cues for person,cues in R13_WORK_CUES.items()}
    for _person,_phases in R13_LATER_CUES.items():
        for _suffix,_cues in zip(("after","crisis"),_phases):
            R13_LIFE_CUES["life:"+_person+":"+_suffix]=_cues
    # Preserve the early witness route, but enter it through Dad's actual purpose.
    # The hunter's account is the existing alibi, not a newly invented event.
    ROOM13["topics"]["ask_mom:kalbaram"]=dict(
        npc="resident_kalbaram",title="숲에서 제 아내를 보셨습니까?",day=[2,14],
        need=["lodging"],not_flags=["mom_reunited"],give=[],
        flags=["alibi:night1:resident_kalbaram"],
        lines=[("dad","여관 13호실에 묵던 제 아내를 찾고 있습니다. 숲에서 보신 적 있습니까?"),
               ("resident_kalbaram","부인은 못 봤소. 다만 댁 마차가 온 날 밤에 아이 하나를 봤지.")]
              +list(R13_ALIBI[("night1","resident_kalbaram")]["claim"][1:3]))

    R13_QUESTION_LEADS = {
        "granny_rules":("heard:door_locks",),
        "life:granny:work":("heard:life:granny:work",),
        "karo_parcel":("J03", "heard:return_parcels"),
        "kalbaram:edge":("heard:forest_edge",),
    }
    for _key in R13_LIFE_CUES:
        R13_QUESTION_LEADS.setdefault(_key,("heard:"+_key,))
    for _key in ROOM13["topics"]:
        if _key.startswith("alibi:night1:"):
            R13_QUESTION_LEADS[_key]=("heard:first_night", "read:tosil:forest", "read:ask_mom:kalbaram")

    def r13_question_clean(text):
        return r13_question_re.sub(r"\{[^}]*\}","",str(text)).replace("【","").replace("】","")

    def r13_question_line_cues(identity,who,text):
        text=r13_question_clean(text)
        found=[]
        # Dad's own questions/thoughts and dated transcript replays are not new facts.
        if who in ("dad","daram") or str(identity).startswith(("topic:review:","topic:record_full:")):return found
        for key,cues in R13_LIFE_CUES.items():
            person=key.split(":")[1]
            notice=who is None and str(identity).startswith(("notice:","greeting:")) and person in str(identity)
            if (who==person or notice) and any(cue in text for cue in cues):
                found.append(key)
        if who in (None,"granny") and any(cue in text for cue in ("빗장", "안쪽 문", "문을 잠", "문도 잠")):
            found.append("door_locks")
        if who in ("karo","seryeon") and any(cue in text for cue in ("반송", "되돌아온 물건", "되돌아오는 짐")):
            found.append("return_parcels")
        if who=="resident_kalbaram" and any(cue in text for cue in ("숲 끝", "옛 길", "절벽")):
            found.append("forest_edge")
        if who in ("resident_tosil","resident_kalbaram") and any(cue in text for cue in ("마차가 온 날 밤", "처음 온 날 밤", "큰 전나무 밑에서 흰 토끼 아이")):
            found.append("first_night")
        return found

    def r13_question_learn(identity,who,text):
        if not getattr(store,"room13",None):return
        cues=r13_question_line_cues(identity,who,text)
        known=dict(store.room13.get("question_cues",{}))
        for cue in cues:
            if cue not in known:
                known[cue]=dict(source=str(identity),day=store.room13["day"],period=store.room13["period"])
        if known!=store.room13.get("question_cues",{}):r13_edit(question_cues=known)

    def r13_question_lead_known(lead,extra=()):
        state=store.room13 or {}
        if lead.startswith("heard:"):
            cue=lead[6:]
            return cue in state.get("question_cues",{}) or cue in extra
        if lead.startswith("read:"):return lead[5:] in state.get("read_topics",[])
        return r13_has(lead)

    def r13_question_discovered(key,spec,extra=()):
        s=store.room13 or {}
        if key=="register" and r13_has("lodging"):return False
        if key=="alibi:night1:resident_kalbaram" and "ask_mom:kalbaram" in s.get("read_topics",[]):return False
        # Preserve a save's already heard testimony, without treating old menu exposure as knowledge.
        if key in s.get("read_topics",[]) or (key.startswith("alibi:") and r13_has(key)):return True
        leads=spec.get("discover_any",R13_QUESTION_LEADS.get(key))
        return leads is None or any(r13_question_lead_known(lead,extra) for lead in leads)

    _r13_discovered_topics=r13_topics
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_discovered_topics(person) if r13_question_discovered(key,spec)]

    # Save the current line's provenance before displaying it. Commit only after all
    # pages were delivered. No writes from prediction, hover, menu building or previews.
    _r13_question_before_line=r13_before_line
    def r13_before_line(identity,index,text):
        store.r13_question_pending=(identity,index,text)
        return _r13_question_before_line(identity,index,text)

    _r13_question_remember_line=r13_remember_line
    def r13_remember_line(key):
        _r13_question_remember_line(key)
        pending=getattr(store,"r13_question_pending",None)
        packet=getattr(store,"r13_packet",None)
        if pending and packet and key==getattr(store,"r13_read_id",None) and not getattr(store,"r13_conv_skip",False) and not getattr(store,"r13_thought_active",False) and getattr(store,"r13_page_i",0)>=len(getattr(store,"r13_pages",[None])):
            r13_question_learn(pending[0],packet[0],pending[2])

    # A small aside about the register supplies a reason for an optional question;
    # it follows the wife/date answer, rather than appearing in the initial menu.
    _r13_question_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        rows=list(_r13_question_topic_lines(key))
        if key=="granny_letter" and key not in (store.room13 or {}).get("read_topics",[]):
            rows.insert(max(0,len(rows)-1),("granny","눈에 길이 막혀 묵는 분이 늘어서요. 장부를 보면서 날짜를 확인하는 게 낫겠어요."))
        return rows

    def r13_question_migrate():
        s=getattr(store,"room13",None)
        if not s or s.get("question_cues_revision")==1:return
        for key,rows in s.get("topic_transcripts",{}).items():
            for row in rows:
                if len(row)<3 or not row[2]:r13_question_learn("saved-transcript:"+key,row[0],row[1])
        r13_edit(question_cues_revision=1)

    config.interact_callbacks.append(r13_question_migrate)
    config.after_load_callbacks.append(r13_question_migrate)

    # Pure presentation relevance. Never probe by calling r13_present: it grants facts.
    # Data-driven presentation routes below also cover future authored episode entries.
    R13_CONTACT_RECORDS = {
        "granny":("E01","E04","E05","E09","E10","E13","E14","E18","E19","E27","E30","E35","E36","E37","M01","P01"),
        "nabi":("E11","M01","J01","P01"),
        "karo":("M01",),
        "daram":("E01","E03","E18","M01","J04","J05","P01"),
        "buri":("E04","E06","E08","E17","E35"),
        "bami":("E06",),
        "resident_tok":("E14",),
        "doto":("E04","E05","E37"),
        "resident_lamplighter":("E01","E03","M01","J01","J04","J05","P01"),
        "resident_sling":("P01",),
        "seryeon":("E01","M01","J02","E19","E27","E30"),
        "neoul":("E19","E27","E30"),
        "resident_ppul":("R01","N08"),
        "resident_seori":("H1",),
        "resident_madam":("H1",),
        "resident_eunho":("H1",),
        "resident_piko":("L01",),
        "resident_librarian":("L00","L03","L04"),
        "resident_teacher":("F01","F03"),
    }

    def r13_contact_presentations(person):
        s=store.room13 or {}
        owned=set(s.get("evidence",[]))
        candidates=set(R13_CONTACT_RECORDS.get(person,()))
        for spec in ROOM13.get("presentations",[]):
            if spec.get("npc")==person:candidates.update(spec.get("items",[]))
        shown=s.get("resident_knowledge",{}).get(person,[])
        def fresh(key):
            if key=="E27":
                revision=s.get("records",{}).get(key,{}).get("revision",0)
                if revision:return not any(v.startswith(key+":") and v.endswith(":revision"+str(revision)) for v in shown)
            return not any(v.split(":",1)[0]==key for v in shown)
        # Previously shown material may acquire a new authored use later. Keep
        # these routes open until their result, rather than guessing from 'shown'.
        pending=set()
        for spec in ROOM13.get("presentations",[]):
            if spec.get("npc")==person and not r13_has("topic:"+spec.get("topic","")):
                pending.update(spec.get("items",[]))
        day=s.get("day",1)
        if person=="resident_librarian" and day==3:
            if not r13_has("lt_lib_warned"):pending.add("L04")
            elif not r13_has("lt_lib_safe"):pending.add("L00")
        if person=="resident_lamplighter" and day>=3 and not r13_has("topic:lamplighter_warning"):
            pending.update(("M01","J04","J05"))
        if person in ("nabi","karo") and s.get("life_poc") and 2<=day<=4 and not r13_has("poc:note_shown:"+person):pending.add("M01")
        if person=="seryeon" and r13_has("J02"):
            if not r13_has("intro:post_letter"):pending.add("E01")
            if not r13_has("intro:post_memo"):pending.add("M01")
        if person=="buri":
            if s.get("victim_state")=="dead":
                if not r13_has("buri_revised"):pending.add("E35")
                if not r13_has("buri_hurt_past"):pending.add("E17")
            if r13_has("medical_consent") and not r13_has("topic:buri_records"):pending.update(("E06","E08"))
            if "plans" in s.get("tool_discoveries",{}) and "tool:plans" not in s.get("read_topics",[]):pending.add("E04")
        if person=="doto" and s.get("case_state")=="occurred" and not r13_has("J10"):pending.update(("E04","E05","E37"))
        if person=="granny" and r13_has("inn_front_door_claim") and not r13_has("inn_claim_retracted"):pending.update(("E04","E05","E37"))
        if person=="resident_eunho" and getattr(store,"r13_grudge_open",lambda p:False)("eunho"):pending.add("H1")
        keys=[key for key in owned & candidates if fresh(key) or key in pending]
        # Transfers keep their own recipient, inventory and quest checks.
        keys.extend(key for key in r13_catalog_entries() if r13_catalog_object(key) and r13_catalog_offer(person,key))
        return keys

    def r13_contact_has_content(person):
        s=store.room13 or {}
        read=set(s.get("read_topics",[]))
        if any(r13_topic_current_fresh(key) or (key not in read and not (key.startswith("alibi:") and r13_has(key))) for key,spec in r13_topics(person)):return True
        if r13_contact_presentations(person):return True
        # A first greeting/notice may itself supply a real subject. Predict whether
        # it will, without awarding its knowledge or recording a meeting.
        if person not in r13_met_people():
            rows=list(r13_conversation_opening(person,True))
            if person in R13_OPENING_SCENES["first_meetings"]:rows+=list(r13_resident_notice(person))
            extra=[]
            for row in rows:extra.extend(r13_question_line_cues("notice:resident:"+person,row[0],row[1]))
            if extra and any(key not in read and r13_question_discovered(key,spec,extra) for key,spec in _r13_discovered_topics(person)):return True
        return False

    def r13_no_conversation_notice(person):
        renpy.notify("지금은 %s에게 더 물어볼 이야기가 없다."%R13_NAMES.get(person,person))

    _r13_question_person_action=r13_person_action
    def r13_person_action(person,entry=False):
        # Events and child/group interactions retain their existing dispatcher.
        special=entry or r13_offer_for_person(person) or any(person in row.get("individual_lines",{}) for row in R13_LIFE_GROUPS)
        if special or r13_contact_has_content(person):return _r13_question_person_action(person,entry)
        return Function(r13_no_conversation_notice,person)
