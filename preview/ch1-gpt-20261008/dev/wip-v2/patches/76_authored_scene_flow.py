# Wait for an asynchronous direction's assets, then its authored hold. Cancelled
# night work must never advance an old scene into a new game.
rep('if(it.dir){try{window.__innDir&&window.__innDir(it.dir)}catch(e){}setTimeout(function(){Promise.resolve(window.__innPresentationWait?window.__innPresentationWait():true).then(function(ready){if(ready)step()})},it.dir.ms!=null?it.dir.ms:420);return}',
    'if(it.dir){var directionWait=true;try{directionWait=window.__innDir?window.__innDir(it.dir):true}catch(e){}Promise.resolve(directionWait).then(function(ok){if(ok===false)return;setTimeout(function(){Promise.resolve(window.__innPresentationWait?window.__innPresentationWait():true).then(function(ready){if(ready)step()})},it.dir.ms!=null?it.dir.ms:420)});return}')
rep('var at=Math.max(I.t0,I.ctx.currentTime);src.start(at,Math.max(0,at-I.t0)%src.loopEnd);',
    'var at=Math.max(I.t0,I.ctx.currentTime);I.mediaAt=at;src.start(at,Math.max(0,at-I.t0)%src.loopEnd);')
rep('var XF=1.1;', '''A.mediaPlaying=function(){var I=L.cur;return {key:I&&I.key||null,started:!!(I&&I.mediaSource&&!I.dead&&!I.stopAt),at:I&&I.mediaAt,now:L.ctx&&L.ctx.currentTime,state:L.ctx&&L.ctx.state,gain:I&&I.g.gain.value,busGain:L.bus&&L.bus.gain.value,duck:A.duck,volume:MUSV}};
 A.retryMedia=function(){if(L.cur){instKill(L.cur);L.cur=null}A.cur=null};
 var XF=1.1;''')
# The epilogue uses the same presentation gate as the prologue.
rep('var go=function(){if(!sceneAlive())return;play(s.items,function(){if(sceneAlive())runEnd(i+1)})};',
    'var go=function(){if(!sceneAlive())return;Promise.resolve(window.__innPresentationWait?window.__innPresentationWait():true).then(function(ready){if(ready&&sceneAlive())play(s.items,function(){if(sceneAlive())runEnd(i+1)})})};')
rep('e.target.closest("#inn-story-cg .cinema-retry")',
    'e.target.closest("#inn-story-cg .cinema-retry,#inn-scene-black .scene-retry")')
