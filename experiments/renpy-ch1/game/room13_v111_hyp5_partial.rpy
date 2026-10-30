# 2026-10-30 소유자 결정(논쟁 점검 P28, B안 「추천안대로」): 11일 가설 회의 5번(13호 난로의 돌)에서 기회가 다하면,
# 1~4번을 이겼어도 회의 전체가 져서 학교에서 불을 끄겠다던 집들까지 다시 불을 켰다. 앞에서 설득한 결과가 한 번에
# 사라지면 처음 하는 사람에게 억울하게 읽힌다. 1~4번 중 하나라도 이겼으면 반쪽으로 끝내고, 설득된 집만 불을 끈다.
# 5번을 못 증명한 것은 결과 줄(hyp_result11)의 반쪽 문구가 그대로 말한다. 하나도 못 이겼으면 예전처럼 진다.
# days1114.rpy 의 줄 번호를 다른 표가 참조하므로 그쪽은 한 줄(jump 대상)만 바꾸고 여기서 잇는다.
label r13_v111_hyp5_after_lost11:
    if any(r13_v111_value("hyp_issue:%d"%i)=="won" for i in (1,2,3,4)):
        $ r13_nw_meeting_end("hypothesis","partial")
        call r13_lines(r13_nw_block('hyp_chief11'),'nw:hyp_chief11')
        jump r13_v111_hyp_end11
    jump r13_v111_hyp_lost_gate11
