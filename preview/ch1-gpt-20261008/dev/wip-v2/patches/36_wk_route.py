# 회의 판정 경로 통일(2026-10-10 dot QA 9006023): 빛나는 말(.wk)을 직접 누르거나 '끼어들기'로 내면 단계 판정(연결 단계·순서·감점 없는 반응)을 건너뛰고
# 엔진 최종 판정으로 바로 가서, 1라운드 나비 ②에 C02(하얀 손자국)를 내면 '헛짚었다'가 됐다. '제시하기' 단추만 단계 판정을 거쳤다.
# → 세 경로 모두 '제시하기'와 같은 판정(문서 캡처 단계 판정 → 엔진 판정)을 거치게 한다.
# 1) 제시하기 → 엔진 판정으로 넘길 때만 빛나는 말 클릭을 통과시키는 표시
rep('   if(g==="present"){var s0=r.querySelector(".rt-bul .bl.on");if(!s0)return;B.classList.remove("rtg-drw");delete B.dataset.rtgsel;var w0=r.querySelector(".rt-bub.stm .wk");if(w0)w0.click();return}',
    '   if(g==="present"){var s0=r.querySelector(".rt-bul .bl.on");if(!s0)return;B.classList.remove("rtg-drw");delete B.dataset.rtgsel;var w0=r.querySelector(".rt-bub.stm .wk");if(w0){window.__rtgWkPass=1;try{w0.click()}finally{window.__rtgWkPass=0}}return}')
# 2) 끼어들기(증거를 고른 상태): 제시하기 단추와 같은 길로
rep('    B.classList.remove("rtg-drw");var w=r.querySelector(".rt-bub.stm .wk");if(w)w.click()}}',
    '    var pb=BAR.querySelector(\'[data-g="present"]\');if(pb&&!pb.disabled){pb.click();return}B.classList.remove("rtg-drw");var w=r.querySelector(".rt-bub.stm .wk");if(w){window.__rtgWkPass=1;try{w.click()}finally{window.__rtgWkPass=0}}}}')
# 3) 빛나는 말 직접 클릭(증거를 고른 상태): 가로채서 제시하기 단추로 보낸다. 증거를 안 골랐으면 엔진 안내 그대로
rep(' window.__rtgPick=function(){return !!PK};',
    ' window.__rtgPick=function(){return !!PK};\n document.addEventListener("click",function(e){var w=e.target.closest&&e.target.closest(".rt .rt-bub.stm .wk");if(!w||window.__rtgWkPass)return;if(!document.querySelector(".rt .rt-bul .bl.on"))return;\n  var pb=document.querySelector(\'#rtgbar [data-g="present"]\');if(!pb||pb.disabled)return;e.stopImmediatePropagation();e.preventDefault();pb.click()},true);')
