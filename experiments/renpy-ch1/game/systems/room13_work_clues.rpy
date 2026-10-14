# Work opens conversations; testimony is recorded only after that conversation.
init 96 python:
    R13_WORK_RELATIONS={
        "nabi_helped":"나비와 식사를 준비하며 따로 놓인 그릇을 물었다.",
        "same_lane":"두 배달의 목적지가 같은 길이라는 것을 확인했다.",
        "karo_trusted":"까로가 다음 배달에는 묶음끈을 빌려주기로 했다.",
        "buri_honest":"부리에게 실제 부품 수와 장부의 차이를 알렸다.",
    }
    ROOM13["evidence"]["J01"]=dict(id="J01",name="나비의 등불지기 이야기",kind="증언",
        establishes="나비는 초롱이 마을 등불을 돌보며, 엄마가 머물던 때에도 여관에 왔다고 말했다. 엄마와 무슨 이야기를 했는지는 듣지 못했다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"]["J01"]="nabi"
    ROOM13["topics"]["life:nabi"]["give"]=["J01"]
    ROOM13["topics"]["life:nabi"]["lines"][-1]=("nabi","네, 아내분이 머물 때도 왔어요. 무슨 이야기를 나눴는지는 못 들었으니까, 그분에게 직접 물어봐요.")
    R13_RECORD_SHORT.update(M01="엄마의 메모",J01="등불지기 이야기")

    _r13_work_compare=r13_compare_result
    def r13_compare_result(selected):
        owned=set((store.room13 or {}).get("evidence",[]))
        if set(selected)=={"M01","J01"} and len(selected)==2 and set(selected)<=owned:
            return "(메모의 ‘등불을 돌보는 분’은 초롱인 것 같다. 아내가 머물 때 여관에도 왔다고 한다. 메모를 직접 보여 주고 확인해 보자.)"
        return _r13_work_compare(selected)

    _r13_work_present=r13_present
    def r13_present(person,key,identity=False):
        if key=="J01" and r13_has("J01"):
            if person=="resident_lamplighter":
                return [("dad","나비에게 들었습니다. 아내가 머물 때도 여관에 오셨다고요."),
                    (person,"식사를 받으러 갔었죠. 혹시 그분이 가족에게 남긴 글이나 물건을 가지고 계십니까?")]
            if person=="nabi":
                return [(person,"초롱에게 직접 물어봐요. 내가 들은 것보다 더 알고 있을 수도 있죠.")]
        return _r13_work_present(person,key,identity)

    def r13_work_available(key):
        return r13_job_allowed(store.room13,key) and r13_where(R13_JOBS[key]["npc"]) is not None

    def r13_work_status(key):
        s=store.room13
        if s.get("period",0)>=2:return "오늘 일할 시간은 끝났다"
        if any(j["day"]==s["day"] and j["key"]==key for j in r13_wallet(s)["jobs"]):return "오늘 마친 일"
        if r13_where(R13_JOBS[key]["npc"]) is None:return "지금은 일을 맡긴 사람을 만날 수 없다"
        return "마치면 "+r13_time_target()
