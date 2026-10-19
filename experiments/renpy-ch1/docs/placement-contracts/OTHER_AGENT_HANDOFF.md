# 다른 작업자용 인수인계

## 작업 시작

1. 이 문서와 README를 먼저 읽고 현재 checkout commit을 확인한다.
2. `dev/placement-contract-preimages.json`과 guard로 실제 원본을 검증한다. 불일치를 우회하거나 guard를 지워서 통과시키지 않는다.
3. 기본 OFF를 유지한다. 이 패키지의 공유 자체는 활성화·병합·배포 지시가 아니다.
4. 기존 staging wrapper, 일정, offer, life_group, 원화 및 native QA 파일을 덮어쓰지 않는다. 후속 수정은 별도 제한된 변경으로 검토한다.

## 세 가지 교체

### 같은 인물, 호환 포즈

- 등록된 정확한 pose를 사용하는 approved asset이어야 한다.
- contact, facing, 발/손/좌판 기준점, uniform scale, 2차 접촉을 모두 검사한다.
- `post.afternoon.seryeon`의 asset을 `seryeon.chair_read`에서 `seryeon.chair_listen`으로 바꾸는 검사 예제가 있다. geometry 좌표는 편집하지 않는다.
- 기존 승인 포즈의 활동 문구를 재사용한다. 없는 포즈나 문구를 neutral/추측한 행동으로 바꾸지 않는다.

### 다른 인물

- 원래 시나리오 roster가 먼저 그 인물을 그 장소/날짜/시간에 포함해야 한다. registry는 인물을 새로 생성하지 않는다.
- 해당 인물 asset의 정체성, 역할·접촉·방향 계약이 슬롯과 맞아야 한다. 새 직업이나 스토리를 추정하지 않는다.
- binding의 actor/asset과 검증된 upstream guard 참조를 바꾼다. 슬롯 좌표를 사람마다 복사하지 않는다.
- 현재 예제에는 다른 인물의 호환 의자 포즈가 충분하지 않다. 강제로 눌러 맞추는 교체는 실패해야 한다.

### 새 원화/새 포즈

- 공유 원래 pose를 덮어쓰지 않는다. 검토된 소스만 `pc_` 격리 alias로 등록한다.
- `status=approved`와 `source_quality.status=reference_reviewed`를 모두 요구한다. 승인 전 후보 이미지는 포함하지 않는다.
- exact Git blob, source_size, crop, alpha_bounds, head, crop 상대 anchors, contact, facing, 기존 승인 활동 문구를 검증한다.
- source quality와 renderer grid를 따로 평가한다. 큰 canvas나 nearest/grid 변경만으로 거친 원화 문제가 해결됐다고 판정하지 않는다.
- alias는 init에서 등록하며 재시작이 필요하다. 같은 revision/path의 파일을 실행 중 덮어쓰는 방식은 지원하지 않는다.

## 우선순위와 실패 동작

entry/활성 장면/미해결 offer는 전체 우회하며 기존 life_group은 그대로 둔다. 명단·스토리 플래그·날짜·직업을 변경하지 않는다.

정확한 pose 전체 spec, 원화 해시, 배경 file/crop/폭, 완전한 14개 upstream guard 필드가 일치해야 한다. 누락/불일치/부적합/얼굴 충돌 악화가 있으면 원래 장면 리스트를 그대로 반환하고 진단을 남긴다. default OFF는 원래 리스트 자체를 반환한다.

## 회귀 검사에서 보존하는 기술 기준

- 여관 누비: foot(420,535), height226, depth535, 기존 lounge 가구 가림.
- 여관 토실: 기존 init179의 위치·크기·가림. 이 registry는 토실을 연결하지 않는다.
- 우체국 오전 세련 C: hand(1566,432), rect[1403,340,195,234], depth560, 기존 counter mask. 이 registry는 오전 세련을 연결하지 않는다.
- 우체국 오전 2160 폭과 오후/저녁 1280 폭을 같은 좌표계로 취급하지 않는다.

이 값들은 현재 소스의 보존 조건이지 시각적 디자인의 최종 합격 선언이 아니다. 특히 세련 C는 오른쪽 서비스 창구에서 일하는 위치·동작으로 충분히 읽히지 않는 실험 배치이며, 배경과 업무 포즈를 다시 맞추는 수정이 필요하다. 클립보드를 들고 서 있는 C를 승인된 최종 working pose로 기록하지 않는다.

이 공유 패키지는 C를 자동 활성화하거나 임의의 새 배치로 대체하지 않는다. 오전 C binding은 계속 없으며 기존 코드·좌표·크기·가림은 기술 기준 그대로다. 후속 배경/업무 포즈 수정은 별도 변경으로 검증하고, 그 결과에 맞춰 사전조건과 fixture를 다시 확인한다.

## 후속 수락 기준

57개 소스 검사와 preimage guard가 먼저 통과해야 한다. 이후 실제 Ren'Py 시작/lint, 이전 save 로드, 상태 전환, offer/그룹, 넓은 배경의 카메라 양끝, 물체와 인물 클릭, 가구 뒤 몸·앞 손/소품을 검증한다. 얼굴 영역 충돌 검사만으로 몸/소품/알파 클릭까지 합격했다고 보고하지 않는다.

다음 작은 이관은 검토된 기존 슬롯을 그대로 재현하는 것부터 한다. 광장 단차, 주방 작업대, 진료소 침대는 각각 분리해서 검증한다. 미검증 장소에 좌표나 새 동작을 추정해 채우지 않는다.
