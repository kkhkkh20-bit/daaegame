const PREF='daram-chapter-one-audio-v1';
let prefs={music:.55,effects:.7},unlocked=false,wanted='calm',lastBlip=0;
try{const p=JSON.parse(localStorage.getItem(PREF));for(const k of ['music','effects'])if(Number.isFinite(p?.[k]))prefs[k]=Math.max(0,Math.min(1,p[k]));}catch{}
function levels(){if(!AC)return;BGMG.gain.value=.1*prefs.music;SFXG.gain.value=.42*prefs.effects;MASTER.gain.value=S.sound?MGAIN:0;}
function pause(){S.sound=false;bgm(null);levels();if(AC&&AC.state==='running')AC.suspend().catch(()=>{});}
function resume(){if(!unlocked||document.hidden||!(prefs.music||prefs.effects))return pause();S.sound=true;try{const a=ac();if(a?.state==='suspended')a.resume().catch(()=>{});levels();if(prefs.music)bgm(wanted);else bgm(null);}catch{}}
window.DaramAudio={
 unlock(){unlocked=true;resume();},
 music(mode){if(!PAT[mode])return;wanted=mode;if(unlocked&&!document.hidden)resume();},
 fx(name,...args){if(!unlocked||!S.sound||document.hidden||!prefs.effects)return;if(name==='blip'){const now=Date.now();if(now-lastBlip<65)return;lastBlip=now;}try{SFX[name]?.(...args);}catch{}},
 set(key,value){if(!['music','effects'].includes(key)||!Number.isFinite(value))return;prefs[key]=Math.max(0,Math.min(1,value));try{localStorage.setItem(PREF,JSON.stringify(prefs));}catch{}resume();},
 get(){return {...prefs};},
 status(){return {unlocked,mode:wanted,playing:!!BGM.timer,context:AC?.state||'uninitialized',musicGain:BGMG?.gain.value||0,effectsGain:SFXG?.gain.value||0};}
};
document.addEventListener('visibilitychange',()=>document.hidden?pause():resume());
window.addEventListener('pagehide',pause);window.addEventListener('pageshow',()=>{if(unlocked)resume();});
// Start or resume only from an explicit game interaction, including iOS touch-generated clicks.
document.addEventListener('click',e=>{if(e.target.closest('#game button,#game select,#game input'))window.DaramAudio.unlock();},true);
