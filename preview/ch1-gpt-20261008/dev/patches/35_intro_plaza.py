# 도입 재배치(2026-10-10 사용자 확정)에 따른 엔진 쪽 최소 수정
# (프롤로그 배경은 build.py가 순번 지정 줄을 이미 지우고 장면별 B(배경)을 쓰므로 따로 고치지 않음)
# 2) 조사 중 광장: 기존 광장 배경(EP.BGS.plaza) 재사용, 첫 방문 일회 이벤트(목걸이를 본 노인, 도입 P2에서 옮김). 재방문 때 다시 나오지 않음(G.beats)
rep(' EP.LOC_BG={front:"reception_desk",hall:"corridor",dotoroom:"doto_room"};',
    ' EP.LOC_BG={front:"reception_desk",hall:"corridor",dotoroom:"doto_room",plaza:"plaza"};\n try{BEATS.inn=BEATS.inn||{};BEATS.inn["loc:plaza"]=[["narr","긴 옷을 입은 노인이 걸음을 멈추고 다람의 목걸이를 바라본다."],["narr","노인은 말없이 고개를 돌려 골목으로 사라진다."],["det1","아빠, 저 할아버지가 내 목걸이 봤어. 그치?"],["det0","…응. 잠깐 보셨네."],["narr","(목걸이를 아는 분이었을까. 마음에 걸리지만, 지금은 여관 일이 먼저다.)"]]}catch(e){}')
rep('  map:{bed13:[300,40,"box"],hall:[220,60,"hall"],dining:[150,110,"hall"],kitchen:[80,90,"door"],dotoroom:[280,120,"door"],front:[150,170,"post"],\n   roads:[["front","dining"],["dining","kitchen"],["dining","hall"],["hall","bed13"],["hall","dotoroom"]],deco:"night"},',
    '  map:{bed13:[300,40,"box"],hall:[220,60,"hall"],dining:[150,110,"hall"],kitchen:[80,90,"door"],dotoroom:[280,120,"door"],front:[150,170,"post"],plaza:[40,170,"post"],\n   roads:[["front","dining"],["dining","kitchen"],["dining","hall"],["hall","bed13"],["hall","dotoroom"],["front","plaza"]],deco:"night"},')
# 전체 지도: 광장 노드를 이번 사건의 광장 장소에 연결
rep('  inn:{bed13:"inn",dining:"inn",kitchen:"inn",hall:"inn",dotoroom:"inn",front:"inn"}};',
    '  inn:{bed13:"inn",dining:"inn",kitchen:"inn",hall:"inn",dotoroom:"inn",front:"inn",plaza:"plaza-fountain"}};')
