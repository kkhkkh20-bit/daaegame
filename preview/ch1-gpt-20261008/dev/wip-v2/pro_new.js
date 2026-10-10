 /* ---- 프롤로그 P1~P13 (2026-10-09 장면 대본 JSON에서 생성: gen/conv.py) ----
    I(속마음[,무대,첫진입만]) / L(화자,대사,"",표정) / N(회색 지문: 대체 그림이 없는 사실만) / D({who,sfx,ms,chime}) 글자 없는 연출 */
 function I(t,cue,entry){var x="("+t+")";if(cue)(window.__INNCUE=window.__INNCUE||{})[x]=cue;if(entry)(window.__INNENTRY=window.__INNENTRY||{})[x]=1;return ["narr",x]}
 function B(bg,who,s){s.bg=bg;s.who=who;return s}
 function D(o){return {dir:o}}
 function SID(id,s){s.sid=id;return s}
 window.__INNSID=SID;
 function FL(w,t,f){return f?[w,t,"","","","",f]:[w,t]}
 window.__INNFL=FL;
 EP.PRO=[
  /* P1 우편 마차 안 */
  SID("P1",B("carriage","det1",S("front","고갯길, 우편 마차 안","첫날 오후",[
   D({"who": "det1", "chime": 1, "ms": 380}),
   {hint:"화면을 누르면 다음 대사로 넘어가요"},
   FL("det1","아빠, 마지막 봉지야. 작은 반은 아빠 몫."),
   FL("det0","서점에 있을 때도 아빠 몫은 작았지."),
   FL("det1","엄마 책 읽고, 아빠 괴물 목소리 내던 거 기억나?"),
   I("결혼 뒤 탐정 일을 접고 서점을 열었다."),
   FL("det1","엄마 찾으면 또 셋이 읽자.","sad"),
   FL("det0","그러자. 괴물 목소리는 아빠가 맡을게."),
   I("엄마가 갑자기 사라지고 옛 편지를 꺼냈다."),
   FL("det0","편지 도장에 마을 이름이 있어."),
   FL("det1","골짜기… 마을. 엄마가 여기서 부친 거야?"),
   FL("det0","몇 해 전 편지야. 우체국에 물어보자.","sad"),
   D({"sfx": "carStop", "ms": 380}),
   D({"who": "karo", "chime": 1, "ms": 380}),
   FL("karo","마부 까로예요. 곧 골짜기 마을입니다."),
   FL("karo","나가는 마차는 내일 정오. 놓치면 봄이에요."),
   FL("det0","그럼 내일 오전에 알아봐야겠군요.","think")]))),
  /* P2 마을 입구 광장 */
  SID("P2",B("plaza","det1",S("front","마을 입구, 광장","첫날 저녁",[
   I("우체국은 닫혔다."),
   D({"who": "det1", "chime": 1, "ms": 380}),
   FL("det1","저기! '겨울잠 여관, 언덕 위'래."),
   FL("det0","오늘은 거기서 묵자."),
   D({"who": "none", "ms": 300}),
   D({"sfx": "steps", "ms": 420})]))),
  /* P3 여관 현관 안 */
  SID("P3",B("reception","innma",S("front","여관 현관","첫날 저녁",[D({sfx:"knock",ms:650}),D({sfx:"doorOpen",ms:550}),D({sfx:"door",ms:450}),
   D({"who": "innma", "chime": 1, "ms": 380}),
   FL("det0","안녕하세요. 하룻밤 묵을 수 있을까요?"),
   FL("innma","어서 와요. 추웠지?","smile"),
   FL("det0","아이 엄마를 찾고 있습니다. 여기서 옛 편지를 부쳤더군요."),
   N("아빠가 엄마 사진을 내민다."),
   FL("innma","…사진 속 엄마를 닮았구나.","think"),
   FL("det1","만나 보셨어요?"),
   FL("innma","…오래전 손님은 잘 기억이 안 나요. 편지는 우체국에 물어봐요.","think"),
   FL("innma","우선 들어와요. 방은 있어요.")]))),
  /* P5 2층 복도와 열세 번째 침대 */
  SID("P5",B("corridor","innma",S("hall","2층 복도","첫날 저녁",[D({sfx:"steps",ms:450}),
   D({"who": "innma", "chime": 1, "ms": 380}),
   FL("innma","등잔은 밤새 켜 둬요. 겨울잠 손님들이 있으니 살금살금."),
   FL("innma","방마다 침대 하나예요. 두 사람은 앞 계단 쪽, 끝에서 둘째 방."),
   FL("det1","열셋. 할머니, 저 안에도 침대가 있어요."),
   FL("innma","거긴 지금은 안 쓰는 방이에요. 손님 받는 침대는 열둘이에요.","think"),
   D({"sfx": "door", "ms": 420})],"title"))),
  /* P10 부녀의 방 */
  SID("P10",B("room","det1",S("hall","부녀의 방","첫날 한밤",[
   D({"who": "det1", "chime": 1, "ms": 380}),
   FL("det1","아빠. 할머니는 엄마를 아는 걸까?","sad"),
   FL("det0","내일 다시 여쭤보자."),
   FL("det1","아빠. 괴물 목소리 한 번만."),
   FL("det0","크르르. 내 책을 누가 가져갔느냐."),
   FL("det1","책 말고 간식이야. 엄마가 맨날 고쳐 줬잖아."),
   FL("det0","맞다. 간식. 크르르."),
   FL("det1","목소리는 똑같네.","smile"),
   FL("det1","나도 아빠처럼 탐정 할래. 엄마 찾는 것도 같이 할래."),
   FL("det0","좋아. 아빠가 놓친 건 네가 알려 줘."),
   FL("det0","대신 혼자 먼저 가지 않기."),
   D({"sfx": "bell10", "ms": 7800}),
   FL("det1","…여덟, 아홉, 열. 열 시다.","sad"),
   FL("det0","정각에만 쳐. 반 시에는 안 치고.","sad"),
   FL("det1","그럼 반 시는 내가 알려 줄게. 땡."),
   FL("det0","잘 자, 다람."),
   {fade:1}]))),
  /* P10b 닫힌 문 밑의 빛 */
  SID("P10b",B("corridor",null,S("hall","부녀의 방 → 2층 복도","그 밤, 열한 시 무렵",[
   FL("narr","이불 끄는 소리에 다람이 눈을 뜬다. 아빠는 잠들어 있다."),
   D({"who": "det1", "chime": 0, "ms": 300}),
   FL("det1","아빠…?","sad"),
   FL("narr","다람이 방문을 조금 연다. 안 쓰는 방의 닫힌 문 밑으로 빛이 샌다."),
   FL("det1","누가 있어요?","nervous"),
   FL("narr","다람이 문에 손을 댄다. 소리가 뚝 멎는다. 빛도 꺼진다."),
   D({"who": "none", "ms": 500}),
   FL("narr","등 뒤 천장에서, 거꾸로 된 두 눈이 뜬다."),
   D({"who": "geokkuri", "chime": 0, "ms": 380}),
   FL("geokkuri","…가서 자, 꼬맹이."),
   FL("geokkuri","저 방은 밤엔 안 열어. 원래 그래."),
   D({"who": "none", "ms": 380}),
   FL("narr","다람이 뛰어 돌아가 이불을 머리끝까지 끌어올린다."),
   D({"ms": 900}),
   {fade:1}]))),
  /* P11 주머니가 사라졌다는 신고 */
  SID("P11",B("corridor","seryeon",S("hall","2층 복도","다음 날 아침 7시",[{sfx:"slam"},

   D({"who": "seryeon", "chime": 0, "ms": 380}),
   FL("seryeon","제 주머니가 없어졌습니다! 다들 나와 보세요!","shock"),
   FL("det0","무슨 일이십니까?"),
   FL("seryeon","세련입니다. 머리맡에 둔 계약금 주머니가 없어졌습니다.","nervous"),
   FL("seryeon","삼백 냥입니다. 종이띠에 제 도장을 찍어 봉했어요."),
   FL("det0","방은 찾아보셨습니까?"),
   FL("seryeon","여섯 시 반에 일어나 방과 복도부터 뒤졌습니다.","nervous"),
   D({"who": "innma", "chime": 0, "ms": 380}),
   FL("innma","주머니가 없어졌다고요?","think"),
   FL("innma","나비야, 너울 씨를 불러 오너라.","think")]))),
  /* P12 자경단장의 수색 */
  SID("P12",B("corridor","wanggu",S("hall","2층 복도","아침 7시 20분",[

   D({"sfx": "steps", "who": "wanggu", "chime": 0, "ms": 380}),
   FL("wanggu","자경단장 너울입니다. 주머니는 어떻게 생겼습니까?"),
   D({"who": "seryeon", "chime": 0, "ms": 260}),
   FL("seryeon","붉은 봉인띠를 두른 가죽 주머니요. 제 도장을 찍었습니다."),
   D({"who": "wanggu", "chime": 0, "ms": 260}),
   FL("wanggu","동의를 받고 방마다 살펴보겠습니다."),
   D({"sfx": "doorOpen", "ms": 420}),
   FL("narr","세련 씨 방. 머리맡, 가방, 침대 밑. 없다."),
   D({"sfx": "doorOpen", "ms": 420}),
   FL("narr","복도의 손님방들. 손님마다 동의를 받고 하나씩. 없다."),

   D({"who": "innma", "chime": 0, "ms": 380}),
   FL("innma","거긴 안 돼요. 안 쓰는 방이에요.","think"),
   D({"who": "wanggu", "chime": 0, "ms": 260}),
   FL("wanggu","빈방도 함께 보시죠. 손댄 것은 기록합니다."),
   FL("wanggu","열겠습니다. 비켜 주십시오."),
   D({"sfx": "doorOpen", "who": "none", "ms": 380})]))),
  /* P13 안 쓰는 방의 주머니 */
  SID("P13",B(null,"wanggu",S("bed13","2층 안 쓰는 방","아침 7시 반",[D({sfx:"steps",ms:450}),

   D({"who": "wanggu", "chime": 0, "ms": 380}),
   FL("wanggu","베개 밑…. 여기 있군요."),
   FL("wanggu","세련 씨 주머니가 맞습니까? 봉인은요?"),
   D({"who": "seryeon", "chime": 0, "ms": 260}),
   FL("seryeon","맞습니다. 제 도장이에요. 뜯긴 데도 없고요."),
   I("너울 씨가 봉인띠를 자르고 은화를 하나씩 센다. 다람이도 입속으로 따라 센다."),
   D({"who": "det1", "chime": 0, "ms": 260}),
   FL("det1","…아흔여덟, 아흔아홉, 백."),
   D({"who": "wanggu", "chime": 0, "ms": 260}),
   FL("wanggu","은화 백 냥입니다."),
   D({"who": "seryeon", "chime": 0, "ms": 260}),
   FL("seryeon","백 냥이라뇨. 삼백 냥이었습니다!","shock"),

   D({"who": "innma", "chime": 0, "ms": 380}),
   FL("narr","할머니가 이불을 들춘다. 빈 베개 구석을 더듬는다."),
   D({"who": "innma", "chime": 0, "ms": 260}),
   FL("innma","어디… 어디 갔지.","think"),

   D({"who": "seryeon", "chime": 0, "ms": 260}),
   FL("seryeon","무엇을 찾으십니까?"),
   D({"who": "wanggu", "chime": 0, "ms": 260}),
   FL("wanggu","봉인 온전, 백 냥. 삼백 냥이라는 주장과 다릅니다."),
   FL("wanggu","정오 전에 회의로 확인하겠습니다."),
   FL("wanggu","해결 못 하면 할머니는 위 마을 관청에 가셔야 합니다. 정오 마차로요."),
   FL("det0","이 방에서 나왔다고 할머니가 도둑은 아니지요?"),
   FL("wanggu","아직 모릅니다."),
   FL("det0","예전에 탐정 일을 했습니다. 저희도 살펴보겠습니다."),
   FL("wanggu","물건의 위치는 바꾸지 마십시오."),
   D({"sfx": "steps", "who": "none", "ms": 380}),
   D({"who": "det1", "chime": 0, "ms": 380}),
   FL("det1","아빠. 할머니, 돈 안 봤어. 이불 봤어.","sad"),
   FL("det1","할머니가 가면 엄마 얘긴 누가 해 줘?","sad"),
   FL("det0","엄마 얘기도 들어야지. 주머니와 이불부터 살펴보자."),
   FL("det1","할머니가 이불 보던 것도 적을게.")])))
 ];
