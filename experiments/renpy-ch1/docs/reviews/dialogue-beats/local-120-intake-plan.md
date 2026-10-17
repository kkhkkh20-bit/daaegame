# Latest scope: approved 20-person / 120-source dialogue package, local only

The parent has conveyed approval for local use of the NEW front-facing, non-pixel
20-person / 120-cut package. Its upload commit has not yet been delivered. This
approval does not cover the earlier six-person intermediate package. No commit,
push, merge or public deployment is requested.

Pending exact input: upload commit and source-only package manifest. Do not guess
which files belong to the new delivery or use previous intermediates to fill slots.
The current new-art registry stays empty until this specific package is received.

Prepared intake:

1. Pin the delivered commit and record archive/source hashes. Resolve actual runtime
   person IDs using the package manifest and existing canonical identity registry.
   Require the expected 20 people and six slots each; list missing/repeated slots.
2. Read original sizes and transparency before choosing sizes. Keep common camera
   scale, canvas and ground anchor per person. Do not resize every expression to its
   own bounding-box height: raised hands and bent knees should not resize the body.
3. Use `audit_dialogue_profile_layout.py` to report upscaling, out-of-canvas bounds,
   neutral-relative foot baseline and visible-height changes. These are measurements;
   pose changes must be visually interpreted before correction. Upscaling is a risk
   flag, not proof that an image is blurry.
4. Build only smooth source-master dialogue profiles under the dedicated directory.
   Preserve map investigation pixel paths and the same face/outfit/species/colors.
   The staging builder always writes HOLD; promote only the exact newly approved
   package entries into the local registry after receipt and identity checks.
5. In the actual Ren'Py dialogue renderer, inspect each person's six slots at the
   used portrait heights, plus surprise_react -> surprise_talk at 0.35 seconds.
   Capture before/after frames and compare body scale, foot position and sharpness.
   Verify same-line click/AUTO/skip and restored load/rollback do not replay flinches.
6. Use actual cue-linked dialogue for available people, including teacher's composed
   reassurance where included. Keep unresolved injury/lying/grief production requests
   explicit; the standing package is not automatic approval of those event poses.
7. Record per-character/slot defects and replacement requirements with screenshots.
   Report locally connected versus missing/replacement-needed separately.

Actual-screen evidence is not available yet: no new source package is present.
No visual pass, sharpness pass or 120-cut connection is claimed at preparation stage.

## Authorization update after initial preparation

The parent subsequently conveyed explicit authorization for publishing the NEW
source package, merging validated code into main, and deploying the existing public
game. The earlier local-only/no-commit restriction above is superseded by this
update. Receipt of the exact upload commit is still pending; old six-person assets
remain prohibited.

Fetched main: `30d7327` (0.19.16). The working branch remains based on `a60d263`;
main is NOT yet integrated. `latest-main-drift.json` lists overlapping edits and
review text references absent from changed main files. Earlier test counts describe
the old working baseline and must be revalidated after integrating main. Preserve
new dialogue/evidence/skip fixes, reconcile exact scene cues, rebuild the generated
public preview via `dev/build_web.py`, and verify the published archive hash against
the resulting build report. Do not hand-merge public build artifacts.
