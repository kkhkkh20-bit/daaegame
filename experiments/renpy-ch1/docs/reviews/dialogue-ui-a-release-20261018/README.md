# Approved dialogue UI — 0.19.62

Owner selected A: Galmuri11 Regular throughout. Character name outlines stay; question names and headings use the shared regular font. No comparison fonts or bold font are shipped.

Dialogue: current-conversation skip, record, More; question screen: present, record, More. Record and More share width 160, visible height 56, with mobile touch height 80. Date panel and More share the right margin. Skip requires confirmation and stops at the next choice.

Auto and backlog live under More. Existing dialogue-hide, morning restart and confirmed main-menu return remain available. Meeting-specific tools keep the existing live-debate stop action and playback behaviour.

Validation: dev/check.sh; official dev/build_web.py; dev/qa_footer_concept.py on Chromium desktop/mobile, including presentation cancellation, records, backlog, auto stop, skip cancellation, and meeting-tools smoke check. Captures and report accompany this note.

Includes the concurrent 0.19.61 shared confirmation-card design; final build regenerated after integration.
