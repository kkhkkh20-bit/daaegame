init 60 python:
    # 0.20.4 (owner 2026-10-22: "첫 마차씬에서 까로가 안등장하는데 말이 나오니 좀 표시가 필요할듯"):
    # a speaker who is heard but not drawn gets a small "where from" tag next to the name ribbon.
    R13_OFFSCREEN_VOICES={("마차 안","까로"):"마부석에서"}
    def r13_offscreen_voice(who):
        return R13_OFFSCREEN_VOICES.get((getattr(store,"place",None),who),"")
