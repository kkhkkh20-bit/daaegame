init python:
    def qa_forest_shot(name):
        import os,json
        out="/tmp/room13-qa/forest"
        if not os.path.isdir(out):os.makedirs(out)
        renpy.screenshot(os.path.join(out,name+".png"))
        acts=[dict(person=a.get("person"),pose=a.get("pose"),x=a.get("x"),y=a.get("y"),xpos=a.get("xpos"),ypos=a.get("ypos"),h=a.get("height"),rect=a.get("rect")) for a in r13_stage_people()]
        open(os.path.join(out,name+".json"),"w").write(json.dumps(dict(acts=acts,cam=getattr(store,"r13_world_x",None),layout={k:v for k,v in (R13_WORLD_LAYOUTS.get("forest") or {}).items() if k in ("width","positions","poses","pinned","critical","slots")},crit=r13_stage_critical("forest",R13_WORLD_LAYOUTS.get("forest"))),default=str,ensure_ascii=False,indent=1))

testcase zz_forest_box:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(lambda: store.room13["flags"].append("v111:applied:option:sleep1:0") if isinstance(store.room13["flags"],list) else store.room13["flags"].add("v111:applied:option:sleep1:0"))
    run Function(r13_v111_set,"day",2)
    run Function(r13_edit,day=2,location="forest",period=0)
    run Jump("r13_v111_box_path")
    click pos (900,600) until screen "r13_hub" timeout 90
    pause 1.0
    run Function(qa_forest_shot,"box_left")
