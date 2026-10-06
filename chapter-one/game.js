(()=>{'use strict';
const $=id=>document.getElementById(id),KEY='daram-illustrated-chapter1-v1',SLOTS=KEY+':slots';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const audio=window.DaramAudio||{music(){},fx(){},get(){return {music:0,effects:0}},set(){}};
const effects=window.DaramEffects||{play(){},clear(){},cue(){},get(){return 'off'},set(){}};
const own=(x,k)=>Object.prototype.hasOwnProperty.call(x,k);
const fresh=()=>({version:1,mode:'dialogue',lines:STORY.intro,index:0,after:'questions',round:1,found:[],read:[],asked:[],pressed:[],statement:0,log:[],speed:28,finished:false,moods:{},pan:.5,room:0,roomVersion:2,roomPans:{},caseTime:'15:40',who:'karo',chats:[],system:null});
let s=fresh(),core,timer=null,full='',last=0,returnFocus=null,toastTimer,scrollTimer,busy=false,checkpoint=null,questionReadyAt=0,questionUnlockTimer;
function valid(v){return v&&v.version===1&&['dialogue','questions','investigate','testimony','review','finale','done','retry'].includes(v.mode)&&Array.isArray(v.lines)&&v.lines.every(l=>l&&typeof l.text==='string')&&Array.isArray(v.found)&&v.found.every(id=>EVIDENCE[id])&&Array.isArray(v.log)&&Number.isInteger(v.index)&&v.index>=0&&[1,2].includes(v.round);}
function bind(){if(!s.caseTime)s.caseTime=s.found.includes('report')?'16:25':s.round===2?'16:05':s.mode==='dialogue'&&s.index===0?'15:40':'15:45';if(!s.roomVersion){s.room=[0,0,2,3][s.system?.loc||0];s.roomVersion=2;s.roomPans={};s.sceneSelection=null;}if(!s.who)s.who=s.round===2?'mungchi':'karo';s={...fresh(),...s};core=DaramLegacy.create(CHAPTER_CASE,COMBINATIONS,s.system);const g=core.state;
 g.found=s.found;g.asked=g.asked||[];g.exam=g.exam||{};g.hintLog=g.hintLog||[];s.system=g;if(!Number.isInteger(s.room)||s.room<0||s.room>3)s.room=0;g.loc=s.room;
 const mapping={delivery:['t_delivery','t_paid'],witness:['t_witness'],spoon:['t_spoon'],key:['t_key'],reason:['t_reason']};
 s.asked.forEach(id=>(mapping[id]||[]).forEach(t=>{if(!g.asked.includes(t))g.asked.push(t)}));
 if(s.round===2)g.broken['round:0']=true;
 if(['review','finale','done'].includes(s.mode)||s.found.includes('report')){g.broken['round:1']=true;if(!g.unlocked.includes('door:archive'))g.unlocked.push('door:archive');}
 if(!core.locationOpen(s.room)){s.room=0;g.loc=0;}
}
try{const v=JSON.parse(localStorage.getItem(KEY));if(valid(v))checkpoint=v;}catch{}
bind();
function save(){s.system=core.state;try{localStorage.setItem(KEY,JSON.stringify(s));}catch{}}
function tell(text){$('toast').textContent=text;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,2500);}
function stop(){clearInterval(timer);timer=null;$('panel').classList.remove('typing');}
function actor(id,mood=0){if(id==='dad')id='daram';const el=$('actor');el.hidden=!id;el.dataset.actor=id||'';if(!id)return;
 const extra=id==='daram'&&mood>=3;el.style.setProperty('--expression',extra?Math.min(2,mood-3):Math.min(2,mood));
 const asset=extra?'daram-extra':id,pixel=window.DaramArt?.has(asset);el.dataset.art=pixel?'pixel':'illustrated';el.style.backgroundImage=`url(${pixel?DaramArt.source(asset):window.ART?.[asset]||'assets/'+asset+'.png'})`;el.dataset.emotion=String(mood);
}
function add(id){if(!s.found.includes(id)){audio.fx('found');effects.play('found');}core.discover(id);save();count();}
function count(){$('count').textContent=s.found.length?' '+s.found.length:'';}
function dialogue(lines,after,actorId=s.who||'karo'){s.casePlace='눈길 거처 · '+room().name;s.mode='dialogue';s.lines=lines.map(l=>({...l,actor:own(l,'actor')?l.actor:actorId}));s.index=0;s.after=after;save();render();}
function showLine(){const l=s.lines[s.index];if(!l){arrive(s.after);return;}if(l.who==='narr'&&FATHER_NARRATION[l.text])l.text=FATHER_NARRATION[l.text];const who=l.who==='dad'&&FATHER_VIEW_TARGET[l.text]?FATHER_VIEW_TARGET[l.text]:own(l,'actor')?l.actor:l.who==='dad'?'daram':'karo';
 if(who&&l.who===who)s.moods[who]=l.mood;actor(who,who?s.moods[who]||0:0);
 if(l.stamp){s.caseTime=l.stamp.time;s.casePlace=l.stamp.place;save();} $('chaptermark').hidden=!l.establish;$('chaptermark').innerHTML='<small>첫 번째 사건</small><h2>사라진 봉투</h2><p class="event-time">12월 18일 · 오후 3시 40분<br>눈길 거처 · 산장 접수대</p>';
 $('panel').className='dialogue';$('panel').innerHTML=`<div class="nameplate">${esc(l.thought?'다람':NAMES[l.who])}<small>${l.thought?'혼잣말':''}</small></div><p id="text" class="${l.thought?'thought':l.who==='narr'?'narration':''}"></p><button id="advance" aria-label="대사 읽기 · 다음"><span>다음 ▸</span></button>`;
 const id=s.lines.map(x=>x.text).join('|')+'#'+s.index;if(s.logged!==id){s.log.push({name:NAMES[l.who],text:l.text,thought:!!l.thought});s.logged=id;save();}
 effects.cue({...l,fx:l.fx||STORY_EFFECTS[l.text]});full=l.text;if(l.thought)audio.fx('thinkin');$('advance').onclick=advance;
 if(!s.speed)$('text').textContent=full;else{let n=0;$('panel').classList.add('typing');timer=setInterval(()=>{if($('modal').childElementCount)return;$('text').textContent=full.slice(0,++n);if(!l.thought&&n%2===0&&/\S/.test(full[n-1]))audio.fx('blip',({daram:880,dad:330,karo:520,mungchi:420})[l.who]||0);if(n>=full.length)stop();},s.speed);}
}
$('game').addEventListener('click',e=>{if(e.target.closest('button,a,input,select,summary,[role=dialog]'))return;if(s.mode==='dialogue')advance();});
$('skip-intro').onclick=()=>{if(!isIntro())return;stop();s.lines.slice(s.index+1).forEach(l=>s.log.push({name:NAMES[l.who],text:l.text,thought:!!l.thought}));s.introSkipped=true;s.index=s.lines.length;audio.fx('page');arrive('questions');};
function advance(){if(s.mode!=='dialogue'||$('modal').childElementCount||!$('title').hidden)return;const t=Date.now();if(t-last<170)return;last=t;if(timer){stop();$('text').textContent=full;return;}audio.fx('page');s.index++;save();render();}
function arrive(mode){if(mode==='questions'||mode==='second')questionReadyAt=Date.now()+850;s.mode=mode;if(mode==='questions'&&s.caseTime==='15:40')s.caseTime='15:45';if(mode==='second'){s.caseTime='16:05';s.room=2;core.state.loc=2;s.pan=.5;s.round=2;s.who='mungchi';s.mode='questions';s.statement=0;}if(mode==='review'){s.caseTime='16:25';s.room=3;core.state.loc=3;s.pan=.5;['envelope','roster','report'].forEach(add);core.ask('confession');}save();render();}
function isIntro(){return s.mode==='dialogue'&&s.lines[0]?.establish===true;}
function render(){ $('skip-intro').hidden=!isIntro();if($('scene-people'))$('scene-people').hidden=true;$('world').querySelectorAll('.scene-selection,.scene-tap').forEach(e=>e.remove());effects.clear();stop();count();audio.music((s.mode==='done'||s.mode==='dialogue'&&s.after==='done')?'win':(s.mode==='testimony'||s.mode==='dialogue'&&s.after==='testimony')?'battle':(s.mode==='dialogue'&&s.after==='second')?'pursuit':s.mode==='finale'?'pursuit':['investigate','review','retry'].includes(s.mode)?'sneak':s.mode==='questions'?'talk':s.round===2?'sneak':'calm');$('chaptermark').hidden=true;$('hotspots').innerHTML='';$('scene').classList.toggle('exploring',s.mode==='investigate');$('panorama').hidden=s.mode!=='investigate';$('pan-controls').hidden=s.mode!=='investigate';$('panel').className='';
 const begun=s.asked.length>0||s.mode!=='dialogue'||s.lines!==STORY.intro&&s.after!=='questions';
 $('case-nav').hidden=!(s.mode!=='dialogue'||s.asked.length||s.round>1);$('case-nav').querySelectorAll('button').forEach(b=>b.disabled=s.mode==='dialogue'||s.mode==='retry');
 for(const [id,mode] of [['nav-scene','investigate'],['nav-talk','questions'],['nav-fight','testimony']])$(id).setAttribute('aria-current',String(s.mode===mode));
 $('nav-hint').textContent='힌트 '+Math.max(0,3-core.state.hints);
 if(s.mode==='dialogue')showLine();else if(s.mode==='questions')questions();else if(s.mode==='investigate')investigate();else if(s.mode==='testimony')testimony();else if(s.mode==='review')review();else if(s.mode==='finale')finale();else if(s.mode==='done')ending();else if(s.mode==='retry')retry();syncCaseUI();window.DaramPortraits?.layout();
}
const button=(id,t,cls='')=>`<button id="${id}" class="${cls}">${t}</button>`;
function questions(){const who=s.who||'karo';actor(who,0);$('panel').className='interactive question-panel';
 let qs=who==='karo'?Object.entries(STORY.questions).map(([id,q])=>[id,q.title]):[['key','목에 건 열쇠는 어디에 쓰나요?'],['reason','봉투가 없어진 걸 언제 알았나요?']];
 if(who==='karo'&&s.round===2)qs.push(['after','접수증을 다시 보니…']);
 $('panel').innerHTML=`<div class="nameplate">${PEOPLE[who].name}<small>${PEOPLE[who].role}</small></div><p class="question-prompt">무엇을 물어볼까? <small>질문 ${qs.length}개</small></p><div class="questions">${qs.map(([id,title],i)=>`<button data-q="${id}"><span class="question-number" aria-hidden="true">${String(i+1).padStart(2,'0')}</span><span class="question-label">${title}</span><small>${s.asked.includes(id)?'다시 듣기':'›'}</small></button>`).join('')}</div><div class="subactions">${button('people','다른 사람')}${button('chat','수다')}${button('show-evidence','증거 보여주기')}</div><div class="question-rest" aria-live="polite">이야기를 다 들었어요. 위에서 질문을 골라 주세요.</div>`;
 clearTimeout(questionUnlockTimer);const choices=[...$('panel').querySelectorAll('button')];if(Date.now()<questionReadyAt){choices.forEach(b=>b.disabled=true);questionUnlockTimer=setTimeout(()=>choices.forEach(b=>b.disabled=false),questionReadyAt-Date.now());}
 $('panel').querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>{if(s.mode!=='questions'||Date.now()<questionReadyAt)return;const id=b.dataset.q;if(!s.asked.includes(id))s.asked.push(id);
 const ids={delivery:['t_delivery','t_paid'],witness:['t_witness'],spoon:['t_spoon'],key:['t_key'],reason:['t_reason']};(ids[id]||[]).forEach(t=>core.ask(t));
 if(id==='key'){add('key');dialogue(STORY.keyFound,'questions','mungchi');}else if(id==='reason')dialogue(STORY.reason,'questions','mungchi');else if(id==='after')dialogue(STORY.afterCrow,'questions','karo');else dialogue(STORY.questions[id].lines,'questions','karo');});
 $('people').onclick=peoplePicker;$('chat').onclick=()=>{if(!s.chats.includes(who)){s.chats.push(who);core.state.actions++;}dialogue(CHAT[who],'questions',who);};$('show-evidence').onclick=()=>inventory('show');}
