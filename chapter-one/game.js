(()=>{'use strict';
const $=id=>document.getElementById(id),KEY='daram-illustrated-chapter1-v1',SLOTS=KEY+':slots';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const own=(x,k)=>Object.prototype.hasOwnProperty.call(x,k);
const fresh=()=>({version:1,mode:'dialogue',lines:STORY.intro,index:0,after:'questions',round:1,found:[],read:[],asked:[],pressed:[],statement:0,log:[],speed:28,finished:false,moods:{},pan:.5,who:'karo',chats:[],system:null});
let s=fresh(),core,timer=null,full='',last=0,returnFocus=null,toastTimer,scrollTimer,busy=false,checkpoint=null;
function valid(v){return v&&v.version===1&&['dialogue','questions','investigate','testimony','review','finale','done','retry'].includes(v.mode)&&Array.isArray(v.lines)&&v.lines.every(l=>l&&typeof l.text==='string')&&Array.isArray(v.found)&&v.found.every(id=>EVIDENCE[id])&&Array.isArray(v.log)&&Number.isInteger(v.index)&&v.index>=0&&[1,2].includes(v.round);}
function bind(){if(!s.who)s.who=s.round===2?'mungchi':'karo';s={...fresh(),...s};core=DaramLegacy.create(CHAPTER_CASE,COMBINATIONS,s.system);const g=core.state;
 g.found=s.found;g.asked=g.asked||[];g.exam=g.exam||{};g.hintLog=g.hintLog||[];s.system=g;
 const mapping={delivery:['t_delivery','t_paid'],witness:['t_witness'],spoon:['t_spoon'],key:['t_key'],reason:['t_reason']};
 s.asked.forEach(id=>(mapping[id]||[]).forEach(t=>{if(!g.asked.includes(t))g.asked.push(t)}));
 if(s.round===2)g.broken['round:0']=true;
 if(['review','finale','done'].includes(s.mode)||s.found.includes('report')){g.broken['round:1']=true;if(!g.unlocked.includes('door:archive'))g.unlocked.push('door:archive');}
}
try{const v=JSON.parse(localStorage.getItem(KEY));if(valid(v))checkpoint=v;}catch{}
bind();
function save(){s.system=core.state;try{localStorage.setItem(KEY,JSON.stringify(s));}catch{}}
function tell(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,2500);}
function stop(){clearInterval(timer);timer=null;$('panel').classList.remove('typing');}
function actor(id,mood=0){if(id==='dad')id='daram';const el=$('actor');el.hidden=!id;el.dataset.actor=id||'';if(!id)return;
 const extra=id==='daram'&&mood>=3;el.style.setProperty('--expression',extra?Math.min(2,mood-3):Math.min(2,mood));
 const asset=extra?'daram-extra':id;el.style.backgroundImage=`url(${window.ART?.[asset]||'assets/'+asset+'.png'})`;el.dataset.emotion=String(mood);
}
function add(id){core.discover(id);save();count();}
function count(){$('count').textContent=s.found.length?' '+s.found.length:'';}
function dialogue(lines,after,actorId=s.who||'karo'){s.mode='dialogue';s.lines=lines.map(l=>({...l,actor:l.who==='dad'?'daram':own(l,'actor')?l.actor:actorId}));s.index=0;s.after=after;save();render();}
function showLine(){const l=s.lines[s.index];if(!l){arrive(s.after);return;}const who=l.who==='dad'?'daram':own(l,'actor')?l.actor:'karo';
 if(who&&l.who===who)s.moods[who]=l.mood;actor(who,who?s.moods[who]||0:0);
 $('chaptermark').hidden=!l.establish;$('chaptermark').innerHTML='<small>첫 번째 사건</small><h2>사라진 봉투</h2><p>눈길 거처 · 어느 겨울 오후</p>';
 $('panel').className='dialogue';$('panel').innerHTML=`<div class="nameplate">${esc(l.thought?'다람':NAMES[l.who])}<small>${l.thought?'혼잣말':l.who==='dad'?'곁에서':''}</small></div><p id="text" class="${l.thought?'thought':l.who==='narr'?'narration':''}"></p><button id="advance" aria-label="대사 읽기 · 다음"><span>⌄</span></button>`;
 const id=s.lines.map(x=>x.text).join('|')+'#'+s.index;if(s.logged!==id){s.log.push({name:NAMES[l.who],text:l.text,thought:!!l.thought});s.logged=id;save();}
 full=l.text;$('advance').onclick=advance;
 if(!s.speed)$('text').textContent=full;else{let n=0;$('panel').classList.add('typing');timer=setInterval(()=>{if($('modal').childElementCount)return;$('text').textContent=full.slice(0,++n);if(n>=full.length)stop();},s.speed);}
}
function advance(){if(s.mode!=='dialogue'||$('modal').childElementCount||!$('title').hidden)return;const t=Date.now();if(t-last<170)return;last=t;if(timer){stop();$('text').textContent=full;return;}s.index++;save();render();}
function arrive(mode){s.mode=mode;if(mode==='second'){s.round=2;s.who='mungchi';s.mode='questions';s.statement=0;}if(mode==='review'){['envelope','roster','report'].forEach(add);core.ask('confession');}save();render();}
function render(){stop();count();$('chaptermark').hidden=true;$('hotspots').innerHTML='';$('scene').classList.toggle('exploring',s.mode==='investigate');$('panorama').hidden=s.mode!=='investigate';$('pan-controls').hidden=s.mode!=='investigate';$('panel').className='';
 const begun=s.asked.length>0||s.mode!=='dialogue'||s.lines!==STORY.intro&&s.after!=='questions';
 $('case-nav').hidden=!(s.mode!=='dialogue'||s.asked.length||s.round>1);$('case-nav').querySelectorAll('button').forEach(b=>b.disabled=s.mode==='dialogue'||s.mode==='retry');
 $('nav-hint').textContent='힌트 '+Math.max(0,3-core.state.hints);
 if(s.mode==='dialogue')showLine();else if(s.mode==='questions')questions();else if(s.mode==='investigate')investigate();else if(s.mode==='testimony')testimony();else if(s.mode==='review')review();else if(s.mode==='finale')finale();else if(s.mode==='done')ending();else if(s.mode==='retry')retry();
}
const button=(id,t,cls='')=>`<button id="${id}" class="${cls}">${t}</button>`;
function questions(){const who=s.who||'karo';actor(who,0);$('panel').className='interactive';
 let qs=who==='karo'?Object.entries(STORY.questions).map(([id,q])=>[id,q.title]):[['key','목에 건 열쇠는 어디에 쓰나요?'],['reason','봉투가 없어진 걸 언제 알았나요?']];
 if(who==='karo'&&s.round===2)qs.push(['after','뭉치의 이야기를 듣고 나니…']);
 $('panel').innerHTML=`<div class="nameplate">${PEOPLE[who].name}<small>${PEOPLE[who].role}</small></div><div class="questions">${qs.map(([id,title])=>`<button data-q="${id}">${title}<small>${s.asked.includes(id)?'다시 듣기':'›'}</small></button>`).join('')}</div><div class="subactions">${button('people','다른 사람')}${button('chat','수다')}${button('show-evidence','증거 보여주기')}</div>`;
 $('panel').querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>{if(s.mode!=='questions')return;const id=b.dataset.q;if(!s.asked.includes(id))s.asked.push(id);
 const ids={delivery:['t_delivery','t_paid'],witness:['t_witness'],spoon:['t_spoon'],key:['t_key'],reason:['t_reason']};(ids[id]||[]).forEach(t=>core.ask(t));
 if(id==='key'){add('key');dialogue(STORY.keyFound,'questions','mungchi');}else if(id==='reason')dialogue([line('daram','봉투가 없어진 건 언제 알았어요?'),line('mungchi','주민이 돈을 받으러 왔을 때요.',1),line('daram','계속 받침을 보고 있었나요?'),line('mungchi','…아뇨.',1)],'questions','mungchi');else if(id==='after')dialogue([line('karo','겁이 나서 숨겼다는 건 알겠습니다.',1),line('karo','그렇다고 제가 도둑이 되어도 되는 건 아니죠.',0),line('daram','그것도 꼭 기록할게요.',0)],'questions','karo');else dialogue(STORY.questions[id].lines,'questions','karo');});
 $('people').onclick=peoplePicker;$('chat').onclick=()=>{if(!s.chats.includes(who)){s.chats.push(who);core.state.actions++;}dialogue(CHAT[who],'questions',who);};$('show-evidence').onclick=()=>inventory('show');}
