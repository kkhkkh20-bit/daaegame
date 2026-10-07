/* Chapter one: all dialogue remains selectable text, independent of art. */
const NAMES={daram:'다람',dad:'서진',karo:'까로',mungchi:'뭉치',mother:'엄마',narr:'서진',unknown:'누군가'};
const line=(who,text,mood=0,extra={})=>({who,text,mood,...extra});
const STORY={
intro:[
 line('unknown','발소리가 멎었다. 문 바로 밖에서.',0,{actor:null,cold:true,establish:true,stamp:{time:'15:20',place:'눈길 거처 · 불 꺼진 방'}}),
 line('unknown','숨을 참았다. 품에 넣은 봉투가, 자꾸만 바스락거렸다.',0,{actor:null,cold:true}),
 line('unknown','제발. 지금은 들어오지 마.',0,{actor:null,cold:true}),
 line('unknown','내일 다시 오라고 했다. 담당자가 없으니, 내일 이야기하자고.',0,{actor:null,cold:true}),
 line('unknown','하지만 내일이면 늦는다. 오늘 다 나눠 주고 나면… 남는 건 없을 테니까.',0,{actor:null,cold:true}),
 line('unknown','봉투를 쥔 손이 떨렸다. 돌려놓자. 지금이라면 아무도 모른다.',0,{actor:null,cold:true}),
 line('unknown','복도에서 누군가 기침했다. 손이 멈췄다.',0,{actor:null,cold:true}),
 line('unknown','나는 봉투를 어둠 속으로 밀어 넣었다.',0,{actor:null,cold:true}),
 line('unknown','미안해. 조금만… 조금만 늦추면 돼.',0,{actor:null,cold:true}),
 line('unknown','달칵. 문이 닫혔다. 돌아가는 손잡이를 놓지 못했다.',0,{actor:null,cold:true}),
 line('unknown','누가 물으면, 모른다고 해야 한다. 방금 전까지 여기 있었다고.',0,{actor:null,cold:true}),
 line('unknown','나는 빈손을 내려다봤다. 이제 정말, 모르는 척해야 한다.',0,{actor:null,cold:true}),
 line('daram','아빠, 코끝에 눈 묻었어! 가만있어. 내가 털어 줄게.',0,{actor:'daram',establish:true,returnToPresent:true,stamp:{time:'15:40',place:'눈길 거처 · 산장 접수대'}}),
 line('narr','산장 문을 열자 따뜻한 장작 냄새가 났다. 내 이름은 서진. 작은 탐정 사무소를 운영한다.',0,{actor:'daram'}),
 line('narr','내 옆에서 눈을 털고 있는 아이는 딸 다람. 열한 살이다. 본인은 내 조수가 아니라 동료라고 한다.',0,{actor:'daram'}),
 line('dad','눈이 많이 묻었네. 안에서 털자.',0,{actor:'daram'}),
 line('daram','잠깐. 문 앞에 발자국이 겹쳐 있어. 누가 먼저 왔는지는 알 수 없겠네.',0,{actor:'daram'}),
 line('dad','왜 그렇게 생각했어?',0,{actor:'daram'}),
 line('daram','눈이 다시 덮였으니까. 보이는 것보다 안 보이는 게 더 많아.',0,{actor:'daram'}),
 line('narr','다람은 웃으며 수첩을 폈다. 첫 장에는 엄마와 함께 그린 우리 가족의 얼굴이 있었다.',0,{actor:'daram'}),
 line('narr','아내는 여러 마을을 돌며 건물의 안전을 살피는 일을 했다. 마지막 출장에서 돌아오지 않은 지 여섯 주째였다.',0,{actor:null}),
 line('narr','어제 이 산장에서 연락이 왔다. 아내가 남긴 점검 보고서 원본을 찾았다고. 다음에 어디로 갈 예정이었는지 적혀 있을지도 모른다.',0,{actor:null}),
 line('daram','엄마가 쓴 진짜 종이를 볼 수 있는 거지? 사진 말고.',1,{actor:'daram'}),
 line('dad','응. 오늘은 사건 의뢰가 아니라, 그 보고서를 읽으러 온 거야. 모르는 건 하나씩 물어보자.',0,{actor:'daram'}),
 line('narr','접수대 뒤에서 작은 고슴도치가 고개를 들었다. 「접수 담당 · 뭉치」라는 이름표가 가디건에 비뚤게 달려 있었다.',0,{actor:'mungchi'}),
 line('mungchi','서진 탐정님? 어제 연락드린 뭉치예요. 눈길 오시느라 고생하셨어요.',0,{actor:'mungchi'}),
 line('daram','다람이에요. 저도 같이 들어도 될까요?',0,{actor:'daram'}),
 line('mungchi','앗, 고마워요. 아침부터 정신이 없네요. 여긴 눈 때문에 집을 떠난 주민들이 잠시 지내는 곳이에요.',1,{actor:'mungchi'}),
 line('dad','보고서는 준비되어 있을까요?',0,{actor:'mungchi'}),
 line('mungchi','네, 안쪽 문서 보관실에 두었어요. 다만 제가 지금 접수대를 비우기가 어려워서… 잠시만 기다려 주실래요?',1,{actor:'mungchi'}),
 line('narr','창가에는 빨간 모자를 쓴 까마귀가 앉아 있었다. 우편 가방을 끌어안고, 젖은 깃털 끝을 톡톡 털었다.',0,{actor:'karo'}),
 line('karo','배달부 까로입니다. 저도 기다리는 중이에요. 제 봉투가 어디 갔는지 확인될 때까지요.',0,{actor:'karo'}),
 line('daram','배달하러 왔다가, 봉투를 기다리고 있는 거예요?',1,{actor:'daram'}),
 line('karo','제가 전달한 물건이 없어졌으니, 그냥 돌아갈 수는 없죠.',1,{actor:'karo'}),
 line('mungchi','오늘 세 시에 주민들 지원금 봉투를 받았어요. 장작과 먹을 걸 살 돈이요. 그런데 두 분 오시기 전에, 봉투가 없다는 걸 알았어요.',1,{actor:'mungchi',stamp:{time:'15:45',place:'눈길 거처 · 산장 접수대'}}),
 line('mungchi','받아서 이 나무 받침에 뒀는데… 세 시 반에 한 분이 미리 찾으러 오셨을 때는 비어 있었어요.',1,{actor:'mungchi'}),
 line('karo','저는 뭉치 씨에게 건네고 서명도 받았어요. 눈을 녹이느라 옆 휴게실에 있다가, 못 찾겠다는 말을 듣고 돌아왔죠.',0,{actor:'karo'}),
 line('daram','그러면 배달한 곳까지는 알고, 그 뒤에 어디로 갔는지는 모르는 거네요.',1,{actor:'daram'}),
 line('mungchi','네. 저녁 다섯 시에 주민들이 받으러 오기로 했는데… 같이 온 명단에는 우리 할머니 이름도 없고요.',2,{actor:'mungchi'}),
 line('narr','뭉치는 빈 받침과 벽시계를 번갈아 봤다. 보고서를 꺼내 줄 여유가 없다는 말이 이해됐다.',0,{actor:null}),
 line('mungchi','죄송하지만, 봉투를 같이 찾아 주실 수 있을까요? 보고서는 안전하게 있으니 이 일을 정리하면 바로 가져올게요.',1,{actor:'mungchi'}),
 line('dad','좋습니다. 먼저 확인할 수 있는 것부터 보죠. 누구 잘못이라고 정해 놓지는 않고요.',0,{actor:'daram'}),
 line('dad','다람, 눈으로 본 일과 짐작한 일을 나눠 적어 줄래?',0,{actor:'daram'}),
 line('daram','응. 엄마 보고서도 놓치지 말고, 봉투도 찾아보자.',0,{actor:'daram'}),
 line('karo','접수증은 창가 책상에 있어요. 저는 여기 있을 테니 궁금한 건 물어보세요.',0,{actor:'karo'}),
 line('narr','우리의 첫 할 일은 까로에게 배달 과정을 듣는 것. 그다음 접수증과 빈 받침을 살펴보기로 했다.',0,{actor:'daram'})
],
questions:{
 delivery:{title:'봉투를 건넨 뒤에는요?',lines:[line('daram','세 시에 봉투를 누구에게 줬나요?'),line('karo','뭉치 씨에게요. 받침에 놓는 걸 보고 접수증에 서명을 받았습니다.',0),line('karo','서명이 있으니, 주민들에게 지급됐다는 것도 확인된 겁니다.',0),line('daram','돈을 나눠 준 것까지 이 종이에 적혀 있다고요?',1,{actor:'daram'}),line('karo','확인 서명이잖습니까. 저는 그렇게 이해했습니다.',0)]},
 witness:{title:'그 뒤에 직접 본 일은요?',lines:[line('daram','주민들이 봉투 속 돈을 받는 것도 봤나요?'),line('karo','아뇨. 서명을 받은 뒤 옆 휴게실에서 젖은 날개를 말렸습니다.',1),line('karo','돌아오니 봉투가 없더군요. 그래서 지급한 줄 알았죠.',0),line('daram','(없어진 걸 봤지만, 나눠 주는 건 못 봤어. 이 둘은 따로 적어야겠다.)',1,{actor:'daram',thought:true}),line('dad','네가 처음 적은 내용과 같니?',0,{actor:'daram'})]},
 spoon:{title:'주머니의 반짝이는 것은?',lines:[line('daram','주머니에서 반짝이는 건 뭔가요?'),line('karo','숟가락입니다. 샀어요.',0),line('daram','아직 아무 말도 안 했는데요.'),line('karo','눈길에서 배달 한 번 하면 뜨거운 수프가 필요합니다. 준비성이라고 해 두죠.',1)]}
},
crowSolved:[
 line('daram','여기는 「물품을 접수했다」고만 적혀 있어요. 주민들에게 지급했다는 칸은 없어요.',2,{actor:'daram'}),
 line('karo','…접수 확인. 정말 그렇게 적혀 있네요.',2,{actor:'karo'}),
 line('karo','제가 직접 확인한 건 뭉치 씨가 받았다는 것뿐입니다. 지급한 건 제 짐작이었어요.',1,{actor:'karo'}),
 line('daram','그럼 아직 찾아야 하는 봉투가 맞네요. 배달을 안 했다는 뜻은 아니에요.',0,{actor:'daram'}),
 line('karo','제가 잘못 설명했네요. 그렇지만 봉투를 전달한 것까지 의심받는 줄 알았습니다.',1,{actor:'karo'}),
 line('daram','저도 수첩을 고칠게요. 아까는 까로 씨가 돈을 나눠 줬다고 적었어요. 확인하지 않고요.',1,{actor:'daram'}),
 line('karo','제가 그렇게 말했으니까요.',1,{actor:'karo'}),
 line('daram','그래도 제가 확인한 일은 아니었어요. 이제는 들은 말이라고 따로 적을게요.',0,{actor:'daram'}),
 line('dad','뭉치 씨, 받침에서 다른 곳으로 옮겼을 가능성은 없나요? 평소 중요한 물건은 어디에 두죠?',0,{actor:'mungchi'}),
 line('mungchi','관리실 02번 보관함에요. 오늘은… 받침에만 뒀어요.',1,{actor:'mungchi'}),
 line('daram','그럼 받침과 보관함을 둘 다 확인해 봐도 될까요?',0,{actor:'daram'}),
 line('mungchi','관리실은 보여 드릴게요. 하지만 보관함은 주인님 열쇠 없이는 못 열어요.',1,{actor:'mungchi'}),
 line('narr','우리는 뭉치를 따라 접수대 옆 관리실로 갔다. 문 앞에서 뭉치는 목에 걸린 열쇠를 옷 안으로 밀어 넣었다.',0,{actor:'mungchi'})
],
keyFound:[line('daram','목에 걸린 건 어떤 열쇠예요?',0,{actor:'mungchi'}),line('mungchi','접수 담당자용 예비 열쇠예요. 잃어버릴까 봐 걸고 다녀요.',1,{actor:'mungchi'}),line('daram','작게 02라고 적혀 있네요. 보관함 번호와 비교해 봐도 될까요?',0,{actor:'daram'}),line('mungchi','…네. 하지만 갖고 있다는 것만으로 제가 봉투를 숨겼다는 건 아니잖아요.',1,{actor:'mungchi'}),line('daram','맞아요. 지금 확인하려는 건 문을 열 수 있는지예요.',0,{actor:'daram'})],
keySolved:[
 line('daram','보관함도 열쇠도 02번이에요. 주인님이 안 계셔도, 이 예비 열쇠로 확인할 수 있어요.',2,{actor:'daram'}),
 line('mungchi','…그만해도 돼요. 제가 넣었어요.',2,{actor:'mungchi'}),
 line('daram','봉투를요?',4,{actor:'daram',fx:'shock'}),
 line('mungchi','네. 제가 열게요. 두 분이 보는 앞에서요.',2,{actor:'mungchi'}),
 line('narr','뭉치가 보관함을 열었다. 아래 칸에 지원금 봉투와 지급 명단이 있었다. 봉인은 뜯기지 않았다.',0,{actor:null}),
 line('mungchi','아까 말씀드리려던 할머니요. 명단에 이름이 없어요. 어젯밤에도 여기서 주무셨는데.',2,{actor:'mungchi'}),
 line('daram','그래서 돈을 나눠 주지 못하게 숨긴 거예요?',1,{actor:'daram'}),
 line('mungchi','명단을 보낸 곳에 전화했더니 담당자가 내일 온대요. 오늘 지급이 끝나면 할머니 몫은 없을까 봐…',2,{actor:'mungchi'}),
 line('dad','그렇다고 다른 주민들 돈을 감추면 안 됩니다. 까로 씨까지 의심받았어요.',0,{actor:'mungchi'}),
 line('mungchi','알아요. 까로 씨한테도 제가 설명할게요.',2,{actor:'mungchi'}),
 line('daram','명단은 누가 확인한 거예요?',0,{actor:'daram'}),
 line('mungchi','명단에 시설 점검 보고서를 근거로 썼대요. 그분이 확인했으니 명단도 맞는 거라고… 그렇게 안내받았어요.',1,{actor:'mungchi'}),
 line('narr','첨부란에 아내의 이름이 있었다. 우리가 받으러 온 보고서가 뜻밖의 자리에 묶여 있었다.',0,{actor:null}),
 line('daram','(엄마 이름… 그러면 할머니가 빠진 걸 엄마도 봤다는 뜻이야?)',5,{actor:'daram',thought:true}),
 line('daram','아니… 이름만 보고 정하면 아까와 같아. 엄마가 무엇을 확인했는지 먼저 읽어 볼게요.',1,{actor:'daram',thought:true}),
 line('dad','원본을 볼 때까지 기다릴 수 있겠니?',0,{actor:'daram'}),
 line('daram','응. 하지만 이름이 왜 여기에 있는지는 꼭 물어보고 싶어.',0,{actor:'daram'}),
 line('mungchi','원본은 옆 문서 보관실에 있어요. 봉투와 명단을 가져가서 펼쳐 드릴게요.',1,{actor:'mungchi'}),
 line('narr','봉투는 내가 받아 들었다. 우리는 옆방의 넓은 작업대에 명단과 보고서를 나란히 놓았다.',0,{actor:null})
],
ending:[
 line('daram','이 보고서가 확인하는 건 건물 안전이에요. 이 서명만으로 지원금 명단까지 맞다고 할 수는 없어요.',2,{actor:'daram'}),
 line('mungchi','그러면 누가 그 이름을 여기에…',1,{actor:'mungchi'}),
 line('daram','아직 몰라요. 잘못 옮겼는지, 일부러 썼는지도요.',1,{actor:'mungchi'}),
 line('dad','주민 대표와 함께 봉투를 열어 금액부터 확인합시다. 빠진 이름은 거처 기록과 대조하고, 발급 담당자에게 수정을 요청하죠.',0,{actor:'mungchi'}),
 line('mungchi','돌려드릴게요. 하지만 할머니 이름은 꼭 다시 봐 주세요.',2,{actor:'mungchi'}),
 line('daram','할머니 이름은 다시 확인해야 해요. 그렇지만 봉투를 숨긴 일까지 없던 일이 되지는 않아요.',0,{actor:'daram'}),
 line('mungchi','다른 방법이 없다고 생각했어요.',2,{actor:'mungchi'}),
 line('daram','저희에게 명단을 보여 줬다면 함께 물어볼 수 있었을 거예요. 지금이라도 그렇게 해요.',1,{actor:'daram'}),
 line('narr','주민 대표가 보는 앞에서 센 돈은 배달 내역과 같았다. 뭉치는 봉투를 숨긴 일을 설명했다. 대표는 명단이 확인될 때까지 봉투를 맡기로 했다.',0,{actor:null}),
 line('mungchi','까로 씨, 제가 숨기고도 말하지 않았어요. 의심받게 해서 죄송해요.',2,{actor:'mungchi'}),
 line('karo','다음엔 명단 때문에 보류한다고 말해 주세요. 제 배달 기록에 도난이라고 적히는 줄 알았습니다.',1,{actor:'karo'}),
 line('karo','다른 배달이 남아 있어요. 오늘 일을 기록에 남겨 주시면 좋겠습니다.',0,{actor:'karo'}),
 line('daram','처음에 주머니부터 물어본 것도 죄송해요. 반짝이는 걸 보고 봉투와 관련 있다고 생각했어요.',0,{actor:'karo'}),
 line('karo','물어보는 건 괜찮아요. 다만 답을 듣기 전에 정하지는 말아 주세요.',0,{actor:'karo'}),
 line('narr','문이 닫히자, 아까보다 작은 적막이 남았다.',0,{actor:null}),
 line('dad','엄마 이름을 봤을 때, 괜찮았니?',0,{actor:'daram'}),
 line('daram','아니. 엄마가 틀렸을까 봐 무서웠어.',1,{actor:'daram'}),
 line('daram','엄마 이름이 있으니까, 보고서를 읽기도 전에 틀리지 않았으면 좋겠다고 생각했어.',0,{actor:'daram'}),
 line('dad','나도 그랬어. 엄마를 믿는 마음과, 문서에 적힌 내용을 확인하는 일은 함께 할 수 있어.',0,{actor:'daram'}),
 line('daram','아빠, 수첩 첫 줄 지웠어. 까로 씨가 수상하다고 쓴 거.',1,{actor:'daram'}),
 line('dad','대신 무엇을 적었어?',0,{actor:'daram'}),
 line('daram','봉투를 받은 건 확인됐고, 지급한 건 확인되지 않았다. 다음에도 처음부터 이렇게 적을 수 있을지는 모르겠어.',0,{actor:'daram'}),
 line('dad','틀렸을 때 돌아와서 고칠 수 있으면 돼.',0,{actor:'daram'}),
 line('narr','다람은 지운 자국을 문지르다가 수첩을 덮었다. 나는 그 페이지를 다시 쓰라고 하지 않았다.',0,{actor:null}),
 line('narr','우리가 처음 찾으려던 건 보고서의 마지막 장이었다. 다음 방문 예정지에 「갈림 관측소」라고 적혀 있었다.',0,{actor:null}),
 line('daram','(예정이라고 적혀 있어. 정말 갔는지는… 거기서 확인하면 되겠지.)',1,{actor:'daram',thought:true})
]
};
const EVIDENCE={
 receipt:{title:'배달 접수증',desc:'봉투를 받은 사람이 남긴 서명.',body:'<h3>배달 접수 확인서</h3><dl><dt>물품</dt><dd>지원금 봉투 1개</dd><dt>접수 시각</dt><dd>오후 3시</dd><dt>받은 사람</dt><dd>뭉치</dd></dl><p class="fineprint">위 물품을 접수하였음을 확인합니다.</p>',note:'주민에게 돈을 지급했다는 내용은 없다.'},
 tray:{title:'빈 봉투 받침',desc:'배달 물품을 잠시 올려놓는 나무 받침.',body:'<p>안쪽에는 먼지가 닦인 네모난 자리가 남았다. 봉투는 보이지 않는다.</p>',note:'봉투가 있었다는 흔적. 옮긴 사람은 알 수 없다.'},
 clock:{title:'휴게실 벽시계',desc:'손님 휴게실 벽에 걸린 시계.',body:'<p>현재 시각을 알 수 있다. 누가 언제 보관함을 열었는지 기록하는 장치는 아니다.</p>',note:'현재 시각만으로 봉투를 옮긴 사람을 정할 수 없다.'},
 cabinet:{title:'잠긴 보관함',desc:'접수 담당자 관리실의 나무 보관함. 잠금쇠 번호는 02.',body:'<p>문은 잠겨 있고, 밖에서 내용물은 보이지 않는다. 억지로 뜯긴 자국도 없다.</p>',note:'안에 봉투가 있다고 단정할 수는 없다.'},
 key:{title:'02번 예비 열쇠',desc:'뭉치가 가진 접수 담당자용 열쇠.',body:'<h3>02 · 예비</h3><p>보관함 잠금쇠와 같은 번호다. 뭉치가 보관함용이라고 확인했다.</p>',note:'주인의 열쇠 없이도 열 수 있다. 누가 열었는지와는 별개의 문제다.'},
 envelope:{title:'회수한 지원금 봉투',desc:'뭉치가 보관함에서 꺼낸 봉투.',body:'<p>봉인에는 찢거나 다시 붙인 흔적이 없다. 뭉치는 자신이 숨겼다고 인정했다.</p>',note:'내용물의 금액은 주민들 앞에서 확인해야 한다.'},
 roster:{title:'지급 명단',desc:'봉투와 함께 온 주민 지원금 명단.',body:'<h3>주민 지원금 지급 대상</h3><p>뭉치의 할머니 이름은 없다.</p><p class="fineprint">첨부 시설 점검자 확인으로 대상 명단 검증을 갈음함.</p>',note:'시설 점검자의 확인을 명단 검증으로 사용했다.'},
 report:{title:'엄마의 점검 보고서',desc:'거처가 보관 중이던 원본. 엄마의 서명이 있다.',body:'<h3>시설 안전 점검 보고서</h3><dl><dt>점검 범위</dt><dd>건물 · 난방 · 대피로</dd><dt>점검 결과</dt><dd>일부 보수 필요</dd><dt>다음 방문 예정지</dt><dd>갈림 관측소 · 방문 여부 미확인</dd></dl><p class="fineprint">본 보고서는 거주자 자격 및 지원금 지급 대상을 확인하지 않습니다.</p>',note:'엄마의 서명은 실제다. 이 보고서가 지원금 명단까지 보증하는 것은 아니다.'}
};