function talkTo(id){s.who=id;if(!room().people.includes(id)){s.room=id==='mungchi'?2:0;core.state.loc=s.room;s.pan=s.roomPans?.[ROOMS[s.room].id]??.5;}s.mode='questions';save();render();}
function peoplePicker(){open(head('누구와 이야기할까?')+['karo',...(s.round>1?['mungchi']:[])].map(id=>`<button class="person-row" data-person="${id}"><b>${PEOPLE[id].name}</b><span>${PEOPLE[id].role}</span></button>`).join(''));document.querySelectorAll('[data-person]').forEach(b=>b.onclick=()=>{close();talkTo(b.dataset.person);});}
function room(){return ROOMS[s.room||0];}
function roomSpots(){return room().spots;}
function sceneAsset(r=room()){return window.ART?.[r.asset]||'assets/'+r.asset+'.png';}
function currentGoal(){
 if(['review','finale'].includes(s.mode)||s.found.includes('report'))return core.have('cx_reception_2')?'확인한 사실로 봉투 사건을 정리하자.':'명단과 보고서의 확인 문구를 검사해 비교하자.';
 if(s.round===1){if(!s.asked.includes('delivery'))return '까로에게 봉투를 건넨 과정을 물어보자.';if(!s.found.includes('receipt'))return '접수대 창가 책상에서 접수증을 찾아보자.';if(!core.state.exam.receipt)return '수첩에서 접수증의 서명 아래 문구를 검사하자.';if(!s.asked.includes('witness'))return '까로가 지급 장면을 직접 봤는지 물어보자.';return '까로의 증언과 접수증을 나란히 비교하자.';}
 if(!s.found.includes('cabinet'))return '관리실 보관함의 잠금쇠를 살펴보자.';
 if(!s.asked.includes('key'))return '뭉치에게 목에 건 열쇠를 물어보자.';
 if(!core.state.exam.key)return '열쇠와 보관함의 번호를 비교하자.';
 return '보관함을 열 수 없다는 말과 열쇠를 비교하자.';
}
function syncCaseUI(){
 const r=room();$('place').textContent=s.mode==='dialogue'&&s.casePlace?s.casePlace.replace('눈길 거처 · ',''):r.name;$('subtitle').textContent='12월 18일 · '+(s.caseTime||'15:45');$('subtitle').classList.add('event-time');$('place').classList.add('event-place');
 $('background').style.backgroundImage=`url(${sceneAsset()})`;
 let goal=$('case-goal');if(!goal){goal=document.createElement('aside');goal.id='case-goal';$('game').append(goal);}
 goal.hidden=s.mode==='dialogue'||s.mode==='done';
 const clues=roomSpots().filter(p=>s.found.includes(p.id)).length;
 goal.innerHTML=`<small>현재 목표</small><span>${esc(currentGoal())}</span><b>${clues}/${roomSpots().length}</b>`;
}
function markSpot(p,title=EVIDENCE[p.id]?.title||p.title){$('world').querySelector('.scene-selection')?.remove();const mark=document.createElement('div');mark.className='scene-selection';mark.style.cssText=`left:${(p.x-p.w/2)*100}%;top:${(p.y-p.h/2)*100}%;width:${p.w*100}%;height:${p.h*100}%`;const label=document.createElement('span');label.textContent=title;mark.append(label);$('world').append(mark);mark.setAttribute('role','status');$('pan-label').textContent=title+' · 선택';setTimeout(()=>mark.remove(),500);return mark;}
let drag=null,moved=false,panoramaLoading=false,sceneLoadSerial=0;
const readyRooms=new Set();
function loadPanorama(){const r=room(),token=++sceneLoadSerial;panoramaLoading=true;$('world').classList.add('loading');$('world').dataset.ready='false';$('scene-load').hidden=false;$('scene-load').textContent=r.name+' 불러오는 중…';$('scene-load').onclick=null;
 const done=()=>{if(token!==sceneLoadSerial)return;panoramaLoading=false;$('world').classList.remove('loading');readyRooms.add(r.id);$('world').style.backgroundImage=`url(${sceneAsset(r)})`;$('world').dataset.room=r.id;$('world').dataset.ready='true';$('scene-load').hidden=true;};
 if(readyRooms.has(r.id)){done();return;}
 const img=new Image();img.onload=done;img.onerror=()=>{if(token!==sceneLoadSerial)return;panoramaLoading=true;$('scene-load').textContent='장소 다시 불러오기';$('scene-load').onclick=loadPanorama;};img.src=sceneAsset(r);
}
function positionWorld(){const v=$('panorama'),world=$('world');world.style.width=Math.max(v.clientWidth,v.clientHeight*1.5)+'px';}
function setPan(f,smooth=false){const v=$('panorama');v.scrollTo({left:(v.scrollWidth-v.clientWidth)*Math.max(0,Math.min(1,f)),behavior:smooth?'smooth':'auto'});}
function panLabel(){const v=$('panorama'),range=v.scrollWidth-v.clientWidth;s.pan=range>0?v.scrollLeft/range:0;s.roomPans=s.roomPans||{};s.roomPans[room().id]=s.pan;core.state.loc=s.room;$('pan-label').textContent=room().name+' · 좌우로 살펴보기';$('pan-left').disabled=s.pan<.02;$('pan-right').disabled=s.pan>.98;clearTimeout(scrollTimer);scrollTimer=setTimeout(save,160);}
function investigationCard(id){
 const e=EVIDENCE[id];if(!e)return;
 $('panel').innerHTML=`<div class="scene-clue-card">${DaramEvidenceArt.thumb(id,e.title)}<div><small>${room().name} · 수첩에 기록됨</small><h3>${esc(e.title)}</h3><p>${esc(e.desc)}</p><button id="inspect-selected" class="primary">자세히 보기 <span aria-hidden="true">›</span></button></div></div>`;
 document.querySelectorAll('[data-spot]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.spot===id)));
 $('inspect-selected').onclick=()=>detail(id);window.DaramPortraits?.layout();
}
function investigate(){loadPanorama();actor(null);$('panel').className='investigation';$('panel').innerHTML=`<div class="nameplate">현장 조사</div><p>좌우로 살펴보고, 궁금한 물건을 눌러 보자.</p><small class="scene-guidance">궁금한 곳을 콕 눌러 살펴봐요.</small><div class="subactions">${button('back','대화로')}${button('openbook','수첩')}${button('move','이동')}</div>`;
 $('hotspots').innerHTML=roomSpots().map(p=>`<button class="spot" data-spot="${p.id}" aria-label="${EVIDENCE[p.id].title} 조사" aria-pressed="false" style="left:${(p.x-p.w/2)*100}%;top:${(p.y-p.h/2)*100}%;width:${p.w*100}%;height:${p.h*100}%"></button>`).join('');
 document.querySelectorAll('[data-spot]').forEach(b=>b.onclick=()=>{if(moved||panoramaLoading)return;const id=b.dataset.spot,p=roomSpots().find(x=>x.id===id);s.sceneSelection=id;markSpot(p);const fresh=!s.found.includes(id);add(id);save();investigationCard(id);syncCaseUI();if(!fresh)audio.fx('tap');if(effects.get()!=='off'){const marker=$('world').querySelector('.scene-selection');marker.classList.add('discovered');if(effects.get()==='standard'&&!matchMedia('(prefers-reduced-motion: reduce)').matches)marker.animate([{outline:'0px solid #f0ca70'},{outline:'9px solid #f0ca7000'}],{duration:500});}});
 positionWorld();setPan(s.pan);panLabel();$('panorama').onscroll=panLabel;
 $('back').onclick=()=>go('questions');$('openbook').onclick=()=>inventory();$('move').onclick=movePicker;
 renderRoomInteractions();
 const picked=roomSpots().find(x=>x.id===s.sceneSelection);if(picked){investigationCard(picked.id);}
}
$('pan-left').onclick=()=>setPan(Math.max(0,s.pan-.5),true);$('pan-right').onclick=()=>setPan(Math.min(1,s.pan+.5),true);
$('panorama').addEventListener('pointerdown',e=>{moved=false;drag={x:e.clientX,y:e.clientY,start:$('panorama').scrollLeft,id:e.pointerId,mouse:e.pointerType==='mouse'};});
$('panorama').addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x;if(Math.hypot(dx,e.clientY-drag.y)>10)moved=true;if(drag.mouse&&moved){$('panorama').setPointerCapture(e.pointerId);$('panorama').scrollLeft=drag.start-dx;}});
$('panorama').addEventListener('pointerup',()=>{drag=null;});$('panorama').addEventListener('pointercancel',()=>{drag=null;moved=true;});
// One marker at the actual world coordinate, including otherwise empty scenery.
$('world').addEventListener('click',e=>{
 if(s.mode!=='investigate'||moved||panoramaLoading||e.target.closest('#scene-load'))return;
 const world=$('world'),rect=world.getBoundingClientRect(),target=e.target.closest('[data-spot],[data-observe]');
 const targetRect=target?.getBoundingClientRect();
 const px=e.detail===0&&targetRect?targetRect.left+targetRect.width/2:e.clientX,py=e.detail===0&&targetRect?targetRect.top+targetRect.height/2:e.clientY;
 const x=Math.max(0,Math.min(1,(px-rect.left)/rect.width)),y=Math.max(0,Math.min(1,(py-rect.top)/rect.height));
 world.querySelector('.scene-tap')?.remove();
 const mark=document.createElement('div');mark.className='scene-tap'+(target?.dataset.spot?' clue':'');mark.style.left=x*100+'%';mark.style.top=y*100+'%';mark.setAttribute('aria-hidden','true');mark.innerHTML='<i></i><span class="tap-paw">●</span>';world.append(mark);setTimeout(()=>mark.remove(),500);
 if(effects.get()==='standard'&&!matchMedia('(prefers-reduced-motion: reduce)').matches)mark.querySelector('i').animate([{transform:'scale(.35)',opacity:1},{transform:'scale(1.8)',opacity:0}],{duration:500,fill:'forwards'});
 if(target)return;
 world.querySelector('.scene-selection')?.remove();s.sceneSelection=null;document.querySelectorAll('[data-spot]').forEach(b=>b.setAttribute('aria-pressed','false'));save();
 const o=sceneryAt(room().id,x,y);$('pan-label').textContent=o.title+' · 살펴봄';
 $('panel').innerHTML=`<div class="observation-note" role="status"><small>다람 · 살펴보기</small><h3>${esc(o.title)}</h3><p>${esc(o.text)}</p></div>`;audio.fx('tap');
});
function visitRoom(i){if(!core.locationOpen(i))return;s.roomPans=s.roomPans||{};s.roomPans[room().id]=s.pan;s.room=i;core.state.loc=i;s.pan=s.roomPans[room().id]??.5;s.sceneSelection=null;audio.fx('steps');close();go('investigate');}
function movePicker(){open(head('눈길 거처 · 장소 이동')+'<p class="muted">방마다 다른 물건과 이야기가 있어요.</p><div class="location-map">'+ROOMS.map((r,i)=>{const unlocked=core.locationOpen(i),done=r.spots.filter(p=>s.found.includes(p.id)).length;return `<button class="location-card" data-loc="${i}" aria-current="${s.room===i}" ${unlocked?'':'disabled'}><span class="location-art" style="background-image:url(${sceneAsset(r)})"></span><span><b>${r.name}</b><small>${unlocked?r.purpose:'보관함 사건을 먼저 확인하세요.'}</small><em>${unlocked?done+' / '+r.spots.length+'개 조사':'잠김'}</em></span></button>`}).join('')+'</div>');document.querySelectorAll('[data-loc]').forEach(b=>b.onclick=()=>visitRoom(+b.dataset.loc));}
function renderRoomInteractions(){
 const r=room();$('hotspots').insertAdjacentHTML('beforeend',r.observations.map(o=>`<button class="spot observation" data-observe="${o.id}" aria-label="${o.title} 살펴보기" style="left:${(o.x-o.w/2)*100}%;top:${(o.y-o.h/2)*100}%;width:${o.w*100}%;height:${o.h*100}%"></button>`).join(''));
 document.querySelectorAll('[data-observe]').forEach(b=>b.onclick=()=>{if(moved||panoramaLoading)return;const o=r.observations.find(x=>x.id===b.dataset.observe);s.sceneSelection=null;markSpot(o);document.querySelectorAll('[data-spot]').forEach(x=>x.setAttribute('aria-pressed','false'));save();$('panel').innerHTML=`<div class="observation-note"><small>다람의 현장 메모</small><h3>${o.title}</h3><p>${o.text}</p><p class="scribble">“${o.memo}”</p></div>`;audio.fx('tap');});
 let cast=$('scene-people');if(!cast){cast=document.createElement('nav');cast.id='scene-people';cast.setAttribute('aria-label','현장에 있는 인물');$('world').append(cast);}const anchor={reception:.82,lounge:.85,cabinet:.47};cast.innerHTML=r.people.filter(id=>id!=='mungchi'||s.round>1).map(id=>`<button class="scene-person" data-room-person="${id}" aria-label="${PEOPLE[id].name}에게 말 걸기" style="left:${(anchor[r.id]||.8)*100}%;background-image:url(${DaramArt.source(id)})"><span>${PEOPLE[id].name} <b>···</b></span></button>`).join('');cast.hidden=false;cast.querySelectorAll('button').forEach(b=>b.onclick=()=>{if(moved||panoramaLoading)return;talkTo(b.dataset.roomPerson);});
}
function go(mode){if(s.mode==='dialogue'||s.mode==='retry')return;s.mode=mode;save();render();}
function battleStart(){if(s.round===1&&!s.asked.includes('delivery')){tell('까로에게 배달 이야기를 먼저 들어 보자.');return;}s.mode='testimony';s.statement=0;core.begin(s.round-1,0);save();render();}
function claims(){return CHAPTER_CASE.rounds[s.round-1].stm.map(x=>x.t);}
function testimony(){actor(s.round===1?'karo':'mungchi',s.round===1?0:1);$('panel').className='interactive testimony';$('panel').innerHTML=`${DaramSceneUI.speaker(s.round===1?'karo':'mungchi')}<div class="nameplate">${s.round===1?'까로':'뭉치'}<small>증언</small></div><div class="testimony-head"><span>문장 ${s.statement+1} / 2</span><span class="trust" aria-label="신뢰도 ${core.state.hp} / 5">${'●'.repeat(core.state.hp)}${'○'.repeat(5-core.state.hp)}</span></div><p class="claim ${s.suspicious?.includes(s.round+':'+s.statement)?'suspicious':''}">${esc(claims()[s.statement])}</p><button id="mark-statement" aria-pressed="${!!s.suspicious?.includes(s.round+':'+s.statement)}">${s.suspicious?.includes(s.round+':'+s.statement)?'★ 수상한 문장으로 표시함':'☆ 수상한 문장 표시'}</button><div class="actions">${button('prev','‹')}${button('press','추궁')}${button('present','증거 제시','primary')}${button('next','›')}</div>`;
 $('mark-statement').onclick=()=>{const key=s.round+':'+s.statement;s.suspicious=s.suspicious||[];if(s.suspicious.includes(key))s.suspicious=s.suspicious.filter(x=>x!==key);else s.suspicious.push(key);save();$('mark-statement').setAttribute('aria-pressed',String(s.suspicious.includes(key)));$('mark-statement').textContent=s.suspicious.includes(key)?'★ 수상한 문장으로 표시함':'☆ 수상한 문장 표시';$('panel').querySelector('.claim').classList.toggle('suspicious',s.suspicious.includes(key));};
 $('prev').onclick=$('next').onclick=()=>{s.statement=1-s.statement;save();render();};$('present').onclick=()=>inventory('present');
 $('press').onclick=()=>{audio.fx('hold');const k=s.round+':'+s.statement;if(!s.pressed.includes(k))s.pressed.push(k);const lines=s.round===1?(s.statement===0?[line('daram','직접 건넨 게 맞나요?'),line('karo','네. 제 앞에서 이름을 썼어요.',1)]:[line('daram','서명이 무엇을 확인한다는 뜻이죠?'),line('karo','주민들이 돈을 받았다는 확인이죠.',1),line('daram','서류에 그렇게 적혀 있나요?'),line('karo','확인서니까… 그런 뜻 아닙니까?',2)]):(s.statement===0?[line('daram','받침에 둔 뒤에는요?'),line('mungchi','다른 일을 했어요. 계속 보고 있지는 않았어요.',1)]:[line('daram','열 수 있는 열쇠는 하나뿐인가요?'),line('mungchi','주인님 열쇠는 여기에 없어요.',1),line('daram','다른 열쇠가 있는지 물었어요.')]);dialogue(lines,'testimony',s.round===1?'karo':'mungchi');effects.play('press');};}
