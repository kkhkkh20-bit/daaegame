# Scene geometry and examination-art review

Final source-art review: 2026-10-18 UTC. Reviewed actual files with image inspection and independent pixel checks. No originals altered; no GitHub writes. These are generated illustrations and code-native reconstructions, **not actual game screenshots**.

## Clear disposition

- **E3 day/night geometry-v3: SOURCE-ART PASS**, for the exact hashes below and the bounded observation contract. The earlier warehouse obstruction is genuinely corrected in v3.
- **Piko native-v4 reconstruction: SOURCE-ART PASS** (superseding v3 solely by restored floor17 marking), for ordinary handling, fixed inner fitting, support, and the complete decisive canonical torn/striped region. The plain folded center is illustrative, not falsely described as exact full-cloth UV identity.
- **Canonical container v2 64/240 icons: SOURCE-ART PASS.** Same vessel, exact canonical texture and parent RGBA mask, independently recreated byte-for-byte; old invented damage icon superseded.
- **Canonical cloth comparison: SOURCE/MASK PASS.** Independently recomposed actual exported parts; exact source reconstruction, complementary masks, and stripe continuation pass.
- **Ren'Py alpha-mask bug: FIXED AT SOURCE/ASSET LEVEL.** RGBA derivatives have alpha equal to canonical masks; installed files and helper paths were checked.
- **Native engine/render/hit/state testing: NOT RUN BY THIS REVIEWER.** Do not label any supplied proof image a native screenshot. Production art-verification gates should remain closed until the coordinator completes the remaining native checks. Source-art PASS is not an unqualified runtime PASS.

No further image generation is requested. The remaining work is integration and bounded runtime verification, not an unspecified permanent art blocker.

## Approved deliverables and exact input contracts

- `metadata/scene-geometry/e3_coordinate_interaction_contract.json`: current exact day/night hashes, actual source coordinates, crop/scale/pointer inverse, hotspots and witness limits. Revision `e3-v3-source-art-reviewed-native-pending`.
- `metadata/scene-geometry/e3_night_v3_reviewed_overlay.svg` and `.png`: annotations over the actual approved night source, not a game capture.
- `metadata/scene-geometry/piko_contact_interaction_contract.json`: approved panel hashes, fixed fitting and inspection region, sequence, identity/inference scope and remaining tests.
- `metadata/scene-geometry/cloth_mask_validation.json`: original independent canonical-source validation.
- `metadata/scene-geometry/latest_review_validation.json`: independent latest projected-part recomposition, screw contact alpha and source dimensions.
- `metadata/scene-geometry/e3_fixed_architecture_reference.png`, `.svg`, `.json`: a clean alternate construction reference with fixed footprints, facing directions, points and unobstructed courtyard. It was supplied to stop unconstrained regeneration loops. It is a fallback design reference, **not the approved v3 image geometry** and should not trigger another redraw.

## E3 actual-image findings

### Architecture and time states

Both approved v3 canvases are **1584x993**. The warehouse now stands sufficiently farther back/right: its approximate front base is `(1195,480)→(1380,550)`. School ground below the reviewed window is approximately `(875,387)`, about28px in front of that extended facade line. Thus the school-to-W ground trace stays on the exterior/front side rather than entering the warehouse footprint. This is a real change from rejected originals and v2, not a ray painted through a wall.

The night source shows an intact side wall and outside doorway ignition. The day source preserves the building, road, can and doorway positions, removes active outside flame, adds front scorching and the separate person-width torn side wall around `(1452,380,106,150)`. The side opening is not a preexisting access door. Bori arrives after ignition and makes that opening. The interior upright lamp can be inspected through the later hole, but neither its position nor soot alone proves ignition cause or intent.

### Logical positions and actual pixels

Keep L=(0,0), M=(5,0), W=(10,0), child=(0,1), teacher=(6,3); child observed0..6, teacher observed4..10, overlap4..6. Native geometry is perspective with a gently bending lane, so these logical route positions are not an assertion that image pixels are affine metres.

