# 대화 스티커 추가 적용

소유자 「대화 창도 확인 / 지도 월드맵도 확인 / 캐릭터 대화 이미지도 스티커로 변경」 및 요청서 확인 후 「적용 해」 지시 범위.

- 받은 primary50 전신 50개를 모두 연결했다. 기존 46개는 그대로이며 보류됐던 초롱 angry·joy·surprise_talk / 선생님 surprise_talk 4개를 추가했다.
- 이전 보류 사유는 기존 원화 발 하단이 캔버스 밖으로 나갔기 때문이다. 새 원본 픽셀은 수정하지 않고, 기존 표시 높이·가로 중심을 유지하면서 하단을 캔버스 안으로 제한했다. 실제 12개 프로필 좌표는 `body-clipping-fix.json`에 기록했다.
- 얼굴 50개는 납품 원본 SHA-256과 대조해 `game/assets/dialogue-b-faces/`에 바이트 그대로 복사했다. 등록은 `room13-dialogue-b-faces.json`, 선택 함수는 `r13_bdialogue_face(person,expression)`이다.
- 전달한 현재 표정과 같은 얼굴만 선택한다. surprise→surprise_talk, flustered→anxious는 기존 전신 렌더러와 같은 별칭이다. neutral·미납품 인물·아빠·불러올 수 없는 파일은 None으로 반환한다. 없는 표정을 웃는 얼굴로 대체하지 않는다.
- 기존 전신 neutral, 특수 동작, 회의 전신, 대사·화자·표정 키·조건·반응 타이밍은 보존했다.
- 기본 37명·얼굴41 / 다람 표정5 / Supporting60 / Residents70은 미납품이므로 연결하지 못했다. 모든 인물의 기본 얼굴과 전신이 스티커로 바뀌었다고 보지 않는다.

## 검증

`python3 -m unittest discover -s dev -p 'test_b_dialogue*.py'`: 7개 통과. 전신 150개 프로필 기하·기존 neutral 보존·특수동작/회의 분리, 얼굴50개 출처 해시·아빠 제외·없는 표정 미대체를 검사했다. 실제 화면·네이티브·웹 검증은 통합 담당이 수행한다.
