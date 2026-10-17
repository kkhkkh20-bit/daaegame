# Review branch: presentation choices do not change clocks, evidence or NPC schedules.
default r13_field_view = "scene"
default r13_field_spots = False
default r13_field_pick = None

init 85 python:
    def r13_field_selection():
        picked=getattr(store,"r13_field_pick",None)
        if not picked or picked[0]!=store.room13["location"]:return None
        spec=ROOM13["objects"].get(picked[0],{}).get(picked[1])
        return picked[1] if spec and r13_object_visible(spec) else None

screen r13_field_spots_overlay(ready):
    for number,(key,spec) in enumerate([(k,v) for k,v in ROOM13["objects"].get(room13["location"],{}).items() if r13_object_visible(v)]):
        $ x,y,w,h=spec["rect"]
        button:
            area (int(x+w/2)-22,int(y+h/2)-22,44,44) padding (0,0)
            background R13InkPanel(alpha="e6",slim=True) hover_background R13InkPanel(focused=True,alpha="ff",slim=True)
            action SetVariable("r13_field_pick",(room13["location"],key)) sensitive ready
            alt (r13_object_name(key)+" 선택") tooltip r13_object_name(key)
            add R13AntiqueIcon("investigate",size=26) align (.5,.5)

screen r13_field_view_controls(ready):
    $ people_alert=bool(r13_offers_here())
    textbutton "주변 살피기":
        area (24,638 if persistent.room13_large_text else 646,196,80 if persistent.room13_large_text else 64) style "r13_action_button" padding (10,8) text_size r13_read_size(22,25)
        background R13InkPanel(focused=r13_field_view=="scene",alpha="ef",slim=True)
        text_color ("#f6dfac" if r13_field_view=="scene" else "#d8d0bf")
        action SetVariable("r13_field_view","scene") sensitive ready
    textbutton ("사람과 대화 · !" if people_alert else "사람과 대화"):
        area (232,638 if persistent.room13_large_text else 646,212,80 if persistent.room13_large_text else 64) style "r13_action_button" padding (10,8) text_size r13_read_size(22,25)
        background R13InkPanel(focused=r13_field_view=="people",alpha="ef",slim=True)
        text_color ("#f6dfac" if r13_field_view=="people" else "#d8d0bf")
        action SetVariable("r13_field_view","people") sensitive ready
    if r13_field_view=="scene":
        textbutton ("조사 지점 숨기기" if r13_field_spots else "조사 지점 표시"):
            area (24,110,210,48) style "r13_action_button" padding (10,6) text_size r13_read_size(19,22)
            action ToggleVariable("r13_field_spots") sensitive ready
        $ target=r13_field_selection()
        frame:
            area (460,638 if persistent.room13_large_text else 646,672,80 if persistent.room13_large_text else 64) padding (16,8) background R13InkPanel(alpha="e6",slim=True)
            if target:
                text r13_object_name(target) xsize 430 yalign .5 size r13_read_size(23,26) color "#fff4df" font r13_ui_font()
            else:
                text "배경의 물건을 눌러 선택하세요" yalign .5 size r13_read_size(21,24) color "#e8d9b0" font r13_ui_font()
        if target:
            textbutton "살펴보기":
                area (940,638 if persistent.room13_large_text else 646,180,80 if persistent.room13_large_text else 64) style "r13_action_button" padding (10,4) text_size r13_read_size(23,26)
                action [Function(r13_click_feedback,target),Return(("object",target))] sensitive ready
