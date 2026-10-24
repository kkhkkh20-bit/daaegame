# Pretendard is the approved face. Only two UI symbols need a fallback.
init -100 python:
    R13_UI_FONT = (FontGroup()
        .add("assets/Galmuri11.ttf", 0x21c6, 0x21c6)
        .add("assets/Galmuri11.ttf", 0x25b8, 0x25b8)
        .add("assets/Pretendard-Regular.otf", None, None))
