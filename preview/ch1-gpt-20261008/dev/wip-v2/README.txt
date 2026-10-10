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
  --retry: 첫 증거 제시 후 재시작해 증거 단계가 처음부터 다시 진행되는지 검사한다.
  --failure: 실제 오답 제시 5회 → 실패 → 증거 유지·설득력 복구를 검사한다.
  --failure --final: 최종 대결에서 같은 실패 검사를 한다.
  새 게임의 조사 전체 완주·실기기·청취 검사를 대신하지 않는다.
- 2026-10-10 훅 연출 요청(dot) 반영: 콜드오픈 8비트(자정), P1+P3 압축, P5 문소리 끊기, P10 압축+밤 장면, P12 수색 장면, P13 할머니 베개 구석 훅·세련 '나머지 이백 냥' 추궁·너울 물러서지 않음, 다람 첫 단서 한 줄, 침대 밑 솜솜 발견(정적·심박, 현재는 직접 조사로 진입).
- 46_meet_gate: 회의 물음(C01~C04)은 유지, 주민 소집 장면(I9)은 '원탁 회의 열기'를 고른 뒤에만 재생.
- 클라우드 Playwright 완주(새 게임→후일담) 844×390·1180×820 확인. 실기기·청취 확인 아님.
- 설계 문서: ../review/CH1_NEW_STRUCTURE.txt. 최신 노션 초안과 구현의 차이는 CODEX_AGENT_REVIEW_20261010.txt 참고.

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

대사 연타 입력 회귀 검사: python3 qa_input.py
수정 전 재현: python3 qa_input.py --baseline (cd0b802 비교)

- 사용자 요청으로 스토리·연출·오류 담당 에이전트 3개 독립 검수. 반영 내용과 검증 범위: CODEX_AGENT_REVIEW_20261010.txt

- 2026-10-10 에이전트 통합 검수: 1.8초 이후에도 지속되는 대사 연타가 조사로 넘어가는 오류 추가 수정. qa_input.py는 18회 연타를 검사한다.

- UI/메인 음악 개선: CODEX_UI_MUSIC_20261010.txt. inn_polish.js는 기존 화면 위에 디자인만 적용한다.
- 음악 소스: gen/music_v2.py. 재생 자산은 preview 루트 audio/v2/에 보관한다.
  재생성: python3 gen/music_v2.py (NumPy, libfluidsynth.so.3, TimGM6mb.sf2, ffmpeg 필요).
  일반 build/publish는 기존 MP3를 사용하며 악기 렌더 의존성이 필요 없다.
- UI/음악 통합 검사: 서버를 켠 뒤 python3 qa_polish.py (가로/세로, 설정, 증거 창, 실제 MP3 재생).

- 현재 조사→회의→대결과 아이콘 UI: CODEX_SIMPLE_UI_20261010.txt.
  조사로 증거 수집 → 회의에서 발언/증거 비교와 표 변화 → 대결에서 직접 증거 제시.
  inn_simple_ui.js가 원래 조작을 증거/질문/다음 아이콘으로 정리한다.
  별도 두 카드+결론 퀴즈와 '추리' 수첩은 제거했다. 단계별 증거 제시는 유지한다.
  CODEX_DEDUCTION_DESIGN_20261010.txt는 제거 전 설계 이력이며 현재 UI와 다르다.
  qa_logic_ui.py / qa_reasoning.py / qa_native_async.py / qa_investigation.py: 현재 UI/반박/비동기/조사 검사.
  qa_flow.py: 기존 회의와 대결의 실제 증거 제시로 결말까지 검사한다.

qa_saved_notebook.py --storage /tmp/investigation-after-linen.json: 실제 수집 저장으로 깨끗한 배포판의 이어하기·증거/증언 보존을 확인한다. 파일명은 이전 검사와 호환되며 수첩 퀴즈는 없다.

- 추리로 누명을 뒤집는 단계별 반전: CODEX_REVERSAL_20261010.txt.
  첫 반박의 실제 표 철회부터 최종 배상·여관 양도 요구 철회까지 qa_flow.py로 검증.
  qa_reversal_route.py: 관련 증거를 세련의 발언에 내도 감점 없이 나비의 발언으로 이어지는 실제 포인터 검사.

- 가족 설정·인물 관계 보강: CODEX_FAMILY_STORY_20261010.txt.
  전직 탐정이 가족 서점을 열었다는 과거, 엄마의 갑작스러운 실종,
  다람의 관찰 역할과 아빠의 보호 책임을 도입·조사·후일담에 연결한다.

- 피아노·관현악 음악 v2: CODEX_PIANO_MUSIC_20261010.txt.
  메인·이동·조사·사건·회의/압박·대결/압박·후일담·인물 7곡을 실제 피아노 녹음으로 제작.
  재제작 준비: python3 gen/fetch_piano_samples.py (악기 데이터를 Git 밖 캐시에 저장).
  재제작: python3 gen/music_piano_v2.py (NumPy, SciPy, ffmpeg, libfluidsynth).
  일반 build/publish는 커밋된 MP3와 inn_piano_tracks.js만 사용하며 큰 악기 라이브러리가 필요 없다.
  qa_piano_assets.py: 인코딩된 전체 16곡의 음량·최대 레벨·스테레오·반복 경계를 검사.
  qa_audio.py: 16곡 Web Audio 디코딩, 전체 메인곡 반복, 장면 큐와 음원 캐시 상한 검사.

- 가족의 감정선과 사건 뒤 일상의 회복: CODEX_EMOTION_20261010.txt.
  낭독 놀이, 다람의 기다림 인정, 아빠의 손잡기, 겨울 숙식과 솜솜의 잠자리 복귀.
  qa_intro.py / qa_flow.py --without-ledger가 재생과 감정 장면의 오디오 전환을 검사한다.
