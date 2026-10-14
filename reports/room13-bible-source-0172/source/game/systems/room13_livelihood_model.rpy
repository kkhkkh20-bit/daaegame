# Pure save-local domain model. No UI/audio/persistent side effects.
init 91 python:
    R13_JOBS = {
        "kitchen": dict(title="여관 식사 준비", npc="nabi", place="dining", pay=4,
            detail="식기를 닦고 손님별로 식사를 나눈다.", choice="따로 놓인 그릇에 관해 묻는다"),
        "delivery": dict(title="마을 소포 배달", npc="karo", place="gate", pay=5,
            detail="까로와 짐표를 확인하고 소포를 배달한다.", choice="두 짐표의 주소를 나란히 살핀다"),
        "repair": dict(title="수리점 부품 정리", npc="buri", place="workshop", pay=6,
            detail="부품을 크기별로 나누고 수량을 확인한다.", choice="장부와 맞지 않는 수량을 알린다"),
    }
    R13_SHOP = {
        "snack": dict(title="다람이와 나눌 구운 밤",price=2,detail="13호실에서 함께 먹는다. 단서를 얻는 데 필요하지 않다."),
        "cord": dict(title="질긴 묶음끈",price=3,detail="같은 길의 소포를 함께 묶을 수 있다. 까로에게 빌리는 방법도 있다."),
    }

    def r13_wallet(state):
        data=winter_copy.deepcopy(state.get("livelihood",{}))
        for key,value in dict(version=1,cash=0,debt=0,settled=[],jobs=[],relations=[],items=[],ledger=[],combined_paid=False).items():
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
        n=winter_copy.deepcopy(state);wallet=r13_wallet(n);item=R13_SHOP[key]
        if n.get("day",1)<2 or "livelihood_open" not in n.get("flags",[]) or wallet["cash"]<item["price"] or key in wallet["items"]:
            return state,False
        wallet["cash"]-=item["price"];wallet["items"].append(key)
        wallet["ledger"].append(dict(day=n["day"],text=item["title"],amount=-item["price"]))
        n["livelihood"]=wallet
        return n,True

    def r13_repay(state):
        n=winter_copy.deepcopy(state);wallet=r13_wallet(n)
        paid=min(wallet["cash"],wallet["debt"])
        wallet["cash"]-=paid;wallet["debt"]-=paid
        if paid:wallet["ledger"].append(dict(day=n["day"],text="외상 상환",amount=-paid))
        n["livelihood"]=wallet
        return n
