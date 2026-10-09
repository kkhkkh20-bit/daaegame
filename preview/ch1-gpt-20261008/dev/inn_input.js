 /* ==== 1장 입력 안정: 연타로 대화를 넘기다가 새로 나타난 질문·버튼·조사 지점이 바로 눌리지 않게 ====
    버튼·질문·조사 지점이 '눌릴 수 있게 보이기 시작한 시각'을 기록한다. 나타나기 전에 시작된 누름은 무시하고, 대화가 끝난 직후 나타난 것은 600ms 동안 입력을 받지 않는다.
    대화창 넘기기(타이핑 중 첫 입력=문장 완성, 다음 입력=다음 문장)는 엔진 규칙 그대로(220ms 이중 입력 방지 포함). */
 (function(){
  var SEL=".topic,#ov .modal .btn,#ov .modal button,#mveil .modal .btn,#mveil .modal button";   /* 질문·증거 카드 확인만. 조사 지점·인물은 힌트 포인터를 보고 바로 누를 수 있게 막지 않는다 */   /* 질문·조사 지점·증거 카드 확인만. 메뉴·레일·회의 버튼은 즉시 반응 */
  var AP=new WeakMap(),downT=0,live=new Set(),endT=-1e9;
  try{var _ed=endDlg;endDlg=function(){endT=performance.now();return _ed.apply(this,arguments)}}catch(e){}
  function inn(){try{return S.screen==="case"&&G&&CASES[G.ci]&&CASES[G.ci].id==="inn"}catch(e){return false}}
  function hittable(el){var r=el.getBoundingClientRect();if(r.width<4||r.height<4)return false;var x=r.left+r.width/2,y=r.top+r.height/2;
   if(x<0||y<0||x>innerWidth||y>innerHeight)return false;var h=document.elementFromPoint(x,y);return !!h&&(h===el||el.contains(h))}
  setInterval(function(){if(!inn()){live.clear();return}var now=performance.now(),seen=new Set();
   document.querySelectorAll(SEL).forEach(function(el){if(!hittable(el))return;seen.add(el);if(!live.has(el))AP.set(el,now)});
   live=seen},50);
  function blocked(e){if(!inn())return false;var t=e.target;if(!t||!t.closest)return false;
   if(typeof DL!=="undefined"&&DL&&t.closest("#ov"))return false;           /* 대화창 자체는 엔진이 처리 */
   if(t.closest(".rt,#w209rail,#w209more,.crec2,#wmap"))return false;
   var el=t.closest(SEL);if(!el)return false;
   if(!live.has(el))return false;                                              /* 가운데가 가려진 대상 등: 기록이 없으면 막지 않는다 */
   var at=AP.get(el),now=performance.now();
   if(downT<at)return true;                                                    /* 나타나기 전에 시작된 누름 */
   return now-at<600&&at-endT<1500&&at>=endT}                                  /* 대화가 끝난 직후 나타난 것은 600ms 동안 보호(직접 연 메뉴는 즉시 반응) */
  function guard(e){if(e.type==="pointerdown"||e.type==="touchstart"||e.type==="mousedown"){if(!(e.type!=="pointerdown"&&performance.now()-downT<80))downT=performance.now()}
   if(blocked(e)){e.stopImmediatePropagation();if(e.cancelable)e.preventDefault();window.__innGuarded=(window.__innGuarded||0)+1}}
  ["pointerdown","touchstart","mousedown","pointerup","touchend","mouseup","click"].forEach(function(t){document.addEventListener(t,guard,{capture:true,passive:false})});
 })();
