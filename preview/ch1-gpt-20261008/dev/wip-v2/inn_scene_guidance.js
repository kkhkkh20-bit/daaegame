/* Persistent physical traces and a deliberate, single discovery scene.
   Uses approved world art as SVG viewports; does not replace image files. */
(function(){
 'use strict';
 var shot=null,NS='http://www.w3.org/2000/svg';
 function inn(){return G&&CASES[G.ci]&&CASES[G.ci].id==='inn'}
 function bedroom(){return inn()&&CASES[G.ci].locations[G.loc].id==='bed13'}
 function has(id){return (G.found||[]).indexOf(id)>=0}
 function node(tag,attrs){var n=document.createElementNS(NS,tag);Object.keys(attrs||{}).forEach(function(k){n.setAttribute(k,attrs[k])});return n}
 function valid(s){return shot===s&&G===s.game&&bedroom()&&G.tab==='scene'}
 function clear(s){if(!s||shot!==s)return;clearInterval(s.timer);if(s.el)s.el.remove();document.body.classList.remove('inn-under-cut');window.__innDiscoveryTransferred=null;shot=null;if(window.__innWorld)window.__innWorld.update()}
 function traces(){
  if(!bedroom())return;
  var world=document.querySelector('#bigscene svg[data-inn-world="bed13"]');if(!world)return;
  var sun=!!(window.__innSun&&window.__innSun()),old=world.querySelector('[data-scene-trace="headboard"]');
  if(!old||old.dataset.sun!==String(sun)){
   if(old)old.remove();var g=node('g',{'data-scene-trace':'headboard','data-sun':String(sun),'aria-label':sun?'햇빛에 드러난 머리판 글씨':'머리판에 남은 흐릿한 글씨 자국'});
   if(sun){[['첫 손님',249],['열한 번째 달 둘째 날',271]].forEach(function(a){var t=node('text',{x:981,y:a[1],fill:'#eedcb2','font-size':17,'font-family':'Galmuri11, sans-serif'});t.textContent=a[0];g.appendChild(t)})}
   else g.appendChild(node('path',{d:'M987 239h6m-3 0v9m-4-3h8m8-6v9m0-5h7m-3-4v10m10-10h8m-4 0v9m-4-4h8m11-5v8m0-3h6m-3-5v10 M988 258h5m-2 0v7m7-7v8m0-4h5m8-4h7m-3 0v8m-4-3h8m7-5v8m0-4h6m6-4h8m-4 0v8m-4-3h8m9-5v8m7-7h6m-3 0v8m-3-4h7',fill:'none',stroke:'#b1946c','stroke-width':1.5,opacity:.8}));
   world.appendChild(g);
  }
  var hot=document.querySelector('#bigscene [data-obs="o_under"]');if(hot){hot.classList.add('inn-under-cue');hot.setAttribute('aria-label',has('C04')?'침대 밑 발견 자리 살펴보기':'어두운 침대 밑 살펴보기');if(!hot.querySelector('.under-cue-icon')){var icon=document.createElement('span');icon.className='under-cue-icon';icon.setAttribute('aria-hidden','true');icon.innerHTML='<svg viewBox="0 0 24 24"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg>';hot.appendChild(icon)}}
 }
 function stage(s,next){
  if(!valid(s)||s.phase===next)return;s.phase=next;
  if(s.el)s.el.dataset.stage=next;
  if(next==='basket'){
   window.__innDiscoveryTransferred=G;
   if(window.__innWorld)window.__innWorld.update();
   // The transfer is now visible in the room. Return to the actors for Neoul.
   if(s.el)s.el.remove();document.body.classList.remove('inn-under-cut');
  }
 }
 function watch(s){
  if(!valid(s)){clear(s);return}
  if(!s.el||!s.el.isConnected){var veil=document.getElementById('dlgveil');if(veil&&s.phase!=='basket'){veil.appendChild(s.el);document.body.classList.add('inn-under-cut')}}
  if(!DL||!DL.lines||!DL.lines[DL.i])return;
  var l=DL.lines[DL.i],t=String(l[7]||l[1]||'');
  if(/빵 바구니와 수건을 빌려 왔다|작은 몸을 바구니에 옮기고/.test(t))stage(s,'basket');
  else if(s.phase!=='basket'&&/작은 몸이 웅크리고 있다|침대 밑에 작은 애가 있어|아빠가 꺼낼게|이렇게 작은 몸/.test(t))stage(s,'body');
  else if(s.phase==='fur'&&/등잔 빛이 상자 모서리/.test(t))stage(s,'light');
  else if(s.phase==='dark'&&/상자 뒤에 뭐가 있어/.test(t))stage(s,'fur');
 }
 function closeup(s){
  var source=document.querySelector('#bigscene svg[data-inn-world="bed13"]');if(!source)return;
  var frame=document.createElement('div');frame.id='inn-under-scene';frame.dataset.stage='dark';frame.setAttribute('aria-hidden','true');
  var svg=source.cloneNode(true);svg.setAttribute('viewBox','760 520 650 285');svg.setAttribute('preserveAspectRatio','xMidYMid slice');svg.removeAttribute('data-inn-world');svg.querySelectorAll('[data-scene-trace],.wn9').forEach(function(n){n.remove()});
  var defs=node('defs'),clip=node('clipPath',{id:'inn-under-body-clip'});clip.appendChild(node('path',{d:'M448 645l27-20 5-35 35-26v-37l23-15h36l11 31 33 2 32-22 35 10 20 19 42 13 26 24 33 26v31l-32 18-33 14h-70l-29-14-20-14-50 8-25-18-46 16h-37z'}));defs.appendChild(clip);svg.appendChild(defs);
  // Frame just the already approved mouse from the basket art, behind the box.
  var body=node('g',{'class':'under-body',transform:'translate(650 450) scale(.36)','clip-path':'url(#inn-under-body-clip)'}),im=node('image',{href:'art/ch1/locations/C04_basket_world.png',x:0,y:0,width:1280,height:1280});body.appendChild(im);
  var box=svg.querySelector('image[data-world-prop="chest_closed"]');while(box&&box.parentNode!==svg)box=box.parentNode;svg.insertBefore(body,box||null);
  svg.appendChild(node('rect',{'class':'under-dark',x:760,y:520,width:650,height:285,fill:'#090807'}));
  var beam=node('radialGradient',{id:'inn-under-light',cx:'34%',cy:'56%',r:'62%'});beam.appendChild(node('stop',{offset:'0%','stop-color':'#f6d398','stop-opacity':'.22'}));beam.appendChild(node('stop',{offset:'100%','stop-color':'#f6d398','stop-opacity':'0'}));defs.appendChild(beam);svg.appendChild(node('rect',{'class':'under-beam',x:760,y:520,width:650,height:285,fill:'url(#inn-under-light)'}));
  frame.appendChild(svg);s.el=frame;
 }
 function record(s){
  if(!valid(s)){clear(s);return}
  stage(s,'basket');G.beats.inn_basket_transferred=1;markObs('o_under');var fresh=!has('C04');window.__innGrant('C04');try{saveProg()}catch(e){}clear(s);render();
  if(fresh){try{SFX.found()}catch(e){}window.__innCard('C04',function(){if(G===s.game&&bedroom()&&G.tab==='scene')render()})}
 }
 window.__innDiscover=function(){
  if(!bedroom()||G.tab!=='scene'||!G.beats.inn_pro||DL||shot||document.querySelector('#ov .modal,#innmove,#wmap,body>.rt'))return;
  // CASES keeps only observation metadata; the authored dialogue lives in EP.
  var room=window.EP1INN.LOCS.filter(function(l){return l.id==='bed13'})[0],obs=room&&room.obs.filter(function(o){return o.id==='o_under'})[0],basket=room&&room.spots.filter(function(o){return o.ev==='C04'})[0];if(!obs||!basket)return;
  if(has('C04')){say([['det1','침대 밑 상자 뒤. 작은 손님이 있던 자리야.']],function(){render()});return}
  var s=shot={game:G,phase:'dark',el:null,timer:0};
  function assess(){if(!valid(s)){clear(s);return}say(basket.say.map(function(l){return l.slice()}),function(){record(s)})}
  if((G.obsSeen||[]).indexOf('o_under')>=0){assess();return}
  try{closeup(s);say(obs.say.map(function(l){return l.slice()}),assess);watch(s);s.timer=setInterval(function(){watch(s)},50)}catch(e){clear(s);throw e}
 };
 var css=document.createElement('style');css.textContent=[
  'html body.inn1 #bigscene .hot.inn-under-cue{pointer-events:auto!important;opacity:1!important;visibility:visible!important;outline:0!important;box-shadow:none!important;animation:none!important}',
  'html body.inn1 #bigscene .hot.inn-under-cue::after{display:none!important}.under-cue-icon{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:22px;height:22px;border:1px solid #c8b38b;border-radius:50%;background:#30271bd9;pointer-events:none;display:grid;place-items:center}.under-cue-icon svg{width:15px;height:15px;fill:none;stroke:#f2dfb7;stroke-width:2}',
  'html body.inn1 #bigscene .hot.inn-under-cue>svg,html body.inn1 #bigscene .hot.inn-under-cue>.hn{display:none!important}html body.inn1 #bigscene .hot.inn-under-cue>.under-cue-icon{display:grid!important;opacity:1!important;visibility:visible!important}',
  'svg[data-inn-world="bed13"] image[data-world-prop="C02_trace"]{opacity:.88!important;mix-blend-mode:normal!important;filter:none!important}',
  '#inn-under-scene{position:absolute;z-index:3;top:18px;left:50%;transform:translateX(-50%);width:min(650px,calc(100vw - 36px));height:calc(100dvh - 156px);max-height:410px;background:#090807;border:2px solid #8c704a;box-shadow:0 0 0 4px #16110c,0 8px 26px #0009;overflow:hidden;pointer-events:none}',
  '#inn-under-scene>svg{display:block;width:100%;height:100%;image-rendering:pixelated}body.inn-under-cut #innstage .isf{opacity:0!important}',
  '#inn-under-scene .under-body{opacity:0;filter:brightness(.2)}#inn-under-scene .under-dark{opacity:.86}#inn-under-scene .under-beam{opacity:0}',
  '#inn-under-scene[data-stage="fur"] .under-body{opacity:.5}#inn-under-scene[data-stage="fur"] .under-dark{opacity:.67}',
  '#inn-under-scene[data-stage="light"] .under-body{opacity:.85;filter:brightness(.6)}#inn-under-scene[data-stage="light"] .under-dark{opacity:.35}#inn-under-scene[data-stage="light"] .under-beam{opacity:1}',
  '#inn-under-scene[data-stage="body"] .under-body{opacity:1;filter:brightness(.85)}#inn-under-scene[data-stage="body"] .under-dark{opacity:.14}#inn-under-scene[data-stage="body"] .under-beam{opacity:1}',
  '@media(prefers-reduced-motion:no-preference){#inn-under-scene .under-body,#inn-under-scene .under-dark,#inn-under-scene .under-beam{transition:opacity .5s ease,filter .5s ease}}'
 ].join('\n');document.head.appendChild(css);
 setInterval(function(){try{traces();if(shot&&!valid(shot))clear(shot)}catch(e){}},160);
})();
