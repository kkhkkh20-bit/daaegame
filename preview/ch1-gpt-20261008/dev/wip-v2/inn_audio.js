 /* ==== 1장 오디오 연출 (오디오 큐시트 2026-10-09 기준, 실제 음원 파일 없이 합성음) ====
    - 음악: 도입(inn_cold) -> 여행·여관(inn_travel, P1~P10) -> 조사(inn_inv, P11 신고 확인~회의·최종) -> 여운(inn_after, 후일담)
      같은 곡 안에서는 장면·화자·장소가 바뀌어도 다시 시작하지 않는다(엔진: 같은 키면 그대로 둠). 낮춤은 덕킹으로만.
    - 환경음: 마차(구름음+덜컹+먼 말발굽), 바깥바람. 장소에 머무는 동안 한 인스턴스만.
    - 타이핑음: 부드럽고 낮게, 최소 간격 75ms. 속마음·지문은 발화보다 낮게. 문장 완성·넘김 때 몰아서 나지 않음(예약 재생 없음). */
 (function(){
  if(!window.__AUD||!__AUD.SONGS)return;
  var A=__AUD;
  function cur(){try{return S.screen==="case"&&!!G&&!!CASES[G.ci]&&CASES[G.ci].id==="inn"}catch(e){return false}}
  function sidOf(pi){try{var E=window.EP1INN||EP;return (E.PRO[pi]&&E.PRO[pi].sid)||("P"+(pi+1))}catch(e){return "P"+(pi+1)}}   /* 2026-10-10: EP는 이 모듈 범위에 없어 장면 번호가 밀려(P6·P8 제외 뒤) 신고 장면에서도 여행곡이 나오던 문제 */
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
  /* 2026-10-10 "수사 중인데도 몽환적·평화롭다": 조사·회의·최종 대결을 다른 곡으로. 하이햇('똑딱')은 쓰지 않고 낮은 킥만 */
  /* 2026-10-10 "배경음이 계속 평화롭다": 조사곡을 8분음 베이스가 몰아붙이는 단조 추적곡으로. 이전 곡은 inn_inv_soft로 보존 */
  A.SONGS.inn_inv={bpm:108,vol:1.6,prog:["Am","Am","F","E","Dm","Am","F","E"],
   mel:[{n:"A4 . C5 . E5 . D#5 E5 | . . . . A4 . B4 . | C5 . A4 . F4 . A4 . | G#4 _ _ _ B4 _ E5 _ | D5 . F5 . A5 . G#5 A5 | . . E5 . C5 . A4 . | C5 . F5 . A5 . C6 . | B5 _ G#5 _ E5 _ . .",i:"stac",v:.16},
        {n:"A3 _ _ _ _ _ _ _ | . . . . . . . . | F3 _ _ _ _ _ _ _ | E3 _ _ _ _ _ _ _ | D3 _ _ _ _ _ _ _ | . . . . . . . . | F3 _ _ _ _ _ _ _ | E3 _ _ _ _ _ _ _",i:"brass",v:.07}],
   arp:{n:"1 5 8 5 1 5 8 5",r:1,i:"pizz",v:.06,o:48},bass:{n:"1 1 1 1 1 1 1 1",i:"bsyn",v:.32,o:30},pad:{i:"string",v:.05,o:52},
   dr:["k.....k.k......."],echo:.12};
  A.SONGS.inn_inv_soft={bpm:92,vol:2.1,prog:["Am","Am","F","E","Am","Dm","F E","Am"],   /* 조사: 단조, 피치카토 베이스 반복, 짧은 스타카토 */
   mel:[{n:"E5 _ _ _ . . C5 _ | B4 _ _ _ . . . . | A4 _ _ _ C5 _ E5 _ | G#4 _ _ _ . . . . | E5 _ _ _ F5 _ E5 _ | D5 _ _ _ . . F5 _ | E5 _ D5 _ C5 _ B4 _ | A4 _ _ _ . . . .",i:"vibe",v:.2}],
   arp:{n:"1 . 5 . 8 . 5 .",r:1,i:"stac",v:.05,o:48},bass:{n:"1 . 1 . 5 . 1 .",i:"pizz",v:.6,o:33},pad:{i:"pad",v:.04,o:55},
   dr:["k.......k......."],echo:.14};
  A.SONGS.inn_meet={bpm:100,vol:1.4,prog:["Dm","Bb","Gm","A","Dm","Bb","Gm A","Dm"],   /* 회의: 맥박처럼 이어지는 베이스, 금관 짧게 */
   mel:[{n:"D5 _ _ _ . . F5 _ | F5 _ D5 _ . . . . | G5 _ _ _ Bb5 _ A5 _ | A5 _ _ _ C#5 _ . . | D5 _ _ _ . . A5 _ | Bb5 _ A5 _ G5 _ F5 _ | G5 _ _ _ E5 _ C#5 _ | D5 _ _ _ . . . .",i:"brass",v:.14}],
   bass:{n:"1 1 1 1 1 1 1 1",i:"bsyn",v:.3,o:30},pad:{i:"string",v:.05,o:54},dr:["k.......k.......","..........d....."],echo:.18};
  A.SONGS.inn_climax={bpm:112,vol:.6,prog:["Cm","Cm","Ab","G","Cm","Fm","Ab Bb","G"],   /* 최종 대결: 빠르고 날카롭게 */
   mel:[{n:"G5 _ _ _ Ab5 _ G5 _ | Eb5 _ _ _ _ _ D5 _ | C5 _ _ _ Eb5 _ D5 C5 | B4 _ _ _ D5 _ _ _ | G5 _ _ _ C6 _ Bb5 _ | Ab5 _ _ _ G5 _ F5 _ | Eb5 _ F5 _ G5 _ Ab5 _ | B5 _ _ _ _ _ . .",i:"brass",v:.16}],
   arp:{n:"1 5 8 5",r:1,i:"stac",v:.05,o:48},bass:{n:"1 . 1 . 1 . 5 .",i:"bsq",v:.45,o:36},dr:["k.....k...k.....","........s......."],echo:.12};
  /* 2026-10-10 사용자: "캐릭터마다 배경음, 사건이 벌어질 땐 심각한 배경음, 배경음이 생명" → 인물 대화 테마 7곡 + 사건곡. 하이햇 없음 */
  A.SONGS.inn_serious={bpm:76,vol:1.35,prog:["Bm","Bm","G","F#","Bm","Em","G F#","Bm"],   /* 사건: 낮은 현·심장 박동 같은 킥·짧은 금관 */
   mel:[{n:"F#5 _ _ _ _ _ . . | . . . . G5 _ F#5 _ | E5 _ _ _ _ _ . . | A#4 _ _ _ _ _ . . | F#5 _ _ _ _ _ B5 _ | A5 _ G5 _ F#5 _ E5 _ | D5 _ _ _ C#5 _ _ _ | B4 _ _ _ _ _ . .",i:"choir",v:.16},{n:"B3 _ _ _ _ _ _ _ | . . . . . . . . | G3 _ _ _ _ _ _ _ | F#3 _ _ _ _ _ _ _ | B3 _ _ _ _ _ _ _ | . . . . . . . . | G3 _ _ _ F#3 _ _ _ | B3 _ _ _ _ _ _ _",i:"brass",v:.1}],
   bass:{n:"1 _ _ _ 1 _ _ _",i:"bsyn",v:.5,o:30},pad:{i:"string",v:.07,o:50},dr:["k..k............"],echo:.2};
  A.SONGS.inn_t_innma={bpm:84,spb:12,vol:.78,prog:["F","Dm","Bb","C","F","Am","Bb C","F"],   /* 할머니: 따뜻한 왈츠, 클라리넷. 끝마디는 단단하게 */
   mel:[{n:"A4 _ C5 _ F5 _ | E5 _ _ _ D5 _ | D5 _ F5 _ Bb5 _ | A5 _ _ _ G5 _ | A4 _ C5 _ F5 _ | E5 _ D5 _ C5 _ | D5 _ C5 _ Bb4 _ | A4 _ _ _ . .",i:"clar",v:.22}],
   arp:{n:"1 . 5 . 8 .",r:2,i:"pizz",v:.08,o:48},bass:{n:"1 _ _ 5 _ _",i:"sub",v:.45,o:36},pad:{i:"warm",v:.05,o:55},echo:.2};
  A.SONGS.inn_t_seryeon={bpm:98,vol:1.84,prog:["Gm","Gm","Eb","D","Gm","Cm","Eb D","Gm"],   /* 세련: 미끄러지는 반음, 리드 악기, 걷는 베이스 */
   mel:[{n:"D5 _ . Eb5 D5 _ . . | C#5 D5 _ . Bb4 _ . . | G5 _ . F#5 G5 _ Eb5 _ | D5 _ _ _ . . A4 _ | D5 _ . Eb5 D5 _ . . | C5 _ Eb5 _ G5 _ . . | Bb5 _ A5 _ G5 _ F#5 _ | G5 _ _ _ . . . .",i:"reed",v:.18}],
   bass:{n:"1 . 3 . 5 . 6 .",i:"pizz",v:.55,o:31},pad:{i:"ep",v:.05,o:55},dr:["k.......k.......","....s.......s..."],echo:.16};
  A.SONGS.inn_t_nabi={bpm:116,vol:3.2,prog:["C","Am","F","G","C","Em","F G","C"],   /* 나비: 밝고 바지런한 마림바 */
   mel:[{n:"E5 G5 C6 _ G5 _ E5 _ | A5 _ G5 E5 C5 _ . . | F5 A5 C6 _ A5 _ F5 _ | G5 _ _ _ B4 _ D5 _ | E5 G5 C6 _ G5 _ E5 _ | B4 _ E5 _ G5 _ B5 _ | A5 G5 F5 _ D5 E5 F5 _ | E5 _ C5 _ C6 _ . .",i:"marimba",v:.22}],
   arp:{n:"1 5 8 5",r:1,i:"stac",v:.05,o:48},bass:{n:"1 . 5 . 1 . 5 .",i:"pizz",v:.5,o:36},pad:{i:"string",v:.04,o:55},echo:.12};
  A.SONGS.inn_t_bami={bpm:68,vol:1.0,prog:["Em","C","Am","B7","Em","C","Am B7","Em"],   /* 밤이: 졸린 밤, 유리·종소리 */
   mel:[{n:"B5 _ _ _ . . G5 _ | E5 _ _ _ _ _ . . | C6 _ _ _ B5 _ A5 _ | D#5 _ _ _ _ _ . . | B5 _ _ _ . . E6 _ | D6 _ _ _ B5 _ . . | C6 _ B5 _ A5 _ F#5 _ | E5 _ _ _ _ _ . .",i:"bell",v:.14}],
   arp:{n:"1 5 8 10 8 5 . .",r:2,i:"glass",v:.05,o:60},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.45,o:33},pad:{i:"pad",v:.06,o:52},echo:.38};
  A.SONGS.inn_t_buri={bpm:104,vol:.85,prog:["D","D","C","G","D","Bm","C G","D"],   /* 부리: 톱니바퀴처럼 맞물리는 반복 */
   mel:[{n:"A5 . A5 . F#5 . D5 . | A5 . B5 . A5 _ . . | G5 . G5 . E5 . C5 . | D5 . E5 . D5 _ . . | A5 . A5 . F#5 . D5 . | B5 . A5 . F#5 _ . . | G5 . E5 . D5 . B4 . | D5 _ _ _ . . . .",i:"chip",v:.1}],
   arp:{n:"1 8 5 8 1 8 5 8",r:1,i:"pizz",v:.08,o:48},bass:{n:"1 . 1 . 5 . 1 .",i:"bsq",v:.35,o:36},dr:["k...k...k...k..."],echo:.1};
  A.SONGS.inn_t_neoul={bpm:88,vol:.89,prog:["Cm","Cm","Ab","G","Cm","Fm","Ab G","Cm"],   /* 너울: 규약과 기록, 오르간·금관으로 또박또박 */
   mel:[{n:"C5 _ _ _ Eb5 _ _ _ | G5 _ _ _ _ _ . . | Ab5 _ _ _ G5 _ F5 _ | D5 _ _ _ _ _ . . | C5 _ _ _ Eb5 _ G5 _ | C6 _ _ _ Bb5 _ Ab5 _ | Ab5 _ G5 _ F5 _ D5 _ | C5 _ _ _ _ _ . .",i:"brass",v:.15}],
   bass:{n:"1 _ _ _ 5 _ _ _",i:"sub",v:.5,o:33},pad:{i:"organ",v:.05,o:52},dr:["k.......k.......","........s......."],echo:.18};
  A.SONGS.inn_t_doto={bpm:80,vol:.96,prog:["Am","F","C","G","Am","F","Dm E","Am"],   /* 도토: 머뭇거리는 플루트, 쉼이 많다 */
   mel:[{n:"E5 _ . . . . D5 _ | C5 _ _ _ . . . . | G5 _ . . E5 _ . . | D5 _ _ _ . . . . | E5 _ . . A5 _ . . | G5 _ F5 _ . . . . | F5 _ E5 _ D5 _ G#4 _ | A4 _ _ _ . . . .",i:"flute",v:.2}],
   arp:{n:"1 5 8 5",r:2,i:"ep",v:.05,o:48},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.42,o:33},pad:{i:"string",v:.05,o:55},echo:.3};
  A.SONGS.inn_inv_old={bpm:76,vol:.85,prog:["Em","CM7","Am7","B7","Em","G","Am C","B7"],
   mel:[{n:"B5 _ _ _ G5 _ E5 _ | E5 _ _ _ D5 _ B4 _ | C5 _ E5 _ A5 _ G5 _ | F#5 _ _ _ D#5 _ _ _ | E5 _ G5 _ B5 _ E6 _ | D6 _ _ B5 _ _ G5 _ | A5 _ C6 _ E6 _ D6 _ | D#6 _ _ _ _ _ . .",i:"kal",v:.2}],
   arp:{n:"1 5 8 10 8 5 . .",r:2,i:"pluck",v:.08,o:52},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.42,o:36},pad:{i:"glass",v:.045,o:60},echo:.3};
  A.SONGS.inn_after={bpm:72,vol:.85,prog:["F","C/E","Dm","Bb","F/A","Gm","Bb C","F"],
   mel:[{n:"A5 _ _ _ G5 _ F5 _ | E5 _ _ _ G5 _ C6 _ | D6 _ _ _ C6 _ A5 _ | Bb5 _ _ _ _ _ A5 G5 | A5 _ _ _ C6 _ F6 _ | D6 _ _ _ Bb5 _ G5 _ | F5 _ G5 _ Bb5 _ C6 _ | A5 _ _ _ _ _ . .",i:"flute",v:.18}],
   arp:{n:"1 5 8 10 12 10 8 5",r:2,i:"ep",v:.06,o:48},bass:{n:"1 _ _ _ _ _ _ _",i:"sub",v:.38,o:33},pad:{i:"string",v:.045,o:57},echo:.3};

  /* ---- 음악 선택 ---- */
  var M={inv:false,p10:0,fin:0};
  var THEME={innma:"inn_t_innma",seryeon:"inn_t_seryeon",nabi:"inn_t_nabi",geokkuri:"inn_t_bami",buri:"inn_t_buri",wanggu:"inn_t_neoul",doto:"inn_t_doto"};
  /* 2026-10-10 사용자 "솜솜을 발견하는 순간은 배경음을 끄고 긴장되고 두근거리는 순간으로, 다람에게도 충격": 발견 줄부터 그 대화가 끝날 때까지 음악을 끄고 심장 박동만.
     (발견 장소는 새 구조에서 침대 밑으로 옮길 예정 — 줄 글로 걸어 두어 장소가 바뀌어도 같은 연출) */
  var TENSE={on:false,k:0};
  var TENSE_ON=/안에 작은 애가 있어|침대 밑에 작은 애가 있어|밑에 작은 애가|^등 뒤 천장에서, 거꾸로 된 두 눈/,TENSE_OFF=/^모르겠어\. 그러니까 알아봐야지|^다람이 뛰어 돌아가/;
  function tenseTick(){try{if(!TENSE.on)return;if(!cur()||typeof DL==="undefined"||!DL){TENSE.on=false;return}
    if(AC&&AC.state==="running"&&S.sound){var v=.34,gap=Math.max(.58,.86-TENSE.k*.02);tone(58,.16,"sine",v,0,null,40);tone(52,.14,"sine",v*.7,gap*.32,null,38);noise(.06,v*.25,0,160,"lowpass");TENSE.k++;setTimeout(tenseTick,gap*1000)}
    else setTimeout(tenseTick,300)}catch(e){TENSE.on=false}}
  window.__innTense=function(){return TENSE.on};
  setInterval(function(){try{if(!cur()||typeof DL==="undefined"||!DL){TENSE.on=false;return}var l=DL.lines&&DL.lines[DL.i],t=l?String(l[1]||""):"";
    if(!TENSE.on&&TENSE_ON.test(t)){TENSE.on=true;TENSE.k=0;try{SFX.cut9&&SFX.cut9()}catch(e){}setTimeout(tenseTick,450)}else if(TENSE.on&&TENSE_OFF.test(t))TENSE.on=false}catch(e){}},60);
  window.__innWant=function(){
   if(!cur())return undefined;
   A.hush=null;A.exp=null;A.pursuit=null;          /* 옛 체계의 일시 정지·승리곡·추격곡이 끼어들어 곡을 다시 시작하지 않게 */
   if(TENSE.on)return null;                         /* 발견 순간: 음악 없음 */
   var b=beats(),now=Date.now();
   /* 2026-10-10 v2 음악 큐시트(dev/review/CH1_V2_DESIGN.txt 5장): 영화처럼 줄·장면 시점에 맞춰 끊고, 한 방 치고, 다시 들어온다 */
   if(!b.inn_pro){var pi=b.inn_pi|0,sid=sidOf(pi);if(M.sid!==sid){M.sid=sid;M.sidT=now;M.p5c=0;M.hit=0}if(+String(sid).slice(1)<11)M.inv=false;
    if(sid==="P1"&&now-M.sidT<2000)return null;
    if(sid==="P10b")return null;   /* 밤 복도: 음악 없이 정적(두 눈이 뜰 때 심장 박동) */   /* 제목 카드 뒤 2초 정적 → 여행곡 */
    if(sid==="P13"){if(!M.hit&&/^베개 밑…/.test(lineText())){M.hit=now;try{SFX.cut9()}catch(e){}}if(M.hit&&now-M.hit<1500)return null}   /* 주머니 발견: 음악 끊고 한 방 → 1.5초 정적 */   /* 2026-10-10: 번호(pi<6) 대신 장면 이름으로(도입 재배치 뒤 P11이 5번) */
    if(['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10'].indexOf(sid)>=0)return "inn_travel";   /* P1~P10 */
    if(sid==="P11"){if(/^제 주머니가 없어졌|^계약금이 든 주머니/.test(lineText()))M.inv=true;   /* 2026-10-10: 범죄를 처음 알아채는 줄(세련의 외침)에서 바로 사건곡 */return M.inv?"inn_serious":null}   /* P11: 신고 확인 뒤 */
    return "inn_serious"}                         /* P12 수색·P13 안 쓰는 방: 사건곡(낮게) */
   if(!b.inn_final){var rt=document.querySelector("body>.rt");if(!rt){var th=null;try{if(G.tab==="talk"&&G.who){if(M.tw!==G.who){M.tw=G.who;M.tt=Date.now()}if(Date.now()-M.tt>2500)th=THEME[G.who]}else M.tw=null}catch(e){}return th||"inn_inv"}   /* 짧게 한 마디 묻고 나오면 조사곡이 처음부터 다시 시작하지 않게: 대화 2.5초 뒤에 테마로 */   /* 조사 중 인물과 대화: 그 인물의 테마 */
    var ph=null,E=window.EP1INN||{},fin=false;try{ph=window.__rtPh&&__rtPh();fin=!!(ph&&E.FINAL&&E.FINAL.phases&&E.FINAL.phases.indexOf(ph)>=0)}catch(e){}
    /* 정답 제시('그건 아니야!'/'이걸 봐!') 순간: 음악을 끊고 외침 → 이어서 추궁곡. 그 발언의 대화가 끝나고 1.5초 뒤(또는 단계가 바뀌면) 원래 곡으로 */
    if(M.obj){if(now-M.obj<1400)return null;var dl0=(typeof DL!=="undefined"&&DL);if(dl0)M.objDL=now;if(ph!==M.objPh||(!dl0&&now-(M.objDL||M.obj)>1500))M.obj=0;else return "inn_climax"}
    if(fin&&M.f4){if(now-M.f4<2500)return null;return "inn_t_innma"}   /* 세련 인정("…네.") 뒤: 정적 → 할머니 테마 작게 */
    if(fin){if(typeof DL!=="undefined"&&DL&&DL.lines){var l4=DL.lines[DL.i];if(l4&&l4[0]==="seryeon"&&/^…네\.$/.test(String(l4[1]||""))&&!M.f4){M.f4=now;try{SFX.cut9()}catch(e){}return null}}return "inn_climax"}
    return "inn_meet"}                              /* 조사 / 원탁회의 / 최종 대결: 장면마다 다른 곡 */
   M.f4=0;if(M.fin&&Date.now()-M.fin>7000)return null;     /* 마지막 줄 뒤 천천히 끝난 다음 */
   return "inn_after"};
  /* 2026-10-10 "배경음이 다들 약하다": 1장 배경음 +4.6dB(×1.7), 대화 중 기본 낮춤(.62)도 .85로 덜 낮춘다. 결정적 대사(아래 KEY)에서는 배경음을 끊는다 */
  var KEY=/^종이 막 그쳤다고도|^자정에 겹친 바늘을 거꾸로|^솜솜은 살아 있습니다|^솜솜의 털에 묻은 글씨를 보시죠|^아침에는 솜솜 아래에서 주머니를 봤다고|^저희 부녀 말고 그 자리를 아는 사람은|^봉인이 온전하다면 봉한 뒤로|^그래서 여쭙겠습니다\. 주머니를 되찾으려던|^…엄마 글씨야/;
  window.__innKeyLine=function(){var t=lineText();return !!t&&KEY.test(t)};
  window.__innDuck=function(){var r=window.__innDuck0.apply(this,arguments);if(!cur()||document.getElementById("inncold"))return r;
   if(window.__innKeyLine())return 0;
   return r*1.7*((typeof DL!=="undefined"&&DL)?.85/.62:1)};
  window.__innDuck0=function(){
   if(document.getElementById("inncold"))return COLDD;   /* 콜드 오픈: 비트마다 정한 낮춤(정적으로 갈수록 작게) */
   if(!cur())return 1;
   var b=beats(),now=Date.now(),f=(typeof DL!=="undefined"&&DL)?.9:1,t=lineText();   /* 2026-10-10: 대화 중 배경음 .62×.9≈.56(-5dB) — 타이핑·효과음이 묻히지 않게 */
   if(!b.inn_pro){var pi=b.inn_pi|0;
    var sd=sidOf(pi);if(sd!=="P10")M.p10=0;
    if(sd==="P5"){f=.8;if(/^열셋/.test(t))M.p5c=1;if(M.p5c)f=.38}   /* P5 복도: 같은 곡 낮게, "열셋."부터 더 낮게 */
    if(sd==="P10"){if(!M.p10)M.p10=now;f=Math.max(0,1-(now-M.p10)/14000)}   /* P10: 여행곡 천천히 종료 */
    if(sd==="P12")f=.7;if(sd==="P13")f=.6;     /* 수색·발견: 사건곡 낮게 */
    return f}
   if(!b.inn_final){if(M.obj&&document.querySelector("body>.rt"))f*=.72;if(M.f4)f*=.55;return f}   /* 추궁곡·인정 뒤 할머니 테마는 낮게 */
   var ei=b.inn_ei|0;
   if(!b.inn_end&&ei===3){f=.6;if(/^이 사람입니다|^할머니, 아까 그 장부/.test(t))f=.12}   /* E4: 엄마 사진을 내미는 순간 정적 */
   if((!b.inn_end&&ei===4&&/^…올해는 네 딸이 왔다/.test(t))||b.inn_end){if(!M.fin)M.fin=now}
   if(M.fin)f*=Math.max(0,1-(now-M.fin)/6500);
   return f};

  /* ---- 타이핑음 ---- */
  var lastT=0;
  window.__innType=function(kind){try{
   if(!S.sound||!AC||AC.state!=="running")return;var now=AC.currentTime;if(now-lastT<.055)return;lastT=now;
   var v=kind==="inner"?.6:kind==="narr"?.7:1;   /* 2026-10-10: 타이핑 약 +10dB, 소리 높이를 조금씩 달리해 반복 피로를 줄임 */
   tone(560+Math.random()*60,.026,"square",.045*v);noise(.01,.06*v,0,2600,"bandpass")}catch(e){}};   /* 2026-10-10 "따따따 전자음": 짧은 사각파 블립 + 작은 클릭 */
  var _blip=SFX.blip;
  SFX.blip=function(){if(!cur())return _blip.apply(this,arguments);window.__innType(lineKind())};

  /* ---- 1장 효과음 보정 ---- */
  function wrap(k,fn){var o=SFX[k];SFX[k]=function(){if(!cur())return o&&o.apply(this,arguments);try{fn.apply(this,arguments)}catch(e){}}}
  wrap("door",function(){if(!S.sound)return;noise(.06,.3,0,900,"lowpass");tone(140,.09,"sine",.28,0,null,90);noise(.015,.1,.03,3000,"highpass")});   /* 문 닫힘: 달칵(옛 '딩동' 아님) */
  wrap("slam",function(){if(!S.sound)return;tone(100,.26,"sine",.55,0,null,45);noise(.18,.45,0,520)});   /* P11 기상: 쾅 1회, 과하지 않게 */
  wrap("letter",function(){});                     /* 장면 제목 글자마다 '틱' 없음 */
  wrap("impact",function(){if(!S.sound)return;if(!document.querySelector("body>.rt")&&!(beats().inn_final&&!beats().inn_end)){tone(660,.5,"sine",.06);tone(990,.35,"sine",.025,.04);return}tone(98,.5,"sine",.3,0,null,62);noise(.25,.12,0,300)});   /* 2026-10-10 검수: 장소·시각 띠마다 쿵 → 회의·최종 대결 밖에서는 부드러운 종 */
  wrap("tick2",function(){});                      /* 빈 곳 터치 '틱' 없음 */
  wrap("roll",function(){});                       /* 옛 드럼롤(마차 대용) 없음 */
  /* 2026-10-10 "앗! 헉! 같은 말에 빠악! 충격음": 날카로운 타격 + 짧은 하강음 */
  SFX.shock9=function(){if(!S.sound)return;try{noise(.09,.5,0,2600,"highpass");tone(1500,.16,"square",.09,0,null,380);tone(110,.28,"sine",.5,0,null,55);noise(.22,.18,.02,700,"lowpass")}catch(e){}};
  /* 증거·재미있는 물건이 튀어나올 때: 짧은 반짝 */
  SFX.pop9=function(){if(!S.sound)return;try{[880,1320,1760].forEach(function(f,i){tone(f,.12,"triangle",.14,i*.05)});noise(.05,.05,0,6000,"highpass")}catch(e){}};
  /* 결정적 대사: 배경음이 끊길 때 둔탁한 한 방 */
  SFX.cut9=function(){if(!S.sound)return;try{tone(70,.6,"sine",.55,0,null,40);noise(.35,.25,0,240,"lowpass");tone(2200,.05,"square",.05)}catch(e){}};
  var lastLn=null;setInterval(function(){try{if(!cur()||typeof DL==="undefined"||!DL||!DL.lines)return;var ln=DL.lines[DL.i];if(!ln||ln===lastLn)return;lastLn=ln;var t=String(ln[1]||"");
    var md=String(ln[2]||"");
    if(/^(앗|헉|엇|으악|아악|어머|세상에)[!?.…,\s]|^…?(앗|헉)/.test(t)||/shock|surprise/.test(md)||/\?!|!\?/.test(t))SFX.shock9();
    else if(/^…움직였어/.test(t))SFX.pop9();   /* 2026-10-10: 솜솜 발견 줄은 충격 연출(TENSE)이라 반짝 효과음 제외 */
    else if(/^거긴 (창고|지금은 안 쓰는 방)/.test(t))SFX.low9();   /* P5: 안 쓰는 방이라는 말에 낮은 단음 하나 */
    else if(KEY.test(t))SFX.cut9()}catch(e){}},60);
  /* 낮은 단음(현 피치카토 + 저음): 분위기만 바꾸는 한 음 */
  SFX.low9=function(){if(!S.sound)return;try{tone(98,1.8,"sine",.32,0,null,92);tone(147,1.2,"triangle",.07,.02);noise(.05,.04,0,500,"lowpass")}catch(e){}};
  /* 회의·최종 대결 정답 외침: 엔진 외침 효과음에 맞춰 음악을 끊고 추궁곡으로 */
  (function(){var o=SFX.shout;SFX.shout=function(){try{if(cur()&&document.querySelector("body>.rt")){M.obj=Date.now();M.objDL=0;M.objPh=window.__rtPh&&__rtPh()}}catch(e){}return o&&o.apply(this,arguments)}})();
  /* 2026-10-10 사용자: "문 여는 소리는 끼익", "마차 멈추는 소리가 배고픈 소리 같다", "종소리가 경보음 같다" */
  function creakAt(a,t,dur,f0,f1,vol){var o=a.createOscillator(),bp=a.createBiquadFilter(),g=a.createGain(),am=a.createOscillator(),ag=a.createGain();
   o.type="sawtooth";o.frequency.setValueAtTime(f0,t);o.frequency.linearRampToValueAtTime(f1,t+dur*.7);o.frequency.linearRampToValueAtTime(f1*.92,t+dur);
   bp.type="bandpass";bp.frequency.value=1500;bp.Q.value=3.5;am.frequency.value=38;ag.gain.value=.45;am.connect(ag);ag.connect(g.gain);   /* 마찰로 떨리는 경첩 */
   g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.05);g.gain.setValueAtTime(vol*.8,t+dur*.8);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
   o.connect(bp);bp.connect(g);g.connect(SFXG);o.start(t);am.start(t);o.stop(t+dur+.05);am.stop(t+dur+.05)}
  /* 2026-10-10 사용자 "문 여는 소리가 이상하다, 더 예쁜 중저음 끼익으로": 높은 톱니파(1.5kHz 대역) 대신 낮은 삼각파 두 겹을 저역 통과로 둥글게.
     경첩이 천천히 도는 느낌(약 190→250→225Hz, 1.1초), 떨림은 약하게(17Hz), 끝에 문이 멈추는 나무 소리 한 번 */
  function hingeAt(a,t,dur,f0,f1,vol){var o=a.createOscillator(),o2=a.createOscillator(),lp=a.createBiquadFilter(),bp=a.createBiquadFilter(),g=a.createGain(),am=a.createOscillator(),ag=a.createGain();
   o.type="triangle";o2.type="triangle";[o,o2].forEach(function(x,k){var m=k?2.005:1;x.frequency.setValueAtTime(f0*m,t);x.frequency.linearRampToValueAtTime(f1*m,t+dur*.55);x.frequency.linearRampToValueAtTime(f1*.9*m,t+dur)});
   var g2=a.createGain();g2.gain.value=.35;o2.connect(g2);
   lp.type="lowpass";lp.frequency.value=700;lp.Q.value=.7;bp.type="bandpass";bp.frequency.value=380;bp.Q.value=1;
   am.frequency.value=17;ag.gain.value=.3;am.connect(ag);ag.connect(g.gain);
   g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.12);g.gain.setValueAtTime(vol*.85,t+dur*.75);g.gain.exponentialRampToValueAtTime(.0001,t+dur);
   o.connect(lp);g2.connect(lp);lp.connect(bp);bp.connect(g);g.connect(SFXG);[o,o2,am].forEach(function(x){x.start(t);x.stop(t+dur+.05)})}
  wrap("doorOpen",function(){if(!S.sound||!AC)return;var t=AC.currentTime;hingeAt(AC,t,1.1,190,250,.12);noise(.09,.1,1.08,380,"lowpass");tone(110,.12,"sine",.12,1.08,null,80)});
  SFX.carStop=function(){if(!S.sound||!AC)return;var t=AC.currentTime;
   [0,.32,.7,1.15].forEach(function(w,i){var v=.32-i*.06;tone(820,.05,"triangle",v,w,null,560);noise(.04,v*.7,w,2200,"bandpass")});   /* 말발굽이 느려지며 */
   noise(.5,.06,1.3,500,"bandpass")};   /* 바퀴 멎음(2026-10-10 까마귀처럼 들리던 차체 삐걱 제거) */
  SFX.bell10=function(){if(!S.sound)return;try{var a=ac();if(!a)return;for(var i=0;i<10;i++){var w=i*1.15;   /* 멀리서 울리는 낮은 마을 종(높은 배음을 줄여 '삐-' 경보음처럼 들리지 않게) */
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
   if(key==="carriage"){
    var lp=a.createBiquadFilter();lp.type="lowpass";lp.frequency.value=2400;lp.connect(out);I.lp=lp;
    /* 2026-10-10 "자동차처럼 웅웅거린다, 마차면 말발굽이 들려야": 낮은 구름음·마찰음 없앰 → 또각또각 말발굽 + 가끔 나무 삐걱·마구 방울 */
    I.bus=lp;I.peak=.7}   /* 2026-10-10 "마차 소리가 거슬린다": 전체 -6dB, 마찰음·덜컹 더 낮게 */
   else if(key==="wind"){var wd=loopSrc(a,out,"bandpass",480,.8,.35);I.src.push(wd.s);
    var l2=a.createOscillator(),g2=a.createGain();l2.frequency.value=.11;g2.gain.value=220;l2.connect(g2);g2.connect(wd.f.frequency);l2.start();I.src.push(l2);I.peak=.5}
   out.gain.exponentialRampToValueAtTime(I.peak,a.currentTime+.4);return I}
  function sched(I){if(I.key!=="carriage"||I.dead)return;if(I.ending&&I.a.currentTime>I.ending)return;var a=I.a,now=a.currentTime,n=I.next;
   if(n.r==null)n.r=now+1+Math.random()*2;if(n.h==null)n.h=now+.3;
   while(n.r<now+.3){var k=3+(Math.random()*3|0),t=n.r;for(var j=0;j<k;j++){burst(a,I.bus,t,.03,.03+Math.random()*.02,"bandpass",900+Math.random()*500,2.5);t+=.03+Math.random()*.05}n.r+=4+Math.random()*4}   /* 차체 덜컹: 간헐적 */
   while(n.h<now+.3){clop(a,I.bus,n.h,.16);clop(a,I.bus,n.h+.19+Math.random()*.02,.12);n.h+=.62+Math.random()*.04}   /* 또각또각(빠른 걸음) */
   /* 2026-10-10 사용자 "마차의 까악거리는 까마귀 소리 제거": 오르는 톱니파 삐걱이 까마귀 울음처럼 들림 → 마차 장면 반복 삐걱 삭제(말발굽·덜컹·방울은 유지) */   /* 차체 나무 삐걱 */
   if(n.j==null)n.j=now+2;while(n.j<now+.3){[0,.09,.2].forEach(function(w){var o=a.createOscillator(),g=a.createGain();o.frequency.value=2900+Math.random()*500;g.gain.setValueAtTime(.0001,n.j+w);g.gain.exponentialRampToValueAtTime(.025,n.j+w+.005);g.gain.exponentialRampToValueAtTime(.0001,n.j+w+.25);o.connect(g);g.connect(I.bus);o.start(n.j+w);o.stop(n.j+w+.3)});n.j+=4+Math.random()*5}}   /* 마구 방울 */
  function clop(a,out,t,vol){var o=a.createOscillator(),g=a.createGain();o.type="triangle";o.frequency.setValueAtTime(900+Math.random()*160,t);o.frequency.exponentialRampToValueAtTime(520,t+.05);
   g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(vol,t+.004);g.gain.exponentialRampToValueAtTime(.0001,t+.07);o.connect(g);g.connect(out);o.start(t);o.stop(t+.09);burst(a,out,t,.04,vol*.8,"bandpass",2000,2)}
  function stop(I,dur){if(!I||I.ending)return;var a=I.a,t=a.currentTime;dur=dur||.8;I.ending=t+dur*.8;AMB.old.push(I);
   try{I.out.gain.cancelScheduledValues(t);I.out.gain.setValueAtTime(Math.max(.0001,I.out.gain.value),t);I.out.gain.exponentialRampToValueAtTime(.0001,t+dur);if(I.lp){I.lp.frequency.setValueAtTime(I.lp.frequency.value,t);I.lp.frequency.exponentialRampToValueAtTime(180,t+dur)}}catch(e){}
   setTimeout(function(){I.dead=true;var k=AMB.old.indexOf(I);if(k>=0)AMB.old.splice(k,1);I.src.forEach(function(s){try{s.stop()}catch(e){}});try{I.out.disconnect()}catch(e){}},dur*1000+300)}
  var AMB={cur:null,dep:null,old:[]};
  function ambWant(){if(!cur()||!S.sound||window.__innAudioHold||document.getElementById("inncold"))return null;var b=beats();
   if(!b.inn_pro){var sd=sidOf(b.inn_pi|0);if(sd==="P1"&&b.inn_bg==="carriage")return "carriage";return null}   /* 2026-10-10 "광장 바람 소리 거슬린다": 뺌 */
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
