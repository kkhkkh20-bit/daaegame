# 0.19.17 다람이와 처음 13호실에 들어온 날 (소유자 2026-10-17)
#   "첫 집방문은 쓸쓸히 서 있는 다람이 보여야 하고, 말 걸으면 '엄마가 정말 없네'라는 대사와
#    어떻게 생각하는지에 대한 선택지가 나와야 함. '오늘은 뭘 하고 있었어'는 맞지 않음."
#   첫 대화 전에는 다람이가 창가 쪽에 혼자 서 있고(그림: distressed), 말을 걸면 이 장면이 먼저 나온다.
#   고른 대답은 깃발로만 남는다(home_first_hope / home_first_doubt / home_first_rest). 진행 조건은 바꾸지 않는다.
init 187 python:
    def r13_daram_home_first_due(state=None):
        s=(store.room13 or {}) if state is None else state
        return (s.get("location")=="room13" and s.get("daram_state") in ("with_dad","rescued")
            and "lodging" in s.get("flags",[]) and s.get("case_state")=="pending"
            and "home_first_talk" not in s.get("flags",[]) and "mom_reunited" not in s.get("flags",[]))

    _r13_home_first_activity=r13_daram_home_activity
    def r13_daram_home_activity(state=None):
        if r13_daram_home_first_due(state):
            return "distressed",(1420,662,185),"창가에 혼자 서 있다"
        return _r13_home_first_activity(state)

    # 첫날에는 "오늘은 여기서 뭘 하고 있었어?"를 묻지 않는다(방금 도착했다).
    _r13_home_first_allowed=r13_daram_home_allowed
    def r13_daram_home_allowed(key,state=None):
        s=(store.room13 or {}) if state is None else state
        if key=="home:daram:rest" and s.get("day",1)<=1:return False
        return _r13_home_first_allowed(key,state)

label r13_daram_home_first:
    $ r13_speaker("daram","anxious")
    call r13_lines([(None,"다람이는 짐도 풀지 않고 창가에 혼자 서 있었다. 내가 다가가도 돌아보지 않았다."),
        ("daram","아빠……. 엄마가 정말 없네.",{"expression":"anxious"}),
        ("daram","편지에는 13호실에서 기다린다고 했잖아.",{"expression":"anxious"}),
        ("daram","아빠는 어떻게 생각해?",{"expression":"anxious"})],"home:first:open")
    menu:
        "엄마는 이 마을 어딘가에 있을 거야":
            call r13_lines([("dad","엄마 물건이 이렇게 그대로 있잖아. 멀리 간 건 아닐 거야."),
                ("daram","……정말?",{"expression":"surprise"}),
                ("dad","응. 엄마가 남긴 걸 하나씩 같이 찾아보자."),
                ("daram","응. 내가 먼저 찾을 거야.",{"expression":"joy"})],"home:first:hope")
            $ r13_flag("home_first_hope")
        "아빠도 이상해. 같이 알아보자":
            call r13_lines([("dad","아빠도 이상해. 오라고 해 놓고 왜 없을까."),
                ("daram","엄마가 우리 잊어버린 건 아니지?",{"expression":"anxious"}),
                ("dad","그럴 리 없어. 그러니까 더 알아봐야 해."),
                ("daram","……응. 나도 눈 크게 뜰게.",{"expression":"neutral"})],"home:first:doubt")
            $ r13_flag("home_first_doubt")
        "오늘은 쉬고, 엄마는 아빠가 찾을게":
            call r13_lines([("dad","먼 길 왔으니 오늘은 좀 쉬자. 엄마 찾는 건 아빠가 할게."),
                ("daram","싫어. 나도 같이 찾을 거야. 나 하나도 안 피곤해.",{"expression":"angry"}),
                ("dad","그래, 그럼 같이 하자. 대신 아빠 옆에 꼭 붙어 있어."),
                ("daram","……응. 약속.",{"expression":"flustered"})],"home:first:rest")
            $ r13_flag("home_first_rest")
    $ r13_flag("home_first_talk")
    return
