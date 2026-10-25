"""스티커 조사 화면의 좌우 이동·사물·대화·도구 실제 클릭 검사."""
from pathlib import Path
import review_field_clear as field
field.runner.FIXTURE=field.runner.FIXTURE.replace('    click "기록"','    click pos (48,276)\n    pause 1\n    assert screen "r13_hub"\n    screenshot "pan-left.png"\n    click pos (1232,276)\n    pause 1\n    assert screen "r13_hub"\n    click "기록"',1)
if __name__=='__main__':
    project=Path(__file__).resolve().parents[1]
    field.runner.capture(project,project/'docs/reviews/field-sticker-20261025')