Actual native anchors:
- L doorstep/route=(245,430), child eye=(245,348).
- M=(850,560), **right of the tall wall pillar** ending nearx824.
- W threshold site=(1300,535), can=(1217,512), outside ignition=(1326,526). W is a small site containing these objects, not a single pixel under the can.
- Teacher eye=(875,246), the left pane of the large school window.
- Route4=(729,534), route6=(940,555).
- School forecourt junction=(925,503); right/Bori approach junction=(1430,610).

The wall can conceal lower legs or the can near the far-left edge4. Do not call it transparent. Teacher can track upper-body movement there; by M5 atx850 an ordinary carried can and hands clear the pillar. For an18px half-width adult silhouette, left edge≈832 is beyond the pillar. The child directly covers0..6. The decisive alleged handoff atM and5..6 is therefore in clear overlap, while continuity starts4. This preserves the stated teacher observation of can-carrying **M→W**, without pretending every body part is visible at every point4..10.

### Bounded witness claims

Child identifies mother's face at L on departure with the can and on empty-handed return, follows the stated L-side interval, and did not witness ignition. The open road does not establish that W is physically impossible to see; the corrected script uses an actual observation limit rather than “거기까지는 안 보여요.”

Teacher observes carrying/placing/outside ignition and the short empty return, but cannot confidently identify the person in the distant, oblique night view and return fire backlight. No hood, forced head-turn, or claim that face visibility is physically impossible at every instant is required. Do not add an unmistakable named-face closeup and then tell the player it is unidentifiable.

Teacher calls out immediately upon ignition while briefly tracking return, then goes to help. Bori's entire offscreen opposite route is not teacher eyewitness knowledge: teacher corroborates his first visible late arrival. The school forecourt and far-right approach remain real paths. Their junctions are visible in the relevant interval; no other crossing/handoff is the witnesses' observation, not a false architecture claim of zero branches. The code's former `branches=0` metadata was replaced with `unobserved_crossings_during_interval=0`.

### Rendering and interaction contract

Use source crop `(80,150,1500,650)` and screen display `(70,116,1140,494)` at1280x720, a single uniform scale0.76. Forward: `sx=70+(px-80)*.76`, `sy=116+(py-150)*.76`; inverse: `px=80+(sx-70)/.76`, `py=150+(sy-116)/.76`. Round final anchors to even screen pixels. Do not independently stretch the source, labels and hit regions.

Steps0–1 click actual L/M/W scene points: can endsW, person returnsL. Step2 displays child0..6 with semantic answerL-M. Step3 displays teacher4..10 with semantic answerM-W. Step4 clicks the actual shared band4..6 aroundM. The JSON records polygon and object regions. Use a transparent alpha focus mask for the overlap, not an invisible full-screen catch-all. Active point buttons need visible focus and at least44px screen hit size. Cancel must retain already acquired observations without advancing the map.

Static inspection of the latest implementation confirms the actual master crop, shared coordinate function,52px L/M/W buttons, source-position witness buttons, and overlap alpha focus region are now wired in `room13_recommended_ep23.rpy`. This is code inspection, not native execution. Native focus/click dispatch remains to test.

## Piko native-v3 actual-image findings

The existing square background's lantern is a small brass/gold four-sided glass lamp with a peaked removable cap and bottom finial. The approved new closeup preserves that silhouette family. It is a designed reconstruction, not a claim that a tiny old background already proved the new internal fastener.

The final scene supports the metal frame on two ordinary wooden blocks on the bench/pad, leaving a recess for the finial instead of balancing on its tip. The blocks are maintenance supports, not new evidence clues. The scene contains stone17 and no oil reservoir, wick or flame.

