"""현재 UI 전체의 실제 렌더 검토. 저장과 이야기 진행은 격리 복사본에만 적용."""
from pathlib import Path
import review_button_fit as runner
project=Path(__file__).resolve().parents[1]
source=(project/'game/qa_tests/current_ui_capture.rpy').read_text()
runner.FIXTURE=source[source.index('testcase current_ui_capture:'):].replace('testcase current_ui_capture:','testcase button_fit_review:\n    $ preferences.fullscreen=True',1).replace('$ _test.timeout=30','$ _test.timeout=90')
runner.FIXTURE=runner.FIXTURE.replace('    run Call("r13_qa_roam"','    $ review_story_state=winter_copy.deepcopy(room13)\n    run Call("r13_qa_roam"',1)
runner.FIXTURE+='''
    click "마을"
    pause .8
    screenshot "09-map-village.png"
    run Hide("r13_map")
    run Show("r13_records")
    pause .8
    screenshot "10-records.png"
    run Hide("r13_records")
    $ room13=winter_copy.deepcopy(review_story_state)
    run Function(r13_qa_fork_a_fixture)
    run Show("r13_fork_screen")
    pause .8
    screenshot "11-forks.png"
    run Hide("r13_fork_screen")
'''
if __name__=='__main__':
    runner.capture(project,project/'docs/reviews/ui-consistency-20261025')
