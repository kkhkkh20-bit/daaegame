# 공통 UI 정리 — 0.19.57

실제 공식 웹 빌드를 Chromium에서 점검했다. PC1280×720, 휴대폰844×390. 전체 이야기 플레이 검수가 아니라 UI와 관련 조작의 범위 검사다. 0.19.56 이야기 흐름 변경을 병합한 빌드를 사용한다.

- 휴대폰에서 글자 확대를 꺼도 공통 버튼 높이80. 마우스 전용 환경에서는64.
- 여관 목록과 마을 건물 선택·취소는 실제 게임 상태 전체를 유지한다. 이동/복귀는232×80으로 일치한다.
- 자료1개에서 불필요한 분류를 숨기고 실제 버튼으로 출처를 펼치고 접었다.155개 소유 자료 UI fixture에서는3열/8개 페이지와 다음 쪽, 필터 영역 경계를 검사했다.
- 조사 안내는3초 후 접히며 장소명에 현재 모드가 남는다. 빈 배경을 실제 터치했을 때 피드백 화면이 나타나고 사라지며 게임 상태 전체는 같았다.
- PC와 터치 각각 실제 초소 선반 조사로G1을 획득하고 돌목에게 제시해 입장 정정을 완료했다. 여관 열쇠·장부 직접 조사와 실제 스와이프640→280도 통과했다.
- 단위 검사와 Ren’Py lint, 공식 웹 빌드 통과. 기존 분리 실행형 기록 검사에는 공통 모바일 판정 의존성을 주입하고 보통 글자/모바일8개 페이지 검사를 보강했다.

## 실제 화면

- [모바일 지도 선택](ui/04-mobile-map-selected.png)
- [모바일 기록](ui/06-mobile-records-folded.png)
- [출처 펼침](ui/07-mobile-records-origin-open.png)
- [배경을 가리지 않는 조사 화면](ui/08-mobile-investigation-clean.png)
- [자료155개](ui/09-mobile-dense-records.png)
- [마우스 화면](ui/11-pc-mouse-field.png)
- [실제 자료 제시](direct-investigation/mobile-owned-record.png)

결과 JSON은 ui/report.json과 direct-investigation/report.json. 테스트는 dev/qa_ui_polish.py와 dev/qa_direct_investigation.py.
