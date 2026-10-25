# 인물·자료·장면의 기존 선택 규칙과 도구함 매칭을 분리하는 어댑터.
init 995 python:
    def r13_asset_mapped_spec(spec):
        if not spec or not spec.get("file"):return spec
        mapped=dict(spec)
        mapped["file"]=r13_asset_path("file:"+spec["file"])
        return mapped

    _r13_assets_fullbody_spec=r13_fullbody_spec
    def r13_fullbody_spec(person,pose="neutral"):
        return r13_asset_mapped_spec(_r13_assets_fullbody_spec(person,pose))

    _r13_assets_close_spec=r13_close_spec
    def r13_close_spec(person,pose):
        return r13_asset_mapped_spec(_r13_assets_close_spec(person,pose))

    _r13_assets_acting_spec=r13_acting_spec
    def r13_acting_spec(person,pose):
        return r13_asset_mapped_spec(_r13_assets_acting_spec(person,pose))

    _r13_assets_dialogue_face=r13_bdialogue_face
    def r13_bdialogue_face(person,expression):
        path=_r13_assets_dialogue_face(person,expression)
        return r13_asset_path("file:"+path) if path else None

    _r13_assets_evidence_art=r13_evidence_art_path
    def r13_evidence_art_path(key):
        path=_r13_assets_evidence_art(key)
        return r13_asset_path("file:"+path) if path else None