function peoplePicker(){open(head('누구와 이야기할까?')+['karo',...(s.round>1?['mungchi']:[])].map(id=>`<button class="person-row" data-person="${id}"><b>${PEOPLE[id].name}</b><span>${PEOPLE[id].role}</span></button>`).join(''));document.querySelectorAll('[data-person]').forEach(b=>b.onclick=()=>{s.who=b.dataset.person;close();s.mode='questions';save();render();});}
const spots=[{id:'receipt',x:.15,y:.53,w:.14,h:.11},{id:'tray',x:.565,y:.558,w:.15,h:.105},{id:'clock',x:.601,y:.254,w:.075,h:.12},{id:'cabinet',x:.75,y:.33,w:.155,h:.31}];
let drag=null,moved=false,panoramaReady=false,panoramaLoading=false;
function loadPanorama(){if(panoramaReady||panoramaLoading)return;panoramaLoading=true;$('world').classList.add('loading');$('scene-load').hidden=false;$('scene-load').textContent='현장을 불러오는 중…';$('scene-load').onclick=null;
 const img=new Image();img.onload=()=>{panoramaLoading=false;panoramaReady=true;$('world').dataset.ready='true';$('world').classList.remove('loading');$('scene-load').hidden=true;};img.onerror=()=>{panoramaLoading=false;$('scene-load').textContent='현장을 다시 불러오기';$('scene-load').onclick=loadPanorama;};img.src=window.ART?.panorama||'assets/panorama.png';
}
function positionWorld(){const v=$('panorama'),world=$('world');world.style.width=Math.max(v.clientWidth,v.clientHeight*1.5)+'px';}
function setPan(f,smooth=false){const v=$('panorama');v.scrollTo({left:(v.scrollWidth-v.clientWidth)*Math.max(0,Math.min(1,f)),behavior:smooth?'smooth':'auto'});}
function panLabel(){const v=$('panorama'),range=v.scrollWidth-v.clientWidth;s.pan=range>0?v.scrollLeft/range:0;const i=Math.min(2,Math.round(s.pan*2));core.state.loc=i;$('pan-label').textContent=CHAPTER_CASE.locations[i].name;$('pan-left').disabled=s.pan<.02;$('pan-right').disabled=s.pan>.98;clearTimeout(scrollTimer);scrollTimer=setTimeout(save,160);}
function investigate(){loadPanorama();actor(null);$('panel').className='investigation';$('panel').innerHTML=`<div class="nameplate">현장 조사<small>${core.player()} 차례</small></div><p>좌우로 살펴보고, 궁금한 물건을 눌러 보자.</p><div class="subactions">${button('back','대화로')}${button('openbook','수첩')}${button('move','이동')}</div>`;
 $('hotspots').innerHTML=spots.map(p=>`<button class="spot" data-spot="${p.id}" aria-label="${EVIDENCE[p.id].title} 조사" style="left:${(p.x-p.w/2)*100}%;top:${(p.y-p.h/2)*100}%;width:${p.w*100}%;height:${p.h*100}%"></button>`).join('');
 document.querySelectorAll('[data-spot]').forEach(b=>b.onclick=()=>{if(moved)return;add(b.dataset.spot);detail(b.dataset.spot);});
 positionWorld();setPan(s.pan);panLabel();$('panorama').onscroll=panLabel;
 $('back').onclick=()=>go('questions');$('openbook').onclick=()=>inventory();$('move').onclick=movePicker;
}
$('pan-left').onclick=()=>setPan(Math.max(0,s.pan-.5),true);$('pan-right').onclick=()=>setPan(Math.min(1,s.pan+.5),true);
$('panorama').addEventListener('pointerdown',e=>{moved=false;drag={x:e.clientX,start:$('panorama').scrollLeft,id:e.pointerId,mouse:e.pointerType==='mouse'};});
$('panorama').addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x;if(Math.abs(dx)>10)moved=true;if(drag.mouse&&moved){$('panorama').setPointerCapture(e.pointerId);$('panorama').scrollLeft=drag.start-dx;}});
$('panorama').addEventListener('pointerup',()=>{drag=null;setTimeout(()=>moved=false,0)});$('panorama').addEventListener('pointercancel',()=>{drag=null;});
function movePicker(){open(head('이동한다')+CHAPTER_CASE.locations.map((l,i)=>`<button class="person-row" data-loc="${i}" ${core.locationOpen(i)?'':'disabled'}><b>${l.name}</b><span>${core.locationOpen(i)?'살펴보기':'아직 열리지 않음'}</span></button>`).join(''));
 document.querySelectorAll('[data-loc]').forEach(b=>b.onclick=()=>{const i=+b.dataset.loc;if(!core.locationOpen(i))return;s.pan=CHAPTER_CASE.locations[i].pan;core.state.loc=i;close();go('investigate');if(i===3)inventory('archive');});}
