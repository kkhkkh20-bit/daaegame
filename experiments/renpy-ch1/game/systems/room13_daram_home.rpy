# Daram is a companion at home, not a quest arrow or omniscient witness.
init 101 python:
    R13_DARAM_HOME_KEYS={
        "home:daram:rest":"오늘은 여기서 뭘 하고 있었어?",
        "home:daram:mother":"엄마가 쓰던 방을 보니 어때?",
        "home:daram:packet":"봉투 이야기를 듣고 무슨 생각이 들었어?",
        "home:daram:letters":"두 편지를 읽고 어떤 생각이 들었어?",
        "home:daram:case":"그날 일을 다시 이야기해도 괜찮겠니?",
        "home:daram:verdict":"재판이 끝나고 나니 어때?",
        "home:daram:cold":"방이 추워졌는데 괜찮아?",
        "home:daram:reunion":"엄마를 다시 만나니 어때?",
    }
    for key,title in R13_DARAM_HOME_KEYS.items():
        ROOM13["topics"][key]=dict(npc="daram",title=title,day=[1,14],need=["lodging"],give=[],flags=[],lines=[("dad",title)])

    def r13_daram_home_activity(state=None):
        s=(store.room13 or {}) if state is None else state
        period=min(s.get("period",0),2)
        if s.get("case_state")=="occurred" and s.get("trial_result")=="pending":
            return "neutral",(873,651,235),"침대 곁에서 쉬는 중"
        return (
            # 0.18.50 (owner): seat on the mattress, not on the bed frame in front of it.
            # 0.18.56 (owner): higher, on top of the blanket rather than sunk into its front edge.
            ("action_1",(950,398,210),"침대에서 책 읽는 중"),
            # 0.18.22 (owner): sat on the suitcase behind the chair and looked cut off; now on the rug.
            ("action_2",(900,645,210),"깔개에 앉아 그림 그리는 중"),
            ("inspect_floor",(875,625,195),"침대 곁을 둘러보는 중"),
        )[period]

    _r13_daram_home_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_daram_home_stage(entry)
        if not r13_home_with_daram():return actors
        result=[]
        for original in actors:
            if original["person"]!="daram":result.append(original);continue
            actor=dict(original)
            pose,(cx,anchor_y,height),activity=r13_daram_home_activity()
            # The temporary room has different furniture; keep its floor seat.
            if store.room13["location"]=="guestroom":cx,anchor_y,height=835,650,210
            # 0.18.59 wide 13호: the same activities on the wide picture's own bed/rug.
            # Child-sized standing height; seated/crouched poses keep the standing head size.
            elif r13_layout("room13") and store.room13["location"]=="room13":cx,anchor_y,height=r13_layout("room13")["home_positions"][pose]
            spec=r13_acting_spec("daram",pose) or {};width,native_height=r13_actor_geometry("daram",pose)
            scale=float(height)/native_height
            anchor=spec.get("seat") if pose=="action_1" and store.room13["location"]=="room13" else spec.get("foot",[width/2.0,native_height])
            x=int(cx-anchor[0]*scale);y=int(anchor_y-anchor[1]*scale);w=int(width*scale);h=int(native_height*scale)
            actor.update(pose=pose,x=x,y=y,width=w,height=h,rect=[x,y,w,h],depth=y+h,occlusion=[],contact=spec.get("contact","standing"),slot=None,activity=activity)
            result.append(actor)
        return sorted(result,key=lambda a:a["depth"])

    def r13_daram_home_allowed(key,state=None):
        s=(store.room13 or {}) if state is None else state
        evidence=set(s.get("evidence",[]));flags=set(s.get("flags",[]))
        if s.get("location") not in ("room13","guestroom") or s.get("daram_state") not in ("with_dad","rescued") or "lodging" not in flags:return False
        if key=="home:daram:rest":return True
        if key=="home:daram:mother":return "M01" in evidence or "E03" in evidence
        if key=="home:daram:packet":return bool(evidence.intersection(("J04","J05")))
        if key=="home:daram:letters":return {"E01","E18"}<=evidence
        if key=="home:daram:case":return s.get("case_state")=="occurred"
        if key=="home:daram:verdict":return s.get("trial_result") in ("acquitted","convicted","cleared") or s.get("trial_ended",False)
        if key=="home:daram:cold":return s.get("day",1)>=R13_WEEK2_DAY and s.get("week2_started",False)
        if key=="home:daram:reunion":return s.get("day",1)>=R13_WEEK2_DAY and s.get("mom_state")=="reunited"
        return False

    def r13_daram_home_context(state=None):
        s=(store.room13 or {}) if state is None else state
        return repr((s.get("day"),min(s.get("period",0),2),s.get("case_state"),s.get("trial_result"),s.get("mom_state"),tuple(sorted(s.get("evidence",[])))))

    def r13_daram_home_lines(key):
        s=store.room13;has=lambda item:item in s.get("evidence",[]) or item in s.get("flags",[])
        if not r13_daram_home_allowed(key):return []
        if key=="home:daram:rest":
            if s.get("case_state")=="occurred":return [("dad","오늘은 어떻게 지냈어?"),("daram","책을 폈는데, 머리에 안 들어와서 같은 줄만 자꾸 읽었어."),("dad","말하고 싶을 때 말해. 지금은 그냥 같이 있기만 해도 돼."),("daram","응. 아빠도 여기 앉아.")]
            period=min(s.get("period",0),2)
            return [
                [("dad","무슨 책 읽고 있어?"),("daram","엄마가 두고 간 책인가 해서 봤는데, 모르는 말이 많아."),("dad","재미있는 그림도 있어?"),("daram","아직은 없어. 내가 하나 그려 넣으면 안 되겠지?")],
                [("dad","수첩에 뭘 그렸어?"),("daram","우리가 타고 온 마차. 그런데 바퀴를 너무 크게 그렸어."),("dad","그 정도 바퀴면 눈에 안 빠지겠는데."),("daram","그럼 엄마도 태워서 집에 갈 수 있겠다.")],
                [("dad","침대 밑에 뭐 있어?"),("daram","연필이 침대 밑으로 굴러갔나 해서 봤어. 아까까지 여기 있었는데."),("dad","연필이 짐 사이에 끼었을 수도 있어."),("daram","내가 찾아볼게. 대신 엄마 물건은 안 건드릴게.")],
            ][period]
        if key=="home:daram:mother":
            if s.get("day",1)>=R13_WEEK2_DAY and s.get("mom_state")=="reunited":return [("dad","처음 왔을 때랑 이 방이 좀 다르게 보이니?"),("daram","처음엔 엄마 물건만 있어서 이상했어. 이제 엄마 얼굴을 봤으니까 조금 달라."),("dad","엄마가 쓰던 물건은 아직 그대로네."),("daram","응. 내가 그린 이 그림은 나중에 엄마한테 보여 줄 거야.")]
            lines=[("dad","엄마가 쓰던 방을 보니 어때?"),("daram","물건은 다 있는데 엄마만 없는 게 이상해.")]
            if has("M01"):lines += [("daram","엄마 메모에는 내 이름도 있잖아. 엄마가 우리 생각하면서 썼겠지?"),("dad","응. 다만 그 메모를 언제 쓴 건지는 아직 모르지만.")]
            elif has("E03"):lines += [("daram","이불 매듭이 엄마가 묶어 준 매듭이랑 닮았어."),("dad","매듭이 닮았다는 거랑 정말 엄마가 묶었다는 건 달라. 따로 적어 두자.")]
            return lines
        if key=="home:daram:packet":
            lines=[("dad","봉투 이야기를 듣고 무슨 생각이 들었어?")]
            if has("J04"):lines += [("daram","나비는 엄마가 봉투를 건네는 걸 봤대. 그런데 봉투 안에 든 건 못 봤대.")]
            if has("J05"):lines += [("daram","까로 아저씨가 본 봉투도 그 봉투와 같은 건지는 모르겠어.")]
            # 0.19.17: once Mom's letter (E18) is read, the envelope is no longer a guess.
            if has("E18"):return lines+[("daram","그 봉투에 엄마 글이 들어 있었던 거지?"),("dad","아마 그럴 거야. 초롱 씨가 엄마에게서 맡아 둔 글이니까. 다만 엄마가 지금 어디 있는지는 그 글에도 없었어.")]
            return lines+[("dad","응. 우리가 들은 이야기도 딱 거기까지야."),("daram","봉투 겉모습이 비슷해도 안에는 다른 편지가 들었을 수 있잖아.")]
        if key=="home:daram:letters":return [("dad","두 편지를 읽고 어떤 생각이 들었어?"),("daram","엄마는 오라는 편지를 쓴 적이 없대. 그럼 우리가 받은 편지는 누가 쓴 거야?"),("dad","응. 그게 이상해."),("daram","엄마가 쓴 오지 말라는 편지는 왜 우리한테 안 왔을까?"),("dad","그 이유는 아직 모르지.")]
        if key=="home:daram:case":return [("dad","그날 일을 다시 이야기해도 괜찮겠니?"),("daram","내가 때린 건 맞아. 그 사실은 안 바뀌잖아."),("dad","응. 네가 한 일하고 그 뒤에 생긴 일을 나눠서 듣고 싶어."),("daram","침대 밑에 숨고 나서는 이불밖에 안 보였어. 그 뒤에 일어난 일은 모르겠어."),("dad","모르는 건 억지로 떠올리지 않아도 돼.")]
        if key=="home:daram:verdict" and s.get("case_state")!="occurred":return [("dad","재판이 끝나고 나니 어때?"),("daram","사람들이 우리 얘기를 그렇게 오래 할 줄은 몰랐어."),("dad","네 이야기를 네 입으로 할 수 있어서 다행이야."),("daram","응. 오늘은 방에서 조금 쉬고 싶어.")]
        if key=="home:daram:verdict":return [("dad","재판이 끝나고 나니 어때?"),("daram","사람들이 여기 와도 된다고 했는데…… 아직도 문 두드리는 소리가 나면 깜짝 놀라."),("dad","한 번에 바로 괜찮아질 필요는 없어."),("daram","그래도 오늘은 책을 조금 읽었어.")]
        if key=="home:daram:cold":return [("dad","방이 추워졌는데 괜찮아?"),("daram","이불 속은 괜찮아. 그런데 아래층에 있는 사람들도 이불 있어?"),("dad","아래층 사람들 형편이 어떤지는 아빠도 아직 몰라."),("daram","다 같이 추운 겨울인데, 방마다 형편이 다른가 봐.")]
        if key=="home:daram:reunion":return [("dad","엄마를 다시 만나니 어때?"),("daram","할 말이 많았는데 엄마 얼굴 보니까 다 까먹었어."),("dad","생각나면 다음에 또 말하면 되지."),("daram","응. 그럼 할 말을 수첩에 조금씩 써 놓을래.")]
        return []

    _r13_daram_home_topics=r13_topics
    def r13_topics(person):
        rows=[(key,spec) for key,spec in _r13_daram_home_topics(person) if key!="intro:direction" and (key not in R13_DARAM_HOME_KEYS or r13_daram_home_allowed(key))]
        if person=="daram":
            fresh=[row for row in rows if row[0] in R13_DARAM_HOME_KEYS and not r13_daram_home_seen(row[0])]
            return fresh+[row for row in rows if row not in fresh]
        return rows

    _r13_daram_home_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        return r13_daram_home_lines(key) if key in R13_DARAM_HOME_KEYS else _r13_daram_home_topic_lines(key)

    def r13_daram_home_seen(key):
        return (store.room13 or {}).get("daram_home_discussions",{}).get(key)==r13_daram_home_context()

    _r13_daram_home_seen=r13_calendar_topic_seen
    def r13_calendar_topic_seen(key,spec):
        return r13_daram_home_seen(key) if key in R13_DARAM_HOME_KEYS else _r13_daram_home_seen(key,spec)

    _r13_daram_home_finish=r13_finish_topic
    def r13_finish_topic(key):
        _r13_daram_home_finish(key)
        if key in R13_DARAM_HOME_KEYS:
            n=winter_copy.deepcopy(store.room13)
            n.setdefault("daram_home_discussions",{})[key]=r13_daram_home_context(n)
            store.room13=n

    _r13_daram_room_intro_goal=r13_intro_goal
    def r13_intro_goal():
        if r13_home_with_daram() and store.room13.get("case_state")=="pending":
            evidence=set(store.room13.get("evidence",[]))
            if {"E01","E18"}<=evidence:return "엄마 이름으로 온 편지는 누가 썼을까?"
            if "M01" in evidence:return "엄마가 남긴 메모는 있는데, 지금 어디 있는지는 모른다."
            return "엄마가 머물렀던 방."
        return _r13_daram_room_intro_goal()

    _r13_daram_home_compare=r13_compare_result
    def r13_compare_result(selected):
        result=_r13_daram_home_compare(selected)
        if not r13_home_with_daram() or len(selected)!=2 or len(set(selected))!=2 or not set(selected)<=set(store.room13.get("evidence",[])):return result
        pair=set(selected)
        if pair=={"E01","E18"}:return "(우리를 부른 편지에는 엄마 이름이 있다. 그런데 엄마는 오라는 편지를 쓴 적이 없다고 썼다.)"
        if pair=={"M01","J04"}:return "(메모에 적힌 초롱의 이름이 나비의 이야기에도 나온다. 나비는 봉투를 건네는 장면을 봤지만, 그 안의 글은 읽지 못했다.)"
        if pair=={"M01","J05"}:return "(메모에는 초롱의 이름이 있다. 까로는 초롱이 봉투를 보관하는 모습을 봤다. 그 봉투가 엄마 것인지는 확인되지 않았다.)"
        if pair=={"E01","M01"} and "E18" in store.room13.get("evidence",[]):return "(메모에는 엄마가 늘 그리던 도토리가 있는데, 편지에는 없다. 엄마가 맡긴 글에는 오라는 편지를 쓴 적 없다고 적혀 있었다. 이 편지는 누가 쓴 걸까?)"
        if pair=={"E01","M01"}:return "(메모에는 엄마가 늘 그리던 도토리가 있는데, 편지에는 없다. 두 글을 같은 사람이 썼는지는 알 수 없다.)"
        return result

    _r13_daram_home_present=r13_present
    def r13_present(person,key,identity=False):
        response=_r13_daram_home_present(person,key,identity)
        state=store.room13 or {}
        if person!="daram" or not r13_home_with_daram() or key not in state.get("evidence",[]):return response
        if key=="E03" and "seam" in state.get("tool_discoveries",{}) and "tool:seam" in state.get("read_topics",[]):return response
        if any(spec.get("npc")==person and key in spec.get("items",[]) for spec in ROOM13.get("presentations",[])):return response
        if key in ("J04","J05"):topic="home:daram:packet"
        elif key in ("E01","E18") and {"E01","E18"}<=set(state.get("evidence",[])):topic="home:daram:letters"
        elif key in ("M01","E03"):topic="home:daram:mother"
        else:topic=None
        if topic and r13_daram_home_allowed(topic):return [("dad","이것도 같이 보자.")]+r13_daram_home_lines(topic)[1:]
        return [("dad","이것도 같이 읽어 볼래?"),("daram","응. 모르는 말이 나오면 물어봐도 돼?"),("dad","그럼. 아빠도 모르는 건 같이 적어 두자.")]
