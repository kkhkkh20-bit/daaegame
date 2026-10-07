/* Original game.html presentation functions, with chapter asset adapters. */
(()=>{'use strict';
const CAST=PEOPLE;
const SFX=new Proxy({},{get:(_,name)=>()=>window.DaramAudio?.fx(name)});
const PANIC={culprit:[["뭐, 뭐라고?!","헉!"],["그, 그건… 그러니까…!","으윽!"],["말도 안 돼… 어떻게 그걸…!","크윽!"],["아아악! 아니야, 아니라고!","끝이다…"]],shy:[["히익! 그, 그거 보지 마!","히잉…"]],mistake:[["어…? 어어?! 그럼 내가…?","어라?"]]};
const HAND='<span aria-hidden="true">☛</span>';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const quiet=()=>window.DaramEffects?.get()!=='standard'||matchMedia('(prefers-reduced-motion: reduce)').matches;
const evById=(_,id)=>EVIDENCE[id];
const tById=(_,id)=>TESTIMONIES[id]&&{who:TESTIMONIES[id].who};
const evIcon=id=>DaramEvidenceArt.thumb(id,EVIDENCE[id]?.title||id);
const pf=(id,mood)=>'<div class="legacy-portrait" style="background-image:url('+DaramArt.source(id)+');background-position:'+(mood==='nervous'?50:0)+'% 0" aria-hidden="true"></div>';
const spiky=()=>'<svg viewBox="0 0 300 100" aria-hidden="true"><path d="M0 30L30 25 20 0 65 16 80 0 110 14 140 0 155 13 185 0 200 16 240 0 250 22 300 10 280 44 300 65 263 70 275 100 230 84 200 100 175 87 145 100 120 86 83 100 65 85 22 100 30 75 0 80 15 55Z"/></svg>';
function quake(){if(quiet())return;document.getElementById('scene')?.animate([{transform:'translateX(0)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'none'}],{duration:240});}
// Keep original durations in basic mode; remove movement and shorten beats in reduced/off modes.
function setTimeout(fn,ms){return window.setTimeout(fn,quiet()?Math.min(ms,160):ms);}
function flash(text,bad,point){
  return new Promise(function(res){
    var f=document.createElement("div");f.className="flash"+(bad?" bad":"")+(point?" point":"");
    f.innerHTML='<div class="wf"></div>'+(point?'<div class="hand">'+HAND+'</div>':'')+'<div class="shout">'+spiky()+'<b>'+text+'</b></div>';
    document.body.appendChild(f);quake();
    if(bad)SFX.buzz();else SFX.shout();
    setTimeout(function(){f.remove();res()},1150);
  });
}
function panicFx(who,kind,level,cb){
  var p=CAST[who];if(!p){cb&&cb();return}
  var arr=PANIC[kind]||PANIC.culprit,pk=arr[Math.min(level||0,arr.length-1)];
  var d=document.createElement("div");d.className="ovr k-"+kind+" lv"+Math.min(level||0,3);
  d.innerHTML='<div class="plines"></div><div class="pcrack"></div><div class="ppor">'+pf(who,kind==="shy"?"shy":kind==="mistake"?"confused":"nervous")+
    '<i class="sw s1"></i><i class="sw s2"></i><i class="sw s3"></i></div><div class="pono">'+pk[1]+'</div><div class="pq"><span>'+p.name+'</span><b>'+pk[0]+'</b></div>';
  document.body.appendChild(d);
  if(kind==="culprit"){SFX.shock();setTimeout(SFX.slam,120);if(level>=2)setTimeout(SFX.crash,260);try{navigator.vibrate&&navigator.vibrate([60,40,60,40,160])}catch(e){}}
  else if(kind==="shy")SFX.blush();else SFX.huh();
  quake();
  setTimeout(function(){d.classList.add("out");setTimeout(function(){d.remove();cb&&cb()},260)},kind==="culprit"?1500:1150);
}
function banner(text,sub){
  return new Promise(function(res){
    var d=document.createElement("div");var tl=String(text||"").replace(/<[^>]+>/g,"").length;d.className="banner"+(tl>10?" xl":tl>6?" lg":"");
    d.innerHTML='<div class="bars"><div class="bar1"></div><div class="mid">'+(sub?'<small>'+sub+'</small>':'')+'<b>'+text+'</b></div><div class="bar2"></div></div>';
    document.body.appendChild(d);SFX.swoosh();
    setTimeout(function(){SFX.slam()},180);
    setTimeout(function(){d.remove();res()},1400);
  });
}
function flyEvidence(from,id,c){
  return new Promise(function(res){
    var r=from?from.getBoundingClientRect():{left:innerWidth/2-20,top:innerHeight-200,width:40,height:40};
    var d=document.createElement("div");d.className="flyev";
    var e=evById(c,id);d.innerHTML=e?evIcon(id):pf(tById(c,id).who);
    d.style.left=(r.left+r.width/2-30)+"px";d.style.top=(r.top+r.height/2-30)+"px";
    document.body.appendChild(d);SFX.swoosh();
    var dx=innerWidth/2-(r.left+r.width/2),dy=innerHeight*0.4-(r.top+r.height/2);
    if(!d.animate){d.remove();res();return}
    d.animate([{transform:"translate(0,0) scale(1) rotate(0)"},{transform:"translate("+dx+"px,"+dy+"px) scale(3) rotate(360deg)"}],{duration:480,easing:"cubic-bezier(.3,.1,.3,1)",fill:"forwards"}).onfinish=function(){
      SFX.present();setTimeout(function(){d.remove();res()},160);
    };
  });
}
window.DaramPresentation={
 flash:(text,bad,point)=>window.DaramEffects?.get()==='off'?Promise.resolve():flash(esc(text),bad,point),
 panic:(who,kind,level)=>window.DaramEffects?.get()==='off'?Promise.resolve():new Promise(resolve=>panicFx(who,kind,level,resolve)),
 banner:(text,sub)=>window.DaramEffects?.get()==='off'?Promise.resolve():banner(esc(text),esc(sub||'')),
 present(from,id){if(quiet())return Promise.resolve();return flyEvidence(from,id,{});}
};
})();
