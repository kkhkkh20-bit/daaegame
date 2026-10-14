# Pure save-local domain model. No UI/audio/persistent side effects.
init 91 python:
    R13_JOBS = {
        "kitchen": dict(title="여관 식사 준비", npc="nabi", place="dining", pay=6,
            detail="식기를 닦고 손님별로 식사를 나눈다.", choice="따로 놓인 그릇에 관해 묻는다"),
        "delivery": dict(title="마을 소포 배달", npc="karo", place="gate", pay=7,
            detail="까로와 짐표를 확인하고 소포를 배달한다.", choice="두 짐표의 주소를 나란히 살핀다"),
        "repair": dict(title="수리점 부품 정리", npc="buri", place="workshop", pay=8,
            detail="부품을 크기별로 나누고 수량을 확인한다.", choice="장부와 맞지 않는 수량을 알린다"),
    }
    # Working both day slots leaves 3-5 spare coins after the 10-coin lodging,
    # so buying something always costs investigation time somewhere.
    R13_DEBT_LIMIT = 20
    # day: on sale from/to. case: only after the room-13 incident happened.
    # Goods for residents open an existing record or topic; none add new proofs.
    R13_SHOP = {
        "snack": dict(title="구운 밤",price=2,day=(2,14),detail="13호실에서 다람이와 나눠 먹는다."),
        "postcard": dict(title="그림엽서",price=3,day=(2,14),detail="다람이와 엄마에게 보낼 엽서를 쓴다."),
        "cord": dict(title="질긴 묶음끈",price=3,day=(2,14),detail="같은 길 소포 두 건을 묶어 배달한다."),
        "hat": dict(title="다람이의 털모자",price=6,day=(2,14),detail="추운 밤에 다람이에게 씌워 준다."),
        "lamp_oil": dict(title="등잔 기름",price=4,day=(3,13),detail="등불을 돌보는 초롱에게 건넬 수 있다."),
        "herbs": dict(title="해열 약초 묶음",price=8,day=(4,7),case=True,detail="진료실의 서리 검사원에게 건넬 수 있다."),
        "file": dict(title="정밀 줄칼",price=7,day=(5,13),case=True,detail="수선하는 톡에게 건넬 수 있다."),
        "blanket": dict(title="두꺼운 담요",price=5,day=(5,13),case=True,detail="처마 밑에서 지내는 밤이에게 건넬 수 있다."),
        "firewood": dict(title="장작 묶음",price=6,day=(8,13),detail="빨래를 맡는 누비 아주머니 가족에게 건넬 수 있다."),
        "rubbing": dict(title="탁본 종이와 숯",price=3,day=(2,14),detail="새겨진 글자를 종이에 그대로 떠 온다."),
        "weight": dict(title="표준 저울추",price=5,day=(2,14),detail="저울이 바르게 재는지 맞춰 볼 수 있다."),
    }

    def r13_shop_price(state,key):
        # Exposing the rigged scale makes 은호 knock one coin off everything.
        price=R13_SHOP[key]["price"]
        return max(1,price-1) if "shop_discount" in state.get("flags",[]) else price

    def r13_shop_on_sale(state,key):
        item=R13_SHOP.get(key)
        if not item:return False
        a,b=item.get("day",(2,14))
        return (a<=state.get("day",1)<=b and (not item.get("case") or state.get("case_state")=="occurred"))

    def r13_wallet(state):
        data=winter_copy.deepcopy(state.get("livelihood",{}))
        for key,value in dict(version=1,cash=0,debt=0,settled=[],jobs=[],relations=[],items=[],used=[],borrowed={},ledger=[],combined_paid=False).items():
            data.setdefault(key,winter_copy.deepcopy(value))
        return data

    def r13_job_allowed(state,key):
        return (key in R13_JOBS and state.get("day",1)>=2 and state.get("period",0)<2
            and "livelihood_open" in state.get("flags",[])
            and not any(j["day"]==state["day"] and (j["period"]==state["period"] or j["key"]==key)
                for j in r13_wallet(state)["jobs"]))

    def r13_complete_job(state,key,choice):
        if choice not in ("finish","ask","combine") or not r13_job_allowed(state,key):
            return state,None
        n=winter_copy.deepcopy(state); wallet=r13_wallet(n); job=R13_JOBS[key]
        combined=(key=="delivery" and choice=="combine" and "same_lane" in wallet["relations"]
            and ("cord" in wallet["items"] or "karo_trusted" in wallet["relations"])
            and not wallet["combined_paid"])
        if choice=="combine" and not combined:return state,None
        pay=job["pay"]*(2 if combined else 1)
        if combined:wallet["combined_paid"]=True
        if choice=="ask":
            marks={"kitchen":["nabi_helped"],"delivery":["same_lane","karo_trusted"],"repair":["buri_honest"]}[key]
            wallet["relations"]=list(dict.fromkeys(wallet["relations"]+marks))
        wallet["cash"]+=pay
        wallet["jobs"].append(dict(day=n["day"],period=n["period"],key=key,choice=choice,pay=pay))
        wallet["ledger"].append(dict(day=n["day"],text=job["title"],amount=pay))
        n["livelihood"]=wallet
        n["period"]+=1
        return n,dict(pay=pay,combined=combined,observed=choice=="ask")

    def r13_settle_lodging(state):
        n=winter_copy.deepcopy(state); wallet=r13_wallet(n); day=n["day"]
        if day in wallet["settled"]:return state
        fee=0 if day==1 else 10
        paid=min(wallet["cash"],fee)
        wallet["cash"]-=paid;wallet["debt"]+=fee-paid
        wallet["settled"].append(day)
        wallet["ledger"].append(dict(day=day,text="첫날 숙식 무료" if day==1 else "방값·밥값 · 갚을 돈 %d냥"%(fee-paid),amount=-paid))
        n["livelihood"]=wallet
        return n

    def r13_purchase(state,key):
        if key not in R13_SHOP:return state,False
        n=winter_copy.deepcopy(state);wallet=r13_wallet(n);item=R13_SHOP[key];price=r13_shop_price(n,key)
        if (n.get("day",1)<2 or "livelihood_open" not in n.get("flags",[]) or wallet["cash"]<price
            or key in wallet["items"] or key in wallet.get("used",[]) or wallet["debt"]>R13_DEBT_LIMIT
            or not r13_shop_on_sale(n,key)):
            return state,False
        wallet["cash"]-=price;wallet["items"].append(key)
        wallet["ledger"].append(dict(day=n["day"],text=item["title"],amount=-price))
        n["livelihood"]=wallet
        return n,True

    def r13_repay(state):
        n=winter_copy.deepcopy(state);wallet=r13_wallet(n)
        paid=min(wallet["cash"],wallet["debt"])
        wallet["cash"]-=paid;wallet["debt"]-=paid
        if paid:wallet["ledger"].append(dict(day=n["day"],text="외상 상환",amount=-paid))
        n["livelihood"]=wallet
        return n