function go(mode){if(s.mode==='dialogue'||s.mode==='retry')return;s.mode=mode;save();render();}
function battleStart(){if(s.round===1&&!s.asked.includes('delivery')){tell('까로에게 배달 이야기를 먼저 들어 보자.');return;}s.mode='testimony';s.statement=0;core.begin(s.round-1,0);save();render();}
function claims(){return CHAPTER_CASE.rounds[s.round-1].stm.map(x=>x.t);}
function testimony(){actor(s.round===1?'karo':'mungchi',s.round===1?0:1);$('panel').className='interactive testimony';$('panel').innerHTML=`<div class="nameplate">${s.round===1?'까로':'뭉치'}<small>증언</small></div><div class="testimony-head"><span>문장 ${s.statement+1} / 2</span><span class="trust" aria-label="신뢰도 ${core.state.hp} / 5">${'●'.repeat(core.state.hp)}${'○'.repeat(5-core.state.hp)}</span></div><p class="claim">${esc(claims()[s.statement])}</p><div class="actions">${button('prev','‹')}${button('press','추궁')}${button('present','증거 제시','primary')}${button('next','›')}</div>`;
 $('prev').onclick=$('next').onclick=()=>{s.statement=1-s.statement;save();render();};$('present').onclick=()=>inventory('present');
 $('press').onclick=()=>{const k=s.round+':'+s.statement;if(!s.pressed.includes(k))s.pressed.push(k);const lines=s.round===1?(s.statement===0?[line('daram','직접 건넨 게 맞나요?'),line('karo','네. 제 앞에서 이름을 썼어요.',1)]:[line('daram','서명이 무엇을 확인한다는 뜻이죠?'),line('karo','주민들이 돈을 받았다는 확인이죠.',1),line('daram','서류에 그렇게 적혀 있나요?'),line('karo','확인서니까… 그런 뜻 아닙니까?',2)]):(s.statement===0?[line('daram','받침에 둔 뒤에는요?'),line('mungchi','다른 일을 했어요. 계속 보고 있지는 않았어요.',1)]:[line('daram','열 수 있는 열쇠는 하나뿐인가요?'),line('mungchi','주인님 열쇠는 여기에 없어요.',1),line('daram','다른 열쇠가 있는지 물었어요.')]);dialogue(lines,'testimony',s.round===1?'karo':'mungchi');};}
