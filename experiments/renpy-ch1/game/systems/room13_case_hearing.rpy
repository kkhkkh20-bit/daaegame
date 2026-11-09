# 실제로 끝까지 들은 말만 회의의 제시 대상으로 남긴다. 자료·판정·기회는 다루지 않는다.
# 기존 화재 연결판 안에서 저장했던 판도 이 새 임시 값으로 재개한다.
default v111_hearing_only = False
init 352 python:
    from collections.abc import Mapping as R13CaseHearingMapping, Sequence as R13CaseHearingSequence

    R13_CASE_HEARING_HEARD_PREFIX="hearing:heard:"
    R13_CASE_HEARING_STAGE_FIELDS=frozenset(("key","speaker","line_ids","title","press_block","kind","latest_only"))
    R13_CASE_HEARING_FILES=("v111/case-hearing.json","v111/case-hearing-early.json",
                            "v111/case-hearing-mid.json","v111/case-hearing-late.json",
                            "v111/case-hearing-ending.json")

    def r13_case_hearing_sequence(value):
        # Ren'Py의 list 이름은 RevertableList다. json.load가 반환한 기본 list도 같은 계약으로 읽는다.
        return isinstance(value,R13CaseHearingSequence) and not isinstance(value,(str,bytes,bytearray))

    def r13_case_hearing_key(key):
        if not isinstance(key,str):return None
        return key[5:] if key.startswith("v111:") else key

    def r13_case_hearing_legacy_case(values):
        return "lamp_attempt" if isinstance(values,R13CaseHearingMapping) and values.get("lamp_bound2") else "lamp"

    def r13_case_hearing_case(values):
        # 기존 3일차 전용 호출의 계약은 남긴다. 전체 사건 조회는 key로 사건을 찾는다.
        return r13_case_hearing_legacy_case(values)

    def r13_case_hearing_merge(sources):
        """누락/손상된 파일은 건너뛰고, 여러 파일이 같은 사건을 정의하면 그 사건은 제외한다."""
        cases={};conflicts=set()
        for source in sources:
            if not isinstance(source,R13CaseHearingMapping):continue
            parts=source.get("cases")
            if not isinstance(parts,R13CaseHearingMapping):continue
            for case,part in parts.items():
                if not isinstance(case,str) or not case.strip():continue
                if case in cases or case in conflicts:
                    cases.pop(case,None);conflicts.add(case)
                else:
                    cases[case]=part
        return dict(cases=cases,conflicts=sorted(conflicts))

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
            kind=stage.get("kind","statement")
            if kind not in ("statement","question"):return []
            latest_only=stage.get("latest_only",False)
            if not isinstance(latest_only,bool):return []
            keys.add(key);targets.update(line_ids)
            result.append(dict(key=key,speaker=stage["speaker"],line_ids=list(line_ids),
                               title=stage["title"],press_block=press,kind=kind,latest_only=latest_only))
        return result

    def r13_case_hearing_eligible_cases(data,values):
        if not isinstance(data,R13CaseHearingMapping):return []
        cases=data.get("cases")
        if not isinstance(cases,R13CaseHearingMapping):return []
        return [case for case in cases if r13_case_hearing_case_enabled(data,case,values)
                and r13_case_hearing_stages(data,case)]

    def r13_case_hearing_case_enabled(data,case,values):
        if not isinstance(case,str) or not case.strip() or not isinstance(data,R13CaseHearingMapping):return False
        cases=data.get("cases")
        if not isinstance(cases,R13CaseHearingMapping) or not isinstance(cases.get(case),R13CaseHearingMapping):return False
        if case in ("lamp","lamp_attempt") and case!=r13_case_hearing_legacy_case(values):return False
        return r13_case_hearing_when(cases[case].get("when"),values)

    def r13_case_hearing_when(when,values):
        """실제 분기값만 읽는다. 미설정은 None으로 비교하고 조건을 실행 코드로 해석하지 않는다."""
        if when is None:return True
        if not isinstance(when,R13CaseHearingMapping):return False
        fields=set(when)
        if fields not in ({"key","equals"},{"key","not_equals"}):return False
        if not isinstance(when.get("key"),str) or not when["key"].strip():return False
        op="equals" if "equals" in when else "not_equals"
        expected=when[op]
        if expected is not None and not isinstance(expected,(str,bool,int,float)):return False
        actual=values.get(when["key"]) if isinstance(values,R13CaseHearingMapping) else None
        return (actual==expected) if op=="equals" else (actual!=expected)

    def r13_case_hearing_case_for(data,key,values):
        """쟁점 이름이 적격한 한 사건에만 속할 때만 선택한다. 다른 사건의 발언은 합치지 않는다."""
        key=r13_case_hearing_key(key)
        if not key:return None
        cases=[case for case in r13_case_hearing_eligible_cases(data,values)
               if r13_case_hearing_spec_for(data,case,key) is not None]
        return cases[0] if len(cases)==1 else None

    def r13_case_hearing_spec_for(data,case,key):
        key=r13_case_hearing_key(key)
        return next((row for row in r13_case_hearing_stages(data,case) if row["key"]==key),None)

    def r13_case_hearing_quote_for(data,case,target,values):
        if not isinstance(target,str) or not isinstance(values,R13CaseHearingMapping):return None
        if not r13_case_hearing_case_enabled(data,case,values):return None
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
            rows=[]
            for target in stage["line_ids"]:
                quote=r13_case_hearing_quote_for(data,case,target,values)
                if quote is not None:
                    rows.append(dict(key=stage["key"],target=target,title=stage["title"],kind=stage["kind"],**quote))
            # 수정된 발언은 실제로 끝까지 들은 뒤에만 이전 인용을 대신한다. 과거 캐시는 지우지 않는다.
            result.extend(rows[-1:] if stage["latest_only"] else rows)
        return result

    def r13_case_hearing_press_for(data,case,key,target,values):
        if r13_case_hearing_spec_for(data,case,key) is None:return None
        if r13_case_hearing_quote_for(data,case,target,values) is None:return None
        return next(stage["press_block"] for stage in r13_case_hearing_stages(data,case) if target in stage["line_ids"])

