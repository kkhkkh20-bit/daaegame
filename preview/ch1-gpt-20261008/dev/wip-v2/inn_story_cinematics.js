/* Important opening pictures. This layer reads the authored scene/dialogue;
   it never advances dialogue, changes clues, or schedules an input handler.
   build.py supplies __innStoryArt from local file existence, so an absent
   approved picture falls back to the existing stage without an HTTP request. */
(function(){
 'use strict';
 var node=null,shown=null,lastGame=null,failed={},reduced=matchMedia('(prefers-reduced-motion: reduce)');
 var ART={
  carriage:{src:'art/ch1/cinematics/carriage-family-close.png',alt:'마차 안에서 나란히 앉아 이야기하는 다람과 아빠'},
  village:{src:'art/ch1/cinematics/village-arrival-wide.png',alt:'저녁빛의 골짜기 마을에 도착한 다람과 아빠'},
  seal:{src:'art/ch1/cinematics/sealed-pouch-close.png',alt:'베개 밑에서 발견한 주머니와 아직 뜯기지 않은 붉은 봉인띠'}
 };
 function scene(){try{
  if(S.screen!=='case'||!G||CASES[G.ci].id!=='inn'||!G.beats||G.beats.inn_pro||document.getElementById('innmain'))return null;
  return window.EP1INN&&window.EP1INN.PRO[G.beats.inn_pi]||null;
 }catch(e){return null}}
 function text(l){return l?String(Array.isArray(l)?(l[7]!=null?l[7]:l[1]||''):l.t||''):''}
 function who(l){return l&&(Array.isArray(l)?l[0]:l.w)||''}
 function desired(){
  var s=scene(),v=document.querySelector('#ov > #dlgveil');
  if(!s||!v||typeof DL==='undefined'||!DL||!DL.lines)return null;
  var l=DL.lines[DL.i],t=text(l);if(!l)return null;
  if(s.sid==='P1'&&G.beats.inn_bg==='carriage'){
   // The driver's arrival changes the camera back to his actual stage. The
   // father's reply in that same dialogue must not restore the family cut.
   for(var i=0;i<=DL.i;i++)if(who(DL.lines[i])==='karo')return null;
   if(who(l)==='det1'||who(l)==='det0'||who(l)==='narr')return 'carriage';
  }
  if(s.sid==='P2'&&G.beats.inn_bg==='plaza')return 'village';
  // Show the intact seal before counting starts. No picture invents a coin
  // count or suggests who put the pouch there.
  if(s.sid==='P13'&&/베개 밑[….\s]*여기 있군요|세련 씨 주머니가 맞습니까|맞습니다\. 제 도장이에요|뜯긴 데도 없고요/.test(t))return 'seal';
  return null;
 }
 function ready(k){return !!(k&&!failed[k]&&window.__innStoryArt&&window.__innStoryArt[k]===true)}
 function cleanup(){
  if(node)node.remove();node=null;shown=null;
  // The engine briefly clones a closing dialogue into #ovfz. Its cloned
  // picture is presentation state, never a second live/stale CG layer.
  document.querySelectorAll('#ovfz #inn-story-cg').forEach(function(n){n.remove()});
  document.body.classList.remove('inn-story-cg-active');delete document.body.dataset.innStoryCut;
 }
 function show(k,v){
  if(shown!==k||!node){
   cleanup();node=document.createElement('div');node.id='inn-story-cg';node.dataset.cut=k;
   node.setAttribute('role','img');node.setAttribute('aria-label',ART[k].alt);
   var surround=document.createElement('img');surround.className='cinema-surround';surround.alt='';surround.setAttribute('aria-hidden','true');surround.src=ART[k].src;
   var picture=document.createElement('img');picture.className='cinema-picture';picture.alt='';picture.src=ART[k].src;
   // A late failed/slow asset may never hide the working original stage.
   picture.onload=function(){if(node&&node.contains(picture)&&shown===k){node.classList.add('ready');document.body.classList.add('inn-story-cg-active');document.body.dataset.innStoryCut=k}};
   picture.onerror=function(){failed[k]=true;if(node&&node.contains(picture))cleanup()};
   node.append(surround,picture);shown=k;
   if(picture.complete&&picture.naturalWidth)picture.onload();
  }
  if(node.parentNode!==v)v.insertBefore(node,v.firstChild);
 }
 function sync(){try{
  document.querySelectorAll('#ovfz #inn-story-cg').forEach(function(n){n.remove()});
  if(lastGame!==G){cleanup();lastGame=G}
  var k=desired(),v=document.querySelector('#ov > #dlgveil');
  if(!k||!ready(k)||!v){if(node)cleanup();return}
  show(k,v);
  var l=DL&&DL.lines[DL.i];
  node.classList.toggle('memory',k==='carriage'&&/엄마 찾으면|엄마가 갑자기 사라지고|편지 도장|골짜기…|몇 해 전 편지/.test(text(l)));
 }catch(e){cleanup()}}
 var css=document.createElement('style');css.id='inn-story-cinematics';css.textContent=
 '#inn-story-cg{position:fixed;inset:0;z-index:1;pointer-events:none!important;overflow:hidden;background:#211c20;visibility:hidden}#inn-story-cg.ready{visibility:visible}'+
 '#inn-story-cg img{position:absolute;inset:0;width:100%;height:100%;max-width:none;image-rendering:pixelated;pointer-events:none!important}#inn-story-cg .cinema-picture{object-fit:cover;object-position:50% 38%;transition:filter .35s ease-out}#inn-story-cg.ready .cinema-picture{animation:inn-cinema-reveal .38s ease-out both}#inn-story-cg.memory .cinema-picture{filter:brightness(.9) saturate(.85)}'+
 '#inn-story-cg .cinema-surround{display:none;object-fit:cover;filter:blur(20px) brightness(.24) saturate(.55);transform:scale(1.08)}'+
 '#inn-story-cg[data-cut="carriage"] .cinema-picture{object-position:50% 0%}#inn-story-cg[data-cut="village"] .cinema-picture{object-position:50% 44%}#inn-story-cg[data-cut="seal"] .cinema-picture{object-position:50% 44%}'+
 'body.inn-story-cg-active #dlgveil>.vnbg,body.inn-story-cg-active #dlgveil>.vnshade,body.inn-story-cg-active #dlgveil>#innstage,body.inn-story-cg-active #dlgveil>#vnfig{visibility:hidden!important}'+
 '@keyframes inn-cinema-reveal{from{opacity:.45}to{opacity:1}}'+
 '@media(max-aspect-ratio:3/4){#inn-story-cg .cinema-surround{display:block}#inn-story-cg .cinema-picture,#inn-story-cg[data-cut] .cinema-picture{object-fit:contain;object-position:50% 24%}}'+
 '@media(prefers-reduced-motion:reduce){#inn-story-cg .cinema-picture{animation:none!important;transition:none!important}}';
 document.head.appendChild(css);
 // The native controller removes/replaces the veil on skips and save loads.
 // Remove its visual layer at that same DOM turn, before the next paint.
 var queued=false;new MutationObserver(function(){if(queued)return;queued=true;Promise.resolve().then(function(){queued=false;sync()})}).observe(document.getElementById('ov')||document.body,{childList:true,subtree:true});
 (function loop(){sync();requestAnimationFrame(loop)})();
 window.__innStoryCinematics=function(){var s=scene();return {cut:shown,visible:!!(node&&node.classList.contains('ready')),tone:node&&node.classList.contains('memory')?'memory':'normal',wanted:desired(),scene:s&&s.sid,cue:typeof DL!=='undefined'&&DL&&text(DL.lines[DL.i])||'',artReady:ready(desired()),reduced:reduced.matches}};
 window.__innStoryCinematicReset=cleanup;
})();
