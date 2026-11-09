# 준비된 사건 상태에서 실제 출력·발언 선택·되묻기·자료 제시를 검사한다. 전체 스토리 연속 플레이가 아니다.
init python:
    QA_HEARING141_PLANS={'early': [{'case': 'gate', 'day': 1, 'key': '함께 들어갈 근거를 고른다', 'correct': ['E02', 'E03'], 'targets': ['MS14_D01_S02_L0013', 'MS14_D01_S03_L0010'], 'kind': 'statement'}, {'case': 'room_letters', 'day': 1, 'key': '두 편지를 나란히 본다', 'correct': ['E01', 'E06'], 'targets': ['NW_D01_S05_V03'], 'kind': 'question'}, {'case': 'measurement', 'day': 3, 'key': '측정 종료와 점검 기록을 대조한다', 'correct': ['E13', 'E11'], 'targets': ['MS14_D03_S03_L0017'], 'kind': 'statement'}, {'case': 'gate_post', 'day': 5, 'key': '밤이 혐의의 근거를 확인한다', 'correct': ['E20', 'E22', 'E23', 'E24'], 'targets': ['MS14_D05_S03_L0009', 'NW_D05_S03_SL01'], 'kind': 'statement'}, {'case': 'warning', 'day': 5, 'key': '두 편지의 초대를 대조한다', 'correct': ['E01', 'E27'], 'targets': ['NW_HEARING141_WARNING_QUESTION'], 'kind': 'question'}], 'late': [{'case': 'room13_hearing', 'day': 10, 'key': '두 상처와 촛대 파손을 대조한다', 'correct': ['E08_CHILD_ACCOUNT', 'E08_TOOL'], 'targets': ['MS14_D10_S02_L0006'], 'kind': 'statement'}, {'case': 'room13_hearing', 'day': 10, 'key': '두 번째 길을 실제 기록으로 보인다', 'correct': ['E09_PASSAGE', 'E08_ROOM'], 'targets': ['MS14_D10_S02_L0021'], 'kind': 'statement'}, {'case': 'room13_hearing', 'day': 10, 'key': '구리선과 수선 출처를 대조한다', 'correct': ['E08_WOUND_WIRE', 'E09_PIN_OWNER'], 'targets': ['MS14_D10_S03_L0002'], 'kind': 'statement'}, {'case': 'room13_hearing', 'day': 10, 'key': '첫 비명 뒤 핀을 다시 채운 때', 'correct': ['E09_PIN_TIME', 'E09_PIN_HANDOVER_TIME'], 'targets': ['MS14_D10_S03_L0018'], 'kind': 'statement'}, {'case': 'room13_hearing', 'day': 10, 'key': '접촉면과 아이의 위치를 대조한다', 'correct': ['E08_CONTACT_ASSEMBLY', 'E08_WOUND_WIRE', 'E08_CHILD_POSITION', 'E08_ROOM_REACH', 'E09_SCARF'], 'targets': ['MS14_D10_S03_L0041'], 'kind': 'statement'}, {'case': 'records_handover', 'day': 10, 'key': '수신인과 가족 전달 권한을 구분한다', 'correct': ['E06_CONTACT', 'E09_MAIL'], 'targets': ['MS14_D10_P01_L0015'], 'kind': 'statement'}, {'case': 'records_handover', 'day': 10, 'key': '반송·필사본·초대 발송을 대조한다', 'correct': ['E01', 'E07', 'E09_MAIL'], 'targets': ['MS14_D10_P01_L0026'], 'kind': 'statement'}], 'end_a': [{'case': 'hypothesis11', 'day': 11, 'key': '초롱과 피코의 하루를 대조한다', 'correct': ['E11', 'E08', 'NW_PIKO_TREMOR'], 'targets': ['NW_H1_Q_01'], 'kind': 'statement'}, {'case': 'hypothesis11', 'day': 11, 'key': '창고에서 잠자는 사람을 짚는다', 'correct': ['NW_KEEPER_DATE'], 'targets': ['NW_H2_Q_01'], 'kind': 'question'}, {'case': 'hypothesis11', 'day': 11, 'key': '요즘 돌이 어디서 오는지 대조한다', 'correct': ['NW_INNER_PRICE', 'NW_MUSOE_DEEP'], 'targets': ['NW_H3_Q_01'], 'kind': 'question'}, {'case': 'hypothesis11', 'day': 11, 'key': '아르카가 없는 아이들과 대조한다', 'correct': ['NW_KKOMI_NOSTONE', 'NW_SICK_BEDS'], 'targets': ['NW_H4_Q_01'], 'kind': 'question'}, {'case': 'hypothesis11', 'day': 11, 'key': '13호 난로의 돌을 내놓는다', 'correct': ['NW_STONE'], 'targets': ['NW_H5_Q_01'], 'kind': 'question'}, {'case': 'soup12', 'day': 12, 'key': '재사용 설명과 개봉 봉인을 대조한다', 'correct': ['E12_FRAGMENT', 'E12_SEAL'], 'targets': ['MS14_D12_S04_L0020'], 'kind': 'statement'}, {'case': 'soup12', 'day': 12, 'key': '파편·봉인·취급 구간을 함께 제시한다', 'correct': ['E12_FRAGMENT', 'E12_SEAL', 'E12_HANDLING'], 'targets': ['MS14_D12_S04_L0040', 'MS14_D12_S04_L0079'], 'kind': 'question'}, {'case': 'soup12', 'day': 12, 'key': '명단과 흰 그릇을 대조한다', 'correct': ['NW_TRANSFER_LIST', 'NW_WHITE_BOWLS'], 'targets': ['NW_SL_Q_01'], 'kind': 'statement'}], 'end_b': [{'case': 'blanket13', 'day': 13, 'key': '아내가 봤다는 담요의 시점을 확인한다', 'correct': ['E13_MENDING'], 'targets': ['MS14_D13_S03_L0017'], 'kind': 'statement'}, {'case': 'blanket13', 'day': 13, 'key': '촌장이 어젯밤 있던 곳을 확인한다', 'correct': ['NW_HALL_WINDOW'], 'targets': ['NW_BQ_03'], 'kind': 'statement'}, {'case': 'piko13_stolen', 'day': 13, 'key': '장부의 두 배를 실룩에게 보인다', 'correct': ['E16'], 'targets': ['NW_RO_03'], 'kind': 'statement'}, {'case': 'piko13_stolen', 'day': 13, 'key': '피코가 막혀야 했던 까닭을 보인다', 'correct': ['NW_PIKO_PAINTING'], 'targets': ['NW_RL_03'], 'kind': 'statement'}, {'case': 'piko13_attempt', 'day': 13, 'key': '인수하지 않은 돌의 약속 값을 보인다', 'correct': ['NW_LA_OFFER'], 'targets': ['NW_HEARING141_REIN_ATTEMPT_CLAIM13'], 'kind': 'statement'}, {'case': 'piko13_attempt', 'day': 13, 'key': '피코가 막혀야 했던 까닭을 보인다', 'correct': ['NW_PIKO_PAINTING'], 'targets': ['NW_RL_03'], 'kind': 'statement'}, {'case': 'altar14', 'day': 14, 'key': '희생의 숫자와 장부를 대조한다', 'correct': ['NW_NEOUL_LEDGER'], 'targets': ['NW_A1_Q02'], 'kind': 'statement'}, {'case': 'altar14', 'day': 14, 'key': '아르카가 부른다는 말과 옛 기록을 대조한다', 'correct': ['NW_TABLET_A', 'NW_TABLET_B'], 'targets': ['NW_A2_Q01'], 'kind': 'statement'}, {'case': 'altar14', 'day': 14, 'key': '쇠가 언제 붙었는지 보인다', 'correct': ['NW_IRON_MARK'], 'targets': ['NW_A3_Q01'], 'kind': 'statement'}, {'case': 'altar14', 'day': 14, 'key': '맨 처음 이름을 짚는다', 'correct': ['NW_NAMES', 'NW_NEOUL_LEDGER'], 'targets': ['NW_A4_Q01'], 'kind': 'statement'}]}

    def qa_hearing141_scope():
        screen=renpy.get_screen("r13_proof_workspace")
        return screen.scope if screen else {}

    def qa_hearing141_packet(target):
        if target in R13_V111['records']:
            rows=r13_v111_lines([target])
            return [p for p in rows if p[2].get('line_id')==target]
        for where in ('before','after','blocks'):
            for rows in R13_NW_TEXT[where].values():
                for row in rows:
                    if row.get('id')==target and R13_NW_WHEN[row.get('when','always')]():
                        return [r13_nw_added_line(row)]
        return []

    def qa_hearing141_start(group):
        store.qa_hearing141_plan=QA_HEARING141_PLANS[group]
        store.qa_hearing141_index=0
        store.qa_hearing141_passed=[]
        store.qa_hearing141_case=None
        persistent.room13_large_text=False
        persistent.room13_text_small=False

    def qa_hearing141_prepare():
        item=store.qa_hearing141_plan[store.qa_hearing141_index]
        if store.qa_hearing141_case!=item['case']:
            room=winter_copy.deepcopy(store.room13)
            values=room['v111']['values']
            for k in list(values):
                if k.startswith('hearing:'):values.pop(k,None)
            room['arguments']={};store.room13=room
            store.r13_pw_views={}
            store.qa_hearing141_case=item['case']
        r13_v111_set('day',item['day'])
        r13_v111_set('lamp_bound2',item['case']=='piko13_attempt')
        r13_v111_set('letter_inquiry_mode138',True)
        r13_v111_set('letter_tail_observed',True)
        r13_edit(location='workshop')
        store.qa_hearing141_item=item
        r13_grant(['V111:'+k for k in item['correct']],'검수 준비')
        packets=[]
        for target in item['targets']:
            packets=qa_hearing141_packet(target)
            if packets:break
        if not packets:raise Exception('검수 대상의 실제 표시 줄 없음: '+item['key'])
        store.qa_hearing141_target=packets[0][2].get('line_id') or packets[0][2].get('source_id')
        store.qa_hearing141_packets=packets
        if (r13_pw_context(item['key']) or {}).get('mode')=='compare':
            claim='v111:'+item['key']
            store.r13_pw_views[claim]=dict(view='pair',pair=tuple('V111:'+k for k in item['correct']),quote_open=False)

    def qa_hearing141_selection():
        r13_pw_set_arguments(store.v111_claim,['V111:'+k for k in store.qa_hearing141_item['correct']])
        renpy.restart_interaction()

    def qa_hearing141_domain():
        return winter_copy.deepcopy((room13['day'],room13['period'],room13['evidence'],room13['v111']['values']))

    def qa_hearing141_validate():
        screen=qa_hearing141_scope();item=store.qa_hearing141_item
        assert screen['hearing_row']['target']==store.qa_hearing141_target,(item,screen['hearing_row'])
        assert screen['hearing_kind']==item['kind']
        assert screen['hearing_rows'] and any(r['key']==item['key'] for r in screen['hearing_rows'])
        assert r13_case_hearing_spec(item['key'])

