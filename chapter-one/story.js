/* Chapter one: all dialogue remains selectable text, independent of art. */
const NAMES={daram:'다람',dad:'다온',karo:'까로',mungchi:'뭉치',mother:'엄마',narr:'다온'};
const line=(who,text,mood=0,extra={})=>({who,text,mood,...extra});
const STORY={
intro:[
 line('narr','눈이 길을 지운 오후. 다람은 아빠보다 한 걸음 먼저 거처의 문을 열었다.',0,{actor:null,establish:true}),
 line('daram','여기가 엄마가 마지막으로 점검한 곳이지?',1,{actor:'daram'}),
 line('dad','마지막으로 확인된 곳. 아직 그 뒤의 일은 몰라.',0,{actor:'daram'}),
 line('daram','…응. 마지막이라고 정해 버리면 안 되지.',1,{actor:'daram'}),
 line('narr','엄마가 돌아오지 않은 지 여섯 주. 오늘은 거처에 남은 점검 보고서를 보러 왔다.',0,{actor:null}),
 line('dad','힘들면 오늘은 내가 보고 와도 돼.',0,{actor:'daram'}),
 line('daram','나도 볼래. 기다리면서 상상만 하는 건 더 무서워.',0,{actor:'daram'}),
 line('daram','엄마처럼 뭐든 알아내고 싶은 건 아니야. 모르는 걸 확인하는 사람이 되고 싶어.',0,{actor:'daram'}),
 line('dad','그럼 같이 확인하자. 내 짐작도 틀릴 수 있으니까.',0,{actor:'daram'}),
 line('narr','안쪽에서 목소리가 높아졌다.',0,{actor:null}),
 line('karo','봉투는 전달했습니다. 눈길을 또 걸으라면 추가 요금입니다.',1,{actor:'karo'}),
 line('mungchi','추가 배달이 아니라… 봉투가 없어졌다고요.',1,{actor:'mungchi'}),
 line('narr','접수대의 나무 받침은 비어 있었다. 주민들에게 줄 지원금 봉투라고 했다.',0,{actor:null}),
 line('dad','문부터 막으면 안 되지. 배달부에게 무슨 일이 있었는지 물어보자.',0,{actor:'karo'}),
 line('daram','제가 적을게요. 직접 본 것부터 말씀해 주세요.',0,{actor:'karo'}),
 line('karo','좋습니다. 제 결백과 근무 시간을 동시에 지켜 주시죠.',0,{actor:'karo'})
],
questions:{
 delivery:{title:'봉투를 누구에게 줬나요?',lines:[line('daram','봉투를 누구에게 줬나요?'),line('karo','세 시에 뭉치에게요. 서명까지 받았습니다.',0),line('karo','접수도 끝났고, 주민 지급도 끝났겠죠.',0),line('daram','주민 지급까지요?',1),line('karo','서명이 있잖아요. 서류는 사람보다 덜 변덕스럽죠.',0)]},
 witness:{title:'주민들이 받는 것도 봤나요?',lines:[line('daram','돈을 나눠 주는 것도 직접 봤어요?'),line('karo','그건 못 봤죠. 여기서 젖은 날개를 말렸습니다.',1),line('daram','(본 일과 생각한 일이 섞여 있어.)',1,{thought:true})]},
 spoon:{title:'주머니에서 반짝이는 건…',lines:[line('daram','주머니에서 반짝이는 건 뭔가요?'),line('karo','숟가락입니다. 샀어요.',0),line('daram','아직 아무 말도 안 했는데요.'),line('karo','미리 말씀드리는 겁니다. 반짝임은 죄가 아니니까.',1)]}
},
crowSolved:[
 line('daram','이 서명은 봉투를 받았다는 확인이에요. 돈을 나눠 줬다는 확인은 아니고요.',2,{actor:'daram'}),
 line('karo','…접수 확인. 정말 그렇게 적혀 있네요.',2,{actor:'karo'}),
 line('karo','제가 본 건 뭉치가 받는 데까지입니다. 그 뒤는 짐작했어요.',1,{actor:'karo'}),
 line('daram','그럼 짐작은 빼고 적을게요.',0,{actor:'karo'}),
 line('karo','제 숟가락 이야기도 빼 주시면 좋겠습니다.',0,{actor:'karo'}),
 line('daram','(말이 틀렸다고 범인인 건 아니야. 이제 받은 사람에게 물어보자.)',1,{actor:'daram',thought:true}),
 line('mungchi','제가 받았어요. 잠깐 받침에 뒀는데… 없어졌어요.',1,{actor:'mungchi'}),
 line('daram','접수대 뒤 보관함도 확인할 수 있을까요?',0,{actor:'mungchi'}),
 line('mungchi','거긴 잠겨 있어요. 주인님 열쇠 없이는 못 열어요.',0,{actor:'mungchi'}),
 line('narr','뭉치는 말하면서 목에 걸린 열쇠를 움켜쥐었다.',0,{actor:'mungchi'})
],
keyFound:[line('daram','목에 건 열쇠는 어디에 쓰는 거예요?',0,{actor:'mungchi'}),line('mungchi','아, 이건… 예비 열쇠예요. 접수 담당자가 갖고 있어요.',1,{actor:'mungchi'}),line('daram','보관함의 번호와 같네요.',0,{actor:'mungchi'}),line('mungchi','열쇠를 갖고 있다고 제가 숨긴 건 아니잖아요.',1,{actor:'mungchi'}),line('daram','맞아요. 그래서 안을 확인하고 싶어요.',0,{actor:'mungchi'})],
keySolved:[line('daram','주인님 열쇠가 없어도 열 수 있어요. 그 예비 열쇠로요.',2,{actor:'daram'}),line('mungchi','…네.',1,{actor:'mungchi'}),line('daram','열쇠만으로 누가 숨겼는지는 몰라요. 같이 열어 봐도 될까요?',0,{actor:'mungchi'}),line('mungchi','제가 열게요.',2,{actor:'mungchi'}),line('narr','보관함 아래 칸에서 봉투가 나왔다. 봉인은 그대로였다.',0,{actor:null}),line('mungchi','제가 넣었어요. 돈은 건드리지 않았어요.',2,{actor:'mungchi'}),line('daram','왜요?',0,{actor:'mungchi'}),line('mungchi','함께 온 지급 명단에 할머니 이름이 없었어요.',2,{actor:'mungchi'}),line('mungchi','명단이 틀렸는데 지급부터 끝나면, 고쳐 달라는 말도 안 들어줄 것 같아서…',1,{actor:'mungchi'}),line('dad','그래서 다른 주민들 몫까지 숨겼구나.',0,{actor:'mungchi'}),line('mungchi','알아요. 그런데 가만히 기다리는 것도 무서웠어요.',2,{actor:'mungchi'}),line('narr','명단 아래에 익숙한 이름이 있었다. 다람의 엄마였다.',0,{actor:null}),line('mungchi','이 명단도 그분이 확인했다던데요. 다람 씨 어머니요.',1,{actor:'mungchi'}),line('daram','(엄마가 그랬을 리 없어. …아니. 그것도 내 짐작이야.)',1,{actor:'daram',thought:true}),line('dad','명단과 점검 보고서를 같이 보자. 이름만 보고 결론 내리지 말고.',0,{actor:'daram'})],
ending:[
 line('daram','엄마가 확인한 건 건물 안전이에요. 지원금 명단은 확인하지 않았어요.',2,{actor:'daram'}),
 line('mungchi','그러면 누가 그 이름을 여기에…',1,{actor:'mungchi'}),
 line('daram','아직 몰라요. 잘못 옮겼는지, 일부러 썼는지도요.',1,{actor:'mungchi'}),
 line('dad','명단은 다시 확인하도록 맡기자. 봉투도 주민들 앞에서 열고 금액을 세고.',0,{actor:'mungchi'}),
 line('mungchi','돌려드릴게요. 하지만 할머니 이름은 꼭 다시 봐 주세요.',2,{actor:'mungchi'}),
 line('daram','그것도 기록할게요. 봉투를 숨긴 일과 따로요.',0,{actor:'mungchi'}),
 line('narr','봉투 안의 금액은 배달 내역과 같았다. 지급은 명단을 다시 확인할 때까지 보류됐다.',0,{actor:null}),
 line('karo','이제 가도 되겠죠? 결백한 배달부도 저녁은 먹어야 합니다.',0,{actor:'karo'}),
 line('daram','숟가락이 있으니 준비는 끝났네요.',0,{actor:'karo'}),
 line('karo','봐요. 중요한 물건이라니까.',0,{actor:'karo'}),
 line('narr','문이 닫히자, 아까보다 작은 적막이 남았다.',0,{actor:null}),
 line('dad','엄마 이름을 봤을 때, 괜찮았니?',0,{actor:'daram'}),
 line('daram','아니. 엄마가 틀렸을까 봐 무서웠어.',1,{actor:'daram'}),
 line('daram','그래도… 무섭다고 덮어 두고 싶지는 않아.',0,{actor:'daram'}),
 line('dad','나도 그래. 같이 읽자.',0,{actor:'daram'}),
 line('narr','보고서 마지막 장에는 다음 점검 장소가 적혀 있었다. 「갈림 관측소」.',0,{actor:null}),
 line('daram','(엄마가 남긴 답이 아니라, 다음에 확인할 곳을 찾았다.)',1,{actor:'daram',thought:true})
]
};
const EVIDENCE={
 receipt:{title:'배달 접수증',desc:'봉투를 받은 사람이 남긴 서명.',body:'<h3>배달 접수 확인서</h3><dl><dt>물품</dt><dd>지원금 봉투 1개</dd><dt>접수 시각</dt><dd>오후 3시</dd><dt>받은 사람</dt><dd>뭉치</dd></dl><p class="fineprint">위 물품을 접수하였음을 확인합니다.</p>',note:'주민에게 돈을 지급했다는 내용은 없다.'},
 tray:{title:'빈 봉투 받침',desc:'배달 물품을 잠시 올려놓는 나무 받침.',body:'<p>안쪽에는 먼지가 닦인 네모난 자리가 남았다. 봉투는 보이지 않는다.</p>',note:'봉투가 있었다는 흔적. 옮긴 사람은 알 수 없다.'},
 clock:{title:'접수대 시계',desc:'접수대에서 보이는 벽시계.',body:'<p>현재 시각을 알 수 있다. 누가 언제 보관함을 열었는지 기록하는 장치는 아니다.</p>',note:'현재 시각만으로 봉투를 옮긴 사람을 정할 수 없다.'},
 cabinet:{title:'잠긴 보관함',desc:'접수대 뒤의 나무 보관함. 잠금쇠 번호는 02.',body:'<p>문은 잠겨 있고, 밖에서 내용물은 보이지 않는다. 억지로 뜯긴 자국도 없다.</p>',note:'안에 봉투가 있다고 단정할 수는 없다.'},
 key:{title:'02번 예비 열쇠',desc:'뭉치가 가진 접수 담당자용 열쇠.',body:'<h3>02 · 예비</h3><p>보관함 잠금쇠와 같은 번호다. 뭉치가 보관함용이라고 확인했다.</p>',note:'주인의 열쇠 없이도 열 수 있다. 누가 열었는지와는 별개의 문제다.'},
 envelope:{title:'회수한 지원금 봉투',desc:'뭉치가 보관함에서 꺼낸 봉투.',body:'<p>봉인에는 찢거나 다시 붙인 흔적이 없다. 뭉치는 자신이 숨겼다고 인정했다.</p>',note:'내용물의 금액은 주민들 앞에서 확인해야 한다.'},
 roster:{title:'지급 명단',desc:'봉투와 함께 온 주민 지원금 명단.',body:'<h3>주민 지원금 지급 대상</h3><p>뭉치의 할머니 이름은 없다.</p><p class="fineprint">첨부 시설 점검자 확인으로 대상 명단 검증을 갈음함.</p>',note:'시설 점검자의 확인을 명단 검증으로 사용했다.'},
 report:{title:'엄마의 점검 보고서',desc:'거처가 보관 중이던 원본. 엄마의 서명이 있다.',body:'<h3>시설 안전 점검 보고서</h3><dl><dt>점검 범위</dt><dd>건물 · 난방 · 대피로</dd><dt>점검 결과</dt><dd>일부 보수 필요</dd></dl><p class="fineprint">본 보고서는 거주자 자격 및 지원금 지급 대상을 확인하지 않습니다.</p>',note:'엄마의 서명은 실제다. 지원금 명단에 대한 보증은 아니다.'}
};

