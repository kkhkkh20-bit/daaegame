# A short scene can introduce a native debate without inserting a new phase.
# Existing final-phase save indices therefore still identify the same topics.
rep('  if(ph.type==="debate"){try{banner(modeOf(ph)==="no"?"토론 개시 · 틀린 말 찾기":"토론 개시 · 맞는 말 찾기",ph.topic)}catch(e){}draw();return}',
    '''  if(ph.type==="debate"){
   var begin=function(){try{banner(modeOf(ph)==="no"?"토론 개시 · 틀린 말 찾기":"토론 개시 · 맞는 말 찾기",ph.topic)}catch(e){}draw()};
   if(ph.intro&&ph.intro.length){sayQ(ph.intro,begin);return}begin();return}''')
# Repeated taps during the objection animation must never start another verdict.
rep(' function hurt(msg){G.wrong=', ''' function hurt(msg){if(busy)return;busy=true;
  var hg=G,he=el,hs=SPEC,hp=curPh(),hinn=C.id==="inn",epoch=window.__logicNativeEpoch||0;
  G.wrong=''')
rep('  flash("헛짚었다!",true).then(function(){sayQ([{w:"det1",t:msg}],function(){draw()})})}',
    '''  flash("헛짚었다!",true).then(function(){
   if(hinn&&(G!==hg||el!==he||!he||!he.isConnected||SPEC!==hs||curPh()!==hp||S.screen!=="case"||(window.__logicNativeEpoch||0)!==epoch))return;
   busy=false;sayQ([{w:"det1",t:msg}],function(){draw()})})}''')
rep(' function fire(){var ph=curPh(),st=ph.stms[si];',
    ' function fire(){if(busy)return;var ph=curPh(),st=ph.stms[si];')
rep(' function vote(k){var ph=curPh(),cul=culOf(C);',
    ' function vote(k){if(busy)return;var ph=curPh(),cul=culOf(C);')
rep('  SFX.gotcha();flash("범인은 너다!",false,true).then(function(){sayQ(ph.ok||[],nextPh)})',
    '''  busy=true;var vg=G,ve=el,vs=SPEC,vinn=C.id==="inn",epoch=window.__logicNativeEpoch||0;
  SFX.gotcha();flash("범인은 너다!",false,true).then(function(){
   if(vinn&&(G!==vg||el!==ve||!ve||!ve.isConnected||SPEC!==vs||curPh()!==ph||S.screen!=="case"||(window.__logicNativeEpoch||0)!==epoch))return;
   busy=false;sayQ(ph.ok||[],nextPh)})''')
# Intro lines use the same audio/meta dispatcher as the native spoken lines.
rep('  (p.lines||[]).forEach(function(x){pool.push(x)});(p.stms||[]).forEach',
    '  (p.intro||[]).concat(p.lines||[]).forEach(function(x){pool.push(x)});(p.stms||[]).forEach')
