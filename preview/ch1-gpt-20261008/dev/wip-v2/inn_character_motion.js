/* 1장 배우 연기: 승인 PNG를 그대로 쓰는 픽셀 이동/분리 레이어.
   입 모양은 움직이지 않는다. 대사·증거·클릭 영역은 기존 엔진이 소유한다. */
(function(){
 'use strict';
 var NS='http://www.w3.org/2000/svg',serial=0,actors=[],tailFrames=0;
 var reduced=matchMedia('(prefers-reduced-motion: reduce)'),nativeLine=null,paused=false;
 var GESTURE={det0:'breath',det1:'tail',innma:'breath',seryeon:'paper',nabi:'ear',geokkuri:'ear-down',doto:'memo',buri:'feather',karo:'crest',wanggu:'emphasis'};
 /* Source pixels inspected against the current runtime files. Only free tips;
    fixed joins overlap by 4px so an ear/feather never separates from its root. */
 var PARTS={
  'art/ch1/action-poses/nabi/dialogue.png':{p:'ear-tip',r:[220,36,70,60],dir:-1},
  'art/ch1/cast/karo-front.png':{p:'crest-tip',r:[98,8,16,20],dir:-1},
  'art/ch1/action-poses/karo/dialogue.png':{p:'crest-tip',r:[157,11,31,35],dir:-1},
  'art/ch1/action-poses/bami/dialogue.png':{p:'ear-tip',r:[75,690,52,52],dir:1},
  'art/ch1/action-poses/doto/dialogue.png':{p:'pencil-tip',r:[568,620,23,25],dir:-1},
  'art/ch1/action-poses/buri/dialogue.png':{p:'feather-tip',r:[188,17,17,20],dir:-1},
  'art/ch1/action-poses/seryeon/dialogue.png':{p:'paper-edge',r:[228,251,26,10],dir:-1}
 };
 function inn(){try{return S.screen==='case'&&G&&CASES[G.ci].id==='inn'}catch(e){return false}}
 function mood(l){return window.__innMood?window.__innMood(l):''}
 function live(){try{if(DL&&DL.lines)return DL.lines[DL.i]||null;if(document.getElementById('rtg'))return (window.__rtActingLine&&window.__rtActingLine())||nativeLine}catch(e){}return null}
 function who(l){return l?(Array.isArray(l)?l[0]:l.w):''}
 function quiet(m){return /^(sad|worried|cower|nervous|panic|shock|surprise|held|held-anger|confront|angry|mad|pout)$/.test(m)}
 function still(){try{var a=window.__innAudioState&&window.__innAudioState(),l=live();return !!((window.__innTense&&window.__innTense())||(a&&(a.key||a.tense))||(l&&document.getElementById('rtg')&&/^(silence|pulse)$/.test(l.audio||'')))}catch(e){return false}}
 function setData(e,k,v){if(e.dataset[k]!==String(v))e.dataset[k]=String(v)}
 function node(tag,attrs){var e=document.createElementNS(NS,tag);Object.keys(attrs||{}).forEach(function(k){e.setAttribute(k,attrs[k])});return e}
 function dispose(im){if(im.__cmLayer){im.__cmLayer.remove();im.__cmLayer=null}im.classList.remove('cm-source')}
 function feature(im){
  var s=(im.getAttribute('src')||'').split('?')[0],f=PARTS[s];
  if(!f||!im.complete||!im.naturalWidth){dispose(im);return null}
  var a=im.__cmLayer;
  if(a&&a.dataset.source!==s){dispose(im);a=null}
  if(!a){
   var id='cmp'+(++serial),w=im.naturalWidth,h=im.naturalHeight,r=f.r;
   a=node('svg',{viewBox:'0 0 '+w+' '+h,'aria-hidden':'true',class:'cm-layer',preserveAspectRatio:'none'});
   a.dataset.source=s;a.dataset.part=f.p;
   var defs=node('defs'),mask=node('mask',{id:id+'m',maskUnits:'userSpaceOnUse',x:0,y:0,width:w,height:h});
   mask.appendChild(node('rect',{width:w,height:h,fill:'white'}));
   mask.appendChild(node('rect',{x:r[0],y:r[1],width:r[2],height:r[3],fill:'black'}));
   var clip=node('clipPath',{id:id+'c',clipPathUnits:'userSpaceOnUse'});
   clip.appendChild(node('rect',{x:r[0],y:r[1]-(f.dir>0?4:0),width:r[2],height:r[3]+4}));
   defs.appendChild(mask);defs.appendChild(clip);a.appendChild(defs);
   a.appendChild(node('image',{href:s,width:w,height:h,mask:'url(#'+id+'m)'}));
   var part=node('g',{class:'cm-part'});part.appendChild(node('image',{href:s,width:w,height:h,'clip-path':'url(#'+id+'c)'}));a.appendChild(part);
   im.insertAdjacentElement('afterend',a);im.__cmLayer=a;im.classList.add('cm-source');
  }
  var isStage=!!im.closest('.isf');
  a.style.left=isStage?'0px':im.style.left;a.style.top=isStage?'0px':im.style.top;
  a.style.width=im.style.width;a.style.height=im.style.height;
  /* One screen pixel, even when a high-resolution source is scaled down. */
  a.style.setProperty('--cm-step',(f.dir*im.naturalWidth/Math.max(1,parseFloat(im.style.width)))+'px');
  return a;
 }
 function tail(im,q){
  if(!im||!/daram-idle-t\d-dialogue/.test(im.getAttribute('src')||''))return;
  if(q){im.__cmTail=0;im.__cmWait=0;if(!/-t0-dialogue/.test(im.getAttribute('src')))im.src=im.getAttribute('src').replace(/-t\d-dialogue/,'-t0-dialogue');return}
  var step=im.__cmTail||0;
  if(!step){im.__cmWait=(im.__cmWait||0)+1;if(im.__cmWait<20)return;im.__cmWait=0;step=1}
  var seq=['t0','t1','t0','t2','t0'],s=seq[step];
  im.setAttribute('src',im.getAttribute('src').replace(/-t\d-dialogue/,'-'+s+'-dialogue'));tailFrames++;
  im.__cmTail=step>=4?0:step+1;
 }
 function tick(){
  var active=inn(),l=live(),sp=who(l),lm=mood(l),allStill=still();
  paused=!active||document.hidden||!!document.querySelector('#innmove,#innppl,.crec2,#innins,#e9pop,#ov .modal,#mveil .modal,#inn-settings');
  document.body.classList.toggle('cm-paused',paused||reduced.matches);actors=[];
  if(!active)return;
  document.querySelectorAll('#innstage .isf>img,.fstalk .tstage .tfig>img,#vnbox .spk9>img,#bigscene image.wn9,#rtg .seat>img,#rtg .seat>svg>image,image.innseat').forEach(function(im){
   var host=im.closest('.isf,.spk9,.seat'),k=(host&&host.dataset.k||im.dataset.k||'det1').split('|')[0];
   if(!GESTURE[k])return;
   var m=host&&host.dataset.mood!=null?host.dataset.mood:(sp===k?lm:'');
   var q=allStill||quiet(m),gesture=GESTURE[k],part=null;
   setData(im,'cmK',k);setData(im,'cmMood',m);setData(im,'cmQuiet',q?'1':'0');setData(im,'cmGesture',gesture);
   if(im.tagName.toLowerCase()==='img'&&im.closest('.isf,.tfig'))part=feature(im);
   if(part){setData(part,'cmK',k);setData(part,'cmMood',m);setData(part,'cmQuiet',q?'1':'0');setData(part,'cmGesture',gesture)}
   /* Sleeping child and emotional silences do not inherit a celebratory idle. */
   tail(im,paused||reduced.matches||q||im.closest('.isf')&&!document.body.classList.contains('inn-st2'));
   var surface=im.closest('.isf')?'stage':im.closest('.tfig')?'talk':im.closest('.spk9')?'portrait':im.closest('.seat')?'council':im.classList.contains('wn9')?'world':'carriage';
   actors.push({k:k,surface:surface,mood:m,gesture:gesture,part:part?part.dataset.part:null,quiet:q,src:im.getAttribute('src')||im.getAttribute('href'),layerCount:part?1:0});
  });
 }
 /* Wrap the existing synchronous cue hook; keep its vote/audio ownership. */
 var native=window.__innNativeLine;
 window.__innNativeLine=function(L){nativeLine=L;if(native)return native.apply(this,arguments)};
 window.__innMotionState=function(){return {reduced:reduced.matches,paused:paused,timerCount:1,actors:actors.map(function(a){return Object.assign({},a)}),tailFrames:tailFrames}};
 var style=document.createElement('style');style.id='inn-character-motion';style.textContent=[
  /* Translations step between integer screen pixels; never rotate/stretch art. */
  '.cm-layer{position:absolute;max-width:none!important;max-height:none!important;pointer-events:none!important;overflow:visible;image-rendering:pixelated}',
  '.cm-layer image{image-rendering:pixelated}.cm-source{opacity:0!important;animation:none!important;translate:0 0!important}',
  'html body.inn1 #rtg .seat>svg.sf{height:65%;position:relative;top:25%;width:auto;image-rendering:pixelated}html body.inn1 #rtg .seat[data-k="geokkuri"]{bottom:auto!important;top:0!important;height:25%!important}html body.inn1 #rtg .seat[data-k="geokkuri"] img{transform:none!important}',
  'html body.w209.inn1 [data-cm-k]{image-rendering:pixelated!important;rotate:none!important;scale:none!important}',
  'html body.w209.inn1 #vnbox .spk9 img{animation:none}',
  'html body.w209.inn1 .fstalk .tfig>img[data-cm-k]{animation:none}',
  'html body.w209.inn1 [data-cm-k][data-cm-quiet="0"]{animation:cm-breath 6.4s steps(1,end) infinite}',
  'html body.w209.inn1 [data-cm-k="det1"],html body.w209.inn1 [data-cm-k="wanggu"],html body.w209.inn1 .cm-source{animation:none}',
  'html body.w209.inn1 .cm-layer{animation:none!important}',
  'html body.w209.inn1 .cm-layer[data-cm-quiet="0"] .cm-part{animation:cm-tip 5.6s steps(1,end) infinite}',
  'html body.w209.inn1 [data-cm-k="innma"][data-cm-quiet="0"]{animation-duration:7.2s}',
  'html body.w209.inn1 [data-cm-k="seryeon"][data-cm-quiet="0"]{animation:cm-settle 7.8s steps(1,end) infinite}',
  'html body.w209.inn1 [data-cm-k="doto"][data-cm-quiet="0"]{animation:cm-memo 5.2s steps(1,end) infinite}',
  'html body.w209.inn1 [data-cm-k="buri"][data-cm-quiet="0"]{animation:cm-listen 6.8s steps(1,end) infinite}',
  'html body.w209.inn1 .cm-layer[data-cm-k="nabi"] .cm-part{animation-duration:5.6s}',
  'html body.w209.inn1 .cm-layer[data-cm-k="geokkuri"] .cm-part{animation-duration:8s}',
  'html body.w209.inn1 .cm-layer[data-cm-k="karo"] .cm-part{animation-duration:6s}',
  'html body.w209.inn1 .cm-layer[data-cm-k="doto"] .cm-part{animation-duration:5.2s}',
  'html body.w209.inn1 .cm-layer[data-cm-k="seryeon"] .cm-part{animation-duration:7.8s}',
  /* Subdued posture only; we do not invent an unapproved sad face. */
  'html body.w209.inn1 [data-cm-quiet="1"]{animation:none!important;translate:0 0}',
  'html body.w209.inn1 [data-cm-mood="sad"],html body.w209.inn1 [data-cm-mood="worried"]{translate:0 2px}',
  'html body.w209.inn1 .cm-layer[data-cm-quiet="1"] .cm-part{animation:none!important;transform:none!important}',
  'html body.w209.inn1 [data-cm-k="wanggu"][data-cm-mood="admonish"],html body.w209.inn1 [data-cm-k="wanggu"][data-cm-mood="claim"],html body.w209.inn1 [data-cm-k="wanggu"][data-cm-mood="resolve"]{animation:cm-emphasis .64s steps(1,end) 1}',
  /* Suspended Bami moves an ear tip, never pivots about feet on the floor. */
  'html body.w209.inn1 [data-cm-k="geokkuri"]{animation:none}',
  '@keyframes cm-breath{0%,72%,100%{translate:0 0}78%,92%{translate:0 -1px}}',
  '@keyframes cm-settle{0%,78%,100%{translate:0 0}82%,89%{translate:0 1px}}',
  '@keyframes cm-memo{0%,67%,100%{translate:0 0}71%,76%{translate:0 1px}80%,85%{translate:0 0}89%,94%{translate:0 1px}}',
  '@keyframes cm-listen{0%,80%,100%{translate:0 0}84%,92%{translate:1px 0}}',
  '@keyframes cm-emphasis{0%,70%,100%{translate:0 0}30%,60%{translate:0 1px}}',
  '@keyframes cm-tip{0%,74%,100%{transform:translateY(0)}78%,84%{transform:translateY(var(--cm-step))}88%,94%{transform:translateY(0)}}',
  'body.cm-paused [data-cm-k],body.cm-paused .cm-part{animation:none!important;translate:0 0!important}body.cm-paused .cm-part{transform:none!important}',
  '@media(prefers-reduced-motion:reduce){html body.w209.inn1 [data-cm-k],html body.w209.inn1 .cm-part,html body.w209.inn1 .spk9,html body.w209.inn1 .spk9 .sw9{animation:none!important;translate:0 0!important}html body.w209.inn1 .cm-part{transform:none!important}}'
 ].join('\n');document.head.appendChild(style);
 /* One scheduler for every surface and the existing tail sequence. */
 setInterval(tick,160);reduced.addEventListener('change',tick);document.addEventListener('visibilitychange',tick);tick();
})();
