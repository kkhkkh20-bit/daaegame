# 승인 소품 6종 연결 결과

기준 main: `00056b214e4c5bc25eb972e04997cbd9fc4911c4`.
원본 전달 commit: `b71a8d8aff2c97953e1b8db63233ff9c598b27c2`.
원본: `experiments/renpy-ch1/art/resident-props-delivery-20261024/props/` 및 상위 `manifest.json`.

## 적용

원본 WebP 6개를 실제로 열어 픽셀과 투명 여백을 확인했다. 전부 RGBA 256×256이며 manifest SHA256·Git blob SHA·바이트 수가 일치한다. 재인코딩 없이 `experiments/renpy-ch1/game/assets/resident-props-20261024/`에 복사했다.

| 기존 키 | 기존 의미 | 연결 파일 |
|---|---|---|
| bag:snack | 구운 밤 | sticker_snack.webp |
| bag:postcard | 그림엽서 | sticker_postcard.webp |
| bag:cord | 질긴 묶음끈 | sticker_cord.webp |
| bag:hat | 다람이의 털모자 | sticker_hat.webp |
| bag:lamp_oil | 등잔 기름 | sticker_lamp_oil.webp |
| bag:herbs | 해열 약초 묶음 | sticker_herbs.webp |

`game/assets/room13-material-icons079.json`의 위 6개 항목 `file`과 `crop`만 변경했다. crop은 `[0, 0, 256, 256]`으로 납품 캔버스와 투명 여백 전체를 보존한다. 그림 자체는 잘라내거나 늘리지 않았다.

실제 상점 호출은 `room13_shop.rpy → R13PixelIcon(key,6) → r13_material_art("bag:"+key)`이다. 요청에서 부른 R13ShopIcon이라는 클래스는 현재 코드에 없으며 기존 R13PixelIcon을 수정하지 않았다. 공통 자료 목록은 `r13_catalog_object_icon → r13_material_art`를 사용한다. 기존 48×48 contain 변환 및 상점 96×96 contain 변환, 클릭 영역·레이아웃·문구·가격·기간·소유·선물·획득조건은 그대로다.

공유 호출 주의: 기존 `room13_v111.rpy`의 `R13_V111_MATERIAL_ART["E28"] = "bag:postcard"` 때문에 `V111:E28`(엄마에게 쓰는 답장)도 같은 엽서 그림을 사용한다. 기존 별칭을 추가하거나 변경하지 않았다. 납품 manifest는 이 6개 기존 키의 의미 보존을 명시하며 새 사건 단서나 새 분기를 연결하지 않았다.

## 검증

- 통과: manifest의 SHA256·Git blob SHA·바이트 수 6/6, 원본과 runtime 바이트 일치 6/6.
- 통과: `python -m unittest discover -s experiments/renpy-ch1/dev -p test_material_art.py` 3개. 키 범위, crop 경계·투명 여백, 읽기 전용 조회·fallback 검증.
- 통과: 같은 명령의 `test_materials.py` 9개, `test_room13_livelihood.py` 6개. 기존 자료·생활 기능 계약 검증.
- 통과: `git diff --check` 및 JSON 변경 키가 승인된 6개뿐임을 대조.
- 미실행: Ren'Py lint·실제 상점/자료 화면·모바일 터치·게임 화면 캡처. 현재 SDK가 없으며 이전 접근 거부 다운로드를 재시도하거나 우회하지 않았다. 원본 픽셀 열람은 엔진 화면 검증을 대신하지 않는다.
- 이 담당 범위에서 실패한 단위검사 없음. 전체 CI·기존 조사 검사 결과는 상위 작업 보고에서 별도로 다룬다.

소품 범위 적용 6개, 보류 0개. 주민 자산과 배치·방향 검토는 별도 담당이며 이 문서의 검증 범위에 포함하지 않는다. 이 담당 작업은 commit·push·merge하지 않았다.
