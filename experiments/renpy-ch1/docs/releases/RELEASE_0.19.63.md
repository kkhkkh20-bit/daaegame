# Release 0.19.63: dialogue state guards and evidence-grounded C2 pressure

## Changes
- Refine dialogue/topic availability and recording guards so the relevant story state and interaction context control what can be discussed and retained.
- Align testimony and question discovery with the actual progression conditions.
- Correct the related dialogue/rules call sites and refresh the override map after integration.
- Revise C2 pressure to distinguish evidence-grounded challenges from pressure unsupported by available evidence.
- Preserve the approved 0.19.62 dialogue UI, fonts, and existing save directory.

## Verification status at preparation
Source changes and static review prepared; official SDK execution is pending. The dedicated CI workflow will run dev/check.sh and dev/build_web.py using verified Ren'Py 8.5.3 and retain a bounded one-day changed-file artifact. A successful build is not deployment. Full UI/browser coverage and public hash verification must be reported separately after they actually run.

## Packaging
Generate preview/room13-dev only with dev/build_web.py, preserving its previous .rpyc seeding and the existing 8 MiB transport parts. Do not manually edit or merge packaged game data.
