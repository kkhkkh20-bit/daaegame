# Field observations belong to the father's viewpoint, not an omniscient voice.
default r13_thought_active = False

init 63 python:
    # Spoken bridges make the child's response audible and motivated. She never
    # answers an unspoken thought, and absent/held children never join in.
    R13_OBSERVATION_CHAT = {
        ("gate","shovel"):[("dad","발밑이 미끄럽네. 천천히 가자."),("daram","응. 아빠도 내 손 놓지 마.")],
        ("square","stall"):[("dad","채소가 얼지 않게 잘 덮어 뒀네."),("daram","우리 가방도 이렇게 덮어 둘까?")],
        ("square","cart"):[("dad","손수레 앞은 좁네. 돌아서 가자."),("daram","아빠, 나도 그렇게 생각해. 이쪽으로 가자.")],
        ("inn","knitting"):[("dad","장갑 한 짝이 아직 덜 됐네."),("daram","다 뜨면 손이 엄청 따뜻하겠다.")],
        ("inn","door"):[("dad","신발에 묻은 눈부터 털고 가자."),("daram","잠깐. 밑창에도 잔뜩 붙었어.")],
        ("room13","boxes"):[("dad","엄마 가방 놓을 자리도 비워 둘까?"),("daram","응. 이쪽은 엄마 자리로 하자.")],
        ("room13","coat"):[("dad","장갑은 여기 넣어 뒀었지."),("daram","아빠, 그거 내 장갑인데.")],
        ("room13","bread"):[("dad","수프에 적시면 이 빵도 먹을 만하겠는데."),("daram","나도 그렇게 생각해! 그냥은 너무 딱딱해.")],
        ("guestroom","boxes"):[("dad","짐은 안쪽으로 놓자. 발에 걸리겠다."),("daram","내 가방은 내가 옮길게.")],
        ("workshop","rag"):[("dad","손에 기름 묻으면 이 천으로 닦나 봐."),("daram","옷에 닦으면 안 되겠지?")],
        ("dining","table"):[("dad","난로 가까운 자리가 덜 춥겠네."),("daram","그럼 아빠는 내 옆에 앉아.")],
        ("school","desks"):[("dad","책상을 조금 옮기면 누울 자리는 나오겠다."),("daram","응. 의자도 내가 옮겨 줄게.")],
    }

    def r13_child_is_along():
        state=store.room13
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
        seen=store.room13.get("observation_chats",[])
        token=r13_observation_chat_key(identity)
        prefix="%s:%s:"%(store.room13["day"],store.room13["period"])
        return token not in seen and sum(k.startswith(prefix) for k in seen)<2

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
    call r13_lines(r13_observed_lines,observed_identity+":dad-thought-v1")
    if r13_observed_chat:
        $ r13_remember_observation_chat(observed_identity)
    $ r13_thought_active=False
    return
