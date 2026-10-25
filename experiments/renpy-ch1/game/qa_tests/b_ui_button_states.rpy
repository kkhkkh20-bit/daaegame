init 999 python:
    def r13_qa_button_mouse(down):
        import pygame
        pos=pygame.mouse.get_pos()
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN if down else pygame.MOUSEBUTTONUP,button=1,pos=pos,test=True))

screen r13_qa_button_states():
    modal True
    zorder 200
    default hits=0
    add Solid("#f7e8cd")
    text "버튼 상태 확인" font R13_UI_BOLD_FONT size 34 color "#493324" xpos 70 ypos 50
    for row,family in enumerate(("primary","standard","wide_choice")):
        $ yy=150+row*145
        text ("빨강" if family=="primary" else "크림" if family=="standard" else "넓은 선택") font R13_UI_BOLD_FONT size 24 color "#493324" xpos 70 ypos yy
        for col,kind in enumerate(("basic","selected","disabled")):
            fixed:
                area (280+col*300,yy-15,250,88)
                use r13_state_button("기본" if kind=="basic" else "선택" if kind=="selected" else "비활성",SetScreenVariable("hits",hits+1),250,88,family,chosen=kind=="selected",enabled=kind!="disabled",control_id="qa_"+family+"_"+kind)
    text ("동작 횟수: %d"%hits) font R13_UI_BOLD_FONT size 24 color "#493324" xpos 70 ypos 630

testcase b_ui_button_states:
    $ _test.timeout=30
    pause 2.0
    run Show("r13_qa_button_states")
    pause .5
    screenshot "button-states.png"
    move id "qa_primary_basic"
    run Function(r13_qa_button_mouse,True)
    pause .3
    assert eval (renpy.get_widget("r13_qa_button_states","qa_primary_basic_visual").pressed)
    screenshot "button-pressed.png"
    run Function(r13_qa_button_mouse,False)
    pause .3
    assert eval (renpy.get_screen("r13_qa_button_states").scope["hits"]==1)
    click id "qa_standard_disabled"
    pause .2
    assert eval (renpy.get_screen("r13_qa_button_states").scope["hits"]==1)
    click id "qa_wide_choice_selected"
    pause .2
    assert eval (renpy.get_screen("r13_qa_button_states").scope["hits"]==2)
    run Hide("r13_qa_button_states")

testcase b_map_status_early:
    $ _test.timeout=30
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=0,location="inn",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    click "지도" until screen "r13_map" timeout 30
    click "마을"
    run Function(r13_qa_village_zoom,1136.0/1642)
    pause .6
    screenshot "map-status-early.png"
    assert eval (any(state!="open" and r13_map_status_kinds(key,state,None)==("locked",) for key,state in r13_village_b_rows() if key!="inn"))
    assert eval (r13_map_status_kinds("inn","open","square")==("current_location",))
    click id "map_name_square"
    assert eval (r13_map_status_kinds("square","open","square")==("map_selected",) and room13["location"]=="inn")
    screenshot "map-status-selected.png"
    assert eval ("greenhouse" not in dict(r13_map_nodes("mountain")) and "altar" not in dict(r13_map_nodes("mountain")))
