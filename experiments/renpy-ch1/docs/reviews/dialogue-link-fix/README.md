# Dialogue actor expression fixes

Base: `6700c5ed957b08c3960b967c3f68d95daf981aff` (0.19.34).
No release/version bump, main merge, deployment, artwork, map placement or name UI changes.

## Changes

- Resolve the line's beat before rendering a narration `show` actor. Explicit authored `show` + `expression` metadata now uses the same approved source-master resource gates as spoken beats. This fixes `kid_siluk2` joy in `ep1:siluk` and supports the authored anxious branch. No keyword inference; special poses retain their own art. Narrated surprise uses the front-facing talk slot without a flinch.
- Rebuild approved plain portraits on an NPC's unbound line even if the logical pose did not change. This removes the previous reviewed emotion. Same-pose refresh does not replay entrance/body reactions. POV replies and narration continue to retain the partner; unchanged special poses are not refreshed.
- Add seven regression tests; extend the existing POV harness for the new source-profile dependency. Update override-map locations. Existing dialogue provenance line numbers remain stable.

## Validation

- `python3 -m unittest discover -s dev -p 'test_*.py'`: **354 passed**.
- Dialogue-focused discovery: **38 passed**, including the seven new regressions.
- `git diff --check`: passed.
- Local Chromium/Ren'Py web engine: patched Python functions and the actual modified `r13_lines` label were parsed/compiled into the running 0.19.32 engine using its own `load_string` / `py_compile`. This is an instrumented runtime fixture, **not a newly built 0.19.34 web release**. Dialogue source/assets used here are unchanged between the audit base and branch base.
- Authored `r13_ep1_siluk` scene: narration now renders `kid_siluk2/840/joy.webp` with a visible smile (before: neutral).
- Controlled unreviewed-line fixture: Daram joy -> approved neutral with unchanged logical neutral pose. The fixture intentionally does not change production dialogue; its background caption is not semantic dialogue evidence.
- Buri: day2 afternoon workshop fixture -> actual map click -> carriage repair topic; neutral -> angry -> neutral retained.
- Siluk: native UI slot4 save/load restores joy; PageUp moves from the second displayed page back to the first and retains joy; skip removes the visitor. The captured page index and visible text demonstrate intra-packet rollback, not previous-scene traversal.
- Kkomi: actual hideout label fixture; reaction -> settled front-facing talk retained. Native UI slot3 save/load restores the same settled talk after resetting the instrumentation baseline. Initial hot-injection attempt failed because old function objects remained in rollback history; this is recorded separately from the successful clean-fixture run.

## Before / after evidence

- Authored Siluk narration: [before: neutral](siluk-before.png) → [after: joy](siluk-after.png).
- Controlled fallback fixture: [prior joy](fallback-prior-joy.png) → [unreviewed line: neutral](fallback-neutral.png). These two images show the renderer transition in the patched runtime, not a natural conversation; the unchanged background caption belongs to the prior scene. The original defect retained joy after that transition.

Only game screenshots are included; state dumps and environment details are omitted.

## Remaining verification / integration

`dev/setup_sdk.sh` could not download the 8.5.3 SDK: `curl: (56) CONNECT tunnel failed, response 403`. No network workaround was attempted. SDK lint, clean SDK compilation, formal web build and clean-release cross-version save compatibility remain unverified. The full Python test suite above passed independently; do not describe this as `dev/check.sh` passing.

Rollback is verified only across the two displayed pages of the Siluk narration in the instrumented session. Earlier Kkomi PageUp did not change the packet; cross-packet/scene traversal and older saves remain unverified. Rerun these on a clean build before release.

Kkomi `door_peek` is intentionally unchanged. The scene says a child's voice comes through the hidden clubhouse door, so the special introductory pose has narrative meaning. Proposed follow-up: retain a short doorway introduction, then explicitly switch to existing approved front-facing talk art for continued speech. Do not globally replace special poses or invent new art.
