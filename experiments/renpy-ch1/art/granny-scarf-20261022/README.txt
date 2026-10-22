할머니 목도리 적용 — 소유자 승인 2026-10-22

변경 범위
- 기존 이미지 31개 교체 + 승인된 기쁨/놀람 acting 이미지 2개 추가 = 이미지 33개.
- 대화 source-master 6표정 × 560/760/840 = 18개.
- withdraw_hand 대화 source 프로필 3개 + 기존 fullbody pose 1개.
- 기존 fullbody acting 4개, redesign 현장/지도/구형 아바타 1개,
  living_keyledger 지도 동작 1개, 회의 착석 1개, composed_answer 1개, 프로필 1개.
- room13-fullbody-dialogue.json: granny joy/surprise만 새 파일로 연결.
- profile-source-art / meeting-source-art: 교체 파일의 현재 sha256만 갱신.
- investigation-native-residual-20261018/receipt.json: living_keyledger의 기존
  export hash 고정 검사 기준 1개만 갱신. 원본 source hash·geometry는 그대로.
- test_expression_acting.py: 소유자가 승인한 새 픽셀/새 슬롯을 검사하도록 기준 갱신.
- .rpy 코드·v111 대사 JSON·preview 빌드·커밋·push는 이 작업에서 변경하지 않음.

런타임 추적 (game/ 기준, 코드 읽기만 수행)
1. room13_fullbody_dialogue.rpy init 58의 r13_fullbody_close_art:
   dialogue beat -> dialogue source -> 기존 fullbody spec 순서.
2. systems/room13_dialogue_beats.rpy init 170:
   authored withdraw_hand pose source가 일반 표정보다 우선.
   일반 대화/회의는 dialogue-source-master 프로필 560/760/840.
   flustered는 source 프로필에서 anxious로 대응.
   surprise는 surprise_talk, 반응은 surprise_react.
   thought_active에서는 일반 source 프로필을 사용하지 않으므로 기존 acting
   네 표정과 joy/surprise 슬롯도 실제 경로로 남아 있음.
3. room13_acting.rpy init 59의 R13_ACTING은 pixel-acting.json을 읽음.
   기본 현장·지도는 redesign, living_keyledger는 전용 파일.
   withdraw_hand fullbody 파일은 현장 acting spec에서도 참조되므로 교체.
4. room13_meeting_seating.rpy: close=False 전경 배치에서 seated 전용 파일.
   close=True는 room13_meeting_camera.rpy init 175의 R13MeetingOrbit 사용:
   composed_answer source slot -> fullbody/source -> 기본 actor 순서.
5. systems/room13_profile_source_art.rpy init 174가 granny avatar_neutral을
   profile-source-master/granny.webp로 재등록. 다른 cast 아바타는 redesign.
6. room13-portraits.json, cast.json, pixel-acting.json의 기본 granny 참조는
   이미 모두 redesign 파일이므로 파일 교체만으로 반영.
7. room13-avatars.json은 런타임 .rpy에서 로드되지 않음. 거기에만 남은
   room13-pixel-main-profile-granny.webp / room13-pixel-dialogue-granny.webp는 제외.
   미참조 구형 non-acting fullbody 6장과 room13-pixel-acting-granny.webp도 제외.
   이전 저장 호환 파일은 삭제하지 않음.

편집 및 정렬
- built-in image_gen으로 서로 다른 원본 17개를 각각 편집. 두 번째 입력은
  승인된 목도리 참고 그림. approved/에는 소유자 제공 6표정 PNG를 보관.
- 공통 지시: 원본 자세·표정·손·옷·색·소품·발 유지. 목 리본/금색 브로치만
  재킷보다 어두운 붉은 뜨개 목도리로 교체. 한 번 감고 끝은 안으로 넣음.
  앞에 작은 은색 옷핀 하나. 찢어진 자리/늘어진 끝 없음. 투명 배경 요청.