async function submit(id){if(busy)return;busy=true;$('game').classList.add('judging');try{const shown=recordName(id);s.lastPresented={id,name:shown,who:s.round===1?'까로':'뭉치',statement:claims()[s.statement]};close();const result=await core.present(s.round-1,s.statement,id);save();
 if(result.kind==='success'){dialogue([line('daram','「'+shown+'」을 봐 주세요.',2),...(s.round===1?STORY.crowSolved:STORY.keySolved)],s.round===1?'second':'review',s.round===1?'karo':'mungchi');effects.play('objection');return;}
 if(result.kind==='exhausted'){s.mode='retry';save();render();return;}
 const msg=result.kind==='inspect'?'열어 보기만 했어. 서류 아래의 문구를 추가로 검사하자.':s.statement===0?'이 자료는 이 문장과 모순되지 않아. 다른 문장을 확인하자.':id==='clock'?'시각만으로 지금 말을 반박할 수는 없어.':'이 자료와 지금 문장은 어떻게 어긋나지? 다시 확인하자.';
 dialogue([line('daram','(「'+shown+'」… '+msg+')',result.kind==='inspect'?1:5,{actor:'daram',thought:true})],'testimony');
 effects.play(result.kind==='inspect'?'insight':'wrong');}finally{busy=false;$('game').classList.remove('judging');}}
