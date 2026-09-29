// Usage: node validate.js <built-test-html> [caseId,...]
// Static solvability + integrity checks for case data (runs inside the page via window.__T).
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const file=process.argv[2], only=(process.argv[3]||"").split(",").filter(Boolean);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+file);await p.waitForTimeout(400);
const out=await p.evaluate((only)=>window.__T(`(function(only){
 var R=[];
 CASES.forEach(function(c,ci){ if(only.length&&only.indexOf(c.id)<0)return;
  var P=function(m){R.push(c.id+": "+m)};
  if(!/^[a-z]+$/.test(c.id))P("case id must be lowercase letters only (cx regex)");
  var spots=allSpots(c),evIds={},tIds={};
  spots.forEach(function(s){if(evIds[s.ev.id])P("duplicate evidence id "+s.ev.id);evIds[s.ev.id]=1;
    if(!s.inZoom&&!HOTS[s.id])P("spot "+s.id+" has no HOTS position");
    if(s.ev.check&&(!s.ev.check.text||!s.ev.check.desc2))P("check missing text/desc2 on "+s.ev.id)});
  Object.keys(c.talk).forEach(function(k){if(!CAST[k])P("talk for unknown CAST "+k);c.talk[k].forEach(function(t){if(tIds[t.id])P("dup talk id "+t.id);tIds[t.id]=1})});
  c.suspects.concat(c.witnesses||[]).forEach(function(k){if(!CAST[k])P("unknown cast "+k);if(!c.talk[k])P("person without talk "+k)});
  c.locations.forEach(function(l){if(!SCENES[c.id+"-"+l.id])P("no SCENES for "+c.id+"-"+l.id)});
  if(!CONFESS[c.id])P("no CONFESS");else if(!tById(c,CONFESS[c.id]))P("CONFESS id missing in talk");
  if(!BATTLE[c.id])P("no BATTLE");
  if(!STORY[c.id])P("no STORY");
  ["timeline","recon","map"].forEach(function(k){if(!c[k])P("no c."+k)});
  var COM=COMBO[c.id]||[];
  function isItem(id){return !!evById(c,id)||!!tById(c,id)}
  c.contra.forEach(function(x){if(!tById(c,x.t))P("contra t missing "+x.t);x.items.forEach(function(i){if(!isItem(i))P("contra "+x.t+" item unknown "+i)});if(x.unlock&&String(x.unlock).indexOf("door:")!==0&&!tById(c,x.unlock))P("contra unlock unknown "+x.unlock)});
  (BATTLE[c.id]||[]).forEach(function(r,ri){stmsOf(r).forEach(function(s,si){(s.a||[]).forEach(function(i){if(!isItem(i))P("battle r"+ri+" s"+si+" accept unknown "+i)})})});
  COM.forEach(function(x,i){if(!isItem(x.a))P("combo "+i+" a unknown "+x.a);if(!isItem(x.b))P("combo "+i+" b unknown "+x.b)});
  (c.timeline||[]).forEach(function(e){e.src.forEach(function(s){s=s.replace("!","");if(s!=="*"&&!isItem(s))P("timeline src unknown "+s)});if(e.claim&&!tById(c,e.claim))P("timeline claim unknown "+e.claim)});
  // ---- reachability fixed point ----
  var unlocked={},found={},asked={},broken={},riddle={};
  function locOpenX(l){return !l.req||unlocked[l.req]}
  var changed=true,guard=0;
  while(changed&&guard++<50){changed=false;
    c.locations.forEach(function(l){if(!locOpenX(l))return;l.spots.forEach(function(s){if(!found[s.ev.id]){found[s.ev.id]=1;changed=true}})});
    (RIDDLES[c.id]||[]).forEach(function(r,i){if(r.loc&&!unlocked[r.loc]){ // riddle needs its hint knowledge: assume solvable
        unlocked[r.loc]=1;changed=true}});
    Object.keys(c.talk).forEach(function(k){c.talk[k].forEach(function(t){if(asked[t.id]||t.q==="")return;var ok=t.after?asked[t.after]:(!t.hidden||unlocked[t.id]);if(ok){asked[t.id]=1;changed=true}})});
    COM.forEach(function(x,i){var id="cx_"+c.id+"_"+i;if(!found[id]&&(found[x.a]||asked[x.a])&&(found[x.b]||asked[x.b])){found[id]=1;changed=true}});
    c.contra.forEach(function(x){if(broken[x.t]||!asked[x.t])return;if(x.items.some(function(i){return found[i]||asked[i]})){broken[x.t]=1;changed=true;if(x.unlock&&!unlocked[x.unlock]){unlocked[x.unlock]=1}}});
  }
  c.locations.forEach(function(l){if(!locOpenX(l))P("location never opens: "+l.id+" req "+l.req)});
  Object.keys(c.talk).forEach(function(k){c.talk[k].forEach(function(t){if(t.q!==""&&t.id!==CONFESS[c.id]&&!asked[t.id])P("testimony never reachable: "+t.id)})});
  c.contra.forEach(function(x){if(!broken[x.t])P("contra never breakable: "+x.t)});
  (BATTLE[c.id]||[]).forEach(function(r,ri){var ok=stmsOf(r).some(function(s){return (s.a||[]).some(function(i){return found[i]||asked[i]})});if(!ok)P("battle round "+ri+" has no reachable accept item")});
  c.final.forEach(function(f,i){if(f.type==="suspect"&&c.suspects.indexOf(f.answer)<0)P("final "+i+" answer not a suspect");if(f.type==="text"&&(f.opts||[]).indexOf(f.answer)<0)P("final "+i+" answer not in opts");if(f.type==="place"&&!c.locations.some(function(l){return l.id===f.answer}))P("final "+i+" place unknown")});
  if(c.final[0].answer!==culOf(c))P("culprit mismatch");
  var nCul=c.contra.filter(function(x){return (x.kind||"culprit")==="culprit"}).length;if(!nCul)P("no culprit contra");
  R.push(c.id+": OK-summary spots="+spots.length+" talk="+Object.keys(tIds).length+" contra="+c.contra.length+" battle="+(BATTLE[c.id]||[]).length+" combos="+COM.length);
 });
 return R;})(`+JSON.stringify(only)+`)`),only);
console.log(out.join("\n"));console.log("pageerrors",errs);await b.close()})();
