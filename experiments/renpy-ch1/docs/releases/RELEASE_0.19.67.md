# 0.19.67 — Investigation character detail and placement repair

## Changes
- Preserve approved source art and restore detail for 47 explicitly reviewed registry bindings (45 selected poses). Remove only their destructive extra half-target scaling; exact source/export/crop checks remain enforced.
- Update 14 canonical investigation assets and 18 exact bindings. Add the two separately reviewed workshop job poses: Chorong holds a brought-in light while changing its stone; Musoe inspects an old tool as a visitor, without creating an employment schedule.
- Replace Ttadak's door-area pose and Tosil's thermos pose with approved source images. Preserve their selection keys, schedules, world feet and stature. Ttadak's image shows held tools; direct hand-to-doorframe contact is not certified.
- Place Granny behind the real inn counter front, separate Ubak from the lower-right controls, and move Musoe's workshop visitor position onto visible floor without clipping his body/tool.
- Unify duplicate investigation hints. Keep conversation readiness and story gates unchanged.

## Verification and limitations
- The preceding exact-source diagnostics passed the complete source suite and official Ren'Py 8.5.3 lint. Controlled engine cases verified Granny's body/topic/register/return flow, Musoe's actual no-content interaction plus wood inspection/return, and Tosil's body/topic/return flow.
- The 21-map × 14-day × 3-period selector audit covered 882 controlled states, 46 people and 98 distinct selected poses with no selector errors. This is not a complete natural-play campaign or visual approval of every map/pose.
- The last Ttadak diagnostic reached the real approach menu but its QA selector used an unabridged title instead of the production summary caption. This release candidate corrects only that physical-click selector; the final native run and web build are required before publication.
- Exact receipt validation and reverse-overlay checks preserve the original source/hash/crop contracts. Source-quality limits in other poses remain documented; no blanket native-detail toggle was applied.
- Diagnostic screenshots used the actual CI game window and are valid visual comparisons, not a claim of native 1280×720 one-to-one pixel-grid proof.
- The new whole-character 2×2 art direction is a separate, unfinished renderer/visual-validation effort. Experimental grid proof code is not included in this release. Recommended-story prototypes and B notebook UI are also excluded.

## Publication contract
Generate preview files only with dev/build_web.py using the existing compiled-script seed. Verify source commit/tree, artifact digest, transport parts and the deployed public manifest separately. A successful commit or build is not itself a completed deployment.
