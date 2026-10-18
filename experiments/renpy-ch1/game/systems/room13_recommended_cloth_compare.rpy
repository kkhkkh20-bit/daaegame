# Code-native examination only. This never changes the direct-removal art gate.
# One generated texture, one cut contour, complementary masks. init915 uses base init905.
init 915 python:
    R13_REC_CLOTH_TEXTURE = "assets/recommended-story-icons/cloth-mask-v1/cloth_texture.png"
    R13_REC_CLOTH_SOURCE_RECT = (112, 136, 1312, 760)
    R13_REC_CLOTH_CONTOUR_V1 = ((300,92),(282,104),(272,104),(272,118),(256,118),(256,130),(244,130),(236,144),(222,144),(222,154),(206,154),(190,174))

    def r13_rec_cloth_part(part):
        # Sample immutable artwork into the logical grid once, then nearest 2x.
        source = Transform(Crop(R13_REC_CLOTH_SOURCE_RECT, R13_REC_CLOTH_TEXTURE), xysize=(300,174), nearest=False)
        mask = "assets/recommended-story-icons/cloth-mask-v1/%s_mask_rgba.png" % part
        return Transform(AlphaMask(source, mask), xysize=(600,348), nearest=True)

screen r13_rec_cloth_comparison():
    modal True
    default piece_position = 0
    $ offset = ((36,44),(0,44),(0,0))[piece_position]
    add Solid("#20202bea")
    frame:
        xalign .5
        yalign .5
        xysize (960,620)
        background Solid("#efe6d3")
        text "같은 천의 찢김선과 두 줄무늬" xpos 34 ypos 22 size 28 color "#352638"
        text "조각을 옮겨 가장자리와 줄무늬가 함께 이어지는지 확인한다." xpos 34 ypos 66 size 21 color "#5a4b57"
        fixed:
            xpos 146
            ypos 126
            xysize (650,400)
            add r13_rec_cloth_part("parent")
            add r13_rec_cloth_part("fragment") xpos offset[0] ypos offset[1]
        hbox:
            xpos 36
            ypos 534
            spacing 16
            textbutton "조각을 옮긴다" action SetScreenVariable("piece_position", (piece_position+1)%3)
            textbutton "두 줄과 가장자리가 이어진다" action Return("matched") sensitive (piece_position==2)
            textbutton "현장으로 돌아간다" action Return(None)
        text "이 대조만으로 반출 동작이나 나사 위치가 검증되지는 않는다." xpos 36 ypos 586 size 16 color "#805849"
