# 현재 공개 본편은 돈을 사용하지 않는다. 과거 잔액은 저장 호환용으로만 둔다.
# 사건 판정·증거·생사는 그대로이며, 임의의 스킬 보상을 만들지 않는다.
init 392 python:
    # 구 캠페인의 r13_prove 래퍼는 이 전역 표를 매번 조회한다.
    # 정답 처리는 원래 함수가 마치고, 현금 보상만 더 이상 생성하지 않는다.
    R13_EP_REWARD={}

    _r13_cash_policy150_cash=r13_cash
    def r13_cash(delta,text):
        if r13_v111_active():return False
        return _r13_cash_policy150_cash(delta,text)

    # 구 상점 호출이 다시 연결되어도 현재 판의 잔액을 구매에 쓰지 않는다.
    _r13_cash_policy150_purchase=r13_purchase
    def r13_purchase(state,key):
        if r13_v111_active():return state,False
        return _r13_cash_policy150_purchase(state,key)