async function submit(id){if(busy)return;busy=true;$('game').classList.add('judging');try{close();const result=await core.present(s.round-1,s.statement,id);save();
 if(result.kind==='success'){dialogue(s.round===1?STORY.crowSolved:STORY.keySolved,s.round===1?'second':'review',s.round===1?'karo':'mungchi');return;}
 if(result.kind==='exhausted'){s.mode='retry';save();render();return;}
 const msg=result.kind==='inspect'?'열어 보기만 했어. 서류 아래의 문구를 추가로 검사하자.':s.statement===0?'이 자료는 이 문장과 모순되지 않아. 다른 문장을 확인하자.':id==='clock'?'시각만으로 지금 말을 반박할 수는 없어.':'이 자료와 지금 문장은 어떻게 어긋나지? 다시 확인하자.';
 dialogue([line('daram','('+msg+')',result.kind==='inspect'?1:5,{actor:'daram',thought:true})],'testimony');
 }finally{busy=false;$('game').classList.remove('judging');}}
function retry(){actor('daram',5);$('panel').className='interactive';$('panel').innerHTML=`<div class="nameplate">다람</div><p>마음이 급했어. 확인한 사실부터 다시 보자.</p><p class="muted">모은 단서는 남아 있습니다.</p><div class="actions">${button('retry-case','이 공방 다시 도전','primary')}${button('retry-book','수첩 보기')}</div>`;$('retry-case').onclick=battleStart;$('retry-book').onclick=()=>inventory();}
function review(){actor('daram',1);$('panel').className='interactive';$('panel').innerHTML=`<div class="nameplate">다람<small>같은 서명, 다른 뜻</small></div><p>명단과 엄마의 보고서는 무엇을 확인했을까?</p><div class="actions">${button('roster','명단 읽기')}${button('report','보고서 읽기')}</div><div class="actions">${button('connect','두 단서 결합','primary')}${button('deduce','사건 정리')}</div>`;
 $('roster').onclick=()=>detail('roster');$('report').onclick=()=>detail('report');$('connect').onclick=combine;
 $('deduce').onclick=()=>{if(!core.have('cx_reception_2')){tell('두 문서를 검사하고, 수첩에서 이어 보자.');return;}s.mode='finale';save();render();};}
