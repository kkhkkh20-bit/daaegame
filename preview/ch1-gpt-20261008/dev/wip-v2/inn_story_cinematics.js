/* Authored camera ownership. A picture belongs to a scene/camera beat, never
   to the short native dialogue batches between @dir instructions. The public
   presentation snapshot lets music wait for the same visual commitment. */
(function(){
 'use strict';
 var node=null,shown=null,pending=null,lastGame=null,owner=null,observedDialogue=null,serial=0,failed={},reduced=matchMedia('(prefers-reduced-motion: reduce)');
 var ART={
  carriage:{src:'art/ch1/cinematics/carriage-family-close.png',alt:'마차 안에서 나란히 앉아 이야기하는 다람과 아빠'},
  driver:{src:'art/ch1/cinematics/carriage-driver-close.png',alt:'마차 앞자리에서 돌아보며 도착을 알리는 마부 까로'},
  village:{src:'art/ch1/cinematics/village-arrival-wide.png',alt:'저녁빛의 골짜기 마을에 도착한 다람과 아빠'},
  seal:{src:'art/ch1/cinematics/sealed-pouch-close.png',alt:'베개 밑에서 발견한 주머니와 아직 뜯기지 않은 붉은 봉인띠'}
 };
 function active(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'&&!document.getElementById('innmain')}catch(e){return false}}
 function authored(){try{
  if(!active()||!G.beats)return null;
  var b=G.beats,ep=window.EP1INN;
  if(!b.inn_pro){var p=ep&&ep.PRO[b.inn_pi];return p&&{phase:'pro',sid:p.sid,scene:p}}
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
 function cleanup(){removePicture();owner=null;lastGame=null;observedDialogue=null;document.body.classList.remove('inn-story-scene-owner')}
 function initialCamera(s){return s.phase==='pro'&&s.sid==='P1'?'carriage':s.phase==='pro'&&s.sid==='P2'?'village':s.phase==='pro'&&s.sid==='P10b'?'night':'stage'}
 function ensureOwner(s){
  var key=s.phase+':'+(s.sid||'scene:'+G.loc+':'+G.tab);
  if(lastGame!==G||!owner||owner.key!==key){
   var dl=typeof DL!=='undefined'&&DL||null,ignore=owner&&dl&&dl===observedDialogue?dl:null;
   removePicture();lastGame=G;owner={game:G,key:key,phase:s.phase,sid:s.sid,scene:s.scene,camera:initialCamera(s),started:s.phase==='investigation',memory:false,lastLine:null,ignoreDialogue:ignore};
  }
  return owner;
 }
 function blocked(){return !!document.querySelector('#innmain,#inncold,.banner,.placecard')}
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
 function desired(){var s=authored();if(!s||blocked())return null;var o=ensureOwner(s);observeLine(o);return ART[o.camera]&&o.started?o.camera:null}
 function show(k,o){
  if(shown===k&&node&&node.isConnected){if(pending){serial++;pending=null}return}
  if(pending&&pending.cut===k&&pending.owner===o)return;
  // Prepare the next shot off screen. The committed previous picture remains
  // visible until decoding succeeds; the native stage never flashes between.
  var token=++serial,game=o.game,key=o.key,request={cut:k,owner:o};pending=request;
  var el=document.createElement('div');el.id='inn-story-cg';el.dataset.cut=k;el.dataset.owner=key;
  el.setAttribute('role','img');el.setAttribute('aria-label',ART[k].alt);
  var surround=document.createElement('img');surround.className='cinema-surround';surround.alt='';surround.setAttribute('aria-hidden','true');
  var picture=document.createElement('img');picture.className='cinema-picture';picture.alt='';
  function valid(){var current=authored();return serial===token&&pending===request&&owner===o&&G===game&&current&&current.phase===o.phase&&current.sid===o.sid&&owner.key===key&&owner.camera===k&&!blocked()}
  // Slow decodes from a previous camera or save can never hide the current
  // original stage. Visibility and audio commit together after this check.
  picture.onload=function(){if(valid()){if(node)node.remove();node=el;shown=k;pending=null;el.classList.add('ready');el.classList.toggle('memory',k==='carriage'&&o.memory);document.body.appendChild(el);document.body.classList.add('inn-story-cg-active');document.body.dataset.innStoryCut=k}};
  picture.onerror=function(){failed[k]=true;if(valid())removePicture()};
  el.append(surround,picture);
  surround.src=ART[k].src;picture.src=ART[k].src;
  if(picture.complete&&picture.naturalWidth)picture.onload();
 }
 function sync(){try{
  document.querySelectorAll('#ovfz #inn-story-cg').forEach(function(n){n.remove()});
  var s=authored();if(!s){if(owner||node)cleanup();return}
  var o=ensureOwner(s);observeLine(o);observedDialogue=typeof DL!=='undefined'&&DL||null;
  document.body.classList.toggle('inn-story-scene-owner',s.phase==='pro');
  if(blocked()){if(node||pending)removePicture();return}
  var k=ART[o.camera]&&o.started?o.camera:null;
  if(!k||!artReady(k)){if(node||pending)removePicture();return}
  show(k,o);if(node)node.classList.toggle('memory',shown==='carriage'&&o.memory);
 }catch(e){cleanup()}}
 window.__innPresentationDirection=function(d){
  var s=authored();if(!s||blocked()||!d)return;var o=ensureOwner(s);o.started=true;
  if(o.sid==='P1'&&d.who==='karo')o.camera='driver';
  sync();
 };
 var css=document.createElement('style');css.id='inn-story-cinematics';css.textContent=
 '#inn-story-cg{position:fixed;inset:0;z-index:59;pointer-events:none!important;overflow:hidden;background:#211c20;visibility:hidden}#inn-story-cg.ready{visibility:visible}'+
 '#inn-story-cg img{position:absolute;inset:0;width:100%;height:100%;max-width:none;image-rendering:pixelated;pointer-events:none!important}#inn-story-cg .cinema-picture{object-fit:cover;object-position:50% 38%;transition:filter .35s ease-out}#inn-story-cg.ready .cinema-picture{animation:inn-cinema-reveal .38s ease-out both}#inn-story-cg.memory .cinema-picture{filter:brightness(.9) saturate(.85)}'+
 '#inn-story-cg .cinema-surround{display:none;object-fit:cover;filter:blur(20px) brightness(.24) saturate(.55);transform:scale(1.08)}'+
 '#inn-story-cg[data-cut="carriage"] .cinema-picture{object-position:50% 0%}#inn-story-cg[data-cut="driver"] .cinema-picture{object-position:50% 22%}#inn-story-cg[data-cut="village"] .cinema-picture{object-position:50% 44%}#inn-story-cg[data-cut="seal"] .cinema-picture{object-position:50% 44%}'+
 'body.inn-story-cg-active #dlgveil{background:transparent!important}body.inn-story-cg-active #dlgveil>.vnbg,body.inn-story-cg-active #dlgveil>.vnshade,body.inn-story-cg-active #dlgveil>#innstage,body.inn-story-cg-active #dlgveil>#vnfig{visibility:hidden!important}'+
 'body.inn-story-cg-active #ovfz .vnbg,body.inn-story-cg-active #ovfz .vnshade,body.inn-story-cg-active #ovfz #innstage,body.inn-story-cg-active #ovfz #vnfig{visibility:hidden!important}'+
 '@keyframes inn-cinema-reveal{from{opacity:.45}to{opacity:1}}'+
 '@media(max-aspect-ratio:3/4){#inn-story-cg .cinema-surround{display:block}#inn-story-cg .cinema-picture,#inn-story-cg[data-cut] .cinema-picture{object-fit:contain;object-position:50% 24%}}'+
 '@media(prefers-reduced-motion:reduce){#inn-story-cg .cinema-picture{animation:none!important;transition:none!important}}';
 document.head.appendChild(css);
 var queued=false;new MutationObserver(function(){if(queued)return;queued=true;Promise.resolve().then(function(){queued=false;sync()})}).observe(document.body,{childList:true,subtree:true});
 (function loop(){sync();requestAnimationFrame(loop)})();
 window.__innPresentationState=function(){
  sync();var cold=!!document.getElementById('inncold'),s=authored(),o=owner;
  if(!s||!o)return {game:active()?G:null,phase:cold?'cold':null,sid:null,owner:cold?'cold':null,camera:null,cut:null,loading:null,ready:false,transitioning:!!s,cold:cold,cue:''};
  var visual=ART[o.camera]&&artReady(o.camera)?!!(shown===o.camera&&node&&node.classList.contains('ready')):true;
  if(o.camera==='night'&&window.__innOpeningDirection){var night=window.__innOpeningDirection();visual=night.game===o.game&&night.scene===o.sid&&night.ready}
  var staleDialogue=!!(o.ignoreDialogue&&typeof DL!=='undefined'&&DL===o.ignoreDialogue),transitioning=blocked()||!o.started||!visual||staleDialogue;
  return {game:o.game,phase:o.phase,sid:o.sid,owner:o.key,camera:o.camera,cut:shown,loading:pending&&pending.cut||null,ready:!transitioning,transitioning:transitioning,cold:cold,cue:staleDialogue?'':text(line())};
 };
 window.__innStoryCinematics=function(){var p=window.__innPresentationState();return {cut:shown,loading:p.loading,visible:!!(node&&node.classList.contains('ready')),tone:shown==='carriage'&&owner&&owner.memory?'memory':'normal',wanted:desired(),scene:p.phase==='pro'?p.sid:null,cue:p.cue,owner:p.owner,ready:p.ready,transitioning:p.transitioning,artReady:artReady(desired()),reduced:reduced.matches}};
 window.__innStoryCinematicReset=cleanup;
})();
