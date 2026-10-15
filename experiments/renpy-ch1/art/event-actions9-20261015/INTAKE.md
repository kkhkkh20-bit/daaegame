# 사건 동작 9종 접수 (2026-10-15 10:35 PDT)

접수·보관만 했다. 게임에는 넣지 않았다(이 브랜치에만 있음).
- ZIP SHA-256: c6cdea06149897d562ee25039a7fa9320354d2479d28542e8ce08d0cbaa50e78
- PNG 9장의 SHA-256은 모두 event-actions9-manifest.json과 일치한다.

| ID | 동작 | 제안 키 | 구분 | 요청 대응 |
|---|---|---|---|---|
| resident_sling 슬링 | 봉투에 김 쐬기 | event_steam | 필수 | ART_REQUEST_01853 §1 (지금은 thinking 포즈로 대신 보여 줌) |
| resident_ttadak 따닥 | 문틀 작업 | living_doorframe | 필수 | ART_REQUEST_01822 B. 부엉이 할아버지 문턱 수리와는 다른 장면 |
| buri 부리 | 공구함에 손 얹기 | event_toolbox | 선택 | 01853 §2 |
| resident_piko 피코 | 판자 물감 닦기 | event_paintwipe | 선택 | 01853 §2. 기존 living_paint는 그대로 둔다 |
| resident_mungchi 뭉치 | 문 쪽을 보며 손 비비기 | event_handrub | 선택 | 01853 §2 |
| resident_librarian 사서 | 장부 더미 끈 묶기 | event_ledgertie | 선택 | 01853 §2 |
| resident_siluk 실룩 | 입 가리고 귓속말 | event_whisper | 선택 | 01853 §2 |
| 소품 | 난로 주전자와 김 | — | 필수 소품 | 01853 §1 |
| 소품 | 문틀 수리 널빤지·못상자·대팻밥 | — | 필수 소품 | 01822 B |

남은 일과 부족한 점
- 메타데이터의 앵커는 원본 PNG 픽셀 기준 육안 추정이다. 잘라낸 영역 기준 상대 좌표(acting.json 형식)로 바꾸고 실제로 재 봐야 한다.
- 01853의 옛 1280 우체국 좌표는 쓰지 않는다. 우체국 아침은 2160 넓은 맵 기준으로 다시 정한다(0.18.57).
- 런타임에서 아직 검수하지 않았다: 손·봉투·김이 닿는 곳, 발 접지, 가림, 클릭 영역.
- 이 ZIP에 없는 것: 새 디자인 할머니의 열쇠·장부 맞추기, 부엉이 할아버지의 수첩 제본 묶기, 원래 그림 까로의 마차 축 감기.
- 피코 living_paint, 부리 tool·kneeling, 톡 seated 같은 기존 포즈는 지우거나 대체하지 않는다.
