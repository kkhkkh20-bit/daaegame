# Rescue follows the first money investigation; health precedes optional clues.
rep('  if(id==="C05")return has("C11")||(has("C04")&&bt("inn_show_innma_C04"));',
    '  if(id==="C05")return has("C04")&&(has("C11")||bt("inn_show_innma_C04"));')
rep(' function sun(){return has("C04")&&["C03","C07","C12","C13"].some(has)}',
    ' function sun(){return has("C04")&&(bt("inn_life_confirmed")||bt("inn_meet")||bt("inn_final")||has("C05")||has("C11"))&&["C03","C07","C12","C13"].some(function(id){return has(id)||(G.asked||[]).indexOf(id)>=0})}')
rep('["det1","{p0}, 증거가 꽤 모였어! 이 정도면 다들 불러서 이야기해 볼 만해.","happy"],["det0","정오까지는 아직 시간이 있다."]',
    '["det1","다들 식당에 모였어. 저 애부터 봐야 해.","sad"],["det0","그래. 상태부터 함께 확인하자."]')
rep('id="tomeet">원탁 회의 열기</button><button class="btn ghost wide" id="tostay2" style="margin-top:8px">조금 더 조사하기',
    'id="tomeet">작은 손님 함께 살펴보기</button><button class="btn ghost wide" id="tostay2" style="margin-top:8px">잠깐 기록 확인하기')
rep('document.getElementById("tomeet").onclick=function(){closeModal();SFX.gotcha();',
    'document.getElementById("tomeet").onclick=function(){closeModal();SFX.tap();')
# An old save may have rescued the guest before collecting any money clues.
# Let it examine him immediately, then pause before the money discussion.
rep(' function ready(c){var D=DEBATE[c.id];',
    ' function ready(c){if(c.id==="inn"&&has("C04")&&!((G.beats||{}).inn_life_confirmed))return true;var D=DEBATE[c.id];')
rep(' function start(){var ph=curPh();\n',
    ''' function start(){var ph=curPh();
  if(C.id==="inn"&&SKEY==="debate"&&stt().pi===2&&!["C01","C02","C03"].every(has)){
   stt().hold={need:["C01","C02","C03"],task:"손님은 살아 있어요. 이제 주머니와 이불, 나비의 말을 확인해요."};
   if(el){el.remove();el=null}window.__inMeeting=false;G.tab="scene";G.notice={title:"돈 사건을 더 살펴봐요",text:stt().hold.task};try{saveProg()}catch(e){}render();return;
  }
''')
# Numbers, unlike the original boolean beats, must survive save sanitization.
rep('  delete n.beats.rtTally;',
    '  delete n.beats.inn_meeting_version;if(b.inn_meeting_version===2)n.beats.inn_meeting_version=2;\n  delete n.beats.rtTally;')
# A mid-examination save must retain all six abstentions, including categories
# that are vote destinations rather than character seats.
rep('(EP.MEET.seats||[]).forEach(function(k){var v=b.rtTally[k];',
    '(EP.MEET.seats||[]).concat(["부녀","기권","기권(나비)"]).forEach(function(k){var v=b.rtTally[k];')
rep('  return out;\n };\n\n /* 증거 카드:',
    '''  if(b.inn_meet||b.inn_final||b.inn_end||(g.debate&&g.debate.done)){
   n.beats.inn_life_confirmed=1;n.beats.inn_meeting_version=2;
  }else if(g.debate&&b.inn_meeting_version!==2){
   n.debate=null;delete n.beats.rtTally;delete n.beats.rtVotes;delete n.beats.toMeet;delete n.beats.inn_i9;n.beats.inn_meeting_version=2;
  }
  return out;
 };

 /* 증거 카드:''')
# The original boolean-beat sanitizer also collapsed the per-person vote map.
rep('  if(b.inn_meet||b.inn_final||b.inn_end||(g.debate&&g.debate.done)){',
    '''  delete n.beats.rtVotes;
  if(b.rtVotes&&typeof b.rtVotes==="object"&&!Array.isArray(b.rtVotes)){
   var vv={},seats=EP.MEET.seats||[],dest=seats.concat(["부녀","기권"]);
   seats.filter(function(k){return k!=="innma"&&k!=="seryeon"}).forEach(function(k){if(dest.indexOf(b.rtVotes[k])>=0)vv[k]=b.rtVotes[k]});n.beats.rtVotes=vv;
  }
  if(b.inn_meet||b.inn_final||b.inn_end||(g.debate&&g.debate.done)){''')
# Also protect an in-memory slot before native stt() interprets its phase index.
rep('function open(c,spec){if(window.__innPreOpen',
    '''function open(c,spec){if(!spec&&c&&c.id==="inn"&&G){G.beats=G.beats||{};if(G.debate&&!G.debate.done&&!G.beats.inn_meet&&G.beats.inn_meeting_version!==2){G.debate=null;delete G.beats.rtTally;delete G.beats.rtVotes;delete G.beats.inn_i9}G.beats.inn_meeting_version=2;try{saveProg()}catch(e){}}if(window.__innPreOpen''')
# Polling a closed council must not create a debate in a newly loaded game.
rep(' var el=null,C=null,Q=null,qi=0,sel=null,si=0,prev={},busy=false;',
    ' var el=null,C=null,Q=null,qi=0,sel=null,si=0,prev={},busy=false,activeGame=null;')
rep('  window.__inMeeting=true;\n', '  window.__inMeeting=true;activeGame=G;\n')
rep(' window.__rtCur=function(){if(!el||!SPEC)return null;var ph=curPh();return ph?ph.type:null};window.__rtPh=function(){return SPEC&&curPh()};',
    ' window.__rtCur=function(){var ph=window.__rtPh();return ph?ph.type:null};window.__rtPh=function(){if(!el||!el.isConnected||!window.__inMeeting||!SPEC||G!==activeGame||!G[SKEY])return null;return SPEC.phases[G[SKEY].pi]||null};')