Before and during the lift, the fitting remains at logical `(220,74)`, display `(440,148)`. It is on the inner/top metal frame, not glass, and the closed-cap section shows that the cap covers it. The same new front crossbar and opaque frame/translucent glass occlusion are present in every state. This makes the glass/frame relationship intelligible rather than drawing hands passing through a solid panel.

The initial stone center aligns with the protected grip rather than jumping into a different place. Both hands visibly grasp through folded cloth; grip→contact rises10 logical pixels, contact→lift rises24 more. The free corner is not carrying the stone's weight. After contact, the fragment stays at the fitting while the parent cloth moves. At the unchanged fastener center, independent inspection finds fragment alpha253; the fixed screw head's sampled center pixels are identical across open/grip/contact/lifted.

### Exact source identity and approved scope

Canonical source SHA-256 remains `56c98afccf32affa08c688071177a9a80913f20084edd03f2cee2d1923c44a46`. The **entire decisive tear boundary plus both adjacent stripe continuations** use canonical UV region `[190,0,300,174]` and the same two affine triangles for texture and complementary masks. Contact projected quadrilateral is `(191,96),(207,51),(232,91),(205,116)`. Independent compositing of actual exported parent+fragment exactly reconstructs the canonical projected patch. No independently invented torn edge substitutes for it.

The central plain folded cloth is generated explanatory drawing. It contains no independent stripe or torn edge and is explicitly not claimed to be an exact full-cloth UV render. The later unfolded container lining is the canonical parent, with the same missing region. The larger flat comparison reconstructs the complete original cloth and both stripes exactly. This separation is honest: an ordinary handling illustration plus an exact decisive tear-match mechanic, not a false assertion that every fold is the same texture pixel.

The matching cloth establishes contact with a fitting hidden under the closed lid. Attribution and timing depend on the already-repaired story ownership/access and intact-before/torn-after observations, not shape alone. This review does not reopen solved chronology or invent an unseen actor/handoff.

### Canonical comparison runtime fix

Original L-mode masks were mathematically correct but incompatible with displayable `AlphaMask`, which uses mask alpha rather than luminance. The defect was reported and fixed: both installed `*_mask_rgba.png` files have alpha exactly equal to the respective canonical L mask, values0/255, exact complement; installed files match the validated derivatives byte-for-byte and the helper references the RGBA paths. Official API: https://www.renpy.org/doc/html/displayables.html#AlphaMask . A real engine render must still confirm separated and restored views are correct.

## Rejection history, resolved rather than ignored

Original E3 and first geometry-v2 placed the school behind the warehouse door plane. Artist received actual footprint overlays and a constrained architectural reference; approvedv3 physically moved the building to the front-visible side. Original generated Piko v2 had incompatible tear damage and a glass-side screw. Nativev1 fixed identity but showed cloth as a flat poster and finial-only support. Nativev2 fixed grip/support but had marginal screw contact and incomplete foreground occlusion. Approved nativev3 corrected those locally, without another full-scene redraw.

## Remaining native tests and stopping condition

1. Check installed approved-source hashes, same1584x993 day/night canvas, and exact single crop/scale for background and pointer coordinates.
2. At1280x720, click L/M/W, both witness choices, the overlap's interior and outside pixels; test keyboard focus, wrong answers and cancel. Confirm the alpha focus region does not intercept unrelated parts of the image.
3. Inspect actual night/day reconstruction, can and rescue-wall regions. Keep wall-state timing, Bori-after-ignition, immediate alarm and safe/loss outcomes intact. Do not draw a definitive face or an invented occlusion.
4. Exercise consent/no-consent, actual support before testimony, sightline-gap and other-crossing conditions. No blocked branch may bypass identity gating.
5. Play approved Piko panels in order, inspect the unchanged fitting, correct frame/glass occlusion, container parent cloth and exact comparison. Test matched/incorrect/cancel/revisit transitions without changing earned history.
6. Verify the one-final2x render contract once at actual engine size; no double pixelization of prequantized640x400 panels or second unrelated sampling pass.
7. Only after real execution/screenshots and input/state assertions pass should the coordinator enable production geometry/contact flags. Source-art approval is finished; native approval remains the precise open item.

