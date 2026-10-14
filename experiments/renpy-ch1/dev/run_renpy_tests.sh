#!/bin/bash
# Ren'Py UI tests (game/qa_tests/tests.rpy) run directly on this project folder.
#   RENPY_SDK=/path/renpy-8.5.3-sdk dev/run_renpy_tests.sh carriage_skip trial_win ...
# Without names it runs the standard set. Needs xvfb-run.
# Ren'Py does not exit after a test: the script waits for "Status:" and stops it.
cd "$(dirname "$0")/.." || exit 1
SDK=${RENPY_SDK:?set RENPY_SDK to the Ren\'Py 8.5.3 SDK folder}
LOG=${ROOM13_QA_OUT:-/tmp/room13-qa}/renpy; mkdir -p "$LOG"
TESTS=("$@"); [ ${#TESTS[@]} -eq 0 ] && TESTS=(newgame carriage_skip fresh_run items_chain shop_flow trial_missing trial_win trial_full finale_win finale_missing town_b_first_run town_b_ambush_musoe town_c_locked town_c_wedge town_n_yeoni town_m_kongi)
fail=0
for tc in "${TESTS[@]}"; do
  ps -eo pid,comm | awk '$2=="renpy"{print $1}' | xargs -r kill -9 2>/dev/null
  rm -rf game/saves tests qa_result.txt qa_items.json ~/.renpy/daaegame-renpy-village-ch1-06/sync/*.save
  log=$LOG/$tc.txt; rm -f "$log"
  timeout 400 xvfb-run -a -s "-screen 0 1280x720x24" "$SDK/renpy.sh" . test "$tc" > "$log" 2>&1 &
  for i in $(seq 1 400); do grep -q "Status:" "$log" 2>/dev/null && break; sleep 1; done
  sleep 1; ps -eo pid,comm | awk '$2=="renpy"{print $1}' | xargs -r kill -9 2>/dev/null
  status=$(grep -o 'Status: [A-Z]*' "$log" | tail -1)
  echo "== $tc $status $(grep -o 'Time: [0-9.]* s' "$log" | tail -1)"
  [ -f qa_result.txt ] && { cat qa_result.txt; echo; }
  [ -f qa_items.json ] && cp qa_items.json "$LOG/$tc-items.json"
  [ -d tests/screenshots ] && { mkdir -p "$LOG/$tc"; cp tests/screenshots/*.png "$LOG/$tc/" 2>/dev/null; }
  [ "$status" = "Status: PASSED" ] || { fail=1; grep -E "Error:|line [0-9]+, in testcase" "$log" | head -3; }
done
rm -rf game/saves tests qa_result.txt qa_items.json
exit $fail