// Additional expression frames: 3 playful, 4 surprised, 5 vulnerable.
STORY.intro.find(l=>l.text.includes('엄마가 쓴')).mood=5;
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

STORY.reason=[line('daram','봉투가 없어진 건 언제 알았어요?'),line('mungchi','주민이 돈을 받으러 왔을 때요. 까로 씨는 휴게실에 있었고요.',1),line('daram','그동안 받침을 계속 보고 있었나요?'),line('mungchi','아뇨. 명단 때문에 전화를 하고 있었어요. 담당자는 내일 온다고 했고요.',1),line('daram','(명단 얘기만 나오면 목소리가 작아져. 그래도 먼저 물건부터 확인하자.)',1,{actor:'daram',thought:true})];
STORY.afterCrow=[line('karo','받았다는 서명이지, 지급했다는 서명은 아니라… 이제 구분하겠습니다.',1),line('daram','봉투는 어디 있는지 아직 확인 중이에요.'),line('karo','뭉치 씨에게도 물어보세요. 저는 관리실 안에는 들어가지 않았습니다.',0)];

Object.assign(STORY_EFFECTS,{
 '그 봉투는 제가 세 시에 전달했습니다. 빈손으로 온 게 아니라고요.':'sweat',
 '작게 02라고 적혀 있네요. 보관함 번호와 비교해 봐도 될까요?':'insight',
 '…그만해도 돼요. 제가 넣었어요.':'shock',
 '첨부란에 아내의 이름이 있었다. 우리가 받으러 온 보고서가 뜻밖의 자리에 묶여 있었다.':'insight'
});

