/* The original CASES / COMBO / BATTLE schema, adapted to this chapter. */
const PERSONAL={
 receipt:'까로 씨의 말을 그대로 적었다. 이 종이가 확인하는 범위를 다시 읽어야 한다.',
 tray:'비어 있다는 사실은 확인했다. 누가 옮겼는지는 아직 모른다.',
 clock:'시각을 아는 것과 그때 있었던 일을 아는 것은 다르다.',
 cabinet:'잠겨 있다는 이유만으로 아무도 열 수 없다고 생각하지 말자.',
 key:'열 수 있었다는 사실만으로 그 사람이 열었다고 정할 수는 없다.',
 envelope:'찾았다고 끝난 게 아니다. 내용물을 함께 확인해야 한다.',
 roster:'이름이 빠진 까닭을 확인해야 한다. 빠졌다는 사실만으로 자격이 없다고 할 수는 없다.',
 report:'엄마의 글씨다. 믿고 싶어서 먼저 결론을 내리지 않도록, 한 줄씩 읽자.'
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
COMBINATIONS.forEach(x=>EVIDENCE[x.id]={title:x.name,desc:x.text,body:'<p>'+x.text+'</p>',note:'두 단서가 이어져 확인한 사실.',memo:'따로 적어 둔 사실을 연결했다. 이 결론으로 알 수 없는 것도 남겨 두자.'});
Object.entries(EVIDENCE).forEach(([id,e])=>{e.memo=e.memo||PERSONAL[id]||'일단 적어 두기. 멋있는 탐정은 메모를 한다.';e.check=INSPECTIONS[id]&&{gate:true,label:INSPECTIONS[id].label,text:INSPECTIONS[id].text,desc2:INSPECTIONS[id].text};});
const TESTIMONIES={
 t_delivery:{who:'karo',q:'봉투를 누구에게?',a:'세 시에 뭉치에게 봉투를 건네고 서명을 받았습니다.'},
 t_paid:{who:'karo',q:'그 서명은 어떤 뜻?',a:'서명이 있으니, 주민들에게 지급됐다는 것도 확인된 겁니다.'},
 t_witness:{who:'karo',q:'직접 지급하는 걸 봤나요?',a:'지급하는 건 못 봤습니다. 휴게실에서 돌아와 봉투가 없는 걸 보고 지급한 줄 알았어요.'},
 t_spoon:{who:'karo',q:'주머니의 반짝이는 것은?',a:'숟가락입니다. 샀어요. 반짝임은 죄가 아니니까.'},
 t_key:{who:'mungchi',q:'목에 건 열쇠는?',a:'보관함 예비 열쇠예요. 접수 담당자가 갖고 있어요.'},
 t_reason:{who:'mungchi',q:'언제 없어진 걸 알았나요?',a:'주민이 돈을 받으러 왔을 때예요. 그 전에는 명단 때문에 전화를 하고 있었어요.'},
 confession:{who:'mungchi',q:'봉투를 왜 숨겼나요?',a:'할머니가 명단에서 빠졌는데, 지급이 끝나면 고칠 수 없을까 봐 숨겼어요.'}
};
const PEOPLE={
 daram:{name:'다람',role:'11살 다람쥐 · 견습 탐정',fact:'실종된 엄마의 보고서를 확인하러 왔다. 궁금한 건 못 참고, 겁이 나면 수첩부터 꼭 쥔다.',memo:'확인한 사실과 내 생각을 나눠 적기. 틀린 기록을 고치는 것도 내 몫이다.'},
 karo:{name:'까로',role:'까마귀 배달부',fact:'봉투를 가져왔다. 지급 장면은 직접 보지 못했다.',memo:'말을 확신한다고 직접 본 것은 아니었다. 나도 그 말을 너무 빨리 믿었다.'},
 mungchi:{name:'뭉치',role:'고슴도치 접수 담당자',fact:'봉투를 받은 접수 담당자. 함께 머무는 할머니와 지급 명단 때문에 마음을 쓰고 있다.',memo:'말하기 어려운 사정이 있어 보인다. 표정으로 결론을 정하지 말자.'},
 dad:{name:'서진',role:'다람의 아빠 · 탐정',fact:'다람과 함께 엄마의 행적을 확인한다.',memo:'아빠도 엄마를 걱정한다. 아빠가 괜찮다고 해도 내가 확인할 수 있는 것은 직접 확인하자.'}
};
const asEvidence=id=>({id,name:EVIDENCE[id].title,desc:EVIDENCE[id].desc,check:EVIDENCE[id].check});
const CHAPTER_CASE={id:'reception',lives:5,suspects:['karo','mungchi'],cast:PEOPLE,
 locations:[
  {id:'reception',name:'산장 접수대',pan:.5,spots:['receipt','tray'].map(id=>({ev:asEvidence(id)}))},
  {id:'lounge',name:'손님 휴게실',pan:.5,req:'door:reception-solved',spots:['clock'].map(id=>({ev:asEvidence(id)}))},
  {id:'cabinet',name:'접수 담당자 관리실',pan:.5,req:'door:reception-solved',spots:['cabinet','key'].map(id=>({ev:asEvidence(id)}))},
  {id:'archive',name:'문서 보관실',pan:.5,req:'door:archive',spots:['envelope','roster','report',...COMBINATIONS.map(x=>x.id)].map(id=>({ev:asEvidence(id)}))}
 ],talk:{karo:[],mungchi:[]},
 rounds:[
  {who:'karo',stm:[{t:'오후 세 시에 뭉치에게 봉투를 건넸습니다.',p:'제 앞에서 서명했어요.',a:[]},{t:'서명이 있으니, 주민들에게 지급됐다는 것도 확인된 겁니다.',p:'확인서니까 지급 확인이죠.',a:['receipt','cx_reception_0']}],hit:'제가 확인한 건 봉투를 받은 데까지네요.'},
  {who:'mungchi',stm:[{t:'봉투는 제가 받아서 접수대에 뒀어요.',p:'받은 건 맞아요.',a:[]},{t:'주인님 열쇠가 없으니 보관함은 아무도 못 열어요.',p:'주인님 열쇠는 없어요.',a:['key','cx_reception_1']}],hit:'제가 예비 열쇠로 열었어요.'}
 ],final:[{question:'봉투를 숨긴 사람',answer:'mungchi',options:[['karo','까로'],['mungchi','뭉치']]},{question:'숨긴 장소',answer:'cabinet',options:[['window','창가'],['cabinet','보관함']]},{question:'숨긴 이유',answer:'hold',options:[['steal','돈을 빼돌리려고'],['hold','잘못된 명단의 지급을 멈추려고']]}]
};
Object.entries(TESTIMONIES).forEach(([id,t])=>CHAPTER_CASE.talk[t.who].push({id,q:t.q,a:t.a}));
