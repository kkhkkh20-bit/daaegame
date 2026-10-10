1장 v2 소스 — 별도 미리보기 배포 (2026-10-10)
- 공개 play.html은 이 폴더가 아니라 dev/ 바로 아래 소스(5ae250d 대본 + 43_council 원탁 복구)로 만든다.
- 이 폴더: 오늘 오전 확정 구조(세련 인수 대리인·노름, 솜솜 침대 밑, 너울 수색) + 조사 확장(방마다 살펴보기, 인물별 질문, 증인에게 증거 보여 주기)
  + 회의 구조(결론 고르기 ask, 주민별 표 바뀜 votes, 휴회 adjourn, 힌트 단계화) + 음악 큐시트 + 사용자 '훅만'(Notion 1막 큰 그림의 훅) 반영 중.
- 빌드(2026-10-10 Codex): 저장소 루트에서 python3 preview/ch1-gpt-20261008/dev/wip-v2/build.py
  실행 위치에 무관하게 이 폴더 소스를 읽고 Git의 164838b 기준본을 사용한다. Node와 Python, 해당 Git 이력이 필요하다.
  출력: 이 폴더 build/play_v2.html, 시험 전용 build/playT.html. build/는 Git에서 제외한다.
  공개 play.html과 공개 dev/build.py는 덮어쓰지 않는다.
  pro_new.js·gen/end_gen.js는 기존 생성 결과물을 유지한다. 입력 JSON이 없으므로 conv.py는 실행하지 않는다.
- 로컬 미리보기: python3 preview/ch1-gpt-20261008/dev/wip-v2/preview.py --port 8000
  http://127.0.0.1:8000/play_v2.html (v2), /playT.html (개발 시험 전용).
  기존 preview 폴더의 자산을 연결한다. 배포 작업은 하지 않는다.
- 브라우저 회귀 검사: 서버를 켠 뒤 python3 preview/ch1-gpt-20261008/dev/wip-v2/qa_flow.py
  Python Playwright와 Chromium 필요. 증거를 준비한 시험 상태에서 회의→최종 대결→후일담을 검사한다.
  --retry: 정답 선택 후 재시작해 같은 결론 선택지가 다시 나타나는지 검사한다.
  --failure: 실제 오답 5회 → M-F → 증거 유지·설득력 복구를 검사한다.
  --failure --final: 최종 대결에서 같은 실패 검사를 한다.
  새 게임의 조사 전체 완주·실기기·청취 검사를 대신하지 않는다.
- 2026-10-10 훅 연출 요청(dot) 반영: 콜드오픈 8비트(자정), P1+P3 압축, P5 문소리 끊기, P10 압축+밤 장면, P12 수색 장면, P13 할머니 베개 구석 훅·세련 '나머지 이백 냥' 추궁·너울 물러서지 않음, 다람 첫 단서 한 줄, 침대 밑 솜솜 발견 자동 진입(정적).
- 46_meet_gate: 회의 물음(C01~C04)은 유지, 주민 소집 장면(I9)은 '원탁 회의 열기'를 고른 뒤에만 재생.
- 클라우드 Playwright 완주(새 게임→후일담) 844×390·1180×820 확인. 실기기·청취 확인 아님.
- 설계 문서: CH1_V2_DESIGN.txt (Notion 훅 반영 전 기준).

- 2026-10-10 Codex: 좁은 세로 화면의 장소 이름표를 상단 메뉴 아래로 이동.
- 47_retry_choices: 회의/최종 대결 재시작 시 지난 정답 기록도 초기화(첫 결론 선택지가 생략되는 오류 수정).
- 이번 검증 기록과 남은 검수: CODEX_QA_20261010.txt
- 48_audio_lines: 원탁 대사를 음악/효과음 큐에 연결.
- 49_retry_pending: 재시작 전 대기열과 지연 처리 초기화.
- 50_required_choice: 필수 결론 선택 전 빠른 넘기기 방지.
- 오디오 검사: 서버를 켠 뒤 python3 preview/ch1-gpt-20261008/dev/wip-v2/qa_audio.py
  실제 청취 대신 큐 전환과 오프라인 신호를 검사한다.
- 대사·스토리·오디오 검수: CODEX_STORY_AUDIO_20261010.txt
- 솜솜 발견 장면 검사: 서버를 켠 뒤 python3 preview/ch1-gpt-20261008/dev/wip-v2/qa_somsom.py
  가로/세로에서 발견 전 음악 중단, 긴장 유지, 종료 후 음악 복귀를 검사한다.

- 사용자 배포 요청에 따라 별도 v2 주소를 공개한다:
  https://kkhkkh20-bit.github.io/daaegame/preview/ch1-gpt-20261008/v2.html
  preview 루트의 v2.html은 기존 화면 맞춤 래퍼를 재사용하고 play_v2.html을 연다.
  기존 index.html/play.html 및 루트 공개 게임은 유지한다. 미승인 아트 변경 없음.
  갱신: python3 preview/ch1-gpt-20261008/dev/wip-v2/publish.py 실행 후 커밋한다.
  실제 v2 빌드를 복사하고 파일 해시로 게임 iframe의 캐시 버전을 갱신한다.
  build/playT.html은 시험용 평가 함수가 있으므로 배포하지 않는다.
  GitHub Pages는 main / 루트를 배포한다.

- 이야기 논리 검사: qa_story.py (발견 위치 공개 순서·상자 허락), qa_intro.py (새 게임 도입).
- qa_flow.py --without-ledger: 선택 장부 C11을 얻지 않은 경로에서도 결말까지 진행한다.
- 전체 동기·인과관계 검수: CODEX_STORY_LOGIC_20261010.txt
