 /* ==== 1장 조작 화면 정리(2026-10-09 2차 피드백) ====
    1) 장소 이동: '더보기' 안에 숨기지 않고 오른쪽 위 주 버튼으로. 누르면 갈 수 있는 방 목록이 바로 열리고, 방을 누르면 이동(2번 누름).
       전체 지도는 목록 아래 '전체 지도'로 그대로 열 수 있다.
    2) 질문 목록: 넓은 2열 → 오른쪽 위 여백의 세로 목록(얼굴을 가리지 않음). 새 질문 표시·읽음 체크·누르는 순간의 선택 테두리.
       답변 중에는 목록을 접고(엔진 dl-on) 대사창 하나만, 답변 뒤 같은 화면·같은 읽음 상태로 돌아온다.
    3) 좌우 보기(식당 파노라마): 화면 가장자리의 넓은 세로 띠, 방향 글자, 끝에 닿으면 '끝'으로 흐리게.
       한 화면짜리 장소(접수대·2층 복도·도토의 방)는 배경 경계 밖으로 밀리지 않게 가운데에 고정하고 좌우 단추를 없앤다.
    4) 조사 화면 빈 탭: 보이는 물건마다 짧은 관찰(아빠 속마음), 빈 곳은 짧은 기본 반응. 새 증거·사건·설정은 만들지 않는다.
       증거 지점·인물 단추는 엔진 처리 그대로이고, 그 밖의 장면 탭만 여기서 처리한다(누름·뗌 기준이라 click 누락에도 반응).
    5) 장소 인물 키: 같은 바닥 기준으로 인물마다 다른 키(검토판 02의 차등 키 비율, 할머니 현재 크기 기준). 밤이는 복도 문 앞 바닥에.
    6) 도토: 사용자가 고른 v4(안경·학구파 복장·책과 펜·비율 그대로, 같은 182 캔버스로 줄임). 기존 도토 도트 3장 자리에 쓴다. */
 (function(){
  var B=document.body;
  function inn(){try{return S.screen==="case"&&G&&CASES[G.ci]&&CASES[G.ci].id==="inn"}catch(e){return false}}
  function dl(){try{return typeof DL!=="undefined"&&!!DL}catch(e){return false}}
  function loc(){try{return CASES[G.ci].locations[G.loc]}catch(e){return null}}

  /* ---------- 6) 도토 v4 ---------- */
  var DOTO="art/ch1/cast/doto-v4-182.png";
  function dotoSwap(){try{document.querySelectorAll('img[src^="art/body/doto-"],image[href^="art/body/doto-"]').forEach(function(e){var a=e.tagName.toLowerCase()==="img"?"src":"href";if(/^art\/body\/doto-[0-2]\.png/.test(String(e.getAttribute(a)||"")))e.setAttribute(a,DOTO)})}catch(e){}}

  /* ---------- 5) 장소 인물 차등 키 ---------- */
  /* 검토판 02의 보이는 키(px) ÷ 할머니 키 → 지금 엔진이 모두 같은 캔버스 높이(66u)로 그리는 것을 인물별로 줄이거나 늘린다(각 그림의 투명 여백 비율 보정 포함) */
  var HK={innma:1,seryeon:1.309,nabi:.945,geokkuri:.764,karo:1.091,det1:.764,wanggu:.931,doto:.711,buri:.896};
  function npcScale(){try{if(!inn())return;document.querySelectorAll("#bigscene .npc.f210").forEach(function(n){var k=n.dataset.npc,f=HK[k];if(!f||f===1)return;var key=n.dataset.f210+"|"+f;if(n.dataset.h9===key)return;
    ["--ih","--iw","--vh","--fw","--fh"].forEach(function(v){var x=parseFloat(n.style.getPropertyValue(v));if(isFinite(x))n.style.setProperty(v,(x*f)+"px")});n.dataset.h9=key})}catch(e){}}

  /* ---------- 3) 한 화면 장소는 가운데 고정 ---------- */
  function lockScroll(){try{if(!inn()||G.tab!=="scene")return;var st=document.querySelector("#app .stage");if(!st)return;var world=st.classList.contains("inn-world-stage");B.classList.toggle("inn-pan9",world);
    if(world)return;var fx=document.getElementById("fsscroll");if(!fx)return;var m=fx.scrollWidth-fx.clientWidth;fx.style.setProperty("overflow-x","hidden","important");var c=Math.max(0,Math.round(m/2));if(Math.abs(fx.scrollLeft-c)>1)fx.scrollLeft=c}catch(e){}}

  /* ---------- 1) 장소 이동 목록 ---------- */
  var SHORT={bed13:"창고 · 열세 번째 침대",dining:"식당",kitchen:"부엌",hall:"2층 복도",dotoroom:"도토의 방",front:"접수대"};
  var MV=null,pass=false;
  function mvClose(){if(MV){MV.remove();MV=null}B.classList.remove("innmv-on")}
  function mvOpen(btn){mvClose();var c=CASES[G.ci],h='<div class="hd"><b>장소 이동</b><button type="button" data-x="1" aria-label="닫기">×</button></div><div class="ls">';
   c.locations.forEach(function(l,i){var open=true;try{open=locOpen(c,i)}catch(e){}if(!open)return;var here=i===G.loc;
    h+='<button type="button" data-i="'+i+'"'+(here?' disabled aria-current="true"':'')+'><span>'+(SHORT[l.id]||l.name)+'</span>'+(here?'<small>지금 여기</small>':'<i aria-hidden="true">›</i>')+'</button>'});
   h+='</div><button type="button" class="wm" data-map="1">전체 지도</button>';
   MV=document.createElement("div");MV.id="innmove";MV.setAttribute("role","dialog");MV.setAttribute("aria-label","장소 이동");MV.innerHTML=h;B.appendChild(MV);B.classList.add("innmv-on");
   MV.addEventListener("click",function(e){var t=e.target.closest("button");if(!t)return;e.preventDefault();e.stopPropagation();
    if(t.dataset.x){try{SFX.tap()}catch(x){}mvClose();return}
    if(t.dataset.map){mvClose();pass=true;try{btn.click()}finally{pass=false}return}
    if(t.dataset.i!=null&&!t.disabled){var i=+t.dataset.i;mvClose();try{SFX.select()}catch(x){}
     try{if(G.tab!=="scene"){G.tab="scene";render()}}catch(x){}
     try{moveTo(CASES[G.ci],i)}catch(x){}}})}
  document.addEventListener("click",function(e){if(pass||!inn())return;var b=e.target.closest&&e.target.closest('#w209rail .g>[data-w="move"]');if(!b)return;
   e.preventDefault();e.stopImmediatePropagation();if(dl())return;try{SFX.tap()}catch(x){}if(MV)mvClose();else mvOpen(b)},true);
  document.addEventListener("pointerdown",function(e){if(MV&&!MV.contains(e.target)&&!(e.target.closest&&e.target.closest('#w209rail [data-w="move"]')))mvClose()},true);
  document.addEventListener("keydown",function(e){if(MV&&e.key==="Escape")mvClose()});

  /* ---------- 4) 장면 관찰 ---------- */
  /* 좌표는 각 배경 원본 픽셀(장면 svg의 viewBox와 같은 좌표). 작은 것부터 먼저 맞는다 */
  var LAMP="(등불이 켜져 있다. 수상한 점은 없다.)";
  var OBS={
   dining:[[1735,195,150,315,"(부엌으로 이어지는 문이다.)"],[100,195,215,320,"(접수대 쪽으로 이어지는 문이다.)"],[345,200,75,115,LAMP],[1295,205,75,115,LAMP],[1035,70,70,160,LAMP],[1505,75,70,160,LAMP],
    [480,185,320,200,"(창 너머가 하얗다. 밤새 눈이 왔다.)"],[415,380,345,150,"(창가의 작은 탁자다. 지금은 비어 있다.)"],[1030,495,760,115,"(긴 의자다. 별다른 건 없다.)"],[840,345,890,175,"(여럿이 둘러앉는 긴 식탁이다.)"]],
   kitchen:[[815,100,160,100,"(찬장 위 찻주전자다.)"],[945,335,110,85,"(반죽 그릇이 놓여 있다.)"],[295,200,70,130,LAMP],[1575,210,120,100,"(선반 위 단지들이다.)"],[1180,170,265,225,"(창밖에 눈이 쌓였다.)"],
    [60,85,215,490,"(위층으로 이어지는 뒤 계단이다.)"],[400,195,250,370,"(식당으로 이어지는 문이다.)"],[1580,330,194,310,"(무쇠 화덕이다.)"],[720,170,340,420,"(그릇 찬장이다.)"],[1005,440,555,260,"(부엌 식탁이다.)"]],
   bed13:[[535,65,250,235,"(작은 창이다. 밖에 눈이 보인다.)"],[185,385,295,285,"(구석에 쌓인 나무 상자다.)"],[700,175,780,510,"(열세 번째 침대다.)"]],
   hall:[[1395,180,100,100,"(복도 벽시계다.)"],[875,165,115,190,"(산을 그린 액자다.)"],[450,295,90,90,"(산을 그린 액자다.)"],[340,240,65,110,LAMP],[545,375,95,150,"(화분이다.)"],
    [1105,85,230,710,"(문틈으로 차가운 빛이 새어 나온다.)"],[690,195,125,380,"(손님방 문이다.)"],[0,380,410,280,"(계단참 난간이다. 아래층이 내려다보인다.)"],[425,525,470,220,"(복도에 깔린 긴 깔개다.)"]],
   front:[[850,360,195,55,"(숙박부가 펼쳐져 있다.)"],[1265,325,120,80,"(큰 무쇠 냄비다.)"],[585,210,80,120,LAMP],[1365,210,70,120,LAMP],[990,185,320,145,"(찬장 문은 닫혀 있다.)"],[765,175,215,135,"(그릇과 단지가 놓인 선반이다.)"],[610,395,820,180,"(접수대 카운터다.)"]]};
  var EMPTY9=["(여긴 특별한 게 없다.)","(눈에 띄는 건 없다.)","(다른 곳을 살펴보자.)"],ei=0;
  var OB=null,obT=0;
  function obHide(){clearTimeout(obT);if(OB){OB.remove();OB=null}}
  function obShow(t){obHide();OB=document.createElement("div");OB.className="innobs";OB.setAttribute("role","status");OB.innerHTML='<span class="nm">아빠</span><p></p>';OB.querySelector("p").textContent=t;
   var born=performance.now();OB.addEventListener("click",function(e){e.stopPropagation();if(performance.now()-born>450)obHide()});   /* 띄운 그 탭의 click이 말풍선 위에 떨어져 바로 닫히던 문제 */B.appendChild(OB);obT=setTimeout(obHide,Math.max(2200,900+t.length*90))}
  function worldPt(sc,x,y){var sv=sc.querySelector("svg[data-inn-world]")||sc.querySelector("svg[data-bg]")||sc.querySelector("svg");if(!sv||!sv.getScreenCTM)return null;try{var p=sv.createSVGPoint();p.x=x;p.y=y;var m=sv.getScreenCTM();if(!m)return null;var q=p.matrixTransform(m.inverse());return {x:q.x,y:q.y}}catch(e){return null}}
  var SKIP=".hot,.npc,button,[data-spot],[data-obs],[data-loc],.lens,.flavb,.innobs,a,input";
  function tappable(t){if(!inn()||G.tab!=="scene"||dl())return false;if(!t||!t.closest)return false;var sc=t.closest("#bigscene");if(!sc)return false;if(t.closest(SKIP))return false;
   if(document.querySelector("#ov .modal,#mveil .modal,#innins,#wmap,.crec2,#innmove,body>.rt"))return false;return sc}
  var down=null;
  document.addEventListener("pointerdown",function(e){var sc=tappable(e.target);down=sc?{x:e.clientX,y:e.clientY,t:performance.now(),sc:sc}:null},true);
  document.addEventListener("pointerup",function(e){var d=down;down=null;if(!d)return;if(Math.abs(e.clientX-d.x)>12||Math.abs(e.clientY-d.y)>12||performance.now()-d.t>700)return;if(!tappable(e.target)&&!d.sc.contains(e.target))return;
   var l=loc(),list=l&&OBS[l.id],p=worldPt(d.sc,e.clientX,e.clientY),hit=null;
   if(list&&p)for(var i=0;i<list.length;i++){var r=list[i];if(p.x>=r[0]&&p.x<=r[0]+r[2]&&p.y>=r[1]&&p.y<=r[1]+r[3]){hit=r[4];break}}
   try{SFX.select()}catch(x){}obShow(hit||EMPTY9[(ei++)%EMPTY9.length]);window.__innObsLast=hit||"(빈 곳)"},true);
  /* 엔진의 빈 탭 말풍선(EMPTY·FLAV)은 1장 장면에선 이 관찰로 대신한다. 증거 지점·인물 단추는 막지 않는다 */
  document.addEventListener("click",function(e){if(tappable(e.target))e.stopPropagation()},true);

  /* ---------- 2) 질문 목록: 누르는 순간 선택 테두리 ---------- */
  document.addEventListener("pointerdown",function(e){var t=e.target.closest&&e.target.closest(".fstalk .topic");if(!t||!inn())return;document.querySelectorAll(".fstalk .topic.sel9").forEach(function(x){x.classList.remove("sel9")});t.classList.add("sel9")},true);

  /* ---------- 세련 앉은 그림 · 질문 화면 상반신 구도 ---------- */
  var SER_SCENE="art/ch1/cast/seryeon-seated-paperwork-v2-scene192.png",SER_TALK="art/ch1/cast/seryeon-seated-paperwork-v2-talk.png";
  function seated(){try{document.querySelectorAll('#bigscene .npc[data-npc="seryeon"] .npcclip img').forEach(function(i){if(i.getAttribute("src")!==SER_SCENE)i.setAttribute("src",SER_SCENE)})}catch(e){}}
  function talkFrame(){try{if(!window.__innFrame)return;var W=innerWidth,H=innerHeight;document.querySelectorAll(".fstalk .tstage .tfig img").forEach(function(i){var k=i.dataset.k;if(!k)return;
    if(k==="seryeon"&&i.getAttribute("src")!==SER_TALK)i.setAttribute("src",SER_TALK);if(k==="doto"&&/^art\/body\/doto-/.test(i.getAttribute("src")||""))i.setAttribute("src",DOTO);
    var F=window.__innFrame(k,i.getAttribute("src")),f=i.parentElement,key=[W,H,i.getAttribute("src")].join("|");if(i.dataset.fr9===key)return;i.dataset.fr9=key;
    ["top:0","height:100vh","left:0","right:0","width:auto","transform:none"].forEach(function(d){var q=d.split(":");f.style.setProperty(q[0],q[1],"important")});
    [["position","absolute"],["left",F.left+"px"],["top",F.top+"px"],["width",F.w+"px"],["height",F.h+"px"],["transform","none"],["max-width","none"],["max-height","none"]].forEach(function(d){i.style.setProperty(d[0],d[1],"important")})})}catch(e){}}

  /* ---------- 그림 미리 풀어 두기 ----------
     장면을 다시 그릴 때 새로 만든 그림이 아직 디코드되지 않아 한두 프레임 비거나 이전 화면이 남아 보이는 일을 줄인다(iPhone 전환 보고 대응, 데스크톱에선 재현 안 됨) */
  var PRE=["ch1/cast/innma-neutral-v5","ch1/cast/innma-concerned-v5","ch1/cast/innma-bright-smile-v6","ch1/cast/seryeon-seated-paperwork-v2-talk","ch1/cast/seryeon-seated-paperwork-v2-scene192",
   "ch1/cast/nabi-front","ch1/cast/bami-front","ch1/cast/bami-shock","ch1/cast/karo-front","ch1/cast/daram-front","ch1/cast/doto-v4-182","body/wanggu-0","body/wanggu-1","body/wanggu-2","body/buri-0","body/buri-1","body/buri-2",
   "ch1/bg/BG_corridor_2f_pixel_v1","ch1/bg/BG01_reception_panorama","ch1/locations/BG02_dining_panorama","ch1/locations/BG03_kitchen_base","ch1/locations/BG04_I1_box_free","ch1/locations/BG04_I7_box_free"],preDone=false,KEEP=[];
  function preload(){if(preDone)return;preDone=true;PRE.forEach(function(f,i){setTimeout(function(){try{var im=new Image();im.src="art/"+f+".png";KEEP.push(im);if(im.decode)im.decode().catch(function(){})}catch(e){}},i*40)})}

  /* ---------- 갱신 ---------- */
  var q=0;function tick(){q=0;if(!inn()){B.classList.remove("inn-pan9");mvClose();return}preload();dotoSwap();seated();talkFrame();npcScale();lockScroll();
   if(MV&&(dl()||G.tab==="move"))mvClose();if(OB&&(dl()||G.tab!=="scene"))obHide()}
  try{new MutationObserver(function(){if(!q)q=requestAnimationFrame(tick)}).observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
  window.addEventListener("resize",function(){if(!q)q=requestAnimationFrame(tick)});setInterval(tick,400);
  /* 회전·주소창 변화: iOS는 회전 직후 innerWidth/innerHeight가 한동안 이전 값으로 남는다. 늦게 바뀐 크기로 다시 그리도록 resize를 몇 번 더 보낸다
     (지도·장면 배율·대화 그림이 회전 전 크기로 굳는 것 방지). 실제 크기가 바뀐 때만 보낸다 */
  var lastWH=innerWidth+"x"+innerHeight,fwd=false;function reflow(){var wh=innerWidth+"x"+innerHeight;if(wh===lastWH)return;lastWH=wh;fwd=true;try{dispatchEvent(new Event("resize"))}finally{fwd=false}}
  function later(){[80,250,600,1200].forEach(function(t){setTimeout(reflow,t)})}
  window.addEventListener("orientationchange",later);window.addEventListener("resize",function(){if(!fwd){lastWH=innerWidth+"x"+innerHeight;later()}});
  try{if(window.visualViewport)visualViewport.addEventListener("resize",later)}catch(e){}

  var css=document.createElement("style");css.id="inn-ui9-css";css.textContent=[
   /* 대사창: 두 줄 자리를 늘 확보(한 줄 쪽·두 줄 쪽에서 창 높이가 출렁이지 않게). 글자 크기는 그대로 */
   "html body.w209.inn1 #dlgveil #vnbox #dtxt{min-height:3em!important}",
   /* 질문 목록: 오른쪽 위 여백의 세로 목록 */
   "html body.w209.inn1 .fstalk .tpanel{left:auto!important;right:12px!important;top:60px!important;bottom:auto!important;transform:none!important;width:min(260px,36vw)!important;max-height:calc(100% - 76px)!important;padding:6px!important;background:rgba(14,18,38,.58)!important;border-radius:10px!important}",
   "html body.w209.inn1 .fstalk .tpanel .topics{grid-template-columns:1fr!important;gap:5px!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic{position:relative!important;min-height:40px!important;padding:6px 10px 6px 30px!important;text-align:left!important;border-width:1.5px!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic .tn{position:absolute!important;left:10px!important;top:50%!important;transform:translateY(-50%)!important;margin:0!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic.done{background:rgba(226,214,188,.92)!important;color:#5A4A36!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic.done::before{content:'✓';position:absolute;left:9px;top:50%;transform:translateY(-50%);font-size:15px;color:#3D7A4A;font-weight:700}",
   "html body.w209.inn1 .fstalk .tpanel .topic.done::after{display:none!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic.done .tn{display:none!important}",
   "html body.w209.inn1 .fstalk .tpanel .topic:focus-visible,html body.w209.inn1 .fstalk .tpanel .topic.sel9{outline:2px solid #FFD84D!important;outline-offset:0!important;border-color:#B8860B!important}",
   /* 장소 이동: 주 버튼(조사 · 이동 · 증거 · 기록 · 더보기) */
   "html body.w209.inn1 #w209rail .g>[data-w=\"move\"]{display:flex!important}",
   "html body.w209.inn1 #w209rail .g>[data-w=\"scene\"]{order:1}html body.w209.inn1 #w209rail .g>[data-w=\"move\"]{order:2}html body.w209.inn1 #w209rail .g>[data-w=\"ev\"]{order:3}html body.w209.inn1 #w209rail .g>[data-w=\"rec\"]{order:4}html body.w209.inn1 #w209rail .g>[data-more]{order:9}",
   "html body.w209.inn1 #w209more [data-w=\"move\"]{display:none!important}",
   "#innmove{position:fixed;z-index:60;top:58px;right:12px;width:min(340px,calc(100vw - 24px));max-height:calc(100vh - 70px);overflow-y:auto;box-sizing:border-box;padding:8px;border-radius:12px;background:#151B3A;border:2px solid #C9A96A;box-shadow:0 8px 20px rgba(0,0,0,.45);color:#FFF6E0;font:var(--t-ui,15px)/1.3 var(--display,Galmuri11,sans-serif)}",
   "#innmove .hd{display:flex;align-items:center;justify-content:space-between;margin:0 0 6px 4px}#innmove .hd b{font-weight:400;color:#FFD84D}#innmove .hd button{width:36px;height:32px;border:0;background:none;color:#FFF6E0;font-size:20px}",
   "#innmove .ls{display:grid;grid-template-columns:1fr 1fr;gap:5px}",   /* 640×360에서도 여섯 방이 스크롤 없이 한 화면에 */
   "#innmove .ls button{display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:40px;padding:6px 12px;border-radius:9px;border:1.5px solid #C9A96A;background:rgba(255,248,232,.95);color:#2A1F16;font:inherit;text-align:left}",
   "#innmove .ls button i{font-style:normal;font-size:18px;color:#8A6A3A}#innmove .ls button small{font-size:var(--t-cap,12px);color:#5E5638}",
   "#innmove .ls button[disabled]{background:#3D5E45;color:#FFF6E0;border-color:#3D5E45;opacity:1}#innmove .ls button[disabled] small{color:#DCEBD8}",
   "#innmove .wm{display:block;width:100%;margin-top:8px;min-height:36px;border-radius:9px;border:1px solid #4A5590;background:#2E3766;color:#FFF6E0;font:inherit}",
   /* 좌우 보기: 식당 파노라마에서만. 화면 가장자리 세로 띠, 끝에서는 흐리게 '끝' */
   "html body.w209.inn1 .stage:not(.inn-world-stage) .fsa,html body.w209.inn1 .stage:not(.inn-world-stage) .fsbar{display:none!important;pointer-events:none!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa{top:24%!important;bottom:auto!important;height:46%!important;width:48px!important;min-height:0!important;margin:0!important;padding:0!important;border-radius:0!important;border:0!important;box-shadow:none!important;display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;gap:4px!important;color:#FFF6E0!important;font-size:20px!important;background:linear-gradient(90deg,rgba(14,18,38,.62),rgba(14,18,38,0))!important;transform:none!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa.l{left:0!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa.r{right:0!important;left:auto!important;background:linear-gradient(270deg,rgba(14,18,38,.62),rgba(14,18,38,0))!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa::after{content:'왼쪽';display:block!important;position:static!important;font-size:var(--t-cap,12px)!important;line-height:1.2!important;color:#FFF6E0!important;background:none!important;padding:0!important;border:0!important;transform:none!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa.r::after{content:'오른쪽'}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa[disabled]{opacity:.32!important;background:none!important}",
   "html body.w209.inn1 .stage.inn-world-stage .fsa[disabled]::after{content:'끝'!important}",
   /* 장소 이름표: 그림자 겹침 제거·줄 간격 */
   "html body.w209.inn1 #app .stagebar .scap b{text-shadow:none!important;font-size:14px!important;line-height:1.25!important;display:block!important}",
   "html body.w209.inn1 #app .stagebar .scap small{text-shadow:none!important;line-height:1.25!important;display:block!important;margin-top:1px!important}",
   /* 장면 관찰: 대사창과 같은 가운데 좁은 띠, 아빠 속마음 색 */
   ".innobs{position:fixed;z-index:40;left:50%;bottom:10px;transform:translateX(-50%);width:min(540px,calc(100vw - 32px));box-sizing:border-box;padding:12px 16px 10px;border-radius:12px;background:rgba(14,17,40,.93);border:1.5px solid #3A4480;box-shadow:0 6px 18px rgba(0,0,0,.35);animation:innobs .14s ease-out;cursor:pointer}",
   ".innobs .nm{position:absolute;top:-11px;left:12px;padding:1px 8px;border-radius:6px;background:#2F4E86;color:#FFF6E0;font:var(--t-label,13px)/1.4 var(--display,Galmuri11,sans-serif)}",
   ".innobs p{margin:0;color:#8CC4FF;font:var(--t-story,16px)/1.5 Galmuri11B,Galmuri11,monospace;word-break:keep-all;text-align:left}",
   "@keyframes innobs{from{opacity:0;transform:translate(-50%,6px)}}"
  ].join("\n");document.head.appendChild(css);
  window.__innUI9={obs:function(){return window.__innObsLast||""},HK:HK,OBS:OBS};
 })();
