# Weekly events depend on the world clock, never persistent playthrough count.
init 47 python:
    def winter_transfer_window(s):
        return (s["day"]-1)%7==1 and winter_period(s)==2

    def winter_service_open(s):
        return winter_transfer_window(s)

    def winter_cart_available(s):
        return winter_transfer_window(s) and not winter_has(s,"cart_seen:%d"%s["day"]) and not winter_has(s,"transfer_seal")

    def winter_cart_traces(s):
        return s["day"]>2 or (s["day"]==2 and (winter_period(s)>2 or winter_has(s,"cart_seen:2")))

    def winter_present_observation(s,place,key):
        rows=winter_observation_lines(s,place,key)
        absent=[who for who,text in rows if who in WINTER_SCHEDULES and winter_where(s,who)!=place]
        if not absent:return rows
        return [(None,{("square","offerings"):"작은 물건마다 번호가 달려 있다. 누가 놓았는지는 광장을 맡는 도토에게 물어봐야겠다.",
            ("post","ledger"):"장부는 덮여 있다. 담당자가 돌아오면 찾는 항목을 요청하자.",
            ("workshop","wheel"):"수리 중인 바퀴에 종이가 끼어 있다. 주인이 돌아오면 함께 확인하자."}.get((place,key),WINTER_WORLD["places"][place]["objects"][key]["text"]))]

label winter_timed_cart:
    if winter_cart_available(winter):
        $ winter=winter_flag(winter,"cart_seen:%d"%winter["day"])
        call winter_lines([(None,"천을 씌운 수레가 돌 뒤에서 멈췄다. 바퀴 밑에 받침을 넣는 경비가 보였다."),("guard","춥죠? 안쪽에 가면 따뜻합니다. 손은 천 밖으로 내밀지 마세요."),(None,"천 안에서 낮은 기침이 들렸다. 끝을 쥔 손가락이 잠깐 움직였다."),("daram","아빠, 안에 누가……"),("dad","쉿. 이쪽으로 와.")],"cart_seen")
        menu:
            "지금 무엇을 남길까?"
            "가까이 나가 어디로 가는지 묻는다":
                call winter_lines([("guard","시설 점검입니다. 아이와 물러나세요."),(None,"경비가 발밑의 종이를 주워 외투 안에 넣었다. 수레는 돌 뒤로 사라졌다."),("daram","사람이 타 있었는데."),("dad","봤다는 말만으로는 막기 어렵겠구나. 남은 자국을 보자.")],"cart_confronted")
                $ winter=winter_flag(winter,"cart_confronted")
            "몸을 숨기고 수레가 지나간 자리를 확인한다":
                call winter_lines([(None,"수레가 지나간 자리에 눌린 종이가 남았다. 눈에 젖은 가장자리만 살짝 들었다."),("daram","아빠. 도장 있어."),(None,"인계 대상 1명. 의식과 호흡 있음. 중앙 정비실 인계. 접수자 서명 아래 바퀴 자국이 겹쳐 있었다."),("dad","말려서 보관하자. 우리가 들은 소리와 따로 확인할 기록이야.")],"cart_record")
                $ winter=winter_collect(winter,"transfer_seal","cart_scene")
        $ winter=winter_flag(winter,"cart_witnessed")
    elif winter_cart_traces(winter):
        call winter_lines([(None,"수레는 없다. 돌 뒤로 꺾인 바퀴 자국은 눈에 조금 덮였다. 가장자리에는 찢긴 끈이 남아 있다."),("daram","한쪽이 유난히 깊네. 무거운 걸 실었나 봐."),("dad","이것만으로 무엇이 타 있었는지는 몰라. 길 끝과 운반 기록도 보자.")],"cart_aftermath")
        $ winter=winter_flag(winter,"cart_trace_seen")
    else:
        call winter_lines([(None,"돌 뒤 좁은 길은 눈이 고르게 쌓여 있다. 두 줄로 패인 바닥 홈만 보인다."),("daram","여긴 아무도 안 지나갔나 봐."),("dad","오늘은 아직 그런 모양이야.")],"cart_before")
    return

label winter_secret_latch:
    if winter_service_open(winter):
        call winter_lines([("daram","아빠, 이 손잡이 눌러 봐도 돼?"),(None,"배관의 떨림이 멎은 사이, 손잡이를 밀었다. 서랍 뒤 벽이 조금 벌어졌다."),("dad","뒤에 계단이 있어. 나부터 확인할게."),("daram","압력이 없어지니까 열린 건가?")],"service_open")
        $ winter=winter_flag(winter,"passage_known")
        $ winter=winter_flag(winter,"service_discovered")
        $ winter=winter_move(winter,"passage")
    else:
        call winter_lines([(None,"분류함 아래 손잡이를 눌렀다. 벽 안 배관이 떨릴 때마다 걸쇠가 바깥으로 밀렸다."),("daram","부러지는 거 아니야?"),("dad","지금은 안 열려. 압력이 걸려 있어."),(None,"작은 점검패에 ‘화요일 저녁, 광장 회수 작업 중 감압’이라고 새겨져 있다.")],"service_closed")
        $ winter=winter_flag(winter,"service_hint")
    return
