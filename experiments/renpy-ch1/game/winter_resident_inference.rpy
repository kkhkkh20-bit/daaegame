# Authored responses only. The cart/alibi chain in the feature proposal is NOT
# canonical case data. The initial full chain uses the existing mother's note.
default winter_disclosure_named = True

init 50 python:
    WINTER_PRESENT_DEFAULTS={
        "buri":"그건 내가 손댄 물건이 아니야. 아는 척까지 하진 않을게.",
        "nabi":"잠깐 보자. 내가 본 일은 아니네. 괜히 내 말 보태지는 마.",
        "granny":"모르는 걸 아는 것처럼 말할 순 없어요. 잘 넣어 둬요.",
        "karo":"내가 본 데까지 말할 수 있죠. 이건 직접 본 게 없어요.",
        "seryeon":"제 담당 기록은 아닙니다. 확인하지 않은 내용엔 이름을 올리지 않겠습니다.",
        "doto":"그건 왜 저한테 보여 주세요? 제가 했다는 뜻은 아니죠?",
        "bami":"가까이 대지 마. 잠깐…… 몰라. 못 봤어.",
        "guard":"지금 확인하는 건 통행입니다. 그 일까지 답할 순 없습니다.",
        "neoul":"기록은 보겠습니다. 하지만 제가 확인한 사실로 적지는 마세요.",
        "resident_nubi":"다른 분께 물어봐 주세요. 제가 잘못 말하면 안 되니까요.",
        "resident_tori":"손 멈추고 봤는데도 모르겠네요. 제가 아는 일이면 말할게요.",
        "resident_bori":"내 눈으로 본 건 아니에요. 짐 나르며 들은 말을 덧붙이진 않을게요.",
        "resident_tok":"작동하는 건 봐 드릴 수 있는데, 남의 얘긴 몰라요.",
        "resident_lamplighter":"내가 돌아본 길에서 본 건 아니구나. 더 말해 줄 건 없어.",
        "mom":"이 자료만 보고 단정하긴 어려워. 실제로 무엇과 이어지는지 더 보자.",
    }
    WINTER_SENSITIVE={
        "tracks":"조사한 수레의 동선. 운반 설명을 맡은 세련에게 보여 주면 조사 범위를 알게 됩니다.",
        "transfer_seal":"사람을 인계한 장소와 서명. 해당 담당자가 반론을 준비할 수 있습니다.",
        "mother_help":"엄마와 몰래 연락하는 방법과 도와주는 사람",
        "mother_reply":"엄마가 마을에 남아 있다는 사실과 은신처를 찾는 말",
        "research":"엄마에게 직접 받은 연구 기록",
        "witness":"누비가 사람을 옮기는 수레를 목격했다는 말",
        "map":"공개된 길과 다른 옛 통로",
        "doto_memory":"도토가 엄마를 목격했다는 말",
    }
    WINTER_TESTIMONY_SPEAKERS={"karo_account":"karo","witness":"resident_nubi","karo_memory":"karo","doto_memory":"doto","kitchen":"nabi","symptoms":"bami","lamp_log":"resident_lamplighter"}

    def winter_expose_mother(s,selected):
        n=winter_copy.deepcopy(s)
        exposed=n.setdefault("exposed_sensitive",[])
        fresh=[key for key in selected if key in ("mother_help","mother_reply","research") and key not in exposed]
        if fresh:
            exposed.extend(fresh)
            n["facts"]=[flag for flag in n["facts"] if flag!="mother_secure"]
            n=winter_flag(n,"mother_contact_compromised")
            n=winter_flag(n,"mother_traced")
        return n

    def winter_share_fact(s,recipients,fact,source):
        n=winter_copy.deepcopy(s)
        for who in recipients:
            known=n.setdefault("known_information",{}).setdefault(who,[])
            if fact not in known:known.append(fact)
        event=dict(day=s["day"],period=winter_period(s),place=s["location"],
            recipients=list(recipients),fact=fact,source=source)
        if event not in n.setdefault("information_transfers",[]):n["information_transfers"].append(event)
        return n

    def winter_disclosure_text(key,named):
        text=WINTER["evidence"][key]["text"]
        if not named and key in WINTER_TESTIMONY_SPEAKERS:
            name=WINTER_NAMES[WINTER_TESTIMONY_SPEAKERS[key]]
            text=text.replace(name,"발언자")
        return text

    def winter_private_conversation(s,who):
        listeners={row[0] for row in winter_people(s)}-{who}
        return s["location"] not in ("gate","square","post") and not listeners.intersection({"guard","neoul","seryeon"})

    def winter_person_closed(s,who):
        return s.get("resident_stance",{}).get(who)=="closed"

    def winter_note_presentation(s,who,selected,named):
        n=winter_copy.deepcopy(s)
        shown=sorted(selected)
        entry=dict(who=who,place=s["location"],day=s["day"],period=winter_period(s),evidence=shown,named=named,
            listeners=[r[0] for r in winter_people(s) if r[0]!=who])
        if entry not in n.setdefault("presentations",[]):n["presentations"].append(entry)
        known=n.setdefault("disclosed",{}).setdefault(who,[])
        for key in shown:
            disclosure=key+(":named" if named else ":names_hidden")
            if disclosure not in known:known.append(disclosure)
        return n

    def winter_prepare_response(s,who,selected,named):
        # Only the confirmed recipient knows this information. Bystanders are
        # context for authored refusals, never an implicit knowledge broadcast.
        n=winter_copy.deepcopy(s)
        if who=="seryeon" and set(selected).intersection({"tracks","witness","transfer_seal"}):
            n=winter_flag(n,"transport_counter_prepared")
            n.setdefault("prepared_responses",{}).setdefault("transport",dict(
                day=s["day"],period=winter_period(s),place=s["location"],
                evidence=list(selected),named=named,recipient=who))
        return n

    def winter_prepared_claim(s,hearing,index):
        claim=winter_copy.deepcopy(WINTER["claims"][hearing]["claims"][index])
        if winter_has(s,"transport_counter_prepared") and claim["id"] in ("transfer","destination"):
            claim["who"]="seryeon"
            claim["text"]="전에 보여 주신 안쪽 수레 동선 말씀이죠. 수리하러 들른 구간입니다. 그 뒤 사람을 어디로 보냈는지는 별개예요."
            claim["press"]="그날 보여 주신 뒤 운반 설명을 미리 맞춰 봤습니다. 안으로 갔다는 건 인정해요. 거기서 사람까지 내렸다는 기록은 있습니까?"
            claim["partial"]="안쪽으로 간 자국은 지워지지 않습니다. 다만 잠깐 수리했다는 반론이 남습니다. 사람을 내려놓도록 한 지시나 실제 인계 기록과 연결해야 합니다."
            if claim["id"]=="destination":
                claim["paths"]=[["route","order"],["route","transfer_seal"],["order","transfer_seal"]]
            claim["win"]="사람의 목적지와 내부 인계를 가리키는 기록이군요. 수레만 잠깐 수리했다는 설명으로 덮을 수 없습니다."
        return claim

    def winter_unlock_topic(s,who,key):
        n=winter_copy.deepcopy(s)
        topics=n.setdefault("new_topics",{}).setdefault(who,[])
        if key not in s["done"] and key not in topics:topics.append(key)
        return n

    def winter_finish_topic(s,who,key):
        n=winter_copy.deepcopy(s)
        n.setdefault("new_topics",{}).setdefault(who,[])
        n["new_topics"][who]=[k for k in n["new_topics"][who] if k!=key]
        return n

    def winter_resident_stance(s,who,stance):
        n=winter_copy.deepcopy(s)
        n.setdefault("resident_stance",{})[who]=stance
        return n

    def winter_shelter_supported(s):
        return winter_has(s,"registry") and (winter_has(s,"ration_public") or winter_has(s,"doto_supported") or
            (winter_has(s,"mill_helped") and winter_has(s,"meal")) or s["first_result"]=="protected")

    def winter_private_greeting(s,who):
        if winter_person_closed(s,who):return [(who,"할 말 없어. 내 가족까지 끌어들이려고 해 놓고 뭘 더 바라나.")]
        if who=="seryeon" and "mother_search" in s.get("known_information",{}).get(who,[]):
            return [(who,"너울 씨에게 편지 이야기는 들었습니다. 아내분이 여기서 보냈다는 편지 말씀이죠?"),("dad","예. 어디에 머물렀는지 알고 싶습니다."),(who,"제가 확인할 수 있는 기록부터 보겠습니다.")]
        if who=="buri" and winter_has(s,"buri_wary"):
            return [(who,"고칠 물건 아니면 나중에 와. 내 이름이 왜 궁금한데?"),(None,"부리는 서명한 종이를 뒤집고 그 위에 공구를 올렸다.")]
        if who=="resident_lamplighter" and winter_has(s,"mother_ally"):
            if winter_private_conversation(s,who):return [(who,"쪽지는 잘 감춰 뒀지? 어디서 받았는지는 말하지 말고.")]
            return [(who,"오늘은 여기 고칠 게 없네. 나중에 이야기하자."),(None,"등불지기는 내 뒤에 선 사람을 보고 말을 줄였다.")]
        if who=="nabi" and s["day"]>=10 and not winter_has(s,"fuel"):
            return [(who,"밥은 줄게. 하지만 내가 너희 편이라고 아무 데서나 말하지 마."),("dad","무슨 일이 있었습니까?"),(who,"우리 집까지 난방이 끊기면 안 돼. 애들 겨우 재워 놓고 왔어.")]
        return None

