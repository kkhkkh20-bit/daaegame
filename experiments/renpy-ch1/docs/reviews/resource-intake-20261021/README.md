# Approved resource intake — 2026-10-21

Source: `art/resource-intake-20261021` @ `ae62bf081fce0e08eebbbf2dcd8896292175bd56`, `design/resource-intake-20261021/`. All three ZIP SHA256 values verified before extracting. Original bytes remain at that commit; no regenerated images or map candidates.

## Connected source data

16 exact existing contexts, 48 lossless WebP profiles (560/760/840). Uses the existing context-art renderer. General six-slot registries, story code, flags, evidence, schedules, maps, furniture and world sprites are unchanged. Four previously connected context entries are preserved.

All ten Daram poses use one source canvas and one scale per height, calibrated to the existing neutral visible height. Leaning poses retain their lower head height. All profiles use the existing canvas and foot baseline. Profiles 760/840 preserve the existing close-up framing; they are not claims that full feet fit on a 720px screen.

| Asset | Exact existing context | Index | Text |
|---|---|---:|---|
| 01_bravado | `MS14_D01_S01_L0013` | 3 | 십삼 호. 내가 외웠어. 아빠는 짐 들어. |
| 02_reproach_lean | `MS14_D03_S02_L0007` | 5 | 어제 고친다고 했잖아. |
| 03_stubborn | `MS14_D01_S04_L0006` | 4 | 외 한 명 말고, 다람. |
| 04_flustered | `MS14_D01_S03_L0005` | 2 | ‘외 한 명’은 나야? 내 이름도 썼는데. |
| 05_playful_evasion | `MS14_D02_S03_L0018` | 8 | 냄비 또 태웠다고 할 때. |
| 06_eureka | `MS14_D03_S03_L0020` | 7 | 아빠. 초롱은 돌이 있었댔잖아. 이 사람은 언제 꺼냈는데? |
| 07_delighted | `MS14_D03_S06_L0003` | 1 | 따뜻해. |
| 08_scared_brave | `MS14_D03_S04_L0003` | 1 | 아빠, 비켜. |
| 09_wipe_tears | `MS14_D03_S06_L0018` | 4 | 약속은 내가 했는데, 피코는 못 왔네. |
| 10_resolve | `MS14_D02_S04_L0027` | 3 | 그림 내가 들게. 안 눌리게. |
| kkomi_anxious | `wf:hideout:refuse` | 1 | 학교는 표 있는 애들 데잖아. 거기 가면 어른들이 이름 물어보고, 그러다 보호소 보내. |
| kkomi_joy | `st:kkomi_class` | 1 | 이게 꼬, 이게 미. 대장 이름부터 외워. |
| dodam_joy | `st:dodam` | 3 | (작게) 휘휘 저어라 겨울 수프, 감자 하나 당근 하나…… |
| saemi_anxious | `ws:soup:all` | 0 | 일어나. 일어나, 도담아. 불 켜졌어. 따뜻해졌어. |
| ubak_anxious | `ep1:ubak` | 3 | 그 아주머니가…… 저 때문이에요? |
| ubak_angry | `MS14_D03_S03_L0023` | 10 | 말을 끝까지 좀 들으세요. |

The ten Daram contexts and angry Ubak context belong to the current D01–D03 native story. The remaining five expressions are bound to existing legacy episode contexts, not newly added to the current D01–D03 story. The supplied six-expression manifest references `production_manifest_audit.json`, which is absent from the ZIP; the exact existing contexts above were separately reviewed. No missing canonical scene was invented.

## Held icons: source present, runtime absent

`icon-source-audit.json` registers all eight ZIP members, hashes, 17 source IDs and exact JSON pointers. All 17 IDs/texts/requires/block conditions match `docs/story-v111/source/다람탐정_82씬_실행매핑_V1.1.1.json`; IDs also exist in the older production source. This is **unimplemented later-day content**, not an ID rename. Native runtime contains D01–D03 (`dev/build_v111_labels.py:124` deliberately ends at day4); older `game/ms14/route.json` contains only D01–D05 (`dev/import_ms14.py:315,342`). D06/D11/D12 assets have no active equivalent. The eight originals are byte-verified in the source ZIP and registered in the held inventory, not in a runtime icon slot. Implementing those story days is outside this art-linking task.

## Reproduction

```sh
python3 dev/import_resource_intake21.py /path/to/extracted-intake
python3 dev/audit_intake21_icons.py
python3 -m unittest discover -s dev -p "test_*.py"
ROOM13_URL=http://127.0.0.1:8765/preview/room13-dev/ python3 dev/qa_resource_intake21.py
```

The importer expects the three verified ZIPs beside their extracted directories. Reconstruct Daram part01+part02 per the intake README. Source originals are not altered; prepared output and source SHA256 values are recorded in `receipt.json`.

## Validation and release boundary

- Unit/regression suite: 782 tests passed; baseline warnings from existing tests were nonfatal.
- All 48 profiles: rendered in Chromium with the actual Ren’Py renderer using a disposable source/data overlay on the existing 0.19.84 build. Desktop and mobile viewport captures were generated; fixture `room13` state remained identical.
- The first save harness call used `renpy.save` instead of the existing engine/UI entry point; it failed before a save. A later natural-route harness tapped the bottom-right carriage skip control, which correctly skipped the target line; corrected to tap the dialogue center (810,400). Neither is a game implementation failure.
- Natural opening-to-letter dialogue: passed. New bravado pose appears on its exact authored line. Save slot 6 → advance → load slot 6 restores the exact packet, settled pose and entire room state with motion disabled (reduced motion enabled), using the existing save/load UI. See `validation.json` and `screens/natural-bravado.png`, `screens/after-load.png`.
- **No fresh SDK lint or build**: Ren’Py SDK absent; prior official download returned CONNECT tunnel 403. No bypass or repeated download attempt.
- **No CI dispatch/main merge/deployment**: account billing usage was denied (403 integration permission); remaining $1 combined allowance cannot be verified. Branch push does not trigger this repository’s main-only workflow; no PR was created.
- This is source integration, not a newly deployed version. Published URL remains https://kkhkkh20-bit.github.io/daaegame/preview/room13-dev/ . No new published hash is claimed.
- Full campaign playthrough, browser restart using a user-supplied old save, new-build browser test, and all-map background production remain incomplete.

Screens are QA artifacts from an existing-build overlay, not newly built production screenshots.
