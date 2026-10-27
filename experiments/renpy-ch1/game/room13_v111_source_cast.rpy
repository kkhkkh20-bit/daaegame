# 새 세계(v111) 대사 원본(MS14 기록)의 화자 이름 → 인물 키, 원본 그림 등록. 2026-10-27 옛 MS14 시험판
# 실행기(ms14_story.rpy)를 지우면서 새 게임이 계속 쓰는 자료만 여기로 옮겼다.
# ms14 변수는 옛 시험판 상태였다. 새 판은 늘 None 이고 시험이 그것을 단언하므로 기본값만 남긴다.
default ms14 = None

init 220 python:
    MS14_ART = json.load(renpy.file("ms14/art.json"))
    # dev/match_ms14_expressions.py·test_newworld_text.py 가 이 사전을 글자로 읽는다. 줄 모양을 바꾸지 않는다.
    MS14_SPEAKERS = {"아빠":"dad", "다람":"daram", "까로":"karo", "돌목":"guard",
        "너울":"neoul", "할머니":"granny", "초롱":"resident_lamplighter", "세련":"seryeon",
        "모모":"resident_momo", "피코":"resident_piko", "나비":"nabi", "네로":"resident_nero",
        "톡":"resident_tok", "부리":"buri", "우박":"resident_ubak", "실룩":"resident_siluk",
        "백 부인":"resident_madam", "바둑이":"resident_badook", "솜이":"resident_somi",
        "콩이":"resident_kongi","토실":"resident_tosil","밤이":"bami","무쇠":"resident_musoe",
        "진료 담당자":"ms14_clinician","종업원":"ms14_attendant"}
    R13_CHARS["ms14_clinician"] = Character("진료 담당자")
    R13_CHARS["ms14_attendant"] = Character("종업원")
