# 대화 화면 그림 동기화: 엔진 hiSwap과 inn_ui9 talkFrame이 서로 다른 그림을 번갈아 넣어 깜빡이던 문제(2026-10-10 확인).
# 1장 행동 포즈(또는 세련 앉은 그림)가 있으면 hiSwap도 같은 그림을 쓴다 — 모든 인물에 적용
rep('''    var k=im.dataset.k,P=window.__PORT[k],pixel=''','''    var k=im.dataset.k;try{var pz=(window.__innPose&&window.__innPose(k))||(k==="seryeon"&&G&&CASES[G.ci]&&CASES[G.ci].id==="inn"?"art/ch1/cast/seryeon-seated-paperwork-v2-talk.png":null);if(pz){if(im.getAttribute("src")!==pz)im.setAttribute("src",pz);im.classList.remove("hires");im.classList.add("innpixel");return}}catch(e){}
    var P=window.__PORT[k],pixel=''')
