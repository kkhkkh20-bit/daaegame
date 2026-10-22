# 0.19.96: 수첩 관계도가 새 세계관 값(숨짐·이송 명단·떠남·데려옴·다람 붙잡힘)과 자료로 그려진다.
testcase v111_nw_relations:
    pause 1.0
    click "처음부터"
    click pos (640,300) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (640,300) until screen "r13_hub" timeout 90
    assert eval (r13_v111_active())
    python:
        for _p in ("granny","nabi","resident_tosil","resident_piko","resident_siluk","resident_madam","resident_lamplighter","resident_owlgp","doto","resident_teacher","resident_badook","resident_ppul","neoul","bami","npc_pandol"):
            r13_note_encounter(_p)
        r13_v111_set("day",8)
        r13_v111_set("OWL_ALIVE",False)
        r13_grant(["V111:E16","V111:E09_SCARF","V111:E09","V111:E20"],"qa")
        r13_v111_set("day",12)
        r13_v111_set("piko_alive",False)
        r13_v111_set("DARAM_DETAINED",True)
        r13_nw_list("nabi","qa");r13_v111_set("departed:nabi",True)
        r13_nw_list("resident_teacher","qa")
        r13_v111_set("day",14)
        r13_v111_set("handed:resident_teacher",True)
    run Show("r13_records",initial_tab="relations")
    pause 1.5
    screenshot "nw_relations.png"
    assert eval (r13_rel_status("resident_owlgp")[0]=="dead" and r13_rel_status("resident_piko")==("dead","12일 아침 숨짐"))
    assert eval (r13_rel_status("nabi")==("gone","12일 아침 수레로 떠남"))
    assert eval (r13_rel_status("resident_teacher")==("saved","14일 아침 수레에서 데려옴"))
    assert eval (r13_rel_status("daram")[0]=="missing" and r13_rel_status("mom")==("missing","아직 못 만남"))
    assert eval (("resident_siluk","resident_madam","suspect","등 조각을 팔고 삼") in r13_rel_edges())
    assert eval (("granny","resident_owlgp","suspect","핀과 목도리") in r13_rel_edges())
    assert eval (not any(l=="편지를 가져오라 부탁" for a,b,k,l in r13_rel_edges()))
    click "전체 관계도"
    pause 1.2
    screenshot "nw_relations_all.png"
