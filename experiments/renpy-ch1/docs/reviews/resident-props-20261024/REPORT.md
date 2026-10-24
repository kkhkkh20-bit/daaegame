# 주민·소품 제한 적용

기준 main `00056b214e4c5bc25eb972e04997cbd9fc4911c4` (PR27 병합). 원본 `b71a8d8aff2c97953e1b8db63233ff9c598b27c2`의 art/resident-props-delivery-20261024 전체77개를 그대로 가져왔다. 주민65·소품6·문서6의 원본 입고와 런타임 적용은 구분한다.

## 적용

- 대화2개, 기존 크기 프로필6개: `resident_teacher/write_attendance` → A7-04, `seryeon/chair_read` → A8-05. 원본 WebP를 game/assets/resident-a-20261024에 복사하고 기존 room13-dialogue-pose-source-art.json의 해당 profile만 연결했다.
- 선생님 호출: room13_ep_story.rpy의 ep5:st_teacher_after (13·14일, teacher_alive), room13_ep5_soup.rpy의 ws:teacher:count / dynamic:418. 대사·생존·날짜·장소 조건은 그대로다.
- 서련은 기존 chair_read 대화 표현만 교체했다. 우체국 오후 조사 그림, chair_listen 및 회의 착석 등록은 변경하지 않았다.
- 기존 알파 높이·수평 중심·발 하단에 균일 배율을 맞추고 캔버스를 유지했다. 정수 offset, 중심/하단 반올림 오차0.5px 이하, 캔버스 내부 알파 확인. 상세 dialogue-mapping.json.
- 소품6개는 기존 bag:snack/postcard/cord/hat/lamp_oil/herbs의 파일·crop만 변경했다. 기존 V111:E28도 bag:postcard를 공유한다. 기존 별칭·획득조건·효과·아이콘 크기는 유지한다. 상세 저장소 루트 docs/reviews/resident-props-20261024/PROPS.md.

## 보류

- 주민63개: 기존 후보16/보류10은 유지한다. 과거 확정30개와 추가 조사7개도 조사 클릭·손발 접점 검증 전에는 적용하지 않았다. 과거 확정은 정적 대응이며 최종 화면 승인이 아니다. 항목별 resident-status.json 참고.
- 조사 클릭은 r13_actor_hit_mask → r13_staged_visible_art의 실제 알파를 공유한다. 새 캔버스/투명 실루엣은 기존과 달라 단순 파일 교체도 클릭 영역을 바꾼다. map27 anchors/foreground_parts/variants, map9 contacts/source_size는 기존 원화 좌표다. 새 손발 접점 없이 이를 옮기거나 배율을 추측하면 가구 위 손·바닥 발·가림이 달라질 수 있다. 배치/클릭 로직을 추가하거나 바꾸지 않았다.
- 피코 구형 공작/뭉치 구형 판다 원화를 새 캐릭터의 대안으로 재사용하지 않았다. 회의 앉은/입석, 이젤, 너울 복장 연속성, 장면 전용 후보는 보류 유지.

## 검증과 한계

- 주민65개 해시·가독성 및 실제 픽셀 모음 확인. 대화2개는 기존 그림과 나란히 비교했다. 원본 재생성/수정 없음.
- 소품6개 픽셀·SHA256·Git blob 확인, 관련 단위18개 통과. 특별 포즈3개·B 표정5개 검사 통과. 전체 Python 단위976개 통과(43.781초). CI 결과는 PR에 기록한다.
- 실제 Ren'Py 화면·PC/모바일 터치·가림·전환은 SDK 부재로 미검증. SDK403 및 거부된 artifact 접근은 재시도·우회하지 않았다. 원본 비교는 실제 플레이 캡처가 아니다.
- 웹 빌드 미실행, preview/room13-dev 변경 없음. 소스 병합/Pages 기존파일 재배포는 새 실행본 갱신이 아니다.
