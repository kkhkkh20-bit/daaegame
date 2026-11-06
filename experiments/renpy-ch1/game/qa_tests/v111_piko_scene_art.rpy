# 사망 확인 컷의 유지·종료와 생존 분리를 실제 원래 라벨로 검사한다.
init python:
    def qa_piko_scene_start(saved=False):
        r13_flag('v111:applied:option:sleep2:0')
        r13_v111_set('day',3)
        r13_v111_set('lamp_bound2',False)
        r13_v111_set('piko_sheltered',saved)
        r13_v111_set('piko_alive',True)
        r13_edit(day=3,period=0,location='dining' if saved else 'square')
        store.place=R13_PLACES[store.room13['location']][0]

testcase v111_piko_scene_holds_until_body_talk_and_clears:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_scene_start)
    run Jump('r13_v111_day3')
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S01_L0002') timeout 60
    assert eval (r13_ep_cut_current=='piko-death3' and 'r13_ep_cut' in renpy.get_showing_tags())
    pause .6
    screenshot 'piko-body-discovery.png'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S01_L0012') timeout 60
    assert eval (r13_ep_cut_current=='piko-death3' and qa_nw_seen('등 쪽으로 돌아누워서요'))
    pause .8
    screenshot 'piko-body-child-question.png'
    # 현재 say 체크포인트 뒤의 시험용 변수도 로드 때 되돌아가므로 비교값은 격리 QA의 persistent에 둔다.
    run SetField(persistent,'qa_piko_cut_saved',dict(cut=r13_ep_cut_current,visible='r13_ep_cut' in renpy.get_showing_tags(),line_id=r13_packet[2].get('line_id'),alive=r13_v111_value('piko_alive')))
    $ renpy.save('qa-piko-scene-cut')
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S01_L0020') timeout 45
    assert eval (r13_ep_cut_current=='piko-death3')
    run Function(renpy.load,'qa-piko-scene-cut')
    pause 1.0
    assert eval (persistent.qa_piko_cut_saved==dict(cut=r13_ep_cut_current,visible='r13_ep_cut' in renpy.get_showing_tags(),line_id=r13_packet[2].get('line_id'),alive=r13_v111_value('piko_alive')))
    assert eval (r13_ep_cut_current=='piko-death3' and 'r13_ep_cut' in renpy.get_showing_tags() and r13_packet[2].get('line_id')=='MS14_D03_S01_L0012')
    screenshot 'piko-body-child-question-restored.png'
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S01_L0020') timeout 45
    assert eval (r13_ep_cut_current=='piko-death3')
    click pos (900,600) until screen 'r13_piko_scene' timeout 90
    assert eval (r13_v111_value('piko_alive') is False and r13_v111_owned('E09'))
    click id 'r13_piko_leave'
    click pos (900,600) until screen 'r13_hub' timeout 90
    assert eval (room13['v111']['gate']=='lamp_inspect3' and r13_v111_value('piko_alive') is False)
    assert eval ('r13_ep_cut' not in renpy.get_showing_tags() and not r13_ep_cut_current)
    assert eval (qa_nw_seen('피코 두고 가') and qa_nw_seen('멀리 안 가'))

testcase v111_piko_scene_saved_has_no_death_cut:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko_scene_start,True)
    run Jump('r13_v111_day3')
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S01_L0023') timeout 60
    assert eval ('r13_ep_cut' not in renpy.get_showing_tags() and not r13_ep_cut_current and r13_v111_value('piko_alive') is True)
    click pos (900,600) until screen 'r13_hub' timeout 90
    assert eval (room13['v111']['gate']=='piko_clean' and r13_v111_value('piko_alive') is True and not r13_v111_tense_context())
    assert eval (not qa_nw_seen('등 쪽으로 돌아누워서요') and not qa_nw_seen('피코 두고 가'))
    screenshot 'piko-saved-no-death-cut.png'
