# 수첩 공통 틀 (2026-10-27 소유자: "수첩 왜 자꾸 유아이 틀이 바뀌어? 일관성있게해야지. 수첩 끝에도 계속 짤리고",
# "갈림길이 그나마 뒤 에셋이 안짤리는데", "뒤 에셋이 수첩모양인데 안짤리게 같은 모형으로 만들어야지").
#   기록(자료·사람·대화·메모·달력·소지품)과 갈림길이 한 틀을 쓴다. 배경은 갈림길·설정창과 같은
#   b_opt_panel.png 을 (-4,-4) 에 그대로 깐다 — 1288x728 이라 화면(1280x720)에 온전히 들어오고 고리가
#   판 밖으로 나가지 않는다. 예전 자료 탭의 R13DiaryPanel(12,12 1256x696) 은 고리를 판 밖에 그려 좌우가
#   잘렸고, 사람·대화·메모 탭은 또 다른 R13TravelSheet 였다.
#   제목·부제·닫기 X·회차/일째 자리는 소유자가 기준으로 지목한 갈림길 화면(room13_fork_screen.rpy)의
#   좌표를 그대로 옮겼다. 글자 크기는 systems/room13_type_scale.rpy 의 단계만 쓴다.
#
#   안쪽 영역 R13_NB_INNER — 내용은 이 안에만 그린다. 왼쪽 132 는 고리(화면 x 90~127) 오른쪽, 오른쪽 1206 은
#   종이 오른쪽 가장자리(약 1210) 안쪽. 아래 636 은 종이(646) 안쪽이다 — 버튼·글자·뷰포트 모두 이 선 위에서 끝난다.
init 60 python:
    R13_NB_PANEL="file:assets/ui-b-options/b_opt_panel.png"   # 갈림길·설정창과 같은 판. "file:" 꼴이 에셋 도구함 규칙이다
    R13_NB_PANEL_POS=(-4,-4)
    R13_NB_TITLE_X=114          # 제목 왼쪽 기준선(갈림길과 같다). 부제·갈림길 안내도 이 선에 맞춘다
    R13_NB_TITLE_Y=64
    R13_NB_SUBTITLE_Y=112
    R13_NB_STAMP=(1150,78)      # 「N회차 · N일째」 오른쪽 끝 기준
    R13_NB_HEAD_CY=88           # 제목 줄의 중심선. 탭·칩·목표 칸이 이 선에 맞춘다
    R13_NB_RULE_Y=128           # 제목 줄 아래 금색 선
    # 2026-10-27 소유자 "버튼이 수첩 안에 있으면 안에 있어야 하고, 애매하게 뒷배경을 초과하면 안 돼": 아래를 종이(646) 안쪽 636 으로.
    R13_NB_INNER=(132,140,1074,496)   # x, y, w, h → 오른쪽 1206, 아래 636(종이 안)
    R13_NB_LEFT=R13_NB_INNER[0]
    R13_NB_TOP=R13_NB_INNER[1]
    R13_NB_RIGHT=R13_NB_INNER[0]+R13_NB_INNER[2]
    R13_NB_BOTTOM=R13_NB_INNER[1]+R13_NB_INNER[3]
    R13_NB_WIDTH=R13_NB_INNER[2]
    # 종이(크림)는 y 646 에서 끝나고 그 아래 20px 은 겹친 종이 가장자리·남색 테두리다. 그 위에 아무것도 걸치지 않는다.
    R13_NB_PAPER_BOTTOM=646
    R13_NB_TEXT_BOTTOM=636
    R13_NB_BUTTON_W=136         # 하단 버튼 한 칸(갈림길 「닫기」와 같다)
    R13_NB_GAP=16

    def r13_nb_close_rect():
        # 갈림길과 같다. 휴대폰은 64, PC 는 52.
        return (1170,52,64,64) if r13_touch_ui() else (1176,60,52,52)

    def r13_nb_footer_y():
        """하단 버튼 줄의 위. 버튼 높이는 공통 부품(R13_CONTROL)의 높이다."""
        return R13_NB_BOTTOM-r13_control_height()

    def r13_nb_body_bottom():
        """하단 버튼 줄 위에서 본문이 끝나는 선."""
        return r13_nb_footer_y()-12

    def r13_nb_footer_x(index,width=None):
        """오른쪽에서 index 번째 하단 버튼의 x. 0 이 맨 오른쪽(닫기)."""
        width=width or R13_NB_BUTTON_W
        return R13_NB_RIGHT-(index*(R13_NB_BUTTON_W+R13_NB_GAP))-width

    def r13_nb_title_size():
        return r13_type("display")

    def r13_nb_small_size():
        return r13_type("small")

    def r13_nb_heading_size():
        """탭 안의 묶음 제목(알게 된 관계, 조사 메모, 달력 …)."""
        return r13_type("subtitle")

    def r13_nb_body_size():
        return r13_type("body")

    def r13_nb_emphasis_size():
        return r13_type("emphasis")

    def r13_nb_ink():
        return r13_type_color("ink")

    def r13_nb_muted():
        return r13_type_color("muted")

    def r13_nb_accent():
        return r13_type_color("accent")

