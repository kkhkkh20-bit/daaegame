# 다람탐정 리소스 도감

Character cards and a place-grouped overview show Korean names and actions; stable character IDs, pose IDs and code evidence remain available in collapsed details. Read-only HTML index at `preview/resource-dashboard/`. This is **not** the Sites design/selection board. No Site registration, selection writes, game art, dialogue, placement or audio replacement is performed.

## Build and preview

From repository root (Python 3.12 + Pillow; browser QA also needs Playwright and Chromium):

```sh
python3 tools/resource-dashboard/build.py
python3 -m unittest discover -s tools/resource-dashboard -p 'test_*.py' -v
node --check tools/resource-dashboard/web/app.js
python3 -m http.server 8765 --bind 127.0.0.1
# separate terminal
python3 tools/resource-dashboard/qa_browser.py
```

Open `http://127.0.0.1:8765/preview/resource-dashboard/`. `file://` is unsupported because details are lazy-loaded JSON. The page uses relative links to existing `experiments/renpy-ch1/game/assets/` and `reports/` files; keep repository-root layout when publishing. No API or token is required. Asset originals are not duplicated; 240px thumbnails are derived for inspection only. Thumbnail resizing does not change game art.

Generator outputs index/version/errors JSON, per-character detail JSON, deduplicated thumbnails and buildless HTML/CSS/JS. It reads `.rpy` init Python literal tables via AST, live asset JSON, runtime selectors, and explicit machine-recorded screenshots. It does **not execute** game code. `SOURCE_DATE_EPOCH` fixes generation time for reproducibility. Source/asset hashes and a data version expose changes. “새 버전 확인” reloads changed deployed data; this does not watch local edits or apply design-board selections.

## Evidence and limits

- Current smooth dialogue frames are separate from legacy six-expression fallback art, authored dialogue poses, map-dot actions and profile icons. Current smooth slots are neutral/joy/angry/anxious/surprise_talk/surprise_react, as in the saved manifest, not invented six emotions.
- Generated = file exists; registered = manifest entry; conditional active-call evidence = runtime selector/cue connection. These are **not** observed runtime execution. Missing files are separate.
- Dialogue frames without reviewed cues stay registered. Special poses without resolved character+pose source references stay registered. Reference snippets alone do not establish branch reachability.
- All schedule function layers are linked. Resident weekly schedules are base candidates for days 1–14; not final presence. Event/offer/pose guards stay in raw JSON and code. No arbitrary `eval` of conditions. Unknown means unknown.
- Map27 and map9 are automatically read, including future added rows. This version indexes 35 map27-family rows (including four newly added Nabi kitchen poses) plus 9 map9 rows. Conditional placement still requires an upstream resident. Coordinates, anchor targets, masks and associated world maps are exposed as source data, not simulated screenshots.
- Audio place rules are **mood** slots calm/search/night, not automatically morning/afternoon/evening. Scene overrides and actual sound choice code are shown. Unknown loop/channel settings are not guessed. The audio control uses its own review volume and intentionally does not loop indefinitely.
- Unresolved game/assets files are listed; these are **not proven unused**. Original production art outside game/assets is not exhaustively classified. Full dynamic path resolution and whole-game reachability are outside this static index.
- Existing report screenshots require explicit person/speaker/actor fields. Newly captured examples are real Ren'Py web rendering under explicit day/location/flag fixtures, not a natural campaign playthrough. Their archive hash and runtime actor coordinates are recorded. Web archive → source commit is unknown unless independently verified. All other combinations show “실제 캡처 없음”.

## Regeneration and integration owner

The new `resource-dashboard.yml` workflow runs extraction/tests on relevant main/PR changes and uploads the generated directory. It has read-only repository permissions and **does not deploy or write main**. Its artifact references the repository's existing assets; it is not a standalone bundle of original media.

Only the single integration owner should merge/publish:

1. Merge this independent branch together with the final map-action integration on top of current main. Changes are confined to `.github/workflows/resource-dashboard.yml`, `tools/resource-dashboard/`, `preview/resource-dashboard/`, and `reports/resource-dashboard-20261017/`.
2. Run `python3 tools/resource-dashboard/build.py` **after** combining game source changes; do not resolve generated JSON conflicts by hand. Run the extractor tests/browser QA. Re-run game lint with an available SDK.
3. If Pages is branch-based (current repo has no tracked deploy workflow), commit the regenerated `preview/resource-dashboard/` alongside the final release. If switching to artifact deployment, add this generator immediately before packaging the existing Pages root. Do not deploy the dashboard artifact over the game root.
4. Publish through the existing single release process. Intended URL: `https://kkhkkh20-bit.github.io/daaegame/preview/resource-dashboard/`. This task did **not** publish that URL.
5. Validate `version.json` source commit/data version and existing relative media paths. Future integration builds must invoke the same generator; CI's build artifact alone does not update branch-based Pages.

The main game builder `dev/build_web.py`, game source, existing preview/room13-dev and root index/service worker are untouched. This avoids conflict with concurrent map integration and the Sites selection board.

## Validation captured here

- Extractor unit/contract tests; JavaScript syntax check.
- Chromium desktop + 390px mobile: search/place/day/period filters; repeated modal open/Back/Escape/focus restore; real WAV and MP3 click playback; exclusive playback, pause/stop/volume; missing/invalid audio and missing image handling; version check.
- Existing game suite: 352 tests passed (35.009 seconds) on latest main 57472ad4fe4e3b83fae41a936a3b2eb9b073dc35, no game modifications.
- Actual field captures: `reports/resource-dashboard-20261017/game/` (Eunho day2 morning market, Sling day2 evening post, Seori day2 morning clinic).
- Ren'Py lint **blocked**: `RENPY_SDK_HOME=/tmp/daram-renpy-sdk bash dev/setup_sdk.sh` attempted SDK URL `https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.tar.bz2`; proxy returned `curl (56) CONNECT tunnel failed, response 403`. SDK was not installed; no access-limit workaround was attempted. Integration owner must run lint where SDK is available.
- No `.agents/skills`, AGENTS.md or engineering skill was present in this checkout/environment. Repository CLAUDE.md and ROOM13_GUIDE.md were read. Sites skill was read; its local-only workflow applies, with explicit user instruction taking precedence over default publishing.

Actual game capture rerun (existing built web game, changes fixture state only in a fresh browser):

```sh
cd experiments/renpy-ch1
python3 ../../tools/resource-dashboard/qa_game_captures.py
cd ../..
python3 tools/resource-dashboard/build.py
```

## UI follow-up (2026-10-18)

See [UI review and integration notes](../../reports/resource-ui-polish-20261018/README.md) for current desktop/mobile evidence, shared original-ratio image viewer, audio credits, and the progressive enhancement of the existing place gallery. The generator also installs gallery UI assets without changing original figure evidence. Current browser QA saves captures in that report directory. Earlier game-suite and SDK results above are historical, not rerun claims for this UI-only change.
