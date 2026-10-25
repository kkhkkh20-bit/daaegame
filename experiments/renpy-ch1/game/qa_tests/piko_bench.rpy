init python:
    def qa_k1_setup():
        qa_nw_day14('prevented')
        r13_edit(day=2,period=1,location='dining')
        r13_v111_set('day',2)
        for key in ('piko_sacks2','piko_cloth2'):
            r13_v111_set(key,True)
        for key in ('piko_bench_seen2','piko_bench_clean2'):
            r13_v111_set(key,None)
        r13_v111_arrive(['nabi','daram'])
label qa_k1_episode:
    call r13_scene(R13_PLACES['dining'][1],'식당','calm')
    jump r13_v111_afternoon

testcase piko_bench_preparation:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_k1_setup)
    run Jump('qa_k1_episode')
    click pos (900,600) until eval (room13['v111'].get('gate')=='afternoon2') timeout 30
    pause 0.8
    assert eval (not any(o.get('index')==2 for o in r13_v111_binding()['options']))
    run Show('qa_hidden_base_return',value=('object','table'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('piko_bench_seen2') timeout 30
    pause 0.8
    assert eval (not any(o.get('index')==2 for o in r13_v111_binding()['options']))
    run Show('qa_hidden_base_return',value=('object','table'))
    pause 0.3
    click 'QA 행동'
    click pos (900,600) until eval r13_v111_value('piko_bench_clean2') timeout 30
    pause 0.8
    assert eval any(o.get('index')==2 for o in r13_v111_binding()['options'])
