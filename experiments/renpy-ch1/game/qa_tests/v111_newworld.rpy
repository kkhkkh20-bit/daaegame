testcase v111_nw_frozen_ending:
    # Four of the five lives lost: the 14th morning opens the frozen village before the kept endings.
    pause 1.0
    click "처음부터"
    pause 1.0
    run Function(r13_v111_set,"day",14)
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_set,"OWL_ALIVE",False)
    run Function(r13_v111_set,"nero_alive",False)
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_confirm" timeout 120
    assert eval (r13_v111_value("ending14")=="frozen" and r13_v111_value("story14_completed") and room13["location"]=="gate")
    screenshot "v111_nw_frozen_end.png"

testcase v111_nw_left_name_dad:
    # Two thefts list the father; the 13th cart leaves with him.
    pause 1.0
    click "처음부터"
    pause 1.0
    run Function(r13_v111_set,"day",14)
    run Function(r13_nw_steal,"qa_a")
    run Function(r13_nw_steal,"qa_b")
    run Function(r13_nw_cart_departs,[])
    assert eval (r13_v111_value("departed:dad") and not r13_v111_value("departed:daram"))
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_confirm" timeout 120
    assert eval (r13_v111_value("ending14")=="left_name_dad" and r13_v111_value("story14_completed"))
    screenshot "v111_nw_left_name_dad.png"
