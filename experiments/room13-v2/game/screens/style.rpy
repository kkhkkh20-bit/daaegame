# 공통 재질: 크림 종이·짙은 잉크·빨강 강조·Pretendard 고딕.
# 글자 크기는 아래 단계(v2_type)로만 정한다. 화면 파일에 숫자 크기를 쓰지 않는다(dev/test_type_scale.py).
# 단계 값은 지금 판 room13_type_scale.rpy 의 PC 열(보통, 크게)을 그대로 옮겼다. 「작게」는 보통에서 2 뺀다.

init python:
    V2_TYPE_SCALE = {
        "tag": (16, 18),        # 현장 인물 이름표(지금 판 r13_actor_nameplates 16, 휴대폰 18)
        "small": (20, 24),      # 꼬리표·출처·칩·날짜
        "body": (22, 26),       # 보조 본문·하단 버튼
        "emphasis": (24, 28),   # 자료 본문·선택지 본문
        "subtitle": (26, 30),   # 묶음 제목·빈 상태 안내
        "title": (28, 32),      # 자료 이름·이름 리본
        "display": (30, 34),    # 대사·기록 제목
    }
    V2_COLOR = {
        "ink": "#4b3420",
        "muted": "#6b5641",
        "disabled": "#a99b86",
        "accent": "#a63a2e",
        "inverse": "#fff3df",
        "paper": "#fff6e6",
        "paper_dark": "#f2e3c8",
        "navy": "#2b3245",
        "red": "#c9434a",
    }

    def v2_type(level):
        base, large = V2_TYPE_SCALE[level]
        size = persistent.v2_text_size
        if size == "large":
            return large
        if size == "small":
            return base - 2
        return base

    # UI 그림의 투명 여백(그림 둘레 그림자 자리). 늘려 쓸 때는 여백을 잘라 내고 쓴다.
    V2_UI_BOX = {
        "ui-b-options/b_opt_choice.png": (16, 16, 190, 52),
        "ui-b-options/b_opt_choice_hover.png": (16, 16, 190, 52),
        "ui-b-options/b_opt_choice_selected.png": (16, 16, 190, 52),
        "ui-b-field/b_button.png": (16, 10, 128, 32),
        "ui-b-field/b_button_primary.png": (16, 10, 128, 32),
        "ui-b-field/b_panel_small.png": (8, 8, 224, 44),
        "ui-b-question/b_tab_title.png": (17, 13, 286, 38),
        "ui-b-question/nameplate_paper.png": (16, 16, 200, 64),
        "ui-b-dialogue/b_ribbon_name.png": (16, 12, 168, 31),
        "ui-b-question/b_panel_card.png": (16, 16, 640, 84),
        "ui-b-question/b_panel_card_hover.png": (16, 16, 640, 84),
    }

    def v2_frame(name, border=16):
        """지금 판 UI 그림(navy 테두리 크림 카드·빨강 버튼)을 늘려 쓴다."""
        box = V2_UI_BOX.get(name)
        img = Crop(box, "assets/" + name) if box else "assets/" + name
        return Frame(img, border, border)

    def v2_ribbon():
        """빨강 리본(오른쪽 끝이 갈라진 모양)을 늘려도 끝 모양이 남게 오른쪽 테두리를 넓게 둔다."""
        return Frame(Crop(V2_UI_BOX["ui-b-dialogue/b_ribbon_name.png"], "assets/ui-b-dialogue/b_ribbon_name.png"), 8, 6, 22, 6)

style default:
    font "assets/Pretendard-Regular.otf"
    color "#4b3420"
    language "korean-with-spaces"

style v2_button is button:
    background v2_frame("ui-b-options/b_opt_choice.png", 18)
    hover_background v2_frame("ui-b-options/b_opt_choice_hover.png", 18)
    selected_background v2_frame("ui-b-field/b_button_primary.png", 14)
    insensitive_background v2_frame("ui-b-options/b_opt_choice.png", 18)
    padding (18, 10)

style v2_button_text is text:
    color "#4b3420"
    selected_color "#fff3df"
    insensitive_color "#a99b86"
    xalign 0.5
    yalign 0.5
    text_align 0.5

# 자료 카드: 고르면 빨강 테두리(지금 판 체크 카드).
style v2_card is button:
    background v2_frame("ui-b-question/b_panel_card.png", 20)
    hover_background v2_frame("ui-b-question/b_panel_card_hover.png", 20)
    selected_background v2_frame("ui-b-question/b_panel_card_hover.png", 20)
    padding (14, 8)

style v2_primary is v2_button:
    background v2_frame("ui-b-field/b_button_primary.png", 14)
    hover_background v2_frame("ui-b-field/b_button_primary.png", 14)
    insensitive_background v2_frame("ui-b-field/b_button.png", 14)

style v2_primary_text is v2_button_text:
    color "#fff3df"
    hover_color "#ffffff"
    insensitive_color "#a99b86"

# 고른 자료 칩: 작은 종이 칸. 칸 높이를 글자에 맞춰 두어 글자가 테두리 밖으로 나가지 않는다.
style v2_chip is button:
    background v2_frame("ui-b-field/b_panel_small.png", 10)
    hover_background v2_frame("ui-b-question/b_panel_card_hover.png", 12)
    padding (14, 6)
    ysize 40

style v2_chip_text is text:
    color "#4b3420"
    hover_color "#a63a2e"
    yalign 0.5
