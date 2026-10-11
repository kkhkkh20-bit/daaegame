/* Authored primary backdrops. Acquire the picture before native render(),
   preload/decode it, and keep it through cards and dialogue batches. Legacy
   world/seat art is never a loading fallback for an authored picture. */
(function(){
 'use strict';
 var node=null,shown=null,pending=null,lastGame=null,owner=null,observedDialogue=null,serial=0,failed={},reduced=matchMedia('(prefers-reduced-motion: reduce)');
 var ART={
  carriage:{src:'art/ch1/cinematics/carriage-family-close.png',alt:'마차 안에서 나란히 앉아 이야기하는 다람과 아빠'},
  driver:{src:'art/ch1/cinematics/carriage-driver-close.png',alt:'마차 앞자리에서 돌아보며 도착을 알리는 마부 까로'},
  village:{src:'art/ch1/cinematics/village-arrival-wide.png',alt:'저녁빛의 골짜기 마을에 도착한 다람과 아빠',place:'골짜기 마을',time:'첫날 저녁'},
  approach:{src:'art/ch1/cinematics/village-approach-road.png',alt:'마차 창밖으로 보이는 고갯길과 저녁 등불이 켜진 골짜기 마을',place:'골짜기 마을로 가는 길',time:'첫날 해 질 무렵'},
  postoffice:{src:'art/ch1/cinematics/post-office-closed-exterior.png',alt:'닫힌 우체국 출입문과 마감 표찰, 셔터가 닫힌 창',place:'우체국 앞',time:'첫날 저녁'},
  innentrance:{src:'art/ch1/cinematics/inn-entrance-evening.png',alt:'계단을 올라 도착한 겨울잠 여관의 등불 켜진 현관 문 앞',place:'겨울잠 여관 앞',time:'첫날 저녁'},
  seal:{src:'art/ch1/cinematics/sealed-pouch-close.png',alt:'베개 밑에서 발견한 주머니와 아직 뜯기지 않은 붉은 봉인띠'}
 };
 var pictures={};
 function prepared(k){
  if(pictures[k])return pictures[k];
  var img=new Image(),entry={img:img,ready:false};img.className='cinema-picture';img.alt='';
  entry.promise=new Promise(function(resolve){
   function error(){failed[k]=true;resolve(false)}
   img.onerror=error;img.onload=function(){
    Promise.resolve(img.decode?img.decode():undefined).then(function(){entry.ready=true;delete failed[k];resolve(true)},error);
   };img.src=ART[k].src;
  });pictures[k]=entry;return entry;
 }
 // Warm the next few shots after play begins. Full-resolution journey art
 // must not compete with the main screen during its first loading screen.
 function warmScene(s){var keys=s.sid==='P1'?['carriage','approach','driver','village']:s.sid==='P2'?['village','postoffice','innentrance']:s.sid==='P3'?['innentrance']:s.sid==='P13'?['seal']:[];keys.forEach(prepared)}
 function active(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'&&!document.getElementById('innmain')}catch(e){return false}}
 function authored(){try{
  if(!active()||!G.beats)return null;
  var b=G.beats,ep=window.EP1INN;
  if(!b.inn_pro){var p=ep&&ep.PRO[b.inn_pi|0];return p&&{phase:'pro',sid:p.sid,scene:p}}
  if(b.inn_final&&!b.inn_end){var e=ep&&ep.END[b.inn_ei];return e&&{phase:'end',sid:e.sid||'E'+(b.inn_ei+1),scene:e}}
  return {phase:'investigation',sid:null,scene:null};
 }catch(e){return null}}
 function scene(){var s=authored();return s&&s.phase==='pro'?s.scene:null}
 function text(l){return l?String(Array.isArray(l)?(l[7]!=null?l[7]:l[1]||''):l.t||''):''}
 function who(l){return l&&(Array.isArray(l)?l[0]:l.w)||''}
 function line(){return typeof DL!=='undefined'&&DL&&DL.lines&&DL.lines[DL.i]||null}
 function artReady(k){return !!(k&&!failed[k]&&window.__innStoryArt&&window.__innStoryArt[k]===true)}
 function removePicture(){
  serial++;pending=null;if(node)node.remove();node=null;shown=null;
  document.querySelectorAll('#ovfz #inn-story-cg').forEach(function(n){n.remove()});
  document.body.classList.remove('inn-story-cg-active');delete document.body.dataset.innStoryCut;
 }
 function cleanup(){if(window.__innSceneFlowReset)window.__innSceneFlowReset();removePicture();owner=null;lastGame=null;observedDialogue=null;document.body.classList.remove('inn-story-scene-owner','inn-story-picture-owned')}
 function initialCamera(s){return s.scene&&s.scene.camera|| (s.phase==='pro'&&s.sid==='P1'?'carriage':s.phase==='pro'&&s.sid==='P2'?'village':s.phase==='pro'&&s.sid==='P10b'?'night':'stage')}
 function ensureOwner(s){
  var key=s.phase+':'+(s.sid||'scene:'+G.loc+':'+G.tab);
  if(lastGame!==G||!owner||owner.key!==key){
   var dl=typeof DL!=='undefined'&&DL||null,ignore=owner&&dl&&dl===observedDialogue?dl:null;
   removePicture();lastGame=G;owner={game:G,key:key,phase:s.phase,sid:s.sid,scene:s.scene,camera:initialCamera(s),started:s.phase==='investigation',memory:false,lastLine:null,ignoreDialogue:ignore};
   if(window.__innSceneFlowBegin)window.__innSceneFlowBegin(owner);
   warmScene(s);
  }
  return owner;
 }
 function blocked(){return !!document.querySelector('#innmain,#inncold')}
 function cardBlocked(){return !!document.querySelector('.banner,.placecard')}
 function observeLine(o){
  if(o.ignoreDialogue&&typeof DL!=='undefined'&&DL===o.ignoreDialogue)return;
  var l=line();if(!l||l===o.lastLine)return;o.lastLine=l;o.started=true;
  var t=text(l),w=who(l);
  if(o.sid==='P1'){
   // The driver's entry is a one-way camera handoff for this scene. A father's
   // reply, a split batch or a null DL cannot bring the family picture back.
   if(w==='karo')o.camera='driver';
   if(/엄마 찾으면|엄마가 갑자기 사라져|편지 도장|골짜기…|몇 해 전 편지/.test(t))o.memory=true;
  }
  if(o.sid==='P13'){
   if(/^베개 밑[….\s]*여기 있군요/.test(t)&&o.camera==='stage')o.camera='seal';
   // The source's opening action ends the intact-seal shot permanently.
   if(/^봉인띠를 자르겠습니다/.test(t))o.camera='stage';
  }
 }
 function desired(){var s=authored();if(!s||blocked())return null;var o=ensureOwner(s);observeLine(o);return ART[o.camera]?o.camera:null}
 function show(k,o){
  if(shown===k&&node&&node.isConnected){if(pending){serial++;pending=null}return}
  if(pending&&pending.cut===k&&pending.owner===o)return;
  if(node&&node.dataset.cut===k&&node.dataset.owner===o.key&&node.classList.contains('error'))return;
  // Prepare the next shot off screen. The committed previous picture remains
  // visible until decoding succeeds; the native stage never flashes between.
  var token=++serial,game=o.game,key=o.key,request={cut:k,owner:o};pending=request;
  var el=document.createElement('div');el.id='inn-story-cg';el.dataset.cut=k;el.dataset.owner=key;
  el.setAttribute('role','img');el.setAttribute('aria-label',ART[k].alt);
  var surround=document.createElement('img');surround.className='cinema-surround';surround.alt='';surround.setAttribute('aria-hidden','true');
  var entry=prepared(k),picture=entry.img;
  function valid(){var current=authored();return serial===token&&pending===request&&owner===o&&G===game&&current&&current.phase===o.phase&&current.sid===o.sid&&owner.key===key&&owner.camera===k&&!blocked()}
  function commit(){if(!valid())return;if(node&&node!==el)node.remove();node=el;shown=k;pending=null;el.classList.remove('loading','error');el.classList.add('ready');el.classList.toggle('memory',k==='carriage'&&o.memory);if(!el.isConnected)document.body.appendChild(el);document.body.classList.add('inn-story-cg-active');document.body.dataset.innStoryCut=k}
  function error(){if(!valid())return;if(node&&node!==el)node.remove();node=el;shown=null;pending=null;el.classList.add('loading','error');el.innerHTML='<button type="button" class="cinema-retry">장면을 불러오지 못했어요 · 다시 시도</button>';el.querySelector('button').onclick=function(e){e.preventDefault();e.stopImmediatePropagation();delete pictures[k];delete failed[k];removePicture();sync()};if(!el.isConnected)document.body.appendChild(el)}
  el.append(surround,picture);
  if(ART[k].place&&window.__innPlaceCard){var place=document.createElement('div');place.className='cinema-place';place.appendChild(window.__innPlaceCard(ART[k].place,ART[k].time));el.appendChild(place)}
  // Text is live, legible UI anchored to the actual empty wooden door plaque,
  // using the same cover transform as the new background. No baked AI text.
  if(k==='postoffice'||k==='innentrance'){var label=document.createElementNS('http://www.w3.org/2000/svg','svg');label.setAttribute('viewBox','0 0 1672 941');label.setAttribute('preserveAspectRatio','xMidYMid slice');label.setAttribute('class','cinema-world-label nodot');label.setAttribute('aria-label',k==='postoffice'?'출입문 표찰: 닫음':'간판: 겨울잠 여관');label.innerHTML=k==='postoffice'?'<text x="906" y="505" text-anchor="middle" fill="#352419" font-family="Galmuri11,monospace" font-size="26">닫음</text>':'<text x="1473" y="370" text-anchor="middle" fill="#eac184" font-family="Galmuri11,monospace" font-size="22">겨울잠 여관</text>';el.appendChild(label)}
  surround.src=ART[k].src;
  if(!node){node=el;el.classList.add('loading');document.body.appendChild(el)}
  if(entry.ready)commit();else entry.promise.then(function(ok){if(ok)commit();else error()});
 }
 function sync(){try{
  document.querySelectorAll('#ovfz #inn-story-cg').forEach(function(n){n.remove()});
  var s=authored();if(!s){if(owner||node)cleanup();return}
  var o=ensureOwner(s);observeLine(o);observedDialogue=typeof DL!=='undefined'&&DL||null;
  document.body.classList.toggle('inn-story-scene-owner',s.phase==='pro');
  if(blocked()){if(node||pending)removePicture();return}
  var k=ART[o.camera]?o.camera:null;
  document.body.classList.toggle('inn-story-picture-owned',!!k);
  if(!k){if(node||pending)removePicture();return}
  show(k,o);if(node)node.classList.toggle('memory',shown==='carriage'&&o.memory);
 }catch(e){cleanup()}}
 // Native boot and runPro both use render(). Do this before it paints any
 // default location, rather than repairing that frame in a later observer.
 var nativeRender=render;render=function(){sync();var result=nativeRender.apply(this,arguments);sync();return result};
 function visualReady(o){
  if(!o)return false;
  if(ART[o.camera])return !!(shown===o.camera&&node&&node.classList.contains('ready'));
  if(o.camera==='night'){var n=window.__innOpeningDirection&&window.__innOpeningDirection();return !!(n&&n.game===o.game&&n.scene===o.sid&&n.ready)}
  return true;
 }
 window.__innPresentationOwner=function(){return owner};
 window.__innPresentationVisualReady=function(){return visualReady(owner)};
 window.__innPresentationWait=function(){
  sync();var captured=owner;
  return new Promise(function(resolve){function check(){
   var s=authored();if(!captured||owner!==captured||G!==captured.game||!s||s.sid!==captured.sid){resolve(false);return}
   sync();var f=window.__innSceneFlowState&&window.__innSceneFlowState();if(visualReady(captured)&&(!f||f.settled)){resolve(true);return}
   requestAnimationFrame(check);
  }check()});
 };
 window.__innPresentationDirection=function(d){
  var s=authored();if(!s||blocked()||!d)return;var o=ensureOwner(s);o.started=true;
  if(d.camera&&(ART[d.camera]||d.camera==='stage')){if(o.camera!==d.camera&&window.__innClearPlaceDialogue){
   window.__innClearPlaceDialogue();
   // Native endDlg() invokes the next direction inside its callback, then an
   // outer freeze wrapper attaches the former dialogue afterward. Clear that
   // tail in this task's microtask, before the first new-camera paint.
   var nextCamera=d.camera;Promise.resolve().then(function(){if(owner===o&&G===o.game&&o.camera===nextCamera)window.__innClearPlaceDialogue()});
  }o.camera=d.camera;}
  else if(o.sid==='P1'&&d.who==='karo')o.camera='driver';
  if(window.__innSceneFlowDirection)window.__innSceneFlowDirection(d);
  sync();
 };
 var css=document.createElement('style');css.id='inn-story-cinematics';css.textContent=
 '#inn-story-cg{position:fixed;inset:0;z-index:59;pointer-events:none!important;overflow:hidden;background:#211c20;visibility:hidden}#inn-story-cg.ready,#inn-story-cg.loading{visibility:visible}#inn-story-cg.loading img{visibility:hidden}.cinema-retry{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:auto!important;min-height:44px;padding:12px 18px;border:1px solid #ac9166;background:#302b27;color:#f5e5c4;font:14px var(--display,sans-serif)}'+
 // A failed picture's retry must sit above the full-screen place-card hit
 // layer (z68); its first pointerdown must not skip that card underneath it.
 '#inn-story-cg.error{z-index:69}'+
 '#inn-story-cg img{position:absolute;inset:0;width:100%;height:100%;max-width:none;image-rendering:pixelated;pointer-events:none!important}#inn-story-cg .cinema-picture{object-fit:cover;object-position:50% 38%;transition:filter .35s ease-out;opacity:1}#inn-story-cg.memory .cinema-picture{filter:brightness(.9) saturate(.85)}'+
 '#inn-story-cg .cinema-surround{display:none;object-fit:cover;filter:blur(20px) brightness(.24) saturate(.55);transform:scale(1.08)}'+
 '#inn-story-cg[data-cut="carriage"] .cinema-picture{object-position:50% 0%}#inn-story-cg[data-cut="driver"] .cinema-picture{object-position:50% 22%}#inn-story-cg[data-cut="village"] .cinema-picture{object-position:50% 44%}#inn-story-cg[data-cut="seal"] .cinema-picture{object-position:50% 44%}'+
 '#inn-story-cg[data-cut="approach"] .cinema-picture,#inn-story-cg[data-cut="postoffice"] .cinema-picture,#inn-story-cg[data-cut="innentrance"] .cinema-picture{object-position:50% 50%}#inn-story-cg[data-cut="approach"] .cinema-picture{animation:inn-approach 14s ease-out both}@keyframes inn-approach{from{transform:scale(1.01)}to{transform:scale(1.06)}}'+
 '#inn-story-cg .cinema-world-label{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}#inn-story-cg .cinema-place{position:absolute;top:74px;left:22px}#inn-story-cg .cinema-place .inn-place-card{display:flex;align-items:center;gap:9px;padding:8px 12px;background:var(--inn-paper);border:1px solid var(--inn-brass);border-left:3px solid var(--inn-muted);border-radius:4px;box-shadow:0 3px 10px #211b1633}#inn-story-cg .cinema-place b{display:block;font:400 14px/1.45 Galmuri11,monospace;color:var(--inn-ink)}#inn-story-cg .cinema-place small{display:flex;align-items:center;gap:4px;margin-top:3px;font:400 10px/1.4 Galmuri11,monospace;color:var(--inn-muted)}#inn-story-cg .cinema-place .location-mark{width:25px;height:30px;flex-basis:25px;padding-right:8px}#inn-story-cg .cinema-place .location-mark svg{width:18px;height:18px}body:has(.banner,.placecard) #inn-story-cg .cinema-place{visibility:hidden}'+
 'body.inn-story-picture-owned #app{visibility:hidden!important}body.inn-story-picture-owned #dlgveil{background:transparent!important}body.inn-story-picture-owned #dlgveil>.vnbg,body.inn-story-picture-owned #dlgveil>.vnshade,body.inn-story-picture-owned #dlgveil>#innstage,body.inn-story-picture-owned #dlgveil>#vnfig{visibility:hidden!important}'+
 'body.inn-story-cg-active #ovfz .vnbg,body.inn-story-cg-active #ovfz .vnshade,body.inn-story-cg-active #ovfz #innstage,body.inn-story-cg-active #ovfz #vnfig{visibility:hidden!important}'+
 '@media(max-aspect-ratio:3/4){#inn-story-cg .cinema-surround{display:block}#inn-story-cg .cinema-picture,#inn-story-cg[data-cut] .cinema-picture{object-fit:contain;object-position:50% 24%}#inn-story-cg .cinema-world-label{display:none}}'+
 '@media(prefers-reduced-motion:reduce){#inn-story-cg .cinema-picture{animation:none!important;transition:none!important}}';
 document.head.appendChild(css);
 var queued=false;new MutationObserver(function(){if(queued)return;queued=true;Promise.resolve().then(function(){queued=false;sync()})}).observe(document.body,{childList:true,subtree:true});
 (function loop(){sync();requestAnimationFrame(loop)})();
 window.__innPresentationState=function(){
  sync();var cold=!!document.getElementById('inncold'),s=authored(),o=owner;
  if(!s||!o)return {game:active()?G:null,phase:cold?'cold':null,sid:null,owner:cold?'cold':null,camera:null,cut:null,loading:null,ready:false,transitioning:!!s,cold:cold,cue:''};
  var visual=visualReady(o),flowState=window.__innSceneFlowState&&window.__innSceneFlowState();
  var staleDialogue=!!(o.ignoreDialogue&&typeof DL!=='undefined'&&DL===o.ignoreDialogue),transitioning=blocked()||cardBlocked()||!o.started||!visual||staleDialogue||!!(flowState&&!flowState.settled);
  return {game:o.game,phase:o.phase,sid:o.sid,owner:o.key,camera:o.camera,cut:shown,loading:pending&&pending.cut||null,visualReady:visual,ready:!transitioning,transitioning:transitioning,cold:cold,cue:staleDialogue?'':text(line())};
 };
 window.__innStoryCinematics=function(){var p=window.__innPresentationState();return {cut:shown,loading:p.loading,visible:!!(node&&node.classList.contains('ready')),tone:shown==='carriage'&&owner&&owner.memory?'memory':'normal',wanted:desired(),scene:p.phase==='pro'?p.sid:null,cue:p.cue,owner:p.owner,ready:p.ready,transitioning:p.transitioning,artReady:artReady(desired()),reduced:reduced.matches}};
 window.__innStoryCinematicReset=cleanup;
})();
