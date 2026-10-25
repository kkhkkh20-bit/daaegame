"""장식 반복 제거의 격리 실제 화면 검사."""
from pathlib import Path
import review_field_clear as field
field.runner.FIXTURE=field.runner.FIXTURE.replace('click "새 생각"','click pos (410,116)')
if __name__=='__main__':
    project=Path(__file__).resolve().parents[1]
    field.runner.capture(project,project/'docs/reviews/field-tape-20261025')
