# 2026-10-10 v2 사용자 승인(구조 피드백): 결론은 플레이어가 고른다(ask), 주민별 표 바뀜 표시(votes), 순서·관련 안내 축소, 회의 진입 완화(휴회), 돋보기는 할머니에게 솜솜 이야기를 하면
# 1) 줄에 붙은 결론 고르기·표 바뀜
rep(' function meta(L){if(!L)return;\n',
    ' function meta(L){if(!L)return;\n  if(L.votes)setVotes(L.votes);\n  if(L.ask)askOpen(L);\n')
rep(' window.__rtgPick=function(){return !!PK};',
    ''' window.__rtgPick=function(){return !!PK};
 /* 결론 고르기: 정답 증거 뒤 아빠가 대신 해설하지 않고 플레이어가 결론을 고른다. 틀리면 설득력 -1(1칸에서 또 틀리면 실패 장면) */
 var ANS=new Set();
 function askOpen(L){if(ANS.has(L)||PK)return;setTimeout(function(){if(ANS.has(L)||PK||!rt())return;
   openPick(L.ask,function(){ANS.add(L);try{SFX.found()}catch(e){}try{flash("바로 그거야!",false,true)}catch(e){}},
    function(w){wrongAsk(L,w)},function(){wrongAsk(L,null)});var px=PK&&PK.querySelector('[data-pi="x"]');if(px)px.remove();if(PK)PK.classList.add("ask9")},350)}
 function wrongAsk(L,w){var was=G.hp==null?5:G.hp;G.wrong=(G.wrong|0)+1;G.hp=Math.max(1,was-1);LW=G.wrong;LH=G.hp;try{saveProg()}catch(e){}
  var fin=isFinal(ph())?"final":"meet";
  try{flash("헛짚었다!",true)}catch(e){}
  if(was<=1){setTimeout(function(){try{window.__innFail&&window.__innFail(fin)}catch(e){MISS.push("askfail "+e.message)}},900);return}
  setTimeout(function(){queue(w&&w.length?w:[{w:"narr",t:"(아니다. 다시 생각해 보자.)"}],function(){askOpen(L)})},700)}
 window.__rtgAsk=function(){return PK&&PK.querySelector("b")?PK.querySelector("b").textContent:null};
 /* 주민별 표: 자리 아래에 지금 누구에게 표를 두었는지, 바뀌면 '이름: 전 → 후' */
 var VN={innma:"할머니",seryeon:"세련","부녀":"부녀","기권":"기권"};
 function votes(){try{return (G.beats&&G.beats.rtVotes)||null}catch(e){return null}}
 function setVotes(v){try{G.beats=G.beats||{};var o=Object.assign({},G.beats.rtVotes||{}),ch=[];Object.keys(v).forEach(function(k){if(o[k]&&o[k]!==v[k])ch.push(k);o[k]=v[k]});G.beats.rtVotes=o;saveProg();
   ch.forEach(function(k,i){setTimeout(function(){toast(k)},i*500)})}catch(e){}}
 function toast(k){var seat=document.querySelector('#rtg .seat[data-k="'+k+'"]');var d=document.createElement("div");d.className="vtoast9";d.textContent=nm(k)+" → "+(VN[(votes()||{})[k]]||"");
  document.body.appendChild(d);var r=seat?seat.getBoundingClientRect():null;d.style.left=(r?Math.max(8,Math.min(innerWidth-160,r.left+r.width/2-70)):innerWidth/2-70)+"px";d.style.top=(r?Math.max(40,r.top-26):60)+"px";
  try{SFX.vote&&SFX.vote(0)}catch(e){}setTimeout(function(){d.remove()},2200)}
 function badges(){var v=votes(),fin=isFinal(ph());document.querySelectorAll("#rtg .seat[data-k]").forEach(function(s){var k=s.dataset.k,b=s.querySelector(".vt9");
   if(!v||fin||!v[k]){if(b)b.remove();return}if(!b){b=document.createElement("i");b.className="vt9";s.appendChild(b)}var t=VN[v[k]]||v[k];if(b.textContent!==t){b.textContent=t;b.dataset.v=v[k];b.classList.remove("bump");void b.offsetWidth;b.classList.add("bump")}})}''')