label winter_present_to_resident:
    $ winter_proof_person=winter_target_id
    $ winter_proof_keys=set(winter_selected)
    if not winter_proof_keys or not winter_proof_keys.issubset(set(winter["evidence"])):
        return
    if winter_person_closed(winter,winter_proof_person):
        call winter_lines([(winter_proof_person,"안 본다고 했어. 치워. 내 이름을 그렇게 써 놓고 또 뭘 바라나?")],"resident_closed")
        return
    $ winter=winter_note_presentation(winter,winter_proof_person,winter_selected,winter_disclosure_named)
    $ winter_prepared_before=winter_has(winter,"transport_counter_prepared")
    $ winter=winter_prepare_response(winter,winter_proof_person,winter_selected,winter_disclosure_named)
    if not winter_prepared_before and winter_has(winter,"transport_counter_prepared"):
        call winter_lines([("seryeon","안쪽 길부터 살펴보셨군요. 어느 구간을 말씀하시는지 알겠습니다."),(None,"세련은 내가 보여 준 부분만 따로 옮겨 적었다."),("dad","무엇을 적는 겁니까?"),("seryeon","다시 물으시면 담당자와 같은 내용을 보고 답해야 하니까요.")],"counter_preparation_seen")
    if winter_proof_person=="karo" and {"route","tracks"}<=winter_proof_keys:
        if winter_has(winter,"karo_hearing_ready"):
            call winter_lines([("karo","사람이 어디 내렸는지는 내가 못 봤어요. 운행 일지와 내가 지킨 마차에 대해서는 말하겠다고 했지요.")],"karo_support_recall")
        else:
            call winter_lines([("karo","자국이 안으로 갔네요. 하지만 내가 본 건 내 마차예요. 저 수레에 누가 탔는지 보증은 못 해요."),("dad","직접 본 일만 함께 확인해 주실 수 있습니까?"),("karo","그 이야기라면 해 봅시다. 어디까지 말할지 정해 두죠.")],"karo_support_opened")
            $ winter=winter_flag(winter,"karo_support_topic")
            $ winter=winter_unlock_topic(winter,"karo","karo_corroboration")
            $ renpy.notify("새 이야기 · 회의에서 함께 확인할 일")
        return
    if winter_proof_person=="buri" and "mother_note" in winter_proof_keys:
        if winter_has(winter,"buri_note_seen"):
            call winter_lines([("buri","그 메모는 봤어. 그날 물었던 일은 이야기할 수 있다고 했지. 다른 일까지 안다는 뜻은 아니야.")],"buri_note_recall")
            return
        if not winter_private_conversation(winter,"buri"):
            call winter_lines([("buri","그분 이름 여기서 꺼내지 마. 종이는 넣고, 내가 일하는 데서 얘기해."),(None,"부리는 기록을 읽다가 주위 사람들의 얼굴부터 살폈다.")],"buri_note_public")
            return
        call winter_lines([("buri","이 글씨…… 어디서 찾았어?"),("dad","아내가 남긴 겁니다. 부리 씨에게 물을 일이 있다고 적었더군요."),("buri","나한테 왔던 건 맞아. 하지만 내가 그분이랑 같이 뭘 했다는 식으로 말하진 마.")],"buri_note_opened")
        $ winter=winter_flag(winter,"buri_note_seen")
        $ winter=winter_unlock_topic(winter,"buri","buri_mother")
        $ renpy.notify("새 이야기 · 메모의 ‘역류’를 물어본다")
        return
    if winter_proof_person=="buri" and winter_proof_keys.intersection({"tracks","transfer_seal"}):
        call winter_lines([("buri","수레가 어디로 갔는지는 이걸 보고 묻는 거군. 내가 아는 건 고친 물건뿐이야. 누가 탔는지까지 내 입으로 말하길 바라진 마.")],"buri_transport_question")
        $ winter=winter_unlock_topic(winter,"buri","buri_cart")
        return
    if winter_proof_person=="resident_lamplighter" and winter_proof_keys.intersection({"mother_note","mother_repair","invitation","mother_linen"}):
        if not winter_private_conversation(winter,winter_proof_person):
            call winter_lines([("resident_lamplighter","등 고칠 일이면 밝을 때 말해. 다른 종이는 넣어 두고."),(None,"그는 편지 쪽으로 손을 뻗다 말고 내 뒤를 보았다.")],"lamp_public")
            return
        if {"invitation","mother_linen"}<=winter_proof_keys:
            if winter_has(winter,"lamp_family_confirmed"):
                call winter_lines([("resident_lamplighter","누구인지는 알아. 더 크게 꺼내 보이지 않아도 돼.")],"lamp_family_recall")
                return
            call winter_lines([("resident_lamplighter","그 단추, 아이 외투에 달아 준다더니. 두 사람이 맞구나."),("daram","엄마를 알아요?"),("resident_lamplighter","응. 따로 전하고 싶었던 말이 있어.")],"lamp_family_opened")
            $ winter=winter_flag(winter,"lamp_family_confirmed")
            $ winter=winter_unlock_topic(winter,winter_proof_person,"lamp_confidence")
            $ renpy.notify("새 이야기 · 엄마에게 전하려던 말")
            return
        if {"mother_note","mother_repair"}<=winter_proof_keys:
            call winter_lines([("resident_lamplighter","내가 점검한 곳을 묻는 거구나. 메모와 부리가 적은 말은 맞아. 어디서 무엇을 봤는지까진 말할 수 있어.")],"lamp_record_opened")
            $ winter=winter_flag(winter,"lamp_trust")
            $ winter=winter_unlock_topic(winter,winter_proof_person,"lamp_mother")
            $ renpy.notify("새 이야기 · 엄마가 보던 가로등")
            return
        call winter_lines([("resident_lamplighter","그 종이만으로 당신이 어느 쪽 사람인지 내가 어떻게 알아. 모르는 사람에게 남의 행방부터 말하지는 않아.")],"lamp_insufficient")
        return
    $ winter_sensitive_reacted=False
    if winter_proof_person in ("seryeon","guard","neoul") and winter_proof_keys.intersection({"mother_help","mother_reply","research"}):
        $ winter_sensitive_reacted=True
        if not any(key not in winter.get("exposed_sensitive",[]) for key in winter_proof_keys.intersection({"mother_help","mother_reply","research"})):
            call winter_lines([(winter_proof_person,"그 연락에 관한 기록은 확인했습니다.")],"disclosure_recall")
        else:
            call winter_lines([(winter_proof_person,"지금도 연락이 닿는다는 기록이군요. 아직 마을 안에 계시겠네요."),("dad","행방을 알려 드리려고 보여드린 건 아닙니다."),(winter_proof_person,"가족이 찾으셨다니 다행입니다. 길 안내는 저희가 하겠습니다."),(None,"그는 내가 가리키지 않은 문장까지 옮겨 적었다.")],"mother_disclosed")
            $ winter=winter_expose_mother(winter,winter_selected)
    if winter_proof_person in ("seryeon","guard") and "witness" in winter_proof_keys:
        $ winter_sensitive_reacted=True
        if winter_disclosure_named:
            if winter["witness"]=="available":
                call winter_lines([(winter_proof_person,"누비 씨 말씀이군요. 집에 가서 직접 확인하겠습니다."),("daram","이름도 알려 준 거야?"),("dad","……잠깐만요.")],"witness_disclosed")
                $ winter=winter_flag(winter,"witness_exposed")
                $ winter=dict(winter,witness="detained")
            else:
                call winter_lines([(winter_proof_person,"말씀하신 내용은 기록하겠습니다.")],"witness_disclosure_recall")
        else:
            call winter_lines([(winter_proof_person,"누가 했는지 밝히지 않는 말만으로는 움직일 수 없습니다. 무엇을 직접 확인하셨는지 보여 주세요.")],"witness_anonymous")
    if winter_sensitive_reacted:
        return
    if winter_proof_person=="nabi" and "ration_notice" in winter_proof_keys:
        call winter_lines([("nabi","여섯을 받았다는 종이가 아니야. 배정했다는 거지. 내 서명이 있는 걸 같이 볼 테야?")],"ration_opened")
        $ winter=winter_flag(winter,"ration_notice_shown")
        $ winter=winter_unlock_topic(winter,"nabi","kitchen_ration")
        $ renpy.notify("새 이야기 · 실제로 받은 곡물")
        return
    if winter_proof_person=="seryeon" and {"ration_notice","kitchen_receipt"}<=winter_proof_keys:
        call winter_lines([("seryeon","적힌 양과 받은 양이 다르군요. 바꾼 기록이 있는지 원본을 봐야겠습니다.")],"ration_order_opened")
        $ winter=winter_flag(winter,"ration_discrepancy_shown")
        $ winter=winter_unlock_topic(winter,"seryeon","delivery_diversion")
        $ renpy.notify("새 이야기 · 다른 곳으로 간 넉 자루")
        return
    call winter_lines([(winter_proof_person,WINTER_PRESENT_DEFAULTS.get(winter_proof_person,"제가 확인해 줄 수 있는 일이 아니에요."))],"resident_unrelated")
    return

