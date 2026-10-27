# 2026-10-27 14일 자동 플레이 4일 아침에서 드러난 것: 옛 MS14 모드(ms14_story.rpy, 0.20.73 에서 지움)가 등록하던
# 세 장소가 같이 빠져 「솜이네 골목」으로 이동하는 순간 R13_PLACES 에서 KeyError 가 났다. 새 이야기(4·5·9·11일)가 쓰는
# 세 곳만 되살린다(제목·배경은 옛 값 그대로). 지도 위치·이름표·방 안 배치는 room13_v111_later_bindings.rpy 에 그대로 있다.
# 별도 파일인 까닭: later_bindings 는 대사 연결표가 줄 번호를 들고 있어 줄을 늘리면 시험이 깨진다.
init 60 python:
    R13_PLACES.setdefault("ms14_somi",("솜이네 골목","winter"))
    R13_PLACES.setdefault("ms14_somi_inside",("솜이네 방","ep_somi_home"))
    R13_PLACES.setdefault("ms14_guardroom",("밝은 초소 안","winter"))
