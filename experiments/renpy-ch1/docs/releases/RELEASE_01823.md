# 0.18.23-dev · 2026-10-15 — NPC 4명 디자인 교체 (소유자 지시, 작업 브랜치)

## 범위

2026-10-15 소유자 지시로 받은 디자인 4개를 기존 NPC 4명의 그림에 적용했다. 새 주민은 만들지 않았다. 그 전에 받은 후보 90장은 적용하지 않았다.

| 디자인(전달 ID) | 적용 NPC | 종족 | 고른 근거 |
|---|---|---|---|
| 여우 마을복 `candidate_fox_town` | `resident_yeoni` 여니 | 여우 → 여우 | 같은 종족·성별(주황 여우 여성). 일(의복 수선과 물자 교환)에 가방·목도리가 맞는다. 흰 여우 남성인 은호 사장과는 맞지 않는다. |
| 검은 뿔 산양 `candidate_goat_shrine` | `resident_momo` 모모 관장 | 염소 → 염소 | 같은 종족·성별(염소 여성). 일(박물관 보관과 옛 생활 자료)에 기록장이 맞는다. |
| 설표 `candidate_snow_tea` | `resident_librarian` 사서 선생님 | 고양이 → 설표 | 소유자 선택. 성인 여성이고 털빛(은회색)이 가깝다. |
| 양 `candidate_sheep_linen` | `resident_nubi` 누비 아주머니 | 오리 → 양 | 소유자 선택. 일(세탁 협업과 임시 숙박 연결)이 린넨 역할과 가장 가깝다. |

### 인계문의 역할 제안과 다른 점

- 인계문에는 설표=광장 차 나눔, 양=여관 린넨 보조, 산양=신당 관리, 여우=상점 심부름 보조로 적혀 있었다. 이 역할들은 실제 설정에 넣지 않았다. 바뀐 것은 그림뿐이다.
- 신당은 지도의 배경일 뿐 이동할 수 있는 장소가 아니다(`node: null`). 찻집, 광장 차 나눔도 현재 설정에 없다. 그래서 모모의 기록장과 사서의 찻잔은 소품으로만 남는다.

## 그대로 둔 것

ID, 이름, 대사, 이야기 속 관계, 단서·증거·해금, 일정, 시간 비용은 바꾸지 않았다.

## 바뀐 것 (그림 데이터만)

- `dev/apply_npc_redesign.py`가 `art/npc-redesign-20261015/redesign.json`을 읽어 적용한다.
  - 다시 돌려도 결과가 같다.
  - 되돌리기: `--revert`. 확인만: `--check`.
- 그림: `game/assets/room13-redesign-<npc>.webp`
  - 원본의 0.5배다. 투명 가장자리가 어두워지지 않게 premultiplied 방식으로 줄였다.
  - WebP 품질 95이고 투명도는 무손실이다(`import_art.encode`).
- 바뀐 데이터 파일과 항목
  - `cast.json`: 몸 상태 전부, avatar, portrait
  - `room13-pixel-acting.json`: 서기 4종과 얼굴 크롭
  - `room13-portraits.json`: 흉상 4종. 전신으로 바꾸고 `full_body`를 붙였다.
  - `room13-fullbody-dialogue.json`: 6표정
- 예전 디자인의 앉기·생활 동작은 뺐다. 남겨 두면 예전 몸이 다시 보이기 때문이다. 이 NPC들은 서 있는 모습으로 나온다.
  - 여니: activity(앉기)
  - 사서: activity(앉기)
  - 모모: living_read
  - 누비: living_fold
- 발 위치는 맨 아래 보이는 줄의 가운데다. 머리·아바타 영역은 원본 기준으로 지정했다.

## 원본 보존

- 바꾸기 전 항목은 그대로 `art/npc-redesign-20261015/original-entries.json`에 옮겨 적었다.
- 원본 그림 28개는 `game/assets`에 그대로 둔다. 예전 저장에 남아 있는 그림을 그릴 수 있게 하기 위해서다.
  - 전용 행동 시트 4개
  - 예전 전신 표정 24개
- `dev/build_web.py`는 이 28개를 첫 로딩에서 빼고, 필요할 때만 받게 했다.
- 여러 인물이 함께 쓰는 흉상·아바타 시트는 다른 인물이 쓰고 있어서 그대로 둔다.
- 전달받은 PNG 4개, manifest, 인계문은 `art/npc-redesign-20261015/source/`에 있다. SHA-256 대조를 통과했다.

## 남은 한계

- 디자인마다 표정이 하나다. 이 4명은 대사에서 표정이 바뀌어도 그림이 같다.
- 예전 오리·고양이 설명이 남아 있다. 옛 캠페인 데이터 `village-residents.json`의 `public_name`과 `legacy-resident-roster.json`이다. Room13 시작(`start` → `room13_start`)에서는 이 화면에 가지 않으므로 고치지 않았다.

## 검증

- 단위 테스트: `dev/check.sh` 통과. `dev/test_npc_redesign.py` 4개가 새로 들어갔다.
- Ren'Py 화면 테스트
  - `redesign_world`: 실제 일정 자리에서 확인했다.
    - 2일 오전 기준이다.
    - 여니는 광장, 모모·사서는 우체국, 누비는 여관 로비 왼쪽 끝이다.
    - 네 명 모두 있고, 서 있고, 발이 바닥에 닿는다.
  - `redesign_dialogue`: 보통·큰 글씨·주제 목록 화면에서 확인했다. 귀·뿔이 위에서 잘리지 않았고, 얼굴이 대사창 위에 있다.
