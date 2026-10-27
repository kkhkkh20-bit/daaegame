# Field observations belong to the father's viewpoint, not an omniscient voice.
default r13_thought_active = False

init 63 python:
    # Spoken bridges make the child's response audible and motivated. She never
    # answers an unspoken thought, and absent/held children never join in.
    R13_OBSERVATION_CHAT = {
        ("gate","shovel"):[("dad","발밑이 미끄럽네. 천천히 걸어가자."),("daram","응. 아빠도 내 손 꼭 잡고 놓지 마.")],
        ("square","stall"):[("dad","채소가 얼지 않게 천으로 잘 덮어 뒀네."),("daram","우리 가방도 이렇게 덮어 둘까?")],
        ("square","cart"):[("dad","손수레 앞은 길이 좁네. 돌아서 가자."),("daram","아빠, 나도 그렇게 생각해. 이쪽으로 가자.")],
        ("inn","knitting"):[("dad","장갑 한 짝은 아직 덜 떴네."),("daram","장갑 다 뜨면 손이 엄청 따뜻하겠다.")],
        ("inn","door"):[("dad","들어가기 전에 신발에 묻은 눈부터 털자."),("daram","잠깐. 밑창에도 눈이 잔뜩 붙었어.")],
        ("room13","boxes"):[("dad","엄마 가방 놓을 자리도 미리 비워 둘까?"),("daram","응. 이쪽은 엄마 자리로 비워 두자.")],
        ("room13","coat"):[("dad","장갑은 여기 넣어 뒀었지."),("daram","아빠, 그거 내 장갑인데.")],
        ("room13","bread"):[("dad","딱딱한 빵도 수프에 적시면 먹을 만하겠는데."),("daram","나도 그렇게 생각해! 빵만 그냥 먹기엔 너무 딱딱해.")],
        ("guestroom","boxes"):[("dad","짐은 안쪽으로 놓자. 문 앞에 두면 발에 걸리겠다."),("daram","내 가방은 내가 직접 옮길게.")],
        ("workshop","rag"):[("dad","손에 기름이 묻으면 이 천으로 닦나 봐."),("daram","기름 묻은 손을 옷에 닦으면 안 되겠지?")],
        ("dining","table"):[("dad","난로 가까운 자리가 덜 춥겠네."),("daram","그럼 아빠는 내 옆에 앉아.")],
        ("school","desks"):[("dad","책상을 조금 옮기면 둘이 누울 자리는 나오겠다."),("daram","응. 의자는 내가 옮겨 줄게.")],
        # 2026-10-26 소유자 "조사하기 클릭해서 여러가지 클릭하면 나오는 아빠와 다람이 문구가 없다": 1~3일 장소.
        # 다람은 자기 욕구·엉뚱한 짐작으로 말하고 아빠가 받아친다(VOICE_GUIDE 1-2-2). 단서의 뜻은 말하지 않는다 —
        # 창·빗장·장부·편지·약초·소포·차축처럼 사건과 닿는 물건은 넣지 않았다.
        ("gate","road"):[("daram","마차 다리가 부러졌어? 그럼 우리 이제 걸어서 집에 가?"),("dad","다리가 아니라 축. 그리고 집은 엄마 만나고 나서 가는 거야.")],
        ("gate","bundles"):[("daram","담요를 끈으로 꽁꽁 묶었네. 담요도 도망가?"),("dad","눈 맞으면 젖으니까. 젖은 담요는 밤에 아무도 안 덮어.")],
        ("gate","crates"):[("daram","아빠, 저 당근은 얼었대. 얼음 당근은 아삭할까?"),("dad","이가 먼저 아삭하겠지. 그래서 언 건 따로 빼 뒀잖아.")],
        ("gate","woodpile"):[("daram","장작도 받침 위에 앉아 있어."),("dad","눈에 바로 두면 젖어서 그래. 너도 눈밭에 털썩 앉지 말고.")],
        ("inn","coats"):[("daram","외투가 울어. 똑, 똑, 똑."),("dad","눈이 녹는 거야. 우리 외투도 걸면 같이 울겠다.")],
        ("inn","cups"):[("daram","컵이 다 짝짝이야. 아빠 양말처럼."),("dad","……양말은 일부러 그렇게 신은 거야.")],
        ("room13","cup"):[("daram","이 컵 금 갔어. 아빠가 써."),("dad","왜 아빠야?"),("daram","아빠는 천천히 마시잖아. 금 간 컵은 천천히 마셔야 돼.")],
        ("room13","notebook"):[("daram","아빠 공책은 왜 이렇게 비었어? 숙제 안 했어?"),("dad","들은 말이랑 본 걸 따로 적으려고 비워 둔 거야."),("daram","그럼 빈 데는 내가 그림 그려 줄게.")],
        ("room13","socks"):[("daram","양말에서 김 나. 아빠 발 냄새도 같이 말라?"),("dad","냄새는 안 마른다. 그래서 일부러 불에서 멀리 걸었지.")],
        ("room13","bedside_books"):[("daram","책으로 탑 쌓았네. 맨 위에 내 모자 올려도 돼?"),("dad","무너지면 네가 다시 쌓는 거다.")],
        ("hall","towels"):[("daram","수건이 층층이 쌓였어. 케이크 같아."),("dad","먹지는 마. 그건 진짜 수건이야.")],
        ("hall","bucket"):[("daram","아빠, 저 걸레로 우리 방도 닦을까?"),("dad","우리가 묻혀 온 눈부터 닦자. 그건 우리 몫이니까.")],
        ("dining","mittens"):[("daram","장갑들이 천장에서 손 흔들어."),("dad","말리는 거야. 네 장갑도 저기 걸어 줄까?"),("daram","싫어. 내 건 내가 끼고 있을래.")],
        ("dining","breadboard"):[("daram","빵 끝 조각만 따로 모아 놨다. 나 끝 조각 제일 좋아하는데."),("dad","먹고 싶으면 주인한테 먼저 여쭤보자. 남의 빵이야.")],
        ("dining","pot"):[("daram","냄새 좋다. 아빠, 저기 뭐 끓였어?"),("dad","뚜껑을 열어 봐야 알지. 그것도 주인한테 여쭤보고.")],
        ("kitchen","stove"):[("daram","불 앞은 따뜻하다. 나 오늘 여기서 자도 돼?"),("dad","부엌에서 자는 손님은 없어. 방은 따로 받았잖아.")],
        ("kitchen","vegetables"):[("daram","껍질도 따로 모아 놨어. 껍질도 먹어?"),("dad","국물 낼 때 쓰나 보다. 여기선 하나도 안 버리네.")],
        ("kitchen","dishes"):[("daram","아빠, 우리가 설거지 도와줄까?"),("dad","남의 부엌이야. 일하는 분한테 먼저 물어보자.")],
        ("kitchen","ladles"):[("daram","국자 하나만 손잡이에 붕대 감았어. 다쳤나?"),("dad","손잡이가 뜨거워서 감은 거야. 국자는 안 다쳐.")],
        ("passage","steps"):[("daram","계단 진짜 좁다. 아빠 배 걸리겠다."),("dad","배는 지나가. 걸리는 건 수건 바구니지.")],
        ("passage","linen"):[("daram","마른 수건은 위, 젖은 수건은 바구니. 우리 집이랑 다르다."),("dad","우리 집은 젖은 수건이 의자에 걸려 있었지. 네 의자.")],
        ("square","stone"):[("daram","돌에서 김이 나. 돌이 따뜻해?"),("dad","안에서 뭘 데우나 봐. 그래도 손은 대지 말자.")],
        ("square","offerings"):[("daram","장갑이 한 짝만 있어. 누가 놓고 갔나 봐."),("dad","……남이 일부러 둔 물건이야. 그냥 두자.")],
        ("square","wood"):[("daram","가게 앞만 눈이 없어. 빗자루가 다 쓸었나 봐."),("dad","주인이 쓸었겠지. 빗자루 혼자서는 안 쓸어.")],
        ("post","notice"):[("daram","편지는 언제 가? 엄마한테 우리 왔다고 보내자."),("dad","엄마는 이 마을에 있잖아. 편지보다 우리가 찾아가는 게 빠르지.")],
        ("post","scarf"):[("daram","목도리 엄청 길다. 두 바퀴 감아도 남겠어."),("dad","그럼 주인도 키가 크겠지. ……아마.")],
        ("workshop","bolts"):[("daram","나사가 크기대로 줄 섰어. 학교 같아."),("dad","그럼 제일 작은 게 너다."),("daram","그럼 제일 큰 건 아빠네. 배 때문에.")],
        ("workshop","tools"):[("daram","벽에 도구 그림자가 남았어."),("dad","자주 쓰는 자리라 색이 바랜 거야. 우리 집 국자 걸던 자리처럼.")],
        # 2026-10-27 소유자 "해줘": 4일 이후 장소. 진료소 병·기록, 학교 담요·장작, 창고 장부·자루, 온실 표식·기계,
        # 시설(사람을 넘겨주는 곳)과 제단(마지막 회의)은 사건과 닿거나 무거운 자리라 넣지 않았다.
        ("clinic","bed"):[("daram","침대 옆에 빨간 줄이 있어. 당기면 뭐가 나와?"),("dad","사람이 와. 아프지 않으면 당기지 말고.")],
        ("clinic","basin"):[("daram","물이 두 그릇이야. 하나는 손 씻고 하나는 세수?"),("dad","치료할 때 쓰는 거야. 우리는 눈으로만 보자.")],
        ("clinic","curtain"):[("daram","커튼에 접힌 줄이 잔뜩이야. 아빠 바지처럼."),("dad","……그건 다림질할 틈이 없어서 그래.")],
        ("school","stove"):[("daram","솥은 엄청 큰데 장작은 조금이네."),("dad","그래서 다들 나무 한 토막도 아껴 쓰는 거야.")],
        ("school","lessons"):[("daram","누가 공책에 글씨 연습했어. 나보다 삐뚤어!"),("dad","남의 공책 흉보는 거 아니다."),("daram","아빠도 지금 웃었잖아.")],
        ("store","scale"):[("daram","저울 밑에 가루가 떨어졌어. 아깝다."),("dad","여기선 그 가루도 쓸어 담을걸.")],
        ("store","burlap"):[("daram","포장천에 매듭 자국이 잔뜩이야. 나 매듭 묶을 줄 알아!"),("dad","그럼 네 신발 끈부터 다시 묶자. 풀렸어.")],
        ("greenhouse","pots"):[("daram","깨진 화분도 그냥 쓰네. 반창고 붙인 것 같아."),("dad","버리지 않고 받침으로 쓰는 거야. 여기선 뭐든 그래.")],
        ("greenhouse","watercan"):[("daram","물뿌리개가 비었어. 내가 눈 담아 올까?"),("dad","그 눈 녹을 때까지 기다리면 해 지겠다. 그냥 두자.")],
    }

    def r13_child_is_along():
        state=store.room13
        # 1일 입구에서는 명단을 고치기 전에도 다람이 바로 옆에 서 있다(현장 그림에도 함께 선다).
        if state.get("location")=="gate" and state.get("day")==1 and state.get("daram_state")=="with_dad":return True
        return state.get("daram_state") in ("with_dad","rescued") and r13_has("entry_corrected")

    def r13_observation_key(identity):
        # Special case IDs deliberately retain their forensic wording and do
        # not receive the light everyday conversations below.
        bits=identity.split(":")
        if len(bits)<3 or bits[0]!="object" or bits[1]=="case":return None
        return (bits[1],bits[2])

    def r13_observation_chat_key(identity):
        key=r13_observation_key(identity)
        if not key:return None
        state=store.room13
        return "%s:%s:%s:%s"%(state["day"],state["period"],key[0],key[1])

    def r13_observation_chat_allowed(identity):
        if not r13_child_is_along():return False
        key=r13_observation_key(identity)
        if key not in R13_OBSERVATION_CHAT:return False
        # No light banter while examining an active murder scene.
        if store.room13.get("case_state")=="occurred" and key[0] in ("room13","hall"):return False
        # 3일 아침 광장은 피코가 죽은(죽을 수 있는) 현장이다(VOICE_GUIDE 1-2-2).
        if key[0]=="square" and store.room13.get("day") in (3,13):return False
        # 12일 학교·진료소는 수프 사건의 자리(아이들이 앓거나 쓰러진다), 13일 광장은 군중·수레의 자리다.
        if key[0] in ("school","clinic") and store.room13.get("day")==12:return False
        seen=store.room13.get("observation_chats",[])
        token=r13_observation_chat_key(identity)
        prefix="%s:%s:"%(store.room13["day"],store.room13["period"])
        # 같은 때(날짜·시간대) 네 번까지. 두 번으로 막았더니 몇 개만 눌러도 반응이 사라졌다(소유자 2026-10-26).
        return token not in seen and sum(k.startswith(prefix) for k in seen)<4

    def r13_make_observation_lines(entries,identity):
        result=[]
        key=r13_observation_key(identity)
        for packet in entries:
            who,text=packet[:2]
            if who=="daram":
                # Old child_remark strings are covered by the paced, spoken
                # exchanges below instead of repeating on every inspection.
                continue
            if who in (None,"dad"):
                if key==("inn","desk") and not r13_has("lodging"):
                    text="장부와 열쇠패가 놓여 있네. 지금 방을 받을 수 있으려나? 주인에게 먼저 여쭤보자."
                elif key==("clinic","curtain"):
                    text=text+" 지금 안쪽을 살펴봐도 되려나? 먼저 물어봐야겠다."
                result.append(("dad","("+text+")",{"thought":True,"expression":"thinking","pose":"thinking"}))
            else:
                result.append(packet)
        if r13_observation_chat_allowed(identity):
            for who,text in R13_OBSERVATION_CHAT[key]:
                result.append((who,text,{"observation_chat":True}))
        return result

    def r13_remember_observation_chat(identity):
        token=r13_observation_chat_key(identity)
        if not token:return
        seen=list(store.room13.get("observation_chats",[]))
        if token not in seen:
            seen.append(token)
            r13_edit(observation_chats=seen)

label r13_observe(observed_entries,observed_identity):
    $ r13_observed_lines=r13_make_observation_lines(observed_entries,observed_identity)
    $ r13_observed_chat=any(len(p)>2 and isinstance(p[2],dict) and p[2].get("observation_chat") for p in r13_observed_lines)
    call r13_lines(r13_observed_lines,observed_identity+":dad-thought-v1", binding_route="dynamic:096")
    if r13_observed_chat:
        $ r13_remember_observation_chat(observed_identity)
    $ r13_thought_active=False
    return