label qa_hearing141_sequence:
    if qa_hearing141_index>=len(qa_hearing141_plan):
        $ qa_hearing141_finished=True
        call screen r13_hub
        return
    $ qa_hearing141_prepare()
    call r13_lines(qa_hearing141_packets,'qa:hearing141:actual_line')
    call r13_v111_proof(qa_hearing141_item['key'],qa_hearing141_item['correct'],'qa_hearing141_solved','qa_hearing141_failed')
    jump expression _return

label qa_hearing141_solved:
    $ qa_hearing141_passed.append(qa_hearing141_item['key'])
    $ qa_hearing141_index+=1
    jump qa_hearing141_sequence

label qa_hearing141_failed:
    $ renpy.error('기존 기본 자료 조합이 실패함: '+qa_hearing141_item['key'])

testcase hearing141_early:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_start,"early")
    run Jump("qa_hearing141_sequence")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==0)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-early-00.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==1)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_pair"
    pause .3
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==2)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==3)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==4)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-early-04.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_pair"
    pause .3
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (len(qa_hearing141_passed)==5 and qa_hearing141_finished)

testcase hearing141_late:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_start,"late")
    run Jump("qa_hearing141_sequence")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==0)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-late-00.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==1)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==2)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==3)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==4)
    run Function(qa_hearing141_validate)
    assert eval (qa_hearing141_scope()['hearing_page']==1 and len(qa_hearing141_scope()['hearing_visible'])==1)
    screenshot 'hearing141-late-five-pc.png'
    run Function(qa_hearing141_touch,True)
    pause .4
    screenshot 'hearing141-late-five-touch.png'
    run Function(qa_hearing141_save_load)
    click pos (900,600) until screen 'r13_proof_workspace' timeout 40
    pause .4
    assert eval (qa_hearing141_scope()['hearing_target']=='MS14_D10_S03_L0041')
    run Function(qa_hearing141_touch,False)
    pause .4
    click id 'r13_hearing_prev'
    pause .3
    assert eval (qa_hearing141_scope()['hearing_page']==0 and len(qa_hearing141_scope()['hearing_visible'])==4)
    click id 'r13_hearing_next'
    pause .3

    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==5)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==6)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-late-06.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (len(qa_hearing141_passed)==7 and qa_hearing141_finished)

