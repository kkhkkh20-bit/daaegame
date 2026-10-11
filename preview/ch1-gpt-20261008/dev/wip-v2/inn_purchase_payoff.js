/* Chapter 1: evidence earned before the final money claim, resumable in old saves. */
(function(){
 var ep=window.EP1INN;
 function inn(){return !!(G&&CASES[G.ci]&&CASES[G.ci].id==='inn')}
 function known(id){return inn()&&((G.found||[]).indexOf(id)>=0||(G.asked||[]).indexOf(id)>=0)}
 function pending(){return inn()&&(G.beats||{}).inn_meet&&!(G.beats||{}).inn_final}
 function needsWitness(){return pending()&&G.innfinal&&G.innfinal.pi===3&&!known('C14')}
 var task='여관 밖 까로에게 세련 손님을 묻자. 이미 들었다면 숙박부를 보여주자.';
 var sanit=sanitizeState;sanitizeState=function(d){
  var out=sanit(d),g=d&&d.prog&&d.prog.inn,n=out.prog&&out.prog.inn,f=g&&g.innfinal;
  if(!n)return out;delete n.innfinal;
  if(!f||typeof f!=='object'||Array.isArray(f)||!Number.isInteger(f.pi)||f.pi<0||f.pi>ep.FINAL.phases.length)return out;
  if(f.pi===ep.FINAL.phases.length&&!f.done)return out;
  var v={pi:f.pi,done:!!f.done,sus:{}};
  (ep.MEET.seats||[]).forEach(function(k){var x=f.sus&&f.sus[k];if(Number.isInteger(x)&&x>=0&&x<=100)v.sus[k]=x});
  if(!v.done&&v.pi===3&&((g.found||[]).indexOf('C14')<0&&(g.asked||[]).indexOf('C14')<0))v.hold={need:['C14'],task:task};
  else if(!v.done&&f.hold&&v.pi===3)v.hold={need:['C14'],task:task};
  n.innfinal=v;return out;
 };
 var rf=renderFinal;renderFinal=function(c){
  if(c.id!=='inn'||!pending())return rf.apply(this,arguments);
  var waiting=needsWitness(),started=!!G.innfinal;
  return '<section class="panel rtpanel"><h3>'+(waiting?'대결 잠시 중단':'최종 대결')+'</h3><p>'+esc(waiting?task:'모은 증거로 세련의 말을 확인하자.')+'</p><button class="btn red wide" id="inn-final-resume"'+(waiting?' disabled':'')+'>'+(started?'대결 이어가기':'대결 시작')+'</button><button class="btn ghost wide" id="inn-final-investigate" style="margin-top:8px">조사하기</button></section>';
 };
 var bf=bindFinal;bindFinal=function(c){bf.apply(this,arguments);var game=G;
  var b=document.getElementById('inn-final-resume');if(b)b.onclick=function(){if(G===game&&pending()&&!needsWitness())window.__innOpenFinal()};
  var r=document.getElementById('inn-final-investigate');if(r)r.onclick=function(){if(G===game&&pending())goTab('scene')};
 };
 // The evidence icon opens the native record. Reuse its footer so returning
 // from witness investigation takes one clear button, without a hidden tab.
 var scheduled=false;
 function recordResume(){scheduled=false;if(!pending()||document.querySelector('body>.rt'))return;
  var record=document.querySelector('.crec2'),b=record&&record.querySelector('.cr199 [data-cr199]');
  if(!b||b.dataset.payoffResume)return;
  var game=G,waiting=needsWitness();b.dataset.payoffResume='1';b.id='inn-final-record-resume';b.dataset.cr199='final';b.disabled=!!waiting;
  b.textContent=waiting?'까로의 증언을 더 확인해요':'대결 이어가기';b.title=waiting?task:'모은 증거로 세련의 말을 확인한다';
  b.onclick=function(){if(G!==game||!pending()||needsWitness())return;var x=record.querySelector('.cr-x');if(x)x.click();else record.remove();if(G===game)window.__innOpenFinal()};
 }
 function schedule(){if(!scheduled){scheduled=true;requestAnimationFrame(recordResume)}}
 new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true});schedule();
 var ns=nextStep;nextStep=function(c){if(c.id==='inn'&&needsWitness()){var i=c.locations.findIndex(function(l){return l.id==='plaza'});return {say:task,tab:'scene',loc:i}}return ns.apply(this,arguments)};
 var ei=evIcon;evIcon=function(id){if(!inn()||id!=='C14')return ei.apply(this,arguments);return '<svg class="evic" viewBox="0 0 72 72" aria-hidden="true"><path fill="#513c2b" d="M13 7h42v4h4v54H13z"/><path fill="#f3e3b7" d="M17 11h34v8h4v42H17z"/><path fill="#b39868" d="M21 25h22v4H21zm0 8h22v4H21zm0 8h14v4H21zM51 11v8h8z"/><path fill="#835632" d="M37 47h22v12H37zM41 43h10v4H41z"/><path fill="#ebd29b" d="M41 49h14v5H41z"/><path fill="#392d25" d="M39 57h6v6h-6zm12 0h6v6h-6z"/></svg>'};
})();
