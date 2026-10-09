 /* ==== 1장 오디오 연출 (오디오 큐시트 2026-10-09 기준, 실제 음원 파일 없이 합성음) ====
    - 음악: 도입(inn_cold) -> 여행·여관(inn_travel, P1~P10) -> 조사(inn_inv, P11 신고 확인~회의·최종) -> 여운(inn_after, 후일담)
      같은 곡 안에서는 장면·화자·장소가 바뀌어도 다시 시작하지 않는다(엔진: 같은 키면 그대로 둠). 낮춤은 덕킹으로만.
    - 환경음: 마차(구름음+덜컹+먼 말발굽), 바깥바람. 장소에 머무는 동안 한 인스턴스만.
    - 타이핑음: 부드럽고 낮게, 최소 간격 75ms. 속마음·지문은 발화보다 낮게. 문장 완성·넘김 때 몰아서 나지 않음(예약 재생 없음). */
 (function(){
  if(!window.__AUD||!__AUD.SONGS)return;
  var A=__AUD;
  function cur(){try{return S.screen==="case"&&!!G&&!!CASES[G.ci]&&CASES[G.ci].id==="inn"}catch(e){return false}}
  function sidOf(pi){try{return (EP.PRO[pi]&&EP.PRO[pi].sid)||("P"+(pi+1))}catch(e){return "P"+(pi+1)}}
  function beats(){try{return (G&&G.beats)||{}}catch(e){return {}}}
  function lineText(){try{var l=DL&&DL.lines&&DL.lines[DL.i];return l?String(l[1]||""):""}catch(e){return ""}}
  function lineKind(){try{var l=DL&&DL.lines&&DL.lines[DL.i];if(!l)return "say";if(l[0]==="narr")return /^\(/.test(String(l[1]))?"inner":"narr";return "say"}catch(e){return "say"}}

  /* ---- 곡: 타악기 없음(박자감이 '똑딱'으로 들리지 않게) ---- */
  A.SONGS.inn_cold={bpm:60,vol:.85,prog:["Dm","Dm","Bb","A","Dm","Dm","Gm","A"],
   mel:[{n:"D5 _ _ _ . . . . | . . . . C5 _ A4 _ | Bb4 _ _ _ . . . . | A4 _ _ _ _ _ . . | D5 _ _ _ . . . . | . . . . E5 _ F5 _ | D5 _ _ _ Bb4 _ . . | C#5 _ _ _ _ _ . .",i:"glass",v:.07}],
   bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.42,o:33},pad:{i:"string",v:.04,o:50},fx:"drone",echo:.4};
  A.SONGS.inn_travel={bpm:92,spb:12,vol:1.05,prog:["F","C/E","Dm","Bb","F","Gm","Bb C","F"],   /* 따뜻한 6/8: 칼림바 선율 + 일렉 피아노 분산화음 + 현 패드, 타악기 없음 */
   mel:[{n:"C5 _ A4 _ C5 F5 | E5 _ _ _ C5 _ | D5 _ F5 _ A5 G5 | F5 _ _ _ D5 _ | C5 _ A4 _ C5 F5 | G5 _ F5 _ E5 D5 | D5 _ C5 _ Bb4 E5 | F5 _ _ _ . .",i:"kal",v:.24}],
   arp:{n:"1 5 8 10 8 5",r:2,i:"ep",v:.05,o:48},bass:{n:"1 _ _ 5 _ _",i:"sub",v:.4,o:36},pad:{i:"string",v:.04,o:57},echo:.28};
  A.SONGS.inn_inv={bpm:76,vol:.85,prog:["Em","CM7","Am7","B7","Em","G","Am C","B7"],
   mel:[{n:"B5 _ _ _ G5 _ E5 _ | E5 _ _ _ D5 _ B4 _ | C5 _ E5 _ A5 _ G5 _ | F#5 _ _ _ D#5 _ _ _ | E5 _ G5 _ B5 _ E6 _ | D6 _ _ B5 _ _ G5 _ | A5 _ C6 _ E6 _ D6 _ | D#6 _ _ _ _ _ . .",i:"kal",v:.2}],
   arp:{n:"1 5 8 10 8 5 . .",r:2,i:"pluck",v:.08,o:52},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.42,o:36},pad:{i:"glass",v:.045,o:60},echo:.3};
  A.SONGS.inn_after={bpm:72,vol:.85,prog:["F","C/E","Dm","Bb","F/A","Gm","Bb C","F"],
   mel:[{n:"A5 _ _ _ G5 _ F5 _ | E5 _ _ _ G5 _ C6 _ | D6 _ _ _ C6 _ A5 _ | Bb5 _ _ _ _ _ A5 G5 | A5 _ _ _ C6 _ F6 _ | D6 _ _ _ Bb5 _ G5 _ | F5 _ G5 _ Bb5 _ C6 _ | A5 _ _ _ _ _ . .",i:"flute",v:.18}],
   arp:{n:"1 5 8 10 12 10 8 5",r:2,i:"ep",v:.06,o:48},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.38,o:33},pad:{i:"string",v:.045,o:57},echo:.3};

  /* ---- 음악 선택 ---- */
  var M={inv:false,p10:0,fin:0};
  window.__innWant=function(){
   if(!cur())return undefined;
   A.hush=null;A.exp=null;A.pursuit=null;          /* 옛 체계의 일시 정지·승리곡·추격곡이 끼어들어 곡을 다시 시작하지 않게 */
   var b=beats();
   if(!b.inn_pro){var pi=b.inn_pi|0,sid=sidOf(pi);
    if(['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10'].indexOf(sid)>=0)return "inn_travel";   /* P1~P10 */
    if(sid==="P11"){if(/^제 주머니가 없어졌|^계약금이 든 주머니/.test(lineText()))M.inv=true;   /* 2026-10-10: 범죄를 처음 알아채는 줄(세련의 외침)에서 바로 긴장곡 */return M.inv?"inn_inv":null}   /* P11: 신고 확인 뒤 */
    return "inn_inv"}
   if(!b.inn_final)return "inn_inv";                /* 조사·회의·최종: 같은 곡, 같은 재생 위치 */
   if(M.fin&&Date.now()-M.fin>7000)return null;     /* 마지막 줄 뒤 천천히 끝난 다음 */
   return "inn_after"};
  window.__innDuck=function(){
   if(document.getElementById("inncold"))return COLDD;   /* 콜드 오픈: 비트마다 정한 낮춤(정적으로 갈수록 작게) */
   if(!cur())return 1;
   var b=beats(),now=Date.now(),f=(typeof DL!=="undefined"&&DL)?.9:1,t=lineText();   /* 2026-10-10: 대화 중 배경음 .62×.9≈.56(-5dB) — 타이핑·효과음이 묻히지 않게 */
   if(!b.inn_pro){var pi=b.inn_pi|0;
    var sd=sidOf(pi);if(sd!=="P10")M.p10=0;
    if(sd==="P5")f=.8;                             /* P5 복도: 같은 곡 낮게 */
    if(sd==="P10"){if(!M.p10)M.p10=now;f=Math.max(0,1-(now-M.p10)/14000)}   /* P10: 여행곡 천천히 종료 */
    if(sd==="P12")f=.75;if(sd==="P13")f=.5;     /* P12 낮게, P13 더 낮게 */
    return f}
   if(!b.inn_final){try{var l=CASES[G.ci].locations[G.loc];if(l&&l.id==="kitchen"&&G.tab==="scene")f=.75}catch(e){}return f}
   var ei=b.inn_ei|0;
   if(!b.inn_end&&ei===3){f=.6;if(/^…아빠\. 이 글씨|^\(지난겨울, 열세 번째 침대|^엄마 글씨야/.test(t))f=.12}   /* E4: 글씨를 알아보는 순간 정적 */
   if((!b.inn_end&&ei===4&&/^반은 잘 지켜/.test(t))||b.inn_end){if(!M.fin)M.fin=now}
   if(M.fin)f*=Math.max(0,1-(now-M.fin)/6500);
   return f};

  /* ---- 타이핑음 ---- */
  var lastT=0;
  window.__innType=function(kind){try{
   if(!S.sound||!AC||AC.state!=="running")return;var now=AC.currentTime;if(now-lastT<.075)return;lastT=now;
   var v=kind==="inner"?.6:kind==="narr"?.7:1;   /* 2026-10-10: 타이핑 약 +10dB, 소리 높이를 조금씩 달리해 반복 피로를 줄임 */
   noise(.016,.11*v,0,2100+Math.random()*500,"bandpass");tone(420+Math.random()*90,.028,"triangle",.07*v)}catch(e){}};
  var _blip=SFX.blip;
  SFX.blip=function(){if(!cur())return _blip.apply(this,arguments);window.__innType(lineKind())};

  /* ---- 1장 효과음 보정 ---- */
  function wrap(k,fn){var o=SFX[k];SFX[k]=function(){if(!cur())return o&&o.apply(this,arguments);try{fn.apply(this,arguments)}catch(e){}}}
  wrap("door",function(){if(!S.sound)return;noise(.06,.3,0,900,"lowpass");tone(140,.09,"sine",.28,0,null,90);noise(.015,.1,.03,3000,"highpass")});   /* 문 닫힘: 달칵(옛 '딩동' 아님) */
  wrap("slam",function(){if(!S.sound)return;tone(100,.26,"sine",.55,0,null,45);noise(.18,.45,0,520)});   /* P11 기상: 쾅 1회, 과하지 않게 */
  wrap("letter",function(){});                     /* 장면 제목 글자마다 '틱' 없음 */
  wrap("impact",function(){if(!S.sound)return;tone(98,.5,"sine",.3,0,null,62);noise(.25,.12,0,300)});
  wrap("tick2",function(){});                      /* 빈 곳 터치 '틱' 없음 */
  wrap("roll",function(){});                       /* 옛 드럼롤(마차 대용) 없음 */
  SFX.bell10=function(){if(!S.sound)return;try{var a=ac();if(!a)return;for(var i=0;i<10;i++){var w=i*.75;tone(330,2.2,"sine",.12,w);tone(330*2.76,1.1,"sine",.03,w);tone(330*5.4,.5,"sine",.01,w)}}catch(e){}};   /* P10 밤 10시 종: 멀리서 10회 */

  /* ---- 콜드 오픈 연출(2026-10-10): 어둠·정적·행동 소리. 대사·그림·단서는 그대로, 카메라와 소리만 ---- */
  var COLDD=1;
  function creak(){noise(.5,.09,0,320,"bandpass",null,190);tone(150,.45,"triangle",.05,0,null,118)}
  function step(){[0,.42].forEach(function(w){noise(.07,.16,w,520,"lowpass");tone(95,.08,"sine",.14,w,null,62)})}
  function breath(){noise(1.1,.05,0,900,"bandpass",null,520)}
  function heart(){[0,.32,1.2,1.52].forEach(function(w,i){tone(58,.16,"sine",i%2?.22:.3,w,null,44)})}
  var COLDFX={creak:creak,step:step,breath:breath,heart:heart};
  window.__innColdFx=function(b){try{if(b.duck!=null)COLDD=b.duck;if(b.fxs&&S.sound&&COLDFX[b.fxs])COLDFX[b.fxs]()}catch(e){}};
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
   if(key==="carriage"){
    var lp=a.createBiquadFilter();lp.type="lowpass";lp.frequency.value=2400;lp.connect(out);I.lp=lp;
    var r=loopSrc(a,lp,"lowpass",150,0,.32);I.src.push(r.s);                      /* 바퀴 구름음(낮게 지속) */
    var w=loopSrc(a,lp,"bandpass",430,1.6,.035);I.src.push(w.s);                  /* 바퀴 마찰 */
    var lfo=a.createOscillator(),lg=a.createGain();lfo.frequency.value=1.7;lg.gain.value=.015;lfo.connect(lg);lg.connect(w.g.gain);lfo.start();I.src.push(lfo);
    I.bus=lp;I.peak=.45}   /* 2026-10-10 "마차 소리가 거슬린다": 전체 -6dB, 마찰음·덜컹 더 낮게 */
   else if(key==="wind"){var wd=loopSrc(a,out,"bandpass",480,.8,.35);I.src.push(wd.s);
    var l2=a.createOscillator(),g2=a.createGain();l2.frequency.value=.11;g2.gain.value=220;l2.connect(g2);g2.connect(wd.f.frequency);l2.start();I.src.push(l2);I.peak=.5}
   out.gain.exponentialRampToValueAtTime(I.peak,a.currentTime+.4);return I}
  function sched(I){if(I.key!=="carriage"||I.dead)return;if(I.ending&&I.a.currentTime>I.ending)return;var a=I.a,now=a.currentTime,n=I.next;
   if(n.r==null)n.r=now+1+Math.random()*2;if(n.h==null)n.h=now+.3;
   while(n.r<now+.3){var k=3+(Math.random()*3|0),t=n.r;for(var j=0;j<k;j++){burst(a,I.bus,t,.03,.03+Math.random()*.02,"bandpass",900+Math.random()*500,2.5);t+=.03+Math.random()*.05}n.r+=4+Math.random()*4}   /* 차체 덜컹: 간헐적 */
   while(n.h<now+.3){thud(a,I.bus,n.h,.05);thud(a,I.bus,n.h+.2+Math.random()*.03,.04);n.h+=.86+Math.random()*.1}}   /* 먼 말발굽: 바퀴보다 낮고 둔하게 */
  function stop(I,dur){if(!I||I.ending)return;var a=I.a,t=a.currentTime;dur=dur||.8;I.ending=t+dur*.8;AMB.old.push(I);
   try{I.out.gain.cancelScheduledValues(t);I.out.gain.setValueAtTime(Math.max(.0001,I.out.gain.value),t);I.out.gain.exponentialRampToValueAtTime(.0001,t+dur);if(I.lp){I.lp.frequency.setValueAtTime(I.lp.frequency.value,t);I.lp.frequency.exponentialRampToValueAtTime(180,t+dur)}}catch(e){}
   setTimeout(function(){I.dead=true;var k=AMB.old.indexOf(I);if(k>=0)AMB.old.splice(k,1);I.src.forEach(function(s){try{s.stop()}catch(e){}});try{I.out.disconnect()}catch(e){}},dur*1000+300)}
  var AMB={cur:null,dep:null,old:[]};
  function ambWant(){if(!cur()||!S.sound||window.__innAudioHold||document.getElementById("inncold"))return null;var b=beats();
   if(!b.inn_pro){var sd=sidOf(b.inn_pi|0);if(sd==="P1"&&b.inn_bg==="carriage")return "carriage";if(sd==="P2")return "wind";return null}
   if(b.inn_final&&!b.inn_end){var ei=b.inn_ei|0;if(ei===0||ei===1)return "wind"}
   return null}
  /* E2 마지막 마차: 출발해서 멀어지며 사라진다(약 7초) */
  SFX.carDepart=function(){if(!S.sound||!AC)return;try{if(AMB.dep&&!AMB.dep.dead)return;var I=build(AC,"carriage");AMB.dep=I;sched(I);var iv=setInterval(function(){if(I.dead){clearInterval(iv);return}sched(I)},120);setTimeout(function(){stop(I,6.5)},500)}catch(e){}};
  setInterval(function(){try{
   if(!AC||AC.state!=="running"){return}
   var k=ambWant();
   if((AMB.cur&&AMB.cur.key)!==k){var was=AMB.cur;if(was)stop(was,(was.key==="carriage"&&k==="wind")?5:.8);AMB.cur=k?build(AC,k):null}   /* 마차 -> 광장: 멀어지며 5초에 걸쳐 사라짐 */
   if(AMB.cur)sched(AMB.cur);AMB.old.forEach(sched)}catch(e){}},120);
  window.__innAmb=function(){return {cur:AMB.cur&&AMB.cur.key,old:AMB.old.length,dep:!!(AMB.dep&&!AMB.dep.dead),music:A.cur,want:A.want,duck:A.duck}};
 })();
