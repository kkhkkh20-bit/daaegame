# 임시(공개 전 삭제): 날짜·시간대·장소별로 생활 일정이 세우는 인물과 자세를 json 으로 쏟는다.
init 999 python:
    def qa_stage_dump():
        import json
        out=[]
        days=[1,2,3,4,5,7,9,10,12,14]
        for day in days:
            for period in (0,1,2):
                for location in R13_WORLD_LAYOUTS:
                    state=dict(day=day,period=period,location=location)
                    if day>=4:state.update(case_state="occurred")
                    if day>=8:state.update(trial_ended=True,week2_started=True)
                    try:
                        r13_admin_apply(state,["entry_corrected","lodging","livelihood_open"] if day>=2 else [],["E01","E02","M01","E03"] if day>=2 else [],fresh=True)
                        rows=[dict(person=a.get("person"),pose=a.get("pose"),x=int(a["rect"][0]+a["rect"][2]/2),foot=int(a["rect"][1]+a["rect"][3]),w=int(a["rect"][2]),h=int(a["rect"][3]),slot=str(a.get("slot") or a.get("contact") or "")) for a in r13_stage_people()]
                    except Exception as e:
                        rows=[dict(error=str(e)[:120])]
                    out.append(dict(day=day,period=period,location=location,people=rows))
        with open("/tmp/claude-0/stage_dump.json","w") as f:json.dump(out,f,ensure_ascii=False,indent=1)
        return len(out)

testcase stage_dump:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (qa_stage_dump()>0)
