# 장부 위에 겹친 큰 서류 지점이 장부의 클릭을 가로채지 않게 한다.
# 사각형·자료·진행 조건은 보존하고, 작은 장부의 입력 순서만 맨 위로 둔다.
init 363 python:
    def r13_gate_prioritize_ledger():
        objects=ROOM13["objects"].get("gate",{})
        if "ledger" not in objects:
            return
        objects["ledger"]=objects.pop("ledger")

    r13_gate_prioritize_ledger()
    # 옛 저장에 객체 사전이 들어 있어도 같은 순서를 복원한다.
    config.after_load_callbacks.append(r13_gate_prioritize_ledger)
