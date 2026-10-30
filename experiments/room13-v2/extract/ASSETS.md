# 그림·소리 목록 — 추출 1단계

2026-10-30. `experiments/renpy-ch1/game` 의 미디어 파일(.webp .png .jpg .mp3 .ogg .wav .ttf .otf .svg)을 **실행하지 않고** 파일 이름 참조로만 분류했다. 크기는 그림의 픽셀(가로x세로), 용량은 바이트.

## 분류 방법과 한계

- A: v111 데이터(records.json 장면 음악·환경음, ms14/art.json, v111 장소의 현장 배경 배치표, dNN 대사 컷 `cut`/`endcut`, v111 자료 그림 `assets/evidence/<ID>.webp`, 1일 마차·오프닝 코드)가 경로를 직접 가리키는 파일. **v111 이 쓰는 것이 확인된 파일.**
- B1: v111 에 말하거나 서는 인물(MS14_SPEAKERS + 대기 관문 인물)의 그림 폴더·매니페스트 파일. 표정·크기(560/760/840)·전신/근접 묶음이 다 들어 있다. 이 가운데 어느 조합이 실제 화면에 뜨는지는 실행해야 안다 — **미확인**(줄마다 표정은 day01.json·inventory 에 있다).
- B2/B3: 시작에서 닿는 label·화면이 있는 rpy(또는 그런 rpy 가 읽는 JSON 표)가 이름이나 계산 경로로 부르는 파일. 공통 UI·도트 연출·자료 아이콘이 여기 든다. 같은 파일 안에 옛 판 코드도 섞여 있어 **실제 v111 화면에 나오는지는 미확인**.
- C/C2/C3/D: v111 에서 쓰지 않는 것으로 본다. C 는 옛 판 rpy(시작에서 label·화면이 하나도 닿지 않는 67개 파일 — 단 함수로 살아 있는 15개는 제외)나 게임이 읽지 않는 표(asset-toolbox, provenance 등)에만 이름이 나온다. 옛 저장 호환(room13_webp_alias.rpy)이 부를 수 있는 파일이 섞여 있을 수 있다.
- 정적 분석이라 문자열을 실행 중에 조립하는 경우(예: 장소·시간대·표정 이름을 이어 붙임)는 B3 로만 잡았다.

## 합계

| 분류 | 파일 수 | 용량 |
|---|---|---|
| A. v111 데이터·코드가 직접 가리킴(확인) | 248 | 120.5 MB |
| B1. v111 출연자 인물 그림(표정·크기 묶음 전체) | 3217 | 254.3 MB |
| B2. 살아 있는 공통 코드·읽는 표가 이름으로 부름(UI·연출·자료 아이콘 등) | 489 | 129.5 MB |
| B3. 살아 있는 코드가 계산한 경로로 부름(%s 등) | 64 | 21.4 MB |
| C. 옛 판 코드·읽지 않는 표에서만 이름이 나옴 | 297 | 137.9 MB |
| C2. v111 에 나오지 않는 인물의 그림 | 570 | 49.9 MB |
| C3. 인물 그림 폴더 규칙에만 걸림(인물 불명) | 3 | 0.4 MB |
| D. 어디서도 이름이 안 나옴 | 2 | 0.4 MB |
| **v111 사용(A+B, B 는 후보 포함)** | 4018 | **525.6 MB** |
| **v111 미사용(C+D)** | 872 | **188.6 MB** |
| 전체 미디어 | 4890 | 714.2 MB |

확실히 쓰는 A 만 따지면 120.5 MB, 확실히 안 쓰는 C+D 는 188.6 MB. 그 사이(B1~B3, 405.2 MB)는 실행 검증이 필요하다.

## v111 이 가리키지만 파일이 없는 것

- 자료 그림 `assets/evidence/<ID>.webp` 가 없는 v111 자료 16개: E07_NUBI, E09, E13_MENDING, E19, E20, E21, E24, E25, E30, NW_INNER_PRICE, NW_KKOMI_NOSTONE, NW_LA_CHECK, NW_LA_FIELD, NW_LA_KNIFE, NW_LA_OFFER, NW_MUSOE_DEEP. 이 자료는 `R13_V111_MATERIAL_ART`(room13_v111.rpy)로 옛 그림을 빌리거나 기본 그림으로 보인다 — 어느 쪽인지 자료별로는 미확인.
- 대사 컷: v111_reunion_close.webp, v111_reunion_far.webp — `R13_NW_CUT_SPECIAL` 의 특수 컷(재회 장면)이라 다른 경로로 그린다(미확인).
- 엔딩 컷: 납품 전이면 아무것도 띄우지 않는다(systems/room13_end_cut.rpy). 기본 판도 -base 판도 없는 키: 없음.

## A. v111 이 확인된 파일 248개 (120.5 MB)

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/amb-clock.mp3 |  | 63 KB | 환경음(records ambience) |
| assets/amb-fire.mp3 |  | 229 KB | 환경음(records ambience) |
| assets/amb-wind.mp3 |  | 52 KB | 환경음(records ambience) |
| assets/bgm-altar.mp3 |  | 6347 KB | 장면 음악(records audio) |
| assets/bgm-council.mp3 |  | 1509 KB | 장면 음악(records audio) |
| assets/bgm-dark.mp3 |  | 6817 KB | 장면 음악(records audio) |
| assets/bgm-ending.mp3 |  | 4130 KB | 장면 음악(records audio) |
| assets/bgm-family.mp3 |  | 2684 KB | 장면 음악(records audio) |
| assets/bgm-inn.mp3 |  | 4238 KB | 장면 음악(records audio) |
| assets/bgm-inn2.mp3 |  | 1955 KB | 장면 음악(records audio) |
| assets/bgm-night.mp3 |  | 1035 KB | 장면 음악(records audio) |
| assets/bgm-pressure.mp3 |  | 3806 KB | 장면 음악(records audio) |
| assets/bgm-search.mp3 |  | 1447 KB | 장면 음악(records audio) |
| assets/bgm-snow.mp3 |  | 3306 KB | 장면 음악(records audio) |
| assets/bgm-think.mp3 |  | 1144 KB | 장면 음악(records audio) |
| assets/bgm-travel.mp3 |  | 3802 KB | 1일 마차·오프닝·v111 코드 직접; 장면 음악(records audio) |
| assets/bgm-village.mp3 |  | 2095 KB | 장면 음악(records audio) |
| assets/bgm-village2.mp3 |  | 1082 KB | 장면 음악(records audio) |
| assets/ending/END-01.webp | 1280x720 | 1021 KB | 엔딩 컷 END-01 |
| assets/ending/END-02-base.webp | 1280x720 | 1225 KB | 엔딩 컷 END-02:portrait-mom-childnose; 엔딩 컷 END-02:portrait-piko |
| assets/ending/END-02-portrait-mom-childnose.webp | 1280x720 | 50 KB | 엔딩 컷 END-02:portrait-mom-childnose |
| assets/ending/END-02-portrait-piko.webp | 1280x720 | 51 KB | 엔딩 컷 END-02:portrait-piko |
| assets/ending/END-03.webp | 1280x720 | 1271 KB | 엔딩 컷 END-03 |
| assets/ending/END-04-base.webp | 1280x720 | 940 KB | 엔딩 컷 END-04; 엔딩 컷 END-04:blanket |
| assets/ending/END-04-blanket.webp | 1280x720 | 16 KB | 엔딩 컷 END-04:blanket |
| assets/ending/END-05.webp | 1280x720 | 692 KB | 엔딩 컷 END-05 |
| assets/ending/END-06.webp | 1280x720 | 1154 KB | 엔딩 컷 END-06 |
| assets/ending/END-07.webp | 1280x720 | 891 KB | 엔딩 컷 END-07 |
| assets/ending/END-08.webp | 1280x720 | 973 KB | 엔딩 컷 END-08 |
| assets/ending/END-09.webp | 1280x720 | 821 KB | 엔딩 컷 END-09 |
| assets/ending/END-10.webp | 1280x720 | 1093 KB | 엔딩 컷 END-10 |
| assets/ending/END-11-father-alone.webp | 1672x941 | 43 KB | 엔딩 컷 END-11:father-alone |
| assets/ending/END-11-three.webp | 1672x941 | 104 KB | 엔딩 컷 END-11:three |
| assets/ending/MEM-01.webp | 720x720 | 686 KB | 엔딩 컷 MEM-01 |
| assets/ending/MEM-02.webp | 720x720 | 588 KB | 엔딩 컷 MEM-02 |
| assets/ending/MEM-03.webp | 720x720 | 544 KB | 엔딩 컷 MEM-03 |
| assets/ending/MEM-04.webp | 720x720 | 586 KB | 엔딩 컷 MEM-04 |
| assets/ending/MEM-05.webp | 720x720 | 514 KB | 엔딩 컷 MEM-05 |
| assets/ending/MEM-06.webp | 720x720 | 511 KB | 엔딩 컷 MEM-06 |
| assets/ending/MEM-07.webp | 720x720 | 601 KB | 엔딩 컷 MEM-07 |
| assets/ending/MEM-08.webp | 720x720 | 483 KB | 엔딩 컷 MEM-08 |
| assets/ending/WILD-ENDING-PROPS-a.webp | 720x720 | 684 KB | 엔딩 컷 WILD-ENDING-PROPS-a |
| assets/ending/WILD-ENDING-PROPS-b.webp | 720x720 | 582 KB | 엔딩 컷 WILD-ENDING-PROPS-b |
| assets/evidence/D01_FAMILY_DRAWING.webp | 384x384 | 19 KB | 대사 컷 ev:D01_FAMILY_DRAWING |
| assets/evidence/D01_SNACK_BAG.webp | 384x384 | 9 KB | 대사 컷 ev:D01_SNACK_BAG |
| assets/evidence/E01.webp | 384x384 | 23 KB | 자료 그림 E01 |
| assets/evidence/E02.webp | 384x384 | 30 KB | 자료 그림 E02 |
| assets/evidence/E03.webp | 384x384 | 23 KB | 자료 그림 E03 |
| assets/evidence/E04.webp | 384x384 | 28 KB | 자료 그림 E04 |
| assets/evidence/E05.webp | 384x384 | 27 KB | 대사 컷 ev:E05; 자료 그림 E05 |
| assets/evidence/E06.webp | 384x384 | 24 KB | 자료 그림 E06 |
| assets/evidence/E06_CONTACT.webp | 384x384 | 33 KB | 자료 그림 E06_CONTACT |
| assets/evidence/E06_EMPTY.webp | 384x384 | 19 KB | 자료 그림 E06_EMPTY |
| assets/evidence/E06_FIRE.webp | 384x384 | 29 KB | 자료 그림 E06_FIRE |
| assets/evidence/E06_RESCUE.webp | 384x384 | 32 KB | 자료 그림 E06_RESCUE |
| assets/evidence/E07.webp | 384x384 | 25 KB | 자료 그림 E07 |
| assets/evidence/E08.webp | 384x384 | 21 KB | 자료 그림 E08 |
| assets/evidence/E08_CHILD_ACCOUNT.webp | 384x384 | 21 KB | 자료 그림 E08_CHILD_ACCOUNT |
| assets/evidence/E08_CHILD_POSITION.webp | 384x384 | 27 KB | 자료 그림 E08_CHILD_POSITION |
| assets/evidence/E08_CONTACT_ASSEMBLY.webp | 384x384 | 115 KB | 자료 그림 E08_CONTACT_ASSEMBLY |
| assets/evidence/E08_RECENT_LETTER.webp | 384x384 | 24 KB | 자료 그림 E08_RECENT_LETTER |
| assets/evidence/E08_ROOM.webp | 384x384 | 29 KB | 자료 그림 E08_ROOM |
| assets/evidence/E08_ROOM_REACH.webp | 384x384 | 25 KB | 자료 그림 E08_ROOM_REACH |
| assets/evidence/E08_TOOL.webp | 384x384 | 24 KB | 자료 그림 E08_TOOL |
| assets/evidence/E08_WOUND_WIRE.webp | 384x384 | 32 KB | 자료 그림 E08_WOUND_WIRE |
| assets/evidence/E09_MAIL.webp | 384x384 | 23 KB | 자료 그림 E09_MAIL |
| assets/evidence/E09_PASSAGE.webp | 384x384 | 23 KB | 자료 그림 E09_PASSAGE |
| assets/evidence/E09_PIN_HANDOVER_TIME.webp | 384x384 | 25 KB | 자료 그림 E09_PIN_HANDOVER_TIME |
| assets/evidence/E09_PIN_OWNER.webp | 384x384 | 23 KB | 자료 그림 E09_PIN_OWNER |
| assets/evidence/E09_PIN_TIME.webp | 384x384 | 24 KB | 자료 그림 E09_PIN_TIME |
| assets/evidence/E09_SCARF.webp | 384x384 | 34 KB | 자료 그림 E09_SCARF |
| assets/evidence/E10.webp | 384x384 | 76 KB | 자료 그림 E10 |
| assets/evidence/E10_PUMP.webp | 384x384 | 22 KB | 자료 그림 E10_PUMP |
| assets/evidence/E11.webp | 384x384 | 24 KB | 자료 그림 E11 |
| assets/evidence/E12.webp | 384x384 | 25 KB | 자료 그림 E12 |
| assets/evidence/E12_FRAGMENT.webp | 384x384 | 94 KB | 자료 그림 E12_FRAGMENT |
| assets/evidence/E12_HANDLING.webp | 384x384 | 28 KB | 자료 그림 E12_HANDLING |
| assets/evidence/E12_SEAL.webp | 384x384 | 92 KB | 자료 그림 E12_SEAL |
| assets/evidence/E13.webp | 384x384 | 26 KB | 자료 그림 E13 |
| assets/evidence/E13_HANDOVER.webp | 384x384 | 25 KB | 자료 그림 E13_HANDOVER |
| assets/evidence/E13_ORDER.webp | 384x384 | 24 KB | 자료 그림 E13_ORDER |
| assets/evidence/E14.webp | 384x384 | 29 KB | 자료 그림 E14 |
| assets/evidence/E14_SUPPLY.webp | 384x384 | 24 KB | 자료 그림 E14_SUPPLY |
| assets/evidence/E15.webp | 384x384 | 28 KB | 자료 그림 E15 |
| assets/evidence/E16.webp | 384x384 | 22 KB | 자료 그림 E16 |
| assets/evidence/E17.webp | 384x384 | 25 KB | 자료 그림 E17 |
| assets/evidence/E18.webp | 384x384 | 27 KB | 자료 그림 E18 |
| assets/evidence/E22.webp | 384x384 | 37 KB | 자료 그림 E22 |
| assets/evidence/E23.webp | 384x384 | 79 KB | 자료 그림 E23 |
| assets/evidence/E26.webp | 384x384 | 27 KB | 자료 그림 E26 |
| assets/evidence/E27.webp | 384x384 | 28 KB | 자료 그림 E27 |
| assets/evidence/E28.webp | 384x384 | 25 KB | 자료 그림 E28 |
| assets/evidence/E29.webp | 384x384 | 28 KB | 자료 그림 E29 |
| assets/evidence/E31.webp | 384x384 | 22 KB | 자료 그림 E31 |
| assets/evidence/E32.webp | 384x384 | 30 KB | 자료 그림 E32 |
| assets/evidence/E33.webp | 384x384 | 16 KB | 자료 그림 E33 |
| assets/evidence/E34.webp | 384x384 | 25 KB | 자료 그림 E34 |
| assets/evidence/E35.webp | 384x384 | 28 KB | 자료 그림 E35 |
| assets/evidence/HIDDEN_A3_paper.webp | 720x253 | 200 KB | 대사 컷 ev:HIDDEN_A3_paper |
| assets/evidence/HIDDEN_A3_paper_marked.webp | 720x253 | 194 KB | 대사 컷 ev:HIDDEN_A3_paper_marked |
| assets/evidence/HIDDEN_A3_plate_back.webp | 720x219 | 151 KB | 대사 컷 ev:HIDDEN_A3_plate_back |
| assets/evidence/HIDDEN_A3_plate_front.webp | 720x216 | 161 KB | 대사 컷 ev:HIDDEN_A3_plate_front |
| assets/evidence/HIDDEN_A4_checklist.webp | 720x483 | 312 KB | 대사 컷 ev:HIDDEN_A4_checklist |
| assets/evidence/HIDDEN_A4_section.webp | 720x457 | 312 KB | 대사 컷 ev:HIDDEN_A4_section |
| assets/evidence/HIDDEN_A5_notebook.webp | 720x468 | 323 KB | 대사 컷 ev:HIDDEN_A5_notebook |
| assets/evidence/HIDDEN_P4_after.webp | 720x531 | 109 KB | 대사 컷 ev:HIDDEN_P4_after |
| assets/evidence/HIDDEN_P4_before.webp | 720x526 | 110 KB | 대사 컷 ev:HIDDEN_P4_before |
| assets/evidence/HIDDEN_P4_pin.webp | 644x496 | 96 KB | 대사 컷 ev:HIDDEN_P4_pin |
| assets/evidence/NW_BURNT_PAGE.webp | 384x384 | 25 KB | 자료 그림 NW_BURNT_PAGE |
| assets/evidence/NW_HALL_WINDOW.webp | 384x384 | 28 KB | 자료 그림 NW_HALL_WINDOW |
| assets/evidence/NW_IRON_MARK.webp | 384x384 | 27 KB | 자료 그림 NW_IRON_MARK |
| assets/evidence/NW_KEEPER_DATE.webp | 384x384 | 28 KB | 자료 그림 NW_KEEPER_DATE |
| assets/evidence/NW_LAUNDRY_TALK.webp | 384x384 | 107 KB | 자료 그림 NW_LAUNDRY_TALK |
| assets/evidence/NW_MADAM_DAY7.webp | 384x384 | 24 KB | 자료 그림 NW_MADAM_DAY7 |
| assets/evidence/NW_NAMES.webp | 384x384 | 38 KB | 대사 컷 ev:NW_NAMES; 자료 그림 NW_NAMES |
| assets/evidence/NW_NEOUL_LEDGER.webp | 384x384 | 35 KB | 자료 그림 NW_NEOUL_LEDGER |
| assets/evidence/NW_NUBI_TICKET.webp | 1254x1254 | 688 KB | 자료 그림 NW_NUBI_TICKET |
| assets/evidence/NW_OLD_RATIONS.webp | 384x384 | 24 KB | 자료 그림 NW_OLD_RATIONS |
| assets/evidence/NW_PIKO_PAINTING.webp | 384x384 | 149 KB | 자료 그림 NW_PIKO_PAINTING |
| assets/evidence/NW_PIKO_SKETCH4.webp | 384x384 | 37 KB | 대사 컷 ev:NW_PIKO_SKETCH4; 자료 그림 NW_PIKO_SKETCH4 |
| assets/evidence/NW_PIKO_TREMOR.webp | 384x384 | 18 KB | 자료 그림 NW_PIKO_TREMOR |
| assets/evidence/NW_RETURNED_BOWL.webp | 384x384 | 17 KB | 자료 그림 NW_RETURNED_BOWL |
| assets/evidence/NW_SICK_BEDS.webp | 384x384 | 24 KB | 자료 그림 NW_SICK_BEDS |
| assets/evidence/NW_STONE.webp | 384x384 | 29 KB | 자료 그림 NW_STONE |
| assets/evidence/NW_TABLET_A.webp | 384x384 | 28 KB | 대사 컷 ev:NW_TABLET_A; 자료 그림 NW_TABLET_A |
| assets/evidence/NW_TABLET_B.webp | 384x384 | 33 KB | 자료 그림 NW_TABLET_B |
| assets/evidence/NW_TRANSFER_LIST.webp | 384x384 | 27 KB | 자료 그림 NW_TRANSFER_LIST |
| assets/evidence/NW_WHITE_BOWLS.webp | 384x384 | 17 KB | 자료 그림 NW_WHITE_BOWLS |
| assets/evidence/PROP_D06_cloth_empty_borrowed_bowl.webp | 384x384 | 38 KB | 대사 컷 ev:PROP_D06_cloth_empty_borrowed_bowl |
| assets/evidence/PROP_D06_two_towels_salt_parcel.webp | 384x384 | 30 KB | 대사 컷 ev:PROP_D06_two_towels_salt_parcel |
| assets/evidence/PROP_D11_blank_name_tag_bundle.webp | 384x384 | 36 KB | 대사 컷 ev:PROP_D11_blank_name_tag_bundle |
| assets/evidence/PROP_D11_child_wet_socks.webp | 384x384 | 40 KB | 대사 컷 ev:PROP_D11_child_wet_socks |
| assets/evidence/PROP_D11_sewing_needle_thread.webp | 384x384 | 12 KB | 대사 컷 ev:PROP_D11_sewing_needle_thread |
| assets/evidence/PROP_D12_large_small_ladles.webp | 384x384 | 16 KB | 대사 컷 ev:PROP_D12_large_small_ladles |
| assets/evidence/PROP_D12_teacher_large_red_bowl.webp | 384x384 | 26 KB | 대사 컷 ev:PROP_D12_teacher_large_red_bowl |
| assets/evidence/PROP_D12_white_bowl_crosswise_spoon.webp | 384x384 | 14 KB | 대사 컷 ev:PROP_D12_white_bowl_crosswise_spoon |
| assets/ms14-audio/cart-roll-light.mp3 |  | 43 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/ms14/blanket_ochre.png | 592x580 | 303 KB | MS14_ART blanket_ochre |
| assets/ms14/blanket_teal.png | 588x640 | 314 KB | MS14_ART blanket_teal |
| assets/ms14/box.png | 1504x1040 | 1517 KB | MS14_ART box |
| assets/ms14/box_forest_buried.png | 168x75 | 1 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/ms14/bundle.png | 1484x1038 | 1337 KB | MS14_ART bundle |
| assets/ms14/carriage.webp | 1386x780 | 152 KB | MS14_ART carriage |
| assets/ms14/clinic.webp | 2048x768 | 281 KB | MS14_ART clinic |
| assets/ms14/dining.webp | 2172x724 | 329 KB | MS14_ART dining |
| assets/ms14/family.png | 1536x1024 | 3329 KB | MS14_ART family |
| assets/ms14/forest.webp | 2172x724 | 296 KB | MS14_ART forest |
| assets/ms14/gate.webp | 1672x941 | 348 KB | MS14_ART gate |
| assets/ms14/guardroom.webp | 2048x768 | 195 KB | MS14_ART guardroom |
| assets/ms14/hall.webp | 2172x724 | 262 KB | MS14_ART hall |
| assets/ms14/inn.webp | 1672x941 | 312 KB | MS14_ART inn |
| assets/ms14/portrait_child.png | 1672x941 | 2138 KB | MS14_ART portrait_child |
| assets/ms14/portrait_complete.png | 1672x941 | 2191 KB | MS14_ART portrait_complete |
| assets/ms14/portrait_unfinished.png | 1672x941 | 2376 KB | MS14_ART portrait_unfinished |
| assets/ms14/post.webp | 2160x728 | 271 KB | MS14_ART post |
| assets/ms14/room.webp | 2172x724 | 273 KB | MS14_ART room |
| assets/ms14/somi_inside.webp | 2172x724 | 259 KB | MS14_ART somi_inside |
| assets/ms14/square.webp | 2048x768 | 480 KB | MS14_ART square |
| assets/ms14/stable.webp | 2172x724 | 161 KB | MS14_ART stable |
| assets/ms14/store.webp | 2048x768 | 307 KB | MS14_ART store |
| assets/ms14/warning_private.png | 960x1280 | 117 KB | MS14_ART warning_private |
| assets/ms14/workshop.webp | 1983x793 | 362 KB | MS14_ART workshop |
| assets/room13-acorn-ink-crooked.png | 32x32 | 1 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-bg-guardroom-afternoon.webp | 2048x768 | 1182 KB | 장소 배경 ms14_guardroom |
| assets/room13-bg-guardroom-evening.webp | 2048x768 | 1276 KB | 장소 배경 ms14_guardroom |
| assets/room13-bg-guardroom-morning.webp | 2048x768 | 1204 KB | 장소 배경 ms14_guardroom |
| assets/room13-bg-somi-alley-afternoon.webp | 2048x768 | 1742 KB | 장소 배경 ms14_somi |
| assets/room13-bg-somi-alley-evening.webp | 2048x768 | 1689 KB | 장소 배경 ms14_somi |
| assets/room13-bg-somi-alley-morning.webp | 2048x768 | 1766 KB | 장소 배경 ms14_somi |
| assets/room13-bg-store-2-afternoon.webp | 2048x768 | 1479 KB | 장소 배경 store |
| assets/room13-bg-store-2-evening.webp | 2048x768 | 1430 KB | 장소 배경 store |
| assets/room13-bg-store-2-morning.webp | 2048x768 | 1512 KB | 장소 배경 store |
| assets/room13-carriage-daram-seat-angry.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-bravado.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-joy.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-neutral.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-pout.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-quiz.webp | 149x227 | 9 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-secret.webp | 149x227 | 8 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-carriage-daram-seat-wistful.webp | 149x227 | 7 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-ep-O47-handprints.webp | 2048x768 | 11 KB | 대사 컷 O47-handprints |
| assets/room13-fx-carriage-window-mask.webp | 1280x720 | 1 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-pixel-carriage-empty-winter.webp | 1386x780 | 152 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/room13-pixel-panorama-holding-morning.webp | 2048x768 | 330 KB | 장소 배경 v111_custody; 장소 배경 v111_supervised |
| assets/room13-pixel-panorama-inn-afternoon.webp | 2048x768 | 348 KB | 장소 배경 inn |
| assets/room13-pixel-panorama-inn-evening.webp | 2048x768 | 341 KB | 장소 배경 inn |
| assets/room13-pixel-panorama-inn-morning.webp | 2048x768 | 347 KB | 장소 배경 inn |
| assets/room13-pixel-panorama-laundry-afternoon.webp | 2048x768 | 394 KB | 장소 배경 laundry |
| assets/room13-pixel-panorama-laundry-evening.webp | 2048x768 | 373 KB | 장소 배경 laundry |
| assets/room13-pixel-panorama-school-afternoon.webp | 1983x793 | 413 KB | 장소 배경 school |
| assets/room13-pixel-panorama-school-evening.webp | 1983x793 | 382 KB | 장소 배경 school |
| assets/room13-pixel-panorama-school-morning.webp | 1984x793 | 407 KB | 장소 배경 school |
| assets/room13-pixel-panorama-square-afternoon.webp | 2048x768 | 487 KB | 장소 배경 square |
| assets/room13-pixel-panorama-square-evening.webp | 2048x768 | 417 KB | 장소 배경 square |
| assets/room13-pixel-panorama-square-morning.webp | 2048x768 | 480 KB | 장소 배경 square |
| assets/room13-pixel-panorama-woodshed-fire.webp | 2048x768 | 297 KB | 장소 배경 v111_fire |
| assets/room13-pixel-panorama-woodshed-intact.webp | 2048x768 | 311 KB | 장소 배경 v111_labor |
| assets/room13-pixel-panorama-woodshed-ruin.webp | 2048x768 | 357 KB | 장소 배경 v111_ruin |
| assets/room13-pixel-panorama-workshop-afternoon.webp | 1983x793 | 368 KB | 장소 배경 workshop |
| assets/room13-pixel-panorama-workshop-evening.webp | 1983x793 | 343 KB | 장소 배경 workshop |
| assets/room13-pixel-panorama-workshop-morning.webp | 1983x793 | 362 KB | 장소 배경 workshop |
| assets/room13-pixel-ready-altar0177-afternoon.webp | 2048x768 | 395 KB | 장소 배경 altar |
| assets/room13-pixel-ready-altar0177-evening.webp | 2048x768 | 346 KB | 장소 배경 altar |
| assets/room13-pixel-ready-altar0177-morning.webp | 2048x768 | 392 KB | 장소 배경 altar |
| assets/room13-pixel-ready-clinic0177-afternoon.webp | 2048x768 | 274 KB | 장소 배경 clinic |
| assets/room13-pixel-ready-clinic0177-evening.webp | 2048x768 | 228 KB | 장소 배경 clinic |
| assets/room13-pixel-ready-clinic0177-morning.webp | 2048x768 | 281 KB | 장소 배경 clinic |
| assets/room13-pixel-ready-facility0177-afternoon.webp | 2048x768 | 201 KB | 장소 배경 facility |
| assets/room13-pixel-ready-facility0177-evening.webp | 2048x768 | 159 KB | 장소 배경 facility |
| assets/room13-pixel-ready-facility0177-morning.webp | 2048x768 | 195 KB | 장소 배경 facility |
| assets/room13-pixel-ready-gate0173-afternoon.webp | 2048x768 | 433 KB | 장소 배경 gate |
| assets/room13-pixel-ready-gate0173-evening.webp | 2048x768 | 378 KB | 장소 배경 gate |
| assets/room13-pixel-ready-gate0173-morning.webp | 2048x768 | 431 KB | 장소 배경 gate |
| assets/room13-pixel-ready-greenhouse0177-afternoon.webp | 2048x768 | 386 KB | 장소 배경 greenhouse |
| assets/room13-pixel-ready-greenhouse0177-evening.webp | 2048x768 | 315 KB | 장소 배경 greenhouse |
| assets/room13-pixel-ready-greenhouse0177-morning.webp | 2048x768 | 388 KB | 장소 배경 greenhouse |
| assets/room13-pixel-wide-ancient-day.webp | 2172x724 | 1389 KB | 장소 배경 ancient |
| assets/room13-pixel-wide-dining-afternoon.webp | 2172x724 | 333 KB | 장소 배경 dining |
| assets/room13-pixel-wide-dining-evening.webp | 2172x724 | 308 KB | 장소 배경 dining |
| assets/room13-pixel-wide-dining-morning.webp | 2172x724 | 329 KB | 장소 배경 dining |
| assets/room13-pixel-wide-facility-afternoon.webp | 2560x768 | 1044 KB | 장소 배경 facility(later_bindings 덮어쓰기) |
| assets/room13-pixel-wide-facility-evening.webp | 2560x768 | 883 KB | 장소 배경 facility(later_bindings 덮어쓰기) |
| assets/room13-pixel-wide-facility-morning.webp | 2560x768 | 1049 KB | 장소 배경 facility(later_bindings 덮어쓰기) |
| assets/room13-pixel-wide-forest-afternoon.webp | 2172x724 | 340 KB | 장소 배경 forest |
| assets/room13-pixel-wide-forest-evening.webp | 2172x724 | 248 KB | 장소 배경 forest |
| assets/room13-pixel-wide-forest-morning.webp | 2172x724 | 296 KB | 장소 배경 forest |
| assets/room13-pixel-wide-hall-after-afternoon.webp | 2172x724 | 251 KB | 장소 배경 hall |
| assets/room13-pixel-wide-hall-after-evening.webp | 2172x724 | 232 KB | 장소 배경 hall |
| assets/room13-pixel-wide-hall-after-morning.webp | 2172x724 | 258 KB | 장소 배경 hall |
| assets/room13-pixel-wide-hall-before-afternoon.webp | 2172x724 | 259 KB | 장소 배경 hall |
| assets/room13-pixel-wide-hall-before-evening.webp | 2172x724 | 232 KB | 장소 배경 hall |
| assets/room13-pixel-wide-hall-before-morning.webp | 2172x724 | 262 KB | 장소 배경 hall |
| assets/room13-pixel-wide-kitchen-afternoon.webp | 2172x724 | 280 KB | 장소 배경 kitchen |
| assets/room13-pixel-wide-kitchen-evening.webp | 2172x724 | 240 KB | 장소 배경 kitchen |
| assets/room13-pixel-wide-kitchen-morning.webp | 2172x724 | 279 KB | 장소 배경 kitchen |
| assets/room13-pixel-wide-post-morning.webp | 2160x728 | 271 KB | 장소 배경 post |
| assets/room13-pixel-wide-room13-after-afternoon.webp | 2172x724 | 273 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-room13-after-evening.webp | 2172x724 | 257 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-room13-after-morning.webp | 2172x724 | 280 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-room13-before-afternoon.webp | 2172x724 | 277 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-room13-before-evening.webp | 2172x724 | 255 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-room13-before-morning.webp | 2172x724 | 273 KB | 장소 배경 room13 |
| assets/room13-pixel-wide-woodshed-inside-afternoon.webp | 2560x768 | 80 KB | 장소 배경 v111_woodshed |
| assets/room13-pixel-wide-woodshed-inside-evening.webp | 2560x768 | 81 KB | 장소 배경 v111_woodshed |
| assets/room13-v111-blanket-after.webp | 1254x1254 | 144 KB | 대사 컷 v111_blanket_after |
| assets/room13-v111-blanket-before.webp | 1254x1254 | 142 KB | 대사 컷 v111_blanket_before |
| assets/sfx-carriage-hooves.wav |  | 193 KB | 1일 마차·오프닝·v111 코드 직접 |
| assets/wild-night/wild-village-dawn-ash.webp | 1672x941 | 2108 KB | 엔딩 컷 END-11 |

## B1. 출연자 인물 그림 (3217개, 254.3 MB)

| 인물 키 | 파일 수 | 용량 |
|---|---|---|
| resident_teacher | 99 | 15.0 MB |
| doto | 83 | 12.0 MB |
| daram | 123 | 11.7 MB |
| neoul | 90 | 11.1 MB |
| resident_lamplighter | 88 | 10.8 MB |
| guard | 87 | 9.2 MB |
| resident_bori | 78 | 8.8 MB |
| resident_musoe | 69 | 8.0 MB |
| granny | 91 | 7.1 MB |
| mom | 97 | 7.1 MB |
| resident_nubi | 76 | 6.9 MB |
| resident_tosil | 71 | 6.7 MB |
| resident_madam | 70 | 6.7 MB |
| nabi | 106 | 6.6 MB |
| seryeon | 80 | 6.6 MB |
| bami | 88 | 6.1 MB |
| resident_piko | 75 | 5.9 MB |
| resident_ppul | 85 | 5.8 MB |
| resident_siluk | 72 | 5.8 MB |
| resident_nero | 77 | 5.3 MB |
| v111_lowerroad_elder | 22 | 5.2 MB |
| kid_kkomi | 79 | 5.1 MB |
| karo | 71 | 5.1 MB |
| buri | 90 | 5.0 MB |
| resident_badook | 75 | 4.8 MB |
| resident_seori | 84 | 4.7 MB |
| resident_ttadak | 67 | 4.5 MB |
| npc_pandol | 64 | 4.3 MB |
| resident_ubak | 69 | 4.3 MB |
| resident_eunho | 68 | 3.9 MB |
| resident_kongi | 66 | 3.9 MB |
| resident_sling | 69 | 3.9 MB |
| resident_tok | 72 | 3.8 MB |
| resident_guldol | 65 | 3.6 MB |
| kid_saemi | 65 | 3.6 MB |
| resident_owlgp | 71 | 3.5 MB |
| resident_momo | 65 | 3.3 MB |
| kid_dodam | 65 | 3.3 MB |
| resident_somi | 63 | 3.2 MB |
| dad | 27 | 2.6 MB |
| kid_bang | 34 | 2.2 MB |
| kid_mong | 29 | 2.0 MB |
| kid_kkam | 29 | 1.6 MB |
| kid_nubi1 | 29 | 1.4 MB |
| kid_nubi2 | 26 | 1.2 MB |
| resident_librarian | 1 | 0.3 MB |
| bodum | 1 | 0.3 MB |
| ms14_attendant | 12 | 0.1 MB |
| v111_patrol | 13 | 0.1 MB |
| npc_panseol | 7 | 0.1 MB |
| kid_nubi3 | 12 | 0.1 MB |
| v111_resident | 1 | 0.0 MB |
| v111_child | 1 | 0.0 MB |

| 폴더 | 파일 수 | 용량 |
|---|---|---|
| (assets 바로 아래) | 602 | 88.8 MB |
| dialogue-source-master | 774 | 55.5 MB |
| dialogue-source-master-v2 | 684 | 39.0 MB |
| dialogue-b-primary50 | 50 | 12.9 MB |
| investigation-canonical-20261018 | 12 | 10.9 MB |
| dialogue-context-master | 60 | 9.0 MB |
| resident-poses-a | 18 | 7.4 MB |
| dialogue-pose-source | 42 | 5.7 MB |
| lowerroad-elder | 9 | 5.1 MB |
| dialogue-dot-v2 | 510 | 3.9 MB |
| map-work-nine | 4 | 2.8 MB |
| map-action27 | 27 | 2.4 MB |
| profile-source-master | 43 | 2.2 MB |
| investigation-source2 | 2 | 1.9 MB |
| resident-a-20261024 | 2 | 1.9 MB |
| field-dot-v2 | 311 | 1.8 MB |
| meeting-source-master | 6 | 1.3 MB |
| ui-b-options | 6 | 1.3 MB |
| dialogue-b-faces | 50 | 0.6 MB |
| meeting-stand | 5 | 0.0 MB |

<details><summary>B1 인물 그림 전체 3217개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/dialogue-b-faces/granny_angry.webp | 160x160 | 8 KB | granny |
| assets/dialogue-b-faces/granny_anxious.webp | 160x160 | 8 KB | granny |
| assets/dialogue-b-faces/granny_joy.webp | 160x160 | 8 KB | granny |
| assets/dialogue-b-faces/granny_surprise_react.webp | 160x160 | 8 KB | granny |
| assets/dialogue-b-faces/granny_surprise_talk.webp | 160x160 | 9 KB | granny |
| assets/dialogue-b-faces/guard_angry.webp | 160x160 | 11 KB | guard |
| assets/dialogue-b-faces/guard_anxious.webp | 160x160 | 11 KB | guard |
| assets/dialogue-b-faces/guard_joy.webp | 160x160 | 11 KB | guard |
| assets/dialogue-b-faces/guard_surprise_react.webp | 160x160 | 12 KB | guard |
| assets/dialogue-b-faces/guard_surprise_talk.webp | 160x160 | 11 KB | guard |
| assets/dialogue-b-faces/mom_angry.webp | 160x160 | 13 KB | mom |
| assets/dialogue-b-faces/mom_anxious.webp | 160x160 | 13 KB | mom |
| assets/dialogue-b-faces/mom_joy.webp | 160x160 | 13 KB | mom |
| assets/dialogue-b-faces/mom_surprise_react.webp | 160x160 | 13 KB | mom |
| assets/dialogue-b-faces/mom_surprise_talk.webp | 160x160 | 13 KB | mom |
| assets/dialogue-b-faces/nabi_angry.webp | 160x160 | 11 KB | nabi |
| assets/dialogue-b-faces/nabi_anxious.webp | 160x160 | 10 KB | nabi |
| assets/dialogue-b-faces/nabi_joy.webp | 160x160 | 11 KB | nabi |
| assets/dialogue-b-faces/nabi_surprise_react.webp | 160x160 | 11 KB | nabi |
| assets/dialogue-b-faces/nabi_surprise_talk.webp | 160x160 | 12 KB | nabi |
| assets/dialogue-b-faces/neoul_angry.webp | 160x160 | 12 KB | neoul |
| assets/dialogue-b-faces/neoul_anxious.webp | 160x160 | 14 KB | neoul |
| assets/dialogue-b-faces/neoul_joy.webp | 160x160 | 11 KB | neoul |
| assets/dialogue-b-faces/neoul_surprise_react.webp | 160x160 | 12 KB | neoul |
| assets/dialogue-b-faces/neoul_surprise_talk.webp | 160x160 | 13 KB | neoul |
| assets/dialogue-b-faces/resident_lamplighter_angry.webp | 160x160 | 8 KB | resident_lamplighter |
| assets/dialogue-b-faces/resident_lamplighter_anxious.webp | 160x160 | 8 KB | resident_lamplighter |
| assets/dialogue-b-faces/resident_lamplighter_joy.webp | 160x160 | 8 KB | resident_lamplighter |
| assets/dialogue-b-faces/resident_lamplighter_surprise_react.webp | 160x160 | 7 KB | resident_lamplighter |
| assets/dialogue-b-faces/resident_lamplighter_surprise_talk.webp | 160x160 | 8 KB | resident_lamplighter |
| assets/dialogue-b-faces/resident_nero_angry.webp | 160x160 | 12 KB | resident_nero |
| assets/dialogue-b-faces/resident_nero_anxious.webp | 160x160 | 11 KB | resident_nero |
| assets/dialogue-b-faces/resident_nero_joy.webp | 160x160 | 13 KB | resident_nero |
| assets/dialogue-b-faces/resident_nero_surprise_react.webp | 160x160 | 13 KB | resident_nero |
| assets/dialogue-b-faces/resident_nero_surprise_talk.webp | 160x160 | 14 KB | resident_nero |
| assets/dialogue-b-faces/resident_ppul_angry.webp | 160x160 | 13 KB | resident_ppul |
| assets/dialogue-b-faces/resident_ppul_anxious.webp | 160x160 | 13 KB | resident_ppul |
| assets/dialogue-b-faces/resident_ppul_joy.webp | 160x160 | 13 KB | resident_ppul |
| assets/dialogue-b-faces/resident_ppul_surprise_react.webp | 160x160 | 12 KB | resident_ppul |
| assets/dialogue-b-faces/resident_ppul_surprise_talk.webp | 160x160 | 13 KB | resident_ppul |
| assets/dialogue-b-faces/resident_seori_angry.webp | 160x160 | 12 KB | resident_seori |
| assets/dialogue-b-faces/resident_seori_anxious.webp | 160x160 | 12 KB | resident_seori |
| assets/dialogue-b-faces/resident_seori_joy.webp | 160x160 | 12 KB | resident_seori |
| assets/dialogue-b-faces/resident_seori_surprise_react.webp | 160x160 | 12 KB | resident_seori |
| assets/dialogue-b-faces/resident_seori_surprise_talk.webp | 160x160 | 12 KB | resident_seori |
| assets/dialogue-b-faces/resident_teacher_angry.webp | 160x160 | 12 KB | resident_teacher |
| assets/dialogue-b-faces/resident_teacher_anxious.webp | 160x160 | 13 KB | resident_teacher |
| assets/dialogue-b-faces/resident_teacher_joy.webp | 160x160 | 13 KB | resident_teacher |
| assets/dialogue-b-faces/resident_teacher_surprise_react.webp | 160x160 | 12 KB | resident_teacher |
| assets/dialogue-b-faces/resident_teacher_surprise_talk.webp | 160x160 | 13 KB | resident_teacher |
| assets/dialogue-b-primary50/granny_angry.webp | 560x840 | 246 KB | granny |
| assets/dialogue-b-primary50/granny_anxious.webp | 560x840 | 232 KB | granny |
| assets/dialogue-b-primary50/granny_joy.webp | 560x840 | 247 KB | granny |
| assets/dialogue-b-primary50/granny_surprise_react.webp | 560x840 | 229 KB | granny |
| assets/dialogue-b-primary50/granny_surprise_talk.webp | 560x840 | 234 KB | granny |
| assets/dialogue-b-primary50/guard_angry.webp | 560x840 | 286 KB | guard |
| assets/dialogue-b-primary50/guard_anxious.webp | 560x840 | 265 KB | guard |
| assets/dialogue-b-primary50/guard_joy.webp | 560x840 | 277 KB | guard |
| assets/dialogue-b-primary50/guard_surprise_react.webp | 560x840 | 282 KB | guard |
| assets/dialogue-b-primary50/guard_surprise_talk.webp | 560x840 | 269 KB | guard |
| assets/dialogue-b-primary50/mom_angry.webp | 560x840 | 294 KB | mom |
| assets/dialogue-b-primary50/mom_anxious.webp | 560x840 | 294 KB | mom |
| assets/dialogue-b-primary50/mom_joy.webp | 560x840 | 302 KB | mom |
| assets/dialogue-b-primary50/mom_surprise_react.webp | 560x840 | 300 KB | mom |
| assets/dialogue-b-primary50/mom_surprise_talk.webp | 560x840 | 295 KB | mom |
| assets/dialogue-b-primary50/nabi_angry.webp | 560x840 | 242 KB | nabi |
| assets/dialogue-b-primary50/nabi_anxious.webp | 560x840 | 213 KB | nabi |
| assets/dialogue-b-primary50/nabi_joy.webp | 560x840 | 221 KB | nabi |
| assets/dialogue-b-primary50/nabi_surprise_react.webp | 560x840 | 268 KB | nabi |
| assets/dialogue-b-primary50/nabi_surprise_talk.webp | 560x840 | 253 KB | nabi |
| assets/dialogue-b-primary50/neoul_angry.webp | 560x840 | 289 KB | neoul |
| assets/dialogue-b-primary50/neoul_anxious.webp | 560x840 | 279 KB | neoul |
| assets/dialogue-b-primary50/neoul_joy.webp | 560x840 | 289 KB | neoul |
| assets/dialogue-b-primary50/neoul_surprise_react.webp | 560x840 | 291 KB | neoul |
| assets/dialogue-b-primary50/neoul_surprise_talk.webp | 560x840 | 277 KB | neoul |
| assets/dialogue-b-primary50/resident_lamplighter_angry.webp | 560x840 | 268 KB | resident_lamplighter |
| assets/dialogue-b-primary50/resident_lamplighter_anxious.webp | 560x840 | 256 KB | resident_lamplighter |
| assets/dialogue-b-primary50/resident_lamplighter_joy.webp | 560x840 | 246 KB | resident_lamplighter |
| assets/dialogue-b-primary50/resident_lamplighter_surprise_react.webp | 560x840 | 292 KB | resident_lamplighter |
| assets/dialogue-b-primary50/resident_lamplighter_surprise_talk.webp | 560x840 | 252 KB | resident_lamplighter |
| assets/dialogue-b-primary50/resident_nero_angry.webp | 560x840 | 266 KB | resident_nero |
| assets/dialogue-b-primary50/resident_nero_anxious.webp | 560x840 | 246 KB | resident_nero |
| assets/dialogue-b-primary50/resident_nero_joy.webp | 560x840 | 269 KB | resident_nero |
| assets/dialogue-b-primary50/resident_nero_surprise_react.webp | 560x840 | 254 KB | resident_nero |
| assets/dialogue-b-primary50/resident_nero_surprise_talk.webp | 560x840 | 264 KB | resident_nero |
| assets/dialogue-b-primary50/resident_ppul_angry.webp | 560x840 | 289 KB | resident_ppul |
| assets/dialogue-b-primary50/resident_ppul_anxious.webp | 560x840 | 261 KB | resident_ppul |
| assets/dialogue-b-primary50/resident_ppul_joy.webp | 560x840 | 282 KB | resident_ppul |
| assets/dialogue-b-primary50/resident_ppul_surprise_react.webp | 560x840 | 289 KB | resident_ppul |
| assets/dialogue-b-primary50/resident_ppul_surprise_talk.webp | 560x840 | 273 KB | resident_ppul |
| assets/dialogue-b-primary50/resident_seori_angry.webp | 560x840 | 213 KB | resident_seori |
| assets/dialogue-b-primary50/resident_seori_anxious.webp | 560x840 | 213 KB | resident_seori |
| assets/dialogue-b-primary50/resident_seori_joy.webp | 560x840 | 219 KB | resident_seori |
| assets/dialogue-b-primary50/resident_seori_surprise_react.webp | 560x840 | 225 KB | resident_seori |
| assets/dialogue-b-primary50/resident_seori_surprise_talk.webp | 560x840 | 198 KB | resident_seori |
| assets/dialogue-b-primary50/resident_teacher_angry.webp | 560x840 | 281 KB | resident_teacher |
| assets/dialogue-b-primary50/resident_teacher_anxious.webp | 560x840 | 299 KB | resident_teacher |
| assets/dialogue-b-primary50/resident_teacher_joy.webp | 560x840 | 277 KB | resident_teacher |
| assets/dialogue-b-primary50/resident_teacher_surprise_react.webp | 560x840 | 280 KB | resident_teacher |
| assets/dialogue-b-primary50/resident_teacher_surprise_talk.webp | 560x840 | 299 KB | resident_teacher |
| assets/dialogue-context-master/bami/560/small_relief.webp | 282x532 | 49 KB | bami |
| assets/dialogue-context-master/bami/760/small_relief.webp | 327x617 | 59 KB | bami |
| assets/dialogue-context-master/bami/840/small_relief.webp | 422x796 | 81 KB | bami |
| assets/dialogue-context-master/daram/560/intake21_01_bravado.webp | 285x500 | 104 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_02_reproach_lean.webp | 285x500 | 104 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_03_stubborn.webp | 285x500 | 102 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_04_flustered.webp | 285x500 | 108 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_05_playful_evasion.webp | 285x500 | 103 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_06_eureka.webp | 285x500 | 111 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_07_delighted.webp | 285x500 | 104 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_08_scared_brave.webp | 285x500 | 105 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_09_wipe_tears.webp | 285x500 | 108 KB | daram |
| assets/dialogue-context-master/daram/560/intake21_10_resolve.webp | 285x500 | 105 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_01_bravado.webp | 388x681 | 180 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_02_reproach_lean.webp | 388x681 | 179 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_03_stubborn.webp | 388x681 | 176 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_04_flustered.webp | 388x681 | 186 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_05_playful_evasion.webp | 388x681 | 176 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_06_eureka.webp | 388x681 | 189 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_07_delighted.webp | 388x681 | 180 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_08_scared_brave.webp | 388x681 | 179 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_09_wipe_tears.webp | 388x681 | 184 KB | daram |
| assets/dialogue-context-master/daram/760/intake21_10_resolve.webp | 388x681 | 181 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_01_bravado.webp | 427x751 | 210 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_02_reproach_lean.webp | 427x751 | 209 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_03_stubborn.webp | 427x751 | 205 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_04_flustered.webp | 427x751 | 217 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_05_playful_evasion.webp | 427x751 | 206 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_06_eureka.webp | 427x751 | 220 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_07_delighted.webp | 427x751 | 209 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_08_scared_brave.webp | 427x751 | 210 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_09_wipe_tears.webp | 427x751 | 215 KB | daram |
| assets/dialogue-context-master/daram/840/intake21_10_resolve.webp | 427x751 | 211 KB | daram |
| assets/dialogue-context-master/kid_dodam/560/intake21_dodam_joy.webp | 345x485 | 122 KB | kid_dodam |
| assets/dialogue-context-master/kid_dodam/760/intake21_dodam_joy.webp | 414x583 | 165 KB | kid_dodam |
| assets/dialogue-context-master/kid_dodam/840/intake21_dodam_joy.webp | 517x728 | 234 KB | kid_dodam |
| assets/dialogue-context-master/kid_kkomi/560/intake21_kkomi_anxious.webp | 379x505 | 125 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/560/intake21_kkomi_joy.webp | 378x505 | 136 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/560/resilient_pride.webp | 331x497 | 51 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/760/intake21_kkomi_anxious.webp | 455x606 | 169 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/760/intake21_kkomi_joy.webp | 454x606 | 184 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/760/resilient_pride.webp | 398x597 | 66 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/840/intake21_kkomi_anxious.webp | 568x757 | 243 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/840/intake21_kkomi_joy.webp | 567x756 | 264 KB | kid_kkomi |
| assets/dialogue-context-master/kid_kkomi/840/resilient_pride.webp | 497x745 | 91 KB | kid_kkomi |
| assets/dialogue-context-master/kid_saemi/560/intake21_saemi_anxious.webp | 364x511 | 141 KB | kid_saemi |
| assets/dialogue-context-master/kid_saemi/760/intake21_saemi_anxious.webp | 437x614 | 191 KB | kid_saemi |
| assets/dialogue-context-master/kid_saemi/840/intake21_saemi_anxious.webp | 546x768 | 270 KB | kid_saemi |
| assets/dialogue-context-master/resident_lamplighter/560/guarded_relief.webp | 383x586 | 55 KB | resident_lamplighter |
| assets/dialogue-context-master/resident_lamplighter/760/guarded_relief.webp | 399x611 | 58 KB | resident_lamplighter |
| assets/dialogue-context-master/resident_lamplighter/840/guarded_relief.webp | 575x880 | 96 KB | resident_lamplighter |
| assets/dialogue-context-master/resident_tosil/560/empathetic_confusion.webp | 365x588 | 54 KB | resident_tosil |
| assets/dialogue-context-master/resident_tosil/760/empathetic_confusion.webp | 381x612 | 56 KB | resident_tosil |
| assets/dialogue-context-master/resident_tosil/840/empathetic_confusion.webp | 547x880 | 94 KB | resident_tosil |
| assets/dialogue-context-master/resident_ubak/560/intake21_ubak_angry.webp | 372x592 | 155 KB | resident_ubak |
| assets/dialogue-context-master/resident_ubak/560/intake21_ubak_anxious.webp | 371x591 | 152 KB | resident_ubak |
| assets/dialogue-context-master/resident_ubak/760/intake21_ubak_angry.webp | 386x616 | 164 KB | resident_ubak |
| assets/dialogue-context-master/resident_ubak/760/intake21_ubak_anxious.webp | 386x615 | 162 KB | resident_ubak |
| assets/dialogue-context-master/resident_ubak/840/intake21_ubak_angry.webp | 556x887 | 291 KB | resident_ubak |
| assets/dialogue-context-master/resident_ubak/840/intake21_ubak_anxious.webp | 556x886 | 286 KB | resident_ubak |
| assets/dialogue-dot-v2/bami/560/angry.webp | 228x342 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/560/anxious.webp | 228x342 | 4 KB | bami |
| assets/dialogue-dot-v2/bami/560/flustered.webp | 228x342 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/560/joy.webp | 228x342 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/560/neutral.webp | 228x342 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/560/surprise_talk.webp | 228x342 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/760/angry.webp | 342x513 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/760/anxious.webp | 342x513 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/760/flustered.webp | 342x513 | 5 KB | bami |
| assets/dialogue-dot-v2/bami/760/joy.webp | 342x513 | 6 KB | bami |
| assets/dialogue-dot-v2/bami/760/neutral.webp | 342x513 | 6 KB | bami |
| assets/dialogue-dot-v2/bami/760/surprise_talk.webp | 342x513 | 5 KB | bami |
| assets/dialogue-dot-v2/buri/560/angry.webp | 260x390 | 5 KB | buri |
| assets/dialogue-dot-v2/buri/560/anxious.webp | 260x390 | 5 KB | buri |
| assets/dialogue-dot-v2/buri/560/flustered.webp | 260x390 | 5 KB | buri |
| assets/dialogue-dot-v2/buri/560/joy.webp | 260x390 | 6 KB | buri |
| assets/dialogue-dot-v2/buri/560/neutral.webp | 260x390 | 6 KB | buri |
| assets/dialogue-dot-v2/buri/560/surprise_talk.webp | 260x390 | 5 KB | buri |
| assets/dialogue-dot-v2/buri/760/angry.webp | 390x585 | 6 KB | buri |
| assets/dialogue-dot-v2/buri/760/anxious.webp | 390x585 | 5 KB | buri |
| assets/dialogue-dot-v2/buri/760/flustered.webp | 390x585 | 6 KB | buri |
| assets/dialogue-dot-v2/buri/760/joy.webp | 390x585 | 7 KB | buri |
| assets/dialogue-dot-v2/buri/760/neutral.webp | 390x585 | 6 KB | buri |
| assets/dialogue-dot-v2/buri/760/surprise_talk.webp | 390x585 | 6 KB | buri |
| assets/dialogue-dot-v2/daram/560/angry.webp | 224x336 | 5 KB | daram |
| assets/dialogue-dot-v2/daram/560/anxious.webp | 224x336 | 5 KB | daram |
| assets/dialogue-dot-v2/daram/560/flustered.webp | 224x336 | 5 KB | daram |
| assets/dialogue-dot-v2/daram/560/joy.webp | 224x336 | 5 KB | daram |
| assets/dialogue-dot-v2/daram/560/neutral.webp | 224x336 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/560/surprise_talk.webp | 224x336 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/angry.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/anxious.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/flustered.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/joy.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/neutral.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/daram/760/surprise_talk.webp | 336x504 | 6 KB | daram |
| assets/dialogue-dot-v2/doto/560/angry.webp | 294x442 | 8 KB | doto |
| assets/dialogue-dot-v2/doto/560/anxious.webp | 294x442 | 6 KB | doto |
| assets/dialogue-dot-v2/doto/560/flustered.webp | 294x442 | 7 KB | doto |
| assets/dialogue-dot-v2/doto/560/joy.webp | 294x442 | 7 KB | doto |
| assets/dialogue-dot-v2/doto/560/neutral.webp | 294x442 | 7 KB | doto |
| assets/dialogue-dot-v2/doto/560/surprise_talk.webp | 294x442 | 7 KB | doto |
| assets/dialogue-dot-v2/doto/760/angry.webp | 441x663 | 8 KB | doto |
| assets/dialogue-dot-v2/doto/760/anxious.webp | 441x663 | 7 KB | doto |
| assets/dialogue-dot-v2/doto/760/flustered.webp | 441x663 | 8 KB | doto |
| assets/dialogue-dot-v2/doto/760/joy.webp | 441x663 | 8 KB | doto |
| assets/dialogue-dot-v2/doto/760/neutral.webp | 441x663 | 8 KB | doto |
| assets/dialogue-dot-v2/doto/760/surprise_talk.webp | 441x663 | 7 KB | doto |
| assets/dialogue-dot-v2/granny/560/angry.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/560/anxious.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/560/flustered.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/560/joy.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/560/neutral.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/560/surprise_talk.webp | 266x400 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/760/angry.webp | 399x600 | 7 KB | granny |
| assets/dialogue-dot-v2/granny/760/anxious.webp | 399x600 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/760/flustered.webp | 399x600 | 6 KB | granny |
| assets/dialogue-dot-v2/granny/760/joy.webp | 399x600 | 7 KB | granny |
| assets/dialogue-dot-v2/granny/760/neutral.webp | 399x600 | 7 KB | granny |
| assets/dialogue-dot-v2/granny/760/surprise_talk.webp | 399x600 | 7 KB | granny |
| assets/dialogue-dot-v2/guard/560/angry.webp | 292x438 | 8 KB | guard |
| assets/dialogue-dot-v2/guard/560/anxious.webp | 292x438 | 7 KB | guard |
| assets/dialogue-dot-v2/guard/560/flustered.webp | 292x438 | 8 KB | guard |
| assets/dialogue-dot-v2/guard/560/joy.webp | 292x438 | 8 KB | guard |
| assets/dialogue-dot-v2/guard/560/neutral.webp | 292x438 | 9 KB | guard |
| assets/dialogue-dot-v2/guard/560/surprise_talk.webp | 292x438 | 9 KB | guard |
| assets/dialogue-dot-v2/guard/760/angry.webp | 438x657 | 9 KB | guard |
| assets/dialogue-dot-v2/guard/760/anxious.webp | 438x657 | 8 KB | guard |
| assets/dialogue-dot-v2/guard/760/flustered.webp | 438x657 | 8 KB | guard |
| assets/dialogue-dot-v2/guard/760/joy.webp | 438x657 | 9 KB | guard |
| assets/dialogue-dot-v2/guard/760/neutral.webp | 438x657 | 10 KB | guard |
| assets/dialogue-dot-v2/guard/760/surprise_talk.webp | 438x657 | 10 KB | guard |
| assets/dialogue-dot-v2/karo/560/angry.webp | 322x482 | 9 KB | karo |
| assets/dialogue-dot-v2/karo/560/anxious.webp | 322x482 | 7 KB | karo |
| assets/dialogue-dot-v2/karo/560/flustered.webp | 322x482 | 9 KB | karo |
| assets/dialogue-dot-v2/karo/560/joy.webp | 322x482 | 9 KB | karo |
| assets/dialogue-dot-v2/karo/560/neutral.webp | 322x482 | 8 KB | karo |
| assets/dialogue-dot-v2/karo/560/surprise_talk.webp | 322x482 | 9 KB | karo |
| assets/dialogue-dot-v2/karo/760/angry.webp | 483x723 | 10 KB | karo |
| assets/dialogue-dot-v2/karo/760/anxious.webp | 483x723 | 8 KB | karo |
| assets/dialogue-dot-v2/karo/760/flustered.webp | 483x723 | 10 KB | karo |
| assets/dialogue-dot-v2/karo/760/joy.webp | 483x723 | 10 KB | karo |
| assets/dialogue-dot-v2/karo/760/neutral.webp | 483x723 | 9 KB | karo |
| assets/dialogue-dot-v2/karo/760/surprise_talk.webp | 483x723 | 10 KB | karo |
| assets/dialogue-dot-v2/kid_dodam/560/angry.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/560/anxious.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/560/flustered.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/560/joy.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/560/neutral.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/560/surprise_talk.webp | 200x302 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/angry.webp | 300x453 | 5 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/anxious.webp | 300x453 | 4 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/flustered.webp | 300x453 | 5 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/joy.webp | 300x453 | 5 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/neutral.webp | 300x453 | 5 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_dodam/760/surprise_talk.webp | 300x453 | 5 KB | kid_dodam |
| assets/dialogue-dot-v2/kid_kkomi/560/angry.webp | 232x348 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/560/anxious.webp | 232x348 | 5 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/560/flustered.webp | 232x348 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/560/joy.webp | 232x348 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/560/neutral.webp | 232x348 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/560/surprise_talk.webp | 232x348 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/angry.webp | 348x522 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/anxious.webp | 348x522 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/flustered.webp | 348x522 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/joy.webp | 348x522 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/neutral.webp | 348x522 | 6 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_kkomi/760/surprise_talk.webp | 348x522 | 7 KB | kid_kkomi |
| assets/dialogue-dot-v2/kid_saemi/560/angry.webp | 240x362 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/560/anxious.webp | 240x362 | 6 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/560/flustered.webp | 240x362 | 6 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/560/joy.webp | 240x362 | 6 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/560/neutral.webp | 240x362 | 6 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/560/surprise_talk.webp | 240x362 | 6 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/angry.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/anxious.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/flustered.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/joy.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/neutral.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/kid_saemi/760/surprise_talk.webp | 360x543 | 7 KB | kid_saemi |
| assets/dialogue-dot-v2/mom/560/angry.webp | 290x434 | 9 KB | mom |
| assets/dialogue-dot-v2/mom/560/anxious.webp | 290x434 | 8 KB | mom |
| assets/dialogue-dot-v2/mom/560/flustered.webp | 290x434 | 8 KB | mom |
| assets/dialogue-dot-v2/mom/560/joy.webp | 290x434 | 8 KB | mom |
| assets/dialogue-dot-v2/mom/560/neutral.webp | 290x434 | 9 KB | mom |
| assets/dialogue-dot-v2/mom/560/surprise_talk.webp | 290x434 | 8 KB | mom |
| assets/dialogue-dot-v2/mom/760/angry.webp | 435x651 | 10 KB | mom |
| assets/dialogue-dot-v2/mom/760/anxious.webp | 435x651 | 9 KB | mom |
| assets/dialogue-dot-v2/mom/760/flustered.webp | 435x651 | 9 KB | mom |
| assets/dialogue-dot-v2/mom/760/joy.webp | 435x651 | 9 KB | mom |
| assets/dialogue-dot-v2/mom/760/neutral.webp | 435x651 | 10 KB | mom |
| assets/dialogue-dot-v2/mom/760/surprise_talk.webp | 435x651 | 9 KB | mom |
| assets/dialogue-dot-v2/nabi/560/angry.webp | 288x432 | 8 KB | nabi |
| assets/dialogue-dot-v2/nabi/560/anxious.webp | 288x432 | 6 KB | nabi |
| assets/dialogue-dot-v2/nabi/560/flustered.webp | 288x432 | 7 KB | nabi |
| assets/dialogue-dot-v2/nabi/560/joy.webp | 288x432 | 8 KB | nabi |
| assets/dialogue-dot-v2/nabi/560/neutral.webp | 288x432 | 8 KB | nabi |
| assets/dialogue-dot-v2/nabi/560/surprise_talk.webp | 288x432 | 7 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/angry.webp | 432x648 | 9 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/anxious.webp | 432x648 | 7 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/flustered.webp | 432x648 | 8 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/joy.webp | 432x648 | 9 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/neutral.webp | 432x648 | 9 KB | nabi |
| assets/dialogue-dot-v2/nabi/760/surprise_talk.webp | 432x648 | 8 KB | nabi |
| assets/dialogue-dot-v2/neoul/560/angry.webp | 288x430 | 9 KB | neoul |
| assets/dialogue-dot-v2/neoul/560/anxious.webp | 288x430 | 8 KB | neoul |
| assets/dialogue-dot-v2/neoul/560/flustered.webp | 288x430 | 9 KB | neoul |
| assets/dialogue-dot-v2/neoul/560/joy.webp | 288x430 | 9 KB | neoul |
| assets/dialogue-dot-v2/neoul/560/neutral.webp | 288x430 | 10 KB | neoul |
| assets/dialogue-dot-v2/neoul/560/surprise_talk.webp | 288x430 | 10 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/angry.webp | 432x645 | 10 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/anxious.webp | 432x645 | 9 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/flustered.webp | 432x645 | 10 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/joy.webp | 432x645 | 10 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/neutral.webp | 432x645 | 11 KB | neoul |
| assets/dialogue-dot-v2/neoul/760/surprise_talk.webp | 432x645 | 11 KB | neoul |
| assets/dialogue-dot-v2/npc_pandol/560/angry.webp | 266x400 | 9 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/560/anxious.webp | 266x400 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/560/flustered.webp | 266x400 | 9 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/560/joy.webp | 266x400 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/560/neutral.webp | 266x400 | 9 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/560/surprise_talk.webp | 266x400 | 9 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/angry.webp | 399x600 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/anxious.webp | 399x600 | 11 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/flustered.webp | 399x600 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/joy.webp | 399x600 | 11 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/neutral.webp | 399x600 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_pandol/760/surprise_talk.webp | 399x600 | 10 KB | npc_pandol |
| assets/dialogue-dot-v2/npc_panseol/560/anxious.webp | 294x442 | 9 KB | npc_panseol |
| assets/dialogue-dot-v2/npc_panseol/560/neutral.webp | 294x442 | 10 KB | npc_panseol |
| assets/dialogue-dot-v2/npc_panseol/560/tired.webp | 294x442 | 9 KB | npc_panseol |
| assets/dialogue-dot-v2/npc_panseol/760/anxious.webp | 441x663 | 10 KB | npc_panseol |
| assets/dialogue-dot-v2/npc_panseol/760/neutral.webp | 441x663 | 11 KB | npc_panseol |
| assets/dialogue-dot-v2/npc_panseol/760/tired.webp | 441x663 | 10 KB | npc_panseol |
| assets/dialogue-dot-v2/resident_badook/560/angry.webp | 294x442 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/560/anxious.webp | 294x442 | 8 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/560/flustered.webp | 294x442 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/560/joy.webp | 294x442 | 8 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/560/neutral.webp | 294x442 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/560/surprise_talk.webp | 294x442 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/angry.webp | 441x663 | 10 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/anxious.webp | 441x663 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/flustered.webp | 441x663 | 10 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/joy.webp | 441x663 | 9 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/neutral.webp | 441x663 | 10 KB | resident_badook |
| assets/dialogue-dot-v2/resident_badook/760/surprise_talk.webp | 441x663 | 10 KB | resident_badook |
| assets/dialogue-dot-v2/resident_bori/560/angry.webp | 334x502 | 9 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/560/anxious.webp | 334x502 | 9 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/560/flustered.webp | 334x502 | 9 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/560/joy.webp | 334x502 | 10 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/560/neutral.webp | 334x502 | 10 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/560/surprise_talk.webp | 334x502 | 10 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/angry.webp | 501x753 | 10 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/anxious.webp | 501x753 | 10 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/flustered.webp | 501x753 | 11 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/joy.webp | 501x753 | 11 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/neutral.webp | 501x753 | 11 KB | resident_bori |
| assets/dialogue-dot-v2/resident_bori/760/surprise_talk.webp | 501x753 | 11 KB | resident_bori |
| assets/dialogue-dot-v2/resident_eunho/560/angry.webp | 296x444 | 7 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/560/anxious.webp | 296x444 | 7 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/560/flustered.webp | 296x444 | 7 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/560/joy.webp | 296x444 | 7 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/560/neutral.webp | 296x444 | 9 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/560/surprise_talk.webp | 296x444 | 7 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/angry.webp | 444x666 | 8 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/anxious.webp | 444x666 | 8 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/flustered.webp | 444x666 | 8 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/joy.webp | 444x666 | 8 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/neutral.webp | 444x666 | 10 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_eunho/760/surprise_talk.webp | 444x666 | 8 KB | resident_eunho |
| assets/dialogue-dot-v2/resident_guldol/560/angry.webp | 332x498 | 10 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/560/anxious.webp | 332x498 | 9 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/560/flustered.webp | 332x498 | 9 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/560/joy.webp | 332x498 | 10 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/560/neutral.webp | 332x498 | 9 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/560/surprise_talk.webp | 332x498 | 10 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/angry.webp | 498x747 | 11 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/anxious.webp | 498x747 | 10 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/flustered.webp | 498x747 | 11 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/joy.webp | 498x747 | 11 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/neutral.webp | 498x747 | 10 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_guldol/760/surprise_talk.webp | 498x747 | 11 KB | resident_guldol |
| assets/dialogue-dot-v2/resident_kongi/560/angry.webp | 230x346 | 5 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/560/anxious.webp | 230x346 | 5 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/560/flustered.webp | 230x346 | 5 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/560/joy.webp | 230x346 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/560/neutral.webp | 230x346 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/560/surprise_talk.webp | 230x346 | 5 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/angry.webp | 345x519 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/anxious.webp | 345x519 | 5 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/flustered.webp | 345x519 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/joy.webp | 345x519 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/neutral.webp | 345x519 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_kongi/760/surprise_talk.webp | 345x519 | 6 KB | resident_kongi |
| assets/dialogue-dot-v2/resident_lamplighter/560/angry.webp | 294x440 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/560/anxious.webp | 294x440 | 7 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/560/flustered.webp | 294x440 | 7 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/560/joy.webp | 294x440 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/560/neutral.webp | 294x440 | 7 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/560/surprise_talk.webp | 294x440 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/angry.webp | 441x660 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/anxious.webp | 441x660 | 7 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/flustered.webp | 441x660 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/joy.webp | 441x660 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/neutral.webp | 441x660 | 8 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_lamplighter/760/surprise_talk.webp | 441x660 | 9 KB | resident_lamplighter |
| assets/dialogue-dot-v2/resident_madam/560/angry.webp | 286x428 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/560/anxious.webp | 286x428 | 7 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/560/flustered.webp | 286x428 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/560/joy.webp | 286x428 | 7 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/560/neutral.webp | 286x428 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/560/surprise_talk.webp | 286x428 | 7 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/angry.webp | 429x642 | 9 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/anxious.webp | 429x642 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/flustered.webp | 429x642 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/joy.webp | 429x642 | 7 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/neutral.webp | 429x642 | 9 KB | resident_madam |
| assets/dialogue-dot-v2/resident_madam/760/surprise_talk.webp | 429x642 | 8 KB | resident_madam |
| assets/dialogue-dot-v2/resident_momo/560/angry.webp | 284x426 | 8 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/560/anxious.webp | 284x426 | 8 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/560/flustered.webp | 284x426 | 8 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/560/joy.webp | 284x426 | 8 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/560/neutral.webp | 284x426 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/560/surprise_talk.webp | 284x426 | 8 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/angry.webp | 426x639 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/anxious.webp | 426x639 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/flustered.webp | 426x639 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/joy.webp | 426x639 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/neutral.webp | 426x639 | 10 KB | resident_momo |
| assets/dialogue-dot-v2/resident_momo/760/surprise_talk.webp | 426x639 | 9 KB | resident_momo |
| assets/dialogue-dot-v2/resident_musoe/560/angry.webp | 318x478 | 10 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/560/anxious.webp | 318x478 | 9 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/560/flustered.webp | 318x478 | 11 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/560/joy.webp | 318x478 | 11 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/560/neutral.webp | 318x478 | 11 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/560/surprise_talk.webp | 318x478 | 11 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/angry.webp | 477x717 | 12 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/anxious.webp | 477x717 | 10 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/flustered.webp | 477x717 | 12 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/joy.webp | 477x717 | 12 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/neutral.webp | 477x717 | 12 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_musoe/760/surprise_talk.webp | 477x717 | 12 KB | resident_musoe |
| assets/dialogue-dot-v2/resident_nero/560/angry.webp | 286x430 | 9 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/560/anxious.webp | 286x430 | 8 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/560/flustered.webp | 286x430 | 8 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/560/joy.webp | 286x430 | 9 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/560/neutral.webp | 286x430 | 8 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/560/surprise_talk.webp | 286x430 | 8 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/angry.webp | 429x645 | 11 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/anxious.webp | 429x645 | 8 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/flustered.webp | 429x645 | 9 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/joy.webp | 429x645 | 10 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/neutral.webp | 429x645 | 9 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nero/760/surprise_talk.webp | 429x645 | 9 KB | resident_nero |
| assets/dialogue-dot-v2/resident_nubi/560/angry.webp | 288x432 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/560/anxious.webp | 288x432 | 7 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/560/flustered.webp | 288x432 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/560/joy.webp | 288x432 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/560/neutral.webp | 288x432 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/560/surprise_talk.webp | 288x432 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/angry.webp | 432x648 | 9 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/anxious.webp | 432x648 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/flustered.webp | 432x648 | 8 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/joy.webp | 432x648 | 9 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/neutral.webp | 432x648 | 9 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_nubi/760/surprise_talk.webp | 432x648 | 9 KB | resident_nubi |
| assets/dialogue-dot-v2/resident_owlgp/560/angry.webp | 276x412 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/560/anxious.webp | 276x412 | 6 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/560/flustered.webp | 276x412 | 7 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/560/joy.webp | 276x412 | 7 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/560/neutral.webp | 276x412 | 7 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/560/surprise_talk.webp | 276x412 | 7 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/angry.webp | 414x618 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/anxious.webp | 414x618 | 7 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/flustered.webp | 414x618 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/joy.webp | 414x618 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/neutral.webp | 414x618 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_owlgp/760/surprise_talk.webp | 414x618 | 8 KB | resident_owlgp |
| assets/dialogue-dot-v2/resident_piko/560/angry.webp | 284x426 | 7 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/560/anxious.webp | 284x426 | 7 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/560/flustered.webp | 284x426 | 7 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/560/joy.webp | 284x426 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/560/neutral.webp | 284x426 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/560/surprise_talk.webp | 284x426 | 7 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/angry.webp | 426x639 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/anxious.webp | 426x639 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/flustered.webp | 426x639 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/joy.webp | 426x639 | 9 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/neutral.webp | 426x639 | 9 KB | resident_piko |
| assets/dialogue-dot-v2/resident_piko/760/surprise_talk.webp | 426x639 | 8 KB | resident_piko |
| assets/dialogue-dot-v2/resident_ppul/560/angry.webp | 294x442 | 9 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/560/anxious.webp | 294x442 | 7 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/560/flustered.webp | 294x442 | 8 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/560/joy.webp | 294x442 | 9 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/560/neutral.webp | 294x442 | 7 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/560/surprise_talk.webp | 294x442 | 8 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/angry.webp | 441x663 | 10 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/anxious.webp | 441x663 | 8 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/flustered.webp | 441x663 | 9 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/joy.webp | 441x663 | 10 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/neutral.webp | 441x663 | 8 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_ppul/760/surprise_talk.webp | 441x663 | 9 KB | resident_ppul |
| assets/dialogue-dot-v2/resident_seori/560/angry.webp | 298x448 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/560/anxious.webp | 298x448 | 8 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/560/flustered.webp | 298x448 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/560/joy.webp | 298x448 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/560/neutral.webp | 298x448 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/560/surprise_talk.webp | 298x448 | 8 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/angry.webp | 447x672 | 11 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/anxious.webp | 447x672 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/flustered.webp | 447x672 | 10 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/joy.webp | 447x672 | 10 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/neutral.webp | 447x672 | 10 KB | resident_seori |
| assets/dialogue-dot-v2/resident_seori/760/surprise_talk.webp | 447x672 | 9 KB | resident_seori |
| assets/dialogue-dot-v2/resident_siluk/560/angry.webp | 288x430 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/560/anxious.webp | 288x430 | 7 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/560/flustered.webp | 288x430 | 7 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/560/joy.webp | 288x430 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/560/neutral.webp | 288x430 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/560/surprise_talk.webp | 288x430 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/angry.webp | 432x645 | 9 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/anxious.webp | 432x645 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/flustered.webp | 432x645 | 8 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/joy.webp | 432x645 | 9 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/neutral.webp | 432x645 | 9 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_siluk/760/surprise_talk.webp | 432x645 | 9 KB | resident_siluk |
| assets/dialogue-dot-v2/resident_sling/560/angry.webp | 294x442 | 8 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/560/anxious.webp | 294x442 | 7 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/560/flustered.webp | 294x442 | 8 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/560/joy.webp | 294x442 | 9 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/560/neutral.webp | 294x442 | 9 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/560/surprise_talk.webp | 294x442 | 8 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/angry.webp | 441x663 | 9 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/anxious.webp | 441x663 | 8 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/flustered.webp | 441x663 | 9 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/joy.webp | 441x663 | 10 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/neutral.webp | 441x663 | 10 KB | resident_sling |
| assets/dialogue-dot-v2/resident_sling/760/surprise_talk.webp | 441x663 | 9 KB | resident_sling |
| assets/dialogue-dot-v2/resident_somi/560/angry.webp | 230x344 | 5 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/560/anxious.webp | 230x344 | 5 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/560/flustered.webp | 230x344 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/560/joy.webp | 230x344 | 5 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/560/neutral.webp | 230x344 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/560/surprise_talk.webp | 230x344 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/angry.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/anxious.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/flustered.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/joy.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/neutral.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_somi/760/surprise_talk.webp | 345x516 | 6 KB | resident_somi |
| assets/dialogue-dot-v2/resident_teacher/560/angry.webp | 312x468 | 10 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/560/anxious.webp | 312x468 | 8 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/560/flustered.webp | 312x468 | 10 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/560/joy.webp | 312x468 | 9 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/560/neutral.webp | 312x468 | 11 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/560/surprise_talk.webp | 312x468 | 10 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/angry.webp | 468x702 | 11 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/anxious.webp | 468x702 | 9 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/flustered.webp | 468x702 | 11 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/joy.webp | 468x702 | 10 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/neutral.webp | 468x702 | 12 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_teacher/760/surprise_talk.webp | 468x702 | 11 KB | resident_teacher |
| assets/dialogue-dot-v2/resident_tok/560/angry.webp | 292x438 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/560/anxious.webp | 292x438 | 7 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/560/flustered.webp | 292x438 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/560/joy.webp | 292x438 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/560/neutral.webp | 292x438 | 7 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/560/surprise_talk.webp | 292x438 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/angry.webp | 438x657 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/anxious.webp | 438x657 | 7 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/flustered.webp | 438x657 | 9 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/joy.webp | 438x657 | 9 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/neutral.webp | 438x657 | 8 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tok/760/surprise_talk.webp | 438x657 | 9 KB | resident_tok |
| assets/dialogue-dot-v2/resident_tosil/560/angry.webp | 226x340 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/560/anxious.webp | 226x340 | 4 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/560/flustered.webp | 226x340 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/560/joy.webp | 226x340 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/560/neutral.webp | 226x340 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/560/surprise_talk.webp | 226x340 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/angry.webp | 339x510 | 6 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/anxious.webp | 339x510 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/flustered.webp | 339x510 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/joy.webp | 339x510 | 6 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/neutral.webp | 339x510 | 5 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_tosil/760/surprise_talk.webp | 339x510 | 6 KB | resident_tosil |
| assets/dialogue-dot-v2/resident_ttadak/560/angry.webp | 284x426 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/560/anxious.webp | 284x426 | 7 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/560/flustered.webp | 284x426 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/560/joy.webp | 284x426 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/560/neutral.webp | 284x426 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/560/surprise_talk.webp | 284x426 | 7 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/angry.webp | 426x639 | 9 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/anxious.webp | 426x639 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/flustered.webp | 426x639 | 9 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/joy.webp | 426x639 | 9 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/neutral.webp | 426x639 | 9 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ttadak/760/surprise_talk.webp | 426x639 | 8 KB | resident_ttadak |
| assets/dialogue-dot-v2/resident_ubak/560/angry.webp | 292x438 | 9 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/560/anxious.webp | 292x438 | 7 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/560/flustered.webp | 292x438 | 9 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/560/joy.webp | 292x438 | 9 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/560/neutral.webp | 292x438 | 9 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/560/surprise_talk.webp | 292x438 | 9 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/angry.webp | 438x657 | 10 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/anxious.webp | 438x657 | 8 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/flustered.webp | 438x657 | 10 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/joy.webp | 438x657 | 11 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/neutral.webp | 438x657 | 10 KB | resident_ubak |
| assets/dialogue-dot-v2/resident_ubak/760/surprise_talk.webp | 438x657 | 10 KB | resident_ubak |
| assets/dialogue-dot-v2/seryeon/560/angry.webp | 290x436 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/560/anxious.webp | 290x436 | 6 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/560/flustered.webp | 290x436 | 6 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/560/joy.webp | 290x436 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/560/neutral.webp | 290x436 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/560/surprise_talk.webp | 290x436 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/angry.webp | 435x654 | 8 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/anxious.webp | 435x654 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/flustered.webp | 435x654 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/joy.webp | 435x654 | 7 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/neutral.webp | 435x654 | 8 KB | seryeon |
| assets/dialogue-dot-v2/seryeon/760/surprise_talk.webp | 435x654 | 8 KB | seryeon |
| assets/dialogue-dot-v2/v111_child/560/angry.webp | 234x352 | 4 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/560/anxious.webp | 234x352 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/560/flustered.webp | 234x352 | 4 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/560/joy.webp | 234x352 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/560/neutral.webp | 234x352 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/560/surprise_talk.webp | 234x352 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/angry.webp | 351x528 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/anxious.webp | 351x528 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/flustered.webp | 351x528 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/joy.webp | 351x528 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/neutral.webp | 351x528 | 6 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_child/760/surprise_talk.webp | 351x528 | 5 KB | kid_nubi3; v111_child; v111_siluk_child |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/angry.webp | 272x408 | 7 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/anxious.webp | 272x408 | 7 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/flustered.webp | 272x408 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/joy.webp | 272x408 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/neutral.webp | 272x408 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/560/surprise_talk.webp | 272x408 | 7 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/angry.webp | 408x612 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/anxious.webp | 408x612 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/flustered.webp | 408x612 | 9 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/joy.webp | 408x612 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/neutral.webp | 408x612 | 9 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_lowerroad_elder/760/surprise_talk.webp | 408x612 | 8 KB | v111_lowerroad_elder |
| assets/dialogue-dot-v2/v111_patrol/560/angry.webp | 298x448 | 7 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/560/anxious.webp | 298x448 | 6 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/560/flustered.webp | 298x448 | 7 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/560/joy.webp | 298x448 | 7 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/560/neutral.webp | 298x448 | 8 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/560/surprise_talk.webp | 298x448 | 7 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/angry.webp | 447x672 | 8 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/anxious.webp | 447x672 | 7 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/flustered.webp | 447x672 | 8 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/joy.webp | 447x672 | 8 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/neutral.webp | 447x672 | 9 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_patrol/760/surprise_talk.webp | 447x672 | 8 KB | v111_patrol |
| assets/dialogue-dot-v2/v111_resident/560/angry.webp | 292x438 | 7 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/560/anxious.webp | 292x438 | 7 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/560/flustered.webp | 292x438 | 7 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/560/joy.webp | 292x438 | 7 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/560/neutral.webp | 292x438 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/560/surprise_talk.webp | 292x438 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/angry.webp | 438x657 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/anxious.webp | 438x657 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/flustered.webp | 438x657 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/joy.webp | 438x657 | 8 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/neutral.webp | 438x657 | 9 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-dot-v2/v111_resident/760/surprise_talk.webp | 438x657 | 9 KB | ms14_attendant; ms14_clinician; v111_lower_resident; v111_resident |
| assets/dialogue-pose-source/granny/withdraw_hand/560.webp | 235x440 | 89 KB | granny |
| assets/dialogue-pose-source/granny/withdraw_hand/760.webp | 319x597 | 151 KB | granny |
| assets/dialogue-pose-source/granny/withdraw_hand/840.webp | 353x660 | 178 KB | granny |
| assets/dialogue-pose-source/kid_bang/cling_leg/560.webp | 244x380 | 89 KB | kid_bang |
| assets/dialogue-pose-source/kid_bang/cling_leg/760.webp | 332x516 | 148 KB | kid_bang |
| assets/dialogue-pose-source/kid_bang/cling_leg/840.webp | 366x570 | 174 KB | kid_bang |
| assets/dialogue-pose-source/kid_dodam/lick_ladle/560.webp | 188x380 | 85 KB | kid_dodam |
| assets/dialogue-pose-source/kid_dodam/lick_ladle/760.webp | 255x516 | 139 KB | kid_dodam |
| assets/dialogue-pose-source/kid_dodam/lick_ladle/840.webp | 282x570 | 164 KB | kid_dodam |
| assets/dialogue-pose-source/kid_kkomi/door_peek/560.webp | 247x380 | 80 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_kkomi/door_peek/760.webp | 335x516 | 138 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_kkomi/door_peek/840.webp | 370x570 | 162 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_kkomi/hideout_proud/560.webp | 249x380 | 86 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_kkomi/hideout_proud/760.webp | 337x516 | 148 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_kkomi/hideout_proud/840.webp | 373x570 | 173 KB | kid_kkomi |
| assets/dialogue-pose-source/kid_saemi/hide_bowl/560.webp | 200x273 | 61 KB | kid_saemi |
| assets/dialogue-pose-source/kid_saemi/hide_bowl/760.webp | 271x371 | 101 KB | kid_saemi |
| assets/dialogue-pose-source/kid_saemi/hide_bowl/840.webp | 299x410 | 117 KB | kid_saemi |
| assets/dialogue-pose-source/mom/show_fragments/560.webp | 279x433 | 103 KB | mom |
| assets/dialogue-pose-source/mom/show_fragments/760.webp | 379x588 | 177 KB | mom |
| assets/dialogue-pose-source/mom/show_fragments/840.webp | 419x650 | 208 KB | mom |
| assets/dialogue-pose-source/npc_pandol/point_name/560.webp | 284x440 | 111 KB | npc_pandol |
| assets/dialogue-pose-source/npc_pandol/point_name/760.webp | 385x597 | 188 KB | npc_pandol |
| assets/dialogue-pose-source/npc_pandol/point_name/840.webp | 426x660 | 222 KB | npc_pandol |
| assets/dialogue-pose-source/resident_badook/block_cart/560.webp | 305x440 | 109 KB | resident_badook |
| assets/dialogue-pose-source/resident_badook/block_cart/760.webp | 390x563 | 168 KB | resident_badook |
| assets/dialogue-pose-source/resident_badook/block_cart/840.webp | 457x660 | 218 KB | resident_badook |
| assets/dialogue-pose-source/resident_teacher/collapse_attendance/560.webp | 258x320 | 87 KB | resident_teacher |
| assets/dialogue-pose-source/resident_teacher/collapse_attendance/760.webp | 350x434 | 144 KB | resident_teacher |
| assets/dialogue-pose-source/resident_teacher/collapse_attendance/840.webp | 387x480 | 173 KB | resident_teacher |
| assets/dialogue-pose-source/resident_teacher/write_attendance/560.webp | 314x440 | 125 KB | resident_teacher |
| assets/dialogue-pose-source/resident_teacher/write_attendance/760.webp | 390x546 | 182 KB | resident_teacher |
| assets/dialogue-pose-source/resident_teacher/write_attendance/840.webp | 471x660 | 247 KB | resident_teacher |
| assets/dialogue-pose-source/resident_tosil/hold_storybook/560.webp | 203x407 | 66 KB | resident_tosil |
| assets/dialogue-pose-source/resident_tosil/hold_storybook/760.webp | 275x552 | 108 KB | resident_tosil |
| assets/dialogue-pose-source/resident_tosil/hold_storybook/840.webp | 304x610 | 132 KB | resident_tosil |
| assets/dialogue-pose-source/seryeon/chair_listen/560.webp | 246x413 | 88 KB | seryeon |
| assets/dialogue-pose-source/seryeon/chair_listen/760.webp | 334x561 | 149 KB | seryeon |
| assets/dialogue-pose-source/seryeon/chair_listen/840.webp | 369x620 | 175 KB | seryeon |
| assets/dialogue-pose-source/seryeon/chair_read/560.webp | 245x413 | 88 KB | seryeon |
| assets/dialogue-pose-source/seryeon/chair_read/760.webp | 333x561 | 149 KB | seryeon |
| assets/dialogue-pose-source/seryeon/chair_read/840.webp | 368x620 | 175 KB | seryeon |
| assets/dialogue-source-master-v2/bami/560/angry.webp | 367x551 | 44 KB | bami |
| assets/dialogue-source-master-v2/bami/560/anxious.webp | 367x551 | 40 KB | bami |
| assets/dialogue-source-master-v2/bami/560/flustered.webp | 367x551 | 41 KB | bami |
| assets/dialogue-source-master-v2/bami/560/joy.webp | 367x551 | 41 KB | bami |
| assets/dialogue-source-master-v2/bami/560/neutral.webp | 367x551 | 39 KB | bami |
| assets/dialogue-source-master-v2/bami/560/surprise_talk.webp | 367x551 | 41 KB | bami |
| assets/dialogue-source-master-v2/bami/760/angry.webp | 427x641 | 52 KB | bami |
| assets/dialogue-source-master-v2/bami/760/anxious.webp | 427x641 | 50 KB | bami |
| assets/dialogue-source-master-v2/bami/760/flustered.webp | 427x641 | 51 KB | bami |
| assets/dialogue-source-master-v2/bami/760/joy.webp | 427x641 | 49 KB | bami |
| assets/dialogue-source-master-v2/bami/760/neutral.webp | 427x641 | 47 KB | bami |
| assets/dialogue-source-master-v2/bami/760/surprise_talk.webp | 427x641 | 52 KB | bami |
| assets/dialogue-source-master-v2/bami/840/angry.webp | 551x826 | 71 KB | bami |
| assets/dialogue-source-master-v2/bami/840/anxious.webp | 551x826 | 68 KB | bami |
| assets/dialogue-source-master-v2/bami/840/flustered.webp | 551x826 | 69 KB | bami |
| assets/dialogue-source-master-v2/bami/840/joy.webp | 551x826 | 65 KB | bami |
| assets/dialogue-source-master-v2/bami/840/neutral.webp | 551x826 | 63 KB | bami |
| assets/dialogue-source-master-v2/bami/840/surprise_talk.webp | 551x826 | 72 KB | bami |
| assets/dialogue-source-master-v2/buri/560/angry.webp | 430x644 | 46 KB | buri |
| assets/dialogue-source-master-v2/buri/560/anxious.webp | 430x644 | 49 KB | buri |
| assets/dialogue-source-master-v2/buri/560/flustered.webp | 430x644 | 48 KB | buri |
| assets/dialogue-source-master-v2/buri/560/joy.webp | 430x644 | 47 KB | buri |
| assets/dialogue-source-master-v2/buri/560/neutral.webp | 430x644 | 45 KB | buri |
| assets/dialogue-source-master-v2/buri/560/surprise_talk.webp | 430x644 | 46 KB | buri |
| assets/dialogue-source-master-v2/buri/760/angry.webp | 465x698 | 51 KB | buri |
| assets/dialogue-source-master-v2/buri/760/anxious.webp | 465x698 | 55 KB | buri |
| assets/dialogue-source-master-v2/buri/760/flustered.webp | 465x698 | 54 KB | buri |
| assets/dialogue-source-master-v2/buri/760/joy.webp | 465x698 | 52 KB | buri |
| assets/dialogue-source-master-v2/buri/760/neutral.webp | 465x698 | 50 KB | buri |
| assets/dialogue-source-master-v2/buri/760/surprise_talk.webp | 465x698 | 53 KB | buri |
| assets/dialogue-source-master-v2/buri/840/angry.webp | 644x967 | 79 KB | buri |
| assets/dialogue-source-master-v2/buri/840/anxious.webp | 644x967 | 86 KB | buri |
| assets/dialogue-source-master-v2/buri/840/flustered.webp | 644x967 | 83 KB | buri |
| assets/dialogue-source-master-v2/buri/840/joy.webp | 644x967 | 81 KB | buri |
| assets/dialogue-source-master-v2/buri/840/neutral.webp | 644x967 | 79 KB | buri |
| assets/dialogue-source-master-v2/buri/840/surprise_talk.webp | 644x967 | 83 KB | buri |
| assets/dialogue-source-master-v2/daram/560/angry.webp | 330x496 | 38 KB | daram |
| assets/dialogue-source-master-v2/daram/560/anxious.webp | 330x496 | 36 KB | daram |
| assets/dialogue-source-master-v2/daram/560/flustered.webp | 330x496 | 35 KB | daram |
| assets/dialogue-source-master-v2/daram/560/joy.webp | 330x496 | 38 KB | daram |
| assets/dialogue-source-master-v2/daram/560/neutral.webp | 330x496 | 37 KB | daram |
| assets/dialogue-source-master-v2/daram/560/surprise_talk.webp | 330x496 | 42 KB | daram |
| assets/dialogue-source-master-v2/daram/760/angry.webp | 450x675 | 58 KB | daram |
| assets/dialogue-source-master-v2/daram/760/anxious.webp | 450x675 | 55 KB | daram |
| assets/dialogue-source-master-v2/daram/760/flustered.webp | 450x675 | 52 KB | daram |
| assets/dialogue-source-master-v2/daram/760/joy.webp | 450x675 | 58 KB | daram |
| assets/dialogue-source-master-v2/daram/760/neutral.webp | 450x675 | 55 KB | daram |
| assets/dialogue-source-master-v2/daram/760/surprise_talk.webp | 450x675 | 60 KB | daram |
| assets/dialogue-source-master-v2/daram/840/angry.webp | 496x745 | 65 KB | daram |
| assets/dialogue-source-master-v2/daram/840/anxious.webp | 496x745 | 62 KB | daram |
| assets/dialogue-source-master-v2/daram/840/flustered.webp | 496x745 | 60 KB | daram |
| assets/dialogue-source-master-v2/daram/840/joy.webp | 496x745 | 66 KB | daram |
| assets/dialogue-source-master-v2/daram/840/neutral.webp | 496x745 | 63 KB | daram |
| assets/dialogue-source-master-v2/daram/840/surprise_talk.webp | 496x745 | 68 KB | daram |
| assets/dialogue-source-master-v2/doto/560/angry.webp | 365x548 | 33 KB | doto |
| assets/dialogue-source-master-v2/doto/560/anxious.webp | 365x548 | 34 KB | doto |
| assets/dialogue-source-master-v2/doto/560/flustered.webp | 365x548 | 36 KB | doto |
| assets/dialogue-source-master-v2/doto/560/joy.webp | 365x548 | 34 KB | doto |
| assets/dialogue-source-master-v2/doto/560/neutral.webp | 365x549 | 33 KB | doto |
| assets/dialogue-source-master-v2/doto/560/surprise_talk.webp | 365x548 | 35 KB | doto |
| assets/dialogue-source-master-v2/doto/760/angry.webp | 407x611 | 38 KB | doto |
| assets/dialogue-source-master-v2/doto/760/anxious.webp | 407x611 | 39 KB | doto |
| assets/dialogue-source-master-v2/doto/760/flustered.webp | 407x611 | 41 KB | doto |
| assets/dialogue-source-master-v2/doto/760/joy.webp | 407x611 | 38 KB | doto |
| assets/dialogue-source-master-v2/doto/760/neutral.webp | 407x612 | 38 KB | doto |
| assets/dialogue-source-master-v2/doto/760/surprise_talk.webp | 407x611 | 40 KB | doto |
| assets/dialogue-source-master-v2/doto/840/angry.webp | 549x824 | 53 KB | doto |
| assets/dialogue-source-master-v2/doto/840/anxious.webp | 549x824 | 56 KB | doto |
| assets/dialogue-source-master-v2/doto/840/flustered.webp | 549x824 | 58 KB | doto |
| assets/dialogue-source-master-v2/doto/840/joy.webp | 549x824 | 52 KB | doto |
| assets/dialogue-source-master-v2/doto/840/neutral.webp | 549x825 | 53 KB | doto |
| assets/dialogue-source-master-v2/doto/840/surprise_talk.webp | 549x824 | 57 KB | doto |
| assets/dialogue-source-master-v2/granny/560/angry.webp | 393x590 | 40 KB | granny |
| assets/dialogue-source-master-v2/granny/560/anxious.webp | 393x590 | 39 KB | granny |
| assets/dialogue-source-master-v2/granny/560/flustered.webp | 393x590 | 39 KB | granny |
| assets/dialogue-source-master-v2/granny/560/joy.webp | 393x590 | 39 KB | granny |
| assets/dialogue-source-master-v2/granny/560/neutral.webp | 393x589 | 40 KB | granny |
| assets/dialogue-source-master-v2/granny/560/surprise_talk.webp | 393x589 | 40 KB | granny |
| assets/dialogue-source-master-v2/granny/760/angry.webp | 426x639 | 44 KB | granny |
| assets/dialogue-source-master-v2/granny/760/anxious.webp | 426x639 | 44 KB | granny |
| assets/dialogue-source-master-v2/granny/760/flustered.webp | 426x639 | 43 KB | granny |
| assets/dialogue-source-master-v2/granny/760/joy.webp | 426x639 | 43 KB | granny |
| assets/dialogue-source-master-v2/granny/760/neutral.webp | 426x639 | 43 KB | granny |
| assets/dialogue-source-master-v2/granny/760/surprise_talk.webp | 426x639 | 44 KB | granny |
| assets/dialogue-source-master-v2/granny/840/angry.webp | 590x885 | 70 KB | granny |
| assets/dialogue-source-master-v2/granny/840/anxious.webp | 590x885 | 69 KB | granny |
| assets/dialogue-source-master-v2/granny/840/flustered.webp | 590x885 | 69 KB | granny |
| assets/dialogue-source-master-v2/granny/840/joy.webp | 590x885 | 68 KB | granny |
| assets/dialogue-source-master-v2/granny/840/neutral.webp | 590x884 | 70 KB | granny |
| assets/dialogue-source-master-v2/granny/840/surprise_talk.webp | 590x884 | 71 KB | granny |
| assets/dialogue-source-master-v2/guard/560/angry.webp | 405x607 | 47 KB | guard |
| assets/dialogue-source-master-v2/guard/560/anxious.webp | 404x607 | 50 KB | guard |
| assets/dialogue-source-master-v2/guard/560/flustered.webp | 405x607 | 47 KB | guard |
| assets/dialogue-source-master-v2/guard/560/joy.webp | 405x607 | 48 KB | guard |
| assets/dialogue-source-master-v2/guard/560/neutral.webp | 404x607 | 50 KB | guard |
| assets/dialogue-source-master-v2/guard/560/surprise_talk.webp | 404x607 | 47 KB | guard |
| assets/dialogue-source-master-v2/guard/760/angry.webp | 452x678 | 54 KB | guard |
| assets/dialogue-source-master-v2/guard/760/anxious.webp | 452x678 | 57 KB | guard |
| assets/dialogue-source-master-v2/guard/760/flustered.webp | 452x678 | 55 KB | guard |
| assets/dialogue-source-master-v2/guard/760/joy.webp | 452x678 | 57 KB | guard |
| assets/dialogue-source-master-v2/guard/760/neutral.webp | 452x678 | 56 KB | guard |
| assets/dialogue-source-master-v2/guard/760/surprise_talk.webp | 452x678 | 55 KB | guard |
| assets/dialogue-source-master-v2/guard/840/angry.webp | 605x908 | 82 KB | guard |
| assets/dialogue-source-master-v2/guard/840/anxious.webp | 605x909 | 83 KB | guard |
| assets/dialogue-source-master-v2/guard/840/flustered.webp | 605x908 | 81 KB | guard |
| assets/dialogue-source-master-v2/guard/840/joy.webp | 605x908 | 83 KB | guard |
| assets/dialogue-source-master-v2/guard/840/neutral.webp | 605x909 | 83 KB | guard |
| assets/dialogue-source-master-v2/guard/840/surprise_talk.webp | 605x909 | 82 KB | guard |
| assets/dialogue-source-master-v2/karo/560/angry.webp | 412x620 | 57 KB | karo |
| assets/dialogue-source-master-v2/karo/560/anxious.webp | 413x619 | 54 KB | karo |
| assets/dialogue-source-master-v2/karo/560/flustered.webp | 412x620 | 61 KB | karo |
| assets/dialogue-source-master-v2/karo/560/joy.webp | 413x619 | 57 KB | karo |
| assets/dialogue-source-master-v2/karo/560/neutral.webp | 413x619 | 55 KB | karo |
| assets/dialogue-source-master-v2/karo/560/surprise_talk.webp | 413x619 | 58 KB | karo |
| assets/dialogue-source-master-v2/karo/760/angry.webp | 445x669 | 65 KB | karo |
| assets/dialogue-source-master-v2/karo/760/anxious.webp | 446x669 | 60 KB | karo |
| assets/dialogue-source-master-v2/karo/760/flustered.webp | 445x669 | 69 KB | karo |
| assets/dialogue-source-master-v2/karo/760/joy.webp | 446x669 | 63 KB | karo |
| assets/dialogue-source-master-v2/karo/760/neutral.webp | 446x669 | 61 KB | karo |
| assets/dialogue-source-master-v2/karo/760/surprise_talk.webp | 446x669 | 64 KB | karo |
| assets/dialogue-source-master-v2/karo/840/angry.webp | 617x928 | 102 KB | karo |
| assets/dialogue-source-master-v2/karo/840/anxious.webp | 618x927 | 96 KB | karo |
| assets/dialogue-source-master-v2/karo/840/flustered.webp | 617x928 | 109 KB | karo |
| assets/dialogue-source-master-v2/karo/840/joy.webp | 618x927 | 101 KB | karo |
| assets/dialogue-source-master-v2/karo/840/neutral.webp | 618x927 | 92 KB | karo |
| assets/dialogue-source-master-v2/karo/840/surprise_talk.webp | 618x927 | 102 KB | karo |
| assets/dialogue-source-master-v2/kid_dodam/560/angry.webp | 356x534 | 34 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/560/anxious.webp | 356x533 | 33 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/560/flustered.webp | 356x534 | 33 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/560/joy.webp | 355x534 | 38 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/560/neutral.webp | 355x534 | 34 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/560/surprise_talk.webp | 355x534 | 38 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/angry.webp | 427x641 | 45 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/anxious.webp | 428x641 | 42 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/flustered.webp | 427x641 | 42 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/joy.webp | 427x642 | 48 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/neutral.webp | 427x642 | 45 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/760/surprise_talk.webp | 427x642 | 49 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/angry.webp | 534x801 | 60 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/anxious.webp | 534x800 | 57 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/flustered.webp | 534x801 | 58 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/joy.webp | 533x801 | 65 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/neutral.webp | 533x801 | 59 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_dodam/840/surprise_talk.webp | 533x801 | 66 KB | kid_dodam |
| assets/dialogue-source-master-v2/kid_kkomi/560/angry.webp | 344x517 | 41 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/560/anxious.webp | 344x516 | 40 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/560/flustered.webp | 344x516 | 38 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/560/joy.webp | 345x516 | 39 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/560/neutral.webp | 344x516 | 40 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/560/surprise_talk.webp | 344x516 | 41 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/angry.webp | 412x621 | 51 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/anxious.webp | 413x620 | 51 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/flustered.webp | 413x620 | 50 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/joy.webp | 414x619 | 50 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/neutral.webp | 413x620 | 50 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/760/surprise_talk.webp | 413x620 | 53 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/angry.webp | 515x775 | 69 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/anxious.webp | 516x774 | 68 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/flustered.webp | 516x774 | 66 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/joy.webp | 516x773 | 68 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/neutral.webp | 516x774 | 69 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_kkomi/840/surprise_talk.webp | 516x774 | 70 KB | kid_kkomi |
| assets/dialogue-source-master-v2/kid_saemi/560/angry.webp | 349x525 | 39 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/560/anxious.webp | 350x525 | 39 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/560/flustered.webp | 349x525 | 40 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/560/joy.webp | 349x525 | 45 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/560/neutral.webp | 349x525 | 42 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/560/surprise_talk.webp | 350x525 | 44 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/angry.webp | 420x630 | 49 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/anxious.webp | 420x630 | 49 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/flustered.webp | 420x630 | 51 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/joy.webp | 420x631 | 58 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/neutral.webp | 420x630 | 54 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/760/surprise_talk.webp | 420x630 | 54 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/angry.webp | 524x788 | 66 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/anxious.webp | 525x787 | 66 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/flustered.webp | 524x788 | 69 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/joy.webp | 524x788 | 76 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/neutral.webp | 524x788 | 71 KB | kid_saemi |
| assets/dialogue-source-master-v2/kid_saemi/840/surprise_talk.webp | 525x787 | 74 KB | kid_saemi |
| assets/dialogue-source-master-v2/mom/560/angry.webp | 435x634 | 52 KB | mom |
| assets/dialogue-source-master-v2/mom/560/anxious.webp | 429x643 | 52 KB | mom |
| assets/dialogue-source-master-v2/mom/560/flustered.webp | 428x644 | 54 KB | mom |
| assets/dialogue-source-master-v2/mom/560/joy.webp | 428x644 | 57 KB | mom |
| assets/dialogue-source-master-v2/mom/560/neutral.webp | 429x643 | 56 KB | mom |
| assets/dialogue-source-master-v2/mom/560/surprise_talk.webp | 429x643 | 54 KB | mom |
| assets/dialogue-source-master-v2/mom/760/angry.webp | 443x644 | 53 KB | mom |
| assets/dialogue-source-master-v2/mom/760/anxious.webp | 436x654 | 52 KB | mom |
| assets/dialogue-source-master-v2/mom/760/flustered.webp | 435x655 | 55 KB | mom |
| assets/dialogue-source-master-v2/mom/760/joy.webp | 436x655 | 59 KB | mom |
| assets/dialogue-source-master-v2/mom/760/neutral.webp | 436x654 | 58 KB | mom |
| assets/dialogue-source-master-v2/mom/760/surprise_talk.webp | 436x654 | 55 KB | mom |
| assets/dialogue-source-master-v2/mom/840/angry.webp | 652x949 | 88 KB | mom |
| assets/dialogue-source-master-v2/mom/840/anxious.webp | 642x964 | 88 KB | mom |
| assets/dialogue-source-master-v2/mom/840/flustered.webp | 641x965 | 93 KB | mom |
| assets/dialogue-source-master-v2/mom/840/joy.webp | 642x964 | 98 KB | mom |
| assets/dialogue-source-master-v2/mom/840/neutral.webp | 642x964 | 97 KB | mom |
| assets/dialogue-source-master-v2/mom/840/surprise_talk.webp | 642x964 | 94 KB | mom |
| assets/dialogue-source-master-v2/nabi/560/angry.webp | 386x588 | 52 KB | nabi |
| assets/dialogue-source-master-v2/nabi/560/anxious.webp | 389x583 | 44 KB | nabi |
| assets/dialogue-source-master-v2/nabi/560/flustered.webp | 389x583 | 46 KB | nabi |
| assets/dialogue-source-master-v2/nabi/560/joy.webp | 395x574 | 50 KB | nabi |
| assets/dialogue-source-master-v2/nabi/560/neutral.webp | 389x583 | 49 KB | nabi |
| assets/dialogue-source-master-v2/nabi/560/surprise_talk.webp | 389x583 | 47 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/angry.webp | 386x588 | 52 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/anxious.webp | 389x583 | 44 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/flustered.webp | 389x583 | 46 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/joy.webp | 395x574 | 50 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/neutral.webp | 389x583 | 49 KB | nabi |
| assets/dialogue-source-master-v2/nabi/760/surprise_talk.webp | 389x583 | 47 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/angry.webp | 584x890 | 90 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/anxious.webp | 588x883 | 76 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/flustered.webp | 588x883 | 79 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/joy.webp | 598x869 | 86 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/neutral.webp | 588x883 | 85 KB | nabi |
| assets/dialogue-source-master-v2/nabi/840/surprise_talk.webp | 588x883 | 81 KB | nabi |
| assets/dialogue-source-master-v2/neoul/560/angry.webp | 371x556 | 51 KB | neoul |
| assets/dialogue-source-master-v2/neoul/560/anxious.webp | 371x557 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/560/flustered.webp | 371x556 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/560/joy.webp | 371x556 | 52 KB | neoul |
| assets/dialogue-source-master-v2/neoul/560/neutral.webp | 371x556 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/560/surprise_talk.webp | 371x557 | 50 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/angry.webp | 371x556 | 51 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/anxious.webp | 371x557 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/flustered.webp | 371x556 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/joy.webp | 371x556 | 52 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/neutral.webp | 371x556 | 49 KB | neoul |
| assets/dialogue-source-master-v2/neoul/760/surprise_talk.webp | 371x557 | 50 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/angry.webp | 585x877 | 87 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/anxious.webp | 584x878 | 85 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/flustered.webp | 585x877 | 90 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/joy.webp | 585x877 | 89 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/neutral.webp | 585x877 | 85 KB | neoul |
| assets/dialogue-source-master-v2/neoul/840/surprise_talk.webp | 584x878 | 87 KB | neoul |
| assets/dialogue-source-master-v2/npc_pandol/560/angry.webp | 394x591 | 55 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/560/anxious.webp | 394x592 | 62 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/560/flustered.webp | 394x591 | 52 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/560/joy.webp | 394x592 | 56 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/560/neutral.webp | 394x592 | 56 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/560/surprise_talk.webp | 394x591 | 56 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/angry.webp | 402x604 | 57 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/anxious.webp | 402x604 | 63 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/flustered.webp | 402x604 | 52 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/joy.webp | 402x604 | 57 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/neutral.webp | 402x604 | 58 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/760/surprise_talk.webp | 402x604 | 57 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/angry.webp | 592x887 | 97 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/anxious.webp | 591x888 | 112 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/flustered.webp | 592x887 | 90 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/joy.webp | 591x888 | 98 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/neutral.webp | 591x888 | 97 KB | npc_pandol |
| assets/dialogue-source-master-v2/npc_pandol/840/surprise_talk.webp | 592x887 | 98 KB | npc_pandol |
| assets/dialogue-source-master-v2/resident_badook/560/angry.webp | 422x633 | 50 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/560/anxious.webp | 422x633 | 48 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/560/flustered.webp | 422x633 | 48 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/560/joy.webp | 422x633 | 48 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/560/neutral.webp | 422x633 | 47 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/560/surprise_talk.webp | 422x633 | 50 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/angry.webp | 427x640 | 50 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/anxious.webp | 427x640 | 49 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/flustered.webp | 427x640 | 49 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/joy.webp | 427x640 | 49 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/neutral.webp | 427x640 | 48 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/760/surprise_talk.webp | 427x640 | 50 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/angry.webp | 634x951 | 84 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/anxious.webp | 634x951 | 84 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/flustered.webp | 634x951 | 83 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/joy.webp | 634x951 | 84 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/neutral.webp | 634x951 | 82 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_badook/840/surprise_talk.webp | 634x951 | 87 KB | resident_badook |
| assets/dialogue-source-master-v2/resident_bori/560/angry.webp | 436x653 | 59 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/560/anxious.webp | 435x654 | 57 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/560/flustered.webp | 435x654 | 58 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/560/joy.webp | 435x654 | 60 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/560/neutral.webp | 436x653 | 53 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/560/surprise_talk.webp | 435x654 | 59 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/angry.webp | 436x653 | 59 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/anxious.webp | 435x654 | 57 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/flustered.webp | 435x654 | 58 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/joy.webp | 435x654 | 60 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/neutral.webp | 436x653 | 53 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/760/surprise_talk.webp | 435x654 | 59 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/angry.webp | 716x1074 | 115 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/anxious.webp | 715x1075 | 115 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/flustered.webp | 714x1075 | 114 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/joy.webp | 715x1075 | 119 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/neutral.webp | 716x1074 | 108 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_bori/840/surprise_talk.webp | 715x1074 | 119 KB | resident_bori |
| assets/dialogue-source-master-v2/resident_eunho/560/angry.webp | 442x664 | 57 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/560/anxious.webp | 442x664 | 57 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/560/flustered.webp | 442x664 | 58 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/560/joy.webp | 442x664 | 57 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/560/neutral.webp | 442x664 | 55 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/560/surprise_talk.webp | 442x664 | 59 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/angry.webp | 445x668 | 57 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/anxious.webp | 445x668 | 57 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/flustered.webp | 445x669 | 59 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/joy.webp | 445x668 | 58 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/neutral.webp | 445x669 | 56 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/760/surprise_talk.webp | 445x668 | 59 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/angry.webp | 658x987 | 95 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/anxious.webp | 658x987 | 95 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/flustered.webp | 657x988 | 97 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/joy.webp | 658x987 | 96 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/neutral.webp | 657x987 | 93 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_eunho/840/surprise_talk.webp | 658x987 | 99 KB | resident_eunho |
| assets/dialogue-source-master-v2/resident_guldol/560/angry.webp | 409x614 | 45 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/560/anxious.webp | 409x614 | 44 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/560/flustered.webp | 409x614 | 43 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/560/joy.webp | 409x614 | 45 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/560/neutral.webp | 409x614 | 45 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/560/surprise_talk.webp | 409x614 | 47 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/angry.webp | 417x627 | 47 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/anxious.webp | 417x626 | 44 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/flustered.webp | 417x626 | 45 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/joy.webp | 417x626 | 46 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/neutral.webp | 417x626 | 46 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/760/surprise_talk.webp | 417x626 | 49 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/angry.webp | 613x920 | 78 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/anxious.webp | 613x920 | 75 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/flustered.webp | 613x920 | 75 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/joy.webp | 613x920 | 78 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/neutral.webp | 613x920 | 76 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_guldol/840/surprise_talk.webp | 613x920 | 82 KB | resident_guldol |
| assets/dialogue-source-master-v2/resident_kongi/560/angry.webp | 405x608 | 48 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/560/anxious.webp | 405x609 | 50 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/560/flustered.webp | 405x608 | 48 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/560/joy.webp | 405x608 | 52 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/560/neutral.webp | 405x609 | 50 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/560/surprise_talk.webp | 405x609 | 53 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/angry.webp | 414x621 | 49 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/anxious.webp | 413x621 | 51 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/flustered.webp | 414x621 | 50 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/joy.webp | 414x621 | 54 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/neutral.webp | 413x621 | 51 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/760/surprise_talk.webp | 413x621 | 54 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/angry.webp | 608x912 | 83 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/anxious.webp | 608x913 | 87 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/flustered.webp | 608x912 | 84 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/joy.webp | 608x912 | 90 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/neutral.webp | 608x913 | 87 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_kongi/840/surprise_talk.webp | 608x913 | 92 KB | resident_kongi |
| assets/dialogue-source-master-v2/resident_lamplighter/560/angry.webp | 435x652 | 51 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/560/anxious.webp | 435x652 | 52 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/560/flustered.webp | 435x652 | 47 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/560/joy.webp | 435x652 | 51 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/560/neutral.webp | 435x652 | 46 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/560/surprise_talk.webp | 435x652 | 56 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/angry.webp | 452x678 | 53 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/anxious.webp | 452x678 | 54 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/flustered.webp | 452x678 | 50 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/joy.webp | 452x678 | 53 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/neutral.webp | 452x678 | 48 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/760/surprise_talk.webp | 452x678 | 59 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/angry.webp | 647x970 | 84 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/anxious.webp | 647x970 | 88 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/flustered.webp | 647x970 | 81 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/joy.webp | 647x970 | 86 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/neutral.webp | 647x970 | 77 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_lamplighter/840/surprise_talk.webp | 647x970 | 95 KB | resident_lamplighter |
| assets/dialogue-source-master-v2/resident_madam/560/angry.webp | 396x594 | 48 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/560/anxious.webp | 396x594 | 46 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/560/flustered.webp | 396x594 | 46 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/560/joy.webp | 395x594 | 49 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/560/neutral.webp | 396x594 | 47 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/560/surprise_talk.webp | 396x594 | 49 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/angry.webp | 439x659 | 56 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/anxious.webp | 439x659 | 52 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/flustered.webp | 439x659 | 55 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/joy.webp | 439x660 | 57 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/neutral.webp | 439x659 | 53 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/760/surprise_talk.webp | 439x659 | 57 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/angry.webp | 594x890 | 84 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/anxious.webp | 594x890 | 79 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/flustered.webp | 594x890 | 83 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/joy.webp | 593x892 | 85 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/neutral.webp | 594x890 | 79 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_madam/840/surprise_talk.webp | 594x890 | 85 KB | resident_madam |
| assets/dialogue-source-master-v2/resident_momo/560/angry.webp | 389x583 | 42 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/560/anxious.webp | 389x583 | 44 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/560/flustered.webp | 389x584 | 42 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/560/joy.webp | 389x583 | 47 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/560/neutral.webp | 389x584 | 47 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/560/surprise_talk.webp | 389x584 | 48 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/angry.webp | 397x596 | 44 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/anxious.webp | 397x596 | 45 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/flustered.webp | 397x596 | 43 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/joy.webp | 397x596 | 48 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/neutral.webp | 397x596 | 51 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/760/surprise_talk.webp | 397x596 | 50 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/angry.webp | 583x875 | 76 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/anxious.webp | 583x875 | 78 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/flustered.webp | 583x876 | 75 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/joy.webp | 583x875 | 83 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/neutral.webp | 583x876 | 84 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_momo/840/surprise_talk.webp | 583x876 | 87 KB | resident_momo |
| assets/dialogue-source-master-v2/resident_musoe/560/angry.webp | 399x598 | 46 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/560/anxious.webp | 399x598 | 46 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/560/flustered.webp | 398x599 | 51 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/560/joy.webp | 399x598 | 48 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/560/neutral.webp | 399x598 | 46 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/560/surprise_talk.webp | 398x598 | 50 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/angry.webp | 407x610 | 47 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/anxious.webp | 407x610 | 46 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/flustered.webp | 406x611 | 52 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/joy.webp | 407x610 | 49 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/neutral.webp | 407x610 | 47 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/760/surprise_talk.webp | 406x611 | 51 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/angry.webp | 599x898 | 80 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/anxious.webp | 599x898 | 79 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/flustered.webp | 598x899 | 88 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/joy.webp | 599x898 | 85 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/neutral.webp | 599x898 | 77 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_musoe/840/surprise_talk.webp | 598x898 | 88 KB | resident_musoe |
| assets/dialogue-source-master-v2/resident_nero/560/angry.webp | 383x574 | 41 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/560/anxious.webp | 383x574 | 41 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/560/flustered.webp | 382x575 | 39 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/560/joy.webp | 382x574 | 42 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/560/neutral.webp | 382x574 | 41 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/560/surprise_talk.webp | 383x574 | 41 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/angry.webp | 390x584 | 42 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/anxious.webp | 390x584 | 41 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/flustered.webp | 389x585 | 40 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/joy.webp | 389x585 | 43 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/neutral.webp | 389x585 | 42 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/760/surprise_talk.webp | 390x584 | 42 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/angry.webp | 574x861 | 70 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/anxious.webp | 574x861 | 70 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/flustered.webp | 574x862 | 68 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/joy.webp | 574x862 | 72 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/neutral.webp | 574x862 | 71 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nero/840/surprise_talk.webp | 574x861 | 70 KB | resident_nero |
| assets/dialogue-source-master-v2/resident_nubi/560/angry.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/560/anxious.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/560/flustered.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/560/joy.webp | 373x560 | 44 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/560/neutral.webp | 373x559 | 39 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/560/surprise_talk.webp | 373x559 | 43 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/angry.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/anxious.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/flustered.webp | 373x559 | 42 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/joy.webp | 373x560 | 44 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/neutral.webp | 373x559 | 39 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/760/surprise_talk.webp | 373x559 | 43 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/angry.webp | 584x875 | 71 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/anxious.webp | 584x875 | 72 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/flustered.webp | 584x875 | 71 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/joy.webp | 583x876 | 73 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/neutral.webp | 584x875 | 67 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_nubi/840/surprise_talk.webp | 584x875 | 75 KB | resident_nubi |
| assets/dialogue-source-master-v2/resident_owlgp/560/angry.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/560/anxious.webp | 408x612 | 41 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/560/flustered.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/560/joy.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/560/neutral.webp | 407x612 | 41 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/560/surprise_talk.webp | 407x612 | 43 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/angry.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/anxious.webp | 408x612 | 41 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/flustered.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/joy.webp | 407x612 | 42 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/neutral.webp | 407x612 | 41 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/760/surprise_talk.webp | 407x612 | 43 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/angry.webp | 618x929 | 71 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/anxious.webp | 619x928 | 70 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/flustered.webp | 618x929 | 73 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/joy.webp | 618x929 | 70 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/neutral.webp | 618x929 | 69 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_owlgp/840/surprise_talk.webp | 618x929 | 76 KB | resident_owlgp |
| assets/dialogue-source-master-v2/resident_piko/560/angry.webp | 399x598 | 45 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/560/anxious.webp | 399x598 | 44 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/560/flustered.webp | 398x599 | 43 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/560/joy.webp | 398x599 | 45 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/560/neutral.webp | 399x598 | 46 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/560/surprise_talk.webp | 399x598 | 47 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/angry.webp | 407x611 | 46 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/anxious.webp | 407x611 | 46 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/flustered.webp | 407x611 | 45 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/joy.webp | 407x611 | 46 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/neutral.webp | 407x611 | 47 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/760/surprise_talk.webp | 407x611 | 48 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/angry.webp | 600x900 | 75 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/anxious.webp | 600x900 | 75 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/flustered.webp | 599x900 | 72 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/joy.webp | 599x900 | 75 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/neutral.webp | 600x900 | 76 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_piko/840/surprise_talk.webp | 600x900 | 81 KB | resident_piko |
| assets/dialogue-source-master-v2/resident_ppul/560/angry.webp | 412x618 | 51 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/560/anxious.webp | 412x618 | 44 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/560/flustered.webp | 412x618 | 45 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/560/joy.webp | 412x618 | 54 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/560/neutral.webp | 412x618 | 51 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/560/surprise_talk.webp | 412x619 | 52 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/angry.webp | 415x623 | 51 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/anxious.webp | 415x623 | 45 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/flustered.webp | 415x623 | 47 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/joy.webp | 415x622 | 54 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/neutral.webp | 415x622 | 52 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/760/surprise_talk.webp | 415x623 | 52 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/angry.webp | 618x927 | 91 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/anxious.webp | 618x927 | 79 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/flustered.webp | 618x927 | 80 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/joy.webp | 618x927 | 93 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/neutral.webp | 618x927 | 89 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_ppul/840/surprise_talk.webp | 618x928 | 91 KB | resident_ppul |
| assets/dialogue-source-master-v2/resident_seori/560/angry.webp | 419x628 | 43 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/560/anxious.webp | 418x628 | 41 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/560/flustered.webp | 419x628 | 41 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/560/joy.webp | 418x628 | 45 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/560/neutral.webp | 419x628 | 41 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/560/surprise_talk.webp | 418x628 | 43 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/angry.webp | 427x641 | 44 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/anxious.webp | 427x641 | 42 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/flustered.webp | 427x641 | 41 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/joy.webp | 427x641 | 46 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/neutral.webp | 427x641 | 42 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/760/surprise_talk.webp | 427x641 | 44 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/angry.webp | 628x942 | 72 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/anxious.webp | 627x942 | 70 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/flustered.webp | 628x942 | 68 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/joy.webp | 627x942 | 75 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/neutral.webp | 628x942 | 70 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_seori/840/surprise_talk.webp | 627x942 | 74 KB | resident_seori |
| assets/dialogue-source-master-v2/resident_siluk/560/angry.webp | 407x611 | 46 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/560/anxious.webp | 407x611 | 47 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/560/flustered.webp | 407x611 | 44 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/560/joy.webp | 407x611 | 47 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/560/neutral.webp | 407x611 | 48 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/560/surprise_talk.webp | 407x611 | 45 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/angry.webp | 424x636 | 48 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/anxious.webp | 424x636 | 50 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/flustered.webp | 424x636 | 46 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/joy.webp | 424x636 | 50 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/neutral.webp | 424x636 | 50 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/760/surprise_talk.webp | 424x637 | 48 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/angry.webp | 610x914 | 81 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/anxious.webp | 610x914 | 83 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/flustered.webp | 610x914 | 77 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/joy.webp | 610x914 | 85 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/neutral.webp | 610x914 | 83 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_siluk/840/surprise_talk.webp | 609x915 | 79 KB | resident_siluk |
| assets/dialogue-source-master-v2/resident_sling/560/angry.webp | 407x611 | 48 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/560/anxious.webp | 407x611 | 47 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/560/flustered.webp | 407x611 | 47 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/560/joy.webp | 407x611 | 47 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/560/neutral.webp | 407x611 | 48 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/560/surprise_talk.webp | 407x611 | 51 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/angry.webp | 424x637 | 51 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/anxious.webp | 424x637 | 49 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/flustered.webp | 424x637 | 50 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/joy.webp | 424x637 | 49 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/neutral.webp | 424x637 | 51 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/760/surprise_talk.webp | 424x637 | 54 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/angry.webp | 612x918 | 83 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/anxious.webp | 612x918 | 82 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/flustered.webp | 612x918 | 81 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/joy.webp | 612x918 | 82 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/neutral.webp | 612x918 | 82 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_sling/840/surprise_talk.webp | 612x918 | 87 KB | resident_sling |
| assets/dialogue-source-master-v2/resident_somi/560/angry.webp | 393x590 | 44 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/560/anxious.webp | 393x590 | 44 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/560/flustered.webp | 393x590 | 43 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/560/joy.webp | 393x590 | 46 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/560/neutral.webp | 393x590 | 44 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/560/surprise_talk.webp | 393x590 | 46 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/angry.webp | 427x640 | 49 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/anxious.webp | 426x641 | 49 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/flustered.webp | 427x640 | 48 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/joy.webp | 427x640 | 50 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/neutral.webp | 426x640 | 50 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/760/surprise_talk.webp | 426x640 | 51 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/angry.webp | 589x883 | 77 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/anxious.webp | 588x885 | 78 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/flustered.webp | 589x883 | 75 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/joy.webp | 589x883 | 79 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/neutral.webp | 588x884 | 76 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_somi/840/surprise_talk.webp | 588x884 | 80 KB | resident_somi |
| assets/dialogue-source-master-v2/resident_teacher/560/angry.webp | 326x489 | 42 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/560/anxious.webp | 326x489 | 39 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/560/flustered.webp | 326x489 | 38 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/560/joy.webp | 326x490 | 43 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/560/neutral.webp | 326x489 | 41 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/560/surprise_talk.webp | 326x489 | 42 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/angry.webp | 326x489 | 42 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/anxious.webp | 326x489 | 39 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/flustered.webp | 326x489 | 38 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/joy.webp | 326x490 | 43 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/neutral.webp | 326x489 | 41 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/760/surprise_talk.webp | 326x489 | 42 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/angry.webp | 580x870 | 88 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/anxious.webp | 580x870 | 81 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/flustered.webp | 580x870 | 80 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/joy.webp | 580x871 | 92 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/neutral.webp | 580x870 | 87 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_teacher/840/surprise_talk.webp | 580x870 | 90 KB | resident_teacher |
| assets/dialogue-source-master-v2/resident_tok/560/angry.webp | 403x604 | 49 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/560/anxious.webp | 403x604 | 44 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/560/flustered.webp | 403x604 | 44 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/560/joy.webp | 403x604 | 51 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/560/neutral.webp | 403x604 | 47 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/560/surprise_talk.webp | 402x605 | 47 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/angry.webp | 410x615 | 50 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/anxious.webp | 410x615 | 46 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/flustered.webp | 410x615 | 46 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/joy.webp | 410x615 | 51 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/neutral.webp | 410x615 | 48 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/760/surprise_talk.webp | 409x616 | 48 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/angry.webp | 603x904 | 82 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/anxious.webp | 603x904 | 74 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/flustered.webp | 603x904 | 73 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/joy.webp | 603x904 | 85 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/neutral.webp | 603x904 | 78 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tok/840/surprise_talk.webp | 602x905 | 82 KB | resident_tok |
| assets/dialogue-source-master-v2/resident_tosil/560/angry.webp | 397x596 | 45 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/560/anxious.webp | 397x596 | 43 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/560/flustered.webp | 397x596 | 42 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/560/joy.webp | 397x596 | 44 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/560/neutral.webp | 397x596 | 42 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/560/surprise_talk.webp | 397x596 | 48 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/angry.webp | 414x621 | 47 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/anxious.webp | 414x621 | 45 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/flustered.webp | 414x621 | 45 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/joy.webp | 414x621 | 46 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/neutral.webp | 414x621 | 44 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/760/surprise_talk.webp | 414x621 | 50 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/angry.webp | 597x896 | 73 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/anxious.webp | 597x896 | 71 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/flustered.webp | 597x896 | 68 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/joy.webp | 597x896 | 70 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/neutral.webp | 597x896 | 68 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_tosil/840/surprise_talk.webp | 597x896 | 81 KB | resident_tosil |
| assets/dialogue-source-master-v2/resident_ttadak/560/angry.webp | 395x594 | 47 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/560/anxious.webp | 396x593 | 42 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/560/flustered.webp | 396x593 | 43 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/560/joy.webp | 396x593 | 48 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/560/neutral.webp | 395x594 | 47 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/560/surprise_talk.webp | 396x593 | 49 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/angry.webp | 407x612 | 50 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/anxious.webp | 408x612 | 44 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/flustered.webp | 408x612 | 45 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/joy.webp | 408x612 | 50 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/neutral.webp | 407x612 | 49 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/760/surprise_talk.webp | 408x612 | 51 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/angry.webp | 593x890 | 84 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/anxious.webp | 593x890 | 74 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/flustered.webp | 593x890 | 78 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/joy.webp | 593x890 | 84 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/neutral.webp | 593x890 | 84 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ttadak/840/surprise_talk.webp | 593x890 | 86 KB | resident_ttadak |
| assets/dialogue-source-master-v2/resident_ubak/560/angry.webp | 402x603 | 43 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/560/anxious.webp | 402x604 | 40 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/560/flustered.webp | 400x606 | 40 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/560/joy.webp | 402x603 | 43 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/560/neutral.webp | 402x604 | 40 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/560/surprise_talk.webp | 402x603 | 45 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/angry.webp | 418x627 | 46 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/anxious.webp | 418x628 | 42 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/flustered.webp | 416x630 | 42 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/joy.webp | 418x627 | 46 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/neutral.webp | 418x628 | 42 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/760/surprise_talk.webp | 418x627 | 47 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/angry.webp | 602x903 | 74 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/anxious.webp | 602x904 | 69 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/flustered.webp | 599x908 | 71 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/joy.webp | 602x903 | 76 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/neutral.webp | 602x904 | 70 KB | resident_ubak |
| assets/dialogue-source-master-v2/resident_ubak/840/surprise_talk.webp | 602x903 | 79 KB | resident_ubak |
| assets/dialogue-source-master-v2/seryeon/560/angry.webp | 410x615 | 48 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/560/anxious.webp | 410x615 | 47 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/560/flustered.webp | 410x615 | 46 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/560/joy.webp | 410x615 | 47 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/560/neutral.webp | 410x615 | 47 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/560/surprise_talk.webp | 410x615 | 48 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/angry.webp | 424x637 | 50 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/anxious.webp | 424x637 | 50 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/flustered.webp | 424x636 | 48 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/joy.webp | 424x637 | 50 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/neutral.webp | 424x637 | 49 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/760/surprise_talk.webp | 424x637 | 51 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/angry.webp | 615x922 | 83 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/anxious.webp | 615x922 | 82 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/flustered.webp | 615x921 | 80 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/joy.webp | 615x922 | 82 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/neutral.webp | 615x922 | 79 KB | seryeon |
| assets/dialogue-source-master-v2/seryeon/840/surprise_talk.webp | 615x922 | 83 KB | seryeon |
| assets/dialogue-source-master/bami/560/angry.webp | 345x517 | 64 KB | bami |
| assets/dialogue-source-master/bami/560/anxious.webp | 274x517 | 33 KB | bami |
| assets/dialogue-source-master/bami/560/joy.webp | 274x517 | 36 KB | bami |
| assets/dialogue-source-master/bami/560/neutral.webp | 280x529 | 41 KB | bami |
| assets/dialogue-source-master/bami/560/surprise_react.webp | 274x517 | 33 KB | bami |
| assets/dialogue-source-master/bami/560/surprise_talk.webp | 275x517 | 37 KB | bami |
| assets/dialogue-source-master/bami/760/angry.webp | 400x600 | 83 KB | bami |
| assets/dialogue-source-master/bami/760/anxious.webp | 318x600 | 41 KB | bami |
| assets/dialogue-source-master/bami/760/joy.webp | 318x600 | 46 KB | bami |
| assets/dialogue-source-master/bami/760/neutral.webp | 325x614 | 53 KB | bami |
| assets/dialogue-source-master/bami/760/surprise_react.webp | 318x600 | 42 KB | bami |
| assets/dialogue-source-master/bami/760/surprise_talk.webp | 319x600 | 47 KB | bami |
| assets/dialogue-source-master/bami/840/angry.webp | 517x776 | 129 KB | bami |
| assets/dialogue-source-master/bami/840/anxious.webp | 411x776 | 64 KB | bami |
| assets/dialogue-source-master/bami/840/joy.webp | 411x776 | 70 KB | bami |
| assets/dialogue-source-master/bami/840/neutral.webp | 421x794 | 81 KB | bami |
| assets/dialogue-source-master/bami/840/surprise_react.webp | 411x776 | 65 KB | bami |
| assets/dialogue-source-master/bami/840/surprise_talk.webp | 412x776 | 73 KB | bami |
| assets/dialogue-source-master/buri/560/angry.webp | 358x588 | 48 KB | buri |
| assets/dialogue-source-master/buri/560/anxious.webp | 369x588 | 37 KB | buri |
| assets/dialogue-source-master/buri/560/joy.webp | 362x588 | 46 KB | buri |
| assets/dialogue-source-master/buri/560/neutral.webp | 278x588 | 45 KB | buri |
| assets/dialogue-source-master/buri/560/surprise_react.webp | 369x588 | 42 KB | buri |
| assets/dialogue-source-master/buri/560/surprise_talk.webp | 369x588 | 42 KB | buri |
| assets/dialogue-source-master/buri/760/angry.webp | 387x637 | 55 KB | buri |
| assets/dialogue-source-master/buri/760/anxious.webp | 400x637 | 43 KB | buri |
| assets/dialogue-source-master/buri/760/joy.webp | 392x637 | 52 KB | buri |
| assets/dialogue-source-master/buri/760/neutral.webp | 301x637 | 51 KB | buri |
| assets/dialogue-source-master/buri/760/surprise_react.webp | 400x637 | 49 KB | buri |
| assets/dialogue-source-master/buri/760/surprise_talk.webp | 400x637 | 49 KB | buri |
| assets/dialogue-source-master/buri/840/angry.webp | 536x882 | 96 KB | buri |
| assets/dialogue-source-master/buri/840/anxious.webp | 554x882 | 75 KB | buri |
| assets/dialogue-source-master/buri/840/joy.webp | 543x882 | 91 KB | buri |
| assets/dialogue-source-master/buri/840/neutral.webp | 417x882 | 88 KB | buri |
| assets/dialogue-source-master/buri/840/surprise_react.webp | 554x882 | 84 KB | buri |
| assets/dialogue-source-master/buri/840/surprise_talk.webp | 554x882 | 84 KB | buri |
| assets/dialogue-source-master/daram/560/angry.webp | 284x500 | 39 KB | daram |
| assets/dialogue-source-master/daram/560/anxious.webp | 284x500 | 37 KB | daram |
| assets/dialogue-source-master/daram/560/joy.webp | 284x500 | 42 KB | daram |
| assets/dialogue-source-master/daram/560/neutral.webp | 292x511 | 41 KB | daram |
| assets/dialogue-source-master/daram/560/surprise_react.webp | 284x500 | 37 KB | daram |
| assets/dialogue-source-master/daram/560/surprise_talk.webp | 284x500 | 36 KB | daram |
| assets/dialogue-source-master/daram/760/angry.webp | 385x678 | 65 KB | daram |
| assets/dialogue-source-master/daram/760/anxious.webp | 385x678 | 61 KB | daram |
| assets/dialogue-source-master/daram/760/joy.webp | 385x678 | 69 KB | daram |
| assets/dialogue-source-master/daram/760/neutral.webp | 396x693 | 67 KB | daram |
| assets/dialogue-source-master/daram/760/surprise_react.webp | 385x678 | 61 KB | daram |
| assets/dialogue-source-master/daram/760/surprise_talk.webp | 385x678 | 60 KB | daram |
| assets/dialogue-source-master/daram/840/angry.webp | 426x750 | 76 KB | daram |
| assets/dialogue-source-master/daram/840/anxious.webp | 426x750 | 73 KB | daram |
| assets/dialogue-source-master/daram/840/joy.webp | 426x750 | 82 KB | daram |
| assets/dialogue-source-master/daram/840/neutral.webp | 438x766 | 80 KB | daram |
| assets/dialogue-source-master/daram/840/surprise_react.webp | 426x750 | 73 KB | daram |
| assets/dialogue-source-master/daram/840/surprise_talk.webp | 426x750 | 71 KB | daram |
| assets/dialogue-source-master/doto/560/angry.webp | 361x541 | 68 KB | doto |
| assets/dialogue-source-master/doto/560/anxious.webp | 356x541 | 38 KB | doto |
| assets/dialogue-source-master/doto/560/joy.webp | 361x541 | 67 KB | doto |
| assets/dialogue-source-master/doto/560/neutral.webp | 361x541 | 67 KB | doto |
| assets/dialogue-source-master/doto/560/surprise_react.webp | 356x541 | 37 KB | doto |
| assets/dialogue-source-master/doto/560/surprise_talk.webp | 356x541 | 40 KB | doto |
| assets/dialogue-source-master/doto/760/angry.webp | 400x600 | 81 KB | doto |
| assets/dialogue-source-master/doto/760/anxious.webp | 394x600 | 46 KB | doto |
| assets/dialogue-source-master/doto/760/joy.webp | 400x600 | 80 KB | doto |
| assets/dialogue-source-master/doto/760/neutral.webp | 400x600 | 80 KB | doto |
| assets/dialogue-source-master/doto/760/surprise_react.webp | 394x600 | 44 KB | doto |
| assets/dialogue-source-master/doto/760/surprise_talk.webp | 394x600 | 48 KB | doto |
| assets/dialogue-source-master/doto/840/angry.webp | 541x811 | 137 KB | doto |
| assets/dialogue-source-master/doto/840/anxious.webp | 533x811 | 76 KB | doto |
| assets/dialogue-source-master/doto/840/joy.webp | 541x811 | 136 KB | doto |
| assets/dialogue-source-master/doto/840/neutral.webp | 541x811 | 134 KB | doto |
| assets/dialogue-source-master/doto/840/surprise_react.webp | 533x811 | 73 KB | doto |
| assets/dialogue-source-master/doto/840/surprise_talk.webp | 533x811 | 79 KB | doto |
| assets/dialogue-source-master/granny/560/angry.webp | 367x588 | 52 KB | granny |
| assets/dialogue-source-master/granny/560/anxious.webp | 367x588 | 50 KB | granny |
| assets/dialogue-source-master/granny/560/joy.webp | 367x588 | 51 KB | granny |
| assets/dialogue-source-master/granny/560/neutral.webp | 367x588 | 47 KB | granny |
| assets/dialogue-source-master/granny/560/surprise_react.webp | 367x588 | 48 KB | granny |
| assets/dialogue-source-master/granny/560/surprise_talk.webp | 368x588 | 47 KB | granny |
| assets/dialogue-source-master/granny/760/angry.webp | 399x639 | 61 KB | granny |
| assets/dialogue-source-master/granny/760/anxious.webp | 399x639 | 58 KB | granny |
| assets/dialogue-source-master/granny/760/joy.webp | 399x639 | 60 KB | granny |
| assets/dialogue-source-master/granny/760/neutral.webp | 399x639 | 56 KB | granny |
| assets/dialogue-source-master/granny/760/surprise_react.webp | 399x639 | 56 KB | granny |
| assets/dialogue-source-master/granny/760/surprise_talk.webp | 400x639 | 55 KB | granny |
| assets/dialogue-source-master/granny/840/angry.webp | 550x882 | 104 KB | granny |
| assets/dialogue-source-master/granny/840/anxious.webp | 550x882 | 100 KB | granny |
| assets/dialogue-source-master/granny/840/joy.webp | 550x882 | 102 KB | granny |
| assets/dialogue-source-master/granny/840/neutral.webp | 550x882 | 95 KB | granny |
| assets/dialogue-source-master/granny/840/surprise_react.webp | 550x882 | 97 KB | granny |
| assets/dialogue-source-master/granny/840/surprise_talk.webp | 552x882 | 95 KB | granny |
| assets/dialogue-source-master/guard/560/angry.webp | 357x588 | 60 KB | guard |
| assets/dialogue-source-master/guard/560/anxious.webp | 357x588 | 55 KB | guard |
| assets/dialogue-source-master/guard/560/joy.webp | 357x588 | 58 KB | guard |
| assets/dialogue-source-master/guard/560/neutral.webp | 357x588 | 58 KB | guard |
| assets/dialogue-source-master/guard/560/surprise_react.webp | 357x588 | 58 KB | guard |
| assets/dialogue-source-master/guard/560/surprise_talk.webp | 357x588 | 56 KB | guard |
| assets/dialogue-source-master/guard/760/angry.webp | 400x658 | 73 KB | guard |
| assets/dialogue-source-master/guard/760/anxious.webp | 400x658 | 67 KB | guard |
| assets/dialogue-source-master/guard/760/joy.webp | 400x658 | 71 KB | guard |
| assets/dialogue-source-master/guard/760/neutral.webp | 399x658 | 70 KB | guard |
| assets/dialogue-source-master/guard/760/surprise_react.webp | 400x658 | 70 KB | guard |
| assets/dialogue-source-master/guard/760/surprise_talk.webp | 400x658 | 68 KB | guard |
| assets/dialogue-source-master/guard/840/angry.webp | 536x882 | 120 KB | guard |
| assets/dialogue-source-master/guard/840/anxious.webp | 536x882 | 110 KB | guard |
| assets/dialogue-source-master/guard/840/joy.webp | 536x882 | 117 KB | guard |
| assets/dialogue-source-master/guard/840/neutral.webp | 535x882 | 116 KB | guard |
| assets/dialogue-source-master/guard/840/surprise_react.webp | 536x882 | 115 KB | guard |
| assets/dialogue-source-master/guard/840/surprise_talk.webp | 536x882 | 112 KB | guard |
| assets/dialogue-source-master/karo/560/angry.webp | 369x588 | 52 KB | karo |
| assets/dialogue-source-master/karo/560/anxious.webp | 369x588 | 54 KB | karo |
| assets/dialogue-source-master/karo/560/joy.webp | 369x588 | 49 KB | karo |
| assets/dialogue-source-master/karo/560/neutral.webp | 369x588 | 56 KB | karo |
| assets/dialogue-source-master/karo/560/surprise_react.webp | 370x588 | 53 KB | karo |
| assets/dialogue-source-master/karo/560/surprise_talk.webp | 370x588 | 50 KB | karo |
| assets/dialogue-source-master/karo/760/angry.webp | 399x636 | 60 KB | karo |
| assets/dialogue-source-master/karo/760/anxious.webp | 399x636 | 62 KB | karo |
| assets/dialogue-source-master/karo/760/joy.webp | 399x636 | 56 KB | karo |
| assets/dialogue-source-master/karo/760/neutral.webp | 399x636 | 64 KB | karo |
| assets/dialogue-source-master/karo/760/surprise_react.webp | 400x636 | 61 KB | karo |
| assets/dialogue-source-master/karo/760/surprise_talk.webp | 400x636 | 58 KB | karo |
| assets/dialogue-source-master/karo/840/angry.webp | 554x882 | 105 KB | karo |
| assets/dialogue-source-master/karo/840/anxious.webp | 554x882 | 108 KB | karo |
| assets/dialogue-source-master/karo/840/joy.webp | 554x882 | 97 KB | karo |
| assets/dialogue-source-master/karo/840/neutral.webp | 554x882 | 110 KB | karo |
| assets/dialogue-source-master/karo/840/surprise_react.webp | 555x882 | 106 KB | karo |
| assets/dialogue-source-master/karo/840/surprise_talk.webp | 555x882 | 100 KB | karo |
| assets/dialogue-source-master/kid_bang/560/angry.webp | 333x500 | 53 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/560/anxious.webp | 333x500 | 50 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/560/joy.webp | 333x500 | 56 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/560/neutral.webp | 333x500 | 50 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/560/surprise_react.webp | 333x500 | 55 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/560/surprise_talk.webp | 333x500 | 52 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/angry.webp | 400x600 | 68 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/anxious.webp | 400x600 | 64 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/joy.webp | 400x600 | 71 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/neutral.webp | 400x600 | 65 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/surprise_react.webp | 400x600 | 70 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/760/surprise_talk.webp | 400x600 | 66 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/angry.webp | 500x750 | 93 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/anxious.webp | 500x750 | 88 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/joy.webp | 500x750 | 98 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/neutral.webp | 500x750 | 88 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/surprise_react.webp | 500x750 | 96 KB | kid_bang |
| assets/dialogue-source-master/kid_bang/840/surprise_talk.webp | 500x750 | 91 KB | kid_bang |
| assets/dialogue-source-master/kid_dodam/560/angry.webp | 333x500 | 49 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/560/anxious.webp | 333x500 | 46 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/560/joy.webp | 333x500 | 52 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/560/neutral.webp | 333x500 | 44 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/560/surprise_react.webp | 333x500 | 51 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/560/surprise_talk.webp | 333x500 | 48 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/angry.webp | 400x600 | 64 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/anxious.webp | 400x600 | 60 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/joy.webp | 400x600 | 67 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/neutral.webp | 400x600 | 57 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/surprise_react.webp | 400x600 | 65 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/760/surprise_talk.webp | 400x600 | 62 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/angry.webp | 500x750 | 88 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/anxious.webp | 500x750 | 82 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/joy.webp | 500x750 | 93 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/neutral.webp | 500x750 | 79 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/surprise_react.webp | 500x750 | 89 KB | kid_dodam |
| assets/dialogue-source-master/kid_dodam/840/surprise_talk.webp | 500x750 | 84 KB | kid_dodam |
| assets/dialogue-source-master/kid_kkam/560/angry.webp | 333x500 | 49 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/560/anxious.webp | 333x500 | 41 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/560/joy.webp | 333x500 | 47 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/560/neutral.webp | 333x500 | 44 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/560/surprise_react.webp | 333x500 | 49 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/560/surprise_talk.webp | 333x500 | 47 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/angry.webp | 400x600 | 64 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/anxious.webp | 400x600 | 53 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/joy.webp | 400x600 | 61 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/neutral.webp | 400x600 | 57 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/surprise_react.webp | 400x600 | 64 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/760/surprise_talk.webp | 400x600 | 61 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/angry.webp | 500x750 | 88 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/anxious.webp | 500x750 | 75 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/joy.webp | 500x750 | 83 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/neutral.webp | 500x750 | 77 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/surprise_react.webp | 500x750 | 88 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkam/840/surprise_talk.webp | 500x750 | 84 KB | kid_kkam |
| assets/dialogue-source-master/kid_kkomi/560/angry.webp | 333x500 | 58 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/560/anxious.webp | 333x500 | 53 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/560/joy.webp | 333x500 | 55 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/560/neutral.webp | 333x500 | 54 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/560/surprise_react.webp | 333x500 | 57 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/560/surprise_talk.webp | 333x500 | 56 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/angry.webp | 400x600 | 74 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/anxious.webp | 400x600 | 68 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/joy.webp | 400x600 | 71 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/neutral.webp | 400x600 | 70 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/surprise_react.webp | 400x600 | 73 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/760/surprise_talk.webp | 400x600 | 71 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/angry.webp | 500x750 | 102 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/anxious.webp | 500x750 | 94 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/joy.webp | 500x750 | 98 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/neutral.webp | 500x750 | 96 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/surprise_react.webp | 500x750 | 100 KB | kid_kkomi |
| assets/dialogue-source-master/kid_kkomi/840/surprise_talk.webp | 500x750 | 98 KB | kid_kkomi |
| assets/dialogue-source-master/kid_mong/560/angry.webp | 333x500 | 62 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/560/anxious.webp | 333x500 | 55 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/560/joy.webp | 333x500 | 57 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/560/neutral.webp | 333x500 | 57 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/560/surprise_react.webp | 333x500 | 58 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/560/surprise_talk.webp | 333x500 | 59 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/angry.webp | 400x600 | 80 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/anxious.webp | 400x600 | 70 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/joy.webp | 400x600 | 75 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/neutral.webp | 400x600 | 73 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/surprise_react.webp | 400x600 | 74 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/760/surprise_talk.webp | 400x600 | 76 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/angry.webp | 500x750 | 109 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/anxious.webp | 500x750 | 96 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/joy.webp | 500x750 | 102 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/neutral.webp | 500x750 | 101 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/surprise_react.webp | 500x750 | 103 KB | kid_mong |
| assets/dialogue-source-master/kid_mong/840/surprise_talk.webp | 500x750 | 104 KB | kid_mong |
| assets/dialogue-source-master/kid_nubi1/560/angry.webp | 333x500 | 46 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/560/anxious.webp | 333x500 | 42 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/560/joy.webp | 333x500 | 44 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/560/neutral.webp | 333x500 | 44 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/560/surprise_react.webp | 333x500 | 42 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/560/surprise_talk.webp | 333x500 | 43 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/angry.webp | 400x600 | 59 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/anxious.webp | 400x600 | 53 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/joy.webp | 400x600 | 56 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/neutral.webp | 400x600 | 57 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/surprise_react.webp | 400x600 | 54 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/760/surprise_talk.webp | 400x600 | 55 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/angry.webp | 500x750 | 79 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/anxious.webp | 500x750 | 70 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/joy.webp | 500x750 | 73 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/neutral.webp | 500x750 | 76 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/surprise_react.webp | 500x750 | 73 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi1/840/surprise_talk.webp | 500x750 | 72 KB | kid_nubi1 |
| assets/dialogue-source-master/kid_nubi2/560/angry.webp | 333x500 | 45 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/560/anxious.webp | 333x500 | 42 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/560/joy.webp | 333x500 | 43 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/560/neutral.webp | 333x500 | 41 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/560/surprise_react.webp | 333x500 | 43 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/560/surprise_talk.webp | 333x500 | 43 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/angry.webp | 400x600 | 59 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/anxious.webp | 400x600 | 52 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/joy.webp | 400x600 | 55 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/neutral.webp | 400x600 | 54 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/surprise_react.webp | 400x600 | 55 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/760/surprise_talk.webp | 400x600 | 54 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/angry.webp | 500x750 | 78 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/anxious.webp | 500x750 | 69 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/joy.webp | 500x750 | 73 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/neutral.webp | 500x750 | 70 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/surprise_react.webp | 500x750 | 73 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_nubi2/840/surprise_talk.webp | 500x750 | 73 KB | kid_nubi2 |
| assets/dialogue-source-master/kid_saemi/560/angry.webp | 333x500 | 54 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/560/anxious.webp | 333x500 | 50 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/560/joy.webp | 333x500 | 54 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/560/neutral.webp | 333x500 | 51 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/560/surprise_react.webp | 333x500 | 53 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/560/surprise_talk.webp | 333x500 | 52 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/angry.webp | 400x600 | 70 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/anxious.webp | 400x600 | 65 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/joy.webp | 400x600 | 69 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/neutral.webp | 400x600 | 67 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/surprise_react.webp | 400x600 | 67 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/760/surprise_talk.webp | 400x600 | 66 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/angry.webp | 500x750 | 96 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/anxious.webp | 500x750 | 89 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/joy.webp | 500x750 | 96 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/neutral.webp | 500x750 | 92 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/surprise_react.webp | 500x750 | 93 KB | kid_saemi |
| assets/dialogue-source-master/kid_saemi/840/surprise_talk.webp | 500x750 | 92 KB | kid_saemi |
| assets/dialogue-source-master/mom/560/angry.webp | 394x588 | 64 KB | mom |
| assets/dialogue-source-master/mom/560/anxious.webp | 394x588 | 65 KB | mom |
| assets/dialogue-source-master/mom/560/joy.webp | 394x588 | 66 KB | mom |
| assets/dialogue-source-master/mom/560/neutral.webp | 394x588 | 63 KB | mom |
| assets/dialogue-source-master/mom/560/surprise_react.webp | 394x588 | 66 KB | mom |
| assets/dialogue-source-master/mom/560/surprise_talk.webp | 394x588 | 64 KB | mom |
| assets/dialogue-source-master/mom/760/angry.webp | 400x598 | 66 KB | mom |
| assets/dialogue-source-master/mom/760/anxious.webp | 400x598 | 67 KB | mom |
| assets/dialogue-source-master/mom/760/joy.webp | 400x598 | 68 KB | mom |
| assets/dialogue-source-master/mom/760/neutral.webp | 400x598 | 65 KB | mom |
| assets/dialogue-source-master/mom/760/surprise_react.webp | 400x598 | 68 KB | mom |
| assets/dialogue-source-master/mom/760/surprise_talk.webp | 400x598 | 66 KB | mom |
| assets/dialogue-source-master/mom/840/angry.webp | 590x882 | 129 KB | mom |
| assets/dialogue-source-master/mom/840/anxious.webp | 590x882 | 129 KB | mom |
| assets/dialogue-source-master/mom/840/joy.webp | 590x882 | 132 KB | mom |
| assets/dialogue-source-master/mom/840/neutral.webp | 590x882 | 127 KB | mom |
| assets/dialogue-source-master/mom/840/surprise_react.webp | 590x882 | 132 KB | mom |
| assets/dialogue-source-master/mom/840/surprise_talk.webp | 590x882 | 128 KB | mom |
| assets/dialogue-source-master/nabi/560/angry.webp | 320x584 | 46 KB | nabi |
| assets/dialogue-source-master/nabi/560/anxious.webp | 321x584 | 45 KB | nabi |
| assets/dialogue-source-master/nabi/560/joy.webp | 321x584 | 45 KB | nabi |
| assets/dialogue-source-master/nabi/560/neutral.webp | 321x584 | 44 KB | nabi |
| assets/dialogue-source-master/nabi/560/surprise_react.webp | 400x584 | 55 KB | nabi |
| assets/dialogue-source-master/nabi/560/surprise_talk.webp | 400x584 | 50 KB | nabi |
| assets/dialogue-source-master/nabi/760/angry.webp | 320x584 | 46 KB | nabi |
| assets/dialogue-source-master/nabi/760/anxious.webp | 321x584 | 45 KB | nabi |
| assets/dialogue-source-master/nabi/760/joy.webp | 321x584 | 45 KB | nabi |
| assets/dialogue-source-master/nabi/760/neutral.webp | 321x584 | 44 KB | nabi |
| assets/dialogue-source-master/nabi/760/surprise_react.webp | 400x584 | 55 KB | nabi |
| assets/dialogue-source-master/nabi/760/surprise_talk.webp | 400x584 | 50 KB | nabi |
| assets/dialogue-source-master/nabi/840/angry.webp | 484x882 | 93 KB | nabi |
| assets/dialogue-source-master/nabi/840/anxious.webp | 484x882 | 91 KB | nabi |
| assets/dialogue-source-master/nabi/840/joy.webp | 485x882 | 92 KB | nabi |
| assets/dialogue-source-master/nabi/840/neutral.webp | 485x882 | 89 KB | nabi |
| assets/dialogue-source-master/nabi/840/surprise_react.webp | 604x882 | 111 KB | nabi |
| assets/dialogue-source-master/nabi/840/surprise_talk.webp | 604x882 | 102 KB | nabi |
| assets/dialogue-source-master/neoul/560/angry.webp | 384x560 | 54 KB | neoul |
| assets/dialogue-source-master/neoul/560/anxious.webp | 384x560 | 50 KB | neoul |
| assets/dialogue-source-master/neoul/560/joy.webp | 384x560 | 52 KB | neoul |
| assets/dialogue-source-master/neoul/560/neutral.webp | 388x566 | 55 KB | neoul |
| assets/dialogue-source-master/neoul/560/surprise_react.webp | 384x560 | 54 KB | neoul |
| assets/dialogue-source-master/neoul/560/surprise_talk.webp | 384x560 | 51 KB | neoul |
| assets/dialogue-source-master/neoul/760/angry.webp | 384x560 | 54 KB | neoul |
| assets/dialogue-source-master/neoul/760/anxious.webp | 384x560 | 50 KB | neoul |
| assets/dialogue-source-master/neoul/760/joy.webp | 384x560 | 52 KB | neoul |
| assets/dialogue-source-master/neoul/760/neutral.webp | 388x566 | 55 KB | neoul |
| assets/dialogue-source-master/neoul/760/surprise_react.webp | 384x560 | 54 KB | neoul |
| assets/dialogue-source-master/neoul/760/surprise_talk.webp | 384x560 | 51 KB | neoul |
| assets/dialogue-source-master/neoul/840/angry.webp | 605x882 | 118 KB | neoul |
| assets/dialogue-source-master/neoul/840/anxious.webp | 605x882 | 110 KB | neoul |
| assets/dialogue-source-master/neoul/840/joy.webp | 605x882 | 114 KB | neoul |
| assets/dialogue-source-master/neoul/840/neutral.webp | 613x893 | 120 KB | neoul |
| assets/dialogue-source-master/neoul/840/surprise_react.webp | 605x882 | 117 KB | neoul |
| assets/dialogue-source-master/neoul/840/surprise_talk.webp | 605x882 | 111 KB | neoul |
| assets/dialogue-source-master/npc_pandol/560/angry.webp | 392x588 | 75 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/560/anxious.webp | 392x588 | 70 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/560/joy.webp | 392x588 | 73 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/560/neutral.webp | 392x588 | 73 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/560/surprise_react.webp | 392x588 | 73 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/560/surprise_talk.webp | 392x588 | 70 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/angry.webp | 400x600 | 77 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/anxious.webp | 400x600 | 72 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/joy.webp | 400x600 | 75 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/neutral.webp | 400x600 | 75 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/surprise_react.webp | 400x600 | 75 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/760/surprise_talk.webp | 400x600 | 72 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/angry.webp | 588x882 | 133 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/anxious.webp | 588x882 | 125 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/joy.webp | 588x882 | 130 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/neutral.webp | 588x882 | 131 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/surprise_react.webp | 588x882 | 129 KB | npc_pandol |
| assets/dialogue-source-master/npc_pandol/840/surprise_talk.webp | 588x882 | 126 KB | npc_pandol |
| assets/dialogue-source-master/resident_badook/560/angry.webp | 395x588 | 59 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/560/anxious.webp | 395x588 | 57 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/560/joy.webp | 395x588 | 56 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/560/neutral.webp | 395x588 | 55 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/560/surprise_react.webp | 395x588 | 58 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/560/surprise_talk.webp | 395x588 | 55 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/angry.webp | 400x595 | 61 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/anxious.webp | 400x595 | 58 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/joy.webp | 400x595 | 57 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/neutral.webp | 400x595 | 57 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/surprise_react.webp | 400x595 | 60 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/760/surprise_talk.webp | 400x595 | 56 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/angry.webp | 593x882 | 118 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/anxious.webp | 593x882 | 114 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/joy.webp | 593x882 | 112 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/neutral.webp | 593x882 | 111 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/surprise_react.webp | 593x882 | 117 KB | resident_badook |
| assets/dialogue-source-master/resident_badook/840/surprise_talk.webp | 593x882 | 109 KB | resident_badook |
| assets/dialogue-source-master/resident_bori/560/angry.webp | 400x531 | 56 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/560/anxious.webp | 400x531 | 47 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/560/joy.webp | 400x531 | 55 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/560/neutral.webp | 400x531 | 53 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/560/surprise_react.webp | 399x531 | 51 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/560/surprise_talk.webp | 400x531 | 51 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/angry.webp | 400x531 | 56 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/anxious.webp | 400x531 | 47 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/joy.webp | 400x531 | 55 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/neutral.webp | 400x531 | 53 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/surprise_react.webp | 399x531 | 51 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/760/surprise_talk.webp | 400x531 | 51 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/angry.webp | 664x882 | 133 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/anxious.webp | 664x882 | 111 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/joy.webp | 664x882 | 132 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/neutral.webp | 664x882 | 127 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/surprise_react.webp | 663x882 | 122 KB | resident_bori |
| assets/dialogue-source-master/resident_bori/840/surprise_talk.webp | 664x882 | 120 KB | resident_bori |
| assets/dialogue-source-master/resident_eunho/560/angry.webp | 397x588 | 48 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/560/anxious.webp | 397x588 | 50 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/560/joy.webp | 397x588 | 52 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/560/neutral.webp | 397x588 | 51 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/560/surprise_react.webp | 397x588 | 53 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/560/surprise_talk.webp | 397x588 | 51 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/angry.webp | 400x593 | 49 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/anxious.webp | 400x593 | 51 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/joy.webp | 400x593 | 53 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/neutral.webp | 400x593 | 52 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/surprise_react.webp | 400x593 | 53 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/760/surprise_talk.webp | 400x593 | 52 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/angry.webp | 595x882 | 96 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/anxious.webp | 595x882 | 100 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/joy.webp | 595x882 | 104 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/neutral.webp | 595x882 | 101 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/surprise_react.webp | 595x882 | 105 KB | resident_eunho |
| assets/dialogue-source-master/resident_eunho/840/surprise_talk.webp | 595x882 | 102 KB | resident_eunho |
| assets/dialogue-source-master/resident_guldol/560/angry.webp | 392x588 | 61 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/560/anxious.webp | 392x588 | 63 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/560/joy.webp | 392x588 | 61 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/560/neutral.webp | 392x588 | 58 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/560/surprise_react.webp | 392x588 | 61 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/560/surprise_talk.webp | 392x588 | 59 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/angry.webp | 400x600 | 62 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/anxious.webp | 400x600 | 64 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/joy.webp | 400x600 | 62 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/neutral.webp | 400x600 | 60 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/surprise_react.webp | 400x600 | 64 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/760/surprise_talk.webp | 400x600 | 61 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/angry.webp | 588x882 | 110 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/anxious.webp | 588x882 | 110 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/joy.webp | 588x882 | 110 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/neutral.webp | 588x882 | 104 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/surprise_react.webp | 588x882 | 110 KB | resident_guldol |
| assets/dialogue-source-master/resident_guldol/840/surprise_talk.webp | 588x882 | 106 KB | resident_guldol |
| assets/dialogue-source-master/resident_kongi/560/angry.webp | 390x588 | 58 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/560/anxious.webp | 392x588 | 82 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/560/joy.webp | 390x588 | 57 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/560/neutral.webp | 390x588 | 56 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/560/surprise_react.webp | 390x588 | 61 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/560/surprise_talk.webp | 390x588 | 56 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/angry.webp | 398x600 | 60 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/anxious.webp | 400x600 | 84 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/joy.webp | 398x600 | 59 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/neutral.webp | 398x600 | 58 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/surprise_react.webp | 398x600 | 63 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/760/surprise_talk.webp | 398x600 | 58 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/angry.webp | 585x882 | 115 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/anxious.webp | 588x882 | 165 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/joy.webp | 585x882 | 114 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/neutral.webp | 585x882 | 112 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/surprise_react.webp | 585x882 | 121 KB | resident_kongi |
| assets/dialogue-source-master/resident_kongi/840/surprise_talk.webp | 585x882 | 112 KB | resident_kongi |
| assets/dialogue-source-master/resident_lamplighter/560/angry.webp | 384x588 | 50 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/560/anxious.webp | 384x588 | 47 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/560/joy.webp | 384x588 | 47 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/560/neutral.webp | 384x588 | 47 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/560/surprise_react.webp | 385x588 | 52 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/560/surprise_talk.webp | 384x588 | 46 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/angry.webp | 400x611 | 53 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/anxious.webp | 400x611 | 50 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/joy.webp | 400x611 | 51 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/neutral.webp | 400x611 | 50 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/surprise_react.webp | 400x611 | 56 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/760/surprise_talk.webp | 400x611 | 49 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/angry.webp | 577x882 | 99 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/anxious.webp | 577x882 | 93 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/joy.webp | 577x882 | 95 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/neutral.webp | 577x882 | 93 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/surprise_react.webp | 577x882 | 104 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_lamplighter/840/surprise_talk.webp | 577x882 | 92 KB | resident_lamplighter |
| assets/dialogue-source-master/resident_madam/560/angry.webp | 360x588 | 52 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/560/anxious.webp | 360x588 | 48 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/560/joy.webp | 360x588 | 51 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/560/neutral.webp | 360x588 | 48 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/560/surprise_react.webp | 360x588 | 53 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/560/surprise_talk.webp | 360x588 | 50 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/angry.webp | 400x654 | 62 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/anxious.webp | 400x654 | 57 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/joy.webp | 400x654 | 61 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/neutral.webp | 400x654 | 57 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/surprise_react.webp | 400x654 | 64 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/760/surprise_talk.webp | 400x654 | 60 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/angry.webp | 539x882 | 103 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/anxious.webp | 540x882 | 95 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/joy.webp | 540x882 | 101 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/neutral.webp | 540x882 | 95 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/surprise_react.webp | 540x882 | 106 KB | resident_madam |
| assets/dialogue-source-master/resident_madam/840/surprise_talk.webp | 540x882 | 100 KB | resident_madam |
| assets/dialogue-source-master/resident_momo/560/angry.webp | 392x588 | 78 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/560/anxious.webp | 384x588 | 51 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/560/joy.webp | 392x588 | 81 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/560/neutral.webp | 392x588 | 77 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/560/surprise_react.webp | 384x588 | 53 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/560/surprise_talk.webp | 385x588 | 50 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/angry.webp | 400x600 | 81 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/anxious.webp | 392x600 | 53 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/joy.webp | 400x600 | 84 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/neutral.webp | 400x600 | 79 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/surprise_react.webp | 392x600 | 55 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/760/surprise_talk.webp | 393x600 | 52 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/angry.webp | 588x882 | 157 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/anxious.webp | 577x882 | 102 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/joy.webp | 588x882 | 162 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/neutral.webp | 588x882 | 155 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/surprise_react.webp | 577x882 | 106 KB | resident_momo |
| assets/dialogue-source-master/resident_momo/840/surprise_talk.webp | 577x882 | 99 KB | resident_momo |
| assets/dialogue-source-master/resident_musoe/560/angry.webp | 392x588 | 85 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/560/anxious.webp | 392x588 | 82 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/560/joy.webp | 392x588 | 84 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/560/neutral.webp | 392x588 | 84 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/560/surprise_react.webp | 392x588 | 85 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/560/surprise_talk.webp | 392x588 | 81 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/angry.webp | 400x600 | 87 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/anxious.webp | 400x600 | 85 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/joy.webp | 400x600 | 87 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/neutral.webp | 400x600 | 87 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/surprise_react.webp | 400x600 | 88 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/760/surprise_talk.webp | 400x600 | 84 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/angry.webp | 588x882 | 169 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/anxious.webp | 588x882 | 164 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/joy.webp | 588x882 | 169 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/neutral.webp | 588x882 | 169 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/surprise_react.webp | 588x882 | 170 KB | resident_musoe |
| assets/dialogue-source-master/resident_musoe/840/surprise_talk.webp | 588x882 | 163 KB | resident_musoe |
| assets/dialogue-source-master/resident_nero/560/angry.webp | 392x588 | 79 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/560/anxious.webp | 392x588 | 75 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/560/joy.webp | 392x588 | 78 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/560/neutral.webp | 392x588 | 76 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/560/surprise_react.webp | 392x588 | 78 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/560/surprise_talk.webp | 392x588 | 75 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/angry.webp | 400x600 | 82 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/anxious.webp | 400x600 | 77 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/joy.webp | 400x600 | 80 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/neutral.webp | 400x600 | 78 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/surprise_react.webp | 400x600 | 81 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/760/surprise_talk.webp | 400x600 | 78 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/angry.webp | 588x882 | 159 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/anxious.webp | 588x882 | 150 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/joy.webp | 588x882 | 156 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/neutral.webp | 588x882 | 152 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/surprise_react.webp | 588x882 | 156 KB | resident_nero |
| assets/dialogue-source-master/resident_nero/840/surprise_talk.webp | 588x882 | 152 KB | resident_nero |
| assets/dialogue-source-master/resident_nubi/560/angry.webp | 400x565 | 50 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/560/anxious.webp | 400x565 | 45 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/560/joy.webp | 399x565 | 48 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/560/neutral.webp | 400x565 | 49 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/560/surprise_react.webp | 400x565 | 50 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/560/surprise_talk.webp | 400x565 | 47 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/angry.webp | 400x565 | 50 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/anxious.webp | 400x565 | 45 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/joy.webp | 399x565 | 48 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/neutral.webp | 400x565 | 49 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/surprise_react.webp | 400x565 | 50 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/760/surprise_talk.webp | 400x565 | 47 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/angry.webp | 624x882 | 107 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/anxious.webp | 624x882 | 96 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/joy.webp | 623x882 | 102 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/neutral.webp | 624x882 | 104 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/surprise_react.webp | 624x882 | 106 KB | resident_nubi |
| assets/dialogue-source-master/resident_nubi/840/surprise_talk.webp | 624x882 | 100 KB | resident_nubi |
| assets/dialogue-source-master/resident_owlgp/560/angry.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/560/anxious.webp | 400x583 | 56 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/560/joy.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/560/neutral.webp | 400x583 | 55 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/560/surprise_react.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/560/surprise_talk.webp | 400x583 | 58 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/angry.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/anxious.webp | 400x583 | 56 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/joy.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/neutral.webp | 400x583 | 55 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/surprise_react.webp | 400x583 | 59 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/760/surprise_talk.webp | 400x583 | 58 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/angry.webp | 605x882 | 120 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/anxious.webp | 605x882 | 115 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/joy.webp | 605x882 | 121 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/neutral.webp | 605x882 | 113 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/surprise_react.webp | 605x882 | 122 KB | resident_owlgp |
| assets/dialogue-source-master/resident_owlgp/840/surprise_talk.webp | 605x882 | 119 KB | resident_owlgp |
| assets/dialogue-source-master/resident_piko/560/angry.webp | 381x588 | 53 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/560/anxious.webp | 381x588 | 49 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/560/joy.webp | 381x588 | 54 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/560/neutral.webp | 381x588 | 49 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/560/surprise_react.webp | 392x588 | 79 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/560/surprise_talk.webp | 381x588 | 46 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/angry.webp | 388x600 | 55 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/anxious.webp | 389x600 | 51 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/joy.webp | 389x600 | 56 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/neutral.webp | 388x600 | 51 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/surprise_react.webp | 400x600 | 83 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/760/surprise_talk.webp | 388x600 | 48 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/angry.webp | 571x882 | 107 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/anxious.webp | 571x882 | 98 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/joy.webp | 571x882 | 108 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/neutral.webp | 571x882 | 98 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/surprise_react.webp | 588x882 | 160 KB | resident_piko |
| assets/dialogue-source-master/resident_piko/840/surprise_talk.webp | 571x882 | 94 KB | resident_piko |
| assets/dialogue-source-master/resident_ppul/560/angry.webp | 396x588 | 58 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/560/anxious.webp | 396x588 | 53 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/560/joy.webp | 396x588 | 58 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/560/neutral.webp | 396x588 | 53 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/560/surprise_react.webp | 396x588 | 58 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/560/surprise_talk.webp | 397x588 | 56 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/angry.webp | 399x593 | 58 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/anxious.webp | 399x593 | 53 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/joy.webp | 399x593 | 59 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/neutral.webp | 399x593 | 54 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/surprise_react.webp | 399x593 | 58 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/760/surprise_talk.webp | 400x593 | 57 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/angry.webp | 594x882 | 115 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/anxious.webp | 594x882 | 105 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/joy.webp | 594x882 | 115 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/neutral.webp | 594x882 | 106 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/surprise_react.webp | 594x882 | 115 KB | resident_ppul |
| assets/dialogue-source-master/resident_ppul/840/surprise_talk.webp | 595x882 | 111 KB | resident_ppul |
| assets/dialogue-source-master/resident_seori/560/angry.webp | 388x588 | 42 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/560/anxious.webp | 388x588 | 40 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/560/joy.webp | 388x588 | 44 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/560/neutral.webp | 388x588 | 40 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/560/surprise_react.webp | 388x588 | 44 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/560/surprise_talk.webp | 392x588 | 69 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/angry.webp | 396x600 | 43 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/anxious.webp | 396x600 | 42 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/joy.webp | 396x600 | 46 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/neutral.webp | 396x600 | 42 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/surprise_react.webp | 396x600 | 46 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/760/surprise_talk.webp | 400x600 | 72 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/angry.webp | 582x882 | 84 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/anxious.webp | 582x882 | 81 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/joy.webp | 582x882 | 88 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/neutral.webp | 582x882 | 81 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/surprise_react.webp | 582x882 | 89 KB | resident_seori |
| assets/dialogue-source-master/resident_seori/840/surprise_talk.webp | 588x882 | 140 KB | resident_seori |
| assets/dialogue-source-master/resident_siluk/560/angry.webp | 383x588 | 51 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/560/anxious.webp | 384x588 | 46 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/560/joy.webp | 383x588 | 49 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/560/neutral.webp | 384x588 | 44 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/560/surprise_react.webp | 383x588 | 47 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/560/surprise_talk.webp | 383x588 | 48 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/angry.webp | 399x613 | 55 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/anxious.webp | 400x613 | 50 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/joy.webp | 399x613 | 53 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/neutral.webp | 400x613 | 47 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/surprise_react.webp | 399x613 | 50 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/760/surprise_talk.webp | 399x613 | 51 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/angry.webp | 574x882 | 101 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/anxious.webp | 576x882 | 91 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/joy.webp | 574x882 | 98 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/neutral.webp | 575x882 | 88 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/surprise_react.webp | 574x882 | 93 KB | resident_siluk |
| assets/dialogue-source-master/resident_siluk/840/surprise_talk.webp | 574x882 | 95 KB | resident_siluk |
| assets/dialogue-source-master/resident_sling/560/angry.webp | 384x588 | 56 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/560/anxious.webp | 384x588 | 53 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/560/joy.webp | 384x588 | 56 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/560/neutral.webp | 384x588 | 53 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/560/surprise_react.webp | 384x588 | 55 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/560/surprise_talk.webp | 384x588 | 56 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/angry.webp | 400x612 | 60 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/anxious.webp | 400x612 | 57 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/joy.webp | 400x612 | 60 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/neutral.webp | 400x612 | 57 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/surprise_react.webp | 400x612 | 58 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/760/surprise_talk.webp | 399x612 | 59 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/angry.webp | 577x882 | 112 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/anxious.webp | 577x882 | 105 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/joy.webp | 577x882 | 112 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/neutral.webp | 577x882 | 107 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/surprise_react.webp | 577x882 | 108 KB | resident_sling |
| assets/dialogue-source-master/resident_sling/840/surprise_talk.webp | 576x882 | 111 KB | resident_sling |
| assets/dialogue-source-master/resident_somi/560/angry.webp | 368x588 | 56 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/560/anxious.webp | 369x588 | 55 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/560/joy.webp | 369x588 | 57 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/560/neutral.webp | 365x582 | 58 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/560/surprise_react.webp | 368x588 | 54 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/560/surprise_talk.webp | 368x588 | 54 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/angry.webp | 399x638 | 64 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/anxious.webp | 400x638 | 63 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/joy.webp | 400x638 | 66 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/neutral.webp | 396x631 | 67 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/surprise_react.webp | 399x638 | 62 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/760/surprise_talk.webp | 399x638 | 62 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/angry.webp | 552x882 | 111 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/anxious.webp | 553x882 | 109 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/joy.webp | 553x882 | 113 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/neutral.webp | 547x873 | 115 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/surprise_react.webp | 552x882 | 109 KB | resident_somi |
| assets/dialogue-source-master/resident_somi/840/surprise_talk.webp | 552x882 | 107 KB | resident_somi |
| assets/dialogue-source-master/resident_teacher/560/angry.webp | 380x497 | 55 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/560/anxious.webp | 380x497 | 49 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/560/joy.webp | 380x497 | 50 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/560/neutral.webp | 374x489 | 52 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/560/surprise_react.webp | 380x497 | 48 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/560/surprise_talk.webp | 380x497 | 48 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/angry.webp | 380x497 | 55 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/anxious.webp | 380x497 | 49 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/joy.webp | 380x497 | 50 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/neutral.webp | 374x489 | 52 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/surprise_react.webp | 380x497 | 48 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/760/surprise_talk.webp | 380x497 | 48 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/angry.webp | 676x882 | 147 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/anxious.webp | 676x882 | 133 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/joy.webp | 675x882 | 133 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/neutral.webp | 665x869 | 138 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/surprise_react.webp | 676x882 | 129 KB | resident_teacher |
| assets/dialogue-source-master/resident_teacher/840/surprise_talk.webp | 676x882 | 128 KB | resident_teacher |
| assets/dialogue-source-master/resident_tok/560/angry.webp | 388x588 | 59 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/560/anxious.webp | 387x588 | 56 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/560/joy.webp | 388x588 | 58 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/560/neutral.webp | 392x588 | 79 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/560/surprise_react.webp | 392x588 | 83 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/560/surprise_talk.webp | 388x588 | 58 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/angry.webp | 396x600 | 62 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/anxious.webp | 395x600 | 58 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/joy.webp | 396x600 | 60 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/neutral.webp | 400x600 | 82 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/surprise_react.webp | 400x600 | 86 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/760/surprise_talk.webp | 396x600 | 60 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/angry.webp | 582x882 | 119 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/anxious.webp | 580x882 | 111 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/joy.webp | 582x882 | 115 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/neutral.webp | 588x882 | 160 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/surprise_react.webp | 588x882 | 166 KB | resident_tok |
| assets/dialogue-source-master/resident_tok/840/surprise_talk.webp | 582x882 | 116 KB | resident_tok |
| assets/dialogue-source-master/resident_tosil/560/angry.webp | 365x588 | 49 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/560/anxious.webp | 384x588 | 45 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/560/joy.webp | 366x588 | 47 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/560/neutral.webp | 366x588 | 46 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/560/surprise_react.webp | 384x588 | 46 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/560/surprise_talk.webp | 366x588 | 46 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/angry.webp | 380x612 | 52 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/anxious.webp | 400x612 | 48 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/joy.webp | 380x612 | 50 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/neutral.webp | 380x612 | 49 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/surprise_react.webp | 400x612 | 49 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/760/surprise_talk.webp | 380x612 | 49 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/angry.webp | 548x882 | 98 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/anxious.webp | 577x882 | 89 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/joy.webp | 548x882 | 94 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/neutral.webp | 548x882 | 91 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/surprise_react.webp | 577x882 | 92 KB | resident_tosil |
| assets/dialogue-source-master/resident_tosil/840/surprise_talk.webp | 548x882 | 91 KB | resident_tosil |
| assets/dialogue-source-master/resident_ttadak/560/angry.webp | 388x588 | 53 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/560/anxious.webp | 388x588 | 50 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/560/joy.webp | 388x588 | 55 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/560/neutral.webp | 388x588 | 51 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/560/surprise_react.webp | 388x588 | 54 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/560/surprise_talk.webp | 388x588 | 47 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/angry.webp | 400x606 | 56 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/anxious.webp | 400x606 | 53 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/joy.webp | 400x606 | 58 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/neutral.webp | 400x606 | 53 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/surprise_react.webp | 400x606 | 57 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/760/surprise_talk.webp | 400x606 | 50 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/angry.webp | 582x882 | 106 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/anxious.webp | 582x882 | 101 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/joy.webp | 582x882 | 110 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/neutral.webp | 582x882 | 100 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/surprise_react.webp | 582x882 | 108 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ttadak/840/surprise_talk.webp | 582x882 | 93 KB | resident_ttadak |
| assets/dialogue-source-master/resident_ubak/560/angry.webp | 384x588 | 57 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/560/anxious.webp | 384x588 | 56 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/560/joy.webp | 384x588 | 59 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/560/neutral.webp | 384x588 | 57 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/560/surprise_react.webp | 384x588 | 57 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/560/surprise_talk.webp | 384x588 | 58 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/angry.webp | 400x612 | 61 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/anxious.webp | 400x612 | 59 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/joy.webp | 400x612 | 62 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/neutral.webp | 400x612 | 60 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/surprise_react.webp | 400x612 | 60 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/760/surprise_talk.webp | 400x612 | 61 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/angry.webp | 577x882 | 102 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/anxious.webp | 577x882 | 100 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/joy.webp | 577x882 | 105 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/neutral.webp | 577x882 | 100 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/surprise_react.webp | 577x882 | 102 KB | resident_ubak |
| assets/dialogue-source-master/resident_ubak/840/surprise_talk.webp | 577x882 | 104 KB | resident_ubak |
| assets/dialogue-source-master/seryeon/560/angry.webp | 384x588 | 53 KB | seryeon |
| assets/dialogue-source-master/seryeon/560/anxious.webp | 386x588 | 45 KB | seryeon |
| assets/dialogue-source-master/seryeon/560/joy.webp | 386x588 | 49 KB | seryeon |
| assets/dialogue-source-master/seryeon/560/neutral.webp | 386x588 | 48 KB | seryeon |
| assets/dialogue-source-master/seryeon/560/surprise_react.webp | 384x588 | 51 KB | seryeon |
| assets/dialogue-source-master/seryeon/560/surprise_talk.webp | 386x588 | 48 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/angry.webp | 398x609 | 57 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/anxious.webp | 400x609 | 48 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/joy.webp | 400x609 | 52 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/neutral.webp | 400x609 | 51 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/surprise_react.webp | 398x609 | 54 KB | seryeon |
| assets/dialogue-source-master/seryeon/760/surprise_talk.webp | 400x609 | 51 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/angry.webp | 575x882 | 106 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/anxious.webp | 579x882 | 90 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/joy.webp | 579x882 | 97 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/neutral.webp | 579x882 | 95 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/surprise_react.webp | 577x882 | 101 KB | seryeon |
| assets/dialogue-source-master/seryeon/840/surprise_talk.webp | 579x882 | 96 KB | seryeon |
| assets/doto-room.png | 1672x941 | 1752 KB | doto |
| assets/field-dot-v2/bami/action_1.webp | 135x157 | 5 KB | bami |
| assets/field-dot-v2/bami/action_2.webp | 119x142 | 4 KB | bami |
| assets/field-dot-v2/bami/distressed.webp | 136x109 | 5 KB | bami |
| assets/field-dot-v2/bami/expressive.webp | 218x154 | 6 KB | bami |
| assets/field-dot-v2/bami/neutral.webp | 76x166 | 4 KB | bami |
| assets/field-dot-v2/bami/thinking.webp | 101x166 | 4 KB | bami |
| assets/field-dot-v2/buri/action_1.webp | 71x153 | 4 KB | buri |
| assets/field-dot-v2/buri/action_2.webp | 108x150 | 5 KB | buri |
| assets/field-dot-v2/buri/distressed.webp | 84x185 | 5 KB | buri |
| assets/field-dot-v2/buri/event_toolbox.webp | 99x142 | 4 KB | buri |
| assets/field-dot-v2/buri/expressive.webp | 84x185 | 5 KB | buri |
| assets/field-dot-v2/buri/group_cooperative.webp | 96x186 | 4 KB | buri |
| assets/field-dot-v2/buri/life_sort_tools.webp | 117x185 | 4 KB | buri |
| assets/field-dot-v2/buri/neutral.webp | 96x185 | 4 KB | buri |
| assets/field-dot-v2/buri/thinking.webp | 84x185 | 5 KB | buri |
| assets/field-dot-v2/dad/action_1.webp | 196x175 | 7 KB | dad |
| assets/field-dot-v2/dad/action_2.webp | 186x203 | 8 KB | dad |
| assets/field-dot-v2/dad/breakdown.webp | 157x130 | 5 KB | dad |
| assets/field-dot-v2/dad/distressed.webp | 176x196 | 7 KB | dad |
| assets/field-dot-v2/dad/expressive.webp | 219x195 | 8 KB | dad |
| assets/field-dot-v2/dad/listen_right.webp | 157x208 | 8 KB | dad |
| assets/field-dot-v2/dad/neutral.webp | 163x210 | 8 KB | dad |
| assets/field-dot-v2/dad/protect.webp | 194x185 | 8 KB | dad |
| assets/field-dot-v2/dad/thinking.webp | 189x193 | 7 KB | dad |
| assets/field-dot-v2/daram/action_1.webp | 151x140 | 5 KB | daram |
| assets/field-dot-v2/daram/action_2.webp | 145x152 | 5 KB | daram |
| assets/field-dot-v2/daram/distressed.webp | 131x165 | 5 KB | daram |
| assets/field-dot-v2/daram/expressive.webp | 174x153 | 6 KB | daram |
| assets/field-dot-v2/daram/inspect_floor.webp | 157x124 | 6 KB | daram |
| assets/field-dot-v2/daram/joy.webp | 140x158 | 5 KB | daram |
| assets/field-dot-v2/daram/neutral.webp | 89x165 | 4 KB | daram |
| assets/field-dot-v2/daram/panic.webp | 136x165 | 6 KB | daram |
| assets/field-dot-v2/daram/thinking.webp | 148x159 | 5 KB | daram |
| assets/field-dot-v2/doto/action_1.webp | 91x210 | 5 KB | doto |
| assets/field-dot-v2/doto/action_2.webp | 114x136 | 4 KB | doto |
| assets/field-dot-v2/doto/distressed.webp | 91x210 | 4 KB | doto |
| assets/field-dot-v2/doto/expressive.webp | 91x210 | 4 KB | doto |
| assets/field-dot-v2/doto/map27_compare_ration_slips_v2.webp | 104x211 | 5 KB | doto |
| assets/field-dot-v2/doto/map27_write_ledger_v2.webp | 109x211 | 5 KB | doto |
| assets/field-dot-v2/doto/neutral.webp | 84x211 | 5 KB | doto |
| assets/field-dot-v2/doto/thinking.webp | 91x210 | 4 KB | doto |
| assets/field-dot-v2/granny/distressed.webp | 83x195 | 5 KB | granny |
| assets/field-dot-v2/granny/expressive.webp | 83x195 | 5 KB | granny |
| assets/field-dot-v2/granny/living_keyledger.webp | 95x195 | 5 KB | granny |
| assets/field-dot-v2/granny/neutral.webp | 76x195 | 4 KB | granny |
| assets/field-dot-v2/granny/thinking.webp | 83x195 | 5 KB | granny |
| assets/field-dot-v2/granny/withdraw_hand.webp | 82x181 | 4 KB | granny |
| assets/field-dot-v2/guard/action_1.webp | 130x138 | 4 KB | guard |
| assets/field-dot-v2/guard/action_2.webp | 110x126 | 4 KB | guard |
| assets/field-dot-v2/guard/check_records_low.webp | 128x116 | 4 KB | guard |
| assets/field-dot-v2/guard/distressed.webp | 104x183 | 5 KB | guard |
| assets/field-dot-v2/guard/expressive.webp | 153x129 | 4 KB | guard |
| assets/field-dot-v2/guard/life_lamp_trim.webp | 143x210 | 6 KB | guard |
| assets/field-dot-v2/guard/life_stamp_ledger.webp | 153x210 | 5 KB | guard |
| assets/field-dot-v2/guard/listen_left.webp | 112x161 | 4 KB | guard |
| assets/field-dot-v2/guard/neutral.webp | 115x210 | 7 KB | guard |
| assets/field-dot-v2/guard/panic.webp | 104x164 | 5 KB | guard |
| assets/field-dot-v2/guard/thinking.webp | 124x210 | 6 KB | guard |
| assets/field-dot-v2/karo/action_1.webp | 206x187 | 8 KB | karo |
| assets/field-dot-v2/karo/action_2.webp | 198x200 | 7 KB | karo |
| assets/field-dot-v2/karo/distressed.webp | 204x224 | 7 KB | karo |
| assets/field-dot-v2/karo/expressive.webp | 256x207 | 7 KB | karo |
| assets/field-dot-v2/karo/life_wheel_check.webp | 214x230 | 6 KB | karo |
| assets/field-dot-v2/karo/living_axlewrap.webp | 127x166 | 5 KB | karo |
| assets/field-dot-v2/karo/neutral.webp | 133x230 | 6 KB | karo |
| assets/field-dot-v2/karo/thinking.webp | 149x235 | 7 KB | karo |
| assets/field-dot-v2/kid_bang/cling_leg.webp | 87x165 | 4 KB | kid_bang |
| assets/field-dot-v2/kid_bang/distressed.webp | 94x165 | 5 KB | kid_bang |
| assets/field-dot-v2/kid_bang/expressive.webp | 94x165 | 5 KB | kid_bang |
| assets/field-dot-v2/kid_bang/group_play.webp | 81x165 | 4 KB | kid_bang |
| assets/field-dot-v2/kid_bang/neutral.webp | 94x165 | 5 KB | kid_bang |
| assets/field-dot-v2/kid_bang/thinking.webp | 94x165 | 5 KB | kid_bang |
| assets/field-dot-v2/kid_dodam/distressed.webp | 90x164 | 5 KB | kid_dodam |
| assets/field-dot-v2/kid_dodam/expressive.webp | 90x164 | 5 KB | kid_dodam |
| assets/field-dot-v2/kid_dodam/lick_ladle.webp | 95x165 | 5 KB | kid_dodam |
| assets/field-dot-v2/kid_dodam/neutral.webp | 62x132 | 3 KB | kid_dodam |
| assets/field-dot-v2/kid_dodam/thinking.webp | 90x164 | 5 KB | kid_dodam |
| assets/field-dot-v2/kid_kkam/distressed.webp | 87x165 | 4 KB | kid_kkam |
| assets/field-dot-v2/kid_kkam/expressive.webp | 87x165 | 4 KB | kid_kkam |
| assets/field-dot-v2/kid_kkam/group_play.webp | 111x165 | 4 KB | kid_kkam |
| assets/field-dot-v2/kid_kkam/neutral.webp | 87x165 | 4 KB | kid_kkam |
| assets/field-dot-v2/kid_kkam/thinking.webp | 87x165 | 4 KB | kid_kkam |
| assets/field-dot-v2/kid_kkomi/distressed.webp | 89x165 | 5 KB | kid_kkomi |
| assets/field-dot-v2/kid_kkomi/door_peek.webp | 96x165 | 4 KB | kid_kkomi |
| assets/field-dot-v2/kid_kkomi/expressive.webp | 89x165 | 5 KB | kid_kkomi |
| assets/field-dot-v2/kid_kkomi/hideout_proud.webp | 114x165 | 5 KB | kid_kkomi |
| assets/field-dot-v2/kid_kkomi/neutral.webp | 88x165 | 4 KB | kid_kkomi |
| assets/field-dot-v2/kid_kkomi/thinking.webp | 89x165 | 5 KB | kid_kkomi |
| assets/field-dot-v2/kid_mong/distressed.webp | 94x165 | 5 KB | kid_mong |
| assets/field-dot-v2/kid_mong/expressive.webp | 94x165 | 5 KB | kid_mong |
| assets/field-dot-v2/kid_mong/group_play.webp | 108x165 | 5 KB | kid_mong |
| assets/field-dot-v2/kid_mong/neutral.webp | 94x165 | 5 KB | kid_mong |
| assets/field-dot-v2/kid_mong/thinking.webp | 94x165 | 5 KB | kid_mong |
| assets/field-dot-v2/kid_nubi1/distressed.webp | 84x165 | 4 KB | kid_nubi1 |
| assets/field-dot-v2/kid_nubi1/expressive.webp | 84x165 | 4 KB | kid_nubi1 |
| assets/field-dot-v2/kid_nubi1/hold_skirt.webp | 102x165 | 4 KB | kid_nubi1 |
| assets/field-dot-v2/kid_nubi1/neutral.webp | 84x165 | 4 KB | kid_nubi1 |
| assets/field-dot-v2/kid_nubi1/thinking.webp | 84x165 | 4 KB | kid_nubi1 |
| assets/field-dot-v2/kid_nubi2/distressed.webp | 101x165 | 4 KB | kid_nubi2 |
| assets/field-dot-v2/kid_nubi2/expressive.webp | 101x165 | 4 KB | kid_nubi2 |
| assets/field-dot-v2/kid_nubi2/neutral.webp | 101x165 | 4 KB | kid_nubi2 |
| assets/field-dot-v2/kid_nubi2/thinking.webp | 101x165 | 4 KB | kid_nubi2 |
| assets/field-dot-v2/kid_saemi/distressed.webp | 103x165 | 5 KB | kid_saemi |
| assets/field-dot-v2/kid_saemi/expressive.webp | 103x165 | 5 KB | kid_saemi |
| assets/field-dot-v2/kid_saemi/hide_bowl.webp | 122x165 | 6 KB | kid_saemi |
| assets/field-dot-v2/kid_saemi/neutral.webp | 92x165 | 4 KB | kid_saemi |
| assets/field-dot-v2/kid_saemi/thinking.webp | 103x165 | 5 KB | kid_saemi |
| assets/field-dot-v2/mom/action_1.webp | 179x186 | 9 KB | mom |
| assets/field-dot-v2/mom/action_2.webp | 195x183 | 10 KB | mom |
| assets/field-dot-v2/mom/distressed.webp | 151x208 | 8 KB | mom |
| assets/field-dot-v2/mom/expressive.webp | 222x188 | 9 KB | mom |
| assets/field-dot-v2/mom/neutral.webp | 128x210 | 7 KB | mom |
| assets/field-dot-v2/mom/show_fragments.webp | 137x210 | 7 KB | mom |
| assets/field-dot-v2/mom/thinking.webp | 163x209 | 9 KB | mom |
| assets/field-dot-v2/nabi/action_1.webp | 185x186 | 7 KB | nabi |
| assets/field-dot-v2/nabi/action_2.webp | 173x189 | 6 KB | nabi |
| assets/field-dot-v2/nabi/distressed.webp | 143x196 | 7 KB | nabi |
| assets/field-dot-v2/nabi/expressive.webp | 203x189 | 7 KB | nabi |
| assets/field-dot-v2/nabi/life_ladle_pot.webp | 142x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/map27_ki_1.webp | 131x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/map31_nabi_arrange_tray.webp | 130x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/map31_nabi_ladle_soup.webp | 140x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/map31_nabi_stir_pot.webp | 138x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/map31_nabi_wash_dishes.webp | 142x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/neutral.webp | 102x210 | 6 KB | nabi |
| assets/field-dot-v2/nabi/thinking.webp | 141x214 | 7 KB | nabi |
| assets/field-dot-v2/neoul/distressed.webp | 140x210 | 6 KB | neoul |
| assets/field-dot-v2/neoul/expressive.webp | 140x210 | 6 KB | neoul |
| assets/field-dot-v2/neoul/life_abacus_ledger.webp | 141x210 | 5 KB | neoul |
| assets/field-dot-v2/neoul/map27_fa_1.webp | 140x210 | 7 KB | neoul |
| assets/field-dot-v2/neoul/map27_ga_1.webp | 138x210 | 7 KB | neoul |
| assets/field-dot-v2/neoul/neutral.webp | 129x210 | 7 KB | neoul |
| assets/field-dot-v2/neoul/thinking.webp | 140x210 | 6 KB | neoul |
| assets/field-dot-v2/npc_pandol/distressed.webp | 128x195 | 7 KB | npc_pandol |
| assets/field-dot-v2/npc_pandol/expressive.webp | 128x195 | 7 KB | npc_pandol |
| assets/field-dot-v2/npc_pandol/neutral.webp | 102x195 | 6 KB | npc_pandol |
| assets/field-dot-v2/npc_pandol/point_name.webp | 130x195 | 7 KB | npc_pandol |
| assets/field-dot-v2/npc_pandol/thinking.webp | 128x195 | 7 KB | npc_pandol |
| assets/field-dot-v2/npc_panseol/neutral.webp | 120x211 | 7 KB | npc_panseol |
| assets/field-dot-v2/resident_badook/block_cart.webp | 160x211 | 8 KB | resident_badook |
| assets/field-dot-v2/resident_badook/distressed.webp | 179x211 | 8 KB | resident_badook |
| assets/field-dot-v2/resident_badook/expressive.webp | 227x189 | 8 KB | resident_badook |
| assets/field-dot-v2/resident_badook/life_patrol_day.webp | 134x210 | 5 KB | resident_badook |
| assets/field-dot-v2/resident_badook/living_bootlace.webp | 200x159 | 8 KB | resident_badook |
| assets/field-dot-v2/resident_badook/map27_check_rope.webp | 111x210 | 7 KB | resident_badook |
| assets/field-dot-v2/resident_badook/map27_lantern_patrol.webp | 121x210 | 7 KB | resident_badook |
| assets/field-dot-v2/resident_badook/neutral.webp | 113x210 | 6 KB | resident_badook |
| assets/field-dot-v2/resident_badook/thinking.webp | 153x192 | 6 KB | resident_badook |
| assets/field-dot-v2/resident_bori/distressed.webp | 207x230 | 11 KB | resident_bori |
| assets/field-dot-v2/resident_bori/expressive.webp | 207x230 | 11 KB | resident_bori |
| assets/field-dot-v2/resident_bori/life_chop_wood.webp | 206x230 | 7 KB | resident_bori |
| assets/field-dot-v2/resident_bori/life_stack_wood.webp | 199x230 | 9 KB | resident_bori |
| assets/field-dot-v2/resident_bori/living_firewood.webp | 132x159 | 6 KB | resident_bori |
| assets/field-dot-v2/resident_bori/map27_carry_firewood_v2.webp | 151x230 | 10 KB | resident_bori |
| assets/field-dot-v2/resident_bori/map27_check_own_ration_v2.webp | 155x230 | 10 KB | resident_bori |
| assets/field-dot-v2/resident_bori/neutral.webp | 146x230 | 8 KB | resident_bori |
| assets/field-dot-v2/resident_bori/thinking.webp | 207x230 | 11 KB | resident_bori |
| assets/field-dot-v2/resident_eunho/distressed.webp | 165x186 | 6 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/expressive.webp | 230x203 | 7 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/life_hand_parcel.webp | 132x210 | 5 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/living_prices.webp | 183x200 | 6 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/map27_mk_2.webp | 137x210 | 6 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/neutral.webp | 114x210 | 6 KB | resident_eunho |
| assets/field-dot-v2/resident_eunho/thinking.webp | 173x208 | 6 KB | resident_eunho |
| assets/field-dot-v2/resident_guldol/distressed.webp | 128x231 | 7 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/expressive.webp | 128x231 | 7 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/map27_inspect_stone_clean.webp | 119x230 | 8 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/map27_sort_chisels_clean.webp | 119x231 | 8 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/map9_stone_tapping.webp | 115x221 | 6 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/neutral.webp | 108x230 | 7 KB | resident_guldol |
| assets/field-dot-v2/resident_guldol/thinking.webp | 128x231 | 7 KB | resident_guldol |
| assets/field-dot-v2/resident_kongi/activity.webp | 141x131 | 5 KB | resident_kongi |
| assets/field-dot-v2/resident_kongi/distressed.webp | 131x133 | 4 KB | resident_kongi |
| assets/field-dot-v2/resident_kongi/expressive.webp | 136x148 | 5 KB | resident_kongi |
| assets/field-dot-v2/resident_kongi/life_peek_listen.webp | 120x165 | 4 KB | resident_kongi |
| assets/field-dot-v2/resident_kongi/neutral.webp | 85x165 | 4 KB | resident_kongi |
| assets/field-dot-v2/resident_kongi/thinking.webp | 106x150 | 4 KB | resident_kongi |
| assets/field-dot-v2/resident_lamplighter/distressed.webp | 100x211 | 5 KB | resident_lamplighter |
| assets/field-dot-v2/resident_lamplighter/expressive.webp | 123x211 | 5 KB | resident_lamplighter |
| assets/field-dot-v2/resident_lamplighter/job_replace_lightstone.webp | 106x210 | 6 KB | resident_lamplighter |
| assets/field-dot-v2/resident_lamplighter/living_inspectlamp.webp | 101x211 | 6 KB | resident_lamplighter |
| assets/field-dot-v2/resident_lamplighter/neutral.webp | 88x210 | 5 KB | resident_lamplighter |
| assets/field-dot-v2/resident_lamplighter/thinking.webp | 101x211 | 6 KB | resident_lamplighter |
| assets/field-dot-v2/resident_madam/distressed.webp | 102x210 | 6 KB | resident_madam |
| assets/field-dot-v2/resident_madam/expressive.webp | 102x210 | 6 KB | resident_madam |
| assets/field-dot-v2/resident_madam/life_pick_goods.webp | 107x209 | 5 KB | resident_madam |
| assets/field-dot-v2/resident_madam/life_tap_ledger.webp | 117x209 | 5 KB | resident_madam |
| assets/field-dot-v2/resident_madam/neutral.webp | 100x209 | 5 KB | resident_madam |
| assets/field-dot-v2/resident_madam/thinking.webp | 102x210 | 6 KB | resident_madam |
| assets/field-dot-v2/resident_momo/distressed.webp | 102x210 | 6 KB | resident_momo |
| assets/field-dot-v2/resident_momo/expressive.webp | 102x210 | 6 KB | resident_momo |
| assets/field-dot-v2/resident_momo/living_lampnumber.webp | 96x210 | 6 KB | resident_momo |
| assets/field-dot-v2/resident_momo/neutral.webp | 120x210 | 6 KB | resident_momo |
| assets/field-dot-v2/resident_momo/thinking.webp | 102x210 | 6 KB | resident_momo |
| assets/field-dot-v2/resident_musoe/distressed.webp | 124x231 | 7 KB | resident_musoe |
| assets/field-dot-v2/resident_musoe/expressive.webp | 150x231 | 8 KB | resident_musoe |
| assets/field-dot-v2/resident_musoe/job_inspect_old_tool.webp | 122x230 | 8 KB | resident_musoe |
| assets/field-dot-v2/resident_musoe/living_foldmap.webp | 132x231 | 8 KB | resident_musoe |
| assets/field-dot-v2/resident_musoe/neutral.webp | 139x231 | 8 KB | resident_musoe |
| assets/field-dot-v2/resident_musoe/thinking.webp | 123x231 | 7 KB | resident_musoe |
| assets/field-dot-v2/resident_nero/activity.webp | 185x191 | 6 KB | resident_nero |
| assets/field-dot-v2/resident_nero/distressed.webp | 193x175 | 7 KB | resident_nero |
| assets/field-dot-v2/resident_nero/expressive.webp | 207x201 | 7 KB | resident_nero |
| assets/field-dot-v2/resident_nero/life_carry_bucket.webp | 133x210 | 5 KB | resident_nero |
| assets/field-dot-v2/resident_nero/life_wait_hands_pocket.webp | 112x210 | 5 KB | resident_nero |
| assets/field-dot-v2/resident_nero/neutral.webp | 115x210 | 6 KB | resident_nero |
| assets/field-dot-v2/resident_nero/thinking.webp | 159x209 | 6 KB | resident_nero |
| assets/field-dot-v2/resident_nubi/distressed.webp | 116x211 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/expressive.webp | 116x211 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/life_fold_linen.webp | 136x210 | 5 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/life_hold_bundle.webp | 107x210 | 5 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/map27_in_1.webp | 109x209 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/map27_mk_4.webp | 120x210 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/map9_inn_sort_tie_laundry.webp | 125x199 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/neutral.webp | 108x210 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_nubi/thinking.webp | 116x211 | 6 KB | resident_nubi |
| assets/field-dot-v2/resident_owlgp/distressed.webp | 92x195 | 5 KB | resident_owlgp |
| assets/field-dot-v2/resident_owlgp/expressive.webp | 92x195 | 5 KB | resident_owlgp |
| assets/field-dot-v2/resident_owlgp/living_notebook.webp | 93x152 | 4 KB | resident_owlgp |
| assets/field-dot-v2/resident_owlgp/neutral.webp | 82x195 | 5 KB | resident_owlgp |
| assets/field-dot-v2/resident_owlgp/thinking.webp | 92x195 | 5 KB | resident_owlgp |
| assets/field-dot-v2/resident_piko/distressed.webp | 113x210 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/expressive.webp | 113x210 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/map27_cl_1.webp | 110x169 | 5 KB | resident_piko |
| assets/field-dot-v2/resident_piko/map27_mix_paint_v2.webp | 114x211 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/map27_paint_sketchboard_v2.webp | 112x211 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/map27_sq_2.webp | 92x210 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/map9_clinic_rest_alive_v2.webp | 317x116 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/neutral.webp | 94x210 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_piko/thinking.webp | 113x210 | 6 KB | resident_piko |
| assets/field-dot-v2/resident_ppul/activity.webp | 215x190 | 7 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/distressed.webp | 148x203 | 7 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/expressive.webp | 181x196 | 7 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/kneel_stone.webp | 142x210 | 7 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/life_count_knots.webp | 97x210 | 5 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/life_pin_notice.webp | 106x210 | 4 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/neutral.webp | 83x210 | 5 KB | resident_ppul |
| assets/field-dot-v2/resident_ppul/thinking.webp | 123x209 | 7 KB | resident_ppul |
| assets/field-dot-v2/resident_seori/distressed.webp | 129x192 | 6 KB | resident_seori |
| assets/field-dot-v2/resident_seori/expressive.webp | 159x197 | 7 KB | resident_seori |
| assets/field-dot-v2/resident_seori/inspect_paper_threequarter_front.webp | 101x210 | 7 KB | resident_seori |
| assets/field-dot-v2/resident_seori/life_write_desk_seated.webp | 134x210 | 7 KB | resident_seori |
| assets/field-dot-v2/resident_seori/living_notes.webp | 134x198 | 6 KB | resident_seori |
| assets/field-dot-v2/resident_seori/neutral.webp | 87x210 | 6 KB | resident_seori |
| assets/field-dot-v2/resident_seori/thinking.webp | 141x205 | 7 KB | resident_seori |
| assets/field-dot-v2/resident_siluk/distressed.webp | 91x210 | 5 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/event_whisper.webp | 121x204 | 6 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/expressive.webp | 91x210 | 5 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/life_carry_sack.webp | 139x209 | 7 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/map27_st_2.webp | 97x210 | 5 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/neutral.webp | 96x209 | 6 KB | resident_siluk |
| assets/field-dot-v2/resident_siluk/thinking.webp | 91x210 | 5 KB | resident_siluk |
| assets/field-dot-v2/resident_sling/activity.webp | 208x165 | 7 KB | resident_sling |
| assets/field-dot-v2/resident_sling/distressed.webp | 157x193 | 6 KB | resident_sling |
| assets/field-dot-v2/resident_sling/event_steam.webp | 149x198 | 7 KB | resident_sling |
| assets/field-dot-v2/resident_sling/expressive.webp | 184x196 | 7 KB | resident_sling |
| assets/field-dot-v2/resident_sling/life_write_letter_standing.webp | 130x211 | 5 KB | resident_sling |
| assets/field-dot-v2/resident_sling/map27_po_1.webp | 141x209 | 7 KB | resident_sling |
| assets/field-dot-v2/resident_sling/neutral.webp | 129x211 | 6 KB | resident_sling |
| assets/field-dot-v2/resident_sling/thinking.webp | 152x209 | 7 KB | resident_sling |
| assets/field-dot-v2/resident_somi/distressed.webp | 117x160 | 5 KB | resident_somi |
| assets/field-dot-v2/resident_somi/expressive.webp | 182x157 | 6 KB | resident_somi |
| assets/field-dot-v2/resident_somi/living_bootice.webp | 146x129 | 5 KB | resident_somi |
| assets/field-dot-v2/resident_somi/neutral.webp | 93x165 | 4 KB | resident_somi |
| assets/field-dot-v2/resident_somi/thinking.webp | 143x146 | 5 KB | resident_somi |
| assets/field-dot-v2/resident_teacher/distressed.webp | 144x230 | 8 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/expressive.webp | 144x230 | 8 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/life_chalk_board.webp | 157x230 | 6 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/map27_sc_1.webp | 147x231 | 8 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/map9_school_spread_wet_coat.webp | 147x221 | 7 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/neutral.webp | 143x230 | 8 KB | resident_teacher |
| assets/field-dot-v2/resident_teacher/thinking.webp | 144x230 | 8 KB | resident_teacher |
| assets/field-dot-v2/resident_tok/activity.webp | 175x186 | 8 KB | resident_tok |
| assets/field-dot-v2/resident_tok/distressed.webp | 161x204 | 7 KB | resident_tok |
| assets/field-dot-v2/resident_tok/expressive.webp | 187x205 | 8 KB | resident_tok |
| assets/field-dot-v2/resident_tok/group_cooperative.webp | 141x210 | 7 KB | resident_tok |
| assets/field-dot-v2/resident_tok/life_fix_stove.webp | 181x209 | 7 KB | resident_tok |
| assets/field-dot-v2/resident_tok/map27_di_1a.webp | 114x151 | 5 KB | resident_tok |
| assets/field-dot-v2/resident_tok/map27_ws_1.webp | 131x210 | 7 KB | resident_tok |
| assets/field-dot-v2/resident_tok/neutral.webp | 95x209 | 5 KB | resident_tok |
| assets/field-dot-v2/resident_tok/thinking.webp | 146x199 | 7 KB | resident_tok |
| assets/field-dot-v2/resident_tosil/distressed.webp | 82x165 | 4 KB | resident_tosil |
| assets/field-dot-v2/resident_tosil/expressive.webp | 82x165 | 4 KB | resident_tosil |
| assets/field-dot-v2/resident_tosil/hold_storybook.webp | 59x129 | 2 KB | resident_tosil |
| assets/field-dot-v2/resident_tosil/living_thermos.webp | 82x165 | 3 KB | resident_tosil |
| assets/field-dot-v2/resident_tosil/neutral.webp | 70x165 | 3 KB | resident_tosil |
| assets/field-dot-v2/resident_tosil/thinking.webp | 82x165 | 4 KB | resident_tosil |
| assets/field-dot-v2/resident_ttadak/distressed.webp | 160x198 | 7 KB | resident_ttadak |
| assets/field-dot-v2/resident_ttadak/expressive.webp | 198x199 | 8 KB | resident_ttadak |
| assets/field-dot-v2/resident_ttadak/living_doorframe.webp | 146x210 | 5 KB | resident_ttadak |
| assets/field-dot-v2/resident_ttadak/living_repair.webp | 182x193 | 7 KB | resident_ttadak |
| assets/field-dot-v2/resident_ttadak/neutral.webp | 120x209 | 6 KB | resident_ttadak |
| assets/field-dot-v2/resident_ttadak/thinking.webp | 173x191 | 6 KB | resident_ttadak |
| assets/field-dot-v2/resident_ubak/distressed.webp | 181x208 | 8 KB | resident_ubak |
| assets/field-dot-v2/resident_ubak/expressive.webp | 177x215 | 8 KB | resident_ubak |
| assets/field-dot-v2/resident_ubak/living_measure.webp | 191x180 | 8 KB | resident_ubak |
| assets/field-dot-v2/resident_ubak/neutral.webp | 101x210 | 6 KB | resident_ubak |
| assets/field-dot-v2/resident_ubak/thinking.webp | 191x197 | 7 KB | resident_ubak |
| assets/field-dot-v2/seryeon/action_1.webp | 164x196 | 6 KB | seryeon |
| assets/field-dot-v2/seryeon/action_2.webp | 183x192 | 7 KB | seryeon |
| assets/field-dot-v2/seryeon/chair_listen.webp | 180x210 | 7 KB | seryeon |
| assets/field-dot-v2/seryeon/chair_read.webp | 177x210 | 7 KB | seryeon |
| assets/field-dot-v2/seryeon/distressed.webp | 134x208 | 6 KB | seryeon |
| assets/field-dot-v2/seryeon/expressive.webp | 204x197 | 7 KB | seryeon |
| assets/field-dot-v2/seryeon/life_stamp_ledger.webp | 118x210 | 4 KB | seryeon |
| assets/field-dot-v2/seryeon/neutral.webp | 108x210 | 5 KB | seryeon |
| assets/field-dot-v2/seryeon/thinking.webp | 126x211 | 6 KB | seryeon |
| assets/field-dot-v2/v111_child/neutral.webp | 91x165 | 4 KB | v111_child |
| assets/field-dot-v2/v111_lowerroad_elder/neutral.webp | 92x195 | 6 KB | v111_lowerroad_elder |
| assets/field-dot-v2/v111_patrol/neutral.webp | 114x210 | 6 KB | v111_patrol |
| assets/field-dot-v2/v111_resident/neutral.webp | 96x210 | 6 KB | v111_resident |
| assets/front.png | 2048x768 | 1399 KB | bami; bodum; buri; chorong_mother; dad; daram; doto; elder |
| assets/investigation-canonical-20261018/doto--map27_compare_ration_slips_v2.webp | 1024x1536 | 853 KB | doto |
| assets/investigation-canonical-20261018/doto--map27_write_ledger_v2.webp | 1024x1536 | 854 KB | doto |
| assets/investigation-canonical-20261018/resident_lamplighter--distressed.webp | 1024x1536 | 913 KB | resident_lamplighter |
| assets/investigation-canonical-20261018/resident_lamplighter--expressive.webp | 1024x1536 | 920 KB | resident_lamplighter |
| assets/investigation-canonical-20261018/resident_lamplighter--neutral.webp | 1024x1536 | 872 KB | resident_lamplighter |
| assets/investigation-canonical-20261018/resident_lamplighter--thinking.webp | 1024x1536 | 887 KB | resident_lamplighter |
| assets/investigation-canonical-20261018/resident_musoe--distressed.webp | 1024x1536 | 962 KB | resident_musoe |
| assets/investigation-canonical-20261018/resident_musoe--expressive.webp | 1024x1536 | 1001 KB | resident_musoe |
| assets/investigation-canonical-20261018/resident_musoe--neutral.webp | 1024x1536 | 963 KB | resident_musoe |
| assets/investigation-canonical-20261018/resident_musoe--thinking.webp | 1024x1536 | 937 KB | resident_musoe |
| assets/investigation-canonical-20261018/resident_piko--map27_mix_paint_v2.webp | 1024x1536 | 1022 KB | resident_piko |
| assets/investigation-canonical-20261018/resident_piko--map27_paint_sketchboard_v2.webp | 1024x1536 | 966 KB | resident_piko |
| assets/investigation-source2/tosil-thermos-v1.webp | 1024x1536 | 968 KB | resident_tosil |
| assets/investigation-source2/ttadak-doorframe-v1.webp | 1024x1536 | 969 KB | resident_ttadak |
| assets/lowerroad-elder/v111_lowerroad_elder-angry.webp | 1024x1536 | 586 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder-anxious.webp | 1024x1536 | 614 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder-flustered.webp | 1024x1536 | 608 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder-joy.webp | 1024x1536 | 605 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder-neutral.webp | 1024x1536 | 612 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder-surprise.webp | 1024x1536 | 604 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder_face-noborder.webp | 555x555 | 206 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder_face.webp | 555x555 | 273 KB | v111_lowerroad_elder |
| assets/lowerroad-elder/v111_lowerroad_elder_fullbody.webp | 1024x1536 | 1085 KB | v111_lowerroad_elder |
| assets/map-action27/CL-1--resident_piko.webp | 512x768 | 87 KB | resident_piko |
| assets/map-action27/DI-1a--resident_tok.webp | 742x768 | 111 KB | resident_tok |
| assets/map-action27/FA-1--neoul.webp | 512x768 | 90 KB | neoul |
| assets/map-action27/GA-1--neoul.webp | 512x768 | 93 KB | neoul |
| assets/map-action27/IN-1--resident_nubi.webp | 512x768 | 77 KB | resident_nubi |
| assets/map-action27/KI-1--nabi.webp | 516x768 | 86 KB | nabi |
| assets/map-action27/KI-2--nabi.webp | 512x768 | 84 KB | nabi |
| assets/map-action27/KI-3--nabi.webp | 516x768 | 86 KB | nabi |
| assets/map-action27/KI-4--nabi.webp | 516x768 | 83 KB | nabi |
| assets/map-action27/KI-5--nabi.webp | 512x768 | 86 KB | nabi |
| assets/map-action27/MK-2--resident_eunho.webp | 512x768 | 83 KB | resident_eunho |
| assets/map-action27/MK-4--resident_nubi.webp | 512x768 | 87 KB | resident_nubi |
| assets/map-action27/PO-1--resident_sling.webp | 512x768 | 87 KB | resident_sling |
| assets/map-action27/SC-1--resident_teacher.webp | 482x768 | 98 KB | resident_teacher |
| assets/map-action27/SQ-2--resident_piko.webp | 512x768 | 70 KB | resident_piko |
| assets/map-action27/ST-2--resident_siluk.webp | 512x768 | 68 KB | resident_siluk |
| assets/map-action27/VA-1--resident_badook.webp | 516x768 | 92 KB | resident_badook |
| assets/map-action27/VA-10--doto.webp | 504x768 | 92 KB | doto |
| assets/map-action27/VA-2--resident_piko.webp | 498x768 | 103 KB | resident_piko |
| assets/map-action27/VA-3--resident_piko.webp | 498x768 | 96 KB | resident_piko |
| assets/map-action27/VA-4--resident_guldol.webp | 512x768 | 89 KB | resident_guldol |
| assets/map-action27/VA-5--resident_guldol.webp | 512x768 | 93 KB | resident_guldol |
| assets/map-action27/VA-6--resident_badook.webp | 516x768 | 90 KB | resident_badook |
| assets/map-action27/VA-7--resident_bori.webp | 578x768 | 134 KB | resident_bori |
| assets/map-action27/VA-8--resident_bori.webp | 578x768 | 135 KB | resident_bori |
| assets/map-action27/VA-9--doto.webp | 506x768 | 91 KB | doto |
| assets/map-action27/WS-1--resident_tok.webp | 512x768 | 91 KB | resident_tok |
| assets/map-work-nine/resident_guldol--stone_tapping.webp | 1024x1536 | 706 KB | resident_guldol |
| assets/map-work-nine/resident_nubi--inn_sort_tie_laundry.webp | 996x1578 | 772 KB | resident_nubi |
| assets/map-work-nine/resident_piko--clinic_rest_alive_v2.webp | 1774x887 | 512 KB | resident_piko |
| assets/map-work-nine/resident_teacher--school_spread_wet_coat.webp | 1004x1567 | 875 KB | resident_teacher |
| assets/map.png | 512x288 | 370 KB | bami; buri; dad; daram; doto; granny; guard; karo |
| assets/meeting-source-master/buri--measured_interject.webp | 397x840 | 215 KB | buri |
| assets/meeting-source-master/granny--composed_answer.webp | 524x840 | 229 KB | granny |
| assets/meeting-source-master/nabi--witness_hesitate.webp | 462x840 | 216 KB | nabi |
| assets/meeting-source-master/resident_ppul--stern_statement.webp | 566x840 | 262 KB | resident_ppul |
| assets/meeting-source-master/resident_seori--evidence_check.webp | 554x840 | 195 KB | resident_seori |
| assets/meeting-source-master/seryeon--confident_report.webp | 551x840 | 243 KB | seryeon |
| assets/meeting-stand/buri.webp | 131x197 | 5 KB | buri |
| assets/meeting-stand/doto.webp | 150x226 | 6 KB | doto |
| assets/meeting-stand/granny.webp | 134x201 | 4 KB | granny |
| assets/meeting-stand/nabi.webp | 144x216 | 6 KB | nabi |
| assets/meeting-stand/resident_bori.webp | 160x240 | 5 KB | resident_bori |
| assets/profile-source-master/bami.webp | 256x256 | 48 KB | bami |
| assets/profile-source-master/buri.webp | 256x256 | 49 KB | buri |
| assets/profile-source-master/daram.webp | 256x256 | 54 KB | daram |
| assets/profile-source-master/doto.webp | 256x256 | 49 KB | doto |
| assets/profile-source-master/granny.webp | 256x256 | 53 KB | granny |
| assets/profile-source-master/guard.webp | 256x256 | 55 KB | guard |
| assets/profile-source-master/karo.webp | 256x256 | 49 KB | karo |
| assets/profile-source-master/kid_bang.webp | 256x256 | 49 KB | kid_bang |
| assets/profile-source-master/kid_dodam.webp | 256x256 | 52 KB | kid_dodam |
| assets/profile-source-master/kid_kkam.webp | 256x256 | 45 KB | kid_kkam |
| assets/profile-source-master/kid_kkomi.webp | 256x256 | 50 KB | kid_kkomi |
| assets/profile-source-master/kid_mong.webp | 256x256 | 58 KB | kid_mong |
| assets/profile-source-master/kid_nubi1.webp | 256x256 | 44 KB | kid_nubi1 |
| assets/profile-source-master/kid_nubi2.webp | 256x256 | 43 KB | kid_nubi2 |
| assets/profile-source-master/kid_saemi.webp | 256x256 | 53 KB | kid_saemi |
| assets/profile-source-master/mom.webp | 256x256 | 57 KB | mom |
| assets/profile-source-master/nabi.webp | 256x256 | 51 KB | nabi |
| assets/profile-source-master/neoul.webp | 256x256 | 59 KB | neoul |
| assets/profile-source-master/npc_pandol.webp | 256x256 | 57 KB | npc_pandol |
| assets/profile-source-master/resident_badook.webp | 256x256 | 53 KB | resident_badook |
| assets/profile-source-master/resident_bori.webp | 256x256 | 51 KB | resident_bori |
| assets/profile-source-master/resident_eunho.webp | 256x256 | 49 KB | resident_eunho |
| assets/profile-source-master/resident_guldol.webp | 256x256 | 50 KB | resident_guldol |
| assets/profile-source-master/resident_kongi.webp | 256x256 | 52 KB | resident_kongi |
| assets/profile-source-master/resident_lamplighter.webp | 256x256 | 47 KB | resident_lamplighter |
| assets/profile-source-master/resident_madam.webp | 256x256 | 61 KB | resident_madam |
| assets/profile-source-master/resident_momo.webp | 256x256 | 51 KB | resident_momo |
| assets/profile-source-master/resident_musoe.webp | 256x256 | 58 KB | resident_musoe |
| assets/profile-source-master/resident_nero.webp | 256x256 | 47 KB | resident_nero |
| assets/profile-source-master/resident_nubi.webp | 256x256 | 52 KB | resident_nubi |
| assets/profile-source-master/resident_owlgp.webp | 256x256 | 56 KB | resident_owlgp |
| assets/profile-source-master/resident_piko.webp | 256x256 | 60 KB | resident_piko |
| assets/profile-source-master/resident_ppul.webp | 256x256 | 60 KB | resident_ppul |
| assets/profile-source-master/resident_seori.webp | 256x256 | 52 KB | resident_seori |
| assets/profile-source-master/resident_siluk.webp | 256x256 | 50 KB | resident_siluk |
| assets/profile-source-master/resident_sling.webp | 256x256 | 50 KB | resident_sling |
| assets/profile-source-master/resident_somi.webp | 256x256 | 52 KB | resident_somi |
| assets/profile-source-master/resident_teacher.webp | 256x256 | 61 KB | resident_teacher |
| assets/profile-source-master/resident_tok.webp | 256x256 | 52 KB | resident_tok |
| assets/profile-source-master/resident_tosil.webp | 256x256 | 42 KB | resident_tosil |
| assets/profile-source-master/resident_ttadak.webp | 256x256 | 46 KB | resident_ttadak |
| assets/profile-source-master/resident_ubak.webp | 256x256 | 53 KB | resident_ubak |
| assets/profile-source-master/seryeon.webp | 256x256 | 55 KB | seryeon |
| assets/resident-a-20261024/resident_teacher/write_attendance/approved.webp | 1123x1549 | 994 KB | resident_teacher |
| assets/resident-a-20261024/seryeon/chair_read/approved.webp | 1030x1693 | 907 KB | seryeon |
| assets/resident-poses-a/bami-seated-writing-noborder.webp | 1167x1173 | 560 KB | bami |
| assets/resident-poses-a/bami-seated-writing.webp | 1167x1173 | 209 KB | bami |
| assets/resident-poses-a/buri-event-toolbox-noborder.webp | 990x1430 | 689 KB | buri |
| assets/resident-poses-a/buri-event-toolbox.webp | 990x1430 | 237 KB | buri |
| assets/resident-poses-a/doto-compare-ration-slips-noborder.webp | 781x1495 | 540 KB | doto |
| assets/resident-poses-a/doto-compare-ration-slips.webp | 781x1495 | 213 KB | doto |
| assets/resident-poses-a/doto-write-ledger-noborder.webp | 820x1526 | 600 KB | doto |
| assets/resident-poses-a/doto-write-ledger.webp | 820x1526 | 241 KB | doto |
| assets/resident-poses-a/granny-keyledger-noborder.webp | 773x1529 | 556 KB | granny |
| assets/resident-poses-a/granny-keyledger.webp | 773x1529 | 201 KB | granny |
| assets/resident-poses-a/karo-axlewrap-noborder.webp | 1037x1393 | 705 KB | karo |
| assets/resident-poses-a/karo-axlewrap.webp | 1037x1393 | 276 KB | karo |
| assets/resident-poses-a/nabi-slice-carrot-noborder.webp | 992x1530 | 567 KB | nabi |
| assets/resident-poses-a/nabi-slice-carrot.webp | 992x1530 | 228 KB | nabi |
| assets/resident-poses-a/neoul-point-documents-noborder.webp | 1013x1516 | 643 KB | neoul |
| assets/resident-poses-a/neoul-point-documents.webp | 1013x1516 | 235 KB | neoul |
| assets/resident-poses-a/seryeon-meeting-seated-noborder.webp | 973x1407 | 626 KB | seryeon |
| assets/resident-poses-a/seryeon-meeting-seated.webp | 973x1407 | 224 KB | seryeon |
| assets/resident_badook-body.png | 158x182 | 11 KB | resident_badook; residents |
| assets/resident_badook-face.png | 192x192 | 11 KB | resident_badook; residents |
| assets/resident_bori-body.png | 110x182 | 12 KB | resident_bori; residents |
| assets/resident_bori-face.png | 192x192 | 11 KB | resident_bori; residents |
| assets/resident_eunho-body.png | 192x182 | 16 KB | resident_eunho; residents |
| assets/resident_eunho-face.png | 192x192 | 12 KB | resident_eunho; residents |
| assets/resident_kongi-body.png | 178x182 | 15 KB | resident_kongi; residents |
| assets/resident_kongi-face.png | 192x192 | 11 KB | resident_kongi; residents |
| assets/resident_lamplighter-body.png | 154x182 | 11 KB | resident_lamplighter; residents |
| assets/resident_lamplighter-face.png | 192x192 | 8 KB | resident_lamplighter; residents |
| assets/resident_madam-body.png | 98x182 | 7 KB | resident_madam; residents |
| assets/resident_madam-face.png | 192x192 | 10 KB | resident_madam; residents |
| assets/resident_momo-body.png | 154x182 | 16 KB | resident_momo; residents |
| assets/resident_momo-face.png | 192x192 | 16 KB | resident_momo; residents |
| assets/resident_musoe-body.png | 142x182 | 13 KB | resident_musoe; residents |
| assets/resident_musoe-face.png | 192x192 | 11 KB | resident_musoe; residents |
| assets/resident_nero-body.png | 120x182 | 10 KB | resident_nero; residents |
| assets/resident_nero-face.png | 192x192 | 12 KB | resident_nero; residents |
| assets/resident_nubi-body.png | 154x182 | 14 KB | resident_nubi; residents |
| assets/resident_nubi-face.png | 192x192 | 11 KB | resident_nubi; residents |
| assets/resident_owlgp-body.png | 144x182 | 17 KB | resident_owlgp; residents |
| assets/resident_owlgp-face.png | 192x192 | 17 KB | resident_owlgp; residents |
| assets/resident_piko-body.png | 184x182 | 13 KB | resident_piko; residents |
| assets/resident_piko-face.png | 192x192 | 9 KB | resident_piko; residents |
| assets/resident_ppul-body.png | 128x182 | 14 KB | resident_ppul; residents |
| assets/resident_ppul-face.png | 192x192 | 16 KB | resident_ppul; residents |
| assets/resident_seori-body.png | 104x182 | 11 KB | resident_seori; residents |
| assets/resident_seori-face.png | 192x192 | 12 KB | resident_seori; residents |
| assets/resident_siluk-body.png | 198x182 | 12 KB | resident_siluk; residents |
| assets/resident_siluk-face.png | 192x192 | 13 KB | resident_siluk; residents |
| assets/resident_sling-body.png | 214x182 | 13 KB | resident_sling; residents |
| assets/resident_sling-face.png | 192x192 | 12 KB | resident_sling; residents |
| assets/resident_somi-body.png | 214x182 | 18 KB | resident_somi; residents |
| assets/resident_somi-face.png | 192x192 | 10 KB | resident_somi; residents |
| assets/resident_tok-body.png | 116x183 | 15 KB | resident_tok; residents |
| assets/resident_tok-face.png | 192x192 | 11 KB | resident_tok; residents |
| assets/resident_ttadak-body.png | 104x182 | 11 KB | resident_ttadak; residents |
| assets/resident_ttadak-face.png | 192x192 | 10 KB | resident_ttadak; residents |
| assets/resident_ubak-body.png | 102x182 | 9 KB | resident_ubak; residents |
| assets/resident_ubak-face.png | 192x192 | 13 KB | resident_ubak; residents |
| assets/room13-action-buri-action_1.webp | 512x768 | 150 KB | buri |
| assets/room13-action-buri-action_2.webp | 512x768 | 180 KB | buri |
| assets/room13-action-buri-event_toolbox.webp | 512x768 | 181 KB | buri |
| assets/room13-action-granny-living_keyledger.webp | 512x768 | 188 KB | granny |
| assets/room13-action-karo-living_axlewrap.webp | 512x768 | 94 KB | karo |
| assets/room13-action-resident_bori-living_firewood.webp | 512x768 | 80 KB | resident_bori |
| assets/room13-action-resident_momo-living_lampnumber.webp | 512x768 | 70 KB | resident_momo |
| assets/room13-action-resident_owlgp-living_notebook.webp | 512x768 | 87 KB | resident_owlgp |
| assets/room13-action-resident_piko-event_paintwipe.webp | 512x768 | 71 KB | resident_piko |
| assets/room13-action-resident_siluk-event_whisper.webp | 512x768 | 62 KB | resident_siluk |
| assets/room13-action-resident_sling-event_steam.webp | 512x768 | 63 KB | resident_sling |
| assets/room13-action-resident_tosil-living_thermos.webp | 512x768 | 140 KB | resident_tosil |
| assets/room13-action-resident_ttadak-living_doorframe.webp | 512x768 | 64 KB | resident_ttadak |
| assets/room13-canonical-default-neoul.webp | 512x750 | 70 KB | neoul |
| assets/room13-canonical-default-resident_bori.webp | 605x650 | 88 KB | resident_bori |
| assets/room13-canonical-default-resident_momo.webp | 502x768 | 71 KB | resident_momo |
| assets/room13-canonical-default-resident_teacher.webp | 492x768 | 86 KB | resident_teacher |
| assets/room13-canonical-default-resident_tosil.webp | 470x756 | 62 KB | resident_tosil |
| assets/room13-epart-neoul-neutral.webp | 512x768 | 69 KB | neoul |
| assets/room13-epart-resident_teacher-neutral.webp | 512x768 | 100 KB | resident_teacher |
| assets/room13-face-kid_bang.webp | 384x384 | 39 KB | kid_bang |
| assets/room13-face-kid_dodam.webp | 384x384 | 35 KB | kid_dodam |
| assets/room13-face-kid_kkam.webp | 384x384 | 36 KB | kid_kkam |
| assets/room13-face-kid_kkomi.webp | 384x384 | 42 KB | kid_kkomi |
| assets/room13-face-kid_mong.webp | 384x384 | 48 KB | kid_mong |
| assets/room13-face-kid_nubi1.webp | 384x384 | 39 KB | kid_nubi1 |
| assets/room13-face-kid_saemi.webp | 384x384 | 40 KB | kid_saemi |
| assets/room13-fullbody-bami-angry-acting.webp | 226x340 | 17 KB | bami |
| assets/room13-fullbody-bami-angry.webp | 512x768 | 81 KB | bami |
| assets/room13-fullbody-bami-anxious-acting.webp | 226x340 | 18 KB | bami |
| assets/room13-fullbody-bami-anxious.webp | 512x768 | 74 KB | bami |
| assets/room13-fullbody-bami-flustered-acting.webp | 226x340 | 15 KB | bami |
| assets/room13-fullbody-bami-flustered.webp | 512x768 | 84 KB | bami |
| assets/room13-fullbody-bami-joy-acting.webp | 226x340 | 18 KB | bami |
| assets/room13-fullbody-bami-joy.webp | 512x768 | 73 KB | bami |
| assets/room13-fullbody-bami-neutral-acting.webp | 226x340 | 18 KB | bami |
| assets/room13-fullbody-bami-neutral.webp | 512x768 | 69 KB | bami |
| assets/room13-fullbody-bami-surprise-acting.webp | 226x340 | 18 KB | bami |
| assets/room13-fullbody-bami-surprise.webp | 512x768 | 81 KB | bami |
| assets/room13-fullbody-bami-thinking-acting.webp | 226x340 | 18 KB | bami |
| assets/room13-fullbody-buri-angry.webp | 662x594 | 57 KB | buri |
| assets/room13-fullbody-buri-anxious.webp | 662x594 | 58 KB | buri |
| assets/room13-fullbody-buri-flustered.webp | 662x594 | 58 KB | buri |
| assets/room13-fullbody-buri-joy.webp | 662x594 | 57 KB | buri |
| assets/room13-fullbody-buri-neutral.webp | 662x594 | 55 KB | buri |
| assets/room13-fullbody-buri-surprise.webp | 662x594 | 56 KB | buri |
| assets/room13-fullbody-dad-angry-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-angry.webp | 512x768 | 68 KB | dad |
| assets/room13-fullbody-dad-anxious-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-anxious.webp | 512x768 | 68 KB | dad |
| assets/room13-fullbody-dad-flustered-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-flustered.webp | 512x768 | 67 KB | dad |
| assets/room13-fullbody-dad-joy-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-joy.webp | 512x768 | 69 KB | dad |
| assets/room13-fullbody-dad-neutral-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-neutral.webp | 512x768 | 67 KB | dad |
| assets/room13-fullbody-dad-surprise-acting.webp | 302x448 | 28 KB | dad |
| assets/room13-fullbody-dad-surprise.webp | 512x768 | 68 KB | dad |
| assets/room13-fullbody-daram-angry-acting.webp | 288x416 | 23 KB | daram |
| assets/room13-fullbody-daram-angry.webp | 512x768 | 72 KB | daram |
| assets/room13-fullbody-daram-anxious-acting.webp | 254x384 | 22 KB | daram |
| assets/room13-fullbody-daram-anxious.webp | 512x768 | 73 KB | daram |
| assets/room13-fullbody-daram-flustered-acting.webp | 288x416 | 23 KB | daram |
| assets/room13-fullbody-daram-flustered.webp | 512x768 | 73 KB | daram |
| assets/room13-fullbody-daram-joy-acting.webp | 254x384 | 22 KB | daram |
| assets/room13-fullbody-daram-joy.webp | 512x768 | 73 KB | daram |
| assets/room13-fullbody-daram-neutral-acting.webp | 254x384 | 22 KB | daram |
| assets/room13-fullbody-daram-neutral.webp | 512x768 | 72 KB | daram |
| assets/room13-fullbody-daram-surprise-acting.webp | 288x416 | 23 KB | daram |
| assets/room13-fullbody-daram-surprise.webp | 512x768 | 73 KB | daram |
| assets/room13-fullbody-doto-angry.webp | 605x650 | 68 KB | doto |
| assets/room13-fullbody-doto-anxious.webp | 605x650 | 68 KB | doto |
| assets/room13-fullbody-doto-flustered.webp | 605x650 | 66 KB | doto |
| assets/room13-fullbody-doto-joy.webp | 605x650 | 68 KB | doto |
| assets/room13-fullbody-doto-neutral.webp | 605x650 | 65 KB | doto |
| assets/room13-fullbody-doto-surprise.webp | 605x650 | 67 KB | doto |
| assets/room13-fullbody-granny-angry-acting.webp | 300x440 | 30 KB | granny |
| assets/room13-fullbody-granny-angry.webp | 512x768 | 67 KB | granny |
| assets/room13-fullbody-granny-anxious-acting.webp | 300x440 | 23 KB | granny |
| assets/room13-fullbody-granny-anxious.webp | 512x768 | 68 KB | granny |
| assets/room13-fullbody-granny-flustered-acting.webp | 300x440 | 26 KB | granny |
| assets/room13-fullbody-granny-flustered.webp | 512x768 | 70 KB | granny |
| assets/room13-fullbody-granny-joy-scarf-acting.webp | 262x420 | 26 KB | granny |
| assets/room13-fullbody-granny-joy.webp | 512x768 | 68 KB | granny |
| assets/room13-fullbody-granny-neutral-acting.webp | 262x420 | 25 KB | granny |
| assets/room13-fullbody-granny-neutral.webp | 512x768 | 68 KB | granny |
| assets/room13-fullbody-granny-pose-withdraw_hand.webp | 512x768 | 190 KB | granny |
| assets/room13-fullbody-granny-surprise-scarf-acting.webp | 262x420 | 28 KB | granny |
| assets/room13-fullbody-granny-surprise.webp | 512x768 | 70 KB | granny |
| assets/room13-fullbody-guard-angry.webp | 512x768 | 75 KB | guard |
| assets/room13-fullbody-guard-anxious.webp | 512x768 | 80 KB | guard |
| assets/room13-fullbody-guard-flustered.webp | 512x768 | 69 KB | guard |
| assets/room13-fullbody-guard-joy.webp | 512x768 | 79 KB | guard |
| assets/room13-fullbody-guard-neutral.webp | 512x768 | 69 KB | guard |
| assets/room13-fullbody-guard-surprise.webp | 512x768 | 73 KB | guard |
| assets/room13-fullbody-karo-angry.webp | 512x768 | 89 KB | karo |
| assets/room13-fullbody-karo-anxious-acting.webp | 298x442 | 23 KB | karo |
| assets/room13-fullbody-karo-anxious.webp | 512x768 | 94 KB | karo |
| assets/room13-fullbody-karo-flustered.webp | 512x768 | 98 KB | karo |
| assets/room13-fullbody-karo-joy.webp | 512x768 | 83 KB | karo |
| assets/room13-fullbody-karo-neutral-acting.webp | 298x442 | 27 KB | karo |
| assets/room13-fullbody-karo-neutral.webp | 512x768 | 83 KB | karo |
| assets/room13-fullbody-karo-surprise.webp | 512x768 | 89 KB | karo |
| assets/room13-fullbody-kid_bang-anxious.webp | 512x768 | 83 KB | kid_bang |
| assets/room13-fullbody-kid_bang-joy.webp | 512x768 | 81 KB | kid_bang |
| assets/room13-fullbody-kid_bang-neutral.webp | 512x768 | 79 KB | kid_bang |
| assets/room13-fullbody-kid_bang-pose-cling_leg.webp | 512x768 | 78 KB | kid_bang |
| assets/room13-fullbody-kid_dodam-anxious.webp | 512x768 | 66 KB | kid_dodam |
| assets/room13-fullbody-kid_dodam-joy.webp | 512x768 | 67 KB | kid_dodam |
| assets/room13-fullbody-kid_dodam-neutral.webp | 512x768 | 62 KB | kid_dodam |
| assets/room13-fullbody-kid_dodam-pose-lick_ladle.webp | 512x768 | 76 KB | kid_dodam |
| assets/room13-fullbody-kid_kkam-anxious.webp | 512x768 | 64 KB | kid_kkam |
| assets/room13-fullbody-kid_kkam-joy.webp | 512x768 | 62 KB | kid_kkam |
| assets/room13-fullbody-kid_kkam-neutral.webp | 512x768 | 59 KB | kid_kkam |
| assets/room13-fullbody-kid_kkomi-angry.webp | 512x768 | 72 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-anxious.webp | 512x768 | 83 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-flustered.webp | 512x768 | 76 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-joy.webp | 512x768 | 83 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-neutral.webp | 512x768 | 81 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-pose-door_peek.webp | 512x768 | 86 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-pose-hideout_proud.webp | 512x768 | 96 KB | kid_kkomi |
| assets/room13-fullbody-kid_kkomi-surprise.webp | 512x768 | 84 KB | kid_kkomi |
| assets/room13-fullbody-kid_mong-anxious.webp | 512x768 | 89 KB | kid_mong |
| assets/room13-fullbody-kid_mong-joy.webp | 512x768 | 89 KB | kid_mong |
| assets/room13-fullbody-kid_mong-neutral.webp | 512x768 | 85 KB | kid_mong |
| assets/room13-fullbody-kid_nubi1-anxious.webp | 512x768 | 75 KB | kid_nubi1 |
| assets/room13-fullbody-kid_nubi1-joy.webp | 512x768 | 72 KB | kid_nubi1 |
| assets/room13-fullbody-kid_nubi1-neutral.webp | 512x768 | 68 KB | kid_nubi1 |
| assets/room13-fullbody-kid_nubi1-pose-hold_skirt.webp | 512x768 | 88 KB | kid_nubi1 |
| assets/room13-fullbody-kid_nubi2-anxious.webp | 512x768 | 67 KB | kid_nubi2 |
| assets/room13-fullbody-kid_nubi2-joy.webp | 512x768 | 68 KB | kid_nubi2 |
| assets/room13-fullbody-kid_nubi2-neutral.webp | 512x768 | 61 KB | kid_nubi2 |
| assets/room13-fullbody-kid_saemi-anxious.webp | 512x768 | 77 KB | kid_saemi |
| assets/room13-fullbody-kid_saemi-joy.webp | 512x768 | 76 KB | kid_saemi |
| assets/room13-fullbody-kid_saemi-neutral.webp | 512x768 | 76 KB | kid_saemi |
| assets/room13-fullbody-kid_saemi-pose-hide_bowl.webp | 512x768 | 79 KB | kid_saemi |
| assets/room13-fullbody-mom-angry.webp | 519x758 | 90 KB | mom |
| assets/room13-fullbody-mom-anxious-acting.webp | 312x454 | 32 KB | mom |
| assets/room13-fullbody-mom-anxious.webp | 519x758 | 91 KB | mom |
| assets/room13-fullbody-mom-flustered.webp | 519x758 | 92 KB | mom |
| assets/room13-fullbody-mom-joy.webp | 519x758 | 91 KB | mom |
| assets/room13-fullbody-mom-neutral-acting.webp | 312x454 | 30 KB | mom |
| assets/room13-fullbody-mom-neutral.webp | 519x758 | 90 KB | mom |
| assets/room13-fullbody-mom-pose-show_fragments.webp | 512x768 | 91 KB | mom |
| assets/room13-fullbody-mom-surprise.webp | 519x758 | 93 KB | mom |
| assets/room13-fullbody-nabi-angry-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-angry.webp | 512x768 | 72 KB | nabi |
| assets/room13-fullbody-nabi-anxious-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-anxious.webp | 512x768 | 73 KB | nabi |
| assets/room13-fullbody-nabi-flustered-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-flustered.webp | 512x768 | 74 KB | nabi |
| assets/room13-fullbody-nabi-joy-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-joy.webp | 512x768 | 73 KB | nabi |
| assets/room13-fullbody-nabi-neutral-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-neutral.webp | 512x768 | 76 KB | nabi |
| assets/room13-fullbody-nabi-surprise-acting.webp | 264x384 | 20 KB | nabi |
| assets/room13-fullbody-nabi-surprise.webp | 512x768 | 74 KB | nabi |
| assets/room13-fullbody-neoul-angry-acting.webp | 512x768 | 212 KB | neoul |
| assets/room13-fullbody-neoul-angry.webp | 572x687 | 70 KB | neoul |
| assets/room13-fullbody-neoul-anxious-acting.webp | 512x768 | 172 KB | neoul |
| assets/room13-fullbody-neoul-anxious.webp | 572x687 | 73 KB | neoul |
| assets/room13-fullbody-neoul-flustered-acting.webp | 512x768 | 178 KB | neoul |
| assets/room13-fullbody-neoul-flustered.webp | 572x686 | 72 KB | neoul |
| assets/room13-fullbody-neoul-joy-acting.webp | 512x768 | 216 KB | neoul |
| assets/room13-fullbody-neoul-joy.webp | 572x687 | 72 KB | neoul |
| assets/room13-fullbody-neoul-neutral.webp | 572x687 | 71 KB | neoul |
| assets/room13-fullbody-neoul-surprise-acting.webp | 512x768 | 212 KB | neoul |
| assets/room13-fullbody-neoul-surprise.webp | 572x688 | 71 KB | neoul |
| assets/room13-fullbody-npc_pandol-angry.webp | 512x768 | 94 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-anxious.webp | 512x768 | 106 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-flustered.webp | 512x768 | 95 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-joy.webp | 512x768 | 108 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-neutral.webp | 512x768 | 112 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-pose-point_name.webp | 512x768 | 113 KB | npc_pandol |
| assets/room13-fullbody-npc_pandol-surprise.webp | 512x768 | 97 KB | npc_pandol |
| assets/room13-fullbody-resident_badook-angry.webp | 512x768 | 79 KB | resident_badook |
| assets/room13-fullbody-resident_badook-anxious.webp | 512x768 | 80 KB | resident_badook |
| assets/room13-fullbody-resident_badook-flustered.webp | 512x768 | 81 KB | resident_badook |
| assets/room13-fullbody-resident_badook-joy.webp | 512x768 | 81 KB | resident_badook |
| assets/room13-fullbody-resident_badook-neutral.webp | 512x768 | 79 KB | resident_badook |
| assets/room13-fullbody-resident_badook-pose-block_cart.webp | 512x768 | 83 KB | resident_badook |
| assets/room13-fullbody-resident_badook-surprise.webp | 512x768 | 81 KB | resident_badook |
| assets/room13-fullbody-resident_bori-angry.webp | 512x768 | 71 KB | resident_bori |
| assets/room13-fullbody-resident_bori-anxious.webp | 512x768 | 70 KB | resident_bori |
| assets/room13-fullbody-resident_bori-flustered.webp | 512x768 | 70 KB | resident_bori |
| assets/room13-fullbody-resident_bori-joy.webp | 512x768 | 69 KB | resident_bori |
| assets/room13-fullbody-resident_bori-neutral.webp | 512x768 | 68 KB | resident_bori |
| assets/room13-fullbody-resident_bori-surprise.webp | 512x768 | 71 KB | resident_bori |
| assets/room13-fullbody-resident_eunho-angry.webp | 512x768 | 63 KB | resident_eunho |
| assets/room13-fullbody-resident_eunho-anxious.webp | 512x768 | 64 KB | resident_eunho |
| assets/room13-fullbody-resident_eunho-flustered.webp | 512x768 | 64 KB | resident_eunho |
| assets/room13-fullbody-resident_eunho-joy.webp | 512x768 | 65 KB | resident_eunho |
| assets/room13-fullbody-resident_eunho-neutral.webp | 512x768 | 62 KB | resident_eunho |
| assets/room13-fullbody-resident_eunho-surprise.webp | 512x768 | 64 KB | resident_eunho |
| assets/room13-fullbody-resident_kongi-angry.webp | 512x768 | 73 KB | resident_kongi |
| assets/room13-fullbody-resident_kongi-anxious.webp | 512x768 | 72 KB | resident_kongi |
| assets/room13-fullbody-resident_kongi-flustered.webp | 512x768 | 74 KB | resident_kongi |
| assets/room13-fullbody-resident_kongi-joy.webp | 512x768 | 74 KB | resident_kongi |
| assets/room13-fullbody-resident_kongi-neutral.webp | 512x768 | 71 KB | resident_kongi |
| assets/room13-fullbody-resident_kongi-surprise.webp | 512x768 | 72 KB | resident_kongi |
| assets/room13-fullbody-resident_lamplighter-angry.webp | 512x768 | 57 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-anxious-acting.webp | 284x422 | 18 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-anxious.webp | 512x768 | 58 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-flustered-acting.webp | 284x422 | 19 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-flustered.webp | 512x768 | 58 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-joy.webp | 512x768 | 58 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-neutral-acting.webp | 284x422 | 18 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-neutral.webp | 512x768 | 56 KB | resident_lamplighter |
| assets/room13-fullbody-resident_lamplighter-surprise.webp | 512x768 | 58 KB | resident_lamplighter |
| assets/room13-fullbody-resident_madam-angry.webp | 512x768 | 51 KB | resident_madam |
| assets/room13-fullbody-resident_madam-anxious.webp | 512x768 | 52 KB | resident_madam |
| assets/room13-fullbody-resident_madam-flustered.webp | 512x768 | 52 KB | resident_madam |
| assets/room13-fullbody-resident_madam-joy.webp | 512x768 | 50 KB | resident_madam |
| assets/room13-fullbody-resident_madam-neutral.webp | 512x768 | 55 KB | resident_madam |
| assets/room13-fullbody-resident_madam-surprise.webp | 512x768 | 51 KB | resident_madam |
| assets/room13-fullbody-resident_momo-angry.webp | 512x768 | 64 KB | resident_momo |
| assets/room13-fullbody-resident_momo-anxious.webp | 512x768 | 66 KB | resident_momo |
| assets/room13-fullbody-resident_momo-flustered.webp | 512x768 | 66 KB | resident_momo |
| assets/room13-fullbody-resident_momo-joy.webp | 512x768 | 65 KB | resident_momo |
| assets/room13-fullbody-resident_momo-neutral.webp | 512x768 | 65 KB | resident_momo |
| assets/room13-fullbody-resident_momo-surprise.webp | 512x768 | 65 KB | resident_momo |
| assets/room13-fullbody-resident_musoe-angry.webp | 512x768 | 70 KB | resident_musoe |
| assets/room13-fullbody-resident_musoe-anxious.webp | 512x768 | 70 KB | resident_musoe |
| assets/room13-fullbody-resident_musoe-flustered.webp | 512x768 | 71 KB | resident_musoe |
| assets/room13-fullbody-resident_musoe-joy.webp | 512x768 | 69 KB | resident_musoe |
| assets/room13-fullbody-resident_musoe-neutral.webp | 512x768 | 64 KB | resident_musoe |
| assets/room13-fullbody-resident_musoe-surprise.webp | 512x768 | 70 KB | resident_musoe |
| assets/room13-fullbody-resident_nero-angry.webp | 512x768 | 71 KB | resident_nero |
| assets/room13-fullbody-resident_nero-anxious.webp | 512x768 | 70 KB | resident_nero |
| assets/room13-fullbody-resident_nero-flustered.webp | 512x768 | 67 KB | resident_nero |
| assets/room13-fullbody-resident_nero-joy.webp | 512x768 | 72 KB | resident_nero |
| assets/room13-fullbody-resident_nero-neutral.webp | 512x768 | 68 KB | resident_nero |
| assets/room13-fullbody-resident_nero-surprise.webp | 512x768 | 71 KB | resident_nero |
| assets/room13-fullbody-resident_nubi-angry.webp | 496x792 | 76 KB | resident_nubi |
| assets/room13-fullbody-resident_nubi-anxious.webp | 496x792 | 72 KB | resident_nubi |
| assets/room13-fullbody-resident_nubi-flustered.webp | 496x792 | 75 KB | resident_nubi |
| assets/room13-fullbody-resident_nubi-joy.webp | 496x792 | 76 KB | resident_nubi |
| assets/room13-fullbody-resident_nubi-neutral.webp | 496x793 | 74 KB | resident_nubi |
| assets/room13-fullbody-resident_nubi-surprise.webp | 496x792 | 75 KB | resident_nubi |
| assets/room13-fullbody-resident_owlgp-angry-acting.webp | 306x460 | 33 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-angry.webp | 544x722 | 69 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-anxious-acting.webp | 306x460 | 27 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-anxious.webp | 544x722 | 72 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-flustered-acting.webp | 306x460 | 32 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-flustered.webp | 544x722 | 71 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-joy-acting.webp | 306x460 | 29 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-joy.webp | 544x722 | 72 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-neutral-acting.webp | 306x460 | 26 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-neutral.webp | 545x722 | 71 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-surprise-acting.webp | 306x460 | 32 KB | resident_owlgp |
| assets/room13-fullbody-resident_owlgp-surprise.webp | 544x722 | 71 KB | resident_owlgp |
| assets/room13-fullbody-resident_piko-angry.webp | 512x768 | 74 KB | resident_piko |
| assets/room13-fullbody-resident_piko-anxious.webp | 512x768 | 77 KB | resident_piko |
| assets/room13-fullbody-resident_piko-flustered.webp | 512x768 | 77 KB | resident_piko |
| assets/room13-fullbody-resident_piko-joy.webp | 512x768 | 76 KB | resident_piko |
| assets/room13-fullbody-resident_piko-neutral.webp | 512x768 | 76 KB | resident_piko |
| assets/room13-fullbody-resident_piko-surprise.webp | 512x768 | 79 KB | resident_piko |
| assets/room13-fullbody-resident_ppul-angry-acting.webp | 304x452 | 34 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-angry.webp | 512x768 | 79 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-anxious-acting.webp | 304x452 | 27 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-anxious.webp | 512x768 | 78 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-flustered-acting.webp | 304x452 | 30 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-flustered.webp | 512x768 | 80 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-joy.webp | 512x768 | 80 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-neutral-acting.webp | 304x452 | 29 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-neutral.webp | 512x768 | 78 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-pose-kneel_stone.webp | 512x768 | 84 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-surprise-acting.webp | 304x452 | 32 KB | resident_ppul |
| assets/room13-fullbody-resident_ppul-surprise.webp | 512x768 | 77 KB | resident_ppul |
| assets/room13-fullbody-resident_seori-angry-acting.webp | 324x476 | 25 KB | resident_seori |
| assets/room13-fullbody-resident_seori-angry.webp | 512x768 | 62 KB | resident_seori |
| assets/room13-fullbody-resident_seori-anxious-acting.webp | 324x476 | 21 KB | resident_seori |
| assets/room13-fullbody-resident_seori-anxious.webp | 512x768 | 61 KB | resident_seori |
| assets/room13-fullbody-resident_seori-flustered-acting.webp | 324x476 | 26 KB | resident_seori |
| assets/room13-fullbody-resident_seori-flustered.webp | 512x768 | 61 KB | resident_seori |
| assets/room13-fullbody-resident_seori-joy-acting.webp | 324x476 | 27 KB | resident_seori |
| assets/room13-fullbody-resident_seori-joy.webp | 512x768 | 61 KB | resident_seori |
| assets/room13-fullbody-resident_seori-neutral-acting.webp | 324x476 | 24 KB | resident_seori |
| assets/room13-fullbody-resident_seori-neutral.webp | 512x768 | 56 KB | resident_seori |
| assets/room13-fullbody-resident_seori-surprise-acting.webp | 324x476 | 28 KB | resident_seori |
| assets/room13-fullbody-resident_seori-surprise.webp | 512x768 | 61 KB | resident_seori |
| assets/room13-fullbody-resident_siluk-angry.webp | 512x768 | 59 KB | resident_siluk |
| assets/room13-fullbody-resident_siluk-anxious.webp | 512x768 | 60 KB | resident_siluk |
| assets/room13-fullbody-resident_siluk-flustered.webp | 512x768 | 59 KB | resident_siluk |
| assets/room13-fullbody-resident_siluk-joy.webp | 512x768 | 58 KB | resident_siluk |
| assets/room13-fullbody-resident_siluk-neutral.webp | 512x768 | 58 KB | resident_siluk |
| assets/room13-fullbody-resident_siluk-surprise.webp | 512x768 | 59 KB | resident_siluk |
| assets/room13-fullbody-resident_sling-angry.webp | 512x768 | 75 KB | resident_sling |
| assets/room13-fullbody-resident_sling-anxious.webp | 512x768 | 75 KB | resident_sling |
| assets/room13-fullbody-resident_sling-flustered.webp | 512x768 | 76 KB | resident_sling |
| assets/room13-fullbody-resident_sling-joy.webp | 512x768 | 75 KB | resident_sling |
| assets/room13-fullbody-resident_sling-neutral.webp | 512x768 | 74 KB | resident_sling |
| assets/room13-fullbody-resident_sling-surprise.webp | 512x768 | 72 KB | resident_sling |
| assets/room13-fullbody-resident_somi-angry.webp | 512x768 | 70 KB | resident_somi |
| assets/room13-fullbody-resident_somi-anxious.webp | 512x768 | 74 KB | resident_somi |
| assets/room13-fullbody-resident_somi-flustered.webp | 512x768 | 74 KB | resident_somi |
| assets/room13-fullbody-resident_somi-joy.webp | 512x768 | 72 KB | resident_somi |
| assets/room13-fullbody-resident_somi-neutral.webp | 512x768 | 72 KB | resident_somi |
| assets/room13-fullbody-resident_somi-surprise.webp | 512x768 | 75 KB | resident_somi |
| assets/room13-fullbody-resident_teacher-angry-acting.webp | 512x768 | 204 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-angry.webp | 512x768 | 62 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-anxious-acting.webp | 512x768 | 186 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-anxious.webp | 512x768 | 61 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-flustered-acting.webp | 512x768 | 187 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-flustered.webp | 512x768 | 64 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-joy-acting.webp | 512x768 | 206 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-joy.webp | 512x768 | 63 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-neutral.webp | 512x768 | 61 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-pose-collapse_attendance.webp | 512x768 | 98 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-pose-wipe_board.webp | 512x768 | 103 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-pose-write_attendance.webp | 512x768 | 101 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-surprise-acting.webp | 512x768 | 196 KB | resident_teacher |
| assets/room13-fullbody-resident_teacher-surprise.webp | 512x768 | 62 KB | resident_teacher |
| assets/room13-fullbody-resident_tok-angry.webp | 512x768 | 68 KB | resident_tok |
| assets/room13-fullbody-resident_tok-anxious.webp | 512x768 | 66 KB | resident_tok |
| assets/room13-fullbody-resident_tok-flustered-acting.webp | 274x412 | 28 KB | resident_tok |
| assets/room13-fullbody-resident_tok-flustered.webp | 512x768 | 70 KB | resident_tok |
| assets/room13-fullbody-resident_tok-joy.webp | 512x768 | 70 KB | resident_tok |
| assets/room13-fullbody-resident_tok-neutral-acting.webp | 274x412 | 26 KB | resident_tok |
| assets/room13-fullbody-resident_tok-neutral.webp | 512x768 | 67 KB | resident_tok |
| assets/room13-fullbody-resident_tok-surprise.webp | 512x768 | 70 KB | resident_tok |
| assets/room13-fullbody-resident_tosil-neutral.webp | 512x768 | 70 KB | resident_tosil |
| assets/room13-fullbody-resident_tosil-pose-hold_storybook.webp | 512x768 | 70 KB | resident_tosil |
| assets/room13-fullbody-resident_ttadak-angry.webp | 512x768 | 74 KB | resident_ttadak |
| assets/room13-fullbody-resident_ttadak-anxious.webp | 512x768 | 76 KB | resident_ttadak |
| assets/room13-fullbody-resident_ttadak-flustered.webp | 512x768 | 75 KB | resident_ttadak |
| assets/room13-fullbody-resident_ttadak-joy.webp | 512x768 | 75 KB | resident_ttadak |
| assets/room13-fullbody-resident_ttadak-neutral.webp | 512x768 | 74 KB | resident_ttadak |
| assets/room13-fullbody-resident_ttadak-surprise.webp | 512x768 | 76 KB | resident_ttadak |
| assets/room13-fullbody-resident_ubak-angry.webp | 512x768 | 67 KB | resident_ubak |
| assets/room13-fullbody-resident_ubak-anxious.webp | 512x768 | 69 KB | resident_ubak |
| assets/room13-fullbody-resident_ubak-flustered.webp | 512x768 | 68 KB | resident_ubak |
| assets/room13-fullbody-resident_ubak-joy.webp | 512x768 | 68 KB | resident_ubak |
| assets/room13-fullbody-resident_ubak-neutral.webp | 512x768 | 65 KB | resident_ubak |
| assets/room13-fullbody-resident_ubak-surprise.webp | 512x768 | 69 KB | resident_ubak |
| assets/room13-fullbody-seryeon-angry.webp | 512x768 | 70 KB | seryeon |
| assets/room13-fullbody-seryeon-anxious.webp | 512x768 | 71 KB | seryeon |
| assets/room13-fullbody-seryeon-flustered.webp | 512x768 | 71 KB | seryeon |
| assets/room13-fullbody-seryeon-joy.webp | 512x768 | 73 KB | seryeon |
| assets/room13-fullbody-seryeon-neutral-acting.webp | 288x432 | 25 KB | seryeon |
| assets/room13-fullbody-seryeon-neutral.webp | 512x768 | 73 KB | seryeon |
| assets/room13-fullbody-seryeon-surprise-acting.webp | 288x432 | 27 KB | seryeon |
| assets/room13-fullbody-seryeon-surprise.webp | 512x768 | 70 KB | seryeon |
| assets/room13-fx-blink-bami-angry-closed.webp | 168x71 | 5 KB | bami |
| assets/room13-fx-blink-bami-angry-half.webp | 168x71 | 8 KB | bami |
| assets/room13-fx-blink-bami-anxious-closed.webp | 169x76 | 4 KB | bami |
| assets/room13-fx-blink-bami-anxious-half.webp | 169x76 | 8 KB | bami |
| assets/room13-fx-blink-bami-flustered-closed.webp | 165x71 | 6 KB | bami |
| assets/room13-fx-blink-bami-flustered-half.webp | 165x71 | 9 KB | bami |
| assets/room13-fx-blink-bami-neutral-closed.webp | 169x77 | 5 KB | bami |
| assets/room13-fx-blink-bami-neutral-half.webp | 169x77 | 8 KB | bami |
| assets/room13-fx-blink-bami-surprise-closed.webp | 168x90 | 5 KB | bami |
| assets/room13-fx-blink-bami-surprise-half.webp | 168x90 | 10 KB | bami |
| assets/room13-fx-blink-buri-angry-closed.webp | 164x65 | 5 KB | buri |
| assets/room13-fx-blink-buri-angry-half.webp | 164x65 | 7 KB | buri |
| assets/room13-fx-blink-buri-anxious-closed.webp | 168x64 | 5 KB | buri |
| assets/room13-fx-blink-buri-anxious-half.webp | 168x64 | 8 KB | buri |
| assets/room13-fx-blink-buri-flustered-closed.webp | 166x61 | 7 KB | buri |
| assets/room13-fx-blink-buri-flustered-half.webp | 166x61 | 9 KB | buri |
| assets/room13-fx-blink-buri-neutral-closed.webp | 165x66 | 5 KB | buri |
| assets/room13-fx-blink-buri-neutral-half.webp | 165x66 | 8 KB | buri |
| assets/room13-fx-blink-buri-surprise-closed.webp | 169x77 | 7 KB | buri |
| assets/room13-fx-blink-buri-surprise-half.webp | 169x77 | 10 KB | buri |
| assets/room13-fx-blink-daram-angry-closed.webp | 157x73 | 5 KB | daram |
| assets/room13-fx-blink-daram-angry-half.webp | 157x73 | 7 KB | daram |
| assets/room13-fx-blink-daram-anxious-closed.webp | 156x71 | 5 KB | daram |
| assets/room13-fx-blink-daram-anxious-half.webp | 156x71 | 7 KB | daram |
| assets/room13-fx-blink-daram-flustered-closed.webp | 162x70 | 8 KB | daram |
| assets/room13-fx-blink-daram-flustered-half.webp | 162x70 | 10 KB | daram |
| assets/room13-fx-blink-daram-neutral-closed.webp | 157x78 | 6 KB | daram |
| assets/room13-fx-blink-daram-neutral-half.webp | 157x78 | 8 KB | daram |
| assets/room13-fx-blink-daram-surprise-closed.webp | 157x81 | 7 KB | daram |
| assets/room13-fx-blink-daram-surprise-half.webp | 157x81 | 9 KB | daram |
| assets/room13-fx-blink-mom-angry-closed.webp | 167x65 | 6 KB | mom |
| assets/room13-fx-blink-mom-angry-half.webp | 167x65 | 8 KB | mom |
| assets/room13-fx-blink-mom-anxious-closed.webp | 167x66 | 7 KB | mom |
| assets/room13-fx-blink-mom-anxious-half.webp | 167x66 | 9 KB | mom |
| assets/room13-fx-blink-mom-neutral-closed.webp | 167x66 | 7 KB | mom |
| assets/room13-fx-blink-mom-neutral-half.webp | 167x66 | 8 KB | mom |
| assets/room13-fx-blink-mom-surprise-closed.webp | 168x77 | 7 KB | mom |
| assets/room13-fx-blink-mom-surprise-half.webp | 168x77 | 10 KB | mom |
| assets/room13-fx-blink-nabi-angry-closed.webp | 174x63 | 4 KB | nabi |
| assets/room13-fx-blink-nabi-angry-half.webp | 174x63 | 7 KB | nabi |
| assets/room13-fx-blink-nabi-anxious-closed.webp | 172x65 | 4 KB | nabi |
| assets/room13-fx-blink-nabi-anxious-half.webp | 172x65 | 7 KB | nabi |
| assets/room13-fx-blink-nabi-flustered-closed.webp | 172x62 | 5 KB | nabi |
| assets/room13-fx-blink-nabi-flustered-half.webp | 172x62 | 9 KB | nabi |
| assets/room13-fx-blink-nabi-neutral-closed.webp | 172x65 | 3 KB | nabi |
| assets/room13-fx-blink-nabi-neutral-half.webp | 172x65 | 7 KB | nabi |
| assets/room13-fx-blink-nabi-surprise-closed.webp | 174x75 | 4 KB | nabi |
| assets/room13-fx-blink-nabi-surprise-half.webp | 174x75 | 8 KB | nabi |
| assets/room13-group-buri-cooperative.webp | 512x768 | 71 KB | buri |
| assets/room13-group-kid_bang-play.webp | 1024x1536 | 162 KB | kid_bang |
| assets/room13-group-kid_kkam-play.webp | 1024x1536 | 169 KB | kid_kkam |
| assets/room13-group-kid_mong-play.webp | 1024x1536 | 195 KB | kid_mong |
| assets/room13-group-resident_tok-cooperative.webp | 512x768 | 83 KB | resident_tok |
| assets/room13-meeting-seated-granny068.webp | 1024x1536 | 527 KB | granny |
| assets/room13-meeting-seated-nabi068.webp | 1024x1536 | 183 KB | nabi |
| assets/room13-meeting-seated-resident_kongi068.webp | 1024x1536 | 183 KB | resident_kongi |
| assets/room13-meeting-seated-resident_ppul068.webp | 1024x1536 | 167 KB | resident_ppul |
| assets/room13-meeting-seated-resident_seori068.webp | 1024x1536 | 149 KB | resident_seori |
| assets/room13-meeting-seated-seryeon068.webp | 1023x1537 | 199 KB | seryeon |
| assets/room13-mom-body-distressed.png | 194x182 | 19 KB | mom |
| assets/room13-mom-body-expressive.png | 194x182 | 19 KB | mom |
| assets/room13-mom-body-neutral.png | 192x182 | 18 KB | mom |
| assets/room13-mom-body-thinking.png | 186x182 | 19 KB | mom |
| assets/room13-mom-face-distressed.png | 192x192 | 12 KB | mom |
| assets/room13-mom-face-expressive.png | 192x192 | 12 KB | mom |
| assets/room13-mom-face-neutral.png | 192x192 | 11 KB | mom |
| assets/room13-mom-face-thinking.png | 192x192 | 13 KB | mom |
| assets/room13-pixel-acting-badook.webp | 1536x1024 | 275 KB | resident_badook |
| assets/room13-pixel-acting-bami.webp | 1536x1024 | 294 KB | bami |
| assets/room13-pixel-acting-buri.webp | 1536x1024 | 334 KB | buri |
| assets/room13-pixel-acting-dad.webp | 1536x1024 | 285 KB | dad |
| assets/room13-pixel-acting-daram-extra-hard.webp | 1536x1024 | 654 KB | daram |
| assets/room13-pixel-acting-daram-world-hard.webp | 1536x1024 | 760 KB | daram |
| assets/room13-pixel-acting-daram.webp | 1536x1024 | 320 KB | daram |
| assets/room13-pixel-acting-doto.webp | 1536x1024 | 327 KB | doto |
| assets/room13-pixel-acting-eunho.webp | 1536x1024 | 254 KB | resident_eunho |
| assets/room13-pixel-acting-family-extra.webp | 1536x1024 | 297 KB | dad; daram |
| assets/room13-pixel-acting-granny.webp | 1536x1024 | 319 KB | granny |
| assets/room13-pixel-acting-guard-extra.webp | 1536x1024 | 247 KB | guard |
| assets/room13-pixel-acting-guard.webp | 1536x1024 | 332 KB | guard |
| assets/room13-pixel-acting-karo.webp | 1536x1024 | 326 KB | karo |
| assets/room13-pixel-acting-lamplighter.webp | 1536x1024 | 253 KB | resident_lamplighter |
| assets/room13-pixel-acting-mom.webp | 1536x1024 | 394 KB | mom |
| assets/room13-pixel-acting-musoe.webp | 1536x1024 | 219 KB | resident_musoe |
| assets/room13-pixel-acting-nabi.webp | 1536x1024 | 342 KB | nabi |
| assets/room13-pixel-acting-neoul.webp | 1536x1024 | 354 KB | neoul |
| assets/room13-pixel-acting-resident_bori.webp | 1536x1024 | 236 KB | resident_bori |
| assets/room13-pixel-acting-resident_kongi.webp | 1536x1024 | 262 KB | resident_kongi |
| assets/room13-pixel-acting-resident_nero.webp | 1536x1024 | 226 KB | resident_nero |
| assets/room13-pixel-acting-resident_owlgp.webp | 1536x1024 | 305 KB | resident_owlgp |
| assets/room13-pixel-acting-resident_ppul.webp | 1536x1024 | 264 KB | resident_ppul |
| assets/room13-pixel-acting-resident_sling.webp | 1536x1024 | 284 KB | resident_sling |
| assets/room13-pixel-acting-resident_teacher.webp | 1536x1024 | 240 KB | resident_teacher |
| assets/room13-pixel-acting-resident_tok.webp | 1536x1024 | 249 KB | resident_tok |
| assets/room13-pixel-acting-seori.webp | 1536x1024 | 218 KB | resident_seori |
| assets/room13-pixel-acting-seryeon-chair.webp | 1774x887 | 238 KB | seryeon |
| assets/room13-pixel-acting-seryeon.webp | 1536x1024 | 324 KB | seryeon |
| assets/room13-pixel-acting-somi.webp | 1536x1024 | 260 KB | resident_somi |
| assets/room13-pixel-acting-ttadak.webp | 1536x1024 | 282 KB | resident_ttadak |
| assets/room13-pixel-acting-ubak.webp | 1536x1024 | 244 KB | resident_ubak |
| assets/room13-pixel-avatar-support-0.webp | 1536x1024 | 296 KB | bodum; elder; resident_bori; resident_kkwak; resident_kongi; resident_tori; workshop |
| assets/room13-pixel-avatar-support-1.webp | 1536x1024 | 317 KB | resident_librarian; resident_nero; resident_owlgp; resident_ppul; resident_sling; resident_teacher; resident_t |
| assets/room13-pixel-avatar-support-2.webp | 1536x1024 | 305 KB | resident_madam; resident_momo; resident_mungchi; resident_musoe; resident_siluk; resident_somi |
| assets/room13-pixel-avatar-support-3.webp | 1536x1024 | 266 KB | resident_eunho; resident_guseul; resident_nubi; resident_seori; resident_ubak |
| assets/room13-pixel-avatar-support-six.webp | 1536x1024 | 270 KB | resident_badook; resident_lamplighter; resident_piko; resident_seol; resident_ttadak; resident_yeoni |
| assets/room13-pixel-daram-motion.webp | 1536x1024 | 308 KB | daram; file |
| assets/room13-pixel-dialogue-bami.webp | 1536x1024 | 213 KB | bami |
| assets/room13-pixel-dialogue-buri.webp | 1536x1024 | 221 KB | buri |
| assets/room13-pixel-dialogue-dad.webp | 1536x1024 | 329 KB | dad |
| assets/room13-pixel-dialogue-daram-joy.webp | 395x330 | 26 KB | daram |
| assets/room13-pixel-dialogue-daram.webp | 1536x1024 | 324 KB | daram |
| assets/room13-pixel-dialogue-doto.webp | 1536x1024 | 203 KB | doto |
| assets/room13-pixel-dialogue-granny.webp | 1536x1024 | 230 KB | granny |
| assets/room13-pixel-dialogue-guard.webp | 1536x1024 | 193 KB | guard |
| assets/room13-pixel-dialogue-karo.webp | 1536x1024 | 217 KB | karo |
| assets/room13-pixel-dialogue-mom.webp | 1536x1024 | 424 KB | mom |
| assets/room13-pixel-dialogue-nabi.webp | 1536x1024 | 246 KB | nabi |
| assets/room13-pixel-dialogue-neoul.webp | 1536x1024 | 234 KB | neoul |
| assets/room13-pixel-dialogue-seryeon.webp | 1536x1024 | 219 KB | seryeon |
| assets/room13-pixel-dialogue-support-03.webp | 1536x1024 | 358 KB | resident_kongi |
| assets/room13-pixel-dialogue-support-05.webp | 1536x1024 | 375 KB | resident_nero |
| assets/room13-pixel-dialogue-support-06.webp | 1536x1024 | 421 KB | resident_ppul |
| assets/room13-pixel-dialogue-support-07.webp | 1536x1024 | 419 KB | resident_sling; resident_tok |
| assets/room13-pixel-dialogue-support-08.webp | 1536x1024 | 359 KB | resident_ttadak |
| assets/room13-pixel-dialogue-support-11.webp | 1536x1024 | 348 KB | resident_musoe; resident_somi |
| assets/room13-pixel-dialogue-support-12.webp | 1536x1024 | 352 KB | resident_seori; resident_ubak |
| assets/room13-pixel-dialogue-support-13.webp | 1536x1024 | 357 KB | resident_eunho |
| assets/room13-pixel-dialogue-support-14.webp | 1536x1024 | 403 KB | resident_badook |
| assets/room13-pixel-dialogue-support-15.webp | 2172x724 | 201 KB | resident_lamplighter |
| assets/room13-pixel-family-profile-icons.webp | 2172x724 | 260 KB | dad; daram; mom |
| assets/room13-pixel-karo-fullbody.webp | 1024x1536 | 199 KB | karo |
| assets/room13-pixel-main-profile-a.webp | 2170x725 | 256 KB | nabi; seryeon |
| assets/room13-pixel-main-profile-b.webp | 2172x724 | 240 KB | bami; buri; doto |
| assets/room13-pixel-main-profile-c.webp | 2172x724 | 253 KB | guard; karo; neoul |
| assets/room13-pixel-main-profile-granny.webp | 1254x1254 | 132 KB | granny |
| assets/room13-pixel-world-dad-gray.webp | 1536x1024 | 389 KB | dad |
| assets/room13-pixel-world-daram-gray-gutter.webp | 1536x1024 | 467 KB | daram |
| assets/room13-pixel-world-family-extra-gray.webp | 1536x1024 | 451 KB | dad; daram |
| assets/room13-pixel-world-mom-gray-gutter.webp | 1536x1024 | 486 KB | mom |
| assets/room13-redesign-granny.webp | 512x768 | 188 KB | granny |
| assets/room13-redesign-resident_bori.webp | 512x768 | 61 KB | resident_bori |
| assets/room13-redesign-resident_momo.webp | 512x768 | 55 KB | resident_momo |
| assets/room13-redesign-resident_nero.webp | 512x768 | 81 KB | resident_nero |
| assets/room13-redesign-resident_nubi.webp | 512x768 | 52 KB | resident_nubi |
| assets/room13-redesign-resident_owlgp.webp | 512x768 | 66 KB | resident_owlgp |
| assets/room13-redesign-resident_siluk.webp | 519x758 | 60 KB | resident_siluk |
| assets/room13-role-buri-angry.webp | 294x468 | 22 KB | buri |
| assets/room13-role-buri-anxious.webp | 294x468 | 20 KB | buri |
| assets/room13-role-buri-flustered.webp | 294x468 | 20 KB | buri |
| assets/room13-role-buri-joy.webp | 294x468 | 21 KB | buri |
| assets/room13-role-buri-neutral.webp | 294x468 | 22 KB | buri |
| assets/room13-role-buri-surprise.webp | 294x468 | 21 KB | buri |
| assets/room13-role-doto-batch-action_1-v1.webp | 1017x1547 | 590 KB | doto |
| assets/room13-role-doto-batch-action_2-v1.webp | 1017x1547 | 521 KB | doto |
| assets/room13-role-doto-batch-angry-v1.webp | 1017x1547 | 563 KB | doto |
| assets/room13-role-doto-batch-anxious-v1.webp | 1017x1547 | 496 KB | doto |
| assets/room13-role-doto-batch-flustered-v1.webp | 1018x1545 | 541 KB | doto |
| assets/room13-role-doto-batch-joy-v1.webp | 1017x1547 | 523 KB | doto |
| assets/room13-role-doto-batch-surprise-v1.webp | 1018x1545 | 604 KB | doto |
| assets/room13-role-doto.webp | 490x746 | 49 KB | doto |
| assets/room13-role-guard-batch-angry-v1.webp | 977x1609 | 689 KB | guard |
| assets/room13-role-guard-batch-anxious-v1.webp | 977x1610 | 688 KB | guard |
| assets/room13-role-guard-batch-flustered-v1.webp | 977x1609 | 741 KB | guard |
| assets/room13-role-guard-batch-joy-v1.webp | 977x1610 | 691 KB | guard |
| assets/room13-role-guard-batch-surprise-v1.webp | 977x1610 | 716 KB | guard |
| assets/room13-role-guard-neutral.webp | 272x448 | 30 KB | guard |
| assets/room13-role-neoul-batch-angry-v1.webp | 1036x1518 | 880 KB | neoul |
| assets/room13-role-neoul-batch-anxious-v1.webp | 1036x1518 | 736 KB | neoul |
| assets/room13-role-neoul-batch-flustered-v1.webp | 1036x1518 | 768 KB | neoul |
| assets/room13-role-neoul-batch-joy-v1.webp | 1036x1518 | 785 KB | neoul |
| assets/room13-role-neoul-batch-surprise-v1.webp | 1036x1518 | 818 KB | neoul |
| assets/room13-role-resident_bori-batch-angry-v1.webp | 1210x1300 | 781 KB | resident_bori |
| assets/room13-role-resident_bori-batch-anxious-v1.webp | 1024x1536 | 1039 KB | resident_bori |
| assets/room13-role-resident_bori-batch-flustered-v1.webp | 1024x1536 | 1063 KB | resident_bori |
| assets/room13-role-resident_bori-batch-joy-v1.webp | 1210x1300 | 779 KB | resident_bori |
| assets/room13-role-resident_bori-batch-surprise-v1.webp | 1024x1536 | 1137 KB | resident_bori |
| assets/room13-role-resident_guldol-angry.webp | 282x420 | 28 KB | resident_guldol |
| assets/room13-role-resident_guldol-anxious.webp | 282x420 | 24 KB | resident_guldol |
| assets/room13-role-resident_guldol-flustered.webp | 284x420 | 27 KB | resident_guldol |
| assets/room13-role-resident_guldol-joy.webp | 284x420 | 25 KB | resident_guldol |
| assets/room13-role-resident_guldol-neutral.webp | 282x420 | 26 KB | resident_guldol |
| assets/room13-role-resident_guldol-surprise.webp | 282x420 | 27 KB | resident_guldol |
| assets/room13-role-resident_lamplighter-batch-angry-v1.webp | 1024x1536 | 988 KB | resident_lamplighter |
| assets/room13-role-resident_lamplighter-batch-joy-v1.webp | 1024x1536 | 971 KB | resident_lamplighter |
| assets/room13-role-resident_lamplighter-batch-surprise-v1.webp | 1014x1551 | 631 KB | resident_lamplighter |
| assets/room13-role-resident_madam-batch-angry-v1.webp | 981x1603 | 710 KB | resident_madam |
| assets/room13-role-resident_madam-batch-anxious-v1.webp | 981x1603 | 683 KB | resident_madam |
| assets/room13-role-resident_madam-batch-flustered-v1.webp | 981x1604 | 743 KB | resident_madam |
| assets/room13-role-resident_madam-batch-joy-v1.webp | 981x1603 | 683 KB | resident_madam |
| assets/room13-role-resident_madam-batch-surprise-v1.webp | 981x1603 | 735 KB | resident_madam |
| assets/room13-role-resident_madam.webp | 466x762 | 71 KB | resident_madam |
| assets/room13-role-resident_nubi-batch-angry-v1.webp | 996x1579 | 747 KB | resident_nubi |
| assets/room13-role-resident_nubi-batch-anxious-v1.webp | 996x1579 | 605 KB | resident_nubi |
| assets/room13-role-resident_nubi-batch-flustered-v1.webp | 996x1578 | 626 KB | resident_nubi |
| assets/room13-role-resident_nubi-batch-joy-v1.webp | 996x1578 | 614 KB | resident_nubi |
| assets/room13-role-resident_nubi-batch-surprise-v1.webp | 996x1578 | 638 KB | resident_nubi |
| assets/room13-role-resident_nubi.webp | 478x758 | 60 KB | resident_nubi |
| assets/room13-role-resident_piko.webp | 497x768 | 69 KB | resident_piko |
| assets/room13-role-resident_siluk-batch-angry-v1.webp | 1038x1515 | 665 KB | resident_siluk |
| assets/room13-role-resident_siluk-batch-anxious-v1.webp | 1038x1515 | 500 KB | resident_siluk |
| assets/room13-role-resident_siluk-batch-flustered-v1.webp | 1038x1515 | 581 KB | resident_siluk |
| assets/room13-role-resident_siluk-batch-joy-v1.webp | 1038x1515 | 588 KB | resident_siluk |
| assets/room13-role-resident_siluk-batch-surprise-v1.webp | 1038x1515 | 649 KB | resident_siluk |
| assets/room13-role-resident_teacher-batch-angry-v1.webp | 1004x1566 | 1008 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-anxious-v1.webp | 1005x1566 | 945 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-collapse_attendance-v1.webp | 1004x1566 | 730 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-flustered-v1.webp | 1004x1566 | 847 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-joy-v1.webp | 1004x1567 | 838 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-surprise-v1.webp | 1004x1566 | 922 KB | resident_teacher |
| assets/room13-role-resident_teacher-batch-write_attendance-v1.webp | 1005x1566 | 922 KB | resident_teacher |
| assets/room13-role-resident_tosil-batch-angry-v1.webp | 988x1591 | 572 KB | resident_tosil |
| assets/room13-role-resident_tosil-batch-anxious-v1.webp | 988x1591 | 484 KB | resident_tosil |
| assets/room13-role-resident_tosil-batch-flustered-v1.webp | 988x1591 | 534 KB | resident_tosil |
| assets/room13-role-resident_tosil-batch-joy-v1.webp | 986x1595 | 585 KB | resident_tosil |
| assets/room13-role-resident_tosil-batch-surprise-v1.webp | 988x1591 | 599 KB | resident_tosil |
| assets/ui-b-options/daram_diary_sticker_acorn.png | 369x437 | 271 KB | daram |
| assets/ui-b-options/daram_diary_sticker_emphasis.png | 432x274 | 187 KB | daram |
| assets/ui-b-options/daram_diary_sticker_gingham_tape.png | 464x239 | 200 KB | daram |
| assets/ui-b-options/daram_diary_sticker_letter.png | 408x318 | 221 KB | daram |
| assets/ui-b-options/daram_diary_sticker_magnifier.png | 404x422 | 268 KB | daram |
| assets/ui-b-options/daram_diary_sticker_star.png | 368x360 | 211 KB | daram |
| assets/winter-guard.webp | 1536x1024 | 219 KB | guard |

</details>

## B2. 살아 있는 공통 코드·읽는 표가 이름으로 부름(UI·연출·자료 아이콘 등) (489개, 129.5 MB)

| 폴더 | 파일 수 | 용량 |
|---|---|---|
| (assets 바로 아래) | 310 | 58.5 MB |
| resident-poses-a | 72 | 32.7 MB |
| hidden-places | 6 | 8.5 MB |
| wild-night | 5 | 7.8 MB |
| special-scenes | 8 | 6.6 MB |
| ui-b-main | 6 | 5.5 MB |
| map-village-b | 3 | 3.7 MB |
| investigation-jobs-20261018 | 2 | 1.6 MB |
| room13-stove | 19 | 1.3 MB |
| map-b | 15 | 1.1 MB |
| ui-b-options | 10 | 1.0 MB |
| ui-b-question | 7 | 0.4 MB |
| resident-props-20261024 | 6 | 0.3 MB |
| panseol | 1 | 0.2 MB |
| ui-b-dialogue | 2 | 0.1 MB |
| solbang-chinchilla-map | 2 | 0.1 MB |
| map-action27 | 1 | 0.1 MB |
| field-dot-v2 | 5 | 0.0 MB |
| diary-sounds | 3 | 0.0 MB |
| map-status | 1 | 0.0 MB |
| ui-field-stickers | 2 | 0.0 MB |
| ui-b-field | 2 | 0.0 MB |
| ui-night | 1 | 0.0 MB |

<details><summary>B2. 살아 있는 공통 코드·읽는 표가 이름으로 부름(UI·연출·자료 아이콘 등) 전체 489개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/Pretendard-ExtraBold.otf |  | 1532 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/Pret |
| assets/after.mp3 |  | 1252 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/approach.png | 1672x941 | 2511 KB | dead:room13_dialogue_openings_20261013.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-too |
| assets/back.png | 72x72 | 3 KB | dead:systems/room13_debate.rpy; dead:systems/room13_gimmicks.rpy; dead:systems/room13_granny_reply.rpy; dead:s |
| assets/bgm-title.mp3 |  | 2820 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:options.rpy; live:sy |
| assets/carriage.png | 1672x941 | 1817 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/comic.mp3 |  | 901 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/council.png | 1672x941 | 2289 KB | dead:systems/room13_ep4_night13.rpy; dead:systems/room13_ep6_cart.rpy; json-unloaded:asset-toolbox/bindings.js |
| assets/diary-sounds/evidence-paper.mp3 |  | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_diary |
| assets/diary-sounds/notebook-open.ogg |  | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_diary |
| assets/diary-sounds/paper-selection.mp3 |  | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_button_states |
| assets/door.wav |  | 38 KB | dead:room13_revision.rpy; dead:systems/room13_ep3_woodfire.rpy; dead:systems/room13_life_closeups.rpy; json-un |
| assets/evidence.png | 72x72 | 6 KB | dead:room13_record_compare.rpy; dead:systems/room13_bundle3.rpy; dead:systems/room13_debate.rpy; dead:systems/ |
| assets/family.png | 1536x1024 | 1749 KB | dead:systems/room13_ep6_cart.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/field-dot-v2/workshop/activity.webp | 182x186 | 9 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/field-dot-v2/workshop/distressed.webp | 184x190 | 7 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/field-dot-v2/workshop/expressive.webp | 202x201 | 8 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/field-dot-v2/workshop/neutral.webp | 163x209 | 7 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/field-dot-v2/workshop/thinking.webp | 148x199 | 8 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/hall.png | 1672x941 | 1593 KB | dead:systems/room13_alibi.rpy; dead:systems/room13_ep4_night13.rpy; dead:systems/room13_inn_change.rpy; dead:s |
| assets/hidden-places/hidden-a1-closed.webp | 2172x724 | 1459 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/hidden-places/hidden-a1-open.webp | 2172x724 | 1445 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/hidden-places/hidden-a2-interior.webp | 2172x724 | 1570 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/hidden-places/hidden-p1-doorway.webp | 2172x724 | 1523 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/hidden-places/hidden-p2-inner.webp | 2173x724 | 1357 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/hidden-places/hidden-p2-wood.webp | 2170x725 | 1342 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_hidde |
| assets/inn.png | 1774x887 | 896 KB | dead:room13_inn_navigation_v4.rpy; dead:room13_week2.rpy; dead:room13_worldmap_v5.rpy; dead:systems/room13_ali |
| assets/investigate.png | 72x72 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/investigation-jobs-20261018/chorong-replace-lightstone-v1.webp | 1014x1551 | 615 KB | json-loaded:assets/room13-field-dot-v2.json; json-loaded:assets/room13-map-action27.json; json-loaded:assets/r |
| assets/investigation-jobs-20261018/musoe-inspect-old-tool-v1.webp | 1024x1536 | 982 KB | json-loaded:assets/room13-field-dot-v2.json; json-loaded:assets/room13-map-action27.json; json-loaded:assets/r |
| assets/kitchen.png | 1774x887 | 1558 KB | dead:systems/room13_ep3_woodfire.rpy; dead:systems/room13_ep4_night13.rpy; dead:systems/room13_episodes.rpy; d |
| assets/lock.png | 72x72 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/map-action27/seori-threequarter-review.webp | 526x768 | 75 KB | json-loaded:assets/room13-field-dot-v2.json; json-loaded:assets/room13-seori-review-art.json; json-unloaded:as |
| assets/map-b/forest_abandoned_greenhouse.webp | 640x577 | 123 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_base.webp | 1136x570 | 208 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_cover_altar.webp | 640x442 | 46 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_cover_greenhouse.webp | 640x366 | 48 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_forest_path.webp | 640x585 | 105 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_mountain_altar.webp | 640x569 | 95 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/forest_protection_facility.webp | 640x453 | 87 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_base.webp | 1136x570 | 75 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_corridor.webp | 512x512 | 52 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_dining.webp | 512x512 | 61 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_hidden_passage.webp | 512x512 | 39 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_kitchen.webp | 512x512 | 56 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_reception.webp | 512x512 | 62 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_room13.webp | 512x512 | 51 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-b/inn_temporary_guestroom.webp | 512x512 | 52 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_b.rpy |
| assets/map-status/current_location.png | 96x96 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_village_b |
| assets/map-village-b/b_panel_small_trimmed.png | 224x44 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_village_b |
| assets/map-village-b/notebook_frame_1280x720.png | 1280x720 | 360 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_village_b |
| assets/map-village-b/village_clean.png | 1642x958 | 3418 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_village_b |
| assets/meeting.mp3 |  | 1024 KB | dead:systems/room13_ep1_lamp_thief.rpy; dead:systems/room13_ep2_kids.rpy; dead:systems/room13_q1_arguments.rpy |
| assets/menu.png | 72x72 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/move.png | 72x72 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/night.mp3 |  | 980 KB | dead:room13_week2.rpy; dead:systems/room13_bundle3.rpy; dead:systems/room13_ep1_lamp_thief.rpy; dead:systems/r |
| assets/notebook.png | 72x72 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/panseol/panseol-face.webp | 470x470 | 170 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_panse |
| assets/present.png | 72x72 | 5 KB | dead:systems/room13_debate.rpy; dead:systems/room13_meeting_flow.rpy; json-unloaded:asset-toolbox/bindings.jso |
| assets/press.png | 72x72 | 5 KB | dead:systems/room13_debate.rpy; dead:systems/room13_meeting_flow.rpy; dead:systems/room13_q1_arguments.rpy; de |
| assets/pressure.mp3 |  | 805 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/record.png | 72x72 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/resident-poses-a/badook-lantern-patrol-noborder.webp | 1078x1547 | 744 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/badook-lantern-patrol.webp | 1078x1547 | 264 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/bori-tie-firewood-noborder.webp | 1016x1292 | 760 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/bori-tie-firewood.webp | 1016x1292 | 242 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/dalgeurak-pots-display-noborder.webp | 1017x1441 | 783 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/dalgeurak-pots-display.webp | 1017x1441 | 301 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/eunho-ledger-noborder.webp | 1040x1536 | 605 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/eunho-ledger.webp | 1040x1536 | 224 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/guldol-stone-tapping-noborder.webp | 816x1524 | 653 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/guldol-stone-tapping.webp | 816x1524 | 251 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/guseul-scale-noborder.webp | 1070x1545 | 537 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/guseul-scale.webp | 1070x1545 | 198 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/hyeoni-lute-noborder.webp | 1028x1564 | 751 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/hyeoni-lute.webp | 1028x1564 | 287 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/jongjong-pack-mailbag-noborder.webp | 725x1527 | 484 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/jongjong-pack-mailbag.webp | 725x1527 | 187 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/jongjong-sort-letters-noborder.webp | 786x1499 | 550 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/jongjong-sort-letters.webp | 786x1499 | 216 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kalbaram-examine-ground-noborder.webp | 1324x1482 | 809 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kalbaram-examine-ground.webp | 1324x1482 | 294 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-bang-play-noborder.webp | 765x1523 | 611 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-bang-play.webp | 765x1523 | 216 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-kkam-play-noborder.webp | 1017x1494 | 694 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-kkam-play.webp | 1017x1494 | 260 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-mong-play-noborder.webp | 973x1488 | 834 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kid-mong-play.webp | 973x1488 | 283 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kkwak-haul-net-noborder.webp | 1350x1135 | 867 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kkwak-haul-net.webp | 1350x1135 | 335 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kongi-meeting-seated-noborder.webp | 975x1489 | 674 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/kongi-meeting-seated.webp | 975x1489 | 250 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/lamplighter-lightstone-noborder.webp | 798x1507 | 620 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/lamplighter-lightstone.webp | 798x1507 | 239 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/librarian-bookpaper-noborder.webp | 998x1523 | 666 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/librarian-bookpaper.webp | 998x1523 | 249 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/momo-lampnumber-noborder.webp | 655x1332 | 441 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/momo-lampnumber.webp | 655x1332 | 176 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/mulgyeol-rope-coiling-noborder.webp | 948x1525 | 767 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/mulgyeol-rope-coiling.webp | 948x1525 | 297 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/mungchi-store-boxes-noborder.webp | 1027x1500 | 718 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/mungchi-store-boxes.webp | 1027x1500 | 275 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/musoe-inspect-tool-noborder.webp | 814x1500 | 640 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/musoe-inspect-tool.webp | 814x1500 | 240 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/nubi-tie-laundry-noborder.webp | 982x1556 | 724 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/nubi-tie-laundry.webp | 982x1556 | 273 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/owlgp-notebook-noborder.webp | 985x1533 | 764 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/owlgp-notebook.webp | 985x1533 | 267 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/piko-paint-sketchboard-noborder.webp | 871x1508 | 644 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/piko-paint-sketchboard.webp | 871x1508 | 227 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/ppul-meeting-seated-noborder.webp | 875x1454 | 605 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/ppul-meeting-seated.webp | 875x1454 | 228 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/seol-bellrope-noborder.webp | 782x1390 | 568 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/seol-bellrope.webp | 782x1390 | 213 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/seori-meeting-seated-noborder.webp | 892x1478 | 555 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/seori-meeting-seated.webp | 892x1478 | 192 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/siluk-event-whisper-noborder.webp | 892x1533 | 682 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/siluk-event-whisper.webp | 892x1533 | 247 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/sling-event-steam-noborder.webp | 974x1349 | 610 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/sling-event-steam.webp | 974x1349 | 221 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/solbang-herb-bundle-noborder.webp | 1031x1521 | 918 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/solbang-herb-bundle.webp | 1031x1521 | 322 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/teacher-wet-coat-noborder.webp | 1000x1547 | 855 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/teacher-wet-coat.webp | 1000x1547 | 299 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tok-repair-lantern-noborder.webp | 977x1555 | 685 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tok-repair-lantern.webp | 977x1555 | 252 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tori-meeting-seated-noborder.webp | 786x1585 | 645 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tori-meeting-seated.webp | 786x1585 | 238 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tosil-thermos-noborder.webp | 738x1506 | 543 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/tosil-thermos.webp | 738x1506 | 195 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/ttadak-doorframe-noborder.webp | 1012x1511 | 692 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/ttadak-doorframe.webp | 1012x1511 | 256 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/yeoni-mend-noborder.webp | 1042x1543 | 810 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-poses-a/yeoni-mend.webp | 1042x1543 | 266 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/resident-props-20261024/sticker_cord.webp | 256x256 | 49 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/resident-props-20261024/sticker_hat.webp | 256x256 | 46 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/resident-props-20261024/sticker_herbs.webp | 256x256 | 46 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/resident-props-20261024/sticker_lamp_oil.webp | 256x256 | 35 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/resident-props-20261024/sticker_postcard.webp | 256x256 | 48 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/resident-props-20261024/sticker_snack.webp | 256x256 | 39 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room.png | 1774x887 | 1461 KB | dead:room13_week2.rpy; dead:systems/room13_inn_change.rpy; dead:systems/room13_town_events.rpy; dead:systems/r |
| assets/room13-ep-O38-shelter-full.webp | 1983x793 | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O39-two-pots.webp | 1983x793 | 23 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O40-spilled.webp | 1983x793 | 21 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O41-four-blankets.webp | 1983x793 | 36 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O42-evac-list.webp | 1983x793 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O43-cabinet-gap.webp | 2048x768 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O44-hideout-empty.webp | 2172x724 | 15 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O45-ancient-shelf.webp | 2172x724 | 19 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O46-mountain-ropes.webp | 2048x768 | 30 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O48-chisel.webp | 2048x768 | 24 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O49-cart.webp | 2048x768 | 60 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-O50-cart-list.webp | 2048x768 | 16 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-U00-open-book.webp | 1280x720 | 125 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-U21-bell-01.webp | 256x384 | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-U21-bell-02.webp | 256x384 | 14 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-U21-bell-03.webp | 256x384 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-U21-soundwaves.webp | 2048x768 | 77 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-ep-icon-F02.webp | 300x300 | 26 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F03.webp | 300x300 | 18 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F04.webp | 300x300 | 26 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F05.webp | 300x300 | 19 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F06.webp | 300x300 | 14 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F07.webp | 300x300 | 21 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F09.webp | 300x300 | 27 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F10.webp | 300x300 | 27 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-F13.webp | 300x300 | 24 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-K04.webp | 300x300 | 26 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-K05.webp | 300x300 | 33 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-K08.webp | 300x300 | 20 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L01.webp | 300x300 | 28 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L02.webp | 300x300 | 22 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L03.webp | 300x300 | 20 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L04.webp | 300x300 | 23 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L07.webp | 300x300 | 22 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L09.webp | 300x300 | 18 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L10.webp | 300x300 | 17 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L12.webp | 300x300 | 36 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L13.webp | 300x300 | 32 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-L14.webp | 300x300 | 29 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-N01.webp | 300x300 | 22 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-N05.webp | 300x300 | 21 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-N06.webp | 300x300 | 16 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-N07.webp | 300x300 | 19 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-N08.webp | 300x300 | 17 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V00.webp | 300x300 | 23 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V01.webp | 300x300 | 17 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V02.webp | 300x300 | 13 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V03.webp | 300x300 | 25 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V04.webp | 300x300 | 37 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V06.webp | 300x300 | 28 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-V08.webp | 300x300 | 21 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y02.webp | 300x300 | 15 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y03.webp | 300x300 | 18 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y05.webp | 300x300 | 27 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y06.webp | 300x300 | 28 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y07.webp | 300x300 | 17 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y08.webp | 300x300 | 29 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y09.webp | 300x300 | 27 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y10.webp | 300x300 | 25 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y11.webp | 300x300 | 14 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y12.webp | 300x300 | 23 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ep-icon-Y14.webp | 300x300 | 25 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-fx-bleed.png | 1280x720 | 182 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-card-glow.webp | 360x360 | 7 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-e0.webp | 832x466 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-e2.webp | 832x467 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-e3.webp | 832x467 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-e4.webp | 832x466 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-e5.webp | 832x466 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-mountain.webp | 832x467 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-proof.webp | 832x467 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-rescue.webp | 832x466 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-return.webp | 832x466 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-cine-reunion.webp | 832x467 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-dither.png | 1280x720 | 3 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-edge-vignette.webp | 1280x720 | 22 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-evidence-sparkle.webp | 768x128 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-carriage-0.webp | 1200x1200 | 19 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e0-0.webp | 288x288 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e2-0.webp | 324x324 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e3-0.webp | 216x216 | 8 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e3-1.webp | 216x216 | 8 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e3-2.webp | 252x252 | 9 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e4-0.webp | 288x288 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e5-0.webp | 288x288 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-e5-1.webp | 252x252 | 10 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-mountain-0.webp | 324x324 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-proof-0.webp | 540x540 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-rescue-0.webp | 324x324 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-return-0.webp | 324x324 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-cine-reunion-0.webp | 324x324 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-clinic-evening-0.webp | 816x816 | 16 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-facility-evening-0.webp | 816x816 | 16 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-greenhouse-evening-0.webp | 748x748 | 15 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-afternoon-0.webp | 1240x1240 | 20 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-0.webp | 1640x1640 | 29 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-1.webp | 560x560 | 15 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-2.webp | 480x480 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-3.webp | 520x520 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-4.webp | 520x520 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-5.webp | 220x220 | 8 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-evening-6.webp | 220x220 | 8 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-inn-morning-0.webp | 1240x1240 | 20 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-school-evening-0.webp | 884x884 | 16 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-square-evening-0.webp | 440x440 | 13 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-store-evening-0.webp | 1020x1020 | 17 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-0.webp | 144x144 | 6 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-1.webp | 120x120 | 5 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-2.webp | 96x96 | 3 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-3.webp | 88x88 | 3 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-4.webp | 80x80 | 3 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-5.webp | 102x102 | 4 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-title-6.webp | 128x128 | 5 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-workshop-evening-0.webp | 748x748 | 15 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-glow-workshop-evening-1.webp | 748x748 | 15 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-inn-fire-afternoon.webp | 1536x156 | 69 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-inn-fire-evening.webp | 1536x156 | 77 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-inn-fire-morning.webp | 1536x156 | 67 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-inn-glow.webp | 2048x768 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-inn-window-mask.webp | 456x212 | 2 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-clinic.webp | 2048x768 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-facility.webp | 2048x768 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-greenhouse.webp | 2048x768 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-school.webp | 1983x793 | 1 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-store.webp | 2048x768 | 1 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-lamp-workshop.webp | 1983x793 | 1 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-carriage.webp | 1280x720 | 6 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-e0.webp | 832x466 | 18 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-e2.webp | 832x467 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-e3.webp | 832x467 | 35 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-e4.webp | 832x466 | 18 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-e5.webp | 832x466 | 29 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-mountain.webp | 832x467 | 11 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-proof.webp | 832x467 | 16 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-rescue.webp | 832x466 | 15 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-return.webp | 832x466 | 17 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-cine-reunion.webp | 832x467 | 14 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-clinic-evening.webp | 2048x768 | 35 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-facility-evening.webp | 2048x768 | 21 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-greenhouse-evening.webp | 2048x768 | 33 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-inn-afternoon.webp | 2048x768 | 25 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-inn-evening.webp | 2048x768 | 46 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-inn-morning.webp | 2048x768 | 25 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-school-evening.webp | 1983x793 | 32 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-square-evening.webp | 2048x768 | 12 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-store-evening.webp | 2048x768 | 24 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-title.webp | 1280x720 | 37 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-shade-workshop-evening.webp | 1983x793 | 46 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-12-0.webp | 12x12 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-12-1.webp | 12x12 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-12-2.webp | 12x12 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-4-0.webp | 4x4 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-4-1.webp | 4x4 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-4-2.webp | 4x4 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-8-0.webp | 8x8 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-8-1.webp | 8x8 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-smoke-8-2.webp | 8x8 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-snow-big.webp | 8x8 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-snow-small.webp | 4x4 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-square-lampglow.webp | 2048x768 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-storybook-frame.webp | 1280x720 | 89 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-sway-inn-afternoon.webp | 2048x768 | 38 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-sway-inn-evening.webp | 2048x768 | 47 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-sway-inn-morning.webp | 2048x768 | 38 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-fx-title-glow.webp | 1280x720 | 0 KB | json-loaded:assets/room13-dot-fx.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-meeting-seated-resident_tori068.webp | 966x1629 | 188 KB | json-loaded:assets/room13-resident-poses-a.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asse |
| assets/room13-pixel-acting-workshop.webp | 1536x1024 | 274 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-altar-afternoon.webp | 1672x941 | 316 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-altar-evening.webp | 1672x941 | 295 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-altar-morning.webp | 1672x941 | 303 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-carriage-family015-morning.webp | 1672x941 | 300 KB | json-loaded:assets/room13-cinematics.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-carriage-letter0153-morning.webp | 1672x941 | 302 KB | json-loaded:assets/room13-cinematics.json; json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-t |
| assets/room13-pixel-carriage-morning.webp | 1672x941 | 293 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-cinematic-endA-family015.webp | 1672x941 | 380 KB | json-loaded:assets/room13-cinematics.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-cinematic-endA.webp | 1672x941 | 417 KB | json-loaded:assets/room13-cinematics.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-cinematic-endB-family015.webp | 1672x941 | 398 KB | json-loaded:assets/room13-cinematics.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-cinematic-key-family015.webp | 1672x941 | 379 KB | json-loaded:assets/room13-cinematics.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-evidence0155.webp | 1448x1086 | 286 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-pixel-gate-afternoon.webp | 1672x941 | 341 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-gate-evening.webp | 1672x941 | 312 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-gate-morning.webp | 1672x941 | 348 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-after-afternoon.webp | 1672x941 | 185 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-after-evening.webp | 1672x941 | 152 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-after-morning.webp | 1672x941 | 195 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-before-afternoon.webp | 1672x941 | 186 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-before-evening.webp | 1672x941 | 160 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-hall-before-morning.webp | 1672x941 | 199 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-inn-afternoon.webp | 1672x941 | 330 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-inn-evening.webp | 1672x941 | 319 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-inn-morning.webp | 1672x941 | 312 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-inspect-desk-nomemo.webp | 1672x941 | 448 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_inspection.rp |
| assets/room13-pixel-inspect-desk.webp | 1672x941 | 112 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-drawer-held.webp | 240x240 | 13 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-drawer-open.webp | 1672x941 | 982 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-drawer.webp | 1672x941 | 150 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-items.webp | 1295x1214 | 141 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-rubbing-done.webp | 610x300 | 158 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-inspect-rubbing-paper.webp | 610x300 | 83 KB | json-loaded:room13-inspection-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-tool |
| assets/room13-pixel-locations-afternoon.webp | 2046x768 | 467 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-locations-evening.webp | 2046x768 | 396 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-locations-morning.webp | 2046x768 | 453 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-material-icons079-objects.webp | 1122x1402 | 773 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room13-pixel-material-icons079-records1.webp | 1254x1254 | 908 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room13-pixel-material-icons079-records2.webp | 1254x1254 | 890 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room13-pixel-material-icons079-records3.webp | 1254x1254 | 928 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room13-pixel-material-icons079-records4.webp | 1254x1254 | 724 KB | json-loaded:assets/room13-material-icons079.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:ass |
| assets/room13-pixel-meeting-altar-standing072.webp | 1672x941 | 380 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_seati |
| assets/room13-pixel-meeting-interview066.webp | 1672x941 | 362 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_seati |
| assets/room13-pixel-meeting-room056.webp | 1672x941 | 372 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_seati |
| assets/room13-pixel-overview-afternoon.webp | 1672x941 | 365 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-overview-evening.webp | 1672x941 | 353 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-overview-morning.webp | 1672x941 | 392 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-panorama-belltower-night.webp | 2048x768 | 358 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-eaves-afternoon.webp | 2048x768 | 381 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-hall-front-afternoon.webp | 2048x768 | 416 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-holding-night.webp | 2048x768 | 235 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-roof-evening.webp | 2048x768 | 413 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-roof-night.webp | 2048x768 | 382 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-panorama-square-spring.webp | 2048x768 | 400 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-ready-store0177-afternoon.webp | 2048x768 | 308 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-ready-store0177-evening.webp | 2048x768 | 274 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-ready-store0177-morning.webp | 2048x768 | 307 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-room-after-afternoon.webp | 1672x941 | 224 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-room-after-evening.webp | 1672x941 | 190 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-room-after-morning.webp | 1672x941 | 246 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-room-before-afternoon.webp | 1672x941 | 218 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-room-before-evening.webp | 1672x941 | 193 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-room-before-morning.webp | 1672x941 | 239 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-village-afternoon.webp | 1672x941 | 430 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-village-evening.webp | 1672x941 | 403 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-village-morning.webp | 1672x941 | 441 KB | json-loaded:assets/room13-pixel-layouts.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-t |
| assets/room13-pixel-wide-hall-cell-evening.webp | 2172x724 | 127 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-wide-hideout-afternoon.webp | 2172x724 | 259 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-wide-market-afternoon.webp | 2172x724 | 418 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-market-evening.webp | 2172x724 | 386 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-market-morning.webp | 2172x724 | 404 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-passage-afternoon.webp | 2172x724 | 183 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-passage-evening.webp | 2172x724 | 153 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-passage-morning.webp | 2172x724 | 169 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-river-afternoon.webp | 2172x724 | 226 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-river-evening.webp | 2172x724 | 171 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-river-morning.webp | 2172x724 | 213 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-pixel-wide-somi-home-afternoon.webp | 2172x724 | 259 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-wide-stable-afternoon.webp | 2172x724 | 161 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_ep_ar |
| assets/room13-pixel-world-context0156.webp | 2171x724 | 223 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-prop-inn-doorframe-repair.webp | 256x384 | 16 KB | json-loaded:assets/room13-world-layout.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/room13-record-m01.webp | 362x362 | 0 KB | json-loaded:assets/room13-evidence-icons.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/ashbin-ration-stone.webp | 38x18 | 1 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-after-afternoon.webp | 232x531 | 78 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-after-evening.webp | 232x531 | 67 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-after-morning.webp | 232x531 | 83 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-before-afternoon.webp | 232x531 | 74 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-before-evening.webp | 232x531 | 65 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-empty-before-morning.webp | 232x531 | 83 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-after-afternoon.webp | 232x531 | 77 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-after-evening.webp | 232x531 | 66 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-after-morning.webp | 232x531 | 82 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-before-afternoon.webp | 232x531 | 73 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-before-evening.webp | 232x531 | 65 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-inner-before-morning.webp | 232x531 | 82 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-after-afternoon.webp | 232x531 | 78 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-after-evening.webp | 232x531 | 66 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-after-morning.webp | 232x531 | 82 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-before-afternoon.webp | 232x531 | 73 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-before-evening.webp | 232x531 | 65 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-stove/stove-ration-before-morning.webp | 232x531 | 82 KB | json-loaded:assets/room13-stove/manifest.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/room13-ui-objection01917.webp | 1943x510 | 567 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_meeti |
| assets/save.png | 72x72 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/search.mp3 |  | 805 KB | dead:room13_week2.rpy; dead:systems/room13_bundle3.rpy; dead:systems/room13_ep1_lamp_thief.rpy; dead:systems/r |
| assets/sfx-bell.wav |  | 115 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-click.wav |  | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_options.rpy;  |
| assets/sfx-clue.wav |  | 85 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-comic.wav |  | 42 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-creak.wav |  | 49 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-door-close.wav |  | 54 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-door-open.wav |  | 79 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-error.wav |  | 9 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-evidence-get.wav |  | 57 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-heartbeat.wav |  | 120 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-knock.wav |  | 64 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-latch.wav |  | 19 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-mystery.wav |  | 463 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-note-close.wav |  | 20 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-note-open.wav |  | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-page.wav |  | 80 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-pencil.wav |  | 103 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-present.wav |  | 21 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_impac |
| assets/sfx-right.wav |  | 80 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-save.wav |  | 97 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-slam.wav |  | 21 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_impac |
| assets/sfx-surprise.wav |  | 53 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-unlock.wav |  | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-walk-snow.wav |  | 151 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-walk-wood.wav |  | 151 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/sfx-wrong.wav |  | 10 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_sound |
| assets/solbang-chinchilla-map/neutral.webp | 280x420 | 39 KB | json-loaded:assets/room13-field-dot-v2.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-to |
| assets/solbang-chinchilla-map/work_herb_bundle.webp | 284x420 | 41 KB | json-loaded:assets/room13-field-dot-v2.json; json-loaded:assets/room13-resident-poses-a.json; json-unloaded:as |
| assets/source-heartbeat.wav |  | 47 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-shock9.wav |  | 14 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-silence.wav |  | 17 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-wood-door-close.wav |  | 51 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/special-scenes/bori_adopts_four_alive.webp | 1387x1134 | 928 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/bori_cares_three_after_dodam_loss.webp | 1312x1199 | 1037 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/bori_kneels_holding_dodam_hand.webp | 1536x1024 | 796 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/bori_silent_single_shoe.webp | 1189x1323 | 825 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/chorong_injured_alive.webp | 1536x1024 | 750 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/nero_weakened_alive.webp | 1254x1254 | 688 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/teacher_blanket_dodam_only.webp | 1536x1024 | 796 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/special-scenes/teacher_blanket_four_children.webp | 1536x1024 | 921 KB | json-loaded:assets/room13-special-scenes.json; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset- |
| assets/table.png | 2120x742 | 1619 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/talk.png | 64x64 | 3 KB | dead:room13_dialogue_openings_20261013.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-too |
| assets/travel.mp3 |  | 1778 KB | dead:room13_week2.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; js |
| assets/type.wav |  | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/ui-b-dialogue/b_panel_dialogue.png | 1200x160 | 134 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy; live:sy |
| assets/ui-b-dialogue/b_ribbon_name.png | 200x56 | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy; live:sy |
| assets/ui-b-field/b_icon_acorn.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_map_village_b |
| assets/ui-b-field/b_icon_pin.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_screens.rpy;  |
| assets/ui-b-main/b_button.png | 160x52 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_title_art.rpy |
| assets/ui-b-main/b_button_primary.png | 160x52 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_title_art.rpy |
| assets/ui-b-main/b_logo.png | 900x300 | 233 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-main/b_main_background_postcard.png | 1672x941 | 3053 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-main/b_main_cast_poster_plain.png | 1122x1402 | 2245 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-main/b_main_panel.png | 620x300 | 134 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_ui_art.rpy; l |
| assets/ui-b-options/b_opt_bar_fill.png | 312x52 | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_bar_thumb.png | 68x68 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_bar_track.png | 312x52 | 9 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_close.png | 88x88 | 7 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy; live:sy |
| assets/ui-b-options/b_opt_divider.png | 1224x38 | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_panel.png | 1288x728 | 919 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_retry |
| assets/ui-b-options/b_opt_sticker_corner.png | 152x152 | 27 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_retry |
| assets/ui-b-options/b_opt_tab.png | 238x94 | 15 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_tab_selected.png | 238x94 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/ui-b-options/b_opt_title_tape.png | 182x76 | 10 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_meeting_retry |
| assets/ui-b-question/b_icon_acorn.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_noteb |
| assets/ui-b-question/b_icon_acorn_done.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_side_ |
| assets/ui-b-question/b_panel_book.png | 760x540 | 340 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_side_ |
| assets/ui-b-question/b_panel_card.png | 672x116 | 43 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_side_ |
| assets/ui-b-question/b_tab_title.png | 320x64 | 15 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_side_ |
| assets/ui-b-question/b_tape_red.png | 96x28 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_noteb |
| assets/ui-b-question/nameplate_paper.png | 232x96 | 18 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_side_ |
| assets/ui-field-stickers/diary.png | 160x96 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_ui_art.rpy |
| assets/ui-field-stickers/ring.png | 28x34 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:room13_ui_art.rpy |
| assets/ui-night/diamond.png | 8x8 | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:screens.rpy |
| assets/wild-night/wild-greenhouse-night.webp | 2048x768 | 1328 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_wild_ |
| assets/wild-night/wild-road-mouth-night.webp | 2048x768 | 1921 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_wild_ |
| assets/wild-night/wild-school-classroom-night.webp | 1983x793 | 1602 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_wild_ |
| assets/wild-night/wild-school-hall-night.webp | 1983x793 | 1231 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_wild_ |
| assets/wild-night/wild-square-burning.webp | 2048x768 | 1898 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; live:systems/room13_wild_ |

</details>

## B3. 살아 있는 코드가 계산한 경로로 부름(%s 등) (64개, 21.4 MB)

| 폴더 | 파일 수 | 용량 |
|---|---|---|
| (assets 바로 아래) | 46 | 18.4 MB |
| panseol | 3 | 3.0 MB |
| ui-field-stickers | 12 | 0.0 MB |
| ui-b-field | 3 | 0.0 MB |

<details><summary>B3. 살아 있는 코드가 계산한 경로로 부름(%s 등) 전체 64개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/panseol/panseol-anxious.webp | 1024x1536 | 1010 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/panseol/panseol-neutral.webp | 1024x1536 | 1013 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/panseol/panseol-tired.webp | 1024x1536 | 1014 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/room13-ep-U01-ending.webp | 900x600 | 163 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U01-opening.webp | 900x600 | 170 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U02-ending.webp | 900x600 | 206 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U02-opening.webp | 900x600 | 219 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U03-ending.webp | 900x600 | 215 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U03-opening.webp | 900x600 | 236 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U04-ending.webp | 900x600 | 191 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U04-opening.webp | 900x600 | 200 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U05-ending-open-window.webp | 900x600 | 93 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U05-ending-prince.webp | 900x600 | 91 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U05-opening.webp | 900x600 | 148 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U06-ending.webp | 900x600 | 194 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U06-opening.webp | 900x600 | 200 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U07-ending.webp | 900x600 | 169 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U07-opening.webp | 900x600 | 159 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-ep-U22-mother-portrait-crayon-nose.webp | 1280x720 | 116 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-ep-U23-small-handprint.webp | 1280x720 | 78 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_v111_ |
| assets/room13-pixel-acting-guseul.webp | 1536x1024 | 236 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-madam.webp | 1536x1024 | 218 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-momo.webp | 1536x1024 | 220 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-mungchi.webp | 1536x1024 | 208 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-nubi.webp | 1536x1024 | 267 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-piko.webp | 1536x1024 | 265 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-acting-siluk.webp | 1536x1024 | 228 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-cinematic-endB.webp | 1672x941 | 427 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_life. |
| assets/room13-pixel-cinematic-ending-E0074.webp | 1672x941 | 428 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E1074.webp | 1672x941 | 364 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E2074.webp | 1672x941 | 472 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E3074.webp | 1672x941 | 449 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E4074.webp | 1672x941 | 410 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E5074.webp | 1672x941 | 473 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-ending-E6074.webp | 1672x941 | 493 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-pixel-cinematic-key.webp | 1672x941 | 430 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:room13_life. |
| assets/room13-pixel-dialogue-support-00.webp | 1536x1024 | 337 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-dialogue-support-01.webp | 1536x1024 | 382 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-dialogue-support-02.webp | 1536x1024 | 357 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-dialogue-support-04.webp | 1536x1024 | 351 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-dialogue-support-09.webp | 1536x1024 | 334 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-dialogue-support-10.webp | 1536x1024 | 354 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-pixel-life-delivery-after.webp | 1672x941 | 1358 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-life-delivery-before.webp | 1672x941 | 1503 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-life-door-after.webp | 1672x941 | 990 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-life-door-before.webp | 1672x941 | 962 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-life-meal-after.webp | 1672x941 | 1403 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-life-meal-before.webp | 1672x941 | 1313 KB | dead:systems/room13_life_closeups.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/ |
| assets/room13-pixel-navigation-village.webp | 1672x941 | 772 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/ui-b-field/b_icon_book.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-b-field/b_icon_map.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-b-field/b_icon_more.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/arrow_left_basic.png | 72x72 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/arrow_left_hover.png | 72x72 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/arrow_right_basic.png | 72x72 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/arrow_right_hover.png | 72x72 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/label_basic.png | 96x36 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/label_hover.png | 96x36 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/paper_basic.png | 160x64 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/paper_hover.png | 160x64 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/place_basic.png | 160x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/place_hover.png | 160x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/primary_basic.png | 160x64 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |
| assets/ui-field-stickers/primary_hover.png | 160x64 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-live:systems/room |

</details>

## 쓰지 않는 파일 (C·C2·C3·D, 188.6 MB)

### C. 옛 판 코드·읽지 않는 표에서만 이름이 나옴 — 297개, 137.9 MB

| 폴더/이름 묶음 | 파일 수 | 용량 |
|---|---|---|
| room13-* | 80 | 23.5 MB |
| outdoor-* | 6 | 15.5 MB |
| source-* | 24 | 14.4 MB |
| r13-* | 13 | 14.3 MB |
| interview-* | 5 | 10.6 MB |
| ui-b-main | 6 | 7.0 MB |
| village-* | 3 | 5.7 MB |
| inn-* | 3 | 5.3 MB |
| gate-wide | 3 | 5.3 MB |
| winter-* | 4 | 5.1 MB |
| Pretendard-* | 2 | 3.0 MB |
| future-* | 1 | 2.0 MB |
| witnesses.png-* | 1 | 2.0 MB |
| Galmuri11.ttf-* | 1 | 1.9 MB |
| scholars.png-* | 1 | 1.9 MB |
| ui-b-sticker | 1 | 1.8 MB |
| driver.png-* | 1 | 1.8 MB |
| map-village-b | 13 | 1.7 MB |
| somsom.png-* | 1 | 1.7 MB |
| ui-b-choice | 1 | 1.5 MB |
| town-* | 1 | 1.5 MB |
| pouch.png-* | 1 | 1.5 MB |
| somsom-* | 1 | 1.4 MB |
| ms14-audio | 4 | 1.3 MB |
| friends.png-* | 1 | 1.1 MB |
| chest-* | 2 | 0.8 MB |
| pouch-* | 1 | 0.6 MB |
| basket-* | 1 | 0.5 MB |
| hidden-* | 1 | 0.4 MB |
| ui-b-field | 6 | 0.4 MB |
| flour-* | 1 | 0.4 MB |
| clock-* | 2 | 0.3 MB |
| ui-b-question | 17 | 0.2 MB |
| contract.png-* | 1 | 0.2 MB |
| cold-* | 7 | 0.2 MB |
| Room13Sans.ttf-* | 1 | 0.2 MB |
| ui-night | 14 | 0.2 MB |
| ui-b-options | 12 | 0.2 MB |
| seal.png-* | 1 | 0.1 MB |
| ui-button-states | 12 | 0.1 MB |

<details><summary>C. 옛 판 코드·읽지 않는 표에서만 이름이 나옴 전체 297개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/Galmuri11.ttf |  | 1918 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/Pretendard-Bold.otf |  | 1540 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/Pret |
| assets/Pretendard-Regular.otf |  | 1537 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/Room13Sans.ttf |  | 211 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/Room13TitleSerif.otf |  | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/basket-world.png | 1254x1254 | 498 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/chest-complete.png | 1254x1254 | 731 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/chest-open.png | 1774x887 | 125 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/chest.png | 1774x887 | 99 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/clock-base.png | 512x512 | 276 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/clock-hands.png | 512x512 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-0.wav |  | 47 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-1.wav |  | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-2.wav |  | 34 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-3.wav |  | 29 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-4.wav |  | 25 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-5.wav |  | 22 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/cold-heart-6.wav |  | 20 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/contract.png | 512x512 | 221 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/driver.png | 1672x941 | 1824 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/flour-world.png | 1365x1152 | 400 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/friends.png | 1774x887 | 1101 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/fur-stamp.png | 512x512 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/future-villagers-v3.png | 1536x1024 | 2053 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/gate-wide/gate-wide-afternoon.webp | 2560x960 | 1882 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/gate-wide/gate-wide-evening.webp | 2560x960 | 1722 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/gate-wide/gate-wide-morning.webp | 2560x960 | 1806 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/hidden-somsom.png | 1313x1198 | 423 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/inn-activities.png | 1536x1024 | 1529 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/inn-lounge.png | 1672x940 | 1465 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/inn-map.png | 1672x941 | 2459 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/interview-family.png | 1536x1024 | 2074 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/interview-friends.png | 1536x1024 | 2126 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/interview-inn.png | 1536x1024 | 2051 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/interview-scholars.png | 1536x1024 | 2287 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/interview-witnesses.png | 1536x1024 | 2283 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/map-b/notebook_frame.webp | 1280x720 | 55 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-status/locked.png | 96x96 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-status/map_selected.png | 96x96 | 14 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-status/new_dialogue.png | 96x96 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_button.png | 160x52 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_button_primary.png | 160x52 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_button_primary_trimmed.png | 128x32 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_button_trimmed.png | 128x32 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_icon_back.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_icon_map.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_icon_pin.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_panel_small.png | 240x60 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_tab_title.png | 320x64 | 15 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_tape_red.png | 96x28 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/b_tape_teal.png | 96x28 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/map_background_1136x570.png | 1136x570 | 1490 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/map-village-b/sticker_daram_stubborn.png | 512x512 | 207 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ms14-audio/SFX_cart_start.wav |  | 188 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ms14-audio/SFX_cart_stop.wav |  | 188 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ms14-audio/SFX_cart_wood_roll_loop.wav |  | 750 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ms14-audio/SFX_cloth_rub_quiet.wav |  | 188 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/outdoor-fountain.png | 1672x941 | 2745 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/outdoor-gate-morning.png | 1672x941 | 2984 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/outdoor-gate.png | 1672x941 | 2567 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/outdoor-inn.png | 1672x941 | 2635 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/outdoor-lane.png | 1672x941 | 2349 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/outdoor-post.png | 1672x941 | 2607 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/pouch-world.png | 1254x1254 | 603 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/pouch.png | 1671x941 | 1508 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/r13-gimmick-floor-closed.webp | 1672x941 | 940 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-floor-open.webp | 1672x941 | 1023 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-lamp-floor.webp | 1672x941 | 1153 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-note-open.webp | 1672x941 | 1009 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-package-closed.webp | 1672x941 | 1012 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-package-revealed.webp | 1672x941 | 1203 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-package-seam.webp | 1672x941 | 1087 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-scale-base.webp | 1672x941 | 1060 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-scale-loaded.webp | 1672x941 | 1094 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-scale-pivot.webp | 1672x941 | 867 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-stone-base.webp | 1672x941 | 1393 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-stone-paper.webp | 1672x941 | 1344 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/r13-gimmick-stone-rubbed.webp | 1672x941 | 1488 KB | dead:systems/room13_gimmicks.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catal |
| assets/room13-acorn-ink.png | 32x32 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/room13-aftermath-ep1.webp | 1671x941 | 488 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-ep2.webp | 1672x941 | 411 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-ep3.webp | 1672x941 | 456 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-ep4.webp | 1672x941 | 408 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-ep5.webp | 1671x941 | 390 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-ep6.webp | 1672x941 | 517 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-aftermath-extra.webp | 1672x941 | 445 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/room |
| assets/room13-before-after.png | 2048x768 | 1777 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-gate.png | 1672x941 | 1931 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-inn.png | 2048x768 | 1975 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-locations.png | 2048x768 | 2208 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-map-mountain-altar-outline.webp | 367x245 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-altar.webp | 367x245 | 91 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-facility-outline.webp | 543x289 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-facility.webp | 543x289 | 159 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-forest-outline.webp | 253x214 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-forest.webp | 253x214 | 60 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-greenhouse-outline.webp | 397x191 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain-greenhouse.webp | 397x191 | 97 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-mountain.webp | 1672x941 | 612 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:room13-cart |
| assets/room13-map-reveal-altar.webp | 472x320 | 200 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:room13-cart |
| assets/room13-map-reveal-greenhouse.webp | 440x330 | 205 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:room13-cart |
| assets/room13-map-village-clinic-base.webp | 388x200 | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-clinic-outline.webp | 388x200 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-clinic-pop.webp | 388x200 | 68 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-clinic.webp | 388x200 | 61 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-forest-outline.webp | 710x414 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-forest.webp | 710x414 | 288 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-gate-base.webp | 439x279 | 49 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-gate-outline.webp | 439x279 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-gate-pop.webp | 439x279 | 87 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-gate.webp | 439x279 | 75 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-inn-base.webp | 663x275 | 92 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-inn-outline.webp | 663x275 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-inn-pop.webp | 663x275 | 193 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-inn.webp | 663x275 | 174 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-laundry-base.webp | 295x138 | 25 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-laundry-outline.webp | 295x138 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-laundry-pop.webp | 295x138 | 43 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-laundry.webp | 295x138 | 37 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-market-base.webp | 459x166 | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-market-outline.webp | 459x166 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-market-pop.webp | 459x166 | 69 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-market.webp | 459x166 | 60 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-post-base.webp | 348x177 | 33 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-post-outline.webp | 348x177 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-post-pop.webp | 348x177 | 55 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-post.webp | 348x177 | 48 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-river-outline.webp | 1230x1035 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-river.webp | 1230x1035 | 394 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-school-base.webp | 533x178 | 47 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-school-outline.webp | 533x178 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-school-pop.webp | 533x178 | 96 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-school.webp | 533x178 | 87 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-somi-base.webp | 432x166 | 34 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-somi-outline.webp | 432x166 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-somi-pop.webp | 432x166 | 69 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-somi.webp | 432x166 | 62 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-square-base.webp | 234x167 | 24 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-square-outline.webp | 234x167 | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-square-pop.webp | 234x167 | 40 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-square.webp | 234x167 | 35 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-store-base.webp | 422x209 | 45 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-store-outline.webp | 422x209 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-store-pop.webp | 422x209 | 90 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-store.webp | 422x209 | 81 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-workshop-base.webp | 358x198 | 38 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-workshop-outline.webp | 358x198 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-workshop-pop.webp | 358x198 | 75 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village-workshop.webp | 358x198 | 67 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; pattern-dead:room13_world |
| assets/room13-map-village.webp | 2304x1344 | 3992 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:room13-cart |
| assets/room13-opening-coach-landscape.webp | 1672x941 | 217 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/room13-title-logo.webp | 2172x724 | 649 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/room13-title-winter020.webp | 1672x941 | 1718 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/room13-ui-inspect.svg |  | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-ui-move.svg |  | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-ui-present.svg |  | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-ui-talk.svg |  | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/room13-village.png | 1536x1024 | 2181 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/scholars.png | 1536x1024 | 1912 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/seal.png | 512x512 | 144 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/sfx-map-tick.wav |  | 8 KB | dead:room13_worldmap_v5.rpy; json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.js |
| assets/somsom-hidden-source.png | 1536x1024 | 1443 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/somsom.png | 1672x941 | 1742 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/sound-off.png | 72x72 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/sound-on.png | 72x72 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-INTRO02_bed.png | 1672x941 | 1611 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-INTRO03_door.png | 1672x941 | 1582 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-INTRO04_carriage_empty.png | 844x390 | 41 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-P10-inn-bedroom-lights-out-background-only-1672x941.png | 1672x941 | 1475 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-bell10.wav |  | 422 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-climax-strings-v3.mp3 |  | 939 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-cut9.wav |  | 28 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-found.wav |  | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-impact.wav |  | 23 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-investigation-context-v4.mp3 |  | 1024 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-knock.wav |  | 25 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-lock.wav |  | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-low9.wav |  | 41 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-meeting-press-strings-v3.mp3 |  | 867 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-page.wav |  | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-pop9.wav |  | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-select.wav |  | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-serious-context-v4.mp3 |  | 1608 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-slam.wav |  | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-steps.wav |  | 30 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-tap.wav |  | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-title-strings-v3.mp3 |  | 1252 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-travel-strings-v3.mp3 |  | 1186 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/source-village-arrival-wide.png | 1672x941 | 2538 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/town-bright.mp3 |  | 1553 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/ui-b-choice/paper-components.png | 1536x1024 | 1568 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-dialogue/b_icon_more.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-dialogue/b_icon_next.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/b_button.png | 160x52 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/b_button_primary.png | 160x52 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/b_panel_dialogue.png | 1200x160 | 134 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/b_panel_small.png | 240x60 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/b_tape_red.png | 96x28 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-field/sticker_daram_delighted.png | 512x512 | 243 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_background.png | 1280x720 | 1912 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_cast_poster.png | 1122x1402 | 2529 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_daram.png | 768x1024 | 599 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_daram_eureka.png | 512x512 | 228 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_sticker_cream.png | 1961x404 | 943 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-main/b_main_sticker_red.png | 1963x410 | 987 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_home.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_keys.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_mute.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_reading.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_reset.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_save.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_screen.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_icon_opt_sound.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_opt_choice.png | 222x84 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_opt_choice_hover.png | 222x84 | 12 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_opt_choice_selected.png | 222x84 | 10 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-options/b_opt_preview_box.png | 892x142 | 101 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/accent_rays_red.png | 96x96 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/accent_rays_white.png | 96x96 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_button.png | 160x52 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_button_primary.png | 160x52 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_icon_more.png | 64x64 | 2 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_lineart_book_corner.png | 292x112 | 30 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_lineart_market.png | 292x112 | 31 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_lineart_village.png | 292x112 | 31 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_lineart_winter.png | 292x112 | 21 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_panel_card_done.png | 672x116 | 54 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_panel_card_hover.png | 672x116 | 41 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/b_tape_teal.png | 96x28 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/icon_arrow_left_bold.png | 64x64 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/icon_book_open.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/icon_document.png | 64x64 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/notebook_holes.png | 64x160 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-question/rule_dotted.png | 512x24 | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-b-sticker/button_sheet.png | 1536x1024 | 1842 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_primary_basic.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_primary_disabled.png | 200x76 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_primary_pressed.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_primary_selected.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_standard_basic.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_standard_disabled.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_standard_pressed.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/main_standard_selected.png | 200x76 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/square_standard_basic.png | 80x80 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/square_standard_disabled.png | 80x80 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/square_standard_pressed.png | 80x80 | 3 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/square_standard_selected.png | 80x80 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_primary_basic.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_primary_disabled.png | 162x68 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_primary_pressed.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_primary_selected.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_standard_basic.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_standard_disabled.png | 162x68 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_standard_pressed.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-fit/topic_standard_selected.png | 162x68 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/primary_basic.png | 160x52 | 6 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/primary_disabled.png | 160x52 | 7 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/primary_pressed.png | 160x52 | 7 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/primary_selected.png | 160x52 | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/standard_basic.png | 160x52 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/standard_disabled.png | 160x52 | 7 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/standard_pressed.png | 160x52 | 7 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/standard_selected.png | 160x52 | 8 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/wide_choice_basic.png | 240x60 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/wide_choice_disabled.png | 240x60 | 13 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/wide_choice_pressed.png | 240x60 | 14 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-button-states/wide_choice_selected.png | 240x60 | 14 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/close_x.png | 34x34 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/diamond_outline.png | 14x14 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/gold_rule.png | 240x9 | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/name_ribbon.png | 220x50 | 17 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_btn_hover.png | 96x88 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_btn_idle.png | 96x88 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_btn_insensitive.png | 96x88 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_btn_selected.png | 96x88 | 5 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_panel.png | 1256x696 | 11 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/opt_tab.png | 400x128 | 70 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/panel.png | 256x256 | 33 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/panel_small.png | 64x64 | 4 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/preview_box.png | 48x44 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-night/say_shade.png | 8x320 | 0 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_primary_basic.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_primary_disabled.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_primary_pressed.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_primary_selected.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_standard_basic.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_standard_disabled.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_standard_pressed.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/ui-question-map-flat-v1/question_map_standard_selected.png | 160x52 | 1 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json |
| assets/village-activities.png | 1536x1024 | 1696 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/village-overview.png | 1672x941 | 3200 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/village-stone.png | 1145x1374 | 963 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/winter-carriage.png | 1672x941 | 1860 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/winter-gate-clean.png | 1672x941 | 2334 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/winter-gate.webp | 1672x941 | 419 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/winter-places.webp | 1536x1024 | 632 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |
| assets/witnesses.png | 1536x1024 | 2016 KB | json-unloaded:asset-toolbox/bindings.json; json-unloaded:asset-toolbox/catalog.json; json-unloaded:assets/prov |

</details>
### C2. v111 에 나오지 않는 인물의 그림 — 570개, 49.9 MB

| 폴더/이름 묶음 | 파일 수 | 용량 |
|---|---|---|
| dialogue-source-master | 288 | 20.6 MB |
| room13-* | 106 | 15.0 MB |
| solbang-chinchilla-source | 5 | 3.9 MB |
| map-work-nine | 5 | 3.7 MB |
| investigation-canonical-20261018 | 2 | 1.8 MB |
| map-action27 | 16 | 1.3 MB |
| resident-poses-a | 2 | 1.0 MB |
| profile-source-master | 16 | 0.7 MB |
| resident-* | 1 | 0.7 MB |
| field-dot-v2 | 114 | 0.6 MB |
| dialogue-pose-source | 3 | 0.4 MB |
| resident_yeoni-* | 2 | 0.0 MB |
| resident_guseul-* | 2 | 0.0 MB |
| resident_tori-* | 2 | 0.0 MB |
| resident_seol-* | 2 | 0.0 MB |
| resident_mungchi-* | 2 | 0.0 MB |
| resident_kkwak-* | 2 | 0.0 MB |

<details><summary>C2. v111 에 나오지 않는 인물의 그림 전체 570개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/dialogue-pose-source/chorong_mother/offer_lantern/560.webp | 194x413 | 85 KB | chorong_mother |
| assets/dialogue-pose-source/chorong_mother/offer_lantern/760.webp | 263x561 | 139 KB | chorong_mother |
| assets/dialogue-pose-source/chorong_mother/offer_lantern/840.webp | 290x620 | 169 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/angry.webp | 392x588 | 58 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/anxious.webp | 392x588 | 57 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/joy.webp | 392x588 | 59 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/neutral.webp | 392x588 | 58 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/surprise_react.webp | 392x588 | 61 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/560/surprise_talk.webp | 392x588 | 58 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/angry.webp | 400x600 | 60 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/anxious.webp | 400x600 | 59 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/joy.webp | 400x600 | 60 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/neutral.webp | 400x600 | 60 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/surprise_react.webp | 400x600 | 62 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/760/surprise_talk.webp | 400x600 | 60 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/angry.webp | 588x882 | 103 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/anxious.webp | 588x882 | 97 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/joy.webp | 588x882 | 104 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/neutral.webp | 588x882 | 104 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/surprise_react.webp | 588x882 | 108 KB | chorong_mother |
| assets/dialogue-source-master/chorong_mother/840/surprise_talk.webp | 588x882 | 104 KB | chorong_mother |
| assets/dialogue-source-master/kid_siluk1/560/angry.webp | 333x500 | 59 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/560/anxious.webp | 333x500 | 53 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/560/joy.webp | 333x500 | 60 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/560/neutral.webp | 333x500 | 56 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/560/surprise_react.webp | 333x500 | 58 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/560/surprise_talk.webp | 333x500 | 54 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/angry.webp | 400x600 | 76 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/anxious.webp | 400x600 | 69 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/joy.webp | 400x600 | 77 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/neutral.webp | 400x600 | 72 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/surprise_react.webp | 400x600 | 75 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/760/surprise_talk.webp | 400x600 | 72 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/angry.webp | 500x750 | 104 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/anxious.webp | 500x750 | 95 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/joy.webp | 500x750 | 106 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/neutral.webp | 500x750 | 101 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/surprise_react.webp | 500x750 | 105 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk1/840/surprise_talk.webp | 500x750 | 102 KB | kid_siluk1 |
| assets/dialogue-source-master/kid_siluk2/560/angry.webp | 333x500 | 53 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/560/anxious.webp | 333x500 | 51 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/560/joy.webp | 333x500 | 51 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/560/neutral.webp | 333x500 | 51 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/560/surprise_react.webp | 333x500 | 51 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/560/surprise_talk.webp | 333x500 | 48 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/angry.webp | 400x600 | 68 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/anxious.webp | 400x600 | 65 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/joy.webp | 400x600 | 66 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/neutral.webp | 400x600 | 65 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/surprise_react.webp | 400x600 | 66 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/760/surprise_talk.webp | 400x600 | 62 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/angry.webp | 500x750 | 95 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/anxious.webp | 500x750 | 89 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/joy.webp | 500x750 | 91 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/neutral.webp | 500x750 | 89 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/surprise_react.webp | 500x750 | 92 KB | kid_siluk2 |
| assets/dialogue-source-master/kid_siluk2/840/surprise_talk.webp | 500x750 | 85 KB | kid_siluk2 |
| assets/dialogue-source-master/resident_dalgeurak/560/angry.webp | 384x588 | 51 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/560/anxious.webp | 384x588 | 48 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/560/joy.webp | 392x588 | 79 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/560/neutral.webp | 390x588 | 47 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/560/surprise_react.webp | 384x588 | 53 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/560/surprise_talk.webp | 390x588 | 49 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/angry.webp | 392x600 | 53 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/anxious.webp | 392x600 | 49 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/joy.webp | 400x600 | 82 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/neutral.webp | 398x600 | 49 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/surprise_react.webp | 392x600 | 55 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/760/surprise_talk.webp | 398x600 | 50 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/angry.webp | 577x882 | 101 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/anxious.webp | 577x882 | 95 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/joy.webp | 588x882 | 160 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/neutral.webp | 584x882 | 94 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/surprise_react.webp | 577x882 | 105 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_dalgeurak/840/surprise_talk.webp | 584x882 | 97 KB | resident_dalgeurak |
| assets/dialogue-source-master/resident_guseul/560/angry.webp | 392x588 | 76 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/560/anxious.webp | 392x588 | 70 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/560/joy.webp | 353x588 | 40 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/560/neutral.webp | 266x588 | 35 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/560/surprise_react.webp | 266x588 | 34 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/560/surprise_talk.webp | 384x588 | 42 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/angry.webp | 400x600 | 78 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/anxious.webp | 400x600 | 72 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/joy.webp | 360x600 | 41 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/neutral.webp | 271x600 | 36 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/surprise_react.webp | 271x600 | 35 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/760/surprise_talk.webp | 392x600 | 43 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/angry.webp | 588x882 | 152 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/anxious.webp | 588x882 | 141 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/joy.webp | 529x882 | 79 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/neutral.webp | 398x882 | 69 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/surprise_react.webp | 399x882 | 66 KB | resident_guseul |
| assets/dialogue-source-master/resident_guseul/840/surprise_talk.webp | 577x882 | 84 KB | resident_guseul |
| assets/dialogue-source-master/resident_hyeoni/560/angry.webp | 392x588 | 69 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/560/anxious.webp | 391x588 | 62 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/560/joy.webp | 392x588 | 62 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/560/neutral.webp | 391x588 | 64 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/560/surprise_react.webp | 391x588 | 70 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/560/surprise_talk.webp | 392x588 | 64 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/angry.webp | 400x600 | 71 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/anxious.webp | 399x600 | 63 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/joy.webp | 400x600 | 64 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/neutral.webp | 399x600 | 66 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/surprise_react.webp | 399x600 | 73 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/760/surprise_talk.webp | 400x600 | 66 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/angry.webp | 588x882 | 121 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/anxious.webp | 587x882 | 108 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/joy.webp | 588x882 | 109 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/neutral.webp | 587x882 | 113 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/surprise_react.webp | 587x882 | 123 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_hyeoni/840/surprise_talk.webp | 588x882 | 112 KB | resident_hyeoni |
| assets/dialogue-source-master/resident_jongjong/560/angry.webp | 378x588 | 50 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/560/anxious.webp | 384x588 | 44 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/560/joy.webp | 378x588 | 45 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/560/neutral.webp | 377x588 | 50 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/560/surprise_react.webp | 377x588 | 55 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/560/surprise_talk.webp | 378x588 | 50 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/angry.webp | 393x612 | 53 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/anxious.webp | 400x612 | 46 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/joy.webp | 393x612 | 49 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/neutral.webp | 393x612 | 52 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/surprise_react.webp | 393x612 | 58 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/760/surprise_talk.webp | 393x612 | 52 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/angry.webp | 566x882 | 86 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/anxious.webp | 577x882 | 78 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/joy.webp | 566x882 | 79 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/neutral.webp | 566x882 | 85 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/surprise_react.webp | 566x882 | 95 KB | resident_jongjong |
| assets/dialogue-source-master/resident_jongjong/840/surprise_talk.webp | 566x882 | 87 KB | resident_jongjong |
| assets/dialogue-source-master/resident_kalbaram/560/angry.webp | 400x586 | 57 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/560/anxious.webp | 383x586 | 49 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/560/joy.webp | 400x586 | 54 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/560/neutral.webp | 400x586 | 51 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/560/surprise_react.webp | 400x586 | 51 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/560/surprise_talk.webp | 400x586 | 52 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/angry.webp | 400x586 | 57 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/anxious.webp | 383x586 | 49 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/joy.webp | 400x586 | 54 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/neutral.webp | 400x586 | 51 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/surprise_react.webp | 400x586 | 51 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/760/surprise_talk.webp | 400x586 | 52 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/angry.webp | 602x882 | 114 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/anxious.webp | 577x882 | 99 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/joy.webp | 602x882 | 107 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/neutral.webp | 602x882 | 101 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/surprise_react.webp | 602x882 | 103 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kalbaram/840/surprise_talk.webp | 602x882 | 103 KB | resident_kalbaram |
| assets/dialogue-source-master/resident_kkwak/560/angry.webp | 392x588 | 82 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/560/anxious.webp | 387x588 | 46 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/560/joy.webp | 392x588 | 79 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/560/neutral.webp | 338x588 | 49 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/560/surprise_react.webp | 338x588 | 51 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/560/surprise_talk.webp | 338x588 | 47 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/angry.webp | 400x600 | 85 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/anxious.webp | 395x600 | 48 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/joy.webp | 400x600 | 82 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/neutral.webp | 345x600 | 51 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/surprise_react.webp | 345x600 | 53 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/760/surprise_talk.webp | 345x600 | 49 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/angry.webp | 588x882 | 164 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/anxious.webp | 581x882 | 92 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/joy.webp | 588x882 | 160 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/neutral.webp | 507x882 | 98 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/surprise_react.webp | 507x882 | 103 KB | resident_kkwak |
| assets/dialogue-source-master/resident_kkwak/840/surprise_talk.webp | 507x882 | 94 KB | resident_kkwak |
| assets/dialogue-source-master/resident_librarian/560/angry.webp | 400x586 | 57 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/560/anxious.webp | 400x586 | 52 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/560/joy.webp | 400x586 | 56 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/560/neutral.webp | 400x586 | 54 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/560/surprise_react.webp | 400x586 | 56 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/560/surprise_talk.webp | 400x586 | 52 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/angry.webp | 400x586 | 57 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/anxious.webp | 400x586 | 52 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/joy.webp | 400x586 | 56 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/neutral.webp | 400x586 | 54 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/surprise_react.webp | 400x586 | 56 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/760/surprise_talk.webp | 400x586 | 52 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/angry.webp | 602x882 | 115 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/anxious.webp | 602x882 | 105 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/joy.webp | 602x882 | 112 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/neutral.webp | 602x882 | 108 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/surprise_react.webp | 602x882 | 112 KB | resident_librarian |
| assets/dialogue-source-master/resident_librarian/840/surprise_talk.webp | 602x882 | 104 KB | resident_librarian |
| assets/dialogue-source-master/resident_mulgyeol/560/angry.webp | 396x588 | 68 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/560/anxious.webp | 396x588 | 61 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/560/joy.webp | 396x588 | 67 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/560/neutral.webp | 396x588 | 62 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/560/surprise_react.webp | 396x588 | 64 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/560/surprise_talk.webp | 396x588 | 64 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/angry.webp | 400x594 | 70 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/anxious.webp | 400x594 | 62 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/joy.webp | 400x594 | 68 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/neutral.webp | 400x594 | 63 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/surprise_react.webp | 400x594 | 65 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/760/surprise_talk.webp | 400x594 | 65 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/angry.webp | 594x882 | 123 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/anxious.webp | 594x882 | 107 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/joy.webp | 594x882 | 120 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/neutral.webp | 594x882 | 111 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/surprise_react.webp | 594x882 | 115 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mulgyeol/840/surprise_talk.webp | 594x882 | 114 KB | resident_mulgyeol |
| assets/dialogue-source-master/resident_mungchi/560/angry.webp | 400x520 | 52 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/560/anxious.webp | 400x520 | 45 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/560/joy.webp | 400x520 | 48 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/560/neutral.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/560/surprise_react.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/560/surprise_talk.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/angry.webp | 400x520 | 52 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/anxious.webp | 400x520 | 45 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/joy.webp | 400x520 | 48 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/neutral.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/surprise_react.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/760/surprise_talk.webp | 400x520 | 47 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/angry.webp | 678x882 | 128 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/anxious.webp | 678x882 | 110 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/joy.webp | 678x882 | 118 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/neutral.webp | 678x882 | 116 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/surprise_react.webp | 678x882 | 116 KB | resident_mungchi |
| assets/dialogue-source-master/resident_mungchi/840/surprise_talk.webp | 678x882 | 117 KB | resident_mungchi |
| assets/dialogue-source-master/resident_seol/560/angry.webp | 375x588 | 59 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/560/anxious.webp | 374x588 | 55 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/560/joy.webp | 374x588 | 56 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/560/neutral.webp | 374x588 | 56 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/560/surprise_react.webp | 375x588 | 61 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/560/surprise_talk.webp | 375x588 | 56 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/angry.webp | 400x627 | 66 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/anxious.webp | 399x627 | 61 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/joy.webp | 399x627 | 63 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/neutral.webp | 399x627 | 63 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/surprise_react.webp | 400x627 | 68 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/760/surprise_talk.webp | 400x627 | 63 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/angry.webp | 562x882 | 118 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/anxious.webp | 562x882 | 110 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/joy.webp | 562x882 | 113 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/neutral.webp | 562x882 | 113 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/surprise_react.webp | 562x882 | 122 KB | resident_seol |
| assets/dialogue-source-master/resident_seol/840/surprise_talk.webp | 562x882 | 112 KB | resident_seol |
| assets/dialogue-source-master/resident_solbang/560/angry.webp | 392x588 | 68 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/560/anxious.webp | 392x588 | 62 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/560/joy.webp | 392x588 | 69 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/560/neutral.webp | 392x588 | 63 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/560/surprise_react.webp | 392x588 | 68 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/560/surprise_talk.webp | 392x588 | 64 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/angry.webp | 400x600 | 70 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/anxious.webp | 400x600 | 64 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/joy.webp | 400x600 | 71 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/neutral.webp | 400x600 | 65 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/surprise_react.webp | 400x600 | 70 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/760/surprise_talk.webp | 400x600 | 66 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/angry.webp | 588x882 | 120 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/anxious.webp | 588x882 | 111 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/joy.webp | 588x882 | 124 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/neutral.webp | 588x882 | 116 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/surprise_react.webp | 588x882 | 121 KB | resident_solbang |
| assets/dialogue-source-master/resident_solbang/840/surprise_talk.webp | 588x882 | 115 KB | resident_solbang |
| assets/dialogue-source-master/resident_tori/560/angry.webp | 346x588 | 42 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/560/anxious.webp | 346x588 | 41 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/560/joy.webp | 346x588 | 41 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/560/neutral.webp | 346x588 | 40 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/560/surprise_react.webp | 346x588 | 41 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/560/surprise_talk.webp | 346x588 | 41 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/angry.webp | 400x680 | 54 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/anxious.webp | 400x680 | 53 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/joy.webp | 400x680 | 53 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/neutral.webp | 400x680 | 51 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/surprise_react.webp | 400x680 | 53 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/760/surprise_talk.webp | 400x680 | 52 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/angry.webp | 519x882 | 83 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/anxious.webp | 519x882 | 81 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/joy.webp | 519x882 | 82 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/neutral.webp | 519x882 | 80 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/surprise_react.webp | 519x882 | 82 KB | resident_tori |
| assets/dialogue-source-master/resident_tori/840/surprise_talk.webp | 519x882 | 80 KB | resident_tori |
| assets/dialogue-source-master/resident_yeoni/560/angry.webp | 376x588 | 58 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/560/anxious.webp | 376x588 | 54 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/560/joy.webp | 376x588 | 56 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/560/neutral.webp | 376x588 | 55 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/560/surprise_react.webp | 376x588 | 57 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/560/surprise_talk.webp | 376x588 | 56 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/angry.webp | 400x625 | 64 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/anxious.webp | 400x625 | 59 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/joy.webp | 400x625 | 61 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/neutral.webp | 400x625 | 61 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/surprise_react.webp | 400x625 | 63 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/760/surprise_talk.webp | 400x625 | 61 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/angry.webp | 564x882 | 101 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/anxious.webp | 564x882 | 92 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/joy.webp | 564x882 | 98 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/neutral.webp | 564x882 | 97 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/surprise_react.webp | 564x882 | 100 KB | resident_yeoni |
| assets/dialogue-source-master/resident_yeoni/840/surprise_talk.webp | 564x882 | 97 KB | resident_yeoni |
| assets/field-dot-v2/bodum/activity.webp | 194x176 | 8 KB | bodum |
| assets/field-dot-v2/bodum/distressed.webp | 148x196 | 7 KB | bodum |
| assets/field-dot-v2/bodum/expressive.webp | 224x196 | 8 KB | bodum |
| assets/field-dot-v2/bodum/neutral.webp | 162x209 | 8 KB | bodum |
| assets/field-dot-v2/bodum/thinking.webp | 162x198 | 8 KB | bodum |
| assets/field-dot-v2/chorong_mother/distressed.webp | 96x210 | 6 KB | chorong_mother |
| assets/field-dot-v2/chorong_mother/expressive.webp | 96x210 | 6 KB | chorong_mother |
| assets/field-dot-v2/chorong_mother/neutral.webp | 96x210 | 6 KB | chorong_mother |
| assets/field-dot-v2/chorong_mother/offer_lantern.webp | 97x210 | 6 KB | chorong_mother |
| assets/field-dot-v2/chorong_mother/thinking.webp | 96x210 | 6 KB | chorong_mother |
| assets/field-dot-v2/elder/activity.webp | 132x195 | 6 KB | elder |
| assets/field-dot-v2/elder/distressed.webp | 166x174 | 7 KB | elder |
| assets/field-dot-v2/elder/expressive.webp | 182x191 | 7 KB | elder |
| assets/field-dot-v2/elder/neutral.webp | 110x194 | 6 KB | elder |
| assets/field-dot-v2/elder/thinking.webp | 184x180 | 7 KB | elder |
| assets/field-dot-v2/kid_siluk1/distressed.webp | 92x164 | 5 KB | kid_siluk1 |
| assets/field-dot-v2/kid_siluk1/expressive.webp | 92x164 | 5 KB | kid_siluk1 |
| assets/field-dot-v2/kid_siluk1/neutral.webp | 92x164 | 5 KB | kid_siluk1 |
| assets/field-dot-v2/kid_siluk1/thinking.webp | 92x164 | 5 KB | kid_siluk1 |
| assets/field-dot-v2/kid_siluk2/distressed.webp | 93x165 | 5 KB | kid_siluk2 |
| assets/field-dot-v2/kid_siluk2/expressive.webp | 93x165 | 5 KB | kid_siluk2 |
| assets/field-dot-v2/kid_siluk2/neutral.webp | 93x165 | 5 KB | kid_siluk2 |
| assets/field-dot-v2/kid_siluk2/thinking.webp | 93x165 | 5 KB | kid_siluk2 |
| assets/field-dot-v2/resident_dalgeurak/distressed.webp | 114x210 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/expressive.webp | 114x210 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/map27_di_1b.webp | 81x151 | 4 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/map27_mk_6.webp | 132x210 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/map27_sq_1.webp | 135x202 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/map9_pots_display.webp | 136x189 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/neutral.webp | 114x210 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_dalgeurak/thinking.webp | 114x210 | 6 KB | resident_dalgeurak |
| assets/field-dot-v2/resident_guseul/distressed.webp | 82x210 | 4 KB | resident_guseul |
| assets/field-dot-v2/resident_guseul/expressive.webp | 82x210 | 4 KB | resident_guseul |
| assets/field-dot-v2/resident_guseul/living_stamp.webp | 90x210 | 5 KB | resident_guseul |
| assets/field-dot-v2/resident_guseul/map27_mk_3.webp | 89x210 | 5 KB | resident_guseul |
| assets/field-dot-v2/resident_guseul/neutral.webp | 82x210 | 4 KB | resident_guseul |
| assets/field-dot-v2/resident_guseul/thinking.webp | 82x210 | 4 KB | resident_guseul |
| assets/field-dot-v2/resident_hyeoni/distressed.webp | 134x210 | 6 KB | resident_hyeoni |
| assets/field-dot-v2/resident_hyeoni/expressive.webp | 134x210 | 6 KB | resident_hyeoni |
| assets/field-dot-v2/resident_hyeoni/map27_mk_8.webp | 132x210 | 7 KB | resident_hyeoni |
| assets/field-dot-v2/resident_hyeoni/neutral.webp | 134x210 | 6 KB | resident_hyeoni |
| assets/field-dot-v2/resident_hyeoni/thinking.webp | 134x210 | 6 KB | resident_hyeoni |
| assets/field-dot-v2/resident_jongjong/distressed.webp | 104x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/expressive.webp | 104x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/life_run_satchel.webp | 156x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/map27_pack_satchel_v2.webp | 94x211 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/map27_po_3.webp | 108x209 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/map27_sort_letters_v2.webp | 98x211 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/map9_letters_waiting.webp | 103x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/neutral.webp | 104x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_jongjong/thinking.webp | 104x210 | 5 KB | resident_jongjong |
| assets/field-dot-v2/resident_kalbaram/distressed.webp | 121x211 | 6 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kalbaram/expressive.webp | 121x211 | 6 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kalbaram/life_walk_in.webp | 170x211 | 6 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kalbaram/map27_fo_1.webp | 129x137 | 5 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kalbaram/neutral.webp | 121x211 | 6 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kalbaram/thinking.webp | 121x211 | 6 KB | resident_kalbaram |
| assets/field-dot-v2/resident_kkwak/distressed.webp | 109x209 | 5 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/expressive.webp | 109x209 | 5 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/life_carry_bucket.webp | 159x209 | 6 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/map27_ri_1.webp | 107x163 | 4 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/map9_river_haul_net.webp | 241x202 | 9 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/neutral.webp | 109x209 | 5 KB | resident_kkwak |
| assets/field-dot-v2/resident_kkwak/thinking.webp | 109x209 | 5 KB | resident_kkwak |
| assets/field-dot-v2/resident_librarian/distressed.webp | 128x210 | 6 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/event_ledgertie.webp | 146x147 | 6 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/expressive.webp | 128x210 | 6 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/living_bookpaper.webp | 135x210 | 7 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/map27_po_2.webp | 146x210 | 7 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/neutral.webp | 128x210 | 6 KB | resident_librarian |
| assets/field-dot-v2/resident_librarian/thinking.webp | 128x210 | 6 KB | resident_librarian |
| assets/field-dot-v2/resident_mulgyeol/distressed.webp | 115x210 | 6 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/expressive.webp | 115x210 | 6 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/life_warm_hands_fire.webp | 159x210 | 6 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/map27_ri_2.webp | 113x210 | 5 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/map9_rope_coiling.webp | 131x210 | 5 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/neutral.webp | 115x210 | 6 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mulgyeol/thinking.webp | 115x210 | 6 KB | resident_mulgyeol |
| assets/field-dot-v2/resident_mungchi/distressed.webp | 116x210 | 6 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/expressive.webp | 116x210 | 6 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/map27_mk_7.webp | 105x201 | 5 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/map27_st_1.webp | 135x202 | 7 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/map9_store_sort_boxes.webp | 137x202 | 6 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/neutral.webp | 116x210 | 6 KB | resident_mungchi |
| assets/field-dot-v2/resident_mungchi/thinking.webp | 116x210 | 6 KB | resident_mungchi |
| assets/field-dot-v2/resident_seol/distressed.webp | 115x210 | 6 KB | resident_seol |
| assets/field-dot-v2/resident_seol/expressive.webp | 115x210 | 6 KB | resident_seol |
| assets/field-dot-v2/resident_seol/living_bellrope.webp | 115x210 | 6 KB | resident_seol |
| assets/field-dot-v2/resident_seol/neutral.webp | 115x210 | 6 KB | resident_seol |
| assets/field-dot-v2/resident_seol/thinking.webp | 115x210 | 6 KB | resident_seol |
| assets/field-dot-v2/resident_solbang/distressed.webp | 140x210 | 8 KB | resident_solbang |
| assets/field-dot-v2/resident_solbang/expressive.webp | 140x210 | 8 KB | resident_solbang |
| assets/field-dot-v2/resident_solbang/map27_mk_1.webp | 124x211 | 7 KB | resident_solbang |
| assets/field-dot-v2/resident_solbang/neutral.webp | 140x210 | 8 KB | resident_solbang |
| assets/field-dot-v2/resident_solbang/thinking.webp | 140x210 | 8 KB | resident_solbang |
| assets/field-dot-v2/resident_solbang/work_herb_bundle.webp | 130x193 | 6 KB | resident_solbang |
| assets/field-dot-v2/resident_tori/activity.webp | 131x171 | 5 KB | resident_tori |
| assets/field-dot-v2/resident_tori/distressed.webp | 102x172 | 4 KB | resident_tori |
| assets/field-dot-v2/resident_tori/expressive.webp | 166x174 | 4 KB | resident_tori |
| assets/field-dot-v2/resident_tori/group_cooperative.webp | 82x210 | 5 KB | resident_tori |
| assets/field-dot-v2/resident_tori/life_handover_cloth.webp | 131x209 | 4 KB | resident_tori |
| assets/field-dot-v2/resident_tori/life_pick_goods.webp | 97x209 | 3 KB | resident_tori |
| assets/field-dot-v2/resident_tori/life_sew_bench.webp | 125x209 | 4 KB | resident_tori |
| assets/field-dot-v2/resident_tori/neutral.webp | 100x209 | 5 KB | resident_tori |
| assets/field-dot-v2/resident_tori/thinking.webp | 99x209 | 5 KB | resident_tori |
| assets/field-dot-v2/resident_tori/world_bench_left.webp | 133x200 | 5 KB | resident_tori |
| assets/field-dot-v2/resident_yeoni/distressed.webp | 124x210 | 5 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/expressive.webp | 124x210 | 5 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/life_hold_bundle.webp | 121x210 | 5 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/life_pick_goods.webp | 120x210 | 4 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/living_mend.webp | 103x155 | 4 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/map27_mk_5.webp | 107x210 | 6 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/neutral.webp | 124x210 | 5 KB | resident_yeoni |
| assets/field-dot-v2/resident_yeoni/thinking.webp | 124x210 | 5 KB | resident_yeoni |
| assets/investigation-canonical-20261018/resident_jongjong--map27_pack_satchel_v2.webp | 1024x1536 | 926 KB | resident_jongjong |
| assets/investigation-canonical-20261018/resident_jongjong--map27_sort_letters_v2.webp | 1024x1536 | 967 KB | resident_jongjong |
| assets/map-action27/DI-1b--resident_dalgeurak.webp | 422x768 | 92 KB | resident_dalgeurak |
| assets/map-action27/FO-1--resident_kalbaram.webp | 702x768 | 111 KB | resident_kalbaram |
| assets/map-action27/MK-1--resident_solbang.webp | 512x768 | 89 KB | resident_solbang |
| assets/map-action27/MK-3--resident_guseul.webp | 512x768 | 64 KB | resident_guseul |
| assets/map-action27/MK-5--resident_yeoni.webp | 512x768 | 73 KB | resident_yeoni |
| assets/map-action27/MK-6--resident_dalgeurak.webp | 512x768 | 87 KB | resident_dalgeurak |
| assets/map-action27/MK-7--resident_mungchi.webp | 512x768 | 74 KB | resident_mungchi |
| assets/map-action27/MK-8--resident_hyeoni.webp | 496x768 | 85 KB | resident_hyeoni |
| assets/map-action27/PO-2--resident_librarian.webp | 512x768 | 82 KB | resident_librarian |
| assets/map-action27/PO-3--resident_jongjong.webp | 512x768 | 76 KB | resident_jongjong |
| assets/map-action27/RI-1--resident_kkwak.webp | 512x768 | 94 KB | resident_kkwak |
| assets/map-action27/RI-2--resident_mulgyeol.webp | 512x768 | 75 KB | resident_mulgyeol |
| assets/map-action27/SQ-1--resident_dalgeurak.webp | 512x768 | 99 KB | resident_dalgeurak |
| assets/map-action27/ST-1--resident_mungchi.webp | 512x768 | 95 KB | resident_mungchi |
| assets/map-action27/VA-11--resident_jongjong.webp | 494x768 | 90 KB | resident_jongjong |
| assets/map-action27/VA-12--resident_jongjong.webp | 492x768 | 89 KB | resident_jongjong |
| assets/map-work-nine/resident_dalgeurak--pots_display.webp | 1021x1540 | 775 KB | resident_dalgeurak |
| assets/map-work-nine/resident_jongjong--letters_waiting.webp | 1005x1566 | 589 KB | resident_jongjong |
| assets/map-work-nine/resident_kkwak--river_haul_net.webp | 1373x1145 | 899 KB | resident_kkwak |
| assets/map-work-nine/resident_mulgyeol--rope_coiling.webp | 1029x1528 | 749 KB | resident_mulgyeol |
| assets/map-work-nine/resident_mungchi--store_sort_boxes.webp | 1037x1517 | 737 KB | resident_mungchi |
| assets/profile-source-master/chorong_mother.webp | 256x256 | 52 KB | chorong_mother |
| assets/profile-source-master/kid_siluk1.webp | 256x256 | 61 KB | kid_siluk1 |
| assets/profile-source-master/kid_siluk2.webp | 256x256 | 52 KB | kid_siluk2 |
| assets/profile-source-master/resident_dalgeurak.webp | 256x256 | 46 KB | resident_dalgeurak |
| assets/profile-source-master/resident_guseul.webp | 256x256 | 41 KB | resident_guseul |
| assets/profile-source-master/resident_hyeoni.webp | 256x256 | 46 KB | resident_hyeoni |
| assets/profile-source-master/resident_jongjong.webp | 256x256 | 40 KB | resident_jongjong |
| assets/profile-source-master/resident_kalbaram.webp | 256x256 | 51 KB | resident_kalbaram |
| assets/profile-source-master/resident_kkwak.webp | 256x256 | 47 KB | resident_kkwak |
| assets/profile-source-master/resident_librarian.webp | 256x256 | 53 KB | resident_librarian |
| assets/profile-source-master/resident_mulgyeol.webp | 256x256 | 50 KB | resident_mulgyeol |
| assets/profile-source-master/resident_mungchi.webp | 256x256 | 48 KB | resident_mungchi |
| assets/profile-source-master/resident_seol.webp | 256x256 | 49 KB | resident_seol |
| assets/profile-source-master/resident_solbang.webp | 256x256 | 49 KB | resident_solbang |
| assets/profile-source-master/resident_tori.webp | 256x256 | 37 KB | resident_tori |
| assets/profile-source-master/resident_yeoni.webp | 256x256 | 44 KB | resident_yeoni |
| assets/resident-librarian-teacher.png | 1774x887 | 697 KB | residents |
| assets/resident-poses-a/bodum-basket-cloth-noborder.webp | 1280x1152 | 747 KB | bodum |
| assets/resident-poses-a/bodum-basket-cloth.webp | 1280x1152 | 245 KB | bodum |
| assets/resident_guseul-body.png | 182x182 | 12 KB | resident_guseul; residents |
| assets/resident_guseul-face.png | 192x192 | 12 KB | resident_guseul; residents |
| assets/resident_kkwak-body.png | 132x182 | 11 KB | resident_kkwak; residents |
| assets/resident_kkwak-face.png | 192x192 | 9 KB | resident_kkwak; residents |
| assets/resident_mungchi-body.png | 90x182 | 9 KB | resident_mungchi; residents |
| assets/resident_mungchi-face.png | 192x192 | 10 KB | resident_mungchi; residents |
| assets/resident_seol-body.png | 116x182 | 10 KB | resident_seol; residents |
| assets/resident_seol-face.png | 192x192 | 12 KB | resident_seol; residents |
| assets/resident_tori-body.png | 130x182 | 11 KB | resident_tori; residents |
| assets/resident_tori-face.png | 192x192 | 11 KB | resident_tori; residents |
| assets/resident_yeoni-body.png | 204x182 | 14 KB | resident_yeoni; residents |
| assets/resident_yeoni-face.png | 192x192 | 12 KB | resident_yeoni; residents |
| assets/room13-action-resident_librarian-event_ledgertie.webp | 656x600 | 64 KB | resident_librarian |
| assets/room13-action-resident_librarian-living_bookpaper.webp | 519x758 | 77 KB | resident_librarian |
| assets/room13-action-resident_mungchi-event_handrub.webp | 512x768 | 63 KB | resident_mungchi |
| assets/room13-action-resident_seol-living_bellrope.webp | 512x768 | 82 KB | resident_seol |
| assets/room13-action-resident_yeoni-living_mend.webp | 512x768 | 73 KB | resident_yeoni |
| assets/room13-canonical-default-resident_seol.webp | 488x768 | 82 KB | resident_seol |
| assets/room13-face-kid_siluk1.webp | 384x384 | 50 KB | kid_siluk1 |
| assets/room13-face-kid_siluk2.webp | 384x384 | 49 KB | kid_siluk2 |
| assets/room13-fullbody-bodum-angry.webp | 512x768 | 73 KB | bodum |
| assets/room13-fullbody-bodum-anxious.webp | 512x768 | 75 KB | bodum |
| assets/room13-fullbody-bodum-flustered.webp | 512x768 | 74 KB | bodum |
| assets/room13-fullbody-bodum-joy.webp | 512x768 | 73 KB | bodum |
| assets/room13-fullbody-bodum-neutral.webp | 512x768 | 63 KB | bodum |
| assets/room13-fullbody-bodum-surprise.webp | 512x768 | 73 KB | bodum |
| assets/room13-fullbody-chorong_mother-anxious.webp | 512x768 | 79 KB | chorong_mother |
| assets/room13-fullbody-chorong_mother-neutral.webp | 512x768 | 76 KB | chorong_mother |
| assets/room13-fullbody-chorong_mother-pose-offer_lantern.webp | 512x768 | 79 KB | chorong_mother |
| assets/room13-fullbody-elder-angry.webp | 512x768 | 94 KB | elder |
| assets/room13-fullbody-elder-anxious.webp | 512x768 | 95 KB | elder |
| assets/room13-fullbody-elder-flustered.webp | 512x768 | 94 KB | elder |
| assets/room13-fullbody-elder-joy.webp | 512x768 | 95 KB | elder |
| assets/room13-fullbody-elder-neutral.webp | 512x768 | 83 KB | elder |
| assets/room13-fullbody-elder-surprise.webp | 512x768 | 95 KB | elder |
| assets/room13-fullbody-kid_siluk1-anxious.webp | 512x768 | 84 KB | kid_siluk1 |
| assets/room13-fullbody-kid_siluk1-joy.webp | 512x768 | 88 KB | kid_siluk1 |
| assets/room13-fullbody-kid_siluk1-neutral.webp | 512x768 | 82 KB | kid_siluk1 |
| assets/room13-fullbody-kid_siluk2-anxious.webp | 512x768 | 80 KB | kid_siluk2 |
| assets/room13-fullbody-kid_siluk2-joy.webp | 512x768 | 76 KB | kid_siluk2 |
| assets/room13-fullbody-kid_siluk2-neutral.webp | 512x768 | 73 KB | kid_siluk2 |
| assets/room13-fullbody-resident_guseul-angry.webp | 512x768 | 58 KB | resident_guseul |
| assets/room13-fullbody-resident_guseul-anxious.webp | 512x768 | 58 KB | resident_guseul |
| assets/room13-fullbody-resident_guseul-flustered.webp | 512x768 | 59 KB | resident_guseul |
| assets/room13-fullbody-resident_guseul-joy.webp | 512x768 | 61 KB | resident_guseul |
| assets/room13-fullbody-resident_guseul-neutral.webp | 512x768 | 58 KB | resident_guseul |
| assets/room13-fullbody-resident_guseul-surprise.webp | 512x768 | 59 KB | resident_guseul |
| assets/room13-fullbody-resident_kkwak-angry.webp | 512x768 | 75 KB | resident_kkwak |
| assets/room13-fullbody-resident_kkwak-anxious.webp | 512x768 | 70 KB | resident_kkwak |
| assets/room13-fullbody-resident_kkwak-flustered.webp | 512x768 | 76 KB | resident_kkwak |
| assets/room13-fullbody-resident_kkwak-joy.webp | 512x768 | 72 KB | resident_kkwak |
| assets/room13-fullbody-resident_kkwak-neutral.webp | 512x768 | 65 KB | resident_kkwak |
| assets/room13-fullbody-resident_kkwak-surprise.webp | 512x768 | 75 KB | resident_kkwak |
| assets/room13-fullbody-resident_librarian-angry.webp | 512x768 | 62 KB | resident_librarian |
| assets/room13-fullbody-resident_librarian-anxious.webp | 512x768 | 74 KB | resident_librarian |
| assets/room13-fullbody-resident_librarian-flustered.webp | 512x768 | 61 KB | resident_librarian |
| assets/room13-fullbody-resident_librarian-joy.webp | 512x768 | 62 KB | resident_librarian |
| assets/room13-fullbody-resident_librarian-neutral.webp | 512x768 | 61 KB | resident_librarian |
| assets/room13-fullbody-resident_librarian-surprise.webp | 512x768 | 63 KB | resident_librarian |
| assets/room13-fullbody-resident_mungchi-angry.webp | 512x768 | 64 KB | resident_mungchi |
| assets/room13-fullbody-resident_mungchi-anxious.webp | 512x768 | 65 KB | resident_mungchi |
| assets/room13-fullbody-resident_mungchi-flustered.webp | 512x768 | 64 KB | resident_mungchi |
| assets/room13-fullbody-resident_mungchi-joy.webp | 512x768 | 66 KB | resident_mungchi |
| assets/room13-fullbody-resident_mungchi-neutral.webp | 512x768 | 64 KB | resident_mungchi |
| assets/room13-fullbody-resident_mungchi-surprise.webp | 512x768 | 65 KB | resident_mungchi |
| assets/room13-fullbody-resident_seol-angry.webp | 512x768 | 68 KB | resident_seol |
| assets/room13-fullbody-resident_seol-anxious.webp | 512x768 | 68 KB | resident_seol |
| assets/room13-fullbody-resident_seol-flustered.webp | 512x768 | 67 KB | resident_seol |
| assets/room13-fullbody-resident_seol-joy.webp | 512x768 | 67 KB | resident_seol |
| assets/room13-fullbody-resident_seol-neutral.webp | 512x768 | 67 KB | resident_seol |
| assets/room13-fullbody-resident_seol-surprise.webp | 512x768 | 67 KB | resident_seol |
| assets/room13-fullbody-resident_tori-angry.webp | 483x814 | 70 KB | resident_tori |
| assets/room13-fullbody-resident_tori-anxious.webp | 483x814 | 69 KB | resident_tori |
| assets/room13-fullbody-resident_tori-flustered.webp | 484x814 | 68 KB | resident_tori |
| assets/room13-fullbody-resident_tori-joy.webp | 484x814 | 68 KB | resident_tori |
| assets/room13-fullbody-resident_tori-neutral.webp | 483x814 | 69 KB | resident_tori |
| assets/room13-fullbody-resident_tori-surprise.webp | 484x814 | 70 KB | resident_tori |
| assets/room13-fullbody-resident_yeoni-angry.webp | 512x768 | 71 KB | resident_yeoni |
| assets/room13-fullbody-resident_yeoni-anxious.webp | 512x768 | 70 KB | resident_yeoni |
| assets/room13-fullbody-resident_yeoni-flustered.webp | 512x768 | 70 KB | resident_yeoni |
| assets/room13-fullbody-resident_yeoni-joy.webp | 512x768 | 70 KB | resident_yeoni |
| assets/room13-fullbody-resident_yeoni-neutral.webp | 512x768 | 70 KB | resident_yeoni |
| assets/room13-fullbody-resident_yeoni-surprise.webp | 512x768 | 71 KB | resident_yeoni |
| assets/room13-fullbody-workshop-angry.webp | 512x768 | 92 KB | workshop |
| assets/room13-fullbody-workshop-anxious.webp | 512x768 | 87 KB | workshop |
| assets/room13-fullbody-workshop-flustered.webp | 512x768 | 89 KB | workshop |
| assets/room13-fullbody-workshop-joy.webp | 512x768 | 95 KB | workshop |
| assets/room13-fullbody-workshop-neutral.webp | 512x768 | 75 KB | workshop |
| assets/room13-fullbody-workshop-surprise.webp | 512x768 | 83 KB | workshop |
| assets/room13-group-resident_tori-cooperative.webp | 512x768 | 61 KB | resident_tori |
| assets/room13-pixel-acting-bodum.webp | 1536x1024 | 264 KB | bodum |
| assets/room13-pixel-acting-elder.webp | 1536x1024 | 265 KB | elder |
| assets/room13-pixel-acting-resident_kkwak.webp | 1536x1024 | 273 KB | resident_kkwak |
| assets/room13-pixel-acting-resident_librarian.webp | 1536x1024 | 253 KB | resident_librarian |
| assets/room13-pixel-acting-resident_seol.webp | 1536x1024 | 314 KB | resident_seol |
| assets/room13-pixel-acting-resident_tori.webp | 1536x1024 | 191 KB | resident_tori |
| assets/room13-pixel-acting-resident_yeoni.webp | 1536x1024 | 284 KB | resident_yeoni |
| assets/room13-redesign-resident_librarian.webp | 519x758 | 74 KB | resident_librarian |
| assets/room13-redesign-resident_seol.webp | 512x768 | 69 KB | resident_seol |
| assets/room13-redesign-resident_yeoni.webp | 519x758 | 70 KB | resident_yeoni |
| assets/room13-role-resident_dalgeurak.webp | 505x762 | 83 KB | resident_dalgeurak |
| assets/room13-role-resident_guseul-batch-angry-v1.webp | 1005x1566 | 565 KB | resident_guseul |
| assets/room13-role-resident_guseul-batch-anxious-v1.webp | 1004x1566 | 486 KB | resident_guseul |
| assets/room13-role-resident_guseul-batch-joy-v1.webp | 1004x1567 | 561 KB | resident_guseul |
| assets/room13-role-resident_guseul-batch-living_stamp-v1.webp | 1004x1566 | 536 KB | resident_guseul |
| assets/room13-role-resident_guseul-batch-surprise-v1.webp | 1004x1566 | 550 KB | resident_guseul |
| assets/room13-role-resident_guseul.webp | 490x764 | 48 KB | resident_guseul |
| assets/room13-role-resident_hyeoni.webp | 508x764 | 80 KB | resident_hyeoni |
| assets/room13-role-resident_jongjong.webp | 492x768 | 59 KB | resident_jongjong |
| assets/room13-role-resident_kalbaram.webp | 490x718 | 78 KB | resident_kalbaram |
| assets/room13-role-resident_kkwak-expression-angry-v1.webp | 1018x1544 | 805 KB | resident_kkwak |
| assets/room13-role-resident_kkwak-expression-anxious-v1.webp | 1018x1544 | 643 KB | resident_kkwak |
| assets/room13-role-resident_kkwak-expression-flustered-v1.webp | 1018x1545 | 685 KB | resident_kkwak |
| assets/room13-role-resident_kkwak-expression-joy-v1.webp | 1018x1544 | 835 KB | resident_kkwak |
| assets/room13-role-resident_kkwak-expression-surprise-v1.webp | 1018x1544 | 900 KB | resident_kkwak |
| assets/room13-role-resident_kkwak-refined-v1.webp | 1019x1544 | 665 KB | resident_kkwak |
| assets/room13-role-resident_mulgyeol.webp | 512x761 | 68 KB | resident_mulgyeol |
| assets/room13-role-resident_mungchi.webp | 512x749 | 59 KB | resident_mungchi |
| assets/solbang-chinchilla-source/angry.webp | 1024x1536 | 825 KB | resident_solbang |
| assets/solbang-chinchilla-source/anxious.webp | 1024x1536 | 759 KB | resident_solbang |
| assets/solbang-chinchilla-source/joy.webp | 1024x1536 | 838 KB | resident_solbang |
| assets/solbang-chinchilla-source/neutral.webp | 1024x1536 | 770 KB | resident_solbang |
| assets/solbang-chinchilla-source/surprise_talk.webp | 1024x1536 | 783 KB | resident_solbang |

</details>
### C3. 인물 그림 폴더 규칙에만 걸림(인물 불명) — 3개, 0.4 MB

| 폴더/이름 묶음 | 파일 수 | 용량 |
|---|---|---|
| room13-* | 3 | 0.4 MB |

<details><summary>C3. 인물 그림 폴더 규칙에만 걸림(인물 불명) 전체 3개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/room13-meeting-seated-buri068.webp | 1190x1322 | 137 KB |  |
| assets/room13-meeting-seated-doto068.webp | 1210x1300 | 156 KB |  |
| assets/room13-meeting-seated-resident_bori068.webp | 1024x1536 | 153 KB |  |

</details>
### D. 어디서도 이름이 안 나옴 — 2개, 0.4 MB

| 폴더/이름 묶음 | 파일 수 | 용량 |
|---|---|---|
| room13-* | 1 | 0.3 MB |
| ending | 1 | 0.1 MB |

<details><summary>D. 어디서도 이름이 안 나옴 전체 2개</summary>

| 경로 | 크기 | 용량 | 근거 |
|---|---|---|---|
| assets/ending/END-11-father-child.webp | 1672x941 | 65 KB |  |
| assets/room13-loading-scene.webp | 1280x720 | 307 KB |  |

</details>

D 두 파일 메모: `assets/room13-loading-scene.webp` 는 게임 코드가 아니라 웹 로딩창 도구(dev/make_loading_scene.py, dev/update_title_loader.py)가 쓴다 — 웹판에서는 쓰임. `assets/ending/END-11-father-child.webp` 는 dNN 의 endcut 층 이름(END-11:father-alone, END-11:three)에 없는 판이다.

## 참고: 옛 판 rpy 로 본 파일(label·화면이 시작에서 하나도 닿지 않음)

`room13_asset_toolbox.rpy`, `room13_cinematics.rpy`, `room13_dialogue_openings_20261013.rpy`, `room13_family_bundle.rpy`, `room13_inn_navigation_v4.rpy`, `room13_record_compare.rpy`, `room13_revision.rpy`, `room13_week2.rpy`, `room13_worldmap_v5.rpy`, `systems/room13_alibi.rpy`, `systems/room13_bundle3.rpy`, `systems/room13_carryover.rpy`, `systems/room13_convenience.rpy`, `systems/room13_daram_mood.rpy`, `systems/room13_debate.rpy`, `systems/room13_direct_work.rpy`, `systems/room13_ending_story.rpy`, `systems/room13_ep1_lamp_thief.rpy`, `systems/room13_ep2_kids.rpy`, `systems/room13_ep3_woodfire.rpy`, `systems/room13_ep4_night13.rpy`, `systems/room13_ep5_soup.rpy`, `systems/room13_ep6_cart.rpy`, `systems/room13_ep_story.rpy`, `systems/room13_episode_aftermath.rpy`, `systems/room13_episodes.rpy`, `systems/room13_evening.rpy`, `systems/room13_gimmicks.rpy`, `systems/room13_granny_reply.rpy`, `systems/room13_inn_change.rpy`, `systems/room13_life_closeups.rpy`, `systems/room13_livelihood_flow.rpy`, `systems/room13_livelihood_ui.rpy`, `systems/room13_meeting_flow.rpy`, `systems/room13_memory.rpy`, `systems/room13_new_cast.rpy`, `systems/room13_owl_buri.rpy`, `systems/room13_piko_causality.rpy`, `systems/room13_poc_route.rpy`, `systems/room13_q1_arguments.rpy`, `systems/room13_q1_difficulty.rpy`, `systems/room13_q1_review.rpy`, `systems/room13_reinspect.rpy`, `systems/room13_return_recovery.rpy`, `systems/room13_shop.rpy`, `systems/room13_sling_confidence.rpy`, `systems/room13_topic_record.rpy`, `systems/room13_town_events.rpy`, `systems/room13_town_events2.rpy`, `systems/room13_use_knowledge.rpy`, `systems/room13_week1_cases.rpy`, `systems/room13_week2_events.rpy`
