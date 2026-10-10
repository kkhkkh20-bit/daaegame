# Different tempos must not cross-play for 1.1 seconds. Fade this chapter's
# old source before starting its new score; leave other cases' policy alone.
rep(' function play(key){\n  if(L.cur&&L.cur.key===key&&!L.cur.stopAt)return;',
    ' function play(key){\n  if(L.cur&&L.cur.key===key&&!L.cur.stopAt)return;\n  var cleanTurn=!!window.__INN_MUSIC&&((key&&key.indexOf("inn_")===0)||(L.cur&&L.cur.key.indexOf("inn_")===0));')
rep('if(L.cur){fadeOut(L.cur,key?XF:.6);L.cur=null}',
    'if(L.cur){fadeOut(L.cur,cleanTurn?.08:(key?XF:.6));L.cur=null}')
rep('var t0=a.currentTime+(L.sceneStart?.005:.08),I=Inst(a,key,s,L.bus,L.wet,t0);',
    'var t0=a.currentTime+(cleanTurn?.14:(L.sceneStart?.005:.08)),I=Inst(a,key,s,L.bus,L.wet,t0);')
rep('t0+(L.sceneStart?.012:(L.old.length?.9:.35))',
    't0+(cleanTurn?.4:(L.sceneStart?.012:(L.old.length?.9:.35)))')
