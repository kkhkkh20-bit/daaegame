/* Shared deduction notebook and compulsory council/confrontation reasoning.
   Cards are observations or testimony; conclusions never exceed their scope. */
(function(){
 var DB={
  linen:{title:'이불을 만진 사람',question:'이불의 손자국을 누구에게 다시 물어볼까?',claim:'나비: “열한 시엔 빵 반죽하고 잤어요. 그 방 쪽엔 아무도 없었어요.”',next:'나비에게 이불을 만졌는지 물어본다. 돈을 옮긴 사람은 아직 모른다.',stages:[{
   ids:['C02','C03'],prompt:'흔적과 어젯밤 행동을 연결해 보자.',options:[
    ['나비도 이불을 만졌는지 확인할 필요가 있다.',true],['나비가 돈을 훔쳤다는 뜻이다.',false,'가루는 이불을 만진 흔적이다. 돈을 옮겼다는 증거는 아니다.'],['방 주인인 할머니의 손자국으로 확정할 수 있다.',false,'방의 주인이라는 사실만으로 가루 묻은 손의 주인을 알 수는 없다.']],
   result:'이불의 가루와 나비의 반죽 일을 함께 보면, 나비에게 그 방에 간 적을 다시 물어볼 이유가 생긴다.',hints:['흔적의 재료와 어젯밤 한 일을 나눠 보자.','이불의 가루와 반죽한 사람의 말을 비교해 보자.','하얀 손자국과 나비의 말을 연결해 보자.']}]},
  time:{title:'밤이의 목격 시각',question:'밤이가 본 시각은 믿어도 될까?',claim:'밤이: “여섯 시 반쯤 세련이 주머니를 들고 갔다가 빈손으로 왔어요.”',next:'세련의 아침 수색 주장과 밤이의 실제 목격을 구분한다. 방에서 한 일은 아직 확인해야 한다.',stages:[{
   ids:['C06','C07'],prompt:'1 · 시계를 본 위치와 자세를 확인하자.',clock:true,options:[
    ['거꾸로 본 시계라면 읽은 시각도 달라질 수 있다.',true],['숫자가 없으니 목격한 사람도 틀렸을 것이다.',false,'시각을 잘못 읽는 것과 사람을 잘못 보는 것은 별개다.'],['이 두 기록만으로 세련의 범행을 확정한다.',false,'시계와 자세는 시각 착오를 확인하는 근거다. 방에서 한 일은 보여주지 않는다.']],
   result:'같은 두 바늘도 거꾸로 보면 아래를 가리킨다. 실제 시각은 다른 기록과 맞춰야 한다.',hints:['밤이가 시계를 본 방향을 생각해 보자.','시계의 숫자 유무와 밤이의 잠자리를 비교하자.','숫자 없는 시계와 밤이의 잠자리를 연결하고, 시계를 돌려 보자.']},{
   ids:['C13','C08'],prompt:'2 · 목격 당시의 날씨를 독립된 기록과 맞추자.',options:[
    ['첫눈이 시작된 자정에 본 것이다.',true],['세련의 기상 시각이 6시 반이므로 목격도 6시 반이다.',false,'세련의 기상 시각은 본인의 말이다. 밤이가 본 순간의 날씨를 설명하지 못한다.'],['밤이가 시각을 틀렸으니 목격 전체를 버린다.',false,'날씨 기록으로 시각을 확인할 수 있다. 사람과 주머니에 관한 목격까지 지울 근거는 없다.']],
   result:'밤이가 말한 “첫눈이 막 시작된 때”와 도토의 “자정, 첫눈” 기록이 맞는다. 아침이 아닌 자정의 목격이다.',hints:['시계 말고 그 순간 함께 본 것이 있다.','밤이의 창밖 관찰과 도토의 날씨 기록을 비교하자.','첫눈을 본 밤이의 목격담과 날씨 일지를 연결하자.']}]},
  location:{title:'공개되지 않은 자리',question:'세련은 발견 위치를 어떻게 알았을까?',claim:'세련: “침대 밑에 처박혀 있던 쥐 하나 꺼내 놓고…”',next:'세련에게 직접 방을 보거나 솜솜을 옮긴 적이 있는지 묻는다. 돈을 숨겼는지는 별도로 증명해야 한다.',stages:[{
   ids:['C04','C10'],prompt:'직접 본 위치와 모두에게 읽어 준 기록을 비교하자.',options:[
    ['세련이 직접 그 자리를 보았을 가능성을 확인해야 한다.',true],['기록부에 침대 밑이라고 적혀 있어 알았을 것이다.',false,'공개 기록은 “같은 방”이라고만 적었다. 침대 밑이라는 위치는 적혀 있지 않다.'],['위치를 안다는 말만으로 돈을 숨긴 범인이 확정된다.',false,'발견 위치를 아는 이유는 물을 수 있다. 그 말만으로 돈을 옮긴 행동까지 증명할 수는 없다.']],
   result:'부녀가 직접 본 자리는 침대 밑 상자 뒤. 공개된 기록에는 “같은 방”만 있다. 세련은 공개되지 않은 위치를 알고 있다.',hints:['어떤 말이 공개된 정보였는지 구분해 보자.','실제 발견 위치와 너울이 읽은 문장을 비교하자.','바구니 속 손님의 발견 기록과 너울의 기록을 연결하자.']}]},
  contact:{title:'털에 남은 붉은 자국',question:'털의 자국으로 어디까지 알 수 있을까?',claim:'세련: “쥐는 옮겼지만 주머니는 보지도 못했습니다.”',next:'솜솜 아래에 주머니가 있었는지 세련에게 묻는다. 붉은 자국은 접촉의 증거이며 살해의 증거가 아니다.',stages:[{
   ids:['C05','C01'],prompt:'글씨의 방향, 별 모양, 잉크 상태를 비교하자.',options:[
    ['솜솜의 털이 덜 마른 주머니 봉인띠에 닿았다.',true],['누군가 솜솜에게 도장을 직접 찍었다.',false,'봉인띠의 글씨와 같은 무늬가 거꾸로 옮겨 묻었다. 직접 찍었다는 설명으로는 이 뒤집힌 방향이 맞지 않는다.'],['이 자국으로 세련이 솜솜을 죽였다고 증명한다.',false,'자국은 무엇과 닿았는지 보여준다. 솜솜의 생사나 가해 행위는 보여주지 않는다.']],
   result:'같은 붉은 글씨와 끝이 말린 별, 뒤집힌 방향. 덜 마른 봉인띠에서 솜솜의 털로 옮겨 묻은 자국이다.',hints:['색만 같은지, 무늬와 방향까지 같은지 살펴보자.','털의 글씨와 봉인띠의 도장을 비교하자.','털의 붉은 자국과 주머니와 계약서를 연결하자.']}]},
  seal:{title:'사라진 이백 냥',question:'봉인이 그대로인데 돈만 빠질 수 있을까?',claim:'세련: “삼백 냥을 봉했습니다. 이백 냥은 그 방 주인이 빼 갔겠죠.”',next:'다른 사람이 돈을 빼 갔다는 설명이 성립하지 않는다. 세련에게 봉하기 전 돈의 행방을 다시 묻는다.',stages:[{
   ids:['C10','C12'],prompt:'발견 때의 상태와 다시 봉할 수 있는 사람을 연결하자.',options:[
    ['세련의 말대로라면 다른 사람이 돈을 빼고 다시 봉할 수 없다.',true],['할머니가 돈을 빼고 세련의 도장으로 다시 봉했다.',false,'세련은 도장을 계속 품에 두었다고 했다. 할머니가 그 도장을 얻었다는 근거가 없다.'],['삼백 냥이었다는 피해자의 말을 그대로 사실로 삼는다.',false,'처음 액수를 확인한 다른 사람은 없다. 온전한 봉인과 확인된 백 냥을 먼저 설명해야 한다.']],
   result:'너울은 온전한 봉인과 백 냥을 확인했다. 세련은 혼자 봉했고 도장을 품에 뒀다고 했다. 이 설명대로라면 다른 사람이 이백 냥을 빼고 다시 봉할 수 없다.',hints:['돈을 꺼냈다면 주머니에 어떤 변화가 남을까?','발견 당시 봉인 상태와 다시 봉할 수 있는 사람을 나눠 보자.','너울의 기록과 세련의 말을 연결해 봉인과 도장 위치를 비교하자.']}]}
 };
 // These are questions the player can now put to the speaker, not verdicts
 // granted by the notebook. Changes in votes and admissions happen afterward.
 var REBUTTAL={
  linen:'“나비 씨도 그 방에 갔다면, 침대 주인만 돈을 숨길 수 있었다는 말은 맞습니까?”',
  time:'“자정에 주머니를 들고 지나갔다면, 자정엔 자고 있었다는 말씀은 어떻게 된 겁니까?”',
  location:'“침대 밑이라는 말은 공개한 적 없습니다. 우리를 의심하는 분이 그 자리를 어떻게 아셨습니까?”',
  contact:'“털에 봉인띠 자국이 남았습니다. 솜솜을 들어 올렸을 때 주머니는 어디에 있었습니까?”',
  seal:'“도장은 계속 품에 있었다면서, 할머니는 어떤 도장으로 다시 봉했다는 겁니까?”'
 };
 var active=null,gen=0,owner=null,returnFocus=null;
 function inn(){return G&&CASES[G.ci]&&CASES[G.ci].id==='inn'}
 function has(id){return !!G&&((G.found||[]).indexOf(id)>=0||(G.asked||[]).indexOf(id)>=0)}
 function beat(k){return !!(G&&G.beats&&G.beats[k])}
 function snow(){return beat('inn_show_geokkuri_C08')||beat('inn_snowWitness')||beat('inn_c13fix')}
 function record(){if(!G.reason||G.reason.version!==1)G.reason={version:1,solved:[]};return G.reason}
 function ready(id){var d=DB[id];return d&&d.stages.every(function(s){return s.ids.every(has)})&&(id!=='time'||snow())&&(id!=='location'||beat('inn_locationClaim'))}
 function text(id){var x=(window.EP1INN.EV||{})[id];if(!x)return '';var fixed=x.fixBeat&&beat(x.fixBeat);return fixed?(x.card2||x.detail2||x.desc2):(x.card||x.detail||x.desc)}
 function name(id){return ((window.EP1INN.EV||{})[id]||{}).name||id}
 function order(id,stage){return ({linen:[1,0,2],time:stage?[0,2,1]:[1,2,0],location:[2,0,1],contact:[1,2,0],seal:[2,1,0]})[id]}
 function notebookClaim(id){return ({linen:'이불에 가루 손자국이 있다. 나비는 어젯밤 반죽을 했다고 말했다.',time:'밤이는 여섯 시 반쯤 보았다고 한다. 목격 당시 첫눈이 막 시작됐다는 관찰도 얻었다.',location:'직접 본 발견 위치와 모두에게 공개된 기록은 같은 정보를 담고 있을까?',contact:'솜솜의 털에 뒤집힌 글씨와 별이 있다. 주머니 봉인띠의 무늬와 비교해 보자.',seal:'세련은 삼백 냥을 혼자 봉했다고 한다. 발견된 백 냥의 봉인은 온전했다.'})[id]}
 function e(s){return esc(String(s||''))}
 function reset(keepGate){gen++;if(!keepGate&&window.__logicGateCancel)window.__logicGateCancel();if(active&&active.el)active.el.remove();active=null;document.body.classList.remove('logic-open');if(returnFocus&&returnFocus.isConnected)returnFocus.focus();returnFocus=null}
 window.__logicReset=reset;
 window.__logicBusy=function(){return !!active};
 // Expose authored questions for tools/accessibility inspection, never progress state.
 window.__logicQuestions=DB;
 // An old dialogue-effect skip hold can swallow clicks in the newly opened
 // notebook. This modal owns its inputs; scene tap protection remains intact.
 var fxEat=window.__fxEat;if(fxEat)window.__fxEat=function(t,ev){if(ev&&ev.target&&ev.target.closest&&ev.target.closest('#logic-panel'))return false;return fxEat.apply(this,arguments)};
 var css=document.createElement('style');css.id='logic-style';css.textContent=`
 #logic-panel{position:fixed;inset:0;z-index:130;background:#151c19e8;color:#332c22;display:grid;place-items:center;padding:10px;box-sizing:border-box;font:15px/1.5 var(--body,sans-serif)}
 #logic-panel *{box-sizing:border-box}#logic-panel .lp-shell{width:min(100%,960px);max-height:100%;background:#f1e5c8;border:2px solid #ae925b;box-shadow:0 12px 60px #0008;display:flex;flex-direction:column;overflow:hidden;border-radius:6px}
 #logic-panel .lp-head{display:flex;gap:12px;align-items:center;padding:9px 14px;background:#353e32;color:#f7eacb;flex:none}#logic-panel .lp-head b{font:18px var(--display,sans-serif)}#logic-panel .lp-head small{flex:1}#logic-panel .lp-close{width:44px;flex:none}
 #logic-panel button{font:14px/1.4 var(--body,sans-serif);border:1px solid #927b50!important;border-image:none!important;border-radius:3px!important;background:#faf0da!important;color:#392f22!important;box-shadow:none!important;min-height:44px;cursor:pointer;padding:7px 10px;white-space:normal;text-shadow:none!important}
 #logic-panel button:before,#logic-panel button:after{display:none!important}#logic-panel button:focus-visible{outline:3px solid #b56734;outline-offset:1px}#logic-panel button:disabled{opacity:.5;cursor:default}
 #logic-panel button[aria-pressed=true],#logic-panel .lp-primary{background:#465443!important;color:#fff2d7!important;border-color:#607752!important}#logic-panel button small{display:block;font-size:11px;opacity:.8}
 #logic-panel .lp-body{overflow:auto;padding:12px 14px;min-height:0;overscroll-behavior:contain}#logic-panel .lp-questions{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:10px}#logic-panel .lp-questions button{flex:1;min-width:125px}
 #logic-panel h2{font:20px/1.3 var(--display,sans-serif);margin:0 0 5px}#logic-panel p{margin:4px 0 9px}#logic-panel .lp-claim{padding:8px 10px;border-left:4px solid #997246;background:#e6d6b5;font-size:14px}
 #logic-panel .lp-layout{display:grid;grid-template-columns:minmax(210px,1fr) minmax(290px,1.45fr);gap:12px}#logic-panel .lp-cards{display:grid;grid-template-columns:1fr 1fr;gap:5px;max-height:190px;overflow:auto;align-content:start;padding:2px}#logic-panel .lp-cards button{text-align:left;min-height:50px}
 #logic-panel .lp-detail{padding:8px;background:#fcf4e1;border:1px solid #b6a17d;font-size:13px;min-height:60px;max-height:100px;overflow:auto;margin-top:7px}#logic-panel .lp-detail b{display:block}#logic-panel .lp-slots{display:flex;gap:6px;margin-bottom:7px}#logic-panel .lp-slots button{flex:1;min-width:0;border-style:dashed!important}
 #logic-panel .lp-options{display:grid;gap:5px}#logic-panel .lp-options button{text-align:left}#logic-panel .lp-feedback{padding:9px;background:#e3dec4;border-left:4px solid #687853;margin-top:7px;font-size:14px}#logic-panel .lp-feedback.error{background:#efddc7;border-left-color:#a35335}
 #logic-panel .lp-actions{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin-top:9px}#logic-panel .lp-actions .lp-primary{margin-left:auto;min-width:130px}#logic-panel .lp-help{font-size:13px;margin-top:7px;color:#615039}
 #logic-panel .lp-clock{display:flex;gap:10px;align-items:center;background:#e8dcc1;padding:6px;margin:6px 0}#logic-panel .lp-clock svg{width:72px;height:72px;flex:none}#logic-panel .lp-clock p{font-size:12px;margin:0}#logic-panel .lp-clock button{min-width:90px}
 #logic-panel .lp-summary{padding:15px;background:#fff5df;border:1px solid #b4a17b}#logic-panel .lp-summary h3{font:21px var(--display,sans-serif);margin:0 0 6px}#logic-panel .lp-summary b{display:block;margin-bottom:6px}
 #logic-panel .lp-body,#logic-panel .lp-cards,#logic-panel .lp-detail{scrollbar-color:#8b7751 #e7dac0;scrollbar-width:auto}#logic-panel .lp-detail small{display:block;color:#726044;font-size:11px;margin-bottom:4px}
 #logic-note{min-height:44px!important}#logic-panel .lp-locked{padding:20px;border:1px dashed #9e885f;background:#f8eed7}
 @media(max-width:550px){#logic-panel{padding:5px}#logic-panel .lp-layout{grid-template-columns:1fr}#logic-panel .lp-cards{max-height:120px}#logic-panel .lp-detail{max-height:100px}#logic-panel .lp-head small{font-size:11px}#logic-panel .lp-questions button{min-width:100px}#logic-panel .lp-body{padding:10px}}
 @media(max-height:450px) and (min-width:551px){#logic-panel .lp-head{padding:5px 12px}#logic-panel .lp-body{padding:8px 12px}#logic-panel .lp-cards{max-height:135px}#logic-panel .lp-detail{max-height:75px}#logic-panel .lp-options button{min-height:40px;padding:5px 8px}#logic-panel h2{font-size:18px}#logic-panel .lp-claim{padding:5px 8px;margin-bottom:5px}}
 `;document.head.appendChild(css);
 function draw(){var a=active;if(!a)return;var previous=document.activeElement,focusKey=null;if(previous&&a.el.contains(previous))Object.keys(previous.dataset).some(function(k){if(['act','card','slot','option','question'].indexOf(k)<0)return false;focusKey=[k,previous.dataset[k]];return true});var scroll=a.el.querySelector('.lp-body'),scrollTop=scroll?scroll.scrollTop:0,cardList=a.el.querySelector('.lp-cards'),cardScroll=cardList?cardList.scrollTop:0;var d=DB[a.id],s=d.stages[a.stage],r=record(),h='<div class="lp-shell"><header class="lp-head"><b>추리 수첩</b><small>'+(a.mode==='notebook'?'조사 · 가설을 세워 보기 (감점 없음)':'주장 검증 · 틀린 제시는 설득력 1칸')+'</small>'+(a.mode==='notebook'?'<button class="lp-close" data-act="close" aria-label="수첩 닫기">×</button>':'')+'</header><main class="lp-body">';
  if(a.mode==='notebook')h+='<nav class="lp-questions" aria-label="풀리지 않은 질문">'+Object.keys(DB).map(function(k){return '<button data-question="'+k+'" aria-pressed="'+(k===a.id)+'">'+e(DB[k].title)+'<small>'+(r.solved.indexOf(k)>=0?'수첩에 정리됨':ready(k)?'근거 비교 가능':'더 조사할 질문')+'</small></button>'}).join('')+'</nav>';
  h+='<h2>'+e(d.question)+'</h2>';
  if(a.mode==='notebook'&&!ready(a.id)){
   var missing=[];d.stages.forEach(function(st){st.ids.forEach(function(id){if(!has(id)&&missing.indexOf(id)<0)missing.push(id)})});
   h+='<section class="lp-locked"><b>아직 비교할 기록이 부족해.</b><p>'+(a.id==='time'&&!snow()?'밤이에게 날씨 일지를 보여 주고, 목격 당시 창밖에 무엇이 있었는지 물어보자.':a.id==='location'&&!beat('inn_locationClaim')?'발견 위치는 공개하지 않았다. 회의에서 사람들이 무슨 말을 하는지 들어 보자.':'현장을 살피고 주민의 말을 더 들어 보자.')+'</p>'+(missing.length?'<p>아직 없는 기록: '+missing.map(name).map(e).join(', ')+'</p>':'')+'</section>';
  }else if(a.complete){
   h+='<section class="lp-summary" role="status"><h3>'+(a.mode==='notebook'?'가설을 정리했어':'반박할 근거를 찾았어')+'</h3>'+a.results.map(function(t){return '<p>'+e(t)+'</p>'}).join('')+'<b>'+(a.mode==='notebook'?'다음에 확인할 일':'이 근거로 되물을 말')+'</b><p>'+e(a.mode!=='notebook'?REBUTTAL[a.id]:a.id==='contact'?'솜솜과 주머니가 같은 자리에 있었는지, 각각을 옮긴 사람에게 확인한다.':d.next)+'</p></section><div class="lp-actions"><button class="lp-primary" data-act="finish">'+(a.mode==='notebook'?'수첩에 남기기':'이 근거로 제시하기')+'</button></div>';
  }else{
   h+='<p class="lp-claim">'+e(a.mode==='notebook'?notebookClaim(a.id):d.claim)+'</p><p>'+e(s.prompt)+' <small>('+ (a.stage+1)+' / '+d.stages.length+')</small></p><div class="lp-layout"><section><div class="lp-cards" aria-label="가진 기록">'+Object.keys(window.EP1INN.EV).filter(has).map(function(id){return '<button data-card="'+id+'" aria-pressed="'+(a.selected.indexOf(id)>=0)+'"><small>'+(id==='C03'||id==='C07'||id==='C12'||id==='C13'?'주민의 진술':'현장·관찰 기록')+'</small>'+e(name(id))+'</button>'}).join('')+'</div><div class="lp-detail" aria-live="polite">'+(a.detail?'<b>'+e(name(a.detail))+'</b><small>기록 원문 · 긴 내용은 이 칸에서 스크롤</small>'+e(text(a.detail)):'기록을 누르면 원문을 읽고 근거 칸에 놓을 수 있어. 같은 기록은 한 번만 쓸 수 있어.')+'</div></section><section><div class="lp-slots">'+[0,1].map(function(i){return '<button data-slot="'+i+'">근거 '+(i+1)+'<br>'+e(a.selected[i]?name(a.selected[i]):'기록 고르기')+'</button>'}).join('')+'</div>';
   if(s.clock)h+='<div class="lp-clock"><svg viewBox="0 0 100 100" role="img" aria-label="숫자 없는 시계. 두 바늘이 겹쳐 '+(a.rotated?'위':'아래')+'를 가리킴"><g transform="rotate('+(a.rotated?0:180)+' 50 50)"><circle cx="50" cy="50" r="43" fill="#fcf1d6" stroke="#635136" stroke-width="3"/>'+Array.from({length:12},function(_,i){return '<path d="M50 10v5" stroke="#806946" stroke-width="2" transform="rotate('+(i*30)+' 50 50)"/>'}).join('')+'<path d="M50 50V21 M50 50V31" stroke="#332c24" stroke-width="4" stroke-linecap="round"/><circle cx="50" cy="50" r="4" fill="#332c24"/></g></svg><p>'+(a.rotated?'바닥에서 보는 방향':'밤이처럼 거꾸로 보는 방향')+'<br>실제 시각은 다음 단계에서 다른 기록과 맞춘다.</p><button data-act="rotate">시계 돌려 보기</button></div>';
   h+='<div class="lp-options" aria-label="이 두 근거로 말할 수 있는 결론">'+order(a.id,a.stage).map(function(i){var o=s.options[i];return '<button data-option="'+i+'" aria-pressed="'+(a.choice===i)+'">'+e(o[0])+'</button>'}).join('')+'</div><div class="lp-actions"><button data-act="help">생각할 거리 '+(a.hint?Math.min(a.hint,3)+'/3':'')+'</button><button class="lp-primary" data-act="submit" '+(a.selected.length!==2||a.choice==null?'disabled':'')+'>근거와 결론 검증</button></div>'+(a.hint?'<p class="lp-help">'+e(s.hints[Math.min(a.hint,3)-1])+'</p>':'')+(a.feedback?'<div class="lp-feedback '+(a.error?'error':'')+'" role="status">'+e(a.feedback)+'</div>':'')+'</section></div>';
  }
  h+='</main></div>';a.el.dataset.reason=a.id;a.el.dataset.stage=a.stage;a.el.innerHTML=h;var target=focusKey&&a.el.querySelector('[data-'+focusKey[0]+'="'+focusKey[1]+'"]');if(!target&&a.complete)target=a.el.querySelector('[data-act=finish]');if(target)target.focus({preventScroll:true});a.el.querySelector('.lp-body').scrollTop=scrollTop;var cards=a.el.querySelector('.lp-cards');if(cards)cards.scrollTop=cardScroll;
 }
 function wrong(a,message){a.feedback=message;a.error=true;if(a.mode!=='notebook'){
  var was=G.hp==null?5:G.hp;G.hp=Math.max(1,was-1);G.wrong=(G.wrong|0)+1;saveProg();a.feedback+=' 설득력 1칸을 잃었어.';
  if(was<=1){var kind=a.mode;reset();window.__innFail(kind);return}
 }
 try{SFX.huh()}catch(x){}draw()}
 function submit(){var a=active;if(!a||a.complete||a.selected.length!==2||a.choice==null||Date.now()-(a.lastSubmit||0)<550)return;a.lastSubmit=Date.now();var st=DB[a.id].stages[a.stage],right=a.selected.every(function(id){return st.ids.indexOf(id)>=0});
  if(!right){var good=a.selected.filter(function(id){return st.ids.indexOf(id)>=0});wrong(a,good.length?'“'+name(good[0])+'”는 관련 있다. 다른 기록은 이 주장에 필요한 사실을 확인하지 못한다. 원문을 다시 비교해 보자.':'이 두 기록으로는 지금 주장의 사실을 연결할 수 없다. 무엇을 언제 보았는지 원문을 다시 비교해 보자.');return}
  var op=st.options[a.choice];if(!op[1]){wrong(a,op[2]);return}
  a.results.push(st.result);try{SFX.found()}catch(x){}
  if(a.stage+1<DB[a.id].stages.length){a.stage++;a.selected=[];a.choice=null;a.detail=null;a.hint=0;a.feedback='시각을 잘못 읽었을 가능성을 확인했어. 이제 실제 시각을 다른 기록으로 확인하자.';a.error=false}else{a.complete=true}draw();
 }
 function open(id,opt){opt=opt||{};if(!inn()||!DB[id]||active)return false;var mode=opt.mode||'notebook';if(mode==='notebook'&&(typeof DL!=='undefined'&&DL||document.querySelector('body>.rt')))return false;
  if(mode!=='notebook'&&id==='location'){G.beats=G.beats||{};G.beats.inn_locationClaim=1;saveProg()}
  owner=G;returnFocus=document.activeElement;var el=document.createElement('div');el.id='logic-panel';el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');el.setAttribute('aria-label','추리 수첩');document.body.appendChild(el);document.body.classList.add('logic-open');
  active={id:id,mode:mode,el:el,game:G,rt:document.querySelector('body>.rt'),stage:0,selected:[],choice:null,detail:null,hint:0,rotated:false,results:[],done:opt.done,token:++gen};draw();
  el.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b||!el.contains(b))return;ev.stopPropagation();var a=active;if(!a||a.el!==el)return;
   if(b.dataset.question){a.id=b.dataset.question;a.stage=0;a.selected=[];a.choice=null;a.detail=null;a.complete=false;a.hint=0;a.feedback='';a.results=[];draw();return}
   if(b.dataset.card){var id=b.dataset.card;if(!has(id))return;a.detail=id;var i=a.selected.indexOf(id);if(i>=0)a.selected.splice(i,1);else if(a.selected.length<2)a.selected.push(id);else{a.feedback='근거 칸이 가득 찼어. 바꿀 칸을 먼저 눌러 비워 줘.';a.error=false}draw();var detail=el.querySelector('.lp-detail');if(detail)detail.scrollIntoView({block:'nearest'});return}
   if(b.dataset.slot!=null){a.selected.splice(+b.dataset.slot,1);draw();return}
   if(b.dataset.option!=null){a.choice=+b.dataset.option;draw();return}
   var act=b.dataset.act;if(act==='close'){reset();return}if(act==='rotate'){a.rotated=!a.rotated;draw();return}if(act==='help'){a.hint=Math.min(3,a.hint+1);draw();return}if(act==='submit'){submit();return}
   if(act==='finish'&&a.complete){var done=a.done,g=a.game;var r=record();if(r.solved.indexOf(a.id)<0)r.solved.push(a.id);saveProg();reset(true);if(done&&G===g)done()}
  });el.querySelector('button').focus();return true;
 }
 window.__logicOpen=open;
 document.addEventListener('keydown',function(ev){if(!active)return;var el=active.el;if(ev.key==='Escape'&&active.mode==='notebook'){ev.preventDefault();ev.stopImmediatePropagation();reset();return}
  if(ev.key==='Tab'){var list=[].slice.call(el.querySelectorAll('button:not(:disabled)'));if(!list.length)return;var i=list.indexOf(document.activeElement);list[(i+(ev.shiftKey?-1:1)+list.length)%list.length].focus();ev.preventDefault();ev.stopImmediatePropagation();return}
  // Enter/Space still activate the focused button, never underlying dialogue.
  ev.stopImmediatePropagation();
 },true);
 function sync(){if(active&&(G!==active.game||!inn()||(active.mode!=='notebook'&&document.querySelector('body>.rt')!==active.rt))){reset();return}
  if(owner&&owner!==G){reset();owner=G}
  var rail=document.querySelector('#w209rail .g');if(inn()&&rail&&!document.getElementById('innmain')){var b=rail.querySelector('#logic-note');if(!b){b=document.createElement('button');b.id='logic-note';b.type='button';b.textContent='추리';b.setAttribute('aria-label','추리 수첩 열기');b.addEventListener('click',function(ev){ev.stopPropagation();if(typeof DL!=='undefined'&&DL)return;open('linen',{mode:'notebook'})});rail.appendChild(b)}b.disabled=!!(typeof DL!=='undefined'&&DL)}
 }
 setInterval(sync,150);
 // C13 keeps the observation obtained by questioning, separate from correction.
 var x=window.EP1INN&&window.EP1INN.EV.C13;if(x)['desc','card','detail','desc2','card2','detail2'].forEach(function(k){var base=x[k];if(!base)return;Object.defineProperty(x,k,{enumerable:true,configurable:true,get:function(){return base+(snow()?' 추가 관찰: 그 사람이 지나갈 때 창밖에 올해 첫눈이 막 내리기 시작했다.':'')}})});
})();
