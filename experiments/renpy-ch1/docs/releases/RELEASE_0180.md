# 0.18.0-dev · 2026-10-14 — 구조 리팩토링 (소유자 지시)

목표는 두 가지였다. 첫 로딩을 줄이고, AI와 사람의 수정·검사·배포를 빠르게 하는 것이다. 게임 내용(대사·규칙·화면 배치)은 바꾸지 않았다. 다만 아래 "보이는 변화"의 두 가지는 예외다.

## 첫 로딩

- 예전: 250MB 압축 파일 하나를 다 받고, 브라우저 메모리 안에서 다시 풀었다.
- 지금
  - 핵심 zip(엔진 쪽 파이썬·스크립트·작은 파일)은 7.5MB다.
  - 그림·글꼴 175개(약 58MB)는 시작 전에 6개씩 병렬로 받아 게임 폴더에 바로 쓴다. 다시 풀지 않는다.
  - 배경음악은 Ren'Py progressive download로 필요할 때 받는다. 시작 8초 뒤부터 미리 받아 둔다.
- 그림은 무손실 WebP에서 품질 95 WebP로 바꿨다(투명도는 무손실).
  - 3배 확대 비교에서 구별되지 않았다(PSNR 36~39dB).
  - 그림 전체는 222MB에서 약 55MB가 됐다.
- 글꼴
  - 쓰지 않는 Room13Title.ttf(3.1MB)를 뺐다.
  - Room13Sans는 ✓ 같은 기호만 남겨 4.9MB에서 0.2MB가 됐다.
- 측정(로컬 서버, Chromium, 회선 5MB/s 제한, 캐시·서비스워커 없음)
  - 받은 양: 289MB → 113MB. 113MB 중 37MB는 고정된 Ren'Py 엔진이다.
  - 메인 화면까지: 70.6초 → 32.9초.

## 작업 구조

- 원본을 `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip`에서 `experiments/renpy-ch1/` 일반 파일로 옮겼다.
  - 예전 저장소의 `experiments/renpy-ch1`(2026-10-12의 오래된 사본)은 대체했다.
  - 그림 원본은 예전에는 지난 공개본 안에만 있었다. 이제 `game/assets/`에 있다.
- 빌드: `dev/build_web.py`가 지난 공개본 없이 원본만으로 만든다. 10초 남짓 걸린다(예전 수 분).
  - 예전 `package_web_webp.py`와 루트의 `build_web.py`·`prepare_assets.py`는 삭제했다.
- git 증가: 바뀌지 않은 그림은 같은 파일로 남아 다시 쌓이지 않는다.
  - 예전: 판마다 250MB.
  - 지금: 판마다 핵심 zip 7.5MB + 바뀐 파일.
- 검사 도구
  - `dev/check.sh`: 단위 테스트 100개 + lint, 약 2초.
  - `dev/run_renpy_tests.sh`: Ren'Py 화면 테스트 12개, `game/qa_tests/`.
  - 브라우저 QA: `dev/qa_carriage.py`, `dev/qa_navigation.py`, `dev/qa_save_slots.py`. 보조 기능은 `dev/webqa.py` 하나로 합쳤다.
- 정리
  - dev의 쓰지 않는 스크립트 119개를 삭제했다(버전별 QA, 갤러리, 예전 포장기, 재현되지 않는 콘텐츠 생성기).
  - QA 결과 폴더 16개를 소스에서 뺐다.
  - 판 기록은 `docs/releases/`로, 예전 인계 기록은 `docs/history/`로 옮겼다.
- 함수 덮어쓰기
  - `dev/override_map.py`가 24개 함수의 층 순서를 계산해 `docs/OVERRIDE_MAP.md`를 만든다.
  - 실제 실행 순서(Ren'Py `override_chain` 테스트)와 24개 모두 같았다.
  - 버려진 정의 2개를 지웠다: `room13_life.rpy`의 `r13_met_people`, 덮어써지던 `r13_learning_archive_keys`. 후자는 원래 자리에서 "앞 회차 없음" 규칙대로 `[]`를 돌려준다.
  - `systems/room13_items.rpy`를 init 95에서 96으로 옮겼다. 파일 이름이 층 순서를 정하던 유일한 경우였다. 바뀐 두 층은 모두 거르기만 하는 층이라 결과는 같다.
  - `test_override_map`이 새 충돌·버려진 정의·지도 미갱신을 잡는다.
- 테스트 수정
  - 디자인 원본 PNG 해시를 보던 테스트 2개를 `game/assets`의 크기·비율 확인으로 바꿨다.
  - 앞 회차 기록 표시를 기대하던 학습 테스트 2개를 "앞 회차 없음" 규칙으로 바꿨다.

## 보이는 변화

- 그림이 손실 압축으로 바뀌었다. 보통 화면에서는 차이가 없다.
- 하단 보조 버튼 글씨(`r13_footer_button`)를 Noto Sans KR Thin에서 Galmuri11로 바꿨다. 0.17.23에서 UI 글꼴을 Galmuri로 통일할 때 남은 곳이다.

## 검증

- 단위 테스트 100개 통과, Ren'Py lint 통과.
- Ren'Py 화면 테스트 12개 통과: newgame, carriage_skip, carriage_view, fresh_run, items_chain, shop_flow, trial_missing/giveup/win/full, finale_win/missing.
- 브라우저: 마차 장면, 마을 이동·저장/불러오기, 저장 슬롯 화면. 결과는 커밋 메시지에 적는다.
