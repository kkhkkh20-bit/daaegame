# Same adopted Daram outfit and explicit Neoul emotions in the native council.
rep('var nv=/fluster|rebuttal/.test(exprOf(m,"0"))?"neoul-admonish-profile":"neoul-default-profile";',
    'var nv="neoul-"+(window.__innNeoState?window.__innNeoState(m,""):"default")+"-profile";')
rep('var f=k==="det1"?"daram-front":k==="karo"?"karo-front":',
    'if(k==="det1"){var dm=window.__innDV4?window.__innDV4(m):"idle-t0";return \'<img alt="" class="sf innpixel" draggable="false" src="art/ch1/daram-v4/daram-\'+dm.replace("idle-t0","idle")+\'-profile.png">\'}var f=k==="karo"?"karo-front":')
rep('function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="wanggu")',
    'function figHtml(k,m){if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="innma"&&window.__innGrandmaSrc){return \'<img alt="" class="sf innpixel" draggable="false" src="\'+window.__innGrandmaSrc(m)+\'">\'}if(G&&CASES[G.ci]&&CASES[G.ci].id==="inn"&&k==="wanggu")')
# A rendered pf() image normalizes smile/sad to happy/neutral. Preserve the
# authored emotion from the actual native or objection queue instead.
rep('function applyLine(){var L=Q&&Q[qi];if(!L)return;',
    'window.__innNativeActingLine=function(){return Q&&Q[qi]||null};\n function applyLine(){var L=Q&&Q[qi];if(!L)return;')
rep('function curLine(){var p=ph(),b=',
    'window.__rtActingLine=function(){return Q&&Q[QI]||(window.__innNativeActingLine&&window.__innNativeActingLine())||curLine()||curStm()};\n function curLine(){var p=ph(),b=')
rep('function moodOf(r){var g=r.querySelector(".rt-big g[id^=\'an-\']");',
    'function moodOf(r){try{var l=window.__rtActingLine&&window.__rtActingLine();if(l)return window.__innMood?window.__innMood(l):(l.m||"")}catch(e){}var g=r.querySelector(".rt-big g[id^=\'an-\']");')
rep('var m=k===spk?mood:(d[k]>0?"nervous":"");var want=figHtml(k,m)',
    'var m=k===spk?mood:(d[k]>0?"nervous":"");s.dataset.mood=m;var want=figHtml(k,m)')
