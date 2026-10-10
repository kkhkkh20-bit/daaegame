# 설정 배경음 실시간(2026-10-10 사용자 "바에서 조절할 때 저장 안 눌러도 바로 줄어들게"): 슬라이더는 이미 바로 바꾸고 있었지만,
# 소리를 낼 때마다 불리는 ac() 감싸기가 저장값(SET)으로 곧바로 되돌려 효과가 없었다 → 조정 중(창 열림) 값(__volLive)을 우선, 닫거나 저장하면 해제
rep(' try{var _ac=ac;ac=function(){var a=_ac.apply(this,arguments);gains(SET);return a}}catch(e){MISS.push("ac")}',
    ' try{var _ac=ac;ac=function(){var a=_ac.apply(this,arguments);gains(window.__volLive||SET);return a}}catch(e){MISS.push("ac")}')
rep('gains({musicVolume:W.musicVolume,sfxVolume:W.sfxVolume});if(k==="sfxVolume"){var _n=Date.now();',
    'window.__volLive={musicVolume:W.musicVolume,sfxVolume:W.sfxVolume};gains(window.__volLive);if(k==="sfxVolume"){var _n=Date.now();')
rep('  function shut(){clearInterval(pvT);gains(SET);',
    '  function shut(){clearInterval(pvT);window.__volLive=null;gains(SET);')
# 배경음 전체를 조금 작게(사용자 "효과음이 묻힌다"): 음악 버스 기준값 0.25 → 0.19(약 -2.4dB). 설정 슬라이더 값은 그대로
rep(' var MBASE=.25;',' var MBASE=.19;   /* 2026-10-10 사용자: 배경음 전체를 조금 작게(효과음이 묻힘). 이전 .25(patches/13) */')
