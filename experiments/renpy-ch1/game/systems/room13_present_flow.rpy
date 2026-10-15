# Question vs. presentation (owner, 0.18.13).
#   A plain question by name gets a vague answer. Showing the right record gets the fact.
#   No topic does the presenting for the player: the portrait and the name rubbing are
#   records that must be shown from the notebook.
#   The portrait helps week-2 contact only as identity: 초롱 no longer needs other proof
#   that Dad is family, and the reply signal is ready at the first period of the next day.
init 113 python:
    ROOM13["evidence"]["P01"]=dict(id="P01",name="피코가 그린 엄마 초상",kind="물증",
        establishes="아빠와 다람이가 말한 대로 피코가 그린 엄마의 얼굴이다. 왼쪽 눈썹에 작은 흉이 있다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["J07"]=dict(id="J07",name="초롱이 확인한 엄마의 얼굴",kind="증언",
        establishes="초롱이 엄마의 얼굴을 확인했다. 편지를 전달할 때 사람을 다시 찾을 필요가 없어졌다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["J08"]=dict(id="J08",name="슬링이 본 엄마의 편지",kind="증언",
        establishes="슬링은 초상 속 사람이 밤마다 편지를 부치러 왔다고 했다. 받는 사람 칸은 비어 있었고, 초롱이 그 편지를 받아 갔다고 했다.",
        does_not_establish="",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"].update(J07="resident_lamplighter",J08="resident_sling")
    R13_RECORD_SHORT.update(P01="엄마 초상",J07="초롱이 본 얼굴",J08="슬링이 본 편지")

    def _r13_ask_mom(npc,title,lines,not_flags):
        return dict(npc=npc,title=title,day=[2,4],need=["lodging"],give=[],flags=[],not_flags=list(not_flags),lines=list(lines))
    ROOM13["topics"].update({
        "ask_mom:lamplighter":_r13_ask_mom("resident_lamplighter","제 아내를 아십니까?",[
            ("dad","제 아내를 찾고 있습니다. 여관 13호실에 묵던 사람입니다."),
            ("resident_lamplighter","여관 손님이라면 등을 갈러 갈 때 몇 분 뵀지요. 그런데 이름만 들어서는 누군지 모르겠어요."),
            ("resident_lamplighter","손님들 이름까지 다 외우고 다니지는 않거든요.")],["intro:memo_shown","portrait_lamp_seen"]),
        "ask_mom:sling":_r13_ask_mom("resident_sling","제 아내를 보신 적 있습니까?",[
            ("dad","제 아내를 보신 적 있습니까? 여관 13호실에 묵던 사람입니다."),
            ("resident_sling","그분을 아느냐고요? 이름만으로는 모르겠는데요."),
            ("resident_sling","우체국에는 하루에도 여러 사람이 와서요.")],["portrait_known"]),
        "ask_mom:seryeon":_r13_ask_mom("seryeon","제 아내가 여기 들른 적 있습니까?",[
            ("dad","제 아내가 이 우체국에 들른 적 있습니까?"),
            ("seryeon","창구에 오신 분의 일은 함부로 말씀드릴 수 없어요."),
            ("seryeon","정말 가족이신지 제가 확인할 수 있어야 해요.")],["J03"]),
    })

    _r13_pf_topics=r13_topics
    def r13_topics(person):
        # These two used to present for the player; now the record itself is shown.
        return [(key,spec) for key,spec in _r13_pf_topics(person) if key not in ("portrait_sling","portrait_lamplighter","ppul_names")]

    _r13_pf_present=r13_present
    def r13_present(person,key,identity=False):
        if key=="P01" and r13_has("P01"):
            if person=="resident_sling" and not r13_has("portrait_known"):
                _r13_pf_present(person,key,identity)
                r13_flag("portrait_known")
                r13_grant(["J08"],"슬링에게 엄마 초상을 보여 줌")
                return [("resident_sling","……아, 이분이라면 봤어요. 밤마다 편지를 부치러 오셨어요. 받는 사람 칸은 늘 비워 두고요."),
                    ("resident_sling","그 편지는 초롱 아저씨가 받아 갔어요. 어디서 만났는지는…… 여기서 말하기는 좀 그래요.")]
            if person=="resident_lamplighter" and not r13_has("portrait_lamp_seen"):
                _r13_pf_present(person,key,identity)
                r13_flag("portrait_lamp_seen","lamplighter_trust")
                r13_grant(["J07"],"초롱에게 엄마 초상을 보여 줌")
                return [("resident_lamplighter","……잘 그렸네요. 이 얼굴이면 제가 아는 분이 맞아요."),
                    ("resident_lamplighter","지금 어디 계신지는 저도 몰라요. 그래도 나중에 편지를 전할 일이 생기면, 이제 그분이 맞는지 따로 확인할 필요는 없겠어요.")]
            if person=="daram":
                return [("daram","엄마다! 웃을 때 코 찡그리는 것까지 똑같아."),("dad","그래. 엄마를 본 사람이 이 얼굴은 알아볼지도 몰라.")]
            if person in ("granny","nabi"):
                return [(person,"13호실 손님이네요. 잘 그렸어요.")]
        if key=="R01" and person=="resident_ppul" and r13_has("R01") and not r13_has("ppul_names_seen"):
            _r13_pf_present(person,key,identity)
            r13_flag("ppul_names_seen")
            return list(ROOM13["topics"]["ppul_names"]["lines"])
        return _r13_pf_present(person,key,identity)

    # Identity reward: with the portrait seen, 초롱 does not ask for more proof of family.
    _r13_pf_w2_present=r13_w2_present
    def r13_w2_present(person,key,repeated):
        if person=="resident_lamplighter" and r13_has("portrait_lamp_seen") and not all(r13_has(k) for k in ("E01","E03")):
            for spec in ROOM13.get("presentations",[]):
                if spec["npc"]!=person or key not in spec["items"]:continue
                known={v.split(":")[0] for v in store.room13["resident_knowledge"].get(person,[])}
                if spec.get("all_shown") and not set(spec["items"]).issubset(known):break
                r13_flag("topic:"+spec["topic"])
                return [(person,"초상으로 얼굴을 확인했으니, 가족이라는 건 따로 묻지 않겠습니다."),(person,spec["reply"]),(None,"새 대화 주제가 열렸다.")]
        return _r13_pf_w2_present(person,key,repeated)