function finale(){actor('daram',2);$('panel').className='interactive finale';$('panel').innerHTML=`<div class="nameplate">사건 정리</div>${CHAPTER_CASE.final.map((f,i)=>`<label class="answer-row">${f.question}<select data-answer="${i}"><option value="">선택하기</option>${f.options.map(([id,t])=>`<option value="${id}">${t}</option>`).join('')}</select></label>`).join('')}<p id="answer-feedback" role="status"></p>${button('finish-case','추리 확인','primary wide')}`;
 $('finish-case').onclick=()=>{const answers=[...document.querySelectorAll('[data-answer]')].map(e=>e.value);if(answers.some(x=>!x)){tell('세 칸을 모두 채워 보자.');return;}if(!core.finish(answers)){$('answer-feedback').textContent='확인한 이야기와 다른 칸이 있어. 봉투를 찾았을 때를 떠올려 보자.';save();return;}dialogue(STORY.ending,'done','daram');};}
function ending(){s.finished=true;save();actor('daram',3);$('panel').className='interactive ending';$('panel').innerHTML=`<div class="nameplate">첫 번째 사건 · 끝</div><small class="eyebrow">사라진 봉투</small><h2>답을 찾으면,<br>다음 질문이 보인다.</h2><p>봉투는 돌아왔다. 명단에 쓰인 엄마의 이름은<br>아직 풀리지 않은 질문으로 남았다.</p><p class="muted">추리 기록 ${'★'.repeat(core.state.result?.stars||1)} · 힌트 ${core.state.hints}회</p><div class="actions">${button('endingbook','사건 수첩')}${button('replay','처음부터')}</div>`;$('endingbook').onclick=()=>inventory();$('replay').onclick=resetPrompt;}
function open(html){returnFocus=document.activeElement;$('modal').innerHTML=`<div class="veil"><section class="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-title">${html}</section></div>`;[...$('game').children].filter(e=>e.id!=='modal'&&e.id!=='toast').forEach(e=>e.inert=true);$('modal').querySelectorAll('[data-close]').forEach(b=>b.onclick=close);$('modal').querySelector('button,select')?.focus();}
function head(t){return `<div class="sheet-head"><h2 id="sheet-title">${esc(t)}</h2><button data-close aria-label="닫기">×</button></div>`;}
function close(){$('modal').innerHTML='';[...$('game').children].forEach(e=>e.inert=false);if(returnFocus?.isConnected)returnFocus.focus();}
let notebookTab='evidence',comboPicks=[];
function inventory(mode='',tab=(mode==='present'||mode==='show'||mode==='archive')?'evidence':notebookTab){notebookTab=tab;const presenting=mode==='present',showing=mode==='show';
 const tabs=[['evidence','증거'],['testimony','증언'],['people','인물'],['timeline','사건 순서']];
 let html=head(presenting?'증거 제시':showing?'증거 보여주기':'다람의 수첩');
 if(presenting)html+=`<p class="current-claim">${esc(claims()[s.statement])}</p>`;
 html+='<nav class="book-tabs">'+tabs.map(([id,t])=>`<button data-tab="${id}" aria-pressed="${id===tab}">${t}</button>`).join('')+'</nav>';
 if(tab==='evidence'){let ids=s.found;if(mode==='archive')ids=ids.filter(id=>['envelope','roster','report'].includes(id));
 const pins=core.state.pins||[];ids=ids.slice().sort((a,b)=>Number(pins.includes(b))-Number(pins.includes(a)));
 html+='<div class="evidence-list">'+ids.map(id=>`<button data-evidence="${id}"><span class="item-number">${pins.includes(id)?'★':String(s.found.indexOf(id)+1).padStart(2,'0')}</span><span><b>${EVIDENCE[id].title}</b><small>${core.gated(id)?'추가 검사 가능':core.state.exam[id]?'검사 완료':id.startsWith('cx_')?'결합한 단서':'발견한 물건'}</small></span><span>›</span></button>`).join('')+'</div>';
 if(!ids.length)html+='<p class="empty">아직 기록이 없다. 현장을 살펴보자.</p>';
 }else if(tab==='testimony')html+='<div class="evidence-list">'+core.state.asked.filter(id=>TESTIMONIES[id]).map(id=>`<button data-evidence="${id}"><span><b>${PEOPLE[TESTIMONIES[id].who].name}</b><small>${esc(TESTIMONIES[id].a)}</small></span><span>›</span></button>`).join('')+'</div>';
 else if(tab==='people')html+=Object.entries(PEOPLE).filter(([id])=>id!=='mungchi'||s.round>1).map(([id,p])=>`<article class="person-note"><h3>${p.name}<small>${p.role}</small></h3><p>${p.fact}</p><aside class="daram-memo"><small>다람이만 보는 메모</small><p>${p.memo}</p></aside></article>`).join('');
 else html='<div>'+html+'<ol class="timeline">'+timeline().map(x=>'<li>'+x+'</li>').join('')+'</ol></div>';
 html+=`<div class="book-footer">${button('combine','단서 결합')}${button('journal-hint','힌트 '+Math.max(0,3-core.state.hints))}</div>`;open(html);
 document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>inventory(mode,b.dataset.tab));document.querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>detail(b.dataset.evidence,mode));$('combine').onclick=()=>combine();$('journal-hint').onclick=hint;
}
function timeline(){const out=['엄마가 남긴 보고서를 보러 눈길 거처에 도착했다.'];if(core.have('t_delivery'))out.push('오후 3시 · 까로는 뭉치에게 봉투를 건넸다고 증언했다.');if(core.state.broken['round:0'])out.push('서명은 접수 확인이었다. 주민 지급 여부는 미확인.');if(core.have('key'))out.push('뭉치에게도 보관함 예비 열쇠가 있었다.');if(core.have('envelope'))out.push('보관함에서 봉투를 회수했다. 뭉치가 숨겼다고 인정했다.');if(core.have('cx_reception_2'))out.push('시설 안전 확인이 주민 명단의 보증으로 옮겨 쓰였다.');return out;}
function detail(id,mode=''){const e=EVIDENCE[id],t=TESTIMONIES[id];if(!e&&!t)return;if(!s.read.includes(id)){s.read.push(id);save();}
 const isEvidence=!!e,examined=!!core.state.exam[id];const title=e?e.title:PEOPLE[t.who].name+'의 증언';
 let html=head(title)+`<small class="item-meta">${e?'발견한 물건':'직접 들은 말'}</small>`;
 if(e)html+=`<p class="item-description">${e.desc}</p><article class="paper">${e.body}</article>`+(e.check?(examined?`<div class="finding"><b>검사 기록</b><p>${e.check.text}</p></div>`:button('examine',e.check.label,'inspect-button')):'')+`<aside class="daram-memo"><small>다람의 낙서</small><p>${e.memo}</p></aside>`;
 else html+=`<p class="quote">“${esc(t.a)}”</p><p class="muted">질문: ${esc(t.q)}</p>`;
 html+=`<div class="item-tools">${isEvidence?button('pin',(core.state.pins||[]).includes(id)?'★ 고정 해제':'☆ 수첩에 고정'):''}${button('connect-item','다른 단서와 결합')}</div><div class="actions">${button('detail-back','수첩 목록')}${mode==='present'?button('submit','이 증거 제시','primary'):mode==='show'?button('show-item','보여주기','primary'):button('return','돌아가기','primary')}</div>`;
 open(html);if($('examine'))$('examine').onclick=()=>{core.examine(id);save();detail(id,mode);};$('detail-back').onclick=()=>inventory(mode);$('connect-item').onclick=()=>combine(id);
 if($('pin'))$('pin').onclick=()=>{let p=core.state.pins||(core.state.pins=[]);if(p.includes(id))p.splice(p.indexOf(id),1);else p.push(id);save();detail(id,mode);};
 if(mode==='present')$('submit').onclick=()=>submit(id);else if(mode==='show')$('show-item').onclick=()=>showEvidence(id);else $('return').onclick=close;
}
function showEvidence(id){close();const who=s.who||'karo';let reply;
 reply=who==='karo'?(id==='receipt'?'제 서명이 아니라 받은 사람의 서명입니다. 저는 건넸고요.':id==='key'?'배달부가 남의 보관함 열쇠까지 갖고 다니지는 않습니다.':'처음 보는 물건이네요. 반짝이지도 않고요.'):(id==='cabinet'?'접수대 뒤 보관함이에요. 중요한 서류를 넣어요.':id==='key'?'담당자가 보관하는 예비 열쇠예요.':'제가 아는 건 수첩에 말한 것까지예요.');
 dialogue([line('daram',`${EVIDENCE[id]?.title||'이 증언'}에 대해 아는 게 있나요?`),line(who,reply,1)],s.mode==='testimony'?'testimony':'questions',who);}
