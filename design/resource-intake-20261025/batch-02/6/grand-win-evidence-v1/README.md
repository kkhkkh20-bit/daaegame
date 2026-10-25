# 대승리 자료 그림 3종 · 도트 스티커 후보 v1

2026-10-25 요청서 3항에 따른 전용 그림입니다. 게임 적용·기존 런타임 교체는 하지 않았습니다.

## 파일
- `NW_NUBI_TICKET`: 누비네 배급표. 다른 필체의 짙은 덧쓴 줄, 기름 얼룩, 접힘.
- `NW_RETURNED_BOWL`: 학교 배식용 흰 그릇. 작은 테두리 이 빠짐, 바닥의 지푸라기·눈 흔적.
- `REWARD_DOLMOK_VOID_MARK`: 돌목의 무효 표기. 한 칸 안의 굵은 취소선 정확히 두 줄, 서명 자국. 이 파일명은 납품용 제안 ID이며 기존 런타임 ID가 아닙니다.

`png/`는 생성 원본 1254×1254 RGBA, `webp/`는 같은 크기의 무손실 WebP입니다. 완전 투명 배경을 포함하며 보이는 RGBA 픽셀의 PNG/WebP 일치를 검사했습니다. `preview_360.png`, `preview_390.png`, `preview_640.png`는 짙은 바탕에 나란히 놓은 표시 크기 검수 이미지입니다. `qa/`는 각 그림의 크기별 검수용 미리보기이며 게임용 투명 원본을 대신하지 않습니다.

## 기준 자료
저장소 `kkhkkh20-bit/daaegame`, 기준 커밋 `15fb56cfbd6b713f9e0caa7cddf1d1fb98de8acc`.
- `experiments/renpy-ch1/docs/reviews/grand-win-20261024/적용보고.md`
- `experiments/renpy-ch1/game/assets/evidence/E34.webp`
- `experiments/renpy-ch1/game/assets/evidence/NW_WHITE_BOWLS.webp`
- `experiments/renpy-ch1/game/assets/evidence/NW_TRANSFER_LIST.webp`

기존 흰 그릇의 넓고 얕은 형태와 낮은 굽, 문서의 격자·낡은 종이 재질만 참조했습니다. 문장·인명·정답은 그림에 적지 않았습니다. 서명과 글씨는 의미 없는 획입니다. 그릇 바닥의 시설 문양은 참조 그림에서 확인되지 않아 새 문양을 발명하지 않았습니다. 문양이 증거 대조에 꼭 필요하면 먼저 기존 학교 그릇과 공유할 정식 문양을 확정해야 합니다.

## 제작·권리·한계
이 요청을 위해 이미지 생성 도구로 새로 제작한 자체 납품 그림입니다. 제3자 스톡 그림·폰트·상표는 사용하지 않았습니다. 기존 게임 자산은 형태 참조이며 소유권을 새로 주장하지 않습니다. AI 생성물의 법적 독점권을 보증하는 별도 라이선스 문서는 아닙니다.

도트 윤곽과 큰 색 면을 우선했고, 360·390·640px에서 덧쓴 줄·그릇의 흔적·장부 두 줄을 육안 확인했습니다. 생성 원본에는 미세한 색 변화와 극소수 가장자리 잔점이 남을 수 있어 엄밀한 고정 팔레트/1비트 알파 스프라이트라고 표기하지 않습니다. 검수 크기에서는 형태가 뚜렷하며 실제 게임 내 표시 검수는 아직 하지 않았습니다.

## 생성 프롬프트 요약
공통: actual transparent background, coarse pixel art, large flat clusters, stepped dark-brown outline, white sticker border, no readable text, no hands/characters/UI.
배급표: old ration sheet, two ruled columns, oil stains and fold creases, unreadable pale entries, one short darker angular added line below table.
그릇: match existing plain warm-white serving bowl, low foot ring, small rim chip, straw and snow traces on foot, no invented facility emblem.
장부: old four-column entry ledger, EXACTLY TWO bold cancellation lines in ONE rightmost-column cell, abstract signature below grid; no readable words.
수정: 장부 네 줄을 두 줄로 줄이고, 종이·그릇의 색 면 및 스티커 외곽을 정리했습니다. 생성 원본을 보존하고 ImageMagick으로 무손실 WebP 및 크기 검수 미리보기만 내보냈습니다.
