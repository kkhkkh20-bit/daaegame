# Work and goods in person (owner, 0.18.56): "일거리를 위에 보여주면 안 돼. 상점이든 직접 가야 해.
# 일거리도 마을을 돌아다니면서 찾게 해." The top board is gone. Each job is a question for the
# person who gives it, at the place where the work is done; goods stay with 은호 사장 at the
# 공동 물품 창고 (moves to the 장터 once that place has its art, docs/ART_REQUEST_01854_PLACES.md).
# The money ledger and shared-work notes stay readable from 메뉴 › 생활 장부.
init 133 python:
    for _r13_job_key,_r13_job in R13_JOBS.items():
        ROOM13["topics"]["job:"+_r13_job_key]=dict(npc=_r13_job["npc"],
            title="일손을 돕겠습니다 · %s (%d냥)"%(_r13_job["title"],_r13_job["pay"]),
            day=[2,14],need=["livelihood_open"],give=[],flags=[],lines=[])
        R13_TOPIC_LABELS["job:"+_r13_job_key]="r13_job_from_talk"

    _r13_direct_work_topics=r13_topics
    def r13_topics(person):
        rows=[]
        for key,spec in _r13_direct_work_topics(person):
            if key.startswith("job:"):
                job=key[4:]
                if not r13_work_available(job) or store.room13.get("location")!=R13_JOBS[job]["place"]:continue
            rows.append((key,spec))
        return rows

label r13_job_from_talk:
    call r13_livelihood_run(r13_topic[4:])
    return "roam"
