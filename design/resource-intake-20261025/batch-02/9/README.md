# 불타는 밤 배경 6종 · 검토용 시안

제작일: 2026-10-25 UTC. 기존 배경 확인 기준: kkhkkh20-bit/daaegame main, 15fb56cfbd6b713f9e0caa7cddf1d1fb98de8acc.
이 파일들은 검토용 이미지이며 게임에 적용·배포하지 않았습니다. 이야기, 조건, UI, 코드 변경은 없습니다.

## 파일과 원본
원본 경로 접두사: experiments/renpy-ch1/game/assets/

- wild-school-classroom-night.png — 1983×793. room13-pixel-panorama-school-evening.webp의 교실 구도 유지. 창밖 붉은 빛, 빈 침구, 난로와 등 소등.
- wild-school-hall-night.png — 1983×793. 별도 학교 복도 원본이 확인되지 않아 같은 school-evening 원본 오른쪽 외투·벤치 공간의 재료와 구조를 참고한 새 각도 시안. 낮게 깔린 연기, 끝 열린 문과 붉은 빛. 기존 구도 일치 검증 대상이 아니며 적용 전 공간 검토 필요. 여관 13호실 복도는 사용하지 않음.
- wild-square-burning.png — 2048×768. room13-pixel-panorama-square-evening.webp 구도 유지. 언덕 집 화재, 중앙 게시판 옆 등은 푸른색, 이름 없는 먼 군중 실루엣. 얼굴·상처 없음.
- wild-road-mouth-night.png — 2048×768. room13-pixel-wide-forest-evening.webp의 숲과 room13-pixel-ready-gate0173-evening.webp의 초소·건축, 기존 마을 지도를 참고한 새 각도 시안. 전경 산길이 아래 마을로 내려가며, 아래쪽 집들이 불타고 오른쪽 가까운 초소 난로는 푸른색. 초소의 정확한 위치와 지형 대응은 미확정이므로 적용 전 공간 검토 필요. 기존 구도 일치 확정본이 아님.
- wild-greenhouse-night.png — 2048×768. room13-pixel-ready-greenhouse0177-evening.webp의 작업대·지붕·가구 구도 유지. 우측 벽에 요청된 낮은 문 추가, 문틈 붉은 빛, 등 소등, 빈 공간. 인물 없음. 문 추가 위치와 인물 배치 공간은 적용 전 검토 필요.
- wild-village-dawn-ash.png — 1672×941. room13-pixel-overview-morning.webp의 건축과 room13-pixel-panorama-square-evening.webp의 게시판 형태, 제공된 기존 마을 지도를 참고한 산길 내려다보기 새 각도 시안. 잔연기, 불탄 지붕과 광장 이름판. 원본과 동일 구도가 아니며 지형·배치 검토 필요.

## 검증과 한계
6개 모두 PNG를 열어 치수와 장면을 육안 확인했습니다. 인물은 광장의 익명 실루엣만 있습니다. 교실 난로 OFF, 광장 등 BLUE, 초소 난로 BLUE를 확인했습니다. 새벽 이름판을 추가 보정한 최종안만 포함했습니다.

기본 이미지 생성 기능으로 각각 제작했습니다. 프롬프트에는 도트 스타일, 2×2 이상 사각 픽셀 군집, 계단형 가장자리, 넓은 색면과 단계 명암, 부드러운 회화 질감 배제를 지시했습니다. 다만 생성 이미지의 모든 픽셀이 균일한 2×2 격자라는 기계적 검증은 하지 않았습니다. 실제 게임 축소·확대·인물 겹침·런타임 검증은 하지 않았습니다.

학교 복도·산길 어귀·새벽 전경은 원본 동일 구도 조건을 완전히 충족한 파일이 아니라 명시적인 검토용 시안입니다. 전체 6장을 동일 구도 확정본이라고 취급하지 마세요.

설계 근거: experiments/renpy-ch1/docs/design/WILD_NIGHT_DESIGN.md 6절 및 docs/reviews/wild-night-20261024/지시서.md 5~6절. 선택 항목인 장갑·도토리 정물과 투명 불꽃은 포함하지 않았습니다.

산길 수정: 2026-10-25 UTC, 내려다보는 구도와 아래쪽 화재가 보이도록 교체했습니다. 이전 입구 정면 시안은 ZIP에서 제외했습니다.
