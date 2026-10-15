'use strict';
const $=s=>document.querySelector(s),game=$('#game');
const artRoot='../../preview/room13-dev/game/assets/';
const zoomArt='../visual-gimmicks-02-20261015/assets/r13-gimmick-floor-open.webp';
const items=[
 {title:'엄마의 두 번째 쪽지',kind:'편지',source:'여관 2층 · 13호실',icon:'letter',description:'다람이 이름 옆에 작은 도토리가 그려져 있다.\n“아빠가 오면 이 종이를 보여 줘.”'},
 {title:'할머니의 초대 편지',kind:'편지',source:'여정에서 가지고 온 자료',icon:'letter',description:'받은 편지의 내용과 출처를 이곳에서 확인한다.\n이 시안에서는 자세한 본문을 생략했다.'},
 {title:'예약 원본',kind:'문서',source:'눈에 막힌 입구',icon:'note',description:'원본에 적힌 등록 내용을 다시 살펴볼 수 있다.\n추리 결론이나 다음 행동은 자동으로 표시하지 않는다.'},
 {title:'옮겨 쓴 명부',kind:'문서',source:'눈에 막힌 입구',icon:'note',description:'옮겨 적은 내용을 원본과 비교할 때 참고한다.\n이 시안은 비교 정답을 표시하지 않는다.'},
 {title:'주방 뒤로 이어진 그을음',kind:'관찰 기록',source:'여관 주방',icon:'map',description:'주방 뒷문 아래에서 벽 쪽으로 이어진 검은 자국.\n관찰한 위치와 내용을 다시 읽을 수 있다.'},
 {title:'광장 돌에 긁힌 이름들',kind:'탁본',source:'돌이 있는 광장',icon:'note',description:'긁어 지운 표면에서 떠낸 자국을 기록했다.\n구체적인 해석은 본편에서 확인한다.'}
];
const people=[{title:'까로',kind:'만난 사람',source:'눈에 막힌 입구',icon:'person',description:'마차를 함께 타고 온 동행.\n직접 이야기한 내용부터 수첩에 남긴다.'}];
const lines=[{who:'까로',text:'바퀴 축에 금이 갔어.\n우선 짐부터 내려야겠네.'},{who:'아빠',text:'다람아, 마차에서 조금 떨어져 있자.'},{who:'까로',text:'짐은 내가 살필게. 물어볼 게 있으면 말해.'}];
const daramLines=[{who:'다람이',text:'아빠, 여기서는 며칠 자고 가?'},{who:'아빠',text:'우선 오늘은 여기서 쉬자.'},{who:'다람이',text:'그럼 창밖을 조금 더 보고 있을게.'}];
const answers={damage:'축 상태부터 살펴봐야겠어. 짐을 실은 채로 움직이긴 어려워.',inn:'마을 안으로 들어가면 여관이 있어. 거기서 쉴 곳을 물어보자.',time:'지금은 장담 못 하겠어. 부품을 구할 수 있는지부터 봐야 해.'};
let view='field',zoomed=false,tab='items',selected=0,presenting=false,lineIndex=0,auto=false,autoTimer,toastTimer,statusTimer,lastFocus,history=[lines[0]],asked=new Set(),pendingFind=false,foundNote=false;
const remembered={items:0,testimony:0,people:0};
const testimony=[
 {title:'까로 · 마차의 상태',kind:'증언',source:'1일째 · 오후 · 눈에 막힌 입구',icon:'chat',author:'까로',portrait:'room13-pixel-main-profile-c.webp',quote:'바퀴 축에 금이 갔어.',description:'“바퀴 축에 금이 갔어.”\n까로에게 직접 들은 말.'},
 {title:'다람이 · 방을 둘러본 이야기',kind:'증언',source:'2일째 · 오전 · 13호실',icon:'chat',author:'다람이',portrait:'room13-pixel-family-profile-icons.webp',quote:'책도 있고, 창문 밖도 잘 보여.',description:'“책도 있고, 창문 밖도 잘 보여.”\n다람이와 방에서 나눈 이야기.'}
];
let presented=null,soundEnabled=true,audioContext;
function recordList(){return tab==='people'?people:tab==='testimony'?testimony:items}

