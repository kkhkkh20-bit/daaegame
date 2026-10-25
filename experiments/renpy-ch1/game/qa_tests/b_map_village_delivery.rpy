# 전체13곳 지도: 선택·드래그는 시간을 쓰지 않고 이동은 기존 확정 버튼으로만 한다.
init 999 python:
    def r13_qa_village_zoom(zoom):
        renpy.get_screen("r13_map").scope["village_zoom"]=zoom
        renpy.restart_interaction()

testcase b_map_village_delivery:
    $ _test.timeout=30
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("entry_corrected","lodging"))
    click pos (640,400) until screen "r13_hub" timeout 40
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    pause 1.0
    screenshot "village-detail.png"
    $ r13_qa_village_selected=renpy.get_screen("r13_map").scope["selected"]
    $ r13_qa_village_location=room13["location"]
    $ r13_qa_village_time=room13["period"]
    $ r13_qa_village_scroll=renpy.get_widget("r13_map","r13_map_view").xadjustment.value
    drag pos (1000,500) to pos (750,350) steps 20
    pause .4
    assert eval (renpy.get_screen("r13_map").scope["selected"]==r13_qa_village_selected and room13["location"]==r13_qa_village_location and room13["period"]==r13_qa_village_time)
    assert eval (renpy.get_widget("r13_map","r13_map_view").xadjustment.value!=r13_qa_village_scroll)
    run Function(r13_qa_village_zoom,max(1136.0/1642,506.0/958))
    pause .6
    screenshot "village-overview.png"
    assert eval (set(R13_VILLAGE_B_PLACES)==set(R13_MAP_NODES["village"])-set(R13_V111_MAP_ALIASES))
    assert eval (renpy.get_widget("r13_map","map_name_school") is not None and renpy.get_widget("r13_map","map_name_clinic") is not None and renpy.get_widget("r13_map","map_name_market") is not None)
    click id "map_name_square"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="square" and room13["location"]=="inn")
    click id "map_name_inn"
    assert eval (renpy.get_screen("r13_map").scope["selected"]=="inn" and room13["location"]=="inn")
    click "여관 안"
    pause .5
    assert eval (renpy.get_screen("r13_map").scope["region"]=="inn")
    click "숲·산길"
    pause .5
    assert eval ("passage" not in dict(r13_map_nodes("inn")) and "ancient" not in dict(r13_map_nodes("inn")) and "altar" not in dict(r13_map_nodes("mountain")))
    click "마을"
    pause .5
    $ renpy.set_physical_size((740,416))
    run Function(r13_qa_village_zoom,1.15)
    pause .5
    screenshot "village-mobile.png"
    click id "r13_map_close"
    pause until screen "r13_hub" timeout 30
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    run Function(r13_qa_village_zoom,max(1136.0/1642,506.0/958))
    pause .5
    click id "map_name_square"
    click id "r13_map_travel"
    pause until screen "r13_hub" timeout 30
    assert eval (room13["location"]=="square")
