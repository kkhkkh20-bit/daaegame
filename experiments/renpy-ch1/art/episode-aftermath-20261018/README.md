# Aftermath artwork provenance

Six original 2×2 atlases generated with `image_gen`, each cell a separately selected cinematic illustration. All references were the latest approved `game/assets/dialogue-source-master/*/760/neutral.webp` character profiles; a contact sheet supplied the secondary child identities where the five-reference limit required it. No human father is depicted.

- ep1: Piko blanket / empty portrait place / Tok repairing / Tok detained. Both portrait boards show their backs to preserve the unfinished nose.
- ep2: Musoe and Somi farewell / clinic / adult boots at river / Somi's silence.
- ep3: Kkomi gives Daram an acorn / Daram buries it / Bori with three survivors / empty burnt shed.
- ep4: living Chorong relights a lamp / bereaved mother / Ttadak with frostbitten hands / empty tools and passage.
- ep5: four living children with an open window / Bori and three survivors / four empty places / Bori holding a shoe. The open window was explicitly corrected in the final image.
- ep6: stopped wagon and safe Badook / empty mountain road with torn armband / laundry escape / aftermath of public unrest. The foreground was corrected from a cap to the canonical torn armband. Road-only and armband-only crops are selected independently.

Original PNGs remain unmodified. `dev/import_art.py` encodes the runtime WebP at quality 95; crop rectangles are runtime display metadata. `receipt.json` records source and runtime hashes. Existing approved `bori_adopts_four_alive` and `chorong_injured_alive` compositions are reused for those poses. Supplemental cast compositions draw the approved source profile directly, preserving its canvas offsets and aspect ratio.

The atlases use progressive web loading (`REMOTE_LATER`) rather than adding six full pictures to the initial download. Existing global ending artwork is retained.
