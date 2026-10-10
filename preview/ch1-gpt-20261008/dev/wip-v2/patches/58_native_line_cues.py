# A native line owns its votes and audio cue. Reading the rendered bubble on a
# timer could miss the first short line when the player advanced quickly.
rep('function applyLine(){var L=Q&&Q[qi];if(!L)return;addSus(L.s);',
    'function applyLine(){var L=Q&&Q[qi];if(!L)return;if(C&&C.id==="inn"&&window.__innNativeLine)window.__innNativeLine(L);addSus(L.s);')
rep(' var lastLine=null;\n function onLine()',
    ' var lastLine=null;\n window.__innNativeLine=function(L){if(Q||L===lastLine)return;lastLine=L;meta(L)};\n function onLine()')
