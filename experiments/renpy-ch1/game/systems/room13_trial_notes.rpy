# After the trial (or the prevention hearing): three lines per claim in the investigation notes
# (owner, 0.18.19). 확인한 사실 / 입증하지 못한 부분 / 그 결과.
# Never names a record, where it is found, or where to go next.
init 121 python:
    R13_TRIAL_NOTE_TEXT={
        "C1":dict(title="잠긴 방에는 아이만 있었다",
            ok=("13호에는 정문 말고도 드나들 길이 있었다.","그 길을 그날 누가 지났는지는 이것만으로 알 수 없다.","잠긴 방에 아이만 있었다는 주장은 무너졌다."),
            no=("정문은 안에서 잠겨 있었다.","정문 말고 다른 길이 그날 쓰일 수 있었는지는 확인하지 못했다.","잠긴 방에는 아이만 있었다는 주장이 남았다.")),
        "C2":dict(title="아이가 친 촛대 때문에 죽었다",
            ok=("다람이가 친 팔의 상처와 목숨을 앗아 간 머리의 상처는 따로 생겼다.","머리를 친 사람이 누구인지는 이 논점만으로 정해지지 않는다.","다람이가 죽였다는 주장은 받아들여지지 않았다."),
            no=("다람이는 할아버지의 팔을 촛대로 쳤다.","그 뒤에 따로 생긴 상처가 있었다는 것은 확인하지 못했다.","다람이가 죽였다는 주장이 남았다.")),
        "C3":dict(title="할머니는 그때 식당에 있었다",
            ok=("할머니가 나비와 함께 있던 것은 첫 비명 때까지였다.","비어 있던 시간에 할머니가 실제로 어디로 갔는지는 아직 모른다.","할머니의 식당 알리바이는 첫 비명 때까지로 줄었다."),
            no=("첫 비명 때 할머니는 나비와 함께 있었다.","그 이후에도 함께 있었다는 것은 확인하지 못했다.","할머니의 이동에 관한 주장은 남았다.")),
        "C4":dict(title="들어갔다 해도 도우려 했을 뿐이다",
            ok=("구조 전에 할머니가 촛대와 어르신에게 닿았다는 흔적이 서로 맞았다.","할머니는 아직 자기 입으로 그날 일을 말하지 않았다.","도우려 했을 뿐이라는 말은 받아들여지지 않았다."),
            no=("할머니는 도우려 했을 뿐이라고 말했다.","구조 전에 할머니가 어르신에게 손을 댔다는 것은 확인하지 못했다.","도우려 했을 뿐이라는 말이 남았다.")),
    }

    def r13_record_trial_notes(prevention=False):
        s=store.room13;rows=[]
        if prevention:
            rows.append(dict(title="회의 · 아이를 따로 맡아 달라는 요청",
                fact="아빠와 딸이 함께 들어왔다는 기록은 인정됐다.",
                question="누가 왜 아이를 떼어 놓으려 했는지는 입증하지 못했다.",
                result="부녀는 함께 지낸다. 그날 밤 무슨 일이 계획됐는지는 기록에 없다."))
        else:
            props=set(s.get("propositions",[]))
            for claim in ("C1","C2","C3","C4"):
                t=R13_TRIAL_NOTE_TEXT[claim]
                fact,gap,result=t["ok"] if claim in props else t["no"]
                # 0.18.35: a claim closed with some statements broken keeps what was broken.
                if claim not in props and claim in R13_DEBATE:
                    sts=[st for st in r13_debate_statements(claim) if not st.get("truth") and not r13_debate_skipped(claim,st)]
                    done=[st for st in sts if r13_debate_is_broken(claim,st["id"])]
                    left=[st for st in sts if not r13_debate_is_broken(claim,st["id"])]
                    if done and left:
                        fact="‘%s’ 부분은 반박했다."%r13_debate_emphasis(done[-1])
                        gap="‘%s’ 부분은 뒤집지 못했다."%r13_debate_emphasis(left[0])
                if claim=="C4" and claim in props and r13_has("c4_unenforced"):
                    result="판결은 났지만 촌장이 집행하지 않았다."
                rows.append(dict(title="재판 · "+t["title"],fact=fact,question=gap,result=result))
        n=winter_copy.deepcopy(s);n["trial_notes"]=rows;store.room13=n

    _r13_tn_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        rows=_r13_tn_notes()
        notes=(store.room13 or {}).get("trial_notes")
        if notes:
            rows=list(rows)+[dict(n,keys=[],hint="") for n in notes]
        return rows
