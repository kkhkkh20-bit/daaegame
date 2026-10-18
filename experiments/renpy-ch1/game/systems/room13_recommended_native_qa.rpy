# Explicit disposable candidate test state, not production approval.
label r13_recommended_native_qa_start:
    call screen r13_recommended_status("QA 전용 새 이야기입니다. 현재 추천 진행을 새 테스트 상태로 바꾸고, 두 미검증 최종 단계를 시험할 수 있게 합니다. 기본 플레이와 승인 상태는 바꾸지 않습니다. 결과는 배포 승인이 아닙니다.")
    menu:
        "별도 QA 캠페인을 새로 시작할까요?"
        "QA 전용 상태로 새로 시작한다":
            pass
        "현재 진행으로 돌아간다":
            jump r13_recommended_hub
    call r13_rec_stage_exit_label
    call r13_recommended_ep23_admin_boot
    $ r13_rec_stage_memory = {}
    $ r13_recommended = r13_rec_opening_state()
    $ room13['day'] = r13_recommended['day']
    $ r13_recommended['qa_fixture'] = 'native_geometry_probe_v1'
    $ r13_recommended['qa_native_gates'] = {'piko':True,'e3':True}
    $ room13['campaign_id'] = 'room13_recommended_qa_v1'
    $ r13_rec_admin_harness = False
    call r13_recommended_carriage_opening
    jump r13_recommended_hub

label r13_rec_stage_exit_label:
    $ r13_rec_stage_exit()
    return
