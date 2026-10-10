# 회의/최종 대결 재시작: 이전 시도의 정답 선택 기록을 지운다.
# ANS가 남으면 같은 대본 객체의 ask가 이미 답한 것으로 취급되어 선택지가 생략된다.
rep('window.__rtgReset=function(){STEP=new Map();PRESSED=new Set();MARK={};FAILP=false;LW=null;LH=null};',
    'window.__rtgReset=function(){STEP=new Map();PRESSED=new Set();MARK={};if(ANS)ANS.clear();FAILP=false;LW=null;LH=null};')
# 마지막 오답 뒤 실패 연출을 기다리는 동안 같은 선택지가 다시 열리지 않게 한다.
# 재시작 때 위 초기화가 이 임시 기록도 지우므로 다음 시도의 질문은 정상 표시된다.
rep('  if(was<=1){setTimeout(function(){try{window.__innFail&&window.__innFail(fin)}catch(e){MISS.push("askfail "+e.message)}},900);return}',
    '  if(was<=1){ANS.add(L);setTimeout(function(){try{window.__innFail&&window.__innFail(fin)}catch(e){MISS.push("askfail "+e.message)}},900);return}')
