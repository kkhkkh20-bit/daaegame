/* 승인된 다람 v4와 기존 복도 위에 얹는 밤 이동. 대본/진행/저장은 변경하지 않는다. */
(function(){
 'use strict';
 var night=null,lastLine=null,lastScene=null,reduced=matchMedia('(prefers-reduced-motion: reduce)');
 function active(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'}catch(e){return false}}
 function scene(){try{return active()&&G.beats&&!G.beats.inn_pro&&window.EP1INN&&window.EP1INN.PRO[G.beats.inn_pi]}catch(e){return null}}
 function makeNight(){
  if(night&&night.isConnected)return night;
  night=document.createElement('div');night.id='inn-night-walk';night.setAttribute('aria-hidden','true');
  night.innerHTML='<svg viewBox="0 0 1672 941" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="inn-door-glow" x2="0" y2="1"><stop stop-color="#ffd995" stop-opacity=".7"/><stop offset="1" stop-color="#ffd995" stop-opacity="0"/></linearGradient></defs><g class="night-light"><path d="M692 561H783L830 626H639Z" fill="url(#inn-door-glow)"/><path d="M692 560H783" stroke="#ffe5aa" stroke-width="5"/></g><g class="night-child"><image href="art/ch1/daram-v4/daram-worried-dialogue.png" x="0" y="0" width="165" height="145" preserveAspectRatio="xMidYMid meet"/></g><g class="night-bedroom"><image href="art/ch1/bg/P10-inn-bedroom-lights-out-background-only-1672x941.png" width="1672" height="941"/><g class="night-room-child"><image href="art/ch1/daram-v4/daram-worried-dialogue.png" width="290" height="236" preserveAspectRatio="xMidYMid meet"/></g></g></svg>';
  document.body.appendChild(night);document.body.classList.add('inn-night-direction');return night;
 }
 function cue(c){var e=makeNight();e.dataset.cue=c;if(c==='out')e.classList.add('out');if(c==='touch')e.classList.add('dark');if(c==='return')e.classList.add('return','dark');document.body.classList.toggle('inn-night-dark',c==='touch'||c==='return')}
 function cleanup(){if(night)night.remove();night=null;document.body.classList.remove('inn-night-direction','inn-night-dark');lastLine=null}
 function sync(){
  var s=scene(),isNight=s&&s.sid==='P10b';
  if(!isNight){if(night)cleanup();lastScene=null;return}
  if(lastScene!==s){cleanup();lastScene=s;makeNight()}
  var l=typeof DL!=='undefined'&&DL&&DL.lines&&DL.lines[DL.i];if(!l||l===lastLine)return;lastLine=l;
  var t=Array.isArray(l)?String(l[7]!=null?l[7]:l[1]||''):String(l.t||'');
  if(/다람이 방문을 조금 연다|다람이 살금살금 복도로 나온다/.test(t))cue('out');
  if(/다람이 문에 손을 댄다/.test(t))cue('touch');
  if(/다람이 뛰어 돌아가/.test(t))cue('return');
 }
 /* Native banner stays alive for its original promise/timing and input guard.
    Only its presentation changes; no replacement overlay or click handler. */
 function decorate(b){if(!b||b.classList.contains('inn-place-panel'))return;b.classList.add('inn-place-panel');
  var sub=b.querySelector('.mid small'),text=sub?sub.textContent:'';var dark=/밤|저녁|열한|자정/.test(text);
  var icon=document.createElement('span');icon.className='place-time-icon';icon.setAttribute('aria-hidden','true');
  icon.innerHTML=dark?'<svg viewBox="0 0 24 24"><path d="M18 16A8 8 0 0 1 8 6a8 8 0 1 0 10 10Z"/></svg>':'<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v3m0 14v3M2 12h3m14 0h3M5 5l2 2m10 10 2 2M5 19l2-2M17 7l2-2"/></svg>';
  var mid=b.querySelector('.mid');if(mid)mid.insertBefore(icon,mid.firstChild);
 }
 try{var oldBanner=banner;banner=function(){var yes=active(),r=oldBanner.apply(this,arguments);if(yes)document.querySelectorAll('.banner').forEach(decorate);return r}}catch(e){}
 var css=document.createElement('style');css.id='inn-opening-direction';css.textContent=
 '.banner.inn-place-panel{background:transparent!important}.banner.inn-place-panel .bars{width:auto!important;max-width:calc(100vw - 40px);align-self:start;margin-top:clamp(68px,18vh,100px)}'+
 '.banner.inn-place-panel .bar1,.banner.inn-place-panel .bar2{display:none!important}.banner.inn-place-panel .mid{display:grid!important;grid-template-columns:28px minmax(0,1fr);gap:3px 10px;width:auto!important;min-width:180px;max-width:min(430px,calc(100vw - 40px));padding:12px 20px!important;text-align:left!important;background:#f4e9d1!important;border:1px solid #9b7b47;border-radius:4px;box-shadow:0 4px 16px #24170b40;animation:inn-panel-in .24s ease-out!important;overflow:visible!important}'+
 '.banner.inn-place-panel .mid::after{display:none!important}.banner.inn-place-panel .mid b{grid-column:2;grid-row:1;font:600 clamp(16px,3vw,22px)/1.3 var(--font,sans-serif)!important;color:#49341f!important;letter-spacing:.035em!important;text-shadow:none!important;overflow-wrap:anywhere}.banner.inn-place-panel .mid b span{animation:none!important}'+
 '.banner.inn-place-panel .mid small{grid-column:2;grid-row:2;font:12px/1.4 var(--font,sans-serif)!important;color:#846a45!important;letter-spacing:.015em!important}.place-time-icon{grid-column:1;grid-row:1 / 3;align-self:center;color:#967440}.place-time-icon svg{display:block;width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}'+
 '@keyframes inn-panel-in{from{opacity:0;translate:0 5px}to{opacity:1;translate:0 0}}'+
 '#inn-night-walk{position:fixed;inset:0;z-index:42;pointer-events:none!important;overflow:hidden}#inn-night-walk svg{width:100%;height:100%;display:block;image-rendering:pixelated}#inn-night-walk image{image-rendering:pixelated}.inn-night-direction #innstage .isf[data-k="det1"]{visibility:hidden!important}'+
 '.inn-night-direction #bigscene>svg[data-bg]{filter:brightness(.58) saturate(.72);transition:filter .3s}.inn-night-direction.inn-night-dark #bigscene>svg[data-bg]{filter:brightness(.43) saturate(.6)}#inn-night-walk .night-room-child{transform:translate(1070px,415px)}#inn-night-walk .night-bedroom{opacity:1;transition:opacity .25s}#inn-night-walk.out .night-bedroom{opacity:0}#inn-night-walk.return .night-bedroom{opacity:1;transition-delay:.85s}#inn-night-walk .night-child{filter:brightness(.86)}'+
 '#inn-night-walk .night-light{opacity:0;transition:opacity .3s}#inn-night-walk.out .night-light{opacity:1}#inn-night-walk.dark .night-light{opacity:0}#inn-night-walk .night-child{opacity:0;transform:translate(1100px,595px)}'+
 '#inn-night-walk.out .night-child{opacity:1;animation:inn-night-out 1.8s steps(16,end) forwards}#inn-night-walk.return .night-child{animation:inn-night-return .85s steps(10,end) forwards}'+
 '@keyframes inn-night-out{0%{opacity:0;transform:translate(1100px,595px)}12%{opacity:1}100%{opacity:1;transform:translate(625px,425px)}}@keyframes inn-night-return{0%{opacity:1;transform:translate(625px,425px)}86%{opacity:1;transform:translate(1100px,595px)}100%{opacity:0;transform:translate(1135px,610px)}}'+
 '@media(max-aspect-ratio:3/4){#inn-night-walk .night-room-child{transform:translate(720px,415px)}.banner.inn-place-panel .bars{margin-top:76px}.banner.inn-place-panel .mid{min-width:160px;padding:11px 16px!important}}'+
 '@media(prefers-reduced-motion:reduce){.banner.inn-place-panel .mid{animation:none!important}#inn-night-walk .night-light,#inn-night-walk .night-bedroom,.inn-night-direction #bigscene>svg[data-bg]{transition:none!important}#inn-night-walk.out .night-child{animation:none;opacity:1;transform:translate(625px,425px)}#inn-night-walk.return .night-child{animation:none;opacity:0}}';
 document.head.appendChild(css);setInterval(sync,100);
 window.__innOpeningDirection=function(){return {night:!!night,cue:night&&night.dataset.cue,scene:lastScene&&lastScene.sid,reduced:reduced.matches}};
})();
