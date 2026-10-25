# Capture the current connected UI only; no new art or production story changes.
testcase current_ui_capture:
    $ _test.timeout=30
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    $ persistent.room13_window_alpha="d4"
    pause 3.0
    screenshot "01-main.png"
    click "설정"
    pause until screen "pause_menu" timeout 20
    pause .5
    screenshot "02-settings.png"
    click "닫기"
    pause until screen "main_menu" timeout 20
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    pause .5
    screenshot "03-field.png"
    $ r13_black_card=False
    run Jump("r13_qa_b_dialogue_lines")
    pause 1.0
    screenshot "04-dialogue.png"
    run Hide("say")
    run Hide("r13_hub")
    run Function(renpy.hide,"r13_visitor")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "05-questions.png"
    run Hide("r13_qa_notebook_topics")
    run Show("r13_qa_choice_reference")
    pause .7
    screenshot "06-choice.png"
    run Hide("r13_qa_choice_reference")
    run Show("r13_map",initial_region="inn")
    pause 1.0
    screenshot "07-map-inn.png"
    click "숲·산길"
    pause .7
    screenshot "08-map-forest.png"
