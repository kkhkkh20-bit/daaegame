/* ===== 다람탐정 1장 「열세 번째 침대」 — 진행 연결 =====
   - 대본·증거 데이터는 ep1_inn_script.js(window.EP1INN). 이 파일은 그 데이터를 기존 엔진에 연결만 한다.
   - 기존 우체국 사건(envelope)의 데이터·대사는 건드리지 않는다. 새 사건 id "inn".
   - 흐름: 프롤로그 P1~P11 → 조사 I1~I9 → 원탁회의 M0~M5(실패 M-F) → 최종 대결 F1~F4 → 후일담 E1~E4 */
(function(){
 var MISS=window.__INNMISS=[];var EP=window.EP1INN;if(!EP){MISS.push("no EP1INN");return}
 window.INN_TODO=EP.TODO;
 function N(t){return ["narr",t]}
 function cur(){try{return (G&&S.screen==="case"&&CASES[G.ci]&&CASES[G.ci].id==="inn")?CASES[G.ci]:null}catch(e){return null}}
 function has(id){return G.found.indexOf(id)>=0||G.asked.indexOf(id)>=0}
 function bt(k){G.beats=G.beats||{};return !!G.beats[k]}
 function setb(k){G.beats=G.beats||{};G.beats[k]=1;try{saveProg()}catch(e){}}

 /* ---- 인물 ---- */
 try{Object.keys(EP.CAST).forEach(function(k){CAST[k]=EP.CAST[k]});
  Object.keys(EP.KIND||{}).forEach(function(k){if(CAST[k])CAST[k].kind=EP.KIND[k]});
  if(!CAST.narr)CAST.narr={name:"",animal:"owl",kind:"",color:"#C9A96A"};
  if(window.VOICE){VOICE.innma=VOICE.grandma||0;VOICE.seryeon=VOICE.sling||0;VOICE.geokkuri=VOICE.bami||0}
 }catch(e){MISS.push("cast "+e.message)}

 /* ---- 증거: 카드 객체 ---- */
 var EVO={};Object.keys(EP.EV).forEach(function(id){var x=EP.EV[id],o={id:id,name:x.name};
  if(x.desc2)Object.defineProperty(o,"desc",{enumerable:true,get:function(){try{return bt(x.fixBeat)?x.desc2:x.desc}catch(e){return x.desc}}});else o.desc=x.desc;EVO[id]=o});

 /* ---- 대사 앞의 지문 괄호((작게)·(문가에서)·(옆에서))는 연출 표시라 화면 글자에서 뺀다 ---- */
 var STAGE=/^\((작게|문가에서|옆에서)\)\s*/;
 function clean(arr){(arr||[]).forEach(function(x){if(Array.isArray(x)){if(x[0]!=="narr"&&typeof x[1]==="string")x[1]=x[1].replace(STAGE,"")}else if(x&&typeof x==="object"){if(x.w&&x.w!=="narr"&&typeof x.t==="string")x.t=x.t.replace(STAGE,"");["ok","press"].forEach(function(k){if(x[k])clean(x[k])});
   if(x.wr)Object.keys(x.wr).forEach(function(k){clean(x.wr[k])});if(x.soft)Object.keys(x.soft).forEach(function(k){clean(x.soft[k].lines)});if(x.steps)x.steps.forEach(function(st){clean(st.lines)})}})}
 /* ---- 지문 분류 적용(ep1_inn_direction.js): 무대 지문은 대사창에서 빼고 소리·표정 명령으로, 관찰은 짧은 문구로 ---- */
 var DIRLOG=window.__INN_DIRLOG=[];
 function dirOf(t){return EP.DIR&&EP.DIR[t]}
 function dirList(arr,mode){if(!arr)return arr;var out=[];
  for(var i=0;i<arr.length;i++){var x=arr[i];
   if(Array.isArray(x)&&x[0]==="narr"){var d=dirOf(x[1]);if(d){DIRLOG.push(d.c);
     if(d.cmd&&d.cmd.mood){for(var j=i+1;j<arr.length;j++){var y=arr[j];if(Array.isArray(y)&&y[0]!=="narr"){if(!y[2])y[2]=d.cmd.mood;break}}}
     if(mode==="play"&&d.cmd&&(d.cmd.sfx||d.cmd.fade))out.push({sfx:d.cmd.sfx||null,fade:d.cmd.fade||0});
     if(d.c==="stage")continue;if(d.t){x=x.slice();x[1]=d.t}}}
   else if(x&&typeof x==="object"&&!Array.isArray(x)&&x.w==="narr"&&typeof x.t==="string"){var d2=dirOf(x.t);if(d2){DIRLOG.push(d2.c);if(d2.c==="stage")continue;if(d2.t){x.t=d2.t}}}
   out.push(x)}
  return out}
 try{EP.PRO.concat(EP.END).forEach(function(sc){sc.items=dirList(sc.items,"play")});EP.I9=dirList(EP.I9,"play");EP.MF=dirList(EP.MF,"play");EP.LOCK.open=dirList(EP.LOCK.open,"say");
  EP.LOCS.forEach(function(l){(l.spots||[]).forEach(function(sp){sp.say=dirList(sp.say,"say")});(l.obs||[]).forEach(function(o){o.say=dirList(o.say,"say")})});
  Object.keys(EP.TALK).forEach(function(k){EP.TALK[k].forEach(function(t){t.lines=dirList(t.lines,"say")})});
  [EP.MEET,EP.FINAL].forEach(function(D0){D0.phases.forEach(function(ph){if(ph.lines)ph.lines=dirList(ph.lines,"meet");if(ph.ok)ph.ok=dirList(ph.ok,"meet");
   (ph.stms||[]).forEach(function(st){if(st.ok)st.ok=dirList(st.ok,"meet");if(st.press)st.press=dirList(st.press,"meet");(st.steps||[]).forEach(function(sp){sp.lines=dirList(sp.lines,"meet")});
    if(st.soft)Object.keys(st.soft).forEach(function(k){st.soft[k].lines=dirList(st.soft[k].lines,"meet")});if(st.wr)Object.keys(st.wr).forEach(function(k){st.wr[k]=dirList(st.wr[k],"meet")})})})})}catch(e){MISS.push("dir "+e.message)}
 try{EP.PRO.concat(EP.END).forEach(function(sc){clean(sc.items)});clean(EP.I9);clean(EP.MF);
  EP.LOCS.forEach(function(l){(l.spots||[]).forEach(function(sp){clean(sp.say)});(l.obs||[]).forEach(function(o){clean(o.say)})});
  Object.keys(EP.TALK).forEach(function(k){EP.TALK[k].forEach(function(t){clean(t.lines)})});
  [EP.MEET,EP.FINAL].forEach(function(D0){D0.phases.forEach(function(ph){clean(ph.lines);clean(ph.stms);clean(ph.ok)})})}catch(e){MISS.push("clean "+e.message)}

 /* ---- 사건 ---- */
 var SPOTSAY={},OBSSAY={};
 var C={id:"inn",part:1,title:EP.title,level:1,lives:5,place:"골짜기 마을 겨울잠 여관",time:"다음 날 아침 7시 ~ 정오",
  teaser:"손님 방은 열둘인데 침대는 열셋. 장부에 없는 침대에서 계약금 주머니가 나왔다.",
  story:"골짜기 마을에 도착한 다음 날 아침. 외지 손님의 계약금이 사라졌다.",
  suspects:["innma","seryeon"],witnesses:["nabi","buri","geokkuri","doto","wanggu","karo"],
  locations:EP.LOCS.map(function(l){
   var spots=(l.spots||[]).map(function(s){SPOTSAY[s.ev]=s.say;return {id:"s_"+s.id,name:s.name,text:EVO[s.ev].desc,ev:EVO[s.ev]}});
   var obs=(l.obs||[]).map(function(o){if(o.say)OBSSAY[o.id]=o.say;return {id:o.id,name:o.name,x:o.x,y:o.y,text:o.text}});
   return {id:l.id,name:l.name,short:l.short,spots:spots,obs:obs,info:l.info||[]}}),
  talk:{innma:[],seryeon:[],nabi:[],geokkuri:[],buri:[],doto:[],wanggu:[],karo:[]},
  contra:[],
  final:[{q:"돈주머니를 숨긴 사람은?",type:"suspect",answer:"seryeon"}],
  hints:["살펴볼 곳을 모두 눌러 보세요.","인물에게 질문하면 증언이 기록돼요.","창고는 햇빛이 들 때 다시 보면 달라요."],
  solution:[],ending:"",timeline:[],recon:{sum:{who:"",what:"",how:"",why:""},steps:[]},
  map:{bed13:[300,40,"box"],hall:[220,60,"hall"],dining:[150,110,"hall"],kitchen:[80,90,"door"],dotoroom:[280,120,"door"],front:[150,170,"post"],
   roads:[["front","dining"],["dining","kitchen"],["dining","hall"],["hall","bed13"],["hall","dotoroom"]],deco:"night"},
  ppl:EP.PPL};
 var TALKBY={};
 Object.keys(EP.TALK).forEach(function(k){C.talk[k]=EP.TALK[k].map(function(t){TALKBY[t.id]=t;var o={id:t.id,q:t.q,a:t.rec};if(t.after)o.after=t.after;if(t.need)o.need=t.need;return o})});
 var LI={};C.locations.forEach(function(l,i){LI[l.id]=i});

 /* ---- 원탁회의 / 최종 대결 ---- */
 var D=EP.MEET,F=EP.FINAL;
 D.onDone=function(){try{setb("inn_meet");G.tab="scene";G.notice=null;saveProg();render();openFinal()}catch(e){MISS.push("meetDone "+e.message)}};
 F.onDone=function(){try{setb("inn_final");G.tab="scene";G.notice=null;saveProg();render();setTimeout(function(){runEnd(0)},300)}catch(e){MISS.push("finalDone "+e.message)}};
 try{window.DEBATE.inn=D}catch(e){MISS.push("debate")}
 window.__INN_D=D;window.__INN_F=F;

 /* ---- 사건 등록 ---- */
 try{
  CASES.push(C);
  var M=window.__MEMO=window.__MEMO||{};Object.keys(EP.MEMO).forEach(function(k){M["inn/"+k]=EP.MEMO[k]});
  /* 핫스팟 위치(360x200 기준, 임시 배경 기준) */
  Object.assign(HOTS,{s_bag:[200,130],s_quilt:[110,120],s_ledger:[150,160],s_basket:[180,120],s_fur:[200,128],s_clock:[250,74],s_diary:[250,110],s_book:[150,120]});
  /* 임시 배경: 기존 SVG 장면 재사용(도트 배경 대기) */
  var AL={bed13:"festival-storeroom",dining:"snow-inn",kitchen:"kitchen-kitchen",hall:"glove-parlor",dotoroom:"dark-office",front:"lining-station"};
  Object.keys(AL).forEach(function(k){if(SCENES[AL[k]])SCENES["inn-"+k]=SCENES[AL[k]];else MISS.push("scene "+AL[k])});
 }catch(e){MISS.push("case "+e.message)}

 /* ---- 장면 배경: 대본 장면에 맞는 그림(EP.BGS). 프롤로그·후일담은 장면별(bg), 조사는 장소별(EP.LOC_BG) ---- */
 function bgKey(locId){try{var o=G&&G.beats&&G.beats.inn_bg;if(o)return o}catch(e){}return (EP.LOC_BG||{})[locId]||null}
 function bgSvg(k){var b=EP.BGS[k];if(!b)return null;
  if(b.plain)return '<svg viewBox="0 0 360 200" preserveAspectRatio="xMidYMid slice" role="img" aria-label="'+b.label+'" data-bg="'+k+'"><defs><linearGradient id="innpl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A3550"/><stop offset=".6" stop-color="#2A2438"/><stop offset="1" stop-color="#1C1826"/></linearGradient></defs><rect width="360" height="200" fill="url(#innpl)"/><rect y="150" width="360" height="50" fill="#16121E" opacity=".55"/></svg>';
  var v=b.view;return '<svg viewBox="'+v.join(" ")+'" preserveAspectRatio="xMidYMid slice" role="img" aria-label="'+(b.note||k)+'" data-bg="'+k+'"><image href="'+b.src+'" x="0" y="0" width="'+b.w+'" height="'+b.h+'" preserveAspectRatio="none" style="image-rendering:pixelated"/></svg>'}
 window.__innBg=function(){var c=cur();if(!c)return null;var l=c.locations[G.loc];var k=l&&bgKey(l.id);return k?{key:k,def:EP.BGS[k]}:null};
 try{C.locations.forEach(function(l){var old=SCENES["inn-"+l.id];SCENES["inn-"+l.id]=function(){var k=bgKey(l.id),h=k&&bgSvg(k);return h||(old?old.apply(this,arguments):"")}})}catch(e){MISS.push("bg "+e.message)}
 /* 그림 속에 이미 있는 인물은 대화 칸에 겹쳐 띄우지 않는다(마차 그림의 다람) */
 function cgSync(){try{var b=window.__innBg&&window.__innBg(),cg=(b&&b.def&&b.def.cg)||[];var f=document.getElementById("vnfig");
   document.body.classList.toggle("inn-cg",!!cg.length);if(f)f.classList.toggle("inn-cghide",cg.indexOf(f.dataset.w)>=0)}catch(e){}}
 try{new MutationObserver(function(){if(cgSync.t)return;cgSync.t=requestAnimationFrame(function(){cgSync.t=0;cgSync()})}).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:["data-w"]})}catch(e){}

 /* ---- 대화·컷신 중 조사 숨김: 대사가 떠 있거나 프롤로그·후일담 진행 중이면 조사 버튼·인물·메뉴를 숨긴다 ---- */
 function cutSync(){try{var c=cur(),on=false;if(c){var dl=(typeof DL!=="undefined"&&!!DL)||!!document.getElementById("dlgveil");
   on=dl||!bt("inn_pro")||(bt("inn_final")&&!bt("inn_end"))||!!window.__innCutting}document.body.classList.toggle("inn-cut",on)}catch(e){}}
 try{new MutationObserver(function(){if(cutSync.t)return;cutSync.t=requestAnimationFrame(function(){cutSync.t=0;cutSync()})}).observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
 /* ---- 할머니(여관 주인) 그림: 1장 전용 도트가 아직 없어 기존 토끼 할머니 도트(art/body/innma-*.png = grandma 복사본)를 임시로 쓴다 ---- */
 try{if(window.__BODY202&&window.__BODY202.grandma&&!window.__BODY202.innma)window.__BODY202.innma=window.__BODY202.grandma.slice()}catch(e){MISS.push("innma body")}
 /* 화면 표시 이름·이름표: 대본대로 '아빠' '다람', 옛 역할 표(탐정·증인·상대)는 숨김 */
 try{var st=document.createElement("style");st.id="inn-ui";st.textContent=[
  "img.b202[data-k=innma]{--bw:148!important}",
  "#vnbox .plate small{display:none!important}",
  "#vnfig.inn-cghide{visibility:hidden!important}",
  /* 도트 그림이 아직 없는 인물(세련·거꾸리)은 임시 얼굴을 대화 칸 위에 보이게 한다. 지문(narr)은 인물 칸을 비운다 */
  "body.w209 #vnfig:not(.b202)>svg{position:absolute;left:50%;top:max(16px,5vh);bottom:auto;transform:translateX(-50%);width:min(58vh,240px);height:min(58vh,240px)}",
  "body.w209 #vnfig:not(.b202){top:0!important;bottom:auto!important;left:0!important;right:0!important;width:auto!important;height:100%!important;transform:none!important}",
  "#vnfig[data-w=narr]{visibility:hidden!important}",
  "body.titlescreen #app{visibility:hidden!important}",
  "body.inn-cut #w209rail,body.inn-cut #bigscene .hot,body.inn-cut #bigscene .npc,body.inn-cut .fsa,body.inn-cut .stagebar,body.inn-cut .fsbar,body.inn-cut #w209back{visibility:hidden!important;pointer-events:none!important}",
  "#innhintt{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 12px);transform:translate(-50%,-8px);z-index:90;padding:6px 14px;border-radius:999px;background:rgba(20,16,30,.88);border:1.5px solid #C9A96A;color:#FFF6E0;font:14px/1.3 var(--display,sans-serif);opacity:0;transition:opacity .25s,transform .25s;pointer-events:none;white-space:nowrap}",
  "#innhintt.on{opacity:1;transform:translate(-50%,0)}",
  ".modal .foundic{display:flex;justify-content:center;margin:2px 0 4px}.modal .foundic svg{width:64px;height:64px}"
 ].join("\n");(document.head||document.documentElement).appendChild(st)}catch(e){}

 /* 증거 카드: 질문·회의에서 얻는 증거도 이름·설명을 카드로 */
 try{var _eb=evById;evById=function(c,id){if(c&&c.id==="inn"&&EVO[id])return EVO[id];return _eb.apply(this,arguments)}}catch(e){MISS.push("evById")}
 /* 질문 조건(need: 먼저 가져야 하는 증거) */
 try{var _vt=visibleTalk;visibleTalk=function(c,k){var r=_vt.apply(this,arguments);if(c&&c.id==="inn")r=r.filter(function(t){return !t.need||has(t.need)});return r}}catch(e){MISS.push("visibleTalk")}

 /* ---- 조사 진행 조건: 조건이 안 된 대상은 장면에서 숨김 ---- */
 var FIRST=["C01","C02","C03","C04","C06","C08","C09","C12","C13"];   /* I1~I6에서 얻는 증거 */
 function sun(){return FIRST.every(has)}   /* [임시] I7 창고 햇빛: I1~I6을 마친 뒤 */
 function avail(id){
  if(id==="C11")return bt("inn_lock");
  if(id==="C05")return has("C11");                                   /* [임시] I8 돋보기: 장부를 얻은 뒤 */
  if(id==="o_inn_head"||id==="o_inn_box")return !sun();
  if(id==="o_inn_head2"||id==="o_inn_lock")return sun()&&!bt("inn_lock");
  return true}
 function prune(){var c=cur();if(!c)return;document.querySelectorAll("#bigscene [data-spot],#bigscene [data-obs]").forEach(function(b){var id=b.dataset.spot||b.dataset.obs;if(!avail(id))b.remove()});
}
 try{var _r=render;render=function(){var r=_r.apply(this,arguments);try{prune()}catch(e){}return r}}catch(e){MISS.push("render")}

 /* ---- 순서 진행기: 대사 묶음 + {grant}{loc}{banner}{beat} ---- */
 function play(items,done){var i=0;
  function step(){if(i>=items.length){done&&done();return}var it=items[i];
   if(Array.isArray(it)){var batch=[];while(i<items.length&&Array.isArray(items[i])){batch.push(items[i].slice());i++}say(batch,function(){step()});return}
   i++;
   if(it.hint){hint(it.hint);step();return}
   if(it.sfx!==undefined||it.fade){if(it.sfx)try{SFX[it.sfx]&&SFX[it.sfx]()}catch(e){}if(it.fade){var fd=document.createElement("div");fd.style.cssText="position:fixed;inset:0;z-index:95;background:#000;opacity:0;transition:opacity .35s;pointer-events:none";document.body.appendChild(fd);requestAnimationFrame(function(){fd.style.opacity="1"});setTimeout(function(){fd.style.opacity="0";setTimeout(function(){fd.remove()},380);step()},650);return}step();return}
   if(it.grant){if(G.found.indexOf(it.grant)<0)G.found.push(it.grant);try{SFX.found()}catch(e){}try{saveProg()}catch(e){}if(it.card){gotCard(it.grant,step);return}step();return}
   if(it.loc){G.loc=LI[it.loc];G.beats.inn_bg=null;G.tab="scene";render();setTimeout(step,80);return}
   if(it.banner){try{banner(it.banner[0],it.banner[1]).then(step)}catch(e){step()}return}
   if(it.beat){setb(it.beat);step();return}
   step()}
  step()}
 window.__innPlay=play;
 /* 짧은 조작 안내(누르지 않아도 사라짐, 화면 진행을 막지 않음) */
 function hint(t){try{var h=document.getElementById("innhintt");if(!h){h=document.createElement("div");h.id="innhintt";document.body.appendChild(h)}
  h.textContent=t;h.classList.remove("on");void h.offsetWidth;h.classList.add("on");clearTimeout(hint.t);hint.t=setTimeout(function(){h.classList.remove("on")},3600)}catch(e){}}
 window.__innHint=hint;
 /* 증거 획득 카드: 대본의 [증거 획득]·[다람 수첩]을 대사 대신 카드로 */
 function gotCard(id,done){var e=EVO[id],m=EP.MEMO[id];if(!e){done&&done();return}
  var h='<span class="kicker">증거 획득</span><div class="foundic">'+(typeof evIcon==="function"?evIcon(id):"")+'</div><h3>'+e.name+'</h3><p>'+e.desc+'</p>'+(m?'<p class="soft" style="margin-top:6px"><b>다람 수첩</b> '+m+'</p>':'')+'<button class="btn" id="okfind">확인</button>';
  try{modal(h,function(){document.getElementById("okfind").onclick=function(){try{SFX.tap()}catch(x){}closeModal();render();done&&done()}})}catch(x){done&&done()}}
 window.__innCard=gotCard;

 /* ---- say 확장: 질문은 대본의 주고받기 전체로 / 회의 직전 안내는 I9로 ---- */
 try{var _say=say;say=function(lines,done,sk){try{if(cur()&&Array.isArray(lines)){
   if(lines.length===2&&lines[0]&&lines[0][0]==="det"&&lines[1]&&lines[1][3]==="testi"&&TALKBY[lines[1][5]]){
    var T=TALKBY[lines[1][5]],id=lines[1][5],out=[],marked=false;
    T.lines.forEach(function(l){var x=l.slice();if(!marked&&x[0]===lines[1][0]){x=[x[0],x[1],x[2]||"","testi","",id];marked=true}out.push(x)});
    lines=out;if(T.ev){var d0=done;done=function(){gotCard(id,function(){d0&&d0()})}}}
   else if(lines[0]&&String(lines[0][1]||"").indexOf("증거가 꽤 모였어")>=0&&!bt("inn_i9")){setb("inn_i9");window.__innCutting=true;play(EP.I9,function(){window.__innCutting=false;done&&done()});return}
  }}catch(e){MISS.push("say "+e.message)}
  return _say.call(this,lines,done,sk)}}catch(e){MISS.push("say")}

 /* ---- 살펴보기 전 대사 / 관찰 대사 / 숫자 자물쇠 ---- */
 var played={};
 document.addEventListener("click",function(e){var c=cur();if(!c)return;var b=e.target.closest&&e.target.closest("#bigscene [data-spot],#bigscene [data-obs]");if(!b)return;
  var id=b.dataset.spot||b.dataset.obs;
  if(id==="o_inn_lock"){e.stopImmediatePropagation();e.preventDefault();lockPad();return}
  var L0=b.dataset.spot?SPOTSAY[id]:OBSSAY[id];if(!L0||played[id]||(b.dataset.spot&&G.found.indexOf(id)>=0))return;
  e.stopImmediatePropagation();e.preventDefault();played[id]=1;
  /* 대사가 끝나면 엔진의 원래 살펴보기 처리(onclick)를 바로 부른다(합성 클릭은 입력 보호에 걸릴 수 있음) */
  say(L0.map(function(x){return x.slice()}),function(){render();setTimeout(function(){var nb=document.querySelector('#bigscene [data-'+(b.dataset.spot?'spot':'obs')+'="'+id+'"]');if(nb&&typeof nb.onclick==="function")nb.onclick.call(nb,{target:nb,stopPropagation:function(){},preventDefault:function(){}});else if(nb)nb.click()},60)})},true);
 function lockPad(){var K=EP.LOCK;
  /* 가로 화면(최소 640x360)에서 스크롤 없이 모든 버튼이 보이게: 숫자 줄 + 버튼 한 줄 */
  var h='<h3 style="margin:0 0 4px">'+K.title+' · '+K.sub+'</h3><p class="soft" style="margin:0 0 6px">'+K.clue+'</p><div id="innpad" style="display:flex;gap:8px;justify-content:center;margin:4px 0 8px">'
   +[0,1,2,3].map(function(i){return '<button type="button" class="btn ghost" data-d="'+i+'" style="min-width:48px;min-height:48px;padding:0;font-size:24px">0</button>'}).join("")+'</div>'
   +'<div id="innbtns" style="display:flex;gap:6px"><button class="btn ghost" id="innhint" style="flex:1;min-height:44px;margin:0">힌트</button><button class="btn ghost" id="innclose" style="flex:1;min-height:44px;margin:0">그만두기</button><button class="btn red" id="innopen" style="flex:1.4;min-height:44px;margin:0">열어 보기</button></div><p id="innmsg" class="soft" style="min-height:18px;margin:6px 0 0;text-align:center"></p>';
  h='<style>#innpad .btn{width:52px!important;height:48px!important;min-height:0!important;padding:0!important;line-height:1!important}#innbtns .btn{height:46px!important;min-height:0!important;padding:0 8px!important;white-space:nowrap!important;line-height:1!important;display:flex!important;align-items:center;justify-content:center}</style>'+h;
  modal(h,function(){var v=[0,0,0,0];document.querySelectorAll("#innpad [data-d]").forEach(function(b){b.onclick=function(){var i=+b.dataset.d;v[i]=(v[i]+1)%10;b.textContent=v[i];try{SFX.tap()}catch(x){}}});
   document.getElementById("innclose").onclick=function(){closeModal();render()};
   /* [선택 힌트] 입력에서 막혀 힌트를 요청한 경우에만 다람이 숫자를 읽는다 */
   document.getElementById("innhint").onclick=function(){try{SFX.tap()}catch(x){}setb("inn_lockhint");var m=document.getElementById("innmsg");if(m)m.textContent=(S.players&&S.players[1]||"다람")+": "+K.hint[1]};
   document.getElementById("innopen").onclick=function(){if(v.join("")===K.code){closeModal();try{SFX.found()}catch(x){}setb("inn_lock");say(K.open.map(function(x){return x.slice()}),function(){render()})}
    else{try{SFX.huh()}catch(x){}var m=document.getElementById("innmsg");if(m)m.textContent=K.wrong}}})}

 window.__innGrant=function(id){if(cur()&&G.found.indexOf(id)<0){G.found.push(id);try{saveProg()}catch(e){}}};
 /* 회의 준비 판정: 회의 중(M2)에 받는 증거는 빼고 본다 */
 try{var _gap=window.__rtGap;if(typeof _gap==="function")window.__rtGap=function(c){var r=_gap.apply(this,arguments);if(c&&c.id==="inn")r=r.filter(function(id){return (D.lateGrant||[]).indexOf(id)<0});return r}}catch(e){MISS.push("rtGap")}
 /* 지목은 유죄 확정이 아니므로 투표 연출 문구를 바꾼다 */
 try{var _fl=flash;flash=function(text){if(cur()&&text==="범인은 너다!"){arguments[0]="지목!"}return _fl.apply(this,arguments)}}catch(e){MISS.push("flash")}

 /* ---- 프롤로그 P1~P11 ---- */
 function runPro(i){var c=cur();if(!c)return;if(i>=EP.PRO.length){setb("inn_pro");G.beats.inn_bg=null;G.loc=LI.bed13;G.tab="scene";
   G.notice={title:EP.GOAL.title,text:EP.GOAL.text+" "+EP.TUT.spot+" "+EP.TUT.talk};render();return}
  G.beats.inn_pi=i;var s=EP.PRO[i];G.beats.inn_bg=s.bg||null;G.loc=LI[s.loc];G.tab="scene";render();
  var go=function(){play(s.items,function(){if(s.after==="title"){(window.banner?banner(EP.title,EP.chapter):Promise.resolve()).then(function(){runPro(i+1)})}else runPro(i+1)})};
  try{banner(s.title,s.sub).then(go)}catch(e){go()}}
 /* ---- 후일담 E1~E4 ---- */
 function runEnd(i){var c=cur();if(!c)return;if(i>=EP.END.length){setb("inn_end");G.loc=LI.hall;G.tab="scene";
   var fin=function(){G.notice=EP.THE_END.notice;try{saveProg()}catch(e){}render()};
   try{banner(EP.THE_END.banner[0],EP.THE_END.banner[1]).then(fin)}catch(e){fin()}return}
  G.beats.inn_ei=i;var s=EP.END[i];G.beats.inn_bg=s.bg||null;G.loc=LI[s.loc];G.tab="scene";render();
  var go=function(){play(s.items,function(){runEnd(i+1)})};
  try{banner(s.title,s.sub).then(go)}catch(e){go()}}
 window.__innRunEnd=runEnd;

 /* ---- 최종 대결 열기 ---- */
 function openFinal(){var c=cur();if(!c)return;G.hp=EP.FINAL_HP||c.lives||5;try{window.__rtgReset&&window.__rtgReset()}catch(e){}
  try{goTab("final")}catch(e){G.tab="final";render()}
  setTimeout(function(){if(cur()&&window.__rtOpen)window.__rtOpen(c,F)},250)}
 window.__innOpenFinal=openFinal;
 /* ---- 설득력 0칸: 회의는 회의 시작(M0)부터, 최종 대결은 F1부터(모은 증거 유지). M-F는 연결하지 않음(D1 결정 대기) ---- */
 window.__innFail=function(kind){var c=cur();if(!c)return;var r=document.querySelector("body>.rt");if(r)r.remove();window.__inMeeting=false;
  try{window.__rtgReset&&window.__rtgReset()}catch(e){}G.hp=c.lives||5;
  if(kind==="final"){G.notice=EP.FINAL_RETRY;try{saveProg()}catch(e){}openFinal();return}
  /* 회의 설득력 0칸은 M-F(4표 미달·무결론)로 바꾸지 않는다: 회의 시작(M0)으로 재개만 한다 */
  G.debate=null;G.beats.rtTally=null;G.notice=EP.MEET_RETRY;try{saveProg()}catch(e){}
  try{goTab("final")}catch(e){G.tab="final";render()}setTimeout(function(){if(cur()&&window.__rtOpen)window.__rtOpen(c)},250)};

 /* 증거 아이콘 C01~C11: 72px 도트 원본(art/evidence/inn/), 흐리게 확대하지 않음. C12·C13은 아직 그림 없음 */
 var ICO={C01:1,C02:1,C03:1,C04:1,C05:1,C06:1,C07:1,C08:1,C09:1,C10:1,C11:1};
 try{var _ei=evIcon;evIcon=function(id){if(ICO[id]&&cur())return '<svg class="evic ev72" viewBox="0 0 72 72" aria-hidden="true"><image href="art/evidence/inn/'+id+'.png" x="0" y="0" width="72" height="72" image-rendering="pixelated" style="image-rendering:pixelated"/></svg>';return _ei.apply(this,arguments)}}catch(e){MISS.push("evIcon")}
 /* 기존 자동 대결(모든 거짓말을 깬 사건에서 옛 대결로 보냄)은 이 사건에서 쓰지 않는다(최종 대결은 위의 F1~F4) */
 try{var _tf=window.__toFight;if(typeof _tf==="function")window.__toFight=function(c){if(c&&c.id==="inn")return;return _tf.apply(this,arguments)}}catch(e){MISS.push("toFight")}
 window.__innStart=function(){var c=cur();if(!c)return;G.beats=G.beats||{};G.beats.toFight=1;try{S.players=["아빠","다람"];persist()}catch(e){}
  if(!bt("inn_pro")){runPro(G.beats.inn_pi|0);return}
  if(bt("inn_final")&&!bt("inn_end")){runEnd(G.beats.inn_ei|0);return}
  if(bt("inn_meet")&&!bt("inn_final")){openFinal();return}};
 if(MISS.length)try{console.warn("inn miss",MISS)}catch(e){}
})();
