# 회의 진행 차단(2026-10-10 dot QA, 9d91bbb): 회의 대화 중 '증거 보기'로 연 사건 기록 창(z58)이 회의 화면(.rt, z60) 아래에 깔려
# 닫기·탭이 모두 회의 화면에 먹히고, 기록 창 안의 '원탁 회의 열기'도 회의 중에 보였다. 토론이 시작돼도 기록 창이 남아 증거 서랍 대신 기록 창만 보였다.
# 1) 회의 중 '증거 보기': 열린 기록 창이 있으면 먼저 닫는다. 토론이면 증거 서랍을 연다(기록 창을 다시 열지 않음)
rep('   if(g==="ev"){if(deb&&!talk){B.classList.toggle("rtg-drw");sync();return}',
    '   if(g==="ev"){var _cr=document.querySelector(".crec2");if(_cr){var _cx=_cr.querySelector(".cr-x");if(_cx)_cx.click();if(document.querySelector(".crec2"))_cr.remove()}\n    if(deb&&!talk){if(_cr)B.classList.add("rtg-drw");else B.classList.toggle("rtg-drw");sync();return}if(_cr){sync();return}')
# 2) 회의가 열려 있으면 기록 창에 '원탁 회의 열기'를 두지 않는다(같은 회의를 두 번 여는 길 차단)
rep('  if(typeof G==="undefined"||!G||G.result)return;var c=CASES[G.ci];var D=window.DEBATE&&DEBATE[c.id];',
    '  if(typeof G==="undefined"||!G||G.result||document.querySelector("body>.rt"))return;var c=CASES[G.ci];var D=window.DEBATE&&DEBATE[c.id];')
# 3) 실제 원인(dot 새 게임 재현): «원탁 회의를 열까요?»의 열기(tomeet)가 0.25초 뒤 회의를 자동으로 여는데, 그 사이 그려진 소개 화면의
#    '원탁 회의 열기'(rtgo)를 한 번 더 누르면 회의 화면(.rt)이 두 장 생겼다. 앞 장은 M0 대화(너울)에 멈춘 채 남고, 하단 단추는 앞 장 기준으로
#    계산돼 끼어들기 꺼짐·증거 보기=일반 기록 창이 됐다. → 같은 회의가 이미 열려 있으면 다시 열지 않고, 다른 회의를 열 때는 남은 화면을 지운다
rep(' function open(c,spec){C=c;Q=null;',
    ' function open(c,spec){if(el&&el.isConnected&&window.__inMeeting&&C===c&&SPEC===(spec||DEBATE[c.id]))return;C=c;Q=null;')
rep('  el=document.createElement("div");el.className="rt";document.body.appendChild(el);',
    '  try{document.querySelectorAll("body>.rt").forEach(function(o){o.remove()})}catch(e){}el=document.createElement("div");el.className="rt";document.body.appendChild(el);')
