# 다른 채팅에 전달할 말

다람탐정 저장소의 `experiments/renpy-ch1/docs/story-workbench/`에서 시작한다.

- 대사: 분기별 편집 JSON을 내려받아 text와 review_status만 수정한다. 조건·ID·화자·원본 hash는 바꾸지 않는다. 받은 JSON은 dev/dialogue_modules.py check로 원본 변경/충돌을 검사하고, 검토 후 apply --write로 실제 반영한다. 반영 후 관련 검사·화면 확인·모듈 재생성을 한다.
- 그림: docs/art-requests에서 제작 요청서와 개별 요청을 받는다. '미납품'과 '납품 확인'을 구분하고 이미 연결된 파일을 새 제작하지 않는다. 납품 원본은 별도 폴더로 받고 기존 asset-modules의 납품·적용·화면 확인 절차를 따른다.

대사는 아빠가 이해하고 묻는 순서, 유쾌한 다람과 아빠의 주고받기, 주민별 행동과 고집을 기준으로 전면 손질한다. 정답·생사·퍼즐 조건을 문장 편집으로 바꾸지 않는다.
