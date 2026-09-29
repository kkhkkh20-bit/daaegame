// Usage: node dumpstory.js <built.html> <outdir>  — dumps all player-visible text per case + canon summary
const { chromium } = require('/home/claude/.npm-global/lib/node_modules/playwright');
const fs=require('fs');const file=process.argv[2],out=process.argv[3];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});const p=await b.newPage();
await p.goto('file://'+file);await p.waitForTimeout(600);
const data=await p.evaluate(()=>window.__T(`(function(){
 function J(x){try{return JSON.stringify(x,function(k,v){return typeof v==="function"?undefined:v},1)}catch(e){return ""}}
 var G2={};try{__twPrep&&__twPrep();__secretPrep&&__secretPrep()}catch(e){}
 var o={canon:[]};
 CASES.forEach(function(c,i){
  var id=c.id,s=[];
  s.push("# "+(i+1)+"장 "+c.title+" ("+id+") part="+(c.part||1));
  s.push("## CASE (story/solution/final/hints/locations/talk/contra)");
  var cc={title:c.title,time:c.time,teaser:c.teaser,story:c.story,solution:c.solution,ending:c.ending,final:c.final,hints:c.hints,suspects:c.suspects,witnesses:c.witnesses,
   locations:c.locations.map(function(l){return {id:l.id,name:l.name,info:l.info,obs:l.obs,spots:l.spots.map(function(sp){return {id:sp.id,text:sp.text,uv:sp.uv,ev:sp.ev}})}}),talk:c.talk,contra:c.contra};
  s.push(J(cc));
  [["STORY",STORY[id]],["BOOK",window.BOOK&&BOOK[id]],["COMBO",COMBO[id]],["BATTLE",BATTLE[id]],["TIMELINE",c.timeline||(window.TIMELINE&&TIMELINE[id])],["RECON",c.recon],["DEDUCE",window.DEDUCE&&DEDUCE[id]],["LETTER",LETTERS[id]],["MOMENT",window.MOMENT&&MOMENT[id]],["RIDDLES",window.RIDDLES&&RIDDLES[id]],["IHINT",window.IHINT&&IHINT[id]],["MEETX",window.MEETX&&MEETX[id]],["TWIST",window.TWIST&&TWIST[id]],["BAIT",window.BAIT&&BAIT[id]],["TRAP",window.TRAP&&TRAP[id]],["SECRET",window.SECRET&&SECRET[id]]].forEach(function(x){if(x[1])s.push("## "+x[0]+"\\n"+J(x[1]))});
  var th={};allSpots(c).forEach(function(sp){if(THINK[sp.ev.id])th[sp.ev.id]=THINK[sp.ev.id]});s.push("## THINK\\n"+J(th));
  var fl={};Object.keys(window.FLAV||{}).forEach(function(k){if(k.indexOf(id+"-")===0)fl[k]=FLAV[k].map(function(f){return f.n+": "+[].concat(f.t).join(" / ")})});s.push("## FLAV\\n"+J(fl));
  o[id]=s.join("\\n");
  o.canon.push((i+1)+"장 "+c.title+" ["+id+"]\\n줄거리: "+c.story+"\\n시간: "+(c.time||"")+"\\n해답: "+J(c.solution)+"\\n편지: "+J(LETTERS[id]||"")+"\\n후일담: "+J(STORY[id]&&STORY[id].outro));
 });
 o.cast=J(Object.keys(CAST).map(function(k){return k+" "+CAST[k].name+" "+CAST[k].animal+" "+(CAST[k].kind||"")+" | BIO: "+(BIO[k]||"")+" | PERSONA: "+J(PERSONA[k]||"")}));
 o.letters=J(LETTERS);o.vfile=J((window.VFILE||[]).map(function(v){return v.text||v.t||v.body||""}));
 return JSON.stringify(o)})()`));
const o=JSON.parse(data);
for(const k of Object.keys(o)){if(k==='canon'){fs.writeFileSync(out+'/canon.txt',o.canon.join('\n\n'));continue}fs.writeFileSync(out+'/'+k+'.txt',o[k])}
console.log(Object.keys(o).map(k=>k+':'+(typeof o[k]==='string'?o[k].length:o[k].length)).join(' '));await b.close()})();
