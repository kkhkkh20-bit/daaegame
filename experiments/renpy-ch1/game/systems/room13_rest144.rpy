# 잠자기는 플레이어가 확인하기 전에는 원래 시나리오 선택을 반환하지 않는다.
init 353 python:
    R13_V111_REST_GATES=frozenset((
        "lamp_prep2","sleep1","sleep2","sleep3","sleep4","sleep5",
        "sleep6","sleep6_input","sleep7","free_sleep7","free_sleep7_input","detained_bed7",
        "sleep8","sleep8_input","sleep9","sleep9_input","sleep10","sleep10_input",
        "sleep11","sleep11_input","sleep12","sleep12_input","sleep12_bed_input",
        "sleep13_input","sleep13_gate_input","departed_bed13"))

    def r13_v111_rest_option():
        if not r13_v111_active():return None
        v=store.room13.get("v111") or {}
        if v.get("gate") not in R13_V111_REST_GATES:return None
        return next((o for o in r13_v111_binding().get("options",[])
                     if o.get("index")==0 and o.get("location")==store.room13.get("location")
                     and o.get("object")),None)

    def r13_v111_rest_message():
        return "오늘 일정을 마치고 잠잘까요?\n잠을 자면 다음 날 아침으로 넘어갑니다."

label r13_v111_rest_confirm:
    if not r13_v111_rest_option():
        return False
    window hide
    call screen r13_confirm(r13_v111_rest_message(),"잠자기","더 둘러보기")
    return bool(_return)
