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
