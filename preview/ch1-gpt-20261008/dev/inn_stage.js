/* ===== 1장 대화 무대 정리 (inn_stage) =====
   기준(2026-10-09 확정): 원탁 회의 밖의 대화는 아빠·다람과 상대 한 명. 화면은 아빠 시점이라 아빠 얼굴은 띄우지 않는다.
   1) 대화 상대 고정: 한 대화(대사 묶음)의 상대를 처음에 정해 끝까지 그 인물만 세운다. 다람·아빠가 말해도 상대를 바꾸지 않는다.
      주민이 없는 부녀 대화는 다람. 상대가 실제로 퇴장하는 지문 뒤에만 다람으로 바뀐다.
   2) 배경 고정: 대화 중에는 장소 이동 입력(좌우 화살표·메뉴·지도)을 막는다. 장면 그림은 화면 너비 전체로(양옆 검은 띠 제거).
   3) 글자 크기 체계: 이야기 글 18 / 버튼 16 / 이름표·소제목 15 / 보조 글 13 / 카드 제목 22 (글자 크기 설정은 이야기 글에 적용).
   4) 대화 창: 두 줄 높이로 줄여 인물 상반신이 보이게. */
(function(){
 var MISS=window.__INNMISS||(window.__INNMISS=[]);var EP=window.EP1INN;if(!EP){MISS.push("stage: no EP");return}
 function bgDef(){try{var b=window.__innBg&&window.__innBg();return b||{}}catch(e){return {}}}
 function cur(){try{return !!(G&&CASES[G.ci]&&CASES[G.ci].id==="inn")}catch(e){return false}}
 /* 그림 크기표: [캔버스 너비, 높이, 몸 왼쪽, 몸 오른쪽, 위 여백, 아래 여백] (PNG 실측) */
 var BOX={"art/ch1/cast/daram-front.png":[192,192,20,136,20,6],"art/ch1/cast/nabi-front.png":[192,192,24,138,10,6],"art/ch1/cast/bami-front.png":[192,192,43,143,9,6],"art/ch1/cast/bami-shock.png":[192,192,4,189,8,6],"art/ch1/cast/karo-front.png":[192,192,27,141,5,6],"art/ch1/cast/daram-ear-grab-signature-v1.png":[192,192,18,163,15,6],"art/ch1/cast/daram-tail-hide-signature-v1.png":[192,192,51,142,9,6],"art/ch1/cast/daram-tail-hide-caught-signature-v2.png":[192,192,51,145,8,6],"art/ch1/cast/daram-surprised-front-v3.png":[192,192,22,164,24,6],"art/ch1/cast/daram-happy-front-v3.png":[192,192,21,148,18,6],"art/ch1/cast/daram-worried-front-v3.png":[192,192,38,141,50,6],"art/ch1/cast/daram-determined-front-v3.png":[192,192,22,183,9,6],"art/ch1/cast/daram-angry-front-v3.png":[192,192,14,162,17,6],"art/ch1/cast/daram-happy-front-v2.png":[192,192,21,141,21,6],"art/ch1/cast/daram-surprised-front-v2.png":[192,192,19,141,23,6],"art/ch1/cast/daram-worried-front-v2.png":[192,192,31,137,23,6],"art/ch1/cast/daram-determined-front-v2.png":[192,192,19,135,22,6],"art/ch1/cast/seryeon-normal-front-v1.png":[192,192,44,155,10,6],"art/ch1/cast/seryeon-surprise-front-v1.png":[192,192,44,156,10,6],
  "art/body/innma-0.png":[146,182,1,115,2,0],"art/ch1/cast/innma-neutral-v5.png":[146,182,5,111,2,0],"art/ch1/cast/innma-concerned-v5.png":[146,182,5,111,2,0],"art/ch1/cast/innma-bright-smile-v6.png":[146,182,5,111,2,0],"art/ch1/cast/innma-0-gaze-neutral-v2.png":[146,182,1,115,2,0],"art/ch1/cast/innma-0-gaze-gentle-smile-v2.png":[146,182,1,115,2,0],"art/body/innma-1.png":[148,182,2,115,4,0],"art/body/innma-2.png":[146,182,2,123,4,0],
  "art/body/wanggu-0.png":[230,182,22,165,3,0],"art/body/wanggu-1.png":[230,182,22,165,3,0],"art/body/wanggu-2.png":[230,182,2,192,1,0],"art/body/doto-0.png":[182,182,1,133,2,0],"art/ch1/cast/doto-v4-182.png":[182,182,0,142,2,0],"art/ch1/cast/seryeon-seated-paperwork-v2-talk.png":[160,216,4,155,2,0],"art/body/doto-1.png":[180,182,1,129,2,0],"art/body/doto-2.png":[174,182,1,120,9,0],
  "art/body/buri-0.png":[136,182,2,113,3,0],"art/body/buri-1.png":[130,182,2,114,2,0],"art/body/buri-2.png":[110,182,2,101,6,0]};
 var INNMA={"0":"art/ch1/cast/innma-neutral-v5.png","1":"art/ch1/cast/innma-concerned-v5.png","2":"art/ch1/cast/innma-bright-smile-v6.png"};
 var CASTF={det1:"daram-front",nabi:"nabi-front",karo:"karo-front"},BODYK={innma:"innma",wanggu:"wanggu",doto:"doto",buri:"buri"};
 function pose(m,k){var f=String(m||"").split(/\s+/)[0];var FP={innma:{think:"1",smile:"2"},doto:{shock:"2",think:"1"},buri:{shock:"2"},wanggu:{think:"1"}};if(k&&FP[k])return FP[k][f]||"0";var e=(window.__MOOD_EXPR||{})[f]||"normal";return e==="fluster"?"2":e==="doubt"?"1":"0"}
 /* 다람 표정: 그림의 감정 강도로 연결한다. 대본의 표정 표시 중 아래 넷만 새 그림을 쓰고, 나머지(가벼운 미소·생각 등)는 기본 그림.
    shock=당황(손을 뺨에 댄 놀람), sad=걱정(손 모음·귀 처짐), laugh=큰 웃음(눈 감은 활짝 웃음, 그만큼 기쁜 대사만), resolve=결심 */
 /* v2 = 약한 감정, v3 = 강한 감정(전신 포즈). 같은 캔버스 배율·같은 접지선으로 그린다(웅크린 걱정을 키 맞춰 키우지 않음) */
 var DFACE={shock:"daram-surprised-front-v2",sad:"daram-worried-front-v2",laugh:"daram-happy-front-v2",resolve:"daram-determined-front-v2",
  oops:"daram-ear-grab-signature-v1",shy:"daram-tail-hide-signature-v1",caught:"daram-tail-hide-caught-signature-v2",
  panic:"daram-surprised-front-v3",cower:"daram-worried-front-v3",joy:"daram-happy-front-v3",confront:"daram-determined-front-v3",mad:"daram-angry-front-v3"};
 function src(k,m){if(k==="wanggu")return "art/ch1/neoul-v2/neoul-"+neoState(m)+"-dialogue.png";var pz=window.__innPose&&window.__innPose(k);if(pz)return pz;   /* 장소의 행동 포즈를 대화에서도 그대로(통합 아트) */
if(k==="det1"){var dm=String(m||"").split(/\s+/)[0];
   /* 다람 v4(2026-10-09 확정 초기 복장) 6상태: 기본(수첩·꼬리 분리 합성, 꼬리 흔들기)/메모/활짝/땀 당황/참는 분노/코믹 분노. 슬픔·겁·결심·꼬리숨김은 기존 그림 유지 */
   /* 2026-10-10 GPT·사용자: 옛 외형(갈색 모자 v2/v3)이 섞여 번쩍이지 않게 모든 표정을 v4로. 정확한 슬픔·겁·결심 표정은 후속 아트 대기 → 가장 가까운 상태 */
   return "art/ch1/daram-v4/daram-"+dv4(dm)+"-dialogue.png"}
  if(CASTF[k])return "art/ch1/cast/"+CASTF[k]+".png";
  if(k==="geokkuri")return "art/ch1/cast/"+(pose(m)==="2"?"bami-shock":"bami-front")+".png";
  /* 세련: 앉아서 서류를 보는 v2(2026-10-09 전달, 개별 시안·최종 승인 아님). 대화에서도 앉은 맥락 유지 → 놀람 차분(서 있는 v1)은 쓰지 않는다 */
  /* 2026-10-10 사용자 "세련 첫 만남(현관 방문)·복도 신고는 서 있어야": 프롤로그·후일담은 서 있는 그림, 조사 중 식당 대화만 앉은 그림 */
  if(k==="seryeon"){var bb=(G&&G.beats)||{};if(!bb.inn_pro||bb.inn_final)return "art/ch1/cast/"+(/nervous|shock|panic|angry|surpr/.test(String(m||""))?"seryeon-surprise-front-v1":"seryeon-normal-front-v1")+".png";return "art/ch1/cast/seryeon-seated-paperwork-v2-talk.png"}
  if(k==="doto")return "art/ch1/cast/doto-v4-182.png";   /* 도토 v4(사용자 선택, 2026-10-09): 표정 차분은 아직 없어 한 장 */
  /* 토끼 할머니 v5(2026-10-09 전달): 머리·목·어깨·책 든 팔을 한 자세로 상대에게. 기본=neutral, 걱정·경계·망설임(think)=concerned(책을 끌어안고 시선을 내림).
     미소(smile)=v6 밝은 미소(따뜻한 인사·안심시키는 말에만, 대본 표정이 '옅은 미소/안도'인 줄) */
  if(k==="innma"){var ip=pose(m,k);return INNMA[ip]||INNMA["0"]}
  if(BODYK[k])return "art/body/"+BODYK[k]+"-"+pose(m,k)+".png";return null}
 var DUO={det0:1,det1:1,narr:1};
 /* 상대가 실제로 자리를 뜨는 지문(화면 표시 문구) */
 function lw(x){return Array.isArray(x)?x[0]:(x&&x.w)}function lt(x){return Array.isArray(x)?x[1]:(x&&x.t)}function ot(x){return Array.isArray(x)&&x[7]!=null?x[7]:lt(x)}function lm(x){return Array.isArray(x)?x[2]:(x&&x.m)}
 function cgList(){try{var b=window.__innBg&&window.__innBg();return (b&&b.def&&b.def.cg)||[]}catch(e){return []}}
 function firstResident(lines){var cg=cgList();for(var i=0;i<(lines||[]).length;i++){var w=lw(lines[i]);if(typeof w==="string"&&!DUO[w]&&cg.indexOf(w)<0)return w}return null}
 function hasDuo(lines){return (lines||[]).some(function(x){var w=lw(x);return w==="det1"||w==="det0"})}
 var visit={loc:-1,n:0,entered:{}};
 function visitKey(){try{if(G.loc!==visit.loc){visit.loc=G.loc;visit.n++}}catch(e){}return "I"+visit.loc+"#"+visit.n}
 function scene(){try{if(G.beats&&G.beats.inn_pro&&!(G.beats.inn_final&&!G.beats.inn_end)&&G.tab==="scene")return {key:visitKey(),s:null};if(G.beats&&G.beats.inn_pi!=null&&!G.beats.inn_pro)return {key:"P"+G.beats.inn_pi,s:EP.PRO[G.beats.inn_pi]};
  if(G.beats&&G.beats.inn_ei!=null&&G.beats.inn_final&&!G.beats.inn_end)return {key:"E"+G.beats.inn_ei,s:EP.END[G.beats.inn_ei]}}catch(e){}return null}
 var IDS=new WeakMap(),idn=0;function dlid(o){if(!IDS.has(o))IDS.set(o,++idn);return IDS.get(o)}
 var st={scene:"",dl:0,who:null,i:-1,m:null,size:""},layer=null,fig=null;
 function ensure(){var v=document.getElementById("dlgveil");if(!v)return null;if(layer&&layer.parentNode===v)return layer;
  layer=document.createElement("div");layer.id="innstage";layer.setAttribute("aria-hidden","true");v.insertBefore(layer,document.getElementById("vnbox"));fig=null;st.size="";return layer}
 /* 등장 효과음 '띠링': 새 인물이 화면에 처음 나타날 때 1회. 표정 변화·같은 인물의 다음 대사에는 없음.
    심각한 장면(돈주머니 발견·부엌의 작은 손님·장부의 엄마 글씨)은 낮게 또는 무음 */
 function chime(){try{if(st.quiet){st.quiet=0;return}tone(1319,.12,"sine",.05);tone(1760,.2,"sine",.04,.08)}catch(e){}}
 /* 인물 크기·위치: 머리(귀) 끝을 화면 높이의 FIGTOP에 맞추고 FIGK로 배율을 정한다(이전: H/180, 머리가 화면 꼭대기에 닿음) */
 var FIGK=215,FIGTOP=.16;
 /* 2026-10-09 대화판 03(상반신 구도) 기준: 인물별 배율(화면 높이 390 기준 원본 픽셀 배율)과 머리 끝 12px.
    얼굴·어깨·손이 읽히고 아래(다리)는 대사창 쪽으로 잘린다. 배경은 확대하지 않는다 */
 var DS={det1:3.15,innma:2.739,geokkuri:2.739,nabi:2.759,karo:2.739,seryeon:2.82,wanggu:2.739,doto:2.132,buri:2.739};
 /* 통합 아트 행동 포즈의 대화 그림(상반신 crop): 그림 높이를 화면 높이 비율로 맞춘다. 밤이는 거꾸로 매달린 그림이라 얼굴이 대사창 위에 오도록 위로 올린다 */
 var FSC={"art/ch1/action-poses/grandma/dialogue.png":[552,680,9,535,10,.96,0],"art/ch1/action-poses/seryeon/dialogue.png":[329,400,0,319,10,.96,0],"art/ch1/action-poses/nabi/dialogue.png":[620,588,9,590,8,.92,0],
  "art/ch1/action-poses/doto/dialogue.png":[960,865,14,928,16,.92,0],"art/ch1/action-poses/bami/dialogue.png":[660,830,15,647,0,.92,-.16],"art/ch1/action-poses/daram/dialogue.png":[760,705,15,738,12,.92,0],
  "art/ch1/action-poses/karo/dialogue.png":[279,320,4,267,10,.92,0],"art/ch1/action-poses/buri/dialogue.png":[297,320,10,289,10,.92,0],"art/ch1/action-poses/neoul/dialogue.png":[459,320,4,441,9,.92,0]};
 /* 너울 v2(2026-10-09 확정: 보안관 복장 자경단장 라쿤) 4상태 — 같은 전신 원본을 같은 축소율로 정규화(240x320, 발선 304), 대화는 같은 창(20,8,200x200)을 2배.
    몸통 중심(181.5)을 고정해 상태가 바뀌어도 몸이 옆으로 튀지 않게, 분노는 넓게 버틴 자세라 머리가 낮은 그대로 */
 ["default","admonish","angry","sheepish"].forEach(function(k){FSC["art/ch1/neoul-v2/neoul-"+k+"-dialogue.png"]=[400,400,181,182,16,.92,0]});
 ["idle-t0","idle-t1","idle-t2","memo","joy","flustered","held-anger","comic-anger"].forEach(function(k){var f="art/ch1/daram-v4/daram-"+k+"-dialogue.png";FSC[f]=[368,300,195,195,10,.92,0];try{var im=new Image();im.src=f}catch(e){}});
 /* 다람 기본 그림의 꼬리 흔들기: 2.6초마다 짧게(t0→t1→t0→t2→t0). 다른 표정은 꼬리가 그림에 포함돼 있어 움직이지 않는다 */
 (function(){var SEQ=["t1","t0","t2","t0"],ph=-1,wait=0;setInterval(function(){try{var im=document.querySelector(".isf img[src*='daram-idle-t']");if(!im){ph=-1;return}
   if(ph<0){if(++wait<16)return;wait=0;ph=0}var f=SEQ[ph];im.setAttribute("src",im.getAttribute("src").replace(/daram-idle-t\d/,"daram-idle-"+f));ph++;if(ph>=SEQ.length)ph=-1}catch(e){}},160)})();
 var DV4={"":"idle-t0",neutral:"idle-t0",think:"memo",memo:"memo",laugh:"joy",joy:"joy",smile:"joy",oops:"flustered",panic:"flustered",nervous:"flustered",shock:"flustered",shy:"flustered",caught:"flustered",cower:"flustered",
   mad:"comic-anger",angry:"comic-anger",pout:"held-anger",held:"held-anger",resolve:"held-anger",confront:"held-anger",sad:"idle-t0",worried:"idle-t0"};
 function dv4(m){var k=String(m||"").split(/\s+/)[0];return Object.prototype.hasOwnProperty.call(DV4,k)?DV4[k]:"idle-t0"}
 window.__innDV4=dv4;
 function neoState(m){var t="";try{var l=DL&&DL.lines&&DL.lines[DL.i];t=String((l&&(l[1]||l.t))||"");   /* 한 대사가 여러 쪽으로 나뉘어도 같은 상태를 유지: 같은 묶음(__pg.g)의 글을 합쳐 판단 */
   if(l&&l.__pg){t=DL.lines.filter(function(x){return x&&x.__pg&&x.__pg.g===l.__pg.g}).map(function(x){return String(x[1]||x.t||"")}).join(" ")}}catch(e){}var md=String(m||"");
  if(/angry|mad|shock/.test(md)||/!/.test(t))return "angry";
  if(/크흠|흠\.|머쓱|실례|죄송|미안|제가 성급|제가 잘못/.test(t))return "sheepish";
  if(/규정|규약|규칙|두십시오|해야 합니다|안 됩니다|벌금|허가|회의를 엽니다|정오 우편 마차|옮기지만 않는다면|기록하겠습니다|안건/.test(t))return "admonish";
  return "default"}
 window.__innNeoState=function(m){try{return neoState(m)}catch(e){return "default"}};
 function frame(k,s,W,H){var f=FSC[s];if(f){var sc=f[5]*H/f[1];return {w:f[0]*sc,h:f[1]*sc,left:W/2-(f[2]+f[3])/2*sc,top:H*12/390-f[4]*sc+f[6]*H}}
  var b=BOX[s]||[192,192,20,170,10,6],sc=(DS[k]||2.739)*H/390;return {w:b[0]*sc,h:b[1]*sc,left:W/2-(b[2]+b[3])/2*sc,top:H*12/390-b[4]*sc}}
 window.__innFrame=function(k,s){return frame(k,String(s||"").split("?")[0],innerWidth,innerHeight)};
 function draw(k,m){var W=innerWidth,H=innerHeight;
  if(k!==st.shown){if(k)chime();st.shown=k||null}
  if(!k){if(fig){fig.remove();fig=null}return}
  var s=src(k,m);
  if(!fig||fig.dataset.k!==k){if(fig)fig.remove();fig=document.createElement("div");fig.className="isf";fig.dataset.k=k;
   if(s){var im=document.createElement("img");im.alt="";im.draggable=false;fig.appendChild(im)}else{fig.dataset.face="1";try{fig.innerHTML=typeof pf==="function"?pf(k,m):""}catch(e){}}
   layer.appendChild(fig);requestAnimationFrame(function(){fig&&fig.classList.add("in")})}
  if(s){var im2=fig.firstChild;if(im2.getAttribute("src")!==s)im2.setAttribute("src",s);var b=BOX[s];if(!b)b=[192,192,20,170,10,6];
   var F=frame(k,s,W,H);im2.style.width=F.w+"px";im2.style.height=F.h+"px";
   fig.style.width=Math.round(F.w)+"px";fig.style.height=Math.round(F.h)+"px";fig.style.left=Math.round(F.left)+"px";fig.style.top=Math.round(F.top)+"px"}
  else{var fw=Math.round(H*.62);fig.style.width=fw+"px";fig.style.height=fw+"px";fig.style.left=Math.round(W/2-fw/2)+"px";fig.style.top=Math.round(H*.05)+"px"}}
 function step1(ln,id){var w=lw(ln),cg=cgList();
  /* 상대가 아닌 사람(아빠·다람)이 말할 때 표정 지정이 없으면 상대의 직전 표정을 유지한다(줄마다 표정이 바뀌어 깜빡이지 않게) */
  if(Array.isArray(ln)&&w!=="narr"&&w!=="@dir"){var f6=ln.length>6?ln[6]||null:null;if(f6||w===st.who||!st.who||st.who==="det1")st.m=f6}
  if(w==="narr"){var cue0=(window.__INNCUE||{})[ot(ln)];if(cue0){st.who=cue0==="none"?null:cue0;st.whoDl=id;st.m=null}return}
  if(!st.who&&(w==="det1"||w==="det0")){st.who="det1";st.whoDl=id;st.quiet=1}
  return;
  if(w==="narr"){var cue=(window.__INNCUE||{})[ot(ln)];if(cue==="none"){st.who=null;st.whoDl=id}else if(cue&&cue!=="det0"&&cg.indexOf(cue)<0&&(src(cue)||cue==="seryeon"||typeof pf==="function")){st.who=cue;st.whoDl=id;st.m=null}return}
  if(typeof w!=="string"||w==="det0")return;
  if(w==="det1"){if(!st.who){st.who="det1";st.whoDl=id;st.m=null}}
  else if(cg.indexOf(w)<0&&w!==st.who&&(!st.who||st.who==="det1"||st.whoDl!==id)){st.who=w;st.whoDl=id;st.m=null}
  if(w===st.who)st.m=lm(ln)||null}
 function sync(){var on=false;try{
  var v=document.getElementById("dlgveil");
  if(cur()&&v&&typeof DL!=="undefined"&&DL&&DL.lines&&!document.getElementById("rtg")&&!document.querySelector(".fstalk")){
   on=true;if(!ensure())return;
   var sc=scene(),sk=sc?sc.key:"D"+dlid(DL),id=dlid(DL),size=innerWidth+"x"+innerHeight;
   if(sk!==st.scene){st.scene=sk;st.who=null;st.m=null;st.whoDl=0;st.shown=null}
   if(id!==st.dl){st.dl=id;st.i=-1}
   if(DL.i!==st.i||size!==st.size){for(var q=Math.max(0,st.i+1);q<=DL.i&&q<DL.lines.length;q++)step1(DL.lines[q],id);st.i=DL.i;st.size=size;
    var ln=DL.lines[DL.i]||[],w=lw(ln),t=String(lt(ln)||"");
    draw(st.who,st.m);if(fig)fig.classList.toggle("ls",w!==st.who);
    }
  }}catch(e){if(!sync.err){sync.err=1;MISS.push("stage "+e.message)}}
  document.body.classList.toggle("inn-st2",on);
  if(!on&&st.dl){st.dl=0;st.i=-1}
  var full=false;try{full=cur()&&!!(G.beats&&G.beats.inn_bg)&&!!document.querySelector("#bigscene>svg[data-bg]:not([data-inn-world])")}catch(e){}
  document.body.classList.toggle("inn-full",full);
  seatSync(on);
  /* 조사 화면(접수대·2층 복도)의 양옆 빈칸: 검은 띠 대신 같은 그림을 흐리고 어둡게 깔아 화면 전체를 장소로 채운다(조사 지점 위치는 그대로) */
  try{var stg=document.querySelector(".stage"),fill=null;if(cur()&&!full&&stg&&document.querySelector("#bigscene svg[data-bg]:not([data-inn-world])")){var bd=bgDef();if(bd&&bd.def&&bd.def.src)fill=bd.def.src}
   if(stg){if(fill){var u='url("'+fill+'")';if(stg.style.getPropertyValue("--innfill")!==u)stg.style.setProperty("--innfill",u);stg.classList.add("inn-fill")}else stg.classList.remove("inn-fill")}}catch(e){}}
 /* 마차 장면: 앉은 다람(192×256, 월드 좌상단 448,124)을 배경 그림 안에 넣고, 대화 중에는 배경+다람을 (318,124,422,195) 구역으로 함께 2배 고정 표시.
    다람만 키우지 않는다. 줌 애니메이션 없음. 걱정 표정은 감정이 바뀌는 줄에서 한 번만 교체 */
 var seat={on:false,scene:""};
 function seatSync(dlgOn){try{var b=bgDef(),car=cur()&&b&&b.key==="carriage";
  if(!car){if(seat.on){seat.on=false;document.querySelectorAll("image.innseat").forEach(function(x){x.remove()})}if(layer)layer.classList.remove("seated");return}
  if(st.scene!==seat.scene){seat.scene=st.scene;seat.on=false;seat.snack=null}
  if(st.who==="det1")seat.on=true;
  var worried=seat.on&&(st.m==="sad"||st.m==="cower");
  /* 간식 포즈(2026-10-09 전달): '마지막 봉지' → 보여 주기, '안 뜯을 거야' → 품으로 당기기, 편지를 꺼내면 기본으로. 이 세 지점에서만 바꾼다 */
  try{var sl=typeof DL!=="undefined"&&DL&&DL.lines[DL.i],stx=sl?String(lt(sl)||""):"";
   if(/^아빠, 이게 마지막 봉지야/.test(stx))seat.snack="show";else if(/^이건 안 뜯을 거야/.test(stx))seat.snack="protect";else if(/^아빠가 안주머니에서 접힌 편지를 꺼낸다/.test(stx)||/엄마 편지/.test(stx))seat.snack=null}catch(e){}
  var pose=worried?"worried":(seat.snack?"snack-"+seat.snack:"neutral");
  var href="art/ch1/cast/daram-seated-"+pose+"-192x256.png";
  document.querySelectorAll('svg[data-bg="carriage"]').forEach(function(sv){
   var vb="0 0 844 390";   /* 2026-10-10: 대화 중 2배 확대 → 1.1배만(배경을 넓게, 다람 도트가 과하게 커지지 않게) */if(sv.getAttribute("viewBox")!==vb)sv.setAttribute("viewBox",vb);
   var im=sv.querySelector("image.innseat");
   if(seat.on){if(!im){im=document.createElementNS("http://www.w3.org/2000/svg","image");im.setAttribute("class","innseat");im.setAttribute("x","490");im.setAttribute("y","143");im.setAttribute("width","166");im.setAttribute("height","221");im.setAttribute("style","image-rendering:pixelated");sv.appendChild(im)}
    if(im.getAttribute("href")!==href)im.setAttribute("href",href)}
   else if(im)im.remove()});
  if(layer)layer.classList.toggle("seated",true)}catch(e){}}
 (function loop(){sync();requestAnimationFrame(loop)})();
 /* 새 대사창이 생기는 순간(그리기 전)에 바로 맞춘다: 첫 프레임에 옛 그림이 비치지 않게 */
 try{var mq=false;new MutationObserver(function(){if(mq)return;mq=true;Promise.resolve().then(function(){mq=false;sync();try{cutSync();plateSync()}catch(e){}})}).observe(document.getElementById("ov")||document.body,{childList:true,subtree:true})}catch(e){}
 /* 대화 중 장소 이동 입력 차단: 좌우 화살표·하단 메뉴·지도·장소 버튼 */
 function talking(){try{return cur()&&((typeof DL!=="undefined"&&!!DL)||!!document.getElementById("dlgveil")||!!document.querySelector("#ov .modal")||document.body.classList.contains("inn-cut")&&!(G.beats&&G.beats.inn_pro))}catch(e){return false}}
 var MOVESEL=".fsa,#fsal,#fsar,#w209rail,#w209more,#wmap,.mapbtn,[data-room],[data-node],#w209back";
 ["pointerdown","touchstart","click"].forEach(function(ev){document.addEventListener(ev,function(e){try{if(!talking())return;var t=e.target&&e.target.closest&&e.target.closest(MOVESEL);if(!t)return;
  /* 2026-10-10 "대사 중에도 더보기(소리 조절·저장)는 항상": 더보기 단추와 펼침 안의 설정·메인으로·닫기는 막지 않는다(이동·힌트는 계속 막음) */
  var ok=e.target.closest("#w209rail [data-more]")||e.target.closest('#w209more [data-w="set"],#w209more [data-w="main"]')||(e.target.closest("#w209more button")&&!e.target.closest("#w209more [data-w]"));if(ok)return;
  e.stopImmediatePropagation();e.preventDefault()}catch(x){}},{capture:true,passive:false})});

 /* ===== 이동·전환 정리 ===== */
 /* 장소 이름 띠가 뜨기 전에 남은 대사창을 치운다(대사가 진행 중이 아닐 때만) */
 function clearDlg(){try{if(cur()&&!(typeof DL!=="undefined"&&DL)){var f=document.getElementById("ovfz");if(f)f.innerHTML="";window.__dlFreeze=false;var v=document.getElementById("dlgveil");if(v)v.remove();document.body.classList.remove("dl-on","inn-st2")}}catch(e){}}
 try{var _bn=banner;banner=function(){clearDlg();setTimeout(clearDlg,0);setTimeout(clearDlg,60);return _bn.apply(this,arguments)}}catch(e){MISS.push("stage banner")}
 /* 1장에서는 옛 사건의 말버릇(도토 초시계 등)을 끈다 */
 var Q0=window.QUIRK;
 /* 마지막 줄 표시: 이어지는 장면·증거 카드가 있으면 ▼, 실제로 대화가 끝나 조사로 돌아갈 때만 '닫기' */
 var lastSpot={id:null,t:0,got:true};
 function spotDown(e){try{var b=e.target.closest&&e.target.closest("#bigscene [data-spot]");if(!b)return;var id=b.dataset.spot,sp=null;
  EP.LOCS.forEach(function(l){(l.spots||[]).forEach(function(x){if(x.id===id||x.ev===id)sp=x})});lastSpot={id:id,t:Date.now(),got:!sp||G.found.indexOf(sp.ev)>=0}}catch(x){}}
 ["pointerdown","touchstart","click"].forEach(function(ev){document.addEventListener(ev,spotDown,{capture:true,passive:true})});
 function seq(){try{return !(G.beats&&G.beats.inn_pro)||(G.beats.inn_final&&!G.beats.inn_end)||!!window.__innCutting}catch(e){return false}}
 /* 1장 인물은 프롤로그에서 이미 만났다: 조사 중 첫 질문 때 '새 인물·안녕하세요' 인사를 띄우지 않는다 */
 function metAll(){try{if(!cur()||!window.__metOf)return;var c=CASES[G.ci],m=window.__metOf(c);if(!Array.isArray(m))return;Object.keys(c.talk||{}).forEach(function(k){if(m.indexOf(k)<0)m.push(k)})}catch(e){}}
 /* 이름표: 아빠가 이름을 듣기 전까지는 '???' (프롤로그 첫 만남). 이름을 말하는 그 줄부터 이름이 뜬다 */
 var REVEAL={karo:"이 마차 마부 까로예요",nabi:"저는 여기 일 돕는 나비예요",geokkuri:"저는 밤이예요",doto:"저는 도토라고 해요",buri:"장치공 부리예요",seryeon:"늦게 든 세련입니다",wanggu:"자경단장 너울입니다"};
 function revealAt(k){for(var i=0;i<EP.PRO.length;i++){var it=EP.PRO[i].items;for(var j=0;j<it.length;j++){var t=lt(it[j]);if(typeof t==="string"&&t.indexOf(REVEAL[k])>=0)return i}}return -1}
 var RPI={};Object.keys(REVEAL).forEach(function(k){RPI[k]=revealAt(k)});var heard={};
 var INVINTRO={buri:1,doto:1,geokkuri:1};   /* 2026-10-10: 프롤로그에서 빠져 조사 중에 처음 만나는 인물 — 자기소개 줄을 듣기 전까지 ??? (들은 것은 저장) */
 function known(k){if(!REVEAL[k])return true;try{if(INVINTRO[k]&&G.beats&&G.beats.inn_pro){if(heard[k]&&!G.beats["inn_heard_"+k])G.beats["inn_heard_"+k]=1;var EVK={buri:"C04",doto:"C08",geokkuri:"C07"};return !!(G.beats["inn_heard_"+k]||heard[k]||G.beats.inn_final||G.found.indexOf(EVK[k])>=0)}if(G.beats&&G.beats.inn_pro)return true;var pi=G.beats&&G.beats.inn_pi;if(pi==null)return true;if(pi>RPI[k])return true;if(pi<RPI[k])return false}catch(e){return true}return !!heard[k]}
 /* 아빠 속마음(괄호로 시작하는 지문): 푸른 글씨와 '아빠' 이름표. 질문 화면을 포함한 모든 대사창에 적용 */
 function innerSync(){try{if(!cur()||typeof DL==="undefined"||!DL)return;var ln=DL.lines[DL.i];var vb=document.querySelector("#vnbox .vband");if(!ln||!vb)return;
  var inr=lw(ln)==="narr"&&String(lt(ln)||"").charAt(0)==="(";vb.classList.toggle("inner",inr);
  var vt=vb.querySelector(".vtxt");if(inr&&vt&&!vt.querySelector(".plate")){var pl=document.createElement("span");pl.className="plate inner-plate";pl.textContent="아빠";vt.insertBefore(pl,vt.firstChild)}}catch(e){}}
 function plateSync(){try{innerSync();if(!cur()||typeof DL==="undefined"||!DL)return;var ln=DL.lines[DL.i];if(!ln)return;var t=String(lt(ln)||"");
  Object.keys(REVEAL).forEach(function(k){if(t.indexOf(REVEAL[k])>=0)heard[k]=1});
  var w=lw(ln),pl=document.querySelector("#vnbox .plate:not(.inner-plate)");if(!pl||!REVEAL[w])return;
  if(!known(w)){if(pl.textContent!=="???"){pl.dataset.real=pl.textContent;pl.textContent="???"}}}catch(e){}}
 /* 증거 카드: 그림·이름 아래 발견 장소(어디서, 누구에게서)를 한 줄로 남긴다 */
 var FOUND={C01:"2층 창고 · 열세 번째 침대 베개 밑",C02:"2층 창고 · 열세 번째 침대 이불",C03:"식당 · 나비에게 들은 말",C04:"부엌 · 빵 바구니",C05:"부엌 · 바구니 속 손님의 옆구리털",C06:"2층 복도 · 꺾이는 곳",C07:"2층 복도 · 밤이에게 들은 말",C08:"도토의 방 · 창가",C09:"접수대 · 숙박부",C10:"원탁회의 · 너울의 기록부",C11:"2층 창고 · 침대 밑 상자",C12:"식당 · 세련에게 들은 말",C13:"2층 복도 · 밤이에게 들은 말"};
 function cardSync(){try{if(!cur())return;var m=document.querySelector("#mveil .modal,#ov .modal");if(!m||m.dataset.found)return;var h=m.querySelector("h3");if(!h)return;var nm=h.textContent.trim(),id=null;
  Object.keys(EP.EV).forEach(function(k){if(EP.EV[k].name===nm)id=k});m.dataset.found="1";if(!id||!FOUND[id])return;
  /* 들은 말(증언)은 실제로 대화한 장소를 쓴다(나비는 식당·부엌 어디서든 만날 수 있다). 첫날 저녁 밤이의 말(C07)은 고정 */
  var TALKF={C03:"나비",C07:"밤이",C12:"세련",C13:"밤이"},place=FOUND[id];if(TALKF[id]){try{var lc=CASES[G.ci].locations[G.loc];if(lc)place=(lc.short||lc.name)+" · "+TALKF[id]+"에게 들은 말"}catch(e){}}
  var sm=document.createElement("small");sm.className="found-at";sm.textContent="발견 장소 · "+place;h.insertAdjacentElement("afterend",sm)}catch(e){}}
 var talkWho=null;
 function talkChime(){try{var ft=document.querySelector(".fstalk");var w=ft&&G&&G.tab==="talk"?G.who:null;if(w&&w!==talkWho)chime();talkWho=w}catch(e){}}
 function tick(){try{document.body.classList.toggle("inn1",cur());talkChime();metAll();plateSync();cardSync();
  if(cur()){if(!tick.q)tick.q={};if(window.QUIRK!==tick.q)window.QUIRK=tick.q}else if(window.QUIRK!==Q0)window.QUIRK=Q0;
  var nx=document.querySelector("#vnbox .nx");
  if(nx&&cur()&&typeof DL!=="undefined"&&DL){var last=DL.i>=DL.lines.length-1,cont=seq()||DL.__more||(!lastSpot.got&&Date.now()-lastSpot.t<120000);
   var want=last?(cont?"▼":"닫기"):"▼";if(nx.textContent!==want)nx.textContent=want;nx.classList.toggle("end",want==="닫기")}
  var h=document.getElementById("innhintt");if(h&&!h.classList.contains("on")&&h.textContent)h.textContent="";
  if(cur()&&G.beats&&G.beats.inn_pro&&h&&/다음 대사/.test(h.textContent))h.textContent="";
 }catch(e){}}
 (function loop2(){tick();requestAnimationFrame(loop2)})();

 /* ===== 관찰 컷: 2층 복도 배치도(침대 세기 근거) ===== */
 function planSvg(){var r=[];var X=[60,106,152,198,244,290];
  function bed(x,y,n,cls){return '<g class="bed '+(cls||"")+'"><rect x="'+(x+8)+'" y="'+(y+8)+'" width="26" height="34" fill="#7A5534"/><rect x="'+(x+10)+'" y="'+(y+10)+'" width="22" height="8" fill="#EFE6D2"/><rect x="'+(x+10)+'" y="'+(y+19)+'" width="22" height="21" fill="#2F6672"/>'+(n?'<text class="bn" x="'+(x+21)+'" y="'+(y+34)+'" text-anchor="middle" style="transition-delay:'+(n*0.12).toFixed(2)+'s">'+n+'</text>':'')+'</g>'}
  r.push('<rect x="2" y="2" width="436" height="196" fill="#F6EEDA" stroke="#6B4A2B" stroke-width="4"/>');
  r.push('<text class="pt" x="14" y="24">2층 복도</text>');
  r.push('<rect x="50" y="88" width="312" height="26" fill="#D9C49A"/>');
  X.forEach(function(x,i){r.push('<rect x="'+x+'" y="36" width="42" height="50" fill="#E9DDBF" stroke="#6B4A2B" stroke-width="2"/>'+bed(x,36,i+1));r.push('<rect x="'+x+'" y="116" width="42" height="50" fill="#E9DDBF" stroke="#6B4A2B" stroke-width="2"/>'+bed(x,116,i+7))});
  r.push('<g><rect x="18" y="86" width="32" height="30" fill="#BFA77A" stroke="#6B4A2B" stroke-width="2"/>'+[0,1,2,3].map(function(k){return '<rect x="'+(22+k*7)+'" y="88" width="2" height="26" fill="#6B4A2B"/>'}).join("")+'<text class="lb" x="34" y="132" text-anchor="middle">앞 계단</text></g>');
  r.push('<g class="far"><rect x="336" y="88" width="26" height="76" fill="#D9C49A"/>'+
   '<g class="clk"><circle cx="376" cy="100" r="11" fill="#F2E6C8" stroke="#3B2A1E" stroke-width="3"/><rect x="375" y="92" width="2" height="9" fill="#3B2A1E"/><rect x="376" y="99" width="6" height="2" fill="#3B2A1E"/><text class="lb" x="392" y="80" text-anchor="middle">벽시계</text></g>'+
   '<rect x="300" y="166" width="62" height="28" fill="none"/>'+
   '<g><rect x="366" y="140" width="66" height="54" fill="#E9DDBF" stroke="#6B4A2B" stroke-width="2"/><g class="b13">'+bed(380,146,0)+'<text class="bn n13" x="401" y="180" text-anchor="middle">13</text></g>'+
   '<rect class="dopen" x="362" y="150" width="6" height="26" fill="#8A5E36"/><rect class="dshut" x="366" y="140" width="66" height="54" fill="#8A5E36" stroke="#6B4A2B" stroke-width="2"/><text class="lb" x="399" y="136" text-anchor="middle">창고</text></g>'+
   '<g><rect x="336" y="166" width="26" height="28" fill="#BFA77A" stroke="#6B4A2B" stroke-width="2"/>'+[0,1,2].map(function(k){return '<rect x="338" y="'+(170+k*8)+'" width="22" height="2" fill="#6B4A2B"/>'}).join("")+'<text class="lb" x="330" y="186" text-anchor="end">부엌 계단</text></g></g>');
  return '<svg viewBox="0 0 440 200" shape-rendering="crispEdges" role="img" aria-label="2층 복도 배치도: 양쪽 방에 침대 열둘, 꺾인 끝 창고에 열세 번째 침대">'+r.join("")+'</svg>'}
 var CUT=[{re:/^하나, 둘, 셋… 열하나, 열둘\.$/,s:1},{re:/벽시계 앞에서 한 번 꺾인다/,s:2},{re:/^열셋\. 할머니/,s:3},{re:/^거긴 (창고|지금은 안 쓰는 방)/,s:3},{re:/^짐 풀고 내려와요/,s:4}];
 var CUT2=[{re:/^안에 작은 애가 있어|^숨을… 안 쉬는 것 같아|^아빠가 볼게|^뚜껑만 살짝|^\(차갑다|^\(이렇게 작은 몸은|^\(함부로 판단하지|^…이렇게 좁은 데 둘 수는 없겠다/,c:"teapot"}];   /* 2026-10-10: 조사 중 찻주전자 발견(대사가 문장 단위로 나뉘어 표시됨) */
 var cut2El=null;
 function cut2Sync(){try{var on=null;if(cur()&&typeof DL!=="undefined"&&DL&&G.beats){var ln=DL.lines[DL.i];var t=ln&&ot(ln);CUT2.forEach(function(c){if(t&&c.re.test(t))on=c.c})}
  var v=document.getElementById("innstage");
  if(on&&v){if(!cut2El||cut2El.parentNode!==v){cut2El=document.createElement("div");cut2El.id="inncut";cut2El.innerHTML='<img alt="찻주전자 안에 작은 겨울잠쥐가 웅크리고 있다" src="art/ch1/cuts/P13-teapot-observation-640x360.png">';v.appendChild(cut2El);requestAnimationFrame(function(){cut2El&&cut2El.classList.add("in")})}v.classList.add("cut2")}
  else{if(cut2El){cut2El.remove();cut2El=null}if(v)v.classList.remove("cut2")}}catch(e){}}
 (function loop4(){cut2Sync();requestAnimationFrame(loop4)})();
 var cutEl=null;
 function cutSync(){try{var on=0;if(cur()&&typeof DL!=="undefined"&&DL&&G.beats&&!G.beats.inn_pro){var ln=DL.lines[DL.i];var t=ln&&ot(ln);CUT.forEach(function(c){if(t&&c.re.test(t))on=c.s})}
  var v=document.getElementById("innstage");
  if(on&&v){if(!cutEl||cutEl.parentNode!==v){cutEl=document.createElement("div");cutEl.id="innplan";cutEl.innerHTML=planSvg();v.appendChild(cutEl);requestAnimationFrame(function(){cutEl&&cutEl.classList.add("in")})}
   for(var k=1;k<=4;k++)cutEl.classList.toggle("s"+k,on>=k);v.classList.add("cut")}
  else{if(cutEl){cutEl.remove();cutEl=null}if(v)v.classList.remove("cut")}}catch(e){}}
 (function loop3(){cutSync();requestAnimationFrame(loop3)})();

 /* ===== 근접 조사: 돈주머니·봉인띠·계약서 앞뒤를 직접 넘겨 본다 ===== */
 var STAR='<svg class="cstar" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 L14.6 8.6 L21.5 9 L16.2 13.4 L18 20.5 L12 16.6 L6 20.5 L7.8 13.4 L2.5 9 L9.4 8.6 Z" fill="currentColor"/><path d="M21.5 9 Q24 6 21 4.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';
 var INSPECT={
  C01a:{title:"돈주머니의 봉인띠",pages:[{art:'<img class="icl" src="art/ch1/closeup/I1-seal-strip-complete-512.png" alt="종이 봉인띠. 붉은 도장 「세련」과 끝이 말린 별">',
    cap:"주머니 입구를 감은 종이 봉인띠. 붉은 도장 「세련」, 그리고 끝이 말린 별. 만진 손끝에 인주가 묻어난다.",look:"봉인띠"}]},
  C01b:{title:"여관 매매 계약서",pages:[
   {art:'<img class="icl" src="art/ch1/closeup/I1-contract-front-complete-512.png" alt="계약서 앞면. 매도인 서명 칸은 비어 있고 매수인 세련 서명 끝에 별">',
    cap:"봉인띠 밑에 접혀 있던 종이. 앞면: 매도인(할머니) 서명 칸은 비어 있다. 매수인 「세련」 서명 끝에 같은 모양의 별.",look:"앞면"},
   {art:'<img class="icl" src="art/ch1/closeup/I1-contract-back-complete-512.png" alt="계약서 뒷면 조항">',
    cap:"뒷면: 「매도인이 숙박 허가를 잃는 날, 이 계약은 효력이 생긴다.」",look:"뒷면"}]},
  /* 정본 = 바탕 그림 + 정확한 글자·문양 덧그림(같은 512 좌표). 미리보기용 합성 그림은 쓰지 않는다 */
  C11:{title:"손님 장부 첫째 권",pages:[{art:lay("guest-ledger","펼친 장부. 이름 대신 발자국, 꽃, 동그라미, 끝이 말린 별을 그린 줄"),
    cap:"30년 전부터 10년 전까지의 손님 장부. 이름 대신 「이름 모르는 손님」이라 적힌 줄이 많고, 그림으로 서명한 줄도 있다. 발자국, 꽃, 동그라미, 별.",look:"장부"}]},
  C05:{title:"옆구리털 (돋보기)",pages:[{art:lay("dormouse-flank","겨울잠쥐 옆구리털에 거꾸로 찍힌 붉은 글씨와 별"),
    cap:"옆구리털에 붉은 글씨와 작은 별이 거꾸로 찍혀 있다. 번졌지만 읽을 수 있고, 털 속까지 배어 있다.",look:"옆구리"}]},
  C08:{title:"도토의 날씨 일지",pages:[{art:lay("weather-diary","날씨 일지. 맑음, 흐림, 비, 바람, 그리고 마지막 줄 자정, 첫눈"),
    cap:"대부분 한 단어다. 어젯밤 줄만 길다. 「자정, 첫눈」.",look:"일지"}]},
  C09:{title:"숙박부",pages:[{art:'<div class="ipaper"><b>숙박부</b><p class="ibook">아빠 · 다람 / 3박</p><p class="ibook hl">세련 / 1박 / 정오 마차로 출발 예정</p></div>',
    cap:"우리 이름 바로 아래 세련 씨의 줄. 1박, 정오 마차로 출발 예정.",look:"숙박부"}]},
  C01show:{title:"돈주머니 (조사 때 본 것)",pages:[{art:'<img class="icl" src="art/ch1/closeup/I1-seal-strip-complete-512.png" alt="돈주머니의 봉인띠">',
    cap:"창고에서 본 돈주머니의 붉은 봉인띠. 현장 물건은 옮기지 않고 조사 기록으로 보여 드린다.",look:"증거"}]}};
 function lay(k,alt){return '<span class="ilay"><img class="ib0" src="art/ch1/closeup/'+k+'-base-512.png" alt="'+alt+'"><img class="ib1" src="art/ch1/closeup/'+k+'-exact-overlay-512.png" alt=""></span>'}
 function inspect(key,done){var D=INSPECT[key];if(!D){done&&done();return}var i=0;
  try{SFX.pop9&&SFX.pop9()}catch(e){}var el=document.createElement("div");el.id="innins";el.setAttribute("role","dialog");el.setAttribute("aria-label",D.title+" 자세히 보기");
  function draw(){var p=D.pages[i],last=i>=D.pages.length-1;
   el.innerHTML='<div class="iin"><div class="ihd"><small>자세히 보기</small><b>'+D.title+'</b>'+(D.pages.length>1?'<span class="ipg">'+D.pages.map(function(x,k){return '<i class="'+(k===i?"on":"")+'">'+x.look+'</i>'}).join("")+'</span>':'')+'</div>'+
    '<div class="iart">'+p.art+'</div><p class="icap">'+p.cap+'</p><div class="ibtns">'+(i>0?'<button class="ib ghost" data-k="prev">◀ 앞면</button>':'')+'<button class="ib" data-k="'+(last?"ok":"next")+'">'+(last?"다 봤어":"뒤집어 보기 ▶")+'</button></div></div>';
   var ar=el.querySelector(".iart");if(ar){ar.setAttribute("role","button");ar.setAttribute("aria-label","크게 보기");ar.onclick=function(e){e.stopPropagation();ar.classList.toggle("big");try{SFX.tap()}catch(x){}}}
   el.querySelectorAll("[data-k]").forEach(function(b){b.onclick=function(e){e.stopPropagation();try{SFX.page()}catch(x){}var k=b.dataset.k;if(k==="next")i++;else if(k==="prev")i--;else{el.remove();done&&done();return}draw()}});
   var f=el.querySelector('[data-k="next"],[data-k="ok"]');if(f)try{f.focus({preventScroll:true})}catch(x){}}
  document.body.appendChild(el);try{SFX.page()}catch(x){}draw()}
 window.__innInspect=inspect;
 /* 연출 지시(글자 없음): 화면 상대 교체·퇴장, 효과음. 대사 사이 잠깐 멈춤 동안 실행된다 */
 function dirRun(d){try{if(!d)return;if(d.sfx)try{SFX[d.sfx]&&SFX[d.sfx]()}catch(e){}
  if(Object.prototype.hasOwnProperty.call(d,"who")){var sc=scene();if(sc&&sc.key!==st.scene){st.scene=sc.key;st.shown=null}if(String(d.chime)==="0")st.quiet=1;st.who=d.who==="none"?null:d.who;st.whoDl=-1;st.m=null;
   var v=document.getElementById("dlgveil");if(v&&ensure()){if(!st.who&&fig){var f=fig;fig=null;f.classList.remove("in");setTimeout(function(){f.remove()},260)}else draw(st.who,null)}}}catch(e){}}
 window.__innDir=dirRun;
 function parseDir(t){var o={};String(t||"").split(";").forEach(function(kv){var i=kv.indexOf(":");if(i>0){var k=kv.slice(0,i).trim(),v=kv.slice(i+1).trim();o[k]=k==="ms"?+v:v}});return o}
 /* 대사 묶음 안의 ["@inspect", 키] 줄에서 대사를 멈추고 근접 조사를 연 뒤 이어서 진행 */
 function entryFilter(lines){try{if(!cur()||!Array.isArray(lines))return lines;var EN=window.__INNENTRY||{};
   if(G.tab==="scene"&&G.beats&&G.beats.inn_pro){var vk=visitKey();var had=visit.entered[vk];visit.entered[vk]=1;
    if(had)lines=lines.filter(function(x){if(!Array.isArray(x))return true;if(x[0]==="narr"&&EN[x[1]])return false;if(x[0]==="@dir"&&/entry:1/.test(x[1]))return false;return true})}
   }catch(e){}return lines}
 function talkEntry(lines){try{if(cur()&&G.tab==="talk"&&G.who&&Array.isArray(lines)){var TE=window.__INNTALKENTRY||{},tk=G.who;if(TE[tk]&&!talkEntered[tk]){talkEntered[tk]=1;lines=[["narr",TE[tk]]].concat(lines)}}}catch(e){}return lines}
 var talkEntered={};
 /* 엔진의 관찰 뒤 한 줄 메모('다람의 속마음' 이름표, [나중에]·[잠김] 꼬리표)는 1장에서 띄우지 않는다: 아빠 시점 규칙과 어긋나고 관찰 대사가 이미 같은 내용을 말한다. 현장 메모 목록에는 남는다 */
 function think1(lines){try{return cur()&&G.beats&&G.beats.inn_pro&&Array.isArray(lines)&&lines.length===1&&Array.isArray(lines[0])&&lines[0][0]==="think"}catch(e){return false}}
 function obsNote(lines){try{if(!think1(lines)||G.tab!=="scene")return false;var tx=lines[0][1],l=CASES[G.ci].locations[G.loc];return !!(l&&(l.obs||[]).some(function(o){return o.text===tx}))}catch(e){return false}}
 /* 힌트 등 엔진의 한 줄 '속마음'(다람의 속마음 이름표)은 1장에서 다람이 직접 말하는 줄로 바꾼다(아빠 시점: 속마음 이름표는 아빠만) */
 try{var _say0=say;say=function(lines,done,sk){if(obsNote(lines)){setTimeout(function(){done&&done()},0);return}
   if(think1(lines))lines=[["det1",String(lines[0][1]||"")]];return _say0.call(this,entryFilter(lines),done,sk)}}catch(e){MISS.push("stage entry")}
 /* 2026-10-10 장르 비교 검수: "[표 변화]·[감점 없음]·[연결]" 같은 시스템 꼬리표가 대사창에 그대로 보여 몰입을 깨던 것 — 표시할 때만 떼어 낸다(데이터·판정은 그대로) */
 var TAGRE=/^\[(표 변화|감점 없음|연결|결정|순서|상황|지목|잠정 투표|다시|추가 질문)\]\s*/;
 function untag(lines){try{if(!cur()||!Array.isArray(lines))return;lines.forEach(function(x){if(Array.isArray(x)&&typeof x[1]==="string"&&TAGRE.test(x[1]))x[1]=x[1].replace(TAGRE,"");else if(x&&typeof x.t==="string"&&TAGRE.test(x.t))x.t=x.t.replace(TAGRE,"")})}catch(e){}}
 function split(base,self,lines,done,sk){untag(lines);try{if(cur()&&Array.isArray(lines)&&lines.some(function(x){return Array.isArray(x)&&(x[0]==="@inspect"||x[0]==="@dir"||x[0]==="@grant")})){
    var parts=[],curp=[];lines.forEach(function(x){if(Array.isArray(x)&&x[0]==="@inspect"){parts.push(curp);parts.push(x[1]);curp=[]}else if(Array.isArray(x)&&x[0]==="@dir"){parts.push(curp);parts.push({dir:parseDir(x[1])});curp=[]}else if(Array.isArray(x)&&x[0]==="@grant"){parts.push(curp);parts.push({grant:x[1]});curp=[]}else curp.push(x)});parts.push(curp);
    var k=0;(function next(){if(k>=parts.length){done&&done();return}var p=parts[k++];
     if(typeof p==="string"){var v=document.getElementById("dlgveil");if(v&&!(typeof DL!=="undefined"&&DL))v.remove();inspect(p,next);return}
     if(p&&p.grant){var gid=p.grant;if(G.found.indexOf(gid)>=0){next();return}try{window.__innGrant&&window.__innGrant(gid)}catch(e){}var v2=document.getElementById("dlgveil");if(v2&&!(typeof DL!=="undefined"&&DL))v2.remove();try{SFX.found()}catch(e){}if(window.__innCard)window.__innCard(gid,function(){next()});else next();return}
     if(p&&p.dir){dirRun(p.dir);setTimeout(next,p.dir.ms!=null?p.dir.ms:420);return}
     if(!p.length){next();return}var more=k<parts.length;base.call(self,p,function(){next()},sk);try{if(DL)DL.__more=more}catch(e){}})();return}}catch(e){}
   return base.call(self,lines,done,sk)}

 /* ---- 대사 쪽 나누기(2026-10-09 실기기 피드백): 한 번 누를 때 한 문장, 긴 문장은 뜻이 이어지는 자리에서 두 줄 ----
    문장 끝(. ? ! 뒤 띄어쓰기)에서 나누되, 합쳐도 아주 짧은 줄("응. 도착하면.")은 한 쪽에 둔다. 말줄임(…) 뒤에서는 나누지 않는다.
    줄바꿈은 가운데에 가까운 띄어쓰기 중 쉼표·연결 어미·조사 뒤를 우선한다. 원래 줄 글은 [7]에 남겨 무대 연출·컷 판정에 쓴다. */
 var PG_JOIN=12,PG_WRAP=28;   /* 대사창 폭 540px·16px에서 한 줄 약 31자 */
 function sents(s){var out=[],buf="",i,ch;for(i=0;i<s.length;i++){ch=s.charAt(i);buf+=ch;
   if(/[.?!]/.test(ch)){var j=i+1;while(j<s.length&&/['"」』)’”]/.test(s.charAt(j))){buf+=s.charAt(j);j++}
    if(j<s.length&&s.charAt(j)===" "){out.push(buf);buf="";i=j;continue}i=j-1}}
  if(buf.trim())out.push(buf);return out.map(function(x){return x.trim()}).filter(Boolean)}
 var ACK=/^(네|응|예|음|아|어|그래|그럼)[.,]$/;   /* 짧은 대답은 다음 문장과 한 쪽에 */
 function joinShort(a){var r=[];a.forEach(function(x){var p=r.length?r[r.length-1]:null;if(p!==null&&((p+" "+x).length<=PG_JOIN||(ACK.test(p)&&(p+" "+x).length<=34)||(x.length<=4&&(p+" "+x).length<=24)))r[r.length-1]+=" "+x;else r.push(x)});return r}
 var GOOD=/(,|고|서|면|데|니까|지만|는데|려고|다가|며|를|에|에서|으로|께|한테)$/,GOOD3=/[이가도로]$/;   /* 이·가·도·로는 세 글자 이상 낱말 끝일 때만(복도·아이·누가 오판 방지) */
 function wrap1(s){if(s.length<=PG_WRAP||s.indexOf("\n")>=0)return s;var best=-1,bs=1e9,mid=s.length/2;
  for(var i=0;i<s.length;i++){if(s.charAt(i)!==" ")continue;var L=s.slice(0,i),R=s.slice(i+1);if(L.length<8||R.length<8)continue;
   var w=L.split(" ").pop(),sc=Math.abs(i-mid);if(/,$/.test(w))sc-=9;else if(GOOD.test(w)||(w.length>=3&&GOOD3.test(w)))sc-=4;if(/[…]$/.test(w))sc-=3;if(sc<bs){bs=sc;best=i}}
  if(best<0)return s;var a=s.slice(0,best),b=s.slice(best+1);return wrap1(a)+"\n"+wrap1(b)}
 /* 한 쪽에 한 의미 문장, 최대 두 줄(2026-10-09 2차 피드백: '한 번 누를 때 시각적 한 줄' 정책 정정).
    실제 대사창과 같은 글꼴·폭으로 줄 수를 재서, 두 줄 안에 들어가면 문장을 통째로 한 쪽에 둔다.
    세 줄 이상이 될 때만 뜻이 이어지는 자리(쉼표·연결 어미·조사)에서 다음 쪽으로 넘긴다. 글자 크기는 바꾸지 않는다. */
 var MZ=null,MC={};
 function textW(){try{var d=document.getElementById("dtxt");if(d&&d.clientWidth>40)return d.clientWidth}catch(e){}return Math.min(innerWidth*.75,900,innerWidth-32)-32-(innerHeight<380?110:122)}
 function nLines(t,w){var k=w+"|"+t;if(MC[k])return MC[k];try{if(!MZ){MZ=document.createElement("div");MZ.setAttribute("aria-hidden","true");MZ.style.cssText="position:fixed;left:-9999px;top:0;visibility:hidden;pointer-events:none;font-family:Galmuri11B,Galmuri11,monospace;line-height:24px;word-break:keep-all;white-space:pre-wrap;overflow-wrap:break-word;padding:0;margin:0";document.body.appendChild(MZ)}
   var d=document.getElementById("dtxt"),fs=d?getComputedStyle(d).fontSize:(getComputedStyle(document.body).getPropertyValue("--t-story")||"16px");MZ.style.fontSize=fs;MZ.style.lineHeight=(parseFloat(fs)*1.5)+"px";MZ.style.width=w+"px";MZ.textContent=t;var n=Math.max(1,Math.round(MZ.offsetHeight/(parseFloat(fs)*1.5)));MC[k]=n;return n}catch(e){return Math.ceil(t.length/30)}}
 window.__innLines=function(t){return nLines(t,textW())};
 function fits2(t,wrapInner){return nLines(wrapInner?"("+t+")":t,textW())<=2}
 function splitAt(s){var best=-1,bs=1e9,mid=s.length/2;
  for(var i=0;i<s.length;i++){if(s.charAt(i)!==" ")continue;var L=s.slice(0,i),R=s.slice(i+1);if(L.length<8||R.length<8)continue;
   var w=L.split(" ").pop(),sc=Math.abs(i-mid);if(/,$/.test(w))sc-=9;else if(GOOD.test(w)||(w.length>=3&&GOOD3.test(w)))sc-=4;if(/[…]$/.test(w))sc-=3;if(sc<bs){bs=sc;best=i}}
  return best}
 function splitLong(s,inner){if(s.indexOf("\n")>=0||fits2(s,inner))return [s];var b=splitAt(s);if(b<0)return [s];
  return splitLong(s.slice(0,b),inner).concat(splitLong(s.slice(b+1),inner))}
 function pageLine(x){if(!Array.isArray(x)||typeof x[1]!=="string"||typeof x[0]!=="string"||x[0].charAt(0)==="@")return [x];
  var t=x[1];if(t.indexOf("<")>=0)return [x];var inner=x[0]==="narr"&&/^\(.*\)$/.test(t),body=inner?t.slice(1,-1):t;
  /* 2026-10-10 사용자 확정 "클릭이 너무 많다": 같은 줄의 짧은 문장 둘이 각각 한 줄에 들고 합쳐 두 줄 안이면 한 쪽에 문장마다 줄을 바꿔 담는다.
     그 밖의 문장만 예전처럼 쉼표 두 줄·긴 문장 나누기. 글자 크기는 바꾸지 않고, 한 줄로 길게 밀어 넣지 않는다 */
  var raw=joinShort(sents(body));if(!raw.length)return [x];var W0=textW(),wr=function(t){return inner?"("+t+")":t},one=function(t){return t.indexOf("\n")<0&&nLines(wr(t),W0)===1};
  var packed=[];raw.forEach(function(q){var pv=packed.length?packed[packed.length-1]:null;
   if(pv&&!pv.j&&one(pv.t)&&one(q)&&nLines(wr(pv.t+"\n"+q),W0)<=2){pv.t=pv.t+"\n"+q;pv.j=1}
   else if(pv&&pv.j&&q.length<=8&&nLines(wr(pv.t+" "+q),W0)<=2){pv.t=pv.t+" "+q}   /* 짧은 꼬리 문장("둘입니다.")만 따로 한 쪽이 되지 않게 둘째 줄 끝에 */
   else packed.push({t:q,j:0})});
  var parts=packed.map(function(o){return o.j?o.t:(BRK[o.t]||commaBreak(o.t))});
  var segs=[];parts.forEach(function(p){if(p.indexOf("\n")>=0&&nLines(wr(p),W0)<=2){segs.push(p);return}splitLong(p,inner).forEach(function(q){segs.push(q)})});
  return segs.map(function(p,k){var y=x.slice();y[1]=inner?"("+p+")":p;y[7]=t;if(k>0){if(y[3]==="testi")y[3]="";if(y[5]!=null)y[5]=""}return y})}
 window.__innPageCold=function(L){try{var o=[];(L||[]).forEach(function(b){if(!b||typeof b.say!=="string"){o.push(b);return}var parts=joinShort(sents(b.say));if(parts.length<2&&fits2(b.say)){o.push(b);return}
   /* 2026-10-10 대사 쪽 규칙과 같게: 한 줄짜리 짧은 문장 둘은 한 쪽에 문장마다 줄바꿈 */
   var W1=textW(),pk=[];parts.forEach(function(q){var pv=pk.length?pk[pk.length-1]:null;if(pv&&pv.indexOf("\n")<0&&nLines(pv,W1)===1&&nLines(q,W1)===1&&nLines(pv+"\n"+q,W1)<=2)pk[pk.length-1]=pv+"\n"+q;else pk.push(q)});
   if(pk.length===1&&pk[0].indexOf("\n")>=0){var c1={};for(var k1 in b)c1[k1]=b[k1];c1.say=pk[0];o.push(c1);return}parts=pk;
   var zEnd=(b.z||1)*(b.push?1+b.push/100:1)/(b.pull?1+b.pull/100:1),segs=[];parts.forEach(function(p){if(p.indexOf("\n")>=0){segs.push(p);return}splitLong(p).forEach(function(q){segs.push(q)})});
   segs.forEach(function(p,i){var c={};for(var k in b)c[k]=b[k];c.say=p;if(i>0){delete c.sfx;delete c.wait;delete c.push;delete c.pull;delete c.fxs;c.z=zEnd;c.id=(b.id||"")+"_"+i}o.push(c)})});return o}catch(e){return L}};
 /* 타이핑 호흡: 방금 찍은 글자 뒤에 쉴 틱 수(1틱 = 대사 속도 간격). 1장에서만 */
 /* 대사 빠르기(2026-10-10): 인물 성격 기본값 × 대사 내용. 1보다 크면 느리게.
    나비·다람은 밝고 빠르게, 세련은 매끄럽게 조금 빠르게, 할머니·도토·밤이는 느리게(나이·망설임·졸음), 너울은 또박또박 */
 var TEMPO={det0:1.05,det1:.8,innma:1.6,seryeon:.9,nabi:.75,geokkuri:1.6,buri:.95,wanggu:1.2,doto:1.45,karo:1};   /* 2026-10-10 "할머니 대사가 다람이 속도": 차이를 크게(할머니 48ms/자 vs 다람 24ms/자) */
 window.__innTempo=function(l,full){if(!cur()||!l)return 1;var w=l.who,t=String(full||""),m=String(l.mood||"");var f=TEMPO[w]||1;
  if(/^\(/.test(t))f=Math.max(f,1)*1.0;                                   /* 속마음: 차분히 */
  var ex=(t.match(/!/g)||[]).length,el=(t.match(/…|\.\./g)||[]).length;
  if(ex)f*=t.length<14?.72:.85;                                            /* 외침·다급: 빠르게 */
  if(el>=2)f*=1.18;else if(el===1&&!ex)f*=1.08;                          /* 머뭇거림: 느리게 */
  if(/nervous|panic|shock/.test(m))f*=.86;if(/sad/.test(m))f*=1.2;
  if(/^(앗|헉|엇|으악|아악|어머|어\?)/.test(t))f*=.7;
  return Math.max(.55,Math.min(1.9,f))};
 window.__innPace=function(full,n){if(!cur())return 0;var ch=full.charAt(n-1),nx=full.charAt(n);if(n>=full.length)return 0;
  if(ch==="…"||(ch==="."&&nx==="."))return 7;                          /* 말줄임: 점마다 */
  if(/[.?!]/.test(ch)&&/[\s)」"”]/.test(nx||" "))return 12;              /* 문장 끝 */
  if(ch===",")return 8;                                                /* 2026-10-10: 쉼표에서 한 박자 멈춤(약 0.25초) */                                                /* 쉼표 */
  if(ch==="\n")return 2;
  var k=full.indexOf("…",n);if(k>0&&k-n<2&&k-n>=0&&/[^\s]/.test(nx))return 1;   /* 말줄임 바로 앞 글자는 느리게 */
  return 0};
 /* 대본에서 의도한 줄바꿈(같은 쪽 두 줄). 문장은 그대로, 줄만 나눈다 */
 /* 2026-10-10 "대사를 두 줄로": 한 줄에 들어가도 18자 이상이고 쉼표가 있으면, 가운데에 가까운 쉼표 뒤에서 줄을 바꿔 두 줄 한 쪽으로(문장은 그대로) */
 function commaBreak(p){if(p.indexOf("\n")>=0||p.length<18)return p;var best=-1,bs=1e9,mid=p.length/2;for(var i=0;i<p.length-1;i++){if(p.charAt(i)===","&&p.charAt(i+1)===" "){var L=i+1,R=p.length-i-2;if(L<7||R<6)continue;var sc=Math.abs(i-mid);if(sc<bs){bs=sc;best=i}}}
  if(best<0)return p;var a=p.slice(0,best+1),b=p.slice(best+2);try{if(nLines(a,textW())>1||nLines(b,textW())>1)return p}catch(e){}return a+"\n"+b}
 var BRK={"두 사람 방은 앞 계단 쪽, 끝에서 둘째 방이에요.":"두 사람 방은 앞 계단 쪽,\n끝에서 둘째 방이에요."};
 /* 같은 화자의 이어진 짧은 줄(한 쪽짜리 두 줄)도 합쳐 두 줄 안이면 한 쪽으로. 화자가 바뀌면 따로. 표정·얼굴·증언 표시·연출 신호가 있는 줄, 무대 연출(컷·이름 공개·인물 신호)이나
    놀람 효과음이 걸린 줄은 합치지 않는다 */
 function cueHit(t){try{if((window.__INNCUE||{})[t])return true;if(/^(앗|헉|엇|으악|아악|어머|세상에)|\?!|!\?/.test(t))return true;
   var L=[].concat(typeof CUT!=="undefined"?CUT:[],typeof CUT2!=="undefined"?CUT2:[]);for(var i=0;i<L.length;i++)if(L[i].re&&L[i].re.test(t))return true;
   if(typeof REVEAL!=="undefined")for(var k in REVEAL)if(t.indexOf(REVEAL[k])>=0)return true}catch(e){return true}return false}
 function plain(x){if(!Array.isArray(x)||typeof x[0]!=="string"||typeof x[1]!=="string"||x[0].charAt(0)==="@"||/[<{]/.test(x[1])||x.length>8)return false;for(var i=3;i<=5;i++)if(x[i])return false;return true}
 function mergeSame(a){var o=[];for(var i=0;i<a.length;i++){var y=a[i],p=o.length?o[o.length-1]:null;
   if(p&&p.__one&&y&&y.__one&&p[0]===y[0]&&String(p[2]||"")===String(y[2]||"")&&String(p[6]||"")===String(y[6]||"")){
    var pi=/^\(.*\)$/.test(p[1]),yi=/^\(.*\)$/.test(y[1]);if(pi===yi){var tx=pi?"("+p[1].slice(1,-1)+"\n"+y[1].slice(1,-1)+")":p[1]+"\n"+y[1];
     if(nLines(tx,textW())<=2){var m=p.slice();m[1]=tx;m[7]=ot(p)+" "+ot(y);m.__one=false;o[o.length-1]=m;continue}}}
   o.push(y)}return o}
 window.__innPage=function(lines){try{if(!cur()||!Array.isArray(lines))return lines;var o=[];lines.forEach(function(x){var pg=pageLine(x);
   if(pg.length===1&&plain(x)&&!cueHit(ot(x))&&!cueHit(String(x[1]))&&pg[0][1].indexOf("\n")<0&&nLines(pg[0][1],textW())===1){var z=pg[0].slice();z.__one=true;if(z[7]==null)z[7]=x[1];pg=[z]}
   pg.forEach(function(y){o.push(y)})});o=mergeSame(o);o.forEach(function(y){if(y&&y.__one)delete y.__one});return o}catch(e){return lines}};
 window.__innSayX=function(base,self,lines,done,sk){return split(base,self,talkEntry(lines),done,sk)};
 /* 힌트: 1장은 단계가 잠겨 있다(햇빛 → 머리판 → 자물쇠 → 장부 → 돋보기). 잠긴 지점을 '남은 곳'으로 세거나 가리키지 않고, 지금 해야 할 단계를 말한다 */
 try{var _ns2=nextStep;nextStep=function(c){try{if(cur()&&!G.battle){var b=G.beats||{},has=function(id){return G.found.indexOf(id)>=0},LI=function(id){for(var i=0;i<c.locations.length;i++)if(c.locations[i].id===id)return i;return null};
   var sun=!!(window.__innSun&&window.__innSun());
   if(sun&&!b.inn_lock&&!has("C11"))return {say:"아빠, 창고에 해가 들었을 거야. 열세 번째 침대 머리판을 다시 보자. 아까 안 보이던 글씨가 보일지도 몰라.",tab:"scene",loc:LI("bed13")};
   if(b.inn_lock&&!has("C11"))return {say:"상자가 열렸어. 창고 침대 밑 상자 안을 살펴보자.",tab:"scene",loc:LI("bed13")};
   if(has("C11")&&!has("C05"))return {say:"부엌 바구니 속 아이를 할머니 돋보기로 다시 보자.",tab:"scene",loc:LI("kitchen")};
  }}catch(e){}return _ns2.apply(this,arguments)}}catch(e){MISS.push("stage hint")}
 /* 조사 화면에서 배경 그림에 없는 단서 물건(복도 벽시계, 접수대 숙박부)을 증거 도트로 그 자리에 보여 준다. 정식 소품 그림이 오면 교체 */
 var PROP={hall:[["C06","art/evidence/inn/C06.png",5]]};   /* 2026-10-09: 문틀 위에 떠 보이던 자리 → 문 오른쪽 벽면(patches/15_hall.py) */   /* 복도 벽시계: 월드 소품 납품 전까지 증거 도트(C06, 숫자 없음·바늘 없음 그대로) */
 /* 접수대 숙박부: 납품된 월드 소품 WP_C09(빈 종이)를 배경 파노라마 좌표(858,372,174,38)에 그대로 놓는다 */
 var WPROP={front:[["art/ch1/bg/WP_C09_lodging_ledger.png",858,372,174,38]]};
 function props(){try{var sc=document.getElementById("bigscene");if(!sc)return;[].slice.call(sc.querySelectorAll(".innprop")).forEach(function(e){e.remove()});
  [].slice.call(sc.querySelectorAll("image.innwprop")).forEach(function(e){e.remove()});
  if(!cur()||G.tab!=="scene"||!(G.beats&&G.beats.inn_pro)||G.beats.inn_final)return;var l=CASES[G.ci].locations[G.loc],P=l&&PROP[l.id],WP=l&&WPROP[l.id];
  if(WP){var sv=sc.querySelector("svg[data-bg]");if(sv)WP.forEach(function(w){var im=document.createElementNS("http://www.w3.org/2000/svg","image");im.setAttribute("class","innwprop");im.setAttribute("href",w[0]);im.setAttribute("x",w[1]);im.setAttribute("y",w[2]);im.setAttribute("width",w[3]);im.setAttribute("height",w[4]);im.setAttribute("style","image-rendering:pixelated");sv.appendChild(im)})}
  if(!P)return;
  P.forEach(function(p){var h=sc.querySelector('[data-spot="'+p[0]+'"]')||sc.querySelector('[data-done="'+p[0]+'"]');   /* 살펴본 뒤(체크 표시)에도 벽시계는 그 자리에 남는다 */if(!h||!h.parentElement)return;var im=document.createElement("img");im.className="innprop";im.alt="";im.src=p[1];
   im.style.left=h.style.left;im.style.top=h.style.top;im.style.width=p[2]+"%";h.parentElement.insertBefore(im,h)})}catch(e){}}
 try{var _rp=render;render=function(){var r=_rp.apply(this,arguments);props();return r}}catch(e){MISS.push("stage props")}
 /* 아침 해: 첫 조사 단서(I1~I6)를 다 모은 순간 한 번, 창고가 달라졌다는 것을 이야기로 알린다(힌트를 쓰지 않아도 다음 단계가 보이게) */
 setInterval(function(){try{if(!cur()||!G.beats||!G.beats.inn_pro||G.beats.inn_final||G.beats.inn_sunnote||G.tab!=="scene")return;if(!(window.__innSun&&window.__innSun()))return;
  if((typeof DL!=="undefined"&&DL)||document.querySelector("#ov .modal,#mveil .modal,#innins,.banner,body>.rt,#wmap,#w209rail.more,.crec2,.placecard"))return;G.beats.inn_sunnote=1;try{saveProg()}catch(e){}
  say([["narr","(창밖이 환해졌다. 아침 해가 창고 창에도 들었겠다.)"],["det1","아빠, 해 떴다! 창고 침대 머리판 글씨, 이제 보일까?"],["det0","가 보자. 아까는 어두워서 못 읽었으니까."]],function(){render()})}catch(e){}},250);
 /* 질문 화면·조사 화면에서 엔진이 그리는 할머니(art/body/innma-N)도 같은 v5로 맞춘다. 같은 146×182 캔버스라 위치는 그대로 */
 var BODY2V5={"art/body/innma-0.png":INNMA["0"],"art/body/innma-1.png":INNMA["1"],"art/body/innma-2.png":INNMA["2"]};
 function innmaSwap(){try{if(!cur())return;document.querySelectorAll('img[src^="art/body/innma-"],image[href^="art/body/innma-"]').forEach(function(e){var a=e.tagName.toLowerCase()==="img"?"src":"href",v=BODY2V5[String(e.getAttribute(a)||"").split("?")[0]];if(v)e.setAttribute(a,v)})}catch(e){}}
 try{var _rp3=render;render=function(){var r=_rp3.apply(this,arguments);innmaSwap();return r}}catch(e){}
 setInterval(innmaSwap,300);
 try{var _say2=say;say=function(lines,done,sk){return split(_say2,this,lines,done,sk)}}catch(e){MISS.push("stage say")}
 var css=document.createElement("style");css.id="inn-stage-css";css.textContent=[

  /* 관찰 컷: 복도 배치도 */
  "#innplan{position:absolute;left:50%;top:max(10px,3vh);width:min(560px,70vw);transform:translateX(-50%) translateY(6px);opacity:0;transition:opacity .25s,transform .25s;z-index:4;filter:drop-shadow(0 6px 0 rgba(0,0,0,.35))}",
  "#innplan.in{opacity:1;transform:translateX(-50%)}#innplan svg{display:block;width:100%;height:auto;max-height:calc(100vh - 150px)}",
  "#innstage.cut .isf{filter:brightness(.55)!important}",
  "#inncut{position:absolute;left:50%;top:max(8px,2vh);height:calc(100vh - 118px);aspect-ratio:16/9;max-width:calc(100vw - 32px);transform:translateX(-50%);opacity:0;transition:opacity .3s;z-index:4;border:4px solid #3B2A1E;box-shadow:0 0 0 3px #B98A3E,0 8px 0 rgba(0,0,0,.4);background:#000}",
  "#inncut.in{opacity:1}#inncut img{display:block;width:100%;height:100%;object-fit:cover;image-rendering:pixelated}#innstage.cut2 .isf{opacity:0!important}",
  "#innplan text{font-family:var(--display,sans-serif);fill:#3B2A1E}#innplan .pt{font-size:15px}#innplan .lb{font-size:12px}",
  "#innplan .bn{font-size:14px;fill:#FFF6DA;stroke:#1C2A30;stroke-width:3px;paint-order:stroke;opacity:0;transition:opacity .2s}#innplan.s1 .bn{opacity:1}",
  "#innplan .far{opacity:0;transition:opacity .4s}#innplan.s2 .far{opacity:1}",
  "#innplan .n13{opacity:0!important}#innplan.s3 .n13{opacity:1!important;fill:#FFD9D0;stroke:#9A2A1E}",
  "#innplan .dshut{opacity:0;transition:opacity .3s}#innplan.s4 .dshut{opacity:1}#innplan.s4 .dopen{opacity:0}",
  /* 근접 조사 */
  "#innins{position:fixed;inset:0;z-index:120;background:rgba(14,10,8,.72);display:flex;align-items:center;justify-content:center;padding:10px 16px;box-sizing:border-box}",
  "#innins .iin{background:#F8F0DC;border:4px solid #B98A3E;box-shadow:0 0 0 3px #3B2A1E,0 8px 0 rgba(0,0,0,.4);width:min(720px,100%);height:min(380px,100%);box-sizing:border-box;padding:10px 18px 12px;display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-rows:auto minmax(0,1fr) auto;gap:6px 20px;color:#3B2A1E;overflow:hidden}",
  "#innins .ihd{grid-column:1/-1;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}#innins .ihd small{font-size:var(--t-cap);color:#8A5E36}#innins .ihd b{font-size:var(--t-head);font-family:var(--display,sans-serif)}",
  "#innins .ipg{margin-left:auto;display:flex;gap:6px}#innins .ipg i{font-style:normal;font-size:var(--t-cap);padding:2px 8px;border:2px solid #B98A3E;color:#8A5E36}#innins .ipg i.on{background:#B98A3E;color:#FFF6DA}",
  "#innins .iart{grid-row:2/4;grid-column:1;display:flex;align-items:center;justify-content:center;min-height:0;height:100%}",
  "#innins .icap{grid-column:2;font-size:var(--t-story);line-height:1.55;margin:0;align-self:center}",
  "#innins .ibtns{grid-column:2;display:flex;gap:8px;justify-content:flex-end;align-self:end}",
  "html body #innins button.ib{all:unset;box-sizing:border-box;font-family:var(--display,sans-serif);font-size:var(--t-ui);min-height:44px;padding:8px 18px;background:#E2B655;border:3px solid #3B2A1E;color:#2A1C10;cursor:pointer;white-space:nowrap;display:inline-flex;align-items:center}",
  "html body #innins button.ib.ghost{background:#F8F0DC}html body #innins button.ib:focus-visible{outline:3px solid #2F6672;outline-offset:2px}",
  "#innins .iart{cursor:zoom-in;position:relative}#innins .iart::after{content:'눌러서 크게';position:absolute;right:0;bottom:0;font-size:var(--t-cap);color:#8A5E36;background:rgba(248,240,220,.9);padding:1px 6px}",
  "#innins .iart.big{position:fixed;inset:0;z-index:5;background:rgba(14,10,8,.92);cursor:zoom-out;display:flex;align-items:center;justify-content:center}#innins .iart.big::after{content:'눌러서 닫기'}",
  "#innins .iart.big .ilay,#innins .iart.big .icl{height:96vh!important;width:auto}#innins .iart.big .ipaper{height:90vh!important}",
  "#innins .ilay{position:relative;display:block;height:min(300px,calc(100vh - 96px));aspect-ratio:1}#innins .ilay img{position:absolute;inset:0;width:100%;height:100%}#innins .ilay .ib0{image-rendering:pixelated}",
  "#innins .ibook{font-size:var(--t-cap)!important;border-bottom:1px solid #C9B48A;padding:4px 0}#innins .ibook.hl{background:rgba(226,182,85,.25)}",
  "#innins .icl{display:block;height:min(300px,calc(100vh - 96px));aspect-ratio:1;image-rendering:pixelated}",
  "#innins .ipouch{position:relative;height:min(230px,calc(100vh - 150px));aspect-ratio:1}#innins .ipouch img{width:100%;height:100%;object-fit:contain;image-rendering:pixelated}",
  "#innins .iband{position:absolute;left:14%;right:14%;top:30%;height:17%;background:#EFE3C4;border:2px solid #6B4A2B;display:flex;align-items:center;justify-content:center;transform:rotate(-4deg)}",
  "#innins .istamp{color:#B3261E;border:2px solid #B3261E;padding:0 6px;font-size:var(--t-label);font-family:var(--display,sans-serif);display:inline-flex;align-items:center;gap:2px;background:rgba(255,255,255,.35)}",
  "#innins .cstar{width:1.1em;height:1.1em;color:#B3261E}",
  "#innins .ipaper{height:min(250px,calc(100vh - 140px));aspect-ratio:3/4;background:#FFFBEF;border:2px solid #6B4A2B;box-shadow:4px 4px 0 #C9B48A;padding:12px;box-sizing:border-box;display:flex;flex-direction:column;gap:8px}",
  "#innins .ipaper b{font-size:var(--t-label);text-align:center}#innins .ipaper p{margin:0;font-size:var(--t-cap);line-height:1.5}",
  "#innins .isig{display:flex;align-items:center;gap:8px}#innins .isig:first-of-type{margin-top:auto}#innins .isig span{font-size:var(--t-cap);width:3.5em;flex:none}#innins .iblank{flex:1;height:26px;border:2px dashed #8A5E36}",
  "#innins .isig em{flex:1;font-style:normal;font-size:var(--t-label);border-bottom:2px solid #3B2A1E;display:flex;align-items:center;gap:2px}#innins .isig em .cstar{color:#3B2A1E}",
  "#innins .ipaper.back{justify-content:center}#innins .iclause{text-align:center;font-size:var(--t-cap)!important;border:2px solid #8A5E36;padding:10px 6px}",
  "@media (max-height:380px){#innins .iin{padding:10px 14px}#innins .icap{line-height:1.45}}",
  /* 이불 손자국: 천 위 가루처럼 */
  "svg[data-inn-world=\"bed13\"] image[data-world-prop=\"C02_trace\"]{opacity:.55;mix-blend-mode:screen;filter:sepia(.25) saturate(.7)}",
  "#vnbox .nx.end{font-size:var(--t-cap)!important}",
  "html body #mveil .modal small.found-at,html body #ov .modal small.found-at{display:block;margin:-2px 0 6px;color:#8A5E36;font-size:var(--t-cap)!important}",
  "#innstage{position:absolute;inset:0;z-index:2;pointer-events:none;overflow:hidden}",
  "#innstage .isf{position:absolute;opacity:0;transition:opacity .22s,filter .15s}",
  "#innstage.seated .isf{display:none!important}",
  "#innstage .isf.in{opacity:1}#innstage .isf.ls{filter:brightness(.84) saturate(.9)}",
  "#innstage .isf img{position:absolute;left:0;top:0;image-rendering:pixelated;max-width:none}",
  "#innstage .isf[data-face] svg{width:100%;height:100%}",
  "html body.w209.inn-st2 #dlgveil #vnfig,html body.w209.inn1.tab-scene #dlgveil #vnfig{display:none!important}",
  /* 얇은 대사창(레퍼런스: 배경을 넓게, 하단에 얇게) */
  "html body.w209.inn1 #dlgveil #vnbox .vband.bot{height:auto!important;min-height:0!important;max-height:40vh}",
  "html body.w209.inn1 #dlgveil #vnbox .vband.bot .vtxt{padding:15px 16px 9px!important;min-height:0!important}",
  /* 질문 화면의 이전·다음 사람(명단) 넘기기: 다른 장소 인물로 배경이 바뀌므로 1장에서는 쓰지 않는다. 같은 장소의 다른 인물은 조사 화면에서 직접 눌러 만난다 */
  "html body.w209.inn1 .fstalk .whonav{display:none!important}",
  /* 질문 목록: 이미 물어본 주제는 체크 표시(흐림과 함께) */
  "html body.w209.inn1 .fstalk .topic.done::after{content:'✓';margin-left:auto;padding-left:8px;color:#2F6672;font-weight:700}",
  "html body.w209.inn-st2 #vnbox .vband.narr .txt,html body.w209.inn-st2 .veil.vn2 .vband.bot.narr .vtxt{color:#E8DCBC!important}",
  /* 아빠의 속마음(괄호): 옅은 푸른 글씨, 크기는 일반 대사와 같게 */
  "html body.w209.inn1 #vnbox .vband.narr:not(.inner) #dtxt{color:#CFC4AE!important}",
  "html body.w209.inn1 #vnbox .vband.inner .txt,html body.w209.inn1 #vnbox .vband.inner #dtxt{color:#8CC4FF!important}",
  /* 대화·연출 중 이동 버튼은 보이지도 눌리지도 않게 */
  "html body.w209.inn-cut .stage .fsa,html body.w209.inn-cut .stage.inn-world-stage .fsa,html body.w209.dl-on .stage.inn-world-stage .fsa{visibility:hidden!important;pointer-events:none!important}",
  "html body.w209 .stage.inn-fill{background:#120d0a!important;overflow:hidden}",
  "html body.w209 .stage.inn-fill::before{content:'';position:absolute;inset:-24px;background:var(--innfill) center/cover no-repeat;filter:blur(10px) brightness(.42) saturate(.85);z-index:0;pointer-events:none}",
  "html body.w209 .stage.inn-fill>.fsscroll{position:relative;z-index:1}",
  "html body.w209.inn-full .stage>.fsscroll>#bigscene{width:100vw!important;max-width:none!important;margin:0!important;left:0!important}",
  "html body.w209.inn-full #bigscene>svg[data-bg]{width:100%!important;height:100%!important}",
  ":root{--t-story:16px;--t-ui:15px;--t-label:13px;--t-cap:12px;--t-head:19px}",
  "body.inn-fs-small{--t-story:15px}body.inn-fs-large{--t-story:18px}",
  /* 이야기 글 18 */
  "html body #inncold .box p,html body #mveil .modal p,html body #mveil .modal .soft,html body #mveil .modal span:not(.kicker):not(.n),html body #app .nt,html body #innpvt{font-size:var(--t-story)!important;line-height:1.55!important}",
  /* 버튼 16 */
  "html body #innmain .menu button,html body #innopt button,html body #innopt .lb,html body #innopt .vv,html body #mveil .modal .btn,html body #okfind,html body .innconf button{font-size:var(--t-ui)!important}",
  /* 이름표·소제목 15 */
  "html body #vnbox .plate,html body #inncold .box b,html body #inncold .tag,html body #inncold .sk,html body #logb,html body #mveil .modal .kicker,html body #mveil .modal b,html body #app .notice b,html body #app .nt b,html body #closeNotice,html body #app .hud b,html body #app b{font-size:var(--t-label)!important}",
  /* 보조 글 13 */
  "html body #innmain small,html body #innmain .pv,html body #innopt small,html body #app small,html body #memobtn .sb,html body #memobtn button,html body #w209rail button,html body #w209rail .n,html body #mveil .modal small{font-size:var(--t-cap)!important}",
  "html body.w209.inn1 #w209rail button,html body.w209.inn1 #w209rail button.on,html body.w209.inn1 #memobtn button.sb,html body.w209.inn1 #memobtn button{font-size:var(--t-cap)!important}",
  /* 제목 22 */
  "html body #mveil .modal h3,html body #innopt h2{font-size:var(--t-head)!important}",
  /* 회의 말풍선 본문도 이야기 글과 같은 크기·행간(이전 15px/1.45) */
  "html body.rtg div.rt .rt-bub p,html body div.rt .rt-bub p{font-size:var(--t-story)!important;line-height:1.55!important}",
  /* ---- 조밀화(2026-10-09 실기기 피드백): 글자·터치 영역을 일괄 축소하지 않고 레이아웃 요소의 여백·높이를 줄인다 ---- */
  /* 대사 본문: 모든 줄 종류(발화·속마음·지문) 같은 크기·행간, 두 줄 높이를 미리 잡아 줄 수가 바뀌어도 창이 출렁이지 않게 */
  "html body.w209 #dlgveil #vnbox #dtxt,html body.w209 #dlgveil #vnbox .txt{font-size:var(--t-story)!important;line-height:1.5!important;min-height:1.5em;text-align:left!important}",
  /* 대사창: 인물이 서는 가운데에 좁게(눈이 화면 왼쪽 끝까지 가지 않게), 그 안에서 왼쪽 정렬. 한 쪽에 한 줄 */
  "html body.w209.inn1 #dlgveil #vnbox .vband.bot{left:50%!important;right:auto!important;width:min(75vw,900px,calc(100vw - 32px))!important;max-width:none!important;transform:translateX(-50%)!important}",   /* 대화 UI v3(2026-10-09 확정): 가운데 약 75% 폭 */
  "html body #inncold .box{left:50%!important;right:auto!important;width:min(540px,calc(100vw - 32px))!important;transform:translateX(-50%)!important}",
  "html body.w209.inn1 #dlgveil #vnbox .plate{font-size:var(--t-label)!important;line-height:16px!important;padding:0 8px!important;top:-16px!important;min-height:0!important}",
  "html body.w209 #dlgveil #vnbox .nx{bottom:3px!important}",
  /* 기록 버튼: 보이는 크기는 작게, 누르는 영역은 ::after로 44px 유지 */
  "html body.w209 #dlgveil #logb{min-height:30px!important;height:30px!important;padding:0 9px!important;font-size:var(--t-label)!important;border-width:2px!important;top:8px!important;left:8px!important}",
  "html body.w209 #dlgveil #logb::after{content:'';position:absolute;left:-7px;right:-7px;top:-7px;bottom:-7px}",
  "html body #innhintt{font-size:var(--t-cap)!important;padding:4px 10px!important;top:10px!important}",
  /* 질문 화면: 위 빈 띠 제거, 질문 단추 높이 40 */
  "html body.w209.inn1 .fstalk .tpanel{padding:8px!important}",
  "html body.w209.inn1 .fstalk .topic{min-height:40px!important;padding:6px 10px!important;font-size:var(--t-ui)!important;line-height:1.3!important}",
  "html body.w209.inn1 .fstalk .tname{padding:1px 10px!important;min-height:0!important;font-size:var(--t-ui)!important}",
  "html body.w209.inn1 #w209back{min-height:36px!important;height:36px!important;padding:0 10px!important;font-size:var(--t-ui)!important}",
  "html body.w209.inn1 #w209back::after{content:'';position:absolute;left:-4px;right:-4px;top:-4px;bottom:-4px}",
  /* 조사 화면: 장소 카드·메모·오른쪽 도구 줄 */
  "html body.w209.inn1 #app .hud{padding:5px 9px!important}",
  "html body.w209.inn1 #memobtn{min-height:30px!important;height:30px!important}",
  "html body.w209.inn1 #w209rail{gap:6px!important}",
  "html body.w209.inn1 #w209rail button{width:42px!important;height:42px!important;min-height:0!important;border-width:1.5px!important}",
  /* 회의: 공개 득표 칸이 말풍선 위쪽(이름표)과 겹치던 문제 → 왼쪽 시계 아래로, 두 줄까지 접힘 */
  "#bigscene .innprop{position:absolute;transform:translate(-50%,-50%);height:auto;image-rendering:pixelated;pointer-events:none;z-index:1;filter:drop-shadow(0 2px 0 rgba(0,0,0,.45))}",
  /* 질문 대화 중 아빠·다람·속마음 줄에서도 상대(질문 대상)를 화면에 그대로 둔다. 다람 큰 그림으로 바뀌지 않게(대화 중 상대 유지 기준) */
  "html body.w209.inn1.tab-talk.vn-other .fstalk .tfig{visibility:visible!important}",
  "html body.w209.inn1.tab-talk #dlgveil #vnfig{display:none!important}",
  "html body #inncold .box p{white-space:pre-line!important}",
  /* iPhone 가로 화면의 글자 자동 확대(텍스트 오토사이징)가 장면마다 글자를 다르게 키우던 원인 후보: 끈다 */
  /* 법정기록 결합 모드: 결합 안내 줄(.cr-comb)이 격자 첫 칸에 자동 배치되며 첫 열을 넓혀 증언 탭·닫기 단추를 밀어내던 문제 → 맨 아래 한 줄 전체로 */
  "html body .crec2 .cr-in>.cr-comb{grid-column:1/-1!important;grid-row:7!important}",
  "html,body{-webkit-text-size-adjust:100%!important;text-size-adjust:100%!important}",
  "html body.rtg #rtgtal{left:8px!important;top:66px!important;transform:none!important;white-space:normal!important;max-width:150px!important;text-align:left!important;line-height:1.35!important}"
 ].join("\n");document.head.appendChild(css);
 window.__innStage=function(){var r=fig&&fig.getBoundingClientRect();return {src:fig&&fig.firstChild&&fig.firstChild.getAttribute?String(fig.firstChild.getAttribute("src")||"").split("/").pop():"",scene:st.scene,who:st.who,fig:fig?(fig.dataset.k+(fig.classList.contains("ls")?"(듣는중)":"")+"@"+Math.round(r.left)+","+Math.round(r.top)+" "+Math.round(r.width)+"x"+Math.round(r.height)):"-"}};
})();
