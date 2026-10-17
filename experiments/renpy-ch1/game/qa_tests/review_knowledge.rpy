# Supplemental 0.19.16 UI regression: the night remembers the daytime promise.
# Fixture-based label test; normal presentation is covered by qa_review_knowledge.py.
testcase review_knowledge01916:
    $ preferences.text_cps=0
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=0,location="room13",life_poc=True,evidence=["E01","M01"]),("night1_seen","mother_letter_promised","mother_recognized"),(),0)
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_life_first_night")
    click pos (640,600) until eval (renpy.get_screen("say") and "초롱 아저씨가 엄마 봉투를 맡고 있대" in renpy.get_screen("say").scope.get("what","")) timeout 40
    pause 0.5
    screenshot "review_night_promise.png"
    click pos (640,600) until eval (renpy.get_screen("say") and "3일에 다시 만나기로 했어" in renpy.get_screen("say").scope.get("what","")) timeout 20
    pause 0.5
    screenshot "review_night_date.png"
    assert eval (r13_mother_knowledge()["pending"] and "E18" not in room13["evidence"])

testcase review_poc_promise01916:
    $ preferences.text_cps=0
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=2,location="room13",life_poc=True,evidence=["E01","M01"]),("mother_letter_promised","mother_recognized"),(),0)
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_poc_night_review")
    click pos (640,600) until eval (renpy.get_screen("say") and "초롱 아저씨가 엄마 봉투" in renpy.get_screen("say").scope.get("what","")) timeout 30
    pause 0.5
    screenshot "review_day2_promise.png"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_has("poc:night:2") and "E18" not in room13["evidence"])
    run Function(r13_edit,day=3,period=2)
    run Call("r13_poc_night_review")
    click pos (640,600) until eval (renpy.get_screen("say") and "초롱 아저씨가 엄마 봉투" in renpy.get_screen("say").scope.get("what","")) timeout 30
    pause 0.5
    screenshot "review_day3_promise.png"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_has("poc:night:3") and "E18" not in room13["evidence"])
