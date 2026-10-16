# 메인 타이틀 로고

기존 `game/assets/room13-title-logo.webp`를 imagegen으로 편집했다. 이름은 유지하고 도토리와 길게 이어진 장식을 제거했다. 깨끗한 아이보리 면, 절제된 황토색 아래 가장자리, 계단형 도트 윤곽으로 겨울 동화책 표지 느낌을 맞췄다. 새 인물은 그리지 않았다.

원본 결과: `/workspace/generated_images/exec-bbee275e-1ce6-4e02-b751-1f0093f6178c.png`.

가져오기: `python dev/import_art.py <결과 PNG> --name room13-title-logo.webp --lossless`.

배경 그림은 새로 만들지 않는다. 화면에서 색·그림자를 조절하므로 기존 모션그래픽용 원본·조명 좌표를 유지한다. 선과 버튼은 Ren'Py UI이며 로고 이미지에 합성하지 않는다.
