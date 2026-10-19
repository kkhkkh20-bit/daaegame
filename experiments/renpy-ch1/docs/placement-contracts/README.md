# 갈아 끼우는 캐릭터 배치 계약

이 폴더는 다른 작업자가 같은 구조와 검증 기준을 재사용할 수 있도록 제공하는 시작 문서입니다.

**기본 OFF인 소스 프로토타입입니다. 기존 화면·배치·원화·시나리오를 활성화하거나 교체하지 않습니다.** 공개/공유와 배포/활성화는 별개의 작업입니다.

## 먼저 읽을 것

1. [OTHER_AGENT_HANDOFF.md](OTHER_AGENT_HANDOFF.md): 안전한 작업 순서와 교체 조건.
2. [MAPPING.md](MAPPING.md): 공간·원화·시나리오가 분리되는 구조와 실제 여관/우체국 예제.
3. [VALIDATION.md](VALIDATION.md): 검증한 범위와 아직 확인하지 않은 것.
4. [ALL_MAP_INDEX.json](ALL_MAP_INDEX.json): 21개 장소 범위에서 관찰한 145개 장소×인물×포즈 묶음. 3개 묶음만 예제 계약이며, 나머지는 기존 경로입니다.

## 구현 파일

경로는 `experiments/renpy-ch1` 기준입니다.

- `game/assets/room13-placement-contracts.json`: 배경별 공간 슬롯, 승인된 기존 원화, 일정 연결, 원래 배치의 사전조건.
- `game/assets/room13-placement-contracts.schema.json`: authoring/CI용 JSON schema. 게임 runtime에는 외부 validator 의존성을 추가하지 않습니다.
- `game/systems/room13_placement_contracts.rpy`: init183의 순수 resolver와 init184의 기본 OFF adapter.
- `dev/test_placement_contracts.py`: 소스-only 회귀 검사.
- `dev/placement-contract-preimages.json`, `dev/verify_placement_contract_preimages.py`: 정확한 기준 파일과 추가 파일의 해시 검사. 이 스크립트는 파일을 수정하지 않습니다.

## 기준

- 기준 commit: `91ec49f1c80af18d0c7298f1e4b7463b426c52bb` (PR18 C 기술검사용 실험 기준).
- 기준 tree: `d98f5c7026b449b10e93c084198600047adfa8ee`.
- 이 기준은 public main 또는 출시 버전이라는 뜻이 아닙니다. 다른 기준으로 옮기기 전에 guard와 fixture를 재검증해야 합니다.
- 여관의 누비/토실 배치와 우체국 오전 세련 C 배치·가림을 회귀 검사 기준으로 보존합니다. 우체국 오전 세련을 새 registry에 중복 연결하지 않습니다.
- **세련 C는 최종 업무 배치·포즈 승인이 아닙니다.** 클립보드를 들고 서 있는 현재 모습은 오른쪽 서비스 창구에서 일하는 동작으로 충분히 읽히지 않아, 배경과 업무 포즈 수정이 필요한 실험 상태입니다. 기술 검사 PASS를 시각적 디자인 승인으로 해석하지 않습니다. 이 패키지는 이를 자동 활성화하거나 다른 작업 배치로 대체하지 않습니다.

## 검사

추가 후 repository checkout의 `experiments/renpy-ch1`에서 실행합니다.

```sh
python dev/verify_placement_contract_preimages.py --root . --after-addition
python dev/test_placement_contracts.py
```

추가 전에는 패키지 쪽 guard 스크립트를 실행하고, `--root`에 대상 checkout의 `experiments/renpy-ch1` 경로를 넘깁니다. `--after-addition`은 생략합니다. 기준이 다르면 적용하지 말고 재기준 검증을 합니다.

## 이 구조가 해결하는 것과 해결하지 않는 것

공간은 자리와 가구 접촉을, 원화는 신체 기준점과 비례를, 시나리오는 누가 언제 어떤 자리를 쓰는지를 가집니다. 호환 포즈는 연결의 asset ID를 바꿔 시험할 수 있어 좌표를 여러 곳에서 다시 편집하지 않아도 됩니다.

이 구조는 거친 원화의 픽셀을 복원하지 않습니다. 2×2 렌더 격자 목표와 원화 품질 검수는 별개입니다. 새 원화·포즈·자리에는 실제 엔진 화면과 가림/클릭 검사가 필요합니다. 파일을 실행 중 덮어쓰는 hot reload 기능도 아닙니다.
