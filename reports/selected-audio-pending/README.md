# 선택 효과음 전달 상태

사용자 선택: 심장음과 작은 휙만 사용. 총성 원형/가공 두 종류 모두 제외. main 배포 없음.

## 파일 수신 차단

Library prepare_materialize는 세 항목 모두 성공했지만, 공식 library_file_transfer.py materialize 실행은 세 항목 모두 `library file transfer failed: download failed` (exit 1)로 종료했습니다. 실행 환경 `/workspace/selected-council-audio`. 권한 거부 메시지는 없으며 전송 실패 상태입니다. 재시도나 다른 경로로 우회하지 않았습니다. 파일 바이트와 출처 manifest는 아직 확보하지 못했습니다.

- 심장: `libfile_914e53871a8c8191aba978c0de6c1c65`, Council_Heartbeat_Loop_EDIT.ogg, 기대 31691 bytes.
- 휙: `libfile_fc3dfe252230819182729d0cea0ac5b2`, Council_Soft-Air_Transition.ogg, 기대 5836 bytes.
- 출처: `libfile_6f81dad7577081918b55c1d7784ed1c7`. 받으면 선택된 두 항목만 공개 크레딧으로 추출. 총성 항목은 공개하지 않음.

## 실제 대본/연결 지점 확인 완료 (아직 미적용)

심장음 후보는 일반 회의가 아닌 `case:father:return:v3`의 다람이(index 5) “아빠…… 나 여기 있어.”입니다. 문에서 연기가 새고 아이가 방에 갇힌 구조 직전 장면으로, 긴장 상황이 대본에 명시돼 있습니다. 해당 발화의 짧은 구간만 사용하고 다음 주민 발화에서 종료하는 방식이 적합합니다. `game/room13.rpy`의 실제 호출을 확인했으며 대사 변경은 하지 않았습니다.

휙은 `R13C2Editorial.render`의 실제 `shot.focus != self.last_focus` 전환에만 연결할 예정입니다. 단순 direct_line 콜백에 연결하면 같은 화면의 연속 대사에서도 재생될 수 있으므로 사용하지 않습니다. 모션 끄기·스킵·예측·로드/롤백 재구성에서는 제외하고 한 전환당 1회 및 짧은 재생 간격 제한이 필요합니다. 파일 도착 전 무음 placeholder나 가짜 완성 처리를 추가하지 않았습니다.

미완료: 두 파일 수신·선택 크레딧 추출·런타임 연결·실제 소리 녹화. 기존 승인 웅성, 아빠 화면 제외는 유지됩니다.
