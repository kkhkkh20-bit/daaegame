# The inn before and after (owner's knowledge-run plan A, 0.18.18). Canon: CASE13_CANON_SYNC.md.
#   A-1 Granny walked back from 13호 through the passage after stepping in the spilled wax (E09):
#       after the case, white wax flakes sit in the laundry-door threshold in the kitchen. Before
#       the case the threshold is clean. Dad mentions the earlier state only if he looked before.
#   A-2 The book reacts to the lever state; no "turn on the kitchen lever" hint.
#       Owner decision (2026-10-15): if before day 4 evening the lever was left raised, or the
#       panel was wedged from the room side, Granny notices someone touched her mechanism and
#       calls off the plan. Prevention only: no fake body, and no proof of the plan is gained.
#   D-2 The wedge's second use: jamming the bookshelf panel from 13호.
init 120 python:
    for _key,_name,_est,_not in (
        ("H12","안쪽에서 밀린 쐐기","책장 아래에 끼워 둔 쐐기가 방 쪽으로 조금 밀려 나와 있었다. 판은 닫힌 채였다.","누가 안쪽에서 밀었는지는 알 수 없다."),
        ("H13","누군가 내려 둔 레버","올려 두었던 주방 레버가 그날 저녁 뒤에는 내려가 있었다.","누가, 언제 내렸는지는 알 수 없다."),
        ("H14","세탁실 문턱의 촛농 부스러기","사건 뒤 주방에서 세탁실로 가는 나무문 문턱 틈에 하얀 촛농 부스러기가 눌려 붙어 있다.","누구의 신발에서 떨어졌는지, 언제 생겼는지는 이것만으로 알 수 없다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="관찰기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(H12="밀린 쐐기",H13="내려 둔 레버",H14="문턱의 촛농")

    _rear=ROOM13["objects"]["kitchen"]["rear"]
    ROOM13["objects"]["kitchen"]["rear_after"]=dict(_rear,give=["H14"],flags=[],inn_after="unseen",
        text="창이 없는 나무문 너머는 세탁실이다. 문턱 틈에 하얀 촛농 부스러기가 눌려 붙어 있다.")
    ROOM13["objects"]["kitchen"]["rear_after_known"]=dict(_rear,give=["H14"],flags=[],inn_after="seen",
        text="창이 없는 나무문 너머는 세탁실이다. 문턱 틈에 하얀 촛농 부스러기가 눌려 붙어 있다. 전에 봤을 때는 없던 것이다.")
    for _k in ("rear_after","rear_after_known"):
        R13_CONTEXT_ACTIVITIES[("kitchen",_k)]=tuple(R13_CONTEXT_ACTIVITIES.get(("kitchen","rear"),()))

    _r13_inn_visible=r13_object_visible
    def r13_object_visible(spec):
        after=(store.room13 or {}).get("case_state")=="occurred"
        if spec is ROOM13["objects"]["kitchen"]["rear"] and after:return False
        if spec.get("inn_after")=="unseen":return after and not r13_has("observed:kitchen:rear")
        if spec.get("inn_after")=="seen":return after and r13_has("observed:kitchen:rear")
        return _r13_inn_visible(spec)

    ROOM13["activities"]["use_wedge_books"]=_r13_item_act("room13","나무 쐐기를 책장 아래 판 틈에 끼운다",[
        (None,"책장 아래 판과 바닥 사이에 나무 쐐기를 밀어 넣었다. 판이 안쪽으로 밀리지 않게 단단히 박혔다.")],
        ["own:wedge","passage_known"],flags=["passage_wedged"],day=(2,4),consume="wedge",cost=0,not_flags=["passage_wedged"])
    ROOM13["activities"]["use_wedge_books"]["case"]="pending"
    R13_CONTEXT_ACTIVITIES[("room13","books")]=tuple(R13_CONTEXT_ACTIVITIES.get(("room13","books"),()))+("use_wedge_books",)

    def r13_plan_noticed():
        s=store.room13 or {}
        return s.get("case_state")=="pending" and (bool(s.get("kitchen_switch")) or r13_has("passage_wedged"))

label r13_case_noticed:
    # The lever or the panel had been changed: Granny never reached 13호.
    $ _was_wedged=r13_has("passage_wedged")
    call r13_scene("hall","여관 2층 · 연기가 새는 문","quiet")
    $ source_fx("knock")
    call r13_lines([(None,"계단 위에서 나무를 두드리는 소리가 들렸다. 우리 방 문틈 아래로 연기가 새어 나왔다."),
        ("nabi","다람아, 문에서 떨어져!"),
        ("doto","안쪽 빗장이 안 풀립니다."),
        ("dad","다람아!"),
        ("daram","아빠…… 나 여기 있어."),
        ("granny","다들 비켜요. 공구 가져왔어."),
        (None,"도토가 지렛대를 문틀 틈에 밀어 넣었다.")],"case:noticed:door")
    $ source_fx("impact")
    call r13_scene("room","여관 2층 · 13호","quiet")
    call r13_lines([(None,"너울이 연기 나는 작은 깔개 위에 젖은 천을 덮었다. 침대 아래에서 다람이가 손을 뻗었다."),
        (None,"어르신은 침대 옆에 쓰러져 있었다. 팔에 멍이 들었지만 가슴이 오르내리고 있었다."),
        ("resident_seori","숨이 붙어 있습니다. 머리는 다치지 않았어요."),
        ("daram","내가 할아버지를 때렸어. 할아버지가 안 놔줘서……"),
        ("dad","다친 데는 없어?"),
        (None,"한참 뒤 어르신이 눈을 떴다."),
        ("resident_owlgp","……아이 손목을 내가 잡았소. 잠깐 정신이 흐려졌었지. 아이 잘못이 아니오.")],"case:noticed:room")
    if _was_wedged:
        call r13_lines([(None,"책장 아래에 끼워 둔 쐐기가 방 쪽으로 조금 밀려 나와 있었다. 판은 닫힌 채였다.")],"case:noticed:wedge")
        $ r13_grant(["H12"],"사건 뒤 13호 책장 아래")
    if room13["kitchen_switch"]:
        call r13_lines([(None,"아래층으로 내려가며 주방 찬장 아래 덮개를 보았다. 올려 두었던 레버가 내려가 있었다.")],"case:noticed:lever")
        $ r13_grant(["H13"],"사건 뒤 주방 찬장 아래")
    call r13_lines([(None,"그날 13호에서는 아무도 죽지 않았다. 그렇다고 누군가 하려던 일을 막았다는 증거를 얻은 것은 아니었다.")],"case:noticed:result")
    $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",kitchen_switch=False,passage_open=False,period=3,location="inn")
    $ r13_flag("victim_protected","plan_noticed")
    $ r13_grant(["E17"],"살아 있는 어르신이 간직해 온 베낀 기록")
    jump r13_roam