label winter_buri_approach:
    call winter_lines([("buri","그분에게 답을 해 준 건 맞아. 하지만 내 이름 걸고 마을 앞에서 떠들면 나도 가만있지 않을 거야. 가족이 여기 있어.")],"buri_boundary")
    menu:
        "어떻게 이야기를 이어 갈까?"
        "엄마가 무엇을 물었는지만 확인한다":
            call winter_lines([("dad","아내가 알아보던 일을 찾는 겁니다. 부리 씨가 데려갔다고 말하려는 게 아닙니다."),("buri","……그날 질문은 내 수리표에 적어 뒀어.")],"buri_cooperates")
            $ winter=winter_resident_stance(winter,"buri","limited_cooperation")
            return True
        "실종 가담을 사람들 앞에 알리겠다고 한다":
            call winter_lines([("buri","그걸 뒷받침할 게 있어? 질문 하나 받아 줬다고 내 식구들까지 몰아넣으려는 거야?")],"buri_last_warning")
            menu:
                "부리는 문 쪽으로 몸을 돌렸다."
                "단정한 말을 거두고 물러난다":
                    call winter_lines([("dad","단정한 건 잘못입니다. 오늘은 물러나겠습니다."),("buri","그래. 일하게 내버려 둬.")],"buri_withdraw")
                    return False
                "문을 열고 부리가 엄마를 데려갔다고 외친다":
                    $ winter=winter_resident_stance(winter,"buri","closed")
                    $ winter=winter_flag(winter,"family_reported")
                    call winter_lines([("buri","경비 불러. 우리 집 이름까지 들먹이고 있어."),("daram","아빠. 우리 여관 이름 적고 있어."),(None,"부리는 종이를 거둬 서랍을 잠갔다. 문 밖의 경비가 나와 다람을 번갈아 보았다.")],"buri_reported")
                    return False
        "다른 근거를 더 찾은 뒤 돌아온다":
            return False

