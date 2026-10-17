# Review-only composition; never connected to the production topic dispatcher.
screen r13_side_topics_preview(person,entries):
    modal True
    zorder 40
    $ big=persistent.room13_large_text
    add Solid("#00000088")
    add r13_close_art(person,"neutral",840):
        xpos r13_close_x(person,"neutral",840)-340 xanchor .5 ypos r13_close_y(person,840,110,"neutral")
    text R13_NAMES[person] xpos 80 ypos 92 size 38 color "#f6d18a" font r13_ui_font() outlines [(1,"#101515",0,0)]
    text "묻고 싶은 이야기" xpos 640 ypos 76 size 26 color "#fff4df" font r13_ui_font()
    text ("질문 %d개 · 모두 표시"%len(entries)) xpos 1020 ypos 92 size 17 color "#d4c8b4" font r13_ui_font()
    for i,(title,command,read) in enumerate(entries):
        button:
            id ("side_topic_"+str(i+1))
            area (640,120+i*62,592,54) padding (20,6)
            background R13InkPanel(alpha="d9",slim=True)
            hover_background R13InkPanel(focused=True,alpha="f5",slim=True)
            action command
            text (str(i+1)+"   "+title) yalign .5 size (28 if big else 26) color "#fff4df" font r13_ui_font()
    use r13_present_design_button(Return("present"),True,640,636,592,72)
    textbutton "← 돌아가기":
        area (24,660,180,48) style "r13_action_button" text_size 22
        action Return("back")
    fixed:
        area (448,646,140,70)
        use r13_antique_button("기록","record",Show("r13_records"),compact=True,width=140)