## Approved hashes and reviewed implementation snapshot

- `/workspace/shared/recommended-story-icons/masters/fire_lmw_night_geometry_v3.png`
  SHA-256 `f1acb0401f7587b3386d88664ede106aa6eb1a5ce868cde2996871b459ef2ae3`
- `/workspace/shared/recommended-story-icons/masters/fire_lmw_day_geometry_v3.png`
  SHA-256 `5c748c1d5fa6a7436464762380e389e1caba6c94a140196ae37ed82586ace7ac`
- `/workspace/shared/recommended-story-icons/contact/piko_native_reconstruction_v3_ko.png`
  SHA-256 `012c00067f62bc6cd8e39d554e1271527f2664f6e9a655256e426637a7952abb`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/manifest.json`
  SHA-256 `9b2c7cfb0f6b7e09150985944c895dfeed53718f2f47045f742375801777fbc2`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/open__640x400.png`
  SHA-256 `dea5df39626bd7cdbed4d90aad89ddffed309717c5f57132e9afeae506e1f4e5`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/grip__640x400.png`
  SHA-256 `b09888c0614fad9c71d41b1f1988835899ac1cc95fdbaac7ec885da260f1220c`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/contact__640x400.png`
  SHA-256 `83bf6df4834978c5aa83a6e36f918d61c2e5eb3851c621c2154e3da974b69db7`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/lifted__640x400.png`
  SHA-256 `0a8d8bbdf1f1a1bdd0ef20d5e0e0ec3c76046009726eea98a15b90d657165674`
- `/workspace/shared/recommended-story-icons/examinations/piko-native-v3/container_unfolded__640x400.png`
  SHA-256 `791d9a9bc50381d88741c24caf6918221138325072d61fc6be876369499956d4`
- `/workspace/shared/recommended-story-icons/masters/cloth_texture.png`
  SHA-256 `56c98afccf32affa08c688071177a9a80913f20084edd03f2cee2d1923c44a46`
- `/workspace/shared/recommended-story-icons/examinations/cloth-mask-v1/parent_mask_rgba.png`
  SHA-256 `98cb5003cef65222ead2d57e3ca45b0a2b367ac8a3a4bb802dd9fd4e491e54d0`
- `/workspace/shared/recommended-story-icons/examinations/cloth-mask-v1/fragment_mask_rgba.png`
  SHA-256 `05a7eeb47a9654d8d8fab5029eb515eadb0c6bcb12232d10bf9fa04f74b57415`
- `/workspace/shared/action-request-20261017/backgrounds/square.webp`
  SHA-256 `212f0dd839b6f937619f4acaeda1094446b5a0d060cc1be14a692b2838a04f30`
- `/workspace/shared/recommended-story-implementation/dev/recommended_ep23_model.py`
  SHA-256 `e0bb03623a0412376c38e938248e6d8336cb9a17467689a5b11797f3843c09f4`
- `/workspace/shared/recommended-story-implementation/game/systems/room13_recommended_ep23.rpy`
  SHA-256 `edc5425a6f724a442feffed836882c4150a41a1ec36795ea0654944b60e9b922`
- `/workspace/shared/recommended-story-implementation/game/systems/room13_recommended_cloth_compare.rpy`
  SHA-256 `9c8c556850521cad9d5e0116222c6d839cd2eaa62a3d877b8acbc0def4f9c222`

## Final delta review: Piko v4 and canonical container v2

This addendum is the latest approved source revision. V3 remains the reviewed baseline, but current integration should use the v4 hashes below and the updated Piko contract. Native/runtime status is unchanged: unverified.

Directly inspected actual v4 open, grip, lifted and empty-after panels, the canonical container proof, both original/empty vessel masters, and the runtime lid section. The same oval teal two-handled lidded vessel is retained. The old arbitrary cloth tear is removed, not rationalized. The replacement is explicitly a comparison view with the same lining laid out, not a new object or new theft event.

Independent v3/v4 pixel differences occur only within display rectangle `(304,224)-(336,248)`, the restored floor17. The complete canonical projections are unchanged. The fitting, hands, ordinary cloth grip, support blocks, glass/frame occlusion and contact geometry are byte-identical outside that floor region. The seated stone partly obscures the marking rather than guaranteeing total invisibility; this bounded wording replaces the earlier overly broad “hidden” description. No art regeneration is needed.

The container64/240 exports were independently rebuilt directly from empty vessel + original texture crop + canonical parent alpha, then one nearest2x pass. Both match the delivered RGBA bytes exactly. All eight delta runtime Piko files and both container icons satisfy exact2x2 blocks. The earlier proof-section diagram is intentionally not the runtime file: use the newly inspected640x280 unlabelled closed/open section whose exact hash appears below. All native pointer/state/render tests listed above remain required.

Validation: `metadata/scene-geometry/final_delta_review_validation.json`. Reproducible check: `metadata/scene-geometry/review_final_delta.py`.

### Latest approved hashes

- `examinations/piko-native-v4/manifest.json`: `101b91b24c700082d09320ffaf2e14147577fe56a5c13250a611bd51d5d61443`
- `examinations/piko-native-v4/parent_projection__640x400.png`: `c7bdef044df90d08b362e9199bba238ea98b6727f811e14cd24da415dda3a891`
- `examinations/piko-native-v4/contact__640x400.png`: `884ec7326df6c640ebf6b6a972132dd7eb621c21a2cf882f22b35f20f99ed983`
- `examinations/piko-native-v4/container_unfolded__640x400.png`: `791d9a9bc50381d88741c24caf6918221138325072d61fc6be876369499956d4`
- `examinations/piko-native-v4/empty_before__640x400.png`: `cce2a67c45dc63465dd7c4f861ffd2c39bc653c63c828003696f3a16d4e0b946`
- `examinations/piko-native-v4/fragment_projection__640x400.png`: `7452c897bcaf3766af108074e339db25662679031b63479c3a23e20038cb4e8b`
- `examinations/piko-native-v4/open__640x400.png`: `d834a9237a9e46e2ec63e3174d98d57b3f880ae71ce7047b3228af4b8e429649`
- `examinations/piko-native-v4/inner_fitting_section.png`: `dbce3577f03ddca2e51ff9ca220649751ccecb4f9aac7fe68131c1c6a3ad7e11`
- `examinations/piko-native-v4/grip__640x400.png`: `5c886226d6bafada8473e857bc4233023a2e73ab1c1bdb3a1de388469398e336`
- `examinations/piko-native-v4/canonical_tail_projection__640x400.png`: `b9b2ba4930c48ae49226acca353c6b4dfbaa342be6e96e80c972fd9de03a95f7`
- `examinations/piko-native-v4/lifted__640x400.png`: `b790840bae0dab830c1062b2bb0aee0b1c059b2f17761170eef53df31c7086d8`
- `examinations/piko-native-v4/empty_after__640x400.png`: `7d967fb74f690ad48f735944f17e2274b30c2870ce91e56fbe49bcb12288b284`
- `transparent/container_canonical_v2__64.png`: `73c1f365058acd039524c4af9baf60a647fe5ab93077bf11bdd78c1b5319ed54`
- `transparent/container_canonical_v2__240.png`: `009f8aaeb4c3a232f45b6212cb088e29d27dfb4923d053d4041dfc1bac3ac319`
- `masters/container_empty.png`: `2cac2fe250a23e75c70fc3b29682b57f0669b3f1dc752ca96105c249d4e267da`
- `delta-v2/game/assets/recommended-story-icons/piko-native-v4/inner_fitting_section.png`: `63cfc8031705e9402a77691901ffd9cf17a435875abfe86e89620f5389239e94`
