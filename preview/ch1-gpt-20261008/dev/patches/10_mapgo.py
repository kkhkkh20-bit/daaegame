# 전체 지도 '이동': 실기기(iPhone)에서 방을 고르고 이동을 눌렀는데 여관 내부 지도에 머무는 사례(2026-10-09 사용자 직접 QA).
# 합성 클릭이 닿지 않은 경우를 대비해, 잠시 뒤에도 같은 지도 화면이면 같은 이동 처리를 직접 실행한다(정상 경로는 그대로).
rep('var i=ROOM;SEL=null;ROOM=null;close();g.dispatchEvent(new MouseEvent("click",{bubbles:true}))}})}',
    'var i=ROOM;SEL=null;ROOM=null;close();var gg=document.querySelector(\'.fsmap g.mvp[data-mvp="\'+i+\'"]\')||g;gg.dispatchEvent(new MouseEvent("click",{bubbles:true}));\n     setTimeout(function(){try{if(G&&G.tab==="move"&&G.loc!==i){var c=CASES[G.ci];if(!locOpen(c,i))return;var p=mapP(c,i);G.tab="scene";moveTo(c,i,[p[0],p[1]-14]);MISS.push("wmap go fallback "+i)}}catch(x){}},160)}})}')