label winter_early_loss:
    call winter_scene("front","여관 · 문 앞의 발소리","night")
    call winter_lines([("granny","지금은 손님들 잘 시간이에요."),("guard","외지인이 주민을 협박했다는 신고입니다. 문 여세요."),("nabi","……우리 식구도 여기 있어요."),("dad","다람아, 내 손 잡아."),("daram","잡았어. 안 놓을게."),(None,"문이 열렸지만 아무도 그 앞을 막지 못했다. 두 사람의 이름이 서로 다른 종이에 적혔다.")],"early_separation")
    $ winter=dict(winter,ending="separated")
    $ persistent.winter_endings=list(set(persistent.winter_endings+["separated"]))
    $ renpy.save_persistent()
    call screen winter_end
    return

label winter_information_echo:
    $ winter=winter_flag(winter,"plaza_plan_echo_seen")
    $ winter=winter_share_fact(winter,["neoul"],"post_visit_tomorrow","resident_tori")
    call winter_lines([("neoul","내일 우편실에 가신다고요. 무슨 일로요?"),("dad","그 얘기는 어디서 들으셨습니까?"),("neoul","광장에서 길을 물으셨다면서요. 토리가 아까 알려 줬습니다."),(None,"갈 곳을 말한 건 광장에서 한 번뿐이었다."),("daram","우리가 부탁한 건 아닌데."),("neoul","눈길에서 헤매실까 봐요. 우편실 담당자에게도 전해 둘까요?")],"information_echo")
    menu:
        "너울이 대답을 기다린다."
        "길만 물었다며 방문은 비밀로 해 달라 한다":
            call winter_lines([("dad","길을 알아본 겁니다. 다른 분께는 전하지 말아 주세요."),("neoul","알겠습니다. 이미 들은 것까진 거둘 수 없겠네요.")],"echo_boundary")
        "아내가 보낸 편지를 확인하려 한다고 말한다":
            $ winter=winter_flag(winter,"mother_search_told_neoul")
            $ winter=winter_share_fact(winter,["neoul","seryeon"],"mother_search","dad_to_neoul")
            call winter_lines([("dad","아내가 여기서 편지를 보냈습니다. 어디서 보냈는지 물으려 합니다."),("neoul","그 일로 오셨군요. 세련 씨에게 편지 이야기를 전하겠습니다.")],"echo_shared")
    return

