# Focused production UI/dispatch fixture; no change to story eligibility.
label r13_design_piko_fixture:
    call r13_qa_setup(2, [], ["lodging","entry_corrected"])
    $ r13_edit(location="square",period=0,case_state="pending")
    $ r13_offer("r13_w1c_portrait")
    call r13_scene("winter_square","광장","calm")
    call screen r13_hub
    $ r13_design_choice=_return
    if r13_design_choice == ("offer","r13_w1c_portrait"):
        call r13_take_offer("r13_w1c_portrait")
    return

testcase design_restore_piko:
    pause 2.0
    $ _preferences.text_cps=0
    click "처음부터"
    pause 2.0
    run Call("r13_design_piko_fixture")
    pause until screen "r13_hub" timeout 30
    pause 1.0
    assert eval (r13_offer_staged("r13_w1c_portrait",r13_stage_people()))
    assert eval ("resident_piko" in r13_visible_people())
    screenshot "piko-nameplate-offer.png"
    click "피코 !"
    advance until eval (r13_packet[0]=="resident_piko") timeout 30
    pause 0.6
    assert eval (r13_design_choice==("offer","r13_w1c_portrait") and "r13_w1c_portrait" not in room13.get("offers",{}))
    screenshot "piko-actual-event-dialogue.png"
