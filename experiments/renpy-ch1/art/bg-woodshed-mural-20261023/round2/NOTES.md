# 2차 배경 제작 기록

## 결과
- 장작 창고 오후·저녁 2장, 보호시설 아침·오후·저녁 3장. 모두 2560×768, 무손실 WebP.
- `preview2_woodshed.png`: 전체 50% 축소, 좌우 1280×720 화면을 각각 50% 축소, 저녁 전체.
- `preview2_facility.png`: 시간대별 오른쪽 1280×720 화면을 원배율로 세로 배치.
- `preview2_dot_compare.png`: 기존·신규의 240×180 픽셀 조각을 모두 최근접 3배 확대.

## 방법
내장 image_gen으로 생성 및 수정했다. CLI/API 우회는 사용하지 않았다. 장작 창고는 첫 생성에서 남은 방사형 장작 균열과 짚 잔선을 지우도록 재생성했다. 그 수정본을 기준으로 저녁 조명을 만들었다. 생성 원본은 `work/*-generated.png`에 보관했다.

생성 후 Pillow로 크기·위치를 정리하고, 디더링 없이 색 수를 제한했다. 3px 단위 최근접 확대를 사용했다. 창고는 물통 약 x520~720, 젖은 장작 약 x800~1300, 문 x1300~1500, 등잔 약 x2000~2100에 배치했다. 원근 및 조사 지점에 맞춰 가로 구간별로 폭을 조정했다.

보호시설은 생성본의 새 벽 부분만 추출했다. 원본 2048×768을 왼쪽에 그대로 붙였으며 x1900~2047도 수정하지 않았다. 새 구간에만 색면 정리, 이음 기둥, 걸레받이 연결, 기존 오른쪽 타일을 이용한 바닥 연장을 적용했다. 생성본에 섞여 나온 카펫 조각은 제거했다. 새 벽은 중앙값 필터와 32색 제한으로 작은 얼룩을 줄였다. 벽화 속 사람 모양만 그림 기호로 있으며 실제 인물은 없다.

`work/assemble.py`에 재조립 과정을 남겼다. `work/validation.json`은 무손실 저장 후 원본 왼쪽과 픽셀 비교한 결과다. 세 시간대 모두 변경 픽셀 0개를 확인했다. 게임 파일은 수정하지 않았다.

## 사용 프롬프트 구성
- 창고 기본: “game background panoramic 2560x768; flat solid color planes, 2-4 shades per material, thick dark brown contours, stepped 3-4 pixel edges; no brush marks, grain, woodgrain, painterly texture or gradients.” 물통·천, 젖은 장작, 반쯤 열린 문, 짚·담요, 도끼 그루터기, 높은 창, 매달린 깡통, 덮개 등잔 및 빈 바닥 위치를 지정했다.
- 창고 수정: “Keep composition and objects identical. Smooth simple oval flat log ends with just 2 shades; remove cracks and radial starburst lines. Straw a few broad angular flat shapes. Snow broad flat white patches. No tiny strands, mottling, grain, scratches or gradients.”
- 창고 저녁: “identical composition; blue twilight outside, purple blue shadows, small covered oil lantern main warm light; remove sunlight floor stripes; preserve chunky step edges.”
- 시설 기본: “Outpaint room to RIGHT only; original left 2048 pixels identical. One wall bay with matching peach plaster, timber, baseboard, purple tiles. Faded flat mural: mountain path, round stone device radiating light, joined hands; no iron or chains. Broken stone tablet, illegible carved strokes and knife scratches. No texture, watercolor, readable text or arrows.”
- 시설 아침: “FIRST image exact geometry, mural, tablet, scratches preserved. MORNING matching second reference: cool lavender blue ambient walls, pale peach sunlight diagonals, lantern off. Clean flat limited color pixel planes.”
- 시설 저녁: “Keep exact geometry. EVENING matching second reference: blue purple plaster and floor, dark brown wood, no sunlight patches, subtle warm lantern light from left. Reduce mural to large flat faded shapes.”

## 직접 확인한 약점
- 기존 배경은 경계에 약간 부드러움이 있지만 신규 창고는 외곽선과 3px 계단이 더 강하다. 완전히 동일한 붓·도트 규칙이라고 보장할 수는 없다. 다만 1차의 장작 균열·붓질·잔무늬는 크게 줄였다.
- 창고 폭을 구간별로 조절해 중앙 젖은 장작 단면이 좌우 더미보다 넓적하다. 문과 젖은 장작은 요청한 대략 범위의 오른쪽에 걸친다.
- 보호시설 신규 벽은 원본보다 팔레트가 단순하다. 연결부를 새 기둥으로 처리했으므로 벽 칸의 경계는 보인다. 타일 원근과 낮 시간 햇빛의 정확한 연속성은 수작업 원화 수준으로 완벽하지 않다.
- 벽화의 원형 장치는 고리처럼 읽힐 수 있지만 쇠·사슬은 넣지 않았다. 저녁의 퇴색 벽화는 의도적으로 대비가 낮다.
- 확대 비교 후 시설 잔얼룩을 한 차례 더 줄이고 불필요한 바닥 조각을 정리했다. 최종 결과에도 소수의 색 경계와 생성 흔적은 남아 있으므로 미리보기로 최종 미술 검수를 할 수 있게 했다.

