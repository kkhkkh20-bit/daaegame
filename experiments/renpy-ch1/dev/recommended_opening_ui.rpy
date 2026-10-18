# Reuse only existing illustrations for the same two genuine entry documents.
init 916 python:
    r13_rec_card_people['entry_karo']='karo'
    r13_rec_card_people['family_travel']='karo'
    for new_key,old_key in (('entry_original','G1'),('entry_list','G3')):
        old_art=r13_record_icon(old_key)
        r13_rec_card_art[new_key]=dict(icon=Transform(old_art,xysize=(64,64),fit='contain',nearest=True),detail=Transform(old_art,xysize=(240,240),fit='contain',nearest=True))

label r13_recommended_carriage_opening:
    call r13_scene("winter_carriage", "1일 · 마차 안", "travel")
    call r13_lines([(None,'마차가 돌부리를 넘자 다람이가 과자 봉지를 꼭 끌어안았다.'),('daram','엄마한테 큰 거 남겨 놨어. 도착하면 바로 줄 거야.'),('dad','좋아. 여관에 가서 엄마부터 찾자.'),(None,'아빠는 아내가 보낸 편지를 다시 접었다. 여관에서 만나 함께 겨울을 보내자는, 출발 전에 받은 초대였다.'),('daram','오늘은 엄마랑 같이 자는 거지?'),('dad','그렇게 하려고 왔지. 어디서 기다리는지 먼저 확인하자.'),('karo','지붕이 보입니다. 발판이 얼었으니 내릴 때 조심해요.')], "recommended:day1:carriage")
    call r13_scene("winter", "1일 · 눈에 막힌 입구", "calm")
    call r13_lines([(None,'까로가 두 사람의 짐을 내려놓고 바퀴 축을 살폈다.'),('karo','축에 금이 갔네요. 이대로는 다시 손님을 태울 수 없어요.'),('dad','짐을 먼저 내려 두면 될까요?'),('karo','제가 지킬 테니 저 초소에서 방문 확인부터 받아 오세요.'),('daram','아빠, 같이 가자.')], "recommended:day1:arrival")
    return

label r13_recommended_entry_present:
    $ r13_rec_entry_selected = []
    while len(r13_rec_entry_selected)<2:
        call screen r13_recommended_cards("메인 수첩에서 같은 날짜의 원본과 돌목이 보여 준 목록을 골라 보자.")
        if _return is None:
            return False
        if _return not in ("entry_original","entry_list"):
            call r13_lines([('guard','함께 오셨다는 말은 들었습니다. 하지만 목록에 옮겨 적은 인원수를 고치려면 원본과 나란히 봐야 합니다.')], "recommended:day1:wrong-card")
        elif _return in r13_rec_entry_selected:
            call r13_lines([('dad','이건 이미 꺼냈어. 다르게 적힌 다른 쪽도 같이 보자.')], "recommended:day1:duplicate-card")
        else:
            $ r13_rec_entry_selected.append(_return)
    if not r13_rec_opening_present(r13_recommended,r13_rec_entry_selected):
        return False
    call r13_lines([('dad','같은 날짜, 같은 제 이름이에요. 원본에는 동행 한 명, 모두 두 명이라고 되어 있네요.'),('daram','그 한 명이 나야. 아빠랑 같이 왔으니까!'),('guard','제가 옮겨 적으면서 동행 칸을 빠뜨렸군요. 미안합니다.'),(None,'돌목이 두 사람 앞에서 목록을 고치고 초소 옆 길을 열었다.'),('guard','이제 함께 들어가십시오.'),('dad','다람아, 손 잡자. 여관으로 가자.')], "recommended:day1:access-cleared")
    return True