function combine(first=null){comboPicks=first?[first]:[];drawCombine();}
function drawCombine(){const ids=s.found.concat(core.state.asked.filter(id=>TESTIMONIES[id]));
 open(head('단서 결합')+'<p class="muted">증거와 증언에서 이어지는 두 가지를 고른다.</p><div class="combine-picks">'+[0,1].map(i=>`<span>${comboPicks[i]?esc(EVIDENCE[comboPicks[i]]?.title||PEOPLE[TESTIMONIES[comboPicks[i]].who].name+'의 증언'):'단서 '+(i+1)+'</span>'}`).join('<b>＋</b>')+'</div><div class="combine-list">'+ids.map(id=>`<button data-combine="${id}" aria-pressed="${comboPicks.includes(id)}">${esc(EVIDENCE[id]?.title||PEOPLE[TESTIMONIES[id].who].name+' · '+TESTIMONIES[id].q)}</button>`).join('')+'</div><p id="combine-feedback" role="status"></p>'+button('combine-go','연결해 보기','primary wide'));
 $('combine-go').disabled=comboPicks.length!==2;document.querySelectorAll('[data-combine]').forEach(b=>b.onclick=()=>{const id=b.dataset.combine;if(comboPicks.includes(id))comboPicks=comboPicks.filter(x=>x!==id);else if(comboPicks.length<2)comboPicks.push(id);else comboPicks=[comboPicks[1],id];drawCombine();});
 $('combine-go').onclick=()=>{const r=core.combine(...comboPicks);save();count();if(r.kind==='success'){detail(r.item.id);return;}$('combine-feedback').textContent=r.kind==='inspect'?'아직 더 검사할 부분이 있어. 증거의 추가 검사부터 해 보자.':'지금 확인한 내용만으로는 둘을 연결할 수 없어.';};}