## 3차 — 보호시설 오른쪽 이음 다듬기 (2026-10-23)

### 납품 및 검증
- `facility-wide3-morning.webp`, `facility-wide3-afternoon.webp`, `facility-wide3-evening.webp`: 각각 2560×768, 무손실 WebP.
- `preview3_facility.png`: 세 시간대 오른쪽 끝 1280×720(x1280, y48)을 원배율로 세로 배치하고, 아래에 원본 시설/새 벽화, 2차/3차 바닥 이음, 2차/3차 돌판과 긁힌 흔적을 최근접 2배 확대해 비교했다. 비교 조각은 각각 원본 320×180px이다.
- 저장한 WebP를 다시 읽어 `../ref/room13-pixel-ready-facility0177-{시간대}.webp`와 x0~2047 전체를 비교했다. 세 시간대 모두 변경 픽셀 **0**, 최대 채널 차이 **0**. `work/validation3.json`에 기록했다.
- 통과한 장작 창고 및 게임 파일은 이번 작업에서 수정하지 않았다. 작업 시작 전에 있던 게임·미리보기 변경도 건드리지 않았다.

### 수정 내용과 방법
- 내장 image_gen 편집으로 오후 확장부를 다시 그렸다. 2차의 중앙값 필터, 32색 제한, 3px 최근접 확대를 적용하지 않았다. 벽화의 큰 블록을 줄이고 작은 경계를 살렸다. 산길, 둥근 돌 장치와 방사광, 손을 모은 벽화 속 사람 기호, 바랜 도장과 일부 벗겨짐을 유지했다. 실제 인물, 쇠·사슬, 읽을 글자, 정답 표시는 추가하지 않았다.
- 기둥 옆 오른쪽 회벽에 짧은 가로 긁힘을 세로로 늘어놓았다. 읽을 이름 대신 칼로 긁은 목록 흔적으로 표현했다.
- 돌판에 두꺼운 회색 측면, 깨진 윗면과 단면, 바닥 접촉 그림자와 음각 줄을 넣었다. 벽에 기대 놓인 깨진 석판으로 수정했다.
- 오후 구도를 기준으로 아침·저녁 조명을 별도 편집했다. 아침은 청보라 주변광과 연한 복숭아색 창 빛, 오후는 따뜻한 벽과 이어지는 사선 창 빛, 저녁은 창 빛을 지운 청보라 어둠으로 맞췄다.
- 바닥은 추가 이미지 편집으로 오른쪽으로 올라가던 가로 줄눈을 내려가는 방향으로 바꿨다. 중앙 이음에서 갈라지던 깊이 줄눈도 기존 방향으로 이어지게 정리했다. 이 바닥 조각을 세 시간대에 공통 합성하고 원본 바닥 중간색 비율로 시간대 색을 맞췄다. 돌판과 접촉 부분은 각 시간대 편집본을 보존했다.
- 생성본은 `work/facility3-*-generated.png`, 바닥 수정본은 `work/facility3-floor-generated.png`, 합성·검증 및 미리보기 코드는 `work/assemble3.py`에 보관했다. 생성본은 1024×768 문맥 조각에 맞춰 Lanczos 축소한 뒤 오른쪽 512px만 사용했다. 최종 왼쪽 2048px은 생성본을 사용하지 않고 원본에서 그대로 복사했다.

### 사용 프롬프트 세트 (내장 도구, CLI/API 미사용)
1. 오후 편집: “precise-object-edit; preserve camera, structure and entire LEFT HALF pixel positions; RIGHT HALF only: redraw faded mural with sharp fine 1–2 pixel edges and flat color shapes matching left original artwork resolution, NOT chunky 6px pixel blocks, no blur or stippling.” 산길 끝 둥근 돌 장치·방사광·손 모은 벽화 인물, 바랜 색·벗겨짐, 기둥 옆 목록 모양 긁힘, 두꺼운 회색 돌판과 깨진 단면, 줄눈 연속성, 오후 창 빛을 지정했다.
2. 아침: “FIRST image is exact geometry MASTER; change ONLY lighting and colors to MORNING matching second reference: cool lavender blue plaster and floor, pale peach sunlight diagonals in exact master positions, muted blue faded mural, brown timber. Do not copy chunky mural from second.”
3. 저녁: “FIRST image exact geometry master; change ONLY colors/lighting to EVENING matching SECOND reference: cool dim blue purple plaster and floor, dark brown timber, subdued muted blue purple mural. Remove ALL sunlight stripes and hard sunlit highlights including on stone and baseboard.”
4. 바닥 재편집: “Correct ONLY floor tiles in RIGHT HALF. The horizontal grout lines currently slope UP toward right, this is incorrect. They must slope gently DOWN toward RIGHT exactly continuing left half tile crosslines. At image center x724, existing crosslines arrive y~941 and ~1015 in this 1448×1086 image. Continue these diagonally DOWN to right with slope +0.10. The near vertical tile depth lines should also continue the existing LEFT floor vanishing direction. No crossing chevrons, no new vanishing point at center pillar.”

생성 기반 편집이므로 원본 작화와 붓·팔레트가 수학적으로 동일하다는 보장은 없다. 왼쪽 원본 보존은 수치 검증했고, 확장부의 선명도·돌 재질·이음은 2배 비교 조각으로 검수할 수 있게 했다.
