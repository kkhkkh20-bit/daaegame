 /* ==== 1장 오디오 연출 (큐·효과음 유지, 음악은 피아노 없는 현악 v3 음원) ====
    - 음악: 타이틀 -> 도입(inn_cold) -> 여행·여관 -> 사건 신고 -> 조사 -> 회의·압박 -> 최종 대결·압박 -> 후일담
      같은 곡 안에서는 장면·화자·장소가 바뀌어도 다시 시작하지 않는다(엔진: 같은 키면 그대로 둠). 낮춤은 덕킹으로만.
    - 환경음: 마차(녹음 말발굽 2박 루프), 바깥바람. 장소에 머무는 동안 한 인스턴스만.
    - 타이핑음: 부드럽고 낮게, 최소 간격 75ms. 속마음·지문은 발화보다 낮게. 문장 완성·넘김 때 몰아서 나지 않음(예약 재생 없음). */
 (function(){
  if(!window.__AUD||!__AUD.SONGS)return;
  var A=__AUD;
  function cur(){try{return S.screen==="case"&&!!G&&!!CASES[G.ci]&&CASES[G.ci].id==="inn"}catch(e){return false}}
  function sidOf(pi){try{var E=window.EP1INN||EP;return (E.PRO[pi]&&E.PRO[pi].sid)||("P"+(pi+1))}catch(e){return "P"+(pi+1)}}   /* 2026-10-10: EP는 이 모듈 범위에 없어 장면 번호가 밀려(P6·P8 제외 뒤) 신고 장면에서도 여행곡이 나오던 문제 */
  function beats(){try{return (G&&G.beats)||{}}catch(e){return {}}}
  var RTLINE=null,CUE={mode:null,press:false,ph:null,at:0,line:null};
  function cueLine(l){var ph=window.__rtPh&&window.__rtPh();if(CUE.ph!==ph){CUE.press=false;CUE.ph=ph}if(CUE.line===l)return;CUE.line=l;CUE.mode=l&&l.audio||null;CUE.at=Date.now();if(CUE.mode==="press"||CUE.mode==="impact")CUE.press=true;if(CUE.mode==="calm")CUE.press=false;}
  window.__innAudioLine=function(l){RTLINE=l||null;cueLine(RTLINE)};
  function liveLine(){try{if(DL&&DL.lines)return DL.lines[DL.i];if(document.querySelector("body>.rt"))return RTLINE}catch(e){}return null}
  function lineText(){var l=liveLine();return l?String(Array.isArray(l)?(l[7]||l[1]||""):(l.t||"")):""}
  function lineWho(){var l=liveLine();return l?(Array.isArray(l)?l[0]:l.w):""}
  function lineKind(){if(lineWho()==="narr")return /^\(/.test(lineText())?"inner":"narr";return "say"}

  /* ---- 음악 선택 ---- */
  var M={inv:false,p10:0,fin:0,carStopped:false,bell:false,failure:false};
  window.__innAudioReset=function(){M.obj=0;M.f4=0;M.fin=0;RTLINE=null;CUE={mode:null,press:false,ph:null,at:0,line:null};tenseStop()};
  window.__innAudioFailure=function(on){M.failure=!!on;M.obj=0;M.f4=0;tenseStop()};
  window.__innAudioState=function(){return {line:lineText(),who:lineWho(),cue:CUE.mode,pressure:CUE.press,heartbeat:TENSE.k,failure:M.failure,bell:M.bell,carStopped:M.carStopped,confession:!!M.f4,key:window.__innKeyLine&&window.__innKeyLine()}};
  /* Complete media definitions: no synthesized piano or mismatched character themes. */
  Object.keys(window.__INN_MUSIC||{}).forEach(function(k){A.SONGS[k]=window.__INN_MUSIC[k]});
  /* 솜솜 발견: 털을 알아본 순간 음악을 끊고 한 호흡 정적 → 낮은 두 박 심장음.
     몸/정지/차가움을 차례로 확인하며 긴장을 유지. 생존 확인은 회의에 남겨 둔다. */
  var TENSE={on:false,k:0,gen:0,nul:0};
  var TENSE_ON=/^…상자 뒤에 뭐가 있어|안에 작은 애가 있어|침대 밑에 작은 애가 있어|밑에 작은 애가|^등 뒤 천장에서, 거꾸로 된 두 눈/,TENSE_OFF=/^바구니랑 수건|^작은 몸을 바구니에 옮기고|^모르겠어\. 그러니까 알아봐야지|^다람이 뛰어 돌아가/;
  function tenseStop(){TENSE.on=false;TENSE.gen++;TENSE.nul=0}
  function tenseTick(gen){try{if(!TENSE.on||gen!==TENSE.gen)return;if(!cur()){tenseStop();return}
    if(AC&&AC.state==="running"&&S.sound){var v=TENSE.discovery?.28:.34,gap=TENSE.discovery?Math.max(.72,1.04-TENSE.k*.015):Math.max(.58,.86-TENSE.k*.02);tone(58,.16,"sine",v,0,null,40);tone(52,.14,"sine",v*.7,gap*(TENSE.discovery?.28:.32),null,38);noise(.06,v*.25,0,160,"lowpass");TENSE.k++;setTimeout(function(){tenseTick(gen)},gap*1000)}
    else setTimeout(function(){tenseTick(gen)},300)}catch(e){tenseStop()}}
  window.__innTense=function(){return TENSE.on};
  setInterval(function(){try{if(!cur()||!liveLine()){if(TENSE.on){if(!TENSE.nul)TENSE.nul=Date.now();else if(Date.now()-TENSE.nul>2500)tenseStop()}return}TENSE.nul=0;
    var t=lineText(); /* 좁은 화면에서도 페이지 분할 전 원문으로 큐를 판별 */
    if(TENSE.on&&TENSE.meeting&&CUE.mode!=="pulse")tenseStop();
    if(!TENSE.on&&(TENSE_ON.test(t)||CUE.mode==="pulse")){TENSE.on=true;TENSE.k=0;TENSE.meeting=CUE.mode==="pulse";var gen=++TENSE.gen;
      var discovery=TENSE.discovery=TENSE.meeting||/상자 뒤|작은 애가/.test(t);if(!discovery)try{SFX.cut9&&SFX.cut9()}catch(e){}
      setTimeout(function(){tenseTick(gen)},discovery?1200:450);
    }else if(TENSE.on&&TENSE_OFF.test(t))tenseStop()}catch(e){}},60);
  window.__innWant=function(){
   if(document.getElementById("innmain"))return "inn_title";
   if(!cur())return undefined;
   A.hush=null;A.exp=null;A.pursuit=null;          /* 옛 체계의 일시 정지·승리곡·추격곡이 끼어들어 곡을 다시 시작하지 않게 */
   if(TENSE.on||M.failure||(CUE.ph===(window.__rtPh&&window.__rtPh())&&(CUE.mode==="silence"||CUE.mode==="pulse"||(CUE.mode==="impact"&&Date.now()-CUE.at<800))))return null;                         /* 발견 순간: 음악 없음 */
   var b=beats(),now=Date.now();
   /* 2026-10-10 v2 음악 큐시트(dev/review/CH1_V2_DESIGN.txt 5장): 영화처럼 줄·장면 시점에 맞춰 끊고, 한 방 치고, 다시 들어온다 */
   if(!b.inn_pro){var pi=b.inn_pi|0,sid=sidOf(pi);if(M.sid!==sid){M.sid=sid;M.sidT=now;M.p5c=0;M.hit=0;M.carStopped=false;M.bell=false}if(+String(sid).slice(1)<11)M.inv=false;
    if(sid==="P1"&&now-M.sidT<2000)return null;
    if(sid==="P10"&&M.bell)return null;
    if(sid==="P10b")return null;   /* 밤 복도: 음악 없이 정적(두 눈이 뜰 때 심장 박동) */   /* 제목 카드 뒤 2초 정적 → 여행곡 */
    if(sid==="P13"){if(!M.hit&&/^베개 밑…/.test(lineText())){M.hit=now;try{SFX.cut9()}catch(e){}}if(M.hit&&now-M.hit<1500)return null}   /* 주머니 발견: 음악 끊고 한 방 → 1.5초 정적 */   /* 2026-10-10: 번호(pi<6) 대신 장면 이름으로(도입 재배치 뒤 P11이 5번) */
    if(['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10'].indexOf(sid)>=0)return "inn_travel";   /* P1~P10 */
    if(sid==="P11"){if(/^제 주머니가 없어졌|^계약금이 든 주머니/.test(lineText()))M.inv=true;   /* 2026-10-10: 범죄를 처음 알아채는 줄(세련의 외침)에서 바로 사건곡 */return M.inv?"inn_serious":null}   /* P11: 신고 확인 뒤 */
    return "inn_serious"}                         /* P12 수색·P13 안 쓰는 방: 사건곡(낮게) */
   if(!b.inn_final){var rt=document.querySelector("body>.rt");if(!rt)return "inn_inv";   /* 인물과 짧게 대화해도 같은 조사곡의 재생 위치를 유지한다. */
    var ph=null,E=window.EP1INN||{},fin=false;try{ph=window.__rtPh&&__rtPh();fin=!!(ph&&E.FINAL&&E.FINAL.phases&&E.FINAL.phases.indexOf(ph)>=0)}catch(e){}
    /* 정답 제시('그건 아니야!'/'이걸 봐!') 순간: 음악을 끊고 외침 → 이어서 추궁곡. 그 발언의 대화가 끝나고 1.5초 뒤(또는 단계가 바뀌면) 원래 곡으로 */
    if(fin&&ph===E.FINAL.phases[E.FINAL.phases.length-1]&&lineWho()==="seryeon"&&/^…네\.$/.test(lineText())&&!M.f4){M.f4=now;M.obj=0;try{SFX.cut9()}catch(e){}return null}
    if(M.obj){if(now-M.obj<1400)return null;var dl0=liveLine();if(dl0)M.objDL=now;if(ph!==M.objPh||(!dl0&&now-(M.objDL||M.obj)>1500))M.obj=0;else return CUE.press&&CUE.ph===ph?(fin?"inn_climax_press":"inn_meet_press"):"inn_climax"}
    if(fin&&M.f4){if(now-M.f4<2500)return null;return "inn_t_innma"}   /* 세련 인정("…네.") 뒤: 정적 → 할머니 테마 작게 */
    if(CUE.press&&CUE.ph===ph)return fin?"inn_climax_press":"inn_meet_press";
    if(fin)return "inn_climax";
    return "inn_meet"}                              /* 조사 / 원탁회의 / 최종 대결: 장면마다 다른 곡 */
   M.f4=0;if(M.fin&&Date.now()-M.fin>7000)return null;     /* 마지막 줄 뒤 천천히 끝난 다음 */
   return "inn_after"};
  /* Important facts/emotional lines take a breath; silence does not imply a hit. */
  var KEY=/^…엄마 글씨(?:야|가 맞아)|^긴 정적\. 모두 바구니|^…움직였어|^첫눈은 자정이었어요|^봉인띠와 겹쳐 보시죠|^그렇다면 주막에서 남은 백 냥|^그래서 여쭙겠습니다/;
  window.__innKeyLine=function(){var t=lineText();return !!t&&KEY.test(t)};
  window.__innDuck=function(){var r=window.__innDuck0.apply(this,arguments);if(!cur()||document.getElementById("inncold"))return r;
   if(window.__innKeyLine())return 0;
   return r};
  window.__innDuck0=function(){
   if(document.getElementById("inncold"))return COLDD;   /* 콜드 오픈: 비트마다 정한 낮춤(정적으로 갈수록 작게) */
   if(!cur())return 1;
   var b=beats(),now=Date.now(),f=(typeof DL!=="undefined"&&DL)?.55:1,t=lineText();   /* 대화 중 배경음 .55: 글자·행동 효과음이 묻히지 않게 */
   if(!b.inn_pro){var pi=b.inn_pi|0;
    var sd=sidOf(pi);if(sd!=="P10")M.p10=0;
    if(sd==="P5"){f=.8;if(/^열셋/.test(t))M.p5c=1;if(M.p5c)f=.38}   /* P5 복도: 같은 곡 낮게, "열셋."부터 더 낮게 */
    if(sd==="P10"){if(!M.p10)M.p10=now;f=Math.max(0,1-(now-M.p10)/14000)}   /* P10: 여행곡 천천히 종료 */
    if(sd==="P12")f=.7;if(sd==="P13")f=.6;     /* 수색·발견: 사건곡 낮게 */
    return f}
   if(!b.inn_final){if(M.obj&&document.querySelector("body>.rt"))f*=.72;if(M.f4)f*=.55;return f}   /* 추궁곡·인정 뒤 할머니 테마는 낮게 */
   var ei=b.inn_ei|0;
   if(!b.inn_end&&ei===3){f=.6;if(/^이 사람입니다|^할머니, 아까 그 장부/.test(t))f=0}   /* E4: 엄마 사진을 내미는 순간 정적 */
   if(!b.inn_end&&((ei===2&&/^식사를 마친 뒤, 할머니가 바구니/.test(t))||
      (ei===4&&/^그동안은 아빠한테 읽어 줘|^다람이 마차에서부터 아껴 둔|^아껴 먹어|^고맙다\. 같이 먹자|^아빠는 다람이 먼저/.test(t))))f=.42;   /* 돌봄의 회수: 같은 후일담 현악을 낮게 유지, 충격음·심박 없이 */
   if((!b.inn_end&&ei===4&&/^…올해는 네 딸이 왔다/.test(t))||b.inn_end){if(!M.fin)M.fin=now}
   if(M.fin)f*=Math.max(0,1-(now-M.fin)/6500);
   return f};

  /* ---- 타이핑음 ---- */
  var lastT=0;
  window.__innType=function(kind){try{
   if(TENSE.on||CUE.mode==="pulse"||CUE.mode==="silence")return; /* 정적/박동 구간에는 글자 효과음도 쉰다 */
   if(!S.sound||!AC||AC.state!=="running")return;var now=AC.currentTime;if(now-lastT<.075)return;lastT=now;
   var v=kind==="inner"?.6:kind==="narr"?.7:1;   /* 작고 둥근 클릭, 발음 사이 75ms 여백 */
   tone(560+Math.random()*30,.022,"triangle",.018*v);noise(.01,.016*v,0,1800,"bandpass")}catch(e){}};   /* 예약 없이 현재 글자에만 짧은 소리 */
  var _blip=SFX.blip;
  SFX.blip=function(){if(!cur())return _blip.apply(this,arguments);window.__innType(lineKind())};

  /* ---- 1장 효과음 보정 ---- */
  function wrap(k,fn){var o=SFX[k];SFX[k]=function(){if(!cur())return o&&o.apply(this,arguments);try{fn.apply(this,arguments)}catch(e){}}}
  wrap("door",function(){window.__innRecordedSfx.play("close")});
  wrap("tap",function(){if(S.sound){tone(460,.032,"sine",.04);noise(.018,.014,0,900,"lowpass")}});
  wrap("select",function(){if(S.sound)tone(587.33,.055,"triangle",.035)});
  wrap("page",function(){if(S.sound)noise(.09,.055,0,1400,"bandpass")});
  wrap("found",function(){if(S.sound)[587.33,880].forEach(function(f,i){tone(f,.18,"triangle",.075,i*.08)})});
  wrap("slam",function(){if(!S.sound)return;tone(100,.26,"sine",.55,0,null,45);noise(.18,.45,0,520)});   /* P11 기상: 쾅 1회, 과하지 않게 */
  wrap("letter",function(){});                     /* 장면 제목 글자마다 '틱' 없음 */
  wrap("impact",function(){if(!S.sound)return;if(!document.querySelector("body>.rt")&&!(beats().inn_final&&!beats().inn_end)){tone(660,.5,"sine",.06);tone(990,.35,"sine",.025,.04);return}tone(98,.5,"sine",.3,0,null,62);noise(.25,.12,0,300)});   /* 2026-10-10 검수: 장소·시각 띠마다 쿵 → 회의·최종 대결 밖에서는 부드러운 종 */
  wrap("tick2",function(){});                      /* 빈 곳 터치 '틱' 없음 */
  wrap("roll",function(){});                       /* 옛 드럼롤(마차 대용) 없음 */
  /* 2026-10-10 "앗! 헉! 같은 말에 빠악! 충격음": 날카로운 타격 + 짧은 하강음 */
  SFX.shock9=function(){if(!S.sound)return;try{noise(.09,.5,0,2600,"highpass");tone(1500,.16,"square",.09,0,null,380);tone(110,.28,"sine",.5,0,null,55);noise(.22,.18,.02,700,"lowpass")}catch(e){}};
  /* 증거·재미있는 물건이 튀어나올 때: 짧은 반짝 */
  SFX.pop9=function(){if(!S.sound)return;try{[880,1320,1760].forEach(function(f,i){tone(f,.12,"triangle",.06,i*.05)});noise(.035,.018,0,4000,"highpass")}catch(e){}};
  /* 결정적 대사: 배경음이 끊길 때 둔탁한 한 방 */
  SFX.cut9=function(){if(!S.sound)return;try{tone(70,.6,"sine",.55,0,null,40);noise(.35,.25,0,240,"lowpass");tone(2200,.05,"square",.05)}catch(e){}};
  var lastLn=null;setInterval(function(){try{if(!cur())return;var ln=liveLine();if(!ln){lastLn=null;return}
    var t=lineText(),who=lineWho(),token=who+"|"+t;
    if(token===lastLn)return;lastLn=token;   /* 분할된 다음 쪽에서도 원문 기준으로 효과음은 한 번만 */
    var md=String(Array.isArray(ln)?(ln[2]||ln[6]||""):(ln.m||""));
    if(ln.audio==="silence"||ln.audio==="pulse")return;
    if(ln.audio==="impact")SFX.cut9();
    else if(/^…움직였어/.test(t))SFX.pop9();   /* 살아 있음을 확인하는 순간: 놀람 타격 대신 작은 반짝 */
    else if(/^거긴 (창고|지금은 안 쓰는 방)/.test(t))SFX.low9();   /* 첫 복도 경고만 낮게. 표정과 짧은 감탄에는 충격음을 붙이지 않는다. */
}catch(e){}},60);
  /* 낮은 단음(현 피치카토 + 저음): 분위기만 바꾸는 한 음 */
  SFX.low9=function(){if(!S.sound)return;try{tone(98,.9,"sine",.08,0,null,92);tone(147,.6,"triangle",.025,.02);noise(.05,.04,0,500,"lowpass")}catch(e){}};
  /* 회의·최종 대결 정답 외침: 엔진 외침 효과음에 맞춰 음악을 끊고 추궁곡으로 */
  (function(){var o=SFX.shout;SFX.shout=function(){try{if(cur()&&document.querySelector("body>.rt")){M.obj=Date.now();M.objDL=0;M.objPh=window.__rtPh&&__rtPh()}}catch(e){}return o&&o.apply(this,arguments)}})();
  wrap("doorOpen",function(){window.__innRecordedSfx.play("open")});
  SFX.carStop=function(){M.carStopped=true;try{if(AMB.cur&&AMB.cur.key==="carriage"){stop(AMB.cur,.3);AMB.cur=null}}catch(e){}};
  SFX.bell10=function(){M.bell=true;if(!S.sound)return;try{var a=ac();if(!a)return;for(var i=0;i<10;i++){var w=i*.75;   /* 멀리서 울리는 낮은 마을 종(높은 배음을 줄여 '삐-' 경보음처럼 들리지 않게) */
    tone(196,3,"sine",.16,w);tone(392,1.6,"sine",.05,w);tone(470,1.2,"sine",.025,w);noise(.05,.05,w,900,"lowpass")}}catch(e){}};
  SFX.bell10_old=function(){if(!S.sound)return;try{var a=ac();if(!a)return;for(var i=0;i<10;i++){var w=i*.75;tone(330,2.2,"sine",.12,w);tone(330*2.76,1.1,"sine",.03,w);tone(330*5.4,.5,"sine",.01,w)}}catch(e){}};   /* P10 밤 10시 종: 멀리서 10회 */

  /* ---- 콜드 오픈 연출(2026-10-10): 어둠·정적·행동 소리. 대사·그림·단서는 그대로, 카메라와 소리만 ---- */
  var COLDD=1;
  function creak(){noise(.5,.09,0,320,"bandpass",null,190);tone(150,.45,"triangle",.05,0,null,118)}
  function step(){[0,.42].forEach(function(w){noise(.07,.16,w,520,"lowpass");tone(95,.08,"sine",.14,w,null,62)})}
  function breath(){noise(1.1,.05,0,900,"bandpass",null,520)}
  function heart(){[0,.32,1.2,1.52].forEach(function(w,i){tone(58,.16,"sine",i%2?.22:.3,w,null,44)})}
  var COLDFX={creak:creak,step:step,breath:breath,heart:heart};
  /* 2026-10-10 "프롤로그는 아주 긴장되게, 심장 박동이 점점 커지며 빨라지게": 콜드 오픈 내내 심장 소리가 이어지고 비트가 지날수록 빠르고 크게(약 55→130bpm) */
  var HB={k:0,n:1,next:0,on:false};
  function hbTick(){try{if(!document.getElementById("inncold")){HB.on=false;return}if(!AC||AC.state!=="running"||!S.sound){setTimeout(hbTick,200);return}
    var p=Math.min(1,HB.k/Math.max(1,HB.n-1)),bpm=55+75*p*p,v=.14+.4*p,gap=60/bpm;
    tone(58,.16,"sine",v,0,null,40);tone(52,.14,"sine",v*.7,gap*.32,null,38);noise(.06,v*.25,0,160,"lowpass");
    setTimeout(hbTick,gap*1000)}catch(e){setTimeout(hbTick,400)}}
  window.__innColdFx=function(b){try{if(b.duck!=null)COLDD=b.duck;var L=(window.EP1INN&&window.EP1INN.COLD)||[];var i=L.indexOf(b);if(i>=0){HB.k=i;HB.n=L.length}
    if(!HB.on){HB.on=true;setTimeout(hbTick,300)}
    if(b.fxs&&b.fxs!=="heart"&&S.sound&&COLDFX[b.fxs])COLDFX[b.fxs]()}catch(e){}};
  /* 비트별 연출: 침대 컷은 '침대 다리'가 아니라 이불 덮인 침대 쪽으로 다가가며 점점 어둡고 조용해진다 */
  try{var STAGE={"01":{fxs:"step",duck:1},"02":{push:3,duck:.9},
   "03":{z:1,fx:.72,fy:.6,push:5,fxs:"creak",duck:.6},"04":{z:1.45,fx:.74,fy:.6,push:6,fxs:"step",duck:.5},"05":{z:1.8,fx:.74,fy:.62,push:4,dim:.8,duck:.4},
   "06":{z:1.8,fx:.74,fy:.62,push:3,dim:.75,duck:.35},"07":{z:2.1,fx:.74,fy:.62,push:3,dim:.7,fxs:"breath",duck:.25},"08":{z:2.1,fx:.74,fy:.62,dim:.65,fxs:"heart",duck:.15},
   "09":{z:2.3,fx:.74,fy:.62,push:2,dim:.6,duck:.08},"10":{fxs:"heart",duck:.3},"11":{duck:.3},"12":{duck:.35},"13":{duck:.35},"14":{duck:.4},"15":{fxs:"step",duck:.45},
   "16":{fxs:"heart",duck:.5},"17":{duck:.5},"18":{duck:.3},"19":{duck:0}};
   var EPC=window.EP1INN||(typeof EP!=="undefined"?EP:{});(EPC.COLD||[]).forEach(function(b){var o=STAGE[b.id];if(o)for(var k in o)b[k]=o[k]});
   /* 2026-10-10 "오프닝이 너무 길다": 같은 망설임이 되풀이되는 줄만 뺀다(대사를 새로 쓰지 않음). 19비트 → 13비트 */
   var DROPC={"06":1,"08":1,"09":1,"11":1,"12":1,"14":1};if(EPC.COLD)EPC.COLD=EPC.COLD.filter(function(b){return !DROPC[b.id]});
   (EPC.COLD||[]).forEach(function(b){if(b.id==="07"){b.duck=.15;b.fxs="heart"}})}catch(e){window.__innColdErr=e.message}

  /* ---- 환경음 ---- */
  window.__innOwnAmb=function(){return !!document.getElementById("innmain")||!!document.getElementById("inncold")||cur()};
  var BUF=null;
  function buf(a){if(BUF&&BUF.ctx===a)return BUF.b;var n=a.sampleRate*4,b=a.createBuffer(1,n,a.sampleRate),d=b.getChannelData(0),last=0;
   for(var i=0;i<n;i++){var w=Math.random()*2-1;last=(last+.02*w)/1.02;d[i]=w*.5+last*3.5}BUF={ctx:a,b:b};return b}
  function loopSrc(a,out,type,freq,q,vol){var s=a.createBufferSource();s.buffer=buf(a);s.loop=true;s.loopStart=Math.random();var f=a.createBiquadFilter();f.type=type;f.frequency.value=freq;if(q)f.Q.value=q;var g=a.createGain();g.gain.value=vol;s.connect(f);f.connect(g);g.connect(out);s.start(a.currentTime,Math.random()*3);return {s:s,f:f,g:g}}
  function burst(a,out,t,dur,vol,type,freq,q){var s=a.createBufferSource();s.buffer=buf(a);var f=a.createBiquadFilter();f.type=type;f.frequency.value=freq;if(q)f.Q.value=q;var g=a.createGain();g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.006);g.gain.exponentialRampToValueAtTime(.0001,t+dur);s.connect(f);f.connect(g);g.connect(out);s.start(t,Math.random()*3);s.stop(t+dur+.02)}
  function thud(a,out,t,vol){var o=a.createOscillator(),g=a.createGain();o.frequency.setValueAtTime(130,t);o.frequency.exponentialRampToValueAtTime(70,t+.08);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+.1);o.connect(g);g.connect(out);o.start(t);o.stop(t+.12);burst(a,out,t,.06,vol*.6,"lowpass",380)}
  function build(a,key){var out=a.createGain();out.gain.setValueAtTime(.0001,a.currentTime);out.connect(SFXG);
   var I={key:key,out:out,src:[],lp:null,next:{},a:a};
   if(key==="carriage"){I.peak=.65;window.__innRecordedSfx.attach(I,"horse")}   /* 녹음 루프 하나만: 합성 발굽·방울·덜컹은 겹치지 않는다. */
   else if(key==="wind"){var wd=loopSrc(a,out,"bandpass",480,.8,.35);I.src.push(wd.s);
    var l2=a.createOscillator(),g2=a.createGain();l2.frequency.value=.11;g2.gain.value=220;l2.connect(g2);g2.connect(wd.f.frequency);l2.start();I.src.push(l2);I.peak=.5}
   out.gain.exponentialRampToValueAtTime(I.peak,a.currentTime+.4);return I}
  function sched(I){}   /* Recorded carriage source loops natively; no synthetic rescheduling. */
  function stop(I,dur){if(!I||I.ending)return;var a=I.a,t=a.currentTime;dur=dur||.8;I.ending=t+dur*.8;AMB.old.push(I);
   try{I.out.gain.cancelScheduledValues(t);I.out.gain.setValueAtTime(Math.max(.0001,I.out.gain.value),t);I.out.gain.exponentialRampToValueAtTime(.0001,t+dur);if(I.lp){I.lp.frequency.setValueAtTime(I.lp.frequency.value,t);I.lp.frequency.exponentialRampToValueAtTime(180,t+dur)}}catch(e){}
   setTimeout(function(){I.dead=true;var k=AMB.old.indexOf(I);if(k>=0)AMB.old.splice(k,1);I.src.forEach(function(s){try{s.stop()}catch(e){}});try{I.out.disconnect()}catch(e){}},dur*1000+300)}
  var AMB={cur:null,dep:null,old:[]};
  function ambWant(){if(!cur()||!S.sound||window.__innAudioHold||document.getElementById("inncold"))return null;var b=beats();if(M.failure)return "wind";
   if(!b.inn_pro){var sd=sidOf(b.inn_pi|0);if(sd==="P1"&&b.inn_bg==="carriage"&&!M.carStopped)return "carriage";return null}   /* 2026-10-10 "광장 바람 소리 거슬린다": 뺌 */
   if(b.inn_final&&!b.inn_end){var ei=b.inn_ei|0;if(ei===0||ei===1)return "wind"}
   return null}
  /* E2 마지막 마차: 출발해서 멀어지며 사라진다(약 7초) */
  SFX.carDepart=function(){if(!S.sound||!AC)return;try{if(AMB.dep&&!AMB.dep.dead)return;var I=build(AC,"carriage");AMB.dep=I;sched(I);var iv=setInterval(function(){if(I.dead){clearInterval(iv);return}sched(I)},120);setTimeout(function(){stop(I,6.5)},500)}catch(e){}};
  setInterval(function(){try{
   if(!AC||AC.state!=="running"){return}
   var k=ambWant();
   if((AMB.cur&&AMB.cur.key)!==k){var was=AMB.cur;if(was)stop(was,was.key==="carriage"?.3:.8);AMB.cur=k?build(AC,k):null}   /* 마차 -> 광장: 멀어지며 5초에 걸쳐 사라짐 */
   if(AMB.cur)sched(AMB.cur);AMB.old.forEach(sched)}catch(e){}},120);
  window.__innAmb=function(){return {cur:AMB.cur&&AMB.cur.key,old:AMB.old.length,dep:!!(AMB.dep&&!AMB.dep.dead),music:A.cur,want:A.want,duck:A.duck}};
  /* 2026-10-10 사용자 "메인 화면 진입 시 클릭 전에 노래가 안 나옴": 브라우저 자동재생 정책(iOS Safari는 첫 터치 전 소리 금지)은 우회하지 않는다.
     메인 화면이 뜨면 한 번 소리 시작을 시도하고(허용된 환경이면 바로 재생), 막혀 있으면 '소리 켜기' 안내를 보여 첫 터치로 시작하게 한다.
     실제 시작은 엔진의 첫 터치 잠금 해제(touchend·pointerup·click·keydown)가 맡는다. 소리를 끈 설정이면 안내하지 않는다 */
  (function(){var tried=false,HB9=null;
   function running(){try{return !!AC&&AC.state==="running"}catch(e){return false}}
   function hint(on,m){if(on&&!HB9&&m){HB9=document.createElement("button");HB9.type="button";HB9.id="sndhint9";HB9.textContent="소리 켜기";HB9.setAttribute("aria-label","소리 켜기: 화면을 누르면 음악이 나와요");
     HB9.style.cssText="position:absolute;right:calc(10px + env(safe-area-inset-right,0px));top:calc(10px + env(safe-area-inset-top,0px));z-index:5;min-height:44px;padding:0 16px;border:2px solid #C9A96A;border-radius:10px;background:rgba(20,16,30,.88);color:#FFF6E0;font:13px/1 Galmuri11,monospace;cursor:pointer";
     m.appendChild(HB9)}else if(!on&&HB9){HB9.remove();HB9=null}}
   setInterval(function(){try{var m=document.getElementById("innmain");if(!m||!S.sound){hint(false);return}
     if(!tried){tried=true;   /* 시험용 소리 장치를 하나 만들어 브라우저가 지금 재생을 허락하는지 본다(허락 안 하면 곧바로 닫고 안내만) */
      try{if(!AC){var C9=window.AudioContext||window.webkitAudioContext,pz=C9?new C9():null;if(pz)setTimeout(function(){try{if(pz.state==="running"){window.__innAutoOK=true;try{ac()}catch(x){}}pz.close()}catch(x){}},250)}}catch(e){}}
     hint(!running(),m)}catch(e){}},400)})();
 })();
