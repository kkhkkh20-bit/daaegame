
label r13_recommended_contact_inspect:
    call screen r13_rec_cloth_comparison
    if _return != "matched":
        return False
    call screen r13_rec_piko_contact_sequence
    if not _return:
        return False
    if not r13_rec_piko_geometry_ready(r13_recommended):
        call screen r13_recommended_status("등과 천의 형상 검수 상태와 실제 화면 검증을 구분합니다. 아직 실행 화면의 대조·좌표 검증이 끝나지 않아 직접 반출 확정은 잠겨 있습니다.")
        return False
    call r13_lines([(None,"뚜껑을 닫으면 가려지는 안쪽 쇠붙이의 조각이다. 밖에 놓인 돌만 집어 넣는 동안에는 닫힌 뚜껑 너머 그 자리에 천이 닿지 않는다."),(None,"용기의 천을 풀어 대자 찢긴 가장자리와 두 줄무늬가 같은 위치에서 이어졌다. 천 중앙은 찢어지지 않았다."),("dad","두 줄과 찢긴 자리가 이어지는구나. 누가 빌려 썼고 돌을 내려놓을 때 천이 어땠는지도 꼬미에게 들은 말과 함께 보자.")], "recommended:contact:match")
    return True

screen r13_recommended_status(message):
    modal True
    add Solid("#172421ed")
    frame:
        xalign .5 yalign .5 xsize 950
        vbox:
            spacing 24
            text "개발 검증 상태" size 28
            text message size 24
            textbutton "돌아가기" action Return(True)

# New explicit testimony detail, not Dad's invented memory or a new evidence item.
label r13_rec_piko_intact_loan:
    call screen r13_rec_piko_intact_cloth
    return True

screen r13_rec_piko_intact_cloth(as_overlay=False):
    modal True
    default after_delivery = False
    add Solid("#20202bea")
    frame:
        align (.5,.5) xsize 960 padding (30,24)
        vbox:
            spacing 20
            text ("꼬미가 설명한 같은 저녁 · 돌을 내려놓을 때" if after_delivery else "꼬미가 설명한 2일 저녁 · 빌려주기 전") size 28
            text ("나비가 천을 풀어 돌을 내려놓았다. 꼬미가 맞춰 접었던 같은 모서리는 이미 찢어져 있었다." if after_delivery else "빈 통에 넣기 전 직접 펼쳐 보고 접었다. 그때는 모서리와 두 줄무늬가 끊기지 않았다.") size 23 xsize 880
            if after_delivery:
                add r13_rec_cloth_part("parent") xalign .5
            else:
                add Transform(Transform(Crop(R13_REC_CLOTH_SOURCE_RECT,R13_REC_CLOTH_TEXTURE),xysize=(300,174),nearest=False),xysize=(600,348),nearest=True) xalign .5
            text "동일한 천의 전후 · 꼬미의 관찰을 그린 재구성" size 19
            textbutton ("빌려주기 전 모습" if after_delivery else "돌을 내려놓을 때 모습") action ToggleScreenVariable("after_delivery")
            textbutton "꼬미의 이야기로 돌아간다" action (Hide("r13_rec_piko_intact_cloth") if as_overlay else Return(True)) sensitive (as_overlay or after_delivery)


screen r13_rec_piko_contact_sequence():
    modal True
    default frame_index = 0
    default fitting_seen = False
    $ frames = [('open__640x400.png','등을 벤치 받침에 놓고 뚜껑을 연 모습'),('grip__640x400.png','천을 접어 뜨거운 돌을 감싸는 동작'),('contact__640x400.png','천이 닿는 안쪽 고정부를 직접 짚어 보자'),('lifted__640x400.png','돌이 빠진 뒤에도 같은 안쪽 고정부에 남은 조각'),('container_unfolded__640x400.png','같은 천을 용기에서 펼쳐 본 모습'),('inner_fitting_section.png','뚜껑을 닫으면 가려지는 고정부 단면')]
    add Solid('#20202bea')
    frame:
        area (150,30,980,660) padding (0,0)
        fixed:
            text '등·돌·천의 접촉 · 동작 재구성' xpos 28 ypos 24 size 28
            text frames[frame_index][1] xpos 28 ypos 68 size 22
            # Exact contract: final640x400 at screen(320,140), no rescaling.
            add ('assets/recommended-story-icons/piko-native-v4/'+frames[frame_index][0]) xpos 170 ypos 110
            if frame_index==2:
                button:
                    area (584,232,54,54)
                    background Solid('#f6d58a25') hover_background Solid('#f6d58a88')
                    action SetScreenVariable('fitting_seen',True)
                    alt '천 모서리가 스치는 안쪽 금속 고정부'
                if fitting_seen:
                    text '고정부 위치 확인' xpos 680 ypos 240 size 18 color '#3a4934'
            text '실제 반출 시점은 꼬미가 본 천의 전후와 함께 판단한다.' xpos 28 ypos 530 size 18
            hbox:
                xpos 28 ypos 577 spacing 28
                textbutton '앞 장면' action SetScreenVariable('frame_index',max(0,frame_index-1)) sensitive frame_index>0
                textbutton '다음 장면' action SetScreenVariable('frame_index',min(len(frames)-1,frame_index+1)) sensitive frame_index<len(frames)-1
                textbutton '구조 확인을 마친다' action Return(True) sensitive (frame_index==len(frames)-1 and fitting_seen)
                textbutton '돌아가기' action Return(False)
            if frame_index==len(frames)-1 and not fitting_seen:
                text '앞 장면의 천 접촉 위치를 직접 확인하자.' xpos 28 ypos 627 size 18
    key 'game_menu' action Return(False)


label r13_recommended_art_admin:
    # Native-only disposable inspection fixture, never awards facts or opens gates.
    call screen r13_rec_cloth_comparison
    call screen r13_rec_piko_contact_sequence
    return
