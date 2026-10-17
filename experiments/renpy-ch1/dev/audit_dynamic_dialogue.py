"""Validate contextual review provenance; never infer emotion or enable artwork.

The literal inventory is a source extraction, not a reachable-state claim. Review
records use paths/lines and exact text. Composed runtime identities use a separate call-site binding registry; they
must not be replaced with a global text lookup.
"""
import ast
import collections
import hashlib
import json
import re
from pathlib import Path
import line_cues

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reviews/dialogue-beats'
FILES = ('dynamic-context-review.json', 'dynamic-expression-review.json',
         'dynamic-duplicate-review.json', 'opening-context-review.json',
         'supplemental-context-review.json', 'expanded-context-review.json', 'binding-additional-review.json')


def literal_inventory():
    people = json.loads((ROOT / 'game/assets/room13-fullbody-dialogue.json').read_text())['people']
    pairs = {(p[0], p[1]) for rows in line_cues.scene_rows().values() for p in rows}
    result = []
    for path in sorted((ROOT / 'game').rglob('*.rpy')):
        if not path.name.startswith('room13') or 'qa_tests' in path.parts:
            continue
        source = path.read_text()
        headers = list(re.finditer(r'^\s*(?:def |label |[A-Z][A-Z_0-9]*\s*=).*', source, re.M))
        for match in re.finditer(r'\(\s*(?:"[^"]+"|\x27[^\x27]+\x27|None)\s*,\s*["\x27]', source):
            end = line_cues._match_bracket(source, match.start())
            if end < 0:
                continue
            try:
                packet = ast.literal_eval(source[match.start():end + 1])
            except (ValueError, SyntaxError):
                continue
            if not isinstance(packet, tuple) or len(packet) < 2 or packet[0] not in set(people) | {None, 'dad'}:
                continue
            if not isinstance(packet[1], str) or not re.search('[가-힣]', packet[1]):
                continue
            if packet[1].startswith(('assets/', 'room13-')):
                continue
            context = next((h.group().strip() for h in reversed(headers) if h.start() < match.start()), 'file scope')
            result.append(dict(source=str(path.relative_to(ROOT)), line=source.count('\n', 0, match.start()) + 1,
                               context=context, person=packet[0], text=packet[1], packet=list(packet),
                               already_static_text=(packet[0], packet[1]) in pairs))
    return result


def review_rows(name):
    data = json.loads((OUT / name).read_text())['rows']
    return list(data.values()) if isinstance(data, dict) else data


def quoted_values(source):
    # Exact literal decoding also checks strings containing escaped quotes.
    for match in re.finditer(r'"(?:[^"\\]|\\.)*"|\x27(?:[^\x27\\]|\\.)*\x27', source):
        try:
            yield ast.literal_eval(match.group())
        except (ValueError, SyntaxError):
            pass


def provenance_errors():
    errors = []
    cache = {}
    for name in FILES:
        for i, row in enumerate(review_rows(name)):
            source = row['source']
            cache.setdefault(source, (ROOT / source).read_text())
            value = None
            if 'path' in row:
                value = json.loads(cache[source])
                for part in row['path']:
                    value = value[part]
                if isinstance(value, list):
                    value = value[1]
            else:
                snippet = cache[source]
                if 'line' in row:
                    snippet = '\n'.join(snippet.splitlines()[row['line'] - 1:row.get('end_line', row['line'])])
                if row['text'] not in {v for line in snippet.splitlines() for v in quoted_values(line)}:
                    errors.append([name, i, source, row.get('line'), 'text not at source'])
                continue
            if value != row['text']:
                errors.append([name, i, source, row.get('path'), 'JSON source mismatch'])
    return errors


def audit():
    inventory = literal_inventory()
    saved = json.loads((OUT / 'dynamic-literal-inventory.json').read_text())
    # JSON round trip normalizes nested tuple values before exact comparison.
    assert json.loads(json.dumps(inventory)) == saved, 'Source inventory changed; review new context first'
    unseen = [r for r in saved if not r['already_static_text']]
    review = json.loads((OUT / 'dynamic-context-review.json').read_text())
    pending = []
    for i, row in enumerate(unseen):
        if row['person'] in (None, 'dad'):
            continue
        entry = review['rows'].get(str(i)) or review['excluded_rows'].get(str(i))
        if not entry or any(entry[k] != row[k] for k in ('source', 'line', 'person', 'text', 'packet')):
            pending.append(dict(index=i, **row))
    errors = provenance_errors()
    summary = dict(source_literal_occurrences=len(saved), non_static_literal_occurrences=len(unseen),
                   non_static_npc_occurrences=sum(r['person'] not in (None, 'dad') for r in unseen),
                   literal_context_reviewed=len(review['rows']), explicit_exclusions=len(review['excluded_rows']),
                   literal_context_pending=len(pending), provenance_errors=errors,
                   review_record_counts={name: len(review_rows(name)) for name in FILES},
                   runtime_assets_active=0, dynamic_runtime_binding='118_local_callsite_snapshots_assets_held',
                   count_note='Counts are source occurrences/components, not unique or reachable runtime lines. Files overlap intentionally; expression fragments are not standalone dialogue.',
                   scope='Room13 r13_lines: static scenes, init-added literal topics, calendar JSON, activities, variable speaker responses, meeting statements/opinions, greetings, presentations and silence. Other winter_* campaigns are outside this renderer.')
    (OUT / 'dynamic-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'dynamic-pending.json').write_text(json.dumps(pending, ensure_ascii=False, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
