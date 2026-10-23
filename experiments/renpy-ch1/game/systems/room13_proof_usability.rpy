# 실제 플레이 검토 U01/U02/U07/U11: 표시 문맥만 정리한다. 자료·제출 판정은 그대로 둔다.
init 345 python:
    import re as _r13_source_re
    R13_SELF_COMPARE_PROOFS=("두 편지를 나란히 본다","두 편지의 초대를 대조한다")
    R13_BOOK_PURPOSE["compare"]=("비교에 추가","비교할 자료")

    def r13_book_ui_copy(purpose=None,chosen=(),hearing=False,target=None):
        count=len(chosen or ())
        if purpose in ("proof","compare"):
            compare=purpose=="compare"
            return dict(title="자료 비교" if compare else "근거 선택",
                note=("비교할 자료" if compare else "근거로 낼 자료")+" · 고른 자료 %d개"%count,
                help="자료를 골라도 아직 제출되지 않습니다. 선택을 마친 뒤 제출할 수 있습니다.",
                stop="선택 마치기 · %d개"%count)
        if purpose=="use":
            return dict(title="기록 꺼내기",note="꺼낼 기록",help="지금 살펴볼 기록을 고르세요.",stop="돌아가기")
        return dict(title="보여주기",note=(R13_NAMES.get(target,"상대")+"에게 보여줄 자료"),
            help=("이 발언에 제시할 자료를 고르세요." if hearing else "먼저 보여주고, 건넬지는 대화 후 결정합니다."),stop="돌아가기")

    def r13_proof_edit_help(chances=None):
        if chances:
            return "선택·추가·빼기는 기회를 쓰지 않습니다. 잘못된 제출은 기회를 1회 사용합니다."
        return "자료를 골라도 제출되지 않습니다. 「선택한 근거 제출」을 누르면 판정합니다."

    def r13_record_source_label(key):
        """원본 source ID를 저장한 채, 플레이 화면에는 획득 장소·사람만 표시한다."""
        state=getattr(store,"room13",None) or {}
        rec=state.get("records",{}).get(key) or {}
        source=str(rec.get("source") or "").strip()
        # 명시적으로 사람에게서 들은 증언만 사람 이름으로 쓴다.
        person=ROOM13.get("evidence_sources",{}).get(key)
        if person in R13_NAMES and (r13_catalog_record(key) or {}).get("kind")=="증언":
            return R13_NAMES[person]+"에게 들은 말"
        if source and not _r13_source_re.search(r"(?:MS\d+_|NW_|V111:|[A-Za-z_][A-Za-z0-9_]*:|^[A-Za-z0-9_./-]+$)",source):
            return source
        place=R13_PLACES.get(rec.get("place"))
        if place:
            return place[0]+" · "+r13_catalog_title(key)
        return "이번 여정에서 확인한 자료"