function hint(){const messages=s.mode==='testimony'?[s.round===1?'까로는 서명으로 무엇까지 확인했다고 했지?':'문을 열 수 있는 방법이 정말 하나뿐일까?','수첩에서 관련 증거를 추가 검사해 보자.','증거를 제시할 때는 문장도 함께 골라야 해.']:s.mode==='review'?['두 서류가 각각 무엇을 확인하는지 살펴보자.','보고서의 점검 범위와 명단 하단을 검사해 보자.','명단과 보고서를 결합하면 확인 범위의 차이가 보여.']:['현장은 좌우로 이어져 있어. 창가의 종이부터 살펴보자.','증언도 수첩에 모여. 서류와 말의 뜻을 비교해 보자.','확인서를 열어 본 다음, 서명 아래 문구를 추가 검사해 보자.'];
 open(head('힌트')+`<p>${core.state.hints>=3?'이번 사건의 힌트는 모두 사용했어. 기록한 내용은 다시 볼 수 있어.':'힌트는 사건마다 세 번. 필요할 때만 펼쳐 보자.'}</p><div class="hint-history">${core.state.hintLog.map(t=>'<p>'+esc(t)+'</p>').join('')}</div>`+(core.state.hints<3?button('use-hint','힌트 펼치기 · '+(3-core.state.hints)+'회 남음','primary wide'):''));
 if($('use-hint'))$('use-hint').onclick=()=>{const n=core.state.hints;if(core.hint()){const t=messages[Math.min(n,2)];core.state.hintLog.push(t);save();hint();$('nav-hint').textContent='힌트 '+(3-core.state.hints);}};
}
function readSlots(){try{const x=JSON.parse(localStorage.getItem(SLOTS));return Array.isArray(x)?[0,1,2].map(i=>x[i]&&valid(x[i].state)?x[i]:null):[null,null,null]}catch{return [null,null,null]}}
function slots(){const a=readSlots();open(head('저장과 불러오기')+'<p class="muted">자동 저장과 별도로 세 지점을 남길 수 있습니다.</p>'+a.map((x,i)=>`<div class="save-slot"><b>기록 ${i+1}</b><small>${x?new Date(x.at).toLocaleString('ko-KR'):'빈 기록'}</small><div class="actions"><button data-save="${i}">여기에 저장</button><button data-load="${i}" ${x?'':'disabled'}>불러오기</button></div></div>`).join('')+`<div class="actions">${button('export','진행 내보내기')}${button('import','파일에서 불러오기')}</div><input id="import-file" type="file" accept="application/json,.json" hidden>`);
 const store=i=>{a[i]={at:Date.now(),state:JSON.parse(JSON.stringify(s))};try{localStorage.setItem(SLOTS,JSON.stringify(a));slots();}catch{tell('저장 공간을 사용할 수 없습니다. 진행을 파일로 내보내 주세요.');}};
 document.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>{const i=+b.dataset.save;if(a[i]){open(head('기록 덮어쓰기')+`<p>기록 ${i+1}을 현재 진행으로 바꿀까요?</p>`+button('overwrite','이 기록에 저장','primary wide'));$('overwrite').onclick=()=>store(i);}else store(i);});
 document.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>{const item=a[+b.dataset.load];if(!item)return;open(head('기록 불러오기')+'<p>자동 저장을 선택한 기록으로 바꿉니다.</p>'+button('load-confirm','불러오기','primary wide'));$('load-confirm').onclick=()=>restore(item.state);});
 $('export').onclick=()=>{const blob=new Blob([JSON.stringify(s)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='daram-chapter-one.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
 $('import').onclick=()=>$('import-file').click();$('import-file').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>2e6)throw Error();const data=JSON.parse(await f.text());if(!valid(data))throw Error();open(head('진행 파일 불러오기')+'<p>현재 자동 저장을 이 파일의 진행으로 바꿉니다.</p>'+button('import-confirm','불러오기','primary wide'));$('import-confirm').onclick=()=>restore(data);}catch{tell('이 1장의 올바른 저장 파일이 아닙니다.')}};
}
function restore(v){if(!valid(v)){tell('저장 기록을 읽지 못했습니다.');return;}close();s=JSON.parse(JSON.stringify(v));bind();$('title').hidden=true;save();render();}
function resetPrompt(){open(head('처음부터 시작')+'<p>자동 저장을 지우고 새로 시작합니다. 별도로 저장한 세 기록은 남습니다.</p>'+button('reset','새로 시작','primary wide'));$('reset').onclick=()=>{close();s=fresh();bind();save();render();};}
$('start').onclick=()=>{$('title').hidden=true;s=fresh();bind();save();render();};$('continue').hidden=!checkpoint;$('continue').onclick=()=>restore(checkpoint);
$('notebook').onclick=()=>inventory();$('log').onclick=()=>open(head('대화 기록')+s.log.map(l=>`<div class="log-line"><b>${esc(l.name)}</b><p class="${l.thought?'thought':''}">${esc(l.text)}</p></div>`).join(''));
$('settings').onclick=()=>{open(head('설정')+'<label class="setting">글자 속도<select id="speed"><option value="45">천천히</option><option value="28">보통</option><option value="0">바로 표시</option></select></label>'+button('save-menu','저장 · 불러오기','wide')+button('reset-menu','처음부터','wide'));$('speed').value=s.speed;$('speed').onchange=e=>{s.speed=Number(e.target.value);save();if(!s.speed&&timer){stop();$('text').textContent=full;}};$('save-menu').onclick=slots;$('reset-menu').onclick=resetPrompt;};
$('nav-scene').onclick=()=>go('investigate');$('nav-move').onclick=movePicker;$('nav-talk').onclick=()=>go('questions');$('nav-note').onclick=()=>inventory();$('nav-fight').onclick=()=>{if(['review','finale','done'].includes(s.mode))go('review');else battleStart();};$('nav-hint').onclick=hint;
window.addEventListener('resize',()=>{if(s.mode==='investigate'){const p=s.pan;positionWorld();setPan(p);panLabel();}});
document.addEventListener('keydown',e=>{if($('modal').childElementCount){if(e.key==='Escape'){e.preventDefault();close();}if(e.key==='Tab'){const a=[...$('modal').querySelectorAll('button:not(:disabled),select,summary')],first=a[0],last=a[a.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}}return;}if((e.key==='Enter'||e.key===' ')&&s.mode==='dialogue'&&[document.body,$('advance')].includes(document.activeElement)){e.preventDefault();advance();}});
actor('daram',0);count();window.chapterStartReady?.();
})();
