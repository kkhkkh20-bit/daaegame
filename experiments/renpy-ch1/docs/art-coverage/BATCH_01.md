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

## 현재 제작·수신 현황 — 2026-10-17

**원래 요청 16장 중 후보 15장 생성 보고, 백 부인 1장 미생성 보류. 배치 승인·게임 적용·배포 완료가 아니다.** 이 표와 `batch-01.json`은 부모 제작 보고를 기록한다. 이 실행 환경에서는 파일을 수신하지 못했으며 후보 원본 해시 검증과 실제 게임 검수는 수행하지 않았다. 기존 게임 연결은 유지한다.

|대상|제작 보고|검토·후속 작업|전달 자료|
|---|---|---|---|
|사자 선생님 5표정+2동작|후보 7장, 승인 대기|붉은 갈기·도포 기준 유지 보고. 생성 1004~1005×1566, 기준 985×1536과 다르며 임의 축소하지 않음. alpha·경계 여유·기준점 검토 및 실제 게임 검수 필요|[ZIP](https://chatgpt.com/api/library/files/libfile_622f1ccfe06481919f3cbd764f45de66/download) · [HTML](https://chatgpt.com/api/library/files/libfile_482b3922b8748191bb43f971f0d3b635/download)|
|돌목 5표정·도토 2동작·구슬 1동작|후보 8장, 승인 대기|제작자가 승인 원본 SHA 일치 확인 후 생성했다고 보고. 로컬 미검증. 기준 캔버스·발점 차이, 엄격 2×2 격자 미인증, 도토 쓰기 시선 추가 검토. 게임·보드 미연결|[ZIP](https://chatgpt.com/api/library/files/libfile_949c77d7c52881918204bb53456b56e6/download) · [HTML](https://chatgpt.com/api/library/files/libfile_2f2c2b7e907081918a3edfca85af97ab/download)|
|백 부인 living_inspect|1장 미생성 보류, 요청 유지|창고 이야기에는 존재하나 여관의 대상 물체는 미확정. [읽기 검토](BATCH_02.md#보관함-읽기-검토--기획-결정-필요)에 따라 장소·물체 기획 결정 후 접점 확인|아직 없음|

### 꽥순 — 원래 16장과 별도

사용자가 확정한 것은 [새 neutral](https://chatgpt.com/api/library/files/libfile_72a40de0b9f88191b32026bb52398807/download)뿐이다. 수신은 **blocked / 정상 첨부 전달 대기**다. 새 destination·새 전송으로 재시도했으나 helper `download failed`, 다운로드 호스트 HTTPS 터널 `403 Forbidden`으로 실패했고 파일 미생성을 확인했다. 차단을 우회하지 않았다. 새 neutral 원본 해시 검증·게임 연결·새 그림의 실제 게임 검수·배포는 미완료다.

추가 5표정은 모두 **미승인 후보**이며 부모 제작 보고만 기록했다. 로컬 파일 미수신·해시 미검증·게임 미연결·실제 화면 미검수다.

|표정|후보|
|---|---|
|joy|[Library](https://chatgpt.com/api/library/files/libfile_c798a0ddc7808191946453176bc65f95/download)|
|flustered|[Library](https://chatgpt.com/api/library/files/libfile_c069ec0ef4b88191a1c32bf45ffb93e3/download)|
|angry|[Library](https://chatgpt.com/api/library/files/libfile_f26106eac7d08191a4f0349bde8008c3/download)|
|anxious|[Library](https://chatgpt.com/api/library/files/libfile_aa51e37bc4188191a1f6100048c47a67/download)|
|surprise|[Library](https://chatgpt.com/api/library/files/libfile_970e2d4218008191bc35dd8660d4bcd1/download)|

[꽥순 후보 비교](https://chatgpt.com/api/library/files/libfile_f811c0fb7910819199a6a1c997f2e003/download). 기존 A/B/C 렌더 비교는 기존 그림의 표시 방식 실험이며 이 새 후보들의 실제 게임 검수 증거가 아니다.

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

- 2026-10-17 사용자 방향 승인으로 엄격 2×2 납품 요구를 대체한다. 선명도·입체감·다양한 상반신 연기와 원본 개성을 보존하고 굵은 2×2 블록으로 강제 재축소하지 않는다. 투명 배경과 최종 표시 품질을 검수한다. [후속 기준·요청](BATCH_02.md).
- 동일 인물은 기준 캔버스와 발 위치 유지. 다른 셀 크기/비율로 납품됐다면 자동 변환하지 않고 검토한다.
- 대화 전신 표정과 현장 조사 동작을 구분한다. 중립 복제는 제작 완료가 아니다.
- 동작은 crop/head/foot, 손/좌면이 필요한 경우 hand/seat와 stature_ratio를 검수해 기록한다.
- 승인 → 원본 해시 등록 → 필요한 채널만 연결 → 정적 검사 → 해당 장면 실제 화면 검수 순서다. 승인이 아직 없으면 후보로 보관한다.
- 할머니 기존 디자인·나비 실내 교복·네로 정본·승인 겨울 행동은 변경하지 않는다. 겨울 옷 보완 6명은 후속 요청으로 분리한다.

실제 게임 화면 검수는 아직 실행하지 않았다. 기존 요청서의 좌표/과거 캡처는 참고 근거이며 현재 화면 합격의 증거가 아니다.
