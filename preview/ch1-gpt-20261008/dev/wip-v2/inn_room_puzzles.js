/* Chapter 1 physical puzzles. Native proof IDs, consent and meeting gates stay
   authoritative: the lock opens its box; the optional ink study grants no item. */
(function(){
 var active=null,pending=null,EP=window.EP1INN;if(!EP||!EP.LOCK)return;
 function inn(){return !!(S.screen==='case'&&G&&CASES[G.ci]&&CASES[G.ci].id==='inn')}
 function has(id){return !!(G&&(G.found||[]).indexOf(id)>=0)}
 function readDate(){return !!(G&&(G.obsSeen||[]).indexOf('o_inn_head2')>=0)}
 function available(){return inn()&&G.beats&&G.beats.inn_pro&&!DL&&!window.__dlFreeze&&!window.__innCutting&&!document.querySelector('body>.rt,#innmove,#wmap,.banner,.placecard,#innopt,.innconf,#innppl,#e9pop,#w209rail.more')}
 function valid(s){return !!(s&&active===s&&G===s.game&&inn()&&!DL&&G.loc===s.loc&&G.tab===s.tab&&s.panel&&s.panel.isConnected)}
 function save(){try{saveProg()}catch(e){}}
 function beat(k,v){G.beats=G.beats||{};G.beats[k]=v;save()}
 function sound(k){try{SFX[k]&&SFX[k]()}catch(e){}}
 var paths={calendar:'<path d="M4 6h16v15H4zM4 10h16M8 3v5M16 3v5M8 14h2M14 14h2M8 18h2"/>',day:'<path d="M4 6h16v15H4zM4 10h16M8 3v5M16 3v5M12 13v5M10 18h4"/>',up:'<path d="m6 15 6-6 6 6"/>',down:'<path d="m6 9 6 6 6-6"/>',hint:'<path d="M8 16a7 7 0 1 1 8 0v2H8zM9 21h6"/>',back:'<path d="m10 5-7 7 7 7M3 12h12a5 5 0 0 1 5 5"/>',lock:'<path d="M6 10h12v11H6zM8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',mirror:'<path d="M12 2v20M3 6l6 6-6 6zM21 6l-6 6 6 6z"/>',overlap:'<path d="M3 3h12v12H3zM9 9h12v12H9z"/>',ok:'<path d="m4 12 5 5L20 5"/>'};
 function icon(k){return '<svg viewBox="0 0 24 24" fill="none" stroke="#59442d" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+(paths[k]||paths.lock)+'</svg>'}
 function button(k,label,id){return '<button type="button" class="rp-action" id="'+id+'" aria-label="'+label+'">'+icon(k)+'<span>'+label+'</span></button>'}
 function close(s,focus){if(!s||active!==s)return;active=null;if(s.panel&&s.panel.isConnected)closeModal();if(focus!==false&&s.origin&&s.origin.isConnected)try{s.origin.focus({preventScroll:true})}catch(e){}}
 function show(s,html,bind){
  if(active)close(active,false);active=s;s.loc=G.loc;s.tab=G.tab;s.ready=performance.now()+650;
  modal(html,function(){s.panel=document.querySelector('#mveil .modal');s.panel.classList.add('inn-room-puzzle');s.panel.dataset.puzzle=s.kind;s.panel.setAttribute('aria-modal','true');s.panel.setAttribute('aria-label',s.kind==='date'?'숫자 자물쇠: 달과 날':'털 자국과 봉인띠 비교');
   document.getElementById('mveil').onclick=function(e){if(e.target.id==='mveil')close(s)};bind();
  });
 }
 function message(s,text){var el=s.panel&&s.panel.querySelector('.rp-message');if(el)el.textContent=text}
 function rememberDigits(s){if(!valid(s))return;for(var i=0;i<4;i++)G.beats['inn_pin_d'+i]=s.digits[i];save()}
 function digit(s,i,step){if(!valid(s)||performance.now()<s.ready)return;s.digits[i]=(s.digits[i]+step+10)%10;paintDigits(s);rememberDigits(s);sound('tap')}
 function paintDigits(s){s.panel.querySelectorAll('#innpad [data-d]').forEach(function(b){var i=+b.dataset.d;b.textContent=s.digits[i];b.setAttribute('aria-label',(i<2?'달':'날')+' '+(i%2?'둘째':'첫째')+' 자리 '+s.digits[i])})}
 function clue(s){var p=s.panel.querySelector('.rp-clue');p.textContent=readDate()?EP.LOCK.clue:'머리판에 남은 자국을 먼저 살펴보자.'}
 function hint(s){if(!valid(s)||performance.now()<s.ready)return;s.hint=Math.min(2,s.hint+1);beat('inn_pin_hint',s.hint);beat('inn_lockhint',1);clue(s);message(s,!readDate()?'머리판을 직접 살펴보면 숫자의 뜻을 알 수 있을 거야.':s.hint===1?'날짜를 옮겨 보자. 달 두 칸, 날 두 칸.':'한 자리 날짜도 두 칸에 넣어야 해.');sound('tap')}
 function unlock(s){if(!valid(s)||performance.now()<s.ready)return;
  if(s.digits.join('')!==EP.LOCK.code){message(s,readDate()?'딸깍… 그대로야. 달과 날을 두 칸씩 넣었을까?':'딸깍… 그대로야. 머리판의 자국을 먼저 읽어 보자.');sound('huh');return}
  var game=s.game;close(s,false);if(G!==game||!inn())return;beat('inn_lock',1);
  say(EP.LOCK.open.map(function(x){return x.slice()}),function(){if(G===game&&inn())render()});
 }
 function openDate(origin){if(!available()||G.beats.inn_lock||active||pending)return;var game=G;
  if(EP.LOCK.permission&&!G.beats.inn_ledger_permission){var room=G.loc,tab=G.tab;say(EP.LOCK.permission.map(function(x){return x.slice()}),function(){if(G!==game||!inn()||G.loc!==room||G.tab!==tab)return;beat('inn_ledger_permission',1);
    // endDlg intentionally holds its previous frame for 700ms. The final
    // authored @dir lasts only 300ms, so its callback can precede that release.
    var wait={game:game,loc:room,tab:tab};pending=wait;var until=performance.now()+1800;(function ready(){if(pending!==wait)return;if(G!==game||!inn()||G.loc!==room||G.tab!==tab||G.beats.inn_lock||active||DL||window.__innCutting||document.querySelector('body>.rt,#innmove,#wmap,.banner,.placecard,#ov .modal,.crec2,#innopt,.innconf,#w209rail.more')){pending=null;return}if(available()){pending=null;openDate(origin);return}if(performance.now()<until)setTimeout(ready,40);else pending=null})();
   });return}
  var s={kind:'date',game:game,origin:origin,digits:[0,1,2,3].map(function(i){var v=G.beats['inn_pin_d'+i];return Number.isInteger(v)&&v>=0&&v<=9?v:0}),hint:G.beats.inn_pin_hint||0};
  var h='<header class="rp-heading">'+icon('lock')+'<b>숫자 자물쇠</b></header><p class="rp-clue"></p><div class="rp-date" id="innpad">';
  [['calendar','달',0],['day','날',2]].forEach(function(g){h+='<section class="rp-date-group"><div class="rp-date-label">'+icon(g[0])+'<span>'+g[1]+'</span></div><div class="rp-wheels">';for(var j=g[2];j<g[2]+2;j++)h+='<div class="rp-wheel"><button type="button" class="rp-number" data-d="'+j+'" title="누르면 한 칸 올라가요">0</button><button type="button" data-digit="'+j+'" data-step="-1" aria-label="'+g[1]+' '+(j%2?'둘째':'첫째')+' 자리 내리기">'+icon('down')+'</button></div>';h+='</div></section>'});
  h+='</div><div class="rp-actions">'+button('hint','도움','innhint')+button('back','닫기','innclose')+button('lock','열기','innopen')+'</div><p class="rp-message" id="innmsg" role="status" aria-live="polite">작은 손님을 돌본 기록이 있을까.</p>';
  show(s,h,function(){clue(s);paintDigits(s);s.panel.querySelectorAll('[data-digit]').forEach(function(b){b.onclick=function(){digit(s,+b.dataset.digit,+b.dataset.step)}});s.panel.querySelectorAll('[data-d]').forEach(function(b){b.onclick=function(){digit(s,+b.dataset.d,1)}});
   document.getElementById('innhint').onclick=function(){hint(s)};document.getElementById('innclose').onclick=function(){close(s)};document.getElementById('innopen').onclick=function(){unlock(s)};s.panel.querySelector('[data-d="0"]').focus({preventScroll:true});
  });
 }
 function mirrorPaint(s){var mark=s.panel.querySelector('.rp-ink-mark');mark.style.transform=s.mirrored?'scaleX(-1)':'none';s.panel.querySelector('#rp-mirror').setAttribute('aria-pressed',String(s.mirrored));s.panel.dataset.overlaid=String(s.overlaid);s.panel.querySelector('#rp-overlap').setAttribute('aria-pressed',String(s.overlaid));}
 function mirror(s){if(!valid(s)||performance.now()<s.ready)return;s.mirrored=!s.mirrored;s.overlaid=false;beat('inn_ink_mirror',s.mirrored?1:0);mirrorPaint(s);message(s,'기록 그림을 뒤집어 봉인띠와 비교해.');sound('page')}
 function compare(s){if(!valid(s)||performance.now()<s.ready)return;
  if(!s.mirrored){s.overlaid=false;mirrorPaint(s);message(s,'글씨의 방향이 달라. 털 자국을 옮긴 종이를 뒤집어 볼까?');sound('huh');return}
  s.overlaid=!s.overlaid;mirrorPaint(s);if(s.overlaid){beat('inn_ink_compared',1);message(s,'글씨와 별이 같은 방향이야. 왜 묻었는지는 회의에서 확인하자.');sound('select')}else message(s,'원래 기록 두 장을 나란히 살펴보자.');
 }
 function openInk(origin){if(!available()||!has('C01')||!has('C05')||active)return;
  var s={kind:'ink',game:G,origin:origin,mirrored:!!G.beats.inn_ink_mirror,overlaid:false};
  var h='<header class="rp-heading">'+icon('overlap')+'<b>붉은 자국 비교</b></header><p class="rp-clue">털 자국을 옮긴 종이와 봉인띠</p><div class="rp-ink-board"><section class="rp-seal"><span>봉인띠</span><div class="rp-ink-crop"><img src="art/ch1/closeup/I1-seal-strip-complete-512.png" alt="봉인띠의 세련 글씨와 꼬리가 말린 별"></div></section><section class="rp-trace"><span>털 자국 기록</span><div class="rp-ink-crop"><div class="rp-ink-mark"><img src="art/ch1/closeup/dormouse-flank-exact-overlay-512.png" alt="털 자국을 옮긴 거울상 기록"></div></div></section></div><div class="rp-actions">'+button('mirror','뒤집기','rp-mirror')+button('overlap','겹치기','rp-overlap')+button('back','닫기','rp-close')+'</div><p class="rp-message" role="status" aria-live="polite">기록 그림을 뒤집어 봉인띠와 비교해.</p>';
  show(s,h,function(){mirrorPaint(s);document.getElementById('rp-mirror').onclick=function(){mirror(s)};document.getElementById('rp-overlap').onclick=function(){compare(s)};document.getElementById('rp-close').onclick=function(){close(s)};document.getElementById('rp-mirror').focus({preventScroll:true})});
 }
 // Catch the native lock only after inn_input's window capture guard has allowed
 // this gesture. A dialogue that is still active never starts a puzzle.
 window.addEventListener('click',function(e){if(!inn()||!e.target.closest)return;if(pending&&e.target.closest('#w209rail,#w209more'))pending=null;var b=e.target.closest('#bigscene [data-obs="o_inn_lock"]');if(!b)return;e.stopImmediatePropagation();e.preventDefault();if(available())openDate(b)},true);
 function attachInk(){if(!available()||!has('C01')||!has('C05'))return;
  var records=document.querySelector('.crec2'),selected=records&&records.querySelector('.cr-th.on'),id=selected&&selected.dataset.crs;
  var detail=records&&records.querySelector('.cr-det .cr-tx'),inspect=document.querySelector('#innins .ihd b'),host=null;
  if(detail&&(id==='C01'||id==='C05'))host=detail.querySelector('.orig9 .e9opt');
  else if(inspect&&/옆구리털/.test(inspect.textContent))host=document.querySelector('#innins .ibtns');
  document.querySelectorAll('[data-room-puzzle="ink"]').forEach(function(b){if(b.parentNode!==host)b.remove()});
  if(!host||host.querySelector('[data-room-puzzle="ink"]'))return;
  var b=document.createElement('button');b.type='button';b.className='rp-study';b.dataset.roomPuzzle='ink';b.innerHTML=icon('overlap')+'<span>겹쳐 보기</span>';b.setAttribute('aria-label','털 자국과 봉인띠 겹쳐 보기');b.onclick=function(e){e.stopPropagation();openInk(b)};host.appendChild(b);
 }
 window.addEventListener('keydown',function(e){if(pending&&e.key==='Escape'){pending=null;e.preventDefault();e.stopImmediatePropagation();return}var s=active;if(!s)return;if(!valid(s)){close(s,false);return}
  if(e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();close(s);return}
  if(e.key==='Tab'){var bs=Array.prototype.slice.call(s.panel.querySelectorAll('button:not(:disabled)')),at=bs.indexOf(document.activeElement);e.preventDefault();e.stopImmediatePropagation();bs[(at+(e.shiftKey?-1:1)+bs.length)%bs.length].focus();return}
  if(e.repeat||performance.now()<s.ready){e.preventDefault();e.stopImmediatePropagation();return}
  var b=document.activeElement,index=b&&b.dataset.d!=null?+b.dataset.d:0;
  if(s.kind==='date'&&/^\d$/.test(e.key)){e.preventDefault();e.stopImmediatePropagation();s.digits[index]=+e.key;paintDigits(s);rememberDigits(s);s.panel.querySelector('[data-d="'+Math.min(3,index+1)+'"]').focus();sound('tap');return}
  if(s.kind==='date'&&/^Arrow/.test(e.key)){e.preventDefault();e.stopImmediatePropagation();if(e.key==='ArrowUp'||e.key==='ArrowDown')digit(s,index,e.key==='ArrowUp'?1:-1);else s.panel.querySelector('[data-d="'+((index+(e.key==='ArrowRight'?1:3))%4)+'"]').focus();return}
  if(s.kind==='date'&&e.key==='Backspace'){e.preventDefault();e.stopImmediatePropagation();s.digits[index]=0;paintDigits(s);rememberDigits(s);s.panel.querySelector('[data-d="'+Math.max(0,index-1)+'"]').focus();return}
  if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopImmediatePropagation();if(s.kind==='date'&&b&&b.dataset.d!=null)unlock(s);else if(b&&s.panel.contains(b)&&typeof b.onclick==='function')b.onclick();}
 },true);
 // Unlike the original boolean-only beat sanitizer, preserve only our bounded
 // integer drafts. Old saves without these fields still open at 0000.
 var sanitize=sanitizeState;sanitizeState=function(d){var keys=['inn_pin_d0','inn_pin_d1','inn_pin_d2','inn_pin_d3','inn_pin_hint'],g=d&&d.prog&&d.prog.inn,raw={};keys.forEach(function(k){if(g&&g.beats){var v=g.beats[k],max=k==='inn_pin_hint'?2:9;if(Number.isInteger(v)&&v>=0&&v<=max)raw[k]=v}});var out=sanitize(d),n=out.prog&&out.prog.inn;if(n&&n.beats)keys.forEach(function(k){delete n.beats[k];if(Object.prototype.hasOwnProperty.call(raw,k))n.beats[k]=raw[k]});return out};
 // Keep the information boundary even if another integration calls the legacy
 // pad. Opening a UI does not count as observing the authored headboard.
 var authoredClue=EP.LOCK.clue;
 Object.defineProperty(EP.LOCK,'clue',{configurable:true,enumerable:true,get:function(){return readDate()?authoredClue:'머리판에 남은 자국을 먼저 살펴보자.'}});
 Object.defineProperty(EP.LOCK,'hint',{configurable:true,enumerable:true,get:function(){return ['det1',readDate()?'달 두 칸, 날 두 칸. 날짜를 옮겨 보자.':'머리판부터 보자. 숫자 힌트가 있을까?']}});
 var css=document.createElement('style');css.id='inn-room-puzzle-style';css.textContent=`
 html body.inn1 #ov:has(.inn-room-puzzle){z-index:205!important}
 html body.inn1 #ov #mveil:has(.inn-room-puzzle){z-index:205!important;background:#11131ab8}
 html body.inn1 #ov .modal.inn-room-puzzle{box-sizing:border-box!important;display:block!important;gap:0!important;width:min(580px,calc(100vw - 24px))!important;max-width:none!important;max-height:calc(100vh - 20px)!important;overflow:auto!important;min-height:0!important;padding:15px 20px 12px!important;border:2px solid #947248!important;border-radius:8px!important;background:#f5eddb!important;color:#493725!important;box-shadow:0 8px 24px #07080a80!important;text-align:center!important;background-image:none!important}
 html body.inn1 #ov .inn-room-puzzle::before,html body.inn1 #ov .inn-room-puzzle::after{display:none!important}
 .inn-room-puzzle .rp-heading{display:flex;align-items:center;justify-content:center;gap:9px;font:19px/1.3 var(--display,sans-serif);margin:0}
 .inn-room-puzzle svg,.rp-study svg{display:block;width:24px;height:24px;flex:none;pointer-events:none}
 .inn-room-puzzle .rp-clue{font:13px/1.5 var(--display,sans-serif);margin:8px 0 12px!important;min-height:20px}
 .inn-room-puzzle .rp-date{display:flex!important;justify-content:center;gap:26px!important;margin:0 0 12px!important}
 .inn-room-puzzle .rp-date-label{display:flex;align-items:center;justify-content:center;gap:6px;font:12px/1.3 var(--display,sans-serif);margin-bottom:5px}
 .inn-room-puzzle .rp-wheels{display:flex;gap:6px}.inn-room-puzzle .rp-wheel{display:grid;gap:3px}
 html body.inn1 #ov .inn-room-puzzle .rp-wheel button{all:unset;display:flex!important;box-sizing:border-box!important;align-items:center;justify-content:center;width:52px!important;height:44px!important;min-height:0!important;color:#493725!important;background:#e5d6b5!important;border:1px solid #ad946a!important;border-radius:3px!important;cursor:pointer!important}
 html body.inn1 #ov .inn-room-puzzle .rp-wheel .rp-number{height:52px!important;background:#fff9ec!important;font:28px/1 var(--display,sans-serif)!important;border:2px solid #8c7350!important}
 .inn-room-puzzle .rp-actions{display:flex;justify-content:center;gap:8px}
 html body.inn1 #ov .inn-room-puzzle .rp-action,.rp-study{all:unset;box-sizing:border-box!important;display:inline-flex!important;align-items:center;justify-content:center;gap:6px;cursor:pointer!important;border:1px solid #aa8f61!important;border-radius:4px!important;background:#e8d8b6!important;color:#493725!important;font:13px/1.2 var(--display,sans-serif)!important;min-height:44px!important;padding:7px 12px!important;white-space:nowrap!important}
 html body.inn1 #ov .inn-room-puzzle .rp-action{flex:1;max-width:154px}
 html body.inn1 #ov .inn-room-puzzle .rp-action[aria-pressed="true"]{background:#d2c28e!important;border-color:#695733!important}
 html body.inn1 #ov .inn-room-puzzle button:focus-visible,.rp-study:focus-visible{outline:3px solid #3c706d!important;outline-offset:2px!important}
 .inn-room-puzzle .rp-message{font:12px/1.5 var(--display,sans-serif);min-height:36px!important;margin:9px 0 0!important;color:#6f5337!important}
 .rp-study{position:relative!important;z-index:1;margin:8px 0!important;flex:none!important}.rp-study svg{width:21px;height:21px}
 /* Native all:unset removed the relative anchor from these buttons. Their
    enlarged ::after areas then covered the entire 562px record detail panel. */
 html body.w209.inn1 .crec2 .orig9 .e9opt button.e9b{position:relative!important}
 .inn-room-puzzle .rp-ink-board{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:16px;height:190px;margin:0 0 12px}
 .inn-room-puzzle .rp-ink-board section{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:0;background:#ede0c4;border:1px solid #b7a078;border-radius:4px;font:12px/1.3 var(--display,sans-serif)}
 .inn-room-puzzle .rp-ink-board section>span{position:absolute;top:4px;left:0;right:0;text-align:center}
 .inn-room-puzzle .rp-ink-crop{position:relative;flex:none;width:110px;height:145px;overflow:hidden;image-rendering:pixelated}
 .inn-room-puzzle .rp-seal img{position:absolute;width:512px;max-width:none!important;height:512px;left:-201px;top:-159px;image-rendering:pixelated}
 .inn-room-puzzle .rp-ink-mark{position:absolute;inset:0;transform-origin:55px 72.5px}
 .inn-room-puzzle .rp-trace img{position:absolute;width:512px;max-width:none!important;height:512px;left:-201px;top:-159px;image-rendering:pixelated}
 .inn-room-puzzle[data-overlaid="true"] .rp-ink-board{display:block}
 .inn-room-puzzle[data-overlaid="true"] .rp-ink-board section{position:absolute;left:50%;top:0;transform:translateX(-50%);width:220px;height:190px}
 .inn-room-puzzle[data-overlaid="true"] .rp-trace{border-color:transparent;background:transparent!important}
 .inn-room-puzzle[data-overlaid="true"] .rp-trace>span{visibility:hidden}
 .inn-room-puzzle[data-overlaid="true"] .rp-trace .rp-ink-crop{opacity:.58}
 @media(max-height:430px){html body.inn1 #ov .modal.inn-room-puzzle{padding:10px 16px 8px!important}.inn-room-puzzle .rp-clue{margin:5px 0 7px!important}.inn-room-puzzle .rp-date{margin-bottom:9px!important}.inn-room-puzzle .rp-date-label{margin-bottom:3px}html body.inn1 #ov .inn-room-puzzle .rp-wheel button{height:44px!important}html body.inn1 #ov .inn-room-puzzle .rp-wheel .rp-number{height:44px!important}.inn-room-puzzle .rp-ink-board{height:160px;margin-bottom:9px}.inn-room-puzzle[data-overlaid="true"] .rp-ink-board section{height:160px}.inn-room-puzzle .rp-message{margin-top:7px!important;min-height:32px!important}}
 @media(prefers-reduced-motion:no-preference){.inn-room-puzzle .rp-ink-mark{transition:transform .25s ease}.inn-room-puzzle{animation:rp-appear .18s ease-out}@keyframes rp-appear{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}}
 `;document.head.appendChild(css);
 setInterval(function(){if(active&&(!valid(active)||(active.kind==='date'&&G.beats.inn_lock)))close(active,false);if(!active)attachInk()},180);
})();
