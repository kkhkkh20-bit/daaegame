# 백 부인 비축 장부(H1): who sees it first changes what can still be confirmed
# (owner's knowledge-run plan B-2, 0.18.15).
#   서리  → counts the goods against the ledger right away (H10 if the goods are still there, H11 if not).
#   백 부인 → calls it an old ledger, and moves the goods at the next time change (work or sleep).
#   은호  → offers a deal and explains only his own part; no independent check.
# The ledger itself is never taken away. Only H1 behaves like this.
init 115 python:
    ROOM13["evidence"]["H10"]=dict(id="H10",name="서리가 대조한 장부와 현물",kind="기록",
        establishes="서리 검사원이 장부를 들고 창고 현물을 직접 세었다. 장부에 적힌 자루와 상자 수가 창고에 그대로 있었다.",
        does_not_establish="누가 쌓아 두라고 시켰는지는 이 대조로 알 수 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["H11"]=dict(id="H11",name="비어 가는 창고",kind="관찰기록",
        establishes="장부에 적힌 수량보다 창고의 상자가 적었다. 바닥에는 상자를 끌어낸 자국이 있다.",
        does_not_establish="누가, 언제, 어디로 옮겼는지는 이 자국만으로 알 수 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(H10="장부와 현물 대조",H11="비어 가는 창고")

    def r13_madam_moved():
        t=r13_town().get("madam_alerted_at")
        return t is not None and r13_abs_time()>t

    # The sacks look the same until the ledger gives a number to compare with.
    ROOM13["objects"]["store"]["hoard"]=dict(ROOM13["objects"]["store"]["sacks"],need=["H1"],give=[],flags=[],ledger_hoard=True,
        text="장부에 적힌 자루와 상자가 그대로 쌓여 있다.")
    ROOM13["objects"]["store"]["hoard_moved"]=dict(ROOM13["objects"]["store"]["sacks"],need=["H1"],give=["H11"],flags=[],ledger_hoard_moved=True,
        text="장부에 적힌 수량보다 상자가 적다. 바닥에는 상자를 끌어낸 자국이 있다.")
    _r13_ledger_visible=r13_object_visible
    def r13_object_visible(spec):
        store_objs=ROOM13["objects"]["store"]
        if spec is store_objs["sacks"] and r13_has("H1"):return False
        if spec.get("ledger_hoard"):return r13_has("H1") and not r13_madam_moved()
        if spec.get("ledger_hoard_moved"):return r13_has("H1") and r13_madam_moved()
        return _r13_ledger_visible(spec)

    ROOM13["topics"]["ledger_deal"]=dict(npc="resident_eunho",title="장부 이야기를 덮어 두기로 한다",day=[3,14],need=["eunho_deal_offered"],not_flags=["eunho_blackmailed","eunho_reconciled"],give=[],flags=["shop_half","eunho_blackmailed"],lines=[
        ("dad","장부 이야기는 당분간 꺼내지 않겠습니다."),
        ("resident_eunho","좋습니다. 그동안 제 가게 물건은 반값에 드리지요. 대신 이 거래는 우리 둘만 아는 걸로 합시다.")])

    _r13_ledger_present=r13_present
    def r13_present(person,key,identity=False):
        if key!="H1" or not r13_has("H1"):
            return _r13_ledger_present(person,key,identity)
        if person=="resident_seori" and not r13_has("ledger_counted"):
            _r13_ledger_present(person,key,identity)
            r13_flag("ledger_counted")
            if r13_madam_moved():
                r13_grant(["H11"],"서리 검사원과 창고를 확인함")
                return [("resident_seori","장부와 현물을 바로 맞춰 보지요."),
                    (None,"서리 검사원과 창고로 갔다. 검사원은 장부를 한 줄씩 짚으며 상자를 세었다."),
                    ("resident_seori","장부보다 상자가 적습니다. 바닥에 끌어낸 자국이 있군요. 언제 옮겼는지는 저도 모릅니다.")]
            r13_grant(["H10"],"서리 검사원이 장부와 현물을 대조함")
            r13_flag("madam_exposed")
            return [("resident_seori","장부와 현물을 바로 맞춰 보지요."),
                (None,"서리 검사원과 창고로 갔다. 검사원은 장부를 한 줄씩 짚으며 자루와 상자를 세었다."),
                ("resident_seori","적힌 수가 그대로 있습니다. 이 대조는 제 이름으로 기록하겠습니다.")]
        if person=="resident_madam" and r13_town().get("madam_alerted_at") is None and not r13_has("ledger_counted"):
            _r13_ledger_present(person,key,identity)
            r13_town_set(madam_alerted_at=r13_abs_time())
            r13_flag("madam_suspicious")
            return [("resident_madam","……그건 오래된 장부예요. 지난겨울 것이 섞였겠지요."),
                ("resident_madam","남의 창고 장부를 들고 다니시는 건 좋은 버릇이 아니에요.")]
        if person=="resident_eunho" and not r13_has("eunho_deal_offered") and not (r13_has("eunho_hostile") and not r13_has("eunho_reconciled")):
            _r13_ledger_present(person,key,identity)
            r13_flag("eunho_deal_offered")
            return [("resident_eunho","……부인 창고 장부군요. 저는 부인 창고에서 넘어온 물건을 받아 팔았을 뿐입니다."),
                ("resident_eunho","그 이야기를 덮어 두신다면, 제 가게 물건은 반값에 드릴 수 있습니다.")]
        return _r13_ledger_present(person,key,identity)
