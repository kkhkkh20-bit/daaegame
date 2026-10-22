# Background speakers borrow an existing resident's dialogue art (owner 2026-10-22: "배경 인물은
# 일단 1번을 써보고 너무 이상하면 2번으로"). These residents have no lines in the current story,
# so their faces do not stand for someone else in the same scene. New art can replace any row.
init 59 python:
    R13_EXTRA_FACES={
        "v111_resident":"resident_mungchi",       # 주민
        "v111_child":"kid_kkam",                  # 아이
        "v111_patrol":"resident_kalbaram",        # 순찰대원
        "v111_lower_resident":"resident_solbang", # 아랫길 주민
        "v111_siluk_child":"kid_siluk1",          # 실룩의 아이
        "ms14_clinician":"resident_eunho",        # 진료 담당자
        "ms14_attendant":"resident_jongjong",     # 종업원
        "kid_nubi3":"kid_nubi2",                  # 누비의 막내
    }
    for _extra,_source in R13_EXTRA_FACES.items():
        _people=R13_FULLBODY.get("people",{})
        if _extra not in _people and _source in _people:_people[_extra]=_people[_source]
        # The close-up only draws people in the cast table; borrow that row as well.
        if _extra not in CAST and _source in CAST:CAST[_extra]=CAST[_source]
