# Dashboard integration on 0.19.44

Parent patch dcdc699c was cherry-picked as c1a1642e after main 0.19.43 Pages run 39081767475 succeeded. Only generated data.json/version.json conflicted; latest local data was retained until the complete generator regenerated all data from c1a1642e. No game/art changes came from the dashboard patch.

Seven unit tests, three JavaScript syntax checks and tools/resource-dashboard/qa_browser.py passed against the regenerated local server. Actual Chromium 151 desktop and 390px touch emulation covered aspect preservation, viewer focus/Back/Escape, filters, two-finger pinch, MP3/WAV playback and error/exclusivity handling. Browser report and final mobile captures are adjacent. This is local verification; public HTTPS reads in this environment are blocked by proxy CONNECT 403. No claim of physical-device testing.
