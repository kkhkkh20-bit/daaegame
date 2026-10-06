/* The original CASES / COMBO / BATTLE schema, adapted to this chapter. */
const PERSONAL={
 receipt:'서명이 지렁이처럼 꼬불꼬불하다. 지렁이도 자기 이름은 읽을까?',
 tray:'봉투도 없고 간식도 없다. 둘 중 하나는 있어야 예의 아닌가.',
 clock:'째깍째깍. 시계는 말을 짧게 해서 좋다. 까로 아저씨도 배우셨으면.',
 cabinet:'비밀을 숨기기에는 너무 「나 비밀 있음」처럼 생겼다.',
 key:'열쇠도 예비가 있다. 내 용기도 예비를 하나 챙겨 올걸.',
 envelope:'돈보다 봉투가 먼저 감금당했다. 일단 봉투는 무사 구조!',
 roster:'할머니 이름이 없다고 할머니가 없는 사람이 되는 건 아닌데.',
 report:'엄마 글씨다. 아는 글씨를 만나니까 괜히 코끝이 간질간질하다.'
};
const INSPECTIONS={
 receipt:{label:'서명 아래 문구 검사',text:'「위 물품을 접수하였음을 확인합니다.」 서명이 확인하는 범위는 봉투 접수다.'},
 key:{label:'열쇠와 잠금쇠 번호 비교',text:'둘 다 02번. 예비 열쇠로도 보관함을 열 수 있다.'},
 roster:{label:'명단 하단의 확인 문구 검사',text:'시설 점검자의 서명으로 지급 대상의 검증까지 대신하고 있다.'},
 report:{label:'보고서의 점검 범위 검사',text:'건물·난방·대피로를 점검했다. 주민의 지원금 자격은 확인하지 않았다.'}
};
const COMBINATIONS=[
 {id:'cx_reception_0',a:'receipt',b:'t_paid',name:'서명이 확인한 것',text:'까로는 서명을 지급 완료로 읽었지만 접수증은 봉투를 받은 것만 확인한다.'},
 {id:'cx_reception_1',a:'key',b:'cabinet',name:'두 번째 열쇠',text:'같은 02번 잠금쇠와 예비 열쇠. 주인의 열쇠가 없어도 열 수 있다.'},
 {id:'cx_reception_2',a:'roster',b:'report',name:'엇갈린 확인 범위',text:'시설 안전을 확인한 서명이 주민 지급 명단의 보증으로 옮겨 쓰였다.'}
];
COMBINATIONS.forEach(x=>EVIDENCE[x.id]={title:x.name,desc:x.text,body:'<p>'+x.text+'</p>',note:'두 단서가 이어져 확인한 사실.',memo:'수첩 두 페이지가 악수를 했다. 나는 박수.'});
Object.entries(EVIDENCE).forEach(([id,e])=>{e.memo=e.memo||PERSONAL[id]||'일단 적어 두기. 멋있는 탐정은 메모를 한다.';e.check=INSPECTIONS[id]&&{gate:true,label:INSPECTIONS[id].label,text:INSPECTIONS[id].text,desc2:INSPECTIONS[id].text};});
const TESTIMONIES={
 t_delivery:{who:'karo',q:'봉투를 누구에게?',a:'세 시에 뭉치에게 봉투를 건네고 서명을 받았습니다.'},
 t_paid:{who:'karo',q:'그 서명은 어떤 뜻?',a:'접수도 끝났고, 주민 지급도 끝났겠죠.'},
 t_witness:{who:'karo',q:'직접 지급하는 걸 봤나요?',a:'그건 못 봤죠. 여기서 젖은 날개를 말렸습니다.'},
 t_spoon:{who:'karo',q:'주머니의 반짝이는 것은?',a:'숟가락입니다. 샀어요. 반짝임은 죄가 아니니까.'},
 t_key:{who:'mungchi',q:'목에 건 열쇠는?',a:'보관함 예비 열쇠예요. 접수 담당자가 갖고 있어요.'},
 t_reason:{who:'mungchi',q:'언제 없어진 걸 알았나요?',a:'주민이 돈을 받으러 왔을 때요. 계속 보고 있지는 않았어요.'},
 confession:{who:'mungchi',q:'봉투를 왜 숨겼나요?',a:'할머니가 명단에서 빠졌는데, 지급이 끝나면 고칠 수 없을까 봐 숨겼어요.'}
};
const PEOPLE={
 daram:{name:'다람',role:'11살 다람쥐 · 견습 탐정',fact:'실종된 엄마의 보고서를 확인하러 왔다. 궁금한 건 못 참고, 겁이 나면 수첩부터 꼭 쥔다.',memo:'명탐정 예정. 예정이니까 아직 실수해도 됨.'},
 karo:{name:'까로',role:'까마귀 배달부',fact:'봉투를 가져왔다. 지급 장면은 직접 보지 못했다.',memo:'첫인상: 얼굴 좀 못생김. 눈썹이 너무 화나 있음. …숟가락은 예쁨.'},
 mungchi:{name:'뭉치',role:'고슴도치 접수 담당자',fact:'봉투를 받은 사람. 담당자용 예비 열쇠를 갖고 있다.',memo:'뭔가 숨기면 안경도 같이 숨고 싶어 하는 얼굴. 내 눈은 안 피하셔도 되는데.'},
 dad:{name:'다온',role:'다람의 아빠 · 탐정',fact:'다람과 함께 엄마의 행적을 확인한다.',memo:'내 편. 가끔 너무 내 편이라 내가 한 번 더 물어봐야 함.'}
};
const asEvidence=id=>({id,name:EVIDENCE[id].title,desc:EVIDENCE[id].desc,check:EVIDENCE[id].check});
const CHAPTER_CASE={id:'reception',lives:5,suspects:['karo','mungchi'],cast:PEOPLE,
 locations:[
  {id:'window',name:'창가',pan:0,spots:['receipt'].map(id=>({ev:asEvidence(id)}))},
  {id:'desk',name:'접수대',pan:.5,spots:['tray','clock'].map(id=>({ev:asEvidence(id)}))},
  {id:'cabinet',name:'보관함',pan:1,spots:['cabinet','key'].map(id=>({ev:asEvidence(id)}))},
  {id:'archive',name:'보관함 안쪽',pan:1,req:'door:archive',spots:['envelope','roster','report',...COMBINATIONS.map(x=>x.id)].map(id=>({ev:asEvidence(id)}))}
 ],talk:{karo:[],mungchi:[]},
 rounds:[
  {who:'karo',stm:[{t:'오후 세 시에 뭉치에게 봉투를 건넸습니다.',p:'제 앞에서 서명했어요.',a:[]},{t:'서명을 받았으니 주민 지급도 끝났습니다.',p:'확인서니까 지급 확인이죠.',a:['receipt','cx_reception_0']}],hit:'제가 확인한 건 봉투를 받은 데까지네요.'},
  {who:'mungchi',stm:[{t:'봉투는 제가 받아서 접수대에 뒀어요.',p:'받은 건 맞아요.',a:[]},{t:'주인님 열쇠가 없으니 보관함은 아무도 못 열어요.',p:'주인님 열쇠는 없어요.',a:['key','cx_reception_1']}],hit:'제가 예비 열쇠로 열었어요.'}
 ],final:[{question:'봉투를 숨긴 사람',answer:'mungchi',options:[['karo','까로'],['mungchi','뭉치']]},{question:'숨긴 장소',answer:'cabinet',options:[['window','창가'],['cabinet','보관함']]},{question:'숨긴 이유',answer:'hold',options:[['steal','돈을 빼돌리려고'],['hold','잘못된 명단의 지급을 멈추려고']]}]
};
Object.entries(TESTIMONIES).forEach(([id,t])=>CHAPTER_CASE.talk[t.who].push({id,q:t.q,a:t.a}));
const CHAT={
 karo:[line('daram','숟가락이 몇 개예요?'),line('karo','필요한 만큼입니다.',0),line('daram','그게 몇 개인데요?',3,{actor:'daram'}),line('karo','…아직 필요한 만큼 모으진 못했습니다.',2)],
 mungchi:[line('daram','안경에 김이 서리면 어떻게 해요?'),line('mungchi','안경을 벗어요.',0),line('daram','그럼 앞이 안 보이잖아요.',4,{actor:'daram'}),line('mungchi','맞아요. 그래서 다시 써요.',1),line('daram','(굉장히 바쁜 안경이다.)',3,{actor:'daram',thought:true})]
};
