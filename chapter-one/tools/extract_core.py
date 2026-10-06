"""Extract original game rule functions verbatim; never copy the old UI renderer."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]
source=(root/'game.html').read_text()
names=['allSpots','evById','tById','locOfEv','fresh','curPlayer','locOpen','evDesc','hpMax','gated','stmsOf','comboFor','haveItem','autoHint','recItems','judgeBattle']
def extract(name):
 start=source.index('function '+name+'(');opening=source.index('{',start);depth=1;i=opening+1;quote=None;escape=False
 while depth:
  c=source[i]
  if quote:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c==quote:quote=None
  elif c in ['"',"'",'`']:quote=c
  elif c=='{':depth+=1
  elif c=='}':depth-=1
  i+=1
 return source[start:i]
functions={n:extract(n) for n in names}
header='''/* Generated from game.html by tools/extract_core.py.
   The original rules execute against a chapter adapter; old DOM/audio effects
   are mapped to events. Do not independently rewrite these rule functions. */
window.DaramLegacy={create:function(c,combos,saved){
var CASES=[c],COMBO={[c.id]:combos},BATTLE={[c.id]:c.rounds},CAST=c.cast,CONFESS={[c.id]:'confession'};
var S={players:['다람','아빠']},DL=null,events=[];
var document={querySelector:function(){return null},getElementById:function(){return null}};
var window={scrollTo:function(){},__hush:function(){return Promise.resolve()},__testi:function(){return []},__CONF2:{}};
var SFX=new Proxy({},{get:function(_,name){return function(){if(globalThis.DaramAudio)globalThis.DaramAudio.fx(name)}}});
function render(){} function floater(){} function bgm(){} function panicFx(w,k,n,done){done()}
function flash(){return Promise.resolve()} function banner(){return Promise.resolve()}
function jo(n){return n} function itemName(c,id){var e=evById(c,id),t=tById(c,id);return e?e.name:t?CAST[t.who].name+'의 말':id}
function say(lines,done){events.push({type:'dialogue',lines:lines});if(done)done()}
function setTimeout(done){done()}
'''
footer='''
var G=Object.assign(fresh(0),saved||{});
return {
 state:G,
 records:function(tab){return recItems(c,tab)},
 selectRecord:function(id){if(recItems(c,"ev").concat(recItems(c,"t")).indexOf(id)<0)return false;G.recordSelection=id;G.seen=G.seen||[];if(G.seen.indexOf(id)<0)G.seen.push(id);return true;},
 evidence:function(id){return evById(c,id)},testimony:function(id){return tById(c,id)},
 have:function(id){return haveItem(c,id)},gated:function(id){return gated(c,id)},
 description:function(id){var e=evById(c,id);return e?evDesc(e):''},
 locationOpen:function(i){return locOpen(c,i)},player:function(){return curPlayer()},
 discover:function(id){if(!evById(c,id))return false;if(G.found.indexOf(id)<0){G.found.push(id);G.actions++;return true}return false},
 examine:function(id){var e=evById(c,id);if(!e||!e.check)return false;G.exam[id]=true;G.actions++;return true},
 ask:function(id){if(!tById(c,id))return false;if(G.asked.indexOf(id)<0){G.asked.push(id);G.actions++}return true},
 combine:function(a,b){
  if(!haveItem(c,a)||!haveItem(c,b))return {kind:'missing'};
  if(gated(c,a)||gated(c,b))return {kind:'inspect'};
  var x=comboFor(c,a,b);if(!x){G.wrong++;return {kind:'wrong'}};
  var i=combos.indexOf(x);if(!G.logic)G.logic=[];
  if(G.logic.indexOf(i)<0){G.logic.push(i);G.found.push(x.id);G.coins=Math.min(30,(G.coins|0)+1);G.actions++}
  return {kind:'success',item:x};
 },
 begin:function(round,si){G.battle={cul:c.rounds[round].who,round:round,si:si||0,lives:G.hp,max:hpMax(c),miss:0,phase:'fight'}},
 present:async function(round,si,id){
  if(!haveItem(c,id))return {kind:'missing'};
  if(!G.battle||G.battle.phase!=='fight'||G.battle.round!==round)this.begin(round,si);
  G.battle.si=si;
  var before=G.hp,st=stmsOf(c.rounds[round]),ok=!!(st[si].a&&st[si].a.indexOf(id)>=0),blocked=ok&&gated(c,id);
  events=[];judgeBattle(c,id);
  // Original visual timers run synchronously in this adapter; drain its promise effects.
  await new Promise(function(resolve){globalThis.setTimeout(resolve,0)});
  var kind=blocked?'inspect':ok?'success':!G.battle?'exhausted':'wrong';
  if(ok&&!blocked){G.broken['round:'+round]=true;if(round===1&&G.unlocked.indexOf('door:archive')<0)G.unlocked.push('door:archive')}
  return {kind:kind,hp:G.hp,before:before,events:events};
 },
 hint:function(){if(G.hints>=3)return false;G.hints++;return true},
 finish:function(answers){var wrong=c.final.filter(function(f,i){return answers[i]!==f.answer}).length;
  if(wrong){G.dtries++;return false}G.answers=answers;G.result={solved:true,stars:Math.max(1,3-(G.wrong>0?1:0)-(G.hints>=2?1:0))};return true}
};
}};
'''
(root/'chapter-one/legacy-core.js').write_text(header+'\n'.join(functions.values())+footer)
(root/'chapter-one/legacy-provenance.json').write_text(json.dumps({n:{'line':source[:source.index('function '+n+'(')].count('\n')+1,'sha256':hashlib.sha256(f.encode()).hexdigest()} for n,f in functions.items()},indent=2))
print('Extracted',len(functions),'original rule functions including judgeBattle')
