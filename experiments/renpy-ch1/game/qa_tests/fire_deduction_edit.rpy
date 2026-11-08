# 시작 상태만 준비하고 관찰 연결·기존 제출·재조사·구 저장 경계를 실제 화면으로 확인한다.
init python:
    def qa_fire_deduction7():
        qa_resident789(7)
        r13_edit(location='laundry')
        r13_grant(['V111:E06_FIRE','V111:E06_RESCUE'],'qa')
        r13_v111_scene('MS14_D07_S01')
        r13_v111_arrive(['resident_nubi','resident_bori'])

    def qa_fire_link_row():
        return r13_fire_links_state(v111_claim)

    def qa_fire_link_remember_domain():
        # 비교 기준은 저장을 불러와도 변하지 않는 검수 모듈에 둔다.
        renpy.test.fire_link_qa_domain=qa_fire_link_domain()

    def qa_fire_link_domain():
        return winter_copy.deepcopy((room13['evidence'],room13['v111']['values']))


testcase fire7_hypothesis_rebut_and_submit:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'KKOMI_ALIVE',False)
    run Call('qa_rr_scene','r13_v111_bori_witness_heard7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (r13_v111_value('fire_lamp_defense_heard') is True and not r13_v111_value('NUBI_admitted_setting_fire'))
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_lamp'
    click id 'r13_fire_slot_1'
    click id 'r13_fire_choice_door'
    click id 'r13_fire_slot_2'
    click id 'r13_fire_choice_wood_owner'
    assert eval (not room13['arguments'][v111_claim])
    click id 'r13_fire_submit'
    assert eval (qa_fire_link_row()['view']=='sources' and not room13['arguments'][v111_claim])
    click id 'r13_fire_sources_submit'
    # 서류 판정 전에 누비가 실제로 답한다. 질문·연결을 바꿔도 아직 주장이 아니다.
    pause until screen 'say' timeout 30
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_nubi') timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_owned('E07_NUBI') and not room13['arguments'][v111_claim])
    screenshot 'fire7_hypothesis.png'
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (qa_fire_link_row()['view']=='board' and not qa_fire_link_row()['notice'] and not r13_v111_value('proof_given:'+R13_FIRE_LINK_FIRST))
    click id 'r13_fire_slot_2'
    click id 'r13_fire_choice_lamp_keeper'
    click id 'r13_fire_submit'
    click id 'r13_fire_sources_submit'
    pause until screen 'say' timeout 30
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_nubi') timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_owned('E07_NUBI') and not room13['arguments'][v111_claim])
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    click id 'r13_fire_slot_1'
    click id 'r13_fire_choice_witness'
    click id 'r13_fire_slot_2'
    click id 'r13_fire_choice_door'
    click id 'r13_fire_submit'
    click id 'r13_fire_sources_submit'
    pause until screen 'say' timeout 30
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_nubi') timeout 60
    assert eval (not r13_v111_value('tries:fire') and not room13['arguments'][v111_claim])
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (not r13_v111_value('fire_origin_hypothesis') and not r13_v111_owned('E07_NUBI') and not qa_fire_link_row()['notice'])
    click id 'r13_fire_slot_1'
    click id 'r13_fire_choice_door'
    screenshot 'fire7_evidence.png'
    click id 'r13_fire_submit'
    click id 'r13_fire_sources_submit'
    click pos (900,600) until eval (r13_packet and '문 앞의 탄 자국과 기름 냄새' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (not r13_v111_owned('E07_NUBI') and not r13_v111_value('NUBI_admitted_setting_fire'))
    screenshot 'fire7_checked.png'
    click pos (900,600) until screen 'r13_fire_recheck' timeout 60
    pause .5
    assert eval (renpy.get_screen('r13_fire_recheck').scope['options']==('trace',) and not r13_v111_owned('E07_NUBI'))
    screenshot 'fire7_admission_recheck_trace.png'
    click id 'r13_fire_recheck_ask'
    click pos (900,600) until eval (r13_packet and '가져간다고 안 했어요' in r13_packet[1].replace('\n',' ')) timeout 90
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E07_NUBI') and r13_v111_value('NUBI_admitted_setting_fire') is True and r13_v111_value('NUBI_intent_to_kill')=='unproven')
    assert eval (qa_nw_seen('이름이 꼬미였어요') and qa_nw_seen('꼬미는 창고에서 나오지 못했습니다'))


testcase fire7_investigate_retry:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_proof7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_lamp'
    click id 'r13_fire_slot_1'
    click id 'r13_fire_choice_door'
    click id 'r13_fire_slot_2'
    click id 'r13_fire_choice_door'
    click id 'r13_fire_investigate'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_value('NUBI_admitted_setting_fire'))
    click '보리'
    # 단일 진행 질문은 담당자를 누르면 바로 주고받기로 이어진다.
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (not room13['arguments'][v111_claim] and qa_fire_link_row()['observations']==['lamp','door'])
    click id 'r13_fire_submit'
    click id 'r13_fire_sources_change'
    click id 'r13_fire_tab_all'
    click id 'r13_fire_pick_E06_FIRE'
    click id 'r13_fire_pick_E06_RESCUE'
    click id 'r13_fire_back'
    click id 'r13_fire_sources_submit'
    click pos (900,600) until eval (r13_v111_value('tries:fire')==1) timeout 60
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (r13_v111_value('tries:fire')==1 and not r13_v111_owned('E07_NUBI'))
    screenshot 'fire7_retry.png'
    click id 'r13_fire_submit'
    click id 'r13_fire_sources_change'
    click id 'r13_fire_tab_all'
    click id 'r13_fire_pick_E06_FIRE'
    click id 'r13_fire_back'
    click id 'r13_fire_sources_submit'
    click pos (900,600) until eval (r13_packet and '문 앞의 탄 자국과 기름 냄새' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_value('tries:fire')==1 and not r13_v111_owned('E07_NUBI'))


testcase fire7_old_success_entry:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Function(r13_v111_set,'proof_given:'+R13_FIRE_LINK_FIRST,['V111:E06_FIRE'])
    run Function(r13_v111_set,'fire_laundry_exchange_heard7',True)
    run Call('qa_rr_scene','r13_v111_nubi_first_question7')
    click pos (900,600) until eval (r13_packet and '문 앞의 탄 자국과 기름 냄새' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_value('fire_lamp_defense_heard') is True and not r13_v111_owned('E07_NUBI'))
    click pos (900,600) until screen 'r13_fire_recheck' timeout 60
    pause .5
    assert eval (renpy.get_screen('r13_fire_recheck').scope['options']==('trace','pot') and not r13_v111_value('tries:fire'))
    click id 'r13_fire_recheck_pot'
    run Function(renpy.take_screenshot)
    run Function(renpy.save,'qa-fire-recheck123')
    click id 'r13_fire_recheck_trace'
    run Function(renpy.load,'qa-fire-recheck123')
    pause until screen 'r13_fire_recheck' timeout 30
    pause .5
    assert eval (renpy.get_screen('r13_fire_recheck').scope['focus']=='pot' and not r13_v111_owned('E07_NUBI') and not r13_v111_value('tries:fire'))
    screenshot 'fire7_admission_recheck_pot.png'
    click id 'r13_fire_recheck_ask'
    click pos (900,600) until eval (r13_packet and '가져간다고 안 했어요' in r13_packet[1].replace('\n',' ')) timeout 90
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E07_NUBI') and r13_v111_value('NUBI_intent_to_kill')=='unproven')


# 증거를 가졌다는 이유만으로 옛 자백 라벨에 들어가 성공을 만들 수 없다.
testcase fire7_unproven_direct_entry_cannot_admit:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Function(r13_v111_set,'fire_lamp_defense_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_admission7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    assert eval (not r13_v111_value('NUBI_admitted_setting_fire') and not r13_v111_owned('E07_NUBI'))
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_value('proof_given:'+R13_FIRE_LINK_FIRST) and not room13['arguments'][v111_claim])


# 관찰을 고른 출처를 직접 읽고 확인한다. 같은 기록을 목록에서 다시 찾지 않는다.
testcase fire7_sources_no_reselect_and_restore:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_proof7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_door'
    click id 'r13_fire_slot_1'
    click id 'r13_fire_choice_witness'
    click id 'r13_fire_slot_2'
    click id 'r13_fire_choice_door'
    assert eval (not room13['arguments'][v111_claim] and not qa_fire_link_row()['materials'])
    click id 'r13_fire_submit'
    pause .4
    assert eval (qa_fire_link_row()['view']=='sources' and not room13['arguments'][v111_claim])
    assert eval (renpy.get_screen('r13_fire_links').scope['chosen']==['V111:E06_FIRE'])
    screenshot 'fire7_sources_before_confirm_pc.png'
    click id 'r13_fire_source_read_E06_FIRE'
    pause .4
    assert eval (qa_fire_link_row()['view']=='read' and qa_fire_link_row()['origin'] is True)
    click id 'r13_fire_back'
    assert eval (qa_fire_link_row()['view']=='sources' and not room13['arguments'][v111_claim])
    run Function(qa_fire_link_remember_domain)
    run Function(renpy.take_screenshot)
    run Function(renpy.save,'qa-fire-sources119')
    click id 'r13_fire_back'
    run Function(renpy.load,'qa-fire-sources119')
    pause until screen 'r13_fire_links' timeout 30
    pause .5
    assert eval (qa_fire_link_row()['view']=='sources' and qa_fire_link_row()['observations']==['door','witness'])
    assert eval (not room13['arguments'][v111_claim] and qa_fire_link_domain()==renpy.test.fire_link_qa_domain)
    $ qa_fire_source_touch_before=r13_touch_ui
    $ qa_fire_source_large_before=persistent.room13_large_text
    $ r13_touch_ui=lambda:True
    $ persistent.room13_large_text=True
    run Function(renpy.set_physical_size,(844,390))
    pause .6
    screenshot 'fire7_sources_before_confirm_touch_large.png'
    $ r13_touch_ui=qa_fire_source_touch_before
    $ persistent.room13_large_text=qa_fire_source_large_before
    run Function(renpy.set_physical_size,(1280,720))
    click id 'r13_fire_sources_submit'
    click pos (900,600) until eval (r13_packet and '문 앞의 탄 자국과 기름 냄새' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (not r13_v111_value('tries:fire') and not r13_v111_owned('E07_NUBI'))


# 실제 호출 스택에서 중간 연결·자료를 저장하고 복원한다. 화면 크기 변경으로 휴대폰 UI도 확인한다.
testcase fire7_links_saved_and_touch:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_fire_deduction7)
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Call('qa_rr_scene','r13_v111_nubi_proof7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .5
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_lamp'
    run Function(qa_fire_link_remember_domain)
    run Function(renpy.take_screenshot)
    run Function(renpy.save,'qa-fire-links117')
    pause .3
    screenshot 'fire7_partial_connection_pc.png'
    click id 'r13_fire_slot_0'
    click id 'r13_fire_choice_door'
    assert eval (qa_fire_link_row()['observations'][0]=='door')
    run Function(renpy.load,'qa-fire-links117')
    pause until screen 'r13_fire_links' timeout 30
    pause .5
    assert eval (qa_fire_link_row()['observations']==['lamp',None] and qa_fire_link_row()['materials']==[] and not room13['arguments'][v111_claim])
    assert eval (qa_fire_link_domain()==renpy.test.fire_link_qa_domain and not r13_v111_value('fire_origin_hypothesis'))
    run Function(renpy.set_physical_size,(844,390))
    $ persistent.room13_large_text=True
    pause .6
    screenshot 'fire7_partial_connection_touch_large.png'
    click id 'r13_fire_words'
    pause .4
    screenshot 'fire7_words_touch_large.png'
    click id 'r13_fire_back'
    assert eval (qa_fire_link_domain()==renpy.test.fire_link_qa_domain and qa_fire_link_row()['observations']==['lamp',None])
    $ persistent.room13_large_text=False
    run Function(renpy.set_physical_size,(1280,720))
