# Comparisons use only materials acquired in this run; never grant source items.
init 78 python:
    def r13_compare_pair(selected,key):
        if key not in (store.room13 or {}).get("evidence",[]):return tuple(selected)
        if key in selected:return tuple(k for k in selected if k!=key)
        return tuple((list(selected)+[key])[-2:])

    def r13_compare_result(selected):
        owned=set((store.room13 or {}).get("evidence",[]))
        if len(set(selected))!=2 or not set(selected)<=owned:
            return "이번 여정에서 모은 기록 두 개를 골라 주세요."
        pair=set(selected)
        if pair=={"E01","E03"}:
            return "(아내 이름으로 온 편지는 이 여관에서 부쳐졌고, 방에는 아내의 바느질과 닮은 매듭이 있다. 여기 머물렀을 가능성은 있지만, 지금도 있는지는 모른다.)" + ("\n다람이: 엄마가 언제 여기 있었는지 물어보자." if r13_home_with_daram() else "")
        if pair=={"G1","G3"}:
            r13_gate_record_comparison()
            return "(신청 원본은 방문객 두 명인데, 초소 명단은 신규 일꾼 본인 한 명으로 옮겨져 있다. 숙소 확인과 겨울철 입장 규칙을 함께 확인해 보여 주자.)"
        if pair in ({"E04","E37"},{"E04","E05"}):
            return "(도면의 연결선과 실제로 움직인 장치가 맞는다. 종이에만 남은 길이 아니었다.)"
        return "(지금 적힌 내용만으로 두 기록이 어떻게 이어지는지는 아직 모르겠다.)"

    def r13_compare_selected(selected,scope=None):
        result=r13_compare_result(selected)
        if scope is not None:scope["feedback"]=result
        else:renpy.set_screen_variable("feedback",result,screen="r13_record_compare")
        renpy.restart_interaction()

# 0.20.x: the old 「기록 비교」 tab (r13_compare_content, a text verdict for two records) was
# unreachable: r13_records maps a "compare" tab to 자료. It is removed; looking at two records
# together is now 「나란히 놓기」 in the 자료 view (systems/room13_evidence_view.rpy), which shows
# no verdict. r13_compare_result and its layers stay for the story code and tests that call them.
# This screen name stays for old saves that had it open.
screen r13_record_compare(called=False):
    modal True
    zorder 80
    use r13_records(initial_tab="all",close_action=(Return() if called else Hide("r13_record_compare")))
