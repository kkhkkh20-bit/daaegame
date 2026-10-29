# 이름·장소·핵심어 글씨 구분 (2026-10-26 소유자: "고유명사나 이름, 생각의 글씨 색상·두께를 차별화. 레퍼런스 보고 맞춰봐").
# 레퍼런스: 역전재판(독백은 괄호 안 파란 글씨, 핵심어는 빨간 글씨), 단간론파(핵심 단어를 굵은 강조색).
#   인물 이름   주황갈색 + 더 굵게(ExtraBold)
#   장소 이름   초록 + 더 굵게
#   「자료」【핵심어】 빨강 + 더 굵게
#   아빠 생각   괄호 + 또렷한 파랑(지금 회청색보다 진하게)
# 2026-10-27 소유자 "추천안대로 해"로 켰다(시안 단계에서는 꺼 두었다).
# 이름 뒤에 조사·띄어쓰기·문장부호가 올 때만 이름으로 본다("도토리" 의 "도토" 는 건드리지 않는다).
init 142 python:
    import re as _r13_na_re
    R13_NAME_ACCENT_ON = True  # 2026-10-27 소유자 "추천안대로 해"로 켬
    R13_ACCENT_FONT = "assets/Pretendard-ExtraBold.otf"
    # 2026-10-28 소유자 「주황·초록이 너무 눈에 띈다, 채도를 줄이자」: 인물(채도 0.74→0.41)·장소(0.39→0.21)를 낮췄다.
    # 밝기는 거의 그대로라 크림 종이 위 대비는 유지된다. 핵심어 빨강·생각 파랑은 그대로.
    R13_ACCENT_COLORS = dict(person="#8A583A", place="#395948", key="#B3261E", thought="#2A5FA8")
    # 관계·직함은 고유명사가 아니다.
    R13_ACCENT_SKIP = {"아빠","엄마","할머니","주민","아이","선생님","사자 선생님","촌장","순찰대원","아랫길 주민","아랫길 노인","실룩의 아이","판돌 영감"}
    _R13_ACCENT_TAIL = r"(?=$|[\s.,!?…~\"'」』)\]·]|이랑|이나|이야|이에요|이었|이오|이다|이고|이지|에게|한테|께서|께|까지|부터|처럼|보다|으로|로|이|가|은|는|을|를|의|에|와|과|도|만|랑|아|야|요|씨|님|네|나)"

    def _r13_accent_words():
        people=set(v for v in R13_NAMES.values() if isinstance(v,str) and len(v)>=2 and v not in R13_ACCENT_SKIP)
        people.add("다람")
        places=set(v for v in getattr(store,"R13_MAP_LABELS",{}).values() if isinstance(v,str) and len(v)>=2)
        return people,places-people

    def _r13_accent_span(word,color):
        return "{font="+R13_ACCENT_FONT+"}{color="+color+"}"+word+"{/color}{/font}"

    # 2026-10-28 소유자(역전재판 캡처 다섯 장): 「한 가지 색을 정하자. 볼드 처리하지 말고. 어두운 빨간색 같은 걸로.
    # 이름마다 체크하는 게 아니라, 쌍따옴표에 들어갈 단어를 강조할 때 쓰는 것으로 규칙을 바꾸고」.
    # 규칙: “인용” · "인용" · 【핵심어】 만 어두운 빨강으로(따옴표·괄호 포함, 굵기 그대로). 이름·장소 자동 색칠은 하지 않는다.
    # 아빠 생각(괄호, 파랑) 안에서도 인용은 빨강이다(레퍼런스: 생각 속 “눈이 자국을 지웠다”).
    R13_QUOTE_COLOR="#8E2A22"
    _R13_QUOTE_RE=_r13_na_re.compile(r'(“[^”{}]+”|"[^"{}]+"|【[^】{}]+】)')
    def r13_name_accent(text):
        if not R13_NAME_ACCENT_ON or not isinstance(text,str):return text
        parts=_r13_na_re.split(r"(\{[^{}]*\}|\[[^\[\]]*\])",text)
        out=[]
        for p in parts:
            if not p:continue
            if p.startswith(("{","[")):out.append(p);continue
            out.append(_R13_QUOTE_RE.sub(lambda m:"{color="+R13_QUOTE_COLOR+"}"+m.group(1)+"{/color}",p))
        return "".join(out)

    _r13_accent_semantic=r13_semantic_text
    def r13_semantic_text(text,opening=True,closing=True):
        if R13_NAME_ACCENT_ON and getattr(store,"r13_thought_active",False) and isinstance(text,str):
            return "{color="+R13_ACCENT_COLORS["thought"]+"}"+r13_name_accent(_r13_accent_semantic(text,opening,closing))+"{/color}"
        if R13_NAME_ACCENT_ON and isinstance(text,str) and getattr(store,"room13_mode",False):
            return r13_name_accent(text)
        return _r13_accent_semantic(text,opening,closing)