testcase hearing141_end_a:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_start,"end_a")
    run Jump("qa_hearing141_sequence")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==0)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-end_a-00.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==1)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==2)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==3)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==4)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==5)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==6)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==7)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-end_a-07.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (len(qa_hearing141_passed)==8 and qa_hearing141_finished)

testcase hearing141_end_b:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_start,"end_b")
    run Jump("qa_hearing141_sequence")
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==0)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-end_b-00.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==1)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==2)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==3)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==4)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==5)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==6)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==7)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==8)
    run Function(qa_hearing141_validate)
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .4
    assert eval (qa_hearing141_index==9)
    run Function(qa_hearing141_validate)
    screenshot "hearing141-end_b-09.png"
    click id "r13_pw_single"
    pause .2
    $ qa_hearing141_before=qa_hearing141_domain()
    click id "r13_pw_press"
    pause .3
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    pause .3
    assert eval (qa_hearing141_domain()==qa_hearing141_before)
    click id "r13_pw_submit"
    pause .2
    run Function(qa_hearing141_selection)
    pause .2
    click id "r13_pw_submit"
    pause .3
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (len(qa_hearing141_passed)==10 and qa_hearing141_finished)

init python:
    def qa_hearing141_touch(enable):
        if enable:
            renpy.test.qa_hearing141_ui=(tuple(config.variants),persistent.room13_large_text)
            config.variants=['touch','pc',None]
            persistent.room13_large_text=True
        else:
            variants,large=renpy.test.qa_hearing141_ui
            config.variants=list(variants)
            persistent.room13_large_text=large
        renpy.restart_interaction()

    def qa_hearing141_fire_prepare(empty=False):
        qa_fire_deduction7()
        r13_v111_set('FIRE_EVACUATED',empty)
        r13_grant(['V111:E06_EMPTY' if empty else 'V111:E06_RESCUE','V111:E07_NUBI'],'검수 준비')
        store.r13_pw_views={}
    def qa_hearing141_save_load():
        renpy.save('hearing141')
        renpy.load('hearing141')