let field='room',speakerId='karo',area='inn',worldOpened=false,arrivalSeen=false,arrivalTimer;
const daramAnswers={damage:'책도 있고, 창문 밖도 잘 보여. 아직 다 보진 못했어.',inn:'지붕에 눈이 잔뜩 쌓였더라. 우리 마차보다 높았어.',time:'조금만 더 아빠랑 이야기하고 싶어.'};
const fieldArt={room:artRoot+'room13-pixel-room-before-afternoon.webp',hall:artRoot+'room13-pixel-hall-before-afternoon.webp',inn:artRoot+'room13-pixel-panorama-inn-morning.webp',dining:artRoot+'room13-pixel-inn-morning.webp',square:artRoot+'room13-pixel-panorama-square-morning.webp',store:artRoot+'room13-pixel-ready-store0177-morning.webp',gate:artRoot+'room13-pixel-ready-gate0173-afternoon.webp',workshop:artRoot+'room13-pixel-panorama-workshop-morning.webp'};
const fieldNames={room:'여관 2층 · 13호실',hall:'여관 2층 · 복도',inn:'여관 · 접수대',dining:'여관 · 식당',square:'돌이 있는 광장',store:'잡화점',gate:'눈에 막힌 입구',workshop:'수리점'};

function icon(id){return '<svg aria-hidden="true"><use href="#i-'+id+'"/></svg>'}
function status(t){$('#status').textContent=t;$('#status').classList.add('show');clearTimeout(statusTimer);statusTimer=setTimeout(()=>$('#status').classList.remove('show'),2200)}
function stopAuto(){auto=false;clearInterval(autoTimer);$('#auto').setAttribute('aria-pressed','false');$('#auto span').textContent='OFF'}
function closeAll(){const finishRead=pendingFind&&!$('#records').hidden;pendingFind=false;for(const id of ['records','backlog','options-panel','move-panel','overlay','questions','question-shade'])$('#'+id).hidden=true;presenting=false;if(finishRead){foundNote=true;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,2600)}if(lastFocus&&lastFocus.isConnected)lastFocus.focus();else if(!$('#records').hidden)$('#close-record').focus()}
function renderView(){endPresentation();delete game.dataset.field;if(view==='field'){renderField();return}$('#resident').hidden=true;$('#desk-target').hidden=true;$('#arrival-note').hidden=true;closeAll();$('#status').classList.remove('show');stopAuto();$('#toast').hidden=true;document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));const talking=view==='talk';const daram=talking&&speakerId==='daram';$('#background').src=talking?(daram?fieldArt.room:artRoot+'room13-pixel-ready-gate0173-afternoon.webp'):zoomed?zoomArt:artRoot+'room13-pixel-room-before-evening.webp';$('#background').alt=talking?'눈 덮인 마을 입구':'13호실의 나무 침대와 판자';$('#character').hidden=!talking;$('#character').src=artRoot+(daram?'room13-fullbody-daram-neutral.webp':'room13-fullbody-karo-neutral.webp');$('#character').alt=daram?'다람이':'까로';$('#character').tabIndex=talking?0:-1;$('#character').setAttribute('role','button');$('#character').setAttribute('aria-label',daram?'다람이에게 물어보기':'까로에게 물어보기');$('#inspection').hidden=talking;$('#dialogue').hidden=!talking;$('#note-target').hidden=talking;$('#reading-actions').hidden=!talking;$('#mode-note').textContent=talking?'':'물건을 눌러 살펴보세요';$('#place').textContent=talking?(daram?'여관 2층 · 13호실':'눈에 막힌 입구'):'여관 2층 · 13호실';$('#time').textContent=talking?(daram?'2일째 · 화요일 · 오전':'1일째 · 월요일 · 오후'):'5일째 · 금요일 · 저녁';$('#back span').textContent=talking?'돌아가기':zoomed?'현장으로':'침대 밑';$('#present').disabled=!talking;$('#investigate').classList.toggle('active',!talking);$('#observation').textContent=zoomed?'판자 아래에 접힌 종이가 있다.':'침대 아래를 더 가까이 살펴볼 수 있다.';$('#note-target').style.cssText=zoomed?'':'left:61%;top:66%;width:28%;height:21%';$('#note-target .hint').textContent=zoomed?'접힌 쪽지':'침대 밑';$('#note-target').setAttribute('aria-label',zoomed?'접힌 쪽지 살펴보기':'침대 밑 확대하기');$('#inspection .tool-tray').hidden=!zoomed;renderLine()}
function setView(v){if(v==='record'){view='inspect';zoomed=true;renderView();openRecords(false);document.querySelector('[data-view="record"]').setAttribute('aria-pressed','true');document.querySelector('[data-view="inspect"]').setAttribute('aria-pressed','false')}else{view=v;if(v==='inspect')zoomed=true;if(v==='talk')speakerId='karo';renderView()}}
function renderLine(){if(presented){const entry=presented.lines[presented.cursor];$('#speaker').textContent=entry.who;$('#line').textContent=entry.text;$('#line').style.whiteSpace='pre-line';return}const l=speakerId==='daram'?daramLines[lineIndex]:lines[lineIndex];$('#speaker').textContent=l.who;$('#line').textContent=l.text;$('#line').style.whiteSpace='pre-line'}
function showQuestions(){endPresentation();stopAuto();const d=speakerId==='daram';$('.question-title').textContent=d?'다람이에게 묻기':'까로에게 묻기';const labels=d?['방은 좀 둘러봤어?','아까 마을에서 뭘 봤어?','오늘은 좀 쉬고 싶어?']:['많이 망가진 거야?','여관은 어디로 가면 돼?','고치는 데 얼마나 걸릴까?'];document.querySelectorAll('[data-question]').forEach((b,i)=>b.textContent=labels[i]);$('#questions').hidden=false;$('#question-shade').hidden=false;document.querySelectorAll('[data-question]').forEach(b=>b.classList.toggle('asked',asked.has(speakerId+':'+b.dataset.question)));([...document.querySelectorAll('[data-question]')].find(b=>!asked.has(speakerId+':'+b.dataset.question))||document.querySelector('[data-question]')).focus()}
function hideQuestions(){$('#questions').hidden=true;$('#question-shade').hidden=true}
const spriteCells=[[0,0],[0,0],[1,0],[2,0],[1,1],[3,0]];
function pixelMarkup(index){const c=spriteCells[index];return '<span class="pixel-icon" style="background-position:'+c[0]*100/3+'% '+c[1]*50+'%" aria-hidden="true"></span>'}
function renderRecords(){
 const list=recordList();selected=Math.max(0,Math.min(selected,list.length-1));const d=list[selected];game.dataset.recordkind=tab;
 $('#record-title').textContent=d.title;$('#kind').textContent=d.kind;
 $('#record-kind').textContent=tab==='people'?'직접 만난 사람':tab==='testimony'?'말한 사람 · '+d.author:'수첩에 남긴 증거';
 $('#record-description').textContent=d.description;$('#record-description').style.whiteSpace='pre-line';$('#record-source').textContent=d.source;
 $('#large-icon use').setAttribute('href','#i-'+d.icon);$('#large-icon').style.display=tab==='people'?'block':'none';
 $('#large-pixel').hidden=tab!=='items';$('#record-portrait').hidden=tab!=='testimony';
 if(tab==='items'){const c=spriteCells[selected];$('#large-pixel').style.backgroundPosition=(c[0]*100/3)+'% '+(c[1]*50)+'%'}
 if(tab==='testimony'){$('#record-portrait').style.backgroundImage='url('+artRoot+d.portrait+')';$('#record-portrait').setAttribute('aria-label',d.author)}
 $('#record-description').scrollTop=0;$('#record-count').textContent=String(selected+1).padStart(2,'0')+' / '+String(list.length).padStart(2,'0');
 $('#record-footer-note').textContent=presenting?'보여줄 자료를 고르세요':'← → 자료 선택';
 $('#submit-evidence').hidden=!presenting||tab==='people';$('#submit-evidence').textContent=(speakerId==='daram'?'다람이':'까로')+'에게 제시';
 document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tab===tab)));
 const grid=$('#item-grid');grid.replaceChildren();
 for(let i=0;i<list.length;i++){const b=document.createElement('button');
  if(tab==='testimony'){const image=document.createElement('span');image.className='witness-thumb witness-face';image.style.backgroundImage='url('+artRoot+list[i].portrait+')';image.setAttribute('aria-hidden','true');b.append(image)}
  else b.innerHTML=tab==='items'?pixelMarkup(i):icon(list[i].icon);
  b.setAttribute('aria-label',list[i].title);b.setAttribute('aria-pressed',String(i===selected));b.classList.toggle('selected',i===selected);b.title=list[i].title;
  b.onclick=()=>{selected=i;remembered[tab]=i;renderRecords();document.querySelectorAll('#item-grid button')[i].focus()};grid.append(b)
 }
}

