# 1부 선택 탐색의 저장 모델. 화면·소리·일정·회의 판정은 여기서 실행하지 않는다.
init 389 python:
    import builtins as R13Ex149Builtins
    from collections.abc import Mapping as R13Ex149Mapping

    R13_EX149_ITEMS=("cord","weight")
    R13_EX149_DELIVERY_PARTS=("delivery_large_tag","delivery_small_tag","delivery_box")
    R13_EX149_MARKS=frozenset(R13_EX149_DELIVERY_PARTS+("intro_seen","delivery_tied","knot_method",
        "scale_reference","scale_placed","scale_pivot","scale_corrected"))

    def r13_ex149_state():
        state=getattr(store,"room13",None)
        story=state.get("v111") if isinstance(state,R13Ex149Mapping) else None
        row=story.get("exploration149",{}) if isinstance(story,R13Ex149Mapping) else {}
        return winter_copy.deepcopy(dict(row)) if isinstance(row,R13Ex149Mapping) else {}

    def r13_ex149_available():
        state=getattr(store,"room13",None)
        if not isinstance(state,R13Ex149Mapping):return False
        story=state.get("v111")
        if not isinstance(story,R13Ex149Mapping) or not isinstance(story.get("exploration149",{}),R13Ex149Mapping):return False
        if not isinstance(story.get("values",{}),R13Ex149Mapping):return False
        day=state.get("day")
        return bool(type(day) is int and 2<=day<=7 and r13_v111_active() and r13_sidequest_calm()
                    and _r13_ex149_wallet() is not None)

    def _r13_ex149_wallet():
        state=getattr(store,"room13",None)
        if not isinstance(state,R13Ex149Mapping) or not isinstance(state.get("livelihood",{}),R13Ex149Mapping):return None
        # 기존 물품 저장 위치만 재사용한다. 과거 cash/debt 값은 해석하지 않는다.
        wallet=winter_copy.deepcopy(dict(state.get("livelihood",{})))
        for key,default in (("items",[]),("used",[]),("ledger",[]),("borrowed",{})):
            wallet.setdefault(key,default)
        for key in ("items","used","ledger"):
            # store.list는 RevertableList다. 구 저장·외부 준비 코드의 기본 list도 받는다.
            if not isinstance(wallet.get(key),R13Ex149Builtins.list):return None
        if any(not isinstance(item,str) for item in wallet["items"]+wallet["used"]):return None
        if not isinstance(wallet.get("borrowed"),R13Ex149Mapping):return None
        return winter_copy.deepcopy(dict(wallet))

    def r13_ex149_owned(item):
        if not isinstance(item,str) or item not in R13_EX149_ITEMS:return False
        wallet=_r13_ex149_wallet()
        return bool(wallet is not None and item in wallet["items"])

    def r13_ex149_weight_borrowed():
        wallet=_r13_ex149_wallet()
        if wallet is None or "weight" not in wallet["items"]:return False
        loan=wallet["borrowed"].get("weight")
        return bool(isinstance(loan,R13Ex149Mapping) and loan.get("owner")=="resident_eunho")

    def r13_ex149_mark(key,value=True):
        if not r13_ex149_available() or not isinstance(key,str) or key not in R13_EX149_MARKS:return False
        if value is not None and type(value) not in (bool,int,str):return False
        if r13_ex149_state().get(key)==value:return False
        state=winter_copy.deepcopy(store.room13)
        state["v111"].setdefault("exploration149",{})[key]=value
        store.room13=state
        return True

    def r13_ex149_person_ready(person):
        return bool(isinstance(person,str) and r13_ex149_available()
                    and person in r13_visible_people() and r13_v111_actor_ready(person)
                    and r13_v111_person_alive(person) and not r13_v111_value("busy:"+person)
                    and not r13_v111_value("departed:"+person))

    def r13_ex149_receive(item):
        if not isinstance(item,str) or item not in R13_EX149_ITEMS or not r13_ex149_person_ready("resident_eunho"):return False
        if store.room13.get("location") not in ("market","store"):return False
        wallet=_r13_ex149_wallet()
        if wallet is None or item in wallet["items"] or (item=="cord" and item in wallet["used"]):return False
        state=winter_copy.deepcopy(store.room13)
        wallet["items"].append(item)
        title={"cord":"질긴 묶음끈","weight":"표준 저울추"}[item]
        if item=="weight":wallet["borrowed"]["weight"]=dict(owner="resident_eunho",day=state["day"])
        wallet["ledger"].append(dict(day=state["day"],text=title+(" 빌림" if item=="weight" else " 받음"),amount=0))
        state["livelihood"]=wallet;store.room13=state
        return True

    def r13_ex149_return_weight():
        if not r13_ex149_person_ready("resident_eunho") or store.room13.get("location") not in ("market","store"):return False
        if not r13_ex149_weight_borrowed():return False
        wallet=_r13_ex149_wallet()
        if wallet is None or "weight" not in wallet["items"]:return False
        state=winter_copy.deepcopy(store.room13)
        wallet["items"].remove("weight");wallet["borrowed"].pop("weight",None)
        wallet["ledger"].append(dict(day=state["day"],text="은호에게 표준 저울추 반납",amount=0))
        state["livelihood"]=wallet;store.room13=state
        return True

    def r13_ex149_observe(part):
        if not isinstance(part,str) or not r13_ex149_available():return False
        here=store.room13.get("location")
        if part in R13_EX149_DELIVERY_PARTS:
            if here!="gate" or not r13_ex149_person_ready("karo"):return False
        elif part=="scale_placed":return r13_ex149_scale_place()
        elif part=="scale_reference":
            if here!="store":return False
        elif part=="scale_pivot":
            if here!="store" or r13_ex149_state().get("scale_placed") is not True:return False
        else:return False
        return r13_ex149_mark(part)

    def r13_ex149_delivery_ready():
        state=r13_ex149_state()
        return bool(r13_ex149_person_ready("karo") and store.room13.get("location")=="gate"
                    and all(state.get(part) is True for part in R13_EX149_DELIVERY_PARTS)
                    and r13_ex149_owned("cord") and not state.get("delivery_tied"))

    def r13_ex149_delivery_tie():
        if not r13_ex149_delivery_ready():return False
        # 짐에 쓴 끈 대신 까로가 실제 여분 한 토막을 건넨다. 보유 수는 그대로다.
        return r13_ex149_mark("delivery_tied")

    def r13_ex149_delivery_report():
        state=r13_ex149_state()
        if (state.get("delivery_tied") is not True or state.get("knot_method")
                or store.room13.get("location")!="gate" or not r13_ex149_person_ready("karo")):return False
        return r13_ex149_mark("knot_method")

    def r13_ex149_scale_place():
        if (not r13_ex149_available() or store.room13.get("location")!="store"
                or not r13_ex149_owned("weight") or r13_ex149_state().get("scale_placed")):return False
        return r13_ex149_mark("scale_placed")

    def r13_ex149_scale_correct():
        if not r13_ex149_available():return False
        state=r13_ex149_state()
        if (store.room13.get("location")!="store" or not r13_ex149_person_ready("resident_eunho")
                or state.get("scale_placed") is not True or state.get("scale_pivot") is not True
                or state.get("scale_corrected") or not r13_ex149_owned("weight")):return False
        return r13_ex149_mark("scale_corrected")

    def r13_ex149_lamp_target(obj):
        if not isinstance(obj,str) or not r13_ex149_available():return False
        state=store.room13;story=state["v111"]
        if (state.get("day")!=2 or story.get("gate")!="lamp_prep2"
                or state.get("location")!="square" or obj!="lamp"):return False
        if (r13_v111_value("lamp_latch_seen2") is not True or r13_v111_value("lamp_bound2")
                or r13_v111_value("lamp_cord2")
                or not r13_ex149_owned("cord")):return False
        # 래치를 이미 보고 아직 끈이 없으면 활성 선택지에는 lamp가 없다.
        # 본편 원본의 고정 대상만 확인하고, 현재 실행 조건은 위에서 검사한다.
        binding=R13_V111_BINDINGS.get("lamp_prep2",{})
        return any(option.get("object")=="lamp" and option.get("location")=="square"
                   and option.get("index",index)==3 for index,option in enumerate(binding.get("options",[])))

    def r13_ex149_lamp_ready(obj):
        return r13_ex149_lamp_target(obj) and r13_ex149_state().get("knot_method") is True

    def r13_ex149_lamp_needs_method(obj):
        return r13_ex149_lamp_target(obj) and r13_ex149_state().get("knot_method") is not True

    def r13_ex149_lamp_supply(obj):
        if not r13_ex149_lamp_ready(obj):return False
        wallet=_r13_ex149_wallet()
        if wallet is None:return False
        state=winter_copy.deepcopy(store.room13)
        wallet["items"].remove("cord")
        if "cord" not in wallet["used"]:wallet["used"].append("cord")
        wallet["ledger"].append(dict(day=state["day"],text="3번 등 걸쇠 고정용 묶음끈",amount=0))
        state["livelihood"]=wallet
        state["v111"].setdefault("values",{})["lamp_cord2"]=True
        store.room13=state
        return True
