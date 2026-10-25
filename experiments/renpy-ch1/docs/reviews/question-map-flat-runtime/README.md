# 질문·지도 버튼 연결 검증

기준 main: d3c0112345d58e81c0b2041fda0e9acc68986590 (0.20.52 계열), 로컬 변경 포함.

질문 하단 4개 및 지도 하단 전용 역할만 추가했다. PNG 원본과 catalog는 변경하지 않았다. 기존 연결 3178개 전체 불변, 전용 역할 4개/상태16개 추가. 현황판 UI 슬롯16개 증가, 전체848개/빈322개.

PNG8 모두 RGBA 160×52, 알파 경계 (16,10,144,42). 원본 전체 균일 확대만 사용, crop/Frame 없음. 기존 역할에서 클릭영역·내용 safe_size·icon_gap·글꼴·상태 이동량을 읽어 유지한다. 새 그림의 보이는128×32 영역이 기존 종이 영역 안에 들도록 배율을 정하며 전체 캔버스를 중앙 배치한다.

정식 경로 `python3 dev/asset_screen_examples.py` 실행: review_button_fit.capture가 xvfb-run 탐색 결과 None을 Path로 변환하다 TypeError 발생. SDK 기본 /tmp/renpy-8.5.3-sdk와 xvfb-run 모두 미설치. 실제 렌더·상태별 가독성·before/current 캡처 및 RenPy lint 미실행. 기존 screens 캡처는 보존했으며 새 결과로 제시하지 않는다. 자연 플레이 검증도 미실행.

후속 환경에서 RENPY_SDK와 xvfb-run 준비 후 dev/check.sh 및 dev/asset_screen_examples.py 실행 필요. 병합/배포 전 실제 질문·지도 PC/터치 및 네 상태 가독성을 확인해야 한다.

검사 결과: asset_toolbox validate 통과, test_button_fit_assets 3개 통과, test_asset_toolbox* 31개 통과, 전체 단위검사1104개 중1103개 통과/1개 오류. 오류는 shallow clone에 과거2ea4d41 객체가 없어 test_historical_semantic_revision_preserved_story_source의 git show가128로 종료한 환경 제한이다. Python init 블록 구문 검사와 git diff --check 통과.
