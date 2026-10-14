# 마차 손 교정 · 소스용 전달

교정 PNG는 1672×941 RGB이며 이름은 `room13-pixel-carriage-letter0153-morning.png`입니다. 리사이즈나 픽셀 후처리 없이 준비된 파일을 그대로 포함했습니다.

- 원본 SHA-256: `14cdd63697a88e34a63370d035354910401459d574f93bab4da6fd2c3b01e9e1`
- 교정 SHA-256: `9ce6389a6b1d6575dac7922d690669b9b9b1843df854ab15db3c4044d3a63f9e`
- 과거 검증 기준 커밋: `a53d8c2b9894a9ff907df9aaa81d934ee8dcc5c1`
- 과거 공개 게임 아카이브: `3317ab76d066865e18ba5e566537e7dc9252bea09bce9d460eb8fadefd5b7aa0`

## 최신 소스에 적용할 때

저장소의 최신 `preview/room13-source/ROOM13_SOURCE_HANDOFF.zip`을 별도 작업 디렉터리에 풀어 실제 프로젝트 위치를 확인하세요. 아래 `PATH_TO_PROJECT`를 해당 `experiments/renpy-ch1` 디렉터리로 바꿉니다. 오래된 저장소 스냅샷을 바로 대상으로 쓰지 마세요.

```sh
python design/room13-ready-assets-20261014/carriage/apply_source_asset.py PATH_TO_PROJECT --dry-run
python design/room13-ready-assets-20261014/carriage/apply_source_asset.py PATH_TO_PROJECT
```

스크립트는 provenance와 기존 PNG의 해시가 위 원본 또는 교정 해시인지 확인합니다. 독립적으로 수정된 다른 이미지라면 중단합니다. 검사를 우회하지 말고 최신 파일과 비교하세요. 성공하면 `art/pixel-b`와 `game/assets`의 두 PNG 경로, `game/assets/provenance.json`의 해당 해시만 갱신합니다. 다시 실행해도 같은 결과를 유지하도록 준비되어 있습니다. 스토리·코드 변경은 하지 않습니다.

## 검증 범위와 기록

과거 준비 단계에서 소스 dry-run, 별도 테스트 트리 적용 및 재적용, 해시 일치, ZIP CRC와 바이트 비교를 확인했습니다. 당시 Ren'Py SDK가 없어 재빌드/lint를 실행하지 못했고, 브라우저도 실행 환경 제한으로 시작하지 못했습니다. 최신 소스에 대한 빌드·플레이 검증은 별도로 필요합니다.

`patch-manifest.json`과 `source-provenance-patch.json`은 당시 검증 기록입니다. 그 안의 아카이브와 공개 파일 해시는 현재 main의 해시나 이번 GitHub 전달의 배포 결과가 아닙니다. 이 폴더에는 과거의 52MB 런타임 패치, 게임 아카이브, 엔진 파일을 포함하지 않았습니다. 원본 빌드에 종속적인 예전 런타임 조각을 최신 공개본에 덮어쓰지 말고, 최신 소스에 해시 검사를 거쳐 적용한 뒤 정상 빌드 절차를 사용하세요.
