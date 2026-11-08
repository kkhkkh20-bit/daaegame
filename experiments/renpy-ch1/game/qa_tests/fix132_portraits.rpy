# 완주 검수에서 지적한 일반/작업 자세와 조연 실제 대사만 준비해 확인한다.
init python:
    def qa_fix132_people(day,scene,people):
        r13_v111_set('day',day)
        r13_edit(day=day,period=0)
        store.room13['v111']['scene']=scene
        r13_v111_arrive(people)
        r13_meeting_direct_end()
        store.r13_meeting_active=False
        store.r13_thought_active=False

    def qa_fix132_frame(person,pose='neutral'):
        profile=r13_dialogue_source_profile(person,pose,840)
        frame=profile['frames'].get(pose) or profile['frames']['neutral']
        return frame['file']


testcase fix132_chorong_work_and_everyday:
    run Function(renpy.set_physical_size,(1280,720))
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call('r13_qa_v111_place','square',0)
    pause until screen 'r13_hub' timeout 30
    run Function(qa_fix132_people,2,'MS14_D02_S01',['daram','resident_lamplighter'])
    $ qa_fix132_evidence=tuple(room13['evidence'])
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D02_S01_L0011']),'v111:square2:MS14_D02_S01_L0010')
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('pose')=='lamp_work132') timeout 30
    assert eval (r13_directed_pose=='lamp_work132' and r13_current_pose=='lamp_work132')
    assert eval ('gaze116/resident_lamplighter/' in qa_fix132_frame('resident_lamplighter','lamp_work132'))
    pause .6
    screenshot 'fix132-chorong-rope-work.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    run Call('r13_qa_v111_place','forest',0)
    pause until screen 'r13_hub' timeout 30
    run Function(qa_fix132_people,2,'MS14_D02_S01',['daram','resident_lamplighter'])
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D02_S01_L0041']),'qa:fix132-forest')
    pause until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D02_S01_L0041') timeout 30
    assert eval (r13_packet[2].get('pose')!='lamp_work132' and '/chorong20261108/' in qa_fix132_frame('resident_lamplighter'))
    pause .6
    screenshot 'fix132-chorong-forest-calm.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    assert eval (tuple(room13['evidence'])==qa_fix132_evidence)


testcase fix132_support_portraits:
    run Function(renpy.set_physical_size,(1280,720))
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call('r13_qa_v111_place','store',0)
    pause until screen 'r13_hub' timeout 30
    run Function(qa_fix132_people,3,'MS14_D03_S04',['daram','resident_madam'])
    $ qa_fix132_evidence=tuple(room13['evidence'])
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D03_S04_L0022']),'qa:fix132-madam')
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='resident_madam') timeout 30
    assert eval ('/madam20261108/' in qa_fix132_frame('resident_madam'))
    pause .6
    screenshot 'fix132-madam.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    run Call('r13_qa_v111_place','clinic',0)
    pause until screen 'r13_hub' timeout 30
    run Function(qa_fix132_people,5,'MS14_D05_S02',['daram','ms14_clinician'])
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D05_S02_L0030']),'qa:fix132-medic')
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='ms14_clinician') timeout 30
    assert eval ('/support132-20261108/ms14_clinician/' in qa_fix132_frame('ms14_clinician'))
    pause .6
    screenshot 'fix132-medic.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    run Call('r13_qa_v111_place','school',0)
    pause until screen 'r13_hub' timeout 30
    run Function(qa_fix132_people,7,'MS14_D07_S02',['daram','kid_nubi1'])
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D07_S02_L0020']),'qa:fix132-child')
    click pos (900,600) until eval (r13_packet and r13_packet[0]=='kid_nubi1') timeout 30
    assert eval ('/support132-20261108/kid_nubi1/' in qa_fix132_frame('kid_nubi1'))
    pause .6
    screenshot 'fix132-child.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    assert eval (tuple(room13['evidence'])==qa_fix132_evidence)
