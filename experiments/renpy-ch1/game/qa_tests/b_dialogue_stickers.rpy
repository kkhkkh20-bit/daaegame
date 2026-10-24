label r13_qa_b_dialogue_lines:
    call r13_lines([("granny","잘 왔구나. 여기 앉아서 천천히 이야기하자.",{"expression":"joy"}),("resident_lamplighter","아직 불빛을 살펴보는 중이에요.",{"expression":"angry"}),("resident_teacher","방금 들은 이야기를 다시 확인해 봐야겠어요.",{"expression":"surprise"}),("dad","어디서 본 물건인지 먼저 물어봐야겠다.",{"thought":True})],"qa:b-dialogue")
    jump r13_roam

testcase b_dialogue_stickers:
    $ preferences.text_cps=0
    pause 2.0
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    $ r13_black_card=False
    run Jump("r13_qa_b_dialogue_lines")
    pause 1.0
    assert eval (r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)).endswith("granny_joy.webp"))
    screenshot "b-dialogue-01-normal.png"
    $ renpy.save("qa-b-dialogue-sticker")
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "b-dialogue-02-large.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "b-dialogue-03-touch.png"
    click pos (640,400)
    pause .5
    assert eval (r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)).endswith("resident_lamplighter_angry.webp"))
    screenshot "b-dialogue-04-lamplighter.png"
    click pos (640,400)
    pause .5
    assert eval (r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)).endswith("resident_teacher_surprise_talk.webp"))
    screenshot "b-dialogue-05-teacher.png"
    click pos (640,400)
    pause .5
    assert eval (r13_bdialogue_face("dad","joy") is None)
    screenshot "b-dialogue-06-thought.png"
    run Function(renpy.load,"qa-b-dialogue-sticker")
    pause 1.0
    assert eval (r13_bdialogue_face(r13_packet[0],r13_fullbody_emotion(r13_directed_pose)).endswith("granny_joy.webp"))
    screenshot "b-dialogue-07-restored.png"
