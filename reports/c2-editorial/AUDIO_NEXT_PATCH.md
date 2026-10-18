> 후속 구현: [이벤트 음향·플레이어 제외 검수](../c2-event-audio/README.md). 아래는 이전 계획 기록이며 책상 타격 후보는 이후 거절되었습니다. 웅성 파일은 이후 전달 승인되어 후속 검수 브랜치에 연결되었습니다.

# 후속 작은 패치: 대사 이벤트 기준 음향

이번 연출 검수와 분리합니다. 아래 동작은 아직 구현/검수 완료가 아닙니다. 현재 배포된 2.4초 자동 복귀 규칙도 이 연출 커밋에서 바꾸지 않았습니다.

확정 방향: 낮은 기본 회의 BGM, 주인공의 중요한 연속 발언 블록에 한 번 ducking, 주민 반응으로 넘어갈 때 복귀. 핵심 반박은 승인된 책상 타격 1회 → 음악/웅성 정적 → 핵심 대사 종료 이벤트 → 기존 단계별 빠른 BGM 재개. 읽는 중 시간 제한으로 소리가 재개되면 안 됩니다. 취소·스킵·씬 탈출·로드·예외 cleanup 필요. 사용자 mixer volume/mute는 변경하지 않고 채널 상대 gain만 조절합니다.

기존 소스 감사:
- `assets/sfx-slam.wav`: `music-v6-credits.txt:49`에 rubberduck의 OpenGameArt “100 CC0 Metal and Wood SFX”, CC0로 기재. `room13_sound.rpy`의 `source_fx("slam")` 경로. 단일 책상 타격으로 적합하다고 청취/승인된 증거는 현재 없음. 새 책상 소스가 전달되기 전 임의 성공 처리하지 않음.
- `assets/source-slam.wav`: provenance.json에 절차적 PCM 재구성으로 기재. 새 책상 녹음으로 간주하지 않음.
- 현재 반박 `source_fx("impact")`는 `sfx-present.wav`. 책상 타격이 아님.
- 현재 회의 환경음은 기존 `fire`/`wind`. 새 승인 주민 웅성 파일은 확인되지 않음. 거부된 crowd A/B, 미선택 stinger/Grady를 추가하지 않음.

다음 수정 지점: `room13_meeting_pressure.rpy`의 quiet/released 상태·2.4초 timer, `room13_meeting_direction.rpy`의 proof boundary/direct_line/direct_end/after_load, `room13_meeting_tempo.rpy`의 기존 단계별 BGM 재개. 증거/분기/대사 변경 없이 presentation state로만 연결합니다. 핵심 읽기 유지(2.4초 초과), 연속 아빠 대사에서 gain 재펌핑 없음, 주민 전환 복귀, 실제 취소·skip·load·exit 검사를 별도 수행해야 합니다.
