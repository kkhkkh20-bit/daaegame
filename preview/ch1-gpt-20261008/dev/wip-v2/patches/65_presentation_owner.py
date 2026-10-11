# A banner/dir timer must belong to the game and chapter scene that created it.
# runEnd already has its scene guard from patch 64; apply the same ownership to
# the prologue and the native item sequencer used by both controllers.
rep(''' function play(items,done){var i=0;
  function step(){if(i>=items.length){done&&done();return}var it=items[i];''',
    ''' function play(items,done){var i=0,playGame=G,playBeats=G.beats||{},playPhase=!playBeats.inn_pro?"pro":playBeats.inn_final&&!playBeats.inn_end?"end":null,playSid=playPhase==="pro"?playBeats.inn_pi:playBeats.inn_ei;
  function step(){if(G!==playGame||S.screen!=="case"||!cur())return;var b=G.beats||{};if(playPhase==="pro"&&(b.inn_pro||b.inn_pi!==playSid)||playPhase==="end"&&(!b.inn_final||b.inn_end||b.inn_ei!==playSid))return;if(i>=items.length){done&&done();return}var it=items[i];''')
rep('''  var go=function(){play(s.items,function(){if(s.after==="title"){(window.banner?banner(EP.title,EP.chapter):Promise.resolve()).then(function(){runPro(i+1)})}else runPro(i+1)})};''',
    '''  var proGame=G;function proAlive(){return G===proGame&&S.screen==="case"&&cur()===c&&!bt("inn_pro")&&G.beats.inn_pi===i}
  var go=function(){if(!proAlive())return;play(s.items,function(){if(!proAlive())return;if(s.after==="title"){(typeof banner==="function"?banner(EP.title,EP.chapter):Promise.resolve()).then(function(){if(proAlive())runPro(i+1)})}else runPro(i+1)})};''')