rep('  if(Q)placeQ();\n  tryFail();\n',
    '  if(Q)placeQ();\n  badges();\n  tryFail();\n')
rep('  "#rtgpick button.x{text-align:center;background:#E6DCC0}"\n',
    '''  "#rtgpick button.x{text-align:center;background:#E6DCC0}",
  "#rtg .seat .vt9{position:absolute;left:50%;top:-16px;transform:translateX(-50%);z-index:6;padding:1px 6px;border-radius:8px;background:#F4EEDC;border:1.5px solid #8C7A4E;color:#2A2F1F;font:400 11px/1.3 var(--display,sans-serif);font-style:normal;white-space:nowrap;pointer-events:none}",
  "#rtg .seat .vt9[data-v=innma]{background:#F3D9C9;border-color:#9A4A2E}#rtg .seat .vt9[data-v=seryeon]{background:#E8D8F0;border-color:#6A3E8A}#rtg .seat .vt9[data-v='부녀']{background:#D9E6F3;border-color:#2E5A8A}#rtg .seat .vt9[data-v='기권']{opacity:.75}",
  "#rtg .seat .vt9.bump{animation:vt9b .5s ease-out}@keyframes vt9b{40%{transform:translateX(-50%) scale(1.35)}100%{transform:translateX(-50%) scale(1)}}",
  ".vtoast9{position:fixed;z-index:72;width:140px;text-align:center;padding:3px 6px;border-radius:8px;background:rgba(20,16,30,.9);border:1.5px solid #FFD84D;color:#FFE9A8;font:12px/1.3 var(--display,sans-serif);pointer-events:none;animation:vt9t 2.2s ease-out forwards}@keyframes vt9t{0%{opacity:0;transform:translateY(6px)}12%,80%{opacity:1;transform:none}100%{opacity:0}}",
  "#rtgpick .bx b{white-space:normal}"
''')
# 2) 안내 축소: '[순서] 감점은 없어요'·'[감점 없음] 관련 있는 증거예요' 대신 발언자의 짧은 반응(순서), 관련 증거를 엉뚱한 발언에 내면 일반 오답
rep('   if(step<steps.length){stop();var sf=s.soft&&s.soft[id];queue(sf&&(sf.untilStep==null||step<sf.untilStep)?sf.lines:HINT_ORDER);return}',
    '   if(step<steps.length){stop();var sf=s.soft&&s.soft[id];queue(sf&&(sf.untilStep==null||step<sf.untilStep)?sf.lines:[{w:s.w,t:"…그것만으로 뭘 말하겠다는 겁니까?"}]);return}')
rep('  if(related(p)[id]){stop();queue(HINT_REL);return}\n','')
# 3) 돋보기(C05): 장부(C11)를 연 뒤가 아니라, 할머니에게 바구니 속 손님(C04)을 보여 주면 빌려주신다. 해(머리판)는 솜솜을 찾고 사람 하나에게 이야기를 들은 뒤
rep('  if(id==="C05")return has("C11");','  if(id==="C05")return has("C11")||(has("C04")&&bt("inn_show_innma_C04"));')
rep(' function sun(){return FIRST.every(has)}',' function sun(){return has("C04")&&["C03","C07","C12","C13"].some(has)}')
# 단계 조회(힌트 3단계가 다음에 낼 증거를 가리키도록)
rep(' window.__rtgQueue=function(){return Q?{i:QI,n:Q.length}:null};',' window.__rtgQueue=function(){return Q?{i:QI,n:Q.length}:null};window.__rtgStep=function(s){return STEP.get(s)||0};')