function retry(){actor('daram',5);$('panel').className='interactive';$('panel').innerHTML=`<div class="nameplate">다람</div><p>마음이 급했어. 확인한 사실부터 다시 보자.</p><p class="muted">모은 단서는 남아 있습니다.</p><div class="actions">${button('retry-case','이 공방 다시 도전','primary')}${button('retry-book','수첩 보기')}</div>`;$('retry-case').onclick=battleStart;$('retry-book').onclick=()=>inventory();}
function review(){actor('daram',1);$('panel').className='interactive';$('panel').innerHTML=`<div class="nameplate">다람<small>같은 서명, 다른 뜻</small></div><p>봉투는 찾았다. 이제 엄마의 서명이 지급 명단까지 보증하는지, 두 문서의 작은 글씨를 비교하자.</p><div class="actions">${button('roster','명단 읽기')}${button('report','보고서 읽기')}</div><div class="actions">${button('connect','두 단서 결합','primary')}${button('deduce','사건 정리')}</div>`;
 $('roster').onclick=()=>detail('roster');$('report').onclick=()=>detail('report');$('connect').onclick=combine;
 $('deduce').onclick=()=>{if(!core.have('cx_reception_2')){tell('두 문서를 검사하고, 수첩에서 이어 보자.');return;}s.mode='finale';save();render();};}