testcase hearing141_fire_bridge:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_fire_prepare,False)
    run Call('qa_rr_scene','r13_v111_bori_witness_heard7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .4
    $ qa141_fire_before=qa_hearing141_domain()
    click id 'r13_fire_words'
    pause until screen 'r13_proof_workspace' timeout 20
    pause .4
    assert eval (qa_hearing141_scope()['hearing_only'] and qa_hearing141_scope()['hearing_row']['target']=='NW_D07_OR02')
    assert eval (not r13_case_hearing_quote('NW_HEARING141_FIRE_RESCUE_TARGET'))
    click id 'r13_pw_press'
    click pos (900,600) until screen 'r13_proof_workspace' timeout 40
    pause .4
    assert eval (qa_hearing141_domain()==qa141_fire_before)
    screenshot 'hearing141-fire-origin-words.png'
    run Function(qa_hearing141_save_load)
    click pos (900,600) until screen 'r13_proof_workspace' timeout 40
    pause .4
    assert eval (qa_hearing141_scope()['hearing_only'] and qa_hearing141_domain()==qa141_fire_before)
    click id 'r13_pw_submit'
    pause until screen 'r13_fire_links' timeout 20
    assert eval (qa_hearing141_domain()==qa141_fire_before and qa_fire_link_row()['view']=='board')
    pause .4
    click id 'r13_fire_slot_0'
    pause .3
    click id 'r13_fire_choice_lamp'
    assert eval (qa_fire_link_row()['observations'][0]=='lamp')


testcase hearing141_fire_responsibility_empty:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_fire_prepare,True)
    run Function(r13_v111_set,'meeting:fire','win')
    run Function(r13_v111_set,'NUBI_admitted_setting_fire',True)
    run Function(r13_edit,location='school')
    run Call('qa_rr_scene','r13_v111_responsibility7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .4
    click id 'r13_fire_words'
    pause until screen 'r13_proof_workspace' timeout 20
    pause .4
    assert eval (qa_hearing141_scope()['hearing_row']['target']=='NW_HEARING141_FIRE_EMPTY_TARGET')
    assert eval (not r13_case_hearing_quote('NW_HEARING141_FIRE_RESCUE_TARGET'))
    screenshot 'hearing141-fire-empty.png'
    click id 'r13_pw_press'
    click pos (900,600) until screen 'r13_proof_workspace' timeout 40
    pause .4
    click id 'r13_pw_submit'
    pause until screen 'r13_fire_links' timeout 20
    assert eval (not r13_v111_value('tries:fire'))


testcase hearing141_fire_responsibility_rescue:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_hearing141_fire_prepare,False)
    run Function(r13_v111_set,'meeting:fire','win')
    run Function(r13_v111_set,'NUBI_admitted_setting_fire',True)
    run Function(r13_edit,location='school')
    run Call('qa_rr_scene','r13_v111_responsibility7')
    click pos (900,600) until screen 'r13_fire_links' timeout 60
    pause .4
    click id 'r13_fire_words'
    pause until screen 'r13_proof_workspace' timeout 20
    pause .4
    assert eval (qa_hearing141_scope()['hearing_row']['target']=='NW_HEARING141_FIRE_RESCUE_TARGET')
    assert eval (not r13_case_hearing_quote('NW_HEARING141_FIRE_EMPTY_TARGET'))
    screenshot 'hearing141-fire-rescue.png'
    click id 'r13_pw_submit'
    pause until screen 'r13_fire_links' timeout 20
    assert eval (not r13_v111_value('tries:fire'))
