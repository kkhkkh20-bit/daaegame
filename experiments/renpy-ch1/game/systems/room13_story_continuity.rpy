# 0.18.90 이야기 앞뒤 맞추기
# - 에피소드에서 죽은 주민은 그 뒤 마을에 나오지 않는다(초롱·따닥·무쇠는 각 에피소드 파일이 이미 처리).
# - 회의에서 죽은 사람의 자리와 말은 같은 일을 하던 사람이 대신한다(바둑이 → 경비).
# - 증언자가 죽은 뒤에 그 사람이 남긴 기록으로 같은 사실을 보이는 경우(따닥의 증축 기록)는
#   R13_DEBATE의 broken_if(room13_debate.rpy r13_debate_judge)가 다른 줄을 고른다.
init 162 python:
    R13_DEATH_FLAGS = {
        "resident_piko":"piko_dead",
        "resident_librarian":"librarian_dead",
        "resident_nero":"nero_dead",
        "resident_teacher":"teacher_dead",
        "resident_badook":"badook_dead",
        "resident_guldol":"guldol_dead",
        "resident_momo":"momo_dead",
        "resident_siluk":"siluk_dead",
    }

    _r13_continuity_where=r13_where
    def r13_where(person):
        flag=R13_DEATH_FLAGS.get(person)
        if flag and store.room13 and r13_has(flag):return None
        return _r13_continuity_where(person)

    # 회의에서만: 죽은 사람의 발언을 같은 일을 하던 사람이 잇는다.
    R13_DEAD_STAND_IN = {"resident_badook":("badook_dead","guard")}

    def r13_dead_stand_in(who):
        spec=R13_DEAD_STAND_IN.get(who)
        return spec[1] if spec and store.room13 and r13_has(spec[0]) else who

    # 0.19.15: 엄마와 다시 만나지 못한 판에서는 ⑤·⑥ 회의에 엄마가 없다(엄마는 14일 제단에서 처음 나타난다).
    # 엄마 자리는 비우고, 엄마의 말은 그 자리에 있던 사람이 자기가 본 것만으로 한다.
    R13_MOM_ABSENT_SESSIONS = ("ep5","ep6")
    R13_MOM_ABSENT_LINES = {
        "오늘 밤부터 데워져요. 아이들은…… 안 죽어도 됐어요.":
            ("resident_seori","등이 전부 밝아졌어요. 돌이 다시 데워진 겁니다. 아이들은…… 안 죽어도 됐어요."),
        "(아빠를 본다) ……여기 사람들이 수레가 어디로 가는지 알아야 해.":
            ("resident_bori","(너울을 노려본다) ……그 수레, 대체 어디로 가는 건데."),
        "이건 마을의 죽은 사람 명단이에요. 여기 모과 할멈. 작년에 보호소로 간 분이죠. 죽은 사람 칸에 있어요.":
            ("dad","이건 마을의 죽은 사람 명단입니다. 여기 모과 할멈. 작년에 보호소로 간 분이지요. 죽은 사람 칸에 있습니다."),
        "어젯밤, 아무도 바치지 않았어요. 옛 시설에 남은 조각을 모아 큰 돌을 데웠어요. 등이 밝아진 거, 다 보셨죠.":
            ("dad","어젯밤, 아무도 바치지 않았습니다. 그런데 광장 등이 전부 밝아졌습니다. 다 보셨지요."),
        "어쩔 수 있어요. 어젯밤에 했잖아요.":
            ("resident_bori","뭘 어쩔 수 없어. 어젯밤 아무도 안 바쳤는데 등이 밝아졌잖아."),
    }

    def r13_mom_absent():
        return bool(store.room13) and not r13_has("mom_reunited")

    def r13_dead_stand_in_packet(packet,identity):
        if not identity.startswith(("debate:","meeting:")) or not packet:return packet
        if packet[0]=="mom" and r13_mom_absent() and packet[1] in R13_MOM_ABSENT_LINES:
            return R13_MOM_ABSENT_LINES[packet[1]]+tuple(packet[2:])
        who=r13_dead_stand_in(packet[0])
        return packet if who==packet[0] else (who,)+tuple(packet[1:])

    # 자리표도 같은 사람으로 바꾼다. 어느 층의 r13_debate_seats가 답하든 마지막에 적용된다.
    _r13_continuity_seats=r13_debate_seats
    def r13_debate_seats(session):
        out=[];seen=set()
        for who,step in _r13_continuity_seats(session):
            who=r13_dead_stand_in(who)
            if who=="mom" and session in R13_MOM_ABSENT_SESSIONS and r13_mom_absent():continue
            if who not in seen:
                seen.add(who);out.append((who,step))
        return out

    # 따닥이 9일 새벽에 죽었다면, 10일 재판에서는 톡이 따닥의 증축 기록을 읽는다.
    for _st in R13_DEBATE["C1"]["statements"]:
        if "H7" in _st.get("accept",[]):
            _st.setdefault("broken_if",{})["H7"]=("ttadak_dead",[
                ("resident_tok","따닥이 남긴 증축 기록이에요. 벽 안에 옛 통로가 그려져 있고, 13호 책장 뒤로 이어진다고 그 녀석 글씨로 적혀 있어요."),
                ("resident_tok","그 녀석은 자기가 본 걸 늘 적어 뒀어요. 남는 게 모자라는 것보다 낫다고요."),
                ("seryeon","……13호에 문 말고 다른 길이 있었다고요?")])
