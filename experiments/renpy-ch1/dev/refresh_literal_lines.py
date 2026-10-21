"""Refresh only the line numbers in the dynamic dialogue literal inventory and its review.

New-world scene edits move lines in the V1.1.1 day files. Every other field of
every row must stay identical; the review rows keep their decisions.
    python3 dev/refresh_literal_lines.py
"""
import json
from pathlib import Path
from audit_dynamic_dialogue import literal_inventory

OUT=Path(__file__).resolve().parents[1]/'docs/reviews/dialogue-beats'

def main():
    new=json.loads(json.dumps(literal_inventory()))
    path=OUT/'dynamic-literal-inventory.json';old=json.loads(path.read_text())
    assert len(new)==len(old),(len(new),len(old))
    strip=lambda r:{k:v for k,v in r.items() if k!='line'}
    for a,b in zip(new,old):assert strip(a)==strip(b),(a,b)
    path.write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
    review_path=OUT/'dynamic-context-review.json';review=json.loads(review_path.read_text());moved=0
    for i,row in enumerate(r for r in new if not r['already_static_text']):
        for table in ('rows','excluded_rows'):
            entry=review[table].get(str(i))
            if entry and entry['line']!=row['line']:entry['line']=row['line'];moved+=1
    review_path.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
    print('inventory rows',len(new),'review lines moved',moved)

if __name__=='__main__':main()
