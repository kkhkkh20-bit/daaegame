# Pretendard is the approved face. Only two UI symbols need a fallback.
init -100 python:
    R13_UI_FONT = (FontGroup()
        .add(r13_asset_path("font.symbols"), 0x21c6, 0x21c6)
        .add(r13_asset_path("font.symbols"), 0x25b8, 0x25b8)
        .add(r13_asset_path("font.body","regular"), None, None))
    R13_UI_BOLD_FONT = (FontGroup()
        .add(r13_asset_path("font.symbols"), 0x21c6, 0x21c6)
        .add(r13_asset_path("font.symbols"), 0x25b8, 0x25b8)
        .add(r13_asset_path("font.bold","bold"), None, None))

    # 화면과 에셋이 함께 참조하는 역할별 타이포 규격.
    R13_UI_TYPE = {
        "title": dict(font=R13_UI_BOLD_FONT, size=30, line_spacing=5),
        "name": dict(font=R13_UI_BOLD_FONT, size=27, line_spacing=4),
        "button": dict(font=R13_UI_BOLD_FONT, size=22, line_spacing=4),
        "dialogue": dict(font=R13_UI_BOLD_FONT, size=29, line_spacing=4),
        "help": dict(font=R13_UI_FONT, size=20, line_spacing=3),
    }
