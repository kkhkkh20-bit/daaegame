# 여관 회의 앉은 자세

기존 fullbody 중립 이미지(보리/할머니는 현재 redesign)를 참조해 같은 복장·종·얼굴의 의자에 앉은 오른쪽 사선 자세를 생성했다. 왼쪽 방향은 런타임 반전한다. 원본 경로는 sources.json, 실제 게임 파일과 알파 128 이상 기준 표시 영역은 game/assets/room13-meeting-seated.json에 있다. game 파일은 dev/import_art.py로 WebP Q95로 변환했다. 원본 이미지는 생성 위치에 보존한다.

전체 원탁과 양옆 인물에만 쓰며 정면 표정 세트는 기존 것을 유지한다. 제단 회의에 의자를 넣지 않는다.
