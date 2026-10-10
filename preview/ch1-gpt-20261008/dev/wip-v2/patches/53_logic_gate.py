# Preserve native presentation's retry protection and old saves. The separate
# two-card/conclusion gate was retired in favour of direct evidence presentation.
rep('return;C=c;Q=null;qi=0;sel=null;si=0;prev={};',
    'return;window.__logicNativeEpoch=(window.__logicNativeEpoch||0)+1;busy=false;C=c;Q=null;qi=0;sel=null;si=0;prev={};')
rep('  busy=true;\n  var md=modeOf(ph),hit=st.k===md&&st.a&&st.a.length;', '''  busy=true;
  var ng=G,ne=el,np=ph,ns=SPEC,ninn=C.id==="inn",epoch=window.__logicNativeEpoch||0;
  function nativeAlive(){return !ninn||(G===ng&&el===ne&&ne&&ne.isConnected&&SPEC===ns&&curPh()===np&&S.screen==="case"&&(window.__logicNativeEpoch||0)===epoch)}
  var md=modeOf(ph),hit=st.k===md&&st.a&&st.a.length;''')
rep('(window.__hush?window.__hush(false):Promise.resolve()).then(function(){return flash(md==="yes"?"그 말이 맞아!":"그건 아니야!",false,true)}).then(function(){busy=false;if(window.__crowd)window.__crowd();sayQ(st.ok||[],nextPh)})',
    '(window.__hush?window.__hush(false):Promise.resolve()).then(function(){if(nativeAlive())return flash(md==="yes"?"그 말이 맞아!":"그건 아니야!",false,true)}).then(function(){if(!nativeAlive())return;busy=false;if(window.__crowd)window.__crowd();sayQ(st.ok||[],nextPh)})')
rep('window.__rtgReset=function(){STEP=new Map();PRESSED=new Set();MARK={};ASKGEN++;',
    'window.__rtgReset=function(){window.__logicNativeEpoch=(window.__logicNativeEpoch||0)+1;STEP=new Map();PRESSED=new Set();MARK={};ASKGEN++;')
# Keep legacy notebook completion history harmlessly; it never advances a claim.
rep('    n.beats=map(g.beats,null,null,400);', '''    if(isObj(g.reason)&&g.reason.version===1)n.reason={version:1,solved:ids(g.reason.solved,function(k){return ["linen","time","location","seal","contact"].indexOf(k)>=0},5)};
    n.beats=map(g.beats,null,null,400);''')
