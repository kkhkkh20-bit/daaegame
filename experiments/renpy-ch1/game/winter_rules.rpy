# Pure, copy-on-write rules. Screens never spend time or decide endings.
init 40 python:
    import copy as winter_copy
    WINTER = json.load(renpy.file("winter-story.json"))

    def winter_new():
        return dict(version=4,day=1,period=0,location="inn",evidence=[],facts=[],done=[],
            records={},log=[],witness="available",mother_day=None,marks=[],ending=None,
            first_result=None,second_result=None)

    def winter_period(s):
        # ap is read only for saves written before the calendar migration.
        return max(0,min(3,s.get("period",3-s.get("ap",3))))

    def winter_period_name(s):
        return ("오전","오후","저녁","저녁 일정 마침")[winter_period(s)]

    def winter_weekday(s):
        return ("월","화","수","목","금","토","일")[(s["day"]-1)%7]

    def winter_clock(s):
        return "%d일째 (%s) · %s"%(s["day"],winter_weekday(s),winter_period_name(s))

    def winter_upgrade(s):
        n=winter_copy.deepcopy(s)
        if n.get("version",1)<2 and "inn_registered" not in n["facts"]:
            n["facts"].append("inn_registered")
        if n.get("version",1)<4 and "inn_registered" in n["facts"] and "entry_corrected" not in n["facts"]:
            n["facts"].append("entry_corrected")
        n["period"]=winter_period(n)
        n.pop("ap",None)
        n["version"]=4
        return n

    def winter_time_target(s):
        return ("오후","저녁","저녁 일정 마침","저녁 일정 마침")[winter_period(s)]

    def winter_wait(s):
        n=winter_copy.deepcopy(s)
        if winter_period(n)<3:
            before=winter_period(n)
            n["period"]=before+1
            n["log"].append(dict(day=n["day"],action="wait",cost=1,period=before))
        return n

    def winter_can_act(s,key):
        return winter_visible(s,key) and (WINTER["actions"][key]["cost"]==0 or winter_period(s)<3)

    def winter_has(s,key):
        return key in s["evidence"] or key in s["facts"]

    def winter_visible(s,key):
        a=WINTER["actions"][key]
        if key in s["done"]: return False
        if not a["start"]<=s["day"]<=a["end"]: return False
        if not all(winter_has(s,k) for k in a["need"]): return False
        if key in ("witness","protect") and s["witness"]!="available": return False
        if key=="rescue" and s["witness"]!="detained": return False
        if key=="relocate" and winter_has(s,"mother_secure"): return False
        return True

    def winter_options(s):
        return [k for k,a in WINTER["actions"].items() if a["place"]==s["location"] and winter_visible(s,k)]

    def winter_apply(s,key,choice=None):
        n=winter_copy.deepcopy(s)
        if not winter_visible(s,key): return n
        a=WINTER["actions"][key]
        if not winter_can_act(s,key): return n
        before=winter_period(n)
        n["period"]=before+a["cost"]
        n["done"].append(key)
        for e in a["give"]:
            if e not in n["evidence"]: n["evidence"].append(e)
            n["records"][e]=dict(day=n["day"],period=before,source=key,place=n["location"])
        for f in a["flags"]:
            if f not in n["facts"]: n["facts"].append(f)
        if key in ("protect","rescue"): n["witness"]="safe"
        if key=="mother":
            n["mother_day"]=n["day"]
            n["facts"].append("mother_secure" if winter_has(n,"timing") else "mother_traced")
        if all(k in n["evidence"] for k in ("karo_memory","doto_memory")) and "sightings" not in n["evidence"]:
            n["evidence"].append("sightings")
            n["records"]["sightings"]=dict(day=n["day"],period=before,source="two_witnesses",place=n["location"])
        n["log"].append(dict(day=n["day"],period=before,action=key,cost=a["cost"]))
        return n

    def winter_flag(s,key):
        n=winter_copy.deepcopy(s)
        if key not in n["facts"]:n["facts"].append(key)
        return n

    def winter_move(s,location):
        n=winter_copy.deepcopy(s)
        if location in WINTER["places"] and (location!="passage" or winter_has(s,"map") or winter_has(s,"passage_known")):
            n["location"]=location
        return n

    def winter_next_day(s):
        n=winter_copy.deepcopy(s)
        if n["day"]>=14:return n
        n["day"]+=1
        n["period"]=0
        n.pop("ap",None)
        n["location"]="inn"
        if n["day"]==6 and n["witness"]=="available":n["witness"]="detained"
        if n["day"]==8 and n["witness"]=="detained":n["witness"]="dead"
        return n

    def winter_proves(s,claim,selected):
        held=set(selected)
        if not held.issubset(set(s["evidence"])):return False
        return any(set(path).issubset(held) for path in claim["paths"])

    def winter_mark(s,key):
        n=winter_copy.deepcopy(s)
        if key not in n["marks"]:n["marks"].append(key)
        return n

    def winter_ending(s):
        proven=set(s["marks"])
        whole={"frame","destination","power","death"}.issubset(proven)
        family=winter_has(s,"mother") and winter_has(s,"mother_secure")
        prepared=all(winter_has(s,k) for k in ("repair","fuel","escape"))
        if s.get("version",3)>=4:
            prepared=prepared and s.get("records",{}).get("repair",{}).get("day",99)<=11
        if whole and family and prepared and s["witness"]=="safe" and winter_has(s,"permission") and s["mother_day"]<=11:
            return "truth"
        if family and winter_has(s,"escape"):return "family"
        if {"frame","destination"}.issubset(proven):return "exposure"
        if winter_has(s,"escape"):return "flight"
        return "separated"

    def winter_missing(s):
        checks=[("엄마와 접촉",winter_has(s,"mother")),("엄마의 은신처 보호",winter_has(s,"mother_secure")),
            ("엄마와 함께 밤의 측정을 준비할 시간 확보",s["mother_day"] is not None and s["mother_day"]<=11),
            ("누비와 가족 보호·공개 증언 허락",s["witness"]=="safe" and winter_has(s,"permission")),
            ("밤별 측정을 마친 비상 운용과 공동 난방",winter_has(s,"repair") and winter_has(s,"fuel") and (s.get("version",3)<4 or s.get("records",{}).get("repair",{}).get("day",99)<=11)),
            ("보행 탈출로",winter_has(s,"escape")),
            ("최종 네 주장 입증",all(k in s["marks"] for k in ("frame","destination","power","death")))]
        return [name for name,ok in checks if not ok]
