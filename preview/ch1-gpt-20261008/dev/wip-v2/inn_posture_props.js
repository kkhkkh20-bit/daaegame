/* 1장 자세 구분. 배경 NPC의 작업 자세와 대화 배우의 서 있는 자세를 분리한다.
   기존 승인 그림만 재사용한다. 회의 좌석/증거·소품 지급/핫스폿은 건드리지 않는다. */
(function(){
 'use strict';
 var ROOT='art/ch1/',standing={
  nabi:ROOT+'cast/nabi-front.png',karo:ROOT+'cast/karo-front.png',
  doto:ROOT+'cast/doto-v4-182.png',buri:'art/body/buri-0.png',
  seryeon:ROOT+'cast/seryeon-normal-front-v1.png'
 };
 var props={
  bed13:{icon:'bed',actors:[],role:'침대·보관함',additional:[]},
  hall:{icon:'hall',actors:['geokkuri'],role:'문·복도 시계',additional:[]},
  dotoroom:{icon:'room',actors:['doto'],role:'기록하는 방',additional:[ROOT+'props/doto_room/prop_weather_notebook_open_rgba.png',ROOT+'props/doto_room/prop_bookstack_rgba.png',ROOT+'props/doto_room/prop_pencilcup_rgba.png']},
  front:{icon:'desk',actors:['wanggu'],role:'접수대·기록',additional:[]},
  dining:{icon:'table',actors:['innma','seryeon'],role:'식탁·서류',additional:[]},
  kitchen:{icon:'pot',actors:['nabi','buri'],role:'조리 도구·책',additional:[]},
  plaza:{icon:'tree',actors:['karo'],role:'여관 밖·우편 가방',additional:[]}
 };
 function active(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'}catch(e){return false}}
 var lastDialogue=null,heldMoods={};
 function mood(k,m){
  var dl=null;try{dl=DL}catch(e){}
  if(dl!==lastDialogue){lastDialogue=dl;heldMoods={}}
  if(m!=null)return String(m).split(/\s+/)[0];
  try{var l=dl&&dl.lines&&dl.lines[dl.i];if(l&&(Array.isArray(l)?l[0]:l.w)===k)heldMoods[k]=window.__innMood?window.__innMood(l):''}catch(e){}
  return heldMoods[k]||'';
 }
 function source(k,m){
  if(!active())return null;var f=mood(k,m);
  if(k==='geokkuri')return ROOT+'action-poses/bami/dialogue.png'; // feet remain attached to ceiling
  if(k==='innma')return window.__innGrandmaSrc?window.__innGrandmaSrc(f):ROOT+'cast/innma-neutral-v5.png';
  if(k==='seryeon')return ROOT+'cast/seryeon-'+(/^(nervous|shock|panic|angry|mad|surprise)$/.test(f)?'surprise':'normal')+'-front-v1.png';
  if(k==='buri'&&/^(shock|surprise|panic)$/.test(f))return 'art/body/buri-2.png';
  return standing[k]||null;
 }
 window.__innPostureSrc=source;
 /* __innPose is only consumed by stage and .fstalk, not world NPC draw/alphaHit.
    Wrapping it also fixes the native question-screen updater in inn_ui9. */
 var previous=window.__innPose;
 window.__innPose=function(k){var f=source(k);return f||(previous&&previous.apply(this,arguments))||null};
 // World alpha-hit reads each live SVG image href, so changing its paint
 // also changes the alpha source; native buttons, data-npc and handlers stay.
 // Visible alpha rectangles retain the old feet (world y=694) and actor centre.
 var WORLD_STANDING={
  nabi:{src:standing.nabi,r:[767.5454545,161.3636364,549.8181818,549.8181818],foot:[999.5,694]},
  buri:{src:standing.buri,r:[1377.472067,290.346369,301.631285,403.653631],foot:[1505,694]}
 };
 function worldStanding(){
  var sc=document.getElementById('bigscene');if(!sc)return;
  var room;try{room=CASES[G.ci].locations[G.loc].id}catch(e){}if(room!=='kitchen')return;
  sc.querySelectorAll('image.wn9').forEach(function(im){var spec=WORLD_STANDING[im.dataset.k];if(!spec)return;
   // Reuse the engine's alpha cache before any pointer reaches a new pose.
   if(window.__innWarmNpcMask)window.__innWarmNpcMask(spec.src);
   if(im.getAttribute('href')!==spec.src)im.setAttribute('href',spec.src);
   ['x','y','width','height'].forEach(function(k,i){if(im.getAttribute(k)!==String(spec.r[i]))im.setAttribute(k,spec.r[i])});
   im.dataset.posture='standing';im.setAttribute('preserveAspectRatio','xMidYMid meet');
  });
 }
 // The atlas remains disabled until its actual transparency/grid is reviewed.
 // Never request a candidate or nonexistent image. Root enables the inspected
 // dimensions here (or through the explicit QA helper) once generation ends.
 var ATLAS={ready:true,src:ROOT+'props/inn-set-dressing-v1.png',width:1254,height:1254,
  // Inspected RGBA source: nominal 418px cells bleed (bag strap, crate leaves).
  // Tight SVG views include each entire object and exclude neighbouring pixels.
  crops:[[15,120,430,317],[460,90,353,340],[838,110,398,318],
         [82,455,280,340],[422,447,409,347],[846,503,384,281],
         [35,858,441,325],[470,818,390,374],[880,893,354,287]]};
 var clipSerial=0;
 var DECOR={
  dining:[{cell:4,r:[1200,369,100,60]},{cell:5,r:[1500,351,120,75]}],
  kitchen:[{cell:3,r:[760,333,68,76]},{cell:5,r:[1250,370,110,85]},{cell:7,r:[110,680,140,102]}],
  front:[{cell:4,r:[1010,340,95,62]},{cell:6,r:[1270,558,94,87]}],
  plaza:[{cell:6,r:[1050,780,104,77]},{cell:7,r:[445,690,123,94]},{cell:8,r:[1220,695,97,77]}],
  dotoroom:[{cell:0,r:[120,480,190,78]},{cell:1,r:[465,675,84,80]},{cell:2,r:[1550,620,102,82]}]
 };
 function dress(){
  if(!ATLAS.ready||!ATLAS.width||!ATLAS.height)return;
  var sc=document.getElementById('bigscene'),sv=sc&&sc.querySelector('svg[data-inn-world],svg[data-bg]');if(!sv)return;
  var room;try{room=CASES[G.ci].locations[G.loc].id}catch(e){}var list=DECOR[room]||[];
  var key=room+'|'+ATLAS.width+'|'+ATLAS.height;if(sv.dataset.postureDecor===key)return;
  sv.querySelectorAll('.inn-set-dressing').forEach(function(e){e.remove()});sv.dataset.postureDecor=key;
  var NS='http://www.w3.org/2000/svg',group=document.createElementNS(NS,'g');group.classList.add('inn-set-dressing');group.setAttribute('aria-hidden','true');group.style.pointerEvents='none';
  list.forEach(function(p){
   var tile=document.createElementNS(NS,'svg'),cw=ATLAS.width/3,ch=ATLAS.height/3;
   ['x','y','width','height'].forEach(function(k,i){tile.setAttribute(k,p.r[i])});
   var crop=ATLAS.crops[p.cell]||[(p.cell%3)*cw,Math.floor(p.cell/3)*ch,cw,ch];
   tile.setAttribute('viewBox',crop.join(' '));tile.setAttribute('preserveAspectRatio','xMidYMax meet');tile.setAttribute('overflow','hidden');tile.dataset.cell=p.cell;
   // Meet can leave viewport letterboxing: overflow alone does not clip the
   // source viewBox. Explicit source-space clipping prevents adjacent cells
   // from bleeding into those transparent margins.
   var defs=document.createElementNS(NS,'defs'),clip=document.createElementNS(NS,'clipPath'),rect=document.createElementNS(NS,'rect'),id='inn-prop-crop-'+(++clipSerial);
   clip.setAttribute('id',id);clip.setAttribute('clipPathUnits','userSpaceOnUse');
   ['x','y','width','height'].forEach(function(k,i){rect.setAttribute(k,crop[i])});clip.appendChild(rect);defs.appendChild(clip);tile.appendChild(defs);
   var im=document.createElementNS(NS,'image');im.setAttribute('clip-path','url(#'+id+')');im.setAttribute('href',ATLAS.src);im.setAttribute('width',ATLAS.width);im.setAttribute('height',ATLAS.height);im.style.imageRendering='pixelated';tile.appendChild(im);group.appendChild(tile);
  });
  // Behind live actors and foreground occluders; decoration never captures input.
  var actor=sv.querySelector('image.wn9,image.wo9');if(actor)sv.insertBefore(group,actor);else sv.appendChild(group);
 }
 window.__innSetDressingEnable=function(width,height){ATLAS.width=width;ATLAS.height=height;ATLAS.ready=!!(width&&height);dress()};
 function stamp(){
  if(!active())return;worldStanding();dress();
  document.querySelectorAll('#innstage .isf,.fstalk .tfig').forEach(function(host){
   var im=host.querySelector('img'),k=host.dataset.k||(im&&im.dataset.k);if(!k)return;
   var p=k==='geokkuri'?'hanging':standing[k]||k==='innma'?'standing':'native';
   if(host.dataset.posture!==p)host.dataset.posture=p;
  });
 }
 window.__innPostureState=function(){
  var room=null;try{room=active()&&CASES[G.ci].locations[G.loc].id}catch(e){}
  return {room:room,roomProps:Object.assign({},props[room]||{}, {actualAssets:Array.from(document.querySelectorAll('#bigscene image.wp9,#bigscene .inn-set-dressing image')).map(function(i){return i.getAttribute('href')})}),setDressing:{ready:ATLAS.ready,src:ATLAS.ready?ATLAS.src:null,cells:ATLAS.ready?(DECOR[room]||[]).map(function(p){return p.cell}):[]},worldActors:Array.from(document.querySelectorAll('#bigscene image.wn9')).map(function(i){return {k:i.dataset.k,src:i.getAttribute('href'),posture:i.dataset.posture||'native',x:i.getAttribute('x'),y:i.getAttribute('y'),width:i.getAttribute('width'),height:i.getAttribute('height')}}),dialogue:'standing',meeting:'native-seated',
   actors:Array.from(document.querySelectorAll('#innstage .isf,.fstalk .tfig')).map(function(h){var i=h.querySelector('img');return {k:h.dataset.k||(i&&i.dataset.k),posture:h.dataset.posture,src:i&&i.getAttribute('src')}})};
 };
 // Warm the six existing images without altering world assets or source canvases.
 Object.values(standing).concat([ROOT+'cast/innma-neutral-v5.png']).forEach(function(s){var i=new Image();i.src=s});
 // Apply to newly-rendered world actors before the browser paints a seated
 // frame. Only child-list changes are observed, so our attribute writes cannot
 // create a MutationObserver loop.
 var pending=false;new MutationObserver(function(){if(pending)return;pending=true;Promise.resolve().then(function(){pending=false;stamp()})}).observe(document.body,{childList:true,subtree:true});
 setInterval(stamp,250);stamp();
})();
