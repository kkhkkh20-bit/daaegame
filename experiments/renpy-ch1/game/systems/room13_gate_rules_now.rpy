# 2026-10-29 1일 입구: 규칙판은 언제 눌러도 처음에 바로 읽힌다(소유자 「두 번 읽어야 증거가 나오는 것 같다」).
# 조사 단계의 같은 읽기(r13_v111_gate_read_rules)와 같은 줄·같은 자료를 쓰고, 대기 화면으로 돌아간다.
label r13_v111_gate_rules_now:
    $ r13_field_reading=True
    call r13_lines(r13_v111_lines(['MS14_D01_S03_L0007']), 'v111:gate_read_rules:MS14_D01_S03_L0007')
    $ r13_field_reading=False
    $ r13_v111_commit('MS14_D01_S03_L0007')
    return
