# Release 0.19.65: dialogue, investigation and interface clarity

## Changes
- Compact two-line paged ordinary dialogue, with positive-speed typing and an animated reading-options preview; retain meeting-specific dialogue geometry.
- Simplify records/relations and align footers; place topic Return on the right; improve discovered-map outlines and its raised centered footer.
- Make existing available field objects/people directly actionable without a nearby-look toggle; normalize older same-location scene-mode saves while preserving gates.
- Match displayed sound percentages to the existing perceptual slider, and raise only typing-sound samples by 6.02 dB without clipping.
- Ground the narrow Nabi/Tosil question paths in established knowledge; refresh source-bound metadata. Enable exactly 36 reviewed investigation native-detail flags without changing source pixels.
- Preserve the 0.19.64 admin Replay optional-key guards and save-state isolation. No new character artwork or broad voice rewrite in this release.

## Verification status at preparation
51 focused local checks and generated metadata provenance/pending checks passed in preparation. Full repository suite, official Ren'Py lint, existing C2/admin native tests, additional UI native screenshots and web build are pending actual CI execution. Local/browser rendering was not claimed. Public Pages and binary hashes require separate post-deployment verification.

## Packaging
Generate only through dev/build_web.py, preserving prior .rpyc seeds and 8 MiB transport parts; never manually edit packaged data.
