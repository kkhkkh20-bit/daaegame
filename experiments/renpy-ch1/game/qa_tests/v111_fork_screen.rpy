init python:
    def qa_fork_fixture():
        # Deterministic fixture, isolated by the QA runner's save directory.
        persistent.r13_fork_seen={}
        persistent.r13_fork_endings={}
        store.r13_fork_win_prior={}
        r13_v111_set('grand:fire',False)
        r13_v111_set('grand:soup',False)
        for meeting in ('gate','lamp','gate_post','fire','room13','records','hypothesis','soup','blanket','piko','altar'):
            r13_v111_set('meeting:'+meeting,None)
        r13_nw_meeting_end('gate','win')
        r13_nw_meeting_end('lamp','win')
        r13_nw_meeting_end('gate_post','win')  # 0.20.5: the post meeting has only win and lose
        r13_nw_meeting_end('fire','win')
        r13_fork_record('lamp','lose')
        r13_fork_record('fire','partial')
        r13_fork_ending('frozen')
        r13_v111_set('day',10)
        store.r13_meeting_active=False
        store.r13_meeting_claim=None

    def qa_fork_locked_count():
        # 0.20.x: unseen results are one lock per meeting with a count ("다른 결과 N").
        return sum(row.get('count',0) for col in r13_fork_columns() for row in col['rows'] if row['kind']=='locked')

testcase v111_fork_screen:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_fork_fixture)
    run Show('r13_records')
    pause 0.5
    click '갈림길'
    pause 0.5
    assert screen 'r13_fork_screen'
    assert eval (qa_fork_locked_count()==9)  # fire의 미확인 grand도 이름 없이 개수에 포함한다.
    assert eval ([col['key'] for col in r13_fork_columns() if col.get('fate')]==['lamp','gate_post','fire'])
    assert eval (sum(col['key'] is None for col in r13_fork_columns())==1)
    assert eval (len(r13_fork_columns())==8 and r13_fork_current()==6)
    screenshot "fork_a.png"
    click '닫기'
    assert screen 'r13_records'
    assert not screen 'r13_fork_screen'
