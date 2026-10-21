# Room13 unused image audit (read-only)

Scope: every image (.webp/.png/.jpg/.svg) under `experiments/renpy-ch1/game/` (all 2532 live under `game/assets/`; `game/cache` and `game/saves` skipped). Date: 2026-10-21. Nothing in the repository was changed.

## Result

| class | files | size |
|---|---:|---:|
| Used by name (live .rpy or a JSON that a live .rpy loads) | 2119 | 363.55 MB |
| Used by a dynamic path pattern in live code | 46 | 3.56 MB |
| Matched only by a dev/build_web.py glob (counted USED per rule 2) | 83 | 35.08 MB |
| Dev/QA-only (named only in dev/*.py or game/qa_tests) | 8 | 0.75 MB |
| Kept for old saves (REDESIGN_BACKUPS) | 83 | 8.93 MB |
| Uncertain (not in unused.txt) | 182 | 14.03 MB |
| UNUSED (unused.txt) | 11 | 1.86 MB |
| **total** | 2532 | 427.75 MB |

## Method

1. Inventory: `find game -type f` for image extensions, minus `cache/` and `saves/`. No `game/images/` folder exists and `config.images_directory` is never set, so Ren'Py auto-naming defines nothing; all `image` statements / `renpy.image()` calls take file paths from literals or JSON `file` fields (options.rpy:127, systems/room13_new_cast.rpy, room13_map_action27.rpy, room13_life_groups.rpy, room13_map_work_nine.rpy, room13_seori_map_art.rpy, room13_profile_source_art.rpy), which the name scan covers.
2. Name scan (`scan.py`): tokenised every text file ([A-Za-z0-9_./-] runs) of game/**/*.{rpy,json,svg,txt,csv}, dev/*.{py,sh,txt,json} and art/**/*.json. A token matches an image if, after stripping an image extension and any leading directories, it equals the image's path without extension (with or without `assets/`), or - for files directly in assets/ - its bare stem. Matching is whole-token, so `room13-role-resident_kkwak` does not match `room13-role-resident_kkwak-refined-v1`. Extension-free matching also covers room13_webp_alias.rpy (old `room13-pixel-*.png` names resolve to the `.webp` twin).
3. Each mentioning file was classed: **live** = any game .rpy outside qa_tests, or a game JSON whose file name occurs in a live .rpy (plus `v111/newworld/dNN.json`, loaded by a computed path); **unloaded game data** = game/assets/provenance.json, resident-art.json, room13-avatars.json, room13-pixel-coverage.json, room13-pixel-acting-audit.json, legacy-resident-roster.json (no script loads them); **dev** = dev/*.py, game/qa_tests/** (excluded from the build); **art backup** = art/**/original-entries.json, original-layout.json, original-files/**, baseline/**, *-before*.json; **art manifest** = other art/**/*.json (receipts, sources, manifests).
4. Dynamic patterns (below) applied to everything not reached by a live name.
5. Classification order: live name > REDESIGN_BACKUPS > live pattern > build_web glob > dev/QA mention > art backup or unloaded game data (uncertain) > unused. Only files with no mention at all, or a mention solely in an art import manifest, are listed as unused. `docs/` and `reports/` were not counted as usage but were checked for the unused files (notes below).

## Dynamic patterns found and how they were bounded

| site | pattern | bound | effect |
|---|---|---|---|
| room13_worldmap_v5.rpy:16 | `assets/room13-map-%s-%s%s.webp` (region, art_key, "-outline") | Enumerated from room13-cartography.json regions/nodes (`art_key` or node key): exactly 30 files, none missing | 30 map plates USED (they have no literal mention) |
| systems/room13_ep_art.rpy:103, :112 (+ room13_v111_newworld_text.rpy:56 check) | `assets/room13-ep-%s.webp` from `{"book": X}` / `{"cut": X}` line options | X must be a literal in live code/data (e.g. "U02-opening" in systems/room13_ep2_kids.rpy:143); file used if its middle part is a live token | 16 room13-ep-U* picture-book/cut files USED |
| systems/room13_ep_art.rpy:111 | `assets/room13-v111-blanket-%s.webp` | state in {before, after} | (both also named literally) |
| room13_life.rpy:75 | `assets/room13-pixel-%s-%s.webp` (group, daylight) | daylight in morning/afternoon/evening (r13_daylight); group not bounded -> every `room13-pixel-*-{morning,afternoon,evening}.webp` counted USED | no extra files (all already named) |
| source.rpy:150 | `"assets/"+key+".png"` for keys starting `outdoor-` | all `assets/outdoor-*.png` USED | already named |
| source.rpy:100 / SOURCE_PATHS | legacy `art/ch1/...` paths mapped through assets/source-map.json (loaded) | name scan of source-map.json | covered |
| systems/room13_ep_art.rpy:35, :83, room13_v111_later_bindings.rpy:93 | `"assets/"+value` / `"assets/"+file` | values are complete file names in R13_EP_BACKGROUNDS / R13_EP_OVERLAYS literals | covered by name scan |
| room13_life.rpy:130 | `"assets/"+name` for R13_PIXEL_LAYOUTS keys | keys of assets/room13-pixel-layouts.json (loaded) | covered |
| systems/room13_dialogue_beats.rpy:53, systems/room13_dialogue_context_art.rpy:22 | `frame["file"]`, `entry["profiles"][560/760/840]` | full paths stored in room13-dialogue-talk-art.json / -context-art.json / -pose-source-art.json | covered (all dialogue-*-master folders resolve by full path) |
| systems/room13_dot_fx.rpy:240 (R13Blink) | `spec["half"]`, `spec["closed"]` | full paths in assets/room13-dot-fx.json; only mom angry/surprise remain | other blink pieces fall out (see uncertain) |
| room13_webp_alias.rpy:7 | `room13-pixel-*.png` -> `.webp` twin | handled by extension-free matching | covered |
| arrival.rpy:99, source.rpy:76, systems/room13_sound.rpy:154 | `cold-heart-N.wav`, `source-KEY.wav`, `NAME.wav` | audio only | n/a |
| dev/build_web.py:36-43 | REMOTE_MUSIC/IMAGE/CLOSEUP/LATER, EXCLUDE globs | not bounded; per instructions every match counted USED | 81 root `assets/*.png` + room13-pixel-cinematic-endB/key.webp counted USED-by-glob |
| dev/build_web.py:54, :108 | START_FILES, ICONS | literal names | sound-on.png / sound-off.png only here + provenance |
| options.rpy:73-79 | build.classify globs (painted-*.png, room13-hall.png, room13-passage.png) | no such images exist now | none |

Observations on dev/build_web.py (worth knowing before deleting):
- `superseded_art()` and `REDESIGN_BACKUPS` are defined but never called by `main()`; likewise REMOTE_MUSIC, REMOTE_IMAGE and REMOTE_CLOSEUP are never used, and REMOTE_LATER only feeds `prefetch_order()`, which nothing calls. The build ships every file in game/ (minus EXCLUDE), so "used-by-build-glob" files are not reached by any game code. They are held back only because the rules said to treat build globs as USED.
- The 81 root PNGs in that group are legacy chapter art (interview-*.png, resident_*-face/body.png, room13-mom-*.png, room13-gate.png ...). They are older, non-pixel painted art, and most are named only in the unloaded provenance.json / resident-art.json. If you drop the glob rule, they move to "uncertain - unloaded data only", and then to unused if those JSONs are treated as metadata. Please double-check legacy source.rpy chapters before deleting them.

## UNUSED (unused.txt) - 11 files, 1.86 MB

| file | bytes | evidence | style / note |
|---|---:|---|---|
| assets/dialogue-pose-source/seryeon-letter-bust.webp | 369040 | no mention anywhere | 660x820 painted dialogue bust (non-pixel, high colour). Seen in an old QA capture docs/reviews/meeting-source/runtime.json ("post_menu"); current pose data uses seryeon/chair_listen|chair_read/<h>.webp instead. |
| assets/room13-action-resident_nero-living_foldtag.webp | 92328 | no mention anywhere | 512x768 pixel-style action pose. dev/test_npc_redesign.py:120 asserts living_foldtag is NOT used (Nero redesign). |
| assets/room13-opening-coach-away.webp | 301042 | no mention anywhere | 1536x1024 opening cut. References removed in commit e9061ab3 (0.19.80, "Replace sliding coach with approved static winter landscape"). |
| assets/room13-opening-village-road.webp | 725532 | no mention anywhere | 1672x941 opening cut, painterly/high colour (not clean pixel grid). Removed in e9061ab3 (0.19.80). |
| assets/room13-pixel-meeting-altar056.webp | 371432 | only in art pipeline manifests: art/meeting-altar-20261016/source.json | 1672x941 meeting background, painterly. Only the reference input of art/meeting-altar-20261016/source.json; replaced by room13-pixel-meeting-altar-standing072.webp. |
| assets/room13-role-resident_kkwak.webp | 61900 | no mention anywhere | 503x762 pixel-style role sprite; superseded by room13-role-resident_kkwak-refined-v1.webp (+ -expression-*-v1). |
| assets/room13-role-resident_solbang-neutral.webp | 24954 | no mention anywhere | 288x420 clean 2x2-cell pixel art; only named in docs/art-coverage reports. |
| assets/room13-ui-frame-aged-paper.webp | 216 | no mention anywhere | 48x48 pixel 9-slice frame (0.18.24, docs/releases/RELEASE_01824.md); frames are now drawn in code (R13PaperFrame/R13InkPanel in systems/room13_typography_roles.rpy:54). |
| assets/room13-ui-frame-aged-window.webp | 218 | no mention anywhere | 48x48 pixel 9-slice frame, same history. |
| assets/room13-ui-frame-dialogue.webp | 218 | no mention anywhere | 48x48 pixel 9-slice frame, same history. |
| assets/room13-ui-frame-hud.webp | 220 | no mention anywhere | 48x48 pixel 9-slice frame, same history. |

Old-save risk for these is low: dialogue, opening and frame art is resolved from JSON or code on every display, not stored in save data. The ui-frame files are tiny (about 220 B each).

## Dev-only (USED, not in unused.txt)

- assets/map-action27/VA-10--doto.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/map-action27/VA-11--resident_jongjong.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/map-action27/VA-12--resident_jongjong.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/map-action27/VA-2--resident_piko.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/map-action27/VA-3--resident_piko.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/map-action27/VA-9--doto.webp - game/qa_tests/baseline-room13-map-action27.json
- assets/room13-action-resident_tosil-living_thermos.webp - game/qa_tests/baseline-room13-pixel-acting.json
- assets/room13-action-resident_ttadak-living_doorframe.webp - game/qa_tests/baseline-room13-pixel-acting.json
- also dev-mentioned but classed under build glob: sound-on.png, sound-off.png (dev/build_web.py ICONS), witnesses.png (dev/test_meeting_flow.py, game/qa_tests/tests.rpy)

## Kept for old saves (REDESIGN_BACKUPS) - 83 files, 8.93 MB

These are `file` values in art/npc-redesign-20261015/original-entries.json or art/ep-art-20261016/original-entries.json that no live data still names: old fullbody/pixel-acting/pixel-dialogue art for granny, neoul, bori, librarian, momo, nubi, owlgp, seol, siluk, teacher and yeoni, plus room13-pixel-dialogue-support-02/04/10 and room13-pixel-main-profile-granny. The full list is in classification.tsv.

## Uncertain (not in unused.txt) - 182 files, 14.03 MB

No live code or data reaches any of these. They are held back because a rollback or backup file still names them (`dev/apply_expression_acting.py --revert` restores art/expression-acting-20261016/original-files/*, and dev/test_expression_acting.py reads that backup), or because only unloaded game metadata names them. Unlike REDESIGN_BACKUPS, these backups are not wired into the build. If the owner gives up those rollbacks, the files are deletable.

### Only in rollback backups: art/expression-acting-20261016 - 81 files, 3.53 MB
`room13-fullbody-bami-angry.webp`, `room13-fullbody-bami-anxious.webp`, `room13-fullbody-bami-flustered.webp`, `room13-fullbody-bami-joy.webp`, `room13-fullbody-bami-neutral.webp`, `room13-fullbody-bami-surprise.webp`, `room13-fullbody-dad-angry.webp`, `room13-fullbody-dad-anxious.webp`, `room13-fullbody-dad-flustered.webp`, `room13-fullbody-dad-joy.webp`, `room13-fullbody-dad-neutral.webp`, `room13-fullbody-dad-surprise.webp`, `room13-fullbody-daram-angry.webp`, `room13-fullbody-daram-anxious.webp`, `room13-fullbody-daram-flustered.webp`, `room13-fullbody-daram-joy.webp`, `room13-fullbody-daram-neutral.webp`, `room13-fullbody-daram-surprise.webp`, `room13-fullbody-karo-anxious.webp`, `room13-fullbody-karo-neutral.webp`, `room13-fullbody-mom-anxious.webp`, `room13-fullbody-mom-neutral.webp`, `room13-fullbody-nabi-angry.webp`, `room13-fullbody-nabi-anxious.webp`, `room13-fullbody-nabi-flustered.webp`, `room13-fullbody-nabi-joy.webp`, `room13-fullbody-nabi-neutral.webp`, `room13-fullbody-nabi-surprise.webp`, `room13-fullbody-resident_lamplighter-angry.webp`, `room13-fullbody-resident_lamplighter-anxious.webp`, `room13-fullbody-resident_lamplighter-flustered.webp`, `room13-fullbody-resident_lamplighter-joy.webp`, `room13-fullbody-resident_lamplighter-neutral.webp`, `room13-fullbody-resident_lamplighter-surprise.webp`, `room13-fullbody-resident_ppul-angry.webp`, `room13-fullbody-resident_ppul-anxious.webp`, `room13-fullbody-resident_ppul-flustered.webp`, `room13-fullbody-resident_ppul-neutral.webp`, `room13-fullbody-resident_ppul-surprise.webp`, `room13-fullbody-resident_seori-angry.webp`, `room13-fullbody-resident_seori-anxious.webp`, `room13-fullbody-resident_seori-neutral.webp`, `room13-fullbody-resident_tok-flustered.webp`, `room13-fullbody-resident_tok-neutral.webp`, `room13-fullbody-seryeon-neutral.webp`, `room13-fullbody-seryeon-surprise.webp`, `room13-fx-blink-bami-angry-closed.webp`, `room13-fx-blink-bami-angry-half.webp`, `room13-fx-blink-bami-anxious-closed.webp`, `room13-fx-blink-bami-anxious-half.webp`, `room13-fx-blink-bami-flustered-closed.webp`, `room13-fx-blink-bami-flustered-half.webp`, `room13-fx-blink-bami-neutral-closed.webp`, `room13-fx-blink-bami-neutral-half.webp`, `room13-fx-blink-bami-surprise-closed.webp`, `room13-fx-blink-bami-surprise-half.webp`, `room13-fx-blink-daram-angry-closed.webp`, `room13-fx-blink-daram-angry-half.webp`, `room13-fx-blink-daram-anxious-closed.webp`, `room13-fx-blink-daram-anxious-half.webp`, `room13-fx-blink-daram-flustered-closed.webp`, `room13-fx-blink-daram-flustered-half.webp`, `room13-fx-blink-daram-neutral-closed.webp`, `room13-fx-blink-daram-neutral-half.webp`, `room13-fx-blink-daram-surprise-closed.webp`, `room13-fx-blink-daram-surprise-half.webp`, `room13-fx-blink-mom-anxious-closed.webp`, `room13-fx-blink-mom-anxious-half.webp`, `room13-fx-blink-mom-neutral-closed.webp`, `room13-fx-blink-mom-neutral-half.webp`, `room13-fx-blink-nabi-angry-closed.webp`, `room13-fx-blink-nabi-angry-half.webp`, `room13-fx-blink-nabi-anxious-closed.webp`, `room13-fx-blink-nabi-anxious-half.webp`, `room13-fx-blink-nabi-flustered-closed.webp`, `room13-fx-blink-nabi-flustered-half.webp`, `room13-fx-blink-nabi-neutral-closed.webp`, `room13-fx-blink-nabi-neutral-half.webp`, `room13-fx-blink-nabi-surprise-closed.webp`, `room13-fx-blink-nabi-surprise-half.webp`, `room13-redesign-resident_nero.webp`

### Only in rollback backups: art/expression-acting-20261016, art/role-connect-20261016 - 54 files, 2.81 MB
`room13-fullbody-buri-angry.webp`, `room13-fullbody-buri-anxious.webp`, `room13-fullbody-buri-flustered.webp`, `room13-fullbody-buri-joy.webp`, `room13-fullbody-buri-neutral.webp`, `room13-fullbody-buri-surprise.webp`, `room13-fullbody-doto-angry.webp`, `room13-fullbody-doto-anxious.webp`, `room13-fullbody-doto-flustered.webp`, `room13-fullbody-doto-joy.webp`, `room13-fullbody-doto-neutral.webp`, `room13-fullbody-doto-surprise.webp`, `room13-fullbody-guard-neutral.webp`, `room13-fullbody-resident_guseul-angry.webp`, `room13-fullbody-resident_guseul-anxious.webp`, `room13-fullbody-resident_guseul-flustered.webp`, `room13-fullbody-resident_guseul-joy.webp`, `room13-fullbody-resident_guseul-neutral.webp`, `room13-fullbody-resident_guseul-surprise.webp`, `room13-fullbody-resident_kkwak-angry.webp`, `room13-fullbody-resident_kkwak-anxious.webp`, `room13-fullbody-resident_kkwak-flustered.webp`, `room13-fullbody-resident_kkwak-joy.webp`, `room13-fullbody-resident_kkwak-neutral.webp`, `room13-fullbody-resident_kkwak-surprise.webp`, `room13-fullbody-resident_madam-angry.webp`, `room13-fullbody-resident_madam-anxious.webp`, `room13-fullbody-resident_madam-flustered.webp`, `room13-fullbody-resident_madam-joy.webp`, `room13-fullbody-resident_madam-neutral.webp`, `room13-fullbody-resident_madam-surprise.webp`, `room13-fullbody-resident_mungchi-angry.webp`, `room13-fullbody-resident_mungchi-anxious.webp`, `room13-fullbody-resident_mungchi-flustered.webp`, `room13-fullbody-resident_mungchi-joy.webp`, `room13-fullbody-resident_mungchi-neutral.webp`, `room13-fullbody-resident_mungchi-surprise.webp`, `room13-fullbody-resident_piko-angry.webp`, `room13-fullbody-resident_piko-anxious.webp`, `room13-fullbody-resident_piko-flustered.webp`, `room13-fullbody-resident_piko-joy.webp`, `room13-fullbody-resident_piko-neutral.webp`, `room13-fullbody-resident_piko-surprise.webp`, `room13-fx-blink-buri-angry-closed.webp`, `room13-fx-blink-buri-angry-half.webp`, `room13-fx-blink-buri-anxious-closed.webp`, `room13-fx-blink-buri-anxious-half.webp`, `room13-fx-blink-buri-flustered-closed.webp`, `room13-fx-blink-buri-flustered-half.webp`, `room13-fx-blink-buri-neutral-closed.webp`, `room13-fx-blink-buri-neutral-half.webp`, `room13-fx-blink-buri-surprise-closed.webp`, `room13-fx-blink-buri-surprise-half.webp`, `room13-redesign-resident_nubi.webp`

### Only in rollback backups: art/role-connect-20261016 - 14 files, 2.97 MB
`room13-action-resident_mungchi-event_handrub.webp`, `room13-action-resident_piko-event_paintwipe.webp`, `room13-meeting-seated-buri068.webp`, `room13-meeting-seated-doto068.webp`, `room13-pixel-acting-buri.webp`, `room13-pixel-acting-doto.webp`, `room13-pixel-acting-guseul.webp`, `room13-pixel-acting-madam.webp`, `room13-pixel-acting-mungchi.webp`, `room13-pixel-acting-piko.webp`, `room13-pixel-acting-resident_kkwak.webp`, `room13-pixel-dialogue-buri.webp`, `room13-pixel-dialogue-doto.webp`, `room13-pixel-dialogue-support-09.webp`

### Only in rollback backups: art/canonical-channel-alignment-20261017 - 11 files, 2.07 MB
`room13-fullbody-neoul-angry-acting.webp`, `room13-fullbody-neoul-anxious-acting.webp`, `room13-fullbody-neoul-flustered-acting.webp`, `room13-fullbody-neoul-joy-acting.webp`, `room13-fullbody-neoul-surprise-acting.webp`, `room13-fullbody-resident_teacher-angry-acting.webp`, `room13-fullbody-resident_teacher-anxious-acting.webp`, `room13-fullbody-resident_teacher-flustered-acting.webp`, `room13-fullbody-resident_teacher-joy-acting.webp`, `room13-fullbody-resident_teacher-surprise-acting.webp`, `room13-meeting-seated-resident_bori068.webp`

### Only in rollback backups: art/canonical-channel-alignment-20261017, art/expression-acting-20261016 - 9 files, 0.71 MB
`room13-epart-neoul-neutral.webp`, `room13-epart-resident_teacher-neutral.webp`, `room13-fullbody-resident_teacher-pose-collapse_attendance.webp`, `room13-fullbody-resident_teacher-pose-wipe_board.webp`, `room13-fullbody-resident_teacher-pose-write_attendance.webp`, `room13-fullbody-resident_tosil-neutral.webp`, `room13-redesign-resident_bori.webp`, `room13-redesign-resident_momo.webp`, `room13-redesign-resident_seol.webp`

### Named only in unloaded game data (provenance.json / room13-pixel-coverage.json) - 7 files, 1.38 MB
`room13-pixel-navigation-village.webp`, `room13-ui-inspect.svg`, `room13-ui-move.svg`, `room13-ui-present.svg`, `room13-ui-talk.svg`, `winter-gate.webp`, `winter-guard.webp`

### Only in rollback backups: art/canonical-channel-alignment-20261017, art/expression-acting-20261016, art/role-connect-20261016 - 5 files, 0.37 MB
`room13-fullbody-guard-angry.webp`, `room13-fullbody-guard-anxious.webp`, `room13-fullbody-guard-flustered.webp`, `room13-fullbody-guard-joy.webp`, `room13-fullbody-guard-surprise.webp`

### Only in rollback backups: art/canonical-channel-alignment-20261017, art/role-connect-20261016 - 1 files, 0.19 MB
`room13-pixel-dialogue-guard.webp`

Uncertain style notes: room13-fullbody-*-{emotion}.webp (non "-acting") are the pre-0.18.89/expression-acting dialogue full-bodies, pixel-style. room13-fx-blink-* are pixel eye-blink patches for faces that were replaced. They are useless with the new faces, since apply_expression_acting.py says "eye-blink pieces of replaced pictures are removed". winter-gate.webp and winter-guard.webp are older winter-campaign art. The room13-ui-*.svg icons are named only in provenance.json.

## Output files
- unused.txt - unused paths (relative to game/), with count and bytes
- classification.tsv - every one of the 2532 images: class, bytes, first evidence
- scan.py, stage2.py - reproducible scripts (read-only); stage1.json, stage2.json - intermediate data
