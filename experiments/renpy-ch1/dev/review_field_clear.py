"""조사 화면의 실제 사물·인물·상단 도구 조작을 격리 검수한다."""
from pathlib import Path
import review_button_fit as runner
runner.FIXTURE='''init 999 python:
    def r13_review_low_object():
        z=r13_field_zoom();offset=r13_world_offset();choices=[]
        actors=r13_stage_people(False)
        for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
            if not r13_object_visible(spec):continue
            x,y,w,h=r13_object_target_rect(key,spec)
            for fx,fy in ((.5,.8),(.2,.8),(.8,.8),(.5,.5)):
                wx,wy=x+w*fx,y+h*fy
                sx,sy=(wx-offset)*z,wy*z
                if not (90<sx<1190 and 260<sy<704):continue
                if any(ax<=wx<=ax+aw and ay<=wy<=ay+ah for a in actors for ax,ay,aw,ah in [a["rect"]]):continue
                choices.append((sy,key,(int(sx),int(sy))))
        assert choices,"화면에서 조사할 사물을 찾지 못했습니다."
        _,store.r13_review_object,store.r13_review_point=max(choices)
        print("실제 사물 조사:",store.r13_review_object,store.r13_review_point)

testcase button_fit_review:
    $ _test.timeout=40
    $ preferences.fullscreen=True
    $ preferences.text_cps=0
    $ r13_touch_ui=lambda: True
    pause 2
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=1,period=0,location="gate",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    pause 1
    screenshot "gate-clear-touch.png"
    click "기록"
    pause until screen "r13_records" timeout 20
    run Hide("r13_records")
    click "새 생각"
    assert eval r13_goal_open
    click "접기"
    assert eval (not r13_goal_open)
    run Function(r13_review_low_object)
    click pos r13_review_point
    pause .7
    assert not screen "r13_hub"
    screenshot "object-open.png"
    run Hide("r13_interaction")
    run Hide("r13_inspection")
    run Hide("say")
    run Jump("r13_roam")
    pause until screen "r13_hub" timeout 30
    click "돌목"
    pause .7
    assert not screen "r13_hub"
    screenshot "person-open.png"
'''
if __name__=='__main__':
    project=Path(__file__).resolve().parents[1]
    runner.capture(project,project/'docs/reviews/field-clear-20261025')
