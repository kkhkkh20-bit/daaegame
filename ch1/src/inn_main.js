/* ===== 다람탐정 1장: 메인 화면 · 설정 · 콜드 오픈 =====
   흐름: 접속 → 메인(이어하기 / 새 게임 / 설정) → 새 게임: 콜드 오픈(그날 새벽) → 전날 오후 마차 → P1
                                         → 이어하기: 콜드 오픈 없이 저장 위치부터
   - 메인은 기존 엔진의 타이틀 대신 보여 준다(엔진 저장·진행 로직은 그대로 사용). 키아트는 메인 3안 중 A안(미리보기, 최종 선택 아님).
   - 설정은 옵션 팩 설계서 기준: 배경 음악·효과음(0~100, 5 단위), 글자 크기(16/18/20px), 대사 속도(45/30/15ms).
     작업 사본에서 조정하고 '저장'을 눌러야 실제 게임에 적용. 저장 키는 이 테스트판 전용(daae-inn1:inn_settings).
   - 콜드 오픈은 인트로 팩 그림·대사만 사용. 클릭/Space로 진행(자동 넘김 없음). 이미 본 경우에만 건너뛰기.
   - 음원 파일이 없어 콜드 오픈 전용 음악·효과음은 아직 없음(기존 합성음만 사용). */
