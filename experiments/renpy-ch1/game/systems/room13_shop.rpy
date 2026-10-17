# Shop (은호, 공동 물품 창고): goods bought with spare coins.
# Goods for residents are handed over through a topic that opens while the item
# is owned; handing it over opens an existing record or topic, then it is used up.
init 94 python:
    # key: (npc, topic title, extra condition, lines, give, flags)
    R13_ITEM_TOPICS = {
        "hat": ("daram","털모자를 씌워 준다",lambda:r13_home_with_daram(),[
            ("dad","이리 와. 오늘 너 주려고 산 털모자야."),
            ("daram","털모자다! 이제 귀 안 시려."),
            ("dad","밤에는 바람이 세니까 이 모자 꼭 쓰고 다녀."),
            ("daram","엄마 만나면 이 모자 보여 줄래. 아빠가 사 줬다고 할 거야.")],[],["daram_hat"]),
        "postcard": ("daram","엄마에게 엽서를 쓴다",lambda:r13_home_with_daram(),[
            ("dad","엄마한테 보낼 엽서야. 어디로 보낼지는 아직 모르지만, 미리 써 두자."),
            ("daram","나는 엽서에 그림 그릴래. 여관이랑 눈사람이랑."),
            ("dad","(어디로 부쳐야 할지 모르는 엽서다. 그래도 이 아이의 그림만큼은 꼭 전하고 싶다.)",{"thought":True}),
            ("daram","다 그렸다. 엄마가 이 그림 보면 웃을 거야.")],[],["postcard_written"]),
        "lamp_oil": ("resident_lamplighter","등잔 기름을 건넨다",lambda:not r13_has("topic:lamplighter_warning"),[
            ("dad","등잔 기름입니다. 밤마다 등을 돌보시니 기름이 모자라실 것 같아서요."),
            ("resident_lamplighter","……고맙습니다. 요즘은 기름도 아껴 써야 해서요."),
            ("resident_lamplighter","부인도 전에 이렇게 기름을 챙겨 주셨어요. 그때 저한테 맡기신 봉투가 하나 있었는데……."),
            ("dad","아내가 맡긴 봉투요?"),
            ("resident_lamplighter","봉투 이야기는 다음에 말씀드릴게요. 지금은 등을 마저 돌봐야 해서요.")],[],["topic:lamplighter_warning","lamplighter_trust"]),
        "herbs": ("resident_seori","해열 약초를 건넨다",lambda:"E20" not in store.room13.get("evidence",[]),[
            ("dad","해열 약초입니다. 열이 나는 환자들에게 쓰실 수 있을까 해서요."),
            ("resident_seori","마침 약초가 떨어져 가던 참이었습니다. 고맙게 받겠습니다."),
            ("resident_seori","약초를 달이는 동안 환자 곁에 있어 보시겠습니까? 열이 내리면서 환자가 어떻게 달라지는지 직접 보시는 게 낫겠군요."),
            (None,"서리와 함께 환자 곁을 지켰다. 열이 내리자 환자는 흐린 눈으로 가족의 이름을 불렀다.")],["E20"],["clinic_observation"]),
        "file": ("resident_tok","정밀 줄칼을 건넨다",lambda:"E13" not in store.room13.get("evidence",[]),[
            ("dad","정밀 줄칼입니다. 작은 핀을 손보실 때 쓰시라고요."),
            ("resident_tok","이런 귀한 걸 어떻게……. 마침 쓰던 줄칼 날이 무뎌져서 애먹던 참이에요."),
            ("resident_tok","그러고 보니 할머니 브로치 핀도 이 줄칼로 다듬었더라면 좋았을 텐데. 새로 갈아 끼운 핀의 수리 쪽지가 아직 있어요. 보시겠어요?")],["E13"],[]),
        "blanket": ("bami","두꺼운 담요를 건넨다",lambda:"E10" not in store.room13.get("evidence",[]),[
            ("dad","두꺼운 담요야. 네가 지내는 처마 밑은 밤에 많이 춥잖아."),
            ("bami","……이거 저 주시는 거예요? 아무것도 안 물어보고요?"),
            ("dad","응. 그냥 네가 따뜻하게 지냈으면 해서."),
            ("bami","그럼…… 나중에 밤에 본 거 조금 말씀드릴게요. 대신 아무한테도 제 이름은 말하지 마세요.")],[],["topic:bami_saw"]),
        "firewood": ("resident_nubi","장작 묶음을 건넨다",lambda:True,[
            ("dad","장작 묶음입니다. 아이들 있는 방부터 데우세요."),
            ("resident_nubi","세상에, 이 귀한 걸……. 고마워요. 빨래 말릴 불도 없던 참이었어요."),
            ("resident_nubi","도움이 필요하면 말해요. 빨랫감 들고 여기저기 드나드는 길은 내가 훤히 알아요.")],[],["topic:w2_laundry","nubi_trust"]),
    }
    for _key,(_npc,_title,_cond,_lines,_give,_flags) in R13_ITEM_TOPICS.items():
        ROOM13["topics"]["item:"+_key]=dict(npc=_npc,title=_title,day=[2,14],need=[],give=list(_give),flags=list(_flags),lines=list(_lines))
    ROOM13["topics"]["shop:eunho"]=dict(npc="resident_eunho",title="물건을 사고 싶습니다",day=[2,14],need=["livelihood_open"],give=[],flags=[],lines=[])

    def r13_item_owned(key):
        return key in r13_wallet(store.room13)["items"]

    _r13_shop_topics=r13_topics
    def r13_topics(person):
        rows=[]
        for key,spec in _r13_shop_topics(person):
            if key.startswith("item:"):
                item=key[5:]
                if not (r13_item_owned(item) and R13_ITEM_TOPICS[item][2]()):continue
            if key=="shop:eunho" and store.room13.get("period",0)>=2:continue
            rows.append((key,spec))
        return rows

    _r13_shop_finish_topic=r13_finish_topic
    def r13_finish_topic(key):
        _r13_shop_finish_topic(key)
        if key.startswith("item:"):
            n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n);item=key[5:]
            if item in wallet["items"]:wallet["items"].remove(item)
            wallet["used"]=list(dict.fromkeys(wallet["used"]+[item]))
            # Shared contract (docs/SHOP_RESIDENT_HELP_CONTRACT.md): an accepted gift
            # is recorded once so resident follow-up questions can read it.
            person=ROOM13["topics"][key]["npc"]
            helps=n.setdefault("resident_help",[])
            if not any(h.get("item")==item and h.get("person")==person for h in helps):
                helps.append(dict(person=person,kind="gift",item=item,day=n["day"],completed=True))
            n["livelihood"]=wallet;store.room13=n

    def r13_item_label(key,wallet):
        if key in globals().get("R13_BORROW",{}):
            return "%s(빌림 · 보증금 %d냥)"%(R13_BORROW[key]["title"],wallet.get("borrowed",{}).get(key,R13_BORROW[key]["deposit"]))
        return R13_SHOP[key]["title"] if key in R13_SHOP else key

    def r13_shop_rows():
        state=store.room13;wallet=r13_wallet(state)
        return [(key,item) for key,item in R13_SHOP.items()
            if key not in wallet["used"] and (r13_shop_on_sale(state,key) or key in wallet["items"])]

