import sys
from pathlib import Path
sys.path.insert(0,'dev')
import review_button_fit as r
r.FIXTURE='''testcase button_fit_review:
    $ _test.timeout=90
    $ preferences.fullscreen=True
    $ preferences.text_cps=0
    pause 2
    click "설정"
    pause .5
    click "읽기"
    pause .5
    screenshot "15-settings-reading.png"
    click "화면"
    pause .5
    screenshot "16-settings-display.png"
    click "닫기"
    click "처음부터"
    pause until screen "say" timeout 30
    $ r13_black_card=False
    $ r13_thought_active=False
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER","V111:E01"],"qa")
    run Hide("r13_evidence_found")
    run Show("r13_records")
    pause .8
    screenshot "10-records.png"
    run Hide("r13_records")
    run Function(r13_v111_set,"D10_S01_main_completed",True)
    run Jump("r13_v111_hearing10")
    pause 2
    click pos (900,600)
    pause .7
    screenshot "17-meeting-dialogue.png"
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 2
    assert screen "r13_crisis_proof"
    screenshot "13-meeting.png"
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .5
    screenshot "14-meeting-touch.png"
    run Hide("r13_crisis_proof")
    run Show("r13_meeting_retry_choice")
    pause .7
    screenshot "12-meeting-retry.png"
'''
if __name__=='__main__':
    project=Path(__file__).resolve().parents[1]
    r.capture(project,project/'docs/reviews/ui-consistency-20261025/meeting')
