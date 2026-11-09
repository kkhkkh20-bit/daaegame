# 실제로 끝까지 들은 말만 회의의 제시 대상으로 남긴다. 자료·판정·기회는 다루지 않는다.
init 352 python:
    from collections.abc import Mapping as R13CaseHearingMapping, Sequence as R13CaseHearingSequence

    R13_CASE_HEARING_HEARD_PREFIX="hearing:heard:"
    R13_CASE_HEARING_STAGE_FIELDS=frozenset(("key","speaker","line_ids","title","press_block"))

    def r13_case_hearing_sequence(value):
        # Ren'Py의 list 이름은 RevertableList다. json.load가 반환한 기본 list도 같은 계약으로 읽는다.
        return isinstance(value,R13CaseHearingSequence) and not isinstance(value,(str,bytes,bytearray))

    def r13_case_hearing_key(key):
        if not isinstance(key,str):return None
        return key[5:] if key.startswith("v111:") else key

    def r13_case_hearing_case(values):
        return "lamp_attempt" if isinstance(values,R13CaseHearingMapping) and values.get("lamp_bound2") else "lamp"

    def r13_case_hearing_stages(data,case):
        """표시 메타의 계약만 읽는다. 같은 발언의 대상·되묻기가 모호하면 사용하지 않는다."""
        if not isinstance(data,R13CaseHearingMapping):return []
        cases=data.get("cases")
        if not isinstance(cases,R13CaseHearingMapping):return []
        part=cases.get(case)
        if not isinstance(part,R13CaseHearingMapping):return []
        stages=part.get("stages")
        if not r13_case_hearing_sequence(stages):return []
        result=[];keys=set();targets=set()
        for stage in stages:
            if not isinstance(stage,R13CaseHearingMapping) or set(stage)-R13_CASE_HEARING_STAGE_FIELDS:return []
            if not all(isinstance(stage.get(name),str) and stage[name].strip() for name in ("key","speaker","title")):return []
            key=r13_case_hearing_key(stage["key"])
            if not key or key in keys:return []
            line_ids=stage.get("line_ids")
            if not r13_case_hearing_sequence(line_ids) or not line_ids:return []
            if any(not isinstance(rid,str) or not rid.strip() for rid in line_ids):return []
            if len(set(line_ids))!=len(line_ids) or targets.intersection(line_ids):return []
            press=stage.get("press_block")
            if press is not None and (not isinstance(press,str) or not press.strip()):return []
            keys.add(key);targets.update(line_ids)
            result.append(dict(key=key,speaker=stage["speaker"],line_ids=list(line_ids),
                               title=stage["title"],press_block=press))
        return result

    def r13_case_hearing_spec_for(data,case,key):
        key=r13_case_hearing_key(key)
        return next((row for row in r13_case_hearing_stages(data,case) if row["key"]==key),None)

    def r13_case_hearing_quote_for(data,case,target,values):
        if not isinstance(target,str) or not isinstance(values,R13CaseHearingMapping):return None
        if not any(target in stage["line_ids"] for stage in r13_case_hearing_stages(data,case)):return None
        heard=values.get(R13_CASE_HEARING_HEARD_PREFIX+target)
        if not isinstance(heard,R13CaseHearingMapping):return None
        if not all(isinstance(heard.get(name),str) and heard[name].strip() for name in ("speaker","text")):return None
        # 표시 메타가 아닌 실제 발화를 반환한다. 호출자가 반환값으로 저장 상태를 바꿀 수 없다.
        return dict(speaker=heard["speaker"],text=heard["text"])

    def r13_case_hearing_rows_for(data,case,key,values):
        if r13_case_hearing_spec_for(data,case,key) is None:return []
        result=[]
        # 배열상의 미래/과거보다 실제 청취를 우선한다. 되돌아온 쟁점에서도 이미 들은 말은 다시 읽는다.
        for stage in r13_case_hearing_stages(data,case):
            for target in stage["line_ids"]:
                quote=r13_case_hearing_quote_for(data,case,target,values)
                if quote is not None:
                    result.append(dict(key=stage["key"],target=target,title=stage["title"],**quote))
        return result

    def r13_case_hearing_press_for(data,case,key,target,values):
        if r13_case_hearing_spec_for(data,case,key) is None:return None
        if r13_case_hearing_quote_for(data,case,target,values) is None:return None
        return next(stage["press_block"] for stage in r13_case_hearing_stages(data,case) if target in stage["line_ids"])

init 353 python:
    R13_CASE_HEARING_DATA={}
    if renpy.loadable("v111/case-hearing.json"):
        try:
            with renpy.file("v111/case-hearing.json") as _r13_case_hearing_file:
                R13_CASE_HEARING_DATA=json.load(_r13_case_hearing_file)
        except (ValueError,TypeError,IOError):
            # 표시 메타가 없는 구 판·불완전한 납품에서는 기존 대조 화면으로 돌아간다.
            R13_CASE_HEARING_DATA={}

    def r13_case_hearing_values():
        room=getattr(store,"room13",None)
        if not isinstance(room,R13CaseHearingMapping):return None
        v=room.get("v111")
        if not isinstance(v,R13CaseHearingMapping):return None
        values=v.get("values")
        return values if isinstance(values,R13CaseHearingMapping) else None

    def r13_case_hearing_spec(key):
        values=r13_case_hearing_values()
        if values is None:return None
        return r13_case_hearing_spec_for(R13_CASE_HEARING_DATA,r13_case_hearing_case(values),key)

    def r13_case_hearing_rows(key):
        values=r13_case_hearing_values()
        if values is None:return []
        return r13_case_hearing_rows_for(R13_CASE_HEARING_DATA,r13_case_hearing_case(values),key,values)

    def r13_case_hearing_quote(target):
        values=r13_case_hearing_values()
        if values is None:return None
        return r13_case_hearing_quote_for(R13_CASE_HEARING_DATA,r13_case_hearing_case(values),target,values)

    def r13_case_hearing_press_block(key,target):
        values=r13_case_hearing_values()
        if values is None:return None
        return r13_case_hearing_press_for(R13_CASE_HEARING_DATA,r13_case_hearing_case(values),key,target,values)

    def r13_case_hearing_heard(packet):
        """r13_lines의 실제 줄 완료 뒤에만 호출한다. 건너뛴 줄을 채워 넣지 않는다."""
        values=r13_case_hearing_values()
        if values is None or not r13_case_hearing_sequence(packet) or len(packet)<3:return False
        if not isinstance(packet[2],R13CaseHearingMapping):return False
        target=packet[2].get("line_id") or packet[2].get("source_id")
        speaker,text=packet[:2]
        if not isinstance(target,str) or not all(isinstance(value,str) and value.strip() for value in (speaker,text)):return False
        stages=r13_case_hearing_stages(R13_CASE_HEARING_DATA,r13_case_hearing_case(values))
        if not any(target in stage["line_ids"] for stage in stages):return False
        name=R13_CASE_HEARING_HEARD_PREFIX+target
        heard=dict(speaker=speaker,text=text)
        if values.get(name)==heard:return False
        room=winter_copy.deepcopy(store.room13)
        room["v111"]["values"][name]=heard
        store.room13=room
        return True
