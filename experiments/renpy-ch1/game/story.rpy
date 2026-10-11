# A bounded engine trial, not the approved final rewrite of chapter one.
label start:
    $ inventory = []
    $ inspected = []
    $ stage = "intro"
    $ meeting_first = None
    $ meeting_proved = False
    $ wrong_attempts = 0
    $ conclusion_attempts = 0
    $ test_complete = False
    $ place, clock_text = "마차 안", "해 질 무렵"
    show screen hud
    scene black
    play music "assets/travel.mp3" fadein 0.3
    $ renpy.pause(0.3, hard=True)
    scene bg carriage with Dissolve(0.25)
    daram "아빠. 주머니 좀 봐."
    dad "또 부스러기야?"
    daram "비상식량이야. 여관 밥이 맛없으면 아빠 것도 줄게."
    dad "내 주머니에 넣었으면서?"
    daram "둘이 나눠 들면 덜 무겁잖아."
    scene bg approach with fade
    $ place = "마을로 들어가는 길"
    daram "불 켜진 집이 있어. 저기가 여관인가?"
    dad "가서 물어보자."
    window hide
    scene black with Dissolve(0.2)
    stop music fadeout 0.2
    $ place, clock_text, stage = "열세 번째 침대", "다음 날 아침", "conflict"
    play music "assets/search.mp3" fadein 0.3
    $ renpy.pause(0.3, hard=True)
    scene bg room with Dissolve(0.25)
    show granny distressed at close_left
    show seryeon neutral at close_right
    seryeon "제 주머니가 할머니 베개 밑에서 나왔어요. 이래도 모르신다고요?"
    granny "그걸 내가 넣었다는 건 아니지."
    seryeon "그럼 이 방에 누가 있었는지 말씀하세요."
    granny "…그 이름은 못 말해."
    dad "물건부터 살펴봐도 되겠습니까?"
    granny "이불은 들춰도 돼. 함부로 잡아당기지만 마."
    hide granny
    hide seryeon
    show daram thinking at close_right
    daram "아빠, 베개만 보지 말고. 아래도 뭔가 있어."
    dad "손 넣지 말고, 내가 볼게."
    hide daram
    $ stage = "investigation"
    jump investigation

label investigation:
    window hide
    scene bg room
    call screen investigate
    $ target = _return
    if target == "meeting":
        jump council_entry
    elif target == "pouch":
        scene cg pouch with dissolve
        if "pouch" not in inventory:
            daram "별 끝이 접혔네. 도장을 잘못 찍었나?"
            dad "도장 자체가 닳은 거야. 같은 자국이 있는지 보자."
            $ acquire("pouch")
            $ inspected.append("pouch")
        else:
            dad "봉인은 그대로다. 접힌 별 끝도 보인다."
    elif target == "fur":
        stop music fadeout 0.2
        scene black with Dissolve(0.15)
        $ renpy.pause(0.3, hard=True)
        scene cg somsom with Dissolve(0.35)
        if "fur" not in inventory:
            daram "…움직였어. 수염."
            dad "그래. 숨 쉬고 있어."
            daram "털에 빨간 게 묻었는데… 별 같아."
            dad "닦지 말자. 먼저 자국을 남겨두자."
            $ acquire("fur")
            $ inspected.append("fur")
        else:
            dad "붉은 자국은 털 위에 있다. 솜솜이는 숨 쉬고 있다."
        play music "assets/search.mp3" fadein 0.3
        $ renpy.pause(0.3, hard=True)
    elif target == "flour":
        if "flour" not in inventory:
            show daram neutral at close_right
            daram "이불에도 손자국이 있어. 이것도 빨간색… 아, 하얀색이네."
            dad "밀가루다. 따로 기억해두자."
            $ acquire("flour")
            $ inspected.append("flour")
            hide daram
        else:
            dad "이불을 정리한 흔적이다. 붉은 도장과는 다르다."
    jump investigation

label council_entry:
    window hide
    scene black with Dissolve(0.2)
    stop music fadeout 0.2
    play music "assets/meeting.mp3" fadein 0.3
    $ renpy.pause(0.3, hard=True)
    $ place, clock_text, stage = "여관 식당", "아침 회의", "meeting"
    scene bg council with Dissolve(0.3)
    show seryeon neutral at close_right
    show granny neutral at close_left
    seryeon "쥐는 처음 봅니다. 제 주머니하고는 아무 관계도 없어요."
    daram "아무 관계도?"
    seryeon "그 얘기로 시간을 끌지 마세요. 돈이 없어진 건 제 쪽이니까."
    hide granny
    jump present_first

label present_first:
    window hide
    call screen testimony
    if _return == "press":
        seryeon "그 작은 쥐에 제 물건이 닿을 이유가 없다고요."
        jump present_first
    elif _return == "flour":
        $ wrong_attempts += 1
        dad "이불을 만진 흔적입니다. 주머니와의 관계를 보여주지는 못하겠군요."
        jump present_first
    $ meeting_first = _return
    if meeting_first == "pouch":
        dad "이 도장입니다. 별 끝이 접혀 있죠."
        seryeon "제 주머니에 제 도장이 있는 게 이상합니까?"
        daram "다른 데도 같은 게 있잖아."
    else:
        dad "솜솜의 털에 붉은 자국이 남았습니다."
        seryeon "빨간 얼룩이면 다 제 탓인가요?"
        daram "모양까지 봐야지."
    $ stage = "comparison"
    jump present_second

label present_second:
    window hide
    call screen testimony
    if _return == "press":
        seryeon "비슷하다는 말만으로 몰아붙이지 마세요."
        jump present_second
    elif _return == "flour":
        $ wrong_attempts += 1
        dad "흰 밀가루 자국으로 붉은 도장의 모양을 설명할 수는 없습니다."
        jump present_second
    elif _return == meeting_first:
        dad "같은 물건을 다시 봐도 비교는 안 된다. 다른 쪽을 보자."
        jump present_second
    $ meeting_proved = True
    show seryeon thinking at close_right
    dad "털에는 반대로 찍혔습니다. 접힌 별 끝까지 같아요."
    seryeon "…다른 주머니일 수도 있죠."
    daram "그 주머니 도장도 똑같이 닳았다는 거야?"
    dad "이 자국을 부정하려면, 먼저 그 물건을 보여주셔야 합니다."
    $ stage = "conclusion"
    jump choose_conclusion

label choose_conclusion:
    menu:
        "지금 증거로 확실히 말할 수 있는 것은?"
        "세련이 돈을 훔쳤다":
            $ conclusion_attempts += 1
            dad "접촉한 흔적만으로 돈을 가져간 사람까지 정할 수는 없다."
            jump choose_conclusion
        "주머니의 도장이 솜솜의 털에 닿았다":
            pass
        "솜솜이가 죽었다":
            $ conclusion_attempts += 1
            daram "아빠, 아까 숨 쉬는 거 같이 봤잖아."
            jump choose_conclusion
    show seryeon distressed at close_right
    dad "관계가 없다는 말씀은 맞지 않습니다. 이제 그 주머니가 어떻게 닿았는지 확인하죠."
    seryeon "…그건 제가 옮긴 게 아닙니다."
    daram "그럼 누가 옮겼는지는 아직 모르는 거네."
    dad "그래. 여기서부터 다시 확인하는 거야."
    hide seryeon
    $ stage = "complete"
    $ test_complete = True
    window hide
    call screen trial_complete
    return
