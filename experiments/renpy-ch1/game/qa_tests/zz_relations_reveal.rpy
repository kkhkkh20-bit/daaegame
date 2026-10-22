# 0.20.6 (Codex R02 / S03): the chart never tells Dodam's death before the clinician confirms it,
# and Daram sent to school is not shown as "함께 있음".
testcase relations_reveal:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    $ r13_v111_set("route12","late_exposure")
    assert eval (r13_rel_status("kid_dodam")[0]!="dead" and "kid_dodam" in r13_nw_dead())
    $ r13_v111_set("alive:kid_dodam",False)
    assert eval (r13_rel_status("kid_dodam")[0]=="dead")
    $ r13_v111_set("DARAM_location","with_father")
    $ r13_v111_set("location:daram","school")
    assert eval (r13_rel_status("daram")==("missing","학교에 있음"))