function finale(){actor('daram',2);$('panel').className='interactive finale';$('panel').innerHTML=`<div class="nameplate">사건 정리</div>${CHAPTER_CASE.final.map((f,i)=>`<label class="answer-row">${f.question}<select data-answer="${i}"><option value="">선택하기</option>${f.options.map(([id,t])=>`<option value="${id}">${t}</option>`).join('')}</select></label>`).join('')}<p id="answer-feedback" role="status"></p>${button('finish-case','추리 확인','primary wide')}`;
 $('finish-case').onclick=()=>{const answers=[...document.querySelectorAll('[data-answer]')].map(e=>e.value);if(answers.some(x=>!x)){tell('세 칸을 모두 채워 보자.');return;}if(!core.finish(answers)){audio.fx('wrong');$('answer-feedback').textContent='확인한 이야기와 다른 칸이 있어. 봉투를 찾았을 때를 떠올려 보자.';save();return;}audio.fx('win');dialogue(STORY.ending,'done','daram');effects.play('win');};}
function ending(){s.finished=true;save();actor('daram',3);$('panel').className='interactive ending';$('panel').innerHTML=`<div class="nameplate">첫 번째 사건 · 끝</div><small class="eyebrow">사라진 봉투</small><h2>답을 찾으면,<br>다음 질문이 보인다.</h2><p>봉투는 돌아왔다. 명단에 쓰인 엄마의 이름은<br>아직 풀리지 않은 질문으로 남았다.</p><p class="muted">추리 기록 ${'★'.repeat(core.state.result?.stars||1)} · 힌트 ${core.state.hints}회</p><div class="actions">${button('endingbook','사건 수첩')}${button('replay','처음부터')}</div>`;$('endingbook').onclick=()=>inventory();$('replay').onclick=resetPrompt;}
function open(html){const existing=$('modal').querySelector('.sheet');if(existing){const y=existing.scrollTop;existing.innerHTML=html;existing.scrollTop=y;}else{returnFocus=document.activeElement;$('modal').innerHTML=`<div class="veil"><section class="sheet" role="dialog" aria-modal="true" aria-labelledby="sheet-title">${html}</section></div>`;}[...$('game').children].filter(e=>e.id!=='modal'&&e.id!=='toast').forEach(e=>e.inert=true);$('modal').querySelectorAll('[data-close]').forEach(b=>b.onclick=close);$('modal').querySelector('button,select')?.focus();}
function head(t,selected=false){return `<div class="sheet-head"><div class="sheet-heading"><small>다람 탐정 · 사건 수첩</small><h2 id="sheet-title">${selected?'<span id="selected-record-name">'+esc(t)+'</span>':esc(t)}</h2></div><button data-close aria-label="닫기">×</button></div>`;}
function close(){$('modal').innerHTML='';if($('title').hidden)syncCaseUI();[...$('game').children].forEach(e=>e.inert=false);if(returnFocus?.isConnected)returnFocus.focus();}
let notebookTab='evidence',comboPicks=[],comboMode='';
const recordName=id=>EVIDENCE[id]?.title||(TESTIMONIES[id]?PEOPLE[TESTIMONIES[id].who].name+'의 증언 · '+TESTIMONIES[id].q:'');

function referencePresent(page=0){const R=DaramReference,ids=core.records('ev'),who=s.round===1?'karo':'mungchi';let selected=ids.includes(core.state.recordSelection)?core.state.recordSelection:ids[0];let h=R.hot(22,150,56,66,'닫기','data-close');h+=R.box(30,251,524,78,`<b>${PEOPLE[who].name}의 증언</b><p>수집한 단서로 지금 말을 확인해 보자.</p>`,'ref-ink');h+=R.box(36,408,364,166,`<small>${PEOPLE[who].name}의 증언 · ${s.statement+1}/2</small><p>“${esc(claims()[s.statement])}”</p><b>이 말과 모순되는 증거는?</b>`,'ref-paper ref-claim comparison-claim');h+=R.box(435,373,117,113,`<div class="ref-portrait" style="background-image:url(${DaramArt.source(who)})"></div>`,'ref-ink');h+=R.box(432,495,121,89,`<b>${PEOPLE[who].name}</b><p>${PEOPLE[who].role}</p>`);h+=R.box(42,596,360,36,'수첩의 증거를 고르고 자세히 확인하세요.');h+=R.hot(428,600,132,40,'힌트','id="ref-hint"');h+=R.hot(307,362,35,40,'이전 문장','id="ref-prev"');h+=R.hot(380,362,29,40,'다음 문장','id="ref-next"');h+=R.box(339,369,35,25,`${s.statement+1}/2`);h+=R.box(289,668,266,30,`<button id="ref-page">단서 ${page+1} / ${Math.max(1,Math.ceil(ids.length/8))} · 다음 ›</button>`,'ref-ink');
for(let i=0;i<8;i++){const id=ids[page*8+i];h+=R.box(31+i%4*138,721+Math.floor(i/4)*125,115,105,id?`<button data-evidence="${id}" aria-pressed="${id===selected}" class="ref-content-button">${DaramEvidenceArt.thumb(id,EVIDENCE[id].title)}<b>${esc(EVIDENCE[id].title)}</b></button>`:'<span class="ref-unknown">?</span>','ref-paper ref-proof');}
h+=R.hot(143,984,300,62,selected?'선택한 증거 확인':'수집한 증거가 없어요',`id="record-open" ${selected?'':'disabled'}`);open(R.plane('contradiction',h,'증거 제시'));$('ref-prev').onclick=$('ref-next').onclick=()=>{s.statement=1-s.statement;save();referencePresent(page);};$('ref-hint').onclick=hint;$('ref-page').onclick=()=>referencePresent((page+1)%Math.max(1,Math.ceil(ids.length/8)));document.querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>{core.selectRecord(b.dataset.evidence);save();referencePresent(page);});$('record-open').onclick=()=>{if(selected)detail(selected,'present');};}