- generation.json에 각 편집의 실제 프롬프트와 도구 출력 경로를 기록.
- generated/의 PNG는 도구의 편집 원본 결과. 도구가 배경/다른 신체 부분을
  바꾼 경우도 있으므로 그대로 게임에 넣지 않음.
- 얼굴/몸의 불변 특징을 SIFT로 매칭하고 RANSAC 유사변환으로 생성본을
  원본에 정렬. 중복 target feature 투표 제거. 실제 행렬은 alignment.json과
  manifest.json에 기록. 생성본에서 목도리와 기존 리본이 있는 사각 영역만
  원본에 반영. 나머지 RGBA 픽셀과 원본 전체 alpha는 정확히 유지.
- acting 및 dialogue pixel-grid2는 최근접 2x2 셀로 변환하고 패치 경계도
  짝수 좌표로 맞춤. smooth pose/meeting/profile은 원래 해상도에 최근접 정렬.
- 560/760 프로필은 같은 840 편집 master의 목도리 패치를 같은 비율로 파생.
  원래 각 프로필의 나머지 픽셀·alpha·canvas·offset은 유지.
- 기쁨/놀람은 승인 PNG에서 균일 배율/최근접 2x2로 변환.
  기존 neutral acting의 262x420 canvas와 map [1.82609,24,2] 사용.
  alpha 실측 최하단을 원래 발 위치 416에 정렬. 새 crop만 새 실측에 맞춤.
- edited/는 실제 배포 bytes. WebP lossless 저장으로 목 이외 픽셀을 보존.
  originals/에는 바꾸기 전 bytes를 experiments/renpy-ch1 상대 경로 그대로 보관.
- manifest.json은 모든 이미지/registry/baseline의 경로·방법·크기·전후 hash 목록.
  source_sha256은 이전 원화의 역사적 출처이므로 기존 항목에서는 유지.

적용/확인/복원 (저장소 루트)
  python3 experiments/renpy-ch1/dev/apply_granny_scarf.py
  python3 experiments/renpy-ch1/dev/apply_granny_scarf.py --check
  python3 experiments/renpy-ch1/dev/apply_granny_scarf.py --revert
  python3 experiments/renpy-ch1/dev/apply_granny_scarf.py --check --revert
전체 파일을 먼저 hash 검사하여 무관한 편집은 덮어쓰지 않음. apply/revert 멱등.
새 파일 두 개는 revert 때 삭제. 원본 파일은 byte-exact 복원.

검증 (experiments/renpy-ch1/dev에서)
  python3 -m unittest test_granny_scarf test_expression_acting test_npc_redesign test_approved_profile_icons test_meeting_direction test_actor_intent_and_source_art test_remaining_approved22 test_fullbody_dialogue test_investigation_native_residual
크기/파일 존재/전체 alpha/발 위치 ±2px/목 이외 픽셀/런타임 레지스트리 커버리지/
격리 임시 폴더에서 적용·복원 2회 및 무관한 변경 거부/기존 hash 기준 검사.
최종 결과: 위 관련 단위 테스트 75개 통과, apply --check 통과, git diff --check 통과.
Ren'Py 실행과 웹 빌드는 Claude 담당이며 여기서는 실행하지 않음.

비교 이미지
/tmp/claude-0/-home-claude/a6c0a1f6-b7da-5023-bdb2-55e6e15573c0/scratchpad/scarf/before_after.png
33개 이미지 모두 원본 | 새 그림을 같은 배율로 표시. 새 두 슬롯의 원본 칸은
geometry 기준인 neutral acting(기존 공용 슬롯 대신 새 표정임을 라벨에 표시).

남은 시각적 한계
- 작은 지도/48~66px 프로필에서는 은색 핀의 선과 잠금부가 몇 픽셀로 축약됨.
- 구형 acting은 원래 2x2 격자라 짜임·핀 디테일이 source master보다 단순함.
- Ren'Py 실제 표시 및 생각/회의/지도 화면 전환 검수는 Claude가 수행해야 함.
