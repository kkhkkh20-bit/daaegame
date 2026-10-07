'use strict';
const scenes=[
  {
    "id": "fall-owlhouse",
    "name": "할아버지 나무 집",
    "time": "정오 무렵",
    "src": "fall-owlhouse.png",
    "alt": "나무 집의 침대, 왼쪽 탁자의 촛대와 순찰 일지, 창문에서 들어오는 낮빛과 빈 앞쪽 마루.",
    "evidence": [
      {
        "spotId": "s2f_log",
        "evidenceId": "f2_owllog",
        "name": "할아버지 순찰 일지",
        "point": [
          132,
          91
        ],
        "bounds": [
          118,
          86,
          28,
          11
        ],
        "description": "침대 옆 탁자에 놓인 두툼한 공책. 옆에는 촛대와 붉은 천이 있습니다.",
        "note": "일지의 날짜·열쇠를 건넨 기록은 확대 조사 UI에서 표시합니다."
      }
    ],
    "characterCapacity": 1,
    "characterPositions": [
      [
        268,
        194
      ]
    ]
  },
  {
    "id": "fall-cell",
    "name": "사무소 지하 철창",
    "time": "아침 7시 30분",
    "src": "fall-cell.png",
    "alt": "차분한 돌벽의 지하 철창, 철창 밖 책상에 펼친 아빠의 외투, 바깥 주머니 손수건과 안주머니 작은 수첩.",
    "evidence": [
      {
        "spotId": "s2f_hanky",
        "evidenceId": "f2_hanky",
        "name": "아빠의 손수건",
        "point": [
          258,
          91
        ],
        "bounds": [
          252,
          84,
          14,
          14
        ],
        "description": "외투 바깥 주머니에서 보이는 밝은 손수건. 검은 그을음은 없습니다.",
        "note": "같은 외투의 바깥 주머니 조사 지점입니다. 작은 세척 얼룩은 확대 조사에서 표현합니다."
      },
      {
        "spotId": "s2f_notebook",
        "evidenceId": "f2_notebook",
        "name": "아빠의 작은 수첩",
        "point": [
          306,
          94
        ],
        "bounds": [
          298,
          87,
          17,
          14
        ],
        "description": "외투의 자주색 안감 주머니에 꽂힌 작은 수첩.",
        "note": "120일 기록과 10:08 확인 내용은 확대 조사 UI에서 표시합니다."
      }
    ],
    "characterCapacity": 1,
    "characterPositions": [
      [
        70,
        194
      ]
    ]
  },
  {
    "id": "fall-pine",
    "name": "높은 소나무",
    "time": "오전",
    "src": "fall-pine.png",
    "alt": "높은 소나무 가지의 둥지와 따뜻한 색의 진짜 별빛 돌, 돌 아래 살짝 드러난 검은 봉투 모서리, 앞쪽 빈 풀밭.",
    "evidence": [
      {
        "spotId": "s2f_nest",
        "evidenceId": "f2_realstone",
        "name": "진짜 별빛 돌",
        "point": [
          265,
          47
        ],
        "bounds": [
          258,
          39,
          16,
          16
        ],
        "markerOffset": [
          -21,
          -12
        ],
        "description": "높은 가지 둥지 속의 따뜻한 별빛 돌.",
        "note": "획득 후에도 원본 PNG의 돌은 남으므로 게임에서 조사 상태를 표현할 별도 오버레이를 검토해 주세요."
      },
      {
        "spotId": "s2f_envelope",
        "evidenceId": "f2_envelope",
        "name": "둥지 밑 검은 봉투",
        "point": [
          270,
          53
        ],
        "bounds": [
          264,
          50,
          14,
          5
        ],
        "markerOffset": [
          25,
          12
        ],
        "description": "돌 밑에 납작하게 깔린 봉투. 배경에서는 어두운 모서리만 보입니다.",
        "note": "둥지 조사 후 확대 검사에서 봉투 전체·도장·지시서를 드러내는 흐름을 권장합니다. markerOffset은 미리보기 번호 간격만 벌리고 실제 좌표는 point입니다."
      }
    ],
    "characterCapacity": 0,
    "characterPositions": []
  }
];
const nav=document.getElementById('scenes'),bg=document.getElementById('background'),markers=document.getElementById('markers'),leaders=document.getElementById('leaders'),detail=document.getElementById('evidence-detail'),showDaram=document.getElementById('show-daram'),showEvidence=document.getElementById('show-evidence');
let active=scenes[0],selected=0,wantDaram=false;
function updateCharacter(){
 const available=active.characterCapacity>0;showDaram.disabled=!available;showDaram.checked=available&&wantDaram;
 document.getElementById('daram').toggleAttribute('hidden',!showDaram.checked);
 if(available)document.getElementById('daram-frame').setAttribute('x',String(active.characterPositions[0][0]));
 document.getElementById('scene-note').textContent=available?'':'높은 소나무는 인물 없이 표시하는 장소입니다.';
}
function svgElement(tag,attributes){const node=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attributes).forEach(([k,v])=>node.setAttribute(k,String(v)));return node}
function updateEvidence(){
 markers.toggleAttribute('hidden',!showEvidence.checked);leaders.toggleAttribute('hidden',!showEvidence.checked);detail.toggleAttribute('hidden',!showEvidence.checked);
 if(!showEvidence.checked)return;markers.replaceChildren();leaders.replaceChildren();
 active.evidence.forEach((e,i)=>{const p=e.point,o=e.markerOffset||[0,0],x=p[0]+o[0],y=p[1]+o[1];
 if(o[0]||o[1]){leaders.append(svgElement('line',{x1:p[0],y1:p[1],x2:x,y2:y,stroke:'#ffcd75','stroke-width':.8,'stroke-dasharray':'2 2'}));leaders.append(svgElement('circle',{cx:p[0],cy:p[1],r:1.8,fill:'#ffcd75',stroke:'#1a1c2c','stroke-width':.6}))}
 const b=document.createElement('button');b.type='button';b.className='marker';b.textContent=String(i+1);b.setAttribute('aria-label',e.name);b.setAttribute('aria-pressed',String(i===selected));b.style.left=(x/360*100)+'%';b.style.top=(y/200*100)+'%';b.addEventListener('click',()=>{selected=i;updateEvidence()});markers.append(b)});
 const e=active.evidence[selected];detail.textContent=e.name+' — '+e.description;
}
function select(s){
 active=s;selected=0;bg.src=s.src;bg.alt=s.alt;document.getElementById('title').textContent=s.name;document.getElementById('time').textContent=s.time;document.getElementById('download').href=s.src;
 document.querySelectorAll('#scenes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===s.id)));updateCharacter();updateEvidence();
}
scenes.forEach(s=>{const b=document.createElement('button');b.type='button';b.dataset.scene=s.id;b.setAttribute('aria-pressed','false');const img=document.createElement('img');img.src=s.src;img.alt='';const label=document.createElement('span');label.textContent=s.name;b.append(img,label);b.addEventListener('click',()=>select(s));nav.append(b)});
showDaram.addEventListener('change',()=>{wantDaram=showDaram.checked;updateCharacter()});showEvidence.addEventListener('change',updateEvidence);
select(scenes.find(s=>s.id===new URLSearchParams(location.search).get('scene'))||scenes[0]);
