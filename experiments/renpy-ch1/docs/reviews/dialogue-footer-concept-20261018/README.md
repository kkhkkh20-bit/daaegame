# 대화 하단 UI 시안 — 추천안

최신 3차 시안: [PC 질문 화면](v3/08-pc-questions.png) · [모바일 질문 화면](v3/07-mobile-questions.png). 날짜 패널과 더보기 우측 여백을48로 맞추고, 인물 이름·질문 제목만 정식 Galmuri11 Bold로 강조했다. 라이선스·출처는 game/assets/Galmuri11-Bold-OFL.txt와 docs/design/GALMURI_BOLD_PROVENANCE.json. PC/모바일 실제 렌더링 및 기존 시안 동작 검사를 통과했다.

최신 2차 시안: [대화창](v2/01-pc-dialogue.png) · [질문](v2/08-pc-questions.png). 현재 대화 건너뛰기를 하단에 꺼내고 더보기에서는 중복 제거했다. 기록·더보기 폭은 둘 다160이다. 확인창은 유지한다. PC/모바일 폭 일치와 직접 건너뛰기 확인창 취소, 자동·기록·제시 복귀 검사를 통과했다. 결과는 v2/report.json.

아래는 최초 시안 기록이다.

별도 design/dialogue-footer-concept-20261018 브랜치의 실제 게임 실행 화면이다. 메인/공개 게임에는 적용하지 않았다. 렌더링 시안용 생성 preview는 커밋하지 않는다. 상세 설계는 ../../design/DIALOGUE_FOOTER_PROPOSAL_20261018.md.

대사를 읽을 때는 기록·더보기 두 개만 오른쪽에 두고, 질문을 고를 때만 자료 보여주기를 같은 줄 왼쪽에 추가한다. 백로그·자동·빠른 읽기는 더보기에 모은다. 버튼 시각 높이56, 아이콘20, 글자22, 간격16을 공유한다. 모바일 입력 영역80은 유지한다.

- [PC 대화창](01-pc-dialogue.png)
- [PC 질문 화면](08-pc-questions.png)
- [PC 더보기](02-pc-more.png)
- [모바일 대화창](03-mobile-dialogue.png)
- [모바일 질문 화면](07-mobile-questions.png)
- [모바일 더보기](04-mobile-more.png)
- [건너뛰기 확인창](05-mobile-skip-confirm.png)
- [자동 읽기 정지 표시](06b-mobile-auto-running.png)

실제 할머니 첫 인사와 질문을 사용했다. 더보기 열기, 건너뛰기 취소 후 같은 대사/게임 상태 유지, 백로그 복귀, 자동 읽기 켜기와 표시를 눌러 정지, 자료 제시·기록 취소 후 같은 질문 복귀를 확인했다. AFM이 켜진 질문 화면에서도 자동 정지 표시와 돌아가기 버튼이 겹치지 않는다. 기록 읽음 표시는 UI 필드로만 변한다. 전체 이야기·회의 재검수는 아니다. 결과 report.json, 재현 dev/qa_footer_concept.py.
