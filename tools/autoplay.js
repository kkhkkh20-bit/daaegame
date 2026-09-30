// Full in-page playthrough of every case: find all, ask all, break all contras via judgePresent, battle via judgeBattle, deduce, wrap.
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const file=process.argv[2], only=(process.argv[3]||"").split(",").filter(Boolean);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage({viewport:{width:390,height:844},hasTouch:true});
const errs=[];p.on('pageerror',e=>errs.push('PAGE '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('CON '+m.text())});
await p.goto('file://'+file);await p.waitForTimeout(400);await p.evaluate(()=>{window.__T('window.__revAll=true;0')});const T=c=>p.evaluate(x=>window.__T(x),c);
const clear=async()=>{await T('while(DL)endDlg();closeModal();document.querySelectorAll(".ovr,.flash,.banner,.crec2,.sbook,.zoomv,.recon,.show,.moment,.cutin,.stampfx,.coach,.lens,.flyev").forEach(function(x){x.remove()});0');};
const n=await T('CASES.length');
for(let ci=0;ci<n;ci++){const cid=await T(`CASES[${ci}].id`);if(only.length&&only.indexOf(cid)<0)continue;
 const log=[];
 await T(`S.tspeed="i";S.story.pro=true;S.story.finale=true;CASES.forEach(function(c,k){if(k<${ci})S.best[c.id]=3});G=fresh(${ci});G.introDone=true;S.screen="case";G.tab="scene";render();0`);await p.waitForTimeout(200);await clear();
 // find everything reachable, ask everything, break contras, iterate
 for(let round=0;round<8;round++){
  const st=await T(`(function(){var c=CASES[${ci}];var f=0;c.locations.forEach(function(l,i){if(!locOpen(c,i))return;l.spots.forEach(function(s){if(G.found.indexOf(s.ev.id)<0){G.found.push(s.ev.id);f++}})});
   var a=0;people(c).forEach(function(k){visibleTalk(c,k).forEach(function(t){if(t.q!==""&&G.asked.indexOf(t.id)<0){G.asked.push(t.id);a++}})});
   (COMBO[c.id]||[]).forEach(function(x,i){if(x.off)return;var id="cx_"+c.id+"_"+i;if(G.found.indexOf(id)<0&&haveItem(c,x.a)&&haveItem(c,x.b)){G.found.push(id);if(!G.logic)G.logic=[];G.logic.push(i);f++}});
   allSpots(c).forEach(function(s){if(s.ev.check){if(!G.exam)G.exam={};G.exam[s.ev.id]=true}});
   return {f:f,a:a}})()`);
  const todo=await T(`JSON.stringify(CASES[${ci}].contra.filter(function(x){return !G.broken[x.t]&&G.asked.indexOf(x.t)>=0}).map(function(x){return [x.t,x.items.filter(function(i){return haveItem(CASES[${ci}],i)})[0]]}))`);
  const list=JSON.parse(todo);
  if(!list.length&&!st.f&&!st.a)break;
  for(const [t,item] of list){ if(!item){log.push('no item in hand for '+t);continue}
   const hp0=await T('G.hp');
   await T(`G.tab="talk";render();judgePresent(CASES[${ci}],"${t}","${item}");0`);await p.waitForTimeout(1900);
   for(let k=0;k<12;k++){const d=await T('!!DL||!!document.querySelector(".ovr,.flash,.banner")');if(!d)break;await T('if(DL)endDlg();0');await p.waitForTimeout(350)}
   const br=await T(`!!G.broken["${t}"]`);if(!br)log.push('present failed '+t+' with '+item+' hp '+hp0+'->'+await T('G.hp'));
   await clear();
  }
 }
 const unb=await T(`JSON.stringify(CASES[${ci}].contra.filter(function(x){return !G.broken[x.t]}).map(function(x){return x.t}))`);if(unb!=='[]')log.push('unbroken '+unb);
 const unq=await T(`(function(){var c=CASES[${ci}],o=[];people(c).forEach(function(k){c.talk[k].forEach(function(t){if(t.q!==""&&t.id!==CONFESS[c.id]&&G.asked.indexOf(t.id)<0)o.push(t.id)})});return JSON.stringify(o)})()`);if(unq!=='[]')log.push('unasked '+unq);
 const unl=await T(`JSON.stringify(CASES[${ci}].locations.filter(function(l,i){return !locOpen(CASES[${ci}],i)}).map(function(l){return l.id}))`);if(unl!=='[]')log.push('locked '+unl);
 // battle
 await T(`(function(){var t=window.TWIST&&TWIST[CASES[${ci}].id];if(t&&t.card){G.exam=G.exam||{};G.exam[t.card.id]=true}})();0`);
 await T(`G.tab="final";G.hp=hpMax(CASES[${ci}]);render();accuse(CASES[${ci}],culOf(CASES[${ci}]));0`);await p.waitForTimeout(2500);
 for(let k=0;k<20;k++){const d=await T('!!DL||!!document.querySelector(".ovr,.flash,.banner")');if(!d)break;await T('if(DL)endDlg();0');await p.waitForTimeout(300)}await clear();
 for(let r=0;r<12;r++){
  const ph=await T('G.battle&&G.battle.phase');if(ph!=='fight')break;
  const pick=await T(`(function(){var c=CASES[${ci}],st=stmsOf(rOf(c));for(var i=0;i<st.length;i++){var it=(st[i].a||[]).filter(function(x){return haveItem(c,x)})[0];if(it)return JSON.stringify([i,it])}return "null"})()`);
  if(pick==='null'){log.push('battle round '+await T('G.battle.round')+' no item');break}
  const [si,it]=JSON.parse(pick);
  await T(`G.battle.si=${si};render();judgeBattle(CASES[${ci}],"${it}");0`);await p.waitForTimeout(2200);
  for(let k=0;k<30;k++){const d=await T('!!DL||!!document.querySelector(".ovr,.flash,.banner")');if(!d)break;await T('if(DL)endDlg();0');await p.waitForTimeout(300)}
  await clear();
 }
 const ph=await T('G.battle&&G.battle.phase');if(ph!=='won')log.push('battle not won, phase '+ph+' lives '+await T('G.battle&&G.battle.lives'));
 // wrap starts by itself after the confession
 await T(`render();0`);await p.waitForTimeout(900);await T('var s=document.getElementById("showskip");if(s)s.click();0');
 for(let k=0;k<80;k++){await p.waitForTimeout(400);const d=await T('!!DL||!!document.querySelector(".show,.recon,.sbook,.banner,.flash,.ovr")');if(!d)break;await T('if(DL)endDlg();var s=document.querySelector("#showskip,#reconskip,#sbskip");if(s)s.click();0')}
 await clear();await p.waitForTimeout(300);
 const res=await T('JSON.stringify({solved:!!(G&&G.result&&G.result.solved),stars:G&&G.result&&G.result.stars,best:S.best})');
 console.log(cid, log.length?log:'OK', res);
 await T('S.screen="board";G=null;render();0');
}
console.log('errors',errs);await b.close()})();
