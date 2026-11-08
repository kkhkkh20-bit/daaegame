# 백 부인 일반 대화 도트 교정

2026-11-08 소유자의 제1부 완주 검수 수정 승인 범위다. 작은 원화를 크게 보간하던 백 부인의 일반 여섯 표정을 고해상도 도트 원화로 교정했다.

- 외형: 점박이 얼굴·금발 웨이브·갈색 리본·크림 망토·세이지 녹색 소매·자주 치마·펼친 장부·반지·꼬리·갈색 장화 보존.
- 스타일: 현행 다람·너울의 작은 계단형 윤곽·2~3단 명암을 참조. 표정만 달리하고 몸·옷·손과 장부·발선을 유지한다.
- 생성 PNG 원본 바이트는 `neutral.png` 등 여섯 파일에 그대로 보관한다. 원래 `/workspace/generated_images/` 파일도 삭제하지 않았다.
- `source-gallery.png`는 원화 검수용 나란히 보기이며 실제 게임 화면 합성이 아니다.
- 런타임은 `game/assets/dialogue-player-facing/madam20261108/`의 여섯 WebP다. `manifest.json`에 원본·런타임 해시와 알파 경계를 기록했다.
- 기존 표시 키: 840 기준 가시 높이 **627**, 질문 가시 높이 **557.3333333333334**. 전신을 임의 확대하거나 키를 바꾸지 않는다.
- 기존 `room13-dialogue-context-art.json`, `room13-dialogue-pose-source-art.json`, `room13-resident-poses-a.json`에는 백 부인 별도 문맥/질문 동작이 없다. 현장 전신은 교체하지 않는다.

가져오기 준비/검사:

```bash
python3 dev/import_madam_pixel132.py
PYTHONPATH=dev python3 -m unittest dev/test_madam_pixel132.py
```

`--apply`는 메인 통합 담당자만 실행한다. 그때 player-facing 일반6표정을 등록하고 기존 크기 맞춤표를 갱신한다. 단위 검사 통과는 실제 PC·휴대폰 대화·질문·회의 화면 검수를 대신하지 않는다.
