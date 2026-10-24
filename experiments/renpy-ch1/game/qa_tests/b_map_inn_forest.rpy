# 2026-10-24 B 지도(여관 안·숲·산길) 화면 시험: 기본/공개 뒤, 마우스 올림 떠오름, 이동 한 번, 휴대폰 크기.
# 숨은 장소는 기존 판정(r13_map_nodes)만 따르는지, 숨은 동안 버튼·이름표가 아예 없는지 본다.
init 999 python:
    def r13_qa_bmap_center(region,key):
        sx,sy,sw,sh=r13_bmap_target(region,key)["sticker"]
        return (sx+sw//2,sy+sh//2)

    def r13_qa_bmap_widget(key):
        return renpy.get_widget("r13_map",key)

    def r13_qa_bmap_scope():
        return renpy.get_screen("r13_map").scope

    def r13_qa_bmap_record(tag):
        import os, json as qa_json
        path=renpy.config.basedir+"/qa_result.txt"
        log={}
        try:
            log=qa_json.loads(open(path).read()) if os.path.exists(path) else {}
        except Exception:
            log={}
        rows={}
        for region in r13_bmap_regions():
            rows[region]=dict(places=r13_bmap_places(region),covers=[k for k,c in r13_bmap_covers(region)],
                targets={k:r13_bmap_target(region,k) for k,s in r13_bmap_places(region)})
        log[tag]=dict(location=store.room13["location"],touch=r13_touch_ui(),regions=rows)
        open(path,"w").write(qa_json.dumps(log,ensure_ascii=False,default=list))

    def r13_qa_bmap_hidden_absent(region):
        """숨은 장소는 버튼·가림판 이외의 어떤 것도 없어야 한다."""
        shown=set(k for k,s in r13_bmap_places(region))
        for key in R13_BMAP[region]["places"]:
            if key in shown:continue
            for prefix in ("map_room_","map_building_","map_locked_"):
                if renpy.get_widget("r13_map",prefix+key) is not None:
                    return False
        return True

testcase b_map_inn_forest:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    click "지도" until screen "r13_map" timeout 30
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    assert eval (r13_qa_bmap_scope()["region"]=="inn")
    pause 0.5
    # 여관 기본: 숨은 통로·옛 시설은 없음.
    assert eval ("passage" not in dict(r13_bmap_places("inn")) and "ancient" not in dict(r13_bmap_places("inn")))
    assert eval (r13_qa_bmap_widget("map_room_passage") is None and r13_qa_bmap_widget("map_room_inn") is not None)
    assert eval r13_qa_bmap_hidden_absent("inn")
    $ r13_qa_bmap_record("pc_inn_default")
    screenshot "bmap-pc-inn-default.png"
    # 마우스 올림: 식당이 떠오른다(선택은 바뀌지 않음).
    move pos r13_qa_bmap_center("inn","dining")
    pause 0.6
    assert eval (r13_qa_bmap_scope()["map_hover"]=="dining" and r13_qa_bmap_scope()["selected"]=="inn")
    screenshot "bmap-pc-inn-hover-dining.png"
    # 이동 한 번: 고르고 이동 버튼으로 확정.
    click id "map_room_dining"
    pause 0.4
    assert eval (r13_qa_bmap_scope()["selected"]=="dining" and room13["location"]=="inn")
    screenshot "bmap-pc-inn-selected-dining.png"
    click "이곳으로 이동"
    pause until screen "r13_hub" timeout 30
    assert eval (room13["location"]=="dining")
    pause 1.0
    click "지도" until screen "r13_map" timeout 30
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    assert eval (r13_qa_bmap_scope()["region"]=="inn" and r13_qa_bmap_scope()["selected"]=="dining")
    # 숲·산길 기본: 폐온실·제단은 가림판만, 보호시설은 공개된 곳이지만 지금은 못 감.
    click "숲·산길"
    pause 0.7
    assert eval (r13_qa_bmap_scope()["region"]=="mountain")
    assert eval (sorted(k for k,c in r13_bmap_covers("mountain"))==["altar","greenhouse"])
    assert eval (r13_qa_bmap_widget("map_building_greenhouse") is None and r13_qa_bmap_widget("map_building_altar") is None)
    assert eval (r13_qa_bmap_widget("map_locked_greenhouse") is None and r13_qa_bmap_widget("map_locked_altar") is None)
    assert eval r13_qa_bmap_hidden_absent("mountain")
    assert eval (dict(r13_bmap_places("mountain")).get("facility")=="locked" and dict(r13_bmap_places("mountain")).get("forest")=="open")
    $ r13_qa_bmap_record("pc_mountain_default")
    screenshot "bmap-pc-mountain-default.png"
    move pos r13_qa_bmap_center("mountain","forest")
    pause 0.6
    assert eval (r13_qa_bmap_scope()["map_hover"]=="forest")
    screenshot "bmap-pc-mountain-hover-forest.png"
    click id "map_locked_facility"
    pause 0.4
    assert eval (r13_qa_bmap_scope()["map_notice"]=="보호시설 · 지금은 이곳으로 갈 수 없습니다." and r13_qa_bmap_scope()["selected"]!="facility")
    screenshot "bmap-pc-mountain-locked-notice.png"
    # 탭 전환·닫기 동작은 그대로.
    click "마을"
    pause 0.5
    assert eval (r13_qa_bmap_scope()["region"]=="village")
    keysym "K_ESCAPE"
    pause 0.6
    assert screen "r13_hub"
    assert eval (room13["location"]=="dining")
    $ r13_qa_note("b_map_inn_forest: inn/mountain default, hover lift, one travel, locked notice")

testcase b_map_revealed:
    pause 2.0
    click "처음부터"
    pause 3.0
    # 숨은 통로: 기존 판정 그대로 (passage_open + secret_route_unlocked).
    run Call("r13_qa_roam",dict(day=4,period=0,location="room13",life_poc=True,passage_open=True,secret_route_unlocked=True,case_state="occurred"),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    run Show("r13_map")
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    assert eval (r13_qa_bmap_scope()["region"]=="inn")
    assert eval (r13_map_discovered("passage") and "passage" in dict(r13_bmap_places("inn")))
    assert eval (r13_qa_bmap_widget("map_room_passage") is not None)
    pause 0.5
    $ r13_qa_bmap_record("pc_inn_revealed")
    screenshot "bmap-pc-inn-revealed.png"
    move pos r13_qa_bmap_center("inn","passage")
    pause 0.6
    assert eval (r13_qa_bmap_scope()["map_hover"]=="passage")
    screenshot "bmap-pc-inn-revealed-hover-passage.png"
    run Hide("r13_map")
    pause 0.3
    # 옛 시설(지하): 기존 조건(passage_open + ancient_found)이 맞을 때만. 그림이 없어 이름표만 남긴다.
    assert eval ("ancient" not in dict(r13_bmap_places("inn")))
    $ room13["flags"]=list(room13["flags"])+["ancient_found"]
    run Show("r13_map")
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    assert eval (dict(r13_bmap_places("inn")).get("ancient")=="open" and r13_bmap_target("inn","ancient")["sticker"] is None)
    assert eval (r13_qa_bmap_widget("map_room_ancient") is not None)
    click id "map_room_ancient"
    pause 0.4
    assert eval (r13_qa_bmap_scope()["selected"]=="ancient")
    $ r13_qa_bmap_record("pc_inn_ancient")
    screenshot "bmap-pc-inn-ancient-label-only.png"
    run Hide("r13_map")
    $ r13_qa_note("b_map_revealed: passage drawn only after the existing gate; ancient label-only")

testcase b_map_revealed_forest:
    pause 2.0
    click "처음부터"
    pause 3.0
    # 폐온실·제단: 2주차(E19) + 결말 시작(finale_started), 제단에 서 있을 때.
    run Call("r13_qa_roam",dict(day=11,period=0,location="altar",life_poc=True,finale_started=True,week2_started=True,case_state="occurred"),("entry_corrected","lodging","E19"))
    click pos (640,600) until screen "r13_hub" timeout 60
    run Show("r13_map")
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    assert eval (r13_qa_bmap_scope()["region"]=="mountain")
    assert eval (r13_map_discovered("greenhouse") and r13_map_discovered("altar"))
    assert eval ("greenhouse" in dict(r13_bmap_places("mountain")) and "altar" in dict(r13_bmap_places("mountain")))
    assert eval (r13_bmap_covers("mountain")==[])
    pause 0.5
    $ r13_qa_bmap_record("pc_mountain_revealed")
    screenshot "bmap-pc-mountain-revealed.png"
    move pos r13_qa_bmap_center("mountain","greenhouse")
    pause 0.6
    assert eval (r13_qa_bmap_scope()["map_hover"]=="greenhouse")
    screenshot "bmap-pc-mountain-revealed-hover-greenhouse.png"
    run Hide("r13_map")
    $ r13_qa_note("b_map_revealed_forest: greenhouse/altar drawn only after the existing gates")

testcase b_map_touch:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    $ r13_touch_ui=lambda: True
    run Show("r13_map")
    pause until eval r13_qa_bmap_scope()["ready"] timeout 10
    pause 0.5
    # 휴대폰 360px 높이에서 44 CSS px = 가상 88px. 스티커 누를 자리가 그보다 커야 한다.
    assert eval all(min(r13_bmap_target("inn",k)["sticker"][2:])>=88 for k in R13_BMAP["inn"]["places"] if R13_BMAP["inn"]["places"][k]["art"])
    assert eval all(min(r13_bmap_target("mountain",k)["sticker"][2:])>=88 for k in R13_BMAP["mountain"]["places"])
    assert eval (r13_map_control_height()==88)
    $ r13_qa_bmap_record("touch_inn_default")
    screenshot "bmap-touch-inn-default.png"
    click id "map_room_kitchen"
    pause 0.4
    assert eval (r13_qa_bmap_scope()["selected"]=="kitchen" and r13_qa_bmap_scope()["map_hover"] is None)
    screenshot "bmap-touch-inn-selected-kitchen.png"
    click "숲·산길"
    pause 0.7
    $ r13_qa_bmap_record("touch_mountain_default")
    screenshot "bmap-touch-mountain-default.png"
    click id "map_building_forest"
    pause 0.4
    assert eval (r13_qa_bmap_scope()["selected"]=="forest")
    screenshot "bmap-touch-mountain-selected-forest.png"
    $ r13_touch_ui=lambda: False
    run Hide("r13_map")
    $ r13_qa_note("b_map_touch: phone-size map targets and footer")
