# 상태를 준비한 질문 목록 화면 시험. 하루 진행·진상·자료 획득은 바꾸지 않는다.
default qa_side_mobile_ready=True
default qa_side_mobile_pick=0

init python:
    def qa_side_mobile_entries():
        titles=("그동안 어떻게 지내셨습니까?","편지를 받은 날 저녁에 어디 계셨습니까?",
                "두 사람의 이름을 같은 명단에서 확인해 주시겠습니까?",
                "아이가 기다리는 동안 무엇을 하고 계셨습니까?",
                "광장의 등이 꺼져 있는 것을 처음 본 때가 언제입니까?",
                "그 종이는 어디서 받으셨습니까?")
        return r13_mark_new_questions([(title,SetVariable("qa_side_mobile_pick",i+1),i%3==1) for i,title in enumerate(titles*2)])

    def qa_side_mobile_text_fits():
        layout=r13_side_question_layout()
        for caption in ("자료 제시","기록","더보기","돌아가기"):
            size=renpy.render(Text(caption,font=R13_UI_BOLD_FONT,size=layout["tool_size"]),4096,200,0,0).get_size()
            if size[0]>layout["tool_width"]-8 or size[1]>72:return False
        return True

    def qa_side_mobile_pages_fit():
        entries=qa_side_mobile_entries()
        pages=r13_side_question_pages(entries)
        if [entry for page in pages for entry,height in page]!=entries:return False
        bottom=r13_notebook_topic_y()-(96 if r13_touch_ui() else 60)-12
        return all(R13_SIDE_QUESTION_TOP+78+sum(height for entry,height in page)+8*(len(page)-1)<=bottom for page in pages)

screen qa_side_mobile_topics():
    modal True
    zorder 40
    use r13_side_question_list("granny","joy",qa_side_mobile_entries(),qa_side_mobile_ready,Hide("qa_side_mobile_topics"))
    use r13_notebook_topic_tools(qa_side_mobile_ready,"granny",SetVariable("qa_side_mobile_pick",99))

testcase side_question_mobile:
    $ qa_side_mobile_touch_original=r13_touch_ui
    $ qa_side_mobile_large_original=persistent.room13_large_text
    $ r13_touch_ui=lambda:False
    $ persistent.room13_large_text=False
    $ preferences.text_cps=0
    run Function(renpy.set_physical_size,(1280,720))
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call("r13_qa_v111_place","inn",0)
    pause until screen "r13_hub" timeout 40
    run Hide("r13_hub")
    run Show("qa_side_mobile_topics")
    pause .7
    assert eval (r13_side_question_layout()["left"]==572)
    screenshot "questions-pc-preserved.png"
    $ r13_touch_ui=lambda:True
    $ persistent.room13_large_text=False
    run Function(renpy.set_physical_size,(844,390))
    run Function(renpy.restart_interaction)
    pause .7
    assert eval (r13_side_question_layout()["body_size"]==32 and qa_side_mobile_text_fits() and qa_side_mobile_pages_fit())
    screenshot "questions-mobile-normal.png"
    click id "r13_topics_next"
    pause .3
    $ qa_side_mobile_expected=r13_side_question_pages(qa_side_mobile_entries())[1][0][0][1].value
    keysym "K_1"
    assert eval (qa_side_mobile_pick==qa_side_mobile_expected)
    screenshot "questions-mobile-page2.png"
    click id "r13_notebook_자료 제시"
    assert eval (qa_side_mobile_pick==99)
    $ qa_side_mobile_ready=False
    $ qa_side_mobile_pick=0
    run Function(renpy.restart_interaction)
    click pos (690,594)
    assert eval (qa_side_mobile_pick==0)
    $ qa_side_mobile_ready=True
    $ persistent.room13_large_text=True
    run Function(renpy.restart_interaction)
    pause .7
    assert eval (r13_side_question_layout()["body_size"]==34 and qa_side_mobile_text_fits() and qa_side_mobile_pages_fit())
    screenshot "questions-mobile-large.png"
    click id "r13_topics_previous"
    pause .3
    click id "r13_notebook_기록"
    assert screen "r13_records"
    run Hide("r13_records")
    click id "r13_notebook_더보기"
    assert screen "r13_more_tools"
    run Hide("r13_more_tools")
    click id "r13_notebook_돌아가기"
    assert not screen "qa_side_mobile_topics"
    $ r13_touch_ui=qa_side_mobile_touch_original
    $ persistent.room13_large_text=qa_side_mobile_large_original
    run Function(renpy.set_physical_size,(1280,720))
