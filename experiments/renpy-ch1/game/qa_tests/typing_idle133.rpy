# 실제 1일차 원문만 재생하는 표시 시험. 사건 자료·정답·진행 값은 쓰지 않는다.
init python:
    def qa_typing133_widget():
        return renpy.get_displayable("say","what") if renpy.get_screen("say") else None

    def qa_typing133_text():
        screen=renpy.get_screen("say")
        return screen.scope.get("what","") if screen else ""

    def qa_typing133_domain():
        return winter_copy.deepcopy((store.room13["evidence"],store.room13.get("v111",{}).get("values",{})))

    def qa_typing133_audio_probe():
        current=renpy.music.get_playing(channel="typing")
        if current and "assets/type.wav" in current:
            renpy.test.typing133_audio_heard=True

    def qa_typing133_prepare(cps=24):
        preferences.text_cps=cps
        preferences.afm_enable=False
        persistent.room13_typing_sound=True
        store.typing_allowed=True
        store.r13_meeting_active=False
        store.r13_thought_active=False
        renpy.test.typing133_audio_heard=False
        renpy.test.typing133_before=qa_typing133_domain()

screen qa_typing133_audio_probe():
    timer .01 repeat True action Function(qa_typing133_audio_probe,_update_screens=False)

label qa_typing133_existing_lines:
    hide screen r13_hub
    # 첫 기록은 긴 일반 대사판, 다음 기록은 {w=.4}가 있는 돌목의 실제 말이다.
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0007','MS14_D01_S02_L0015']),'qa:typing133:existing')
    jump r13_qa_v111_field

testcase typing133_reveal_click_wait_idle:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_typing133_prepare,24)
    run Show('qa_typing133_audio_probe')
    run Call('qa_typing133_existing_lines')
    pause until eval (qa_typing133_widget() is not None and qa_typing133_widget().slow and r13_typing_timer_needed()) timeout 20
    pause until eval (renpy.test.typing133_audio_heard and qa_typing133_widget().r13_revealed>0) timeout 5
    $ qa_typing133_first=qa_typing133_text()
    assert eval (r13_page_i==0 and qa_typing133_first==r13_line_markup(r13_pages[0]))
    # 첫 클릭은 현재 글자만 완성한다. 같은 원문·같은 페이지에 그대로 머문다.
    click pos (900,600)
    pause until eval (not qa_typing133_widget().slow and not r13_typing_timer_needed()) timeout 5
    assert eval (r13_page_i==0 and qa_typing133_text()==qa_typing133_first)
    pause .2
    assert eval (renpy.music.get_playing(channel='typing') is None)
    screenshot 'typing133-first-click-completed-idle.png'
    # 두 번째 클릭만 다음 두 줄로 넘어간다.
    click pos (900,600)
    pause until eval (r13_page_i==1) timeout 10
    assert eval (qa_typing133_text()!=qa_typing133_first)
    click pos (900,600) until eval (r13_packet[2].get('line_id')=='MS14_D01_S02_L0015') timeout 30
    assert eval ('{w=.4}' in r13_packet[1])
    # {w} 앞뒤 조각은 자동으로 이어지되 완성된 페이지는 다음 클릭을 기다린다.
    $ qa_typing133_wait_page=r13_page_i
    pause until eval (qa_typing133_widget() is not None and not qa_typing133_widget().slow and not r13_typing_timer_needed()) timeout 10
    assert eval (r13_page_i==qa_typing133_wait_page and qa_typing133_text()==r13_line_markup(r13_pages[r13_page_i]))
    pause .2
    assert eval (renpy.music.get_playing(channel='typing') is None and qa_typing133_domain()==renpy.test.typing133_before)
    screenshot 'typing133-wait-fragment-completed-idle.png'
    run Hide('qa_typing133_audio_probe')

testcase typing133_options_and_saved_text:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_typing133_prepare,24)
    run Call('qa_typing133_existing_lines')
    pause until eval (qa_typing133_widget() is not None and qa_typing133_widget().slow and r13_typing_timer_needed()) timeout 20
    $ renpy.test.typing133_saved_text=qa_typing133_text()
    run Function(renpy.save,'qa-typing133-unfinished')
    # 음향 설정은 저장과 별개다. 미완성 글자를 불러와도 무음은 유지된다.
    run Function(r13_set_option,'room13_typing_sound',False)
    run Function(renpy.load,'qa-typing133-unfinished')
    pause until screen 'say' timeout 30
    assert eval (qa_typing133_text()==renpy.test.typing133_saved_text and not r13_typing_timer_needed() and not persistent.room13_typing_sound)
    pause .2
    assert eval (renpy.music.get_playing(channel='typing') is None)
    screenshot 'typing133-unfinished-load-muted.png'
    # 같은 say에 설정을 열고 닫은 뒤 음향을 켜도 지나간 글자를 큐에 쌓지 않는다.
    run Show('pause_menu')
    pause until screen 'pause_menu' timeout 10
    assert eval (not r13_typing_timer_needed())
    run Hide('pause_menu')
    run Function(r13_set_option,'room13_typing_sound',True)
    click pos (900,600)
    pause until eval (qa_typing133_widget() is not None and not qa_typing133_widget().slow and not r13_typing_timer_needed()) timeout 10
    $ renpy.test.typing133_complete_text=qa_typing133_text()
    $ renpy.test.typing133_complete_page=r13_page_i
    run Function(renpy.save,'qa-typing133-completed')
    run Preference('text speed',0)
    click pos (900,600)
    run Function(renpy.load,'qa-typing133-completed')
    pause until screen 'say' timeout 30
    assert eval (qa_typing133_text()==renpy.test.typing133_complete_text and r13_page_i==renpy.test.typing133_complete_page and not r13_typing_timer_needed())
    pause .2
    assert eval (renpy.music.get_playing(channel='typing') is None)
    screenshot 'typing133-completed-load-instant-idle.png'
    # 즉시 표시는 음향 폴링을 만들지 않는다. 건너뛰기가 끝나면 보통 속도가 다시 시작된다.
    $ renpy.config.skipping='slow'
    click pos (900,600) until screen 'r13_hub' timeout 30
    run Function(renpy.stop_skipping)
    run Function(qa_typing133_prepare,24)
    run Call('qa_typing133_existing_lines')
    pause until eval (qa_typing133_widget() is not None and qa_typing133_widget().slow and r13_typing_timer_needed()) timeout 20
    assert eval (qa_typing133_domain()==renpy.test.typing133_before)
    screenshot 'typing133-normal-reveal-after-skip.png'
