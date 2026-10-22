# 다람탐정 — 엄마의 도토리 낙서

| 파일 | 크기 | 용도 |
| --- | --- | --- |
| `acorn_ink.png` | 96 × 96 | 엄마의 편지·쪽지 끝 기본 도토리 |
| `acorn_ink_small.png` | 32 × 32 | 글자 옆에 붙이는 기본 도토리 |
| `acorn_ink_crooked.png` | 96 × 96 | 급히 쓴 방 메모의 삐뚤한 변형 |
| `acorn_ink_crooked_small.png` | 32 × 32 | 글자 옆에 붙이는 삐뚤한 변형 |
| `contact.png` | 1080 × 720 | 베이지 종이 위 한글 문장과 실제 크기 배치 확인 |
| `README.md` | — | 파일 목록 및 제작 정보 |

도토리 네 파일은 RGBA 투명 PNG입니다. 내부도 투명하며 잉크 RGB는 모두 `#5a3a24`입니다. 가장자리의 알파값으로 안티앨리어싱을 유지했습니다. `contact.png`는 종이 배경이 있는 불투명 확인용 이미지입니다.

기본형은 엄마의 진짜 편지·쪽지 끝에만 사용합니다. 가짜 초대 편지에는 붙이지 않습니다. 삐뚤한 변형은 방의 메모에 사용합니다. 확인용 한글 문장은 배치 예시이며 게임 확정 대사가 아닙니다.

## 제작

내장 이미지 생성 도구(image_gen)로 기본형 생성 후, 해당 이미지를 참조하여 삐뚤한 변형을 생성했습니다. Python Pillow(PIL)로 알파 영역을 자르고, 잉크색을 통일하고, 여백 및 96px/32px 크기를 맞췄습니다. 변형에는 왼쪽으로 10도 기울기를 더했고, 32px에서는 가는 선의 알파를 보강했습니다. `ref_icon.webp`는 크기감만 참고했으며 픽셀 화풍을 따르지 않았습니다.

최종 생성 프롬프트 요지:
- 기본: “A single tiny acorn pen doodle for a mother's handwritten letter signature in a winter mystery visual novel. Transparent background, one warm brown ink #5a3a24, adult casual handwriting, simple rounded tapering outline, shallow cap with only four short diagonal hatches, one bent stem, empty transparent interior. Legible at 32px. No face, text, frame, shadow or decoration.”
- 변형: “Edit the same mother's acorn signature into a slightly crooked hastily handwritten version. Preserve single brown ink, transparent interior, four cap hatches and one stem. Subtly lopsided cap, uneven nut outline, wonky stem, gentle left lean. Easily recognizable as the same acorn. No added elements.”

확인: 네 파일의 지정 크기, RGBA 모드, 투명 픽셀, 단일 RGB 잉크를 검사했고, contact.png에서 한글 표시와 실제 크기 배치를 육안 확인했습니다.
