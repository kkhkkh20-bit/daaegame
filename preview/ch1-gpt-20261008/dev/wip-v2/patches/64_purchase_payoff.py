# Keep the five native final phase indices stable; testimony is earned in play.
rep('function dlgOpen(){return !!(document.getElementById("dlgveil")||document.querySelector(".sbook,.csx"))}',
    'function dlgOpen(){return !!(document.getElementById("dlgveil")||document.querySelector(".sbook,.csx,#inn-mother-lead,#inn-ch2-peek"))}')
rep('  if(C.id==="inn"&&SKEY==="debate"&&stt().pi===2', '''  if(C.id==="inn"&&SKEY==="innfinal"&&stt().pi===3&&!has("C14")){
   stt().hold={need:["C14"],task:"여관 밖 까로에게 세련 손님을 묻자. 이미 들었다면 숙박부를 보여주자."};
   Q=null;qi=0;sel=null;if(el){el.remove();el=null}window.__inMeeting=false;G.tab="scene";G.notice={title:"대결 잠시 중단",text:stt().hold.task};try{saveProg()}catch(e){}render();return;
  }
  if(C.id==="inn"&&SKEY==="debate"&&stt().pi===2''')
rep('if(spec){SPEC=spec;SKEY=spec.key||"debate2";G[SKEY]=null}',
    'if(spec){SPEC=spec;SKEY=spec.key||"debate2";if(!(c.id==="inn"&&SKEY==="innfinal"&&G[SKEY]&&!G[SKEY].done&&Number.isInteger(G[SKEY].pi)&&G[SKEY].pi>=0&&G[SKEY].pi<spec.phases.length))G[SKEY]=null}')
rep('  var s=stt();if(s.hold){var adj=SPEC.phases[s.pi-1];',
    '  var s=stt();if(C.id==="inn"&&SKEY==="innfinal"&&s.pi===3&&!has("C14")){start();return}if(s.hold){var adj=SPEC.phases[s.pi-1];')
rep('  banner("회의 중단","증거를 더 찾아 와야 해요").then(function(){',
    '  var pausedGame=G,pausedEl=el,pausedSpec=SPEC,isFinal=C.id==="inn"&&SKEY==="innfinal";banner(isFinal?"대결 잠시 중단":"회의 중단","증언을 더 확인해요").then(function(){if(G!==pausedGame||el!==pausedEl||SPEC!==pausedSpec||S.screen!=="case")return;')
rep('G.notice={title:"회의가 중단됐어요",text:esc(ph.task||"증거를 더 찾아 오세요.")+" 찾으면 아래 \'증거\'에서 \'원탁 회의 열기\'로 다시 열 수 있어요."};render()})}',
    'G.notice={title:isFinal?"대결 잠시 중단":"회의가 중단됐어요",text:esc(ph.task||"증거를 더 찾아 오세요.")+(isFinal?" 확인하면 대결을 이어갈 수 있어요.":" 찾으면 아래 \'증거\'에서 \'원탁 회의 열기\'로 다시 열 수 있어요.")};render()})}')
rep('function openFinal(){var c=cur();if(!c)return;G.hp=EP.FINAL_HP||c.lives||5;',
    'function openFinal(){var c=cur();if(!c)return;var finalGame=G;if(!(G.innfinal&&!G.innfinal.done))G.hp=EP.FINAL_HP||c.lives||5;')
rep('setTimeout(function(){if(cur()&&window.__rtOpen)window.__rtOpen(c,F)},250)',
    'setTimeout(function(){if(G===finalGame&&S.screen==="case"&&cur()===c&&!bt("inn_final")&&window.__rtOpen)window.__rtOpen(c,F)},250)')
rep('if(kind==="final"){G.notice=EP.FINAL_RETRY;',
    'if(kind==="final"){G.innfinal=null;G.notice=EP.FINAL_RETRY;')
rep('F.onDone=function(){try{setb("inn_final");G.tab="scene";G.notice=null;saveProg();render();setTimeout(function(){runEnd(0)},300)}',
    'F.onDone=function(){try{var finishedGame=G;setb("inn_final");G.tab="scene";G.notice=null;saveProg();render();setTimeout(function(){if(G===finishedGame&&S.screen==="case"&&bt("inn_final")&&!bt("inn_end"))runEnd(0)},300)}')
rep('  var go=function(){play(s.items,function(){runEnd(i+1)})};',
    '  var sceneGame=G;function sceneAlive(){return G===sceneGame&&S.screen==="case"&&bt("inn_final")&&!bt("inn_end")&&G.beats.inn_ei===i}var go=function(){if(!sceneAlive())return;play(s.items,function(){if(sceneAlive())runEnd(i+1)})};')
rep('   var fin=function(){G.notice=EP.THE_END.notice;try{saveProg()}catch(e){}render()};\n   try{banner(EP.THE_END.banner[0],EP.THE_END.banner[1]).then(fin)}catch(e){fin()}return}',
    '''   var endGame=G;function aliveEnd(){return G===endGame&&S.screen==="case"&&cur()===c&&bt("inn_end")}
   var fin=function(){if(!aliveEnd())return;G.notice=EP.THE_END.notice;try{saveProg()}catch(e){}render()};
   var peek=function(){if(!aliveEnd())return;try{if(window.__innChapter2Peek&&window.__innChapter2Peek(fin))return}catch(e){}fin()};
   try{banner(EP.THE_END.banner[0],EP.THE_END.banner[1]).then(peek)}catch(e){peek()}return}''')
