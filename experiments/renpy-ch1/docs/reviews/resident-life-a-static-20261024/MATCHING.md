# 주민생활 A 1~6차 56종 정적 매칭 준비

기준 main: `056c2a89a359d648bb9852fe5fe5963363fbbfe2`. 문서 전용 작업이며 에셋 적용·시각 승인·실행 검증 결과가 아니다. Claude의 대사 조정과 독립적으로 작성했으므로 실제 적용 직전에 최신 main 대사를 다시 대조한다.

정적 확정 30종 / 후보 16종 / 보류 10종. **새 파일명·시각 검증은 56종 모두 미확인, 실제 적용 0종.**

## 중복 작업 확인

최신 main의 추적 파일명과 game/art/docs의 납품명·Library ID 참조를 검색했다. 이번 6개 ZIP의 반영을 입증하는 기록은 찾지 못했다. 기존 map9/map27·생활동작·구판 장면 원화는 이미 존재하므로 새 시스템이나 중복 등록을 만들지 않는다. ZIP 바이트/해시가 없어 이름을 바꿔 넣은 동일 그림의 부재까지 보장하지는 않는다. B안 UI 스티커는 별개다.

## 판정과 검증 범위

확정은 기존 활동 호출과 전달받은 동작 설명의 정적 대응이다. 후보는 소품·몸짓 또는 현재 실행 경로 확인이 더 필요하다. 보류는 최신 이야기의 대응 호출 미확인 또는 동일 원화 등록 없음이다. 모든 납품은 정적 이미지이며 걷기 애니메이션이 아니다. 정확한 ZIP 내부 이름은 JSON의 null로 남겼다.

최신 대사 데이터는 game/v111/records.json과 game/v111/newworld/d01~d14.json, 조건은 room13_v111_newworld_text.rpy의 R13_NW_WHEN을 대조했다. 각 행의 대사 인용은 키워드와 인물로 좁힌 의미 후보이며 pose 호출 확정이 아니다. 조건부 교체/드롭과 before/after/blocks를 JSON에 표시한다. 대사 전체를 수정하거나 모든 분기를 실플레이하지 않았다.

## 공통 등장·기하 조건

- room13_v111.rpy의 r13_visible_people/r13_stage_people: 원래 스케줄에 현재 바인딩 인물을 합친 뒤 piko_alive/musoe_alive 및 r13_v111_person_alive로 걸러낸다. 피코 장소, 실룩 강제노동, 할머니/선생님 구금, 다람 구금, 가족 위치도 유지한다.
- room13_v111_later_bindings.rpy의 r13_v111_actor_ready: 생존 별칭(OWL_ALIVE/TOK_ALIVE/KKOMI_ALIVE 등), busy/location, 장면의 실제 등장 인물 및 r13_where를 검사한다. 대사 후보에 이 필터가 자동으로 붙는다고 가정하지 않는다.
- map27: 승인 상태, 이벤트 제안 없음, 장소/period/day/flags/replace_poses, daylight/world_width 일치. map9: 원래 존재하는 배우만 변경하고 활동 pose와 장소/period를 검사. map27과 이후 층이 우선할 수 있다.
- life_groups: entry 제외, 조사 활성, 컷/회의/후일담 없음, 날짜/시각/깃발/월드폭, 원래 출석·이벤트 및 공간 검사를 유지. school_play의 conditional_cast는 별도 조건을 가진다.
- 최종 stage 층은 init 337까지 이어진다(docs/OVERRIDE_MAP.md). field_layout의 조사 대상 회피, 발/좌석 기준점, crop·단일 배율, 가구 마스크와 동일 클릭 마스크를 보존해야 한다.
- 회의 착석은 room13-meeting-seated.json과 venue_kind==round 경로다. 최신 NW 회의의 room/field/stone 설정과 동일시하지 않는다.

## 56종 매칭표

| ID | 납품 동작 | 판정 | 캐릭터 / 기존 pose | 활동·대사 근거 | 주요 보류 사항 |
|---|---|---|---|---|---|
| A1-01 | 피코 화판 그림 | 확정 | `resident_piko` / `map27_paint_sketchboard_v2` | VA-2 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A1-02 | 피코 이젤 그림 | 보류 | `resident_piko` / `미확인` | 호출 미확인 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 이젤은 시안 기반. 기존 화판 원화 직접 변환이 아니므로 화판 파일로 추정 매칭하지 않음. |
| A1-03 | 뭉치 상자 정리 | 확정 | `resident_mungchi` / `map9_store_sort_boxes` | store | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A1-04 | 보리 회의 착석 | 보류 | `resident_bori` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. R13_MEETING_SEATED에 이 인물 없음. 다람 마차 seat_* 표정 세트도 별개. |
| A2-01 | 달그락 그릇 진열 | 확정 | `resident_dalgeurak` / `map9_pots_display` | market | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-02 | 굴돌 돌 두드리기 | 확정 | `resident_guldol` / `map9_stone_tapping` | workshop | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-03 | 꽉 그물 당기기 | 확정 | `resident_kkwak` / `map9_river_haul_net` | river | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-04 | 물결 밧줄 감기 | 확정 | `resident_mulgyeol` / `map9_rope_coiling` | river | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-05 | 할머니 열쇠와 장부 | 후보 | `granny` / `living_keyledger` | room13_spatial_contacts.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 현재 기본 여관 pose는 world_counter_wipe; living_keyledger를 기본 동작으로 교체하지 않음. |
| A2-06 | 까로 차축 감싸기 | 후보 | `karo` / `living_axlewrap` | room13_acting.rpy, room13_v111_field_layout.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 납품은 천만 포함, 차축 없음. 기존 배경 차축·손 접점 및 발 기준점 맞춤 필요. |
| A2-07 | 사서 책·종이 정리 | 확정 | `resident_librarian` / `living_bookpaper` | post | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-08 | 모모 등 살피기 | 확정 | `resident_momo` / `living_lampnumber` | post | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-09 | 부엉이 할아버지 앉아 수첩 살피기 | 확정 | `resident_owlgp` / `living_notebook` | inn, dining | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-10 | 설 종줄 다루기 | 확정 | `resident_seol` / `living_bellrope` | room13_spatial_contacts.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-11 | 토실 보온병 | 확정 | `resident_tosil` / `living_thermos` | inn | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A2-12 | 여니 바느질 | 확정 | `resident_yeoni` / `living_mend` | inn_mending, square | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-01 | 도토 장부 쓰기 | 확정 | `doto` / `map27_write_ledger_v2` | VA-9-square, VA-9-hall | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-02 | 종종 편지 분류 | 확정 | `resident_jongjong` / `map27_sort_letters_v2` | VA-11-post | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-03 | 무쇠 오래된 도구 검사 | 확정 | `resident_musoe` / `job_inspect_old_tool` | JOB-MUSOE-OLD-TOOL | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-04 | 누비 여관 빨래 정리 | 확정 | `resident_nubi` / `map9_inn_sort_tie_laundry` | inn | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-05 | 부리 공구함에 손 올리기 | 후보 | `buri` / `event_toolbox` | room13_event_offers.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-06 | 실룩 속삭이기 | 확정 | `resident_siluk` / `event_whisper` | room13_v111_field_layout.rpy, room13_event_offers.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-07 | 슬링 봉투 들고 살피기 | 후보 | `resident_sling` / `event_steam` | room13_event_offers.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 기존 event_steam은 봉투를 김에 쐬는 행동. 단순 봉투 살피기와 의미/소품 동일 여부 미확인. |
| A3-08 | 따닥 망치 들고 날개 뻗기 | 후보 | `resident_ttadak` / `living_repair` | 호출 미확인 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-09 | 선생님 젖은 외투 펼치기 | 확정 | `resident_teacher` / `map9_school_spread_wet_coat` | school | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-10 | 솔방 약초 묶기 | 확정 | `resident_solbang` / `work_herb_bundle` | room13_solbang_chinchilla.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A3-11 | 콩이 회의 착석 | 후보 | `resident_kongi` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. |
| A3-12 | 등지기 등돌 교체 | 확정 | `resident_lamplighter` / `job_replace_lightstone` | JOB-CHORONG-STONE | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-01 | 톡 등 수리 드라이버 | 확정 | `resident_tok` / `map27_ws_1` | WS-1 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-02 | 너울 서류 들고 방향 안내 | 후보 | `neoul` / `map27_ga_1` | GA-1 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 기존 map27_ga_1은 winter_official_navy_v1/map_only. 남색 옷·붉은 완장과 흰 대화 의상 연속성 확인 전 대화에 적용 금지. |
| A4-03 | 칼바람 웅크려 땅 검사 | 확정 | `resident_kalbaram` / `map27_fo_1` | FO-1 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-04 | 나비 당근 썰기 | 확정 | `nabi` / `map27_ki_1` | KI-1 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-05 | 은호 장부 쓰기 | 확정 | `resident_eunho` / `map27_mk_2` | MK-2 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-06 | 구슬 치즈 무게 재기 | 확정 | `resident_guseul` / `map27_mk_3` | MK-3 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-07 | 현이 현악기 연주 | 확정 | `resident_hyeoni` / `map27_mk_8` | MK-8 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-08 | 바둑 등불 들고 주변 살피기 | 확정 | `resident_badook` / `map27_lantern_patrol` | VA-1 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A4-09 | 뿔 회의 착석 | 후보 | `resident_ppul` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. |
| A4-10 | 서리 회의 착석 | 후보 | `resident_seori` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. |
| A4-11 | 토리 회의 착석 | 후보 | `resident_tori` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. |
| A4-12 | 서련 회의 착석 | 후보 | `seryeon` / `meeting_seated` | room13_meeting_seating.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. |
| A5-01 | 다람 착석 | 보류 | `daram` / `미확인` | room13_story_pose.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. R13_MEETING_SEATED에 이 인물 없음. 다람 마차 seat_* 표정 세트도 별개. 납품 설명은 착석만 명시한다. 회의 착석으로 단정하지 않음. 현재 room13/action_2 바닥 그림 그리기와 마차 seat_*는 별도 후보이나 같은 동작인지 미확인. |
| A5-02 | 엄마 조각 보여주기 | 보류 | `mom` / `show_fragments` | r13_ws_lab | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-03 | 판돌 이름 가리키기 | 보류 | `npc_pandol` / `point_name` | r13_st_pandol, r13_cv_morning | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-04 | 초롱엄마 등 건네기 | 보류 | `chorong_mother` / `offer_lantern` | r13_lines(entries,identity,binding_route=None), r13_nt_after_trial | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-05 | 방 방울 아래 두 손 모으기 | 후보 | `kid_bang` / `group_play` | school_play | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음. |
| A5-06 | 도담 국자 맛보기 | 보류 | `kid_dodam` / `lick_ladle` | r13_ws_soup | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-07 | 꼬미 몸 기울여 엿보기 | 보류 | `kid_kkomi` / `door_peek` | r13_wf_hideout | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-08 | 새미 웅크려 그릇 안기 | 보류 | `kid_saemi` / `hide_bowl` | r13_ws_soup | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. |
| A5-09 | 깜 손 흔드는 장난스런 걸음 | 후보 | `kid_kkam` / `group_play` | school_play | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음. |
| A5-10 | 몽 한발 뛰어놀기 | 후보 | `kid_mong` / `group_play` | school_play | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음. |
| A5-11 | 밤이 앉아 수첩 쓰기 | 후보 | `bami` / `action_2` | room13_acting.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. action_2는 정적 후보. 납품 원화의 맨발과 현재 의상/접지 확인 필요. |
| A5-12 | 보듬 쪼그려 빵바구니 천 열기 | 후보 | `bodum` / `activity` | 호출 미확인 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A6-01 | 보리 쪼그려 장작 묶음 끈 조이기 | 확정 | `resident_bori` / `living_firewood` | 호출 미확인 | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. gate는 현재 map27_carry_firewood_v2 우선 배치. 장작 나르기와 끈 조이기를 구분. |
| A6-02 | 토실 닫힌 그림책 가슴에 안기 | 보류 | `resident_tosil` / `hold_storybook` | r13_cv_altar, room13_ep_art.rpy | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 구판 r13_cv_altar/cv:altar:book 후반 전용. 보온병·일반 독서와 혼용 금지. |
| A6-03 | 도토 배급표 두 장 비교 | 확정 | `doto` / `map27_compare_ration_slips_v2` | VA-10-square, VA-10-hall | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |
| A6-04 | 종종 열린 우편가방에 편지 묶음 챙기기 | 확정 | `resident_jongjong` / `map27_pack_satchel_v2` | VA-12-post | 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. |