(function(){
 var MISS=window.__INNMAIN_MISS=[];var EP=window.EP1INN;if(!EP||!window.__EP1INN)return;
 var B=document.body;
 function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}

 /* ---------- 설정 저장 ---------- */
 var SKEY="inn_settings",DEF={schemaVersion:1,musicVolume:70,sfxVolume:80,fontSize:"normal",dialogueSpeed:"normal",coldSeen:false};
 function vol(v,d){v=Math.round(+v/5)*5;return isFinite(v)?Math.max(0,Math.min(100,v)):d}
 function norm(o){o=o||{};return {schemaVersion:1,musicVolume:o.musicVolume==null?DEF.musicVolume:vol(o.musicVolume,DEF.musicVolume),sfxVolume:o.sfxVolume==null?DEF.sfxVolume:vol(o.sfxVolume,DEF.sfxVolume),
  fontSize:["small","normal","large"].indexOf(o.fontSize)>=0?o.fontSize:DEF.fontSize,dialogueSpeed:["slow","normal","fast"].indexOf(o.dialogueSpeed)>=0?o.dialogueSpeed:DEF.dialogueSpeed,coldSeen:!!o.coldSeen}}
 function loadSet(){var o=null;try{o=JSON.parse(localStorage.getItem(SKEY)||"null")}catch(e){o=null}return norm(o)}
 function saveSet(o){var s=JSON.stringify(norm(o));localStorage.setItem(SKEY,s);if(localStorage.getItem(SKEY)!==s)throw new Error("verify")}
 var SET=loadSet();window.__innSettings=function(){return JSON.parse(JSON.stringify(SET))};
 var MS={slow:45,normal:30,fast:15};
 function gains(o){try{if(typeof BGMG!=="undefined"&&BGMG)BGMG.gain.value=.1*o.musicVolume/70;if(typeof SFXG!=="undefined"&&SFXG)SFXG.gain.value=.42*o.sfxVolume/80}catch(e){}}
 function apply(o){["small","normal","large"].forEach(function(k){B.classList.toggle("inn-fs-"+k,o.fontSize===k)});
  try{TSPD.s=MS.slow;TSPD.n=MS.normal;TSPD.f=MS.fast;S.tspeed={slow:"s",normal:"n",fast:"f"}[o.dialogueSpeed]}catch(e){MISS.push("tspd")}
  gains(o)}
 try{var _ac=ac;ac=function(){var a=_ac.apply(this,arguments);gains(SET);return a}}catch(e){MISS.push("ac")}
 apply(SET);

 /* ---------- 공통 스타일 ---------- */
 var css=document.createElement("style");css.id="inn-main-css";css.textContent=[
  "html body.w209.inn-fs-small #vnbox #dtxt,html body.w209.inn-fs-small #vnbox .txt{font-size:16px!important}",
  "html body.w209.inn-fs-normal #vnbox #dtxt,html body.w209.inn-fs-normal #vnbox .txt{font-size:18px!important}",
  "html body.w209.inn-fs-large #vnbox #dtxt,html body.w209.inn-fs-large #vnbox .txt{font-size:20px!important}",
  /* 메인 */
  "#innmain{position:fixed;inset:0;z-index:200;background:#0c1018;overflow:hidden;font-family:var(--display,sans-serif);color:#F4EDD8}",
  "#innmain .kv{position:absolute;inset:0;background:#0c1018 center/cover no-repeat;image-rendering:pixelated}",
  "#innmain .tt{position:absolute;left:50%;top:max(16px,env(safe-area-inset-top));transform:translateX(-50%);text-align:center;pointer-events:none}",
  "#innmain .tt small{display:block;font:600 9px/1.2 sans-serif;letter-spacing:.18em;color:#D8CDB0;opacity:.85}",
  "#innmain .tt h1{margin:4px 0 0;font:700 34px/1.15 'Noto Serif KR','Nanum Myeongjo',serif;color:#FFF6E4;text-shadow:0 2px 0 rgba(0,0,0,.55),0 0 12px rgba(0,0,0,.4);letter-spacing:.02em}",
  "#innmain .tt i{display:block;width:30px;height:1px;margin:8px auto 0;background:#DDB877}",
  "#innmain .menu{position:absolute;left:50%;bottom:max(16px,env(safe-area-inset-bottom));transform:translateX(-50%);display:flex;gap:12px;align-items:center}",
  "#innmain .menu button{position:relative;min-width:88px;height:48px;padding:0 14px 0 22px;border:0;background:none;color:#F4EDD8;font:400 17px/1 var(--display,sans-serif);text-shadow:0 2px 0 rgba(0,0,0,.7);cursor:pointer;display:flex;align-items:center;gap:6px;white-space:nowrap}",
  "#innmain .menu button:before{content:'';position:absolute;left:8px;top:50%;width:7px;height:7px;margin-top:-4px;background:#DDB877;transform:rotate(45deg);opacity:0}",
  "#innmain .menu button.f:before,#innmain .menu button:focus-visible:before{opacity:1}",
  "#innmain .menu button:focus-visible{outline:2px solid #A4E0D4;outline-offset:2px}",
  "#innmain .menu button[disabled]{color:#8E8B80;cursor:default}",
  "#innmain .menu button small{font-size:11px;color:#B8B09A}",
  "#innmain .st{position:absolute;left:50%;bottom:70px;transform:translateX(-50%);font-size:12px;color:#D8CDB0;text-shadow:0 1px 0 #000}",
  "#innmain .pv{position:absolute;right:10px;bottom:6px;font:10px/1 sans-serif;color:#B8B09A;opacity:.7}",
  ".innconf{position:fixed;inset:0;z-index:260;display:flex;align-items:center;justify-content:center;background:rgba(6,10,16,.6)}",
  ".innconf .bx{width:min(418px,calc(100vw - 32px));box-sizing:border-box;padding:18px 22px 16px;background:#101E2A;border:1.5px solid #38515A;color:#F4EDD8;font-family:var(--display,sans-serif)}",
  ".innconf b{display:block;font-size:19px;font-weight:400;margin-bottom:6px}.innconf p{margin:0 0 14px;font-size:14px;color:#B8C8C7;line-height:1.45}",
  ".innconf .rw{display:flex;gap:12px}.innconf button{flex:1;height:46px;border:1.5px solid #38515A;background:#20343D;color:#F4EDD8;font:16px var(--display,sans-serif);cursor:pointer}",
  ".innconf button.pri{background:#DDB877;color:#10212B;border-color:#DDB877}.innconf button:focus-visible{outline:2px solid #A4E0D4;outline-offset:2px}",
  /* 설정 */
  "#innopt{position:fixed;inset:0;z-index:240;color:#F4EDD8;font-family:var(--display,sans-serif)}",
  "#innopt .bg{position:absolute;inset:0;background:#101E2A center/cover no-repeat}#innopt .bg:after{content:'';position:absolute;inset:0;background:rgba(16,30,42,.78)}",
  "#innopt .in{position:absolute;inset:0;padding:max(10px,env(safe-area-inset-top)) max(64px,env(safe-area-inset-right)) max(14px,env(safe-area-inset-bottom)) max(64px,env(safe-area-inset-left));display:flex;flex-direction:column}",
  "@media (max-width:700px){#innopt .in{padding-left:max(32px,env(safe-area-inset-left));padding-right:max(32px,env(safe-area-inset-right))}}",
  "#innopt .hd{display:flex;align-items:center;gap:10px;height:58px;border-bottom:1px solid #38515A}#innopt .hd small{display:block;font:600 8px/1 sans-serif;letter-spacing:.14em;color:#DDB877}",
  "#innopt .hd h2{margin:2px 0 0;font:400 22px/1 var(--display,sans-serif)}#innopt .hd img{width:24px;height:24px;image-rendering:pixelated}",
  "#innopt .x{margin-left:auto;width:48px;height:48px;border:1.5px solid #38515A;background:#20343D;display:flex;align-items:center;justify-content:center;cursor:pointer}#innopt .x img{width:24px;height:24px;image-rendering:pixelated}",
  "#innopt .rows{flex:1;display:flex;flex-direction:column;justify-content:center;gap:4px;min-height:0}",
  "#innopt .row{display:flex;align-items:center;gap:12px;min-height:46px}#innopt .row .lb{width:150px;display:flex;align-items:center;gap:10px;font-size:17px}#innopt .row .lb img{width:24px;height:24px;image-rendering:pixelated}",
  "@media (max-width:700px){#innopt .row .lb{width:118px}}",
  "#innopt input[type=range]{flex:1;height:44px;margin:0;background:none;-webkit-appearance:none;appearance:none;accent-color:#DDB877}",
  "#innopt input[type=range]::-webkit-slider-runnable-track{height:6px;background:linear-gradient(90deg,#DDB877 var(--p),#20343D var(--p));border:1px solid #38515A}",
  "#innopt input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:26px;margin-top:-11px;background:#F6DFAA;border:2px solid #B7965D}",
  "#innopt input[type=range]::-moz-range-track{height:6px;background:#20343D}#innopt input[type=range]::-moz-range-progress{height:6px;background:#DDB877}",
  "#innopt input[type=range]:focus-visible{outline:2px solid #A4E0D4;outline-offset:2px}",
  "#innopt .vv{width:44px;text-align:right;font-size:17px;font-variant-numeric:tabular-nums}",
  "#innopt .grp{flex:1;display:flex;gap:6px}#innopt .grp button{flex:1;height:44px;border:1.5px solid #38515A;background:#20343D;color:#F4EDD8;font:17px var(--display,sans-serif);cursor:pointer}",
  "#innopt .grp button[aria-checked=true]{background:#5B4A2E;border-color:#DDB877;box-shadow:inset 0 -3px 0 #DDB877;font-weight:700}#innopt .grp button:focus-visible{outline:2px solid #A4E0D4;outline-offset:2px}",
  "#innopt .sep{height:1px;background:#38515A;margin:2px 0}",
  "#innopt .ft{display:flex;align-items:flex-end;gap:12px;border-top:1px solid #38515A;padding-top:6px}#innopt .ft .pv{flex:1;min-width:0}#innopt .ft .pv small{display:block;font-size:11px;color:#B8C8C7}",
  "#innopt .ft .pv p{margin:2px 0 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}#innopt .err{font-size:12px;color:#F2A38A;min-height:14px}",
  "#innopt .sv{width:128px;height:46px;border:0;background:#DDB877;color:#10212B;font:700 17px var(--display,sans-serif);cursor:pointer}#innopt .sv:focus-visible{outline:2px solid #A4E0D4;outline-offset:2px}",
  /* 콜드 오픈 */
  "#inncold{position:fixed;inset:0;z-index:220;background:#000;overflow:hidden;cursor:pointer;-webkit-tap-highlight-color:transparent;font-family:var(--display,sans-serif)}",
  "#inncold .cbg{position:absolute;inset:0;background:#000 center/cover no-repeat;image-rendering:pixelated;transition:transform 4s linear,opacity .35s}",
  "#inncold .blk{position:absolute;inset:0;background:#000;opacity:0;transition:opacity .45s;pointer-events:none}#inncold.dark .blk{opacity:1}",
  "#inncold .tag{position:absolute;left:max(18px,env(safe-area-inset-left));top:max(14px,env(safe-area-inset-top));padding:4px 10px;background:rgba(0,0,0,.55);border-left:2px solid #DDB877;color:#F4EDD8;font-size:14px;opacity:0;transition:opacity .4s}#inncold .tag.on{opacity:1}",
  "#inncold .ttl{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;color:#F4EDD8;font:400 24px/1.3 var(--display,sans-serif);opacity:0;transition:opacity .4s}#inncold .ttl.on{opacity:1}",
  "#inncold .box{position:absolute;left:50%;bottom:max(12px,env(safe-area-inset-bottom));transform:translateX(-50%);width:min(680px,calc(100vw - 40px));box-sizing:border-box;padding:12px 18px 14px;background:rgba(12,10,16,.82);border:1px solid rgba(221,184,119,.55);color:#F4EDD8;display:none}",
  "#inncold .box.on{display:block}#inncold .box b{display:inline-block;margin-bottom:4px;padding:1px 8px;background:#5B2E2E;font-weight:400;font-size:13px}#inncold .box p{margin:0;font-size:18px;line-height:1.55;min-height:28px}",
  "html body.inn-fs-small #inncold .box p{font-size:16px}html body.inn-fs-large #inncold .box p{font-size:20px}",
  "#inncold .nx{position:absolute;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));color:#DDB877;font-size:14px;opacity:0;transition:opacity .3s}#inncold .nx.on{opacity:1}",
  "#inncold .sk{position:absolute;right:max(12px,env(safe-area-inset-right));top:max(10px,env(safe-area-inset-top));height:44px;padding:0 14px;border:1px solid rgba(244,237,216,.4);background:rgba(0,0,0,.45);color:#F4EDD8;font:14px var(--display,sans-serif);cursor:pointer}"
 ].join("\n");(document.head||document.documentElement).appendChild(css);

 /* ---------- 확인창 ---------- */
 function confirmBox(title,text,okLabel,cancelLabel,onOk,onCancel,focusCancel){var d=document.createElement("div");d.className="innconf";d.setAttribute("role","dialog");d.setAttribute("aria-modal","true");
  d.innerHTML='<div class="bx"><b>'+esc(title)+'</b><p>'+esc(text)+'</p><div class="rw"><button type="button" data-k="ok">'+esc(okLabel)+'</button><button type="button" class="pri" data-k="no">'+esc(cancelLabel)+'</button></div></div>';
  document.body.appendChild(d);var bn=d.querySelector('[data-k="no"]'),bo=d.querySelector('[data-k="ok"]');(focusCancel===false?bo:bn).focus();
  function close(){d.remove();document.removeEventListener("keydown",kd,true)}
  function kd(e){if(e.key==="Escape"){e.preventDefault();e.stopPropagation();close();onCancel&&onCancel()}else if(e.key==="Tab"){e.preventDefault();(document.activeElement===bn?bo:bn).focus()}}
  document.addEventListener("keydown",kd,true);
  bo.onclick=function(){close();onOk&&onOk()};bn.onclick=function(){close();onCancel&&onCancel()};return d}

 /* ---------- 설정 화면 ---------- */
 var OPT=null;
 function openOptions(back){if(OPT)return;var W0=JSON.parse(JSON.stringify(SET)),W=JSON.parse(JSON.stringify(SET));
  OPT=document.createElement("div");OPT.id="innopt";OPT.setAttribute("role","dialog");OPT.setAttribute("aria-label","설정");
  function grp(id,label,icon,opts,val){return '<div class="row"><span class="lb"><img src="art/ch1/options/'+icon+'-24.png" alt="">'+label+'</span><div class="grp" role="radiogroup" aria-label="'+label+'" data-g="'+id+'">'
   +opts.map(function(o){return '<button type="button" role="radio" data-v="'+o[0]+'" aria-checked="'+(val===o[0])+'" tabindex="'+(val===o[0]?0:-1)+'">'+o[1]+'</button>'}).join("")+'</div></div>'}
  function sld(id,label,icon,v){return '<div class="row"><span class="lb"><img src="art/ch1/options/'+icon+'-24.png" alt="">'+label+'</span><input type="range" min="0" max="100" step="5" value="'+v+'" data-s="'+id+'" aria-label="'+label+'" style="--p:'+v+'%"><span class="vv" data-vv="'+id+'">'+v+'</span></div>'}
  OPT.innerHTML='<div class="bg" style="background-image:url(art/ch1/options/winter-inn-keyart.png)"></div><div class="in"><div class="hd"><img src="art/ch1/options/gear-24.png" alt=""><div><small>DARAM DETECTIVE</small><h2>설정</h2></div><button type="button" class="x" aria-label="설정 닫기"><img src="art/ch1/options/close-24.png" alt=""></button></div>'
   +'<div class="rows">'+sld("musicVolume","배경 음악","music",W.musicVolume)+sld("sfxVolume","효과음","sound",W.sfxVolume)+'<div class="sep"></div>'
   +grp("fontSize","글자 크기","type",[["small","작게"],["normal","보통"],["large","크게"]],W.fontSize)+grp("dialogueSpeed","대사 속도","dialogue",[["slow","느리게"],["normal","보통"],["fast","빠르게"]],W.dialogueSpeed)+'</div>'
   +'<div class="ft"><div class="pv"><small>대사 미리보기</small><p id="innpvt"></p><div class="err" id="innerr" role="alert"></div></div><button type="button" class="sv">저장</button></div></div>';
  document.body.appendChild(OPT);
  var pvT=null,SAMPLE="발자국이 여관으로 이어져 있어.";
  function preview(){var p=document.getElementById("innpvt");if(!p)return;p.style.fontSize={small:"16px",normal:"18px",large:"20px"}[W.fontSize];clearInterval(pvT);var n=0;p.textContent="";
   pvT=setInterval(function(){n++;p.textContent=SAMPLE.slice(0,n);if(n>=SAMPLE.length)clearInterval(pvT)},MS[W.dialogueSpeed])}
  function dirty(){return ["musicVolume","sfxVolume","fontSize","dialogueSpeed"].some(function(k){return W[k]!==W0[k]})}
  OPT.querySelectorAll("input[type=range]").forEach(function(r){var k=r.dataset.s;
   r.addEventListener("input",function(){W[k]=vol(r.value,W[k]);r.style.setProperty("--p",W[k]+"%");OPT.querySelector('[data-vv="'+k+'"]').textContent=W[k];if(k==="musicVolume")gains({musicVolume:W.musicVolume,sfxVolume:SET.sfxVolume})});
   r.addEventListener("change",function(){if(k==="sfxVolume"&&W.sfxVolume>0){try{ac();gains({musicVolume:W.musicVolume,sfxVolume:W.sfxVolume});SFX.select();setTimeout(function(){gains({musicVolume:W.musicVolume,sfxVolume:SET.sfxVolume})},350)}catch(e){}}})});
  OPT.querySelectorAll(".grp").forEach(function(g){var k=g.dataset.g,bs=[].slice.call(g.querySelectorAll("button"));
   function pick(b){bs.forEach(function(x){var on=x===b;x.setAttribute("aria-checked",on);x.tabIndex=on?0:-1});W[k]=b.dataset.v;preview()}
   bs.forEach(function(b,i){b.onclick=function(){pick(b)};b.onkeydown=function(e){if(e.key==="ArrowRight"||e.key==="ArrowLeft"){e.preventDefault();var j=(i+(e.key==="ArrowRight"?1:-1)+bs.length)%bs.length;bs[j].focus();pick(bs[j])}}})});
  function shut(){clearInterval(pvT);gains(SET);OPT.remove();OPT=null;document.removeEventListener("keydown",kd,true);back&&back()}
  function tryClose(){if(!dirty()){shut();return}
   confirmBox("저장하지 않고 나갈까요?","조정한 값은 이전 설정으로 돌아갑니다.","저장 안 함","계속 조정",function(){shut()},function(){var x=OPT&&OPT.querySelector(".x");x&&x.focus()})}
  function kd(e){if(e.key==="Escape"&&!document.querySelector(".innconf")){e.preventDefault();tryClose()}}
  document.addEventListener("keydown",kd,true);
  OPT.querySelector(".x").onclick=tryClose;
  OPT.querySelector(".sv").onclick=function(){var er=document.getElementById("innerr");try{saveSet(W);SET=norm(W);apply(SET);try{persist()}catch(e){}shut()}catch(e){if(er)er.textContent="설정을 저장하지 못했어요. 다시 시도해 주세요."}};
  preview();OPT.querySelector(".x").focus()}
 window.__innOptions=openOptions;
 /* 게임 안 '설정'(더보기)도 같은 설정 화면으로 */
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest('#w209rail [data-w="set"],#w209more [data-w="set"]');if(!b)return;e.preventDefault();e.stopImmediatePropagation();
  try{var r=document.getElementById("w209rail");r&&r.classList.remove("more")}catch(x){}openOptions(function(){})},true);

 /* ---------- 콜드 오픈 ---------- */
 function cold(done){var L=EP.COLD||[],i=-1,typing=null,full="",waitT=null,busy=false,ended=false;
  var el=document.createElement("div");el.id="inncold";el.setAttribute("role","region");el.setAttribute("aria-label","콜드 오픈");
  el.innerHTML='<div class="cbg"></div><div class="blk"></div><div class="tag"></div><div class="ttl"></div><div class="box"><b>'+esc(EP.COLD_SPEAKER||"???")+'</b><p></p></div><div class="nx">▼</div>'+(SET.coldSeen?'<button type="button" class="sk">건너뛰기</button>':'');
  document.body.appendChild(el);var bg=el.querySelector(".cbg"),tag=el.querySelector(".tag"),ttl=el.querySelector(".ttl"),box=el.querySelector(".box"),tx=box.querySelector("p"),nx=el.querySelector(".nx");
  function cam(b,z){bg.style.transition="none";bg.style.backgroundImage="url("+b.img+")";bg.style.transformOrigin=(b.fx*100)+"% "+(b.fy*100)+"%";bg.style.transform="scale("+z+")";void bg.offsetWidth;bg.style.transition=""}
  function type(t){full=t;tx.textContent="";var n=0;clearInterval(typing);typing=setInterval(function(){n++;tx.textContent=full.slice(0,n);if(n>=full.length){clearInterval(typing);typing=null;nx.classList.add("on")}},MS[SET.dialogueSpeed])}
  function show(){var b=L[i];nx.classList.remove("on");box.classList.remove("on");ttl.classList.remove("on");el.classList.remove("dark");clearTimeout(waitT);busy=false;
   cam(b,b.z||1);if(b.push)requestAnimationFrame(function(){bg.style.transform="scale("+((b.z||1)*(1+b.push/100))+")"});if(b.pull)requestAnimationFrame(function(){bg.style.transform="scale("+((b.z||1)/(1+b.pull/100))+")"});
   tag.textContent=b.tag||"";tag.classList.toggle("on",!!b.tag);
   if(b.say){box.classList.add("on");tx.textContent="";if(b.wait){busy=true;waitT=setTimeout(function(){busy=false;type(b.say)},b.wait)}else type(b.say)}
   else if(b.title){busy=true;waitT=setTimeout(function(){el.classList.add("dark");waitT=setTimeout(function(){ttl.textContent=b.title;ttl.classList.add("on");busy=false;nx.classList.add("on")},b.black||450)},700)}
   else waitT=setTimeout(function(){nx.classList.add("on")},900)}
  function next(){if(ended)return;if(typing){clearInterval(typing);typing=null;tx.textContent=full;nx.classList.add("on");return}if(busy)return;i++;if(i>=L.length){end();return}show()}
  function end(){ended=true;clearTimeout(waitT);clearInterval(typing);SET.coldSeen=true;try{saveSet(SET)}catch(e){}document.removeEventListener("keydown",kd,true);
   done&&done();setTimeout(function(){el.style.transition="opacity .35s";el.style.opacity="0";setTimeout(function(){el.remove()},380)},650)}
  function kd(e){if(e.key===" "||e.key==="Enter"){e.preventDefault();next()}}
  document.addEventListener("keydown",kd,true);
  el.addEventListener("click",function(e){var s=e.target.closest&&e.target.closest(".sk");if(s){e.stopPropagation();end();return}next()});
  try{ac()}catch(e){}window.__innColdState=function(){return {i:i,typing:!!typing,busy:busy,ended:ended}};
  next()}
 window.__innCold=cold;

 /* ---------- 메인 화면 ---------- */
 function hasSave(){try{return !!(S.prog&&S.prog.inn)}catch(e){return false}}
 function main(boot){
  var startNew=false;try{startNew=sessionStorage.getItem("inn_newgame")==="1";if(startNew)sessionStorage.removeItem("inn_newgame")}catch(e){}
  if(startNew){cold(boot);return}
  var M=document.createElement("div");M.id="innmain";M.setAttribute("aria-label","다람탐정 메인");
  M.innerHTML='<div class="kv" style="background-image:url('+EP.MAIN.keyart+')"></div><div class="tt"><small>'+esc(EP.MAIN.eyebrow)+'</small><h1>'+esc(EP.MAIN.title)+'</h1><i></i></div>'
   +'<div class="st" id="innst">저장 확인 중</div><div class="menu" role="menu"><button type="button" data-m="cont" disabled>이어하기</button><button type="button" data-m="new" disabled>새 게임</button><button type="button" data-m="set" disabled>설정</button></div><div class="pv">메인 A안 미리보기</div>';
  document.body.appendChild(M);var bs=[].slice.call(M.querySelectorAll(".menu button")),busy=false,st=M.querySelector("#innst");
  var save=hasSave();
  function enable(){bs.forEach(function(b){b.disabled=false});var c=bs[0];if(!save){c.disabled=true;c.innerHTML='이어하기<small>저장 없음</small>'}st.textContent="";focus(save?0:1)}
  function focus(i){bs.forEach(function(b,j){b.classList.toggle("f",j===i)});bs[i].focus()}
  setTimeout(enable,120);
  M.addEventListener("keydown",function(e){if(e.key!=="ArrowRight"&&e.key!=="ArrowLeft")return;e.preventDefault();var en=bs.filter(function(b){return !b.disabled}),cur=en.indexOf(document.activeElement);var j=(cur+(e.key==="ArrowRight"?1:-1)+en.length)%en.length;focus(bs.indexOf(en[j]))});
  bs.forEach(function(b){b.addEventListener("focus",function(){bs.forEach(function(x){x.classList.toggle("f",x===b)})})});
  function go(fn){if(busy)return;busy=true;bs.forEach(function(b){b.disabled=true});try{ac()}catch(e){}fn()}
  bs[0].onclick=function(){if(!save)return;go(function(){st.textContent="불러오는 중";setTimeout(function(){M.remove();boot()},60)})};
  bs[1].onclick=function(){if(busy)return;
   if(!save){go(function(){M.remove();cold(boot)});return}
   confirmBox("처음부터 새로 시작할까요?","지금까지의 1장 진행 기록이 지워져요. 설정은 그대로예요.","새로 시작","취소",function(){go(function(){st.textContent="새 게임 준비 중";
     try{var keep=SET;localStorage.clear();saveSet(keep);sessionStorage.setItem("inn_newgame","1")}catch(e){MISS.push("newgame "+e.message)}location.reload()})},function(){focus(1)})};
  bs[2].onclick=function(){if(busy)return;openOptions(function(){focus(2)})};
 }
 window.__innMain=main;
})();
