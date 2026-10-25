# 2026-10-25 납품 불타는 밤 배경. 등록만 하며 사건·장소·공개 조건은 만들지 않는다.
init 166 python:
    R13_WILD_NIGHT_BACKGROUNDS = {
        "wild_school_classroom":"assets/wild-night/wild-school-classroom-night.webp",
        "wild_school_hall":"assets/wild-night/wild-school-hall-night.webp",
        "wild_square_burning":"assets/wild-night/wild-square-burning.webp",
        "wild_road_mouth":"assets/wild-night/wild-road-mouth-night.webp",
        "wild_greenhouse":"assets/wild-night/wild-greenhouse-night.webp",
        "wild_village_dawn":"assets/wild-night/wild-village-dawn-ash.webp",
    }
    R13_WILD_NIGHT_REVIEW_KEYS = ("wild_school_hall","wild_road_mouth","wild_greenhouse","wild_village_dawn")

    def r13_wild_night_background(key):
        path=r13_asset_path("file:"+R13_WILD_NIGHT_BACKGROUNDS[key])
        iw,ih=renpy.image_size(path)
        zoom=max(1280.0/iw,720.0/ih)
        # 같은 비율로 확대하고 무대 중앙1280×720을 표시한다.
        return Crop((int((iw*zoom-1280)/2),int((ih*zoom-720)/2),1280,720),Transform(path,zoom=zoom,nearest=True))

    _r13_before_wild_night_background=r13_background
    def r13_background(key):
        if key in R13_WILD_NIGHT_BACKGROUNDS:return r13_wild_night_background(key)
        return _r13_before_wild_night_background(key)
