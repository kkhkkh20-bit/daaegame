# Proof UI gates sit before the legacy single-evidence verdict.  Records in
# G.reason are notebook history, never authority to skip an interactive gate.
rep('window.addEventListener(t,function(e){if(!e.isTrusted)return;var o=blocker();',
    'window.addEventListener(t,function(e){if(!e.isTrusted)return;if(e.target&&e.target.closest&&e.target.closest("#logic-panel"))return;var o=blocker();')
# The older 400ms dialogue burst guard must not consume new modal controls.
rep('t.closest("#dlgveil,.sbook,.csx")', 't.closest("#dlgveil,.sbook,.csx,#logic-panel")', 2)
# Native proof presentation crosses two asynchronous effects.  A retry can
# create another table before those effects finish, so snapshot its identity.
rep('return;C=c;Q=null;qi=0;sel=null;si=0;prev={};',
    'return;window.__logicNativeEpoch=(window.__logicNativeEpoch||0)+1;busy=false;C=c;Q=null;qi=0;sel=null;si=0;prev={};')
rep('  busy=true;\n  var md=modeOf(ph),hit=st.k===md&&st.a&&st.a.length;', '''  busy=true;
  var ng=G,ne=el,np=ph,ns=SPEC,ninn=C.id==="inn",epoch=window.__logicNativeEpoch||0;
  function nativeAlive(){return !ninn||(G===ng&&el===ne&&ne&&ne.isConnected&&SPEC===ns&&curPh()===np&&S.screen==="case"&&(window.__logicNativeEpoch||0)===epoch)}
  var md=modeOf(ph),hit=st.k===md&&st.a&&st.a.length;''')
rep('(window.__hush?window.__hush(false):Promise.resolve()).then(function(){return flash(md==="yes"?"그 말이 맞아!":"그건 아니야!",false,true)}).then(function(){busy=false;if(window.__crowd)window.__crowd();sayQ(st.ok||[],nextPh)})',
    '(window.__hush?window.__hush(false):Promise.resolve()).then(function(){if(nativeAlive())return flash(md==="yes"?"그 말이 맞아!":"그건 아니야!",false,true)}).then(function(){if(!nativeAlive())return;busy=false;if(window.__crowd)window.__crowd();sayQ(st.ok||[],nextPh)})')
rep(' var STEP=new Map(),PRESSED=new Set(),MARK={};', ''' var STEP=new Map(),PRESSED=new Set(),MARK={};
 var REASONPASS=new WeakSet(),REASONWAIT=null,REASONGEN=0,REASONOWNER=null;
 var REASONIDS=["linen","time","location","seal","contact"];
 function reasonId(value){return typeof value==="string"&&REASONIDS.indexOf(value)>=0}
 function reasonInn(){try{if(G!==REASONOWNER){REASONOWNER=G;REASONGEN++;REASONWAIT=null;REASONPASS=new WeakSet()}return G&&S.screen==="case"&&CASES[G.ci].id==="inn"}catch(e){return false}}
 window.__logicGateCancel=function(){REASONGEN++;REASONWAIT=null};
 function reasonStart(value,done){
  if(!reasonInn()||!value||!reasonId(value.reason)||REASONPASS.has(value))return false;
  if(REASONWAIT)return true;
  /* Fail closed when a bundle omits the required UI module. */
  if(typeof window.__logicOpen!=="function"){window.__logicEngineError="Missing reasoning UI";return true}
  var token={gen:REASONGEN,g:G,r:rt(),p:ph(),value:value},committed=false;
  REASONWAIT=token;
  window.__logicOpen(value.reason,{mode:isFinal(token.p)?"final":"meet",done:function(){
   if(committed||REASONWAIT!==token||token.gen!==REASONGEN||G!==token.g||S.screen!=="case"||rt()!==token.r||ph()!==token.p)return;
   committed=true;REASONWAIT=null;REASONPASS.add(value);done&&done();
  }});
  return true;
 }
 /* Pending contact lines must survive clicks before meta's observer runs. */
 document.addEventListener("click",function(e){
  if(!reasonInn())return;
  var t=e.target&&e.target.closest&&e.target.closest('#rtnext,#rtgq,#rtgbar [data-g="next"],.rt .rt-bub.stm .wk,#rtgbar [data-g="present"],#rtnx,#rtprev,#rtleave,#rtgtr [data-g="leave"]');
  if(!t)return;
  if(REASONWAIT||(window.__logicBusy&&window.__logicBusy())){e.stopImmediatePropagation();e.preventDefault();return}
  if(t.matches('#rtnext,#rtgq,#rtgbar [data-g="next"]')){
   var line=Q?Q[QI]:curLine();
   if(reasonStart(line)){e.stopImmediatePropagation();e.preventDefault()}
  }
 },true);
''')
rep('window.__rtgReset=function(){STEP=new Map();PRESSED=new Set();MARK={};ASKGEN++;',
    'window.__rtgReset=function(){window.__logicNativeEpoch=(window.__logicNativeEpoch||0)+1;REASONGEN++;REASONWAIT=null;REASONPASS=new WeakSet();if(window.__logicReset)window.__logicReset();STEP=new Map();PRESSED=new Set();MARK={};ASKGEN++;')
rep(' function meta(L){if(!L)return;\n',
    ' function meta(L){if(!L)return;\n  if(L.reason)reasonStart(L);\n')
rep('  var steps=s.steps||[],step=STEP.get(s)||0,a=s.a||[];\n', '''  var steps=s.steps||[],step=STEP.get(s)||0,a=s.a||[];
  if(reasonInn()&&reasonId(s.reason)&&!REASONPASS.has(s)){
   stop();
   reasonStart(s,function(){
    if(curStm()!==s){REASONPASS.delete(s);return}
    var id0=a[0],pick=[].slice.call(document.querySelectorAll(".rt .rt-bul [data-bl]")).filter(function(x){return x.dataset.bl===id0})[0];
    if(!pick){REASONPASS.delete(s);window.__logicEngineError="Required evidence is unavailable: "+id0;return}
    STEP.set(s,steps.length);
    /* Selecting the native evidence redraws the statement and supplies the
       legacy fire() closure with a[0].  No proof result invokes fire directly. */
    pick.click();
    if(curStm()!==s){REASONPASS.delete(s);return}
    var live=document.querySelector('#rtgbar [data-g="present"]');
    if(!live)return;
    live.dataset.go="1";B.classList.add("rtg-drw");
    try{live.click()}finally{delete live.dataset.go}
   });return;
  }
''')
rep('window.__rtgPausedExtra=function(){return !!Q||!!PK}',
    'window.__rtgPausedExtra=function(){return !!Q||!!PK||!!REASONWAIT||!!(window.__logicBusy&&window.__logicBusy())}')
rep('function advance(){\n',
    'function advance(){\n if(window.__logicBusy&&window.__logicBusy())return;\n')
# The save sanitizer drops unknown fields by default.  Only completed known
# puzzle ids survive; drafts and arbitrary user-provided fields are discarded.
rep('    n.beats=map(g.beats,null,null,400);', '''    if(isObj(g.reason)&&g.reason.version===1)n.reason={version:1,solved:ids(g.reason.solved,function(k){return ["linen","time","location","seal","contact"].indexOf(k)>=0},5)};
    n.beats=map(g.beats,null,null,400);''')
