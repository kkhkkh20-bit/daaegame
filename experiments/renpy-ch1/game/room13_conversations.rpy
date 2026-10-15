# Authored question wording and ordinary early-game conversations. Topic IDs,
# existing dialogue packets, evidence, conditions and time costs stay intact.
init 70 python:
    R13_CONVERSATION_TITLES = {
        "register":"저희가 묵을 방이 있습니까?",
        "granny_letter":"제게 편지를 보내신 이유를 여쭤도 될까요?",
        "granny_rules":"밤에는 안쪽 문도 잠그십니까?",
        "karo_road":"돌아가는 마차는 언제 탈 수 있습니까?",
        "karo_parcel":"제 앞으로 되돌아온 물건이 있다고요?",
        "owl_glove":"어르신, 거기서 무엇을 보고 계십니까?",
        "owl_mother":"이 편지에 적힌 손님을 아십니까?",
        "buri_work":"저희가 타고 온 마차를 봐주실 수 있습니까?",
        "buri_consent":"할아버지에 관해 어떤 말이 돌고 있습니까?",
        "buri_records":"할아버지가 남기신 일을 들려주시겠습니까?",
        "nabi_food":"나비야, 내가 도울 일 있어?",
        "nabi_alibi":"그날 식당에서는 무슨 일이 있었어?",
        "nabi_gap":"공구를 가지러 간 뒤에도 할머니를 봤어?",
        "doto_corridor":"문이 열릴 때까지 무슨 일이 있었니?",
        "bami_boundary":"밤이야, 거기서는 어디까지 보였니?",
        "bami_saw":"촛대가 떨어진 뒤에는 무엇을 봤니?",
        "tok_pin":"이 핀의 이음매를 확인해 주시겠습니까?",
        "tok_repair":"지금 고치는 핀은 어디에 쓰는 겁니까?",
        "lamplighter_guarded":"등에 문제가 있습니까?",
        "lamplighter_warning":"아내가 맡긴 편지가 있습니까?",
        "neoul_custody":"아이를 언제 만날 수 있습니까?",
        "seryeon_mail":"아내 앞으로 온 편지를 확인할 수 있습니까?",
        "w2_contact":"아내에게 연락을 전해 주시겠습니까?",
        "w2_lamps":"등을 점검할 때 누가 따라옵니까?",
        "w2_doctor":"지금도 상태가 나아지는 환자가 있습니까?",
        "w2_erased":"이 경과 기록은 왜 지워졌습니까?",
        "w2_school":"비어 있는 교실을 쓸 수 있습니까?",
        "w2_eunho":"쌓아 둔 식량과 장작을 나눌 수 있습니까?",
        "w2_supply_receipt":"남겨 둘 몫도 이 장부에 적으면 되겠습니까?",
        "w2_buri_ops":"장치를 멈추면 누가 남아야 합니까?",
        "w2_bori":"대피할 짐을 옮겨 주실 수 있습니까?",
        "w2_nubi":"세탁물이 들어가는 곳을 여쭤도 되겠습니까?",
        "w2_laundry":"세탁물을 들일 때 무엇을 조심해야 합니까?",
        "w2_stay_order":"이 명령은 누구를 대상으로 합니까?",
        "w2_maintenance":"바깥 점검문으로 들어갈 수 있습니까?",
        "w2_route":"고개 말고 다른 길은 없습니까?",
        "w2_prevented_plan":"그날 아이를 따로 받으라는 쪽지가 왔습니까?",
        "w2_mom_past":"왜 직접 나타나지 못했어?",
        "w2_mom_stone":"돌은 원래 무엇이었어?",
        "w2_mom_plan":"그냥 끄면 안 돼?",
        "seori_case":"그날 진료 기록에는 무엇을 남겼습니까?",
        "seori_previous":"전날 들어온 진료 요청은 어떤 내용이었습니까?",
        "life:nabi:changed":"접수대도 네가 보고 있어?",
        "life:resident_bori:changed":"식구들이 쉴 자리는 확인하셨습니까?",
        "life:resident_teacher:changed":"대피소 준비는 어디까지 됐습니까?",
        "life:resident_tori:changed":"할머니께 돌려드릴 물건은 어떻게 하셨습니까?",
        "life:resident_tori:repair":"그 부품을 누가 수리했는지 아십니까?",
        "life:resident_librarian:dated":"이 장부에서 더 확인할 줄이 있습니까?",
        "life:resident_ubak:measurement":"다시 측정할 때는 무엇을 비교해야 합니까?",
        "life:resident_guseul:receipt":"이 수량은 네가 직접 확인한 것과 같니?",
        "life:resident_nero:privacy":"이 연락 기록을 함께 봐주시겠습니까?",
    }

    # Each row contains three individually authored titles, not a generic
    # suffix/question-mark conversion: ordinary work, days 5–7, later crisis.
    # Aligned with upstream dialogue revision b55ba61: Doto observes a new
    # ledger before asking, and later questions follow the rewritten replies.
    R13_LIFE_QUESTION_WORDING = {
        "resident_tori":("제가 천을 잡아 드릴까요?","납품할 때 어려운 일은 없습니까?","지금 천을 나눌 때 무엇을 챙겨야 합니까?"),
        "resident_bori":("그 짐은 혼자 옮기십니까?","장작을 옮기는 일은 괜찮으십니까?","다른 집 일을 맡기 전에 무엇부터 해야 합니까?"),
        "resident_yeoni":("옷 수선도 맡길 수 있습니까?","요즘 납품 일은 괜찮습니까?","납품하러 가는 분들을 어떻게 도와야 합니까?"),
        "nabi":("이 그릇도 치울까?","밥을 못 챙겨 먹는 사람도 있어?","밥을 나눌 때 누구부터 살펴야 할까?"),
        "buri":("버릴 부품도 따로 보관하십니까?","수리 일이 많이 밀렸습니까?","수리 말고도 맡아야 할 일이 생겼습니까?"),
        "resident_kongi":("이 근처 길을 잘 아니?","요즘도 빵 배달을 하니?","먹을 것은 잘 챙기고 있니?"),
        "doto":("새 장부를 쓰는 거니?","장부를 고치는 일은 어떠니?","지금 기록을 남길 때 뭐가 제일 어렵니?"),
        "resident_kkwak":("강에서 물을 길으셨습니까?","요즘 쓸 물은 충분합니까?","물 나르는 일 말고도 부탁을 받으십니까?"),
        "granny":("손님이 많습니까?","오늘 밤 밖에 머물러도 괜찮겠습니까?","오늘 밤은 어떻게 지내야 하겠습니까?"),
        "resident_librarian":("책을 빌릴 수 있습니까?","땔감으로 쓸 종이를 구할 수 있습니까?","원본과 베낀 것은 어디에 둡니까?"),
        "resident_owlgp":("아직도 기록을 하십니까?","어르신 말씀도 함께 확인해도 되겠습니까?","앞으로 기록은 어떻게 맞춰 보면 좋겠습니까?"),
        "resident_teacher":("수업은 계속합니까?","학교에서 환자도 받을 수 있습니까?","더 머물 사람을 받아도 되겠습니까?"),
        "karo":("축을 갈면 출발할 수 있습니까?","마차가 못 가면 어떻게 해야 합니까?","걸어서 갈 길도 살펴봐 주시겠습니까?"),
        "resident_nero":("그 이름표는 버리지 않으십니까?","배식에서 빠지는 사람은 없습니까?","목록에 없는 사람들도 챙길 수 있을까요?"),
        "resident_seol":("정해진 때에 치는 종입니까?","종소리를 헷갈리는 사람도 있습니까?","오늘 종이 울리면 어떻게 움직여야 합니까?"),
        "resident_ppul":("나눠 줄 식량은 얼마나 남았습니까?","오늘 밤 머물 곳은 충분합니까?","불을 줄이면 사람들은 어디서 쉬어야 합니까?"),
        "resident_tok":("다 같은 부품입니까?","급하게 고쳐 달라는 부탁이 많습니까?","수리를 맡기면 무엇부터 확인해야 합니까?"),
        "bami":("여기서 자니?","밤이야, 쉴 곳은 괜찮니?","네가 쉴 곳은 무엇부터 확인할까?"),
        "resident_sling":("받을 사람이 없으면 어떻게 합니까?","요즘 편지 배달은 잘됩니까?","배달하지 못한 편지는 어떻게 합니까?"),
        "resident_momo":("쓸 수 있는 물건도 보관합니까?","그 그림을 함께 맞춰 봐도 됩니까?","옛 장치를 쓰기 전에 무엇을 확인해야 합니까?"),
        "resident_ttadak":("벽이 비뚤어졌습니까?","건물을 고치는 일은 잘됩니까?","급히 고칠 집이 많습니까?"),
        "resident_piko":("그림을 봐도 됩니까?","요즘 그림을 그리기는 어떠십니까?","지금 마음에 드는 색은 무엇입니까?"),
        "resident_mungchi":("무거운 쪽을 옮겨 줄까?","옮긴 상자는 다 확인했니?","옮겨 놓은 물건은 어디까지 확인할 수 있니?"),
        "resident_madam":("물자를 나눠 쓰는 중입니까?","물건을 가져갈 때 어떻게 기록합니까?","물자를 꺼내 쓰려면 무엇부터 정해야 합니까?"),
        "resident_siluk":("눈길에서도 수레를 끌 수 있습니까?","짐을 싣기 전에 확인할 수 있습니까?","앞으로 맡을 짐은 어떻게 확인하시겠습니까?"),
        "neoul":("문을 지키는 이유가 뭡니까?","실제로 따른 명령도 기록에 남아 있습니까?","확인하신 일에 이름을 남겨 주시겠습니까?"),
        "resident_musoe":("밖으로 나가는 길입니까?","지금 마을에서 무엇이 가장 걱정되십니까?","솜이에게 일을 부탁할 때 무엇을 조심해야 합니까?"),
        "resident_somi":("어디 다녀왔니?","요즘도 어른들이 심부름을 시키니?","솜아, 지금 무엇이 제일 걱정이니?"),
        "resident_seori":("확인한 사람의 이름까지 남깁니까?","검사원님의 기록도 다시 봐도 되겠습니까?","기록을 바로잡는 일은 어떻습니까?"),
        "resident_ubak":("측정할 때마다 숫자가 다릅니까?","요즘 측정 결과는 어떻습니까?","다르게 나온 수치도 보여 주시겠습니까?"),
        "resident_nubi":("빨래 묶음마다 표가 다른 이유가 있습니까?","가족들이 지내는 곳은 괜찮습니까?","일을 부탁드리기 전에 무엇부터 마련할까요?"),
        "resident_eunho":("가격을 바꾸셨습니까?","창고를 여는 일이 걱정되십니까?","물자를 함께 쓰려면 어떤 약속이 필요합니까?"),
        "resident_guseul":("도장만 있어도 물건을 내주니?","네가 직접 확인한 물량은 얼마나 되니?","수량을 확인할 때 누구한테 물어야 하니?"),
        "resident_badook":("밤에도 혼자 다닙니까?","대피할 때도 통행 명령을 확인합니까?","순찰할 때 가장 먼저 챙길 것은 무엇입니까?"),
        "resident_lamplighter":("등마다 밝기가 다른 이유가 있습니까?","요즘 마음에 걸리는 일이 있습니까?","연락을 맡긴 분들은 어떻게 지켜야 합니까?"),
    }
    for r13_person,r13_titles in R13_LIFE_QUESTION_WORDING.items():
        for r13_suffix,r13_title in zip(("work","after","crisis"),r13_titles):
            R13_CONVERSATION_TITLES["life:"+r13_person+":"+r13_suffix]=r13_title
    for r13_key,r13_title in R13_CONVERSATION_TITLES.items():
        if r13_key in ROOM13["topics"]:
            r13_old_topic=dict(ROOM13["topics"][r13_key])
            r13_old_topic["title"]=r13_title
            ROOM13["topics"][r13_key]=r13_old_topic

    # First-week small talk grounded in the public work/activity descriptions.
    # No hidden biography, new case facts, evidence, flags or time advancement.
    # The few callbacks require a topic actually read in this save, not a
    # persistent memory or a merely unlocked evidence topic.
    R13_EARLY_CONVERSATIONS = [
        ("kkwak_ice","resident_kkwak","물통이 얼면 어떻게 비우십니까?",[
            ("resident_kkwak","얼음은 가장자리부터 조금씩 떼요. 통까지 깨뜨리면 물을 길어 와도 담을 데가 없잖아요."),
            ("dad","급하다고 세게 두드려서 될 일은 아니군요."),
            ("resident_kkwak","그래서 통이 비어 있을 때부터 미리 살피는 거예요. 물이 가득 찬 다음에는 손대기 더 어렵고요.")],None),
        ("kkwak_tracks","resident_kkwak","발자국만 보고 따라가면 안 되겠군요.",[
            ("resident_kkwak","네. 아까도 말씀드렸지만, 발자국이 갔다가 돌아온 자국까지 봐야 해요."),
            ("dad","아이에게도 남의 발자국을 무작정 따라가지 말라고 하겠습니다."),
            ("resident_kkwak","길을 모르면 물어보세요. 아예 안 가는 게 나은 날도 있으니까요.")],"life:resident_kkwak:work"),
        ("bori_bundle","resident_bori","장작 묶음은 어떻게 나누십니까?",[
            ("resident_bori","길이가 비슷한 것끼리 묶어요. 긴 게 하나 삐져나오면 옆 사람 옷을 잡아당기거든요."),
            ("dad","매듭만 단단하게 묶으면 되는 줄 알았습니다."),
            ("resident_bori","직접 들어 봐야 알아요. 한쪽으로 쏠리면 묶은 자리부터 다시 보고요.")],None),
        ("bori_home","resident_bori","집의 불도 보러 가셔야 한다고 했죠?",[
            ("resident_bori","네. 밖에서 바쁜 건 저만이 아니에요. 집에서도 식구들이 저를 기다리고 있어요."),
            ("dad","부탁할 일이 생기면 언제 돌아가셔야 하는지부터 여쭙겠습니다."),
            ("resident_bori","그렇게만 해 주세요. 붙잡아 놓고 금방 끝난다는 말씀은 하지 마시고요.")],"life:resident_bori:work"),
        ("nero_tag","resident_nero","이름표를 떼면 짐이 섞이지 않습니까?",[
            ("resident_nero","짐이랑 짐표를 같이 외워 둬요. 짐표를 아무나 읽게 매달아 두는 건 싫어서요."),
            ("dad","제가 짐을 찾아 드릴 일이 생기면 먼저 여쭙겠습니다."),
            ("resident_nero","네. 사람들 앞에서 큰 소리로 이름부터 부르지는 말고요.")],None),
        ("siluk_cart","resident_siluk","짐을 싣기 전에 바퀴부터 보십니까?",[
            ("resident_siluk","눈부터 털어야 어디에 걸렸는지 보여요. 힘으로 당기면 실은 짐부터 쏟아지고요."),
            ("dad","뒤에서 밀기 전에 먼저 물어보는 편이 낫겠군요."),
            ("resident_siluk","그렇죠. 제가 멈춘 데는 다 이유가 있으니까.")],None),
        ("tori_stitches","resident_tori","바느질을 마치면 무엇부터 확인합니까?",[
            ("resident_tori","접히는 부분을 봐요. 펼쳐 놨을 땐 멀쩡해도, 접으면 실이 당겨질 수 있거든요."),
            ("dad","실제로 쓰는 모양대로 접어서 다시 보시는군요."),
            ("resident_tori","네. 받는 분이 직접 한 번 써 보고 알려 주시면 더 좋고요.")],None),
        ("tori_count","resident_tori","받은 천의 수량도 적어 두신다고요?",[
            ("resident_tori","받은 것하고 돌려드린 것, 둘 다 세어 둬요. 나중에 모자란다고 하면 헷갈리니까."),
            ("dad","제가 물건을 맡길 때도 같이 세겠습니다."),
            ("resident_tori","그럼 좋죠. 다 끝난 뒤에 기억을 더듬어 맞춰 보는 것보다 훨씬 쉬워요.")],"life:resident_tori:work"),
        ("yeoni_seam","resident_yeoni","수선을 맡기기 전에 준비할 것이 있습니까?",[
            ("resident_yeoni","옷은 말려서 가져오세요. 입을 때 어디가 불편한지도 알려 주시고요."),
            ("dad","뜯어진 곳만 보여 드리면 되는 줄 알았습니다."),
            ("resident_yeoni","입을 때 계속 당기는 곳이면 꿰매 놓기만 해도 금방 또 터지거든요.")],None),
        ("kongi_basket","resident_kongi","바구니는 어디를 잡아 주면 되니?",[
            ("resident_kongi","빵 밑을 받쳐 주세요. 위에서 누르면 빵이 더 납작해져요."),
            ("dad","알았어. 빵 들기 전에 먼저 말할게."),
            ("resident_kongi","네. 말없이 갑자기 가져가면 제가 떨어뜨린 줄 알잖아요.")],None),
        ("ttadak_wood","resident_ttadak","보수할 나무는 어떻게 고르십니까?",[
            ("resident_ttadak","판이 들어갈 자리를 먼저 봐요. 남는 판부터 고르면 결국 또 깎아야 하니까."),
            ("dad","빈틈이 작아도 메우려면 손이 많이 가는군요."),
            ("resident_ttadak","겉에서만 작아 보일 수도 있죠. 직접 대 보기 전에는 다 됐다고 못 해요.")],None),
        ("ttadak_plan","resident_ttadak","말씀하신 대로 도면부터 봐야겠군요.",[
            ("resident_ttadak","네. 어디를 고쳤는지도 같이 적어 오세요. 오래된 도면만 들고 오시면 지금 집과 안 맞을 수 있어요."),
            ("dad","보이는 벽만 재서 대충 짐작하지는 않겠습니다."),
            ("resident_ttadak","그럼 괜히 벽을 뜯었다가 다시 막을 일은 줄겠네요.")],"life:resident_ttadak:work"),
        ("tok_parts","resident_tok","작은 부품은 어떻게 구분해 두십니까?",[
            ("resident_tok","물건은 꺼낸 순서대로 놓아요. 비슷하다고 한데 모으면 다시 찾느라 더 걸려요."),
            ("dad","치워 드린답시고 함부로 건드리면 안 되겠군요."),
            ("resident_tok","치울 게 있으면 말만 해 주세요. 비울 자리는 제가 알려 드릴게요.")],None),
        ("lamplighter_check","resident_lamplighter","점검을 마치면 바로 자리를 옮기십니까?",[
            ("resident_lamplighter","등을 조금 더 지켜보고 가요. 손을 댔을 때만 괜찮은 건 고친 게 아니니까."),
            ("dad","불이 켜지는 순간만 확인해서는 안 되겠군요."),
            ("resident_lamplighter","네. 멀리서 봐도 불빛 밝기가 고른지까지 보고요.")],None),
        ("piko_cloth","resident_piko","그림에는 왜 천을 덮어 두십니까?",[
            ("resident_piko","천을 덮어 두면 먼지도 막고, 아직 보여 드릴 준비가 안 된 그림도 가리고요."),
            ("dad","허락 없이 그림에 덮인 천을 걷지는 않겠습니다."),
            ("resident_piko","고마워요. 그림이 완성됐는지는 그리는 사람에게 먼저 물어봐 주세요.")],None),
        ("seol_rope","resident_seol","종을 울리기 전에 끈을 다시 매십니까?",[
            ("resident_seol","매듭이 손에 걸리는 데가 없는지 봐요. 급할 때 잡아당겼는데 풀리면 곤란하니까."),
            ("dad","종이 안 울릴 때도 살필 일이 있군요."),
            ("resident_seol","종소리를 낼 때만 제 일이 시작되는 건 아니에요.")],None),
    ]
    for r13_suffix,r13_person,r13_title,r13_replies,r13_read_after in R13_EARLY_CONVERSATIONS:
        r13_key="smalltalk:"+r13_suffix
        ROOM13["topics"][r13_key]=dict(npc=r13_person,title=r13_title,
            lines=[("dad",r13_title)]+list(r13_replies),day=[1,4],need=[],
            flags=[],give=[],cost=0,read_after=[r13_read_after] if r13_read_after else [])

    r13_conversation_base_available=r13_available
    def r13_available(spec):
        # Existing specs have no read_after field, so retain their availability
        # exactly. All existing callers still use the same eligibility function.
        return r13_conversation_base_available(spec) and all(
            key in store.room13.get("read_topics",[])
            for key in spec.get("read_after",[]))
