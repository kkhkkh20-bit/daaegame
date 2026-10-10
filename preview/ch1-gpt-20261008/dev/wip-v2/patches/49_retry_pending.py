# 초기화 전 대기열/선택지 예약이 새 회의에 끼어들지 않도록 세대를 구분한다.
rep('if(ANS)ANS.clear();if(window.__innAudioReset)',
    'ASKGEN++;clear();lastLine=null;if(ANS)ANS.clear();if(window.__innAudioReset)')
rep(' var ANS=new Set();', ' var ANS=new Set(),ASKGEN=0;')
rep('function askOpen(L){if(ANS.has(L)||PK)return;setTimeout(function(){if(ANS.has(L)||PK||!rt())return;',
    'function askOpen(L){if(ANS.has(L)||PK)return;var gen=ASKGEN;setTimeout(function(){if(gen!==ASKGEN||ANS.has(L)||PK||!rt())return;')
rep('function wrongAsk(L,w){var was=', 'function wrongAsk(L,w){var gen=ASKGEN;var was=')
rep('ANS.add(L);setTimeout(function(){try{window.__innFail&&window.__innFail(fin)}',
    'ANS.add(L);setTimeout(function(){if(gen!==ASKGEN)return;try{window.__innFail&&window.__innFail(fin)}')
rep('setTimeout(function(){queue(w&&w.length?w:',
    'setTimeout(function(){if(gen!==ASKGEN)return;queue(w&&w.length?w:')
