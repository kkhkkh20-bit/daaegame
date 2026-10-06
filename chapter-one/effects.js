/* Original-game effect vocabulary, adapted to a fixed portrait scene.
   No camera shake, fullscreen flashes or input-blocking overlays. */
(()=>{'use strict';
const KEY='daram-chapter-one-effects-v1';let preference='standard',timer,animation,serial=0;
try{const v=localStorage.getItem(KEY);if(['standard','simple','off'].includes(v))preference=v;}catch{}
const cues={
 shock:{mark:'!',label:'깜짝',sound:'shock'},sweat:{mark:'…',label:'당황',sound:'gulp'},insight:{mark:'!',label:'잠깐, 이건…',sound:'thinkin'},tease:{mark:'♪',label:'시치미',sound:'blush'},
 press:{mark:'잠깐!',label:'추궁',sound:null},objection:{mark:'모순 발견!',label:'증거로 반박',sound:null},wrong:{mark:'…?',label:'다시 생각해 보자',sound:null},
 found:{mark:'증거 기록',label:'수첩에 추가',sound:null},connect:{mark:'단서 연결!',label:'추리가 이어졌다',sound:null},win:{mark:'사건 해결',label:'첫 번째 사건',sound:null}
};
function layer(){let e=document.getElementById('scene-effect');if(!e){e=document.createElement('div');e.id='scene-effect';e.setAttribute('role','status');e.setAttribute('aria-live','polite');document.getElementById('game').appendChild(e);}return e;}
function clear(){serial++;clearTimeout(timer);animation?.cancel();animation=null;const e=document.getElementById('scene-effect');if(e){e.replaceChildren();e.removeAttribute('data-effect');}}
function play(kind){const c=cues[kind];if(!c||document.hidden)return;clear();if(c.sound)window.DaramAudio?.fx(c.sound);if(preference==='off')return;
 const e=layer(),quiet=preference==='simple'||matchMedia('(prefers-reduced-motion: reduce)').matches;e.dataset.effect=kind;e.dataset.motion=quiet?'simple':'standard';
 const tag=document.createElement('div');tag.className='effect-tag';const small=document.createElement('small');small.textContent=c.label;const b=document.createElement('b');b.textContent=c.mark;tag.append(small,b);e.append(tag);
 const actor=document.getElementById('actor');if(!quiet&&actor&&!actor.hidden){const frames=kind==='shock'?[{transform:'translateY(0)'},{transform:'translateY(-7px)',offset:.3},{transform:'translateY(0)'}]:kind==='sweat'||kind==='wrong'?[{transform:'translateX(0)'},{transform:'translateX(-3px)'},{transform:'translateX(3px)'},{transform:'translateX(0)'}]:null;if(frames)animation=actor.animate(frames,{duration:300,easing:'ease-out'});}
 const token=serial;timer=setTimeout(()=>{if(token===serial)clear();},quiet?650:900);
}
window.DaramEffects={play,clear,get:()=>preference,set(v){if(!['standard','simple','off'].includes(v))return;preference=v;try{localStorage.setItem(KEY,v);}catch{}clear();},cue(line){if(line?.fx)play(line.fx);}};
document.addEventListener('visibilitychange',()=>{if(document.hidden)clear();});
})();
