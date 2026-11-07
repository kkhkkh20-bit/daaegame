# 조사 획득 뒤 실제 확대창. 부분 확대·저장 복원·닫기가 기존 논증 묶음을 건드리지 않는다.
init python:
    def qa_fire_site_remember():
        renpy.test.fire_site_domain=qa_fire_link_domain()
        renpy.test.fire_site_arguments=winter_copy.deepcopy(room13['arguments'])

label qa_fire_site_called:
    call screen r13_pw_picture('V111:E06_FIRE',called=True)
    return

testcase fire_site_picture_restore_and_back:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_proof7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .4
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_lamp'
    click id 'r13_fire_materials'
    click id 'r13_fire_tab_all'
    click id 'r13_fire_pick_E06_FIRE'
    click id 'r13_fire_back'
    run Function(qa_fire_site_remember)
    click id 'r13_fire_site'
    pause .5
    assert screen 'r13_pw_picture'
    assert eval (renpy.get_screen('r13_pw_picture').scope['fire_focus'] is None)
    screenshot 'fire-site-pair.png'
    click id 'r13_fire_site_panel_0'
    pause .5
    assert eval (renpy.get_screen('r13_pw_picture').scope['fire_focus']==0)
    screenshot 'fire-site-lamp.png'
    run Function(renpy.save,'qa-fire-site118')
    click id 'r13_fire_site_pair'
    click id 'r13_fire_site_panel_1'
    assert eval (renpy.get_screen('r13_pw_picture').scope['fire_focus']==1)
    screenshot 'fire-site-door.png'
    run Function(renpy.load,'qa-fire-site118')
    pause until screen 'r13_fire_links' timeout 30
    pause .4
    # 자료 그림은 일시적인 읽기창이다. 불러오면 원래 연결판을 안전하게 이어 간다.
    assert screen 'r13_fire_links'
    assert not screen 'r13_pw_picture'
    assert eval (qa_fire_link_domain()==renpy.test.fire_site_domain and room13['arguments']==renpy.test.fire_site_arguments)
    assert eval (qa_fire_link_row()['observations']==['lamp',None] and room13['arguments'][v111_claim]==['V111:E06_FIRE'])
    $ qa_site_touch_before=r13_touch_ui
    $ qa_site_large_before=persistent.room13_large_text
    $ r13_touch_ui=lambda:True
    $ persistent.room13_large_text=True
    click id 'r13_fire_site'
    pause .5
    assert eval (renpy.get_screen('r13_pw_picture').scope['fire_focus'] is None)
    screenshot 'fire-site-pair-large-touch.png'
    click id 'r13_fire_site_panel_1'
    pause .5
    screenshot 'fire-site-door-large-touch.png'
    click '닫기'
    $ r13_touch_ui=qa_site_touch_before
    $ persistent.room13_large_text=qa_site_large_before
    assert screen 'r13_fire_links'

testcase fire_site_called_returns_to_scene:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    $ qa_site_domain=qa_fire_link_domain()
    run Call('qa_rr_scene','qa_fire_site_called')
    pause until screen 'r13_pw_picture' timeout 30
    click id 'r13_fire_site_panel_1'
    click '닫기'
    pause until screen 'r13_hub' timeout 30
    assert eval (qa_fire_link_domain()==qa_site_domain)