init 353 python:
    _r13_case_hearing_sources=[]
    for _r13_case_hearing_path in R13_CASE_HEARING_FILES:
        if not renpy.loadable(_r13_case_hearing_path):continue
        try:
            with renpy.file(_r13_case_hearing_path) as _r13_case_hearing_file:
                _r13_case_hearing_sources.append(json.load(_r13_case_hearing_file))
        except (ValueError,TypeError,IOError):
            # 표시 메타가 없는 구 판·불완전한 납품에서는 기존 대조 화면으로 돌아간다.
            pass
    R13_CASE_HEARING_DATA=r13_case_hearing_merge(_r13_case_hearing_sources)
    # 표시 메타는 init 뒤 불변이다. 일반 대사의 완료 훅은 사건 전체를 다시 읽지 않고 거른다.
    R13_CASE_HEARING_REGISTERED_TARGETS=frozenset(target
        for case in R13_CASE_HEARING_DATA["cases"]
        for stage in r13_case_hearing_stages(R13_CASE_HEARING_DATA,case)
        for target in stage["line_ids"])

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
        case=r13_case_hearing_case_for(R13_CASE_HEARING_DATA,key,values)
        return r13_case_hearing_spec_for(R13_CASE_HEARING_DATA,case,key) if case else None

    def r13_case_hearing_rows(key):
        values=r13_case_hearing_values()
        if values is None:return []
        case=r13_case_hearing_case_for(R13_CASE_HEARING_DATA,key,values)
        return r13_case_hearing_rows_for(R13_CASE_HEARING_DATA,case,key,values) if case else []

    def r13_case_hearing_quote(target):
        values=r13_case_hearing_values()
        if values is None:return None
        for case in r13_case_hearing_eligible_cases(R13_CASE_HEARING_DATA,values):
            quote=r13_case_hearing_quote_for(R13_CASE_HEARING_DATA,case,target,values)
            if quote is not None:return quote
        return None

    def r13_case_hearing_press_block(key,target):
        values=r13_case_hearing_values()
        if values is None:return None
        case=r13_case_hearing_case_for(R13_CASE_HEARING_DATA,key,values)
        return r13_case_hearing_press_for(R13_CASE_HEARING_DATA,case,key,target,values) if case else None

    def r13_case_hearing_heard(packet):
        """r13_lines의 실제 줄 완료 뒤에만 호출한다. 건너뛴 줄을 채워 넣지 않는다."""
        if not r13_case_hearing_sequence(packet) or len(packet)<3:return False
        if not isinstance(packet[2],R13CaseHearingMapping):return False
        candidates=[target for target in (packet[2].get("line_id"),packet[2].get("source_id"))
                    if isinstance(target,str) and target in R13_CASE_HEARING_REGISTERED_TARGETS]
        if not candidates:return False
        values=r13_case_hearing_values()
        if values is None:return False
        speaker,text=packet[:2]
        if not all(isinstance(value,str) and value.strip() for value in (speaker,text)):return False
        # 호출 직전 v111_claim은 이전 사건일 수도 있다. 완료한 실제 RID가 등록된 적격 사건만 확인한다.
        registered={target for case in r13_case_hearing_eligible_cases(R13_CASE_HEARING_DATA,values)
                    for stage in r13_case_hearing_stages(R13_CASE_HEARING_DATA,case) for target in stage["line_ids"]}
        targets=[]
        for target in candidates:
            if target in registered and target not in targets:targets.append(target)
        heard=dict(speaker=speaker,text=text)
        changed=[R13_CASE_HEARING_HEARD_PREFIX+target for target in targets
                 if values.get(R13_CASE_HEARING_HEARD_PREFIX+target)!=heard]
        if not changed:return False
        room=winter_copy.deepcopy(store.room13)
        for name in changed:room["v111"]["values"][name]=dict(heard)
        store.room13=room
        return True
