/* A quiet Chapter 2 peek after the native Chapter 1 ending. This is a
   presentation transaction, not an additional case, clue or paid entry. */
(function(){
 'use strict';
 var active=null,replay=null,reduce=matchMedia('(prefers-reduced-motion: reduce)');
 function inn(){try{return S.screen==='case'&&G&&CASES[G.ci]&&CASES[G.ci].id==='inn'}catch(e){return false}}
 function ended(){return !!(inn()&&G.beats&&G.beats.inn_end)}
 function idle(){return ended()&&!DL&&!window.__dlFreeze&&!window.__innCutting&&!document.querySelector('body>.rt,#innmain,#inncold,#ov .modal,#dlgveil,#innmove,#wmap,.banner,.placecard,#innopt,.innconf,.crec2,#innins,#w209rail.more')}
 function valid(s){return !!(s&&active===s&&!s.closed&&G===s.game&&S.screen===s.screen&&ended()&&G.loc===s.loc&&G.tab===s.tab&&s.node&&s.node.isConnected)}
 function timer(s,delay,fn){var id=setTimeout(function(){var i=s.timers.indexOf(id);if(i>=0)s.timers.splice(i,1);if(!valid(s)){dispose(s,false);return}fn()},delay);s.timers.push(id)}
 function phase(s,key){if(!valid(s))return;s.node.dataset.stage=key;s.phase=key}
 function gate(on){try{if(window.__AUD&&__AUD.sceneGate)__AUD.sceneGate(on);else window.__innAudioHold=!!on}catch(e){window.__innAudioHold=!!on}}
 function dispose(s,success){
  if(!s||active!==s||s.closed)return;
  var current=valid(s),done=success&&current?s.done:null;s.closed=true;active=null;
  s.timers.forEach(clearTimeout);s.timers=[];if(s.watch)clearInterval(s.watch);
  if(s.node)s.node.remove();document.body.classList.remove('inn-ch2-peek-active');
  s.inert.forEach(function(x){if(x.el.isConnected)x.el.inert=x.old});
  // Do not release another scene's audio hold after a loaded game replaces us.
  if(s.held&&window.__innChapter2AudioOwner===s){delete window.__innChapter2AudioOwner;if(!document.getElementById('inncold'))gate(false)}
  if(success&&current){s.game.beats=s.game.beats||{};s.game.beats.inn_ch2_peek_seen=true;try{saveProg()}catch(e){}}
  if(current&&s.focus&&s.focus.isConnected)try{s.focus.focus({preventScroll:true})}catch(e){}
  // A stale completion never advances or renders the newly loaded game.
  if(done)done();
 }
 function finish(s,e){if(!valid(s)||!s.ready||performance.now()<s.readyAt)return;
  if(e&&e.type==='click'&&e.detail>0&&s.down<s.readyAt)return;
  dispose(s,true);
 }
 function svg(){
  var flakes='';for(var i=0;i<34;i++){var x=235+(i*97%491),y=89+(i*71%256),o=(i%3===0?.6:.25);flakes+='<rect x="'+x+'" y="'+y+'" width="'+(i%4===0?3:2)+'" height="2" fill="#d3dfdc" opacity="'+o+'"/>'}
  function star(x,klass){return '<g class="peek-foil '+(klass||'')+'" transform="translate('+x+' 332)"><path d="M0-16 5-5 17-5 8 3 11 16 0 9-11 16-8 3-17-5-5-5Z" fill="#b9c9c4"/><path d="M0-16 0 9-8 3Z" fill="#e9f1de"/><path d="M0-16 5-5 17-5 0 0Z" fill="#7b9295"/><path d="M0 0 17-5 8 3 11 16Z" fill="#d9e5d2"/><path d="M0 0 0 9-11 16-8 3Z" fill="#809c9b"/><path d="m-3-8 4 2 4-1M-8 5-3 4" fill="none" stroke="#f2f4dc" stroke-width="1"/></g>'}
  return '<svg class="peek-window" viewBox="0 0 960 480" role="img" aria-label="눈 내리는 여관 창틀. 은박별 세 개 중 가운데 별이 사라진다.">'+
   '<defs><linearGradient id="peek-night" x2="0" y2="1"><stop stop-color="#141f2b"/><stop offset="1" stop-color="#34494b"/></linearGradient><linearGradient id="peek-room" x2="0" y2="1"><stop stop-color="#05070b"/><stop offset="1" stop-color="#111515"/></linearGradient></defs>'+
   '<rect width="960" height="480" fill="url(#peek-room)"/><path d="M181 54H779V390H181Z" fill="#12171a"/><rect x="215" y="75" width="530" height="293" fill="url(#peek-night)"/>'+
   '<path d="m218 260 44-39 51 14 51-47 78 46 57-33 47 38 77-44 48 23 73-26v166H218Z" fill="#26383c"/><path d="M218 333l53-9 77 14 107-10 104 8 70-13 116 9v36H218Z" fill="#647674" opacity=".32"/>'+
   '<g class="peek-snow">'+flakes+'</g><path d="M222 83H738" stroke="#92a29d" opacity=".17"/><path d="M226 82V339M502 82V339" stroke="#9eaca6" opacity=".1"/>'+
   '<path d="M204 66H756V82H204ZM204 66H220V359H204ZM740 66H756V359H740ZM466 79H482V359H466ZM218 203H742V217H218Z" fill="#302c28"/><path d="M204 66H756V72H204ZM204 66H210V359H204ZM466 79H471V359H466" fill="#4a4135"/><path d="M218 83H222V349H218ZM482 83H486V349H482" fill="#101619"/>'+
   '<path d="M192 351H768V373H192ZM181 373H779V388H181Z" fill="#40382d"/><path d="M192 351H768V357H192Z" fill="#77664c"/><path d="M181 373H779V378H181Z" fill="#574b38"/><path d="M205 363H742" stroke="#aaa185" opacity=".15"/>'+
   star(333,'')+star(479,'peek-stolen')+star(625,'')+
   '<g class="peek-empty"><path d="m467 347 7-3 10 3" fill="none" stroke="#9e9c7e" stroke-width="2" opacity=".34"/><rect x="486" y="344" width="3" height="2" fill="#c2c7aa" opacity=".42"/></g>'+
   '<path d="M183 56H207V347H183ZM755 56H779V347H755Z" fill="#080b0e"/><path d="M0 0H960V480H0ZM175 47V391H787V47Z" fill="#010305" fill-rule="evenodd" opacity=".28"/></svg>';
 }
 function open(done,fromReplay){
  if(active||!idle()||window.__innAudioHold)return false;
  var s={game:G,screen:S.screen,loc:G.loc,tab:G.tab,done:typeof done==='function'?done:null,closed:false,timers:[],ready:false,readyAt:Infinity,down:-Infinity,inert:[],focus:document.activeElement,phase:'black'};
  var node=document.createElement('section');s.node=node;node.id='inn-ch2-peek';node.dataset.stage='black';node.setAttribute('role','dialog');node.setAttribute('aria-modal','true');node.setAttribute('aria-label','2장 예고');node.tabIndex=-1;
  node.innerHTML='<div class="peek-frame">'+svg()+'<div class="peek-black" aria-hidden="true"></div><div class="peek-caption" aria-live="polite"><p class="peek-number">2장</p><h2>까마귀의 둥지</h2><p class="peek-question">창밖의 반짝이는 것은 누가 가져갔을까?</p><button type="button" class="peek-finish" disabled>예고 마치기</button></div></div>';
  active=s;document.body.appendChild(node);document.body.classList.add('inn-ch2-peek-active');
  ['app','ov'].forEach(function(id){var el=document.getElementById(id);if(el){s.inert.push({el:el,old:el.inert});el.inert=true}});
  if(replay){replay.remove();replay=null}
  s.held=true;window.__innChapter2AudioOwner=s;gate(true);
  try{node.focus({preventScroll:true})}catch(e){}
  node.addEventListener('click',function(e){e.preventDefault();e.stopImmediatePropagation();if(e.target.closest('.peek-finish'))finish(s,e)},true);
  node.addEventListener('pointerdown',function(){s.down=performance.now()},true);
  timer(s,650,function(){phase(s,'knock');try{if(S.sound&&SFX.knock)SFX.knock()}catch(e){}});
  timer(s,1350,function(){phase(s,'window')});
  timer(s,3300,function(){phase(s,'missing')});
  timer(s,4050,function(){phase(s,'title')});
  timer(s,4700,function(){phase(s,'ready');s.ready=true;s.readyAt=performance.now();var b=node.querySelector('.peek-finish');b.disabled=false;try{b.focus({preventScroll:true})}catch(e){}});
  s.watch=setInterval(function(){if(!valid(s)||DL)dispose(s,false)},40);
  return true;
 }
 window.__innChapter2Peek=function(done){return open(done,false)};
 window.__innChapter2PeekState=function(){return active?{active:true,stage:active.phase,ready:active.ready,reduced:reduce.matches}: {active:false,seen:!!(ended()&&G.beats.inn_ch2_peek_seen)}};
 window.__innChapter2PeekReset=function(){if(active)dispose(active,false)};
 window.addEventListener('keydown',function(e){var s=active;if(!s)return;if(!valid(s)){dispose(s,false);return}
  if(e.key==='Tab'){e.preventDefault();e.stopImmediatePropagation();if(s.ready)s.node.querySelector('.peek-finish').focus();else s.node.focus();return}
  if(e.key==='Enter'||e.key===' '||e.key==='Escape'){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)finish(s);return}
  // Stop game shortcuts while allowing the browser's own reload/zoom keys.
  e.stopImmediatePropagation();
 },true);
 function syncReplay(){
  if(active)return;
  if(!idle()){if(replay){replay.remove();replay=null}return}
  if(replay&&replay.isConnected)return;
  replay=document.createElement('button');replay.type='button';replay.id='inn-ch2-replay';replay.setAttribute('aria-label','2장 예고 다시 보기');
  replay.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 7 7 1-5 5 1 7-6-4-6 4 1-7-5-5 7-1Z"/></svg><span>2장 예고</span>';
  replay.onclick=function(e){e.stopPropagation();var game=G;open(function(){if(G===game&&ended())render()},true)};document.body.appendChild(replay);
 }
 var css=document.createElement('style');css.id='inn-ch2-peek-style';css.textContent=`
 #inn-ch2-peek{position:fixed!important;inset:0!important;z-index:10020!important;background:#020305!important;display:flex!important;align-items:center!important;justify-content:center!important;overflow:hidden!important;isolation:isolate;color:#ece9d8!important;outline:none!important;touch-action:manipulation}
 #inn-ch2-peek .peek-frame{position:relative;width:min(100vw,1280px);height:100%;display:flex;align-items:center;justify-content:center;overflow:hidden}
 #inn-ch2-peek .peek-window{position:absolute;width:100%;height:100%;inset:0;object-fit:contain;opacity:0;transition:opacity .85s ease;pointer-events:none}
 #inn-ch2-peek .peek-black{position:absolute;inset:0;background:#020305;opacity:1;transition:opacity .9s ease;pointer-events:none}
 #inn-ch2-peek[data-stage="window"] .peek-window,#inn-ch2-peek[data-stage="missing"] .peek-window{opacity:1}
 #inn-ch2-peek[data-stage="window"] .peek-black,#inn-ch2-peek[data-stage="missing"] .peek-black{opacity:0}
 #inn-ch2-peek .peek-stolen{opacity:1;transition:opacity .14s ease-out}
 #inn-ch2-peek .peek-empty{opacity:0;transition:opacity .3s ease}
 #inn-ch2-peek[data-stage="missing"] .peek-stolen,#inn-ch2-peek[data-stage="title"] .peek-stolen,#inn-ch2-peek[data-stage="ready"] .peek-stolen{opacity:0}
 #inn-ch2-peek[data-stage="missing"] .peek-empty,#inn-ch2-peek[data-stage="title"] .peek-empty,#inn-ch2-peek[data-stage="ready"] .peek-empty{opacity:1}
 #inn-ch2-peek[data-stage="title"] .peek-window,#inn-ch2-peek[data-stage="ready"] .peek-window{opacity:.38}
 #inn-ch2-peek[data-stage="title"] .peek-black,#inn-ch2-peek[data-stage="ready"] .peek-black{opacity:.32}
 #inn-ch2-peek .peek-caption{position:relative;z-index:2;text-align:center;padding:22px 18px;opacity:0;visibility:hidden;transform:translateY(5px);transition:opacity .65s ease,transform .65s ease;box-sizing:border-box;width:min(90vw,600px)}
 #inn-ch2-peek[data-stage="title"] .peek-caption,#inn-ch2-peek[data-stage="ready"] .peek-caption{visibility:visible;opacity:1;transform:none}
 #inn-ch2-peek .peek-number{font:12px/1.5 var(--display,sans-serif)!important;letter-spacing:.28em!important;color:#baa98a!important;margin:0 0 10px!important}
 #inn-ch2-peek h2{font:clamp(25px,4.4vw,43px)/1.5 var(--display,sans-serif)!important;letter-spacing:.14em!important;color:#eee9d4!important;margin:0 0 18px!important;font-weight:400!important;text-shadow:0 3px 16px #000!important}
 #inn-ch2-peek .peek-question{font:clamp(12px,1.65vw,16px)/1.65 var(--display,sans-serif)!important;color:#d4d2c7!important;margin:0!important;word-break:keep-all!important;text-shadow:0 2px 12px #000!important}
 html body #inn-ch2-peek .peek-finish{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:9px 22px;margin:25px 0 0;border:1px solid #76694e;border-radius:4px;font:14px/1.3 var(--display,sans-serif);color:#e9ddbb;background:#171716c7;cursor:pointer;opacity:1;transition:opacity .3s ease}
 html body #inn-ch2-peek .peek-finish:disabled{visibility:hidden;pointer-events:none;opacity:0}
 html body #inn-ch2-peek .peek-finish:focus-visible{outline:2px solid #d7c79b;outline-offset:4px}
 html body #inn-ch2-replay{all:unset;box-sizing:border-box;position:fixed;left:calc(14px + env(safe-area-inset-left,0px));bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:90;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:7px 13px;font:13px/1.3 var(--display,sans-serif);background:#252b2bf0;border:1px solid #9d947c;border-radius:5px;color:#e2dfcd;box-shadow:0 3px 10px #0005;cursor:pointer}
 #inn-ch2-replay svg{width:20px;height:20px;fill:#bccdca;stroke:#e1e5d5;stroke-width:.5;pointer-events:none}
 #inn-ch2-replay:focus-visible{outline:3px solid #d0aa68;outline-offset:3px}
 @media(max-height:380px){#inn-ch2-peek .peek-caption{padding:10px 18px}#inn-ch2-peek h2{margin-bottom:12px!important}html body #inn-ch2-peek .peek-finish{margin-top:16px}}
 @media(max-aspect-ratio:3/4){#inn-ch2-peek .peek-window{width:160%;height:68%;left:-30%;top:3%}#inn-ch2-peek .peek-caption{margin-top:24vh}#inn-ch2-peek[data-stage="title"] .peek-window,#inn-ch2-peek[data-stage="ready"] .peek-window{opacity:.33}}
 @media(prefers-reduced-motion:reduce){#inn-ch2-peek .peek-window,#inn-ch2-peek .peek-black,#inn-ch2-peek .peek-stolen,#inn-ch2-peek .peek-empty,#inn-ch2-peek .peek-caption,#inn-ch2-peek .peek-finish{transition:none!important;transform:none!important;animation:none!important}}
 `;document.head.appendChild(css);
 setInterval(function(){if(active&&!valid(active))dispose(active,false);syncReplay()},120);
 // Keep an explicit boolean through the native bounded save sanitizer.
 var sanitizer=sanitizeState;sanitizeState=function(d){var g=d&&d.prog&&d.prog.inn,seen=!!(g&&g.beats&&(g.beats.inn_ch2_peek_seen===true||g.beats.inn_ch2_peek_seen===1)),out=sanitizer(d),n=out.prog&&out.prog.inn;if(n&&n.beats){delete n.beats.inn_ch2_peek_seen;if(seen)n.beats.inn_ch2_peek_seen=true}return out};
})();
