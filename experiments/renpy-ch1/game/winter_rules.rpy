# Pure, copy-on-write rules. Screens never spend time or decide endings.
init 40 python:
    import copy as winter_copy
    WINTER = json.load(renpy.file("winter-story.json"))

    def winter_new():
        return dict(version=1,day=1,ap=3,location="inn",evidence=[],facts=[],done=[],
            records={},log=[],witness="available",mother_day=None,marks=[],ending=None,
            first_result=None,second_result=None)

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
        if n["ap"]<a["cost"]: return n
        n["ap"]-=a["cost"]
        n["done"].append(key)
        for e in a["give"]:
            if e not in n["evidence"]: n["evidence"].append(e)
            n["records"][e]=dict(day=n["day"],source=key,place=a["place"])
        for f in a["flags"]:
            if f not in n["facts"]: n["facts"].append(f)
        if key in ("protect","rescue"): n["witness"]="safe"
        if key=="mother":
            n["mother_day"]=n["day"]
            n["facts"].append("mother_secure" if winter_has(n,"timing") else "mother_traced")
        n["log"].append(dict(day=n["day"],action=key,cost=a["cost"]))
        return n

    def winter_flag(s,key):
        n=winter_copy.deepcopy(s)
        if key not in n["facts"]:n["facts"].append(key)
        return n

    def winter_move(s,location):
        n=winter_copy.deepcopy(s)
        if location in WINTER["places"] and (location!="passage" or winter_has(s,"map")):
            n["location"]=location
        return n

    def winter_next_day(s):
        n=winter_copy.deepcopy(s)
        if n["day"]>=10:return n
        n["day"]+=1
        n["ap"]=3
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
        if whole and family and prepared and s["witness"]=="safe" and winter_has(s,"permission") and s["mother_day"]<=7:
            return "truth"
        if family and winter_has(s,"escape"):return "family"
        if {"frame","destination"}.issubset(proven):return "exposure"
        if winter_has(s,"escape"):return "flight"
        return "separated"

    def winter_missing(s):
        checks=[("엄마와 접촉",winter_has(s,"mother")),("엄마의 은신처 보호",winter_has(s,"mother_secure")),
            ("7일 안에 엄마와 합류",s["mother_day"] is not None and s["mother_day"]<=7),
            ("누비와 가족 보호·공개 증언 허락",s["witness"]=="safe" and winter_has(s,"permission")),
            ("비상 운용과 공동 난방",winter_has(s,"repair") and winter_has(s,"fuel")),
            ("보행 탈출로",winter_has(s,"escape")),
            ("최종 네 주장 입증",all(k in s["marks"] for k in ("frame","destination","power","death")))]
        return [name for name,ok in checks if not ok]
