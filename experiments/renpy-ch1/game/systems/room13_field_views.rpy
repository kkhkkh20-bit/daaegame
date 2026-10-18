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
    use r13_footer_control(0,"주변 살피기","investigate",SetVariable("r13_field_view","scene"),enabled=ready,chosen=r13_field_view=="scene")
    use r13_footer_control(1,"사람과 대화 !" if people_alert else "사람과 대화","dialogue",SetVariable("r13_field_view","people"),enabled=ready,chosen=r13_field_view=="people")
    use r13_footer_control(3,"더보기","settings",Show("r13_more_tools"),enabled=ready)
    if r13_field_view=="scene":
        fixed:
            area (28,104,232,64)
            use r13_control("지점 숨기기" if r13_field_spots else "조사 지점","investigate",ToggleVariable("r13_field_spots"),enabled=ready,chosen=r13_field_spots,height=64)
        $ target=r13_field_selection()
        frame:
            area (28,r13_control_y()-64,944,48) padding (16,8) background R13InkPanel(alpha="e6",slim=True)
            text (r13_object_name(target) if target else "배경의 물건을 눌러 선택하세요") yalign .5 size r13_read_size(21,24) color "#fff4df" font r13_ui_font()
        use r13_footer_control(2,"살펴보기","investigate",[Function(r13_click_feedback,target),Return(("object",target))] if target else NullAction(),enabled=ready and bool(target),primary=True)
