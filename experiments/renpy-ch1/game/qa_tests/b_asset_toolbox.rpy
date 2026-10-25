# 매칭 한 번이 서로 다른 화면의 같은 버튼 역할에 전파되는지 확인한다.
testcase b_asset_toolbox:
    $ _test.timeout=30
    $ preferences.text_cps=0
    pause 2.0
    screenshot "toolbox-main-before.png"
    $ r13_qa_asset_before=__import__('copy').deepcopy(room13)
    run Function(r13_assets_assign,"button.primary","button.standard.basic")
    pause .6
    assert eval (r13_asset_spec("button.primary")["id"]=="button.standard.basic")
    assert eval (room13==r13_qa_asset_before)
    screenshot "toolbox-main-matched.png"
    click "처음부터"
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    run Hide("r13_hub")
    run Hide("say")
    run Function(renpy.hide,"r13_visitor")
    run Show("r13_qa_notebook_topics")
    pause .6
    screenshot "toolbox-question-matched.png"
    $ r13_qa_asset_before=__import__('copy').deepcopy(room13)
    run Function(r13_assets_reload)
    pause .6
    assert eval (r13_asset_spec("button.primary")["id"]=="button.primary.basic")
    assert eval (room13==r13_qa_asset_before)
    screenshot "toolbox-question-restored.png"
    run Hide("r13_qa_notebook_topics")

screen r13_qa_asset_file_alias():
    modal True
    zorder 210
    add Solid("#f7e8cd")
    text "공통 파일 연결 · 기존 경로도 함께 적용" font R13_UI_BOLD_FONT size 30 color "#493324" xpos 110 ypos 60
    text "기존 직접 경로" font R13_UI_BOLD_FONT size 24 color "#493324" xpos 170 ypos 160
    text "도구함 역할" font R13_UI_BOLD_FONT size 24 color "#493324" xpos 540 ypos 160
    text "또 다른 기존 화면" font R13_UI_BOLD_FONT size 24 color "#493324" xpos 900 ypos 160
    add "assets/map-status/locked.png" xpos 190 ypos 240 zoom 1.5
    add r13_asset("file:assets/map-status/locked.png") xpos 560 ypos 240 zoom 1.5
    add Transform("assets/map-status/locked.png",zoom=1.5) xpos 930 ypos 240

testcase b_asset_file_alias:
    $ _test.timeout=30
    pause 2.0
    run Show("r13_qa_asset_file_alias")
    pause .4
    screenshot "toolbox-file-before.png"
    $ r13_qa_asset_before=__import__('copy').deepcopy(room13)
    run Function(r13_assets_assign,"icon.map.locked","file:assets/map-status/map_selected.png")
    pause .6
    $ r13_qa_alias_bytes=renpy.file("assets/map-status/locked.png").read()
    $ r13_qa_target_bytes=renpy.file("assets/map-status/map_selected.png").read()
    assert eval (r13_qa_alias_bytes==r13_qa_target_bytes and room13==r13_qa_asset_before)
    screenshot "toolbox-file-matched.png"
    run Function(r13_assets_reload)
    pause .4
    assert eval (renpy.file("assets/map-status/locked.png").read()!=r13_qa_target_bytes)
    screenshot "toolbox-file-restored.png"
    run Hide("r13_qa_asset_file_alias")
