# 2026-10-27 검수: 등록 뒤 지도로 여관에 먼저 간 경우의 초소 대사 자리(room13_v111_days123.rpy registered_depart 가 부른다).
init 319 python:
    def r13_v111_depart_from_booth():
        """2026-10-27 검수(p11 캡처): 등록 뒤 지도에서 「여관 접수대」로 가면 r13_v111_wait 가 장소를 먼저 여관으로 바꾸고
        registered_depart 갈래로 돌아와, 초소 장면(너울이 초소로 들어온다)이 여관 배경 위에 나왔고 돌목·까로까지 여관에
        서 있었다. 초소 대사는 초소에서 한다 — 지도로 왔으면 초소로 되돌려 말하고, 그 뒤 r13_v111_inn 이 여관으로
        바로 데려간다(v111_depart_direct: 이미 고른 길이라 다시 묻지 않는다). renpy.call 은 이 함수 뒤 문장으로 돌아온다."""
        direct=store.room13["location"]!="gate"
        store.v111_depart_direct=direct
        if direct:
            r13_edit(location="gate")
            renpy.call("r13_scene",R13_PLACES["gate"][1],R13_PLACES["gate"][0],"calm")
