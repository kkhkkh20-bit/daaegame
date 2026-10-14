# 생성 프롬프트 구성 기록

도구: built-in `image_gen__imagegen`만 사용. `transparent_background=false`. 각 파일은 독립 호출로 생성했다. 기존 참조 파일은 먼저 직접 보았다. 아래는 호출에 사용한 최종 프롬프트의 구조화 기록이며 모델 seed/결정론적 재현을 보장하는 명세가 아니다.

## 공통
- 기존 배경과 동일한 chunky clean pixel-art, crisp stepped silhouettes, broad low-noise colour clusters, warm wood/cream plaster/blue bedding.
- No smooth painting, photorealism, characters, hands, text, labels, arrows, UI, magic or extra doorway.
- 기존 상태 편집은 camera, framing, every stationary object, time-of-day colour를 유지하고 목표 장치/소품만 변경하도록 요청.
- 확대는 16:9, wide는 2048×768 /8:3 요청. 실제 출력 크기는 manifest에 별도 기록.

## kitchen-lever-off
Reference: kitchen/afternoon.png. 선반 아래 작은 숨은 기계장치의 1인칭 상세. 덮개를 왼쪽으로 미는 rail, 중간 pivot의 나무 손잡이 철제 레버 DOWN, wall로 들어가는 느슨한 steel cable, 위쪽 fixed retaining notch. 선반 접시 일부와 왼쪽 후면문 목재로 위치 연결. 유지식 기계 구조이며 전선/불빛/손 없음.

## kitchen-lever-on
Edit target: off. Canvas 1672×941와 주변 물건·덮개·pivot·케이블 출구 유지. 레버만 위로 올려 기존 retaining notch에 걸고 cable을 팽팽하게 변경. 유지식 상태이므로 붙잡는 손 없음. 고정부품 추가/카메라 변경 금지.

## book-latch-locked
Reference: room-before/afternoon.png. 우측 책장 하반부에 가까이 낮춘 카메라, 왼쪽 파란 침대와 오른쪽 전경 원래 바구니. 하부 목재 push-in panel CLOSED, 그 위 낮은 책칸 오른쪽 dark-red leather spine with gold bands를 조작 손잡이로 명확히 노출. 책/파란 상자/목재의 원래 색감. 경첩·문고리·일반 정문 없음. 공간 재구성은 QA에서 별도 승인사항으로 기록.

## book-latch-open
Edit target: locked. 같은 camera/책/침대/바구니/조명 유지. 오른쪽 붉은 책을 아래에서 누른 후 왼쪽 약25도 tilt. 하부판은 안쪽으로 들어가 출입구를 막지 않고 좁은 descending stone steps가 어둠 속으로 내려감. Hinged door/ascending stairs/magic portal 금지. Inside right manual-release handle.

최종 추가 교정: open + passage/afternoon 두 참조. open의 composition을 고정하고 inside-right의 작은 고리만 passage 참조의 dark vertical iron plate + short brown wooden-gripped lever pointing down-left + pivot으로 교체. 이 최종본의 실제 폭은 1671px로 나와 그대로 보존함.

## room13-passage-open-{morning,afternoon,evening}
각 원래 room-before/{period}.png를 독립 편집. 2048×768 ultrawide8:3 full room. far-right bookshelf lowest bay 안쪽만 shadowy pushed-in opening으로 변경. 기존 basket/towel 그대로; 위 책/머그/상자/식물 그대로. 어두운 gap과 아래로 떨어지는 threshold의 얇은 edge만, rising stair flight 금지. 오른쪽 작은 붉은 book handle. 바구니 obstruction을 해결하려고 책장 확대/바구니 이동/새 문 추가 금지. Before incident: upright tabletop candlestick, intact rug/bed.

- Afternoon 초기의 올라가는 계단처럼 보이는 flight를 삭제하도록 원래 source에서 다시 생성.
- Morning 초기 바구니 drift를 교정하려 원래 source에서 다시 생성. Basket 기준 top y443 / bottom y566 / x1601..1761 명시.
- 최종 3장은 obstruction을 유지한 작은 틈 시안이며 입구 통과 기하를 완성했다고 주장하지 않음.

## room13-after-evidence-removed-{morning,afternoon,evening}
각 원래 room-after/{period}.png를 독립 편집. 2048×768 원래 framing/lighting/architecture를 유지. floor upper-left rug corner, right of chair/in front of bed around x1000..1108,y550..610의 TWO BRASS CANDLESTICK FRAGMENTS만 제거. 흰 candle stub x1080..1134,y575, wax drips, small local black scorch, singed rug edge, intact blue bed 유지. 탁자 촛대 재생성 금지. 새 불/연기/사람/흉기/핀 금지.

결과는 금속 두 조각은 제거했지만 wax/작은 갈색 자국이 시간대별로 재생성/소실되어 QA에 정확히 기록함. 프롬프트의 보존 요청이 결과의 픽셀 보존 검증을 뜻하지 않음.
