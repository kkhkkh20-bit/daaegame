# Research fixture only: not connected to the public topics dispatcher.
screen r13_reference_topics(person,entries,layout="grid"):
    modal True
    zorder 40
    default page=0
    $ big=persistent.room13_large_text
    $ page_size=8 if layout=="grid" else 4
    $ pages=max(1,(len(entries)+page_size-1)//page_size)
    $ page=min(page,pages-1)
    add Solid("#00000030")
    add r13_close_art(person,"neutral",840):
        xpos r13_close_x(person,"neutral") xanchor .5 ypos r13_close_y(person,840,110,"neutral")
    text (R13_NAMES[person]+"에게 묻기") xpos 420 ypos 92 xsize 440 text_align .5 size 26 color "#f6d18a" font r13_ui_font() outlines [(1,"#101515",0,0)]
    text ("질문 %d개 · 모두 표시"%len(entries) if layout=="grid" and pages==1 else "질문 %d개 · %d / %d쪽"%(len(entries),page+1,pages)) xpos 420 ypos 132 xsize 440 text_align .5 size 17 color "#efe2c2" font r13_ui_font() outlines [(1,"#101515",0,0)]
    for slot,(title,command,read) in enumerate(entries[page*page_size:(page+1)*page_size]):
        $ number=page*page_size+slot+1
        $ card_w=376 if layout=="grid" else 752
        $ card_h=(96 if big else 88) if layout=="grid" else (96 if big else 84)
        $ card_x=(24 if slot%2==0 else 880) if layout=="grid" else 264
        $ card_y=164+(slot//2 if layout=="grid" else slot)*(card_h+12)
        button:
            id ("reference_topic_"+str(number))
            area (card_x,card_y,card_w,card_h) padding (16,10)
            background R13InkPanel(alpha="e6",slim=True)
            hover_background R13InkPanel(focused=True,alpha="f5",slim=True)
            action command
            text (str(number)+"  "+r13_question_caption(title,read,False)) xsize card_w-32 yalign .5 size r13_read_size(24,28) color "#fff4df" font r13_ui_font() line_spacing 4
    if pages>1:
        textbutton "← 이전 질문":
            area (264,588,220,42) style "r13_action_button" text_size 20
            background R13InkPanel(alpha="e6",slim=True) sensitive page>0
            action SetScreenVariable("page",page-1)
        textbutton ("다음 질문 %d개 →"%min(page_size,len(entries)-(page+1)*page_size) if page+1<pages else "마지막 쪽"):
            area (756,588,260,42) style "r13_action_button" text_size 20
            background R13InkPanel(alpha="e6",slim=True) sensitive page+1<pages
            action SetScreenVariable("page",page+1)
    use r13_present_design_button(Return("present"),True,474,638,332,80 if big else 72)
    textbutton "돌아가기":
        area (24,676,156,44) style "r13_action_button" text_size 20
        action Return("back")
    fixed:
        area ((1148,650,132,70) if big else (1168,664,112,56))
        use r13_antique_button("기록","record",Show("r13_records"),compact=True,width=(132 if big else 112))
