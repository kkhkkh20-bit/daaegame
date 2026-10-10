# Sampled score shares the existing music bus, ducking, fades and mute controls.
rep(' function Inst(ctx,key,s,bus,wetIn,t0){', '''
 var MEDIA={},MEDIA_DATA={};A.mediaState={};
 function mediaBuffer(ctx,url){
  if(MEDIA_DATA[url])return Promise.resolve(MEDIA_DATA[url]);
  if(!MEDIA[url]){A.mediaState[url]="loading";MEDIA[url]=fetch(url).then(function(r){if(!r.ok)throw Error("music "+r.status+" "+url);return r.arrayBuffer()}).then(function(b){return ctx.decodeAudioData(b)}).then(function(b){MEDIA_DATA[url]=b;A.mediaState[url]="ready";return b}).catch(function(e){A.mediaState[url]="error";delete MEDIA[url];throw e})}
  return MEDIA[url];
 }
 function mediaStart(I){if(!I.s.media)return;
  function start(buf){if(I.dead||I.stopAt)return;var src=I.ctx.createBufferSource();src.buffer=buf;src.loop=true;src.connect(I.g);I.mediaSource=src;A.stats.made++;A.stats.live++;
   src.onended=function(){try{src.disconnect()}catch(e){}A.stats.live--;A.stats.ended++};
   var at=Math.max(I.t0,I.ctx.currentTime);src.start(at,Math.max(0,at-I.t0)%buf.duration)}
  if(MEDIA_DATA[I.s.media])start(MEDIA_DATA[I.s.media]);else mediaBuffer(I.ctx,I.s.media).then(start).catch(function(e){lg("music error "+e.message)});
 }
 function Inst(ctx,key,s,bus,wetIn,t0){''')
rep('A.stats.inst++;fxStart(ctx,I);return I}', 'A.stats.inst++;fxStart(ctx,I);mediaStart(I);return I}')
rep('function instKill(I){if(I.dead)return;I.dead=true;fxStop(I,I.ctx.currentTime);',
    'function instKill(I){if(I.dead)return;I.dead=true;if(I.mediaSource){try{I.mediaSource.stop()}catch(e){}I.mediaSource=null}fxStop(I,I.ctx.currentTime);')
rep('  var I=Inst(ctx,key,s,bus,wet,0.02);I.g.gain.setValueAtTime(s.vol||1,0);',
    '''  if(s.media)return mediaBuffer(ctx,s.media).then(function(){var J=Inst(ctx,key,s,bus,wet,0.02);J.g.gain.setValueAtTime(s.vol||1,0);return ctx.startRendering().then(function(buf){instKill(J);return buf})});
  var I=Inst(ctx,key,s,bus,wet,0.02);I.g.gain.setValueAtTime(s.vol||1,0);''')
