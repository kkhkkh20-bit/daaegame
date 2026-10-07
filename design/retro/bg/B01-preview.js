'use strict';
const scenes=[
  {
    "id": "fall-steps",
    "name": "언덕 돌계단",
    "time": "새벽",
    "src": "fall-steps.png",
    "alt": "새벽 하늘과 멀리 보이는 마을, 오른쪽 돌계단에 흩어진 유리돌 세 개와 긴 미끄러진 자국, 앞쪽의 빈 돌바닥.",
    "evidence": [
      {
        "spotId": "s2f_glass",
        "evidenceId": "f2_glassbits",
        "name": "계단 위 유리돌",
        "point": [
          274,
          94
        ],
        "bounds": [
          245,
          88,
          61,
          14
        ],
        "supportingBounds": [
          253,
          100,
          30,
          31
        ],
        "description": "둥근 유리돌 세 개. 아래 계단에는 길게 미끄러진 자국.",
        "note": "유리돌의 금과 작은 스티커는 확대 조사 화면에서 보여 주세요. 계단 표면의 세 줄은 미끄러진 자국입니다."
      }
    ],
    "characterPositions": [
      [
        30,
        194
      ],
      [
        156,
        194
      ]
    ]
  },
  {
    "id": "fall-square",
    "name": "잔치 광장",
    "time": "아침",
    "src": "fall-square.png",
    "alt": "줄무늬 가판대의 유리돌 병과 간식 병, 오른쪽 게시판과 쓰레기통, 왼쪽 상자 옆 공책, 넓게 비운 광장.",
    "evidence": [
      {
        "spotId": "s2f_jar",
        "evidenceId": "f2_jar",
        "name": "가판대 유리돌 병",
        "point": [
          141,
          96
        ],
        "bounds": [
          109,
          82,
          43,
          25
        ],
        "description": "두 유리돌 병. 옆에는 비슷한 크기의 간식 병.",
        "note": "병의 라벨은 배경에서는 빈 면입니다. '까로 상회 · 도토리 3개'는 증거 조사 UI에서 표시해 주세요."
      },
      {
        "spotId": "s2f_flyer",
        "evidenceId": "f2_flyer",
        "name": "광장 게시판",
        "point": [
          289,
          91
        ],
        "bounds": [
          279,
          77,
          22,
          29
        ],
        "description": "글자 대신 작은 등불 그림이 있는 가운데 전단지.",
        "note": "전단지 문구·주문 번호는 확대 조사 UI에서 표시해 주세요."
      },
      {
        "spotId": "s2f_receipt",
        "evidenceId": "f2_receipt",
        "name": "광장 쓰레기통",
        "point": [
          233,
          113
        ],
        "bounds": [
          221,
          108,
          23,
          33
        ],
        "description": "쓰레기통 위 구겨진 종이. 잎과 다른 종이가 함께 놓여 있습니다.",
        "note": "영수증 인쇄 내용과 날짜는 확대 조사 UI에서 표시해 주세요."
      },
      {
        "spotId": "s2f_birdlog",
        "evidenceId": "f2_birdlog",
        "name": "상자 옆 공책",
        "point": [
          86,
          142
        ],
        "bounds": [
          75,
          137,
          22,
          10
        ],
        "description": "상자 옆에 놓인 짙은 푸른색 공책.",
        "note": "표지 이름과 10:24 기록은 확대 조사 UI에서 표시해 주세요."
      }
    ],
    "characterPositions": [
      [
        112,
        194
      ],
      [
        260,
        194
      ]
    ]
  },
  {
    "id": "fall-pond",
    "name": "연못",
    "time": "아침",
    "src": "fall-pond.png",
    "alt": "조용한 푸른 연못과 갈대, 왼쪽 작은 선착장, 오른쪽 물가 진흙의 뒤엉킨 물갈퀴 발자국, 앞쪽 빈 풀밭.",
    "evidence": [
      {
        "spotId": "s2f_landing",
        "evidenceId": "f2_landing",
        "name": "연못가 뒤엉킨 발자국",
        "point": [
          260,
          131
        ],
        "bounds": [
          237,
          122,
          57,
          18
        ],
        "description": "방향이 제각각인 물갈퀴 발자국. 가지런한 이동 경로가 아닙니다.",
        "note": "진흙 면의 일부를 조사 대상으로 쓰세요. 갈대·돌·낙엽은 장식입니다."
      }
    ],
    "characterPositions": [
      [
        80,
        194
      ]
    ]
  }
];
const nav=document.getElementById('scenes'),bg=document.getElementById('background'),markers=document.getElementById('markers'),detail=document.getElementById('evidence-detail'),showDaram=document.getElementById('show-daram'),showEvidence=document.getElementById('show-evidence');
let active=scenes[0],selected=0;
function updateEvidence(){
 markers.toggleAttribute('hidden',!showEvidence.checked);
 detail.toggleAttribute('hidden',!showEvidence.checked);
 if(!showEvidence.checked)return;
 markers.replaceChildren();
 active.evidence.forEach((e,i)=>{const b=document.createElement('button');b.type='button';b.className='marker';b.textContent=String(i+1);b.setAttribute('aria-label',e.name);b.setAttribute('aria-pressed',String(i===selected));b.style.left=(e.point[0]/360*100)+'%';b.style.top=(e.point[1]/200*100)+'%';b.addEventListener('click',()=>{selected=i;updateEvidence()});markers.append(b)});
 const e=active.evidence[selected];detail.textContent=e.name+' — '+e.description;
}
function select(s){
 active=s;selected=0;bg.src=s.src;bg.alt=s.alt;
 document.getElementById('title').textContent=s.name;document.getElementById('time').textContent=s.time;document.getElementById('download').href=s.src;
 document.getElementById('daram-frame').setAttribute('x',String(s.characterPositions[0][0]));
 document.querySelectorAll('#scenes button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.scene===s.id)));updateEvidence();
}
scenes.forEach(s=>{const b=document.createElement('button');b.type='button';b.dataset.scene=s.id;b.setAttribute('aria-pressed','false');const img=document.createElement('img');img.src=s.src;img.alt='';const label=document.createElement('span');label.textContent=s.name;b.append(img,label);b.addEventListener('click',()=>select(s));nav.append(b)});
showDaram.addEventListener('change',()=>document.getElementById('daram').toggleAttribute('hidden',!showDaram.checked));
showEvidence.addEventListener('change',updateEvidence);
select(scenes.find(s=>s.id===new URLSearchParams(location.search).get('scene'))||scenes[0]);
