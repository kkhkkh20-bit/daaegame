# 메인 메뉴: 지금 판과 같은 납품 B 좌표(엽서 배경·왼쪽 위 로고·오른쪽 출연진 포스터·아래 단추 넷).

screen main_menu():
    tag menu
    $ newest = renpy.newest_slot()
    add Transform("assets/ui-b-main/b_main_background_postcard.png", zoom=1280.0 / 1672)
    add Transform("assets/ui-b-main/b_logo.png", zoom=0.85) xpos -18 ypos 10
    add Transform("assets/ui-b-main/b_main_cast_poster_plain.png", zoom=610.0 / 1402) xpos 754 ypos 80
    hbox:
        xpos 44 ypos 616 spacing 14
        textbutton "이어하기" style "v2_button" xysize (184, 64) action FileLoad(newest, confirm=False, page=None) sensitive newest is not None text_size v2_type("subtitle")
        textbutton "처음부터" style "v2_primary" xysize (184, 64) action Start() text_size v2_type("subtitle")
        textbutton "불러오기" style "v2_button" xysize (184, 64) action Show("v2_files", mode="load") text_size v2_type("subtitle")
        textbutton "설정" style "v2_button" xysize (184, 64) action Show("v2_settings") text_size v2_type("subtitle")
    text "v2 1일 시범" xpos 1130 ypos 674 size v2_type("small") color "#b2b8b8"
