/* Generated from game.html by tools/extract_core.py.
   The original rules execute against a chapter adapter; old DOM/audio effects
   are mapped to events. Do not independently rewrite these rule functions. */
window.DaramLegacy={create:function(c,combos,saved){
var CASES=[c],COMBO={[c.id]:combos},BATTLE={[c.id]:c.rounds},CAST=c.cast,CONFESS={[c.id]:'confession'};
var pending=[];function track(p){pending.push(p);return p;}
var S={players:['다람','아빠']},DL=null,events=[];
var document={querySelector:function(){return null},getElementById:function(){return null}};
var window={scrollTo:function(){},__hush:function(){return Promise.resolve()},__testi:function(){return []},__CONF2:{}};
var SFX=new Proxy({},{get:function(_,name){return function(){if(globalThis.DaramAudio)globalThis.DaramAudio.fx(name)}}});
function render(){} function floater(){} function bgm(){}
function panicFx(w,k,n,done){var fx=globalThis.DaramPresentation;if(fx)track(fx.panic(w,k,n).then(done));else done()}
function flash(text,bad,point){var fx=globalThis.DaramPresentation;return fx?track(fx.flash(text,bad,point)):Promise.resolve()}
function banner(text,sub){var fx=globalThis.DaramPresentation;return fx?track(fx.banner(text,sub)):Promise.resolve()}
function jo(n){return n} function itemName(c,id){var e=evById(c,id),t=tById(c,id);return e?e.name:t?CAST[t.who].name+'의 말':id}
function say(lines,done){events.push({type:'dialogue',lines:lines});if(done)done()}
function setTimeout(done){done()}
function allSpots(c){var r=[];c.locations.forEach(function(l){l.spots.forEach(function(s){r.push(s)})});return r}
function evById(c,id){var e=null;allSpots(c).forEach(function(s){if(s.ev.id===id)e=s.ev});return e}
function tById(c,id){var r=null;Object.keys(c.talk).forEach(function(k){c.talk[k].forEach(function(t){if(t.id===id)r={t:t,who:k}})});return r}
function locOfEv(c,id){var r="";c.locations.forEach(function(l){l.spots.forEach(function(s){if(s.ev.id===id)r=l.name})});return r}
function fresh(i){return {mem:[],coins:1,hintLog:[],dtries:0,ci:i,tab:"scene",loc:0,found:[],asked:[],unlocked:[],broken:{},marks:{},who:CASES[i].suspects[0],notice:null,wrong:0,hints:0,actions:0,answers:{},result:null,introDone:false,target:null,trayTab:"ev",seen:[],battle:null,accuse:null,hp:CASES[i].lives||5,exam:{},tf:"all"}}
function curPlayer(){return S.players[G.actions%2]}
function locOpen(c,i){var l=c.locations[i];return !l.req||G.unlocked.indexOf(l.req)>=0}
function evDesc(e){return e.check&&G.exam&&G.exam[e.id]?e.check.desc2:e.desc}
function hpMax(c){return c.lives||5}
function gated(c,id){var e=evById(c,id);return !!(e&&e.check&&e.check.gate&&!(G.exam&&G.exam[id]))}
function stmsOf(r){if(!r)return [{t:"",p:"",a:[]}];return r.stm||[{t:r.claim,p:r.press,a:r.accept}]}
function comboFor(c,a,b){return (COMBO[c.id]||[]).filter(function(x){return (x.a===a&&x.b===b)||(x.a===b&&x.b===a)})[0]}
function haveItem(c,id){return G.found.indexOf(id)>=0||G.asked.indexOf(id)>=0}
function autoHint(c,st){
  var s=st.filter(function(x){return x.a})[0];if(!s)return "";
  var a0=s.a.filter(function(id){return G.found.indexOf(id)>=0||G.asked.indexOf(id)>=0})[0]||s.a[0];
  var src=evById(c,a0)?"현장 '"+locOfEv(c,a0)+"'에서 찾은 증거":(tById(c,a0)?CAST[tById(c,a0).who].name+"의 증언":"수첩");
  return "\""+s.t.slice(0,20)+"…\" 이 문장이 수상해. "+src+"랑 나란히 놓고 비교해 보자.";
}
function recItems(c,tab){return tab==="t"?G.asked.filter(function(id){var x=tById(c,id);return x&&x.t.q!==""}):G.found.slice()}
function judgeBattle(c,item){
  var B=G.battle,R=BATTLE[c.id];if(!B||B.round>=R.length||B.phase!=="fight"||DL||document.querySelector(".ovr,.flash,.banner"))return;
  var r=R[B.round],st=stmsOf(r),s=st[(B.si||0)%st.length],cul=B.cul,name=CAST[cul].name;
  var ok=!!(s.a&&s.a.indexOf(item)>=0),elsewhere=!ok&&st.some(function(x){return x.a&&x.a.indexOf(item)>=0});
  if(ok&&gated(c,item)){SFX.huh();say([["think","이 증거가 이 문장이랑 부딪칠 것 같은데… 이것만으론 결정적이지 않아. 수첩에서 이 증거를 눌러 더 자세히 살펴보자.","",curPlayer()]],function(){render()});return}
  if(ok){
    var last=B.round===R.length-1;
    SFX.gotcha();SFX.present();
    window.__hush(last).then(function(){return flash(last?"결정적 증거!":"이의 있음!",false,true)}).then(function(){
      B.round++;B.si=0;B.miss=0;render();floater(".comp","여유 -1","bad");if(!last&&window.__crowd)setTimeout(function(){window.__crowd()},250);
      var foe=document.getElementById("foe");if(foe){foe.classList.add("hit")}
      var _s2=say;say=function(l,d,k){say=_s2;panicFx(cul,"culprit",last?3:Math.min(B.round,2),function(){_s2(l,d,k)})};
      if(!last){
        var nx=function(){say(window.__testi(c,cul,B.round,false),function(){render()},true)};
        say([[cul,r.hit,"nervous","","shock"]],function(){if(B.round===R.length-1)banner("최후의 반론",name).then(nx);else banner("새 반론",name+"의 반론 "+(B.round+1)).then(nx)});
      }else{
        SFX.stamp();
        if(foe){foe.classList.add("breakdown");SFX.crash()}
        setTimeout(function(){
        say([[cul,r.hit,"nervous","","angry"],["narr",name+"의 반론이 모두 무너졌어요!","sad",cul,"shock"],[cul,tById(c,CONFESS[c.id]).t.a,"sad","","cry"]].slice(0,2).concat((window.__CONF2&&window.__CONF2[c.id])||[[cul,tById(c,CONFESS[c.id]).t.a,"sad","","cry"]]),function(){
          G.hp=B.lives;B.phase="won";G.answers={};bgm("sneak");render();window.scrollTo(0,0);
        });
        },1500);
      }
    });
  }else{
    B.lives--;G.hp=B.lives;G.wrong++;B.miss=(B.miss||0)+1;SFX.life();
    flash("헛짚었다!",true).then(function(){
      B.smug=true;B.crack=B.lives;render();floater(".lives","신뢰도 -1","bad");
      var taunts=["흥, "+itemName(c,item)+"? 그게 뭐 어쨌다는 거야?","후후, 그걸로는 어림없지!","그게 내 말이랑 무슨 상관인데? 탐정 맞아?"];
      var bt=window.__bait&&window.__bait(c,s,item);
      var lines=bt?bt.map(function(l){return l[0]==="think"&&!l[3]?[l[0],l[1],"",curPlayer()]:l}):[[cul,taunts[B.lives%3],"smug","","smug"]];
      lines.push(["think",elsewhere?"증거는 맞는 것 같은데… 부딪치는 문장이 달라! ◀ ▶로 다른 문장을 넘겨 보자.":"아니야, 그건 이 문장이랑 부딪치지 않아.","",curPlayer()]);
      if(B.miss>=2&&B.lives>0){var hh=autoHint(c,st);if(hh)lines.push(["think",hh,"",curPlayer()])}
      if(B.lives<=0){
        lines.push(["narr","신뢰도가 바닥났다… "+jo(name,"이","가")+" 빠져나갔어요. 수첩을 다시 정리하고 도전해요."]);
        say(lines,function(){G.battle=null;G.accuse=null;G.hp=hpMax(c);bgm("sneak");render()});
      }else{
        if(B.lives<=2)lines.push(["narr","위험하다! 신뢰도가 "+B.lives+"칸뿐이에요."]);
        say(lines,function(){render()});
      }
    });
  }
}
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
  events=[];pending=[];judgeBattle(c,id);
  // Wait for original effect chains before returning their final rule state.
  do {if(pending.length)await Promise.all(pending.splice(0));await new Promise(function(resolve){globalThis.setTimeout(resolve,0)});}while(pending.length);
  var kind=blocked?'inspect':ok?'success':!G.battle?'exhausted':'wrong';
  if(ok&&!blocked){G.broken['round:'+round]=true;if(round===1&&G.unlocked.indexOf('door:archive')<0)G.unlocked.push('door:archive')}
  return {kind:kind,hp:G.hp,before:before,events:events};
 },
 hint:function(){if(G.hints>=3)return false;G.hints++;return true},
 finish:function(answers){var wrong=c.final.filter(function(f,i){return answers[i]!==f.answer}).length;
  if(wrong){G.dtries++;return false}G.answers=answers;G.result={solved:true,stars:Math.max(1,3-(G.wrong>0?1:0)-(G.hints>=2?1:0))};return true}
};
}};
