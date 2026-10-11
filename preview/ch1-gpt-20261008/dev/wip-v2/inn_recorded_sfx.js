/* Recorded wood doors. Horse audio is disabled by the user's request. */
(function(){
 var files={open:"wood-door-open.wav",close:"wood-door-close.wav"},cache={},context=null;
 var stats={starts:{horse:0,open:0,close:0},live:{horse:0,open:0,close:0},errors:0};
 function chapter(){try{return S.screen==="case"&&G&&CASES[G.ci].id==="inn"}catch(e){return false}}
 function load(a,key){
  if(context!==a){context=a;cache={}}
  if(!cache[key])cache[key]=fetch("audio/v3/sfx/"+files[key]).then(function(r){if(!r.ok)throw Error("SFX "+r.status);return r.arrayBuffer()}).then(function(b){return a.decodeAudioData(b)}).catch(function(e){delete cache[key];stats.errors++;throw e});
  return cache[key];
 }
 function source(a,key,b,out,loop){
  var src=a.createBufferSource();src.buffer=b;src.loop=loop;if(loop){src.loopStart=0;src.loopEnd=1.2}
  src.connect(out);stats.starts[key]++;stats.live[key]++;src.onended=function(){stats.live[key]--;try{src.disconnect()}catch(e){}};return src;
 }
 function play(key){
  if(!files[key]||!chapter()||!S.sound||!AC||AC.state!=="running")return;
  var a=AC,game=G,at=performance.now();
  load(a,key).then(function(b){
   if(!chapter()||G!==game||AC!==a||!S.sound||a.state!=="running"||performance.now()-at>300)return;
   var g=a.createGain();g.gain.value=.65;g.connect(SFXG);var src=source(a,key,b,g,false),end=src.onended;
   src.onended=function(){end();g.disconnect()};src.start();
  }).catch(function(){});
 }
 function attach(I,key){
  if(!files[key])return;
  load(I.a,key).then(function(b){
   if(I.dead||I.ending||!S.sound||AC!==I.a||!chapter())return;
   var src=source(I.a,key,b,I.out,true);I.src.push(src);src.start();
  }).catch(function(){});
 }
 window.__innRecordedSfx={play:play,attach:attach,stats:function(){return JSON.parse(JSON.stringify(stats))}};
 // Decode doors only; the archived horse recording is never fetched.
 setInterval(function(){if(AC&&AC.state==="running"&&S.sound&&(chapter()||document.getElementById("innmain")))Object.keys(files).forEach(function(k){load(AC,k).catch(function(){})})},800);
})();
