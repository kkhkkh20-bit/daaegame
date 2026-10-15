# Borrowed tools and using items on places.
# - Borrow: a resident lends a tool for a deposit, refunded on return.
# - Use: while an item is held, inspecting a certain place offers "~을 쓴다".
#   Results are story records, resident topics or existing flags; meeting
#   proof rules are unchanged. The only route change: lamp soot + Buri's knife
#   reveal the secret passage in a first run (owner's decision, strict chain);
#   opening it still needs the existing kitchen lever + book latch puzzle.
# init 96: after systems/room13_first_day_flow.rpy (95), so layer order never
# depends on file names (dev/override_map.py).
init 96 python:
    R13_BORROW = {
        "knife": dict(title="부리의 작업칼",npc="buri",deposit=5,need=["life:buri_honest"],
            detail="얇은 판자나 벽지를 들출 수 있다. 돌려주면 보증금을 돌려받는다."),
        "lantern": dict(title="초롱의 손등불",npc="resident_lamplighter",deposit=3,need=["lamplighter_trust"],
            detail="어두운 바닥의 그을음이나 자국을 비춰 볼 수 있다."),
    }

    # New records: story notes, not claim evidence.
    ROOM13["evidence"]["M02"]=dict(id="M02",name="엄마의 두 번째 쪽지",kind="물증",
        establishes="13호실 침대 밑 판자 아래에서 찾은 엄마의 글. ‘이 마을의 불은 장작으로 타지 않아. 사람이 타. 아빠가 오면 이 종이를 보여 줘. 그리고 할머니께는 보여 주지 마.’라고 적혀 있다.",
        does_not_establish="엄마가 지금 어디 있는지는 알려 주지 않는다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["R01"]=dict(id="R01",name="광장 돌에 긁힌 이름들",kind="기록",
        establishes="겨울마다 누군가의 이름이 돌에 새겨졌다가 긁혀 지워졌다. 가장 최근의 이름은 아직 덜 지워졌다.",
        does_not_establish="그 사람들이 어떻게 되었는지는 적혀 있지 않다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["R02"]=dict(id="R02",name="주방 뒤로 이어진 그을음",kind="관찰기록",
        establishes="주방 뒷문 아래 그을음 자국이 벽을 따라 여관 2층 쪽으로 이어진다. 그을음은 여러 겹 겹쳐 있다.",
        does_not_establish="누가, 언제 지나갔는지는 알 수 없다.",scenes=[],current_run_only=True,retained_on_show=True)

    def _r13_item_act(place,title,lines,need,give=(),flags=(),day=(2,13),consume=None,cost=1,not_flags=()):
        return dict(place=place,title=title,lines=list(lines),day=list(day),need=list(need),give=list(give),
            flags=list(flags),cost=cost,not_flags=list(not_flags),item_consume=consume)

    R13_ITEM_ACTIVITIES = {
        "use_knife_under": ("room13","under",_r13_item_act("room13","작업칼로 침대 밑 판자를 들어 올린다",[
            (None,"침대 밑 판자 하나가 다른 판자보다 조금 들떠 있었다. 칼끝을 틈에 밀어 넣자 판자가 쉽게 들렸다."),
            (None,"판자 아래에 접힌 종이가 있었다. 다람이 이름 옆에 작은 도토리가 그려져 있었다. 아내가 쓰던 표시였다."),
            (None,"‘다람아, 이 마을의 불은 장작으로 타지 않아. 사람이 타. 아빠가 오면 이 종이를 보여 줘. 그리고 할머니께는 보여 주지 마.’"),
            ("dad","(아내는 불의 비밀을 알고 있었다. 그리고 그 사실을 이 방 주인에게도 숨겼다.)",{"thought":True})],
            ["own:knife","lodging"],give=["M02"],not_flags=["M02"])),
        "use_knife_burlap": ("store","burlap",_r13_item_act("store","작업칼로 포장천 자루 바닥을 갈라 본다",[
            (None,"포장천 자루는 위쪽만 헐렁했다. 아래쪽은 이상하게 단단했다. 칼로 바닥 실밥을 끊자 숨겨진 이중 바닥이 드러났다."),
            (None,"그 안에 말린 고기와 곡식 자루가 차곡차곡 숨겨져 있었다. 모두 창고 장부에 ‘바닥남’으로 적힌 물건들이었다."),
            ("dad","(은호 사장이 이걸 모를 리 없다. 겨울 끝까지 버틸 몫을 몰래 따로 빼 둔 것이다.)",{"thought":True})],
            ["own:knife"],flags=["hidden_stock"],day=(5,13),not_flags=["hidden_stock"])),
        "use_rubbing_stone": ("square","stone",_r13_item_act("square","탁본 종이를 대고 숯으로 문지른다",[
            (None,"광장 돌 표면은 매끈해 보였다. 하지만 종이를 대고 숯으로 문지르자 긁힌 자국 아래에서 글자가 떠올랐다."),
            (None,"떠오른 글자는 이름이었다. 한 줄에 하나씩, 겨울마다 하나씩 늘어난 이름들이었다. 누군가 날카로운 것으로 긁어 지운 것이다."),
            (None,"맨 아래 이름은 아직 덜 지워져 있었다. 돌 아래 놓인 꽃 가운데 그 이름 앞의 꽃만 시들지 않았다."),
            ("dad","(마을 사람 누구도 제물이라는 말을 입에 올리지 않았다. 대신 돌에서 이름을 지웠다.)",{"thought":True})],
            ["own:rubbing"],give=["R01"],consume="rubbing",not_flags=["R01"])),
        "use_lantern_rear": ("kitchen","rear",_r13_item_act("kitchen","손등불로 뒷문 아래 바닥을 비춰 본다",[
            (None,"손등불을 낮게 들자 문턱 아래 바닥에 검은 줄이 보였다. 그을음이었다. 등을 든 누군가가 같은 자리를 여러 번 오간 것이다."),
            (None,"그을음 자국은 뒷문 밖으로 나가지 않았다. 벽을 따라 안쪽으로 이어지다가 계단 밑 벽에서 끊겼다. 그 벽 너머 위층은 13호실이다."),
            ("dad","(누군가 문이 아닌 곳으로 드나들었다. 바로 저 벽 쪽으로.)",{"thought":True})],
            ["own:lantern"],give=["R02"],flags=["soot_trail"],not_flags=["soot_trail"])),
        "use_knife_books": ("room13","books",_r13_item_act("room13","작업칼로 책장 뒤 벽지를 들춘다",[
            (None,"책장 뒤 벽지는 그을음 자국이 끊긴 바로 그 벽이었다. 벽지 이음매를 칼로 따라 긋자 종이 아래에서 나무판이 드러났다."),
            (None,"판 가장자리에는 손때 묻은 홈이 있었다. 책장 아래 칸의 붉은 책에는 가는 줄이 이어져 있었다. 판은 밀어도 꿈쩍하지 않았다. 반대편 어딘가에서 걸쇠가 잡고 있는 것이다."),
            ("dad","(그을음은 주방에서 시작됐다. 그렇다면 이 판을 여는 손잡이도 주방 쪽에 있을 것이다.)",{"thought":True})],
            ["own:knife","soot_trail"],flags=["passage_found"],not_flags=["passage_found"])),
        "use_weight_scale": ("store","scale",_r13_item_act("store","표준 저울추를 올려 저울을 맞춰 본다",[
            (None,"표준 추를 올리자 저울 바늘이 눈금보다 한 칸 더 기울었다. 살펴보니 바늘 뒤 나사가 새로 조여져 있었다."),
            ("dad","(저울이 무게를 더 많이 재면, 같은 돈을 받고도 물건은 덜 내주게 된다.)",{"thought":True})],
            ["own:weight"],flags=["scale_rigged"],consume="weight",not_flags=["scale_rigged"])),
    }
    for _key,(_place,_obj,_spec) in R13_ITEM_ACTIVITIES.items():
        ROOM13["activities"][_key]=_spec
        R13_CONTEXT_ACTIVITIES[(_place,_obj)]=tuple(R13_CONTEXT_ACTIVITIES.get((_place,_obj),()))+(_key,)

    # Topics: borrow / return, and resident reactions to what the items found.
    for _key,_b in R13_BORROW.items():
        ROOM13["topics"]["borrow:"+_key]=dict(npc=_b["npc"],title=_b["title"]+"을 빌린다",day=[2,14],need=list(_b["need"]),give=[],flags=[],lines=[
            ("dad","%s을 잠시 빌릴 수 있을까요? 보증금으로 %d냥을 맡기겠습니다."%(_b["title"].split("의 ")[-1],_b["deposit"])),
            (_b["npc"],"조심해서 쓰고 꼭 돌려줘요. 보증금은 그때 돌려드릴게요.")])
        ROOM13["topics"]["return:"+_key]=dict(npc=_b["npc"],title=_b["title"]+"을 돌려준다",day=[2,14],need=[],give=[],flags=[],lines=[
            ("dad","덕분에 잘 썼습니다. 이제 돌려드릴게요."),
            (_b["npc"],"멀쩡하네요. 보증금 여기 있어요.")])
    ROOM13["topics"]["eunho_hidden"]=dict(npc="resident_eunho",title="자루 밑에 숨긴 식량을 묻는다",day=[5,14],need=["hidden_stock"],give=[],flags=["supply_terms","eunho_exposed"],lines=[
        ("dad","포장천 자루 바닥에 식량이 따로 숨겨져 있더군요. 장부에는 바닥났다고 적혀 있던데요."),
        ("resident_eunho","……겨울은 길어요. 겨울 끝에 가서 아무도 가진 게 없으면, 그때는 누가 나눠 줍니까."),
        ("dad","겨울 끝이 오기 전에 굶은 사람들이 먼저 쓰러집니다."),
        ("resident_eunho","알겠습니다. 대피소가 정해지면 숨겨 둔 몫을 내놓지요. 대신 가져가는 사람은 이름을 적는다는 조건으로요.")])
    ROOM13["topics"]["eunho_scale"]=dict(npc="resident_eunho",title="저울이 기울어 있다고 말한다",day=[2,14],need=["scale_rigged"],give=[],flags=["shop_discount"],lines=[
        ("dad","가게 저울에 표준 추를 올려 보니 바늘이 한 칸 더 기울더군요."),
        ("resident_eunho","……다른 가게도 다들 그렇게 하는 줄 알았어요. 저울 바늘은 오늘 바로잡지요."),
        ("resident_eunho","그동안 물건을 덜 드린 만큼, 앞으로는 한 냥씩 깎아 드리겠습니다.")])
    ROOM13["topics"]["ppul_names"]=dict(npc="resident_ppul",title="돌에 긁힌 이름들을 보여 준다",day=[2,14],need=["R01"],give=[],flags=["ppul_names_seen"],lines=[
        ("dad","광장 돌에 종이를 대고 숯으로 떠 온 겁니다. 긁어 지운 자국 아래에 이름들이 남아 있었어요."),
        ("resident_ppul","……대체 어디서 그걸 떠 왔소."),
        ("resident_ppul","이름을 지우라고 한 건 나요. 이름이 남아 있으면 가족들이 매일 그 돌 앞에서 울었으니까."),
        ("dad","이름을 지운다고 그 사람들이 없던 사람이 되지는 않습니다."),
        ("resident_ppul","알아요. 그래서 맨 아래 이름만은…… 차마 다 못 지웠소.")])

    _r13_items_has=r13_has
    def r13_has(key):
        if key.startswith("own:"):
            return key[4:] in r13_wallet(store.room13)["items"]
        return _r13_items_has(key)

    _r13_items_route=r13_secret_route_available
    def r13_secret_route_available():
        return _r13_items_route() or ("passage_found" in (store.room13 or {}).get("flags",[]))

    _r13_items_visible=r13_object_visible
    def r13_object_visible(spec):
        # The bookshelf shows once the soot trail points at this wall.
        if spec is ROOM13["objects"]["room13"].get("books") and r13_has("soot_trail"):
            return True
        return _r13_items_visible(spec)

    _r13_items_topics=r13_topics
    def r13_topics(person):
        wallet=r13_wallet(store.room13);rows=[]
        for key,spec in _r13_items_topics(person):
            if key.startswith("borrow:"):
                tool=key[7:]
                if tool in wallet["items"] or wallet["cash"]<R13_BORROW[tool]["deposit"]:continue
            if key.startswith("return:") and key[7:] not in wallet["borrowed"]:continue
            rows.append((key,spec))
        return rows

    _r13_items_finish_topic=r13_finish_topic
    def r13_finish_topic(key):
        _r13_items_finish_topic(key)
        if key.startswith("borrow:") or key.startswith("return:"):
            n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n);tool=key.split(":",1)[1];b=R13_BORROW[tool]
            if key.startswith("borrow:") and tool not in wallet["items"] and wallet["cash"]>=b["deposit"]:
                wallet["cash"]-=b["deposit"];wallet["items"].append(tool);wallet["borrowed"][tool]=b["deposit"]
                wallet["ledger"].append(dict(day=n["day"],text=b["title"]+" 보증금",amount=-b["deposit"]))
            elif key.startswith("return:") and tool in wallet["borrowed"]:
                refund=wallet["borrowed"].pop(tool)
                if tool in wallet["items"]:wallet["items"].remove(tool)
                wallet["cash"]+=refund
                wallet["ledger"].append(dict(day=n["day"],text=b["title"]+" 보증금 돌려받음",amount=refund))
            # Borrow/return can be repeated; never keep them as read.
            if key in n.get("read_topics",[]):n["read_topics"].remove(key)
            n["livelihood"]=wallet;store.room13=n

    _r13_items_finish_action=r13_finish_action
    def r13_finish_action(key):
        _r13_items_finish_action(key)
        item=ROOM13["activities"].get(key,{}).get("item_consume")
        if item:
            n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n)
            if item in wallet["items"]:wallet["items"].remove(item)
            wallet["used"]=list(dict.fromkeys(wallet["used"]+[item]))
            n["livelihood"]=wallet;store.room13=n
