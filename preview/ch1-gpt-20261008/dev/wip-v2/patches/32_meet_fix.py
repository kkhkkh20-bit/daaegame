# 회의 UI 검수(2026-10-10 에이전트 보고):
# 1) 연결 단계 증거를 낸 뒤 선택(.bl.on)이 남아, '끼어들기'를 누르면 이미 낸 증거가 다시 제시되어 감점되던 문제 → 단계가 넘어가면 선택을 푼다
rep('   var adv=function(){STEP.set(s,step+1);try{SFX.found()}catch(x){}queue(sp.lines)};',
    '   var adv=function(){STEP.set(s,step+1);try{var _on=document.querySelectorAll(".rt .rt-bul .bl.on");for(var _i=0;_i<_on.length;_i++)_on[_i].classList.remove("on");delete B.dataset.rtgsel}catch(x){}try{SFX.found()}catch(x){}queue(sp.lines)};')
# 2) 안내 문구 '…을(를) 쏴요' → 받침에 맞는 조사
rep("sel?'빛나는 말을 눌러 <b>'+esc(itemName(C,sel))+'</b>을(를) 쏴요'",
    "sel?'빛나는 말을 눌러 <b>'+esc(itemName(C,sel))+'</b>'+(function(w){var c=String(w||'').replace(/[^가-힣0-9]/g,'').slice(-1),k=c.charCodeAt(0);return (k>=0xAC00&&k<=0xD7A3)?((k-0xAC00)%28?'을':'를'):'을(를)'})(itemName(C,sel))+' 쏴요'")
# 연결 단계 뒤 안내 문구가 '방금 낸 증거를 쏴요'로 남던 것: 토론 모듈 안의 선택(sel)도 비운다
rep('  el.querySelectorAll("[data-bl]").forEach(function(b){b.onclick=function(){sel=b.dataset.bl;SFX.select();draw()}});',
    '  el.querySelectorAll("[data-bl]").forEach(function(b){b.onclick=function(){sel=b.dataset.bl;SFX.select();draw()}});window.__rtClearSel=function(){sel=null;try{draw()}catch(e){}};')
rep('for(var _i=0;_i<_on.length;_i++)_on[_i].classList.remove("on");delete B.dataset.rtgsel}catch(x){}',
    'for(var _i=0;_i<_on.length;_i++)_on[_i].classList.remove("on");delete B.dataset.rtgsel;window.__rtClearSel&&window.__rtClearSel()}catch(x){}')
