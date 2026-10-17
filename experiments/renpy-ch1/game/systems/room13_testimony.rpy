# Testimony scope (owner's knowledge-run plan C, 0.18.15).
#   C-1 나비: first says 할머니 stayed with her (J09). After 도토's record (E11) she narrows it
#       to "until the first scream" (nabi_gap → E12). The first statement stays in the notebook.
#   C-2 도토: "nobody got into that room". Shown a passage record, he narrows it to the hall door (J10).
#       What he guarded did hold; he is not made a liar.
#   C-4 A rumor about 엄마 has sources: 여니 heard it from 까로, 누비 heard it in the dining room,
#       까로 saw only luggage with her name on it (canon: the returned package at the outer post).
init 116 python:
    for _key,_name,_kind,_est,_not in (
        ("J09","나비의 처음 말","증언","나비는 첫 비명 뒤에도 할머니가 자기와 주방에 있었다고 말했다.",""),
        ("J10","도토가 지킨 범위","증언","도토가 지킨 곳은 복도 쪽 13호 문이다. 방 안의 다른 출입구는 문밖에서 볼 수 없었다고 했다.","도토가 지킨 앞문으로 드나든 사람이 없었다는 말은 그대로다."),
        ("J11","여니가 들은 엄마 이야기","증언","여니는 엄마가 짐을 싸서 외곽 초소 쪽으로 갔다고 들었다. 까로에게 들은 말이고, 여니가 직접 본 것은 아니다.",""),
        ("J12","누비가 들은 엄마 이야기","증언","누비는 엄마가 짐을 들고 마을 밖으로 나갔다는 말을 식당에서 들었다. 누가 한 말인지는 기억하지 못한다.",""),
        ("J13","까로가 실어 간 짐","증언","까로가 직접 본 것은 엄마 이름표가 붙은 짐이 외곽 초소로 실려 간 것뿐이다. 엄마는 보지 못했다.",""),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind=_kind,establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"].update(J09="nabi",J10="doto",J11="resident_yeoni",J12="resident_nubi",J13="karo")
    R13_RECORD_SHORT.update(J09="나비의 처음 말",J10="도토가 지킨 범위",J11="여니가 들은 말",J12="누비가 들은 말",J13="까로가 실어 간 짐")

    def _r13_tm_topic(npc,title,give,lines,need=("lodging",),not_flags=()):
        return dict(npc=npc,title=title,day=[2,4],need=list(need),not_flags=list(not_flags),give=list(give),flags=[],state={"case_state":["pending"]},lines=list(lines))
    ROOM13["topics"].update({
        "rumor_mom:yeoni":_r13_tm_topic("resident_yeoni","제 아내 이야기를 들은 적 있습니까?",["J11"],[
            ("dad","여관 13호실에 묵던 제 아내 이야기를 들은 적 있습니까?"),
            ("resident_yeoni","그 부인이요? 짐을 싸서 외곽 초소 쪽으로 갔다던데요."),
            ("dad","직접 보셨습니까?"),
            ("resident_yeoni","아뇨, 까로 아저씨한테 들었어요. 그 아저씨가 짐을 실어 날랐다나요.")]),
        "rumor_mom:nubi":_r13_tm_topic("resident_nubi","제 아내 이야기를 들은 적 있습니까?",["J12"],[
            ("dad","여관 13호실에 묵던 제 아내 이야기를 들은 적 있습니까?"),
            ("resident_nubi","짐을 들고 마을 밖으로 나갔다던데요. 식당에서 누가 그러더라고요."),
            ("dad","누가 그런 말을 했는지 기억나십니까?"),
            ("resident_nubi","그건 모르겠어요. 밥 먹으면서 흘려들은 말이라서요.")]),
        "rumor_mom:karo":_r13_tm_topic("karo","부인의 짐을 실어 갔다고 들었습니다",["J13"],[
            ("dad","아내의 짐을 외곽 초소로 실어 가셨다고 들었습니다. 아내도 함께 갔습니까?"),
            ("karo","제가 실은 건 부인 이름표가 붙은 짐뿐이에요. 초소로 되돌려 보내는 짐이라고 해서요."),
            ("dad","그때 아내를 보셨습니까?"),
            ("karo","아뇨. 짐만 봤어요. 부인이 어디 계셨는지는 몰라요.")],need=("lodging","J11")),
    })

    # 0.18.22 audit: the first statement (J09) is read against the narrowed one (E12) in 기록 → 비교하기.
    _r13_tm_compare=r13_compare_result
    def r13_compare_result(selected):
        if set(selected)=={"J09","E12"} and {"J09","E12"}<=set((store.room13 or {}).get("evidence",[])):
            return "(나비는 처음에는 첫 비명 뒤에도 할머니가 함께 있었다고 했다. 도토의 기록을 본 뒤에는 첫 비명까지로 좁혔다. 그 뒤 할머니가 어디 있었는지는 나비도 모른다.)"
        return _r13_tm_compare(selected)

    _r13_tm_present=r13_present
    def r13_present(person,key,identity=False):
        if person=="doto" and key in ("E05","E37","E04") and r13_has(key) and not r13_has("J10"):
            _r13_tm_present(person,key,identity)
            r13_grant(["J10"],"도토에게 통로 기록을 보여 줌")
            return [("dad","그날 어느 출입구를 지켰니?"),
                ("doto","복도 쪽 문입니다."),
                ("dad","방 안의 다른 출입구도 보였니?"),
                ("doto","그건…… 문밖에서는 볼 수 없었습니다. 제가 지킨 문으로는 아무도 들어가지 못했어요. 그 말은 맞습니다.")]
        return _r13_tm_present(person,key,identity)