function openRecords(asPresent=false,targetIndex=null){lastFocus=document.activeElement;stopAuto();hideQuestions();presenting=asPresent;if(asPresent||targetIndex!==null)tab='items';selected=targetIndex===null?remembered[tab]:targetIndex;$('#overlay').hidden=false;$('#records').hidden=false;renderRecords();$('#close-record').focus()}
function showPanel(id){lastFocus=document.activeElement;stopAuto();closeAll();$('#overlay').hidden=false;$('#'+id).hidden=false;$('#'+id+' button').focus()}
function openLog(){showPanel('backlog');const list=$('#log-lines');list.replaceChildren();for(const l of history){const e=document.createElement('div');e.className='backlog-entry';const n=document.createElement('strong');n.textContent=l.who;const p=document.createElement('p');p.textContent=l.text;e.append(n,p);list.append(e)}}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>setView(b.dataset.view));document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{remembered[tab]=selected;tab=b.dataset.tab;selected=remembered[tab];renderRecords()});document.querySelectorAll('[data-tool]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-tool]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));$('#observation').textContent=b.dataset.tool==='knife'?'판자는 이미 열려 있다. 종이는 손으로 집을 수 있다.':'판자 아래에 접힌 종이가 있다.'});
$('#note-target').onclick=()=>{if(!zoomed){zoomed=true;renderView();return}openRecords(false,0);pendingFind=!foundNote};
$('#character').onclick=showQuestions;$('#character').onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showQuestions()}};$('#line').onclick=()=>presented?advanceDialogue():showQuestions();$('#next').onclick=advanceDialogue;document.querySelectorAll('[data-question]').forEach(b=>b.onclick=()=>{asked.add(speakerId+':'+b.dataset.question);hideQuestions();const who=speakerId==='daram'?'다람이':'까로';const text=(speakerId==='daram'?daramAnswers:answers)[b.dataset.question];$('#speaker').textContent=who;$('#line').textContent=text;history.push({who:'아빠',text:b.textContent},{who,text})});$('#question-back').onclick=hideQuestions;$('#record').onclick=()=>openRecords(false);$('#present').onclick=()=>openRecords(true);$('#investigate').onclick=()=>{view='field';renderView()};$('#back').onclick=()=>{if(!$('#questions').hidden){hideQuestions();return}if(view==='inspect'){zoomed=!zoomed;renderView()}else{view='field';renderView()}};$('#close-record').onclick=closeAll;$('#close-log').onclick=closeAll;$('#close-options').onclick=closeAll;$('#overlay').onclick=closeAll;$('#options').onclick=()=>showPanel('options-panel');$('#log').onclick=openLog;$('#font-size').onclick=()=>{game.classList.toggle('large-text');$('#font-size span').textContent=game.classList.contains('large-text')?'크게':'기본'};$('#window-opacity').onclick=()=>{game.classList.toggle('solid-dialogue');$('#window-opacity span').textContent=game.classList.contains('solid-dialogue')?'진하게':'보통'};$('#auto').onclick=()=>{if(auto)return stopAuto();auto=true;$('#auto').setAttribute('aria-pressed','true');$('#auto span').textContent='ON';autoTimer=setInterval(()=>{if(view!=='talk'||!$('#records').hidden||!$('#questions').hidden)return stopAuto();$('#next').click();if(!presented&&lineIndex===lines.length-1)stopAuto()},3200)};$('#submit-evidence').onclick=submitPresentation;document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeAll();stopAuto()}if(e.key==='Tab'){const active=['records','backlog','options-panel','move-panel','questions'].map(id=>$('#'+id)).find(x=>!x.hidden);if(!active)return;const nodes=[...active.querySelectorAll('button:not([disabled])')].filter(x=>!x.hidden);if(!nodes.length)return;const first=nodes[0],last=nodes.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}});$('#item-grid').addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(e.key))return;e.preventDefault();const n=recordList().length;const offset={ArrowLeft:-1,ArrowRight:1,ArrowUp:-6,ArrowDown:6};selected=e.key==='Home'?0:e.key==='End'?n-1:Math.max(0,Math.min(n-1,selected+offset[e.key]));remembered[tab]=selected;renderRecords();document.querySelectorAll('#item-grid button')[selected].focus()});window.uiConcept={state:()=>({view,zoomed,field,speakerId,area,asked:[...asked],tab,selected,auto,presented:presented?{title:presented.data.title,kind:presented.kind,cursor:presented.cursor}:null,soundEnabled})};

