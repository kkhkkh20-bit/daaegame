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
  var SHORT={bed13:"안 쓰는 방 · 열세 번째 침대",dining:"식당",kitchen:"부엌",hall:"2층 복도",dotoroom:"도토의 방",front:"접수대",plaza:"광장 (여관 밖)"};
  var MV=null,pass=false;
  function mvClose(){if(MV){MV.remove();MV=null}B.classList.remove("innmv-on")}
  function mvOpen(btn){mvClose();var c=CASES[G.ci],h='<div class="hd"><b>장소 이동</b><button type="button" data-x="1" aria-label="닫기">×</button></div><div class="ls">';
   c.locations.forEach(function(l,i){var open=true;try{open=locOpen(c,i)}catch(e){}if(!open)return;var here=i===G.loc;
    h+='<button type="button" data-i="'+i+'"'+(here?' disabled aria-current="true"':'')+'><span>'+(SHORT[l.id]||l.name)+'</span>'+(here?'<small>지금 여기</small>':'')+'</button>'});
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
   if(document.querySelector("#ov .modal,#mveil .modal,#innins,#wmap,.crec2,#innmove,body>.rt"))return false;if(document.getElementById("closeNotice")){if(!t.closest("#app .notice")){try{document.getElementById("closeNotice").click()}catch(x){}}return false}return sc}
  var down=null;
  document.addEventListener("pointerdown",function(e){var sc=tappable(e.target);down=sc?{x:e.clientX,y:e.clientY,t:performance.now(),sc:sc}:null},true);
  document.addEventListener("pointerup",function(e){var d=down;down=null;if(!d)return;if(Math.abs(e.clientX-d.x)>12||Math.abs(e.clientY-d.y)>12||performance.now()-d.t>700)return;if(!tappable(e.target)&&!d.sc.contains(e.target))return;
   /* 2026-10-10 "가방 누르는 범위가 그림과 안 맞는다": 증거 지점·인물 바로 옆(28px 안)을 누르면 큰 물건 관찰(예: 침대) 대신 그 지점을 연다 */
   /* 2026-10-10 "조사할 때 인물 선택 범위가 너무 크다, 몸에 닿았을 때만": 장면 속 인물(.npc.w9)은 단추 사각형이 아니라 그림의 불투명 픽셀에 닿아야 연다 */
   /* 이미 본 관찰 지점(침대 밑 상자 등)은 엔진이 숨겨 버려 다시 누르면 뒤의 침대 관찰로 새던 문제: 그 자리면 그 지점의 아빠 속마음 한 줄(예: 할머니가 손대지 말라고 하셨지…) */
   var so=null;[].slice.call(d.sc.querySelectorAll(".hot.obs[data-obs]")).some(function(h){var cs=getComputedStyle(h);if(cs.visibility!=="hidden"&&cs.pointerEvents!=="none")return false;var r=h.getBoundingClientRect();if(r.width&&e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top&&e.clientY<=r.bottom){so=h;return true}return false});
   if(so){var oo=null;try{oo=(loc().obs||[]).filter(function(x){return x.id===so.dataset.obs})[0]}catch(x){}if(oo&&oo.text){try{SFX.select()}catch(x){}obShow("("+String(oo.text).replace(/^\(|\)$/g,"")+")");return}}
   var nh=npcHit(d.sc,e.clientX,e.clientY);if(nh){setTimeout(function(){try{nh.click()}catch(x){}},0);return}
   /* 도토의 방: 도토 단추는 일지 지점과 겹쳐 꺼 두었다 — 도토 몸을 누르면 '아무것도 없다' 대신 안내 한 줄 */
   try{var dimg=d.sc.querySelector('svg image.wn9[data-k="doto"]');if(dimg&&alphaAt(dimg,e.clientX,e.clientY,3)>60){try{SFX.select()}catch(x){}obShow("(도토 씨가 앉아 있다. 창가의 일지부터 보자.)");return}}catch(x){}
   var near=null,nd=1e9;[].slice.call(d.sc.querySelectorAll(".hot:not(.done),.npc:not(.w9)")).forEach(function(h){var r=h.getBoundingClientRect();if(!r.width)return;var dx=Math.max(r.left-e.clientX,0,e.clientX-r.right),dy=Math.max(r.top-e.clientY,0,e.clientY-r.bottom),dd=Math.max(dx,dy);if(dd<=28&&dd<nd){nd=dd;near=h}});
   if(near){setTimeout(function(){try{near.click()}catch(x){}},0);return}
   /* 2026-10-10 "침대·자물쇠 상자를 다시 누르면 다른 네모 상자가 생긴다": 이미 챙긴 증거 자리(주머니·손자국·상자)를 다시 누르면 뒤의 침대 관찰로 새어 나가 엉뚱한 자리에 표시가 생기던 문제. 그 증거 이름만 짧게 알려 준다 */
   var dn=null;nd=1e9;[].slice.call(d.sc.querySelectorAll(".hot.done[data-done]")).forEach(function(h){var r=h.getBoundingClientRect();if(!r.width)return;var dx=Math.max(r.left-e.clientX,0,e.clientX-r.right),dy=Math.max(r.top-e.clientY,0,e.clientY-r.bottom),dd=Math.max(dx,dy);if(dd<=28&&dd<nd){nd=dd;dn=h}});
   if(dn){var ev=(window.EP1INN&&window.EP1INN.EV||{})[dn.dataset.done];try{SFX.select()}catch(x){}obShow("("+(ev?ev.name:"이미 살펴본 곳")+". 이미 증거로 챙겼다.)");return}
   var l=loc(),list=l&&((((window.EP1INN||{}).LOOK||{})[l.id]||[]).concat(OBS[l.id]||[])),p=worldPt(d.sc,e.clientX,e.clientY),hit=null;
   var hi=-1;if(list&&p)for(var i=0;i<list.length;i++){var r=list[i];if(p.x>=r[0]&&p.x<=r[0]+r[2]&&p.y>=r[1]&&p.y<=r[1]+r[3]){hit=r[4];hi=i;break}}
   if(hi>=0){markSeen(l.id,hi);setTimeout(drawMarks,0)}
   var rr=hi>=0?list[hi]:null,lk=rr&&rr[5]?l.id+":"+rr[0]+","+rr[1]:null;   /* 2026-10-10 v2 "방마다 누를 게 너무 적다": 처음 누르면 아빠·다람 주고받기, 그 뒤엔 한 줄 */
   if(lk&&(G.look9||[]).indexOf(lk)<0){(G.look9=G.look9||[]).push(lk);try{SFX.select()}catch(x){}obHide();window.__innObsLast=hit;try{saveProg()}catch(x){}
    try{say(rr[5].map(function(x){return x.slice()}),function(){try{render()}catch(x){}})}catch(x){obShow(hit)}return}
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
  var q=0;function tick(){q=0;if(!inn()){B.classList.remove("inn-pan9");mvClose();return}speaker();preload();dotoSwap();seated();talkFrame();bump();topicSync();npcScale();lockScroll();worldNpc();drawMarks();doneMarks();pplTab();recDetail();metMark();if(PP&&!document.querySelector(".crec2"))pplClose();
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
   "html body.w209.inn1 .fstalk .tpanel .topic.done::before{content:'들음';position:absolute;left:auto;right:9px;top:50%;transform:translateY(-50%);font-size:var(--t-cap,12px);color:#3D7A4A;font-weight:400}","html body.w209.inn1 .fstalk .tpanel .topic.done{padding-left:12px!important;padding-right:44px!important}",
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
   /* 2026-10-10 "증거 글씨가 그림자처럼 흔들려 보인다": 상세 칸 전체에 걸린 drop-shadow 필터가 글자에도 3px 아래 그림자를 만들던 것 제거. 크기는 16px(3배 화면에서 픽셀 격자와 맞음) */
   "html body.w209.inn1 .crec2 .cr-det{filter:none!important}",
   "html body.w209.inn1 .crec2 .cr-det .cr-tx>p{font-size:16px!important;border-bottom:0!important;text-shadow:none!important}",
   /* 2026-10-10 "프롤로그·대사 중에도 더보기 칸은 항상 보여 줘(소리 조절·저장)" */
   "html body.w209.inn1.dl-on #w209rail [data-more]{visibility:visible!important;pointer-events:auto!important}",
   "html body.w209.inn1.dl-on #w209rail{z-index:60!important}",
   "html body.w209.inn1.dl-on #w209rail.more #w209more{visibility:visible!important;pointer-events:auto!important}",
   "html body.w209.inn1.dl-on #w209rail.more #w209more *{visibility:visible!important}",
   "html body.w209.inn1.dl-on #w209more [data-w=\"move\"],html body.w209.inn1.dl-on #w209more [data-w=\"hint\"],html body.w209.inn1.dl-on #w209more [data-w=\"reset\"]{display:none!important}",
   /* 2026-10-10 UI 검수 반영 */
   "@media (max-width:700px){html body.w209.inn1 #rtgtpc{left:158px!important;right:auto!important;transform:none!important;max-width:calc(100vw - 158px - 240px)!important;overflow:hidden!important;white-space:nowrap!important;text-overflow:ellipsis!important}html body.w209.inn1 #rtgtop{max-width:none!important;white-space:nowrap!important}}",
   "html body.w209.inn1 .rt .wk{padding:6px 4px!important;margin:-6px 0!important}",
   "html body.w209.inn1 #closeNotice{min-width:44px!important;min-height:44px!important}",
   "html body.w209.inn1 button.e9b,html body.w209.inn1 #innppl .plog{position:relative}html body.w209.inn1 button.e9b::after,html body.w209.inn1 #innppl .plog::after{content:\"\";position:absolute;inset:-7px -3px}",
   "html body.w209.inn1{overflow-x:hidden}",
   "html body.w209.inn1 .crec2 .cr-det .cr-ic svg{transform:none!important;animation:none!important}",
   /* 증거 획득 창: 그림 왼쪽·글 오른쪽, 확인 단추는 글자 크기에 맞춘 보통 크기 */
   "html body.w209.inn1 #vnbox .vtxt .spk9 img{animation:br9 3.6s steps(1,end) infinite}",
   "@keyframes br9{0%{translate:0 0}45%{translate:0 -1px}55%{translate:0 -1px}100%{translate:0 0}}",
   "html body.w209.inn1 #vnbox .vtxt .spk9 .sw9{position:absolute;right:14%;top:18%;width:12px;height:18px;background:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 8 12' shape-rendering='crispEdges'%3E%3Cpath d='M3 0h2v2h1v2h1v2h1v4h-1v1h-1v1h-4v-1h-1v-1h-1v-4h1v-2h1v-2h1z' fill='%232E5E8C'/%3E%3Cpath d='M3 2h2v2h1v2h1v4h-1v1h-4v-1h-1v-4h1v-2h1z' fill='%23A9DDFF'/%3E%3Crect x='2' y='6' width='1' height='2' fill='%23ffffff'/%3E%3C/svg%3E\") center/100% 100% no-repeat;image-rendering:pixelated;animation:sw9 1.5s steps(5,end) infinite;pointer-events:none}",
   "@keyframes sw9{0%{opacity:0;transform:translateY(-2px)}20%{opacity:1;transform:translateY(0)}80%{opacity:1;transform:translateY(8px)}100%{opacity:0;transform:translateY(10px)}}",
   "html body.w209.inn1 #vnbox .vtxt .spk9.jolt9{animation:jolt9 .32s steps(4,end) 1}",
   "@keyframes jolt9{0%{translate:0 0}25%{translate:-2px -2px}50%{translate:2px 0}75%{translate:-1px 0}100%{translate:0 0}}",
   "@media (prefers-reduced-motion:reduce){html body.w209.inn1 #vnbox .vtxt .spk9 img,html body.w209.inn1 #vnbox .vtxt .spk9 .sw9,html body.w209.inn1 #vnbox .vtxt .spk9.jolt9{animation:none}}",
   "#e9pop ol.e9log{margin:8px 0 6px;padding:0 0 0 4px;list-style:none;display:flex;flex-direction:column;gap:8px}",
   "#e9pop ol.e9log li{font:400 16px/1.6 Galmuri11,monospace;color:#2A1C12;word-break:keep-all;border-bottom:1px dashed #C9B48C;padding-bottom:6px}",
   "#e9pop ol.e9log em{display:block;font-style:normal;font-size:13px;color:#2F6B3A;margin-bottom:2px}",
   "#innppl button.e9b.plog{all:unset;cursor:pointer;box-sizing:border-box;margin-top:6px;font:400 13px/20px Galmuri11,monospace;padding:4px 12px;min-height:32px;border:2px solid #8A5E36;border-radius:4px;color:#6B4A2B;background:#FFF9EA}",
   "#innppl button.e9b.plog i{font-style:normal;color:#A23B2A;margin-left:4px}",
   "html body.w209.inn1 #bigscene .npc.w9{pointer-events:none!important}",
   "#e9pop{position:fixed;inset:0;z-index:2000;background:rgba(10,8,6,.55);display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;cursor:pointer}",
   "#e9pop .e9pc{width:min(580px,100%);max-height:100%;overflow-y:auto;box-sizing:border-box;background:#FBF4E2;border:3px solid #6B4A2B;box-shadow:0 0 0 3px #2A1C12;padding:12px 18px 10px;text-align:left}",
   "#e9pop b{display:inline-block;background:#F2C230;color:#2A1C12;padding:2px 10px;font:400 16px/1.4 Galmuri11B,Galmuri11,monospace}",
   "#e9pop p{margin:8px 0 4px;font:400 16px/1.75 Galmuri11,monospace;color:#2A1C12;word-break:keep-all}",
   "#e9pop small{display:block;text-align:right;font:400 12px Galmuri11,monospace;color:#8A5E36}",
   "html body.w209.inn1 .crec2 #crdaram,html body.w209.inn1 .crec2 .cr-det:not(.empty) .cr-tx>#crdaram{display:none!important}",
   "html body.w209.inn1 .crec2 .cr-det .dmemo{display:none!important}",
   "html body.rtg .crec2{z-index:66!important}",
   /* 2026-10-10 사용자 "모든 캐릭터 다람이 꼬리처럼 무빙 가볍게": 새 그림 없이 아주 작은 숨쉬기·흔들림(발밑 기준 ±0.5도, 세로 1.2%). 다람은 꼬리 프레임이 있어 무대 그림에서는 제외.
      줄이기 설정(prefers-reduced-motion)이면 멈춘다 */
   "@keyframes idle9{0%,100%{rotate:0deg;scale:1 1}25%{rotate:-.5deg}50%{scale:1 1.012}75%{rotate:.5deg}}",
   "html body.w209.inn1 #innstage .isf.in:not([data-k=\"det1\"]) img{transform-origin:50% 100%;animation:idle9 3.6s ease-in-out infinite}",
   "html body.w209.inn1 .fstalk .tstage .tfig img[data-fr9]{transform-origin:50% 100%;animation:in9 .24s ease-out,idle9 3.6s ease-in-out .3s infinite}",
   "html body.w209.inn1 #bigscene svg image.wn9{transform-box:fill-box;transform-origin:50% 100%;animation:idle9 4s ease-in-out infinite}",
   "html body.w209.inn1 svg[data-bg=\"carriage\"] image.innseat{transform-box:fill-box;transform-origin:50% 100%;animation:idle9 3.8s ease-in-out infinite}",
   "html body.w209.inn1 #bigscene svg image.wn9:nth-of-type(2n){animation-delay:-1.3s}html body.w209.inn1 #bigscene svg image.wn9:nth-of-type(3n){animation-delay:-2.6s}",
   "html body.rtg #rtg .seat:not(.front) img{transform-origin:50% 100%;animation:idle9 4.2s ease-in-out infinite}html body.rtg #rtg .seat:nth-child(2n) img{animation-delay:-1.5s}html body.rtg #rtg .seat:nth-child(3n) img{animation-delay:-2.8s}",
   "@media (prefers-reduced-motion:reduce){html body.w209.inn1 #innstage .isf img,html body.w209.inn1 .fstalk .tstage .tfig img,html body.w209.inn1 #bigscene svg image.wn9,html body.rtg #rtg .seat img{animation:none!important}}",
   "html body.rtg .rtpanel{visibility:hidden!important}",   /* 회의 화면 아래 남은 소개 화면의 '원탁 회의 열기'(rtgo)가 키보드·접근성 클릭으로 눌려 회의가 두 장 열리던 것(dot QA 진행 차단의 실제 원인) */   /* 회의 중 연 사건 기록 창이 회의 화면(z60)·하단 단추(z62)·증거 서랍(z63) 아래에 깔려 닫히지 않던 것(dot QA 2026-10-10) */
   "html body.w209.inn1 .crec2 .cr-det .cr-tx>h3{background:#F2C230!important;color:#2A1C12!important;padding:3px 10px!important;margin:0 0 4px!important;border:0!important;background-image:none!important}",
   "html body.w209.inn1 .crec2 .cr-det .cr-tx>p{line-height:30px!important;background:repeating-linear-gradient(to bottom,transparent 0 28px,#C9B48C 28px 29px,transparent 29px 30px)}",
   "html body.w209.inn1 .crec2 .orig9{margin:6px 0 0}",
   "html body.w209.inn1 .crec2 .orig9 .e9opt{display:flex;gap:8px;flex-wrap:wrap}",
   "html body.w209.inn1 .crec2 .orig9 button.e9b{all:unset;cursor:pointer;box-sizing:border-box;font:400 13px/20px Galmuri11,monospace;padding:4px 12px;min-height:32px;border:2px solid #8A5E36;border-radius:4px;color:#6B4A2B;background:#FFF9EA}",
   "html body.w209.inn1 .crec2 .orig9 button.e9b.on{background:#6B4A2B;color:#FFF6E0}",
   "html body.w209.inn1 #ov .modal.ev9{display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:8px!important;width:min(700px,calc(100vw - 24px))!important;max-width:none!important;max-height:calc(100vh - 16px)!important;height:auto!important;min-height:0!important;padding:12px 14px 10px!important;text-align:left!important;overflow:hidden!important;background:#FBF4E2!important;border:3px solid #6B4A2B!important;box-shadow:0 0 0 3px #2A1C12,0 6px 0 rgba(0,0,0,.35)!important;border-radius:6px!important;box-sizing:border-box!important}",
   "html body.w209.inn1 #ov .modal.ev9::before,html body.w209.inn1 #ov .modal.ev9::after{display:none!important}",
   "html body.w209.inn1 #ov .modal.ev9 .e9card{width:100%;box-sizing:border-box;justify-content:stretch;display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:16px;min-height:0;flex:1 1 auto;overflow:hidden}",
   "html body.w209.inn1 #ov .modal.ev9 .e9ic{width:124px;height:124px;background:#E9DFC8;border:3px solid #3B2A1E;box-shadow:inset 0 0 0 3px #F6EEDB;display:grid;place-items:center;align-self:start}",
   "html body.w209.inn1 #ov .modal.ev9 .e9ic>*{width:100%!important;height:100%!important;border:0!important;border-radius:0!important;box-shadow:none!important;background:transparent!important;margin:0!important;animation:none!important;display:grid!important;place-items:center!important}",
   "html body.w209.inn1 #ov .modal.ev9 .e9ic svg{width:100px!important;height:100px!important}",
   "html body.w209.inn1 #ov .modal.ev9 .e9tx{min-height:0;overflow-y:auto;overscroll-behavior:contain;display:flex;flex-direction:column;gap:5px;padding-right:2px}",
   "html body.w209.inn1 #ov .modal.ev9 .e9k{font:400 12px/1.3 Galmuri11,monospace;color:#A23B2A;letter-spacing:.04em}",
   "html body.w209.inn1 #ov .modal.ev9 .e9t{margin:0!important;background:#F2C230;color:#2A1C12;padding:3px 10px!important;font:400 20px/1.3 Galmuri11B,Galmuri11,monospace!important;text-align:left!important;border:0!important}",
   "html body.w209.inn1 #ov .modal.ev9 .e9d{margin:2px 0 0!important;font:400 16px/30px Galmuri11,monospace!important;color:#2A1C12!important;text-align:left!important;word-break:keep-all;background:repeating-linear-gradient(to bottom,transparent 0 28px,#C9B48C 28px 29px,transparent 29px 30px)}",
   "html body.w209.inn1 #ov .modal.ev9 .e9opt{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}",
   "html body.w209.inn1 #ov .modal.ev9 button.e9b{all:unset;cursor:pointer;box-sizing:border-box;font:400 13px/20px Galmuri11,monospace;padding:4px 12px;min-height:32px;border:2px solid #8A5E36;border-radius:4px;color:#6B4A2B;background:#FFF9EA}",
   "html body.w209.inn1 #ov .modal.ev9 button.e9b.on{background:#6B4A2B;color:#FFF6E0}",
   "html body.w209.inn1 #ov .modal.ev9 .e9pan{font:400 14px/1.6 Galmuri11,monospace;color:#4A3A28;background:#F3E8CC;border-left:3px solid #B98A3E;padding:6px 10px;text-align:left}",
   "html body.w209.inn1 #ov .modal.ev9 .e9pan[hidden]{display:none!important}",
   "html body.w209.inn1 #ov .modal.ev9 .e9pan small{display:block;color:#8A5E36;font-size:12px;margin-bottom:2px}",
   "html body.w209.inn1 #ov .modal.ev9 .e9pan p{margin:0}",
   "html body.w209.inn1 #ov .modal.ev9 .e9foot{width:100%;box-sizing:border-box;display:flex;align-items:center;gap:12px;border-top:2px solid #D9C7A0;padding-top:8px;flex:0 0 auto}",
   "html body.w209.inn1 #ov .modal.ev9 .e9add{flex:1;font:400 15px/1.4 Galmuri11,monospace;color:#2F4E86;text-align:left}",
   "html body.w209.inn1 #ov .modal.ev9 #okfind{position:static!important;margin:0!important;width:auto!important;min-width:100px!important;min-height:40px!important;height:42px!important;padding:0 20px!important;line-height:1!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;box-sizing:border-box!important;grid-row:auto!important;flex:0 0 auto}",
   "@media (max-height:380px){html body.w209.inn1 #ov .modal.ev9 .e9ic{width:100px;height:100px}html body.w209.inn1 #ov .modal.ev9 .e9ic svg{width:80px!important;height:80px!important}html body.w209.inn1 #ov .modal.ev9 .e9t{font-size:18px!important}}",
   "@media (max-width:560px){html body.w209.inn1 #ov .modal.ev9 .e9ic{width:84px;height:84px}html body.w209.inn1 #ov .modal.ev9 .e9ic svg{width:68px!important;height:68px!important}}",
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
   "html body.w209.inn1 #bigscene .hot.done::after{content:'확인'!important;position:absolute!important;left:50%!important;top:50%!important;right:auto!important;bottom:auto!important;transform:translate(-50%,-50%)!important;width:auto!important;height:auto!important;padding:1px 6px!important;border-radius:6px!important;background:rgba(61,122,74,.92)!important;color:#fff!important;font:400 11px/16px var(--display,Galmuri11,sans-serif)!important;white-space:nowrap!important;text-align:center!important;box-shadow:0 0 0 2px #FFF6E0!important;opacity:1!important;visibility:visible!important;display:block!important;border:0!important}",
   "#innmk9{position:fixed;inset:0;pointer-events:none;z-index:6}#innmk9 i{position:absolute;transform:translate(-50%,-50%);padding:0 5px;border-radius:5px;background:rgba(61,122,74,.78);color:#fff;font:400 10px/15px Galmuri11,sans-serif;white-space:nowrap;text-align:center;font-style:normal;box-shadow:0 0 0 1.5px rgba(255,246,224,.85)}",
   /* 인물 탭 */
   "#innppl{position:fixed;inset:0;z-index:80;background:rgba(8,10,24,.55);display:flex;align-items:center;justify-content:center}",
   "#innppl .pin{width:min(820px,calc(100vw - 24px));height:calc(100vh - 20px);box-sizing:border-box;display:flex;flex-direction:column;background:#FFF8E8;border:2px solid #C9A96A;border-radius:12px;padding:10px 12px;color:#2A1F16}",
   "#innppl .phd{display:flex;align-items:baseline;gap:10px;margin:0 0 8px}#innppl .phd b{font:400 var(--t-head,19px)/1.2 var(--display,Galmuri11,sans-serif)}#innppl .phd small{flex:1;color:#6B5A3A;font-size:var(--t-cap,12px)}#innppl .phd button{width:40px;height:36px;border:0;background:none;font-size:22px;color:#2A1F16}",
   "#innppl .pls{flex:1;min-height:0;overflow-y:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px;align-content:start}",
   "#innppl .pc{display:flex;gap:10px;padding:8px;border:1px solid #E1CFA6;border-radius:10px;background:#FFFDF6}#innppl .pf{flex:none;width:64px;height:64px;border-radius:8px;overflow:hidden;background:#EADBB8}#innppl .pf svg{width:64px;height:64px}",
   "#innppl .pt{min-width:0}#innppl h4{margin:0;font:400 var(--t-ui,15px)/1.3 var(--display,Galmuri11,sans-serif)}#innppl .pt>small{color:#8A5A2A;font-size:var(--t-cap,12px)}#innppl .pt p{margin:2px 0 0;font-size:var(--t-cap,12px);line-height:1.45;color:#4A3C2A}",
   "html body.w209.inn1 #bigscene .npc.w9 .npcclip{display:none!important}html body.w209.inn1 #bigscene .npc.w9{background:transparent!important;border:0!important;box-shadow:none!important}html body.w209.inn1 #bigscene .npc.w9>span{bottom:-6px!important;top:auto!important}",
   "#innppl .pf img{width:64px;height:64px;image-rendering:pixelated;display:block}",
   "html body.w209.inn1{--spk:96px}@media (max-height:380px){html body.w209.inn1{--spk:84px}}",   /* 2026-10-10: 화자 초상 1.5배, 대사창 위로 조금 나오게(창 높이·폭·글자 크기는 그대로) */
   "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt{position:relative!important;padding-left:calc(var(--spk) + 26px)!important;min-height:82px!important;box-sizing:border-box!important}",
   "html body.w209.inn1 #vnbox .vtxt .spk9{position:absolute;left:12px;bottom:8px;width:var(--spk);height:var(--spk);border-radius:10px;overflow:hidden;background:#2B2130;box-shadow:0 0 0 2px #C9A96A,0 4px 10px rgba(0,0,0,.35);z-index:2}",
   "html body.w209.inn1 #vnbox .vtxt .spk9 img{width:100%;height:100%;image-rendering:auto;display:block}",
   "html body.w209.inn1 #vnbox .vtxt .spk9.none{display:none}html body.w209.inn1 #vnbox .vtxt .spk9.sil img{display:none}",
   "html body.w209.inn1 #vnbox .vtxt .spk9.sil{background:radial-gradient(circle at 50% 38%,rgba(18,22,40,.9) 0 22%,transparent 23%),radial-gradient(ellipse 46% 30% at 50% 100%,rgba(18,22,40,.9) 0 98%,transparent 100%),rgba(255,246,224,.07)}",
   "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt .plate{left:calc(var(--spk) + 22px)!important}",
   "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt .nx{position:absolute!important;right:14px!important;bottom:8px!important;left:auto!important;top:auto!important;margin:0!important}",
   "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt,html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt #dtxt,html body.w209.inn1 #dlgveil #vnbox .vband.bot.narr .vtxt .txt{text-align:left!important;justify-content:flex-start!important;align-items:flex-start!important}",
   "html body.w209.inn1 .fstalk .tpanel:not(:has(.topic)){display:none!important}",
   ".arr10{position:fixed;z-index:45;left:50%;top:18%;transform:translateX(-50%);display:flex;align-items:center;gap:14px;pointer-events:none;animation:arr10 1.7s ease-out forwards;white-space:nowrap}",
   ".arr10 b{font:400 var(--t-head,19px)/1.2 var(--display,Galmuri11,sans-serif);font-size:24px;color:#FFF6E0;letter-spacing:.08em;text-shadow:0 2px 0 rgba(0,0,0,.55),0 0 12px rgba(0,0,0,.45)}",
   ".arr10 .ln{display:block;width:56px;height:1px;background:linear-gradient(90deg,rgba(255,230,170,0),rgba(255,230,170,.9),rgba(255,230,170,0))}",
   "@keyframes arr10{0%{opacity:0}15%{opacity:1}75%{opacity:1}100%{opacity:0}}",
   "html body.w209.inn1 mark.kw,html body.w209.inn1 .vband mark.kw,html body.w209.inn1:not(.ds-mc) .vband:not(.narr) mark.kw{color:inherit!important;background:none!important;font-weight:inherit!important;padding:0!important}",   /* 장소·시각 강조(빨강+노랑 밑줄) 없앰 */
   "html body.w209.inn1 .crec2 .cr-det{overflow-y:auto!important;overscroll-behavior:contain}html body.w209.inn1 .crec2 .cr-det .cr-tx{padding-bottom:40px!important}",   /* 긴 증거 글이 아래 단추에 가려 잘리던 것: 상세 칸 안에서 스크롤 */
   ".crec2 .orig9{margin:4px 0;font-size:var(--t-cap,12px);color:#5A4A36}.crec2 .orig9 summary{cursor:pointer;color:#8A5A2A;min-height:28px;line-height:28px}.crec2 .orig9 p{margin:2px 0 0;line-height:1.5}",
   /* 2026-10-10: 증언 상세에서 질문 줄과 답 줄이 같은 칸에 겹쳐 흐리게 보이던 문제 → 질문 2행, 답 3행 */
   "html body.w209.inn1 .crec2 .cr-det .cr-tx>.cr-q{grid-row:2!important;margin:0!important;border-bottom:0!important;padding-bottom:0!important}html body.w209.inn1 .crec2 .cr-det .cr-tx>.cr-a{grid-row:3!important}",
   /* 별표(중요 표시)는 쓰지 않는다 */
   "html body.w209.inn1 .crec2 #crpin,html body.w209.inn1 .evfil [data-evf=\"pin\"]{display:none!important}",
   /* 2026-10-10: '줄기'(사건 줄기) 기능은 1장에서 동작하지 않아 메뉴에서 뺀다 */
   "html body.w209.inn1 #w209rail [data-w=\"spine\"],html body.w209.inn1 #w209more [data-w=\"spine\"]{display:none!important}",
   /* 증언 카드·기록 증언에는 다람 수첩을 넣지 않는다(글이 너무 길어짐) */
   "html body.w209.inn1 #ov .modal.testi9 .soft,html body.w209.inn1 .crec2.testi9 .dmemo{display:none!important}",
   "#innppl ul{margin:4px 0 0;padding:0;list-style:none}#innppl li{font-size:var(--t-cap,12px);line-height:1.45;margin-top:3px}#innppl li b{display:block;color:#3D5E45;font-weight:700}#innppl .no{color:#8A7A5A!important}"
  ].join("\n");document.head.appendChild(css);

  /* ==== 2026-10-09 3차: 전환 플래시·흔들림 정리, 조사 체크 표시, 인물 탭, 인물 연출 ==== */
  /* (1) 장면 속 주민 전신 경로(엔진 F 모듈이 처음부터 이 그림을 쓴다: patches/18_ui_flash.py) */
  window.__innBody=function(k){if(!inn())return null;return {innma:"art/ch1/cast/innma-neutral-v5.png",seryeon:SER_SCENE,doto:DOTO,karo:"art/ch1/cast/karo-front.png",geokkuri:"art/ch1/cast/bami-front.png",det1:"art/ch1/cast/daram-front.png",nabi:"art/ch1/cast/nabi-front.png"}[k]||null};
  /* (2) 장면 제목 띠가 나올 때마다 화면 전체가 흔들리던 것(배너 → quake) 제거. 회의·대결의 '헛짚었다' 같은 판정 연출의 흔들림은 둔다 */
  var lastBan=-1e9;
  try{var _bn9=banner;banner=function(){if(inn())lastBan=performance.now();return _bn9.apply(this,arguments)}}catch(e){}
  try{var _qk9=quake;quake=function(){if(inn()&&performance.now()-lastBan<3500&&!document.querySelector("body>.rt .flash,.flash,.shout"))return;return _qk9.apply(this,arguments)}}catch(e){}
  /* 도착 연출(2026-10-10): 방에 도착하는 순간 한 번만, 화면 위쪽 가운데에 큰 장소 이름과 얇은 선이 잠깐 떴다 사라진다(흔들림 없음). 상단 상시 위치 표시는 그대로 */
  var ARR=null,arrT=0;
  try{var _pc9=placeCard;placeCard=function(){if(!inn())return _pc9.apply(this,arguments);document.querySelectorAll(".placecard").forEach(function(e){e.remove()});
   var l=loc();if(!l)return;var nm=SHORT[l.id]||l.name;clearTimeout(arrT);if(ARR)ARR.remove();ARR=document.createElement("div");ARR.className="arr10";ARR.setAttribute("role","status");
   ARR.innerHTML='<span class="ln"></span><b></b><span class="ln"></span>';ARR.querySelector("b").textContent=nm;B.appendChild(ARR);arrT=setTimeout(function(){if(ARR){ARR.remove();ARR=null}},1700)}}catch(e){}
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
  function drawMarks(){var L1=document.getElementById("innmk9");if(L1)L1.remove();return;/* 관찰 자리 표시는 쓰지 않는다(누른 곳과 다른 자리에 \"확인\" 상자가 생겨 혼란, 2026-10-10) */try{var sc=document.getElementById("bigscene"),L0=document.getElementById("innmk9");if(!sc||!inn()||G.tab!=="scene"||dl()||document.querySelector("#ov .modal,.crec2,#wmap")){if(L0)L0.innerHTML="";return}var l=loc(),list=l&&OBS[l.id],seen=l&&SEEN[l.id];var lay=document.getElementById("innmk9");
    if(!list||!seen){if(lay)lay.remove();return}if(!lay){lay=document.createElement("div");lay.id="innmk9";B.appendChild(lay)}
    var sv=sc.querySelector("svg[data-inn-world]")||sc.querySelector("svg[data-bg]")||sc.querySelector("svg"),m=sv&&sv.getScreenCTM&&sv.getScreenCTM(),br=sc.getBoundingClientRect();if(!m)return;var h="";
    Object.keys(seen).forEach(function(i){var r=list[i];if(!r)return;var p=sv.createSVGPoint();p.x=r[0]+r[2]/2;p.y=r[1]+Math.min(r[3]/2,40);var q=p.matrixTransform(m);if(q.x>br.left-4&&q.x<br.right+4)h+='<i style="left:'+Math.round(q.x)+'px;top:'+Math.round(q.y)+'px">확인</i>'});
    if(lay.innerHTML!==h)lay.innerHTML=h}catch(e){}}

  /* (8) 기록 안 '인물' 탭: 만난 사람만, 이미 나온 정보(이름·하는 일·이 여관과의 관계)와 직접 물어 들은 말만. 새 설정·스포일러 없음 */
  var ROLE={innma:["여관 주인","이 여관을 꾸려 가는 토끼 할머니"],seryeon:["외지 손님","어젯밤 이 여관에 묵은 손님"],nabi:["여관 일을 돕는 고양이","여관에서 일한다"],geokkuri:["겨울 장기 투숙객","이 여관 2층에 겨울 동안 묵는다"],
   doto:["투숙객","여관 2층 방에 묵는다"],buri:["장치공","여관 일을 손봐 준다"],wanggu:["마을 자경단장","주민 규약을 지키게 하고 회의를 기록한다"],karo:["마차 마부","우리를 태우고 마을에 왔다"]};
  var ORDER=["innma","nabi","seryeon","buri","wanggu","karo","geokkuri","doto"];
  /* 아빠·다람은 늘 맨 앞에(기본 정보만, 증언 없음) */
  var SELF=[["det0","다돌 (36)","탐정 · 다람의 아빠","다람과 함께 마차를 타고 와서 이 여관에 묵는 손님","art/ch1/father/father-profile-128.png?v=n4"],["det1","다람 (11)","탐정 · 아빠의 딸","아빠와 함께 이 여관에 묵는 손님","art/ch1/daram-v4/daram-idle-profile.png"]];
  function metMark(){try{if(!inn()||!dl())return;var ln=DL.lines[DL.i];var w=ln&&ln[0];if(!ROLE[w])return;var pl=document.querySelector("#vnbox .plate");if(pl&&/\?\?\?/.test(pl.textContent))return;G.beats=G.beats||{};if(!G.beats["inn_met_"+w]){G.beats["inn_met_"+w]=1}}catch(e){}}
  function metList(){var b=G.beats||{},pro=!!b.inn_pro;return ORDER.filter(function(k){if(b["inn_met_"+k])return true;if(k==="geokkuri")return G.found.indexOf("C07")>=0;if(k==="doto")return G.found.indexOf("C08")>=0;return pro&&["innma","nabi","seryeon","buri","wanggu","karo"].indexOf(k)>=0})}
  var PP=null;function pplClose(){if(PP){PP.remove();PP=null}}
  /* 인물별 대사 기록(인물 탭 [대사 열기]용): 화면에 나온 대사 줄을 화자별로 G.said9에 쌓는다(속마음·서술·아빠/다람 제외, 저장 데이터에 같이 남음) */
  function sayLog(){try{if(!inn()||typeof DL==="undefined"||!DL||!DL.lines)return;var ln=DL.lines[DL.i];if(!ln)return;var key=DL.i+"|"+DL.lines.length;if(sayLog.d===DL&&sayLog.k===key)return;sayLog.d=DL;sayLog.k=key;
    var w=Array.isArray(ln)?ln[0]:ln.w,t=String((Array.isArray(ln)?ln[1]:ln.t)||"").replace(/[{}]/g,"").replace(/\s*\n\s*/g," ").trim();if(!w||!PROF[w]||w==="det1"||!t||/^\(/.test(t))return;
    var S=G.said9=G.said9||{},a=S[w]=S[w]||[];if(a.indexOf(t)>=0)return;a.push(t);if(a.length>300)a.shift()}catch(e){}}
  setInterval(sayLog,120);
  /* 더보기: 대사 중에도 열리게(대사 중 클릭이 두 번 전달돼 열렸다 바로 닫히던 것) — 문서 캡처 단계에서 한 번만 열고 닫는다 */
  document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("#w209rail [data-more]");if(!b||!inn())return;e.preventDefault();e.stopImmediatePropagation();
    var r=document.getElementById("w209rail");if(!r)return;var now=performance.now();if(now-(b.__t||0)<250)return;b.__t=now;r.classList.toggle("more");try{SFX.tap()}catch(x){}},true);
  /* QA 저장칸 표시(?qa=1 / ?slot=이름) */
  try{if(window.__QASLOT){var qb=document.createElement("div");qb.id="qaslot9";qb.textContent="QA 저장칸 · "+window.__QASLOT;qb.style.cssText="position:fixed;left:6px;bottom:6px;z-index:3000;padding:2px 8px;border-radius:6px;background:rgba(162,59,42,.85);color:#fff;font:12px Galmuri11,monospace;pointer-events:none";(document.body||document.documentElement).appendChild(qb)}}catch(e){}
  /* 2026-10-10 v2: 주머니·이불을 본 뒤에도 침대 밑을 안 봤으면, 다음 할 일은 안 쓰는 방 침대 밑 */
  try{var _nsx=nextStep;nextStep=function(c){var r=_nsx.apply(this,arguments);try{if(!inn()||!G.beats||!G.beats.inn_pro||G.beats.inn_final||!r)return r;
    if((G.obsSeen||[]).indexOf("o_under")>=0||G.found.indexOf("C04")>=0||G.found.indexOf("C01")<0||G.found.indexOf("C02")<0)return r;var bi=-1;c.locations.forEach(function(l,i){if(l.id==="bed13")bi=i});if(bi<0)return r;
    setTimeout(function(){try{window.__pointAt&&window.__pointAt('[data-obs="o_under"]')}catch(e){}},900);
    return {say:"아빠, 침대 밑이 너무 어두워. 안쪽까지 한번 들여다보자.",tab:"scene",loc:bi}}catch(e){}return r}}catch(e){}
  /* 독립 QA ④: 증거로 이어지는 관찰(찻주전자, 햇빛 든 머리판, 숫자 자물쇠)이 남았는데 '증거 수집 완료'로 뜨던 것 → '살펴볼 곳 N군데 남음' */
  var KEYOBS={o_under:"C04",o_inn_head2:"C11",o_inn_lock:"C11"};
  function statusFix(){try{var sm=document.querySelector(".stagebar .scap small");if(!sm||!/^증거 수집 완료/.test(sm.textContent))return;var sc=document.getElementById("bigscene");if(!sc)return;
    var k=[].slice.call(sc.querySelectorAll("[data-obs]")).filter(function(b){var id=b.dataset.obs,cs=getComputedStyle(b);return KEYOBS[id]&&G.found.indexOf(KEYOBS[id])<0&&cs.visibility!=="hidden"&&(G.obsSeen||[]).indexOf(id)<0}).length;
    if(!k)return;var m=sm.textContent.match(/관찰\s*(\d+)/);sm.textContent="살펴볼 곳 "+(m?+m[1]:k)+"군데 남음"}catch(e){}}
  setInterval(statusFix,300);
  /* 독립 QA ③: 넓은 화면(1180)에서 회의 말풍선이 왼쪽 위 상태판(설득력·시각·득표)을 가리던 것 → 겹치면 상태판 아래로 내린다 */
  function bubFix(){try{var b=document.querySelector("body>.rt .rt-bub");if(!b)return;var hs=["#rtgtop","#rtgtal","#rtgclk",".rt-clock"].map(function(q){return document.querySelector(q)}).filter(Boolean);if(!hs.length)return;
    var br=b.getBoundingClientRect(),dy=0;hs.forEach(function(h){var r=h.getBoundingClientRect();if(!r.width)return;if(br.left<r.right&&br.right>r.left&&br.top<r.bottom&&br.bottom>r.top)dy=Math.max(dy,r.bottom+6-br.top)});
    if(dy>0){var t0=parseFloat(b.style.top);if(isNaN(t0))t0=br.top;b.style.top=(t0+dy)+"px"}}catch(e){}}
  setInterval(bubFix,250);
  function pplOpen(){pplClose();var c=CASES[G.ci],ks=metList(),h='<div class="pin"><div class="phd"><b>인물</b><small>만난 사람 '+(ks.length+SELF.length)+'명 · [대사 열기]로 들은 말 보기</small><button type="button" data-x="1" aria-label="닫기">×</button></div><div class="pls">';
   SELF.forEach(function(x){h+='<section class="pc self"><div class="pf"><img alt="" src="'+x[4]+'"></div><div class="pt"><h4>'+esc(x[1])+'</h4><small>'+esc(x[2])+'</small><p>'+esc(x[3])+'</p></div></section>'});
   ks.forEach(function(k){var nm=({innma:"복례 할머니"})[k]||(CAST[k]&&CAST[k].name)||k,r=ROLE[k]||["",""],said=((c.talk&&c.talk[k])||[]).filter(function(t){return G.asked.indexOf(t.id)>=0&&t.q});
    var face="";try{face=PROF[k]?'<img alt="" data-k="'+k+'" src="'+(k==="wanggu"?NV2+"neoul-default-profile.png":AP+PROF[k]+'/profile.png?v=e4')+'">':pf(k,"neutral")}catch(e){}
    h+='<section class="pc"><div class="pf">'+face+'</div><div class="pt"><h4>'+esc(nm)+'</h4><small>'+esc(r[0])+'</small><p>'+esc(r[1])+'</p>'+
     (function(){var n=((G.said9||{})[k]||[]).length+said.length;return n?'<button type="button" class="e9b plog" data-k="'+k+'">대사 열기 <i>'+n+'</i></button>':'<p class="no">아직 나눈 대화가 없어요.</p>'})()+'</div></section>'});
   h+='</div></div>';PP=document.createElement("div");PP.id="innppl";PP.setAttribute("role","dialog");PP.setAttribute("aria-label","인물");PP.innerHTML=h;B.appendChild(PP);
   /* 초상 파일을 못 받으면(배포 직후 캐시 등) 깨진 그림 대신 같은 인물의 작은 얼굴로 */
   [].slice.call(PP.querySelectorAll(".pf img[data-k]")).forEach(function(im){function fb(){var k=im.dataset.k,w=im.parentNode;if(!w)return;try{w.innerHTML=pf(k,"neutral")}catch(e){w.innerHTML=""}}im.addEventListener("error",fb);if(im.complete&&!im.naturalWidth)fb()});
   /* 2026-10-10 사용자: 인물 카드는 기본 정보만, [대사 열기]를 누르면 그 인물에게 들은 말 기록(물어본 질문의 답 + 대화 중 그 인물이 한 말, 나온 순서) */
   PP.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".plog");if(!b)return;e.stopPropagation();var k=b.dataset.k,nm=({innma:"복례 할머니"})[k]||(CAST[k]&&CAST[k].name)||k,c=CASES[G.ci];
     var qa=((c.talk&&c.talk[k])||[]).filter(function(t){return G.asked.indexOf(t.id)>=0&&t.q}).map(function(t){return [t.q,String(t.a||"").replace(/[{}]/g,"")]});
     var lines=((G.said9||{})[k]||[]).slice(),seen={};qa.forEach(function(x){seen[x[1]]=1});lines=lines.filter(function(t){return !seen[t]});
     pop9(nm+"에게 들은 말",qa.concat(lines))},true);
   PP.addEventListener("click",function(e){var t=e.target;if(t===PP||(t.closest&&t.closest("[data-x]"))){e.stopPropagation();try{SFX.tap()}catch(x){}pplClose()}})}
  function pplTab(){try{var r=document.querySelector(".crec2");if(!r||!inn()){pplClose();return}if(r.querySelector('[data-crt="ppl9"]'))return;var t=r.querySelector('[data-crt="t"]');if(!t)return;
    var b=document.createElement("button");b.type="button";b.className=t.className.replace(/\bon\b/,"");b.dataset.crt="ppl9";b.textContent="인물 "+metList().length;b.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();try{SFX.page()}catch(x){}pplOpen()},true);t.parentNode.insertBefore(b,t.nextSibling)}catch(e){}}

  /* (9) 인물 연출: 대화 화면에 들어올 때 살짝 떠오르고, 같은 인물의 표정 그림이 바뀌면 작게 들썩인다 */
  function doneMarks(){try{var W9=window.__innWorld,sc=document.getElementById("bigscene"),im=sc&&sc.querySelector("svg[data-inn-world]");if(!W9||!im)return;var k=im.dataset.innWorld,c=W9.camera(k),A=W9.anchors&&W9.anchors[k==="storage"?"bed13":k];if(!A)return;
    sc.querySelectorAll(".hot.done[data-done]").forEach(function(e){var r=A[e.dataset.done];if(!r)return;var x=(r[0]-c.x)*c.scale,y=(r[1]-c.y)*c.scale;e.style.setProperty("left",x+"px","important");e.style.setProperty("top",y+"px","important")})}catch(e){}}
  /* 증거를 주는 질문(C12 등)은 답이 끝난 뒤 질문 화면이 다시 그려지지 않아 읽음 체크가 안 붙고 같은 질문이 또 눌리던 문제: 들은 질문이 남아 있으면 한 번 다시 그린다 */
  function topicSync(){try{if(dl()||G.tab!=="talk"||document.querySelector("#ov .modal,.cutin,.crec2"))return;var stale=[].slice.call(document.querySelectorAll(".fstalk .topic[data-ask]")).some(function(t){return G.asked.indexOf(t.dataset.ask)>=0});if(stale)render()}catch(e){}}
  /* 증거 획득 창: 글은 오른쪽 칸 안에서만 스크롤하고, 확인 단추는 그 아래 별도 줄(긴 증언에서도 글을 가리지 않음) */
  /* 2026-10-10 사용자 "증거가 너무 길다 · 다람 메모는 옵션으로 · UI가 직관적이어야" (역전재판식 참고 화면):
     증거 획득 창 = 왼쪽 그림 / 노란 띠 제목 / 짧은 한두 줄 / [자세히 보기]·[다람 메모]는 눌러야 열림 / 아래 "《이름》을 기록에 넣었다." + 확인 */
  function josa(w,a,b){var c=(w||"").replace(/[^가-힣0-9]/g,"").slice(-1),k=c.charCodeAt(0);if(k>=0xAC00&&k<=0xD7A3)return (k-0xAC00)%28?a:b;return "013678".indexOf(c)>=0?a:b}
  function evOf(name){var E=(window.EP1INN||{}).EV||{},id=null;Object.keys(E).forEach(function(k){if(E[k].name===name||E[k].full===name)id=k});return id}
  function fixedOf(x){try{return !!(x.fixBeat&&G.beats&&G.beats[x.fixBeat])}catch(e){return false}}
  function cardWrap(){try{var m=document.querySelector("#ov .modal");if(!m||!inn()||m.classList.contains("ev9"))return;var ic=m.querySelector(":scope>.foundic,:scope>.bigic"),kk=m.querySelector(":scope>.kicker"),h3=m.querySelector(":scope>h3");
    if(!ic||!kk||!h3||!/증거 (발견|획득)/.test(kk.textContent))return;if(!m.dataset.found){clearTimeout(cardWrap.t);cardWrap.t=setTimeout(cardWrap,50);return}var ok=m.querySelector(":scope>#okfind");var id=evOf(h3.textContent.trim()),E=(window.EP1INN||{}).EV||{},x=id&&E[id];
    var fx=x&&fixedOf(x),short=x?(fx&&x.desc2?x.desc2:x.desc):"",det=x?(fx&&x.detail2?x.detail2:(x.detail||"")):"",memo="";
    var T={C03:1,C07:1,C12:1,C13:1};try{if(!T[id]&&window.__memoOf)memo=window.__memoOf(CASES[G.ci],id)||""}catch(e){}
    var at=m.querySelector(".found-at"),place=at?at.textContent:"",who=(kk.textContent.split("·")[1]||"").trim();
    if(!short){var p0=m.querySelector(":scope>p");short=p0?p0.textContent:""}
    var nm=h3.textContent.trim();m.classList.add("ev9");if(/증거 획득/.test(kk.textContent)){try{SFX.found()}catch(e){}}   /* 증언 카드는 효과음이 없던 것 */
    var card=document.createElement("div");card.className="e9card";card.innerHTML='<div class="e9ic"></div><div class="e9tx"><div class="e9k"></div><h3 class="e9t"></h3><p class="e9d"></p><div class="e9opt"></div><div class="e9pan" hidden></div></div>';
    card.querySelector(".e9ic").appendChild(ic);card.querySelector(".e9k").textContent="증거 발견"+(who?" · "+who:"");card.querySelector(".e9t").textContent=nm;card.querySelector(".e9d").textContent=short;
    var opt=card.querySelector(".e9opt"),pan=card.querySelector(".e9pan");
    function addB(lbl,fill){var b=document.createElement("button");b.type="button";b.className="e9b";b.textContent=lbl;b.addEventListener("click",function(ev){ev.stopPropagation();var on=b.classList.contains("on");opt.querySelectorAll(".e9b").forEach(function(o){o.classList.remove("on")});if(on){pan.hidden=true;return}b.classList.add("on");pan.innerHTML="";fill(pan);pan.hidden=false;try{SFX.select()}catch(e){}});opt.appendChild(b)}
    if(det&&det!==short||place)addB("자세히 보기",function(P){if(place){var a=document.createElement("small");a.textContent=place;P.appendChild(a)}if(det){var q=document.createElement("p");q.textContent=det;P.appendChild(q)}});
    if(memo)addB("다람 메모",function(P){var q=document.createElement("p");q.className="e9memo";q.textContent=memo;P.appendChild(q)});
    var add=document.createElement("div");add.className="e9add";add.textContent="《"+nm+"》"+josa(nm,"을","를")+" 기록에 넣었다.";
    var foot=document.createElement("div");foot.className="e9foot";foot.appendChild(add);if(ok)foot.appendChild(ok);
    [].slice.call(m.children).forEach(function(ch){ch.remove()});m.appendChild(card);m.appendChild(foot)}catch(e){}}
  try{new MutationObserver(cardWrap).observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
  var lastK="",lastSrc="";function bump(){try{var i=document.querySelector(".fstalk .tstage .tfig img");if(!i)return;var k=i.dataset.k,s=i.getAttribute("src");if(k===lastK&&s!==lastSrc){i.classList.remove("bump9");void i.offsetWidth;i.classList.add("bump9")}lastK=k;lastSrc=s}catch(e){}}

  try{new MutationObserver(function(){drawMarks()}).observe(document.documentElement,{subtree:true,attributes:true,attributeFilter:["viewBox"]})}catch(e){}

  /* ==== 통합 아트(2026-10-09): 장소 인물 행동 포즈를 배경과 같은 좌표·같은 팬 변환으로 ====
     배경 svg 안에 원본 픽셀 좌표로 넣는다(식당 2048x768, 부엌 1774x887, 복도·도토 방 1672x941). 누르는 영역은 그림 자리에 맞춘 기존 인물 단추 */
  var AP="art/ch1/action-poses/";
  window.__innPose=function(k){try{if(!inn())return null;if(k==="buri")return AP+"buri/dialogue.png";if(k==="wanggu")return "art/ch1/neoul-v2/neoul-default-dialogue.png";   /* 너울 v2: 옛 주황 조끼 고해상 그림 대신 */   /* 2026-10-10 "부엉이 시선은 플레이어로": 통합 아트 후보(정면 시선) */
   var b=G.beats||{};if(!b.inn_pro||b.inn_final)return null;var lid=(loc()||{}).id;
    if(k==="seryeon")return AP+"seryeon/dialogue.png";if(k==="innma"&&lid==="dining")return AP+"grandma/dialogue.png";if(k==="geokkuri"&&lid==="hall")return AP+"bami/dialogue.png";
    if(k==="nabi"&&lid==="kitchen")return AP+"nabi/dialogue.png";if(k==="doto"&&lid==="dotoroom")return AP+"doto/dialogue.png";}catch(e){}return null};
  /* [인물, 파일, x, y, 폭, 높이] — 식당은 통합 아트 배치표 그대로(세련 735,283 / 할머니는 좌우 보기 반대쪽 끝 부엌문 앞 바닥 579에 발), 부엌 나비는 식당 대비 가구 배율 1.6(의자 좌석 높이 비교) */
  var WN={dining:[["innma",AP+"grandma/npc.png",1800,303,162,276],["seryeon",AP+"seryeon/npc.png",735,283,241,361]],
   kitchen:[["nabi",AP+"nabi/npc.png",830,190,339,504],["buri",AP+"buri/npc.png",1380,297,250,397]],
   front:[["wanggu","art/ch1/neoul-v2/neoul-default-full240.png",1120,240,260,347]],
   plaza:[["karo",AP+"karo/npc.png",1130,420,254,432]],
   hall:[["geokkuri",AP+"bami/npc.png",100,25,424,429]],
   dotoroom:[["doto",AP+"doto/npc.png",690,161,472,533,1]]};
  var OCC={dining:[["art/ch1/fg/dining_tabletop_occluder.png",858,427,906,86]]};
  var WPX={dotoroom:[["art/ch1/props/doto_room/prop_weather_notebook_open_rgba.png",1106,450.45,164,28.55],["art/ch1/props/doto_room/prop_bookstack_rgba.png",1309.5,408.7,105,53.3],["art/ch1/props/doto_room/prop_pencilcup_rgba.png",1435,396.4,30,65.6]]};
  function svgOf(sc){return sc&&(sc.querySelector("svg[data-inn-world]")||sc.querySelector("svg[data-bg]"))}
  function img(sv,f,x,y,w,h,cls){var im=document.createElementNS("http://www.w3.org/2000/svg","image");im.setAttribute("class",cls);im.setAttribute("href",f);im.setAttribute("x",x);im.setAttribute("y",y);im.setAttribute("width",w);im.setAttribute("height",h);im.setAttribute("preserveAspectRatio","none");im.setAttribute("style","image-rendering:pixelated;pointer-events:none");sv.appendChild(im);return im}
  /* 인물 그림 알파 마스크(같은 출처 이미지). 읽지 못하면 그림 가운데 기둥(가로 40%)만 인정 */
  var MASK={};
  function maskOf(src){if(!src)return {};if(MASK[src])return MASK[src];var o={ready:false};MASK[src]=o;var im=new Image();
    im.onload=function(){try{var c=document.createElement("canvas");c.width=im.naturalWidth;c.height=im.naturalHeight;var x=c.getContext("2d");x.drawImage(im,0,0);var dd=x.getImageData(0,0,c.width,c.height).data,a=new Uint8Array(c.width*c.height);for(var i=0;i<a.length;i++)a[i]=dd[i*4+3];o.a=a;o.w=c.width;o.h=c.height;o.ready=true}catch(e){o.bad=true}};
    im.onerror=function(){o.bad=true};im.src=src;return o}
  function alphaAt(im,x,y,R){var r=im.getBoundingClientRect();if(!r.width||x<r.left||x>r.right||y<r.top||y>r.bottom)return -1;var M=maskOf(im.getAttribute("href")),u=(x-r.left)/r.width,v=(y-r.top)/r.height;
    if(!M.ready)return (Math.abs(u-.5)<.2&&v>.06&&v<.97)?255:0;var px=Math.floor(u*M.w),py=Math.floor(v*M.h),best=0;
    for(var dy=-R;dy<=R;dy++)for(var dx=-R;dx<=R;dx++){var X=px+dx,Y=py+dy;if(X<0||Y<0||X>=M.w||Y>=M.h)continue;var a=M.a[Y*M.w+X];if(a>best)best=a}return best}
  window.__innMask=function(){var o={};Object.keys(MASK).forEach(function(k){o[k]=MASK[k].ready?"ok":MASK[k].bad?"bad":"wait"});return o};
  function npcHit(sc,x,y){try{var sv=svgOf(sc);if(!sv)return null;
    /* 앞가림(식탁 상판 등)의 불투명 부분을 누르면 그 뒤 인물은 열지 않는다 */
    var occ=[].slice.call(sv.querySelectorAll("image.wo9")).some(function(im){return alphaAt(im,x,y,0)>60});if(occ)return null;
    var hit=null;[].slice.call(sv.querySelectorAll("image.wn9")).reverse().some(function(im){var bt=sc.querySelector('.npc.w9[data-npc="'+im.dataset.k+'"]');if(!bt||bt.dataset.nohit)return false;
      if(alphaAt(im,x,y,3)>60){hit=bt;return true}var tg=bt.querySelector("span");if(tg){var r=tg.getBoundingClientRect();if(r.width&&x>=r.left-4&&x<=r.right+4&&y>=r.top-4&&y<=r.bottom+4){hit=bt;return true}}return false});return hit}catch(e){return null}}
  window.__innNpcHit=function(x,y){var b=npcHit(document.getElementById("bigscene"),x,y);return b?b.dataset.npc:""};
  function worldNpc(){try{var sc=document.getElementById("bigscene"),sv=svgOf(sc);if(!sv||!inn()||G.tab!=="scene"){return}var b=G.beats||{};if(!b.inn_pro||b.inn_final)return;var lid=(loc()||{}).id,L=WN[lid]||[];var key=lid+"|"+L.length;   /* 나비는 너울을 부르러 갔다가, 찻주전자 발견 뒤 부엌에 돌아와 있다(찻주전자를 본 사람은 부녀뿐) */
    if(sv.dataset.wn9!==key){[].slice.call(sv.querySelectorAll("image.wn9,image.wo9,image.wp9")).forEach(function(e){e.remove()});
     (WPX[lid]||[]).forEach(function(p){img(sv,p[0],p[1],p[2],p[3],p[4],"wp9")});
     L.forEach(function(n){var e=img(sv,n[1],n[2],n[3],n[4],n[5],"wn9");e.dataset.k=n[0];maskOf(n[1])});
     (OCC[lid]||[]).forEach(function(o){img(sv,o[0],o[1],o[2],o[3],o[4],"wo9");maskOf(o[0])});sv.dataset.wn9=key}
    /* 인물 단추를 그림 자리로(누름 영역 = 그림 사각형, 최소 48px). 옛 전신 그림은 숨긴다 */
    var m=sv.getScreenCTM(),br=sc.getBoundingClientRect();if(!m)return;
    L.forEach(function(n){var bt=sc.querySelector('.npc[data-npc="'+n[0]+'"]');if(!bt)return;bt.classList.add("w9");
     var p1=sv.createSVGPoint();p1.x=n[2];p1.y=n[3];var a=p1.matrixTransform(m);var p2=sv.createSVGPoint();p2.x=n[2]+n[4];p2.y=n[3]+n[5];var z=p2.matrixTransform(m);
     var w=Math.max(48,z.x-a.x),h=Math.max(48,z.y-a.y),l=a.x-br.left,t=a.y-br.top;
     [["left",l+"px"],["top",t+"px"],["width",w+"px"],["height",h+"px"],["transform","none"],["margin","0"]].forEach(function(d){bt.style.setProperty(d[0],d[1],"important")})});
    }catch(e){}}   /* 2026-10-10 v2 "도토 클릭해도 말 안 걸어짐": 도토에게도 질문이 생겨 단추를 켠다(일지 지점은 따로) */
  var PROF={det1:"daram",innma:"grandma",geokkuri:"bami",nabi:"nabi",karo:"karo",seryeon:"seryeon",wanggu:"neoul",doto:"doto",buri:"buri"};

  /* ==== 대화 UI v3(2026-10-09 확정): 대사창 안 왼쪽에 작은 화자 초상(누구 말인지 표시용, 표정·행동은 장면 인물이 맡음) ====
     초상은 통합 아트 profile.png(9명). 아빠는 공개된 얼굴이 없으므로 중립 실루엣. 지문(회색)은 초상 없이 같은 글 위치 */
  /* 2026-10-10 깜빡임 수정: 엔진은 대사마다 대사창 노드를 새로 만든다. 예전엔 초상·여백을 최대 60ms 뒤에 붙여 창 높이·글 위치가 한 프레임씩 튀었다.
     이제 여백·높이는 CSS로 늘 같고, 초상은 같은 img 요소 하나를 새 창으로 옮겨 붙인다(새로 받지 않음). 노드가 생기는 즉시(그리기 전, MutationObserver) 처리 */
  var SPK=document.createElement("span");SPK.className="spk9";SPK.setAttribute("aria-hidden","true");SPK.innerHTML="<img alt=''>";var SPKIMG=SPK.firstChild,SPKC={};
  var FV="art/ch1/father/father-v5-",V4="art/ch1/daram-v4/",NV2="art/ch1/neoul-v2/";
  ["default-smile","finger-base","finger-raised","pose-thinking","pose-surprised","pose-sheepish"].map(function(n){return FV+n+"-speaker128.png"})
   .concat(["idle","memo","joy","flustered","held-anger","comic-anger"].map(function(n){return V4+"daram-"+n+"-speaker128.png"}))
   .concat(["default","admonish","angry","sheepish"].map(function(n){return NV2+"neoul-"+n+"-speaker128.png"})).forEach(function(f){var im=new Image();im.src=f});
  /* 작은 얼굴(질문 목록·대화 화면·기록 등 pf)도 새 외형으로: 아빠 v5·다람 v4·너울 v2. 옛 갈색 모자 다람·주황 조끼 너울이 섞여 뜨지 않게 */
  try{var _pf9=pf;pf=function(k,mood){try{if(inn()&&(k==="det0"||k==="det1"||k==="wanggu")){var m=String(mood||""),f=k==="det0"?"art/ch1/father/father-profile-64.png?v=n4":k==="det1"?V4+"daram-"+String(window.__innDV4?window.__innDV4(m):"idle").replace("idle-t0","idle")+"-64.png":NV2+"neoul-default-64.png";
    return '<svg class="nodot inn-pixel-face" data-face="'+k+'" viewBox="0 0 100 101" aria-hidden="true" style="image-rendering:pixelated"><image href="'+f+'" x="0" y="0" width="100" height="100" style="image-rendering:pixelated"/></svg>'}}catch(e){}return _pf9.apply(this,arguments)}}catch(e){}
  /* 아빠 화자 포즈: 놀람(?! · 설마), 머쓱(죄송·하하·벌금은 내겠), 생각(물음으로 끝나는 속마음), 그 밖은 둥근 미소 기본 */
  function dadPose(t,inner,md){if(/shock|surpr|panic/.test(md)||/\?!|!\?|^(뭐라|설마|네\?|어\?)/.test(t))return "pose-surprised";
   if(/죄송|미안|하하|벌금은 내겠|머쓱|그 말 내일 아침/.test(t))return "pose-sheepish";
   if(inner&&/\?\)?$|^\(?(흠|글쎄)/.test(t))return "pose-thinking";return "default-smile"}
  var DAD="art/ch1/father/father-speaker128.png?v=n4";   /* 2026-10-10 사용자 채택 dadol-profile-daram-matched-v2(father-v6-matched) */   /* 아빠 기본 프로필: 2026-10-09 사용자 확정 정직·따뜻한 얼굴(이전 능청 얼굴은 father-sly-*로 보존, 연결 없음) — 화자 칸에만 */
  function spkSrc(k){return k==="det0"?DAD:(PROF[k]?AP+PROF[k]+"/speaker128.png":"")}
  [DAD].concat(Object.keys(PROF).map(function(k){return AP+PROF[k]+"/speaker128.png"})).forEach(function(f){var im=new Image();im.src=f;SPKC[f]=im;try{im.decode&&im.decode().catch(function(){})}catch(e){}});
  function speaker(){try{if(!inn()||!dl())return;var vt=document.querySelector("#vnbox .vtxt");if(!vt)return;var ln=DL.lines[DL.i]||[],w=ln[0],vb=vt.closest(".vband");
    var inner=vb&&vb.classList.contains("inner");var k=inner?"det0":w;if(SPK.parentNode!==vt)vt.insertBefore(SPK,vt.firstChild);
    var md=String(ln[2]||""),tx=String(ln[1]||"");
    /* 2026-10-10 화자 초상 통일(GPT·사용자): 아빠 v5(둥근 미소 기본 + 생각/놀람/머쓱 + 손가락 2프레임), 다람 v4 6상태, 너울 v2 4상태 — 모두 확정 원본에서 직접 크롭 */
    var f=spkSrc(k),fing=false;
    if(k==="det1")f=V4+"daram-"+String(window.__innDV4?window.__innDV4(md):"idle").replace("idle-t0","idle")+"-speaker128.png";
    else if(k==="wanggu")f=NV2+"neoul-"+(window.__innNeoState?window.__innNeoState(md):"default")+"-speaker128.png";
    else if(k==="det0"){fing=false;f=DAD}   /* 2026-10-10 사용자 "아빠 프로필·대화 프사를 채택한 한 장으로 통일": 옛 v5 포즈·손가락 프레임(다른 얼굴) 연결 해제 */
    var mode=f?"img":"none";if(SPK.dataset.k!==k+"|"+mode){SPK.dataset.k=k+"|"+mode;SPK.className="spk9 "+mode+(k==="det0"?" dad":"")}
    var fk=DL.i+"|"+tx.length;
    if(fing){if(SPK.dataset.fk!==fk){SPK.dataset.fk=fk;SPKIMG.setAttribute("src",FV+"finger-base-speaker128.png");clearTimeout(SPK.__ft);SPK.__ft=setTimeout(function(){if(SPK.dataset.fk===fk)SPKIMG.setAttribute("src",FV+"finger-raised-speaker128.png")},200)}}
    else{if(SPK.dataset.fk){SPK.dataset.fk="";clearTimeout(SPK.__ft)}if(f){if(SPKIMG.getAttribute("src")!==f)SPKIMG.setAttribute("src",f)}else SPKIMG.removeAttribute("src")}
    /* 2026-10-10 작은 연출: 긴장·당황 표정(nervous/shock/worried) 줄에서는 초상 옆으로 땀방울이 조금씩 흐르고, 놀람(shock)·"?!" 줄은 한 번 움찔한다 */
    var fx=/nervous|shock|worried|panic|sweat/.test(md)||/땀/.test(tx)?"sweat":"",jolt=/shock|surprise/.test(md)||/\?!|!\?/.test(tx);
    if(SPK.dataset.fx!==fx){SPK.dataset.fx=fx;var sw=SPK.querySelector(".sw9");if(fx&&!sw){sw=document.createElement("i");sw.className="sw9";SPK.appendChild(sw)}else if(!fx&&sw)sw.remove()}
    var lk=DL.i+"|"+tx.length;if(jolt&&SPK.dataset.jk!==lk){SPK.dataset.jk=lk;SPK.classList.remove("jolt9");void SPK.offsetWidth;SPK.classList.add("jolt9")}
    if(!vt.classList.contains("v3"))vt.classList.add("v3")}catch(e){}}
  try{new MutationObserver(speaker).observe(document.getElementById("ov")||document.body,{childList:true,subtree:true})}catch(e){}
  setInterval(speaker,120);

  /* 기록 증거 상세: '원문 보기'로 축약 전 원문(그대로 보존)을 펼친다 */
  /* 기록 화면의 [자세히 보기]·[다람 메모]: 화면 가운데 쪽지로 띄우고, 누르면 닫힌다(좁은 화면에서 목록에 가려지지 않게 body에 붙인다) */
  function pop9(title,text,onClose){var o=document.getElementById("e9pop");if(o){var f=o._c;o.remove();if(f)try{f()}catch(e){}}if(!title)return;
    o=document.createElement("div");o.id="e9pop";o._c=onClose;o.innerHTML='<div class="e9pc"><b></b><p></p><small>눌러서 닫기</small></div>';o.querySelector("b").textContent=title;
    if(Array.isArray(text)){var ol=document.createElement("ol");ol.className="e9log";text.forEach(function(it){var li=document.createElement("li");if(Array.isArray(it)){var q=document.createElement("em");q.textContent=it[0];li.appendChild(q);li.appendChild(document.createTextNode(it[1]))}else li.textContent=it;ol.appendChild(li)});o.querySelector("p").replaceWith(ol)}else o.querySelector("p").textContent=text;
    o.addEventListener("click",function(e){e.stopPropagation();pop9()});document.body.appendChild(o);try{SFX.select()}catch(e){}}
  setInterval(function(){if(document.getElementById("e9pop")&&!document.querySelector(".crec2,#innppl"))pop9()},400);
  function recDetail(){try{var r=document.querySelector(".crec2");if(!r||!inn())return;var th=r.querySelector(".cr-th.on");var id=th&&th.dataset.crs;var EPX=window.EP1INN||{},x=id&&EPX.EV&&EPX.EV[id];
    var host=r.querySelector(".cr-in");if(!host)return;var box=r.querySelector(".orig9");if(box&&!r.querySelector(".cr-det .cr-tx .orig9")){box.remove();box=null}
    if(!x||!x.detail){if(box)box.remove();return}
    var fixed=false;try{fixed=!!(x.fixBeat&&G.beats&&G.beats[x.fixBeat])}catch(e){}var txt=fixed&&x.detail2?x.detail2:x.detail;
    if(box&&box.dataset.id===id+(fixed?"f":""))return;if(box)box.remove();
    box=document.createElement("div");box.className="orig9";box.dataset.id=id+(fixed?"f":"");var mm="";try{if(!{C03:1,C07:1,C12:1,C13:1}[id]&&window.__memoOf)mm=window.__memoOf(CASES[G.ci],id)||""}catch(e){}box.innerHTML='<div class="e9opt"><button type="button" class="e9b" data-o="d">자세히 보기</button>'+(mm?'<button type="button" class="e9b" data-o="m">다람 메모</button>':'')+'</div>';[].slice.call(box.querySelectorAll(".e9b")).forEach(function(b){b.addEventListener("click",function(ev){ev.stopPropagation();var on=b.classList.contains("on");box.querySelectorAll(".e9b").forEach(function(o){o.classList.remove("on")});if(on){pop9();return}b.classList.add("on");pop9(b.dataset.o==="m"?"다람 메모":"자세히 보기",b.dataset.o==="m"?mm:txt,function(){b.classList.remove("on")})})});
    var tp=r.querySelector(".cr-det .cr-tx>p");if(tp)tp.insertAdjacentElement("afterend",box);else (r.querySelector(".cr-det")||host).appendChild(box)}catch(e){}}

  /* 증언(들은 말) 카드 표시: 증거 획득 창과 기록 상세에서 다람 수첩을 숨기도록 표시만 붙인다 */
  var TESTI={C03:1,C07:1,C12:1,C13:1};
  function testiMark(){try{var m=document.querySelector("#ov .modal");if(m&&m.querySelector(":scope .foundic, :scope>.foundic")){var h=m.querySelector("h3"),E=window.EP1INN||{},id=null;if(h&&E.EV)Object.keys(E.EV).forEach(function(k){if(E.EV[k].name===h.textContent.trim())id=k});m.classList.toggle("testi9",!!(id&&TESTI[id]))}
    var r=document.querySelector(".crec2");if(r){var th=r.querySelector(".cr-th.on"),tid=th&&th.dataset.crs,tab=r.querySelector('[data-crt="t"]');var testi=(tid&&TESTI[tid])||(tab&&/on|true/.test(tab.className+" "+tab.getAttribute("aria-pressed")));r.classList.toggle("testi9",!!testi)}}catch(e){}}
  try{new MutationObserver(testiMark).observe(document.documentElement,{childList:true,subtree:true})}catch(e){}
  window.__innUI9={obs:function(){return window.__innObsLast||""},HK:HK,OBS:OBS};

  /* ==== 2026-10-10 v2 구조 피드백(사용자 승인) ==== */
  /* (1) 위기가 눈앞에: 솜솜을 찾은 뒤 식당에 처음 들어서면, 세련이 계약서와 펜을 펴 두고 할머니는 동전 깡통을 센다(한 번) */
  var STAKES=[["narr","(식당 공기가 아까와 다르다.)"],["seryeon","할머니. 회의가 끝나면 이백 냥을 물어내시든지, 여기 서명하시든지 둘 중 하나입니다.","smug"],
   ["seryeon","미리 펴 두는 겁니다. 정오엔 바쁠 테니까요.","smug"],
   ["narr","(식탁 위에 계약서와 펜, 인주가 가지런히 놓였다. 할머니는 대답 대신 무릎 위 낡은 깡통에서 동전을 한 닢씩 꺼내 세고 계신다.)"],
   ["det1","…할머니, 그거 뭐예요?","sad"],["innma","…봄에 이불 새로 사려고 모아 둔 거야.","sad"],
   ["narr","(깡통 바닥이 보인다. 이백 냥에는 한참 모자란다.)"],["narr","(다람이가 내 소매를 꽉 쥔다. 아무 말도 하지 않는다. 정오까지. 이게 진짜 시간이다.)"]];
  setInterval(function(){try{if(!inn()||G.tab!=="scene"||dl()||!G.beats||!G.beats.inn_pro||G.beats.inn_meet||G.beats.inn_stakes)return;if(document.querySelector("#ov .modal,#innmove,#wmap,.crec2,body>.rt,.placecard"))return;
    var l=loc();if(!l||l.id!=="dining"||G.found.indexOf("C04")<0)return;G.beats.inn_stakes=1;try{saveProg()}catch(e){}say(STAKES.map(function(x){return x.slice()}),function(){try{render()}catch(e){}})}catch(e){}},700);
  /* (1-2) 「훅 연출 요청」 9: 침대 밑 발견은 반드시 지나가는 장면 — 주머니·이불을 본 뒤 안 쓰는 방에 있으면, 할머니가 찾던 것을 따라 침대 밑을 본다 */
  setInterval(function(){try{if(!inn()||G.tab!=="scene"||dl()||!G.beats||!G.beats.inn_pro||G.beats.inn_meet)return;if(document.querySelector("#ov .modal,#innmove,#wmap,.crec2,body>.rt,.placecard,#innins"))return;
    var l=loc();if(!l||l.id!=="bed13"||(G.obsSeen||[]).indexOf("o_under")>=0||G.found.indexOf("C04")>=0||G.found.indexOf("C01")<0||G.found.indexOf("C02")<0)return;
    var b=document.querySelector('#bigscene [data-obs="o_under"]');if(b&&!under9.t){under9.t=1;setTimeout(function(){under9.t=0;try{if(!dl())b.click()}catch(e){}},600)}}catch(e){}},500);
  var under9={t:0};
  /* (2) 회의 힌트 단계화: 1번째 방향만 → 2번째 어느 발언인지 → 3번째부터 다음에 낼 증거까지 */
  setTimeout(function(){var _rh9=window.__rtHint;if(!_rh9)return;window.__rtHint=function(C,ph,has,setSi){if(!inn()||!ph||!ph.stms)return _rh9.apply(this,arguments);
    var left=window.__hintLeft?window.__hintLeft():3;if(left<=0)return _rh9.apply(this,arguments);
    G.hints=(G.hints|0)+1;G.beats=G.beats||{};var key="rth|"+(ph.topic||""),n=G.beats[key]=(G.beats[key]|0)+1;window.__rtPt=null;
    if(n===1)return ph.hint;
    for(var i=0;i<ph.stms.length;i++){var st=ph.stms[i];if(!st.a||!st.k)continue;var nmk=(CAST[st.w]||{}).name||st.w;setSi(i);
     if(n===2){window.__rtPt=[".rt-bub.stm .wk"];return nmk+"의 이 말, 우리가 본 것과 맞아? 밑줄 친 부분을 다시 들어 보자."}
     var need=(st.steps||[]).map(function(x){return x.ids}).concat([st.a]),sp=0;try{sp=window.__rtgStep?window.__rtgStep(st):0}catch(e){}
     var ids=need[Math.min(sp,need.length-1)]||st.a,it=ids.filter(function(x){return has(x)})[0];
     if(!it)return nmk+"의 이 말을 깰 증거가 아직 없어. 회의를 잠깐 멈추고 더 조사해 보자.";
     window.__rtPt=[".rt-bub.stm .wk",'[data-bl="'+it+'"]'];var inm=itemName(C,it);return "'"+inm+"'"+josa(inm,"을","를")+" 떠올려 봐. "+nmk+"의 그 말과 부딪쳐."}
    return ph.hint}},0);
  /* 원탁 복구 보정: 개발용 '임시 자산' 표기는 숨기고, 너울(서 있는 진행자)은 다른 인물과 같은 크기로 */
  try{var st9=document.createElement("style");st9.textContent="body.inn1 #rtg .tmp{display:none!important}#rtg .seat img.neoul9{height:52%!important;width:auto!important;position:relative;top:34%;border-radius:50%;border:3px solid #C9A96A;background:#3A2A1E;box-sizing:border-box}";document.head.appendChild(st9)}catch(e){}
  /* (3) 설득력이 바닥나면: 할머니 서명 장면(EP.MF) → 처음부터 다시(모은 증거 유지) */
  setTimeout(function(){var _f=window.__innFail;if(!_f)return;window.__innFail=function(kind){var a=arguments,self=this;if(!inn()||!window.__innPlay||!(window.EP1INN||{}).MF)return _f.apply(self,a);
    try{var r=document.querySelector("body>.rt");if(r)r.remove();window.__inMeeting=false;document.body.classList.remove("rtg","rtg-drw")}catch(e){}
    try{window.__innPlay(window.EP1INN.MF,function(){_f.apply(self,a)})}catch(e){_f.apply(self,a)}}},0);
  /* (4) 회의 진입: 주민 소집(I9)은 플레이어가 '원탁 회의 열기'를 고른 뒤 한 번만 */
  window.__innPreOpen=function(c,spec,op){try{if(!inn()||!G)return false;G.beats=G.beats||{};if(G.beats.inn_i9||G.battle||!window.__innPlay||!(window.EP1INN||{}).I9)return false;
    G.beats.inn_i9=1;try{saveProg()}catch(e){}window.__innCutting=true;
    window.__innPlay(window.EP1INN.I9,function(){window.__innCutting=false;try{goTab("final")}catch(e){}setTimeout(function(){op(c,spec)},120)});return true}catch(e){return false}};
 })();
