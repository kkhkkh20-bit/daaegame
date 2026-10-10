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
 /* Native banner keeps its promise, duration and tap guard. Place/time cards
    share the arrival presentation; verdicts and debate titles keep theirs. */
 function placeCard(title,time){
  var card=document.createElement('div');card.className='mid inn-place-card';
  card.innerHTML='<span class="location-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#81603d" stroke-width="1.7" stroke-linejoin="round"><path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg></span><div class="place-copy"><b></b><small><span class="place-time-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#80694b" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/></svg></span><span class="place-time-text"></span></small></div>';
  card.querySelector('b').textContent=title||'';card.querySelector('.place-time-text').textContent=time||'';return card;
 }
 window.__innPlaceCard=placeCard;
 function isPlace(title,sub){
  if(!active()||!sub)return false;
  var list=window.EP1INN&&window.EP1INN.PRO||[];
  return list.some(function(s){return s.title===title&&s.sub===sub})||/^(첫날|다음 날|그 밤|아침|오전|오후|저녁|한밤)/.test(String(sub));
 }
 function decorate(b){if(!b||b.classList.contains('inn-place-panel'))return;
  var mid=b.querySelector('.mid'),title=mid&&mid.querySelector('b'),sub=mid&&mid.querySelector('small');if(!mid||!title)return;
  var card=placeCard(title.textContent,sub?sub.textContent:'');mid.replaceWith(card);b.classList.add('inn-place-panel');
 }
 try{var oldBanner=banner;banner=function(title,sub){var yes=isPlace(title,sub),r=oldBanner.apply(this,arguments);if(yes)document.querySelectorAll('.banner:not(.inn-place-panel)').forEach(decorate);return r}}catch(e){}
 var css=document.createElement('style');css.id='inn-opening-direction';css.textContent=
 '.banner.inn-place-panel{display:block!important;background:transparent!important}.banner.inn-place-panel .bars{position:absolute!important;left:22px;top:74px;width:auto!important;max-width:calc(100vw - 44px);margin:0!important;align-items:flex-start!important}'+
 '.banner.inn-place-panel .bar1,.banner.inn-place-panel .bar2{display:none!important}.banner.inn-place-panel .mid.inn-place-card,.arr10 .inn-place-card{box-sizing:border-box;display:flex!important;align-items:center;gap:12px;width:max-content!important;min-width:200px;max-width:min(410px,calc(100vw - 44px));padding:11px 16px 11px 12px!important;text-align:left!important;background:#f6edd8!important;border:1px solid #9b8059;border-left:4px solid #85623d;border-radius:8px 3px 3px 8px;box-shadow:0 3px 0 #24170b35,0 7px 20px #24170b30;animation:inn-panel-in .24s ease-out!important;overflow:visible!important}'+
 '.inn-place-card .location-mark{display:grid;place-items:center;flex:0 0 36px;width:36px;height:42px;border-right:1px solid #d6c4a2;padding-right:10px;color:#81603d}.inn-place-card .location-mark svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linejoin:round}.inn-place-card .place-copy{min-width:0}'+
 '.banner.inn-place-panel .mid::after{display:none!important}.banner.inn-place-panel .mid b,.arr10 .inn-place-card b{display:block!important;font:400 20px/1.4 Galmuri11,monospace!important;color:#3d2e21!important;letter-spacing:0!important;text-shadow:none!important;white-space:normal!important;overflow-wrap:anywhere}.banner.inn-place-panel .mid b span{opacity:1!important;transform:none!important;animation:none!important}'+
 '.banner.inn-place-panel .mid small,.arr10 .inn-place-card small{display:flex!important;align-items:center;gap:5px;margin-top:3px;font:400 12px/1.4 Galmuri11,monospace!important;color:#80694b!important;letter-spacing:0!important}.place-time-icon svg{display:block;width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round}'+
 '.arr10:has(.inn-place-card){left:22px!important;top:74px!important;transform:none!important;gap:0!important;white-space:normal!important}.arr10:has(.inn-place-card) .mid::after{display:none!important}'+
 '@keyframes inn-panel-in{from{opacity:0;translate:-6px 0}to{opacity:1;translate:0 0}}'+
 '#inn-night-walk{position:fixed;inset:0;z-index:42;pointer-events:none!important;overflow:hidden}#inn-night-walk svg{width:100%;height:100%;display:block;image-rendering:pixelated}#inn-night-walk image{image-rendering:pixelated}.inn-night-direction #innstage .isf[data-k="det1"]{visibility:hidden!important}'+
 '.inn-night-direction #bigscene>svg[data-bg]{filter:brightness(.58) saturate(.72);transition:filter .3s}.inn-night-direction.inn-night-dark #bigscene>svg[data-bg]{filter:brightness(.43) saturate(.6)}#inn-night-walk .night-room-child{transform:translate(1070px,415px)}#inn-night-walk .night-bedroom{opacity:1;transition:opacity .25s}#inn-night-walk.out .night-bedroom{opacity:0}#inn-night-walk.return .night-bedroom{opacity:1;transition-delay:.85s}#inn-night-walk .night-child{filter:brightness(.86)}'+
 '#inn-night-walk .night-light{opacity:0;transition:opacity .3s}#inn-night-walk.out .night-light{opacity:1}#inn-night-walk.dark .night-light{opacity:0}#inn-night-walk .night-child{opacity:0;transform:translate(1100px,595px)}'+
 '#inn-night-walk.out .night-child{opacity:1;animation:inn-night-out 1.8s steps(16,end) forwards}#inn-night-walk.return .night-child{animation:inn-night-return .85s steps(10,end) forwards}'+
 '@keyframes inn-night-out{0%{opacity:0;transform:translate(1100px,595px)}12%{opacity:1}100%{opacity:1;transform:translate(625px,425px)}}@keyframes inn-night-return{0%{opacity:1;transform:translate(625px,425px)}86%{opacity:1;transform:translate(1100px,595px)}100%{opacity:0;transform:translate(1135px,610px)}}'+
 '@media(max-aspect-ratio:3/4){#inn-night-walk .night-room-child{transform:translate(720px,415px)}.banner.inn-place-panel .bars,.arr10:has(.inn-place-card){left:16px!important;top:80px!important}.banner.inn-place-panel .mid.inn-place-card,.arr10 .inn-place-card{max-width:calc(100vw - 32px);min-width:180px}.banner.inn-place-panel .mid b,.arr10 .inn-place-card b{font-size:18px!important}}'+
 '@media(prefers-reduced-motion:reduce){.banner.inn-place-panel .mid,.arr10:has(.inn-place-card){animation:none!important}#inn-night-walk .night-light,#inn-night-walk .night-bedroom,.inn-night-direction #bigscene>svg[data-bg]{transition:none!important}#inn-night-walk.out .night-child{animation:none;opacity:1;transform:translate(625px,425px)}#inn-night-walk.return .night-child{animation:none;opacity:0}}';
 document.head.appendChild(css);setInterval(sync,100);
 window.__innOpeningDirection=function(){return {night:!!night,cue:night&&night.dataset.cue,scene:lastScene&&lastScene.sid,reduced:reduced.matches}};
})();
