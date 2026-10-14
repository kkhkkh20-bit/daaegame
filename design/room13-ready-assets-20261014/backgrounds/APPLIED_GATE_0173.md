# 입구 배경 선별 적용

원본: ac8760b38a5d75f2a0ef26f914e7ecb4faf7503f의 background/gate 오전·오후·저녁 3장. 사용자의 2026-10-14 전체 적용 요청 이후 위치 대조·런타임 QA를 거쳐 선별한다. 다른 39장 및 캐릭터 후보를 통째로 가져오지 않았다.

이 PNG는 원본 픽셀/해시 그대로다. 소스 ZIP에는 중복 삽입하지 않으며 `dev/selected_asset_overlay.json`이 원본 경로와 해시를 명시한다. 소스 ZIP을 풀고 `package_web_webp.py --release <저장소>/preview/room13-dev --sdk <SDK>`로 빌드하면 소스 로컬에 없는 이미지는 해당 저장소의 이 경로에서 읽는다. 필요 시 `--asset-root <저장소 루트>`를 지정한다. 런타임 변환은 무손실 WebP이며 픽셀 동일성을 검사한다.
