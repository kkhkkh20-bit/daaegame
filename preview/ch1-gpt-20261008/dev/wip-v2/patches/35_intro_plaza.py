# 도입 재배치(2026-10-10 사용자 확정)에 따른 엔진 쪽 최소 수정
# (프롤로그 배경은 build.py가 순번 지정 줄을 이미 지우고 장면별 B(배경)을 쓰므로 따로 고치지 않음)
# 2) 광장 배경/이동은 유지. 사진보다 먼저 암시하던 노인/목걸이 장면은
# 2026-10-10 사용자 피드백으로 제거했으므로 재방문 callback도 만들지 않는다.
rep(' EP.LOC_BG={front:"reception_desk",hall:"corridor",dotoroom:"doto_room"};',
    ' EP.LOC_BG={front:"reception_desk",hall:"corridor",dotoroom:"doto_room",plaza:"plaza"};')
rep('  map:{bed13:[300,40,"box"],hall:[220,60,"hall"],dining:[150,110,"hall"],kitchen:[80,90,"door"],dotoroom:[280,120,"door"],front:[150,170,"post"],\n   roads:[["front","dining"],["dining","kitchen"],["dining","hall"],["hall","bed13"],["hall","dotoroom"]],deco:"night"},',
    '  map:{bed13:[300,40,"box"],hall:[220,60,"hall"],dining:[150,110,"hall"],kitchen:[80,90,"door"],dotoroom:[280,120,"door"],front:[150,170,"post"],plaza:[40,170,"post"],\n   roads:[["front","dining"],["dining","kitchen"],["dining","hall"],["hall","bed13"],["hall","dotoroom"],["front","plaza"]],deco:"night"},')
# 전체 지도: 광장 노드를 이번 사건의 광장 장소에 연결
rep('  inn:{bed13:"inn",dining:"inn",kitchen:"inn",hall:"inn",dotoroom:"inn",front:"inn"}};',
    '  inn:{bed13:"inn",dining:"inn",kitchen:"inn",hall:"inn",dotoroom:"inn",front:"inn",plaza:"plaza-fountain"}};')
