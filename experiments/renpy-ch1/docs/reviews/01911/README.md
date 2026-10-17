# 0.19.11 — first ten characters, cumulative

0.19.10 delivered Kkwak's five expressions. This release adds nine people: guard (돌목), teacher (사자 선생님), Neoul, Nubi, Bori, Chorong, Madam, Guseul and Doto. This is **ten characters cumulatively, not ten newly completed characters in this commit**, and does not mean every requested channel is finished.

## Connected

- 39 distinct dialogue expressions: guard/Neoul/Nubi/Bori five each; teacher four; Chorong three (two already existed); Madam/Guseul/Doto four each.
- Teacher's writing-attendance and collapsed-attendance dialogue poses: native original canvas mapped into the existing character reference frame, without stretching seated art to standing height.
- Doto's ledger-writing and seated-reading investigation actions; Guseul's stamp-cleaning action at the inn. Original action meanings come from `art/pixel-b/acting/main-acting-labels.json` and source props.
- Original PNG bytes are retained under `art/incoming/reviewed-batches-20261017`; runtime WebP decoding matches every source RGBA pixel. Native detail and one scale per character preserve source detail. Neutral/profile/meeting art is unchanged. Bori's taller standing variants align to the neutral head rather than stretching the crouched neutral body.

## Evidence and limits

`results.json` records 50 local Ren'Py web-render captures: nine unchanged neutral baselines, 39 new expressions and two dialogue poses, plus four field fixtures. `gallery-*.png` are browser contact sheets, cropped centrally for inspection; individual PNGs are full 1280×720 frames. These are **local engine renders**, not screenshots of the deployed website and not a full story playthrough. Dialogue fixtures use height 360 to show the complete source silhouette. Each character was visually compared for species, face, clothing and props. Unit tests verify all 44 source hashes, lossless pixels, alpha margins, distinct expression connections and mapped poses.

`world-hall-0.png` and `world-hall-2.png` show Doto with correct standing/floor contact. `world-inn-2.png` shows Guseul holding the stamp and cloth. `world-post-1.png` records a **failed candidate location**: the old crowded post staging hides Guseul behind another visitor. That location mapping was therefore removed before release and is explicitly pending in the canonical report; the source and inn action remain available. No crowd placement engine changes are included.

## Still pending

- Teacher joy: right-hand silhouette meets the original right canvas edge (19 connected alpha>32 pixels); source held, neutral fallback retained. A new complete-hand source is required; no silent crop or generated repair.
- Guseul stamp action in the old post layout: fix crowd staging, then review again.
- Madam `living_inspect`: no confirmed source/contact anchor; remains pending.
- Guard's nine old investigation poses still need the approved mouth correction. These existing actions were not flattened to neutral.
- Unprovided expressions, including Madam/Guseul/Doto flustered, retain canonical neutral fallbacks and are not counted as completed expressions.
- Tosil's approved winter action and all UI proposals remain untouched.

Validation: 239 unit tests passed; source/path and JSON checks included. Ren'Py lint and release build are recorded in the release workflow. The art-coverage generator still labels new art `available_unreviewed` until its separate hash-bound coverage evidence registry is updated; this document provides the narrower render evidence, not blanket approval of every channel.