function referenceInventory(mode=''){
 const R=DaramReference;let ids=core.records('ev');if(mode==='archive')ids=ids.filter(id=>['envelope','roster','report'].includes(id));const pins=core.state.pins||[];ids=ids.slice().sort((a,b)=>Number(pins.includes(b))-Number(pins.includes(a)));const selected=ids.includes(core.state.recordSelection)?core.state.recordSelection:ids[0];
 let h=R.hot(20,132,73,59,'닫기','data-close');
 [['case','사건'],['evidence','단서'],['testimony','증언'],['people','인물'],['timeline','순서']].forEach(([id,label],i)=>h+=R.box(88+i*78,335,76,39,`<button data-tab="${id}" aria-pressed="${id==='evidence'}">${label}</button>`,'ref-paper ref-tab'));
 h+=R.box(482,313,87,51,`모은 단서<br><b>${ids.length}개</b>`);
 h+=R.box(105,383,448,315,ids.map(id=>`<button data-evidence="${id}" aria-label="${esc(EVIDENCE[id].title)} 조사하기" aria-pressed="${selected===id}" class="ref-content-button">${DaramEvidenceArt.thumb(id,EVIDENCE[id].title)}<b>${esc(EVIDENCE[id].title)}</b></button>`).join('')||'<p>현장에서 첫 단서를 찾아보자.</p>','ref-live-grid evidence-grid');
 h+=R.box(61,766,162,156,selected?DaramEvidenceArt.thumb(selected,EVIDENCE[selected].title):'<span class="ref-unknown">?</span>','ref-ink ref-selected-picture');
 h+=R.box(249,736,305,188,selected?`<h3>${esc(EVIDENCE[selected].title)}</h3><p>${esc(EVIDENCE[selected].desc)}</p><small>${core.state.exam[selected]?'검사 완료':'사진을 눌러 자세히 조사하기'}</small>`:'<h3>아직 기록이 없어요</h3><p>궁금한 곳을 눌러 조사해 보세요.</p>','ref-paper ref-detail-copy ref-scroll');
 h+=R.box(267,940,272,71,selected?esc(EVIDENCE[selected].memo):'작은 단서도 적어 두자.','ref-paper ref-scroll');
 if(selected)h+=R.hot(51,749,184,220,'선택한 증거 자세히 보기','id="record-open"');
 h+=R.box(166,1089,154,40,'<button id="combine">단서 결합</button>');h+=R.box(348,1090,160,40,`<button id="journal-hint">힌트 ${Math.max(0,3-core.state.hints)}</button>`);
 open(R.plane('clues',h,'다람의 수첩'));document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>inventory(mode,b.dataset.tab));document.querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>{const scroll=document.querySelector('.ref-live-grid').scrollTop;core.selectRecord(b.dataset.evidence);save();referenceInventory(mode);document.querySelector('.ref-live-grid').scrollTop=scroll;});if($('record-open'))$('record-open').onclick=()=>detail(selected,mode);$('combine').onclick=()=>combine();$('journal-hint').onclick=hint;
}

function inventory(mode='',tab=(mode==='present'||mode==='show'||mode==='archive')?'evidence':notebookTab){notebookTab=tab;if(tab==='case'){open(DaramReference.board(s,core));document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>inventory(mode,b.dataset.tab));document.querySelectorAll('[data-board-evidence]').forEach(b=>b.onclick=()=>detail(b.dataset.boardEvidence));$('board-hypothesis').onclick=()=>combine();return;}if(mode==='present'){referencePresent();return;}if(tab==='evidence'){referenceInventory(mode);return;}const presenting=mode==='present',showing=mode==='show';
 const tabs=[['case','사건'],['evidence','증거'],['testimony','증언'],['people','인물'],['timeline','사건 순서']];
 let html=head(presenting?'증거 제시':showing?'증거 보여주기':'다람의 수첩');
 if(presenting)html+=`<section class="comparison-claim">${DaramSceneUI.speaker(s.round===1?'karo':'mungchi')}<small>${s.round===1?'까로':'뭉치'}의 증언 · ${s.statement+1} / ${claims().length}</small><p>“${esc(claims()[s.statement])}”</p><b>이 말과 모순되는 증거는?</b></section>`;
 html+='<nav class="book-tabs">'+tabs.map(([id,t])=>`<button data-tab="${id}" aria-pressed="${id===tab}">${t}</button>`).join('')+'</nav>';
 if(tab==='case'){html+=DaramSceneUI.board(s,core);}
 else if(tab==='evidence'){let ids=core.records('ev');if(mode==='archive')ids=ids.filter(id=>['envelope','roster','report'].includes(id));
 const pins=core.state.pins||[];ids=ids.slice().sort((a,b)=>Number(pins.includes(b))-Number(pins.includes(a)));
 const selected=ids.includes(core.state.recordSelection)?core.state.recordSelection:ids[0];
 html+='<div class="record-browser">';
 if(selected)html+=`<section class="record-overview">${DaramEvidenceArt.thumb(selected,EVIDENCE[selected].title)}<div><small>증거 기록</small><h3>${esc(EVIDENCE[selected].title)}</h3><p>${esc(EVIDENCE[selected].desc)}</p></div></section><p class="record-instruction">증거 ${ids.length}개 <span>선택해서 자세히 보기</span></p>`;
 html+='<div class="evidence-list evidence-grid">'+ids.map(id=>`<button data-evidence="${id}" aria-label="${esc(EVIDENCE[id].title)} 조사하기" aria-pressed="${selected===id}">${DaramEvidenceArt.thumb(id,EVIDENCE[id].title)}<b>${esc(EVIDENCE[id].title)}</b><small>${pins.includes(id)?'★ ':''}${core.gated(id)?'추가 검사':core.state.exam[id]?'검사 완료':id.startsWith('cx_')?'결합 단서':'증거'}</small></button>`).join('')+'</div>';
 if(selected)html+=button('record-open',mode==='present'?'이 증거 확인하고 제시':mode==='show'?'이 증거 확인하고 보여주기':'이 증거 자세히 보기','record-open primary wide');
 html+='</div>';
 if(!ids.length)html+='<p class="empty">아직 기록이 없다. 현장을 살펴보자.</p>';
 }else if(tab==='testimony')html+='<div class="evidence-list">'+core.records('t').filter(id=>TESTIMONIES[id]).map(id=>`<button data-evidence="${id}" aria-pressed="${core.state.recordSelection===id}"><span><b>${PEOPLE[TESTIMONIES[id].who].name}</b><small>${esc(TESTIMONIES[id].a)}</small></span><span>›</span></button>`).join('')+'</div>';
 else if(tab==='people')html+=Object.entries(PEOPLE).filter(([id])=>id!=='mungchi'||s.round>1).map(([id,p])=>`<article class="person-note"><h3>${p.name}<small>${p.role}</small></h3><p>${p.fact}</p><aside class="daram-memo"><small>다람이만 보는 메모</small><p>${p.memo}</p></aside></article>`).join('');
 else html='<div>'+html+'<ol class="timeline">'+timeline().map(x=>'<li>'+x+'</li>').join('')+'</ol></div>';
 html+=`<div class="book-footer">${button('combine','단서 결합')}${button('journal-hint','힌트 '+Math.max(0,3-core.state.hints))}</div>`;open(html);
 document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>inventory(mode,b.dataset.tab));document.querySelectorAll('[data-evidence]').forEach(b=>b.onclick=()=>{if(tab==='evidence'){core.selectRecord(b.dataset.evidence);save();inventory(mode,tab);}else detail(b.dataset.evidence,mode);});if($('record-open'))$('record-open').onclick=()=>{const picked=document.querySelector('.evidence-grid [aria-pressed=true]');if(picked)detail(picked.dataset.evidence,mode);};$('combine').onclick=()=>combine();$('journal-hint').onclick=hint;document.querySelectorAll('[data-board-evidence]').forEach(b=>b.onclick=()=>detail(b.dataset.boardEvidence));if($('board-hypothesis'))$('board-hypothesis').onclick=()=>combine();
}
function timeline(){const out=['엄마가 남긴 보고서를 보러 눈길 거처에 도착했다.'];if(core.have('t_delivery'))out.push('오후 3시 · 까로는 뭉치에게 봉투를 건넸다고 증언했다.');if(core.state.broken['round:0'])out.push('서명은 접수 확인이었다. 주민 지급 여부는 미확인.');if(core.have('key'))out.push('뭉치에게도 보관함 예비 열쇠가 있었다.');if(core.have('envelope'))out.push('보관함에서 봉투를 회수했다. 뭉치가 숨겼다고 인정했다.');if(core.have('cx_reception_2'))out.push('시설 안전 확인이 주민 명단의 보증으로 옮겨 쓰였다.');return out;}
function detail(id,mode=''){if(!core.selectRecord(id))return;save();const e=EVIDENCE[id],t=TESTIMONIES[id];if(!e&&!t)return;if(!s.read.includes(id)){s.read.push(id);save();}
 const isEvidence=!!e,examined=!!core.state.exam[id];const title=recordName(id);
 const ids=core.records(e?'ev':'t').filter(x=>EVIDENCE[x]||TESTIMONIES[x]);
 let html=head(title,true)+`<section class="record-selection" aria-label="선택한 증거"><div class="selection-label">${mode==='present'?'제시할 증거':mode==='show'?'보여줄 증거':'선택한 기록'}<span>${ids.indexOf(id)+1} / ${ids.length}</span></div><div class="record-strip" aria-label="기록 선택">${ids.map(x=>`<button data-record="${x}" aria-pressed="${x===id}">${esc(recordName(x))}${x===id?'<span aria-hidden="true"> ✓</span>':''}</button>`).join('')}</div></section>`;
 if(mode==='present')html+=`<section class="current-claim comparison-claim">${DaramSceneUI.speaker(s.round===1?'karo':'mungchi')}<small>${s.round===1?'까로':'뭉치'} · 문장 ${s.statement+1}</small><p>“${esc(claims()[s.statement])}”</p><b>선택한 증거와 나란히 확인하세요.</b></section>`;
 if(mode==='show')html+=`<p class="current-claim">보여줄 사람: <b>${PEOPLE[s.who||'karo'].name}</b></p>`;
 html+=`<small class="item-meta">${e?(examined?'검사 완료':e.check?'추가 검사 가능':'증거 기록'):'수집한 증언'}</small>`;
 if(e)html+=(window.DaramEvidenceArt?.html(id,title)||'')+`<p class="item-description">${e.desc}</p><article class="paper">${e.body}</article>`+(e.check?(examined?`<div class="finding"><b>검사 기록</b><p>${e.check.text}</p></div>`:button('examine',e.check.label,'inspect-button')):'')+`<details class="daram-memo"><summary>다람의 낙서</summary><p>${e.memo}</p></details>`;
 else html+=`<p class="quote">“${esc(t.a)}”</p><p class="muted">질문: ${esc(t.q)}</p>`;
 html+=`<div class="item-tools">${isEvidence?button('pin',(core.state.pins||[]).includes(id)?'★ 고정 해제':'☆ 수첩에 고정'):''}${button('connect-item','다른 단서와 결합')}</div><div class="actions record-actions">${button('detail-back','수첩 목록')}${mode==='present'?button('submit','「'+esc(title)+'」 제시','primary'):mode==='show'?button('show-item','「'+esc(title)+'」 보여주기','primary'):button('return','돌아가기','primary')}</div>`;
 open(html);$('modal').querySelectorAll('[data-record]').forEach(b=>b.onclick=()=>{audio.fx('select');detail(b.dataset.record,mode);});{const strip=$('modal').querySelector('.record-strip'),picked=strip?.querySelector('[aria-pressed=true]');if(picked)strip.scrollLeft=Math.max(0,picked.offsetLeft-strip.clientWidth/2+picked.offsetWidth/2);}if($('examine'))$('examine').onclick=()=>{core.examine(id);audio.fx('ok');save();detail(id,mode);};$('detail-back').onclick=()=>inventory(mode);$('connect-item').onclick=()=>combine(id,mode);
 if($('pin'))$('pin').onclick=()=>{let p=core.state.pins||(core.state.pins=[]);if(p.includes(id))p.splice(p.indexOf(id),1);else p.push(id);save();detail(id,mode);};
 if(mode==='present')$('submit').onclick=()=>submit(id);else if(mode==='show')$('show-item').onclick=()=>showEvidence(id);else $('return').onclick=close;
}
function showEvidence(id){close();const who=s.who||'karo';let reply;
 reply=who==='karo'?(id==='receipt'?'제 서명이 아니라 받은 사람의 서명입니다. 저는 건넸고요.':id==='key'?'배달부가 남의 보관함 열쇠까지 갖고 다니지는 않습니다.':'처음 보는 물건이네요. 반짝이지도 않고요.'):(id==='cabinet'?'접수대 뒤 보관함이에요. 중요한 서류를 넣어요.':id==='key'?'담당자가 보관하는 예비 열쇠예요.':'제가 아는 건 수첩에 말한 것까지예요.');
 dialogue([line('daram',`${EVIDENCE[id]?.title||'이 증언'}에 대해 아는 게 있나요?`),line(who,reply,1)],s.mode==='testimony'?'testimony':'questions',who);}
