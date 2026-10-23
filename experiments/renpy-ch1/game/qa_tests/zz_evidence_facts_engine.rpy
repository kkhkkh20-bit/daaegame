# 0.20.6 (Codex R03): the authored summaries load inside the real engine (store dict/list are the
# revertable types; a plain JSON dict must still pass) and replace the record's opening sentences.
testcase evidence_facts_engine:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (len(R13_EVIDENCE_FACTS)>=80)
    assert eval (r13_evidence_facts("V111:E01")==["다람이를 데리고 와 달라는 편지다.","여관 13호실에서 기다린다고 적혔다."])
    assert eval (r13_evidence_facts("V111:NW_KEEPER_DATE")[0].startswith("3일, 창고 침상의 노인이"))
