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
  /* 식당은 실제 가구 기준(2026-10-09 피드백): 세련은 앉은 그림의 좌석 높이·발바닥을 같은 깊이의 긴 의자(좌석 높이 약 88px, 원본 좌표)에 맞추고, 할머니도 같은 방 배율로 */
  var DINE={innma:1.77,seryeon:2.24};
  function npcScale(){try{if(!inn())return;var lid=(loc()||{}).id;document.querySelectorAll("#bigscene .npc.f210").forEach(function(n){var k=n.dataset.npc,f=(lid==="dining"&&DINE[k])||HK[k];if(!f||f===1)return;var key=n.dataset.f210+"|"+f;if(n.dataset.h9===key)return;
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
     try{moveTo(CASES[G.ci],i)}catch(x){}}})}   /* 대화 화면에서도 곧바로 새 방으로(이전 방이 한 번 더 보이지 않게) */
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
   var hi=-1;if(list&&p)for(var i=0;i<list.length;i++){var r=list[i];if(p.x>=r[0]&&p.x<=r[0]+r[2]&&p.y>=r[1]&&p.y<=r[1]+r[3]){hit=r[4];hi=i;break}}
   if(hi>=0){markSeen(l.id,hi);setTimeout(drawMarks,0)}
   try{SFX.select()}catch(x){}obShow(hit||EMPTY9[(ei++)%EMPTY9.length]);window.__innObsLast=hit||"(빈 곳)"},true);
  /* 엔진의 빈 탭 말풍선(EMPTY·FLAV)은 1장 장면에선 이 관찰로 대신한다. 증거 지점·인물 단추는 막지 않는다 */
  document.addEventListener("click",function(e){if(tappable(e.target))e.stopPropagation()},true);

  /* ---------- 2) 질문 목록: 누르는 순간 선택 테두리 ---------- */
  document.addEventListener("pointerdown",function(e){var t=e.target.closest&&e.target.closest(".fstalk .topic");if(!t||!inn())return;document.querySelectorAll(".fstalk .topic.sel9").forEach(function(x){x.classList.remove("sel9")});t.classList.add("sel9")},true);

  /* ---------- 세련 앉은 그림 · 질문 화면 상반신 구도 ---------- */
  var SER_SCENE="art/ch1/cast/seryeon-seated-paperwork-v2-scene192.png",SER_TALK="art/ch1/cast/seryeon-seated-paperwork-v2-talk.png";
  function seated(){try{document.querySelectorAll('#bigscene .npc[data-npc="seryeon"] .npcclip img').forEach(function(i){if(i.getAttribute("src")!==SER_SCENE)i.setAttribute("src",SER_SCENE)})}catch(e){}}
  function talkFrame(){try{if(!window.__innFrame)return;var W=innerWidth,H=innerHeight;document.querySelectorAll(".fstalk .tstage .tfig img").forEach(function(i){var k=i.dataset.k;if(!k)return;
    var want=(window.__innPose&&window.__innPose(k))||(k==="seryeon"?SER_TALK:null);if(want&&i.getAttribute("src")!==want)i.setAttribute("src",want);if(!want&&k==="doto"&&/^art\/body\/doto-/.test(i.getAttribute("src")||""))i.setAttribute("src",DOTO);
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
  var q=0;function tick(){q=0;if(!inn()){B.classList.remove("inn-pan9");mvClose();return}speaker();preload();dotoSwap();seated();talkFrame();bump();topicSync();npcScale();lockScroll();worldNpc();drawMarks();doneMarks();pplTab();metMark();if(PP&&!document.querySelector(".crec2"))pplClose();
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
   "@keyframes innobs{from{opacity:0;transform:translate(-50%,6px)}}",
   /* 3차: 전환 중 옛 화면 요소 숨김 */
   "html body.w209.inn1 #bigscene .npc:not(.f210){visibility:hidden!important}",
   "html body.w209.inn1 .fsmap,html body.w209.inn1 .placecard{opacity:0!important}",
   "html body.w209.inn1 .placecard{display:none!important}",
   "html body.w209.inn1 .scene.arrive svg,html body.w209.inn1 .scene.arrive img{animation:none!important}",
   "html body.w209.inn1 #bigscene.arrive{animation:innarr9 .3s ease-out}@keyframes innarr9{from{opacity:.55}to{opacity:1}}",
   "html body.w209.inn1 #app .stagebar .scap.arr9{animation:arr9 1.1s ease-out}@keyframes arr9{0%{filter:brightness(1.35);box-shadow:0 0 0 3px rgba(255,216,77,.9)}100%{filter:none;box-shadow:0 0 0 0 rgba(255,216,77,0)}}",
   "html body.inn1 #ovfz,html body.inn1 #ovfz *{pointer-events:none!important}",
   "html body.w209.inn1 .fstalk .tstage .tfig img:not([data-fr9]){visibility:hidden!important}",
   "html body.w209.inn1 .fstalk .tstage .tfig img[data-fr9]{animation:in9 .24s ease-out}@keyframes in9{from{opacity:0;translate:0 10px}to{opacity:1;translate:0 0}}",
   "html body.w209.inn1 .fstalk .tstage .tfig img.bump9{animation:bump9 .28s ease-out!important}@keyframes bump9{40%{translate:0 -8px}100%{translate:0 0}}",
   /* 증거 획득 창: 그림 왼쪽·글 오른쪽, 확인 단추는 글자 크기에 맞춘 보통 크기 */
   "html body.w209.inn1 #ov .modal:has(>.foundic){display:grid!important;grid-template-columns:92px minmax(0,1fr);column-gap:16px;align-items:start;text-align:left;width:min(560px,calc(100vw - 32px))!important}",
   "html body.w209.inn1 #ov .modal:has(>.foundic)>*{grid-column:2;margin-top:0}",
   "html body.w209.inn1 #ov .modal:has(>.fbody9){max-height:calc(100vh - 20px)!important;height:auto!important;overflow:hidden!important;grid-template-rows:auto auto!important;row-gap:0!important}",
   "html body.w209.inn1 #ov .modal>.fbody9{grid-column:2;grid-row:1;min-height:0;max-height:calc(100vh - 112px);overflow-y:auto;overscroll-behavior:contain}",
   "html body.w209.inn1 #ov .modal:has(>.fbody9)>.foundic{grid-row:1!important}html body.w209.inn1 #ov .modal:has(>.fbody9)>#okfind{grid-row:2!important}",
   "html body.w209.inn1 #ov .modal:has(>.foundic)>.foundic{grid-column:1;grid-row:1 / span 6;margin:6px 0 0!important}",
   "html body.w209.inn1 #ov .modal:has(>.foundic) .foundic svg{width:84px!important;height:84px!important}",
   "html body.w209.inn1 #ov .modal:has(>.foundic)>#okfind,html body.w209.inn1 #ov .modal:has(>.bigic)>#okfind{grid-column:1 / -1;justify-self:center;width:auto!important;min-width:132px;position:static!important;margin:8px auto 0!important;min-height:40px!important;height:auto!important;padding:1px 22px!important;border-width:6px!important;border-image-width:6px!important;font-size:var(--t-ui)!important;display:block}",
   "html body.w209.inn1 #ov .modal:has(>.bigic)>#okfind{grid-column:2;justify-self:end;margin-right:0!important}",
   /* 조사 체크 표시 */
   "html body.w209.inn1 #bigscene .hot.done{display:block!important;visibility:visible!important;pointer-events:none!important;background:transparent!important;border:0!important;box-shadow:none!important;animation:none!important}",
   "html body.w209.inn1 #bigscene .hot.done>*{opacity:0!important;visibility:hidden!important}",
   "html body.w209.inn1 #bigscene .hot.done::after{content:'✓'!important;position:absolute!important;left:50%!important;top:50%!important;right:auto!important;bottom:auto!important;transform:translate(-50%,-50%)!important;width:26px!important;height:26px!important;border-radius:50%!important;background:rgba(61,122,74,.92)!important;color:#fff!important;font:700 16px/26px sans-serif!important;text-align:center!important;box-shadow:0 0 0 2px #FFF6E0!important;opacity:1!important;visibility:visible!important;display:block!important;border:0!important}",
   "#innmk9{position:fixed;inset:0;pointer-events:none;z-index:6}#innmk9 i{position:absolute;transform:translate(-50%,-50%);width:18px;height:18px;border-radius:50%;background:rgba(61,122,74,.78);color:#fff;font:700 12px/18px sans-serif;text-align:center;font-style:normal;box-shadow:0 0 0 1.5px rgba(255,246,224,.85)}",
   /* 인물 탭 */
   "#innppl{position:fixed;inset:0;z-index:80;background:rgba(8,10,24,.55);display:flex;align-items:center;justify-content:center}",
   "#innppl .pin{width:min(820px,calc(100vw - 24px));height:calc(100vh - 20px);box-sizing:border-box;display:flex;flex-direction:column;background:#FFF8E8;border:2px solid #C9A96A;border-radius:12px;padding:10px 12px;color:#2A1F16}",
   "#innppl .phd{display:flex;align-items:baseline;gap:10px;margin:0 0 8px}#innppl .phd b{font:400 var(--t-head,19px)/1.2 var(--display,Galmuri11,sans-serif)}#innppl .phd small{flex:1;color:#6B5A3A;font-size:var(--t-cap,12px)}#innppl .phd button{width:40px;height:36px;border:0;background:none;font-size:22px;color:#2A1F16}",
   "#innppl .pls{flex:1;min-height:0;overflow-y:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px;align-content:start}",
   "#innppl .pc{display:flex;gap:10px;padding:8px;border:1px solid #E1CFA6;border-radius:10px;background:#FFFDF6}#innppl .pf{flex:none;width:64px;height:64px;border-radius:8px;overflow:hidden;background:#EADBB8}#innppl .pf svg{width:64px;height:64px}",
   "#innppl .pt{min-width:0}#innppl h4{margin:0;font:400 var(--t-ui,15px)/1.3 var(--display,Galmuri11,sans-serif)}#innppl .pt>small{color:#8A5A2A;font-size:var(--t-cap,12px)}#innppl .pt p{margin:2px 0 0;font-size:var(--t-cap,12px);line-height:1.45;color:#4A3C2A}",
   "html body.w209.inn1 #bigscene .npc.w9 .npcclip{display:none!important}html body.w209.inn1 #bigscene .npc.w9{background:transparent!important;border:0!important;box-shadow:none!important}html body.w209.inn1 #bigscene .npc.w9>span{bottom:-6px!important;top:auto!important}",
   "#innppl .pf img{width:64px;height:64px;image-rendering:pixelated;display:block}",
   "html body.w209.inn1{--spk:64px}@media (max-height:380px){html body.w209.inn1{--spk:56px}}",
   "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt.v3{position:relative!important;padding-left:calc(var(--spk) + 26px)!important;min-height:calc(var(--spk) + 18px)!important;box-sizing:border-box!important}",
   "html body.w209.inn1 #vnbox .vtxt .spk9{position:absolute;left:12px;bottom:9px;width:var(--spk);height:var(--spk);border-radius:8px;overflow:hidden;background:rgba(255,246,224,.07);box-shadow:inset 0 0 0 1px rgba(201,169,106,.45)}",
   "html body.w209.inn1 #vnbox .vtxt .spk9 img{width:100%;height:100%;image-rendering:auto;display:block}",
   "html body.w209.inn1 #vnbox .vtxt .spk9.none{display:none}html body.w209.inn1 #vnbox .vtxt .spk9.sil img{display:none}",
   "html body.w209.inn1 #vnbox .vtxt .spk9.sil{background:radial-gradient(circle at 50% 38%,rgba(18,22,40,.9) 0 22%,transparent 23%),radial-gradient(ellipse 46% 30% at 50% 100%,rgba(18,22,40,.9) 0 98%,transparent 100%),rgba(255,246,224,.07)}",
   "html body.w209.inn1 #dlgveil #vnbox .vtxt.v3 .plate{left:calc(var(--spk) + 22px)!important}",
   "html body.w209.inn1 #dlgveil #vnbox .vtxt.v3 .nx{position:absolute!important;right:14px!important;bottom:8px!important;left:auto!important;top:auto!important;margin:0!important}",
   "html body.w209.inn1 #dlgveil #vnbox .vband .vtxt.v3,html body.w209.inn1 #dlgveil #vnbox .vband .vtxt.v3 #dtxt,html body.w209.inn1 #dlgveil #vnbox .vband.narr .vtxt.v3 .txt{text-align:left!important;justify-content:flex-start!important;align-items:flex-start!important}",
   "html body.w209.inn1 .fstalk .tpanel:not(:has(.topic)){display:none!important}",
   "#innppl ul{margin:4px 0 0;padding:0;list-style:none}#innppl li{font-size:var(--t-cap,12px);line-height:1.45;margin-top:3px}#innppl li b{display:block;color:#3D5E45;font-weight:700}#innppl .no{color:#8A7A5A!important}"
  ].join("\n");document.head.appendChild(css);

  /* ==== 2026-10-09 3차: 전환 플래시·흔들림 정리, 조사 체크 표시, 인물 탭, 인물 연출 ==== */
  /* (1) 장면 속 주민 전신 경로(엔진 F 모듈이 처음부터 이 그림을 쓴다: patches/18_ui_flash.py) */
  window.__innBody=function(k){if(!inn())return null;return {innma:"art/ch1/cast/innma-neutral-v5.png",seryeon:SER_SCENE,doto:DOTO,karo:"art/ch1/cast/karo-front.png",geokkuri:"art/ch1/cast/bami-front.png",det1:"art/ch1/cast/daram-front.png",nabi:"art/ch1/cast/nabi-front.png"}[k]||null};
  /* (2) 장면 제목 띠가 나올 때마다 화면 전체가 흔들리던 것(배너 → quake) 제거. 회의·대결의 '헛짚었다' 같은 판정 연출의 흔들림은 둔다 */
  var lastBan=-1e9;
  try{var _bn9=banner;banner=function(){if(inn())lastBan=performance.now();return _bn9.apply(this,arguments)}}catch(e){}
  try{var _qk9=quake;quake=function(){if(inn()&&performance.now()-lastBan<3500&&!document.querySelector("body>.rt .flash,.flash,.shout"))return;return _qk9.apply(this,arguments)}}catch(e){}
  /* (3) 옛 '장소 이동' 카드 대신 왼쪽 위 장소 이름표를 잠깐 밝힌다 */
  try{var _pc9=placeCard;placeCard=function(){if(!inn())return _pc9.apply(this,arguments);document.querySelectorAll(".placecard").forEach(function(e){e.remove()});
   setTimeout(function(){var b=document.querySelector("#app .stagebar .scap");if(b){b.classList.remove("arr9");void b.offsetWidth;b.classList.add("arr9")}},30)}}catch(e){}
  /* (4) 방 이동: 옛 지도 말이 걷는 820ms 대기 없이 곧바로(그동안 이전 방·옛 지도가 그대로 보이던 문제) */
  try{var _mt9=moveTo;moveTo=function(c,i,pp){if(!inn())return _mt9.apply(this,arguments);
    if(MOVING||G.loc===i||!locOpen(c,i)||dl())return;MOVING=true;var g0=G;try{SFX.steps()}catch(e){}
    setTimeout(function(){if(G!==g0||S.screen!=="case"){MOVING=false;return}var first=false;
     try{G.tab="scene";G.loc=i;G.arrive=true;if(!G.visited)G.visited=[];first=G.visited.indexOf(i)<0;if(first)G.visited.push(i);render();G.arrive=false}finally{MOVING=false}
     try{placeCard()}catch(e){}
     try{var l=c.locations[i];if(first){var bk2=(BEATS[c.id]||{})["loc:"+l.id];if(bk2&&!(G.beats&&G.beats["loc:"+l.id]))setTimeout(function(){if(G===g0)beat(c,"loc:"+l.id)},350)}}catch(e){}},90)}}catch(e){}
  /* (5) 대화 시작 컷인: 1장 말투에 맞게 */
  try{var _ci9=cutin;cutin=function(k,text){if(inn()&&!text)text="대화 시작";return _ci9.call(this,k,text)}}catch(e){}
  /* (6) 마지막 대사를 700ms 붙잡아 두는 동안(깜빡임 방지) 그 위의 탭을 먹지 않게: 누르면 곧바로 풀고 아래 단추가 받는다 */
  var fzT=null;
  document.addEventListener("pointerdown",function(e){fzT=null;if(!inn()||!window.__dlFreeze)return;var fz=document.getElementById("ovfz");if(fz)fz.innerHTML="";window.__dlFreeze=false;
   try{if(!dl()){B.classList.remove("dl-on");B.classList.remove("inn-cut")}}catch(x){}
   try{var el=document.elementFromPoint(e.clientX,e.clientY),b=el&&el.closest&&el.closest("#w209back,#w209rail button");if(b&&b!==e.target){fzT=b;if(window.__g199)window.__g199.dlg=false}}catch(x){}},true);
  /* 대화가 끝난 직후의 연타 방지(엔진 g199)는 대사창 쪽 연타만 막으면 된다: 조사로·오른쪽 위 도구 단추는 바로 받는다(대사창과 겹치지 않음) */
  document.addEventListener("pointerdown",function(e){try{if(!inn())return;var g=window.__g199;if(!g||!g.dlg||dl())return;var t=e.target;if(t&&t.closest&&t.closest("#w209back,#w209rail,#innmove,#innppl"))g.dlg=false}catch(x){}},true);
  /* 누르는 순간엔 숨어 있던 단추(조사로·질문 등)가 대상이 못 되므로, 같은 탭을 뗄 때 그 단추로 넘긴다 */
  document.addEventListener("pointerup",function(e){var b=fzT;fzT=null;if(!b||!inn())return;setTimeout(function(){try{if(document.contains(b))b.click()}catch(x){}},0)},true);

  /* (7) 조사 체크 표시: 살펴본 증거 지점은 ✓ 표시를 남기고(옛 아이콘은 숨김), 관찰한 물건도 작은 ✓를 이 방에 남긴다 */
  var SEEN={};try{SEEN=JSON.parse(sessionStorage.getItem("inn9seen")||"{}")||{}}catch(e){SEEN={}}
  function markSeen(lid,idx){(SEEN[lid]=SEEN[lid]||{})[idx]=1;try{sessionStorage.setItem("inn9seen",JSON.stringify(SEEN))}catch(e){}}
  function drawMarks(){try{var sc=document.getElementById("bigscene"),L0=document.getElementById("innmk9");if(!sc||!inn()||G.tab!=="scene"||dl()||document.querySelector("#ov .modal,.crec2,#wmap")){if(L0)L0.innerHTML="";return}var l=loc(),list=l&&OBS[l.id],seen=l&&SEEN[l.id];var lay=document.getElementById("innmk9");
    if(!list||!seen){if(lay)lay.remove();return}if(!lay){lay=document.createElement("div");lay.id="innmk9";B.appendChild(lay)}
    var sv=sc.querySelector("svg[data-inn-world]")||sc.querySelector("svg[data-bg]")||sc.querySelector("svg"),m=sv&&sv.getScreenCTM&&sv.getScreenCTM(),br=sc.getBoundingClientRect();if(!m)return;var h="";
    Object.keys(seen).forEach(function(i){var r=list[i];if(!r)return;var p=sv.createSVGPoint();p.x=r[0]+r[2]/2;p.y=r[1]+Math.min(r[3]/2,40);var q=p.matrixTransform(m);if(q.x>br.left-4&&q.x<br.right+4)h+='<i style="left:'+Math.round(q.x)+'px;top:'+Math.round(q.y)+'px">✓</i>'});
    if(lay.innerHTML!==h)lay.innerHTML=h}catch(e){}}

  /* (8) 기록 안 '인물' 탭: 만난 사람만, 이미 나온 정보(이름·하는 일·이 여관과의 관계)와 직접 물어 들은 말만. 새 설정·스포일러 없음 */
  var ROLE={innma:["여관 주인","이 여관을 꾸려 가는 토끼 할머니"],seryeon:["외지 손님","어젯밤 이 여관에 묵은 손님"],nabi:["여관 일을 돕는 고양이","여관에서 일한다"],geokkuri:["겨울 장기 투숙객","이 여관 2층에 겨울 동안 묵는다"],
   doto:["투숙객","여관 2층 방에 묵는다"],buri:["장치공","여관 일을 손봐 준다"],wanggu:["마을 규정 담당","주민 규약과 기록을 맡는다"],karo:["마차 마부","우리를 태우고 마을에 왔다"]};
  var ORDER=["innma","nabi","seryeon","buri","wanggu","karo","geokkuri","doto"];
  function metMark(){try{if(!inn()||!dl())return;var ln=DL.lines[DL.i];var w=ln&&ln[0];if(!ROLE[w])return;var pl=document.querySelector("#vnbox .plate");if(pl&&/\?\?\?/.test(pl.textContent))return;G.beats=G.beats||{};if(!G.beats["inn_met_"+w]){G.beats["inn_met_"+w]=1}}catch(e){}}
  function metList(){var b=G.beats||{},pro=!!b.inn_pro;return ORDER.filter(function(k){if(b["inn_met_"+k])return true;if(k==="geokkuri")return G.found.indexOf("C07")>=0;if(k==="doto")return G.found.indexOf("C08")>=0;return pro&&["innma","nabi","seryeon","buri","wanggu","karo"].indexOf(k)>=0})}
  var PP=null;function pplClose(){if(PP){PP.remove();PP=null}}
  function pplOpen(){pplClose();var c=CASES[G.ci],ks=metList(),h='<div class="pin"><div class="phd"><b>인물</b><small>만난 사람 '+ks.length+'명 · 직접 들은 말만 적어요</small><button type="button" data-x="1" aria-label="닫기">×</button></div><div class="pls">';
   ks.forEach(function(k){var nm=(CAST[k]&&CAST[k].name)||k,r=ROLE[k]||["",""],said=((c.talk&&c.talk[k])||[]).filter(function(t){return G.asked.indexOf(t.id)>=0&&t.q});
    var face="";try{face=PROF[k]?'<img alt="" data-k="'+k+'" src="'+AP+PROF[k]+'/profile.png?v=e4">':pf(k,"neutral")}catch(e){}
    h+='<section class="pc"><div class="pf">'+face+'</div><div class="pt"><h4>'+esc(nm)+'</h4><small>'+esc(r[0])+'</small><p>'+esc(r[1])+'</p>'+
     (said.length?'<ul>'+said.map(function(t){return '<li><b>'+esc(t.q)+'</b>'+esc(String(t.a||"").replace(/[{}]/g,""))+'</li>'}).join("")+'</ul>':'<p class="no">아직 직접 물어본 이야기는 없어요.</p>')+'</div></section>'});
   h+='</div></div>';PP=document.createElement("div");PP.id="innppl";PP.setAttribute("role","dialog");PP.setAttribute("aria-label","인물");PP.innerHTML=h;B.appendChild(PP);
   /* 초상 파일을 못 받으면(배포 직후 캐시 등) 깨진 그림 대신 같은 인물의 작은 얼굴로 */
   [].slice.call(PP.querySelectorAll(".pf img[data-k]")).forEach(function(im){function fb(){var k=im.dataset.k,w=im.parentNode;if(!w)return;try{w.innerHTML=pf(k,"neutral")}catch(e){w.innerHTML=""}}im.addEventListener("error",fb);if(im.complete&&!im.naturalWidth)fb()});
   PP.addEventListener("click",function(e){var t=e.target;if(t===PP||(t.closest&&t.closest("[data-x]"))){e.stopPropagation();try{SFX.tap()}catch(x){}pplClose()}})}
  function pplTab(){try{var r=document.querySelector(".crec2");if(!r||!inn()){pplClose();return}if(r.querySelector('[data-crt="ppl9"]'))return;var t=r.querySelector('[data-crt="t"]');if(!t)return;
    var b=document.createElement("button");b.type="button";b.className=t.className.replace(/\bon\b/,"");b.dataset.crt="ppl9";b.textContent="인물 "+metList().length;b.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();try{SFX.page()}catch(x){}pplOpen()},true);t.parentNode.insertBefore(b,t.nextSibling)}catch(e){}}

  /* (9) 인물 연출: 대화 화면에 들어올 때 살짝 떠오르고, 같은 인물의 표정 그림이 바뀌면 작게 들썩인다 */
  function doneMarks(){try{var W9=window.__innWorld,sc=document.getElementById("bigscene"),im=sc&&sc.querySelector("svg[data-inn-world]");if(!W9||!im)return;var k=im.dataset.innWorld,c=W9.camera(k),A=W9.anchors&&W9.anchors[k==="storage"?"bed13":k];if(!A)return;
    sc.querySelectorAll(".hot.done[data-done]").forEach(function(e){var r=A[e.dataset.done];if(!r)return;var x=(r[0]-c.x)*c.scale,y=(r[1]-c.y)*c.scale;e.style.setProperty("left",x+"px","important");e.style.setProperty("top",y+"px","important")})}catch(e){}}
  /* 증거를 주는 질문(C12 등)은 답이 끝난 뒤 질문 화면이 다시 그려지지 않아 읽음 체크가 안 붙고 같은 질문이 또 눌리던 문제: 들은 질문이 남아 있으면 한 번 다시 그린다 */
  function topicSync(){try{if(dl()||G.tab!=="talk"||document.querySelector("#ov .modal,.cutin,.crec2"))return;var stale=[].slice.call(document.querySelectorAll(".fstalk .topic[data-ask]")).some(function(t){return G.asked.indexOf(t.dataset.ask)>=0});if(stale)render()}catch(e){}}
  /* 증거 획득 창: 글은 오른쪽 칸 안에서만 스크롤하고, 확인 단추는 그 아래 별도 줄(긴 증언에서도 글을 가리지 않음) */
  function cardWrap(){try{var m=document.querySelector("#ov .modal");if(!m||!m.querySelector(":scope>.foundic")||m.querySelector(":scope>.fbody9"))return;var ok=m.querySelector(":scope>#okfind"),w=document.createElement("div");w.className="fbody9";
    [].slice.call(m.children).forEach(function(ch){if(!ch.classList.contains("foundic")&&ch!==ok)w.appendChild(ch)});m.insertBefore(w,ok||null)}catch(e){}}
  try{new MutationObserver(cardWrap).observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
  var lastK="",lastSrc="";function bump(){try{var i=document.querySelector(".fstalk .tstage .tfig img");if(!i)return;var k=i.dataset.k,s=i.getAttribute("src");if(k===lastK&&s!==lastSrc){i.classList.remove("bump9");void i.offsetWidth;i.classList.add("bump9")}lastK=k;lastSrc=s}catch(e){}}

  try{new MutationObserver(function(){drawMarks()}).observe(document.documentElement,{subtree:true,attributes:true,attributeFilter:["viewBox"]})}catch(e){}

  /* ==== 통합 아트(2026-10-09): 장소 인물 행동 포즈를 배경과 같은 좌표·같은 팬 변환으로 ====
     배경 svg 안에 원본 픽셀 좌표로 넣는다(식당 2048x768, 부엌 1774x887, 복도·도토 방 1672x941). 누르는 영역은 그림 자리에 맞춘 기존 인물 단추 */
  var AP="art/ch1/action-poses/";
  window.__innPose=function(k){try{if(!inn())return null;var b=G.beats||{};if(!b.inn_pro||b.inn_final)return null;var lid=(loc()||{}).id;
    if(k==="seryeon")return AP+"seryeon/dialogue.png";if(k==="innma"&&lid==="dining")return AP+"grandma/dialogue.png";if(k==="geokkuri"&&lid==="hall")return AP+"bami/dialogue.png";
    if(k==="nabi"&&lid==="kitchen")return AP+"nabi/dialogue.png";if(k==="doto"&&lid==="dotoroom")return AP+"doto/dialogue.png";}catch(e){}return null};
  /* [인물, 파일, x, y, 폭, 높이] — 식당은 통합 아트 배치표 그대로(세련 735,283 / 할머니는 좌우 보기 반대쪽 끝 부엌문 앞 바닥 579에 발), 부엌 나비는 식당 대비 가구 배율 1.6(의자 좌석 높이 비교) */
  var WN={dining:[["innma",AP+"grandma/npc.png",1800,303,162,276],["seryeon",AP+"seryeon/npc.png",735,283,241,361]],
   kitchen:[["nabi",AP+"nabi/npc.png",830,190,339,504]],
   hall:[["geokkuri",AP+"bami/npc.png",100,25,424,429]],
   dotoroom:[["doto",AP+"doto/npc.png",690,161,472,533,1]]};
  var OCC={dining:[["art/ch1/fg/dining_tabletop_occluder.png",858,427,906,86]]};
  var WPX={dotoroom:[["art/ch1/props/doto_room/prop_weather_notebook_open_rgba.png",1106,450.45,164,28.55],["art/ch1/props/doto_room/prop_bookstack_rgba.png",1309.5,408.7,105,53.3],["art/ch1/props/doto_room/prop_pencilcup_rgba.png",1435,396.4,30,65.6]]};
  function svgOf(sc){return sc&&(sc.querySelector("svg[data-inn-world]")||sc.querySelector("svg[data-bg]"))}
  function img(sv,f,x,y,w,h,cls){var im=document.createElementNS("http://www.w3.org/2000/svg","image");im.setAttribute("class",cls);im.setAttribute("href",f);im.setAttribute("x",x);im.setAttribute("y",y);im.setAttribute("width",w);im.setAttribute("height",h);im.setAttribute("preserveAspectRatio","none");im.setAttribute("style","image-rendering:pixelated;pointer-events:none");sv.appendChild(im);return im}
  function worldNpc(){try{var sc=document.getElementById("bigscene"),sv=svgOf(sc);if(!sv||!inn()||G.tab!=="scene"){return}var b=G.beats||{};if(!b.inn_pro||b.inn_final)return;var lid=(loc()||{}).id,L=WN[lid]||[],key=lid+"|"+L.length;
    if(sv.dataset.wn9!==key){[].slice.call(sv.querySelectorAll("image.wn9,image.wo9,image.wp9")).forEach(function(e){e.remove()});
     (WPX[lid]||[]).forEach(function(p){img(sv,p[0],p[1],p[2],p[3],p[4],"wp9")});
     L.forEach(function(n){var e=img(sv,n[1],n[2],n[3],n[4],n[5],"wn9");e.dataset.k=n[0]});
     (OCC[lid]||[]).forEach(function(o){img(sv,o[0],o[1],o[2],o[3],o[4],"wo9")});sv.dataset.wn9=key}
    /* 인물 단추를 그림 자리로(누름 영역 = 그림 사각형, 최소 48px). 옛 전신 그림은 숨긴다 */
    var m=sv.getScreenCTM(),br=sc.getBoundingClientRect();if(!m)return;
    L.forEach(function(n){var bt=sc.querySelector('.npc[data-npc="'+n[0]+'"]');if(!bt)return;bt.classList.add("w9");
     var p1=sv.createSVGPoint();p1.x=n[2];p1.y=n[3];var a=p1.matrixTransform(m);var p2=sv.createSVGPoint();p2.x=n[2]+n[4];p2.y=n[3]+n[5];var z=p2.matrixTransform(m);
     var w=Math.max(48,z.x-a.x),h=Math.max(48,z.y-a.y),l=a.x-br.left,t=a.y-br.top;
     [["left",l+"px"],["top",t+"px"],["width",w+"px"],["height",h+"px"],["transform","none"],["margin","0"]].forEach(function(d){bt.style.setProperty(d[0],d[1],"important")})});
    if(lid==="dotoroom"){var d=sc.querySelector('.npc[data-npc="doto"]');if(d)d.style.setProperty("pointer-events","none","important")}}catch(e){}}
  var PROF={det1:"daram",innma:"grandma",geokkuri:"bami",nabi:"nabi",karo:"karo",seryeon:"seryeon",wanggu:"neoul",doto:"doto",buri:"buri"};

  /* ==== 대화 UI v3(2026-10-09 확정): 대사창 안 왼쪽에 작은 화자 초상(누구 말인지 표시용, 표정·행동은 장면 인물이 맡음) ====
     초상은 통합 아트 profile.png(9명). 아빠는 공개된 얼굴이 없으므로 중립 실루엣. 지문(회색)은 초상 없이 같은 글 위치 */
  function speaker(){try{if(!inn()||!dl())return;var vt=document.querySelector("#vnbox .vtxt");if(!vt)return;var ln=DL.lines[DL.i]||[],w=ln[0],vb=vt.closest(".vband");
    var inner=vb&&vb.classList.contains("inner");var k=inner?"det0":w;var sp=vt.querySelector(".spk9");if(!sp){sp=document.createElement("span");sp.className="spk9";sp.setAttribute("aria-hidden","true");sp.innerHTML="<img alt=''>";vt.insertBefore(sp,vt.firstChild)}
    var f=PROF[k]?AP+PROF[k]+"/speaker128.png":"",mode=f?"img":(k==="det0"?"sil":"none");if(sp.dataset.k!==k+"|"+mode){sp.dataset.k=k+"|"+mode;sp.className="spk9 "+mode;var im=sp.firstChild;if(f){im.src=f}else im.removeAttribute("src")}
    vt.classList.add("v3")}catch(e){}}
  setInterval(speaker,60);
  window.__innUI9={obs:function(){return window.__innObsLast||""},HK:HK,OBS:OBS};
 })();
