'use strict';
const faces=[
  {
    "id": "neutral",
    "name": "기본",
    "description": "살짝 웃으며 이야기를 듣는 얼굴.",
    "sample": "먼저 직접 확인해 보자.",
    "src": "neutral.png"
  },
  {
    "id": "happy",
    "name": "활짝 웃음",
    "description": "기쁨을 드러내는 열린 웃음.",
    "sample": "찾았다! 이 기록이 필요했어.",
    "src": "happy.png"
  },
  {
    "id": "think",
    "name": "생각",
    "description": "동물 손을 턱에 대고 검토하는 얼굴.",
    "sample": "잠깐… 시간부터 다시 맞춰 볼까.",
    "src": "think.png"
  },
  {
    "id": "smug",
    "name": "의기양양",
    "description": "반쯤 감은 눈과 한쪽 올라간 입꼬리.",
    "sample": "이제 두 기록이 이어져.",
    "src": "smug.png"
  }
];
const container=document.getElementById('faces'),portrait=document.getElementById('dialogue-portrait'),line=document.getElementById('dialogue-line');
function select(face){document.querySelectorAll('.card').forEach(card=>{const selected=card.dataset.face===face.id;card.classList.toggle('selected',selected);card.querySelector('button').setAttribute('aria-pressed',String(selected))});portrait.src=face.src;portrait.alt='다람 '+face.name+' 정면 얼굴';line.textContent=face.sample}
faces.forEach(f=>{const card=document.createElement('article');card.className='card';card.dataset.face=f.id;const b=document.createElement('button');b.type='button';b.className='choose';b.setAttribute('aria-label',f.name+' 대화창에서 보기');b.setAttribute('aria-pressed','false');const frame=document.createElement('div');frame.className='portrait';const img=document.createElement('img');img.src=f.src;img.alt='다람 '+f.name+' 정면 얼굴';img.width=1254;img.height=1254;frame.append(img);const name=document.createElement('h2');name.textContent=f.name;b.append(frame,name);b.addEventListener('click',()=>select(f));const a=document.createElement('a');a.href=f.src;a.download=f.src;a.textContent='PNG 받기 ↓';card.append(b,a);container.append(card)});
document.getElementById('size').addEventListener('change',e=>{document.documentElement.style.setProperty('--portrait',e.target.value+'px');document.body.classList.toggle('large',e.target.value==='192')});
document.getElementById('surface').addEventListener('change',e=>{document.body.classList.toggle('check',e.target.value==='check');document.documentElement.style.setProperty('--surface',e.target.value==='cream'?'#f4e4c1':'#2b2d4a')});
select(faces[0]);
