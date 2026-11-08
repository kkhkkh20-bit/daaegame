# 책상에서 읽은 편지의 원문과 끝 그림을 실제 읽기 크기로 보여 준다.
# 내용·정답·자료 획득은 변경하지 않는다.
init 356 python:
    import re as _r13_room_document_re
    def r13_room_document_original(key):
        record=r13_catalog_record(key)
        body=r13_material_body(record) if record else ""
        if key not in ("V111:E01","V111:E06"):
            return dict(text=body,mark=None)
        # 작은 inline 그림을 글자 사이에 두는 대신 원문 끝에 별도로 그린다.
        # 원문 자료 자체는 보존하며, 아직 얻지 않은 자료에 그림을 보태지 않는다.
        body=_r13_room_document_re.sub(r"\{image=[^{}]*\}","",body).strip()
        mark="assets/room13-acorn-ink-crooked.png" if record and key=="V111:E06" else None
        return dict(text=body,mark=mark)

    # 책상 서류로 정리한 가족 자료에 예전 열린 보따리 그림이 다시 나오지 않게 한다.
    _r13_room_documents_material_art=r13_material_art
    def r13_material_art(key):
        if key=="V111:E30" and r13_v111_active():
            return Transform("assets/evidence/D01_FAMILY_DRAWING.webp",xysize=(160,100),fit="contain",nearest=True)
        return _r13_room_documents_material_art(key)

    _r13_room_documents_evidence_art_path=r13_evidence_art_path
    def r13_evidence_art_path(key):
        if key=="V111:E30" and r13_v111_active():
            return "assets/evidence/D01_FAMILY_DRAWING.webp"
        return _r13_room_documents_evidence_art_path(key)

    # 구저장에 남은 물건 키는 보존하되, 없앤 주머니의 투명 클릭 영역은 노출하지 않는다.
    _r13_room_bundle_spec=ROOM13["objects"].get("room13",{}).get("family_bundle")
    if _r13_room_bundle_spec is not None:
        _r13_room_bundle_spec["retired_room_bundle"]=True
    _r13_room_documents_object_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec.get("retired_room_bundle") and r13_v111_active():return False
        return _r13_room_documents_object_visible(spec)
