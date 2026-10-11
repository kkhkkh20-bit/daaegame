/* A private visual observation in E4, not a public proof or another quiz.
   The two papers are UI diagrams of the already-authored handwriting; this
   module does not replace an illustration or disclose another guest's line. */
(function(){
 'use strict';
 var active=null,last={visible:false,compared:false,recorded:false,scene:null,reason:'idle'};
 function scene(){try{
  if(!G||!S||S.screen!=='case'||!CASES[G.ci]||CASES[G.ci].id!=='inn'||!G.beats||!G.beats.inn_final||G.beats.inn_end)return null;
  return window.EP1INN&&window.EP1INN.END&&window.EP1INN.END[G.beats.inn_ei]||null;
 }catch(e){return null}}
 function valid(s){var sc=scene();return !!(active===s&&!s.closed&&G===s.game&&sc&&sc.sid==='E4'&&!document.getElementById('innmain'))}
 function state(s,reason){var sc=scene();return {
  visible:!!(s&&active===s&&!s.closed&&s.el&&s.el.isConnected),
  compared:!!(s&&s.compared),recorded:!!(s&&s.game&&s.game.beats&&s.game.beats.inn_mother_lead),
  scene:sc&&sc.sid||null,reason:reason||s&&s.reason||'idle'
 }}
 function sound(){try{if(typeof SFX!=='undefined'&&SFX.page)SFX.page()}catch(e){}}
 function cleanup(s,reason){
  if(!s||s.closed)return;s.closed=true;s.reason=reason||'closed';clearInterval(s.watch);clearTimeout(s.focusTimer);
  document.removeEventListener('keydown',s.key,true);
  if(s.el)s.el.remove();if(active===s){active=null;document.body.classList.remove('inn-mother-lead-open')}
  last=state(s,s.reason);last.visible=false;
 }
 function finish(s,reason){
  if(!valid(s)){cleanup(s,'stale');return}
  var cb=s.done;cleanup(s,reason);
  // The paused @inspect continuation has its own captured game check. Avoid
  // restoring focus to a removed dialogue button before that continuation.
  if(typeof cb==='function')cb();
 }
 function ink(){return '<svg class="mother-ink" viewBox="0 0 220 145" role="img" aria-label="다. 마지막 세로획이 길게 이어져 꼬리를 만든다">'+
  '<path class="mother-letter" d="M38 39 C55 38 73 39 85 38 M39 40 L38 91 Q38 99 47 98 L86 97 M110 31 L109 93 Q108 116 130 119 Q156 124 180 105 M110 60 L146 60"/>'+
  '<path class="mother-tail" d="M109 93 Q108 116 130 119 Q156 124 180 105"/>'+
  '</svg>'}
 var ICON={
  compare:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="12" height="14" rx="1"/><rect x="9" y="8" width="12" height="13" rx="1"/><path d="M6 8h5M12 12h6M12 16h6"/></svg>',
  record:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h11l3 3v15H5zM8 12l3 3 6-6M15 3v4h4"/></svg>',
  close:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
 };
 function action(s,k){
  if(!valid(s)){cleanup(s,'stale');return}
  var now=performance.now();if(now-s.lastAction<180)return;s.lastAction=now;
  if(k==='compare'){
   if(s.compared)return;s.compared=true;s.el.dataset.compared='true';s.reason='compared';
   // The only write is a private observation beat, after the actual button.
   s.game.beats.inn_mother_lead=1;try{saveProg()}catch(e){}
   s.el.querySelector('[data-mother-conclusion]').textContent='같은 긴 꼬리. 엄마 글씨가 이 여관에 남았다.';
   s.el.querySelector('[data-mother-action="compare"]').hidden=true;
   var record=s.el.querySelector('[data-mother-action="record"]');record.classList.remove('mother-quiet');
   record.innerHTML=ICON.record+'<span>기록</span>';sound();
   try{record.focus({preventScroll:true})}catch(e){}
  }else if(k==='record')finish(s,s.compared?'recorded':'continued');
  else if(k==='close')finish(s,'closed');
 }
 function mount(s){
  var el=s.el=document.createElement('div');el.id='inn-mother-lead';el.dataset.compared='false';
  el.setAttribute('role','dialog');el.setAttribute('aria-modal','true');el.setAttribute('aria-labelledby','mother-lead-title');
  el.innerHTML='<section class="mother-desk"><header class="mother-heading"><div><small>두 글씨</small><h2 id="mother-lead-title">남겨진 한 줄</h2></div>'+
   '<button type="button" class="mother-close" data-mother-action="close" aria-label="관찰을 닫고 계속">'+ICON.close+'</button></header>'+
   '<div class="mother-papers" aria-label="책 이름표와 장부에 남은 글씨 비교">'+
    '<figure class="mother-paper mother-book" data-mother-paper="book"><figcaption>서점 책 이름표</figcaption><div class="mother-ruled">'+ink()+'</div></figure>'+
    '<figure class="mother-paper mother-ledger" data-mother-paper="ledger"><figcaption>장부의 한 줄</figcaption><div class="mother-ruled">'+ink()+'</div></figure>'+
   '</div><p class="mother-conclusion" data-mother-conclusion aria-live="polite">책 이름표와 나란히 놓아 본다.</p>'+
   '<footer class="mother-actions"><button type="button" data-mother-action="compare">'+ICON.compare+'<span>겹쳐보기</span></button>'+
    '<button type="button" class="mother-quiet" data-mother-action="record"><span>계속</span></button></footer></section>';
  s.pointerStart=null;
  el.addEventListener('pointerdown',function(e){if(valid(s)&&el.contains(e.target))s.pointerStart=performance.now()});
  el.addEventListener('click',function(e){e.stopPropagation();var b=e.target.closest('[data-mother-action]');
   // A real press must begin in this newly opened panel. A release from the
   // previous dialogue cannot accidentally compare or close the papers.
   if(e.isTrusted&&e.detail>0&&s.pointerStart==null)return;s.pointerStart=null;
   if(b&&el.contains(b))action(s,b.dataset.motherAction)});
  // Catch keyboard input before the engine's dialogue/shortcut handlers.
  s.key=function(e){
   if(active!==s)return;if(!valid(s)){cleanup(s,'stale');return}
   if(e.key==='Escape'||e.key==='Enter'||e.key===' '){
    e.preventDefault();e.stopImmediatePropagation();if(e.repeat)return;
    if(e.key==='Escape')action(s,'close');
    else {var b=document.activeElement;if(b&&el.contains(b)&&b.dataset.motherAction)action(s,b.dataset.motherAction)}
   }else if(e.key==='Tab'){
    e.preventDefault();e.stopImmediatePropagation();
    var bs=Array.prototype.slice.call(el.querySelectorAll('button')).filter(function(b){return !b.hidden&&!b.disabled});
    var i=bs.indexOf(document.activeElement);i=(i+(e.shiftKey?-1:1)+bs.length)%bs.length;if(bs[i])bs[i].focus();
   }else if(/^(Arrow|Page|Home|End)/.test(e.key))e.stopImmediatePropagation();
  };
  document.body.appendChild(el);document.body.classList.add('inn-mother-lead-open');document.addEventListener('keydown',s.key,true);
  s.focusTimer=setTimeout(function(){if(!valid(s)){cleanup(s,'stale');return}var b=el.querySelector('[data-mother-action="compare"]');try{b.focus({preventScroll:true})}catch(e){}},0);
  s.watch=setInterval(function(){if(!valid(s)||!el.isConnected)cleanup(s,'stale')},80);sound();
 }
 window.__innMotherLead=function(done){
  var sc=scene();
  if(active){if(valid(active))return;cleanup(active,'superseded')}
  if(!sc||sc.sid!=='E4'||document.getElementById('innmain')){last={visible:false,compared:false,recorded:false,scene:sc&&sc.sid||null,reason:'unavailable'};if(typeof done==='function')done();return}
  var s=active={game:G,done:done,el:null,compared:false,closed:false,lastAction:-Infinity,watch:0,focusTimer:0,reason:'open'};
  try{mount(s)}catch(e){var canContinue=valid(s);cleanup(s,'unavailable');if(canContinue&&typeof done==='function')done()}
 };
 window.__innMotherLeadState=function(){return active?state(active):Object.assign({},last)};
 var css=document.createElement('style');css.id='inn-mother-lead-style';css.textContent=[
  '#inn-mother-lead{position:fixed;inset:0;z-index:150;box-sizing:border-box;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(19,15,12,.85);color:#37291f}',
  '#inn-mother-lead *{box-sizing:border-box}#inn-mother-lead .mother-desk{width:min(680px,100%);max-height:calc(100dvh - 32px);overflow:auto;border:1px solid #aa8a5b;border-radius:12px;padding:18px 24px;background:radial-gradient(ellipse at 45% 0%,#f7edd8 0%,#eadebe 80%);box-shadow:0 0 0 3px #392c21,0 18px 60px #0007}',
  '#inn-mother-lead .mother-heading{display:flex;align-items:center;justify-content:space-between;gap:12px}#inn-mother-lead .mother-heading small{font-size:12px;letter-spacing:.12em;color:#80694d}#inn-mother-lead h2{font-family:var(--display,sans-serif);font-size:22px;font-weight:700;margin:4px 0 0;line-height:1.3}',
  '#inn-mother-lead .mother-papers{position:relative;height:204px;margin:16px 0 2px}#inn-mother-lead .mother-paper{position:absolute;top:8px;width:45%;height:175px;margin:0;padding:12px 14px 6px;border:1px solid #bda57c;background:linear-gradient(100deg,#f7edce,#fff7e0 70%,#ecddba);box-shadow:2px 5px 10px #392a2226;transition:left .38s ease,top .38s ease,transform .38s ease,background .38s ease}',
  '#inn-mother-lead .mother-book{left:0;transform:rotate(-3deg);color:#593923}#inn-mother-lead .mother-ledger{left:55%;transform:rotate(2deg);color:#987746;background:linear-gradient(100deg,#e9d6ac,#f1e2c1 75%,#decaa4)}',
  '#inn-mother-lead figcaption{font-size:13px;line-height:1.3;white-space:nowrap;color:inherit}#inn-mother-lead .mother-ruled{height:132px;background:repeating-linear-gradient(transparent,transparent 31px,#b5a17b35 32px,transparent 33px)}#inn-mother-lead .mother-ink{display:block;width:100%;height:100%;overflow:visible}#inn-mother-lead .mother-letter{fill:none;stroke:currentColor;stroke-width:4.4;stroke-linecap:round;stroke-linejoin:round}#inn-mother-lead .mother-tail{fill:none;stroke:currentColor;stroke-width:4.4;stroke-linecap:round;opacity:0;transition:opacity .3s}',
  '#inn-mother-lead[data-compared="true"] .mother-paper{left:50%;transform:translateX(-50%);width:53%;color:#674326}#inn-mother-lead[data-compared="true"] .mother-book figcaption{visibility:hidden}#inn-mother-lead[data-compared="true"] .mother-ledger{background:transparent;border-color:#927952;color:#a98247;mix-blend-mode:multiply;box-shadow:none}#inn-mother-lead[data-compared="true"] .mother-ledger figcaption{text-align:center}#inn-mother-lead[data-compared="true"] .mother-ledger .mother-ruled{background:none}#inn-mother-lead[data-compared="true"] .mother-ledger .mother-letter{stroke-width:2.2}#inn-mother-lead[data-compared="true"] .mother-tail{opacity:1}',
  '#inn-mother-lead .mother-conclusion{font-size:16px;line-height:1.55;text-align:center;min-height:25px;margin:0 0 14px;color:#58432b}#inn-mother-lead .mother-actions{display:flex;justify-content:center;gap:10px;flex-wrap:wrap}',
  'html body #inn-mother-lead button{all:unset;box-sizing:border-box;min-height:44px;min-width:44px;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:8px 16px;border:1px solid #6a4c2b;border-radius:6px;color:#35271b;background:#dab567;cursor:pointer;font-family:var(--display,sans-serif);font-size:16px;line-height:1.4;touch-action:manipulation}html body #inn-mother-lead button[hidden]{display:none!important}html body #inn-mother-lead button.mother-quiet{background:#f5ebd3;border-color:#a7906e;color:#6e5940}html body #inn-mother-lead button.mother-close{padding:10px;background:transparent;border:0;flex-shrink:0;color:#6e5940}html body #inn-mother-lead button:focus-visible{outline:3px solid #2f6672;outline-offset:3px}#inn-mother-lead button svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}',
  '@media(max-width:440px) and (min-height:450px){#inn-mother-lead{padding:12px}#inn-mother-lead .mother-desk{padding:14px 16px;max-height:calc(100dvh - 24px)}#inn-mother-lead .mother-papers{height:302px;margin-top:12px}#inn-mother-lead .mother-paper{left:50%;width:230px;max-width:90%;height:141px;transform:translateX(-50%) rotate(-2deg);padding-top:10px}#inn-mother-lead .mother-ledger{top:155px;transform:translateX(-50%) rotate(2deg)}#inn-mother-lead .mother-ruled{height:108px}#inn-mother-lead[data-compared="true"] .mother-paper{top:77px;width:230px;transform:translateX(-50%)}#inn-mother-lead .mother-conclusion{font-size:15px}}',
  '@media(max-height:420px){#inn-mother-lead{padding:8px}#inn-mother-lead .mother-desk{padding:10px 20px;max-height:calc(100dvh - 16px)}#inn-mother-lead h2{font-size:20px}#inn-mother-lead .mother-papers{height:147px;margin:8px 0 0}#inn-mother-lead .mother-paper{height:135px;top:3px;padding:7px 10px 3px}#inn-mother-lead .mother-ruled{height:105px}#inn-mother-lead .mother-conclusion{font-size:14px;margin-bottom:8px;min-height:22px}}',
  '@media(prefers-reduced-motion:reduce){#inn-mother-lead .mother-paper,#inn-mother-lead .mother-tail{transition:none!important}}'
 ].join('\n');document.head.appendChild(css);
})();