# 틀 한 벌: 어두운 막, 수첩 판, 제목(과 부제·회차), 상단 탭 줄, 닫기 X, 금색 선.
#   tabs    [(key, title, action), ...] — 제목 오른쪽에 90px 간격으로 놓는다(r13_ev_tab_x 가 제목 길이를 피한다).
#   note    탭 오른쪽의 짧은 안내(보여주기 책이 쓴다).
#   stamp   오른쪽 위 「N회차 · N일째」(갈림길).
#   rule_y  금색 선의 y. 갈림길은 부제 아래(149)에 둔다.
screen r13_notebook_shell(title,subtitle=None,close_action=None,tabs=None,current=None,note=None,stamp=None,rule_y=None):
    $ touch=r13_touch_ui()
    $ tab_h=88 if touch else 48
    $ nb_small=r13_nb_small_size()
    $ close_rect=r13_nb_close_rect()
    add Solid("#05070fa6")
    add r13_asset_path(R13_NB_PANEL) xpos R13_NB_PANEL_POS[0] ypos R13_NB_PANEL_POS[1]
    text title xpos R13_NB_TITLE_X ypos R13_NB_TITLE_Y size r13_nb_title_size() color r13_nb_ink() font R13_UI_BOLD_FONT
    if subtitle:
        text subtitle xpos R13_NB_TITLE_X ypos R13_NB_SUBTITLE_Y size nb_small color r13_nb_muted() font R13_UI_BOLD_FONT
    if stamp:
        text stamp xpos R13_NB_STAMP[0] xanchor 1.0 ypos R13_NB_STAMP[1] size nb_small color r13_nb_ink() font R13_UI_BOLD_FONT
    if tabs:
        $ tab_x=r13_ev_tab_x(title)
        for index,(tab_key,tab_title,tab_action) in enumerate(tabs):
            fixed:
                xpos (tab_x+index*R13_EV_TAB_PITCH) ypos (R13_NB_HEAD_CY-tab_h//2) xysize (88,tab_h)
                if tab_key==current:
                    add Transform(r13_notebook_button_surface(True),xysize=(86,44)) align (.5,.5)
                textbutton tab_title:
                    style "r13ev_tab_button" text_style "r13ev_tab_button_text" xysize (88,tab_h)
                    text_size nb_small selected tab_key==current action tab_action alt tab_title
        if note:
            text note xpos (tab_x+len(tabs)*R13_EV_TAB_PITCH+12) ypos (R13_NB_HEAD_CY-nb_small//2-2) size nb_small color r13_nb_accent() font R13_UI_BOLD_FONT xsize max(120,1150-(tab_x+len(tabs)*R13_EV_TAB_PITCH+12))
    if close_action is not None:
        button:
            id "r13_ev_close"
            xpos close_rect[0] ypos close_rect[1] xysize (close_rect[2],close_rect[3])
            background None hover_background Solid("#fff6e214")
            action close_action alt "닫기"
            add Transform(r13_asset_path("file:assets/ui-b-options/b_opt_close.png"),xysize=(40,40)) align (.5,.5)
    $ line_y=rule_y or R13_NB_RULE_Y
    add r13_asset_path("file:"+(R13_NIGHT_UI+"diamond.png")) xpos (R13_NB_TITLE_X-20) ypos (line_y-4)
    add Solid("#c9a86a99") xpos (R13_NB_TITLE_X-10) ypos line_y xsize (R13_NB_RIGHT-(R13_NB_TITLE_X-10)) ysize 1

# 하단 버튼 줄의 한 칸. 오른쪽에서 index 번째, 공통 부품 높이.
screen r13_nb_footer_button(index,caption,action,enabled=True,primary=False,width=None,control_id=None):
    $ fw=width or R13_NB_BUTTON_W
    fixed:
        xpos r13_nb_footer_x(index,fw) ypos r13_nb_footer_y() xysize (fw,r13_control_height())
        use r13_control(caption,None,action,enabled=enabled,primary=primary,width=fw,control_id=control_id)
