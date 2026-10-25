# Isolated visual comparison only. These captions do not enter the story or save progression.
screen r13_qa_choice_reference():
    modal True
    zorder 200
    add Transform("assets/room13-pixel-carriage-empty-winter.webp",xysize=(1280,720))
    $ entries=[("마지막 줄을 본다",SetVariable("r13_qa_notebook_pick",1),False),("글씨를 살핀다",SetVariable("r13_qa_notebook_pick",2),False),("편지를 접는다",SetVariable("r13_qa_notebook_pick",3),False)]
    use r13_notebook_choice_list("daram","neutral","편지를 살펴볼까?",entries,True,caption="편지를 살펴볼까?")


testcase b_choice_reference:
    $ _test.timeout=30
    pause 2.0
    run Function(renpy.set_physical_size,(1280,720))
    $ persistent.room13_large_text=False
    run Show("r13_qa_choice_reference")
    pause 1.0
    screenshot "reference-choice-pc.png"
    click id "r13_notebook_choice_1"
    pause .3
    assert eval (r13_qa_notebook_pick==1)
    screenshot "reference-choice-focused.png"
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "reference-choice-touch.png"
    click id "r13_notebook_choice_3"
    assert eval (r13_qa_notebook_pick==3)
