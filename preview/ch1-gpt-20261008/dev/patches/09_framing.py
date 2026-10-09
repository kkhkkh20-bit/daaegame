# 구도(2026-10-09 실기기 피드백 "배경이 너무 확대, 인물이 거인"): 현관 대화 장면의 잘라 보기 범위를 넓혀 문·카운터·바닥이 읽히게 한다.
# 조사 화면 '접수대'(reception_desk)는 조사 지점 좌표가 기존 범위에 맞춰져 있으므로 그대로 두고, 대화용 넓은 범위는 별도 키로 둔다.
rep('view:[0,100,900,500],note:"BG01 현관 쪽(문)"','view:[0,90,1300,600],note:"BG01 현관 쪽(문·카운터 일부·바닥)"')
rep('  reception_desk:{src:"art/ch1/bg/BG01_reception_panorama.png",w:2048,h:768,view:[520,100,900,500],note:"BG01 접수대 쪽(숙박부)"}',
    '  reception_desk:{src:"art/ch1/bg/BG01_reception_panorama.png",w:2048,h:768,view:[520,100,900,500],note:"BG01 접수대 쪽(숙박부)"},\n  reception_desk_wide:{src:"art/ch1/bg/BG01_reception_panorama.png",w:2048,h:768,view:[420,90,1300,600],note:"BG01 접수대 쪽 넓게(P4 대화)"}')