// Additional expression frames: 3 playful, 4 surprised, 5 vulnerable.
STORY.intro[6].mood=5;
STORY.questions.spoon.lines[2].mood=3;STORY.questions.spoon.lines[2].actor='daram';
STORY.keySolved.find(l=>l.thought).mood=5;
STORY.ending.filter(l=>l.who==='daram').forEach(l=>{if(l.text.includes('무서'))l.mood=5;else if(l.text.includes('숟가락')){l.mood=3;l.actor='daram';}});

// Explicit beats only; ordinary dialogue does not trigger random animations.
// Text lookup also applies to dialogue arrays in saves made before these cues.
const STORY_EFFECTS={
 '추가 배달이 아니라… 봉투가 없어졌다고요.':'shock',
 '주민 지급까지요?':'insight',
 '숟가락입니다. 샀어요.':'sweat',
 '아직 아무 말도 안 했는데요.':'tease',
 '…접수 확인. 정말 그렇게 적혀 있네요.':'shock',
 '제 숟가락 이야기도 빼 주시면 좋겠습니다.':'sweat',
 '뭉치는 말하면서 목에 걸린 열쇠를 움켜쥐었다.':'sweat',
 '아, 이건… 예비 열쇠예요. 접수 담당자가 갖고 있어요.':'sweat',
 '보관함의 번호와 같네요.':'insight'
};

// Father's narrative viewpoint; migrate the same lines in earlier saves too.
const FATHER_NARRATION={
 '눈이 길을 지운 오후. 다람은 아빠보다 한 걸음 먼저 거처의 문을 열었다.':'눈이 길을 지운 오후. 다람이 나보다 한 걸음 먼저 거처의 문을 열었다.',
 '엄마가 돌아오지 않은 지 여섯 주. 오늘은 거처에 남은 점검 보고서를 보러 왔다.':'아내가 돌아오지 않은 지 여섯 주. 다람과 함께 그녀가 남긴 점검 보고서를 찾으러 왔다.',
 '명단 아래에 익숙한 이름이 있었다. 다람의 엄마였다.':'명단 아래에 익숙한 이름이 있었다. 아내의 이름이었다.'
};

const FATHER_VIEW_TARGET={'문부터 막으면 안 되지. 배달부에게 무슨 일이 있었는지 물어보자.':'karo','그래서 다른 주민들 몫까지 숨겼구나.':'mungchi'};