## A1-01 피코 화판 그림

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_piko`. 기존 pose: `map27_paint_sketchboard_v2`.
- 기존 렌더 파일: `assets/investigation-canonical-20261018/resident_piko--map27_paint_sketchboard_v2.webp`
- 원화 출처: `art/investigation-canonical-20261018/originals/resident_piko--map27_paint_sketchboard_v2.png`
- 조건: `{"life_key":"piko_alive","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"square","periods":[0,1],"replace_poses":["neutral","activity","inn_activity","world"],"max_day":10,"days":[1,3,5,6,7,9]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "그림과 가족 초상 작업", "weekly_locations": [["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"]], "activity": "완성하지 못한 초상에 천을 덮는다."}`
- 코드: `game/systems/room13_event_offers.rpy:29` — "r13_w1c_portrait":("resident_piko",("map27_paint_sketchboard_v2","event_paintwipe","living_paint")),
- 최신 대사 **의미 후보**: `MS14_D02_S03_L0001` (`game/v111/records.json`), when=None, drop=[] — 우체국에서 광장으로. 모모가 피코의 그림을 내려놓고 돌아선다.
- 최신 대사 **의미 후보**: `MS14_D02_S03_L0003` (`game/v111/newworld/d02.json`), when=None, drop=[] — 다음에요, 모모 관장님? 그때면 눈 다 녹겠네. 그림도 젖고.
- 최신 대사 **의미 후보**: `MS14_D02_S03_L0015` (`game/v111/newworld/d02.json`), when=None, drop=[] — 자, 눈부터. 엄마 눈은 아빠 그림보다 커, 작아?
- 최신 대사 **의미 후보**: `MS14_D02_S03_L0022` (`game/v111/newworld/d02.json`), when=None, drop=[] — 그림 팔아서 침대 하나 사야 하는데. 이 그림들이 돈을 안 벌어다 주네요.

## A1-02 피코 이젤 그림

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_piko`. 기존 pose: `미확인`.
- 기존 렌더 파일: 동일 동작 파일 미확인
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"piko_alive","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 이젤은 시안 기반. 기존 화판 원화 직접 변환이 아니므로 화판 파일로 추정 매칭하지 않음.
- 기존 주민 활동·주간 위치: `{"work": "그림과 가족 초상 작업", "weekly_locations": [["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"], ["square", "square", "home"]], "activity": "완성하지 못한 초상에 천을 덮는다."}`
- 최신 대사 **의미 후보**: `NW_D14_MM01` (`game/v111/newworld/d14.json`), when=dead:resident_piko, drop=[] — 광장 3번 등 아래, 피코의 이젤은 그대로 서 있었다.

## A1-03 뭉치 상자 정리

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_mungchi`. 기존 pose: `map9_store_sort_boxes`.
- 기존 렌더 파일: `assets/map-work-nine/resident_mungchi--store_sort_boxes.webp`
- 원화 출처: `assets/resident_mungchi--store_sort_boxes.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_mungchi","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"store","periods":[1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "수집상 집 심부름", "weekly_locations": [["home", "store", "home"], ["home", "store", "home"], ["home", "store", "home"], ["home", "store", "home"], ["home", "store", "home"], ["home", "store", "home"], ["home", "store", "home"]], "activity": "작은 상자와 큰 상자를 따로 쌓는다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A1-04 보리 회의 착석

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_bori`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: 동일 동작 파일 미확인
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_bori","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. R13_MEETING_SEATED에 이 인물 없음. 다람 마차 seat_* 표정 세트도 별개.
- 기존 주민 활동·주간 위치: `{"work": "장작 운반과 가족 돌봄", "weekly_locations": [["gate", "workshop", "square"], ["gate", "store", "home"], ["gate", "workshop", "home"], ["store", "workshop", "square"], ["gate", "store", "home"], ["store", "school", "home"], ["home", "square", "home"]], "activity": "장작을 묶고 끈을 다시 조이고 있다."}`
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사 **의미 후보**: `NW_D07_S02_M01` (`game/v111/newworld/d07.json`), when=None, drop=[] — 회의가 끝난다. 누비는 회관에 남는다. 나는 나비, 보리와 함께 학교로 건너간다.

## A2-01 달그락 그릇 진열

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_dalgeurak`. 기존 pose: `map9_pots_display`.
- 기존 렌더 파일: `assets/map-work-nine/resident_dalgeurak--pots_display.webp`
- 원화 출처: `assets/resident_dalgeurak--pots_display.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_dalgeurak","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"market","periods":[0,1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사 **의미 후보**: `MS14_D06_S01_L0018` (`game/v111/newworld/d06.json`), when=None, drop=[] — 뒤뜰에서 아이 하나가 물동이 뒤로 숨는다. 목에 맨 헝겊 보따리 속에서 빈 그릇이 달그락 부딪친다.

## A2-02 굴돌 돌 두드리기

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_guldol`. 기존 pose: `map9_stone_tapping`.
- 기존 렌더 파일: `assets/map-work-nine/resident_guldol--stone_tapping.webp`
- 원화 출처: `assets/resident_guldol--stone_tapping.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_guldol","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"workshop","periods":[0,1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사 **의미 후보**: `MS14_D11_S03_L0001` (`game/v111/records.json`), when=None, drop=[] — 여관 아래 옛 시설. 자유 상태 할머니의 출입은 이미 확보한 동행자와 함께 통제하고, 구금 상태라면 돌목의 입회 아래 기록·시설만 연다. 아빠 가족만 적대자의 잠긴 집에 무방비로 들어가지 않는다. 굴돌이 실제 동행 가능한 경로에서는 벽 글자 앞에 선다.
- 최신 대사 **의미 후보**: `MS14_D11_S03_L0006` (`game/v111/newworld/d11.json`), when=None, drop=[] — 여기 보시오. 돌판 하나가 떨어져 있소.
- 최신 대사 **의미 후보**: `MS14_D11_S03_L0007` (`game/v111/records.json`), when=None, drop=[] — 굴돌이 관 하나를 두드린다. 돌이 들어 있지 않은 관에서는 빈 소리만 난다.
- 최신 대사 **의미 후보**: `MS14_D13_S04_L0033` (`game/v111/records.json`), when=None, drop=[] — 실룩은 감독 아래 인계한다. 구조했다고 기존 책임이 사라지지 않는다. 모모·굴돌 등 실제 탑승한 사람도 한 명씩 하차하고 목적지 인수를 확인한다. 없는 사람은 추가하지 않는다. 인력이 부족하면 기존 13-B의 보온·감시 대기로 이어지며 전원 완료라고 표시하지 않는다.

## A2-03 꽉 그물 당기기

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_kkwak`. 기존 pose: `map9_river_haul_net`.
- 기존 렌더 파일: `assets/map-work-nine/resident_kkwak--river_haul_net.webp`
- 원화 출처: `assets/resident_kkwak--river_haul_net.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_kkwak","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"river","periods":[1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "빨래 물 나르기와 하천 길 확인", "weekly_locations": [["store", "lowroad", "home"], ["store", "lowroad", "home"], ["store", "lowroad", "home"], ["store", "lowroad", "home"], ["store", "lowroad", "home"], ["store", "lowroad", "home"], ["store", "lowroad", "home"]], "activity": "빈 물통 안의 얼음을 두드린다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A2-04 물결 밧줄 감기

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_mulgyeol`. 기존 pose: `map9_rope_coiling`.
- 기존 렌더 파일: `assets/map-work-nine/resident_mulgyeol--rope_coiling.webp`
- 원화 출처: `assets/resident_mulgyeol--rope_coiling.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_mulgyeol","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"river","periods":[0,1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A2-05 할머니 열쇠와 장부

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `granny`. 기존 pose: `living_keyledger`.
- 기존 렌더 파일: `assets/room13-action-granny-living_keyledger.webp`
- 원화 출처: `art/priority3-actions-20261015/granny/granny-key-ledger-v3.png`
- 조건: `{"life_key":"alive:granny","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 현재 기본 여관 pose는 world_counter_wipe; living_keyledger를 기본 동작으로 교체하지 않음.
- 기존 주민 활동·주간 위치: `{"work": "여관 접수와 옛 돌 운용 자문", "weekly_locations": [["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"]], "activity": "접수대에서 방 열쇠와 장부를 맞춘다."}`
- 코드: `game/systems/room13_spatial_contacts.rpy:64` — elif location=="inn" and r13_world_width()==1920 and person=="granny" and actor["pose"]=="living_keyledger":
- 최신 대사 **의미 후보**: `MS14_D10_S03_L0009` (`game/v111/records.json`), when=None, drop=[] — [플레이어 조작: 핀 뒤를 돌려 구리선 수리를 살핀 뒤 수선 장부·톡의 진술과 함께 제출한다. 핀의 흔한 겉모양만 내면 “같은 걸 쓰는 사람이 얼마나 많은데 그러니?”라는 할머니의 반박 후 관찰 화면으로 돌아간다. 아래 소유 확인은 올바른 묶음을 제출한 뒤에만 나온다.]
- 최신 대사 **의미 후보**: `NW_D08_S02_A03` (`game/v111/newworld/d08.json`), when=None, drop=[] — 그 도토 말이에요. 장부를 정리한다더니, 노인 책상에 펼쳐 놓은 수첩만 자꾸 들여다보더라고요. 그러니 도둑 소리를 들었겠지요.
- 최신 대사 **의미 후보**: `NW_D14_S01_A05` (`game/v111/newworld/d14.json`), when=None, drop=[] — 장부를 다시 넘겨 보다가 찾았어요. 7일, 여관, 안쪽 돌 하나. 할머니가 사 갔어요.
- 최신 대사 **의미 후보**: `NW_D14_S03_A01` (`game/v111/newworld/d14.json`), when=has_ledger, drop=[] — 나는 너울의 장부 뒤에 묶인 종이를 할머니 앞에 펼친다. 날짜와 집 이름, 돌 기구의 수. 한 줄도 빠지지 않았다. 마지막 날짜 옆에 ‘보미’라고 적혀 있다.

## A2-06 까로 차축 감싸기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `karo`. 기존 pose: `living_axlewrap`.
- 기존 렌더 파일: `assets/room13-action-karo-living_axlewrap.webp`
- 원화 출처: `art/priority3-actions-20261015/karo/karo-axlewrap-v2.png`
- 조건: `{"life_key":"alive:karo","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 납품은 천만 포함, 차축 없음. 기존 배경 차축·손 접점 및 발 기준점 맞춤 필요.
- 기존 주민 활동·주간 위치: `{"work": "마차 수리와 반송품 운반", "weekly_locations": [["gate", "post", "inn"], ["gate", "post", "gate"], ["gate", "workshop", "inn"], ["gate", "post", "gate"], ["gate", "post", "inn"], ["gate", "store", "inn"], ["inn", "gate", "inn"]], "activity": "마차 축의 갈라진 부분을 감싼다."}`
- 코드: `game/room13_acting.rpy:283` — ("karo","gate"):"action_2" if period==2 else ("living_axlewrap" if "living_axlewrap" in poses else "action_1"),
- 코드: `game/room13_v111_field_layout.rpy:68` — poses={"guard":"neutral","daram":"thinking","resident_siluk":"event_whisper","karo":"living_axlewrap",
- 최신 대사 **의미 후보**: `MS14_D12_S01_L0001` (`game/v111/records.json`), when=None, drop=[] — 상실 경로의 아침. 아랫길 천막. 아빠가 천을 들어 올리기 전에 까로가 안쪽을 보고 모자를 벗는다. 서로 기대 앉은 몸. 네로의 손 아래 이름표 꾸러미가 놓여 있다. 아이에게 시신 확인을 맡기지 않는다.
- 최신 대사 **의미 후보**: `NW_DLG_D12_01` (`game/v111/newworld/d12.json`), when=None, drop=[] — 아랫길 천막. 까로가 먼저 안을 들여다보고 모자를 벗는다. 서로 기대 앉은 사람들 사이, 네로의 손 아래 이름표 꾸러미가 놓여 있다.

## A2-07 사서 책·종이 정리

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_librarian`. 기존 pose: `living_bookpaper`.
- 기존 렌더 파일: `assets/room13-action-resident_librarian-living_bookpaper.webp`
- 원화 출처: `art/librarian-bookpaper-20261015/librarian_book.png`
- 조건: `{"life_key":"alive:resident_librarian","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "도서관 기록 보존", "weekly_locations": [["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"]], "activity": "젖은 책 사이에 마른 종이를 끼운다."}`
- 최신 대사 **의미 후보**: `MS14_D14_S04_L0002` (`game/v111/records.json`), when=None, drop=[] — 부엉이가 살아 있는 경로에서는 멀리서 자기 걸음으로 다가와 기록을 건네고, 사망 경로에서는 그가 쓰던 종이를 실제 보관자가 가져온다. 피코·사서·네로·아이들도 각 생존 상태에 맞는 행동만 한다.

## A2-08 모모 등 살피기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_momo`. 기존 pose: `living_lampnumber`.
- 기존 렌더 파일: `assets/room13-action-resident_momo-living_lampnumber.webp`
- 원화 출처: `art/map-action-storybook3-20261015/momo/momo-v2.png`
- 조건: `{"life_key":"alive:resident_momo","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "박물관 보관과 옛 생활 자료", "weekly_locations": [["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"], ["library", "library", "home"]], "activity": "낡은 등잔 바닥에 붙은 번호를 읽는다."}`
- 최신 대사 **의미 후보**: `MS14_D13_S04_L0033` (`game/v111/records.json`), when=None, drop=[] — 실룩은 감독 아래 인계한다. 구조했다고 기존 책임이 사라지지 않는다. 모모·굴돌 등 실제 탑승한 사람도 한 명씩 하차하고 목적지 인수를 확인한다. 없는 사람은 추가하지 않는다. 인력이 부족하면 기존 13-B의 보온·감시 대기로 이어지며 전원 완료라고 표시하지 않는다.

## A2-09 부엉이 할아버지 앉아 수첩 살피기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_owlgp`. 기존 pose: `living_notebook`.
- 기존 렌더 파일: `assets/room13-action-resident_owlgp-living_notebook.webp`
- 원화 출처: `art/priority3-actions-20261015/owlgp/owlgp-notebook-binding-v2.png`
- 조건: `{"life_key":"OWL_ALIVE","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님.","custody_life":"OWL_ALIVE=False이면 제외. 기존 주간 위치와 현재 authored/busy/location 우선."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "은퇴 탐정과 등 점검", "weekly_locations": [["square", "library", "inn"], ["square", "library", "inn"], ["square", "library", "inn"], ["square", "library", "inn"], ["square", "library", "inn"], ["square", "library", "inn"], ["square", "library", "inn"]], "activity": "낡은 수첩의 풀린 제본을 묶는다."}`
- 최신 대사 **의미 후보**: `NW_RU_A4_BURNT` (`game/v111/newworld/d14.json`), when=altar4_won_with_burnt_page, drop=[] — 부엉이 어르신 수첩에도 그 벽의 이름이 하나 남아 있었습니다. 보미. 날짜를 적던 아이였다고요.

## A2-10 설 종줄 다루기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_seol`. 기존 pose: `living_bellrope`.
- 기존 렌더 파일: `assets/room13-action-resident_seol-living_bellrope.webp`
- 원화 출처: `art/map-action-storybook3-20261015/seol/seol.png`
- 조건: `{"life_key":"alive:resident_seol","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "종탑과 야간 안내", "weekly_locations": [["tower", "tower", "home"], ["tower", "tower", "home"], ["tower", "tower", "home"], ["tower", "tower", "home"], ["tower", "tower", "home"], ["tower", "tower", "home"], ["tower", "tower", "home"]], "activity": "작은 종의 끈을 풀었다 다시 매단다."}`
- 코드: `game/systems/room13_spatial_contacts.rpy:22` — "resident_seol": dict(poses=("living_bellrope","neutral"),foot=(365,415),ground=460,elevation=45,standing=175),
- 최신 대사 **의미 후보**: `MS14_D10_P01_L0061` (`game/v111/records.json`), when=None, drop=[] — 아빠는 부엉이의 설명만으로 모든 것을 해결했다고 표시하지 않는다. 관찰한 별도 종이와 기존 공개 기록의 대조가 그의 ‘없다’는 주장을 먼저 깬 뒤에, 왜 바로 말을 고치지 않았는지를 듣는다.
- 최신 대사 **의미 후보**: `MS14_D12_S04_L0047` (`game/v111/records.json`), when=None, drop=[] — 최종 입력: 작은 냄비의 파편과 병 / 온전했던 봉인과 재사용 설명 / 교사의 취급 구간과 세척대 진술. 세 항목은 이미 확인한 기록을 자유롭게 골라 결론에 놓는다.
- 최신 대사 **의미 후보**: `NW_H_RE_12` (`game/v111/newworld/d11.json`), when=guldol_listed, drop=[] — 너울의 명단 종이에 이름이 하나 는다. 굴돌. 이유 칸에는 ‘시설 출입’.

## A2-11 토실 보온병

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_tosil`. 기존 pose: `living_thermos`.
- 기존 렌더 파일: `assets/investigation-source2/tosil-thermos-v1.webp`
- 원화 출처: `art/map-actions-20261015/p0-20261016/resident_tosil-living_thermos.png`
- 조건: `{"life_key":"alive:resident_tosil","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 코드: `game/systems/room13_spatial_contacts.rpy:74` — elif location=="inn" and r13_world_width()==1920 and (person,actor["pose"]) in (("resident_nubi","map27_in_1"),("resident_tosil","living_thermos")):
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A2-12 여니 바느질

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_yeoni`. 기존 pose: `living_mend`.
- 기존 렌더 파일: `assets/room13-action-resident_yeoni-living_mend.webp`
- 원화 출처: `art/map-action-storybook3-20261015/yeoni/yeoni.png`
- 조건: `{"life_key":"alive:resident_yeoni","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"life_group":{"id":"inn_mending","status":"approved","location":"inn","days":[2,3,6],"periods":[1],"world_width":1920,"label":"함께 바느질","label_position":[740,104],"need_flags":[],"not_flags":[],"lines":[["resident_tori","여기 한 땀 더 하면 돼요?"],["resident_yeoni","응. 천부터 펴고. 급하게 당기지는 말고."],["resident_tori","이번엔 제가 해 볼게요."]],"art_gap":"","review":"Native SDK desktop/mobile individual/group clicks and non-consuming conversation checks; reports/life-groups-01946."},"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "의복 수선과 물자 교환", "weekly_locations": [["home", "square", "home"], ["square", "square", "home"], ["home", "inn", "home"], ["workshop", "square", "home"], ["home", "square", "home"], ["square", "inn", "home"], ["home", "school", "home"]], "activity": "헤진 소매 안쪽을 뒤집어 살핀다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-01 도토 장부 쓰기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `doto`. 기존 pose: `map27_write_ledger_v2`.
- 기존 렌더 파일: `assets/investigation-canonical-20261018/doto--map27_write_ledger_v2.webp`; `assets/investigation-canonical-20261018/doto--map27_write_ledger_v2.webp`
- 원화 출처: `art/investigation-canonical-20261018/originals/doto--map27_write_ledger_v2.png`
- 조건: `{"life_key":"alive:doto","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"hall","periods":[0],"replace_poses":["action_1"]},{"location":"square","periods":[0,1],"replace_poses":["action_1"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "장부 정리와 광장 배급 보조", "weekly_locations": [["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"]], "activity": "여러 장부의 모서리를 맞춘다."}`
- 최신 대사 **의미 후보**: `MS14_D07_S03_L0001` (`game/v111/records.json`), when=None, drop=[] — [화면] 방문을 열어 둔 채 부엉이가 책상에 서류를 펼친다. 다람은 문과 가까운 의자에 앉는다. 도토는 학교 당번을 교대한 뒤 여관 복도에서 장부를 정리하고 있다. [배치 고정: 침대 발치가 복도 문 안쪽 아래에 가깝다. 책상은 방 안쪽에 있어 문 곁에 웅크린 아이가 닿을 수 없다. 이후 틈은 이 문틀 아래를 도토가 실제로 벌려 만든다. 처음부터 열린 틈이나 새 통로가 아니다.]
- 최신 대사 **의미 후보**: `MS14_D07_S03_L0024` (`game/v111/newworld/d07.json`), when=None, drop=[] — 예, 예. 제 장부도 안으로 가져오겠습니다. 다람아, 내 옆에 앉을래?
- 최신 대사 **의미 후보**: `MS14_D08_S02_L0038` (`game/v111/records.json`), when=None, drop=[] — 문하고 책장부터 다시 보겠습니다. 도토 씨가 서 있던 곳도요.
- 최신 대사 **의미 후보**: `MS14_D09_S04_L0008` (`game/v111/newworld/d09.json`), when=None, drop=[] — 세련이 장부 옆에 보조표를 놓는다. ‘맡긴 사람’ 칸에 여관 이름과 도토의 표시가 있다.

## A3-02 종종 편지 분류

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_jongjong`. 기존 pose: `map27_sort_letters_v2`.
- 기존 렌더 파일: `assets/investigation-canonical-20261018/resident_jongjong--map27_sort_letters_v2.webp`
- 원화 출처: `art/investigation-canonical-20261018/originals/resident_jongjong--map27_sort_letters_v2.png`
- 조건: `{"life_key":"alive:resident_jongjong","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"post","periods":[0],"replace_poses":["neutral","activity","inn_activity","world","map9_letters_waiting"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-03 무쇠 오래된 도구 검사

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_musoe`. 기존 pose: `job_inspect_old_tool`.
- 기존 렌더 파일: `assets/investigation-jobs-20261018/musoe-inspect-old-tool-v1.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"musoe_alive","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"workshop","periods":[0,1,2],"replace_poses":["living_foldmap"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "폐광 통로와 손녀 돌봄", "weekly_locations": [["workshop", "home", "home"], ["workshop", "home", "home"], ["workshop", "home", "home"], ["workshop", "home", "home"], ["workshop", "home", "home"], ["workshop", "home", "home"], ["workshop", "home", "home"]], "activity": "낡은 지도를 접어 안주머니 깊이 넣는다."}`
- 코드: `game/systems/room13_spatial_contacts.rpy:87` — elif location=="workshop" and r13_world_width()==1800 and person=="resident_musoe" and actor["pose"]=="job_inspect_old_tool":
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-04 누비 여관 빨래 정리

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_nubi`. 기존 pose: `map9_inn_sort_tie_laundry`.
- 기존 렌더 파일: `assets/map-work-nine/resident_nubi--inn_sort_tie_laundry.webp`
- 원화 출처: `assets/resident_nubi--inn_sort_tie_laundry.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_nubi","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"inn","periods":[0]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "세탁 협업과 임시 숙박 연결", "weekly_locations": [["inn", "workshop", "store"], ["inn", "workshop", "store"], ["inn", "workshop", "store"], ["inn", "workshop", "store"], ["inn", "workshop", "store"], ["inn", "workshop", "store"], ["inn", "workshop", "store"]], "activity": "마른 빨래를 사람별로 나눠 묶는다."}`
- 최신 대사 **의미 후보**: `MS14_D07_S01_L0002` (`game/v111/newworld/d07.json`), when=None, drop=[] — 빨래 맡길 거면 내일 와요. 누비네 빨래터는 지금 바빠요.
- 최신 대사 **의미 후보**: `MS14_D07_S01_L0004` (`game/v111/newworld/d07.json`), when=None, drop=[] — 빨래터 천이요? 마을에 그런 천이 얼마나 많은데요.
- 최신 대사 **의미 후보**: `MS14_D07_S01_L0007` (`game/v111/newworld/d07.json`), when=None, drop=[] — 내가 써요. 애들도 물 데울 때 쓰고요. 그래서요? 빨래 다 얼어요.
- 최신 대사 **의미 후보**: `MS14_D07_S01_L0046` (`game/v111/newworld/d07.json`), when=None, drop=[] — 빨래터 천이 여기만 있는 줄 알아요?

## A3-05 부리 공구함에 손 올리기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `buri`. 기존 pose: `event_toolbox`.
- 기존 렌더 파일: `assets/room13-action-buri-event_toolbox.webp`
- 원화 출처: `art/event-actions9-20261015/buri-toolbox/buri-toolbox.png`; `art/map-actions-20261015/buri-v7-20261016/buri-v7-event_toolbox.png`
- 조건: `{"life_key":"alive:buri","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "수리점과 조부의 도구 관리", "weekly_locations": [["workshop", "workshop", "home"], ["workshop", "workshop", "home"], ["workshop", "workshop", "home"], ["workshop", "workshop", "home"], ["workshop", "workshop", "home"], ["workshop", "workshop", "home"], ["workshop", "workshop", "home"]], "activity": "작은 부품을 천 위에 순서대로 놓는다."}`
- 코드: `game/systems/room13_event_offers.rpy:36` — "r13_w2e_tools":("buri",("event_toolbox",)),
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-06 실룩 속삭이기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_siluk`. 기존 pose: `event_whisper`.
- 기존 렌더 파일: `assets/room13-action-resident_siluk-event_whisper.webp`
- 원화 출처: `art/event-actions9-20261015/siluk-whisper/room13-pixel-acting-resident_siluk-whisper-v2.png`
- 조건: `{"life_key":"alive:resident_siluk","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "짐 운반과 마구간", "weekly_locations": [["gate", "store", "home"], ["gate", "store", "home"], ["gate", "store", "home"], ["gate", "store", "home"], ["gate", "store", "home"], ["gate", "store", "home"], ["gate", "store", "home"]], "activity": "짐수레 바퀴의 끼인 눈을 털어 낸다."}`
- 코드: `game/room13_v111_field_layout.rpy:68` — poses={"guard":"neutral","daram":"thinking","resident_siluk":"event_whisper","karo":"living_axlewrap",
- 코드: `game/systems/room13_event_offers.rpy:33` — "r13_w1c_testimony":("resident_siluk",("event_whisper",)),
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-07 슬링 봉투 들고 살피기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_sling`. 기존 pose: `event_steam`.
- 기존 렌더 파일: `assets/room13-action-resident_sling-event_steam.webp`
- 원화 출처: `art/event-actions9-20261015/sling-event-steam/sling-event-steam.png`
- 조건: `{"life_key":"alive:resident_sling","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 기존 event_steam은 봉투를 김에 쐬는 행동. 단순 봉투 살피기와 의미/소품 동일 여부 미확인.
- 기존 주민 활동·주간 위치: `{"work": "우편 접수와 마을 안 배달", "weekly_locations": [["post", "square", "post"], ["post", "square", "post"], ["post", "square", "post"], ["post", "square", "post"], ["post", "square", "post"], ["post", "square", "post"], ["post", "square", "post"]], "activity": "봉투를 배달할 순서대로 나눈다."}`
- 코드: `game/systems/room13_event_offers.rpy:30` — "r13_w1c_letters":("resident_sling",("event_steam","thinking")),
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-08 따닥 망치 들고 날개 뻗기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_ttadak`. 기존 pose: `living_repair`.
- 기존 렌더 파일: `assets/room13-pixel-acting-ttadak.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_ttadak","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "건물 보수와 목재 점검", "weekly_locations": [["workshop", "inn", "home"], ["workshop", "inn", "home"], ["workshop", "inn", "home"], ["workshop", "inn", "home"], ["workshop", "inn", "home"], ["workshop", "inn", "home"], ["workshop", "inn", "home"]], "activity": "벽의 벌어진 이음에 나무 조각을 대 본다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-09 선생님 젖은 외투 펼치기

- 판정: 확정. 근거: map9의 기존 인물·활동·파일 등록과 납품 동작 설명이 대응. map27 및 이후 배치층에 의해 대체될 수 있어 최종 활성 여부는 별도 확인.
- 새 파일명: 미확인. 캐릭터: `resident_teacher`. 기존 pose: `map9_school_spread_wet_coat`.
- 기존 렌더 파일: `assets/map-work-nine/resident_teacher--school_spread_wet_coat.webp`
- 원화 출처: `assets/resident_teacher--school_spread_wet_coat.png` (기존 납품 묶음 상대경로, 현재 로컬 원본 미확인)
- 조건: `{"life_key":"alive:resident_teacher","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-work-nine.json":[{"location":"school","periods":[0,1]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "학교와 비상 대피소", "weekly_locations": [["school", "school", "home"], ["school", "school", "home"], ["school", "school", "home"], ["school", "school", "home"], ["school", "school", "home"], ["school", "school", "home"], ["school", "school", "home"]], "activity": "아이들 외투의 젖은 끝을 펴 놓는다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-10 솔방 약초 묶기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_solbang`. 기존 pose: `work_herb_bundle`.
- 기존 렌더 파일: `assets/solbang-chinchilla-map/work_herb_bundle.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_solbang","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"specific":"forest, period 0/1, 이전 pose neutral/world/activity/inn_activity일 때 work_herb_bundle"}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 코드: `game/systems/room13_solbang_chinchilla.rpy:7` — return "work_herb_bundle"
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-11 콩이 회의 착석

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_kongi`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: `assets/room13-meeting-seated-resident_kongi068.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_kongi","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음.
- 기존 주민 활동·주간 위치: `{"work": "가게 심부름과 동네 길 안내", "weekly_locations": [["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"]], "activity": "배달 바구니에서 눌린 빵을 꺼낸다."}`
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A3-12 등지기 등돌 교체

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_lamplighter`. 기존 pose: `job_replace_lightstone`.
- 기존 렌더 파일: `assets/investigation-jobs-20261018/chorong-replace-lightstone-v1.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_lamplighter","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"workshop","periods":[0],"replace_poses":["living_inspectlamp"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "등불 점검과 비밀 식량 전달", "weekly_locations": [["square", "gate", "workshop"], ["square", "greenhouse", "workshop"], ["square", "gate", "greenhouse"], ["square", "library", "workshop"], ["square", "gate", "greenhouse"], ["square", "workshop", "home"], ["square", "gate", "home"]], "activity": "등 아래 점검함을 닫고 매듭을 확인한다."}`
- 최신 대사 **의미 후보**: `MS14_D01_S05_L0019` (`game/v111/records.json`), when=None, drop=[] — 메모: “내가 자리를 비웠으면 광장 등의 초롱에게 소식을 물어봐. 물건은 책상 아래에 두었어.” 끝에 작은 도토리.
- 최신 대사 **의미 후보**: `MS14_D01_S05_L9101` (`game/v111/newworld/d01.json`), when=None, drop=[] — 내가 자리를 비웠으면 광장 등의 초롱에게 소식을 물어봐. 물건은 책상 아래에 두었어. {image=assets/room13-acorn-ink-crooked.png}
- 최신 대사 **의미 후보**: `MS14_D01_S05_L0037` (`game/v111/newworld/d01.json`), when=None, drop=[] — 초롱은 오늘 바깥쪽 등을 보고 돌아와요. 내일 아침이면 광장에 있지. 소식 들으면 나한테도 알려 줘요, 응?
- 최신 대사 **의미 후보**: `MS14_D02_S01_L0009` (`game/v111/records.json`), when=None, drop=[] — 등 덮개가 바람에 달그락거린다. 초롱은 장갑 한쪽을 입에 물고 나사를 조인다.

## A4-01 톡 등 수리 드라이버

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_tok`. 기존 pose: `map27_ws_1`.
- 기존 렌더 파일: `assets/map-action27/WS-1--resident_tok.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"TOK_ALIVE","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"workshop","periods":[0,1],"replace_poses":["neutral","activity","inn_activity","world"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "시계·등·작은 금속 수리", "weekly_locations": [["workshop", "workshop", "square"], ["workshop", "workshop", "home"], ["workshop", "post", "home"], ["workshop", "inn", "home"], ["workshop", "clinic", "home"], ["post", "workshop", "home"], ["square", "workshop", "home"]], "activity": "작은 핀을 집게로 물고 살핀다."}`
- 최신 대사 **의미 후보**: `MS14_D03_S02_L0009` (`game/v111/newworld/d03.json`), when=None, drop=[] — 톡 씨는 걸쇠를 고치라고 맡은 사람입니다. 돌까지 가져갔는지는 등 안부터 보고 따집시다.
- 최신 대사 **의미 후보**: `MS14_D03_S05_L0002` (`game/v111/newworld/d03.json`), when=None, drop=[] — 등을 연 사람은 톡, 하나요. 적혀 있소. 그건 변하지 않소.
- 최신 대사 **의미 후보**: `MS14_D03_S05_L0022` (`game/v111/records.json`), when=None, drop=[] — 톡이 빈 등 앞에서 넓고 무딘 공구를 바깥 걸쇠에 대 본다. 내부 받침에 닿지 않는다. 이어 돌받침 옆 지렛대 틈을 가리킨다.
- 최신 대사 **의미 후보**: `NW_MV_D03_04` (`game/v111/newworld/d03.json`), when=None, drop=[] — 가 봤죠. 수리점이 비었어요. 톡이 광장에 붙들려 있대요. 3번 등 돌을 훔쳤다고.

## A4-02 너울 서류 들고 방향 안내

- 판정: 후보. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `neoul`. 기존 pose: `map27_ga_1`.
- 기존 렌더 파일: `assets/map-action27/GA-1--neoul.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:neoul","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"gate","periods":[0,1,2],"replace_poses":["neutral","activity","inn_activity","world"],"costume_id":"winter_official_navy_v1","usage":"map_only"}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 기존 map27_ga_1은 winter_official_navy_v1/map_only. 남색 옷·붉은 완장과 흰 대화 의상 연속성 확인 전 대화에 적용 금지.
- 기존 주민 활동·주간 위치: `{"work": "광장 질서와 행사 준비", "weekly_locations": [["square", "school", "home"], ["square", "school", "home"], ["square", "school", "home"], ["square", "school", "home"], ["square", "school", "home"], ["square", "school", "home"], ["square", "school", "home"]], "activity": "통행하는 사람들과 길가 짐을 번갈아 살핀다."}`
- 최신 대사 **의미 후보**: `MS14_D13_A_L0004` (`game/v111/records.json`), when=None, drop=[] — 돌목이 엄마 이름의 집행 중지를 명단에 적어 너울에게 보이고, 실제 배급과 자리표를 건넨다. 까로가 세 사람과 함께 입구로 이동한다. 까로는 수레 운반에 동시에 남지 않는다.
- 최신 대사 **의미 후보**: `NW_D05_S04_A01` (`game/v111/newworld/d05.json`), when=None, drop=[] — 너울 아저씨도 입구에서 그랬잖아. 여관에 먼저 연락하라고.

## A4-03 칼바람 웅크려 땅 검사

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_kalbaram`. 기존 pose: `map27_fo_1`.
- 기존 렌더 파일: `assets/map-action27/FO-1--resident_kalbaram.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_kalbaram","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"forest","periods":[0,1,2],"replace_poses":["neutral","activity","inn_activity","world"],"min_day":2}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-04 나비 당근 썰기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `nabi`. 기존 pose: `map27_ki_1`.
- 기존 렌더 파일: `assets/map-action27/KI-1--nabi.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:nabi","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"kitchen","periods":[0],"replace_poses":["neutral","activity","inn_activity","world"],"days":[2,7,12],"min_day":2}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "여관 식사와 임시 운영", "weekly_locations": [["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"], ["inn", "inn", "inn"]], "activity": "그릇 바닥을 닦아 포개 놓는다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-05 은호 장부 쓰기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_eunho`. 기존 pose: `map27_mk_2`.
- 기존 렌더 파일: `assets/map-action27/MK-2--resident_eunho.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_eunho","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"market","periods":[0,1],"replace_poses":["neutral","activity","inn_activity","world"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "도시 물품·보석 거래", "weekly_locations": [["post", "store", "inn"], ["post", "store", "inn"], ["post", "store", "inn"], ["post", "store", "inn"], ["post", "store", "inn"], ["post", "store", "inn"], ["post", "store", "inn"]], "activity": "물자 목록 옆에 값을 다시 적는다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-06 구슬 치즈 무게 재기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_guseul`. 기존 pose: `map27_mk_3`.
- 기존 렌더 파일: `assets/map-action27/MK-3--resident_guseul.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_guseul","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"market","periods":[0,1],"replace_poses":["neutral","activity","inn_activity","world","living_stamp"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "거래품 정리와 견습", "weekly_locations": [["store", "post", "inn"], ["store", "post", "inn"], ["store", "post", "inn"], ["store", "post", "inn"], ["store", "post", "inn"], ["store", "post", "inn"], ["store", "post", "inn"]], "activity": "계약서에 눌린 도장을 닦아 낸다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-07 현이 현악기 연주

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_hyeoni`. 기존 pose: `map27_mk_8`.
- 기존 렌더 파일: `assets/map-action27/MK-8--resident_hyeoni.webp`; `assets/map-action27/MK-8--resident_hyeoni.webp`; `assets/map-action27/MK-8--resident_hyeoni.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_hyeoni","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"dining","periods":[0,1,2],"replace_poses":["neutral","activity","inn_activity","world"]},{"location":"square","periods":[0,1,2],"replace_poses":["neutral","activity","inn_activity","world"]},{"location":"market","periods":[0,1,2],"replace_poses":["neutral","activity","inn_activity","world"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-08 바둑 등불 들고 주변 살피기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_badook`. 기존 pose: `map27_lantern_patrol`.
- 기존 렌더 파일: `assets/map-action27/VA-1--resident_badook.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_badook","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"square","periods":[2],"replace_poses":["living_bootlace"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "야간 순찰과 대피 경호", "weekly_locations": [["gate", "home", "square"], ["gate", "home", "square"], ["gate", "home", "square"], ["gate", "home", "square"], ["gate", "home", "square"], ["gate", "home", "square"], ["gate", "home", "square"]], "activity": "순찰화의 끈을 조여 맨다."}`
- 최신 대사 **의미 후보**: `MS14_D05_S05_L0021` (`game/v111/newworld/d05.json`), when=None, drop=[] — 식당 앞자리에서 아침 먹는 동안은 내가 있겠소. 그 뒤엔 나도 순찰 가야 하오.
- 최신 대사 **의미 후보**: `MS14_D05_S05_L9101` (`game/v111/records.json`), when=None, drop=[] — 내일 아침, 식당 앞자리에서 바둑이와 다람이 함께 기다린다. 순찰 전까지 아빠가 안 오면 둘이 초소로 간다. 종일 보호 약속은 아니다.
- 최신 대사 **의미 후보**: `NW_DLG_D05_01` (`game/v111/newworld/d05.json`), when=None, drop=[] — 문간에 바둑이가 와 있다. 순찰 길에 들른 참이다.

## A4-09 뿔 회의 착석

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_ppul`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: `assets/room13-meeting-seated-resident_ppul068.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_ppul","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음.
- 기존 주민 활동·주간 위치: `{"work": "촌장·배급·경비 지휘", "weekly_locations": [["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"]], "activity": "식량 나눔표 위에 작은 돌을 눌러 둔다."}`
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-10 서리 회의 착석

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_seori`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: `assets/room13-meeting-seated-resident_seori068.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_seori","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음.
- 기존 주민 활동·주간 위치: `{"work": "외부 관리국 검사와 사실 확인", "weekly_locations": [["post", "clinic", "inn"], ["post", "clinic", "inn"], ["post", "clinic", "inn"], ["post", "clinic", "inn"], ["post", "clinic", "inn"], ["post", "clinic", "inn"], ["post", "clinic", "inn"]], "activity": "메모 옆에 확인한 사람 이름을 적는다."}`
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-11 토리 회의 착석

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_tori`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: `assets/room13-meeting-seated-resident_tori068.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:resident_tori","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음.
- 기존 주민 활동·주간 위치: `{"work": "광장 수선과 여관 납품", "weekly_locations": [["square", "square", "home"], ["square", "inn", "home"], ["home", "square", "home"], ["workshop", "inn", "home"], ["square", "home", "home"], ["square", "inn", "home"], ["home", "square", "inn"]], "activity": "접힌 천의 바늘땀을 세고 있다."}`
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A4-12 서련 회의 착석

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `seryeon`. 기존 pose: `meeting_seated`.
- 기존 렌더 파일: `assets/room13-meeting-seated-seryeon068.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:seryeon","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음.
- 코드: `game/room13_meeting_seating.rpy:22` — R13_MEETING_SEATED=r13_meeting_json.load(renpy.file("assets/room13-meeting-seated.json")) if renpy.loadable("assets/room13-meeting-seated.json") else {}
- 코드: `game/room13_meeting_seating.rpy:118` — if seated and who in R13_MEETING_SEATED:
- 코드: `game/room13_meeting_seating.rpy:119` — spec=R13_MEETING_SEATED[who]
- 코드: `game/room13_meeting_seating.rpy:130` — spec=R13_MEETING_SEATED.get(who) if seated else None
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A5-01 다람 착석

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `daram`. 기존 pose: `미확인`.
- 기존 렌더 파일: 동일 동작 파일 미확인
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:daram","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"meeting":"기존 seated 사용은 venue_kind==round. 현재 R13_NW_MEETINGS room/field/stone 및 인물별 생존/참석 필터와 구분."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 회의 등록만으로 현재 회의에 착석 그림이 쓰인다고 볼 수 없음. R13_MEETING_SEATED에 이 인물 없음. 다람 마차 seat_* 표정 세트도 별개. 납품 설명은 착석만 명시한다. 회의 착석으로 단정하지 않음. 현재 room13/action_2 바닥 그림 그리기와 마차 seat_*는 별도 후보이나 같은 동작인지 미확인.
- 코드: `game/systems/room13_story_pose.rpy:18` — r13_daram_story_activity: 첫날 room13의 action_2/inspect_floor 분기; 납품 착석과 동일성 미확인
- 최신 대사 **의미 후보**: `MS14_D01_S05_L0043` (`game/v111/newworld/d01.json`), when=None, drop=[] — ……마차도 없으면?
- 최신 대사 **의미 후보**: `MS14_D04_S04_L0001` (`game/v111/records.json`), when=None, drop=[] — 밝은 초소 안. 바둑이가 문가에 앉고, 밤이는 문이 보이는 의자를 고른다. 아빠와 다람도 함께 있다.
- 최신 대사 **의미 후보**: `MS14_D05_S05_L0025` (`game/v111/newworld/d05.json`), when=None, drop=[] — 창문 보이는 자리. 거기 앉을래.
- 최신 대사 **의미 후보**: `MS14_D06_S01_L0009` (`game/v111/newworld/d06.json`), when=None, drop=[] — 다돌이라고 합니다. 얘는 제 딸 다람이고요. 낮에 이 아이가 앉아 있을 자리만이라도 부탁드립니다. 제가 어디 가는지는 여기 적어 놓겠습니다.

## A5-02 엄마 조각 보여주기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `mom`. 기존 pose: `show_fragments`.
- 기존 렌더 파일: `assets/room13-fullbody-mom-pose-show_fragments.webp`; `assets/dialogue-pose-source/mom/show_fragments/560.webp`; `assets/dialogue-pose-source/mom/show_fragments/760.webp`; `assets/dialogue-pose-source/mom/show_fragments/840.webp`
- 원화 출처: `art/approved-remaining22/originals/mom--show_fragments.png`
- 조건: `{"life_key":"alive:mom","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/systems/room13_ep5_soup.rpy:313` / `r13_ws_lab` — ("mom","이 조각 셋을 한데 모아 볼게. 잘 봐.",{"pose":"show_fragments"}),
- 최신 대사 **의미 후보**: `MS14_D02_S04_L9101` (`game/v111/records.json`), when=None, drop=[] — 네로: 엄마에게 교환함 옆에서 식량을 줬다. 엄마는 혼자였고 빵 한 조각을 먹고 남은 것을 싸 갔다. 물자는 학교 옆 공동 창고에서 받는다. 함 너머의 거처는 모른다.
- 최신 대사 **의미 후보**: `MS14_D04_S01_L9102` (`game/v111/records.json`), when=None, drop=[] — 네로: 엄마에게 교환함 옆에서 식량을 줬다. 엄마는 혼자였고 빵 한 조각을 먹고 남은 것을 싸 갔다. 물자는 학교 옆 공동 창고에서 받는다. 함 너머의 거처는 모른다.
- 최신 대사 **의미 후보**: `MS14_D11_S02B_L0044` (`game/v111/newworld/d11.json`), when=None, drop=[] — 그전에, 할머니가 날 아래 시설로 데려간 적이 있어. 사람을 보내야 돌을 살릴 수 있다고 했어. 그런데…… 벽의 글하고 남은 조각을 봤어. 거기 적힌 건 사람을 새로 보내라는 게 아니었어.
- 최신 대사 **의미 후보**: `MS14_D14_S04_L0016` (`game/v111/records.json`), when=None, drop=[] — 학교 인계대. 엄마가 아직 쓰지 않은 돌 조각과 이미 사용 중인 받침의 표를 나눠 놓는다. 숫자는 실제 회수·소모·인계 상태에서 계산한다. 사라진 물자를 새 숫자로 채우지 않는다. 사용 중인 학교 돌을 빼서 전시하지 않고 해당 자리로 함께 가 확인한다.

## A5-03 판돌 이름 가리키기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `npc_pandol`. 기존 pose: `point_name`.
- 기존 렌더 파일: `assets/room13-fullbody-npc_pandol-pose-point_name.webp`; `assets/dialogue-pose-source/npc_pandol/point_name/560.webp`; `assets/dialogue-pose-source/npc_pandol/point_name/760.webp`; `assets/dialogue-pose-source/npc_pandol/point_name/840.webp`
- 원화 출처: `art/approved-remaining22/originals/npc_pandol--point_name.png`
- 조건: `{"life_key":"alive:npc_pandol","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/systems/room13_ep_story.rpy:98` / `r13_st_pandol` — ("npc_pandol","그래서 매일 와서 이름을 손가락으로 짚어 보오. 이것까지 잊으면, 할멈은 정말 없는 사람이 되니까.",{"pose":"point_name"}),
- 코드: `game/systems/room13_ep6_cart.rpy:130` / `r13_cv_morning` — (None,"게시판 앞에 판돌 영감이 지팡이를 짚고 서 있었다. 자기 이름을 손가락으로 몇 번이고 짚었다.",{"show":"npc_pandol","pose":"point_name"}),
- 최신 대사 **의미 후보**: `MS14_D13_S02_L0012` (`game/v111/records.json`), when=None, drop=[] — 저녁. 광장으로 돌아가는 길. 판돌이 탄 수레를 본다. 회색 담요 끝에서 아침의 새 천이 보인다. 엄마는 아빠 옆에 있으며 수레에 타 있지 않다. 너울이 엄마 이름이 있는 명단을 들고 다가온다.
- 최신 대사 **의미 후보**: `MS14_D14_S02_L0081` (`game/v111/records.json`), when=None, drop=[] — 플레이어가 판돌의 학교 인수 완료가 적힌 줄을 펼친다. 그 아래 다른 이름은 실제 인수된 경우만 보인다. 새로운 구조자나 생존자를 추가하지 않는다.
- 최신 대사 **의미 후보**: `NW_AUD_D13_02` (`game/v111/newworld/d13.json`), when=None, drop=[] — 나는 수첩을 펴고 사람들 앞에서 읽는다. 판돌 씨에게 전해진 거짓 전언, 그리고 수레에 실린 이름들. 다 읽기도 전에, 구경하던 주민 하나가 너울의 소매를 움켜쥔다.

## A5-04 초롱엄마 등 건네기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `chorong_mother`. 기존 pose: `offer_lantern`.
- 기존 렌더 파일: `assets/room13-fullbody-chorong_mother-pose-offer_lantern.webp`; `assets/dialogue-pose-source/chorong_mother/offer_lantern/560.webp`; `assets/dialogue-pose-source/chorong_mother/offer_lantern/760.webp`; `assets/dialogue-pose-source/chorong_mother/offer_lantern/840.webp`
- 원화 출처: `art/approved-remaining22/originals/chorong_mother--offer_lantern.png`
- 조건: `{"life_key":"alive:chorong_mother","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/room13.rpy:59` / `r13_lines(entries,identity,binding_route=None)` — # own (e.g. {"show":"chorong_mother","pose":"offer_lantern"}); narration keeps them.
- 코드: `game/systems/room13_ep4_night13.rpy:385` / `r13_nt_after_trial` — (None,"초롱의 어머니가 말했다. \"그저께 밤에 그 애 대신 켜 주셨다지요. 동쪽 등 셋. 우리 집 창에서 보였어요. 그 애가 돌아온 줄 알았어요.\"",{"show":"chorong_mother","pose":"offer_lantern"}),
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A5-05 방 방울 아래 두 손 모으기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_bang`. 기존 pose: `group_play`.
- 기존 렌더 파일: `assets/room13-group-kid_bang-play.webp`
- 원화 출처: `art/resident-life-groups-20261018/originals/kid_bang-play-source.png`
- 조건: `{"life_key":"alive:kid_bang","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"life_group":{"id":"school_play","status":"approved","location":"school","days":[8,9],"periods":[0,1],"world_width":1800,"label":"아이들과 함께 이야기","label_position":[1300,290],"conditional_cast":true,"need_flags":["kids_school","wf_kkomi_saved","st_kkomi_class_seen"],"not_flags":["soup_kids_dead","kkomi_dead","kkomi_dead_soup"],"lines":[["kid_kkam","이번엔 내가 먼저!"],["kid_mong","같이 해. 하나, 둘!"],["kid_bang","잠깐, 나도!"],["kid_kkam","그럼 다시. 하나!"]],"individual_lines":{"kid_kkam":"이번엔 내 차례예요!","kid_mong":"하나, 둘! 같이 세고 있어요.","kid_bang":"잠깐만요. 저도 같이 할래요!"},"art_gap":"","review":"Native SDK desktop/mobile individual/group clicks and non-consuming conversation checks; reports/life-groups-01946.","member_conversation":true}}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A5-06 도담 국자 맛보기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_dodam`. 기존 pose: `lick_ladle`.
- 기존 렌더 파일: `assets/room13-fullbody-kid_dodam-pose-lick_ladle.webp`; `assets/dialogue-pose-source/kid_dodam/lick_ladle/560.webp`; `assets/dialogue-pose-source/kid_dodam/lick_ladle/760.webp`; `assets/dialogue-pose-source/kid_dodam/lick_ladle/840.webp`
- 원화 출처: `art/approved-remaining22/originals/kid_dodam--lick_ladle.png`
- 조건: `{"life_key":"alive:kid_dodam","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/systems/room13_ep5_soup.rpy:374` / `r13_ws_soup` — ("kid_dodam","선생님, 오늘 수프 진짜 맛있다.",{"pose":"lick_ladle"}),
- 최신 대사 **의미 후보**: `NW_D12_EO03` (`game/v111/newworld/d12.json`), when=None, drop=[] — 도담이 빈 그릇을 들고 와 한 그릇 더 달라고 한다. 나비가 웃으며 국자를 든다.

## A5-07 꼬미 몸 기울여 엿보기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_kkomi`. 기존 pose: `door_peek`.
- 기존 렌더 파일: `assets/room13-fullbody-kid_kkomi-pose-door_peek.webp`; `assets/dialogue-pose-source/kid_kkomi/door_peek/560.webp`; `assets/dialogue-pose-source/kid_kkomi/door_peek/760.webp`; `assets/dialogue-pose-source/kid_kkomi/door_peek/840.webp`
- 원화 출처: `art/approved-remaining22/originals/kid_kkomi--door_peek.png`
- 조건: `{"life_key":"KKOMI_ALIVE","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/systems/room13_ep3_woodfire.rpy:221` / `r13_wf_hideout` — ("kid_kkomi","누구야! ……나비 누나 그릇이네. 누나 심부름이야?",{"pose":"door_peek"}),
- 최신 대사 **의미 후보**: `MS14_D06_S02_L0001` (`game/v111/records.json`), when=None, drop=[] — [소리] 틈새 바람, 얇은 깡통 두드리는 소리. 꼬미가 다람에게 천장 못에 매단 줄을 보여 준다. 문을 열면 깡통이 울린다.
- 최신 대사 **의미 후보**: `MS14_D06_S02_L0013` (`game/v111/records.json`), when=None, drop=[] — 아이는 학교로 돌아간다. 꼬미가 창고 문을 발로 받치고 보리의 수레를 잡아 준다.
- 최신 대사 **의미 후보**: `MS14_D06_S02_L0023` (`game/v111/newworld/d06.json`), when=None, drop=[] — 자리 생기면 이 도토리 찾으러 와. 그럼 비밀 문 열어 줄게.
- 최신 대사 **의미 후보**: `MS14_D06_P01_L0004` (`game/v111/newworld/d06.json`), when=None, drop=[] — 진짜 들어가도 돼요? 문 닫고 나서…… 쫓아내면 싫어요.

## A5-08 새미 웅크려 그릇 안기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_saemi`. 기존 pose: `hide_bowl`.
- 기존 렌더 파일: `assets/room13-fullbody-kid_saemi-pose-hide_bowl.webp`; `assets/dialogue-pose-source/kid_saemi/hide_bowl/560.webp`; `assets/dialogue-pose-source/kid_saemi/hide_bowl/760.webp`; `assets/dialogue-pose-source/kid_saemi/hide_bowl/840.webp`
- 원화 출처: `art/approved-remaining22/originals/kid_saemi--hide_bowl.png`
- 조건: `{"life_key":"alive:kid_saemi","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음.
- 코드: `game/systems/room13_ep5_soup.rpy:376` / `r13_ws_soup` — (None,"새미가 반만 먹고 그릇을 무릎에 감췄다.",{"show":"kid_saemi","pose":"hide_bowl"}),
- 최신 대사 **의미 후보**: `MS14_D12_S03_L0001` (`game/v111/records.json`), when=None, drop=[] — 저녁. 아빠가 운반 상자를 문 안에 내린다. 노래가 중간에서 끊겨 있다. 새미는 숟가락을 그릇 위에 가로놓았고, 보리는 6일 학교 앞에서 기다리던 자기 아이 도담을 흔들어 부르고 있다.
- 최신 대사 **의미 후보**: `MS14_D12_A_L0011` (`game/v111/records.json`), when=None, drop=[] — 아이들 이동과 두 냄비·그릇 보존 뒤 12-4의 병·봉인·동선 대결로 이어진다. ‘같이 먹었다’, 새미의 식사 관찰, 증상·쓴맛·사망 대사는 삭제. 시간 대사 세 개를 다음으로 정확히 교체한다.
- 최신 대사 **의미 후보**: `NW_AUD_D12_01` (`game/v111/newworld/d12.json`), when=None, drop=[] — 나비가 흰 그릇을 하나씩 놓는다. 새미 앞, 그리고 의자를 끌어다 앉은 아이들 앞이다.
- 최신 대사 **의미 후보**: `NW_D12_S02_A02` (`game/v111/newworld/d12.json`), when=None, drop=[] — 도담이 보리 옆자리를 찾다가, 자리가 없는 새미 옆에 앉는다. 도담 앞에도 흰 그릇이 놓인다.

## A5-09 깜 손 흔드는 장난스런 걸음

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_kkam`. 기존 pose: `group_play`.
- 기존 렌더 파일: `assets/room13-group-kid_kkam-play.webp`
- 원화 출처: `art/resident-life-groups-20261018/originals/kid_kkam-play-source.png`
- 조건: `{"life_key":"alive:kid_kkam","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"life_group":{"id":"school_play","status":"approved","location":"school","days":[8,9],"periods":[0,1],"world_width":1800,"label":"아이들과 함께 이야기","label_position":[1300,290],"conditional_cast":true,"need_flags":["kids_school","wf_kkomi_saved","st_kkomi_class_seen"],"not_flags":["soup_kids_dead","kkomi_dead","kkomi_dead_soup"],"lines":[["kid_kkam","이번엔 내가 먼저!"],["kid_mong","같이 해. 하나, 둘!"],["kid_bang","잠깐, 나도!"],["kid_kkam","그럼 다시. 하나!"]],"individual_lines":{"kid_kkam":"이번엔 내 차례예요!","kid_mong":"하나, 둘! 같이 세고 있어요.","kid_bang":"잠깐만요. 저도 같이 할래요!"},"art_gap":"","review":"Native SDK desktop/mobile individual/group clicks and non-consuming conversation checks; reports/life-groups-01946.","member_conversation":true}}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음.
- 최신 대사 **의미 후보**: `NW_D13_S02_A02` (`game/v111/newworld/d13.json`), when=listed:daram, drop=[] — 순찰대원이 다람의 손목 끈을 짐칸 고리에 건다. 나는 그 손을 쳐낸다. 너울은 눈도 깜박이지 않는다.

## A5-10 몽 한발 뛰어놀기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `kid_mong`. 기존 pose: `group_play`.
- 기존 렌더 파일: `assets/room13-group-kid_mong-play.webp`
- 원화 출처: `art/resident-life-groups-20261018/originals/kid_mong-play-source.png`
- 조건: `{"life_key":"alive:kid_mong","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"life_group":{"id":"school_play","status":"approved","location":"school","days":[8,9],"periods":[0,1],"world_width":1800,"label":"아이들과 함께 이야기","label_position":[1300,290],"conditional_cast":true,"need_flags":["kids_school","wf_kkomi_saved","st_kkomi_class_seen"],"not_flags":["soup_kids_dead","kkomi_dead","kkomi_dead_soup"],"lines":[["kid_kkam","이번엔 내가 먼저!"],["kid_mong","같이 해. 하나, 둘!"],["kid_bang","잠깐, 나도!"],["kid_kkam","그럼 다시. 하나!"]],"individual_lines":{"kid_kkam":"이번엔 내 차례예요!","kid_mong":"하나, 둘! 같이 세고 있어요.","kid_bang":"잠깐만요. 저도 같이 할래요!"},"art_gap":"","review":"Native SDK desktop/mobile individual/group clicks and non-consuming conversation checks; reports/life-groups-01946.","member_conversation":true}}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. group_play 원화와 납품 몸짓 동일성 미확인. 정적 그림이며 걷기/점프 애니메이션으로 등록하지 않음.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A5-11 밤이 앉아 수첩 쓰기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `bami`. 기존 pose: `action_2`.
- 기존 렌더 파일: `assets/room13-pixel-acting-bami.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:bami","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. action_2는 정적 후보. 납품 원화의 맨발과 현재 의상/접지 확인 필요.
- 기존 주민 활동·주간 위치: `{"work": "처마 거처와 밤길 관찰", "weekly_locations": [["inn", "home", "inn"], ["inn", "home", "inn"], ["inn", "home", "inn"], ["inn", "home", "inn"], ["inn", "home", "inn"], ["inn", "home", "inn"], ["inn", "home", "inn"]], "activity": "따뜻한 처마 가까이 몸을 움츠린다."}`
- 코드: `game/room13_acting.rpy:292` — ("bami","hall"):"action_2" if period==2 else "action_1",
- 코드: `game/room13_acting.rpy:293` — ("bami","inn"):"action_2" if r13_has("bami_protected") or period==2 else "action_1",
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A5-12 보듬 쪼그려 빵바구니 천 열기

- 판정: 후보. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `bodum`. 기존 pose: `activity`.
- 기존 렌더 파일: `assets/room13-pixel-acting-bodum.webp`
- 원화 출처: 독립 원화 경로 미확인. 기존 렌더 파일만으로 납품 원화 동일성 단정 금지.
- 조건: `{"life_key":"alive:bodum","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A6-01 보리 쪼그려 장작 묶음 끈 조이기

- 판정: 확정. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_bori`. 기존 pose: `living_firewood`.
- 기존 렌더 파일: `assets/room13-action-resident_bori-living_firewood.webp`
- 원화 출처: `art/bori-nero-storybook-20261015/bori/bori-firewood-plump-v2.png`
- 조건: `{"life_key":"alive:resident_bori","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"pose_selection":"room13_acting.rpy r13_living_pose의 장소 allowlist/desired/첫 living_ fallback과 후속 배치층을 함께 확인. 등록된 pose가 매번 선택되는 것은 아님."}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. gate는 현재 map27_carry_firewood_v2 우선 배치. 장작 나르기와 끈 조이기를 구분.
- 기존 주민 활동·주간 위치: `{"work": "장작 운반과 가족 돌봄", "weekly_locations": [["gate", "workshop", "square"], ["gate", "store", "home"], ["gate", "workshop", "home"], ["store", "workshop", "square"], ["gate", "store", "home"], ["store", "school", "home"], ["home", "square", "home"]], "activity": "장작을 묶고 끈을 다시 조이고 있다."}`
- 최신 대사 **의미 후보**: `MS14_D06_S02_L0014` (`game/v111/newworld/d06.json`), when=None, drop=[] — 보리가 말없이 장작 두 개를 문 옆으로 던진다. 갈라진 손바닥에 나무 가시가 박힌다. 그의 수레 아래에는 여관 표가 찍힌 장작이 담요로 덮여 있다.
- 최신 대사 **의미 후보**: `MS14_D06_S03_L0011` (`game/v111/records.json`), when=None, drop=[] — [조작] 물통을 받아 천 적시기 → 보리에게 건네기 → 옆문 장작 밀어내기. 각 입력 뒤 화면은 조금씩 가까워지지만, 열린 통로와 쓰러지는 지붕을 함께 보여 준다.
- 최신 대사 **의미 후보**: `MS14_D06_S04_L0025` (`game/v111/newworld/d06.json`), when=None, drop=[] — 아이들부터 재워 주십시오. 보리 씨가 아이를 안고 나온 건 제 눈으로 봤습니다. 장작을 훔쳤으니 불까지 놓았다고 보시는 겁니까?
- 최신 대사 **의미 후보**: `MS14_D06_S04_L0028` (`game/v111/newworld/d06.json`), when=None, drop=[] — 아이 넷은 학교에 있습니다. 보리 씨가 불을 끄려 한 것도 봤습니다. 장작을 훔친 일과 불이 난 일은 따로 봐 주십시오.

## A6-02 토실 닫힌 그림책 가슴에 안기

- 판정: 보류. 근거: 기존 pose/원화 등록 및 코드 인용 참조. 최신 대사 후보는 별도이며 원화 존재만으로 최신 실행 연결을 확정하지 않음.
- 새 파일명: 미확인. 캐릭터: `resident_tosil`. 기존 pose: `hold_storybook`.
- 기존 렌더 파일: `assets/room13-fullbody-resident_tosil-pose-hold_storybook.webp`; `assets/dialogue-pose-source/resident_tosil/hold_storybook/560.webp`; `assets/dialogue-pose-source/resident_tosil/hold_storybook/760.webp`; `assets/dialogue-pose-source/resident_tosil/hold_storybook/840.webp`
- 원화 출처: `art/approved-remaining22/originals/resident_tosil--hold_storybook.png`
- 조건: `{"life_key":"alive:resident_tosil","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류. 최신 이야기의 동일 행동 호출이 확인되지 않거나 직접 대응 원화 등록이 없음. 구판 장면을 새 이야기로 자동 이식하지 않음. 구판 r13_cv_altar/cv:altar:book 후반 전용. 보온병·일반 독서와 혼용 금지.
- 코드: `game/systems/room13_ep6_cart.rpy:355` / `r13_cv_altar` — ([("resident_tosil","……이거. 할머니가 맨날 읽어 주던 거야. 너 줄라고 가져왔어.",{"pose":"hold_storybook"}),
- 코드: `game/systems/room13_ep_art.rpy:132` — if packet[0]=="resident_tosil" and options.get("pose")=="hold_storybook" and "book" not in options:
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A6-03 도토 배급표 두 장 비교

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `doto`. 기존 pose: `map27_compare_ration_slips_v2`.
- 기존 렌더 파일: `assets/investigation-canonical-20261018/doto--map27_compare_ration_slips_v2.webp`; `assets/investigation-canonical-20261018/doto--map27_compare_ration_slips_v2.webp`
- 원화 출처: `art/investigation-canonical-20261018/originals/doto--map27_compare_ration_slips_v2.png`
- 조건: `{"life_key":"alive:doto","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"hall","periods":[1,2],"replace_poses":["action_1","action_2"]},{"location":"square","periods":[2],"replace_poses":["action_1"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 기존 주민 활동·주간 위치: `{"work": "장부 정리와 광장 배급 보조", "weekly_locations": [["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"], ["square", "post", "home"]], "activity": "여러 장부의 모서리를 맞춘다."}`
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## A6-04 종종 열린 우편가방에 편지 묶음 챙기기

- 판정: 확정. 근거: map27의 기존 request_id·활동 설명·동작 등록과 대응. 날짜/장소/깃발/replace_poses/이벤트 제안 조건을 그대로 보존.
- 새 파일명: 미확인. 캐릭터: `resident_jongjong`. 기존 pose: `map27_pack_satchel_v2`.
- 기존 렌더 파일: `assets/investigation-canonical-20261018/resident_jongjong--map27_pack_satchel_v2.webp`
- 원화 출처: `art/investigation-canonical-20261018/originals/resident_jongjong--map27_pack_satchel_v2.png`
- 조건: `{"life_key":"alive:resident_jongjong","shared":["r13_v111_person_alive","r13_visible_people","r13_where","r13_v111_actor_ready（장면 호출에서 사용되는 경우）"],"room13-map-action27.json":[{"location":"post","periods":[1,2],"replace_poses":["neutral","activity","inn_activity","world","map9_letters_waiting"]}]}`
- 보류/새 아트 확인: 새 ZIP과 매니페스트 미열람: 납품 파일명·픽셀·출처 동일성 및 실행 검증 전 적용 보류.
- 최신 대사: 이 동작에 대응한다고 확정할 대사 ID 없음. 기존 활동 호출 이상의 연결 금지.

## 검사와 미실행

검증 통과: 56개 고유 ID, 차수별 4·12·12·12·12·4개, JSON 파싱, 등록된 기존 렌더 파일과 로컬 원화 경로의 존재, 참조 코드 파일·줄 범위, 대사 근거 파일 존재. map9 원화 7개는 과거 납품 묶음 상대경로만 확인되므로 로컬 원본 존재 확인 대상에서 제외하고 미확인으로 표기했다. git diff --check 통과. 문서 두 파일 외 변경 없음. 새 에셋을 로드하지 않았으므로 Ren'Py lint/이미지 배율/맵→대화 전환/생존 분기/모바일 터치 실화면 검증은 미실행. 이 문서로 적용 승인을 대체하지 않는다.
