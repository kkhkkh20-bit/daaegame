init python:
    def qa_gate_spots_apply():
        lay=R13_WORLD_LAYOUTS["gate"]
        lay["positions"]=dict(karo=[140,672,230],guard=[1228,640,255],daram=[1040,714,205],resident_badook=[1800,694,250])
        lay["pinned"]=["karo","guard","daram","resident_badook"]
        lay["critical"]=list(lay["critical"])+[[880,420,310,180]]
        _old=store.r13_visible_people
        store.r13_visible_people=lambda:[p for p in _old() if p not in ("resident_bori","resident_nero","resident_siluk")]
        R13_STAGE_CACHE.clear()
    def qa_gate_cam(x):
        store.r13_world_cameras=dict(store.r13_world_cameras);store.r13_world_cameras["gate"]=x
        R13_STAGE_CACHE.clear();renpy.restart_interaction()

testcase gate_spots:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    run Function(qa_gate_cam,0)
    pause 1.0
    screenshot "before-left.png"
    run Function(qa_gate_cam,640)
    pause 1.0
    screenshot "before-right.png"
    run Function(qa_gate_spots_apply)
    run Function(qa_gate_cam,0)
    pause 1.2
    screenshot "after-left.png"
    run Function(qa_gate_cam,640)
    pause 1.2
    screenshot "after-right.png"
