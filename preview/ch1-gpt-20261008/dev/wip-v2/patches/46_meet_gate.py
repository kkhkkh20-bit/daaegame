# 2026-10-10 v2: 회의 진입 최소 조건(C01~C04)에서 '열까요' 물음이 뜨는 것은 유지하되,
# 주민 소집 장면(I9: "그럼 시작하겠습니다")은 플레이어가 회의를 고른 뒤에만 재생한다.
# 이전에는 물음보다 I9가 먼저 나와, '조금 더 조사하기'를 고르면 이미 시작된 회의를 두고 조사로 돌아가는 모순이 생겼다.
rep("function open(c,spec){if(el&&el.isConnected",
    'function open(c,spec){if(window.__innPreOpen&&window.__innPreOpen(c,spec,open))return;if(el&&el.isConnected')
rep('else if(lines[0]&&String(lines[0][1]||"").indexOf("증거가 꽤 모였어")>=0&&!bt("inn_i9")){setb("inn_i9");window.__innCutting=true;play(EP.I9,function(){window.__innCutting=false;done&&done()});return}',
    '/* I9는 회의를 고른 뒤(__innPreOpen)에 재생 */')
rep('["det0","좋다. 모두 한자리에 모아 원탁 회의를 열자."]','["det0","정오까지는 아직 시간이 있다."]')
