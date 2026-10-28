# 2026-10-27 타이포그래피 시안(TYPOGRAPHY_V2): 글자 크기 단계표와 색 토큰.
#   설계 docs/design/TYPOGRAPHY_V2.md. 2026-10-27 소유자 "적용" 으로 켰다. 끄면 이전 값으로 돌아가고,
#   꺼진 동안 화면은 이전과 픽셀 단위로 같아야 한다. 켜는 자리는 세 곳뿐이다 —
#   대사창(screens.rpy say, systems/room13_night_ui.rpy), 선택지(systems/room13_notebook_choices.rpy),
#   기록 화면(room13_notebook.rpy r13_records, systems/room13_evidence_view.rpy).
#   글꼴은 바꾸지 않는다(Pretendard, 2026-10-24 소유자 결정).
define R13_TYPE_V2 = True

init 59 python:
    # (PC 보통, PC 크게, 휴대폰 보통, 휴대폰 크게). 「작게」는 r13_read_size 가 지금처럼 깎는다.
    # 지금 가장 많이 쓰는 18/20/22/24/28/32 를 그대로 단계로 삼아 바뀌는 폭을 줄였다.
    # 휴대폰 값은 지금 화면들의 관행(PC +4, 크게 +2)을 따르고, 맨 위 두 단계만 더 올리지 않는다 —
    # 988px 너비 대사줄에서 36px 을 넘기면 한 줄에 27자도 안 들어간다.
    # 2026-10-27 소유자 "폰트 크기는 별표 친 게 마음에 드네": 대사창은 36px(이전 시안의 PC 큰 글씨),
    # 기록 화면은 지금 휴대폰 크기(자료 본문 30·출처 26)를 골랐다. 그래서 「보통」을 그 크기로 올리고
    # 「크게」는 한 단 더 둔다. 휴대폰은 그보다 작아지지 않게 같은 값 이상으로 맞춘다.
    # 2026-10-28 소유자 「잘 보이긴 하는데 무식하게 크고 두꺼운 느낌」→ 시안 2 선택: 모든 단계를 한 단씩(약 12%) 줄이고
    # 굵기는 보통(Regular)으로(room13_font.rpy). 여섯 단계 구조는 그대로다. 휴대폰 열(뒤 둘)은 그대로 둔다 —
    # 390px 화면에서 자료 본문이 16px 아래로 내려가면 읽기 어렵다(test_evidence_view).
    R13_TYPE_SCALE = {
        "small":    (20, 24, 26, 28),   # 꼬리표·출처·칩·날짜
        "body":     (22, 26, 28, 30),   # 보조 본문·하단 버튼·화면 밖 목소리
        "emphasis": (24, 28, 30, 32),   # 자료 본문(사실)·기록 대화·쟁점 작은 줄·선택지 본문
        "subtitle": (26, 30, 32, 34),   # 묶음 제목·빈 상태 안내
        "title":    (28, 32, 34, 36),   # 자료 이름·이름 리본·선택지 번호
        "display":  (30, 34, 36, 38),   # 대사·기록 제목
    }
    # 2026-10-27 소유자 "전체적으로 폰트 사이즈 6단계 이하로 통일해": hero(38/40)를 display 에 합쳐 여섯 단계.
    # 화면마다 박힌 숫자·r13_read_size(a,b)·「R13_TYPE_V2 꺼짐」 이중 경로는 같은 날 전부 이 단계로 바꿨다.
    R13_TYPE_LEVELS = ("small", "body", "emphasis", "subtitle", "title", "display")

    # 크림 종이(#f5ecd9) 위 글자색. 대비는 TYPOGRAPHY_V2.md 표에 있다. 4.5:1 미만은 disabled 하나뿐이고
    # 비활성 조작은 WCAG 1.4.3 의 예외다. accent 는 테이프 빨강(#bc4134, 4.53:1)보다 한 단 어두운
    # 값이라 작은 글씨에도 쓸 수 있다. 빨강 바탕·갈색 배지 등 어두운 면 위에는 inverse 만 쓴다.
    R13_TYPE_COLORS = {
        "ink":      "#4b3420",   # 본문. 대사·자료 본문·제목
        "muted":    "#6b5641",   # 보조. 출처·꼬리표·안내
        "disabled": "#a99b86",   # 비활성 조작
        "accent":   "#a63a2e",   # 강조. 구분 꼬리표·발언 표시
        "inverse":  "#fff3df",   # 반전. 남색·갈색·빨강 면 위
    }

    def r13_type(level):
        """단계 이름 → 지금 설정(작게·보통·크게)과 기기(휴대폰)에 맞는 px."""
        pc_base, pc_large, touch_base, touch_large = R13_TYPE_SCALE[level]
        if r13_touch_ui():
            return r13_read_size(touch_base, touch_large)
        return r13_read_size(pc_base, pc_large)

    def r13_type_color(token):
        return R13_TYPE_COLORS[token]