screen r13_shop(close=Return(False)):
    modal True
    zorder 95
    style_prefix "r13opt"
    default page=0
    default picked=None
    $ wallet=r13_wallet(room13)
    $ rows=r13_shop_rows()
    $ pages=max(1,(len(rows)+5)//6)
    $ page=min(page,pages-1)
    $ shown=rows[page*6:page*6+6]
    $ blocked=wallet["debt"]>R13_DEBT_LIMIT
    add Solid("#000000a8")
    add r13_close_art("resident_eunho","neutral",760):
        xpos 220 xanchor .5 ypos r13_close_y("resident_eunho",760,126,"neutral")
    text "은호 사장의 물건" xpos 450 ypos 26 size r13_read_size(28,32) color "#ebcd8a"
    text ("가진 돈 %d냥 · 갚을 돈 %d냥"%(wallet["cash"],wallet["debt"])) xpos 452 ypos 68 size r13_read_size(19,22) color ("#ffb3a3" if blocked else "#e5ece6")
    textbutton "돌아가기" xpos 1250 xanchor 1.0 ypos 24 xsize 170 action close text_size r13_read_size(22,26)
    grid 3 2:
        xpos 450 ypos 104 spacing 18
        for key,item in shown:
            button:
                xsize 256 ysize 196 padding (10,10)
                background R13ActionPanel() hover_background R13ActionPanel(True) selected_background R13ActionPanel(True)
                selected picked==key action SetScreenVariable("picked",key)
                vbox:
                    xalign .5 spacing 4
                    add R13PixelIcon(key,6) xalign .5
                    text item["title"] size r13_read_size(18,21) xalign .5 color "#fff2cf"
                    text (("가지고 있음" if key in wallet["items"] else "%d냥"%r13_shop_price(room13,key))) size r13_read_size(18,21) xalign .5 color ("#9fb0ab" if key in wallet["items"] else "#ffe39a")
        for _empty in range(6-len(shown)):
            null
    if pages>1:
        hbox:
            xpos 450+402 xanchor .5 ypos 532 spacing 20
            textbutton "‹" xsize 80 sensitive page>0 action [SetScreenVariable("page",page-1),SetScreenVariable("picked",None)] text_size 28
            text ("%d / %d"%(page+1,pages)) yalign .5 size r13_read_size(20,24)
            textbutton "›" xsize 80 sensitive page<pages-1 action [SetScreenVariable("page",page+1),SetScreenVariable("picked",None)] text_size 28
    frame:
        xpos 450 ypos 600 xsize 806 ysize 104 padding (20,12) background Solid("#14272bf0")
        if picked and picked in R13_SHOP:
            $ item=R13_SHOP[picked]
            hbox:
                spacing 16
                vbox:
                    xsize 560 spacing 4
                    text item["title"] size r13_read_size(21,24) color "#ebcd8a"
                    text item["detail"] size r13_read_size(18,21) color "#e5ece6" xsize 560
                textbutton (("가지고 있음") if picked in wallet["items"] else ("%d냥에 사기"%r13_shop_price(room13,picked))):
                    xsize 190 yalign .5
                    sensitive picked not in wallet["items"] and wallet["cash"]>=r13_shop_price(room13,picked) and not blocked
                    action [Function(r13_life_apply_purchase,picked),SetScreenVariable("picked",None)]
                    text_size r13_read_size(20,24)
        else:
            vbox:
                spacing 4 yalign .5
                text ("외상이 %d냥이다. 먼저 갚아야 물건을 살 수 있다."%wallet["debt"] if blocked else "물건을 누르면 설명이 나온다. 외상이 %d냥을 넘으면 팔지 않는다."%R13_DEBT_LIMIT) size r13_read_size(19,22) color ("#ffb3a3" if blocked else "#cfd9d4")
                if wallet["items"]:
                    text ("가진 물건 · "+", ".join(r13_item_label(k,wallet) for k in wallet["items"])) size r13_read_size(17,20) color "#ebcd8a" xsize 760
    key "game_menu" action close
