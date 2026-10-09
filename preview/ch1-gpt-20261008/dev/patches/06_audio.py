# 오디오: 1장 전용 음악 선택(__innWant)·덕킹(__innDuck)·콜드 오픈 도입곡·타이핑음 교체·옛 환경음(사무소 시계 똑딱) 차단
rep('  if(window.__innAudioHold)return null;\n  if(!S.sound)return null;',
    '  if(window.__innAudioHold)return window.__innColdMus||null;\n  if(!S.sound)return null;\n  if(window.__innWant){var _iw=window.__innWant();if(_iw!==undefined)return _iw}')
rep('  if(window.__innAudioHold)d=0;A.duck=d;',
    '  if(window.__innDuck){try{d*=window.__innDuck(d)}catch(e){}}if(window.__innAudioHold&&!window.__innColdMus)d=0;A.duck=d;')
# 옛 환경음 체계: 1장 화면(타이틀·콜드 오픈·여관 사건)에서는 끈다. 제목 화면의 사무소 시계(1초 똑딱)가 콜드 오픈 밑에 깔리던 원인
rep(' function ambKey(){\n  if(!AC||!S.sound)return "";',
    ' function ambKey(){\n  if(!AC||!S.sound)return "";\n  if(window.__innOwnAmb&&window.__innOwnAmb())return "";')
# 콜드 오픈 글자음: 글자마다 520Hz 사각파 '틱' -> 공용 부드러운 타이핑음(간격 제한)
rep('  function tick(ch){\n   if(!coldAudioReady||ended||document.hidden||!SET.sfxVolume||/\\s/.test(ch)||!S.sound)return;',
    '  function tick(ch){\n   if(!coldAudioReady||ended||document.hidden||!SET.sfxVolume||/\\s/.test(ch)||!S.sound)return;\n   if(window.__innType){window.__innType("cold");return}')
# 콜드 오픈: 어두운 도입곡(inn_cold) -> 끝나면 즉시 정리 -> 최소 0.9초 암전 -> 마차 첫 프레임에 여행곡·마차 소리
rep('function cold(done){window.__innAudioHold=true;','function cold(done){window.__innAudioHold=true;window.__innColdMus="inn_cold";')
rep('  function end(){if(ended)return;ended=true;transitioning=true;clearTimeout(waitT);stopTyping();',
    '  function end(){if(ended)return;ended=true;transitioning=true;clearTimeout(waitT);stopTyping();var endT=Date.now();window.__innColdMus=null;try{window.__AUD&&__AUD.tick&&__AUD.tick()}catch(e){}')
rep('    if(!bgReady||!scene||scene.key!=="carriage"){revealFrame=requestAnimationFrame(reveal);return}',
    '    if(!bgReady||!scene||scene.key!=="carriage"||Date.now()-endT<900){revealFrame=requestAnimationFrame(reveal);return}')
