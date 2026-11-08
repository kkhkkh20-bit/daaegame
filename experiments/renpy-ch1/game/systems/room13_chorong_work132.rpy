# 끈을 입에 문 작업 원화는 실제 그 끈을 잡아 달라는 한 대사에서만 고른다.
# 그 밖의 듣기·안내·조사 대화는 일반 평상 표정으로 돌아간다.
init 391 python:
    R13_CHORONG_WORK_RECORD132="MS14_D02_S01_L0011"
    _r13_chorong_work132_line=r13_v111_line
    def r13_v111_line(rid):
        packet=_r13_chorong_work132_line(rid)
        if rid!=R13_CHORONG_WORK_RECORD132 or packet[0]!="resident_lamplighter":
            return packet
        return (packet[0],packet[1],dict(packet[2],pose="lamp_work132"))

    # 연기 정규화와 화자 렌더 모두 원화가 등록된 이 자세를 그대로 통과시킨다.
    _r13_chorong_work132_authored=r13_fullbody_authored_pose
    def r13_fullbody_authored_pose(person,pose):
        if person=="resident_lamplighter" and pose=="lamp_work132" and r13_dialogue_pose_source(person,pose):
            return True
        return _r13_chorong_work132_authored(person,pose)
