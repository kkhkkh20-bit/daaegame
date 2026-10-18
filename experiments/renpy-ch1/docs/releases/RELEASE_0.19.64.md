# Release 0.19.64: admin meeting Replay keymap hotfix

## Fix
Native Ren'Py 8.5.3 execution found an Invalid key specifier quick_load exception when entering the new admin meeting Replay. Bind optional quick-save/load events only when registered in config.keymap. Registered shortcuts remain blocked; native Replay save protection, disabled autosave and menu exit behavior remain intact. No story, dialogue, UI design or artwork changes.

## Verification
The real native C2 meeting_direction test passed for 0.19.63, including wrong/correct counter choices and a captured screenshot. The new admin native test exposed this defect before reaching its state-restoration assertions. This hotfix retains that test and adds a static registration guard regression. Updated native execution, unit/lint/build and public deployment verification are pending at preparation; no runtime pass is claimed here.

## Packaging
Use dev/build_web.py with prior .rpyc seeding and 8 MiB parts. Apply only verified generated output. No manual packaged-data edits.
