"""검토 기록의 줄 번호만 다시 맞춘다 (2026-10-23).

검토 기록 두 곳이 대사 위치를 "파일:줄"로 들고 있다. 게임은 실행 중 줄 번호를 쓰지 않으므로
(대사 식별자·순번·문장으로 맞춘다) .rpy 에 줄을 더하면 시험만 깨진다. 지금 소스로 다시 계산한
목록과 저장된 목록을 항목별로 맞대어 **줄 번호 말고는 모두 같을 때만** 줄 번호를 고친다.
다른 칸이 하나라도 다르면 고치지 않고 멈춘다(사람이 다시 검토할 일이다).

  python3 dev/reanchor_lines.py          확인만
  python3 dev/reanchor_lines.py --write  고친다
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'dev'))


LINE_KEYS = ('line', 'source_line')


def same_but_line(a, b):
    return {k: v for k, v in a.items() if k not in LINE_KEYS} == {k: v for k, v in b.items() if k not in LINE_KEYS}


def check(name, fresh, stored):
    if len(fresh) != len(stored):
        sys.exit(f'{name}: 항목 수가 다르다({len(stored)} -> {len(fresh)}). 다시 검토해야 한다.')
    for a, b in zip(fresh, stored):
        if not same_but_line(a, b):
            sys.exit(f'{name}: 줄 번호 말고도 달라진 항목이 있다: {b} -> {a}')
    moved = sum(any(a.get(k) != b.get(k) for k in LINE_KEYS) for a, b in zip(fresh, stored))
    print(f'{name}: 줄 번호만 바뀐 항목 {moved}개')
    return moved


def main(write):
    from audit_dynamic_dialogue import literal_inventory
    path = ROOT / 'docs/reviews/dialogue-beats/dynamic-literal-inventory.json'
    fresh = json.loads(json.dumps(literal_inventory()))
    if check('대사 목록', fresh, json.loads(path.read_text())) and write:
        path.write_text(json.dumps(fresh, ensure_ascii=False, indent=2) + '\n')

    from import_resource_intake21 import reviewed_bindings, BATCH
    path = ROOT / 'game/assets/room13-dialogue-context-art.json'
    data = json.loads(path.read_text())
    stored = [c for c in data['bindings'] if c.get('batch') == BATCH]
    fresh = json.loads(json.dumps(reviewed_bindings()))
    if check('그림 연결(intake21)', fresh, stored) and write:
        it = iter(fresh)
        data['bindings'] = [next(it) if c.get('batch') == BATCH else c for c in data['bindings']]
        text = path.read_text()
        indent = 2 if text.startswith('{\n  ') else None
        path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + ('\n' if text.endswith('\n') else ''))


if __name__ == '__main__':
    main('--write' in sys.argv)
