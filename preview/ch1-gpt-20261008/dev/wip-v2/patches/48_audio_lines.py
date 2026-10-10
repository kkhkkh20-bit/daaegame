# 원탁 대사는 DL이 아니라 엔진 Q/확장 Q에 있으므로 오디오에 실제 대사 객체를 전달한다.
rep(' function meta(L){if(!L)return;\n',
    ' function meta(L){if(!L)return;\n  if(window.__innAudioLine)window.__innAudioLine(L);\n')
rep('if(L)meta(L);else if(!Q)showEv(null)',
    'if(L)meta(L);else if(!Q){showEv(null);if(window.__innAudioLine)window.__innAudioLine(null)}')
rep(' function clear(){[CLK,TAL,QEL,SHOW]',
    ' function clear(){if(window.__innAudioLine)window.__innAudioLine(null);[CLK,TAL,QEL,SHOW]')
rep('if(ANS)ANS.clear();FAILP=false;',
    'if(ANS)ANS.clear();if(window.__innAudioReset)window.__innAudioReset();FAILP=false;')

# 확장 대기열이 말하는 동안 숨은 엔진 대사가 오디오 큐를 덮지 않게 한다.
rep('function onLine(){var L=curLine();', 'function onLine(){if(Q)return;var L=curLine();')
rep('if(QI>=Q.length){Q=null;', 'if(QI>=Q.length){Q=null;lastLine=null;')
