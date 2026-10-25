default r13_qa_notebook_pick = 0

screen r13_qa_notebook_topics():
    modal True
    zorder 40
    $ entries=[("마을에 관해서",SetVariable("r13_qa_notebook_pick",1),False),("장터에 관해서",SetVariable("r13_qa_notebook_pick",2),True),("이곳의 겨울에 관해서",SetVariable("r13_qa_notebook_pick",3),False),("여관에서 하는 일",SetVariable("r13_qa_notebook_pick",4),False),("마차가 다니는 길",SetVariable("r13_qa_notebook_pick",5),False),("따뜻한 차에 관해서",SetVariable("r13_qa_notebook_pick",6),True)]
    use r13_side_question_list("granny","joy",entries,True,Hide("r13_qa_notebook_topics"))
    use r13_notebook_topic_tools(True,"granny",NullAction())

label r13_qa_notebook_menu:
    call r13_lines([("granny","편지에서 무엇을 더 살펴보겠니?",{"expression":"joy"})],"qa:notebook-menu")
    $ r13_last_partner="granny"
    $ r13_qa_notebook_pick=0
    menu:
        "마지막 줄을 본다":
            $ r13_qa_notebook_pick=1
        "글씨를 살핀다":
            $ r13_qa_notebook_pick=2
        "편지를 접는다":
            $ r13_qa_notebook_pick=3
    jump r13_roam

testcase b_notebook_questions:
    $ preferences.text_cps=0
    pause 2.0
    screenshot "notebook-01-main.png"
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    $ r13_black_card=False
    run Hide("r13_hub")
    run Show("r13_qa_notebook_topics")
    pause 1.0
    screenshot "notebook-02-questions-pc.png"
    click id "r13_side_topic_2"
    assert eval (r13_qa_notebook_pick==2)
    click "더보기"
    pause .5
    assert screen "r13_more_tools"
    run Hide("r13_more_tools")
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "notebook-03-questions-touch.png"
    click id "r13_topics_next"
    pause .3
    screenshot "notebook-04-questions-page2.png"
    click id "r13_side_topic_1"
    assert eval (r13_qa_notebook_pick==3)
    click "돌아가기"
    assert not screen "r13_qa_notebook_topics"

testcase b_notebook_choices:
    $ preferences.text_cps=0
    pause 2.0
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    $ r13_black_card=False
    run Jump("r13_qa_notebook_menu")
    pause .5
    click pos (640,400) until screen "choice" timeout 20
    pause .5
    screenshot "notebook-05-choices-pc.png"
    assert eval ("r13_visitor" not in renpy.get_showing_tags())
    $ renpy.save("qa-notebook-choice")
    click id "r13_notebook_choice_2"
    pause .5
    assert eval (r13_qa_notebook_pick==2)
    run Function(renpy.load,"qa-notebook-choice")
    pause 1.0
    assert screen "choice"
    assert eval ("r13_visitor" not in renpy.get_showing_tags())
    screenshot "notebook-06-choices-restored.png"
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "notebook-07-choices-touch.png"
    click id "r13_notebook_choice_1"
    pause .5
    assert eval (r13_qa_notebook_pick==1 and r13_choice_hidden_actor is None)
