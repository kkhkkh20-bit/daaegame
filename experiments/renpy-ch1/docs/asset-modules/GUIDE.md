# 에셋·표정 모듈 채우기

## 누구나 확인하기

프로젝트 폴더에서 `python3 -m http.server 8788` 실행 후 `http://localhost:8788/docs/asset-modules/`를 연다. 캐릭터 이름(현재 내부 ID)·표정·UI 역할로 검색하고 ‘빈 슬롯만’을 선택한다. requests.csv는 제작 요청 후보, inventory.json은 전체 연결표다. 생성 시점의 스냅샷이므로 파일을 바꾸면 `python3 dev/asset_modules.py`로 갱신한다.

‘연결됨’은 파일이 있고 연결표에 등록되었다는 뜻이며 실제 렌더 검수를 뜻하지 않는다. 같은 그림을 여러 상태가 공유할 수 있다. ‘미연결’과 ‘파일 없음’을 구분한다. 중립 대사 얼굴과 아빠 얼굴 등 기존 정책상 비운 자리는 제작 담당자가 임의로 채우지 않는다. 참고 원본이 없는 슬롯은 크기·기준 포즈를 적용 담당자에게 먼저 확정받는다. 대사에서 실제 사용되는 표정의 빈도/우선순위는 이 표가 판정하지 않는다.

## UI 에셋

1. `python3 dev/asset_toolbox.py serve`로 기존 연결 도구를 연다.
2. 역할·상태를 선택하고 제작 요청 묶음을 내려받는다. 기존 원본, 캔버스 크기, 자르기/배율/Frame 규격을 따른다.
3. 받은 파일을 game/assets 아래 별도 폴더에 넣고 `python3 dev/asset_toolbox.py scan`을 실행한다.
4. 연결 도구에서 태그·역할을 매칭한다. 같은 그룹은 함께 바뀐다.
5. `python3 dev/asset_toolbox.py validate` 후 실제 화면에서 확인한다.

## 캐릭터 표정

- 대사 얼굴 연결 원본: game/assets/room13-dialogue-b-faces.json
- 전신 표정 연결 원본: game/assets/room13-fullbody-dialogue.json의 people → 캐릭터 → images → 표정
- 감정별 대사 연결: game/assets/room13-fullbody-line-emotions.json. 제작 담당자는 대사별 감정 판정을 변경하지 않는다.
- 대사 얼굴은 캐릭터 → 표정 → assets/...webp 경로를 등록한다. 전신은 기존 동일 캐릭터 항목의 file/size/crop/map 구조를 보존한다. 새 파일에 맞는 crop과 size를 실측하며 다른 캐릭터의 정렬 수치를 복사하지 않는다.
- 참고 원본과 같은 비율·발 위치·얼굴 위치·투명 여백을 유지한다. 표정만 바꾸고 캐릭터 정체성/포즈는 계약을 따른다. 없던 표정을 다른 표정으로 대신 등록하지 않는다.
- 경로 연결만 완료해도 실제 게임에 반영되지만, 전신 crop/map과 표정 별칭은 적용 담당자가 실측 검수해야 한다.
- 적용 후 scan → validate → 현황판 갱신 → 게임 재시작 및 PC/모바일 캡처 순서로 확인한다.

이 모듈은 기존 게임 연결표를 읽는다. 별도 중복 연결표를 만들지 않으므로 누가 채워도 실제 적용 경로를 추적할 수 있다.

## 질문·지도 버튼 전용 연결

`button.question_flat_primary/standard`는 질문 하단 도구, `button.map_flat_primary/standard`는 지도 하단 탭·이동·현장으로에만 연결한다. `ui-question-map-flat-v1` 원본 8장은 전체 캔버스를 균일 확대하며 crop/Frame을 사용하지 않는다. 기존 클릭영역과 글꼴·내용 정렬 계산을 유지한다. 전역 `button.primary/standard`와 메인·현장 연결은 유지한다.

이 연결의 실제 화면 캡처는 아직 미검증이다. screens의 0.20.48 격리 렌더는 적용 전 참고 자료이며 이번 변경의 결과 화면이 아니다.
