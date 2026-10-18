# Local candidate only: 14 originals / 18 exact bindings
Base: main 24ce3b6037093a562f0bd9b1c35c64a9b690a13d, version .66.
No remote writes or SDK execution performed. All map comparisons are static.

## Final explicit overlay step
Copy candidate art/, game/assets/investigation-canonical-20261018/, and dev/ files to the disposable integration tree. Preserve the existing full registries until final overlay application.
After ALL historical importers, registry ordering, and the existing 36 native_detail fixes finish, run:

    python dev/investigation_canonical_overlay.py --apply
    python dev/investigation_canonical_overlay.py
    python -m unittest discover -s dev -p 'test_*.py'

Do not hook this into the middle of import_action27_p0.py or import_action27_remaining.py. Exact .66 source inspection proves P0 prepends its eight rows; remaining removes/appends its rows. Intermediate row order is not the final registry. The overlay fails closed if an expected identity/index/spec differs. Neither historical importer generates the eight VA job sources nor the acting family. A final project generator was not identified in this source scope.

New exporter reads only packaged PNG originals and receipt, checks pinned source/stored-export SHA and exact RGBA equality; independently regenerates lossless WebP in memory and checks only decoded pixels, not encoder-specific bytes, checks the 18 exact preconditions, then changes only those specs. Existing source/crop validations are not globally weakened. test_native_detail_scope first verifies/reverses the exact overlay, then runs its existing 36 flags and unchanged baseline digest assertions. New tests additionally pin the unchanged .66 registry semantics after reversal.

## Alias label blocker
Exact .66 game/room13_acting.rpy Git blob 995e510803eb2867a3aea337e68950b388cd5c49 line 512:

    activity=r13_calendar_activity(person) if person in R13_CALENDAR else spec.get("activity_label",spec.get("action_ko",spec.get("action",r13_activity_text(person))))

Thus spec.action_ko does NOT override a scheduled character's calendar activity. The two temporary aliases have truthful proposed labels but these will be ignored on that branch:
- resident_musoe/living_foldmap -> canonical neutral, “지도를 들고 주변을 살핀다.”
- resident_lamplighter/living_inspectlamp -> canonical neutral, “등불을 들고 주변을 살핀다.”

Do not silently release these two aliases under incompatible folding/inspection labels. Integration choice: explicitly prioritize action_ko only for source_kind=temporary_canonical_neutral_fallback_no_old_art, then test scheduled states; or defer the two aliases until matching job poses are bound. No global calendar rewrite is proposed. Corrected seated Musoe is NOT a substitute for all scenes. Keeping the aliases staged is not a claim this blocker has been resolved.

## Placement and QA
All dates, periods, row order, heights, coordinates, occlusion, and world layout are unchanged by this source bundle. Separate post-furniture candidate must not be folded in without native same-scene QA. Crop/sole checks pass for all14, but conservative head boxes and collision/hit region behavior remain reviewed:false. Native runtime capture, selected pose/row logging, foot/furniture contact and crowded scene click tests are required before release. Kwaeksun RI-1 is outside this new source scope.

Local encoder: Pillow 12.3.0 / libwebp 1.6.0. CI Pillow 11.3 was reported by writer; its libwebp version is not verified here. Stored approved output SHA is never relaxed or replaced with local re-encoding. --apply checks the full pinned baseline after reversing only the18 allowed specs before writing.
