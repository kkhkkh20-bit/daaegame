# 아랫길 노인·누비 배급표 자산 적용

범위: `design/resource-intake-20261025/batch-02/2`, `6/grand-win-evidence-v1`. 소유자의 적용 지시에 따라 기존 런타임 인물·자료 ID에만 연결했다.

- `v111_lowerroad_elder` 전용 기본 전신·얼굴을 `assets/lowerroad-elder/`로 복사했다. 납품 PNG와 런타임 WebP의 RGBA 픽셀이 완전히 같다. 원본 PNG는 `art/batch02-elder-ticket-20261025/`에 보존했다.
- `systems/room13_lowerroad_elder_art.rpy`의 init 172 등록은 해당 인물의 R13_FULLBODY·CAST·기본 얼굴 행만 별도 사전으로 교체한다. `elder` 원본 데이터·그림과 공유 사전은 수정하지 않는다. 기존 표정 키와 화자 ID를 유지한다. 납품은 기본 자세 한 장이므로 미납품 기쁨·걱정·앉은 자세를 새로 만들지 않는다.
- `NW_NUBI_TICKET`의 기존 `assets/evidence/NW_NUBI_TICKET.webp` 경로를 새 납품 WebP로 교체했다. 이전 파일은 `art/batch02-elder-ticket-20261025/NW_NUBI_TICKET-before.webp`로 보존했다. 자료 이름·설명·획득·정답 판정은 변경하지 않았다.
- 배급표 납품 PNG/WebP는 보이는 RGBA와 알파가 같으며 완전 투명 영역의 RGB만 다르다. 런타임에는 납품 WebP를 그대로 사용한다.
- `NW_RETURNED_BOWL`은 핵심 바닥 표식이 없어 기존 런타임 그림을 유지한다. 새 그릇과 `REWARD_DOLMOK_VOID_MARK`는 `art/.../held-candidates/`에만 보관했다. 무효표기 제안 ID를 자료로 등록하지 않았다.

검증: `test_lowerroad_elder_ticket_art.py` 2개 통과(별지기 원본·공유행 불변, 표정API 키 유지, 원본 RGBA·런타임 바이트 보존). `git diff --check` 통과. 네이티브 testcase `lowerroad_elder_ticket_art`는 일반·큰 글씨/터치 노인 대화 및 배급표 기록 화면 4장을 캡처한다. 실제 실행은 통합 담당이 수행한다.
