# Native runner only; never entered by an authored failure branch.
default r13_qa_retry_returns=[]
default r13_qa_retry_unchanged=False

label r13_qa_retry_contract:
    $ r13_qa_retry_returns=[]
    $ r13_qa_retry_before=__import__('copy').deepcopy(room13)
    call r13_meeting_retry_prompt
    $ r13_qa_retry_returns.append(_return)
    call r13_meeting_retry_prompt
    $ r13_qa_retry_returns.append(_return)
    $ r13_qa_retry_unchanged=(room13==r13_qa_retry_before)
    jump r13_roam

init python:
    def r13_qa_fork_a_fixture(meeting='fire',grand=False,all_seen=False):
        qa_fork_fixture()
        persistent.r13_fork_seen={}
        persistent.r13_fork_endings={}
        store.r13_fork_win_prior={}
        store.room13['v111']['fork_run']=3
        store.room13['day']=7 if meeting=='fire' else 12
        if meeting=='soup':
            for key in ('room13','records','hypothesis'):
                r13_v111_set('meeting:'+key,'win')
        r13_v111_set('meeting:'+meeting,'win' if grand else 'lose')
        r13_fork_record(meeting,'win' if grand else 'lose')
        if grand:r13_v111_set('grand:'+meeting,True)
        if all_seen:
            seen=dict(persistent.r13_fork_seen)
            for outcome in ('win','partial','lose'):
                seen[(meeting,outcome)]=dict(png=None,run=1)
            persistent.r13_fork_seen=seen

testcase b_meeting_retry_ui:
    $ preferences.text_cps=0
    pause 2.0
    click '처음부터'
    pause until screen 'say' timeout 30
    run Call('r13_qa_roam',dict(day=7,period=0,location='square',life_poc=True),('lodging',))
    click pos (640,400) until screen 'r13_hub' timeout 40
    run Jump('r13_qa_retry_contract')
    pause until screen 'r13_meeting_retry_choice' timeout 10
    pause .5
    screenshot 'meeting-retry-pc.png'
    click id 'r13_meeting_retry_accept'
    pause .5
    assert eval (r13_qa_retry_returns==['accept'])
    assert eval (room13==r13_qa_retry_before)
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot 'meeting-retry-touch.png'
    click id 'r13_meeting_retry_again'
    pause .5
    assert eval (r13_qa_retry_returns==['accept','retry'])
    assert eval r13_qa_retry_unchanged
    assert not screen 'r13_meeting_retry_choice'
    $ r13_touch_ui=lambda: False

testcase b_fork_a_grand:
    $ preferences.text_cps=0
    pause 2.0
    click '처음부터'
    pause until screen 'say' timeout 30
    assert eval (r13_v111_active())
    $ r13_black_card=False
    run Function(r13_v111_set,"day",7)
    run Call("r13_qa_v111_place","square",0)
    pause until screen "r13_hub" timeout 40
    run Function(r13_qa_fork_a_fixture)
    run Show('r13_fork_screen')
    pause .5
    assert eval (next(c for c in r13_fork_columns() if c['key']=='fire')['rows'][-1]['count']==3)
    screenshot 'fork-a-fire-unseen.png'
    run Hide('r13_fork_screen')
    run Function(r13_qa_fork_a_fixture,'fire',True)
    run Show('r13_fork_screen')
    pause .5
    assert eval (('fire','grand') in persistent.r13_fork_seen and ('fire','win') not in persistent.r13_fork_seen)
    screenshot 'fork-a-fire-seen.png'
    run Hide('r13_fork_screen')
    run Function(r13_qa_fork_a_fixture,'soup',True,True)
    $ r13_touch_ui=lambda: True
    run Show('r13_fork_screen')
    pause .5
    screenshot 'fork-a-soup-all-seen-touch.png'
    assert eval (len(next(c for c in r13_fork_columns() if c['key']=='soup')['rows'])==4)
    run Hide('r13_fork_screen')
    $ r13_touch_ui=lambda: False
