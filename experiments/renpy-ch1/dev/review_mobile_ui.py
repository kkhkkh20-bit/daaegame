"""실제 연결된 전체 UI를 터치 모드의 격리 게임에서 캡처한다."""
from pathlib import Path
import review_button_fit as runner

if __name__=='__main__':
    project=Path(__file__).resolve().parents[1]
    fixture=(project/'game/qa_tests/current_ui_capture.rpy').read_text()
    fixture=fixture[fixture.index('testcase current_ui_capture:'):]
    fixture=fixture.replace('testcase current_ui_capture:','testcase button_fit_review:\n    $ preferences.fullscreen=True\n    $ r13_touch_ui=lambda: True',1)
    fixture+='''
    run Hide("r13_map")
    run Show("r13_meeting_retry_choice")
    pause .5
    screenshot "09-retry-touch.png"
    click id "r13_meeting_retry_accept"
'''.replace('    click id "r13_meeting_retry_accept"\n','    run Hide("r13_meeting_retry_choice")\n')
    runner.FIXTURE=fixture
    runner.capture(project,project/'docs/reviews/mobile-integration-20261025')
