/* Scene-owned entry: next score starts in black, then decoded scenery opens.
   Sound disabled/suspended is an explicit bypass, never a stuck title card. */
(function(){
 'use strict';
 var flow=null,veil=null,cache={},serial=0;
 function alive(f){try{return flow===f&&f.game===G&&S.screen==='case'&&!document.getElementById('innmain')&&window.__innPresentationOwner()===f.owner}catch(e){return false}}
 function picture(src){
  if(!src)return Promise.resolve(true);
  if(cache[src])return cache[src];
  return cache[src]=new Promise(function(resolve){var im=new Image();im.onerror=function(){delete cache[src];resolve(false)};im.onload=function(){Promise.resolve(im.decode?im.decode():null).then(function(){resolve(true)},function(){delete cache[src];resolve(false)})};im.src=src});
 }
 function reset(){serial++;flow=null;if(veil)veil.remove();veil=null;document.body.classList.remove('inn-scene-black')}
 function darken(f){
  if(veil)veil.remove();veil=document.createElement('div');veil.id='inn-scene-black';veil.setAttribute('aria-hidden','true');document.body.appendChild(veil);document.body.classList.add('inn-scene-black');
  f.black=true;f.revealAt=null;f.audioAt=null;f.audioClock=null;f.bypass=null;f.enteredAt=performance.now();prepare(f);
 }
 function audioTick(){try{__AUD.tick()}catch(e){}}
 function prepare(f){
  var b=window.__innBg&&window.__innBg();
  f.assets=null;f.failed=false;
  Promise.all([picture(b&&b.def&&b.def.src),f.sid==='P10b'&&window.__innNightPrepare?window.__innNightPrepare():true]).then(function(rows){if(alive(f)){f.assets=rows.every(Boolean);f.failed=!f.assets}});
 }
 function error(f){if(!veil||veil.querySelector('button'))return;
  veil.removeAttribute('aria-hidden');var button=document.createElement('button');button.className='scene-retry';button.textContent='장면을 불러오지 못했어요 · 다시 시도';veil.appendChild(button);
  button.onclick=function(e){e.preventDefault();e.stopImmediatePropagation();if(!alive(f))return;button.remove();prepare(f);
   var song=window.__INN_MUSIC[f.music];if(song&&__AUD.mediaState[song.media]==='error'){__AUD.retryMedia();__AUD.tick()}
  };
 }
 function poll(f){
  if(!alive(f)){if(flow===f)reset();return}
  if(f.black){
   var media=__AUD.mediaPlaying(),song=window.__INN_MUSIC[f.music],audioError=!!(S.sound&&song&&__AUD.mediaState[song.media]==='error');
   var bypass=!S.sound||window.__innAudioHold||!media.state||media.state!=='running'||f.music===null||media.volume===0;
   var lead=bypass||media.key===f.music&&media.started&&media.now-media.at>=.28&&media.gain>.01&&media.busGain>0;
   if(f.failed||audioError)error(f);
   if(f.assets&&window.__innPresentationVisualReady()&&lead){
    f.black=false;f.revealAt=performance.now();f.audioAt=bypass?null:media.at;f.audioClock=bypass?null:media.now;f.bypass=bypass;
    veil.classList.add('opening');var el=veil;setTimeout(function(){if(flow===f&&veil===el){el.remove();veil=null;document.body.classList.remove('inn-scene-black')}},240);
   }
  }
  requestAnimationFrame(function(){poll(f)});
 }
 window.__innSceneFlowBegin=function(owner){
  reset();if(!owner||!owner.scene||!owner.scene.music)return;
  var f=flow={owner:owner,game:owner.game,sid:owner.sid,key:owner.key,music:owner.scene.music,black:true,token:++serial,enteredAt:performance.now()};
  darken(f);audioTick();requestAnimationFrame(function(){poll(f)});
 };
 window.__innSceneFlowDirection=function(d){if(!flow||!alive(flow))return;if(Object.prototype.hasOwnProperty.call(d,'music'))flow.music=d.music;if(d.transition)darken(flow);audioTick()};
 window.__innAuthoredMusic=function(){return flow&&alive(flow)?{key:flow.music,black:flow.black,owner:flow.key}:null};
 window.__innSceneFlowState=function(){return flow&&alive(flow)?{sid:flow.sid,owner:flow.key,music:flow.music,black:flow.black,settled:!veil,revealAt:flow.revealAt,audioAt:flow.audioAt,audioClock:flow.audioClock,bypass:flow.bypass,assets:flow.assets,failed:flow.failed}:null};
 window.__innSceneFlowReset=reset;
 var style=document.createElement('style');style.textContent='#inn-scene-black{position:fixed;inset:0;z-index:66;background:#090b10;opacity:1;pointer-events:none;transition:opacity .24s ease}#inn-scene-black.opening{opacity:0}#inn-scene-black .scene-retry{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);pointer-events:auto;min-height:44px;padding:12px 18px;border:1px solid #ac9166;background:#302b27;color:#f5e5c4;font:14px var(--display,sans-serif)}#inn-scene-black:has(.scene-retry){z-index:69}@media(prefers-reduced-motion:reduce){#inn-scene-black{transition:none}}';document.head.appendChild(style);
})();
