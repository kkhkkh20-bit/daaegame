# 통합 아트(2026-10-09) 방 연결
# 1) 도토의 방: 옛 사무실 벡터 장면(dark-office) 대신 BG_doto_room_pixel_v1(1672x941). 다른 방과 같은 1.8 비율로 위 929px를 쓴다
rep('reception_desk:{src:"art/ch1/bg/BG01_reception_panorama.png",w:2048,h:768,view:[520,100,900,500],note:"BG01 접수대 쪽(숙박부)"}',
    'reception_desk:{src:"art/ch1/bg/BG01_reception_panorama.png",w:2048,h:768,view:[520,100,900,500],note:"BG01 접수대 쪽(숙박부)"},doto_room:{src:"art/ch1/bg/BG_doto_room_pixel_v1.png",w:1672,h:941,view:[0,0,1672,929],note:"통합 아트 도토 방(가을 낮)"}')
rep(' EP.LOC_BG={front:"reception_desk",hall:"corridor"};',' EP.LOC_BG={front:"reception_desk",hall:"corridor",dotoroom:"doto_room"};')
# 2) C08 날씨 일지 지점: 이전 [250,110] 대신 새 방의 열린 노트 자리(원본 1188,465 → 360x200 단위)
rep('s_diary:[250,110]','s_diary:[256,100]')
# 3) 식당 카메라: 화면이 덜 넓을 때(640x360, 태블릿·데스크톱) 세로를 768까지 더 보여 줘서 한 번에 보이는 가로 폭을 1125px 이상으로(인물이 화면 끝에 반쯤 걸리지 않게). 844x390은 그대로
rep("if(k==='dining'){vh=520;vw=vh*w/h;x=pan*Math.max(0,2048-vw);y=140;s=h/vh}",
    "if(k==='dining'){vh=Math.min(768,Math.max(520,1125*h/w));vw=vh*w/h;x=pan*Math.max(0,2048-vw);y=Math.max(0,Math.min(768-vh,400-vh/2));s=h/vh}")
# 4) 창고 돈주머니 누르는 영역: 주머니 그림(보이는 57x65)보다 넉넉하게 — 이불·베개 쪽으로 빗나간 탭도 주머니로
rep("bed13:{C01:[1219,335,58,65]","bed13:{C01:[1219,338,96,96]")