function combine(first=null,mode=''){comboMode=typeof mode==='string'?mode:'';comboPicks=typeof first==='string'?[first]:[];drawCombine();}
function drawCombine(){const ids=s.found.concat(core.state.asked.filter(id=>TESTIMONIES[id]));
 open(head('단서 결합')+'<p class="muted">증거와 증언에서 이어지는 두 가지를 고른다.</p><div class="combine-picks">'+[0,1].map(i=>`<span>${comboPicks[i]?esc(EVIDENCE[comboPicks[i]]?.title||PEOPLE[TESTIMONIES[comboPicks[i]].who].name+'의 증언'):'단서 '+(i+1)+'</span>'}`).join('<b>＋</b>')+'</div><div class="combine-list">'+ids.map(id=>`<button data-combine="${id}" aria-pressed="${comboPicks.includes(id)}">${esc(EVIDENCE[id]?.title||PEOPLE[TESTIMONIES[id].who].name+' · '+TESTIMONIES[id].q)}</button>`).join('')+'</div><p id="combine-feedback" role="status"></p>'+button('combine-go','연결해 보기','primary wide'));
 $('combine-go').disabled=comboPicks.length!==2;document.querySelectorAll('[data-combine]').forEach(b=>b.onclick=()=>{const id=b.dataset.combine;if(comboPicks.includes(id))comboPicks=comboPicks.filter(x=>x!==id);else if(comboPicks.length<2)comboPicks.push(id);else comboPicks=[comboPicks[1],id];drawCombine();});
 $('combine-go').onclick=()=>{const r=core.combine(...comboPicks);save();count();if(r.kind==='success'){audio.fx('found');detail(r.item.id,comboMode);effects.play('connect');return;}audio.fx('huh');$('combine-feedback').textContent=r.kind==='inspect'?'아직 더 검사할 부분이 있어. 증거의 추가 검사부터 해 보자.':'지금 확인한 내용만으로는 둘을 연결할 수 없어.';};}
