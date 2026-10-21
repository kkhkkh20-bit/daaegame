# Approved resource intake — 2026-10-21

Resource transport only. No runtime files changed; no new generation.
Base: 31f838c71daa1109fd9f2039fae7fe215e4e2f4c

Packages:
- dialogue-icons-8.zip: 8 dialogue-grounded props, original masters and strict 2x2 candidates, scene/line mapping manifest.
- other-expressions-6.zip: 6 additional expressions for Kkomi, Dodam, Saemi and Ubak, references and manifest. Not a complete cast.
- daram-approved-10.zip.part01 + part02: exact binary split of approved Daram 10 poses ZIP. Concatenate in numeric order, then verify SHA256 below before extracting.

Reassemble:
cat daram-approved-10.zip.part01 daram-approved-10.zip.part02 > daram-approved-10.zip
sha256sum dialogue-icons-8.zip other-expressions-6.zip daram-approved-10.zip

Expected SHA256:
63a23ba25e3c75502c5804df763b2e7d78ae39eff7f856c7eb4476fcfe406feb  dialogue-icons-8.zip
6c6d285ad88b5e5df7732fd79afa77c8ea51563fbb296abe97b804a3b21a4c5f  other-expressions-6.zip
f6c3e2d6e6ddcc632253ea15f6a4e7de2532a71107d52846c41224fcef53eb30  daram-approved-10.zip

Preserve originals and existing actor scale. Read per-package manifests before mapping to existing runtime slots/poses. Do not invent dialogue or change story conditions. Icons and additional expressions were not yet runtime-connected at handoff. Daram contains static poses, not animation. Map candidates are deliberately excluded because they failed QA.
