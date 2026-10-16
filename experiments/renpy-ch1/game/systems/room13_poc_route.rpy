# A short mother-search loop. Work opens questions, never automatically awards
# testimony. Existing direct routes, later crime and meeting rules stay intact.
init 100 python:
    def r13_poc_active(state=None):
        s=(store.room13 or {}) if state is None else state
        return bool(s.get("life_poc") and 2<=s.get("day",1)<=4 and s.get("case_state")=="pending")

    def r13_poc_worked(key,state=None):
        s=(store.room13 or {}) if state is None else state
        return any(job.get("key")==key for job in r13_wallet(s)["jobs"])

    def r13_poc_helped(person,state=None):
        s=(store.room13 or {}) if state is None else state
        if any(R13_JOBS.get(job.get("key"),{}).get("npc")==person for job in r13_wallet(s)["jobs"]):return True
        # Shop integration writes only accepted, completed help, not purchases.
        # Reading this optional history neither consumes items nor fakes work.
        return any(isinstance(event,dict) and event.get("person")==person and event.get("kind") in ("gift","errand") and event.get("completed") is True for event in s.get("resident_help",[]))

    # Picking up an already located envelope is ordinary investigation, not a
    # half-day research activity. Reading still precedes the original E18 grant.
    ROOM13["activities"]["warning"]["cost"]=0
    ROOM13["evidence"]["E18"]["establishes"]="첫 주에 가족에게 남긴 엄마의 글. ‘너희한테 오라는 편지를 쓴 적 없어. 여관에 내가 어디로 가는지 말하지 마. 등불을 고치는 사람을 통해 답해 줘. 혼자 누구를 만나러 가지 말고.’라고 적혀 있다."
    for key in ("intro:lamplighter_mother","intro:post_visit"):
        ROOM13["topics"][key]["day"]=[2,4]
    ROOM13["topics"]["intro:direction"]["day"]=[1,4]

    R13_POC_WITNESSES = {
        "J04":dict(name="나비가 본 엄마의 봉투",who="nabi",short="엄마가 맡긴 봉투",
            text="나비는 엄마가 여관에서 초롱에게 접힌 봉투를 건네는 것을 봤다고 했다. 봉투 안의 글은 읽지 않았고, 둘이 나눈 말도 듣지 못했다."),
        "J05":dict(name="까로가 본 초롱의 보관함",who="karo",short="초롱의 보관함",
            text="까로는 초롱이 광장 등불 아래 점검함에 봉투를 넣고 잠그는 것을 본 적이 있다고 했다. 엄마의 봉투인지, 누구에게 보낼 것인지는 모른다."),
        "J06":dict(name="할머니가 설명한 초대 이유",who="granny",short="할머니의 초대 이유",
            text="할머니는 그 편지를 자기가 받아 적어 부쳤다고 인정했다. 엄마가 불러 달라고 했다는 말은 할머니의 주장일 뿐이다. 엄마가 여관을 피하라고 경고한 이유까지 확인된 것은 아니다."),
    }
    for key,note in R13_POC_WITNESSES.items():
        ROOM13["evidence"][key]=dict(id=key,name=note["name"],kind="증언",establishes=note["text"],does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
        ROOM13["evidence_sources"][key]=note["who"]
        R13_RECORD_SHORT[key]=note["short"]

    ROOM13["topics"]["poc:nabi_packet"]=dict(npc="nabi",title="다람이 엄마가 초롱 씨에게 뭘 맡긴 적 있었니?",day=[2,4],need=["poc:note_shown:nabi"],give=["J04"],flags=[],poc_help="nabi",lines=[
        ("dad","아내가 여기서 초롱 씨를 만났다고 하더구나. 아내가 그 사람에게 뭘 맡긴 적도 있었니?"),
        ("nabi","부인이 봉투 하나를 건네는 건 봤어요. 접힌 채로요."),
        ("dad","그 봉투 안에 무엇이 들었는지도 아니?"),
        ("nabi","봉투는 안 읽었어요. 두 분이 하는 말도 못 들었고요."),
        ("dad","아내가 봉투를 직접 건네는 걸 봤다는 것만 적어 둘게. 나머지는 초롱 씨에게 확인해 봐야겠구나.")])
    ROOM13["topics"]["poc:karo_box"]=dict(npc="karo",title="초롱 씨는 맡은 편지를 어디에 둡니까?",day=[2,4],need=["poc:note_shown:karo"],give=["J05"],flags=[],poc_help="karo",lines=[
        ("dad","아내 메모에는 초롱 씨에게 소식을 물어보라고 적혀 있네요. 그분이 편지를 따로 맡아 두는 곳이 있습니까?"),
        ("karo","광장 등불 아래에 있는 점검함이요. 그 함에 봉투를 넣고 잠그는 걸 본 적 있어요."),
        ("dad","그 봉투가 아내에게서 받은 것인지도 아십니까?"),
        ("karo","누구 봉투인지는 몰라요. 그래도 허락 없이 함을 열어 보지는 마세요."),
        ("dad","점검함을 찾기 전에, 아내의 메모와 들은 이야기를 가지고 초롱 씨에게 먼저 물어보겠습니다.")])
    ROOM13["topics"]["poc:granny_letter"]=dict(npc="granny",title="아내는 쓴 적 없다는데, 그 편지는 누가 썼습니까?",day=[3,4],need=["poc:letter_conflict","warning_exposed"],give=["J06"],flags=["poc:granny_explained"],lines=[
        ("dad","아내 이름으로 온 편지와 아내가 직접 쓴 글을 함께 읽었습니다. 아내는 오라는 편지를 쓴 적이 없다고 썼더군요."),
        ("granny","부인이 가족을 보고 싶다고 했어요. 그 말을 제가 받아 적어 부쳤을 뿐이에요."),
        ("dad","그럼 아내는 왜 여관에는 자기 행선지를 말하지 말라고 했을까요?"),
        ("granny","부인을 기다리는 저도 그 이유를 알고 싶네요. 부인이 돌아와서 직접 말해 주면 좋겠어요."),
        ("dad","편지를 할머니가 썼다는 것은 적어 두겠습니다. 아내가 행선지를 말하지 말라고 경고한 이유는 더 알아봐야겠군요.")])

    _r13_poc_topics=r13_topics
    def r13_topics(person):
        rows=_r13_poc_topics(person)
        rows=[(key,spec) for key,spec in rows if not key.startswith("poc:") or (r13_poc_active() and (not spec.get("poc_help") or r13_poc_helped(spec["poc_help"])))]
        return sorted(rows,key=lambda row:0 if row[0].startswith("poc:") and row[0] not in store.room13.get("read_topics",[]) else 1)

    _r13_poc_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13 or {}
        if not r13_poc_active() or key not in s.get("evidence",[]):return _r13_poc_present(person,key,identity)
        if key=="M01" and person in ("nabi","karo"):
            original=_r13_poc_present(person,key,identity)
            r13_flag("poc:note_shown:"+person)
            job="kitchen" if person=="nabi" else "delivery"
            if person=="karo":
                r13_flag("mother_lamplighter_lead")
                original=[("dad","아내가 남긴 메모입니다. 등불을 돌보는 분에게 소식을 물어보라고 적혀 있네요."),(person,"초롱 씨를 말하는군요. 맡겨 둔 소식을 찾으시는 거라면, 제가 본 것도 말씀드릴 수 있어요.")]
            if r13_poc_helped(person):
                return original+[(person,"도와주셔서 고마워요. 말씀하신 때에 제가 본 것도 생각났어요. 무엇이 궁금한지 물어봐 주세요.")]
            return original+[(person,"식사 준비를 같이 하고 나면, 그분이 오셨을 때 제가 본 것도 차분히 말씀드릴게요." if person=="nabi" else "배달을 마치고 짐표를 정리할 때, 초롱 씨가 소식을 맡아 두는 곳도 말씀드릴게요.")]
        if key in ("J04","J05") and person=="resident_lamplighter":
            _r13_poc_present(person,key,identity)
            if s["day"]<3:
                return [("dad","혹시 아내가 맡긴 봉투가 있는지 직접 확인하고 싶습니다."),(person,"가족에게 전할 것이 있어요. 오늘은 챙길 일이 남아 있어서, 내일 다시 와 주시겠어요?")]
            r13_flag("topic:lamplighter_warning")
            return [("dad","아내가 봉투를 맡겼다는 이야기와 점검함 이야기를 들었습니다. 혹시 가족에게 남긴 글입니까?"),(person,"맞아요. 먼저 어디서 어떻게 받을지 설명할게요. 물어보세요.")]
        result=_r13_poc_present(person,key,identity)
        if key=="E18" and person=="granny":r13_flag("poc:warning_shown_granny")
        return result

    _r13_poc_compare=r13_compare_result
    def r13_compare_result(selected):
        s=store.room13 or {};owned=set(s.get("evidence",[]))
        if r13_poc_active() and len(selected)==2 and len(set(selected))==2 and set(selected)<=owned:
            pair=set(selected)
            if pair=={"E01","E18"}:
                r13_flag("poc:letter_conflict")
                return "(우리는 엄마 이름으로 온 편지를 받고 왔다. 그런데 엄마는 ‘오라는 편지를 쓴 적 없어’라고 썼다. 우리가 받은 편지는 누가 썼을까? 그리고 엄마는 왜 여관을 피하라고 했을까? 엄마가 여관을 피하라고 한 글을, 여관 사람에게 보여 줘도 될까?)"
            if pair=={"M01","J04"}:
                return "(엄마의 메모는 초롱에게 물어보라고 했다. 나비는 엄마가 그에게 봉투를 건네는 것을 봤다. 봉투 안의 글은 나비도 모른다.)"
            if pair=={"M01","J05"}:
                return "(메모는 초롱에게 물어보라고 했고, 까로는 그의 보관함을 안다. 함에 있는 봉투가 엄마 것이라는 뜻까지 확인되지는 않았다. 남의 보관함을 허락 없이 열어도 될까?)"
            if pair=={"M01","E18"}:
                return "(엄마는 우리가 올 경우를 위한 메모를 남겼고, 다른 글에서는 여관에 행선지를 말하지 말라고 경고했다. 가족을 버렸다고 단정할 수는 없다. 초롱을 통해 소식을 확인하라는 부탁은 두 글에 이어진다.)"
        return _r13_poc_compare(selected)

    def r13_poc_goal():
        s=store.room13 or {}
        if not r13_poc_active():return None
        has=lambda k:k in s.get("flags",[]) or k in s.get("evidence",[])
        # 0.18.74 (design review #1): before any testimony points at granny the question stays
        # open; it names her only after J06 (she says she wrote it), H9, H16 or the rope night.
        if has("poc:granny_explained"):return "할머니는 엄마 말을 받아 적었을 뿐이라고 했다. 엄마는 ‘쓴 적 없다’고 했는데, 할머니는 왜 우리를 여관에 두려 할까?"
        if has("poc:letter_conflict"):
            if any(has(k) for k in ("H9","H16","know_granny_reads","granny_lure_seen")):return "엄마가 부탁하지 않았다면, 할머니는 왜 우리를 불렀을까?"
            return "엄마가 쓰지 않았다면, 누가 어떤 사정으로 이 편지를 보냈을까?"
        if has("E18"):return "‘오라는 편지를 쓴 적 없어’ — 그럼 우리가 받은 편지는?"
        if has("warning_location"):return "초롱이 말한 점검함에는 무엇이 들어 있을까?"
        if has("J04") or has("J05"):return "엄마가 초롱에게 맡긴 봉투에는 무엇이 적혀 있을까?"
        if has("poc:note_shown:nabi") and r13_poc_helped("nabi"):return "나비는 여관에서 엄마와 초롱을 함께 본 적이 있을까?"
        if has("poc:note_shown:karo") and r13_poc_helped("karo"):return "초롱은 맡은 소식을 어디에 둘까?"
        if has("J03"):
            return "우체국을 나온 엄마는 누구를 만났을까?"
        if has("J02") and s.get("period",0)>=2:return "엄마는 정말 우체국 안에 들어갔을까? · 창구는 내일 오전에 연다"
        return None

    _r13_poc_intro_goal=r13_intro_goal
    def r13_intro_goal():return r13_poc_goal() or _r13_poc_intro_goal()
    _r13_poc_campaign_goal=r13_campaign_goal
    def r13_campaign_goal():return r13_poc_goal() or _r13_poc_campaign_goal()

    _r13_poc_job_context=r13_learning_job_context
    def r13_learning_job_context(key,state=None):
        s=(store.room13 or {}) if state is None else state
        if r13_poc_active(s) and "M01" in s.get("evidence",[]) and key in ("kitchen","delivery"):
            topic="poc:nabi_packet" if key=="kitchen" else "poc:karo_box"
            if topic not in s.get("read_topics",[]):
                pass
        return _r13_poc_job_context(key,s)

    _r13_poc_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_poc_notes()
        if not r13_poc_active():return rows
        s=store.room13;has=lambda k:k in s.get("flags",[]) or k in s.get("evidence",[])
        if has("E18"):
            rows[0]=dict(title="왜 초대 편지와 엄마의 경고가 다를까?",fact="엄마는 오라는 편지를 쓴 적 없으며, 여관에 행선지를 알리지 말라고 썼다.",question="엄마 이름으로 온 편지는 누가 썼을까? 엄마는 왜 여관을 피할까?",hint="두 글을 나란히 놓으면 무엇이 서로 다른가? 편지를 부친 사람은 그 이유를 어떻게 설명할까? 아직 범인이라고 단정할 수는 없다.",keys=["E01","E18"])
        elif has("J04") or has("J05"):
            rows[0]=dict(title="초롱에게 맡긴 글은 가족에게 남긴 것일까?",fact="함께 일한 주민에게 봉투 또는 보관함에 관한 말을 들었다. 내용과 받는 사람은 아직 모른다.",question="초롱이 엄마에게서 직접 맡은 글이 있을까?",hint="들은 말은 봉투가 있었다는 것뿐이다. 봉투를 맡은 사람은 무엇을 알고 있을까? 남의 보관함을 함부로 열면 신뢰를 잃는다.",keys=[k for k in ("M01","J04","J05") if has(k)])
        elif has("J03"):
            rows[0]=dict(title="엄마가 남긴 소식은 누구에게 맡겨졌을까?",fact="우체국 방문까지 확인했지만 그 이후 행선지는 모른다. 메모는 초롱에게 물어보라고 했다.",question="나비가 두 사람 사이에서 본 것, 까로가 아는 연락 방법은 있을까?",hint="엄마가 여관에 머무는 동안 날마다 마주친 사람은 누구였을까? 함께 일하면 바쁜 사람과도 차분히 이야기할 수 있다.",keys=["M01","J02","J03"])
        return rows

label r13_poc_night_review:
    if not r13_poc_active() or not r13_home_with_daram() or room13["day"] not in (2,3):
        return
    $ r13_poc_night_key="poc:night:"+str(room13["day"])
    if r13_has(r13_poc_night_key):
        return
    if r13_has("poc:letter_conflict"):
        call r13_lines([("daram","엄마는 오라는 편지를 쓴 적 없대. 그럼 우리가 받은 건 누가 쓴 거야?"),("dad","응. 두 편지를 나란히 놓으니 말이 서로 달라."),("daram","엄마는 우리가 오는 게 싫었던 거야?",{"expression":"anxious"}),("dad","아니. 엄마 글에는 우리 걱정만 적혀 있었어. 누가 엄마 이름으로 우리를 불렀는지 알아내야 해.")],"poc:night:letters")
    elif r13_has("E18"):
        call r13_lines([("daram","엄마 글에는 오라는 편지를 쓴 적 없다고 적혀 있어."),("dad","그럼 엄마 이름으로 온 초대 편지는 누가, 왜 쓴 걸까?")],"poc:night:uncompared")
    elif r13_has("J04") or r13_has("J05"):
        call r13_lines([("daram","어딘가에 엄마가 맡겨 둔 글이 있을지도 몰라."),("dad","응. 봉투가 있었다는 것만 알아. 안에 뭐가 적혔는지는 봉투를 맡아 둔 사람만 알겠지.")],"poc:night:packet")
    elif r13_has("J02") and not r13_has("J03"):
        call r13_lines([("daram","우체국에도 엄마가 갔었는지 아직 못 물어봤지?"),("dad","응. 우체국 창구는 오전에 열어. 그런데 손님 이야기를 우리한테 해 줄까?")],"poc:night:post")
    else:
        call r13_lines([("daram","오늘 물어본 건 수첩에 다 적어 뒀지?"),("dad","응. 엄마는 우리가 올 걸 알았는데 왜 기다리지 않았을까. 그게 계속 마음에 걸려.")],"poc:night:search")
    $ r13_flag(r13_poc_night_key)
    return
