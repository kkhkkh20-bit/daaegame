/* 원탁회의·최종 대결 장면(rtg)에 대본 기능 연결
   - 시간 표시(clock), 공개 득표(tally), 되묻기(press), 증거별 오답 반응(wr, 설득력 -1),
     감점 없는 반응(soft: 다른 발언으로 이동·단계 완료 포함), 차례로 이어 내는 증거(steps),
     장부 줄 고르기(pick), 증거 다시 보여 주기(show), 증거 지급(grant), 상태 표시(beat), 설득력 0칸 처리
   - 회의 데이터에 있는 선택 항목만 읽는다. 없으면 아무것도 하지 않는다(우체국 회의 그대로). */
(function(){
 var MISS=window.__RTI=[],B=document.body;
 function rt(){return document.querySelector("body>.rt")}
 function ph(){try{return window.__rtPh&&window.__rtPh()}catch(e){return null}}
 function strip(t){return String(t||"").replace(/[{}]/g,"")}
 function nm(k){if(k==="det0")return (S.players&&S.players[0])||"아빠";if(k==="det1")return (S.players&&S.players[1])||"다람";if(k==="narr")return "";return (CAST[k]||{}).name||k}
 function EP(){return window.EP1INN||null}
 function isFinal(p){var e=EP();return !!(e&&e.FINAL&&p&&e.FINAL.phases.indexOf(p)>=0)}
 function curStm(){var p=ph(),b=document.querySelector(".rt .rt-bub.stm p");if(!p||!p.stms||!b)return null;var t=b.textContent;return p.stms.filter(function(s){return strip(s.t)===t})[0]||null}
 function curLine(){var p=ph(),b=document.querySelector(".rt #rtnext .rt-bub p, .rt .rt-mid.talk .rt-bub p");if(!p||!b)return null;var t=b.textContent,pool=[];
  (p.lines||[]).forEach(function(x){pool.push(x)});(p.stms||[]).forEach(function(s){(s.ok||[]).forEach(function(x){pool.push(x)})});(p.ok||[]).forEach(function(x){pool.push(x)});
  return pool.filter(function(x){return x&&strip(x.t)===t})[0]||null}
 function setBeat(k){try{G.beats=G.beats||{};G.beats[k]=1;saveProg()}catch(e){}}
 /* 대사에 붙은 부가 정보: 득표·증거 지급·상태·증거 보여 주기 */
 function meta(L){if(!L)return;
  if(L.tally){G.beats=G.beats||{};G.beats.rtTally=L.tally;try{saveProg()}catch(e){}}
  if(L.grant&&window.__innGrant)window.__innGrant(L.grant);
  if(L.beat)setBeat(L.beat);
  showEv(L.show||null)}
 function tal(){try{G.beats=G.beats||{};return G.beats.rtTally||null}catch(e){return null}}
 var lastLine=null;
 function onLine(){var L=curLine();if(L===lastLine)return;lastLine=L;if(L)meta(L);else if(!Q)showEv(null)}

 var st=document.createElement("style");st.textContent=[
  "#rtgclk{position:fixed;left:8px;top:42px;z-index:62;padding:3px 9px;border-radius:6px;background:rgba(20,16,30,.82);border:1px solid #C9A96A;color:#FFE9A8;font:12px/1.2 var(--display,sans-serif)}",
  "#rtgtal{position:fixed;left:50%;top:40px;transform:translateX(-50%);z-index:62;padding:3px 10px;border-radius:6px;background:rgba(244,238,220,.95);border:1.5px solid #C9A96A;color:#2A2F45;font:12px/1.25 var(--display,sans-serif);white-space:nowrap;max-width:60vw;overflow:hidden;text-overflow:ellipsis}",
  "#rtgtal b{color:#8A2E2E;font-weight:400}",
  "#rtgq{position:fixed;z-index:63;box-sizing:border-box;padding:6px 12px 7px;background:#FFF6D8;color:#1B2447;border:2.5px solid #8A2E2E;border-radius:14px;box-shadow:0 3px 0 rgba(0,0,0,.35);font:15px/1.45 var(--body,sans-serif);cursor:pointer}",
  "#rtgq small{display:block;font:12px/1.2 var(--display,sans-serif);color:#8A2E2E;margin-bottom:1px}#rtgq.narr{background:rgba(20,16,30,.9);color:#FFF6E0;border-color:#C9A96A}#rtgq.narr small{display:none}",
  "body.rtgq-on .rt .rt-bub{visibility:hidden!important}",
  "html body.rtg .rt .rt-bub.rtgnarr{background:rgba(20,16,30,.92)!important;color:#FFF6E0!important;border-color:#C9A96A!important}html body.rtg .rt .rt-bub.rtgnarr small{display:none!important}html body.rtg .rt .rt-bub.rtgnarr:after{display:none}",
  /* 증거 다시 보여 주기 */
  "#rtgshow{position:fixed;right:10px;top:72px;z-index:62;display:flex;gap:6px;pointer-events:none}",
  "#rtgshow .ch{display:flex;flex-direction:column;align-items:center;width:78px;padding:5px 4px 4px;background:#F4EEDC;border:2px solid #8C7A4E;box-shadow:2px 2px 0 rgba(0,0,0,.35);color:#2A2F1F;font:11px/1.2 var(--display,sans-serif);text-align:center}",
  "#rtgshow .ch svg,#rtgshow .ch img{width:48px;height:48px}#rtgshow .ch span{margin-top:3px}",
  "@media (max-height:380px){#rtgshow{top:64px}#rtgshow .ch{width:66px}#rtgshow .ch svg,#rtgshow .ch img{width:40px;height:40px}}",
  /* 장부 줄 고르기 */
  "#rtgpick{position:fixed;inset:0;z-index:70;display:flex;align-items:center;justify-content:center;background:rgba(10,8,16,.55)}",
  "#rtgpick .bx{width:min(420px,calc(100vw - 32px));max-height:calc(100vh - 24px);overflow:auto;box-sizing:border-box;padding:12px 14px;background:#F4EEDC;border:2.5px solid #8C7A4E;box-shadow:3px 3px 0 rgba(0,0,0,.4);color:#2A2F1F}",
  "#rtgpick b{display:block;font:400 15px/1.3 var(--display,sans-serif);margin-bottom:8px}",
  "#rtgpick button{display:block;width:100%;min-height:44px;margin:0 0 6px;padding:0 12px;text-align:left;background:#FFF9E8;border:2px solid #2A2F1F;color:#2A2F1F;font:14px/1.2 var(--display,sans-serif);cursor:pointer}",
  "#rtgpick button.x{text-align:center;background:#E6DCC0}"
 ].join("\n");(document.head||document.documentElement).appendChild(st);

 var CLK=null,TAL=null,Q=null,QI=0,QEL=null,QDONE=null,SHOW=null;
 /* 단계·되묻기·표시 상태: 회의를 다시 열면 초기화 */
 var STEP=new Map(),PRESSED=new Set(),MARK={};
 window.__rtgReset=function(){STEP=new Map();PRESSED=new Set();MARK={};FAILP=false;LW=null;LH=null};
 function ensure(){if(!CLK){CLK=document.createElement("div");CLK.id="rtgclk";document.body.appendChild(CLK)}if(!TAL){TAL=document.createElement("div");TAL.id="rtgtal";document.body.appendChild(TAL)}}
 function clear(){[CLK,TAL,QEL,SHOW].forEach(function(x){if(x)x.remove()});CLK=TAL=QEL=SHOW=null;Q=null;B.classList.remove("rtgq-on");closePick()}
 function showEv(ids){if(!ids||!ids.length){if(SHOW){SHOW.remove();SHOW=null}return}
  if(!SHOW){SHOW=document.createElement("div");SHOW.id="rtgshow";document.body.appendChild(SHOW)}
  var c=CASES[G.ci];SHOW.innerHTML=ids.map(function(id){var n="";try{n=itemName(c,id)}catch(e){n=id}return '<div class="ch">'+(typeof evIcon==="function"?evIcon(id):"")+'<span>'+String(n).replace(/[<>&]/g,"")+'</span></div>'}).join("")}

 /* 설득력 0칸 감지: 엔진은 1칸 아래로 내리지 않으므로, 1칸에서 또 틀리면 0칸으로 본다 */
 var LW=null,LH=null,FAILP=false,FAILK=null;
 function watchHp(){var w=G.wrong|0,h=G.hp==null?5:G.hp;if(LW==null){LW=w;LH=h;return}
  if(w>LW){if(LH<=1){FAILP=true;FAILK=isFinal(ph())?"final":"meet"}LW=w;LH=h}else LH=h}
 function tryFail(){if(!FAILP||Q)return;if(document.querySelector(".rt #rtnext"))return;FAILP=false;var k=FAILK;
  setTimeout(function(){try{window.__innFail&&window.__innFail(k)}catch(e){MISS.push("fail "+e.message)}},200)}

 function sync(){try{var r=rt();if(!r||!B.classList.contains("rtg")){if(CLK||TAL||QEL||SHOW)clear();LW=null;return}var p=ph();ensure();
  watchHp();
  /* 엔진 대사(#rtnext)가 나오면 증거 서랍을 닫는다: 판정 연출 중에 서랍을 열어도 '계속 듣기'가 숨지 않게 */
  if(r.querySelector("#rtnext")&&B.classList.contains("rtg-drw")&&!Q)B.classList.remove("rtg-drw");
  CLK.style.display=p&&p.clock?"":"none";if(p&&p.clock)CLK.textContent=p.clock;
  onLine();var t=tal(),vote=!!r.querySelector(".rt-mid.vote");
  TAL.style.display=t&&!vote&&!isFinal(p)?"":"none";if(t)TAL.innerHTML="공개 득표 · "+Object.keys(t).map(function(k){return '<b>'+(CAST[k]?nm(k):k)+'</b> '+t[k]}).join(" · ");
  var bar=document.getElementById("rtgbar");if(bar){var pb=bar.querySelector('[data-g="press"]');
   if(!pb){pb=document.createElement("button");pb.type="button";pb.dataset.g="press";pb.textContent="되묻기";var obj=bar.querySelector('[data-g="obj"]');bar.insertBefore(pb,obj);
    pb.addEventListener("click",function(e){e.stopPropagation();var s=curStm();if(s&&s.press){PRESSED.add(s);queue(s.press)}},true)}
   var s=curStm(),drw=B.classList.contains("rtg-drw");pb.style.display=drw||!s?"none":"";pb.disabled=!(s&&s.press)}
  var eb=document.querySelector(".rt .rt-bub:not(.stm)"),en=eb&&eb.querySelector("small");if(eb)eb.classList.toggle("rtgnarr",!!en&&!en.textContent.trim());
  if(Q)placeQ();
  tryFail();
 }catch(e){MISS.push("sync "+e.message)}}

 /* 대기열(되묻기·반응·안내): 엔진 진행과 별개로 보여 주고, 끝나면 엔진 말풍선으로 돌아간다 */
 function queue(lines,done){if(!lines||!lines.length){done&&done();return}Q=lines.slice();QI=0;QDONE=done||null;showQ()}
 function showQ(){if(!Q)return;if(QI>=Q.length){Q=null;if(QEL){QEL.remove();QEL=null}B.classList.remove("rtgq-on");showEv(null);var d=QDONE;QDONE=null;d&&d();return}
  var L=Q[QI];if(!QEL){QEL=document.createElement("div");QEL.id="rtgq";document.body.appendChild(QEL);QEL.addEventListener("click",function(e){e.stopPropagation();QI++;showQ()})}
  B.classList.add("rtgq-on");QEL.className=L.w==="narr"?"narr":"";QEL.innerHTML='<small>'+nm(L.w)+'</small>'+String(L.t).replace(/[<>&]/g,"");QEL.dataset.w=L.w;meta(L);placeQ()}
 function placeQ(){if(!QEL)return;var W=innerWidth,bw=Math.min(W*.5,380),seat=document.querySelector('#rtg .seat[data-k="'+QEL.dataset.w+'"] img, #rtg .seat[data-k="'+QEL.dataset.w+'"]');
  QEL.style.width=bw+"px";var l=(W-bw)/2,t=48;if(seat){var r=seat.getBoundingClientRect();l=Math.max(8,Math.min(W-bw-8,r.left+r.width/2-bw/2));t=Math.max(44,r.top+r.height*.08-QEL.offsetHeight-8)}
  QEL.style.left=l+"px";QEL.style.top=t+"px"}
 window.__rtgQueue=function(){return Q?{i:QI,n:Q.length}:null};
 /* '계속 듣기'는 대기열이 있으면 대기열부터 */
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest('#rtgbar [data-g="next"]');if(!b||!Q)return;e.stopImmediatePropagation();e.preventDefault();QI++;showQ()},true);

 /* 장부 줄 고르기 */
 var PK=null;
 function closePick(){if(PK){PK.remove();PK=null}}
 function openPick(pk,onOk,onWr,onMiss){closePick();PK=document.createElement("div");PK.id="rtgpick";
  PK.innerHTML='<div class="bx"><b>'+String(pk.title).replace(/[<>&]/g,"")+'</b>'+pk.items.map(function(it,i){return '<button type="button" data-pi="'+i+'">'+String(it.label).replace(/[<>&]/g,"")+'</button>'}).join("")+'<button type="button" class="x" data-pi="x">돌아가기</button></div>';
  document.body.appendChild(PK);
  PK.addEventListener("click",function(e){var t=e.target.closest("[data-pi]");if(!t)return;e.stopPropagation();var v=t.dataset.pi;closePick();try{SFX.tap()}catch(x){}
   if(v==="x")return;var it=pk.items[+v];if(it.ok)onOk();else if(it.wr)onWr(it.wr);else onMiss()})}
 window.__rtgPick=function(){return !!PK};

 /* 발언 이동(숨긴 엔진 ◀▶ 버튼 사용) */
 function goStm(p,idx){var target=p.stms[idx];for(var k=0;k<p.stms.length+1;k++){if(curStm()===target)return true;var nx=document.querySelector(".rt #rtnx");if(!nx)return false;nx.click()}return curStm()===target}
 function related(p){var o={};(p.stms||[]).forEach(function(s){(s.a||[]).forEach(function(x){o[x]=1});(s.steps||[]).forEach(function(x){x.ids.forEach(function(y){o[y]=1})});Object.keys(s.soft||{}).forEach(function(y){o[y]=1})});return o}
 var HINT_ORDER=[{w:"narr",t:"[순서] 먼저 이어서 제시할 증거가 있어요. 감점은 없어요."}],
     HINT_REL=[{w:"narr",t:"[감점 없음] 관련 있는 증거예요. 다른 발언과 이어 보세요."}];

 /* 제시 판정 */
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest('#rtgbar [data-g="present"]');if(!b||b.dataset.go)return;
  var p=ph(),s=curStm(),sel=document.querySelector(".rt .rt-bul .bl.on");if(!p||!s||!sel)return;var id=sel.dataset.bl;
  function stop(){e.stopImmediatePropagation();e.preventDefault();B.classList.remove("rtg-drw")}
  function resend(){b.dataset.go="1";B.classList.add("rtg-drw");b.click();delete b.dataset.go}
  var steps=s.steps||[],step=STEP.get(s)||0,a=s.a||[];
  /* 1) 다음 단계 증거 */
  if(step<steps.length&&steps[step].ids.indexOf(id)>=0){stop();var sp=steps[step];
   var adv=function(){STEP.set(s,step+1);try{SFX.found()}catch(x){}queue(sp.lines)};
   if(sp.pick)openPick(sp.pick,adv,function(w){queue(w,resend)},resend);else adv();return}
  /* 2) 최종 정답 증거 */
  if(a.indexOf(id)>=0){
   if(step<steps.length){stop();var sf=s.soft&&s.soft[id];queue(sf&&(sf.untilStep==null||step<sf.untilStep)?sf.lines:HINT_ORDER);return}
   if(s.needPress&&!PRESSED.has(s)&&s.press){stop();queue(s.press,function(){PRESSED.add(s);resend()});return}
   return}  /* 엔진이 정답 처리 */
  /* 3) 감점 없는 반응 */
  var so=s.soft&&s.soft[id];
  if(so&&(!so.req||MARK[so.req])&&(so.untilStep==null||step<so.untilStep)){stop();
   queue(so.lines,function(){if(so.mark)MARK[so.mark]=1;if(so.to==null)return;var tg=p.stms[so.to];if(so.step!=null)STEP.set(tg,Math.max(STEP.get(tg)||0,so.step));if(so.pressed)PRESSED.add(tg);
    if(!goStm(p,so.to)){MISS.push("goStm");return}
    if((tg.a||[]).indexOf(id)>=0&&(STEP.get(tg)||0)>=(tg.steps||[]).length)setTimeout(resend,120)});return}
  /* 4) 증거별 오답 반응(감점) */
  var wr=s.wr&&s.wr[id];if(wr){stop();queue(wr,resend);return}
  /* 5) 같은 라운드의 관련 증거를 다른 발언에 냄 → 감점 없이 안내 */
  if(related(p)[id]){stop();queue(HINT_REL);return}
  /* 6) 그 밖: 엔진 판정(감점) */
 },true);
 /* 자동 진행: 대기열·줄 고르기 중에는 멈춤 */
 try{window.__rtgPausedExtra=function(){return !!Q||!!PK}}catch(e){}
 var qd=0;try{new MutationObserver(function(ms){if(ms.every(function(m){return m.target&&m.target.closest&&m.target.closest("#rtgq,#rtgclk,#rtgtal,#rtgshow,#rtgpick")}))return;if(!qd)qd=requestAnimationFrame(function(){qd=0;sync()})}).observe(document.body,{childList:true,subtree:true,characterData:true})}catch(e){MISS.push("obs")}
})();