function renderField(){endPresentation();game.dataset.field=field;closeAll();stopAuto();clearTimeout(arrivalTimer);$('#status').classList.remove('show');$('#toast').hidden=true;$('#background').src=fieldArt[field];$('#background').alt=fieldNames[field];$('#character').hidden=true;$('#dialogue').hidden=true;$('#inspection').hidden=true;$('#reading-actions').hidden=true;$('#note-target').hidden=true;$('#resident').hidden=field!=='room';$('#desk-target').hidden=field!=='room';$('#place').textContent=fieldNames[field];$('#time').textContent='2일째 · 화요일 · 오전';$('#back span').textContent=field==='room'?'복도로':field==='hall'?'13호실':'장소 이동';$('#mode-note').textContent='';$('#present').disabled=true;$('#investigate').classList.add('active');document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view==='field')));$('#arrival-note').hidden=true;if(field==='room'&&!arrivalSeen){arrivalSeen=true;$('#arrival-note').hidden=false;history.push({who:'아빠',text:'엄마가 머물던 방. 책상 위에 접힌 종이가 있다.'});arrivalTimer=setTimeout(()=>$('#arrival-note').hidden=true,6500)}}
function navigateField(key){field=key;view='field';renderView()}
function moveButton(title,sub,fn,current=false){const b=document.createElement('button');b.className='destination';const titleEl=document.createElement('span');titleEl.textContent=title;const detail=document.createElement('small');detail.textContent=current?'현재 위치':sub;b.append(titleEl,detail);b.disabled=current;b.onclick=fn;$('#move-list').append(b)}
function renderMove(){document.querySelector('[data-area=world]').disabled=!worldOpened;const list=$('#move-list');list.replaceChildren();$('#work-detail').hidden=true;$('#move-location').textContent='현재 · '+fieldNames[field];$('#move-wallet').textContent='소지금 0냥';$('#move-title').textContent=area==='jobs'?'일거리':area==='shop'?'상점':'이동';document.querySelectorAll('[data-area]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.area===area)));if(area==='inn'){for(const [key,label] of [['room','13호실'],['hall','2층 복도'],['inn','접수대'],['dining','식당']])moveButton(label,'이동',()=>navigateField(key),field===key);moveButton('여관 밖으로 ›','마을 지도로',()=>{worldOpened=true;area='world';renderMove()})}else if(area==='world'){for(const [key,label] of [['square','광장'],['store','잡화점'],['gate','마차 · 마을 입구'],['workshop','수리점'],['inn','여관']])moveButton(label,'이동',()=>navigateField(key),field===key)}else if(area==='jobs'){for(const j of [{title:'여관 식사 준비',pay:6,place:'dining',detail:'식기를 닦고 손님별로 식사를 나눈다.'},{title:'마을 소포 배달',pay:7,place:'gate',detail:'짐표를 확인하고 소포를 배달한다.'},{title:'수리점 부품 정리',pay:8,place:'workshop',detail:'부품을 크기별로 나누고 수량을 확인한다.'}])moveButton(j.title,'보수 '+j.pay+'냥',()=>showWork(j))}else{for(const [title,price] of [['구운 밤',2],['그림엽서',3],['질긴 묶음끈',3]])moveButton(title,price+'냥 · '+price+'냥 부족',()=>status('소지금이 부족하다.'));list.querySelectorAll('button').forEach(b=>{b.disabled=true;b.classList.add('unaffordable')})}}
function showWork(job){$('#move-list').replaceChildren();const box=$('#work-detail');box.replaceChildren();box.hidden=false;const title=document.createElement('h3');title.textContent=job.title;const detail=document.createElement('p');detail.textContent=job.detail;const cost=document.createElement('p');cost.className='time-cost';cost.textContent='오전 사용 → 오후 · 보수 '+job.pay+'냥';const actions=document.createElement('div');const back=document.createElement('button');back.textContent='다른 일 보기';back.onclick=renderMove;const accept=document.createElement('button');accept.className='accept-job';accept.textContent='도우러 가기';accept.onclick=()=>navigateField(job.place);actions.append(back,accept);box.append(title,detail,cost,actions)}
function openMove(){lastFocus=document.activeElement;stopAuto();closeAll();worldOpened=!['room','hall','inn','dining'].includes(field);area=worldOpened?'world':'inn';$('#overlay').hidden=false;$('#move-panel').hidden=false;renderMove();$('#close-move').focus()}
function setupFieldControls(){$('#move').onclick=openMove;$('#close-move').onclick=closeAll;$('#jobs').onclick=()=>{area='jobs';renderMove()};$('#shop').onclick=()=>{area='shop';renderMove()};document.querySelectorAll('[data-area]').forEach(b=>b.onclick=()=>{area=b.dataset.area;renderMove()});$('#close-arrival').onclick=()=>{$('#arrival-note').hidden=true;clearTimeout(arrivalTimer)};$('#resident').onclick=()=>{speakerId='daram';view='talk';lineIndex=0;renderView()};$('#desk-target').onclick=()=>{const text='책상 위에 접힌 종이가 있다.';history.push({who:'아빠',text});status(text)};$('#back').onclick=()=>{if(view==='field'){if(field==='room')navigateField('hall');else if(field==='hall')navigateField('room');else openMove()}else if(view==='inspect'){view='field';field='room';renderView()}else{view='field';renderView()}}}


function playPresentSound(){
 if(!soundEnabled)return;
 try{const C=window.AudioContext||window.webkitAudioContext;if(!C)return;audioContext=audioContext||new C();audioContext.resume().catch(()=>{});
 const duration=.16,t=audioContext.currentTime,buffer=audioContext.createBuffer(1,Math.ceil(audioContext.sampleRate*duration),audioContext.sampleRate),data=buffer.getChannelData(0);let seed=177;
 for(let i=0;i<data.length;i++){seed=(seed*16807)%2147483647;data[i]=(seed/2147483647*2-1)*Math.sin(Math.PI*i/data.length)**2}
 const source=audioContext.createBufferSource(),filter=audioContext.createBiquadFilter(),gain=audioContext.createGain();source.buffer=buffer;filter.type='bandpass';filter.Q.value=.7;filter.frequency.setValueAtTime(2200,t);filter.frequency.exponentialRampToValueAtTime(450,t+duration);gain.gain.value=.09;source.connect(filter);filter.connect(gain);gain.connect(audioContext.destination);source.start(t);source.stop(t+duration);
 }catch{}
}
function submitPresentation(){
 if(view!=='talk'||tab==='people')return;
 const kind=tab,data={...recordList()[selected]},who=speakerId==='daram'?'다람이':'까로';
 const snapshot={who:$('#speaker').textContent,text:$('#line').textContent};closeAll();stopAuto();$('#toast').hidden=true;$('#arrival-note').hidden=true;
 const scripted=kind==='testimony'?
  [{who:'아빠',text:''}, {who,text:data.author===who?'아까 내가 한 말이네. 어느 부분이 궁금해?':data.author+'가 그렇게 이야기했어?'}, {who:'아빠',text:'이 말을 했을 때의 상황을 같이 짚어보고 싶어.'}]:
  [{who:'아빠',text:data.kind==='편지'?'이 편지를 같이 봐줄래?':data.kind==='문서'?'이 문서를 같이 봐줄래?':'이 기록을 같이 봐줄래?'},{who,text:speakerId==='daram'?'응. 나도 같이 볼게.':'적힌 내용부터 차례로 살펴볼게.'},{who:'아빠',text:'기억나는 점이 있으면 이야기해 줘.'}];
 if(kind==='testimony')scripted[0].text=data.author+'가 했던 이 말을 봐줘. “'+data.quote+'”';
 presented={kind,data,lines:scripted,cursor:0,snapshot};
 $('#presented-kind').textContent=kind==='testimony'?'증언 제시 중':'증거 제시 중';$('#presented-title').textContent=data.title;
 $('#presented-icon').hidden=kind!=='items';$('#presented-portrait').hidden=kind!=='testimony';$('#presented-quote').hidden=kind!=='testimony';
 if(kind==='items'){const c=spriteCells[selected];$('#presented-icon').style.backgroundPosition=(c[0]*100/3)+'% '+(c[1]*50)+'%'}
 else{$('#presented-portrait').style.backgroundImage='url('+artRoot+data.portrait+')';$('#presented-portrait').setAttribute('aria-label',data.author);$('#presented-quote').textContent='“'+data.quote+'”'}
 const card=$('#presented-card');card.hidden=false;card.classList.remove('entering');void card.offsetWidth;card.classList.add('entering');game.classList.add('presenting-topic');
 history.push(scripted[0]);renderLine();playPresentSound();$('#next').focus()
}
function endPresentation(){
 if(!presented)return;
 const snapshot=presented.snapshot;presented=null;stopAuto();$('#presented-card').hidden=true;game.classList.remove('presenting-topic');
 $('#speaker').textContent=snapshot.who;$('#line').textContent=snapshot.text
}
function advanceDialogue(){
 if(presented){presented.cursor++;if(presented.cursor>=presented.lines.length){endPresentation();showQuestions();return}history.push(presented.lines[presented.cursor]);renderLine();return}
 const active=speakerId==='daram'?daramLines:lines;lineIndex=(lineIndex+1)%active.length;history.push(active[lineIndex]);renderLine()
}
$('#end-presentation').onclick=()=>{endPresentation();showQuestions()};$('#sfx').onclick=()=>{soundEnabled=!soundEnabled;$('#sfx span').textContent=soundEnabled?'켜짐':'꺼짐'};
setupFieldControls();renderView();
