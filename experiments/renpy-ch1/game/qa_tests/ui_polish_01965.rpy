# Native presentation fixture, not a natural campaign replay. No production hooks.
default r13_qa_ui065_done = False

label r13_qa_ui065_lines:
    hide screen r13_hub
    $ r13_qa_ui065_done=False
    $ preferences.text_cps=34
    $ preferences.afm_enable=False
    $ persistent.room13_large_text=False
    $ r13_meeting_active=False
    $ typing_allowed=True
    call r13_lines([(None,"창밖에 쌓인 눈 위로 작은 발자국이 이어져 있었다. 아직 확인하지 못한 이야기는 서두르지 않고 하나씩 살펴보기로 했다. 책상 위에는 오래된 편지와 새로 적은 기록이 가지런히 놓여 있었다. 문을 열기 전에 지금까지 들은 이야기를 다시 생각했다.")],"qa:ui065")
    $ r13_qa_ui065_done=True
    jump r13_field

testcase ui_polish_01965:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01"]),("entry_corrected","lodging"))
    click pos (640,600) until screen "r13_hub" timeout 40
    # Same-location old-save mode is migrated without changing story state.
    $ r13_field_location=room13["location"]
    $ r13_field_view="scene"
    run Function(r13_field_sync)
    assert eval (r13_field_view=="people")
    run Call("r13_qa_ui065_lines")
    pause until screen "say" timeout 20
    pause 0.1
    assert eval (preferences.text_cps==34 and len(r13_pages)>1 and r13_page_i==0)
    assert eval (all(len(page.split("\n"))<=2 for page in r13_pages))
    assert eval (_r13_say_size() in (28,31) and r13_control_y()-16-_r13_say_top(r13_pages[0]) in (104,112))
    # First dismiss aborts the current reveal, not its page. Second advances.
    click pos (640,560)
    pause 0.1
    assert eval (r13_page_i==0 and not r13_qa_ui065_done)
    screenshot "ui065-first-click-complete.png"
    click pos (640,560)
    pause 0.1
    assert eval (r13_page_i==1 and not r13_qa_ui065_done)
    screenshot "ui065-second-click-next-page.png"
    click pos (640,560) until eval (r13_qa_ui065_done) timeout 40
    pause until screen "r13_hub" timeout 20
    $ persistent.room13_option_tab="reading"
    run Show("pause_menu")
    pause 0.3
    assert screen "pause_menu"
    click "느리게"
    pause 0.2
    assert eval (preferences.text_cps==24 and renpy.get_screen("pause_menu").scope["typing_preview"].signature[0]==24)
    screenshot "ui065-settings-preview-slow.png"
    click "다시 보기"
    pause 0.2
    assert eval (renpy.get_screen("pause_menu").scope["typing_preview"].started is not None)
    click "즉시"
    pause 0.2
    assert eval (preferences.text_cps==0 and renpy.get_screen("pause_menu").scope["typing_preview"].signature[0]==0)
    screenshot "ui065-settings-preview-instant.png"
    click "보통"
    run Hide("pause_menu")
    click "지도 · 이동" until screen "r13_map" timeout 20
    pause 0.5
    assert eval (room13["location"]=="inn")
    screenshot "ui065-map-idle-outline-footer.png"
    click "현장으로"
    pause until screen "r13_hub" timeout 20
    assert eval (room13["location"]=="inn" and preferences.text_cps==34)
    screenshot "ui065-direct-field-people-and-props.png"
    # Actual prop hit test, not a direct call to the observation label.
    assert eval (not r13_secret_route_available() and not r13_object_visible(ROOM13["objects"]["room13"]["books"]))
    assert eval (r13_object_visible(ROOM13["objects"]["inn"]["keys"]) and not r13_has("observed:inn:keys"))
    $ r13_qa_object_rect=ROOM13["objects"]["inn"]["keys"]["rect"]
    $ r13_qa_object_x=r13_qa_object_rect[0]+r13_qa_object_rect[2]/2-r13_world_offset()
    $ r13_qa_object_y=r13_qa_object_rect[1]+r13_qa_object_rect[3]/2
    assert eval (0<r13_qa_object_x<1280 and 0<r13_qa_object_y<720)
    click pos (r13_qa_object_x,r13_qa_object_y)
    pause until eval (r13_has("observed:inn:keys")) timeout 20
    assert screen "say"
    screenshot "ui065-direct-object-keys-observed.png"
    click pos (640,560) until screen "r13_hub" timeout 30
    assert eval (not r13_secret_route_available() and not r13_object_visible(ROOM13["objects"]["room13"]["books"]))
    click "할머니"
    click pos (640,560) until screen "r13_resident_approach" timeout 30
    assert screen "r13_resident_approach"
    screenshot "ui065-direct-person-approach.png"
    $ r13_qa_note("ui065: native two-line pagination; cps34 first/second click; settings preview/replay/instant; map idle outline/footer; old scene mode migration")
