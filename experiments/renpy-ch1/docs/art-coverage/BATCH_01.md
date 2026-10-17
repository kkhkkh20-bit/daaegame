# 첫 제작 묶음 — 16장

기준 main `1f4f888` / 0.19.4. 아래 경로는 `experiments/renpy-ch1/` 기준이다. 기계용 `batch-01.json`에는 원본 SHA-256·크기·납품 파일명·현황 ID가 있다. 새 디자인 선택이 아닌 확정 디자인의 표정·동작 보완이다.

|순서|대상|필요 그림|승인 기준 원본|
|---|---|---|---|
|A1|돌목 guard|joy / flustered / angry / anxious / surprise, 5장|`art/role-connect-20261016/sources/approved/review-dolmok-mouth-v1.png`|
|A2|사자 선생님 resident_teacher|같은 5표정, 5장|`art/canonical48-rev45/originals/resident_teacher.webp`|
|A3|사자 선생님|write_attendance / collapse_attendance, 2장|위 도포 정본|
|B1|도토 doto|action_1 / action_2, 2장|`art/canonical48-rev45/originals/doto.webp`|
|B2|구슬 resident_guseul|living_stamp, 1장|`art/canonical48-rev45/originals/resident_guseul.webp`|
|B3|백 부인 resident_madam|living_inspect, 1장|`art/canonical48-rev45/originals/resident_madam.webp`|

## 장면 요구

- 돌목: 입구 명부 확인 대화. 승인 중립의 수정된 입을 나머지 5표정에 일치시킨다. 기존 그림의 표정/자세 참고는 가능하나 예전 입으로 돌아가면 안 된다. 조사 동작 입 수정은 다음 묶음이다.
- 사자 선생님 표정: 붉은 갈기·녹색 도포·띠·지팡이 유지. 조끼/바지 버전 금지. 감정만 바꾸고 키·캔버스·얼굴 기본 비율은 동일하게 한다.
- `write_attendance`: `game/systems/room13_ep5_soup.rpy`의 “하나도 안 틀렸지요”와 `room13_ep_story.rpy` 출석 대화. 출석부에 이름을 적는 자세.
- `collapse_attendance`: `game/systems/room13_ep6_cart.rpy`의 `teacher_on_cart` 조건. 출석부를 품에 안고 앉아 있음. 선 키로 늘리지 않는다. `wipe_board`는 현재 호출 줄이 없는 준비 그림이므로 이번 16장에서 제외하고 P1로 남긴다.
- 도토: `game/room13_acting.rpy`의 `r13_living_pose`, 2층 복도. 오전·오후 서서 수첩에 적기, 저녁 바닥에 앉아 책 읽기. 기존 일정은 바꾸지 않는다. 어린 사슴·파란 외투 유지. `docs/ART_REQUEST_01867_LIFE_ACTIONS.md`의 발 기준 (1471,616)은 적용 시 최신 맵에서 다시 확인한다.
- 구슬: 여관 및 기존 우체국 장면. 계약서에 눌렀던 도장을 천으로 닦는다. 긴 귀·주황 털·녹색 재킷. 도장과 천은 손에 포함하고 새 배경/책상을 만들지 않는다.
- 백 부인: 여관 대기자리에서 보관함 봉인 부위를 손으로 확인한다. 점박이 강아지·금발 유지. 판다 금지. 보관함의 실제 위치에 맞출 손끝 anchor가 필요하다.

## 납품과 승인

`art/incoming/art-coverage-batch-01/<character>/<channel>-<key>.png`에 한 파일당 한 그림을 납품한다. 이 폴더는 아직 생성된 그림이 있다는 뜻이 아니다.

- 원본 2×2 픽셀 셀과 투명 배경. 임의 리샘플링·벡터화·코드 생성 대체 금지.
- 동일 인물은 기준 캔버스와 발 위치 유지. 다른 셀 크기/비율로 납품됐다면 자동 변환하지 않고 검토한다.
- 대화 전신 표정과 현장 조사 동작을 구분한다. 중립 복제는 제작 완료가 아니다.
- 동작은 crop/head/foot, 손/좌면이 필요한 경우 hand/seat와 stature_ratio를 검수해 기록한다.
- 승인 → 원본 해시 등록 → 필요한 채널만 연결 → 정적 검사 → 해당 장면 실제 화면 검수 순서다. 승인이 아직 없으면 후보로 보관한다.
- 할머니 기존 디자인·나비 실내 교복·네로 정본·승인 겨울 행동은 변경하지 않는다. 겨울 옷 보완 6명은 후속 요청으로 분리한다.

실제 게임 화면 검수는 아직 실행하지 않았다. 기존 요청서의 좌표/과거 캡처는 참고 근거이며 현재 화면 합격의 증거가 아니다.
