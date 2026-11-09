# 자료의 수신자와 이미 들은 답만 보고 반응을 고른다. 기록·시간·판정은 바꾸지 않는다.
init 350 python:
    def r13_inquiry_reaction_block(gate,person,shown,values):
        """정규 자료 제시가 일치하지 않은 뒤에만 쓰는, 조사 대화의 짧은 응답."""
        if not isinstance(shown,str) or not shown.startswith("V111:") or len(shown)<=5:
            return None
        known=values or {}
        key=shown[5:]
        if gate=="gate_investigate" and person=="guard":
            if key=="E03":
                # 첫 제시는 본편의 바인딩과 대사가 처리한다. 아직 인정하지 않은 것을 대신 인정하지 않는다.
                return "gate_application_repeat139" if known.get("gate_application_acknowledged") else None
            return {"E01":"gate_invitation_scope139",
                    "E02":"gate_list_repeat139",
                    "E04":"gate_rules_scope139"}.get(key,"gate_unfamiliar_record139")
        if gate in ("chorong_documents2","go_box") and person=="resident_lamplighter":
            if key=="E06":
                return "chorong_memo_repeat139" if known.get("chorong_memo_checked2") else None
            if key=="E01":
                return "chorong_invitation_repeat139" if known.get("chorong_invitation_checked2") else None
            return "chorong_unfamiliar_record139"
        return None