function hint(){const messages=s.mode==='testimony'?[s.round===1?'까로는 서명으로 무엇까지 확인했다고 했지?':'문을 열 수 있는 방법이 정말 하나뿐일까?','수첩에서 관련 증거를 추가 검사해 보자.','증거를 제시할 때는 문장도 함께 골라야 해.']:s.mode==='review'?['두 서류가 각각 무엇을 확인하는지 살펴보자.','보고서의 점검 범위와 명단 하단을 검사해 보자.','명단과 보고서를 결합하면 확인 범위의 차이가 보여.']:['현장은 좌우로 이어져 있어. 창가의 종이부터 살펴보자.','증언도 수첩에 모여. 서류와 말의 뜻을 비교해 보자.','확인서를 열어 본 다음, 서명 아래 문구를 추가 검사해 보자.'];
 open(head('힌트')+`<p>${core.state.hints>=3?'이번 사건의 힌트는 모두 사용했어. 기록한 내용은 다시 볼 수 있어.':'힌트는 사건마다 세 번. 필요할 때만 펼쳐 보자.'}</p><div class="hint-history">${core.state.hintLog.map(t=>'<p>'+esc(t)+'</p>').join('')}</div>`+(core.state.hints<3?button('use-hint','힌트 펼치기 · '+(3-core.state.hints)+'회 남음','primary wide'):''));
 if($('use-hint'))$('use-hint').onclick=()=>{const n=core.state.hints;if(core.hint()){const t=messages[Math.min(n,2)];core.state.hintLog.push(t);save();hint();for(const [id,mode] of [['nav-scene','investigate'],['nav-talk','questions'],['nav-fight','testimony']])$(id).setAttribute('aria-current',String(s.mode===mode));
 $('nav-hint').textContent='힌트 '+(3-core.state.hints);}};
}
function readSlots(){try{const x=JSON.parse(localStorage.getItem(SLOTS));return Array.isArray(x)?[0,1,2].map(i=>x[i]&&valid(x[i].state)?x[i]:null):[null,null,null]}catch{return [null,null,null]}}
function slots(){const a=readSlots();open(head('저장과 불러오기')+'<p class="muted">자동 저장과 별도로 세 지점을 남길 수 있습니다.</p>'+a.map((x,i)=>`<div class="save-slot"><b>기록 ${i+1}</b><small>${x?new Date(x.at).toLocaleString('ko-KR'):'빈 기록'}</small><div class="actions"><button data-save="${i}">여기에 저장</button><button data-load="${i}" ${x?'':'disabled'}>불러오기</button></div></div>`).join('')+`<div class="actions">${button('export','진행 내보내기')}${button('import','파일에서 불러오기')}</div><input id="import-file" type="file" accept="application/json,.json" hidden>`);
 const store=i=>{a[i]={at:Date.now(),state:JSON.parse(JSON.stringify(s))};try{localStorage.setItem(SLOTS,JSON.stringify(a));slots();}catch{tell('저장 공간을 사용할 수 없습니다. 진행을 파일로 내보내 주세요.');}};
 document.querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>{const i=+b.dataset.save;if(a[i]){open(head('기록 덮어쓰기')+`<p>기록 ${i+1}을 현재 진행으로 바꿀까요?</p>`+button('overwrite','이 기록에 저장','primary wide'));$('overwrite').onclick=()=>store(i);}else store(i);});
 document.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>{const item=a[+b.dataset.load];if(!item)return;open(head('기록 불러오기')+'<p>자동 저장을 선택한 기록으로 바꿉니다.</p>'+button('load-confirm','불러오기','primary wide'));$('load-confirm').onclick=()=>restore(item.state);});
 $('export').onclick=()=>{const blob=new Blob([JSON.stringify(s)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='daram-chapter-one.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
 $('import').onclick=()=>$('import-file').click();$('import-file').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>2e6)throw Error();const data=JSON.parse(await f.text());if(!valid(data))throw Error();open(head('진행 파일 불러오기')+'<p>현재 자동 저장을 이 파일의 진행으로 바꿉니다.</p>'+button('import-confirm','불러오기','primary wide'));$('import-confirm').onclick=()=>restore(data);}catch{tell('이 1장의 올바른 저장 파일이 아닙니다.')}};
}
function restore(v){if(!valid(v)){tell('저장 기록을 읽지 못했습니다.');return;}close();s=JSON.parse(JSON.stringify(v));bind();$('title').hidden=true;$('game').classList.remove('title-screen');save();render();}
function resetPrompt(){open(head('처음부터 시작')+'<p>자동 저장을 지우고 새로 시작합니다. 별도로 저장한 세 기록은 남습니다.</p>'+button('reset','새로 시작','primary wide'));$('reset').onclick=()=>{close();s=fresh();bind();save();render();};}
$('start').onclick=()=>{$('title').hidden=true;$('game').classList.remove('title-screen');s=fresh();bind();save();render();};$('continue').hidden=false;$('continue').onclick=()=>restore(checkpoint);
$('notebook').onclick=()=>inventory();$('log').onclick=()=>open(head('대화 기록')+s.log.map(l=>`<div class="log-line"><b>${esc(l.name==='아빠'?NAMES.dad:l.name)}</b><p class="${l.thought?'thought':''}">${esc(l.text)}</p></div>`).join(''));
$('settings').onclick=()=>{open(head('설정')+'<label class="setting">화면 연출<select id="effects-level"><option value="standard">기본</option><option value="simple">움직임 줄이기</option><option value="off">끄기</option></select></label><label class="setting">배경음<input id="music-volume" aria-label="배경음 음량" type="range" min="0" max="100"></label><label class="setting">효과음<input id="effects-volume" aria-label="효과음 음량" type="range" min="0" max="100"></label><p class="muted">0으로 내리면 해당 소리를 끕니다.</p>'+'<label class="setting">글자 속도<select id="speed"><option value="45">천천히</option><option value="28">보통</option><option value="0">바로 표시</option></select></label>'+button('save-menu','저장 · 불러오기','wide')+button('reset-menu','처음부터','wide'));$('effects-level').value=effects.get();$('effects-level').onchange=e=>effects.set(e.target.value);for(const k of ['music','effects']){const el=$(k+'-volume');el.value=Math.round(audio.get()[k]*100);el.oninput=()=>audio.set(k,Number(el.value)/100);} $('speed').value=s.speed;$('speed').onchange=e=>{s.speed=Number(e.target.value);save();if(!s.speed&&timer){stop();$('text').textContent=full;}};$('save-menu').onclick=slots;$('reset-menu').onclick=resetPrompt;};
$('nav-scene').onclick=()=>go('investigate');$('nav-move').onclick=movePicker;$('nav-talk').onclick=()=>go('questions');$('nav-note').onclick=()=>inventory();$('nav-fight').onclick=()=>{if(['review','finale','done'].includes(s.mode))go('review');else battleStart();};$('nav-hint').onclick=hint;
window.addEventListener('resize',()=>{if(s.mode==='investigate'){const p=s.pan;positionWorld();setPan(p);panLabel();}});
document.addEventListener('keydown',e=>{if($('modal').childElementCount){if(e.key==='Escape'){e.preventDefault();close();}if(e.key==='Tab'){const a=[...$('modal').querySelectorAll('button:not(:disabled),select,summary')],first=a[0],last=a[a.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}}return;}if((e.key==='Enter'||e.key===' ')&&s.mode==='dialogue'&&[document.body,$('advance')].includes(document.activeElement)){e.preventDefault();advance();}});
document.addEventListener('click',e=>{const b=e.target.closest('button');if(b&&!b.disabled&&b.id!=='advance'&&!b.classList.contains('spot'))audio.fx(['notebook','nav-note','log'].includes(b.id)?'page':'tap');});
window.chapterTitleReady=()=>{if(!$('title').hidden){actor(null);$('game').classList.add('title-ready');$('continue').disabled=!checkpoint&&!readSlots().some(Boolean);if($('continue').disabled)$('continue').querySelector('small').textContent='아직 시작한 사건이 없어요';}};
$('home-settings').onclick=()=>{if(checkpoint){s=JSON.parse(JSON.stringify(checkpoint));bind();}$('settings').click();};
$('home-guide').onclick=()=>open(head('탐정 수첩 사용법')+'<article><h3>살펴보고, 듣고, 이어 보기</h3><p>조사 화면을 좌우로 움직여 보세요. 궁금한 곳을 누르면 그 자리에서 반응하고, 다람이 살펴본 내용을 알려줘요.</p><p>모은 증거는 수첩에서 자세히 검사하세요. 사람들의 말과 다른 부분을 발견하면, 그 말을 골라 증거로 반박해요.</p></article>');
const scrapbook=DaramReference.controller({open,esc,checkpoint:()=>checkpoint,slots:readSlots,restore});
$('home-clues').onclick=()=>scrapbook.clues();
$('home-friends').onclick=()=>scrapbook.friends();$('home-codex').onclick=()=>scrapbook.friends();$('home-guide').onclick=()=>open(head('우편함')+'<p>눈길 거처에서 엄마의 점검 보고서를 찾았다는 연락이 왔다. 다람과 다온은 보고서에 적힌 다음 행선지를 확인하러 간다.</p>');$('home-achievements').onclick=()=>open(head('사건 기록')+'<p>'+ (checkpoint?.finished?'첫 번째 사건 · 사라진 봉투 해결':'아직 해결한 사건이 없어요. 다람의 첫 사건을 시작해 보세요.')+'</p>');
$('continue').onclick=()=>scrapbook.saves();
count();window.chapterStartReady?.();
})();