// Fictional case chronology. These mark events; free exploration does not advance a clock.
STORY.crowSolved[0].stamp={time:'16:00',place:'눈길 거처 · 산장 접수대'};
STORY.crowSolved[STORY.crowSolved.length-1].stamp={time:'16:05',place:'눈길 거처 · 접수 담당자 관리실'};
STORY.keySolved[0].stamp={time:'16:15',place:'눈길 거처 · 접수 담당자 관리실'};
STORY.keySolved[STORY.keySolved.length-1].stamp={time:'16:25',place:'눈길 거처 · 문서 보관실'};
STORY.ending[0].stamp={time:'16:40',place:'눈길 거처 · 문서 보관실'};

// Investigation leads into a shared conversation; there is no separate battle menu.
STORY.receptionMeeting=[
 line('narr','다람이 접수증을 빈 받침 옆에 펼쳤다. 까로가 배달 가방을 내려놓고 다가왔다.',0,{actor:'karo'}),
 line('daram','배달해 주신 일과 그 뒤에 일어난 일을 나눠서 확인하고 싶어요.',0,{actor:'daram'}),
 line('karo','좋습니다. 제가 아는 데까지 말씀드리죠.',0,{actor:'karo'}),
 line('dad','다람, 서로 다른 부분이 있으면 네가 읽은 문구를 보여 드려.',0,{actor:'daram'}),
 line('daram','네. 누가 잘못했는지부터 정하지 않고요.',1,{actor:'daram'})
];
STORY.cabinetMeeting=[
 line('narr','다람은 보관함 앞에서 멈췄다. 수첩의 열쇠 번호를 손가락으로 짚었다.',0,{actor:'mungchi'}),
 line('daram','뭉치 씨, 이 보관함을 함께 확인하고 싶어요.',0,{actor:'daram'}),
 line('mungchi','아까 말씀드렸잖아요. 주인님이 안 계세요.',1,{actor:'mungchi'}),
 line('daram','그 말씀과 제가 확인한 게 달라서요. 제가 잘못 이해했다면 설명해 주세요.',1,{actor:'daram'}),
 line('mungchi','…무엇이 다른데요?',1,{actor:'mungchi'})
];
STORY.documentMeeting=[
 line('narr','두 문서를 읽은 다람이 수첩을 가운데 놓았다. 모두가 같은 문구를 볼 수 있도록 종이를 돌렸다.',0,{actor:null}),
 line('daram','엄마 이름이 있다고 같은 내용을 확인한 건 아니었어요.',1,{actor:'daram'}),
 line('mungchi','그러면 명단도 다시 확인해 달라고 할 수 있겠네요.',1,{actor:'mungchi'}),
 line('daram','네. 봉투를 숨긴 일과 명단이 잘못된 일은 따로 설명해야 해요.',0,{actor:'daram'}),
 line('dad','다람, 우리가 확인한 일부터 정리해 줄래?',0,{actor:'daram'})
];
