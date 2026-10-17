# 0.19.16: a fact learned on one route is remembered on every other route.
# Queries are read-only (including old saves); learning happens on explicit presentation.
init 173 python:
    def r13_mother_knowledge(state=None):
        s=(store.room13 or {}) if state is None else state
        flags=set(s.get("flags",[])); evidence=set(s.get("evidence",[]))
        shown=s.get("resident_knowledge",{}).get("resident_lamplighter",[])
        met=any(e.get("person")=="resident_lamplighter" for e in s.get("encounters",[]) if isinstance(e,dict))
        recognized=bool(flags & {"intro:memo_shown","portrait_lamp_seen","mother_recognized"}) or bool(evidence & {"J02","J07"}) or any(v.startswith("M01:") for v in shown)
        promised=bool(flags & {"mother_letter_promised","intro:memo_shown","topic:lamplighter_warning"}) or any(v.startswith(("M01:","J04:","J05:")) for v in shown) or "lamplighter_warning" in s.get("read_topics",[])
        received="E18" in evidence
        named=met or recognized or promised or bool(flags & {"mother_lamplighter_lead","poc:note_shown:karo"}) or "J01" in evidence or bool(shown)
        return dict(named=named,recognized=recognized,promised=promised,received=received,
            due=3,pending=promised and not received and "chorong_dead" not in flags and s.get("case_state")=="pending" and "lamplighter_warning" not in s.get("read_topics",[]),
            post="J02" in evidence,post_checked="J03" in evidence)

    def r13_mother_remember_show(person,key,identity=False):
        # Earlier presentation layers sometimes return before the base recorder.
        # Record only an owned item, without fabricating evidence or a conversation.
        if not r13_has(key):return
        n=winter_copy.deepcopy(store.room13)
        known=n.setdefault("resident_knowledge",{}).setdefault(person,[])
        disclosure=key+(":named" if identity else ":anonymous")
        if disclosure not in known:known.append(disclosure)
        store.room13=n
        r13_note_encounter(person)

    _r13_review_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13 or {}
        owned=key in s.get("evidence",[])
        early=s.get("life_poc") and s.get("case_state")=="pending" and s.get("day",1)<=R13_CASE_DAY
        if owned and early and person=="resident_lamplighter" and key in ("M01","J04","J05"):
            before=r13_mother_knowledge()
            result=_r13_review_present(person,key,identity)
            r13_mother_remember_show(person,key,identity)
            r13_flag("mother_lamplighter_lead","mother_letter_promised")
            if key=="M01":r13_flag("mother_recognized","intro:memo_shown")
            if s.get("day",1)<3:
                when="모레" if s.get("day",1)==1 else "내일"
                # 0.19.17 (owner): not straight to "부인이…": a beat of recognising, then the promise, then when to come back.
                opener={"M01":[(None,"초롱이 메모를 받아 들고 한참 들여다보았다."),(person,"……아, 이거군요. 이 글씨, 알아요.")],
                    "J04":[(person,"……나비가 그걸 봤군요."),(person,"네. 그날 부인이 제게 무언가 건네신 건 맞아요.")],
                    "J05":[(person,"……까로 씨가 점검함을 봤군요."),(person,"네. 거기 넣은 건 제 물건이 아니에요.")]}[key]
                return opener+[(person,"맞습니다. 부인이 가족분께 전해 달라고 봉투 하나를 저에게 맡기셨어요."),
                    (person,"점검함 깊숙이 넣어 둬서 지금 바로 꺼내 드릴 수는 없어요. "+when+" 찾아서 전해 드릴게요."),
                    # 0.19.17 (owner): residents name the weekday and the place, not "3일째".
                    (person,r13_weekday(3)+"요일 오전에 수리점으로 저를 찾아와 주시겠어요? 아침마다 거기서 등 부품을 손보거든요."),
                    ("dad",r13_weekday(3)+"요일 오전, 수리점으로 꼭 찾아가겠습니다.")]
            r13_flag("topic:lamplighter_warning")
            if before["received"]:
                return [(person,"전에 드린 편지가 부인이 가족에게 남긴 글이에요. 지금 어디 계신지는 저도 몰라요.")]
            return [(person,"말씀드린 봉투를 찾아뒀어요. 어디서 받으실지 말씀드릴게요." if before["promised"] else "부인이 가족에게 전해 달라고 맡긴 봉투가 있어요."),
                (person,"여기서 길게 이야기하진 맙시다. 무엇이 궁금하신가요?")]
        if owned and early and person=="resident_lamplighter" and key=="E01":
            r13_mother_remember_show(person,key,identity)
            if r13_mother_knowledge()["recognized"]:
                return [(person,"부인 가족인 것은 알아요. 다만 이 초대 편지를 쓰거나 부치시는 모습은 보지 못했어요."),
                    (person,"이 편지의 글쓴이가 누구인지는 제가 확인해 드릴 수 없어요.")]
            return [(person,"이름만으로는 어느 분인지 확인하기 어려워요. 부인의 얼굴이나 직접 남긴 표시가 있다면 알아볼 수 있을 거예요.")]
        if owned and person=="resident_seori" and key in ("L02","L03","L04","L05","L06"):
            r13_mother_remember_show(person,key,identity)
            if key=="L02":
                return [(person,"온도계는 제가 빌렸습니다. 광장 등은 제자 우박에게 재 오라고 했고요."),
                    (person,"어느 등을 언제 열었는지는 직접 다녀온 우박이 말해야 합니다.")]
            if key=="L03":
                return [(person,"측정값을 적은 쪽지군요. 우박에게 등 온도를 재 오라고 한 건 저입니다."),
                    (person,"이 숫자를 적었는지, 조각을 어떻게 했는지는 우박에게 확인해야 해요. 제가 현장에 있었던 건 아니니까요.")]
            if key=="L04":
                return [(person,"저는 이 노끈을 본 적이 없습니다. 측정에 쓴 물건인지도 직접 확인해야겠어요."),
                    (person,"끈만으로 제자가 조각을 가져갔다고 정할 수는 없습니다.")]
            if key=="L05":
                return [(person,"우박은 조각을 돌려놨다고 했습니다. 제자라는 이유로 그 말만 믿어 달라고 하진 않겠어요."),
                    (person,"그 뒤에도 등이 따뜻했는지 본 사람이 있을까요?")]
            return [(person,"초롱이 새벽에 따뜻한 등을 직접 확인했다는 말이군요."),
                (person,"그 시각과 우박이 측정을 마친 시각을 맞춰 보면, 그 뒤에 무슨 일이 있었는지 좁힐 수 있겠어요.")]
        return _r13_review_present(person,key,identity)

    def r13_mother_note_row():
        k=r13_mother_knowledge(); s=store.room13 or {}
        if k["received"] or k["post_checked"]:return None
        if k["pending"]:
            due=k["due"];late=s.get("day",1)>=due
            return dict(title="초롱이 맡아 둔 봉투에는 무엇이 있을까?",
                fact="초롱은 엄마가 가족에게 남긴 봉투를 맡고 있으며, 3일에 다시 오라고 했다.",
                question="약속한 날이다. 엄마가 남긴 글은 무엇일까?" if late else "엄마는 왜 초롱에게 봉투를 맡겼을까?",
                hint="약속은 달력에도 적어 두었다. 봉투를 읽기 전에는 내용과 행선지를 알 수 없다.",keys=[v for v in ("M01","J04","J05") if r13_has(v)])
        if k["promised"] and not k["received"]:
            return dict(title="엄마가 맡긴 봉투에는 무엇이 있을까?",fact="초롱은 엄마가 맡긴 봉투를 등 밑 점검함에 두었다고 했다.",
                question="봉투에 남긴 글은 무엇일까?",hint="아직 읽지 않은 글의 내용은 알 수 없다.",keys=[v for v in ("M01","J04","J05") if r13_has(v)])
        if k["post"] or r13_has("J04") or r13_has("J05"):return None
        if k["recognized"]:
            return dict(title="초롱은 엄마를 마지막으로 어디서 봤을까?",fact="초롱은 엄마가 남긴 표시나 얼굴을 알아봤다.",
                question="엄마와 무슨 이야기를 했으며, 어디로 가는 것을 봤을까?",hint="엄마를 안다는 것과 지금 있는 곳을 안다는 것은 다르다.",keys=[v for v in ("M01","J07") if r13_has(v)])
        if k["named"] and r13_has("M01"):
            return dict(title="초롱은 엄마를 기억할까?",fact="메모에 적힌 등불을 돌보는 사람은 초롱이다.",question="초롱도 엄마를 만났을까?",
                hint="이름만으로 누구인지 알 수 있을까? 초롱은 오전에는 수리점, 오후에는 광장, 저녁에는 입구에서 등불을 돌본다.",keys=[v for v in ("M01","J01") if r13_has(v)])
        return None

    _r13_review_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_review_notes()
        if (store.room13 or {}).get("case_state")=="pending":
            row=r13_mother_note_row()
            if row:rows=[row]+rows[1:]
        return rows

    _r13_review_direction=r13_intro_direction_lines
    def r13_intro_direction_lines():
        s=store.room13 or {};k=r13_mother_knowledge()
        if not s.get("life_poc") or s.get("case_state")!="pending":return _r13_review_direction()
        if k["received"]:
            return [("daram","엄마가 맡긴 글에는 오라는 편지를 쓴 적이 없다고 적혀 있었지?"),
                ("dad","응. 가져온 편지와 엄마가 맡긴 글을 나란히 놓고 확인해 보자.")]
        if k["promised"]:
            return [("daram","초롱 아저씨가 엄마 봉투를 맡고 있댔지?"),
                ("dad","응. 일요일 오전에 수리점에서 받기로 했어. 엄마가 어떤 글을 남겼을까?" if k["pending"] else "응. 등 밑 점검함에 두었다고 했어. 어떤 글을 남겼을까?")]
        if k["post"] or k["post_checked"]:return _r13_review_direction()
        if r13_has("J04"):
            return [("daram","나비 언니가 엄마가 초롱 아저씨에게 봉투를 건네는 걸 봤대."),("dad","그 봉투는 누구에게 남긴 글일까?")]
        if r13_has("J05"):
            return [("daram","까로 아저씨가 초롱 아저씨의 점검함에서 봉투를 봤대."),("dad","엄마가 남긴 소식과 관련이 있을까?")]
        if k["recognized"]:
            return [("daram","초롱 아저씨는 엄마를 알아봤지?"),("dad","응. 엄마와 마지막으로 어디서 만났는지도 더 들어 보고 싶어.")]
        if k["named"] and r13_has("M01"):
            return [("daram","메모에 적힌 분은 초롱 아저씨지?"),("dad","응. 그분도 엄마를 만났을까?")]
        return _r13_review_direction()

    _r13_review_intro_goal=r13_intro_goal
    def r13_intro_goal():
        previous=_r13_review_intro_goal();s=store.room13 or {};k=r13_mother_knowledge()
        ready=all(r13_has(v) for v in ("entry_corrected","lodging","M01","E03"))
        if s.get("life_poc") and s.get("case_state")=="pending" and ready and not r13_home_with_daram() and not (k["received"] or k["post"] or k["post_checked"]):
            row=r13_mother_note_row()
            if row and (k["promised"] or k["recognized"]):return row["title"]
        return previous

    _r13_review_promises=r13_calendar_promises
    def r13_calendar_promises():
        rows=_r13_review_promises(); k=r13_mother_knowledge()
        if k["pending"]:
            rows.append("3일째 · %s요일 — 초롱에게 엄마가 맡긴 봉투를 확인하기로 했다."%r13_weekday(3))
        return rows

    _r13_review_opening=r13_conversation_opening
    def r13_conversation_opening(person,first):
        k=r13_mother_knowledge(); s=store.room13 or {}
        if person=="resident_lamplighter" and k["pending"] and not r13_has("chorong_dead"):
            if s.get("day",1)>=3:
                r13_flag("topic:lamplighter_warning")
                return [(person,"다시 오셨군요. 말씀드린 봉투를 찾아뒀어요. 어디에 두었는지 알려드릴게요.")]
            return [(person,"봉투는 "+r13_weekday(3)+"요일 오전까지 찾아둘게요. 수리점으로 오세요. 다른 궁금한 일이 있으세요?")]
        return _r13_review_opening(person,first)

    _r13_review_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        s=store.room13 or {}
        if key in s.get("read_topics",[]):return _r13_review_topic_lines(key)
        if key=="ep1:tok_lamps" and r13_has("lt_dawn") and key not in s.get("read_topics",[]):
            return [("resident_tok","제 장부에는 그 등이 밤마다 깜빡인다고 적혀 있어요. 그런데 이제 조각까지 없어졌다니……."),
                ("buri","온도계는 지난주에 진료소 검사원님이 빌려 갔어요. 등 속 온도를 재는 기구예요."),
                ("resident_tok","제가 열었다고 몰아세우기 전에, 그 도구를 빌려 간 쪽에도 확인해 주세요.")]
        if key=="ask_mom:lamplighter":
            k=r13_mother_knowledge()
            if k["promised"]:
                return [("resident_lamplighter","부인이 가족에게 전해 달라고 한 봉투를 맡고 있어요. 지금 어디 계신지는 저도 몰라요.")]
            if k["recognized"]:
                return [("resident_lamplighter","전에 보여주신 부인은 기억해요. 다만 지금 어디 계신지는 저도 몰라요.")]
        if key=="register" and s.get("life_poc"):
            if s.get("day",1)>1:return [("granny","13호실 그대로 쓰세요. 부인이 잡아 둔 방이에요.")]
            return [("dad","아내가 머물던 방을 볼 수 있을까요?"),("granny","13호실이에요. 부인이 잡아 둔 그대로예요. 짐은 거기 두세요."),
                ("daram","엄마는 지금 어디 있어요?"),("granny","며칠째 안 보여요. 나간 뒤로 돌아오지 않았어요."),
                ("dad","방에 남긴 것부터 살펴보겠습니다.")]
        if key=="granny_letter" and s.get("life_poc"):
            return [("dad","아내가 가족을 부르겠다고 직접 말했습니까?"),("granny","네. 가족이 오면 【13호실】을 그대로 내주라고 했어요."),
                ("dad","언제 여관을 떠났나요?"),("granny","정확한 날짜는 숙박 장부에 있어요. 어디로 갔는지는 못 들었고요.")]
        if key=="lamplighter_warning" and r13_mother_knowledge()["recognized"]:
            return [("dad","아내가 맡긴 봉투를 받으러 왔습니다."),("resident_lamplighter","등 밑 점검함에 두었어요. 여관에는 맡기면 안 되는 글이라고 했어요."),
                ("resident_lamplighter","꺼내서 다른 곳에서 읽어 주세요. 누가 보냈는지 여기서 이야기하지 마시고요.")]
        return _r13_review_topic_lines(key)
