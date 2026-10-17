# 0.19.24 — 승인 원화 프로필 58명

전달된 58명 얼굴 crop와 원본 SHA256·크기를 모두 검증했다. 같은 승인 neutral 원본에서 직접 정사각형을 잘라 256px, 사방 12px 투명 여백의 lossless WebP를 만들었다. 대화 이미지의 trim/scale/padding을 역산하는 대신 원본 좌표를 사용하여 이중 변환 오차를 피했다. 명세의 정규화 좌표를 정수 픽셀로 반올림했으며 별도 얼굴 재생성이나 crop 변경은 없다.

init 174에서 해당 인물의 `avatar_neutral`만 등록한다. 기록→사람, 관계도, 다람이 수첩 및 기존 동일 프로필 참조는 승인 얼굴을 사용한다. 작은 아이콘의 강제 nearest 필터는 적용 대상만 해제한다. 새 얼굴은 부드럽게 축소하고 제외 인물은 기존 처리 그대로다. 사망 grayscale·취소선·X, 실종 흐림, 엄마 재회 전 물음표, 실제 만난 인물만 표시하는 조건은 변경하지 않았다.

솔방울은 친칠라 승인 후 새 원화/crop 수신 대기이므로 이번 58명에 포함하지 않았다. 구 솔방울 프로필을 새로 제작하지 않았으며 아빠·legacy3도 제외했다. 조사 맵 포즈와 픽셀 배율, 기존 대화 59명·354슬롯은 바꾸지 않았다. cast/acting/world-layout/dialogue-talk-art registry 바이트가 직전 main과 동일함을 확인했다.

검증: 단위 검사 308개 및 Ren’Py lint 통과. 실제 Chromium/WASM 게임에서 58명 모두 44/60/76/80px 총 232개 표시를 검토했다. 귀·눈·입 잘림이 없어 승인 crop를 그대로 사용했다. 기록→사람 전체/인물 중심, 엄마 재회 전후, 다람이 수첩을 확인했다. 아직 만나지 않은 선생님은 목록에 나오지 않았고, 재회 fixture에서 엄마만 추가로 기록됐다. 사망/떠남/생존 상태는 기존 판정과 표현을 유지했다. QA 화면 목록에 수첩 이름이 빠진 테스트 harness 오류는 직접 screen 존재 검사로 수정했으며 게임 코드 오류가 아니었다.

58개 파일 모두 최종 ZIP에 포함되고 파일 SHA256이 원본 생성 결과와 일치한다. 추가 크기는 3,027,564 bytes다. 최종 웹 아카이브 SHA256은 `f948784eabc3dc2df7e5b1e4e848cbf4044df3f2fa36b8e480fea4bf433abab9`.

근거: `docs/reviews/profile-icons/approved-crops.json`, `receipt.json`, `transport.json`, `runtime.json`, `screens/`. 외부 Library 업로드는 하지 않았다.
