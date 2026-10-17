# 27 map actions: preparation snapshot

This document describes preparatory commit fa1caeff. Runtime activation of the first eight actions is documented in ../../releases/RELEASE_01931.md; the zero-row statements below describe that earlier snapshot.

Base: main `334b8b52f5ac019a327a443bbae0db61f1c867f3` (0.19.30).
Branch: `prep/map-actions27-placement`. No new artwork, active image registration, main merge, web build or deployment.

## Ready code

`game/systems/room13_map_action27.rpy` runs at init178, after perspective126/map9 176/Solbang177. Its shipped registry has **zero rows** and returns existing actors unchanged. No character or schedule is created. Existing dead/detained/off-schedule filtering remains upstream. Pending offers are protected even in entry views. Each future row must explicitly list replaceable poses: no default replacement of map9, Solbang herbs, seats, or authored event poses.

Variants require both daylight and exact world width. Missing art or a missing period variant retains the existing pose; morning coordinates never fall back onto the afternoon scene. New poses must first be registered from approved assets separately; this preparation registers none.

The final transform uses one crop-relative anchor and one uniform scale. `render_height` is the reviewed final height, including perspective and seated/kneeling stature, not a second input to the old perspective wrapper. Optional secondary contacts must land within 6px. Every actor carries its own occlusion polygons and optional source-space hand/prop foreground polygons. The existing hit mask consumes the same visible-art function, including both furniture masks and foreground cutouts. There is no rectangle-only replacement picker. The new actor is constructed from a copy, preserving upstream caches.

## Background contact review

`contacts.json` and seven annotated PNGs record adopted background pixels, not screenshots of completed character placement. `background-provenance.json` records source hashes and crops. Render with `python dev/review_map27_contacts.py`. Final visible bounds, hand silhouettes, chair fit and clickability remain pending the original artwork.

| Action | Time / world size | Primary contact | Secondary / art requirements |
|---|---|---|---|
| Sling PO-1 (resident_sling) | Morning 2160×720 | parcel bottom centre (1450,548) | Hands + parcel foreground polygons; standing reference 190px |
| PO-1 | Afternoon 1280×720 | parcel bottom centre (700,550) | Independent atlas crop; standing reference 240px |
| PO-1 | Evening 1280×720 | parcel bottom centre (700,548) | Independent atlas crop; standing reference 240px |
| Tok DI-1a | Evening 2160×720 | seat (660,415) | Bowl bottom (720,365), faces right; standing reference156 × authored stature_ratio |
| Piko CL-1 | Each daylight 1920×720 | seat (1150,410) | Near mattress edge, legs in front of bedding; standing reference189 × authored stature_ratio |

The proposed Sling feet y499 do not provide counter occlusion, so feet must be derived from the approved parcel anchor. Parcel/hands need foreground silhouettes to remain on the tabletop while the torso behind them is masked. No background counter is drawn into the asset.

Tok's proposed x990 was beyond the left back table. The chosen seat is at the left end facing right, with a second target on the table surface. Source chair must occupy the existing painted chair footprint instead of adding a second visible chair. The seat-to-bowl vector in final world coordinates is (+60,-50); an original unable to match that vector at uniform scale must be adjusted before activation, never stretched. Existing chair alignment is still an art-fit acceptance test.

Piko sits at the near white/red mattress seam. No bed or chair is included in the source. Legs must appear in front of the hanging bedding, so the lying map9 blanket mask is deliberately not reused. The current alive lying pose stays active until this alternate is approved. Three daylight backgrounds were inspected; the mattress contact aligns at the same world position.

## Original artwork handoff

For every PNG supply: request ID, runtime character ID, approved design reference, SHA256, bytes, source dimensions, alpha bounds, head rectangle, foot/seat/hand/prop-bottom points in **full original coordinates**, stature_ratio and any hands/props that must appear in front of background furniture. Keep all full bodies and props within the alpha canvas. Explicitly distinguish source pixels, crop-relative export pixels, and world pixels; do not mix them.

1024×1536 originals remain byte-for-byte preserved in the eventual approved art directory with receipt/hash. `dev/map27_pixel_derivative.py` prepares the map-only 768-high RGBA derivative in memory using the existing approved Solbang map resize → nearest 2px grid path. It writes no files or registries. A 1024×1536 input becomes512×768; alpha transparency and exact 2×2 blocks are checked. Future import saves lossless WebP, reopens and validates it, remaps original anchors through the recorded source_to_export transform and crop, and keeps the existing runtime2px map renderer. Do not set native_detail to bypass the map renderer. Never feed dialogue/profile smooth art into this import or change those registries.

Before activation: verify original receipt; derive map-only resource; review alpha/face/props at actual size; populate approved pose spec; choose explicit replacement/time/width conditions; match primary+secondary contacts; validate furniture draw/hit-mask agreement in native WASM and save/load; then perform a separately authorized merge/deployment. No pending path belongs in CAST/R13_ACTING.

## Deferred / preserved

- GA-1/FA-1 Neoul: owner approved request/CAST_BIBLE executive coat on follow-up. Await two map-only source poses. No meeting-only costume condition found; do not change meeting art. This eight-image release contains no Neoul change.
- KI-1 Nabi: no kitchen schedule; no schedule added. Future asset only, unless a separately chosen existing event needs it.
- Keep map9 9 actions, Solbang herbs and all15 smooth dialogue cuts. Reuse/alternate decisions require explicit per-row replace_poses, not blanket neutralization.
- Original story/event/death/custody conditions remain unchanged. No new event text or action label has been attached to neutral art.

## Validation

Eight focused tests cover dormant behavior, missing assets, per-period width rejection, offer/prior map9/Solbang pose protection, removed residents staying absent, day/flag gates, uniform anchors and secondary mismatches, shared drawing/picking composition, original image immutability, alpha and 2px grid validation. Full `dev/check.sh` result is recorded in `validation.txt` after completion. No completed-art browser acceptance is claimed.
