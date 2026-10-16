# New village places (0.18.63, owner 2026-10-15): 큰 강, 깊은 숲, 장터.
# Basis: docs/ART_REQUEST_01854_PLACES.md (owner decision: river = fishing, forest = hunting,
# market) and the approved v3 wide art (art/new-maps-v3-20261015, time slots in
# art/new-maps-time9-20261015). The pictures are the approved 2172x724 3:1 compositions shown at
# 2160x720 (room13-world-layout.json); the old 2048x768 request layout is not used.
#
# Only places and what is visible in them are added. No story, event, clue, unlock, job or
# schedule: residents are not moved here until the owner chooses which time slots move
# (01854 says "some library / lower road / home slots" without naming them), fishing and
# hunting are not jobs, and the ancient stone facility is not connected (no entry or unlock
# decided). The places open with the inn's other rooms (after lodging).
init 57 python:
    R13_NEW_PLACES=("river","forest","market")
    R13_PLACES.update({
        "river":("마을 아래 · 큰 강가","r13_river"),
        "forest":("마을 서쪽 · 길 없는 숲","r13_forest"),
        "market":("여관 앞 · 장터","r13_market"),
    })
    def _r13_place_object(rect,text):
        return dict(rect=list(rect),text=text,need=[],give=[],flags=[])
    # Rects are placeholders here; room13-world-layout.json holds the wide-picture rects (init 62).
    ROOM13["objects"].setdefault("river",{}).update({
        "river_reeds":_r13_place_object((10,410,160,250),"눈 덮인 둑에 마른 갈대가 꺾여 있다. 바람이 불 때마다 얼음 가루가 떨어진다."),
        "river_rocks":_r13_place_object((162,529,195,80),"강둑의 검은 바위들이 반쯤 눈에 묻혀 있다. 물가 쪽은 얼음이 얇다."),
        "river_ice":_r13_place_object((1437,632,330,70),"강가에 떠밀려 온 얼음판이 겹쳐 있다. 밟으면 깨질 것 같다."),
        "river_water":_r13_place_object((700,300,700,200),"넓은 강이 천천히 흐른다. 가운데는 얼지 않았다."),
        "river_cliffs":_r13_place_object((1717,151,227,119),"건너편 기슭에 눈 덮인 절벽과 전나무가 늘어서 있다."),
    })
    ROOM13["objects"].setdefault("forest",{}).update({
        "forest_roots":_r13_place_object((108,454,650,194),"굵은 뿌리가 눈 위로 드러나 서로 엉켜 있다. 길은 보이지 않는다."),
        "forest_trunk":_r13_place_object((194,0,281,454),"아름드리 전나무 줄기에 눈이 들러붙어 있다."),
        "forest_rock":_r13_place_object((1134,605,140,65),"눈에 반쯤 묻힌 바위가 있다."),
        "forest_branches":_r13_place_object((1274,0,346,324),"낮게 드리운 전나무 가지에 눈이 무겁게 얹혀 있다."),
    })
    ROOM13["objects"].setdefault("market",{}).update({
        "market_produce":_r13_place_object((594,389,335,86),"채소와 과일 바구니가 놓인 노점이다. 양배추와 사과가 쌓여 있다."),
        "market_oven":_r13_place_object((432,324,108,108),"노점 안쪽 화덕에 불이 지펴져 있다."),
        "market_firewood":_r13_place_object((335,443,173,151),"노점 옆에 장작이 가지런히 쌓여 있다."),
        "market_cheese":_r13_place_object((1210,346,356,162),"치즈 덩이와 매달아 둔 고기를 파는 노점이다."),
        "market_cloth":_r13_place_object((1728,400,216,108),"털실과 천이 색깔별로 쌓인 노점이다."),
        "market_pots":_r13_place_object((2030,367,119,140),"항아리와 그릇이 선반에 놓여 있다."),
    })

init 99 python:
    R13_OBJECT_NAMES.update({
        "river_reeds":"마른 갈대","river_rocks":"강둑 바위","river_ice":"얼음판","river_water":"강물","river_cliffs":"건너편 절벽",
        "forest_roots":"엉킨 뿌리","forest_trunk":"큰 전나무","forest_rock":"눈 속 바위","forest_branches":"전나무 가지",
        "market_produce":"채소 노점","market_oven":"노점 화덕","market_firewood":"장작 더미","market_cheese":"치즈·고기 노점",
        "market_cloth":"천 노점","market_pots":"그릇 선반",
    })
    R13_MAP_LABELS.update({"river":"큰 강","forest":"깊은 숲","market":"장터"})
