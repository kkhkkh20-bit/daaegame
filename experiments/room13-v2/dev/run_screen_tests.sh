#!/bin/bash
# 새 판 화면 시험. 지금 판 시험기와 달리 다른 renpy 를 죽이지 않는다 — 자기가 띄운 프로세스 묶음만 끝낸다.
#   dev/run_screen_tests.sh [시험 이름 ...]   (기본: 1일 셋)
cd "$(dirname "$0")/.." || exit 1
SDK=${RENPY_SDK:-$HOME/.cache/renpy/renpy-8.5.3-sdk}
OUT=${V2_QA_OUT:-/tmp/room13-v2-qa}; mkdir -p "$OUT"
TESTS=("$@"); [ ${#TESTS[@]} -eq 0 ] && TESTS=(v2_day01_right v2_day01_partial v2_day01_detours)
fail=0
for tc in "${TESTS[@]}"; do
  rm -rf game/saves tests "$HOME/.renpy/room13-v2"
  mkdir -p tests
  log=$OUT/$tc.txt; rm -f "$log"
  start=$(date +%s.%N)
  setsid timeout ${V2_TEST_TIMEOUT:-600} xvfb-run -a -s "-screen 0 1280x720x24" "$SDK/renpy.sh" . test "$tc" > "$log" 2>&1 &
  pid=$!
  for i in $(seq 1 ${V2_TEST_TIMEOUT:-600}); do grep -q "Status:" "$log" 2>/dev/null && break; kill -0 $pid 2>/dev/null || break; sleep 1; done
  end=$(date +%s.%N)
  # setsid 로 띄워 세션 번호가 곧 $pid 다. 그 세션(우리가 띄운 renpy·Xvfb)만 끝낸다.
  sleep 1; pkill -KILL -s $pid 2>/dev/null; wait $pid 2>/dev/null
  status=$(grep -ao 'Status: [A-Z]*' "$log" | tail -1)
  echo "== $tc ${status:-Status: KILLED} $(grep -ao 'Time: [0-9.]* s' "$log" | tail -1) wall $(echo "$end - $start" | bc)"
  [ -f tests/boot.txt ] && echo "boot_epoch $(cat tests/boot.txt) start_epoch $start"
  [ -f tests/measure.txt ] && cat tests/measure.txt && echo
  [ -d tests/screenshots ] && { mkdir -p "$OUT/$tc"; cp tests/screenshots/*.png "$OUT/$tc/" 2>/dev/null; }
  [ "$status" = "Status: PASSED" ] || { fail=1; grep -a -B2 -A12 "Traceback\|FAILED\|Error\|assert" "$log" | tail -60; }
done
exit $fail