screen winter_disclosure_review(target,selected,named):
    modal True
    zorder 70
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    key "K_ESCAPE" action Return(False)
    add Solid("#0b191af8")
    add Transform(target+" avatar_neutral" if target in CAST else "assets/notebook.png",size=(100,110),fit="contain") xpos 90 ypos 35
    text (WINTER_NAMES[target]+"에게 보여 줄 내용") xpos 215 ypos 48 size 31 color "#edcf94"
    text "읽거나 취소하면 전달되지 않는다. 보여 준 뒤에도 원본은 갖고 있는다." xpos 215 ypos 98 size 19 color "#bac9c5"
    viewport:
        xpos 95 ypos 160 xsize 1090 ysize 398 mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 20
            for key in selected:
                frame:
                    xsize 1060 padding (18,16) background Solid("#243b3d")
                    vbox:
                        spacing 8
                        text WINTER["evidence"][key]["name"] size 26 color "#edcf94"
                        if key in WINTER_TESTIMONY_SPEAKERS:
                            text ("들은 말을 전달한다 · 발언자 이름도 밝힌다" if named else "들은 말을 전달한다 · 발언자 이름은 가린다") size 19 color "#bac9c5"
                        text winter_disclosure_text(key,named) size 22 xsize 995
                        if key in WINTER_SENSITIVE:
                            if key in WINTER_TESTIMONY_SPEAKERS and not named:
                                text "이름을 숨겨도 목격 내용과 내가 조사한 범위는 상대가 알게 된다." size 20 color "#f0ba85" xsize 995
                            else:
                                text ("전해지는 민감한 내용 · "+WINTER_SENSITIVE[key]) size 20 color "#f0ba85" xsize 995
    hbox:
        xpos 215 ypos 607 spacing 35
        textbutton "이 사람에게 보여주기" style "winter_button" xsize 400 action Return(True) sensitive ready
        textbutton "공개하지 않고 돌아가기" style "winter_button" xsize 400 action Return(False) sensitive ready
