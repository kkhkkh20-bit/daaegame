# 최신 UI 실제 런타임 검수

기준 main `83102b0993c77ceaea131b4fdf3f95a27bd21a2d`, 기존 웹 빌드의 엔진 확인 버전0.20.28. 이전 a23138f 이후 다른 Codex의 폰트·얼굴·메인·옵션 변경을 보존했다. .agents/skills 파일은 현재 checkout에 없으며 AGENTS 및 운영 안내를 확인했다.

## 확인 및 수정

- 기존 저장소 웹 실행본을 localhost:8765에서 /usr/bin/chromium으로 실행했다. 메인·질문·마차 선택 PC/모바일 캡처를 직접 확인했다. 별도 데스크톱 SDK 실행이라고 표시하지 않는다.
- 질문 카드 b_panel_card 원본은 얇은 외곽선이며 실제 질문 샘플도 같은 종이 카드로 나온다. 이미 해결된 제목 찌그러짐/질문 뒤 대사 겹침을 새 결함으로 보고하지 않았다.
- 마차 선택의 R13ReferenceChoice는 아직 ui-night의 갈색 카드와 불투명 번호 상자를 사용했다. 기존 승인 B 종이 카드 normal/hover로 연결하고 글자·번호를 갈색으로 맞췄다. 원본 PNG 추가·재생성 없음.
- R13ReferenceChoice는 일반 선택도 공유하므로 기본 표시를 유지하고 마차 호출에만 parchment=True를 지정했다. 좌표·600px 너비·80/88px 높이·padding·글자 크기·줄바꿈·번호키·ready·action·대사·분기·주민·회의·지도·옵션은 그대로다.

## 화면 증거의 범위

captures/carriage-before.png와 carriage-after-runtime.png는 같은 입력/배경의 실제 엔진 캡처다. 모바일과 hover도 별도 기록했다. QA는 임시 화면에 샘플 문구와 무해한 선택 콜백을 넣어 비교했다. 자연 플레이 특정 장면을 완주했다는 의미는 아니다.

수정 후 화면은 기존0.20.28 웹 엔진에 변경한 Python 표시 클래스와 screen 소스를 메모리에서 불러온 검수 결과다. 지원된 기존 renpy_exec 연결과 엔진 load_string을 사용했다. preview/room13-dev 파일은 수정하지 않았다. 새 웹 패키지를 빌드·배포한 결과가 아니며, 신규 패키지 통합 검증은 남아 있다. 재현 스크립트 qa_runtime.py는 로컬 서버8765가 필요하다.

## 막힌 부분 및 보류

- 공개 URL 직접 접속: net::ERR_TUNNEL_CONNECTION_FAILED. 우회하지 않고 이미 받은 저장소의 로컬 실행본을 사용했다. 현재 공개 서버의 archive_sha와 최신 checkout 일치는 미확정이다.
- Library 최신8화면(libfile_24d4c1d7572481919b3efb8018a3f2fc): 새 공식 helper·companion을 같은 디렉터리에 두고 complete transfer를 materialize에 전달했으나 `library file transfer failed: download failed`. HTTP 상태/권한 거부 여부는 반환되지 않았다. signed URL 방식이므로 없는 workspace_path 재시도 조건은 해당하지 않는다. 동일 실패 반복·raw URL 다운로드 없음.
- 새 UI kit(libfile_0dc63a1895148191ae2d630cbfd9801a), 메인/선택 참고 시안은 준비 응답만 받았으며 다운로드 성공이나 픽셀 확인을 주장하지 않는다. 신규 메인 버튼/대사 이름표·아이콘·미승인 얼굴 크기 변경은 보류했다. 불필요한 장식은 추가하지 않았다.
- /workspace/renpy-sdk/renpy-8.5.3-sdk/renpy.sh는 현재 설치되어 있지 않다. 과거SDK403/거부된 경로·artifact 접근은 재시도하지 않았다. SDK lint·새 웹 빌드 미실행.

이번 브랜치는 UI 일부의 검수·수정이며 전체 UI 완료가 아니다. 병합·배포하지 않는다.

## 검사 결과

- 전체 단위978개 통과(44.737초), 관련 입력/질문배치/선택길이6개 통과. git diff --check 통과.
- 실제 웹 엔진 임시 소스 검수: PC1280×720/모바일844×390, 긴 문구, hover, 반복 열기·닫기3회, 번호키2와 터치2번 동일콜백 실행 통과. pageerror 없음.
- 초기 QA 스크립트에서 호출간 임시변수 유지 가정 오류를 발견해 store에 결과를 보존하도록 수정했다. 최종 재실행 통과. 게임 코드 결함으로 분류하지 않는다.
- SDK lint, 새 패키지 빌드/실행, 공개본 최신SHA 검증은 미실행 또는 미확정.
