/* Explicit P10b directions own the room/corridor camera and resident presence.
   Prepare decoded world art before the first line; never infer motion from text. */
(function(){
 'use strict';
 var night=null,lastScene=null,lastGame=null,nightReady=false,nightSerial=0,nightCue='home',nightPromise=null,reduced=matchMedia('(prefers-reduced-motion: reduce)'),prepared={};
 function active(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'&&!document.getElementById('innmain')}catch(e){return false}}
 function scene(){try{return active()&&G.beats&&!G.beats.inn_pro&&window.EP1INN&&window.EP1INN.PRO[G.beats.inn_pi|0]}catch(e){return null}}
 function preload(src){
  if(prepared[src])return prepared[src];
  var entry=prepared[src]={ready:false};entry.promise=new Promise(function(resolve){var im=entry.image=new Image();
   im.onerror=function(){entry.failed=true;resolve(false)};im.onload=function(){Promise.resolve(im.decode?im.decode():null).then(function(){entry.ready=!!im.naturalWidth;entry.failed=!entry.ready;resolve(entry.ready)},function(){entry.failed=true;resolve(false)})};im.src=src;
  });return entry;
 }
 function valid(game,sc,token){return token===nightSerial&&lastGame===game&&lastScene===sc&&G===game&&scene()===sc&&active()}
 function applyCue(){if(!night)return;night.dataset.cue=nightCue;['out','dark','return','home','eyes','bami'].forEach(function(k){night.classList.remove(k)});
  if(nightCue==='home')night.classList.add('home');else night.classList.add('out');
  if(nightCue==='touch'||nightCue==='eyes'||nightCue==='bami'||nightCue==='return')night.classList.add('dark');
  if(nightCue==='eyes'||nightCue==='bami'||nightCue==='return')night.classList.add(nightCue);
  document.body.classList.toggle('inn-night-dark',nightCue!=='home'&&nightCue!=='out');
 }
 function makeNight(){
  if(night&&night.isConnected)return night;
  night=document.createElement('div');night.id='inn-night-walk';night.setAttribute('aria-hidden','true');
  // Both positions are inside the room/world, so use the authored full body.
  // Keep its planned source while decoding; a slow atlas must not pin an old
  // upper-body portrait into the scene for the rest of this night.
  var world=window.__innDialogueManifest&&window.__innDialogueManifest.world&&window.__innDialogueManifest.world.det1;
  var legacy='art/ch1/cast/daram-front.png';
  function actor(a,w,h,id){if(!a)return '<image href="'+legacy+'" width="'+w+'" height="'+h+'" preserveAspectRatio="xMidYMid meet"/>';
   var c=a.crop;return '<svg data-cast="det1" data-surface="'+id+'" x="0" y="0" width="'+w+'" height="'+h+'" viewBox="'+c.join(' ')+'" preserveAspectRatio="xMidYMid meet" overflow="hidden"><defs><clipPath id="night-cast-'+id+'" clipPathUnits="userSpaceOnUse"><rect x="'+c[0]+'" y="'+c[1]+'" width="'+c[2]+'" height="'+c[3]+'"/></clipPath></defs><image clip-path="url(#night-cast-'+id+')" href="'+a.src+'" width="'+a.width+'" height="'+a.height+'"/></svg>';
  }
  night.innerHTML='<svg viewBox="0 0 1672 941" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="inn-door-glow" x2="0" y2="1"><stop stop-color="#ffd995" stop-opacity=".7"/><stop offset="1" stop-color="#ffd995" stop-opacity="0"/></linearGradient></defs><g class="night-light"><path d="M692 561H783L830 626H639Z" fill="url(#inn-door-glow)"/><path d="M692 560H783" stroke="#ffe5aa" stroke-width="5"/></g><g class="night-eyes"><ellipse cx="902" cy="174" rx="5" ry="3" fill="#e5dfc7"/><ellipse cx="927" cy="174" rx="5" ry="3" fill="#e5dfc7"/></g><g class="night-child">'+actor(world,165,145,'world')+'</g><g class="night-bedroom"><image href="art/ch1/bg/P10-inn-bedroom-lights-out-background-only-1672x941.png" width="1672" height="941"/><g class="night-room-child">'+actor(world,252,350,'room')+'</g></g></svg>';
  var el=night,game=G,sc=lastScene,token=++nightSerial;
  var bami=window.__innDialogueManifest&&window.__innDialogueManifest.characters.geokkuri;
  var sources=Array.from(new Set([world?world.src:legacy,'art/ch1/bg/P10-inn-bedroom-lights-out-background-only-1672x941.png'].concat(bami&&bami.neutral?[bami.neutral.src]:[])));
  nightPromise=Promise.all(sources.map(function(src){return preload(src).promise})).then(function(ok){
   if(!valid(game,sc,token)||night!==el)return false;
   nightReady=ok.every(Boolean);el.classList.toggle('ready',nightReady);el.classList.toggle('error',!nightReady);return nightReady;
  });
  document.body.appendChild(night);document.body.classList.add('inn-night-direction');applyCue();return night;
 }
 function layoutNight(){if(!night)return;var svg=night.querySelector(':scope>svg'),child=night.querySelector('.night-room-child'),m=svg&&svg.getScreenCTM();if(!m||!child)return;
  var plate=document.querySelector('#vnbox .vtxt'),r=plate&&plate.getBoundingClientRect(),floor=Math.min(innerHeight-18,r&&r.height>10?r.top-14:innerHeight*.72),point=svg.createSVGPoint();point.x=innerWidth*.7;point.y=floor;point=point.matrixTransform(m.inverse());
  var world=window.__innDialogueManifest&&window.__innDialogueManifest.world.det1,c=world&&world.crop,feet=world&&world.feet,foot=c&&feet?(feet[1]-c[1])*350/c[3]:350;
  var transform='translate('+(innerHeight>innerWidth*1.15?720:1070)+'px,'+Math.round(Math.min(735,point.y)-foot)+'px)';if(child.style.transform!==transform)child.style.transform=transform;
 }
 function cleanup(){nightSerial++;if(night)night.remove();night=null;nightReady=false;nightPromise=null;nightCue='home';document.body.classList.remove('inn-night-direction','inn-night-dark');if(window.__innNightActor)window.__innNightActor(null)}
 function sync(){
  var s=scene(),isNight=s&&s.sid==='P10b'&&!document.querySelector('#inncold');
  if(!isNight){if(night)cleanup();lastScene=null;lastGame=null;return}
  if(lastScene!==s||lastGame!==G){cleanup();lastScene=s;lastGame=G;makeNight();if(window.__innNightActor)window.__innNightActor('none')}
  if(!night)makeNight();
  layoutNight();
 }
 window.__innNightPrepare=function(){
  if(night&&night.classList.contains('error')){Object.keys(prepared).forEach(function(src){if(prepared[src].failed)delete prepared[src]});cleanup();lastScene=null;lastGame=null}
  sync();return nightPromise||Promise.resolve(false);
 };
 window.__innNightDirection=function(d){
  sync();if(!night||!d||['out','touch','eyes','bami','return','home'].indexOf(d.night)<0)return Promise.resolve(false);
  nightCue=d.night;applyCue();if(window.__innNightActor)window.__innNightActor(nightCue==='bami'?'geokkuri':'none');layoutNight();
  return nightPromise||Promise.resolve(false);
 };
 /* Place/time has its own quiet card. Keep the native Promise duration and
    __skip/__t0 input contract; letter impacts belong to chapter/debate titles. */
 function placeCard(title,time){
  var card=document.createElement('div');card.className='mid inn-place-card';
  card.innerHTML='<span class="location-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#81603d" stroke-width="1.7" stroke-linejoin="round"><path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg></span><div class="place-copy"><b></b><small><span class="place-time-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="#80694b" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2"/></svg></span><span class="place-time-text"></span></small></div>';
  card.querySelector('b').textContent=title||'';card.querySelector('.place-time-text').textContent=time||'';return card;
 }
 window.__innPlaceCard=placeCard;
 function isPlace(title,sub){
  if(!active()||!sub)return false;
  var ep=window.EP1INN,list=ep?(ep.PRO||[]).concat(ep.END||[]):[];
  return list.some(function(s){return s.title===title&&s.sub===sub})||/^(첫날|다음 날|그 밤|아침|오전|오후|저녁|한밤)/.test(String(sub));
 }
 function placeBanner(title,time){return new Promise(function(resolve){
  if(window.__innClearPlaceDialogue){window.__innClearPlaceDialogue();setTimeout(window.__innClearPlaceDialogue,0);setTimeout(window.__innClearPlaceDialogue,60)}
  var b=document.createElement('div'),bars=document.createElement('div');b.className='banner inn-place-panel';bars.className='bars';bars.appendChild(placeCard(title,time));b.appendChild(bars);document.body.appendChild(b);
  var ended=false,timer,n=Array.from(String(title)).filter(function(c){return c!==' '}).length,hold=Math.max(1400,560+n*60+700);
  function finish(fast){if(ended)return;ended=true;clearTimeout(timer);b.classList.add('out');if(fast)b.classList.add('skip');setTimeout(function(){b.remove();resolve()},fast?170:320)}
  b.__t0=Date.now();b.__skip=function(){finish(true)};timer=setTimeout(function(){finish(false)},hold);
 })}
 try{var oldBanner=banner;banner=function(title,sub){var result=isPlace(title,sub)?placeBanner(title,sub):oldBanner.apply(this,arguments);
  // Commit the audio gate in the same task as the card, including the chapter
  // title. Waiting for the 220ms music poll leaves the previous cue audible.
  if(active()&&window.__AUD&&window.__AUD.tick)window.__AUD.tick();return result;
 }}catch(e){}
 var css=document.createElement('style');css.id='inn-opening-direction';css.textContent=
 '.banner.inn-place-panel{display:block!important;background:transparent!important}.banner.inn-place-panel .bars{position:absolute!important;left:22px;top:74px;width:auto!important;max-width:calc(100vw - 44px);margin:0!important;align-items:flex-start!important;animation:none!important;transform:none!important}'+
 '.banner.inn-place-panel .bar1,.banner.inn-place-panel .bar2{display:none!important}.banner.inn-place-panel .mid.inn-place-card,.arr10 .inn-place-card{box-sizing:border-box;display:flex!important;align-items:center;gap:12px;width:max-content!important;min-width:200px;max-width:min(410px,calc(100vw - 44px));padding:11px 16px 11px 12px!important;text-align:left!important;background:#f6edd8!important;border:1px solid #9b8059;border-left:4px solid #85623d;border-radius:8px 3px 3px 8px;box-shadow:0 3px 0 #24170b35,0 7px 20px #24170b30;animation:inn-panel-in .24s ease-out!important;overflow:visible!important}'+
 '.inn-place-card .location-mark{display:grid;place-items:center;flex:0 0 36px;width:36px;height:42px;border-right:1px solid #d6c4a2;padding-right:10px;color:#81603d}.inn-place-card .location-mark svg{width:25px;height:25px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linejoin:round}.inn-place-card .place-copy{min-width:0}'+
 '.banner.inn-place-panel .mid::after{display:none!important}.banner.inn-place-panel .mid b,.arr10 .inn-place-card b{display:block!important;font:400 20px/1.4 Galmuri11,monospace!important;color:#3d2e21!important;letter-spacing:0!important;text-shadow:none!important;white-space:normal!important;overflow-wrap:anywhere}.banner.inn-place-panel .mid b span{opacity:1!important;transform:none!important;animation:none!important}'+
 '.banner.inn-place-panel .mid small,.arr10 .inn-place-card small{display:flex!important;align-items:center;gap:5px;margin-top:3px;font:400 12px/1.4 Galmuri11,monospace!important;color:#80694b!important;letter-spacing:0!important}.place-time-icon svg{display:block;width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round}'+
 '.arr10:has(.inn-place-card){left:22px!important;top:74px!important;transform:none!important;gap:0!important;white-space:normal!important}.arr10:has(.inn-place-card) .mid::after{display:none!important}'+
 '.banner.inn-place-panel.out .mid.inn-place-card{animation:inn-panel-out .2s ease-in forwards!important}@keyframes inn-panel-in{from{opacity:0;translate:-6px 0}to{opacity:1;translate:0 0}}@keyframes inn-panel-out{to{opacity:0;translate:-4px 0}}'+
 '#inn-night-walk{position:fixed;inset:0;z-index:42;pointer-events:none!important;overflow:hidden;visibility:hidden}#inn-night-walk.ready{visibility:visible}#inn-night-walk>svg{width:100%;height:100%;display:block;image-rendering:pixelated}#inn-night-walk svg{image-rendering:pixelated}#inn-night-walk image{image-rendering:pixelated}.inn-night-direction #innstage .isf[data-k="det1"],.inn-night-direction #dlgveil>#vnfig,.inn-night-direction #bigscene image[data-k="geokkuri"]{visibility:hidden!important}'+
 '.inn-night-direction #bigscene>svg[data-bg]{filter:brightness(.58) saturate(.72);transition:filter .3s}.inn-night-direction.inn-night-dark #bigscene>svg[data-bg]{filter:brightness(.43) saturate(.6)}#inn-night-walk .night-room-child{transform:translate(1070px,415px)}#inn-night-walk .night-bedroom{opacity:1}#inn-night-walk.out .night-bedroom{opacity:0;visibility:hidden}#inn-night-walk .night-child{filter:brightness(.86)}'+
 '#inn-night-walk .night-light{opacity:0;transition:opacity .3s}#inn-night-walk.out .night-light{opacity:1}#inn-night-walk.dark .night-light{opacity:0}#inn-night-walk .night-child{opacity:0;transform:translate(1100px,595px)}'+
 '#inn-night-walk.out .night-child{opacity:1;transform:translate(625px,425px)}#inn-night-walk[data-cue="out"] .night-child{animation:inn-night-out 1.8s steps(16,end) forwards}#inn-night-walk.return .night-child{animation:inn-night-return .85s steps(10,end) forwards}#inn-night-walk.home .night-child{opacity:0;visibility:hidden}#inn-night-walk .night-eyes{opacity:0;visibility:hidden}#inn-night-walk.eyes .night-eyes{opacity:.5;visibility:visible}'+
 '@keyframes inn-night-out{0%{opacity:0;transform:translate(1100px,595px)}12%{opacity:1}100%{opacity:1;transform:translate(625px,425px)}}@keyframes inn-night-return{0%{opacity:1;transform:translate(625px,425px)}86%{opacity:1;transform:translate(1100px,595px)}100%{opacity:0;transform:translate(1135px,610px)}}'+
 '@media(max-aspect-ratio:3/4){#inn-night-walk .night-room-child{transform:translate(720px,415px)}.banner.inn-place-panel .bars,.arr10:has(.inn-place-card){left:16px!important;top:80px!important}.banner.inn-place-panel .mid.inn-place-card,.arr10 .inn-place-card{max-width:calc(100vw - 32px);min-width:180px}.banner.inn-place-panel .mid b,.arr10 .inn-place-card b{font-size:18px!important}}'+
 '@media(prefers-reduced-motion:reduce){.banner.inn-place-panel .mid,.arr10:has(.inn-place-card){animation:none!important}#inn-night-walk .night-light,#inn-night-walk .night-bedroom,.inn-night-direction #bigscene>svg[data-bg]{transition:none!important}#inn-night-walk.out .night-child{animation:none;opacity:1;transform:translate(625px,425px)}#inn-night-walk.return .night-child{animation:none;opacity:0}}';
 document.head.appendChild(css);
 var queued=false;new MutationObserver(function(){if(queued)return;queued=true;Promise.resolve().then(function(){queued=false;sync()})}).observe(document.body,{childList:true,subtree:true});
 (function loop(){sync();requestAnimationFrame(loop)})();
 window.__innOpeningDirection=function(){return {night:!!night,ready:!!(night&&nightReady),error:!!(night&&night.classList.contains('error')),game:lastGame,cue:night&&night.dataset.cue,scene:lastScene&&lastScene.sid,actor:nightCue==='bami'?'geokkuri':null,reduced:reduced.matches}};
})();
