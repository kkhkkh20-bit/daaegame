# Existing dispatcher, actual engine effects. Prior movement is a QA fixture.
testcase existing_inn_content:
    pause 1.0
    click "처음부터"
    pause 2.0
    assert eval (ms14 is None)
    run Jump("r13_qa_existing_inn_setup")
    pause 2.0
    assert screen "r13_hub"
    assert eval ("M01" not in room13["evidence"] and "FAMILY_BUNDLE" not in room13["evidence"])
    assert eval (not r13_object_visible(ROOM13["objects"]["room13"]["family_bundle"]))
    click pos (210,400)
    pause 0.6
    click pos (640,600) until screen "r13_hub" timeout 45
    assert eval ("M01" in room13["evidence"] and r13_has("mother_lamplighter_lead"))
    assert eval ("물건은 책상 아래에 두었어." in ROOM13["evidence"]["M01"]["establishes"])
    assert eval (r13_object_visible(ROOM13["objects"]["room13"]["family_bundle"]))
    pause 0.6
    click pos (548,629)
    pause 0.6
    click pos (640,600) until screen "r13_hub" timeout 45
    assert eval (room13["evidence"].count("FAMILY_BUNDLE")==1 and r13_has("under_desk_checked"))
    screenshot "existing_inn_bundle.png"
    pause 0.6
    click pos (548,629)
    pause 0.6
    click pos (640,600) until screen "r13_hub" timeout 45
    assert eval (room13["evidence"].count("FAMILY_BUNDLE")==1)
    $ renpy.save("qa-existing-inn","inn")
    $ room13["evidence"].remove("FAMILY_BUNDLE")
    run Function(renpy.load,"qa-existing-inn")
    pause 0.8
    assert eval (ms14 is None and room13["evidence"].count("FAMILY_BUNDLE")==1)

label r13_qa_existing_inn_setup:
    $ room13=r13_new()
    $ r13_edit(day=1,period=1,location="room13",flags=["entry_corrected","lodging"])
    $ r13_world_cameras={"room13":0}
    $ _preferences.text_cps=0
    jump r13_roam
