# 0.18.91 B안 · 사건 중심 시간 (소유자 2026-10-17)
# - 평소엔 이벤트가 있어야 시간이 흐른다(대화·이동은 공짜, 일거리는 없앴다).
# - 사건이 열리면 목표 줄에 "회의까지 남은 칸"과 "반박할 수 있는 말"을 보인다(시간대 4칸: 오전·오후·저녁·늦은 저녁).
# - 자료가 다 모이면 회의를 미리 열 수 있는 곳(③ 6일 저녁 학교)은 그렇게 알려 준다. 빨리 풀면 남은 칸으로 다른 일을 한다.
init 169 python:
    # (회의, 열린 표식, 끝난 표식, 마감 (날, 마지막 칸), 회의 이름, 미리 열 수 있는 때 (날, 칸, 장소 이름) 또는 None)
    R13_MEETING_CLOCK = [
        ("Q1","lt_dawn","lt_done",(4,1),"광장 회의",None),
        ("Q3","wf_fire","wf_done",(7,1),"학교 회의",(6,2,"학교")),
    ]

    def r13_meeting_countdown():
        s=store.room13 or {}
        now=s.get("day",1)*4+s.get("period",0)
        rows=[]
        for claim,opened,done,(dd,dp),name,early in R13_MEETING_CLOCK:
            if not r13_has(opened) or r13_has(done):continue
            left=dd*4+dp-now+1
            if left<=0:continue
            sts=r13_debate_statements(claim)
            ready=sum(1 for st in sts if not st.get("truth") and r13_debate_answerable(claim,st))
            need=sum(1 for st in sts if not st.get("truth"))
            text="%s까지 %d칸 · 반박할 수 있는 말 %d/%d"%(name,left,ready,need)
            if early and ready==need and now<early[0]*4+4:  # 0.19.8: not after that evening has passed
                text+=" · %d일 저녁 %s에서 미리 열 수 있다"%(early[0],early[2])
            if claim=="Q1":
                text="광장 회의 · 4일 오전부터 오후까지 · 조사 마감까지 %d칸"%left
            rows.append((left,text))
        return min(rows)[1] if rows else None

    _r13_time_campaign_goal=r13_campaign_goal
    def r13_campaign_goal():
        return r13_meeting_countdown() or _r13_time_campaign_goal()
